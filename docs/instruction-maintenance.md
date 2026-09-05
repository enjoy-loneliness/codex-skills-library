# 指令维护与回归

使用最小、可判定的技能描述，只读相关流程。当前用户要求和现行仓库 ADR 优先；不要把可逆步骤或已授权交付拆成重复审批。

工具入口：

- `python3 skills/collab-project-sync-audit/scripts/workflow_preflight.py --repo <repo> --file <relative-file>`：只读状态、文件归属与 Python/Docker 版本检查，不执行 Git 同步或部署。
- `python3 skills/instruction-maintenance/scripts/instruction_health.py --manifest <targets.json>`：预算、失效条款、来源副本和保留的 provider 检查。提供 `--state` 才保存通知去重状态。
- `python3 -B skills/instruction-maintenance/scripts/test_workflow_tools.py`：隔离临时 Git 仓库、带空格文件、丢失关键文件、路径边界、镜像漂移、预算和通知恢复回归。

历史经验只转为有明确触发/退出条件的规则。不把一次登录过期、仓库删除或统计排名固化为长期事实。保留实盘票据、秘密、生产删除、不可逆动作与真实权限边界。
