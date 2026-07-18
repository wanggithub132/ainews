# 🚀 AiNews 项目运行指南

## 📌 项目概述

**AiNews** 是一个完整的科技新闻自动爬虫系统，可以：
- 🌍 从 HackerNews、TechCrunch 等源爬取最新科技新闻
- 📱 自动推送到企业微信群组
- ⏰ 通过 GitHub Actions 每天定时自动运行

---

## 🎯 快速查看项目效果

### 方案 1️⃣: 查看项目文档 (推荐，无需配置)

```bash
# 查看项目分析报告
cat PROJECT_ANALYSIS.md

# 查看系统架构设计
cat ARCHITECTURE.md

# 查看运行指南
cat README.md
```

**效果**: 📖 了解项目的完整功能、架构和工作流程

---

### 方案 2️⃣: 运行项目测试工具 (需要 Python)

```bash
# 运行项目测试工具
python test_project.py
```

**效果**: 📊 交互式展示项目结构、依赖、配置、工作流程、数据流等

**输出内容**:
- ✅ 环境配置检查
- ✅ 依赖包检查
- ✅ 项目结构展示
- ✅ 使用示例
- ✅ 数据流程图
- ✅ RSS 源信息
- ✅ 快速开始指南

---

### 方案 3️⃣: 运行快速开始工具 (需要 Python)

```bash
# 运行快速开始指南
python quickstart.py
```

**效果**: 🚀 启动交互式配置检查和设置向导

**功能**:
- 检查环境设置
- 显示配置步骤
- 提供故障排查指南
- 显示后续步骤

---

### 方案 4️⃣: 演示爬虫功能 (需要 Python + 网络)

```bash
# 运行演示爬虫 (无需 WeChat Key)
python demo_scraper.py
```

**效果**: 🌐 实时演示爬取新闻的过程，显示从 RSS 源获取的实际数据

**输出示例**:
```
🚀 Starting tech news scraper demo...
============================================================

📡 Fetching from HackerNews...
   Found 30 entries from HackerNews
   [1] Show HN: Exploring 3D Graphics...
       URL: https://news.ycombinator.com/item?id=123456
   [2] Ask HN: What's your setup?...
   [3] New in Python 3.12...

📡 Fetching from TechCrunch...
   Found 25 entries from TechCrunch
   [1] OpenAI releases GPT-4 Turbo...
   [2] Apple launches new MacBook Pro...
   [3] Meta's new AI features...

============================================================
✅ Scraped 6 articles total
============================================================

📊 Summary by Source:
   HackerNews: 3 articles
   TechCrunch: 3 articles

📰 Sample Articles (for WeChat push):
   [1] Show HN: Exploring 3D Graphics
       Source: HackerNews
       Summary: A detailed exploration of modern 3D graphics techniques...
   
   ... and more
```

---

### 方案 5️⃣: 完整本地测试 (需要 WeChat Webhook Key)

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置环境变量
# Windows:
set WEIXIN_WEBHOOK_KEY=your_webhook_key_here

# Linux/Mac:
export WEIXIN_WEBHOOK_KEY="your_webhook_key_here"

# 3. 运行爬虫并推送到 WeChat
python scraper.py

# 4. 查看企业微信群
# 在群组中会看到推送的新闻消息
```

**效果**: ✨ 实时爬取新闻并推送到企业微信群组

---

## 🛠️ 环境准备

### 系统要求
- **Python**: 3.11 或更新
- **OS**: Windows / Linux / Mac
- **网络**: 需要访问 RSS 源和 WeChat API

### 安装 Python 依赖

```bash
# 进入项目目录
cd ainews

# 安装依赖
pip install -r requirements.txt

# 验证安装
pip show requests feedparser python-dotenv
```

**所需依赖**:
- `requests` - HTTP 客户端库
- `feedparser` - RSS/Atom 解析库
- `python-dotenv` - 环境变量管理

---

## 📁 项目文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `scraper.py` | **主爬虫脚本** | 爬取新闻 + 推送到 WeChat |
| `demo_scraper.py` | **演示脚本** | 演示爬虫功能 (无需 WeChat key) |
| `test_project.py` | **测试工具** | 展示项目结构和配置 |
| `quickstart.py` | **快速开始** | 交互式配置指南 |
| `config.py` | **配置文件** | 项目配置管理 |
| `requirements.txt` | **依赖列表** | Python 包依赖 |
| `README.md` | **项目说明** | 项目概述和快速指南 |
| `SETUP.md` | **配置指南** | 详细的配置步骤 |
| `PROJECT_ANALYSIS.md` | **项目分析** | 完整的功能分析报告 |
| `ARCHITECTURE.md` | **架构设计** | 系统架构和数据流 |
| `HOW_TO_RUN.md` | **运行指南** | 本文档 |

---

## 🎬 实际操作步骤

### 快速查看 (5 分钟)

```bash
# 1. 查看项目文档
cat README.md
cat PROJECT_ANALYSIS.md

# 2. 查看项目代码
cat scraper.py  # 查看主爬虫脚本
cat config.py   # 查看配置
```

**结果**: 了解项目的功能和工作原理

---

### 中等体验 (15 分钟)

```bash
# 1. 安装依赖
pip install requests feedparser python-dotenv

# 2. 运行项目测试工具
python test_project.py

# 3. 运行演示爬虫
python demo_scraper.py
```

**结果**: 看到实际的爬虫效果和爬取的新闻数据

---

### 完整体验 (30 分钟)

```bash
# 1. 准备环境
pip install -r requirements.txt

# 2. 获取企业微信 Webhook Key
# - 打开企业微信
# - 群聊 → 群机器人 → 添加机器人
# - 复制 Webhook URL 中的 key 部分

# 3. 本地测试
set WEIXIN_WEBHOOK_KEY=your_key_here
python scraper.py

# 4. 查看企业微信群
# - 应该收到推送的新闻消息

# 5. 查看日志
cat logs/ainews.log
```

**结果**: 看到完整的爬虫 → 推送流程

---

### 自动化部署 (GitHub Actions)

```bash
# 1. 推送到 GitHub
git push

# 2. 配置 GitHub Secrets
# Repository Settings → Secrets and variables → Actions
# 添加: WEIXIN_WEBHOOK_KEY = your_key_here

# 3. 每天 09:00 UTC 自动运行
# 或手动触发: Actions → Run workflow

# 4. 企业微信会自动收到新闻推送
```

**结果**: 全自动每天推送新闻到企业微信

---

## 📊 查看项目效果的不同角度

### 1. 代码角度 👨‍💻
```bash
# 查看主爬虫逻辑
head -60 scraper.py

# 查看数据处理
grep -A 10 "article = {" scraper.py

# 查看推送逻辑
grep -A 20 "def send_to_weixin" scraper.py
```

### 2. 配置角度 ⚙️
```bash
# 查看项目配置
cat config.py

# 查看环境变量模板
cat .env.example

# 查看依赖信息
cat requirements.txt
```

### 3. 文档角度 📖
```bash
# 查看项目说明
cat README.md

# 查看详细配置
cat SETUP.md

# 查看项目分析
cat PROJECT_ANALYSIS.md

# 查看系统架构
cat ARCHITECTURE.md
```

### 4. 运行角度 🚀
```bash
# 查看环境检查
python test_project.py

# 查看爬虫演示
python demo_scraper.py

# 查看快速开始
python quickstart.py
```

### 5. 日志角度 📝
```bash
# 运行后查看日志
python scraper.py
cat logs/ainews.log

# 或查看 GitHub Actions 日志
# 访问: https://github.com/your_repo/actions
```

---

## 🌟 项目亮点展示

### ✨ 亮点 1: 多源爬虫
支持从多个 RSS 源获取新闻:
- 📍 HackerNews - 编程社区
- 📍 TechCrunch - 科技新闻
- 🔧 可轻松扩展新源

### ✨ 亮点 2: 智能推送
- 📱 企业微信集成
- 🎯 消息卡片格式
- ⚡ 自动重试机制

### ✨ 亮点 3: 自动化执行
- 🤖 GitHub Actions 集成
- ⏰ 每天定时执行
- 📊 完整日志记录

### ✨ 亮点 4: 模块化设计
```
scraper.py
├── scrape_tech_news()    # 爬虫模块
├── send_to_weixin()      # 推送模块
└── main()               # 主控制模块
```

### ✨ 亮点 5: 完善的文档
- 📘 项目说明
- 📗 配置指南
- 📙 架构设计
- 📕 使用示例

---

## ⚠️ 常见问题

### Q1: 没有 WeChat Key，怎么看效果？
**A**: 运行 `python demo_scraper.py` 看爬虫效果，无需 WeChat key

### Q2: 没有装 Python，怎么了解项目？
**A**: 查看文档: README.md, PROJECT_ANALYSIS.md, ARCHITECTURE.md

### Q3: 想在本地测试完整流程？
**A**: 
```bash
pip install -r requirements.txt
set WEIXIN_WEBHOOK_KEY=your_key
python scraper.py
```

### Q4: 想部署到 GitHub Actions？
**A**: 参考 SETUP.md 中的 GitHub 配置部分

### Q5: 想添加新的新闻源？
**A**: 编辑 scraper.py 中的 RSS_FEEDS 列表

---

## 📋 推荐查看顺序

### 初次接触 (15 分钟)
1. ✅ 阅读 README.md
2. ✅ 查看 PROJECT_ANALYSIS.md
3. ✅ 浏览 scraper.py 代码

### 深入理解 (30 分钟)
1. ✅ 查看 ARCHITECTURE.md
2. ✅ 运行 python test_project.py
3. ✅ 运行 python demo_scraper.py

### 本地部署 (1 小时)
1. ✅ pip install -r requirements.txt
2. ✅ 获取企业微信 Webhook Key
3. ✅ 运行 python scraper.py
4. ✅ 查看企业微信群接收消息

### 线上自动化 (30 分钟)
1. ✅ 推送到 GitHub
2. ✅ 配置 GitHub Secrets
3. ✅ 启用 Actions
4. ✅ 定时自动推送

---

## 🎓 学习收获

通过这个项目，你将学到：

- 🌐 **Web 爬虫技术** - RSS 源爬取和解析
- 🔗 **API 集成** - 调用第三方 API
- ⚙️ **自动化流程** - GitHub Actions 工作流
- 📊 **数据处理** - JSON 序列化和转换
- 🐍 **Python 编程** - 模块设计和错误处理
- 🔒 **安全实践** - 环境变量和密钥管理
- 📝 **日志管理** - 结构化日志记录

---

## 🚀 后续可以做的事

- ✨ 添加更多新闻源 (Medium, Dev.to 等)
- 🎨 开发 Web 前端展示新闻
- 💾 集成数据库存储历史新闻
- 🔍 添加内容过滤和搜索
- 🌐 部署到云服务 (AWS, Azure, Vercel)
- 📊 实现数据分析和可视化
- 🤖 集成 AI 进行摘要和翻译

---

**祝你使用愉快！** 🎉

如有问题，查看相关文档或运行 `python quickstart.py` 获取帮助。
