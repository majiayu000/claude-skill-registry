---
name: confirm-plan
description: Plan confirmation workflow - extract plan from conversation, create file, auto-review with Interactive Recovery. Use for confirming plans after /00_plan.
---

# SKILL: Confirm Plan (Plan Confirmation Workflow)

> **Purpose**: Extract plan from conversation, create plan file, run auto-review with Interactive Recovery
> **Target**: Plan-Reviewer Agent confirming plans after `/00_plan`

---

## Quick Start

### When to Use This Skill
- Confirm plan after `/00_plan` completes
- Create plan file in `.pilot/plan/draft/`
- Run auto-review with Interactive Recovery for BLOCKING findings
- Verify 100% requirements coverage

### Quick Reference
```bash
# TaskList Pattern: TaskUpdate (analyzing → completed) + TaskCreate (confirming)
TaskUpdate "analyzing" "completed"
TaskCreate "confirming" "in_progress"

# Extract plan from conversation
PLAN_CONTENT=$(extract_from_conversation "$CONVERSATION")

# Generate plan file name
TS="$(date +%Y%m%d_%H%M%S)"
PLAN_FILE="$PROJECT_ROOT/.pilot/plan/draft/${TS}_{work_name}.md"

# Requirements verification (BLOCKING if incomplete)
verify_requirements_coverage "$PLAN_CONTENT"

# Auto-review with Interactive Recovery
invoke_plan-reviewer "$PLAN_FILE"
resolve_blocking_findings "$PLAN_FILE"
```

---

## What This Skill Covers

### In Scope
- **Dual-source extraction**: Load decisions from draft file + scan conversation
- **Cross-check verification**: Compare draft vs conversation, detect omissions
- Plan file creation with full template structure
- Requirements verification (100% coverage required)
- Conversation highlights extraction (code examples, diagrams)
- Auto-review with Interactive Recovery for BLOCKING findings
- GPT delegation for large plans (5+ SCs)

### Out of Scope
- Plan creation → `/00_plan` command
- Plan execution → `/02_execute` command
- TDD methodology → @.claude/skills/tdd/SKILL.md

---

## Core Philosophy

**No Execution**: Only creates plan file and reviews | **Context-Driven**: Extract from conversation | **English Only**: Plan MUST be in English | **Strict Mode Default**: BLOCKING → Interactive Recovery

---

### Definition of Done

**Functional Completion**:
- [ ] All SC implemented
- [ ] All tests passing
- [ ] Coverage >= 80%

**Quality Gates**:
- [ ] Type check: 0 errors
- [ ] Lint: 0 violations
- [ ] E2E verification passed

**Delivery Contract**:
- No partial completion allowed
- No "demo/skeleton/basic" versions
- Only explicit deferral with user approval permitted

---

## ⚠️ EXECUTION DIRECTIVE

**IMPORTANT**: Execute ALL steps below IMMEDIATELY and AUTOMATICALLY without waiting for user input.
- Do NOT pause between steps
- Do NOT ask "should I continue?" or wait for "keep going"
- Execute Step 1 → 2 → 2.5 → 3 → 4 in sequence
- Only stop for BLOCKING findings that require Interactive Recovery

---

## Execution Steps (Summary)

### Step 1: Dual-Source Extraction
1. Load draft file from `.pilot/plan/draft/` (reuse existing or create new)
2. Scan conversation for User Requirements (UR-1, UR-2, ...) and Decisions (D-1, D-2, ...)
3. Cross-check draft vs conversation, flag MISSING items
4. Resolve omissions using AskUserQuestion
5. Extract conversation highlights (code examples, diagrams, CLI commands)
6. Verify 100% requirements coverage (UR → SC mapping)
7. Verify scope completeness (scope vs SC mapping, assumptions verified)
8. Run Self-Contained verification (9-point checklist)
9. SC Granularity Check: Verify each SC follows Atomic SC Principle ("One SC = One File OR One Concern")

**BLOCKING if**: Requirements incomplete, scope gaps, or self-contained check fails

### Step 2: Create or Update Plan File
- Use absolute path based on Claude Code's initial working directory
- Reuse existing draft or create new one
- Apply full plan template (User Requirements, Context Pack, Success Criteria, PRP Analysis, etc.)
- Include Context Pack Formats and Zero-Knowledge TODO Format sections

### Step 2.5: GPT Delegation Check (Mandatory Oracle Consultation)
- **Trigger**: Large plans (5+ Success Criteria) OR architecture keywords in plan
- **Architecture keywords**: architecture, tradeoff, design, scalability, pattern, choice
- **Oracle Role**: Auditor - Plan quality audit
- Delegate to GPT Plan Reviewer using codex CLI
- Graceful fallback if Codex not installed

**Mandatory Oracle Consultation**: All plans receive quality audit via GPT Auditor to verify requirements coverage, SC clarity, dependencies, and risks before confirmation.

### Step 3: Auto-Review & Auto-Apply
- Spawn teammate "plan-reviewer" (role: plan-reviewer)
- Review criteria: requirements coverage, SC clarity, dependencies, risks
- Output: <PLAN_COMPLETE> or <PLAN_BLOCKED>
- BLOCKING → Interactive Recovery loop (max 5 iterations)
- Auto-apply Critical, Warning, Suggestion findings

### Step 4: Move to pending
- Move plan file to `.pilot/plan/pending/`
- STOP: Do NOT proceed to /02_execute automatically

### Step 4.5: Cleanup Intermediate Files
- Delete matching `*_draft.md` and `*_context_pack.md` files from draft/
- Match by work_name extracted from confirmed plan filename
- Log deleted files for audit trail

---

## Argument Parsing

Parse `$ARGUMENTS` from command invocation:
- `[work_name]`: Optional work name for plan file
- `--lenient`: Bypass BLOCKING findings
- `--no-review`: Skip all review steps

---

## Further Reading

**Internal**: @.claude/skills/confirm-plan/REFERENCE.md - Detailed implementation, Context Pack formats, Zero-Knowledge TODO format, Self-Contained verification checklist | @.claude/skills/spec-driven-workflow/SKILL.md - SPEC-First methodology (Problem-Requirements-Plan)

**External**: [Specification by Example](https://www.amazon.com/Specification-Example-Gojko-Adzic/dp/0321842733) | [User Stories Applied](https://www.amazon.com/Stories-Agile-Development-Software-Cohn/dp/0321205685)

---

**⚠️ MANDATORY**: This skill only creates plan. Run `/02_execute` to implement.
