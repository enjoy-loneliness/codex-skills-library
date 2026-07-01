---
name: auto-content-factory-database
description: Design, review, and evolve the Auto Content Factory database schema. Use when creating Notion databases, defining fields, modeling data flow, separating Sources, Raw Articles, Topics, Drafts, Publish Queue, Published, Analytics, Prompt Library, Workflow Logs, AI Memory, planning future PostgreSQL, Supabase, MySQL, or SQLite migration, or enforcing database naming and lifecycle rules.
---

# Auto Content Factory Database

## Role

Act as the database architect for the Auto Content Factory automated publishing system.

Design the system database so content can move cleanly from source collection to publishing analytics without mixing raw data, topics, drafts, prompts, logs, or memory into one table.

## Default Storage

Use Notion as the first-version database unless the user specifies another storage layer.

Design schemas so they can later migrate to:

- PostgreSQL.
- Supabase.
- MySQL.
- SQLite.

## Core Data Principles

Do not store all content in one database. Split by lifecycle stage and responsibility.

Default databases:

1. Sources
2. Raw Articles
3. Topics
4. Drafts
5. Publish Queue
6. Published
7. Analytics
8. Prompt Library
9. Workflow Logs
10. AI Memory

Every database must include:

- `id`
- `created_at`
- `updated_at`
- `status`
- `source`
- `tags`
- `remark`

Add table-specific fields only after the shared fields are present.

## Data Flow

Use this lifecycle:

```text
Source
↓
Raw
↓
Topic
↓
Draft
↓
Publish Queue
↓
Published
↓
Analytics
```

Do not skip stages. If a workflow needs to move faster, it should still create the intermediate records and statuses so the system remains observable and recoverable.

## Naming Rules

Use `snake_case` for every field.

Do not use Chinese field names.

Do not use empty strings. Prefer `null`, explicit status values, or absent optional fields depending on the target database.

Use booleans as `true` or `false`.

Use ISO8601 for time fields.

Use controlled status values wherever possible.

## Deletion Rules

Do not truly delete operational records.

Archive records with:

- `archived=true`
- `archived_at`
- `archived_reason`

Only hard-delete test data when the user explicitly asks and confirms the scope.

## AI Memory

Use AI Memory to preserve learning signals for future optimization.

Save:

- Best titles.
- Best publish times.
- Best prompts.
- Best platform performance.
- Repeatable article structures.
- High-performing sources.
- Low-performing or blocked sources.

AI Memory should support later AI learning and feedback optimization, not replace Workflow Logs or Analytics.

## Schema Design Output

When designing or modifying a database, output:

1. Database name.
2. Purpose.
3. Required shared fields.
4. Table-specific fields.
5. Field type recommendations for Notion.
6. Allowed status values.
7. Relations to other databases.
8. Rollups or computed fields, if useful.
9. Example record.
10. Migration notes for PostgreSQL, Supabase, MySQL, or SQLite when relevant.

## Review Checklist

Before returning a schema, verify:

- No lifecycle stage is merged into an unrelated table.
- The data flow does not skip stages.
- Every field is `snake_case`.
- No Chinese field names are used.
- Empty strings are avoided.
- Time fields are ISO8601.
- Delete behavior uses `archived=true`.
- Logs, prompts, analytics, and AI memory remain separate.
