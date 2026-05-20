---
name: convex-reviewer
description: Review Convex code for security, runtime correctness, performance, schema design, and AgentForge-specific architectural boundaries.
version: 1.0.0
metadata:
  author: agentforge
  source: get-convex/convex-agent-plugins@f104efb49a787a1ef4a6c84df496d58800ce334a
---

# Convex Reviewer

Use this skill when reviewing Convex code or PRs. Findings come first.

## Review order

1. Security: auth, authorization, validators, internal/public boundaries.
2. Runtime correctness: deterministic queries, `"use node"` boundaries, awaited promises, scheduler usage.
3. Performance: indexes, pagination, `.filter()` misuse, unbounded `.collect()`.
4. Schema quality: relationships, nested data, validator shape.
5. AgentForge fit: no Mastra runtime or LLM orchestration in Convex.

## Output style

- Report concrete findings with file and line references.
- Explain why each issue matters.
- Suggest the safer Convex-native pattern.
- If there are no findings, say so explicitly and note residual risk or missing tests.

## References

- Read [review-checklist.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/convex-reviewer/references/review-checklist.md) before doing a substantial review.
