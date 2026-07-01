---
name: auto-content-factory-n8n
description: Design, generate, review, and optimize modular n8n workflows for the Auto Content Factory automated publishing system. Use when creating n8n workflows for RSS or GitHub Trending collection, Notion storage, deduplication, AI topic scoring, WeChat article generation, Telegram review, publishing queues, analytics collection, workflow logs, error handling, or any n8n automation in the content factory.
---

# Auto Content Factory n8n

## Role

Act as the n8n Workflow architect for Auto Content Factory.

Design, generate, and optimize n8n workflows for the automated content publishing system. Keep workflows modular, testable, observable, and aligned with the WeChat Official Account path first.

## Workflow Contract

Every workflow must include these stages unless there is a clear reason to omit one:

1. Trigger
2. Input Normalize
3. Main Process
4. AI Process, when needed
5. Database Write
6. Log Write
7. Error Handling
8. Notification, when needed

Do not design a large all-in-one workflow. Split by responsibility and let workflows pass records through Notion status fields, webhook triggers, or queue tables.

## Node Naming

Use explicit node names that reveal intent and domain.

Good examples:

- Trigger - Daily Collect
- HTTP - Fetch GitHub Trending
- Code - Normalize Articles
- Notion - Save Raw Articles
- AI - Score Topic
- Code - Parse AI Result
- Telegram - Send Review Message
- Notion - Update Status
- Log - Write Workflow Log
- Error - Notify Admin

Do not use vague names:

- Node 1
- Code
- HTTP Request
- Untitled
- Test

## Required Output Format

When designing a workflow, output:

1. Workflow name.
2. Workflow goal.
3. Trigger method.
4. Input data.
5. Output data.
6. Node list.
7. Purpose of each node.
8. Key expressions.
9. Error handling.
10. Log fields.
11. Test method.
12. Future extension points.

When generating workflow JSON, also explain any credentials, environment variables, Notion database IDs, and webhook URLs that must be configured by the user.

## Standard Workflow Types

Prioritize these workflow boundaries.

### Content Collection Workflow

Use for:

- RSS collection.
- GitHub Trending collection.
- Product Hunt collection.
- Hacker News collection.
- Official blog collection.

Output to Raw Articles.

### Dedup Workflow

Use for:

- URL deduplication.
- Similar-title deduplication.
- Summary/content deduplication.

Output deduplicated Raw Articles and update duplicate status when needed.

### AI Topic Scoring Workflow

Use for:

- Deciding whether content is worth writing.
- Judging WeChat Official Account fit.
- Judging commercial value.
- Judging reader appeal.
- Judging suitability for secondary creation.

Output to Topics.

### Article Generation Workflow

Use for:

- Generating WeChat article drafts from selected topics.
- Generating titles.
- Generating summaries.
- Generating body content.
- Generating cover image prompts.
- Generating tags and keywords.

Output to Drafts.

### Review Workflow

Use for:

- Sending Telegram review messages.
- Receiving user approval commands.
- Updating Notion status.
- Triggering the publish queue.

Output to Publish Queue.

The review workflow must authenticate both the platform request and the human actor. Verify an
allowlisted reviewer user/chat ID or role, bind the command to the original review message and
record ID, reject stale or replayed commands, and make every state transition idempotent.

### Publishing Workflow

Use for:

- Publishing or assisting publishing to WeChat Official Account.
- Later publishing to Zhihu, Xiaohongshu, Juejin, and CSDN.

Output to Published Articles.

### Analytics Workflow

Use for:

- Collecting reads.
- Collecting likes.
- Collecting saves.
- Collecting comments.
- Collecting follower changes.
- Collecting revenue data.

Output to Analytics.

## Error Handling

Every workflow must handle:

- API request failure.
- AI invalid output format.
- Notion write failure.
- Duplicate data.
- Empty data.
- Missing fields.
- Timeout.
- Permission failure.

Write every error to Workflow Logs. Include enough data to retry or inspect the failed item without rereading the whole execution.

Recommended error pattern:

1. Validate required fields early.
2. Use explicit branches for empty and duplicate data.
3. Add AI output parsing after every AI node.
4. Route JSON parse failures to an AI repair step or an error branch.
5. Write Workflow Logs for both success and failure.
6. Notify the admin for errors that require human action.

## Log Fields

Record these fields for every execution:

- workflow_name
- run_id
- status
- input_count
- output_count
- error_message
- started_at
- finished_at
- duration
- related_record_id
- retry_count

Use `success`, `partial_success`, `skipped`, and `failed` status values unless the target schema already defines another controlled list.

## AI Node Rules

Prefer JSON output for AI nodes.

After every AI node:

1. Add a parse node.
2. Validate required fields.
3. Validate value ranges when scoring.
4. Route invalid JSON to a repair branch or error branch.
5. Save prompt name and prompt version in the related record or log.

Do not rely on raw prose AI output for downstream automation.

Before every AI node, keep collected source text in a delimited untrusted-data field and include the
shared Prompt Library instruction-injection boundary. After parsing, allow only declared fields and
state transitions. AI output must never directly publish, blacklist, retrieve secrets, or invoke
privileged tools.

## Telegram Review Rules

Review messages must include:

- Title.
- Score.
- Recommendation reason.
- Content source.
- Original link.
- Operation commands.

Use this command pattern by default:

```text
回复：
1 = 生成文章
2 = 跳过
3 = 加入待定
4 = 拉黑来源
```

The review workflow must update Notion status based on the reply and log the reviewer action only
after all of these checks pass:

- Telegram webhook/source authenticity.
- Reviewer user ID, chat ID, and required role allowlist.
- Reply-to/original message ID and target Notion record binding.
- Timestamp/replay window and idempotency key.
- Explicit authorization for high-impact actions such as blacklisting or advancing to live
  publication.

## Development Priority

Implement first:

1. RSS and GitHub Trending collection.
2. Notion storage.
3. AI topic scoring.
4. Telegram review.
5. WeChat article generation.

Defer until the core loop works:

- Full automatic publishing.
- Multi-platform synchronization.
- Complex analytics.
- Automatic monetization recommendation.

## Design Checklist

Before returning a workflow design or JSON, verify:

- The workflow has a clear module boundary.
- Node names are specific.
- Raw Articles, Topics, Drafts, Publish Queue, Published Articles, Analytics, and Workflow Logs remain separate.
- Prompts are versioned outside the node body when AI is used.
- Success and failure paths both write logs.
- Empty, duplicate, and malformed data paths are handled.
- The workflow can be tested independently with a small sample input.
