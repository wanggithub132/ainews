"""解析 HTML 页面，提取视频列表信息（播放地址、标题、图片地址）

支持两种输入方式:
  1. 本地 HTML 文件路径
  2. 网页 URL 地址（自动下载后解析）

用法:
  python parse_videos.py                          # 默认解析桌面文件
  python parse_videos.py "c:\\path\\to\\file.html"  # 指定本地文件
  python parse_videos.py "https://example.com"     # 指定网页地址
"""
import re
import json
import sys
import os


def crawl_page(url):
    """爬虫方式获取网页内容（仅在内存中，不保存文件）。

    使用 curl_cffi 模拟浏览器 TLS 指纹，可绕过 Cloudflare 等反爬。

    Args:
        url: 网页地址

    Returns:
        str: HTML 文本内容（仅存在于内存）
    """
    from curl_cffi import requests as cffi_requests

    print(f"正在请求页面: {url}")

    # curl_cffi 模拟浏览器 TLS 指纹，依次尝试有效的指纹
    for browser in ["chrome", "chrome119", "safari"]:
        session = cffi_requests.Session(impersonate=browser)
        response = session.get(url, timeout=30, allow_redirects=True)
        if response.status_code == 200:
            break
        print(f"{browser} 被拦截({response.status_code})，尝试下一个...")

    if response.status_code != 200:
        raise Exception(
            f"请求失败: {response.status_code} {response.reason}\n"
            f"该网站可能有较强的反爬保护，建议手动保存网页后用本地文件模式解析"
        )

    # 尝试自动检测编码
    text = response.text
    if not text or len(text) < 100:
        # 可能编码有问题，尝试用 content 解码
        for enc in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
            try:
                text = response.content.decode(enc)
                if len(text) > 100:
                    break
            except (UnicodeDecodeError, AttributeError):
                continue

    print(f"请求成功，页面大小: {len(text)} 字符（内存中，未写入文件）")
    return text


def parse_video_list(source):
    """从 HTML 内容中提取所有视频条目信息。

    Args:
        source: HTML 文本内容（str）

    Returns:
        list[dict]: 每条包含 url, title, image, duration, author, views
    """
    html = source

    videos = []

    # 按 video-elem 块拆分
    blocks = re.split(r'<div class="video-elem[^"]*">', html)

    for block in blocks[1:]:  # 跳过第一个空块
        video = {}

        # 1. 提取播放地址和缩略图（来自 display 区域的 <a>）
        display_match = re.search(
            r'<a[^>]*class="display[^"]*"[^>]*href="([^"]+)"', block)
        if display_match:
            video['url'] = display_match.group(1)

        # 2. 提取缩略图 URL（background-image: url(...)）
        img_match = re.search(
            r'background-image:\s*url\([&#39;\'"]*([^)\'"&#\s]+)[&#39;\'"]*\)', block)
        if img_match:
            img_url = img_match.group(1)
            # 清理 HTML 实体
            img_url = img_url.replace('&#39;', '').replace('&amp;', '&')
            # 补全协议头（处理 // 开头的地址）
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            video['image'] = img_url
        else:
            video['image'] = ''

        # 3. 提取视频时长
        duration_match = re.search(
            r'<small class="layer">\s*([\d:]+)\s*</small>', block)
        if duration_match:
            video['duration'] = duration_match.group(1).strip()
        else:
            video['duration'] = ''

        # 4. 提取视频标题（class="title" 的 <a> 标签文字）
        title_match = re.search(
            r'<a[^>]*class="title[^"]*"[^>]*>(.*?)</a>', block, re.DOTALL)
        if title_match:
            # 清理 HTML 标签
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            # 解码 HTML 实体
            import html as html_module
            title = html_module.unescape(title)
            video['title'] = title
        else:
            video['title'] = ''

        # 5. 提取作者
        author_match = re.search(
            r'作者:\s*<a[^>]*>(.*?)</a>', block, re.DOTALL)
        if author_match:
            video['author'] = re.sub(r'<[^>]+>', '', author_match.group(1)).strip()
        else:
            # 可能是纯文字格式 "作者: xxx"
            author_match2 = re.search(r'作者:\s*(\S+)', block)
            video['author'] = author_match2.group(1).strip() if author_match2 else ''

        # 6. 提取播放次数
        views_match = re.search(
            r'([\d.]+万次?播放|\d+次播放)', block)
        if views_match:
            video['views'] = views_match.group(1)
        else:
            video['views'] = ''

        # 只保留有标题的条目（过滤掉纯广告块）
        if video.get('title'):
            videos.append(video)

    return videos


def is_url(s):
    """判断字符串是否为 URL 地址。"""
    return s.startswith('http://') or s.startswith('https://')


def main():
    if len(sys.argv) > 1:
        input_arg = sys.argv[1]
    else:
        # input_arg = r'c:\Users\Lenovo\Desktop\净化.html'
        input_arg = r'https://baidu.com'

    # 根据输入类型获取 HTML 内容
    if is_url(input_arg):
        html = crawl_page(input_arg)
        output_name = 'web_videos'
    else:
        with open(input_arg, 'r', encoding='utf-8') as f:
            html = f.read()
        # 从文件路径生成输出名
        output_name = os.path.splitext(os.path.basename(input_arg))[0] + '_videos'

    videos = parse_video_list(html)

    # 格式化输出
    print(f"共提取到 {len(videos)} 个视频条目\n")
    print("=" * 70)

    for i, v in enumerate(videos, 1):
        print(f"\n[{i}] {v['title']}")
        print(f"    播放地址: {v['url']}")
        print(f"    图片地址: {v['image']}")
        if v['duration']:
            print(f"    时长:     {v['duration']}")
        if v['author']:
            print(f"    作者:     {v['author']}")
        if v['views']:
            print(f"    播放量:   {v['views']}")
        print("-" * 70)

    # # 输出 JSON 文件到当前目录
    # json_path = output_name + '.json'
    # with open(json_path, 'w', encoding='utf-8') as f:
    #     json.dump(videos, f, ensure_ascii=False, indent=2)
    # print(f"\nJSON 已保存: {os.path.abspath(json_path)}")


if __name__ == '__main__':
    main()
