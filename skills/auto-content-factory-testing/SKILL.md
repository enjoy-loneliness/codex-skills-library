---
name: auto-content-factory-testing
description: 用于为 ACF 变更选择和实现相关回归、mock 或 replay 验证。
---

# Auto Content Factory Testing

## Role

Act as the testing and launch-readiness guardian for Auto Content Factory.

Any developed module must include tests before launch. Any workflow without tests is not allowed to go online.

## Required Test Cases

Select tests for the actual behavior and failure modes changed; do not add irrelevant API/AI/JSON cases or tests that mirror implementation:

- Normal data.
- Empty data.
- Duplicate data.
- Abnormal data.
- API failure.
- AI failure.
- Timeout.
- JSON error.

Add module-specific cases when needed, such as permission failure, missing Notion relation, invalid Telegram command, publish failure, or partial API response.

## Workflow Test Modes

Workflows that mutate state or call external services need appropriate safe validation modes:

- Dry Run: execute logic without writing or publishing irreversible changes.
- Mock: replace external APIs, AI calls, Notion writes, Telegram messages, and publishers with controlled fake responses.
- Replay: rerun from captured input, prior log record, or saved failed execution payload.

These modes must be clear in config or input flags.

## Launch Rule

No tests, no launch.

Do not mark a workflow production-ready until:

- Required cases exist.
- Dry Run works.
- Mock works for external dependencies.
- Replay works for failures or captured examples.
- Logs are checked for success and failure paths.

## Applicable Output

When designing tests, output:

1. Module or workflow under test.
2. Test scope.
3. Required test cases.
4. Dry Run behavior.
5. Mock strategy.
6. Replay strategy.
7. Expected outputs.
8. Required log assertions.
9. Launch readiness result.

## Review Checklist

Before approving a module or workflow, verify:

- Normal, empty, duplicate, abnormal, API failure, AI failure, timeout, and JSON error cases are covered.
- Dry Run exists.
- Mock exists.
- Replay exists.
- Failure paths write logs.
- The workflow is blocked from launch if tests are missing.
