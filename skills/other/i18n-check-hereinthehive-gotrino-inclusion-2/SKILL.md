---
name: i18n-check
description: Analyze code for internationalization issues, understanding the UI context and user impact before flagging problems. Use when reviewing code for global readiness.
allowed-tools: Read, Grep, Glob
user-invocable: true
---

# i18n Check

Analyze code for internationalization issues, with emphasis on understanding impact and user experience.

## Philosophy

This is not about flagging every hardcoded string. It's about asking:

> "If someone in Cairo, Munich, or Tokyo uses this, will it work for them?"

i18n issues aren't just bugs—they're barriers. A date shown as "12/05/2024" is ambiguous to most of the world. A text field that truncates German words breaks the experience. A layout that assumes left-to-right excludes 400 million RTL readers.

## Scope

The user may specify a file path, glob pattern, or directory. If not specified, ask what they'd like to check.

## Config Integration

Before starting, check for `.inclusion-config.md` in the project root.

If it exists:
1. **Read** scope decisions and acknowledged findings
2. **If i18n is "out of scope"**: Skip the check entirely, output brief note:
   ```
   ## i18n Analysis: [path]

   **Skipped:** i18n checks disabled per project config (US-only)
   To re-enable, update .inclusion-config.md
   ```
3. **If in scope**: Skip acknowledged findings, note them in output
4. **Note** at the top of output: "Config loaded: .inclusion-config.md"

## Process

### 1. Read and Understand

First, **read the code** to understand:
- What does this component/file do?
- Is this user-facing or internal tooling?
- What kind of content does it display? (dates, numbers, text, forms)
- Is there existing i18n infrastructure? (react-intl, i18next, etc.)

### 2. Trace the User Experience

Think through what users see:
- Where do dates/times appear? How are they formatted?
- Where does text appear? Can it expand without breaking?
- What direction does the layout assume?
- What do forms ask for? Are fields US-specific?

### 3. Assess Impact by Audience

**Critical** (breaks functionality):
- Date formats that cause confusion (12/05 - December 5 or May 12?)
- Forms that require US-only fields (State, ZIP) with no alternatives
- Layouts completely broken in RTL

**Serious** (degraded experience):
- Text truncated due to expansion
- Currency/number formats that look wrong
- Hardcoded strings that can't be translated

**Minor** (suboptimal):
- Missing locale parameter where one could be added
- CSS using `left/right` instead of logical properties
- Concatenated strings that work but aren't ideal for translators

### 4. Apply Context

Not everything needs fixing. Use judgment:

**Probably needs attention:**
- User-facing dates without locale formatting
- Forms with required State/ZIP fields
- Fixed-width containers with text
- Hardcoded currency symbols users will see

**Probably fine:**
- Internal logging timestamps
- Developer-facing debug output
- Config files with technical strings
- Third-party library code you don't control

## Reference

For detailed patterns to check, see `references/i18n-checklist.md`. Use this as a guide for what to look for, not a checklist to grep through.

## Output Format

Keep it **compact**. Group by severity, use tables, actionable fixes.

```markdown
## i18n Analysis: [path]

[1-2 sentences: What is this? i18n setup present? Overall readiness?]

**Readiness:** Not ready / Partial / Good / Excellent

---

### Critical (breaks functionality)

| Location | Issue | Who's Affected | Fix |
|----------|-------|----------------|-----|
| form.tsx:17 | Hardcoded MM/DD/YYYY | Non-US users (ambiguous date) | `Intl.DateTimeFormat(locale)` |
| form.tsx:52 | Required "State" field | International users | Make optional or use "Region" |

### Serious (degraded experience)

| Location | Issue | Who's Affected | Fix |
|----------|-------|----------------|-----|
| card.tsx:34 | Fixed 200px width | German (+30% text) | Use flexible width |
| btn.tsx:72 | `text-align: left` | RTL users (Arabic, Hebrew) | `text-align: start` |

### Minor (improvements)

| Location | Issue | Fix |
|----------|-------|-----|
| utils.ts:15 | Hardcoded `$` | `Intl.NumberFormat` |

---

### Exceptions

- Timestamp in logger.ts:8 — internal debug, fine

### Summary

**5 issues**: 2 critical, 2 serious, 1 minor. Priority: date format and State field block international users.

**i18n setup:** None detected. Consider react-intl or i18next.
```

## Output Guidelines

- **Use tables** grouped by severity—Critical/Serious/Minor
- **"Who's Affected" column**—makes impact concrete
- **Fix column**—specific solution, not generic advice
- **Readiness rating upfront**—quick assessment
- **Summary as TL;DR**—counts, priority, i18n tooling status

## What Makes This Different From a Linter

A linter would flag every `margin-left`. You should:

1. **Understand the UI** - Is this actually directional or just spacing?
2. **Assess real impact** - Will this actually break for RTL users?
3. **Prioritize by visibility** - User-facing > internal tooling
4. **Consider the stack** - Does this project even need RTL support?

Your value is understanding **user impact**, not finding patterns.
