# 📖 AiNews - 科技新闻自动爬虫 + 企业微信推送

完整的自动化科技新闻爬虫系统，每天定时爬取全球最新科技新闻，并推送到企业微信群组。

## ✨ 核心功能

- 🌍 **多源新闻爬虫** - 从 HackerNews、TechCrunch 等爬取最新科技新闻
- 📱 **企业微信推送** - 将新闻结构化推送到企业微信群组
- ⏰ **定时自动执行** - GitHub Actions 每天自动运行
- 📊 **结构化数据** - 统一的数据格式便于扩展
- 🔄 **自动重试机制** - 失败自动重试确保可靠性
- 📝 **完整日志** - 详细的执行日志便于调试和监控

## 🚀 快速开始

### 前置要求
- Python 3.11+
- 企业微信账号和群组
- GitHub 账户和仓库

### 1️⃣ 获取企业微信 Webhook Key

```
企业微信 → 群聊 → 群机器人 → 添加机器人 → 复制 Webhook URL
从 URL 中提取 key 值：https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY_HERE
```

### 2️⃣ 配置 GitHub Secret

1. 进入仓库 **Settings** → **Secrets and variables** → **Actions**
2. 创建新 Secret：
   - **Name**: `WEIXIN_WEBHOOK_KEY`
   - **Value**: 你的 webhook key
3. 保存

### 3️⃣ 手动触发工作流

1. 进入 **Actions** 标签
2. 选择 **Daily Tech News Scraper**
3. 点击 **Run workflow**
4. 等待 2-3 分钟，查看企业微信群

### 4️⃣ 自动定时执行

工作流已配置为每天 **09:00 UTC**（北京时间 17:00）自动运行

## 📁 项目结构

```
ainews/
├── scraper.py              # 主爬虫脚本
├── quickstart.py           # 快速开始工具
├── daily-scraper.yml       # GitHub Actions 工作流（位置：.github/workflows/）
├── .env.example            # 环境变量模板
├── requirements.txt        # Python 依赖
├── README.md               # 本文档
└── SETUP.md               # 详细配置指南
```

## 🔧 本地测试

### 安装依赖
```bash
pip install -r requirements.txt
```

### 设置环境变量
```bash
# Linux/Mac
export WEIXIN_WEBHOOK_KEY="your_key_here"

# Windows
set WEIXIN_WEBHOOK_KEY=your_key_here
```

### 运行爬虫
```bash
python scraper.py
```

### 查看快速开始指南
```bash
python quickstart.py
```

## 📊 工作流配置

| 属性 | 值 |
|------|-----|
| **触发方式** | 定时 + 手动 |
| **执行时间** | 每天 09:00 UTC |
| **运行环境** | Ubuntu Latest |
| **Python 版本** | 3.11 |
| **依赖** | requests, feedparser |

## 📈 监控执行

### 查看执行历史
1. 仓库 → **Actions** 标签
2. 选择 **Daily Tech News Scraper**
3. 查看所有历史执行

### 查看详细日志
1. 点击具体的执行记录
2. 展开 **Run tech news scraper** 步骤
3. 查看完整的执行输出

## 🛠️ 高级配置

### 修改爬取数量
编辑 `scraper.py`：
```python
for entry in feed.entries[:3]:  # 修改数字
```

### 添加新闻源
编辑 `scraper.py` 的 `RSS_FEEDS` 列表

### 修改执行时间
编辑 `.github/workflows/daily-scraper.yml` 的 cron 表达式

## ❓ 常见问题

### Q: 没有收到推送？
- 检查 GitHub Secret 是否正确设置
- 验证 webhook key 是否正确
- 查看 Actions 执行日志
- 确保企业微信群组允许机器人发送

### Q: 如何立即运行？
- 进入 Actions → 选择工作流 → 点击 Run workflow

### Q: 如何修改执行时间？
- 编辑 `.github/workflows/daily-scraper.yml` 中的 cron 表达式

### Q: 支持哪些新闻源？
- HackerNews
- TechCrunch
- 可自行添加其他 RSS 源

## 📚 文档

- **SETUP.md** - 详细的配置和使用指南
- **scraper.py** - 爬虫主脚本
- **quickstart.py** - 快速开始验证工具

## 🔒 安全建议

✅ 永远不要在代码中硬编码 webhook key
✅ 使用 GitHub Secrets 存储敏感信息
✅ 定期检查 Actions 日志
✅ 及时更新依赖包

## 📄 许可证

MIT License

---

**需要帮助？** 查看 `SETUP.md` 获取详细配置指南
