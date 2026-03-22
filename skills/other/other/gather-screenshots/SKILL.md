---
name: gather-screenshots
description: Generate screenshot capture checklists for Product Demo lessons based on readiness assessment.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Gather Screenshots

## Description

Generates a structured screenshot capture checklist from a course's readiness assessment. Used during Phase 6 (Gather Context) of the course workflow to prepare assets for Product Demo lessons.

## When to Use

- After `/self-assess-readiness` identifies Product Demo SLTs as "Needs Context"
- When the Context Shopping List includes screenshots
- Before building Product Demo lessons

## Invocation

```
/gather-screenshots                           # Interactive: asks which course
/gather-screenshots andamio-for-contributors  # Specify course
```

## Instructions

### 1. Identify Course

If no course specified, scan `courses-in-progress/` and ask which course to generate checklist for.

### 2. Read Readiness Assessment

Read `04-readiness-assessment.md` to identify:
- Which SLTs are "Needs Context"
- Which of those are Product Demo lesson type (cross-reference with `03-lesson-type-classification.md`)
- What specific screenshots are needed (from Gap Analysis sections)

### 3. Read Course Outline

Read `00-course.md` to get:
- Lesson focus for each SLT (what UI flows to capture)
- Lesson inputs specified (what screenshots were already anticipated)

### 4. Generate Checklist

Create `assets/screenshots/README.md` with:

```markdown
# Screenshot Capture Checklist: [Course Name]

**Generated from:** `04-readiness-assessment.md`
**Target site:** [primary URL]
**Last updated:** [date]

## Capture Settings

- **Browser:** Chrome or Firefox (consistent across all screenshots)
- **Window width:** 1280px recommended
- **Theme:** Use default theme
- [Any course-specific settings]

## Naming Convention

```
[slt-number]-[flow-name]-[sequence].png
```

## Checklist

### SLT [X.Y]: [SLT text]

| # | Filename | What to Show | Status |
|---|----------|--------------|--------|
| 1 | `X.Y-flow-name-01.png` | [specific UI state] | [ ] |
| 2 | `X.Y-flow-name-02.png` | [next UI state] | [ ] |

**Capture notes:**
- [specific guidance for this flow]

---

[Repeat for each Product Demo SLT]

## Summary

| SLT | Screenshots Needed | Captured | Notes |
|-----|-------------------|----------|-------|
| X.Y | [count] | 0 | [brief note] |

**Total:** [n] screenshots

## Capture Session Notes

_Use this space to record observations during capture:_

- Date:
- Tester:
- Environment:
- Observations:
```

### 5. Create Directory Structure

Ensure `assets/screenshots/` directory exists:

```
courses-in-progress/[course-slug]/
  assets/
    screenshots/
      README.md  # The checklist
      # Screenshots will be added here
```

### 6. Output Summary

After generating, report:

```markdown
## Screenshot Checklist Generated

**Course:** [name]
**Location:** `assets/screenshots/README.md`

| SLT | Flow | Screenshots |
|-----|------|-------------|
| X.Y | [flow-name] | [count] |

**Total:** [n] screenshots across [m] SLTs

### Capture Tiers

| Tier | SLTs | Prerequisites | Est. Time |
|------|------|---------------|-----------|
| 1: No login | [list] | Just browse | [time] |
| 2: Logged in | [list] | Wallet connected | [time] |
| 3: Async | [list] | Prior actions completed | Later |

**Next step:** Capture Tier 1 screenshots to validate the system.
```

## Naming Convention

### Format

```
[slt]-[flow]-[step].png
```

### Parts

| Part | Format | Example | Purpose |
|------|--------|---------|---------|
| `slt` | `X.Y` | `1.2` | SLT number |
| `flow` | `kebab-case` | `wallet-connect` | Human-readable flow name |
| `step` | `01`, `02` | `01` | Sequence (zero-padded) |

### Examples

| Filename | Description |
|----------|-------------|
| `1.2-wallet-connect-01.png` | First step of wallet connection |
| `1.2-wallet-connect-02.png` | Second step |
| `2.1-course-catalog-01.png` | Course catalog overview |
| `3.2-enrollment-03.png` | Third step of enrollment |

### Why This Convention

1. **Sorted by SLT** — Files group naturally
2. **Predictable paths** — Lessons reference without guessing
3. **Sequence clear** — Steps are numbered
4. **Grep-friendly** — `ls 3.2-*` shows all enrollment screenshots

## Flow Name Guidelines

Choose flow names that are:
- **Descriptive** — `wallet-connect` not `step1`
- **Consistent** — Same flow = same name across courses
- **Short** — 2-3 words max

### Common Flow Names

| Flow | Use For |
|------|---------|
| `wallet-connect` | Connecting wallet to platform |
| `mint-token` | Minting any token/NFT |
| `course-catalog` | Browsing course listings |
| `project-catalog` | Browsing project listings |
| `enrollment` | Enrolling in course/module |
| `submission` | Submitting evidence/assignment |
| `credential-claim` | Claiming earned credential |
| `project-join` | Joining a project |
| `task-commit` | Committing to a task |

## Guidelines

- **One checklist per course** — Don't split across files
- **Specific UI states** — "Landing page with Connect button" not "homepage"
- **Capture notes matter** — Include edge cases, error states, prerequisites
- **Tier by dependencies** — Group screenshots by what's required to capture them
- **Update after capture** — Check off items, note any issues
- **Flat directory** — No subdirectories per SLT (simpler for ~50 files or fewer)
