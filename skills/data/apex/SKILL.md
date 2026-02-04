---
name: APEX Methodology
description: |
  Systematic development workflow: Analyze → Plan → Execute → eLicit → eXamine.
  Use for ANY development task: features, bug fixes, refactoring, hotfixes.
  Triggers: "implement", "create", "build", "fix", "add feature", "refactor", "develop".
  Auto-detects project type (Laravel, Next.js, React, Swift) and loads framework-specific references.
  Enforces: files <100 lines, interfaces separated, SOLID principles, expert self-review, sniper validation.
  Modes: --auto (default), --manual, --skip-elicit
argument-hint: "[task-description]"
user-invocable: false
hooks:
  PostToolUse:
    - matcher: Edit
      hooks:
        - type: command
          command: |
            echo '{"decision":"block","reason":"APEX RULE: File modified via Edit. You MUST immediately launch sniper agent to validate this change before proceeding."}'
    - matcher: Write
      hooks:
        - type: command
          command: |
            echo '{"decision":"block","reason":"APEX RULE: File created via Write. You MUST immediately launch sniper agent to validate this change before proceeding."}'
---

**Current Task:** $ARGUMENTS

# APEX Methodology Skill

**Analyze → Plan → Execute → eLicit → eXamine**

Complete development workflow for features, fixes, and refactoring.

---

## Step 0: Initialize Tracking (MANDATORY FIRST ACTION)

**BEFORE anything else**, run this command to initialize APEX tracking:

```bash
mkdir -p .claude/apex/docs && cat > .claude/apex/task.json << 'INITEOF'
{
  "current_task": "1",
  "created_at": "'"$(date -u +"%Y-%m-%dT%H:%M:%SZ")"'",
  "tasks": {
    "1": {
      "status": "in_progress",
      "started_at": "'"$(date -u +"%Y-%m-%dT%H:%M:%SZ")"'",
      "doc_consulted": {}
    }
  }
}
INITEOF
echo "✅ APEX tracking initialized in $(pwd)/.claude/apex/"
```

This creates:
- `.claude/apex/task.json` - Tracks documentation consultation status
- `.claude/apex/docs/` - Stores consulted documentation summaries

**The PreToolUse hooks will BLOCK Write/Edit until documentation is consulted.**

---

## Workflow Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│                     APEX WORKFLOW                               │
├─────────────────────────────────────────────────────────────────┤
│  00-init-branch     → Create feature branch                     │
│  01-analyze-code    → Understand codebase (A)                   │
│  02-features-plan   → Plan implementation (P)                   │
│  03-execution       → Write code (E)                            │
│  03.5-elicit        → Expert self-review (L) ← NEW              │
│  04-validation      → Verify quality (X)                        │
│  05-review          → Self-review                               │
│  06-fix-issue       → Handle issues                             │
│  07-add-test        → Write tests                               │
│  08-check-test      → Run tests                                 │
│  09-create-pr       → Create Pull Request                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase References

| Phase | File | Purpose |
| --- | --- | --- |
| **00** | `references/00-init-branch.md` | Create feature branch |
| **01** | `references/01-analyze-code.md` | Explore + Research (APEX A) |
| **02** | `references/02-features-plan.md` | TodoWrite planning (APEX P) |
| **03** | `references/03-execution.md` | Implementation (APEX E) |
| **03.5** | `references/03.5-elicit.md` | Expert self-review (APEX L) ← NEW |
| **04** | `references/04-validation.md` | sniper validation (APEX X) |
| **05** | `references/05-review.md` | Self-review checklist |
| **06** | `references/06-fix-issue.md` | Fix validation/review issues |
| **07** | `references/07-add-test.md` | Write unit/integration tests |
| **08** | `references/08-check-test.md` | Run and verify tests |
| **09** | `references/09-create-pr.md` | Create and merge PR |

---

## Quick Start

### Standard Feature Flow

```text
1. 00-init-branch     → git checkout -b feature/xxx
2. 01-analyze-code    → explore-codebase + research-expert
3. 02-features-plan   → TodoWrite task breakdown
4. 03-execution       → Implement (files <100 lines)
5. 03.5-elicit        → Expert self-review (75 techniques) ← NEW
6. 04-validation      → sniper agent
7. 07-add-test        → Write tests
8. 08-check-test      → Run tests
9. 05-review          → Self-review
10. 09-create-pr      → gh pr create
```

### Bug Fix Flow

```text
1. 00-init-branch     → git checkout -b fix/xxx
2. 01-analyze-code    → Understand bug context
3. 07-add-test        → Write failing test FIRST
4. 03-execution       → Fix the bug
5. 08-check-test      → Verify test passes
6. 04-validation      → sniper agent
7. 09-create-pr       → gh pr create
```

### Hotfix Flow

```text
1. 00-init-branch     → git checkout -b hotfix/xxx
2. 03-execution       → Minimal fix only
3. 04-validation      → sniper agent
4. 08-check-test      → Run tests
5. 09-create-pr       → Urgent merge
```

---

## Core Rules

### File Size (ABSOLUTE)

```text
🚨 STOP at 90 lines → Split immediately
❌ NEVER exceed 100 lines
📊 Target: 50-80 lines per file
```

### Interface Location

```text
✅ src/interfaces/     (global)
✅ src/types/          (type definitions)
✅ Contracts/          (PHP/Laravel)
❌ NEVER in component files
```

### Agent Usage

```text
01-analyze:  explore-codebase + research-expert (PARALLEL)
04-validate: sniper (MANDATORY after ANY change)
```

---

## APEX Phases Explained

### A - Analyze

```text
ALWAYS run 2 agents in parallel:

1. explore-codebase
   → Map project structure
   → Find existing patterns
   → Identify change locations

2. research-expert
   → Verify official documentation
   → Confirm API methods
   → Check best practices
```

### P - Plan

```text
ALWAYS use TodoWrite:

1. Break down into tasks
2. Each task <100 lines
3. Plan file splits FIRST
4. Map dependencies
```

### E - Execute

```text
FOLLOW plan strictly:

1. Create interfaces FIRST
2. Monitor file sizes
3. Write JSDoc/comments
4. Atomic commits
```

### X - eXamine

```text
ALWAYS run sniper:

6-phase validation:
1. explore-codebase
2. research-expert
3. grep usages
4. run linters
5. apply fixes
6. ZERO errors
```

---

## Branching Strategy

### Branch Naming

```text
feature/ISSUE-123-short-description
fix/ISSUE-456-bug-name
hotfix/ISSUE-789-urgent-fix
refactor/ISSUE-321-cleanup
docs/ISSUE-654-readme
test/ISSUE-987-coverage
```

### Best Practices (2025)

```text
✅ Short-lived branches (1-3 days)
✅ Small, focused changes
✅ Sync frequently with main
✅ Squash and merge
```

---

## Commit Convention

### Format

```text
<type>(<scope>): <description>

Types: feat, fix, refactor, docs, test, chore
Scope: component/feature name
Description: imperative mood, <50 chars
```

### Examples

```bash
feat(auth): add JWT authentication
fix(cart): resolve quantity validation
refactor(api): extract fetch utilities
test(auth): add login component tests
```

---

## Validation Requirements

### Before PR

```text
□ sniper passes (ZERO errors)
□ All tests pass
□ Build succeeds
□ Self-review complete
□ No console.logs
□ No TODO unaddressed
```

### Code Quality

```text
□ Files <100 lines
□ Interfaces in correct location
□ JSDoc on all exports
□ No any types
□ Error handling complete
```

---

## PR Guidelines

### Title Format

```text
feat(auth): add social login with Google
fix(cart): resolve quantity update bug
refactor(api): extract fetch utilities
```

### Description Must Include

```text
□ Summary (1-3 bullets)
□ Changes (added/modified/removed)
□ Related issues (Closes #xxx)
□ Test plan (checkboxes)
□ Screenshots (if UI changes)
```

---

## Flow Diagram

```text
                    START
                      │
                      ▼
              ┌───────────────┐
              │ 00-init-branch│
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ 01-analyze    │ ← explore + research
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ 02-plan       │ ← TodoWrite
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ 03-execute    │ ← Write code
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ 04-validate   │ ← sniper
              └───────┬───────┘
                      │
              ┌───────┴───────┐
              │               │
              ▼               ▼
        ┌──────────┐   ┌──────────┐
        │ 06-fix   │   │ 07-test  │
        └────┬─────┘   └────┬─────┘
             │              │
             └──────┬───────┘
                    │
                    ▼
              ┌───────────────┐
              │ 08-check-test │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ 05-review     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ 09-create-pr  │
              └───────┬───────┘
                      │
                      ▼
                    DONE
```

---

## NEVER

```text
❌ Skip explore-codebase or research-expert
❌ Assume API syntax without verification
❌ Create files >100 lines
❌ Put interfaces in component files
❌ Skip sniper after changes
❌ Merge without tests
❌ Large PRs (>400 lines)
```

---

## Reference Files

All detailed guides in `references/` directory:

```text
references/
├── 00-init-branch.md     # Branch creation
├── 01-analyze-code.md    # Code analysis
├── 02-features-plan.md   # Planning
├── 03-execution.md       # Implementation
├── 04-validation.md      # Validation
├── 05-review.md          # Self-review
├── 06-fix-issue.md       # Issue fixes
├── 07-add-test.md        # Test writing
├── 08-check-test.md      # Test running
└── 09-create-pr.md       # PR creation
```

---

## Language-Specific References

Framework-specific APEX methodology guides:

| Framework | Directory | Tools |
| --- | --- | --- |
| **Laravel** | `references/laravel/` | Pest, Larastan, Pint |
| **Next.js** | `references/nextjs/` | Vitest, Playwright, ESLint |
| **React** | `references/react/` | Vitest, Testing Library, Biome |
| **Swift** | `references/swift/` | XCTest, SwiftLint, swift-format |

### Auto-Detection

```text
Project Type        → References Used
─────────────────────────────────────
composer.json       → references/laravel/
next.config.*       → references/nextjs/
vite.config.*       → references/react/
Package.swift       → references/swift/
Default             → references/ (generic)
```

### Structure (Each Framework)

```text
references/[framework]/
├── 00-init-branch.md     # Framework-specific branching
├── 01-analyze-code.md    # Framework exploration tools
├── 02-features-plan.md   # Planning patterns
├── 03-execution.md       # SOLID implementation
├── 04-validation.md      # Linters and formatters
├── 05-review.md          # Framework checklist
├── 06-fix-issue.md       # Common fixes
├── 07-add-test.md        # Testing patterns
├── 08-check-test.md      # Test commands
└── 09-create-pr.md       # PR template
```
