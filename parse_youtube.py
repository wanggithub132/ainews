"""YouTube 视频信息提取工具

从 YouTube 提取视频信息（标题 / 链接 / 时长 / 缩略图），支持四种模式。
底层：curl_cffi 模拟 Chrome 指纹 + 自动检测系统代理（自由猫 127.0.0.1:7892）
+ InnerTube API（browse / search）翻页。结果保存到用户 Downloads 目录。

============================ 使用示例 ============================

1) collect —— 聚合符合条件的 Running Man 二次创作视频（主力模式）
   先用多关键词搜索发现频道，再逐频道翻页补足，套用 qualifies() 精筛：
   中文标题 + 韩国 Running Man + 二次创作特征 + 时长 2~20 分钟，
   并排除电影影评、中国版《奔跑吧》。支持断点续爬（重跑只补差额）。
       python parse_youtube.py collect          # 默认目标 500 条
       python parse_youtube.py collect 300      # 自定义目标数量
   输出：Downloads/runningman_500.json / runningman_500.csv

2) channel —— 直接爬取【指定频道】的全部视频（不做任何内容过滤）
   适合“我明确知道就是这个博主”的场景，博主发什么就爬什么。
   三种链接形式都支持（会自动补 /videos）：
       python parse_youtube.py channel https://www.youtube.com/@频道名
       python parse_youtube.py channel https://www.youtube.com/@频道名/videos
       python parse_youtube.py channel https://www.youtube.com/channel/UCxxxxxxxx
   输出：Downloads/youtube_<频道名>.json / .csv

3) search —— 单关键词搜索并翻页（不过滤，返回搜索到的视频）
       python parse_youtube.py search "拳击 KO 集锦"
   输出：Downloads/youtube_search.json / .csv

4) playlist —— 解析本地已保存的播放列表 JSON（离线）
       python parse_youtube.py playlist yt_data.json            # 全部
       python parse_youtube.py playlist yt_data.json 关键词     # 按标题关键词过滤
   输出：Downloads/youtube_playlist.json / .csv

注意：需开启代理（自由猫等）才能访问 YouTube；脚本会自动检测系统代理。
=================================================================
"""
import json
import csv
import os
import re
import sys
import io

# 统一输出编码为 UTF-8，避免 Windows GBK 终端/重定向时打印韩文、emoji 崩溃
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

try:
    from curl_cffi import requests as cffi_requests
    HAS_CFFI = True
except ImportError:
    HAS_CFFI = False
    import urllib.request

DOWNLOADS = os.path.join(os.environ.get('USERPROFILE', os.path.expanduser('~')), 'Downloads')


def detect_proxy():
    """自动检测系统代理。优先读 Windows 代理设置，其次探测常见本地代理端口。"""
    # 1) 读取 Windows 系统代理
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
        enable, _ = winreg.QueryValueEx(key, 'ProxyEnable')
        if enable:
            server, _ = winreg.QueryValueEx(key, 'ProxyServer')
            winreg.CloseKey(key)
            if server and '=' not in server:  # 形如 127.0.0.1:7892
                return f'http://{server}'
        else:
            winreg.CloseKey(key)
    except Exception:
        pass

    # 2) 探测常见本地代理端口（自由猫/Clash 等）
    import socket
    for port in (7892, 7890, 7891, 10809, 1080):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        try:
            if s.connect_ex(('127.0.0.1', port)) == 0:
                s.close()
                return f'http://127.0.0.1:{port}'
        except Exception:
            pass
        finally:
            s.close()
    return None


PROXY = detect_proxy()


# ---------------------------------------------------------------------------
# 通用：从 lockupViewModel 提取单条视频
# ---------------------------------------------------------------------------
def extract_lockup_video(lockup):
    """从 lockupViewModel 中提取 标题/链接/时长/缩略图。"""
    try:
        vid = lockup.get('contentId', '')
        if not vid:
            vid = lockup.get('rendererContext', {}).get('commandContext', {})\
                .get('onTap', {}).get('innertubeCommand', {})\
                .get('watchEndpoint', {}).get('videoId', '')

        # 标题
        meta = lockup.get('metadata', {}).get('lockupMetadataViewModel', {})
        title_data = meta.get('title', {})
        title = title_data.get('content', '') if isinstance(title_data, dict) else str(title_data)

        # 缩略图
        thumb_vm = lockup.get('contentImage', {}).get('thumbnailViewModel', {})
        thumbnails = thumb_vm.get('image', {}).get('sources', [])
        thumbnail_url = ''
        if thumbnails:
            thumbnail_url = max(thumbnails, key=lambda x: x.get('width', 0)).get('url', '')

        # 时长 - 从 thumbnailBadge / overlay 中提取
        duration = find_duration(thumb_vm)

        if vid and title:
            return {
                'title': title,
                'url': f'https://www.youtube.com/watch?v={vid}',
                'duration': duration,
                'thumbnail': thumbnail_url,
            }
    except Exception:
        pass
    return None


def find_duration(obj):
    """递归查找形如 12:34 的时长文本。"""
    if isinstance(obj, dict):
        # thumbnailBadgeViewModel.text 通常就是时长
        for k, v in obj.items():
            if isinstance(v, str):
                if re.fullmatch(r'\d{1,2}(:\d{2}){1,2}', v.strip()):
                    return v.strip()
            else:
                r = find_duration(v)
                if r:
                    return r
    elif isinstance(obj, list):
        for i in obj:
            r = find_duration(i)
            if r:
                return r
    return ''


# ---------------------------------------------------------------------------
# 通用：递归提取所有 videoRenderer / lockupViewModel
# ---------------------------------------------------------------------------
def collect_videos(obj, videos, seen):
    """递归遍历任意 JSON，收集所有视频。"""
    if isinstance(obj, dict):
        if 'lockupViewModel' in obj:
            v = extract_lockup_video(obj['lockupViewModel'])
            if v and v['url'] not in seen:
                seen.add(v['url'])
                videos.append(v)
        if 'videoRenderer' in obj:
            v = extract_video_renderer(obj['videoRenderer'])
            if v and v['url'] not in seen:
                seen.add(v['url'])
                videos.append(v)
        for val in obj.values():
            collect_videos(val, videos, seen)
    elif isinstance(obj, list):
        for i in obj:
            collect_videos(i, videos, seen)


def extract_video_renderer(r):
    """从旧版 videoRenderer 提取视频信息（含所属频道）。"""
    try:
        vid = r.get('videoId', '')
        title_runs = r.get('title', {}).get('runs', [])
        title = ''.join(run.get('text', '') for run in title_runs)
        if not title:
            title = r.get('title', {}).get('simpleText', '')
        duration = r.get('lengthText', {}).get('simpleText', '')
        thumbs = r.get('thumbnail', {}).get('thumbnails', [])
        thumbnail_url = max(thumbs, key=lambda x: x.get('width', 0)).get('url', '') if thumbs else ''

        # 所属频道
        channel_name, channel_id = '', ''
        byline = r.get('ownerText', {}).get('runs', []) or r.get('longBylineText', {}).get('runs', [])
        if byline:
            channel_name = byline[0].get('text', '')
            channel_id = byline[0].get('navigationEndpoint', {})\
                .get('browseEndpoint', {}).get('browseId', '')

        if vid and title:
            return {
                'title': title,
                'url': f'https://www.youtube.com/watch?v={vid}',
                'duration': duration,
                'thumbnail': thumbnail_url,
                'channel': channel_name,
                'channelId': channel_id,
            }
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# 网络请求
# ---------------------------------------------------------------------------
def http_get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    proxies = {'http': PROXY, 'https': PROXY} if PROXY else None
    if HAS_CFFI:
        s = cffi_requests.Session(impersonate='chrome')
        return s.get(url, headers=headers, timeout=30, proxies=proxies).text
    if PROXY:
        handler = urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})
        opener = urllib.request.build_opener(handler)
        req = urllib.request.Request(url, headers=headers)
        return opener.open(req, timeout=30).read().decode('utf-8', 'replace')
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')


def http_post_json(url, payload):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    body = json.dumps(payload).encode('utf-8')
    proxies = {'http': PROXY, 'https': PROXY} if PROXY else None
    if HAS_CFFI:
        s = cffi_requests.Session(impersonate='chrome')
        return s.post(url, headers=headers, data=body, timeout=30, proxies=proxies).json()
    if PROXY:
        handler = urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})
        opener = urllib.request.build_opener(handler)
        req = urllib.request.Request(url, data=body, headers=headers, method='POST')
        return json.loads(opener.open(req, timeout=30).read().decode('utf-8', 'replace'))
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace'))


# ---------------------------------------------------------------------------
# 频道视频爬取（含 InnerTube API 翻页）
# ---------------------------------------------------------------------------
def scrape_channel(channel_url, on_page=None, max_pages=200):
    """爬取频道 /videos 页面的视频。

    on_page: 可选回调 on_page(new_videos_this_page) -> bool，返回 True 则提前停止。
    max_pages: 翻页上限（collect 场景可传较小值避免超大频道拖慢）。
    """
    if not channel_url.rstrip('/').endswith('/videos'):
        channel_url = channel_url.rstrip('/') + '/videos'

    print(f"正在请求频道页: {channel_url}", flush=True)
    html = http_get(channel_url)

    # 提取 ytInitialData
    m = re.search(r'var ytInitialData = ({.*?});</script>', html)
    if not m:
        m = re.search(r'ytInitialData"\]\s*=\s*({.*?});', html)
    if not m:
        print("未找到 ytInitialData")
        return []
    data = json.loads(m.group(1))

    # 提取 InnerTube 配置
    api_key = _search(html, r'"INNERTUBE_API_KEY":"([^"]+)"')
    client_version = _search(html, r'"INNERTUBE_CONTEXT_CLIENT_VERSION":"([^"]+)"') or '2.20240101.00.00'
    visitor_data = _search(html, r'"visitorData":"([^"]+)"')

    videos = []
    seen = set()
    page_videos = []
    collect_videos(data, page_videos, seen)
    videos.extend(page_videos)
    if on_page and page_videos and on_page(page_videos):
        return videos

    # 找 continuation token
    token = _find_continuation(data)

    # 循环翻页
    page = 1
    while token and api_key:
        page += 1
        payload = {
            'context': {
                'client': {
                    'clientName': 'WEB',
                    'clientVersion': client_version,
                    'visitorData': visitor_data,
                }
            },
            'continuation': token,
        }
        api_url = f'https://www.youtube.com/youtubei/v1/browse?key={api_key}&prettyPrint=false'
        try:
            resp = http_post_json(api_url, payload)
        except Exception as e:
            print(f"翻页请求失败: {e}")
            break

        page_videos = []
        before_seen = len(seen)
        collect_videos(resp, page_videos, seen)
        videos.extend(page_videos)
        token = _find_continuation(resp)

        if on_page and page_videos and on_page(page_videos):
            break
        if len(seen) == before_seen:
            # 没有新增，结束
            break
        if page > max_pages:
            break

    return videos


def _search(text, pattern):
    m = re.search(pattern, text)
    return m.group(1) if m else ''


def _find_continuation(obj):
    """递归查找 continuation token。"""
    if isinstance(obj, dict):
        if 'continuationItemRenderer' in obj:
            token = obj['continuationItemRenderer'].get('continuationEndpoint', {})\
                .get('continuationCommand', {}).get('token', '')
            if token:
                return token
        for v in obj.values():
            r = _find_continuation(v)
            if r:
                return r
    elif isinstance(obj, list):
        for i in obj:
            r = _find_continuation(i)
            if r:
                return r
    return None


# ---------------------------------------------------------------------------
# YouTube 搜索（InnerTube search API + 翻页）
# ---------------------------------------------------------------------------
def _get_innertube_config(html):
    api_key = _search(html, r'"INNERTUBE_API_KEY":"([^"]+)"')
    client_version = _search(html, r'"INNERTUBE_CONTEXT_CLIENT_VERSION":"([^"]+)"') or '2.20240101.00.00'
    visitor_data = _search(html, r'"visitorData":"([^"]+)"')
    return api_key, client_version, visitor_data


def _extract_initial_data(html):
    m = re.search(r'var ytInitialData = ({.*?});</script>', html)
    if not m:
        m = re.search(r'ytInitialData"\]\s*=\s*({.*?});', html)
    return json.loads(m.group(1)) if m else None


def search_youtube(query, max_items=400, sp=None):
    """搜索 YouTube 并翻页，返回视频列表（含频道信息）。

    sp: 可选搜索过滤/排序参数，如 'CAI%253D' 表示按上传日期排序（最新优先）。
    """
    import urllib.parse
    q = urllib.parse.quote(query)
    url = f'https://www.youtube.com/results?search_query={q}&hl=zh-CN&gl=HK'
    if sp:
        url += f'&sp={sp}'
    print(f"  搜索: {query}")
    try:
        html = http_get(url)
    except Exception as e:
        print(f"  搜索请求失败: {e}")
        return []

    data = _extract_initial_data(html)
    if not data:
        return []
    api_key, client_version, visitor_data = _get_innertube_config(html)

    videos, seen = [], set()
    collect_videos(data, videos, seen)
    token = _find_continuation(data)

    page = 1
    while token and api_key and len(videos) < max_items:
        page += 1
        payload = {
            'context': {'client': {
                'clientName': 'WEB', 'clientVersion': client_version,
                'visitorData': visitor_data, 'hl': 'zh-CN', 'gl': 'HK'}},
            'continuation': token,
        }
        api_url = f'https://www.youtube.com/youtubei/v1/search?key={api_key}&prettyPrint=false'
        try:
            resp = http_post_json(api_url, payload)
        except Exception:
            break
        before = len(videos)
        collect_videos(resp, videos, seen)
        token = _find_continuation(resp)
        if len(videos) == before:
            break
        if page > 30:
            break
    return videos


# ---------------------------------------------------------------------------
# 过滤：中文 + RunningMan + 二次创作特征
# ---------------------------------------------------------------------------
CJK = re.compile(r'[\u4e00-\u9fff]')

# 二次创作/解说/剪辑类特征词
EDIT_KEYWORDS = [
    '解说', '盘点', '名场面', '合集', '一口气', '看完', '爆笑', '恶搞', '混剪',
    '高能', '名场面', '搞笑', '名场', '名嘴', '整活', '名局', '经典', '回顾',
    '剪辑', '名梗', '名段', '名瞬间', '名画面', '名桥段', '名片段', '名场景',
    '笑翻', '笑死', '名场合', '故事', '第几集', '这一期', '这期', '那一期',
]

# RunningMan 相关标志（强标志，直接命中即认定；“跑男”歧义大已移除，避免命中中国版）
RM_MARKERS = ['running man', 'runningman', '런닝맨', 'rm家族', 'rm成员']
# RunningMan 成员名（增强判定，去除“哈哈/gary”等易误伤的宽泛词）
RM_MEMBERS = ['刘在石', '劉在錫', '李光洙', '李光珠', '金钟国', '金鐘國',
              '宋智孝', '池石镇', '池石鎮', '全烒烒', '全昭旻', '梁世灿', '梁世燦']
# 词边界匹配的缩写标志（避免 lingorm / form 等误伤）
RM_WORD = re.compile(r'(?<![a-z])rm(?![a-z])')


def has_chinese(text):
    return bool(CJK.search(text))


def is_running_man(title):
    t = title.lower()
    if any(m in t for m in RM_MARKERS):
        return True
    if RM_WORD.search(t):
        return True
    return any(m.lower() in t for m in RM_MEMBERS)


def looks_secondary(title):
    """标题是否具备二次创作特征。"""
    if any(k in title for k in EDIT_KEYWORDS):
        return True
    # 含多个 hashtag 也是二次创作常见特征
    if title.count('#') >= 2:
        return True
    return False


# 负向排除：电影《The Running Man（猎杀游戏）》影评、中国版《奔跑吧》等非韩综内容
# （小写匹配，英文词用小写）
EXCLUDE_KEYWORDS = [
    # 电影影评类
    '电影解说', '影评', '猎杀游戏', '反乌托邦', '生存游戏', '神作',
    # 中国版《奔跑吧（兄弟）》
    '奔跑吧', '奔跑吧兄弟', 'keep running', 'keeprunning', '跑男',
    # 中国版常驻/常见嘉宾
    '邓超', '鄧超', '李晨', '郑恺', '鄭愷', '杨颖', 'angelababy', '鹿晗',
    '陈赫', '陳赫', '王祖蓝', '王祖藍', '蔡徐坤', '白鹿', '周深',
    '沙溢', '范丞丞', '宋雨琦',
]


def duration_ok(duration):
    """时长合规：2 分钟 <= 时长 <= 20 分钟（无时长视为不合规）。"""
    if not duration:
        return False
    parts = duration.strip().split(':')
    try:
        parts = [int(p) for p in parts]
    except ValueError:
        return False
    if len(parts) == 2:
        secs = parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        secs = parts[0] * 3600 + parts[1] * 60 + parts[2]
    else:
        return False
    return 120 <= secs <= 1200


def qualifies(video):
    """综合判定：中文标题 + 韩综 RunningMan + 二次创作特征 + 时长合规，
    且排除电影影评与中国版《奔跑吧》。"""
    title = video.get('title', '')
    if not has_chinese(title):
        return False
    tl = title.lower()
    if any(k in tl for k in EXCLUDE_KEYWORDS):
        return False
    if not is_running_man(title):
        return False
    if not looks_secondary(title):
        return False
    return duration_ok(video.get('duration', ''))


# ---------------------------------------------------------------------------
# 编排：搜索发现频道 -> 爬取整频道 -> 过滤聚合到目标数量
# ---------------------------------------------------------------------------
SEARCH_QUERIES = [
    'runningman 中文解说', 'running man 盘点', 'runningman 名场面 中文',
    'running man 爆笑 合集', 'runningman 一口气看完', 'running man 混剪 中文',
    'runningman 李光洙 名场面', 'runningman 金钟国 搞笑',
    'running man 刘在石 名场面', 'runningman 宋智孝 名场面',
    'running man 中文字幕 剪辑', 'runningman 经典 回顾 中文',
    'running man 名场面 合集 中文',
    # 补充：面向短片二创的更多入口
    'runningman 名场面', 'runningman 搞笑 中字', 'running man 高能',
    'runningman 解说', 'runningman 爆笑名场面', '런닝맨 中文字幕',
    'runningman 中字 合集', 'running man 金钟国 名场面',
    'runningman 李光洙 搞笑', 'running man 宋智孝 搞笑',
    'runningman 池石镇', 'runningman 梁世灿 搞笑',
    'running man 全昭旻 名场面', 'running man 经典 名场面',
]


def collect_target(target=500):
    """搜索发现频道并爬取，聚合符合条件的视频到目标数量。

    支持断点续爬：若已存在 runningman_500.json，先加载已有（并用新
    过滤器重新校验，剔除旧误判），再回补到 target。
    """
    all_videos, seen = [], set()
    channel_ids, channel_order = set(), []

    def _log(msg):
        print(msg, flush=True)

    # 断点续爬：加载已有结果，用新过滤器重新校验
    existing_path = os.path.join(DOWNLOADS, 'runningman_500.json')
    if os.path.exists(existing_path):
        try:
            old = json.load(open(existing_path, encoding='utf-8'))
            kept = 0
            for v in old:
                if qualifies(v) and v.get('url') and v['url'] not in seen:
                    seen.add(v['url'])
                    all_videos.append(v)
                    kept += 1
            _log(f"断点续爬：已有 {len(old)} 条，新过滤器保留 {kept} 条")
        except Exception as e:
            _log(f"加载已有结果失败，重新开始: {e}")

    # 阶段一：搜索，直接收集符合条件的视频 + 发现频道
    _log("=== 阶段一：搜索发现 ===")
    for q in SEARCH_QUERIES:
        vids = search_youtube(q, max_items=120)
        for v in vids:
            cid = v.get('channelId', '')
            if cid and cid.startswith('UC') and cid not in channel_ids:
                channel_ids.add(cid)
                channel_order.append(cid)
            if qualifies(v) and v['url'] not in seen:
                seen.add(v['url'])
                all_videos.append(v)
        save_results(all_videos, 'runningman_500')  # 增量保存
        _log(f"  累计符合条件: {len(all_videos)}，已发现频道: {len(channel_order)}")
        if len(all_videos) >= target:
            break

    # 阶段二：爬取发现的频道，补足数量
    if len(all_videos) < target:
        _log(f"\n=== 阶段二：爬取 {len(channel_order)} 个频道补足 ===")
        for cid in channel_order:
            if len(all_videos) >= target:
                break
            ch_url = f'https://www.youtube.com/channel/{cid}/videos'

            def on_page(page_videos):
                added_now = 0
                for v in page_videos:
                    if qualifies(v) and v['url'] not in seen:
                        seen.add(v['url'])
                        all_videos.append(v)
                        added_now += 1
                if added_now:
                    save_results(all_videos, 'runningman_500')  # 增量保存
                return len(all_videos) >= target  # 达标即停

            try:
                # 每个频道最多翻 40 页，避免超大频道拖慢整体
                scrape_channel(ch_url, on_page=on_page, max_pages=40)
            except Exception as e:
                _log(f"  频道 {cid} 爬取失败: {e}")
                continue
            _log(f"  频道 {cid}: 累计 {len(all_videos)}")

    return all_videos[:target]



def parse_playlist(json_path, keyword=None):
    with open(json_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    videos = []
    seen = set()
    collect_videos(data, videos, seen)
    if keyword:
        videos = [v for v in videos if keyword.lower() in v['title'].lower()]
    return videos


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------
def _write_csv(videos, output_csv):
    """写 CSV；若目标被 Excel 等占用，退而写入 *_new.csv 避免中断。"""
    for path in (output_csv, output_csv.replace('.csv', '_new.csv')):
        try:
            with open(path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['title', 'url', 'duration', 'thumbnail'],
                                        extrasaction='ignore')
                writer.writeheader()
                writer.writerows(videos)
            return path
        except PermissionError:
            continue
    return None


def save_results(videos, name):
    """静默写入 JSON + CSV（不打印，供增量保存调用）。"""
    output_json = os.path.join(DOWNLOADS, f'{name}.json')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    _write_csv(videos, os.path.join(DOWNLOADS, f'{name}.csv'))


def save_and_print(videos, name):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print(f"\n共提取 {len(videos)} 个视频")
    print("=" * 80)
    for i, v in enumerate(videos, 1):
        print(f"\n[{i}] {v['title'][:80]}")
        print(f"    链接:   {v['url']}")
        print(f"    时长:   {v['duration']}")
        print(f"    缩略图: {v['thumbnail'][:80]}")

    output_json = os.path.join(DOWNLOADS, f'{name}.json')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    print(f"\nJSON 已保存: {output_json}")

    csv_path = _write_csv(videos, os.path.join(DOWNLOADS, f'{name}.csv'))
    if csv_path:
        print(f"CSV 已保存: {csv_path}")
    else:
        print("CSV 保存失败（文件被占用），请关闭 Excel 后重试")


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python parse_youtube.py collect [目标数量]   # 爬取符合条件的 RunningMan 二次创作视频")
        print("  python parse_youtube.py channel https://www.youtube.com/@频道名")
        print("  python parse_youtube.py search <关键词>")
        print("  python parse_youtube.py playlist <yt_data.json> [关键词]")
        return

    mode = sys.argv[1]

    if mode == 'collect':
        target = int(sys.argv[2]) if len(sys.argv) > 2 else 500
        videos = collect_target(target)
        save_and_print(videos, 'runningman_500')

    elif mode == 'search':
        if len(sys.argv) < 3:
            print("请提供搜索关键词")
            return
        videos = search_youtube(sys.argv[2], max_items=200)
        save_and_print(videos, 'youtube_search')

    elif mode == 'channel':
        if len(sys.argv) < 3:
            print("请提供频道 URL")
            return
        channel_url = sys.argv[2]
        # 从 URL 提取频道名做文件名
        name_m = re.search(r'@([\w.-]+)', channel_url)
        name = f"youtube_{name_m.group(1)}" if name_m else "youtube_channel"
        videos = scrape_channel(channel_url)
        save_and_print(videos, name)

    elif mode == 'playlist':
        json_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(DOWNLOADS, 'yt_data.json')
        keyword = sys.argv[3] if len(sys.argv) > 3 else None
        if keyword and keyword.lower() == 'all':
            keyword = None
        videos = parse_playlist(json_path, keyword)
        save_and_print(videos, 'youtube_playlist')

    else:
        print(f"未知模式: {mode}")


if __name__ == '__main__':
    main()
