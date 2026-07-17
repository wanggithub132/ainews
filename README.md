# AiNews - Automated News Web Scraper

自动新闻网络爬虫工具，用于从多个新闻源自动采集和解析新闻内容。

## 功能特性

- 🚀 **模块化设计**: 易于扩展支持新的数据源
- 🔄 **自动重试机制**: 内置请求失败自动重试
- 📊 **结构化数据**: 统一的数据格式，便于存储和分析
- 🛡️ **礼貌爬取**: 支持请求延迟，避免对服务器造成压力
- 📝 **详细日志**: 完整的操作日志，便于调试和监控
- ⚙️ **灵活配置**: 基于环境变量的配置系统

## 安装

### 1. 克隆仓库
```bash
git clone https://github.com/wanggithub132/ainews.git
cd ainews
```

### 2. 创建虚拟环境
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\\Scripts\\activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
```bash
cp .env.example .env
# 根据需要编辑 .env 文件
```

## 使用

### 运行爬虫
```bash
python main.py
```

### 自定义爬虫

创建新的爬虫类继承 `BaseScraper`:

```python
from scrapers.base_scraper import BaseScraper

class CustomScraper(BaseScraper):
    def scrape(self):
        # 实现你的爬虫逻辑
        pass
```

### 支持的新闻源

在 `config.py` 中配置 `NEWS_SOURCES`:

```python
NEWS_SOURCES = [
    {
        'name': 'BBC News',
        'url': 'https://www.bbc.com/news',
        'category': 'world',
    },
    # 添加更多新闻源
]
```

## 项目结构

```
ainews/
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py      # 基础爬虫类
│   └── news_scraper.py      # 新闻爬虫实现
├── config.py                 # 配置文件
├── main.py                   # 主入口
├── requirements.txt          # Python 依赖
├── .env.example             # 环境变量模板
└── README.md                # 本文档
```

## 配置说明

### 环境变量

- `LOG_LEVEL`: 日志级别 (默认: INFO)
- `SCRAPER_TIMEOUT`: 请求超时时间，单位秒 (默认: 10)
- `SCRAPER_RETRIES`: 失败重试次数 (默认: 3)
- `SCRAPER_DELAY`: 请求间隔延迟，单位秒 (默认: 1)
- `DATABASE_URL`: 数据库连接字符串 (可选)
- `API_HOST`: API 服务地址 (默认: 0.0.0.0)
- `API_PORT`: API 服务端口 (默认: 8000)

## 进阶用法

### 编程方式使用

```python
from scrapers import NewsScraper

scraper = NewsScraper('https://example.com')
articles = scraper.run(category='tech')

for article in articles:
    print(article['title'])
    print(article['url'])
    print(article['date'])
```

### 定时执行

使用 `schedule` 库进行定时爬取：

```bash
pip install schedule
```

```python
import schedule
import time
from main import run_all_scrapers

def job():
    run_all_scrapers()

schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 最佳实践

1. **尊重网站**: 总是检查 `robots.txt` 和网站的 ToS
2. **合理延迟**: 设置适当的 `SCRAPER_DELAY` 避免频繁请求
3. **处理异常**: 自定义爬虫时，添加充分的错误处理
4. **数据持久化**: 考虑将爬取的数据存储到数据库
5. **监控日志**: 定期检查日志文件，监控爬虫运行状态

## 常见问题

**Q: 如何处理需要 JavaScript 渲染的页面？**
A: 使用 Selenium 替代 Requests。参考 `requirements.txt` 中已包含的 `selenium` 依赖。

**Q: 如何处理验证码和登录？**
A: 对于简单情况，可以通过 Cookie 处理。复杂情况建议使用 Selenium + 手动干预。

**Q: 爬虫被屏蔽了怎么办？**
A: 尝试以下方法：
- 增加 `SCRAPER_DELAY`
- 轮换 User-Agent
- 使用代理 IP
- 检查是否违反了网站 ToS

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- GitHub: [@wanggithub132](https://github.com/wanggithub132)
