# Skills 中文介绍

本页按用途分组介绍仓库内的 26 个自定义 skills。

## 内容工厂主线

| Skill | 中文介绍 | 推荐场景 |
| --- | --- | --- |
| `auto-content-factory` | 自动内容工厂的总入口，负责规划、设计、搭建和运营可变现的自动发布系统。 | 需要从选题采集、AI 评分、写作、审核、发布到数据反馈形成闭环时使用。 |
| `auto-content-factory-constitution` | 内容工厂的最高优先级宪章和 CTO 工作模式。 | 任何 ACF 相关任务开始前，用来校准范围、边界、优先级和不要做什么。 |
| `auto-content-factory-project-structure` | 规范内容工厂仓库结构、文件命名和目录归属。 | 新增工作流、提示词、脚本、文档、测试、日志或重构目录时使用。 |
| `auto-content-factory-database` | 设计和演进内容工厂的数据模型。 | 规划 Notion 数据库、发布队列、分析表、Prompt Library、Workflow Logs 或后续迁移到 PostgreSQL/Supabase/MySQL/SQLite。 |
| `auto-content-factory-prompt-library` | 设计、版本化和评审可复用提示词。 | 写 AI 评分、文章生成、JSON 抽取、修复、总结、改写、审稿等提示词时使用。 |
| `auto-content-factory-topic-score` | 评估和排序内容选题。 | 判断 AI 工具、自动化方案、GitHub 项目、RSS 条目、SEO 机会和变现潜力时使用。 |
| `auto-content-factory-article` | 写作、评估、改写和包装微信公众号文章。 | 面向“科技&Tools乐园”的工具推荐、教程、开源项目、n8n 案例和普通人赚钱工具文章。 |
| `auto-content-factory-publish` | 规划和执行多平台发布。 | 微信公众号、知乎、掘金、CSDN、小红书的标题、标签、封面、CTA、发布队列和失败重试。 |
| `auto-content-factory-analytics` | 采集、分析和复盘内容表现。 | 统计阅读、点赞、收藏、关注、收益、发布时间、标签表现，并更新 AI Memory。 |
| `auto-content-factory-monetization` | 评估内容和系统的变现能力。 | 判断选题、文章、工具评测、自动化案例能否带来增长、私域转化、课程、咨询、会员或广告价值。 |
| `auto-content-factory-optimization` | 优化内容工厂成本和效率。 | 降低 token、API 调用、重复扫描、重复生成、全量抓取和无效工作流运行。 |
| `auto-content-factory-ai-agent` | 设计 agent 化内容工厂架构。 | 拆分 Collector、Scorer、Writer、Reviewer、Publisher、Reporter、Optimizer 等角色和交接协议。 |
| `auto-content-factory-n8n` | 设计、生成、审查和优化 n8n 工作流。 | RSS/GitHub Trending 采集、Notion 入库、去重、AI 评分、文章生成、Telegram 审核、发布队列和日志。 |
| `auto-content-factory-coding` | 编写和审查内容工厂代码。 | 写服务、脚本、n8n Code 节点、集成、配置、测试和重构时使用。 |
| `auto-content-factory-testing` | 为模块和工作流设计测试。 | dry-run、mock、重放测试、错误场景、AI 失败、API 失败、超时、JSON 解析和上线前检查。 |
| `auto-content-factory-security` | 保护密钥、Webhook、日志、数据库和外部请求。 | 处理 API key、token、cookie、环境变量、日志脱敏、Webhook 校验、Git 安全和错误记录。 |
| `auto-content-factory-workflow-logging` | 设计追加式工作流日志和可观测性。 | 记录 n8n、服务、脚本、AI/API 调用、重试、错误、成本、token、模型和生产告警。 |
| `auto-content-factory-review` | 对完成的内容工厂改动做交付前评审。 | 任意模块、工作流、提示词、数据库、发布器、分析任务、测试或仓库改动完成后使用。 |
| `auto-content-factory-git` | 为内容工厂准备 Git 提交和 PR。 | 写 Conventional Commit、PR 描述、变更动机、影响、测试、风险和 checklist。 |

## 写作与内容

| Skill | 中文介绍 | 推荐场景 |
| --- | --- | --- |
| `wechat-mp-writer` | 面向技术和工具推荐类公众号的写作 skill。 | 选题、资料研究、工具信息卡、原创文章、非洗稿改写、n8n 草稿发布。 |

## 项目开发与协作

| Skill | 中文介绍 | 推荐场景 |
| --- | --- | --- |
| `uniapp-project-builder` | 初始化 Vue 3 uni-app 项目。 | 用户说“用 uniapp 开发网站/小程序/多端项目”时，自动生成 H5、微信小程序或多端项目骨架。 |
| `collab-project-sync-audit` | 多人协作项目改动前的同步和部署审计。 | 修改、部署、调试或 review 共享仓库前，检查本地、远端、生产环境是否一致。 |
| `pdf` | PDF 阅读、生成和版式检查。 | 需要渲染页面、检查视觉布局、抽取文本、生成 PDF 或审查 PDF 文件时使用。 |

## 交易与运维

| Skill | 中文介绍 | 推荐场景 |
| --- | --- | --- |
| `trading-ops` | Fangxing 交易项目运维 skill。 | Discord 信号解析、交易服务、n8n 交接、D1 清理、auto-trade 调试、Bitget/Binance 纸盘或实盘问题。 |
| `trade-executor` | 交易下单执行 skill。 | 用户明确要求通过已配置 n8n webhook 下单、提交或执行交易时使用。 |

## TVBox 自动化

| Skill | 中文介绍 | 推荐场景 |
| --- | --- | --- |
| `tvbox-automation` | TVBox/影视仓自动化运维 skill。 | n8n 片源采集、片源健康回填、GitHub Actions 更新、Cloudflare KV 配置和多源可用性检查。 |

## 公开推荐建议

通用性强、适合直接推荐给别人：

- `uniapp-project-builder`
- `wechat-mp-writer`
- `pdf`
- `collab-project-sync-audit`
- `auto-content-factory` 及其通用子 skills

强个人化或需要私有环境支持，推荐前应先脱敏和改造：

- `trading-ops`
- `trade-executor`
- `tvbox-automation`
- 含有个人品牌、账号、服务器、Webhook、数据库命名的 ACF 子 skills
