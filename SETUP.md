# 🔧 完整配置指南

## 第一步：获取企业微信 Webhook Key

### 1. 打开企业微信
- 登录企业微信
- 进入你的群聊

### 2. 添加机器人
- 点击群聊右上角的菜单
- 选择 **群机器人** 或 **Add Bot**
- 点击 **添加机器人**

### 3. 复制 Webhook URL
- 复制机器人的完整 URL，类似于：
```
https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5383441a-eb3b-48c7-96fd-fbcea462cd63
```

### 4. 提取 Key 值
- 从 URL 中提取 `key` 参数的值
- 示例：`5383441a-eb3b-48c7-96fd-fbcea462cd63`

---

## 第二步：配置 GitHub Secret

### 1. 进入仓库设置
- 打开：https://github.com/wanggithub132/ainews
- 点击 **Settings** (设置)

### 2. 打开 Secrets 配置
- 左侧菜单 → **Secrets and variables**
- 选择 **Actions**

### 3. 新建 Secret
- 点击 **New repository secret**
- 填写：
  - **Name**: `WEIXIN_WEBHOOK_KEY`
  - **Secret**: 粘贴你的 webhook key（从第一步提取的值）
- 点击 **Add secret**

✅ 完成！现在 GitHub Actions 可以访问这个 key 了

---

## 第三步：手动触发工作流（测试）

### 1. 进入 Actions 页面
- 打开：https://github.com/wanggithub132/ainews/actions

### 2. 选择工作流
- 左侧菜单中选择 **Daily Tech News Scraper**

### 3. 触发运行
- 点击 **Run workflow**
- 选择分支（保持 main）
- 点击 **Run workflow** 确认

### 4. 监控执行
- 等待 2-3 分钟
- 查看执行进度（黄色 ⏳ → 绿色 ✅）

### 5. 检查企业微信
- 打开你的微信群聊
- 查看是否收到新闻推送

---

## 第四步：自动定时执行

### 当前配置
- ✅ **每天 09:00 UTC**（北京时间 17:00）自动运行
- ✅ **支持手动随时触发**

### 修改执行时间（可选）

编辑 `.github/workflows/daily-scraper.yml`：

找到这一行：
```yaml
- cron: '0 9 * * *'
```

修改为你想要的时间。Cron 格式：`分 时 日 月 周`

常见示例：
- `0 9 * * *` - 每天 09:00 UTC
- `0 0 * * *` - 每天 00:00 UTC
- `0 12 * * *` - 每天 12:00 UTC
- `0 1,9,17 * * *` - 每天 01:00, 09:00, 17:00 UTC
- `0 9 * * MON` - 每周一 09:00 UTC

---

## 🐛 故障排查

### 问题1：企业微信没有收到推送

**检查清单**：

1. ✅ GitHub Secret 是否已正确配置
   - 进入 Settings → Secrets → 检查是否有 `WEIXIN_WEBHOOK_KEY`

2. ✅ Webhook key 是否正确
   - 确认复制的是 **key 值**，不是整个 URL
   - 正确 ✅：`5383441a-eb3b-48c7-96fd-fbcea462cd63`
   - 错误 ❌：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...`

3. ✅ 企业微信群组设置
   - 确认机器人还在群组中（未被移除）
   - 确认群组没有禁用机器人消息

4. ✅ 查看 Actions 日志
   - 进入 Actions → 最新运行 → 展开日志
   - 查看是否有错误信息

### 问题2：Actions 工作流失败

**常见错误**：

❌ `WEIXIN_WEBHOOK_KEY not set`
- 原因：GitHub Secret 未正确配置
- 解决：重新检查 Settings → Secrets 的配置

❌ `Connection timeout`
- 原因：网络问题或 webhook URL 不可达
- 解决：检查网络连接，稍后重试

❌ `errcode: 43001`
- 原因：企业微信 API 错误，通常是 key 不正确或机器人已删除
- 解决：验证 webhook key 是否正确，机器人是否还在群组

### 问题3：如何查看详细错误

1. 进入 https://github.com/wanggithub132/ainews/actions
2. 点击最新的执行记录
3. 点击 **Run tech news scraper** 步骤
4. 展开查看完整的日志输出
5. 根据错误信息排查问题

---

## 💡 常用操作

### 立即运行工作流（不等待定时）

1. 进入 https://github.com/wanggithub132/ainews/actions
2. 选择 **Daily Tech News Scraper**
3. 点击 **Run workflow** → **Run workflow**
4. 工作流立即开始执行

### 查看执行历史

1. 进入 Actions 页面
2. 选择 **Daily Tech News Scraper**
3. 可以看到所有历史执行记录
4. 点击任意记录查看详细日志

### 修改爬取数量

编辑 `scraper.py`，找到这一行：
```python
for entry in feed.entries[:3]:  # 修改这里的数字
```

- `:3` = 每个源爬取 3 条
- `:5` = 每个源爬取 5 条
- `:10` = 每个源爬取 10 条

修改后保存并提交，下次运行会生效。

### 添加新闻源

编辑 `scraper.py` 的 `RSS_FEEDS` 部分：

```python
RSS_FEEDS = [
    {'name': 'HackerNews', 'url': 'https://news.ycombinator.com/rss'},
    {'name': 'TechCrunch', 'url': 'https://feeds.techcrunch.com/TechCrunch/'},
    # 添加你的新闻源
    {'name': 'Your Source', 'url': 'https://example.com/rss'},
]
```

---

## 🧪 本地测试（可选）

### 前置条件
- Python 3.11+
- 已安装依赖：`pip install -r requirements.txt`

### 运行爬虫

```bash
# 设置环境变量
export WEIXIN_WEBHOOK_KEY="你的_webhook_key"

# 运行爬虫
python scraper.py
```

### 预期输出

```
==========================================
🤖 Tech News Scraper with WeChat Integration
==========================================
✓ Webhook key loaded: 5383441a-eb3b-48c7-9...
🚀 Starting tech news scraper...
📡 Fetching from HackerNews...
  ✓ Article title 1...
  ✓ Article title 2...
  ✓ Article title 3...
✅ Scraped 6 articles total
📤 Preparing to send 5 articles to WeChat...
✅ Successfully sent 5 articles to WeChat!
==========================================
✅ All tasks completed successfully!
==========================================
```

---

## 🔒 安全建议

✅ 永远不要在代码中硬编码 webhook key
✅ 始终使用 GitHub Secrets 存储敏感信息
✅ 定期检查 Actions 日志，监控执行状态
✅ 及时更新依赖包（定期运行 `pip install --upgrade -r requirements.txt`）

---

## ✅ 配置完成检查清单

- [ ] ✅ 从企业微信获取了 Webhook key
- [ ] ✅ 在 GitHub Secrets 中配置了 `WEIXIN_WEBHOOK_KEY`
- [ ] ✅ 手动触发过一次工作流
- [ ] ✅ 在企业微信群组中收到过推送
- [ ] ✅ Actions 工作流状态为绿色 ✅
- [ ] ✅ 验证自动定时执行已启用

---

## 🎉 完成！

你的系统现在已经完全配置好了：

✅ 每天自动爬取最新科技新闻
✅ 自动推送到企业微信群组
✅ 支持手动随时触发
✅ 完整的执行日志和监控

**如有问题**，查看详细日志或参考 `README.md`
