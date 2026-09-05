---
name: auto-content-factory-project-structure
description: 用于 ACF 新文件归属、目录整理和结构调整，沿用已有约定。
---

# Auto Content Factory Project Structure

## Role

Act as the repository structure guardian for Auto Content Factory.

Keep the project organized so workflows, prompts, services, tests, docs, logs, and assets remain maintainable as the system grows.

## Required Directories

Use these top-level directories:

- `docs`
- `config`
- `database`
- `n8n`
- `scripts`
- `services`
- `prompts`
- `tests`
- `logs`
- `assets`

Create only the directories needed for the current work, but keep new files aligned with this structure.

## Placement Rules

Do not put all files in the repository root.

Use:

- `docs/` for architecture, module docs, operating guides, and decisions.
- `config/` for environment examples and non-secret configuration.
- `database/` for Notion schemas, SQL migrations, and database documentation.
- `n8n/` for workflow JSON and workflow examples.
- `scripts/` for runnable maintenance or import/export scripts.
- `services/` for application/service code.
- `prompts/` for prompt files.
- `tests/` for test cases, fixtures, mocks, and replay payloads.
- `logs/` for local sample logs only; production logs should go to the configured database or log store.
- `assets/` for images, templates, and static assets.

## Documentation Rules

README must be updated when setup, commands, directory structure, or user-facing behavior changes.

Docs must be synced when architecture, workflow behavior, database schema, prompt contracts, or launch/test requirements change.

Do not let implementation drift away from docs.

## Workflow and Prompt Rules

Use one file per workflow.

Use one file per prompt.

Name files clearly with module and purpose, for example:

- `n8n/workflows/rss_collect_raw_articles.json`
- `n8n/workflows/topic_score_candidates.json`
- `prompts/topic_score.v1.md`
- `prompts/article_generate_wechat.v1.md`

## Applicable Output

When organizing project files, output:

1. Proposed file locations.
2. Why each file belongs there.
3. README changes needed.
4. Docs changes needed.
5. Workflow file boundaries.
6. Prompt file boundaries.

## Review Checklist

Before approving a file layout, verify:

- Files are not dumped into the root.
- Required directories are used consistently.
- README impact is considered.
- Docs impact is considered.
- Each workflow has one file.
- Each prompt has one file.
