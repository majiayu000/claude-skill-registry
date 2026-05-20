---
name: meta-reviewing-reviewing
description: Code review patterns, feedback principles. Use when reviewing PRs, implementations, or making approval/rejection decisions. Covers self-correction, progress tracking, feedback principles, severity levels.
---

# Reviewing Patterns

> **Quick Guide:** Read ALL files completely before commenting. Provide specific file:line references for every issue. Distinguish severity (Must Fix vs Should Fix vs Nice to Have). Explain WHY, not just WHAT. Suggest solutions following existing patterns. Acknowledge good work - positive reinforcement teaches what to repeat.

---

**Detailed Resources:**

- For core examples (progress tracking, retrieval), see [examples/core.md](examples/core.md)
- For feedback pattern examples, see [examples/feedback-patterns.md](examples/feedback-patterns.md)
- For anti-pattern examples, see [examples/anti-patterns.md](examples/anti-patterns.md)
- For decision frameworks and red flags, see [reference.md](reference.md)

---

<critical_requirements>

## CRITICAL: Before Any Review

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST read ALL files mentioned in the PR/spec completely before providing feedback)**

**(You MUST provide specific file:line references for every issue found)**

**(You MUST distinguish severity: Must Fix vs Should Fix vs Nice to Have)**

**(You MUST explain WHY something is an issue, not just WHAT is wrong)**

**(You MUST verify success criteria are met with evidence before approving)**

**(You MUST acknowledge what was done well - not just issues)**

</critical_requirements>

---

**Auto-detection:** code review, PR review, pull request, review code, check implementation, verify changes

**When to use:**

- Reviewing any code changes (PRs, implementations, specs)
- Providing structured feedback on code quality
- Making approval/rejection decisions
- Ensuring codebase standards are maintained

**When NOT to use:**

- When implementing code (use developer skills instead)
- For automated linting/type-checking (use tooling, CI/CD)
- For security audits (use security/security skill for deep security analysis)
- For high-level architecture decisions (use planning tools instead)

**Key patterns covered:**

- Self-correction checkpoints for reviewers
- Post-action reflection after reviews
- Progress tracking for multi-file reviews
- Retrieval strategy for reviewing unfamiliar code
- Feedback principles (specific, explain why, suggest solutions, severity, acknowledge good)
- Decision framework for approval/rejection
- Review-specific anti-patterns (scope creep, refactoring, not using utilities)

---

<philosophy>

## Philosophy

Code review is about **improving code quality while teaching good patterns**. Every piece of feedback should help the author become a better developer. Be direct but constructive.

**When reviewing code:**

- Always read the full context before commenting
- Base feedback on facts, not assumptions
- Distinguish blocking issues from improvements
- Teach through your feedback - explain the "why"
- Recognize good work to reinforce patterns

**When NOT to be harsh:**

- Don't nitpick style when code is functionally correct
- Don't request changes for personal preference
- Don't block PRs for minor issues that can be follow-ups
- Don't forget that the author worked hard on this

**Core principles:**

- **Evidence-based**: Base all feedback on what you actually read
- **Actionable**: Every issue should have a clear path to resolution
- **Proportional**: Match feedback severity to actual impact
- **Educational**: Help authors understand WHY, not just WHAT
- **Balanced**: Acknowledge good work alongside issues

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Self-Correction Triggers

These checkpoints prevent review drift and ensure thorough analysis. Check yourself throughout the review process.

**Self-Correction Checkpoints:**

| Trigger                                           | Correction                                 |
| ------------------------------------------------- | ------------------------------------------ |
| Providing feedback without reading full file      | Stop. Read the complete file first.        |
| Saying "this needs improvement" without specifics | Stop. Provide file:line references.        |
| Approving without checking success criteria       | Stop. Verify each criterion with evidence. |
| Focusing only on issues                           | Stop. Add positive feedback.               |
| Making assumptions about code behavior            | Stop. Read the actual implementation.      |
| Flagging issues without explaining WHY            | Stop. Add rationale for each issue.        |
| Reviewing code outside your domain                | Stop. Defer to specialist reviewer.        |

**Why this matters:** Self-correction prevents incomplete reviews, missed issues, and unfair feedback. Checking yourself throughout the review leads to higher quality, more actionable feedback.

---

### Pattern 2: Post-Action Reflection

After completing your review, verify quality before finalizing.

**Reflection Questions:**

1. Did I read all relevant files completely before commenting?
2. Did I check against all success criteria in the spec?
3. Are my issues specific (file:line) and actionable?
4. Did I distinguish severity correctly (blocker vs improvement)?
5. Did I acknowledge what was done well?
6. Should any part go to a specialist reviewer?
7. Is my recommendation (approve/request changes) justified?

**Only finalize review when you can answer "yes" to all applicable questions.**

**Why this matters:** Reflection catches oversights before they affect the author. A review that misses context or lacks specificity wastes everyone's time.

---

### Pattern 3: Progress Tracking

For multi-file reviews, track your progress to maintain orientation.

**Track These Elements:**

1. **Files Examined:** [list of files read completely]
2. **Success Criteria Status:** [checked/unchecked for each criterion]
3. **Issues Found:** [categorized by severity]
4. **Positive Patterns Noted:** [what was done well]
5. **Deferred Items:** [what needs specialist review]

**Why this matters:** Multi-file reviews are complex. Tracking progress prevents missed files, forgotten criteria, and lost context.

For detailed tracking examples, see [examples/core.md](examples/core.md).

---

### Pattern 4: Feedback Principles

All feedback should follow these principles for maximum effectiveness.

#### Be Specific

Every issue needs a precise location. Vague feedback wastes time. Specific feedback can be acted on immediately.

#### Explain Why

Don't just say what's wrong - explain the impact. Understanding impact helps authors learn and prevents repeat mistakes.

#### Suggest Solutions

Point to existing patterns when possible. Solutions (especially referencing existing code) make fixes faster and maintain consistency.

#### Distinguish Severity

Use clear markers to communicate priority:

| Marker           | Category                              | Examples                                                                                                |
| ---------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Must Fix**     | Blockers - cannot approve until fixed | Security vulnerabilities, breaks functionality, missing required criteria, major convention violations  |
| **Should Fix**   | Improvements - strongly recommended   | Performance optimizations, minor convention deviations, missing edge case handling, code simplification |
| **Nice to Have** | Suggestions - optional enhancements   | Further refactoring, additional tests, documentation, future enhancements                               |

#### Acknowledge Good Work

Always include positive feedback. Positive reinforcement teaches what to repeat. Reviews that only criticize demotivate and miss teaching opportunities.

For detailed examples of each principle, see [examples/feedback-patterns.md](examples/feedback-patterns.md).

</patterns>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST read ALL files mentioned in the PR/spec completely before providing feedback)**

**(You MUST provide specific file:line references for every issue found)**

**(You MUST distinguish severity: Must Fix vs Should Fix vs Nice to Have)**

**(You MUST explain WHY something is an issue, not just WHAT is wrong)**

**(You MUST verify success criteria are met with evidence before approving)**

**(You MUST acknowledge what was done well - not just issues)**

**Failure to follow these rules will produce low-quality reviews that waste author time and miss important issues.**

</critical_reminders>
