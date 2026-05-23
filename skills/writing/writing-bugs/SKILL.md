---
name: writing-bugs
description: Creates actionable bug reports with reproduction steps. Use when documenting bugs, creating defect tickets, or improving existing bug reports.
---

# Bug Report Writing

Create bug reports developers can reproduce and fix.

## Required Sections

**Title** - Action + Object + Context. "Submit button unresponsive on checkout page after adding coupon" not "Button broken".

**Environment** - Application version, OS, browser, device, relevant configuration.

**Severity**

| Severity | Impact | Examples |
|----------|--------|----------|
| Critical | System unusable, data loss | Crash on launch, data corruption, auth bypass |
| High | Major feature broken | Cannot checkout, search returns nothing |
| Medium | Feature impaired | Sorting broken, validation missing |
| Low | Minor/cosmetic | Typo, alignment, slow animation |

**Steps to Reproduce** - Numbered, specific steps from a known state. Include exact inputs. One action per step.

**Expected Behavior** - What should happen per requirements or reasonable expectation.

**Actual Behavior** - What actually happens. Copy/paste exact error messages.

**Additional Context** (optional) - Screenshots, console logs, stack traces, related issues, workarounds.

## Writing Guidelines

Be specific: "Enter 'test@example.com' in the email field" not "Enter some data".

Be objective: "Login page returns 500 error" not "The terrible login page crashes".

Be complete: Include versions, exact error messages, frequency (always, sometimes, once).

Be concise: One bug per report. Avoid narrative. Use bullet points.

## Anti-Patterns

Do not combine multiple bugs in one report. Do not use vague steps like "click around until it breaks". Report symptoms, not your theory of the cause. Do not submit without version info. Always explain what screenshots show.

## Directory Structure

```
bugs/
├── BUG-001-brief-description.md
├── BUG-002-brief-description.md
└── archive/
```

Scan `bugs/` for highest number, increment by 1, pad to 3 digits.

## Template

Use `templates/bug-report.md` for new reports.
