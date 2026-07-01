# Templates

## Topic Selection Prompt

```text
你是“科技&Tools乐园”的选题编辑。请从候选资讯里筛选最多 3 个适合公众号的选题。

要求：
- 不追热点空话，只选有真实用户任务的内容。
- 给出 topic_angle、reader_value、target_reader、publish_priority。
- 如果信息不足，标记 missing_facts。
```

## Info Card Prompt

```text
请把这个工具/技术整理成资料卡：

tool_name:
official_site:
source_urls:
problem_solved:
target_users:
core_features:
best_use_cases:
pricing_or_limits:
setup_difficulty:
risks_or_caveats:
alternatives:
editorial_judgment:

不要编造未验证事实。
```

## Article Draft Prompt

```text
请基于资料卡写一篇微信公众号文章，账号定位是“科技工具筛选 + 上手说明 + 值不值得用”。

结构：
标题：具体问题 + 工具价值
开头：这个工具/技术是干什么的，为什么现在值得看。
一、它解决什么问题
二、适合谁使用
三、核心功能和使用场景
四、价格、限制、注意点
五、同类工具对比
六、我的结论

要求：
- 800-1200 字。
- 口吻清楚、实用、少营销腔。
- 有明确判断，不要只罗列功能。
- 重要事实来自 source_urls，不确定就写“暂未确认”。
```

## Rewrite From Popular Articles Prompt

```text
请把这些高浏览文章只当作研究材料，而不是改写底稿。

任务：
1. 提取它们共同关注的用户痛点。
2. 提取可以被官方来源验证的事实。
3. 重新设计一个不同的文章角度和大纲。
4. 写一篇原创文章，不沿用原文标题、结构、段落顺序、比喻和表达。
5. 最后列出 transformation_checklist。

禁止：
- 段落级改写。
- 翻译式改写。
- 保留原文叙事顺序。
- 使用原文独特表达。
```
