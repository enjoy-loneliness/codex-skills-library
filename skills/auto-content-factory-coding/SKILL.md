---
name: auto-content-factory-coding
description: 用于实现或评审 ACF 服务、脚本及集成代码，保持已有模块职责。
---

# Auto Content Factory Coding

## Role

Act as the coding quality guardian for Auto Content Factory.

Write code that is simple, modular, maintainable, and testable. Prefer boring, reliable code over clever code.

## Code Principles

Always optimize for:

- Simplicity.
- Modularity.
- Maintainability.
- Testability.

Each function must have a single responsibility.

Split files or modules before they become hard to understand. Do not allow source files, scripts, or large n8n Code nodes to exceed 500 lines without a clear reason and a refactor plan.

## Naming Rules

Use English names.

Use `camelCase` for variables and ordinary JavaScript/TypeScript identifiers unless the language or existing codebase uses another established convention.

Keep naming consistent across modules, workflows, payloads, and tests.

Use `snake_case` only for database fields and external schemas that require it.

## Configuration Rules

Do not hard-code configuration.

Move configuration into:

- `.env`
- `.env.example`
- `config/`
- runtime environment variables
- deployment secrets

Examples of configuration:

- API base URLs.
- Model names.
- Temperature.
- Notion database IDs.
- Telegram chat IDs.
- Webhook URLs.
- Retry limits.
- Timeout values.
- Feature flags.

## Secret Rules

Never commit secrets to Git.

Secrets include:

- API keys.
- Tokens.
- Cookies.
- Webhook secrets.
- Passwords.
- Private keys.

Use `.env` for local secrets and keep `.env` ignored by Git. Provide `.env.example` with placeholder values only.

## Applicable Output

When implementing or reviewing code, report:

1. Modules changed.
2. Configuration required.
3. Secrets required.
4. Tests added or needed.
5. Any file or function that should be split.
6. Any hard-coded value removed or still present.

## Review Checklist

Before delivering code, verify:

- Functions have single responsibility.
- Files and large Code nodes stay under 500 lines or have a refactor plan.
- Variables use consistent English naming.
- Configuration is not hard-coded.
- Secrets are not committed.
- `.env.example` exists when env vars are required.
- Code can be tested independently.
