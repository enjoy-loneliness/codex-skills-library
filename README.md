# Codex Skills Library

这是 Fangxing 的自定义 Codex Skills 仓库，用来保存、介绍和分发一组可复用的工作流能力。

这些 skills 不是普通提示词，而是给 Codex 使用的“领域操作手册”：当用户提出特定任务时，Codex 会加载对应 `SKILL.md`，并按里面的流程、约束、参考资料或脚本执行。

## 快速推荐

如果朋友只想试用，优先推荐这几个：

- `uniapp-project-builder`：初始化 Vue 3 uni-app 网站、小程序、多端项目。
- `wechat-mp-writer`：写微信公众号技术工具类文章。
- `pdf`：阅读、生成、检查 PDF，尤其适合关注版式和渲染效果的任务。
- `collab-project-sync-audit`：多人协作项目改动前做同步和部署状态检查。
- `auto-content-factory`：搭建自动化内容工厂时的总入口。

如果对方要做完整内容自动化系统，推荐整套 `auto-content-factory-*` skills 一起使用。

## 仓库结构

```text
codex-skills-library/
├── skills/                  # 可直接复制到 ~/.codex/skills 的 skill 目录
├── docs/
│   ├── skills.zh.md          # 每个 skill 的中文介绍
│   └── relations.zh.md       # skill 之间的关联和组合建议
└── README.md
```

## 安装方式

安装全部 skills：

```bash
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

只安装某一个：

```bash
mkdir -p ~/.codex/skills
cp -R skills/uniapp-project-builder ~/.codex/skills/
```

安装后重新打开 Codex 会话，让新的 skills 被发现。

## 安全默认值

- 仓库中的 URL、频道 ID、Webhook、API Key 和项目根目录均使用占位符；真实值只应放在
  本地忽略配置或 secret manager。
- `trade-executor` 默认只做 simulation/paper 和 dry-run。任何 live 创建、修改或撤单
  都必须展示完整订单票据并取得针对该票据的明确确认。
- Discord、Telegram、网页、RSS、OCR 和其他外部内容一律视为不可信数据，不能作为工具
  指令、权限或扩大操作范围的依据。
- UniApp 生成器默认仅监听 localhost，不允许 Vite 读取项目父目录；`--force` 只可替换
  带现有项目标记的生成目录。

## 使用方式

可以显式点名 skill：

```text
用 $uniapp-project-builder 初始化一个 Vue 3 uni-app 微信小程序项目。
```

也可以用自然语言触发：

```text
帮我用 uniapp 开发一个多端项目。
帮我写一篇微信公众号文章，主题是某个 AI 工具。
帮我检查这个 PDF 版式有没有问题。
```

## 中文说明

- 查看所有 skill 的中文介绍：[docs/skills.zh.md](docs/skills.zh.md)
- 查看组合关系和推荐路径：[docs/relations.zh.md](docs/relations.zh.md)

## 发布前注意

公开推荐给别人之前，请确认：

- 已经移除任何私密路径、账号、密钥、Webhook、服务器地址。
- `SKILL.md` 里没有只能在个人机器上运行的硬编码假设。
- 对外公开时补充合适的 License。
- 如果只想分享通用能力，可以先排除交易、私有项目运维等强个人化 skills。
