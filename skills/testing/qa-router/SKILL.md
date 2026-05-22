---
name: qa-router
description: Catalog of all QA skills and sub-agents. Exposes available tooling so the agent can decide what and when to use. Use when starting validation to discover appropriate testing tools.
category: orchestration
---

# QA Skill Router

> "Catalog of all QA tools - discover what you need, use what you choose."

## Overview

This skill provides a complete catalog of available QA skills and sub-agents. It does **not** automatically load skills - the agent decides which tools to use based on task context.

## Quick Reference: Validation Scenarios

| Scenario              | Skills                                                                                  | Sub-Agent                                   |
| --------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------- |
| **New Feature**       | `qa-test-creation` → `qa-code-review` → `qa-validation-workflow` → `qa-browser-testing` | `test-creator` → `qa-browser-validator`     |
| **Gameplay**          | `qa-test-creation` → `qa-gameplay-testing` → `qa-code-review`                           | `test-creator` → `qa-gameplay-tester`       |
| **Multiplayer**       | `qa-test-creation` → `qa-multiplayer-testing` → `qa-code-review`                        | `test-creator` → `qa-multiplayer-validator` |
| **Visual/Shaders**    | `qa-test-creation` → `qa-visual-testing` → `qa-code-review`                             | `test-creator` → `visual-regression-tester` |
| **Assets**            | `qa-validation-asset` → `qa-browser-testing`                                            | `qa-browser-validator`                      |
| **Bug Re-validation** | `qa-code-review` → `qa-validation-workflow` → `qa-browser-testing`                      | `qa-browser-validator`                      |

## Quick Reference: By Validation Stage

| Stage                  | Skills to Use                                               |
| ---------------------- | ----------------------------------------------------------- |
| **0. Session Start**   | `qa-workflow`, `qa-router` (this skill)                     |
| **1. Message Queue**   | `shared-messaging`                                          |
| **2. Worktree Setup**  | `shared-worker`                                             |
| **3. Task Memory**     | `shared-retrospective`                                      |
| **4. Test Coverage**   | `qa-test-creation` (invokes `test-creator` if needed)       |
| **5. Test Execution**  | `qa-validation-workflow` (type-check → lint → test → build) |
| **6. Code Review**     | `qa-code-review`                                            |
| **7. Browser Testing** | `qa-browser-testing` + scenario-specific sub-agent          |
| **8. Bug Reporting**   | `qa-reporting-bug-reporting`                                |

### Decision Tree

```
START VALIDATION
        │
├─→ Task needs tests?
│   └─ Yes → Load qa-test-creation → test-creator sub-agent
│   └─ No → Continue
│
├─→ Run test execution (qa-validation-workflow)
│   └─ Tests fail?
│       ├─ Test code issue? → Fix test → Re-run
│       └─ Game code issue? → Bug report → Return to Developer
│
├─→ Code review needed?
│   ├─ Yes → Load qa-code-review
│   └─ No → Skip to browser testing
│
├─→ Task type?
│   ├─ Basic feature → qa-browser-testing + qa-browser-validator
│   ├─ Gameplay → qa-gameplay-testing + qa-gameplay-tester
│   ├─ Multiplayer → qa-multiplayer-testing + qa-multiplayer-validator
│   ├─ Visual/UI → qa-visual-testing + visual-regression-tester
│   └─ Assets → qa-validation-asset + qa-browser-validator
│
└─→ Validation failed?
    └─ Yes → qa-reporting-bug-reporting
```

## Usage Pattern

```markdown
1. Load skills: Use Skill("skill-name") or /skill-name
2. Validate: Execute validation workflow
3. Report: Use qa-reporting-bug-reporting if failed
```
