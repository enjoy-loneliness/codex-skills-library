# Skill 关联关系

本页描述 skills 之间的组合方式。可以把它当成推荐路线图：先选主入口，再按任务阶段叠加辅助 skill。

## 总览

```text
auto-content-factory-constitution
  -> auto-content-factory
      -> project-structure / database / prompt-library
      -> topic-score -> article -> publish -> analytics
      -> n8n / ai-agent / coding
      -> security / workflow-logging / testing / review / git
      -> monetization / optimization

wechat-mp-writer
  -> auto-content-factory-article
  -> auto-content-factory-publish

trading-ops
  -> trade-executor
  -> collab-project-sync-audit

uniapp-project-builder
  -> collab-project-sync-audit

tvbox-automation
  -> collab-project-sync-audit
```

## 内容工厂组合

### 1. 立项和系统边界

优先组合：

- `auto-content-factory-constitution`
- `auto-content-factory`
- `auto-content-factory-project-structure`
- `auto-content-factory-database`

适合问题：

- “我要设计一个自动内容工厂。”
- “这个系统边界是什么，哪些不该做？”
- “仓库和数据库怎么拆？”

### 2. 选题到文章生产

优先组合：

- `auto-content-factory-topic-score`
- `auto-content-factory-prompt-library`
- `auto-content-factory-article`
- `wechat-mp-writer`

适合问题：

- “帮我判断这些选题哪个更值得写。”
- “给我生成公众号文章。”
- “把这个工具整理成信息卡和文章草稿。”

### 3. 自动化工作流落地

优先组合：

- `auto-content-factory-n8n`
- `auto-content-factory-ai-agent`
- `auto-content-factory-coding`
- `auto-content-factory-workflow-logging`

适合问题：

- “用 n8n 搭 RSS 采集和 AI 评分流程。”
- “把内容工厂拆成多个 agent。”
- “给工作流补日志、重试和告警。”

### 4. 发布、复盘和增长

优先组合：

- `auto-content-factory-publish`
- `auto-content-factory-analytics`
- `auto-content-factory-monetization`
- `auto-content-factory-optimization`

适合问题：

- “发到公众号、知乎、掘金、小红书怎么排？”
- “这周哪些文章值得继续写？”
- “怎么降低成本并提高转化？”

### 5. 质量门禁

优先组合：

- `auto-content-factory-security`
- `auto-content-factory-testing`
- `auto-content-factory-review`
- `auto-content-factory-git`

适合问题：

- “上线前帮我检查安全和测试。”
- “这个工作流有没有日志、重试、脱敏和回放？”
- “帮我写提交信息和 PR 描述。”

## 独立能力组合

### uni-app 项目开发

主 skill：

- `uniapp-project-builder`

辅助 skill：

- `collab-project-sync-audit`：多人协作或部署前先同步状态。

推荐触发语：

```text
用 uniapp 开发一个 Vue 3 微信小程序项目。
用 uniapp 初始化一个 H5 网站。
用 uniapp 做一个多端项目，小程序和网页都要支持。
```

### 微信公众号写作

主 skill：

- `wechat-mp-writer`

可叠加：

- `auto-content-factory-topic-score`：先选题评分。
- `auto-content-factory-article`：文章生产和包装。
- `auto-content-factory-publish`：发布和多平台分发。
- `auto-content-factory-analytics`：发布后复盘。

### PDF 任务

主 skill：

- `pdf`

适合独立使用。若 PDF 是内容工厂产物，可在发布前叠加 `auto-content-factory-review` 做最终检查。

### 交易任务

主 skill：

- `trading-ops`

执行下单时才叠加：

- `trade-executor`

协作或部署前叠加：

- `collab-project-sync-audit`

注意：`trade-executor` 应只在用户明确要求下单、提交或执行交易时使用。

### TVBox 自动化

主 skill：

- `tvbox-automation`

协作或部署前叠加：

- `collab-project-sync-audit`

适合问题：

- “检查 TVBox 多源配置是否可用。”
- “回填片源健康状态。”
- “更新 Cloudflare KV 里的 FINAL_CONFIG/MULTI_CONFIG。”

## 推荐给别人的方式

按需求推荐，不要一次把全部 skills 都塞给对方：

- 做前端/小程序：推荐 `uniapp-project-builder`。
- 做公众号内容：推荐 `wechat-mp-writer`，需要自动化再加 ACF 套件。
- 做 PDF：推荐 `pdf`。
- 做多人项目：推荐 `collab-project-sync-audit`。
- 做完整内容工厂：推荐 `auto-content-factory` + ACF 子 skills。

涉及交易、私有服务器、账号、Webhook 或个人业务流程的 skills，先脱敏再分享。
