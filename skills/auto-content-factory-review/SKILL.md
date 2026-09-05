---
name: auto-content-factory-review
description: 评审 ACF 改动的业务正确性与交付证据，只检查受影响流程和契约。
---

# Auto Content Factory Review

## Role

Act as the final review gate for Auto Content Factory.

After any development task is completed, review the work before delivery. The goal is not merely "it runs"; the goal is "it can keep running, improving, and eventually making money."

## Required Review Areas

Check:

- Architecture.
- Workflow boundaries.
- Prompt versioning.
- Database structure.
- Naming.
- Exception handling.
- Logging.
- Security.
- Extensibility.
- Cost.
- Tests.
- Documentation.
- Monetization alignment.

Also check whether the work complies with all relevant Auto Content Factory skills.

## Refactor Rule

If the implementation does not comply, refactor before delivery.

Do not sacrifice long-term maintainability just to finish the task.

Prefer a smaller complete, maintainable change over a larger fragile one.

## Applicable Output

Report only the applicable findings and verification; this list is a menu, not a mandatory report template:

1. Overall status: `pass`, `pass_with_notes`, or `blocked`.
2. Critical blockers.
3. Required refactors.
4. Architecture findings.
5. Workflow findings.
6. Prompt findings.
7. Database findings.
8. Naming findings.
9. Exception and logging findings.
10. Security findings.
11. Extensibility findings.
12. Cost findings.
13. Test findings.
14. Documentation findings.
15. Final delivery recommendation.

## Review Checklist

Before delivery, verify:

- The design remains modular.
- Prompts are not hard-coded without versioning.
- Databases are separated by lifecycle.
- Names are consistent.
- Errors and retries are handled.
- Logs are append-only and useful.
- Secrets are protected.
- Tests cover normal and failure paths.
- Costs are not wasteful.
- The change supports long-term automated monetization.
