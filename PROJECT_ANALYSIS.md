# AiNews 项目分析报告

## 📋 项目概述

**项目名称**: AiNews - 科技新闻自动爬虫 + 企业微信推送  
**开发语言**: Python 3.11+  
**项目类型**: 自动化爬虫系统  
**核心功能**: 定时爬取科技新闻，自动推送到企业微信

---

## 🎯 核心功能

### 1. **多源新闻爬虫**
- 从多个 RSS 源爬取最新科技新闻
- 支持的数据源:
  - **HackerNews** - 编程和科技讨论社区
  - **TechCrunch** - 科技新闻媒体
- 可扩展的 RSS 源配置

### 2. **企业微信推送**
- 将爬取的新闻推送到企业微信群组
- 采用消息卡片格式（news 类型）
- 支持自动重试机制

### 3. **自动化执行**
- **GitHub Actions** 集成
- 每天 09:00 UTC (北京时间 17:00) 自动运行
- 支持手动触发运行

### 4. **数据结构化**
- 统一的新闻数据格式
- 包含标题、URL、摘要、来源、发布时间
- 便于扩展和集成

---

## 📁 项目结构

```
ainews/
├── scraper.py              # ⭐ 主爬虫脚本 - 核心逻辑
├── main.py                 # 主入口 - 运行多个爬虫
├── quickstart.py           # 快速开始指南
├── demo_scraper.py         # 演示脚本（无需 WeChat key）
├── config.py               # 配置管理
├── requirements.txt        # Python 依赖
├── .env.example            # 环境变量模板
├── README.md               # 项目说明
├── SETUP.md                # 详细配置指南
├── daily-scraper.yml       # GitHub Actions 工作流
├── scrapers/               # 爬虫模块
│   ├── __init__.py
│   ├── base_scraper.py     # 基础爬虫类
│   └── news_scraper.py     # 新闻爬虫实现
└── data/                   # 数据存储目录
    logs/                   # 日志目录
```

---

## 🔧 技术栈

| 组件 | 说明 |
|------|------|
| **语言** | Python 3.11+ |
| **HTTP 库** | requests 2.31.0 |
| **RSS 解析** | feedparser 6.0.10 |
| **环境管理** | python-dotenv 1.0.0 |
| **自动化** | GitHub Actions |
| **推送平台** | 企业微信 WebHook |

---

## 🚀 工作流程

### 本地执行流程

```
1. 安装依赖
   └─ pip install -r requirements.txt
   
2. 设置环境变量
   └─ export WEIXIN_WEBHOOK_KEY="your_key"
   
3. 运行爬虫
   ├─ python scraper.py (推送到微信)
   ├─ python main.py (本地运行)
   └─ python demo_scraper.py (演示模式)
   
4. 查看结果
   └─ 在企业微信群中查看推送消息
```

### 自动执行流程 (GitHub Actions)

```
1. 定时触发 (每天 09:00 UTC)
   └─ 或手动在 Actions 标签点击 Run workflow
   
2. 环境准备
   └─ Ubuntu Latest + Python 3.11 + 依赖安装
   
3. 执行爬虫
   └─ python scraper.py
   
4. 推送结果
   └─ 发送到企业微信 WebHook
   
5. 记录日志
   └─ Actions 执行日志
```

---

## 📊 数据流

### 爬虫数据处理

```
RSS Feed (HackerNews/TechCrunch)
    ↓
[ feedparser 解析 ]
    ↓
Article 对象
├─ title:        新闻标题
├─ url:          原文链接
├─ summary:      摘要内容
├─ source:       来源名称
└─ published_at: 发布时间
    ↓
[ 数据聚合 & 过滤 ]
    ↓
WeChat Payload (JSON)
    ↓
[ requests 发送 ]
    ↓
企业微信 API
    ↓
👥 微信群组显示
```

---

## 🔑 配置要求

### 必需配置
- **WEIXIN_WEBHOOK_KEY**: 企业微信群机器人的 Webhook Key

### 可选配置
- `LOG_LEVEL`: 日志级别 (默认: INFO)
- `SCRAPER_TIMEOUT`: 爬虫超时时间 (默认: 10 秒)
- `SCRAPER_RETRIES`: 重试次数 (默认: 3)
- `SCRAPER_DELAY`: 请求延迟 (默认: 1 秒)

---

## 💻 快速开始

### 1️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

### 2️⃣ 获取 WeChat Webhook Key
1. 打开企业微信 → 群聊 → 群机器人
2. 创建新机器人，复制 Webhook URL
3. 提取 URL 中的 `key` 参数

### 3️⃣ 本地测试
```bash
# Linux/Mac
export WEIXIN_WEBHOOK_KEY="your_key_here"

# Windows
set WEIXIN_WEBHOOK_KEY=your_key_here

# 运行爬虫
python scraper.py
```

### 4️⃣ 查看演示 (无需 WeChat key)
```bash
python demo_scraper.py
```

---

## 🌟 主要特性

### ✅ 已实现
- [x] RSS 源爬虫
- [x] 数据聚合
- [x] WeChat 推送
- [x] 错误处理和重试
- [x] 日志记录
- [x] GitHub Actions 集成
- [x] 环境变量管理
- [x] 模块化设计

### 🔄 可扩展方向
- 添加更多新闻源 (Hacker News, Medium, etc.)
- 数据库存储 (避免重复)
- Web 前端查看
- 内容过滤和分类
- 自然语言处理 (摘要、翻译)
- 推送频率自定义
- 消息格式自定义

---

## 🧪 测试场景

### 场景 1: 本地测试爬虫
```bash
python demo_scraper.py
# 输出: 显示从 HackerNews 和 TechCrunch 爬取的最新新闻
```

### 场景 2: 本地推送到 WeChat
```bash
export WEIXIN_WEBHOOK_KEY="xxx"
python scraper.py
# 输出: 在企业微信群中收到新闻消息
```

### 场景 3: 查看快速开始指南
```bash
python quickstart.py
# 输出: 交互式的设置验证和配置指南
```

### 场景 4: 自动定时执行
```
GitHub Actions 每天 09:00 UTC 自动运行
查看结果: 仓库 → Actions → Daily Tech News Scraper
```

---

## 📈 性能指标

| 指标 | 值 |
|------|-----|
| **爬虫源数** | 2 个 (可扩展) |
| **每源文章数** | 3 条 |
| **最多推送文章** | 5 条 |
| **超时时间** | 10 秒 |
| **重试次数** | 3 次 |
| **请求延迟** | 1 秒 |

---

## 🔒 安全性

✅ **已实现的安全措施**
- 环境变量管理 (避免硬编码)
- GitHub Secrets 加密存储
- 请求延迟 (防止滥用)
- 错误处理 (不暴露敏感信息)
- 日志记录 (审计追踪)

⚠️ **建议**
- 定期轮换 Webhook Key
- 限制机器人权限
- 监控异常推送
- 更新依赖包

---

## 📝 日志示例

```
2024-01-15 17:00:00 - __main__ - INFO - ============================================================
2024-01-15 17:00:00 - __main__ - INFO - 🤖 Tech News Scraper with WeChat Integration
2024-01-15 17:00:00 - __main__ - INFO - ============================================================
2024-01-15 17:00:01 - __main__ - INFO - ✓ Webhook key loaded: xxx...
2024-01-15 17:00:01 - __main__ - INFO - 🚀 Starting tech news scraper...
2024-01-15 17:00:02 - __main__ - INFO - 📡 Fetching from HackerNews...
2024-01-15 17:00:05 - __main__ - INFO -   ✓ Show HN: Exploring 3D Graphics...
2024-01-15 17:00:05 - __main__ - INFO -   ✓ Ask HN: What's your setup?...
2024-01-15 17:00:06 - __main__ - INFO - 📡 Fetching from TechCrunch...
2024-01-15 17:00:08 - __main__ - INFO -   ✓ OpenAI releases GPT-4 Turbo...
2024-01-15 17:00:08 - __main__ - INFO - ✅ Scraped 6 articles total
2024-01-15 17:00:08 - __main__ - INFO - 📤 Preparing to send 6 articles to WeChat...
2024-01-15 17:00:09 - __main__ - INFO - ✅ Successfully sent 5 articles to WeChat!
2024-01-15 17:00:09 - __main__ - INFO - ============================================================
2024-01-15 17:00:09 - __main__ - INFO - ✅ All tasks completed successfully!
2024-01-15 17:00:09 - __main__ - INFO - ============================================================
```

---

## 🎓 学习价值

这个项目展示了以下编程概念:

1. **Web 爬虫** - 使用 feedparser 解析 RSS 源
2. **API 集成** - 调用企业微信 API
3. **错误处理** - try-catch, 重试机制
4. **日志管理** - 结构化日志记录
5. **环境配置** - 环境变量管理
6. **自动化** - GitHub Actions 工作流
7. **模块设计** - 代码组织和复用
8. **异步处理** - 可扩展到异步爬虫

---

## 🤝 贡献方向

欢迎贡献以下改进:
- 支持更多新闻源
- Web 前端界面
- 数据库集成
- 内容过滤
- 推送自定义
- 性能优化

---

## 📞 支持

- 📖 查看 `README.md` 了解项目概况
- 🔧 查看 `SETUP.md` 获取详细配置
- ⚡ 运行 `python quickstart.py` 启动配置向导
- 🚀 查看 GitHub Actions 执行日志

---

**最后更新**: 2024年1月  
**项目状态**: ✅ 生产就绪
