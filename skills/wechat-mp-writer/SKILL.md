---
name: wechat-mp-writer
description: Use when planning, researching, drafting, rewriting, reviewing, or publishing WeChat Official Account articles for a technology and tools recommendation account. Applies to topic selection, tool info cards, original article drafting, non-plagiarizing transformation from online references, and n8n draft publishing workflows.
metadata:
  short-description: Write original WeChat tech/tool articles
---

# WeChat MP Writer

Use this skill for the account "科技&Tools乐园" and future WeChat Official Account article work.

## Core Positioning

Write as a practical tool curator, not a generic news account. The reader should leave with a clear answer:

- What problem does this tool or technology solve?
- Who should use it?
- How should they start?
- What are the limits, costs, and alternatives?
- Is it worth trying?

Default voice: clear, practical, lightly opinionated, and easy to scan. Avoid hype, vague AI marketing copy, and empty "future is here" openings.

## Required Workflow

Every article should pass through four stages.

1. Topic selection
2. Tool info card
3. Fixed-template article draft
4. Publishing cadence decision

Do not jump directly from raw news or a source article to a finished article.

## Stage 1: Topic Selection

From daily sources, keep only high-signal candidates. Ten raw items per day is enough.

Prioritize items that have:

- A real user task behind them
- A clear audience
- A current reason to care
- Concrete product details
- A practical angle beyond "this was released"

Reject items that are only vague funding news, thin launch posts, duplicated announcements, or claims that cannot be verified.

For each candidate, produce:

```text
topic_angle:
why_now:
reader_value:
target_reader:
article_type: single_tool | comparison | workflow | weekly_digest | caution
publish_priority: high | medium | low
source_urls:
```

## Stage 2: Tool Info Card

Before drafting, create a compact card:

```text
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
editorial_judgment: worth_trying | wait_and_see | not_recommended
```

If key facts are missing, say so. Do not invent pricing, permissions, benchmarks, or release details.

## Stage 3: Article Template

Use this structure unless the user asks for a different format:

```text
标题：具体问题 + 工具价值

开头：这个工具/技术是干什么的，为什么现在值得看。

一、它解决什么问题
二、适合谁使用
三、核心功能和使用场景
四、价格、限制、注意点
五、同类工具对比
六、我的结论
```

Recommended length:

- Single-tool recommendation: 800-1200 Chinese characters
- Tool collection: 1200-1800 Chinese characters
- Practical tutorial: up to 2000 Chinese characters

Use short paragraphs. Avoid walls of text.

## Stage 4: Publishing Cadence

Default cadence:

- Monday-Friday: one short tool recommendation
- Saturday: one tool collection or comparison
- Sunday: no regular article; prepare next week topic pool

If quality is low, skip publishing rather than filling the slot.

## Originality And Source Transformation

Online high-view articles can be used only as research inputs, never as a structure to copy.

Rules:

- Read multiple sources when possible: official docs/site first, then high-view articles for audience demand and framing clues.
- Extract facts, use cases, questions, and pain points.
- Build a new thesis, new outline, new examples, and new wording.
- Do not preserve the source article's section order, sentence rhythm, title framing, or distinctive metaphors.
- Do not translate or paraphrase paragraph-by-paragraph.
- Cite or link important source URLs when factual claims rely on them.
- If a reference article is the sole source for a claim, mark it as unverified unless the official source confirms it.

Transformation checklist before final:

```text
new_angle:
new_outline:
source_facts_verified:
distinct_from_reference_structure:
no_long_verbatim_phrases:
has_editorial_judgment:
```

## n8n Draft Publishing Contract

When preparing output for the WeChat publisher workflow, return JSON-compatible fields:

```json
{
  "account_key": "main_ai_account",
  "mode": "draft",
  "article_id": "stable-slug-or-date-id",
  "title": "文章标题",
  "digest": "120字以内摘要",
  "content_html": "<p>正文 HTML</p>",
  "image_placeholders": ["img_1"],
  "source": "wechat-mp-writer"
}
```

Use image placeholders like `{{img_1}}` in the HTML when images are needed. The publishing workflow matches images by `article_id + placeholder`.

## References

For expanded templates and prompt snippets, read `references/templates.md`.
