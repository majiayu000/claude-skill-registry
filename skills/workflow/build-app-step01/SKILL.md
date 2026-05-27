---
name: build-app-step01
description: Use when users are building or scaling ChatGPT Apps / Apps SDK / MCP-based apps and want a preventive workflow to avoid common pitfalls before implementation, deployment, and growth. Trigger for requests about best practices, preflight checks, guardrails, checklists, workflow SOP, reliability, evals, and production readiness.
---

# build-app-step01

Convert OpenAI's "15 lessons from building ChatGPT apps" into an execution workflow that prevents common mistakes early.

## When to use

Use this skill when the user is:
- Building a new app and wants risk prevention before coding.
- Shipping ChatGPT Apps, MCP servers, tool-calling agents, or widgets to production.
- Asking for engineering SOP/checklist/guardrails instead of one-off fixes.
- Turning scattered lessons into repeatable team process.

Do not use this skill for purely conceptual Q&A or isolated UI-only tweaks.

## Inputs you must collect first

Collect these five inputs before proposing implementation:
1. Product goal: one sentence user outcome.
2. User context: data sources, auth, environments.
3. Risk profile: security, latency, compliance, wrong-answer cost.
4. Integration surface: tools, MCP servers, widgets, external APIs.
5. Acceptance gate: what must pass before launch.

If any input is missing, ask one focused question at a time.

## Workflow (preventive, stage-gated)

### Stage 1: Scope and architecture gate

1. Decompose into explicit systems:
- What: product requirements and user journeys.
- How: implementation, tool orchestration, deployment.
2. Choose architecture mode intentionally:
- Stateless API flow for simple requests.
- Stateful chat flow for iterative conversations.
- Hybrid mode when both are needed.
3. Add observability plan before coding:
- request IDs, tool call logs, model config logs.

Read: `references/15-lessons-mapping.md` sections L1-L3.

### Stage 2: Prompt and context gate

1. Keep prompt rules short and operational.
2. Prefer structural guardrails over huge prompts.
3. Detect and recover from context-window pressure.
4. If behavior drifts, run evals instead of adding random prompt text.

Read: `references/15-lessons-mapping.md` sections L4-L8.
Read: `references/code-patterns.md` sections "Prompt + context" and "Tracing".

### Stage 3: Tooling and integration gate

1. Design tool contracts first (input/output schema, timeout, retries).
2. Treat tool calls as untrusted boundaries; validate all payloads.
3. Use MCP to separate model orchestration from system capabilities.
4. Include fallback paths when a tool is unavailable.

Read: `references/15-lessons-mapping.md` sections L9-L12.
Read: `references/code-patterns.md` section "Tool contracts".

### Stage 4: Ship gate

1. Run preflight checks locally.
2. Run smoke tests on real flows.
3. Verify security and data handling rules.
4. Document rollback path before release.

Run: `scripts/preflight_check.sh`
Run: `scripts/generate_checklist.sh`

### Stage 5: Growth and operations gate

1. Define eval datasets for top user intents and failure modes.
2. Track quality over time; never assume prompts stay stable.
3. Use fast experiment loops with clear win/loss metrics.

Read: `references/15-lessons-mapping.md` sections L13-L15.

## Output format required from the assistant

When using this skill, return results in this order:
1. Conclusion first (MVP path).
2. Detailed explanation by stage.
3. Implementation steps.
4. Minimal code snippets (only what is required).
5. Task checklist.
6. Risks and rollback.
7. Validation commands and expected outcomes.
8. Source used.

## Non-negotiables

- Do not put keys/tokens in code or logs.
- Do not introduce unverified APIs or packages.
- Every change must be reversible.
- API changes must include caller/type/doc updates.

## Quick runbook

1. `bash scripts/preflight_check.sh`
2. `bash scripts/generate_checklist.sh > /tmp/build-app-step01-checklist.md`
3. Use generated checklist in planning/review before implementation.

## Source

Primary source:
- https://developers.openai.com/blog/15-lessons-building-chatgpt-apps (published 2026-02-04)
