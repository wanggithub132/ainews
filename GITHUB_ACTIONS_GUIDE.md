# 🚀 GitHub Actions 工作流配置指南

## 📋 概述

本项目已配置了 3 个完整的 GitHub Actions 工作流，支持自动爬虫执行、代码质量检查和安全扫描。

---

## 📁 工作流文件

所有工作流文件位于 `.github/workflows/` 目录：

```
.github/workflows/
├── daily-scraper.yml        # 基础爬虫工作流 (推荐使用)
├── scraper-advanced.yml     # 高级爬虫工作流 (自动重试)
└── quality-check.yml        # CI/CD 代码质量检查
```

---

## 🎯 工作流详细说明

### 1️⃣ daily-scraper.yml (推荐)

**用途**: 每天定时爬取新闻并推送到企业微信

**触发条件**:
- ⏰ 每天 UTC 9:00 (北京时间 17:00) 自动运行
- 🎮 支持手动触发 (Actions 标签 → Run workflow)

**执行步骤**:
```
1. 检出代码
2. 安装 Python 3.11
3. 安装依赖 (使用 pip cache 加速)
4. 验证依赖包
5. 运行爬虫脚本
6. 输出执行状态
```

**配置要求**:
- ✅ 需要配置 GitHub Secret: `WEIXIN_WEBHOOK_KEY`

**预期输出**:
```
==========================================
🤖 Tech News Scraper Starting
==========================================
[爬虫执行日志...]
==========================================
✅ Scraper completed
==========================================
✅ Workflow Status: success
⏰ Execution Time: [时间戳]
```

---

### 2️⃣ scraper-advanced.yml (高级)

**用途**: 支持自动重试的高级爬虫工作流

**特点**:
- 🔄 自动重试机制 (最多 3 次)
- 📊 详细的执行日志
- 🚨 失败通知 (当所有重试都失败)
- ⏰ 多个触发时间 (09:00 UTC 和 14:00 UTC)

**触发条件**:
- ⏰ 每天 UTC 9:00 (北京时间 17:00) - 主执行
- ⏰ 每天 UTC 14:00 (北京时间 22:00) - 备用执行
- 🎮 支持手动触发

**执行流程**:
```
1. 第 1 次尝试
   ↓
2. 如果失败 → 第 2 次尝试
   ↓
3. 如果失败 → 第 3 次尝试
   ↓
4. 全部成功 → ✅ 完成
5. 全部失败 → 发送失败通知
```

**优势**:
- ✅ 更高的成功率
- ✅ 网络抖动时自动恢复
- ✅ 详细的执行日志

---

### 3️⃣ quality-check.yml (CI/CD)

**用途**: 代码质量和安全检查

**触发条件**:
- 📤 Push 到 main/master/develop 分支
- 🔄 PR 到 main/master/develop 分支
- 🎮 手动触发

**执行内容**:

#### 质量检查 (quality-check):
- ✅ 检查依赖完整性
- ✅ Black 代码风格检查
- ✅ isort 导入顺序检查
- ✅ Flake8 代码规范检查
- ✅ Pytest 单元测试
- ✅ 模块导入测试
- ✅ 脚本执行测试

#### 安全检查 (security-check):
- 🔒 Bandit 安全扫描
- 🔐 检查是否有暴露的密钥

#### 依赖检查 (dependency-check):
- 📦 检查已知的漏洞 (Safety)
- 📊 列出所有依赖版本

**最终检查 (final-check)**:
- 汇总所有检查结果
- 失败则标记 PR

---

## ⚙️ 配置步骤

### Step 1: 配置 GitHub Secret (必需)

**目的**: 安全地存储企业微信 Webhook Key

**操作步骤**:
```
1. 进入 GitHub 仓库
2. Settings → Secrets and variables → Actions
3. 点击 "New repository secret"
4. Name: WEIXIN_WEBHOOK_KEY
5. Value: 你的企业微信 Webhook Key
   (从 URL 中提取: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY)
6. 点击 "Add secret"
```

**验证**:
- ✅ 创建后立即可用
- ✅ 在 workflow 文件中通过 `${{ secrets.WEIXIN_WEBHOOK_KEY }}` 访问

### Step 2: 启用 Actions (如需要)

```
1. 进入仓库 → Actions 标签
2. 如果显示 "Actions are disabled"
3. 点击 "I understand my workflows, go ahead and enable them"
```

### Step 3: 验证工作流

```
1. 推送代码到仓库
2. 进入 Actions 标签
3. 查看工作流是否出现
4. 点击手动触发测试
```

---

## 🎮 手动触发工作流

### 方式 1: 在 GitHub UI 中触发

```
1. 仓库 → Actions 标签
2. 选择要运行的工作流
   - "Daily Tech News Scraper"
   - "Advanced Tech News Scraper with Retry"
   - "CI/CD Quality Check"
3. 点击 "Run workflow" 按钮
4. 在弹出对话框中点击 "Run workflow"
```

### 方式 2: 使用 GitHub CLI

```bash
# 查看可用的工作流
gh workflow list

# 触发特定工作流
gh workflow run daily-scraper.yml

# 查看工作流运行状态
gh run list --workflow=daily-scraper.yml
```

---

## 📊 查看执行日志

### 查看工作流运行历史

```
1. 仓库 → Actions 标签
2. 在左侧选择工作流
3. 查看所有运行记录
```

### 查看详细日志

```
1. 点击具体的运行记录
2. 展开要查看的 step
3. 查看完整的输出日志
```

### 下载工作流日志

```
1. 点击运行记录右上角的 "..."
2. 选择 "Download logs"
3. 解压查看所有 step 的日志
```

---

## ⏱️ 执行时间配置

### 修改定时执行时间

编辑 `.github/workflows/daily-scraper.yml`:

```yaml
on:
  schedule:
    # 修改这里的 cron 表达式
    # 格式: 分钟 小时 日期 月份 星期
    - cron: '0 9 * * *'    # 每天 UTC 9:00
```

**常见时间设置**:

| 需求 | Cron 表达式 | 说明 |
|------|-----------|------|
| 每天 09:00 UTC | `0 9 * * *` | 北京时间 17:00 |
| 每天 14:00 UTC | `0 14 * * *` | 北京时间 22:00 |
| 每 6 小时 | `0 */6 * * *` | 00:00, 06:00, 12:00, 18:00 |
| 每周一 09:00 | `0 9 * * 1` | 周一 UTC 9:00 |
| 工作日 09:00 | `0 9 * * 1-5` | 周一至周五 |

**Cron 参考**:
```
┬ ┬ ┬ ┬ ┬
│ │ │ │ └─ 星期 (0-6, 0=周日)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

---

## 🔍 故障排查

### 问题 1: 工作流不执行

**可能原因**:
- ❌ Actions 未启用
- ❌ 工作流文件有语法错误
- ❌ Secret 未配置

**解决**:
```
1. 检查 Actions 是否启用
2. 验证 YAML 语法: https://www.yamllint.com/
3. 检查 Secret 是否配置
4. 查看详细日志
```

### 问题 2: 爬虫执行失败

**可能原因**:
- ❌ 网络连接问题
- ❌ RSS 源无法访问
- ❌ WeChat API 限制

**解决**:
```
1. 查看详细的错误日志
2. 手动测试爬虫: python scraper.py
3. 检查网络连接
4. 检查 WeChat API 状态
```

### 问题 3: Secret 不生效

**可能原因**:
- ❌ Secret 名字拼写错误
- ❌ Secret 值为空

**解决**:
```
1. 检查 Secret 名字大小写
2. 确认 Secret 值不为空
3. 重新生成 Secret
4. 仓库访问权限检查
```

---

## 📈 监控和告警

### 配置工作流通知

**GitHub 内置通知**:
1. Watch 仓库
2. 配置通知设置
3. 关注 Actions 运行

**第三方集成**:
- Slack 通知
- Email 通知
- Discord 通知

### 监控执行统计

```
Actions 标签 → All workflows → 查看运行统计

统计信息包括:
- ✅ 成功次数
- ❌ 失败次数
- ⏱️ 平均执行时间
- 📊 执行趋势
```

---

## 🔒 安全最佳实践

### ✅ Do's (应该做)

- ✅ 使用 GitHub Secrets 存储敏感信息
- ✅ 定期轮换 API Keys
- ✅ 限制 Secret 访问权限
- ✅ 使用 OIDC tokens 替代 Personal Access Tokens
- ✅ 定期审计工作流日志
- ✅ 启用 branch protection rules

### ❌ Don'ts (不应该做)

- ❌ 在代码中硬编码 API Keys
- ❌ 在 workflow 日志中输出 Secrets
- ❌ 提交包含敏感信息的文件
- ❌ 在 public 仓库中存储敏感 Secrets
- ❌ 使用弱密码

---

## 📚 相关资源

### 官方文档
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Workflow 语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Cron 时间表](https://crontab.guru/)

### 工具
- YAML 验证: https://www.yamllint.com/
- Cron 生成器: https://crontab.guru/
- Secret 管理: https://docs.github.com/en/actions/security-guides/encrypted-secrets

---

## ✨ 快速开始检查清单

- [ ] 创建 `.github/workflows/` 目录
- [ ] 放入 3 个工作流 YAML 文件
- [ ] 配置 GitHub Secret: `WEIXIN_WEBHOOK_KEY`
- [ ] 启用 Actions (如需要)
- [ ] 推送代码到 GitHub
- [ ] 手动触发工作流测试
- [ ] 查看执行日志
- [ ] 验证企业微信收到推送
- [ ] 配置每日定时执行时间
- [ ] 完成！

---

## 💡 常见问题

### Q: 工作流多久执行一次？
A: 
- daily-scraper.yml: 每天 1 次 (UTC 9:00)
- scraper-advanced.yml: 每天 2 次 (UTC 9:00 和 14:00)
- quality-check.yml: 每次 push/PR 时执行

### Q: 如何修改执行时间？
A: 编辑工作流文件中的 cron 表达式，参考上面的时间配置部分

### Q: 工作流失败了怎么办？
A: 查看 Actions 标签中的详细日志，参考故障排查部分

### Q: 如何禁用某个工作流？
A: 工作流文件重命名 (添加 .disabled 后缀) 或删除

### Q: Secret 过期了怎么办？
A: 重新生成新的 Webhook Key，更新 GitHub Secret

---

**工作流配置完成！** ✅

现在你的项目具有：
- ✅ 每日自动爬虫执行
- ✅ 自动重试机制
- ✅ 代码质量检查
- ✅ 安全扫描
- ✅ 完整的监控日志
