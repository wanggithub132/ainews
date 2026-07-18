#!/usr/bin/env python
"""
Interactive project testing utility.
展示 AiNews 项目的功能和数据流
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_banner(text, width=70):
    """打印格式化的横幅"""
    print(f"\n{'='*width}")
    print(f"  {text}")
    print(f"{'='*width}\n")

def print_section(title, symbol="📋"):
    """打印章节标题"""
    print(f"\n{symbol} {title}")
    print("-" * 60)

def test_environment():
    """测试环境配置"""
    print_section("环境配置检查", "🔍")
    
    checks = []
    
    # 检查 Python 版本
    import sys
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 11):
        print(f"✅ Python 版本: {py_version} (3.11+)")
        checks.append(True)
    else:
        print(f"⚠️  Python 版本: {py_version} (建议 3.11+)")
        checks.append(False)
    
    # 检查项目文件
    files_to_check = [
        ('scraper.py', '主爬虫脚本'),
        ('config.py', '配置文件'),
        ('requirements.txt', '依赖文件'),
        ('README.md', '项目说明'),
    ]
    
    for filename, desc in files_to_check:
        if os.path.exists(filename):
            print(f"✅ {filename}: {desc}")
            checks.append(True)
        else:
            print(f"❌ {filename}: 未找到")
            checks.append(False)
    
    return all(checks)

def test_dependencies():
    """测试依赖包"""
    print_section("依赖包检查", "📦")
    
    required_packages = [
        ('requests', 'HTTP 库'),
        ('feedparser', 'RSS 解析库'),
        ('dotenv', '环境变量管理'),
    ]
    
    installed = []
    
    for package_name, description in required_packages:
        try:
            __import__(package_name)
            print(f"✅ {package_name}: {description} (已安装)")
            installed.append(True)
        except ImportError:
            print(f"❌ {package_name}: {description} (未安装)")
            print(f"   安装命令: pip install {package_name}")
            installed.append(False)
    
    return all(installed)

def show_project_structure():
    """展示项目结构"""
    print_section("项目结构", "📁")
    
    structure = """
ainews/
├── 🔴 核心脚本
│   ├── scraper.py              # 主爬虫脚本 (RSS爬取 + WeChat推送)
│   ├── main.py                 # 主程序入口
│   └── quickstart.py           # 快速开始指南
│
├── 🟠 配置与测试
│   ├── config.py               # 项目配置
│   ├── demo_scraper.py         # 演示脚本 (无需WeChat Key)
│   ├── test_project.py         # 测试工具 (本文件)
│   └── requirements.txt        # Python 依赖
│
├── 📚 文档
│   ├── README.md               # 项目说明
│   ├── SETUP.md                # 详细配置指南
│   ├── PROJECT_ANALYSIS.md     # 项目分析报告
│   └── ARCHITECTURE.md         # 系统架构设计
│
├── 🤖 爬虫模块
│   └── scrapers/
│       ├── __init__.py
│       ├── base_scraper.py     # 基础爬虫类
│       └── news_scraper.py     # 新闻爬虫实现
│
├── 📊 数据和日志
│   ├── data/                   # 数据存储目录
│   └── logs/                   # 日志文件
│
└── ⚙️  GitHub Actions
    └── .github/workflows/
        └── daily-scraper.yml   # 自动执行工作流
"""
    print(structure)

def show_usage_examples():
    """显示使用示例"""
    print_section("使用示例", "💡")
    
    examples = """
┌─ 1️⃣  安装依赖 ────────────────────────────────────────┐
│ pip install -r requirements.txt                       │
└──────────────────────────────────────────────────────┘

┌─ 2️⃣  快速开始指南 ────────────────────────────────────┐
│ python quickstart.py                                  │
│ # 显示交互式配置指南和检查列表                         │
└──────────────────────────────────────────────────────┘

┌─ 3️⃣  演示爬虫功能 (无需WeChat Key) ──────────────────┐
│ python demo_scraper.py                               │
│ # 展示从HackerNews和TechCrunch爬取的新闻             │
└──────────────────────────────────────────────────────┘

┌─ 4️⃣  本地测试 (需要WeChat Key) ─────────────────────┐
│ # Windows:
│ set WEIXIN_WEBHOOK_KEY=your_key_here
│ python scraper.py
│
│ # Linux/Mac:
│ export WEIXIN_WEBHOOK_KEY="your_key_here"
│ python scraper.py
└──────────────────────────────────────────────────────┘

┌─ 5️⃣  本项目测试 ──────────────────────────────────────┐
│ python test_project.py                               │
│ # 运行此项目测试工具 (本程序)                         │
└──────────────────────────────────────────────────────┘
"""
    print(examples)

def show_data_flow():
    """显示数据流"""
    print_section("数据流程", "🔄")
    
    flow = """
🌍 RSS 源
├─ HackerNews: https://news.ycombinator.com/rss
└─ TechCrunch: https://feeds.techcrunch.com/TechCrunch/
    │
    ↓
📥 feedparser 解析
├─ 发起 HTTP 请求
├─ 解析 RSS/Atom XML
└─ 提取 entries 列表
    │
    ↓
📝 数据清洗
├─ 提取: title, link, summary
├─ 限制长度 (title:128, summary:200)
└─ 为每篇添加: source, published_at
    │
    ↓
🔗 数据聚合
├─ 每个源取 3 篇 (共 6-8 篇)
└─ 筛选最多 5 篇用于推送
    │
    ↓
📨 构建微信消息
{
  "msgtype": "news",
  "news": {
    "articles": [
      {
        "title": "新闻标题",
        "description": "摘要",
        "url": "链接"
      },
      ...
    ]
  }
}
    │
    ↓
💬 企业微信 API
POST /cgi-bin/webhook/send?key=WEBHOOK_KEY
    │
    ↓
👥 微信群组显示
展示为漂亮的新闻卡片格式
"""
    print(flow)

def show_rss_sources():
    """显示 RSS 源信息"""
    print_section("RSS 数据源", "📡")
    
    sources = [
        {
            "name": "HackerNews",
            "url": "https://news.ycombinator.com/rss",
            "description": "编程和科技讨论社区，聚合最新科技新闻和讨论",
            "update_freq": "实时更新"
        },
        {
            "name": "TechCrunch",
            "url": "https://feeds.techcrunch.com/TechCrunch/",
            "description": "全球科技新闻和评论，包括创业、融资、产品发布",
            "update_freq": "持续更新"
        }
    ]
    
    for i, source in enumerate(sources, 1):
        print(f"\n{i}. {source['name']}")
        print(f"   URL: {source['url']}")
        print(f"   描述: {source['description']}")
        print(f"   更新频率: {source['update_freq']}")

def show_configuration():
    """显示配置信息"""
    print_section("项目配置", "⚙️")
    
    config = {
        "爬虫超时": "10 秒",
        "重试次数": "3 次",
        "请求延迟": "1 秒 (防止滥用)",
        "每源条目数": "3 篇",
        "最多推送条目": "5 篇",
        "定时执行": "每天 09:00 UTC (17:00 北京时间)",
        "执行环境": "GitHub Actions (Ubuntu Latest)",
        "Python 版本": "3.11+",
    }
    
    for key, value in config.items():
        print(f"  {key:<15} → {value}")
    
    print("\n📌 必需环境变量:")
    print(f"  WEIXIN_WEBHOOK_KEY: 企业微信群机器人的 Webhook Key")
    
    print("\n📌 可选环境变量:")
    optional = [
        "LOG_LEVEL (默认: INFO)",
        "SCRAPER_TIMEOUT (默认: 10)",
        "SCRAPER_RETRIES (默认: 3)",
        "SCRAPER_DELAY (默认: 1)",
    ]
    for var in optional:
        print(f"  {var}")

def show_workflow():
    """显示执行工作流"""
    print_section("执行工作流", "🚀")
    
    workflow = """
【本地开发模式】
1. 安装依赖 → pip install -r requirements.txt
2. 配置 WeChat Key → set WEIXIN_WEBHOOK_KEY=xxx
3. 运行爬虫 → python scraper.py
4. 查看企业微信群 → 接收消息

【自动执行模式】
1. 代码推送到 GitHub
2. GitHub Actions 定时触发 (每天 09:00 UTC)
3. 环境自动准备 (Python 3.11 + 依赖)
4. 从 GitHub Secrets 获取 WEIXIN_WEBHOOK_KEY
5. 执行爬虫脚本
6. 推送到企业微信
7. 记录执行日志

【手动触发】
1. 访问 GitHub 仓库 → Actions 标签
2. 选择 "Daily Tech News Scraper"
3. 点击 "Run workflow"
4. 等待 2-3 分钟
5. 查看企业微信群接收消息
"""
    print(workflow)

def show_features():
    """显示项目特性"""
    print_section("项目特性", "✨")
    
    print("""
✅ 已实现的功能:
  • 多源 RSS 爬虫 (可扩展)
  • 自动化企业微信推送
  • GitHub Actions 定时执行
  • 结构化数据格式
  • 完善的错误处理
  • 自动重试机制
  • 详细的日志记录
  • 环境变量隔离
  • 模块化设计

🔄 可扩展方向:
  • 添加更多新闻源
  • Web 前端展示
  • 数据库存储
  • 内容过滤和分类
  • 自然语言处理
  • 消息推送自定义
  • 性能优化 (异步爬虫)
  • 监控指标集成
""")

def show_getting_started():
    """显示快速开始指南"""
    print_section("快速开始", "🎯")
    
    print("""
【第 1 步】获取企业微信 Webhook Key
  1. 打开企业微信 → 群聊 → 群机器人
  2. 创建新机器人，复制 Webhook URL
  3. 从 URL 中提取 key 值:
     https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY_HERE

【第 2 步】本地安装和测试
  1. 克隆或下载项目
  2. pip install -r requirements.txt
  3. 设置环境变量:
     • Windows: set WEIXIN_WEBHOOK_KEY=your_key_here
     • Linux/Mac: export WEIXIN_WEBHOOK_KEY="your_key_here"
  4. python scraper.py

【第 3 步】配置 GitHub (可选自动化)
  1. Fork/Push 项目到 GitHub
  2. 仓库 Settings → Secrets and variables → Actions
  3. 添加新 Secret:
     • Name: WEIXIN_WEBHOOK_KEY
     • Value: 你的 webhook key
  4. Actions 会自动每天运行

【第 4 步】查看结果
  • 本地: 查看 logs/ainews.log 文件
  • GitHub: 查看 Actions 执行日志
  • 企业微信: 在群组中查看新闻消息
""")

def show_summary():
    """显示项目总结"""
    print_section("项目总结", "📊")
    
    summary = {
        "项目名": "AiNews - 科技新闻自动爬虫",
        "主要语言": "Python 3.11+",
        "核心功能": "定时爬取科技新闻 → 推送到企业微信",
        "数据源": "HackerNews, TechCrunch (2 个，可扩展)",
        "执行频率": "每天 1 次 (可调整)",
        "推送平台": "企业微信 WebHook API",
        "自动化": "GitHub Actions",
        "适用场景": "团队内部科技资讯推送",
        "部署成本": "免费 (GitHub Actions 免费额度)",
        "维护难度": "低 (配置简单，自动执行)",
    }
    
    print()
    max_key_len = max(len(k) for k in summary.keys())
    for key, value in summary.items():
        print(f"  {key:<{max_key_len}} : {value}")

def main():
    """主函数"""
    print_banner("🤖 AiNews 项目测试工具", 70)
    
    print("""
欢迎使用 AiNews 项目测试工具！
本工具将帮助你了解项目的结构、功能和使用方式。
""")
    
    # 环境检查
    env_ok = test_environment()
    
    # 依赖检查
    deps_ok = test_dependencies()
    
    if not deps_ok:
        print("\n⚠️  部分依赖未安装。建议执行:")
        print("   pip install -r requirements.txt\n")
    
    # 显示项目结构
    show_project_structure()
    
    # 显示使用示例
    show_usage_examples()
    
    # 显示数据流
    show_data_flow()
    
    # 显示 RSS 源
    show_rss_sources()
    
    # 显示配置
    show_configuration()
    
    # 显示工作流
    show_workflow()
    
    # 显示特性
    show_features()
    
    # 显示快速开始
    show_getting_started()
    
    # 显示总结
    show_summary()
    
    print_banner("✅ 项目测试完成！", 70)
    
    print("""
📚 后续建议:

1️⃣  查看文档
   • README.md - 项目概述
   • SETUP.md - 详细配置
   • PROJECT_ANALYSIS.md - 项目分析
   • ARCHITECTURE.md - 系统架构

2️⃣  本地测试
   • python quickstart.py - 启动配置向导
   • python demo_scraper.py - 演示爬虫 (无需 WeChat key)

3️⃣  部署上线
   • 配置 GitHub Secrets
   • 启用 GitHub Actions
   • 每天自动推送新闻

4️⃣  扩展功能
   • 添加新的 RSS 源
   • 优化消息格式
   • 集成数据库
   • 增加 Web 前端

祝你使用愉快! 🎉
""")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
