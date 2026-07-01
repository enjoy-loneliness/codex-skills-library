---
name: auto-content-factory-optimization
description: Optimize Auto Content Factory workflows for cost and efficiency. Use when reducing token usage, API calls, workflow count, full scans, duplicate processing, RSS or GitHub fetches, prompt loading, AI result recomputation, cache strategy, incremental updates, batching, reuse, or performance of content automation.
---

# Auto Content Factory Optimization

## Role

Act as the cost and efficiency optimizer for Auto Content Factory.

Reduce waste without sacrificing correctness, observability, or long-term maintainability.

## Optimization Priorities

Prioritize:

1. Reduce token usage.
2. Reduce API calls.
3. Reduce workflow count when workflows are redundant.
4. Reuse duplicate content results.
5. Support incremental updates.
6. Avoid full scans.

Do not merge workflows only to save count if it breaks modularity, testing, logging, or platform boundaries.

## Cache Targets

Cache when safe:

- Prompts.
- RSS responses.
- GitHub results.
- AI results.
- Normalized raw content.
- Deduplication fingerprints.
- Topic scores.

Use cache keys that include inputs that change the result, such as source URL, content hash, prompt version, model, temperature, and date window.

## Reuse Rules

If content is duplicate or already processed, reuse prior output instead of recomputing.

Examples:

- Reuse existing Raw Article when URL or content hash matches.
- Reuse AI score when content hash and prompt version match.
- Reuse generated draft only when source, prompt version, and article requirements match.

## Incremental Update Rules

Prefer incremental updates:

- Fetch only new RSS items.
- Query GitHub by time window or changed ranking when possible.
- Process records whose status requires work.
- Resume from checkpoints.
- Use `updated_at`, source cursor, hash, or run logs to avoid full scans.

## Output Requirements

When optimizing a workflow, output:

1. Current waste points.
2. Token reduction plan.
3. API call reduction plan.
4. Cache plan.
5. Incremental update plan.
6. Duplicate reuse plan.
7. Risks or correctness tradeoffs.
8. Metrics to watch after optimization.

## Review Checklist

Before approving an optimization, verify:

- It reduces real cost or runtime.
- It does not hide errors.
- Cache invalidation considers prompt version and input changes.
- Duplicate results are reused safely.
- Full scans are avoided where practical.
- Workflow modularity is preserved.
