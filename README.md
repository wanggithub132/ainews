# AiNews - 科技新闻自动爬虫 + 企业微信推送

自动化科技新闻爬虫系统，每天定时爬取全球最新科技新闻，推送到企业微信群组。

## 功能

- 从 HackerNews、TechCrunch 等 RSS 源爬取最新科技新闻
- 自动推送到企业微信群组（新闻卡片格式）
- GitHub Actions 每天定时执行，支持手动触发
- 自动重试机制，失败自动恢复
- 完整的执行日志

## 项目结构

```
ainews/
├── .github/workflows/       # GitHub Actions 工作流
│   ├── daily-scraper.yml    # 每日爬虫 + WeChat 推送
│   └── quality-check.yml    # 代码质量检查
├── src/                     # 源代码
│   ├── config.py            # 配置管理
│   ├── scraper.py           # 主爬虫脚本（WeChat 推送）
│   ├── main.py              # 本地爬虫运行器
│   ├── quickstart.py        # 快速开始工具
│   └── scrapers/            # 爬虫模块
│       ├── base_scraper.py  # 基础爬虫类
│       └── news_scraper.py  # 新闻爬虫实现
├── .env.example             # 环境变量模板
├── requirements.txt         # Python 依赖
└── README.md
```

## 快速开始

### 前置条件

- Python 3.11+
- 企业微信群组和机器人

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 获取企业微信 Webhook Key

1. 企业微信 → 群聊 → 群机器人 → 添加机器人
2. 复制 Webhook URL，提取 `key` 参数值：
   ```
   https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY_HERE
   ```

### 3. 本地运行

```bash
# 设置环境变量
# Windows:
set WEIXIN_WEBHOOK_KEY=your_key_here

# Linux/Mac:
export WEIXIN_WEBHOOK_KEY="your_key_here"

# 运行爬虫
cd src
python scraper.py
```

## GitHub Actions 自动化

### 配置 Secret

1. 进入仓库 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. Name: `WEIXIN_WEBHOOK_KEY`，Value: 你的 webhook key
4. 保存

### 执行方式

- **定时执行**：每天 UTC 09:00（北京时间 17:00）自动运行
- **手动触发**：Actions → Daily Tech News Scraper → Run workflow

### 代码质量检查

每次 push 到 main 分支会自动运行：
- Flake8 代码检查
- 模块导入测试
- 敏感信息扫描

## 配置说明

环境变量（参考 `.env.example`）：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `WEIXIN_WEBHOOK_KEY` | 必需 | 企业微信 Webhook Key |
| `SCRAPER_TIMEOUT` | 10 | HTTP 请求超时（秒） |
| `SCRAPER_RETRIES` | 3 | 失败重试次数 |
| `SCRAPER_DELAY` | 1 | 请求间隔（秒） |

## 添加新闻源

编辑 `src/config.py` 中的 `NEWS_SOURCES` 列表：

```python
NEWS_SOURCES = [
    {
        'name': 'BBC News',
        'url': 'https://www.bbc.com/news',
        'category': 'world',
    },
    # 添加更多新闻源...
]
```

## 常见问题

**Q: 没有收到推送？**
- 检查 GitHub Secret 中的 WEIXIN_WEBHOOK_KEY 是否正确
- 查看 Actions 执行日志

**Q: 如何修改执行时间？**
- 编辑 `.github/workflows/daily-scraper.yml` 中的 cron 表达式

## License

MIT
