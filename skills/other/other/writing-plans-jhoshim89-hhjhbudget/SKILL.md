---
name: writing-plans
description: Create comprehensive implementation plans for engineers with minimal codebase knowledge. This skill should be used when breaking down features into detailed, step-by-step implementation guides following TDD principles.
license: Based on obra/superpowers
user_invocable: always
---

# Writing Plans

Create detailed implementation plans that break down features into bite-sized actions (2-5 minutes each), following Test-Driven Development principles with frequent commits.

## Auto-Trigger Keywords

- "플랜 짜줘", "플랜 세워", "계획 세워", "계획 짜줘"
- "plan this", "create a plan", "make a plan"
- "구현 계획", "implementation plan"
- "어떻게 구현", "how to implement"

**Important:** Save plans to `docs/plans/YYYY-MM-DD-<feature-name>.md`, not in conversation.

## Activation

Begin with: "I'm using the writing-plans skill to create the implementation plan."

## Core Workflow

### Step 1: Pre-Planning Questions

Before writing, ask clarifying questions using `AskUserQuestion`:

| When to Ask | Example |
|-------------|---------|
| Local vs Cloud | "로컬에서 먼저 테스트할까요, 바로 클라우드에?" |
| Data handling | "기존 데이터 유지? 백업 후 교체? 삭제 후 새로?" |
| Performance tradeoff | "빠르게 (정확도↓) vs 느리지만 정확하게?" |
| Step-by-step vs batch | "단계별 확인 vs 한번에 실행?" |

**Skip questions when:** Simple bug fix, user already specified, easily reversible.

### Step 2: Choose Plan Type

| Type | Use For | Format |
|------|---------|--------|
| **Type A: TDD** | New features, refactoring, bug fixes | Step 1-5 TDD pattern |
| **Type B: Infrastructure** | DB migration, external services, infra | Phase-based steps |

### Step 3: Write Plan

Use templates from `references/` folder:
- `plan-header-template.md` - Required header structure
- `tdd-task-format.md` - Type A task format
- `infrastructure-task-format.md` - Type B task format
- `subagent-strategy.md` - Subagent configuration

### Step 4: Execution Handoff

Offer two paths:
1. **Subagent-Driven** (Recommended): Fresh agent per task, use `execute-plan` skill
2. **Sequential**: Single agent executes all tasks

## Core Philosophy

**DRY. YAGNI. TDD. Tidy First. Frequent commits.**

### Tidy First (Kent Beck)

Never mix structural and behavioral changes in same commit:
- `refactor:` - Renaming, extracting, moving (structural)
- `feat:`, `fix:` - New features, bug fixes (behavioral)

### Task Granularity

Each task = single 2-5 minute action:
1. Write failing test
2. Verify test fails
3. Implement minimal code
4. Verify tests pass
5. Commit changes

## Key Principles

- Break complex features into atomic, testable steps
- Provide complete code examples, not placeholders
- Include exact file paths and expected outputs
- Design for engineers unfamiliar with the codebase
- Enable verification at every step

## References

For detailed templates and examples, load from `references/`:
- **Plan Header**: `grep "Required Plan Header" references/plan-header-template.md`
- **TDD Tasks**: `grep "Task Structure" references/tdd-task-format.md`
- **Infrastructure**: `grep "Phase" references/infrastructure-task-format.md`
- **Subagents**: `grep "Subagent" references/subagent-strategy.md`
