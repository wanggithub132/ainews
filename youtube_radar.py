#!/usr/bin/env python
"""YouTube 关键词雷达 -> 企业微信每日推送

每天按固定关键词搜索 YouTube（按上传日期排序，最新优先），
套用 parse_youtube.qualifies() 过滤出符合条件的 Running Man 二创视频，
与 pushed_videos.json 去重后取前 N 条，以图文卡片（带封面图）推送到
企业微信群机器人，并把已推送的视频记录回 pushed_videos.json。

设计要点：
  - 运行环境为 GitHub Actions（海外直连 YouTube，无需代理；
    parse_youtube.detect_proxy 在 Linux 上会自然返回 None 直连）
  - 去重状态 pushed_videos.json 由 workflow 在运行后 commit 回仓库
  - 本地调试可用 --dry-run，只打印不发送、不写状态

用法：
    WEIXIN_WEBHOOK_KEY=xxx python youtube_radar.py     # 正式推送
    python youtube_radar.py --dry-run                  # 本地试跑
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from parse_youtube import search_youtube, qualifies

# 每日推送上限（企业微信 news 卡片单条消息最多 8 篇，取 5）
MAX_PUSH = 5

# 关键词清单（Running Man 二创向，控制数量以缩短 Actions 运行时间）
QUERIES = [
    'runningman 名场面',
    'runningman 中文解说',
    'running man 爆笑 合集',
    'runningman 搞笑 中字',
    'running man 混剪 中文',
    'runningman 一口气看完',
]

# 按上传日期排序（最新优先）的 sp 参数
SP_NEWEST = 'CAI%253D'

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'pushed_videos.json')
STATE_CAP = 5000  # 状态文件最多记录条数，防止无限膨胀


def load_state():
    """读取已推送视频 URL 集合。"""
    if not os.path.exists(STATE_FILE):
        return []
    try:
        with open(STATE_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"读取状态文件失败（将视为空）: {e}")
        return []


def save_state(urls):
    """写回已推送 URL 列表（保留最近 STATE_CAP 条）。"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(urls[-STATE_CAP:], f, ensure_ascii=False, indent=0)


def find_new_videos(pushed):
    """搜索并返回未推送过的合格视频（按发现顺序）。"""
    pushed_set = set(pushed)
    fresh, seen = [], set()
    for q in QUERIES:
        try:
            vids = search_youtube(q, max_items=60, sp=SP_NEWEST)
        except Exception as e:
            print(f"  搜索失败 [{q}]: {e}")
            continue
        for v in vids:
            url = v.get('url', '')
            if not url or url in seen or url in pushed_set:
                continue
            seen.add(url)
            if qualifies(v):
                fresh.append(v)
        if len(fresh) >= MAX_PUSH * 3:  # 候选够多就提前收手
            break
    return fresh


def send_to_weixin(videos, webhook_key):
    """把视频列表推成企业微信图文卡片（带封面图）。"""
    import requests
    webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    beijing_now = datetime.now(timezone(timedelta(hours=8)))
    articles = []
    for v in videos:
        articles.append({
            'title': v['title'][:128],
            'description': f"时长 {v['duration']} | RunningMan 二创精选 "
                           f"{beijing_now.strftime('%m-%d')}",
            'url': v['url'],
            'picurl': v.get('thumbnail', ''),
        })
    payload = {'msgtype': 'news', 'news': {'articles': articles}}
    resp = requests.post(webhook_url, json=payload, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    if result.get('errcode') == 0:
        print(f"✅ 已推送 {len(articles)} 条到企业微信")
        return True
    print(f"❌ 企业微信返回错误: {result.get('errmsg')}")
    return False


def main():
    dry_run = '--dry-run' in sys.argv
    print("=" * 60)
    print("YouTube RunningMan 二创雷达", "(dry-run)" if dry_run else "")
    print("=" * 60)

    pushed = load_state()
    print(f"历史已推送: {len(pushed)} 条")

    fresh = find_new_videos(pushed)
    print(f"\n本次发现新视频: {len(fresh)} 条")
    to_push = fresh[:MAX_PUSH]
    for i, v in enumerate(to_push, 1):
        print(f"  [{i}] {v['title'][:60]}  ({v['duration']})")

    if not to_push:
        print("今日无新视频，跳过推送")
        return True

    if dry_run:
        print("\n[dry-run] 不发送、不写状态")
        return True

    webhook_key = os.getenv('WEIXIN_WEBHOOK_KEY')
    if not webhook_key:
        print("❌ 未设置 WEIXIN_WEBHOOK_KEY 环境变量")
        return False

    ok = send_to_weixin(to_push, webhook_key)
    if ok:
        pushed.extend(v['url'] for v in to_push)
        save_state(pushed)
        print(f"状态已更新: {STATE_FILE}")
    return ok


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
