---
name: auto-content-factory-publish
description: Plan and operate platform-specific publishing for Auto Content Factory. Use when preparing WeChat Official Account publishing, Zhihu, Juejin, CSDN, Xiaohongshu distribution, platform-specific publishers, titles, tags, covers, CTAs, prompts, retry queues, Telegram failure notifications, or multi-platform automated publishing workflows.
---

# Auto Content Factory Publish

## Role

Act as the publishing architect for Auto Content Factory.

Default platform: WeChat Official Account.

Later platforms:

- Zhihu.
- Juejin.
- CSDN.
- Xiaohongshu.

Do not add other publishing platforms unless the user explicitly asks and the addition serves automated publishing.

## Publisher Boundary

Each platform must have an independent Publisher.

Do not build one workflow that publishes to every platform.

Each platform must have independent:

- Publisher workflow.
- Prompt.
- Title.
- Tags.
- Cover.
- CTA.
- Formatting rules.
- Success and failure logs.

Use shared upstream records, but keep publishing execution platform-specific.

## Platform Packaging

For each platform, prepare:

1. Platform name.
2. Publisher workflow name.
3. Source draft ID.
4. Platform-specific title.
5. Platform-specific summary.
6. Platform-specific body.
7. Platform-specific tags.
8. Platform-specific cover prompt or asset.
9. Platform-specific CTA.
10. Prompt ID and version.
11. Publish status.
12. Scheduled time.
13. Retry state.

## Failure Handling

If publishing fails, move the item into Retry Queue.

Track:

- `platform`
- `publisher_name`
- `source_record_id`
- `error_message`
- `retry_count`
- `last_retry_at`
- `next_retry_at`
- `status`

If publishing fails continuously, notify Telegram.

Continuous failure means repeated failures after the configured retry limit, or any permission/authentication failure that requires human action.

## Workflow Rules

Every Publisher workflow must include:

- Trigger from Publish Queue or manual test input.
- Input validation.
- Platform formatting.
- Platform publish or assisted-publish step.
- Published record write.
- Workflow log write.
- Retry Queue write on failure.
- Telegram notification for repeated or human-action failures.

## Review Checklist

Before returning a publishing plan, verify:

- WeChat is treated as the default platform.
- Each platform has an independent Publisher.
- No workflow publishes to all platforms at once.
- Each platform has independent title, tags, cover, CTA, and prompt.
- Failures enter Retry Queue.
- Repeated failures notify Telegram.
