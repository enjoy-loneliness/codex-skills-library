---
name: auto-content-factory-workflow-logging
description: 用于设计或修复 ACF 运行日志、失败诊断和成本可观测性。
---

# Auto Content Factory Workflow Logging

## Role

Act as the workflow logging and observability guardian for Auto Content Factory.

Every workflow must record logs. No production workflow should run without success, skip, retry, and error logs.

## Required Log Fields

Every workflow run must record:

- `workflow_name`
- `run_id`
- `status`
- `duration`
- `retry`
- `error`
- `input`
- `output`
- `api_cost`
- `token`
- `model`

Recommended additional fields:

- `started_at`
- `finished_at`
- `related_record_id`
- `platform`
- `source`
- `prompt_id`
- `prompt_version`
- `node_name`
- `error_type`
- `stack`

## Append-Only Rule

Logs must be append-only.

Do not overwrite prior log records.

If a workflow retries, create a new log entry or append a retry event record with the same `run_id` and incremented `retry`.

If a later step changes final status, write a new status event rather than mutating away the original failure context.

## Error Rule

Errors must preserve the full stack trace when available.

Store:

- Error message.
- Full stack.
- Failing node or step.
- Input snapshot or input reference.
- Output snapshot when partial output exists.
- Retry count.
- Whether Telegram was notified.

All exceptions must notify Telegram unless the workflow is running in an explicit dry-run or mock mode.

## Status Values

Prefer:

- `started`
- `success`
- `skipped`
- `partial_success`
- `retrying`
- `failed`

Use consistent status values across workflows so analytics can aggregate reliability.

## Applicable Output

When designing logging for a workflow, output:

1. Log destination.
2. Required fields.
3. Success log behavior.
4. Skip log behavior.
5. Retry log behavior.
6. Error log behavior.
7. Telegram notification behavior.
8. Cost, token, and model tracking.
9. Example log record.
10. How to test logging.

## Review Checklist

Before approving a workflow, verify:

- It writes logs on success and failure.
- Logs are append-only.
- Errors include full stack traces when available.
- Telegram is notified for exceptions.
- API cost, token, and model are recorded for AI/API calls.
- Retries are traceable.
