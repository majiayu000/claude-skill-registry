---
name: vibe-using-vibe-engineering
description: Bootstraps the agent to check for applicable vibe-engineering skills before every action. Loads at conversation start for skill discovery.
user-invocable: true
---

# vibe-using-vibe-engineering

You have access to the **vibe-engineering** skill collection — 34 engineering discipline skills extracted from real-world development.

## How This Works

Before taking any action, check if a vibe-engineering skill applies. Skills use the `vibe-` prefix.

## Skill Quick Reference

### Before Building
- `vibe-research-before-design` — SOTA research before proposing architecture/features
- `vibe-start-informed` — Research agents for real projects, papers, and documented failures
- `vibe-decision-journal` — Record architectural decisions for cross-session memory
- `vibe-production-mindset` — Set "1 million users" quality expectations

### While Building
- `vibe-quality-loop` — Implement→Review→Test→Fix→Loop until clean
- `vibe-scope-guard` — Detect and redirect scope creep
- `vibe-anti-rationalization-check` — Catch shortcut rationalization
- `vibe-acceptance-gate` — Validate against acceptance criteria
- `vibe-coverage-enforcer` — Enforce tiered coverage standards
- `vibe-concurrent-test-safety` — Audit for race conditions in tests
- `vibe-adversarial-test-generation` — Generate edge case tests
- `vibe-fuzz-parser-inputs` — Fuzz test scaffolding for parsers
- `vibe-golden-file-testing` — Snapshot tests with temporal normalization
- `vibe-pattern-library` — Record and suggest established patterns

### Before Shipping
- `vibe-devil-advocate-review` — 5-dimension adversarial challenge
- `vibe-spec-vs-code-audit` — Spec compliance check
- `vibe-doc-quality-gate` — 6-point document quality check
- `vibe-pre-commit-audit` — Secrets, debug statements, TODO scan
- `vibe-safe-deploy` — Pre-flight checks with rollback
- `vibe-rollback-plan` — Documented rollback runbook
- `vibe-structured-output` — Enforced output format

### After Building
- `vibe-reflect-and-compound` — Extract learnings from experience
- `vibe-debugging-journal` — Record bug patterns
- `vibe-iteration-review` — Quality grading and trends
- `vibe-handover-doc` — Session continuity document

### Scaling Work
- `vibe-parallel-task-decomposition` — DAG analysis for parallelism
- `vibe-cherry-pick-integration` — Safe parallel branch integration
- `vibe-wave-based-remediation` — Prioritized batch fixes
- `vibe-async-task-queue` — Cross-session task persistence

### Planning & Requirements
- `vibe-requirements-validator` — SMART criteria validation
- `vibe-scenario-matrix` — Behavioral scenario test planning
- `vibe-service-health-dashboard` — Multi-service health check
- `vibe-session-context-flush` — Smart context summarization

## When to Use This Skill

**ALWAYS** — This skill should be loaded at the start of every conversation. It's the skill discovery mechanism.

## When NOT to Use This Skill

- Never. This is always applicable.

## The Rule

If there's even a 1% chance a vibe- skill applies to what you're doing, invoke it. Check before acting.

## Red Flags (You're Rationalizing)

| Thought | Reality |
|---------|---------|
| "This is too simple for a skill" | Simple tasks compound into complex ones |
| "I already know the pattern" | Skills evolve. Read the current version |
| "I'll check after I start" | Check BEFORE starting |
| "The skill is overkill" | Discipline prevents expensive mistakes |
| "Let me just do this one thing" | That one thing is where bugs hide |
