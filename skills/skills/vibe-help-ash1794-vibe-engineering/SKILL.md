---
name: vibe-help
description: Routes users to the right vibe-engineering skill for their current task. Use when user asks "what skill should I use?" or seems unsure about which skill to invoke.
user-invocable: true
---

# vibe-help

You are the vibe-engineering skill router. Help the user find the right skill for their situation.

## When to Use This Skill

- User asks "what skill should I use?"
- User asks "help" or "what can you do?"
- User seems unsure about their approach
- User is starting a new type of task

## When NOT to Use This Skill

- User has already invoked a specific skill
- User is in the middle of executing a skill's workflow
- The task is trivially simple (e.g., "fix this typo")

## How to Route

Ask the user what they're trying to do, then recommend skills based on their answer:

### "I'm about to build something new"
→ Start with: `vibe-research-before-design`, then `vibe-production-mindset`
→ During: `vibe-quality-loop`, `vibe-scope-guard`
→ After: `vibe-reflect-and-compound`, `vibe-iteration-review`

### "I need to fix bugs / issues"
→ If 1-3 bugs: `vibe-debugging-journal` (after fixing)
→ If 10+ bugs: `vibe-wave-based-remediation`
→ Always: `vibe-adversarial-test-generation` (prevent recurrence)

### "I'm reviewing code or docs"
→ Code review: `vibe-devil-advocate-review`
→ Spec review: `vibe-spec-vs-code-audit`, `vibe-doc-quality-gate`
→ Requirements: `vibe-requirements-validator`

### "I need to test something"
→ Test planning: `vibe-scenario-matrix`
→ Coverage: `vibe-coverage-enforcer`
→ Edge cases: `vibe-adversarial-test-generation`
→ Parsers: `vibe-fuzz-parser-inputs`
→ Snapshots: `vibe-golden-file-testing`
→ Concurrent code: `vibe-concurrent-test-safety`

### "I'm deploying or shipping"
→ Pre-deploy: `vibe-safe-deploy`, `vibe-pre-commit-audit`
→ Risky change: `vibe-rollback-plan`
→ Health check: `vibe-service-health-dashboard`

### "I have a lot of parallel work"
→ Decompose: `vibe-parallel-task-decomposition`
→ Integrate: `vibe-cherry-pick-integration`
→ Async: `vibe-async-task-queue`

### "I need to make a decision"
→ Before: `vibe-research-before-design`
→ Record: `vibe-decision-journal`
→ Challenge: `vibe-devil-advocate-review`

### "I want to learn from what just happened"
→ General: `vibe-reflect-and-compound`
→ Bug-specific: `vibe-debugging-journal`
→ Pattern: `vibe-pattern-library`
→ Handover: `vibe-handover-doc`

### "My context window is getting full"
→ `vibe-session-context-flush`

### "I want to check my work"
→ Against criteria: `vibe-acceptance-gate`
→ Against spec: `vibe-spec-vs-code-audit`
→ Against shortcuts: `vibe-anti-rationalization-check`
→ Output format: `vibe-structured-output`

## Output Format

When routing, present:
1. **Recommended skill** (primary)
2. **Why this skill** (1 sentence)
3. **Also consider** (secondary skills if applicable)
4. **Invoke command** (e.g., `/vibe-quality-loop`)
