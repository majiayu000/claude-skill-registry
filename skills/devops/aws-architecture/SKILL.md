---
name: aws-architecture
description: Architect AWS infrastructure and application integrations with production-grade service selection, boundaries, rollout thinking, and verification. Use when the user asks for AWS architecture, infra design, service selection, or AWS-backed implementation planning. Do not use for repo-specific Nova guidance unless the active repo adapter calls into it.
---

# AWS Architecture

Use this skill for reusable AWS architecture work, not repo-specific policy.

## Workflow

1. Read the repo `AGENTS.md`.
2. Run `/home/bjorn/.codex/skill-support/bin/repo-inventory detect --cwd <repo> --out <json>` if the repo context matters.
3. Read the relevant AWS references before finalizing service choices.
4. Prefer managed services and the simplest correct topology.
5. Output the architecture, tradeoffs, rollout notes, and verification plan.

## Use When

- The task needs AWS service selection or architecture planning.
- The work spans infra design, serverless boundaries, deployment flow, or AWS-backed runtime behavior.

## Do Not Use When

- The task is repo-specific Nova policy only.
- The task is only docs alignment or only dependency work.

## Outputs

- architecture recommendation
- service map
- rollout and verification plan

