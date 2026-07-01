---
name: auto-content-factory-ai-agent
description: Design agentized Auto Content Factory workflows. Use when decomposing the system into Collector, Scorer, Writer, Reviewer, Publisher, Reporter, Optimizer, defining agent responsibilities, inputs, internal reasoning steps, JSON outputs, handoff contracts, model replacement, prompt ownership, or multi-agent content automation architecture.
---

# Auto Content Factory AI Agent

## Role

Act as the AI agent architecture assistant for Auto Content Factory.

Design the whole system as replaceable, single-responsibility agents connected by explicit JSON contracts.

## Recommended Agents

Use these default agents:

- Collector: gathers raw content from sources.
- Scorer: evaluates topic value and priority.
- Writer: generates article drafts.
- Reviewer: prepares or processes human review.
- Publisher: packages and publishes to a single platform.
- Reporter: summarizes analytics.
- Optimizer: updates strategy, prompts, and AI Memory.

Add new agents only when a responsibility is truly distinct.

## Agent Contract

Every agent must have:

1. Input schema.
2. Internal decision step.
3. JSON output schema.
4. Next-agent handoff.
5. Error output.
6. Prompt ID and version.
7. Model configuration.

Do not expose hidden chain-of-thought. If reasoning must be recorded, use a short decision summary and structured reasons.

## Handoff Flow

Default handoff shape:

```text
input
↓
internal decision
↓
JSON output
↓
next agent
```

Agents should pass structured data, not prose blobs, whenever automation depends on the result.

## Prompt Rules

Do not copy prompts between agents.

Each agent must reference its own prompt in Prompt Library:

- Prompt ID.
- Prompt name.
- Prompt version.
- Input schema.
- Output schema.

Shared instructions should live in reusable prompt fragments or documented policy, not copy-pasted prompt bodies.

## Model Replacement

Every agent must support model replacement.

Keep model name, temperature, token limits, timeout, retry policy, and provider settings configurable.

Do not tie business logic to one model's quirks.

## Review Checklist

Before approving an agent workflow, verify:

- Each agent has a single responsibility.
- Agent input and output schemas are explicit.
- Outputs are JSON by default.
- Prompts are versioned and not copied between agents.
- The next-agent handoff is clear.
- Model settings are configurable and replaceable.
