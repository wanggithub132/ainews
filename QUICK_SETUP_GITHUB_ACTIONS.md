# ⚡ GitHub Actions 快速配置 (5 分钟)

## 📋 需要做的 3 个步骤

### Step 1️⃣: 配置 Webhook Key Secret (2 分钟)

```
1. 打开你的 GitHub 仓库
2. Settings → Secrets and variables → Actions
3. 点击 "New repository secret"
4. 填写表单:
   Name:  WEIXIN_WEBHOOK_KEY
   Value: 从企业微信 Webhook URL 中复制的 key 值
5. 点击 "Add secret"
```

✅ **完成！Secret 已配置**

---

### Step 2️⃣: 推送代码到 GitHub (1 分钟)

```bash
cd f:\work\fromgithub\ainews

# 如果还没有 git 仓库，初始化一个
git init
git add .
git commit -m "Initial commit: AiNews project with GitHub Actions"

# 添加 GitHub 仓库
git remote add origin https://github.com/your-username/ainews.git
git branch -M main

# 推送代码
git push -u origin main
```

✅ **完成！代码已推送到 GitHub**

---

### Step 3️⃣: 启用并测试工作流 (2 分钟)

```
1. 进入你的 GitHub 仓库
2. 点击 "Actions" 标签
3. 如果看到 3 个工作流，说明已启用:
   ✅ Daily Tech News Scraper
   ✅ Advanced Tech News Scraper with Retry
   ✅ CI/CD Quality Check
4. 点击 "Daily Tech News Scraper"
5. 点击 "Run workflow" 进行测试
6. 等待执行完成 (通常 1-2 分钟)
7. 查看企业微信群，应该收到推送的新闻
```

✅ **完成！工作流已启用并测试**

---

## 📊 工作流概览

| 工作流 | 触发方式 | 执行频率 | 用途 |
|--------|---------|---------|------|
| **Daily Scraper** | 定时 + 手动 | 每天 1 次 | 爬取新闻 |
| **Advanced Scraper** | 定时 + 手动 | 每天 2 次 | 爬取新闻 (带重试) |
| **Quality Check** | Push/PR + 手动 | 每次提交 | 代码质量检查 |

---

## 🎯 立即可做

### 测试爬虫工作流

```
1. 仓库 → Actions → Daily Tech News Scraper
2. "Run workflow" → "Run workflow"
3. 等待完成
4. 查看企业微信群中的新闻推送
```

### 查看执行日志

```
1. 点击具体的运行记录
2. 展开 "Run tech news scraper" step
3. 查看详细的爬虫执行日志
```

### 修改定时时间 (可选)

编辑 `.github/workflows/daily-scraper.yml`:

```yaml
on:
  schedule:
    # 改这里的时间 (UTC)
    - cron: '0 9 * * *'    # 改成你需要的时间
```

常见时间:
- `0 9 * * *` → 每天 UTC 9:00 (北京时间 17:00)
- `0 14 * * *` → 每天 UTC 14:00 (北京时间 22:00)
- `0 0 * * *` → 每天 UTC 0:00 (北京时间 08:00)

---

## ✅ 完成清单

- [ ] 配置 GitHub Secret (WEIXIN_WEBHOOK_KEY)
- [ ] 推送代码到 GitHub
- [ ] 看到 3 个工作流出现在 Actions 标签
- [ ] 手动触发测试 "Daily Tech News Scraper"
- [ ] 在企业微信群看到推送的新闻
- [ ] (可选) 修改定时执行时间
- ✅ 完成！

---

## 🚀 现在可以做什么

### 自动化已启用 ✅

- ✅ **每日自动爬虫** - 每天 UTC 9:00 自动运行
- ✅ **企业微信推送** - 新闻自动推送到群组
- ✅ **代码质量检查** - 每次 push 自动检查
- ✅ **安全扫描** - 自动检查安全漏洞
- ✅ **手动触发** - 任时间手动运行

### 可选的高级设置

- 📧 配置邮件通知
- 💬 配置 Slack 通知
- 📊 设置 Actions 统计
- 🔔 配置分支保护规则

---

## 💡 故障排查

### 工作流不运行？
- 检查 Secret 是否配置: Settings → Secrets
- 检查 Actions 是否启用: Actions 标签
- 查看工作流日志获取错误信息

### 收不到企业微信推送？
- 检查 Secret 值是否正确 (复制时不要包含 key= 前缀)
- 检查工作流日志中的错误
- 手动运行 `python scraper.py` 测试

### 工作流执行超时？
- 增加超时时间
- 检查网络连接
- 检查 RSS 源是否可访问

---

## 📚 查看详细文档

- **GITHUB_ACTIONS_GUIDE.md** - 完整的配置和使用文档
- **START_HERE.md** - 项目开始指南
- **SETUP.md** - 详细的部署说明

---

**就这样！你的 GitHub Actions 工作流已配置完成。** 🎉

从现在开始，你的爬虫会自动运行，新闻会自动推送到企业微信！

下一步：推送代码到 GitHub 并在 Actions 标签中看到工作流运行。
