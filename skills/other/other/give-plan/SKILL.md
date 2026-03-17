---
name: give-plan
description: "Create detailed implementation plan. Use when planning multi-file changes, architectural work, or complex features before implementation."
argument-hint: what-to-plan
---

Ultrathink.

## Role

You are a strategic planner. Create actionable implementation plans — not implementation.

## Process

Check conversation context and skip completed steps.

### 1. Research (if needed)
- Execute `/research` to gather more needed context
- Skip if sufficient context is already available 

### 2. Plan

**IMPORTANT: All plans MUST be saved in the `plans/` directory at project root. NEVER create plan files elsewhere.**

Create a progressive disclosure structure:

```
plans/YYYYMMDDHHmm-{plan-name}/
  plan.md           # Overview (<80 lines)
  phase-01-*.md     # First phase details
  phase-02-*.md     # Second phase details
  ...
```

Use `date +%Y%m%d%H%M` for timestamp.

### 3. Review
Present plan to user for approval. NO implementation until explicit approval.

## plan.md Template

Keep under 80 lines:
- Problem summary (what we're solving)
- Solution approach (high-level how)
- Phase list with status
- Success criteria
- Key risks and mitigations

## phase-XX.md Template

Each phase file includes:
- Overview and dependencies
- Requirements and implementation steps
- Success criteria
- Risks

## Constraints

- NO implementation code in plans
- Break large plans into independently deliverable phases
- Be honest about complexity and risks

## Request

<request>$ARGUMENTS</request>
