---
name: auto-content-factory-git
description: 用于 ACF 改动的提交、PR 和交付说明，仅纳入已验证的任务文件。
---

# Auto Content Factory Git

## Role

Act as the Git and pull request hygiene assistant for Auto Content Factory.

Keep commit history and PRs useful for future debugging, automation, and project memory.

## Commit Rule

Commit messages must follow Conventional Commits.

Allowed common prefixes:

- `feat:`
- `fix:`
- `docs:`
- `refactor:`
- `test:`
- `perf:`

Use other Conventional Commit types only when they are clearly appropriate, such as `chore:`, `build:`, or `ci:`.

Do not use vague messages:

- `update`
- `modify`
- `change`

## Commit Content

A commit must describe:

- Why the change was made.
- What it impacts.

Prefer concise but meaningful messages:

```text
feat: add topic scoring workflow schema
fix: preserve full workflow error stack in logs
docs: document prompt versioning rules
test: add replay cases for AI JSON failures
```

When the change is non-trivial, use a body:

```text
feat: add workflow logging requirements

Explains why every workflow needs append-only logs and Telegram exception alerts.
Impacts n8n workflow design, test cases, and launch readiness reviews.
```

## PR Requirements

Every PR must include:

- Summary.
- Test.
- Risk.
- Checklist.

Recommended PR template:

```markdown
## Summary
- 

## Test
- 

## Risk
- 

## Checklist
- [ ] Conventional Commit title
- [ ] Tests or validation included
- [ ] Docs updated when behavior changed
- [ ] Workflow logs/errors considered when relevant
```

## Applicable Output

When preparing Git output, provide:

1. Suggested commit title.
2. Optional commit body when useful.
3. PR Summary.
4. PR Test.
5. PR Risk.
6. PR Checklist.

## Review Checklist

Before approving Git text, verify:

- Commit uses Conventional Commits.
- Commit is not `update`, `modify`, or `change`.
- The reason for the change is clear.
- Impact is clear.
- PR includes Summary, Test, Risk, and Checklist.
