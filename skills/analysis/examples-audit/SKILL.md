---
name: examples-audit
description: Analyze mock data and examples for cultural assumptions, understanding what they communicate about who the product is for. Use when reviewing test data, documentation, or seed data.
allowed-tools: Read, Grep, Glob
user-invocable: true
---

# Examples Audit

Analyze mock data and examples for cultural assumptions, with emphasis on understanding what these choices communicate.

## Philosophy

This is not about finding "Christmas" and replacing it with "holiday". It's about asking:

> "What do our examples say about who we think our users are?"

Every example is a choice. When your demo shows a user ordering a hamburger for their Christmas party, paying with a credit card, and shipping to their house in California, you're painting a picture of your "default user." Everyone else is an edge case.

## Scope

The user may specify a file path, glob pattern, or directory. If not specified, ask what they'd like to check.

## Config Integration

Before starting, check for `.inclusion-config.md` in the project root.

If it exists:
1. **Read** scope decisions and acknowledged findings
2. **Skip** acknowledged findings (note them in output)
3. **Respect** scope decisions (e.g., if US-only, don't flag US address examples)
4. **Note** at the top of output: "Config loaded: .inclusion-config.md"

## Process

### 1. Read and Understand

First, **read the content** to understand:
- What is this? (test data, documentation, marketing, UI copy)
- Who sees this? (developers only, or end users?)
- What story are the examples telling?

### 2. Look for Patterns

Don't just flag individual terms. Look for patterns:
- Do ALL the examples assume US location?
- Do ALL the food references assume meat-eating?
- Do ALL the family references assume nuclear families?
- Do ALL the payment examples assume credit cards?

A single Christmas reference in otherwise diverse examples is different from a codebase where every example assumes Christian, Western, affluent users.

### 3. Understand the Assumptions

For each pattern, ask what it assumes:

**Holiday/Event examples**
- Christmas, Easter, Thanksgiving → Assumes Christian/Western holidays
- "Holiday season" in December → Assumes Northern hemisphere
- Birthday celebrations → Not all cultures celebrate birthdays
- Mother's Day, Father's Day → Can be painful; not universal

**Food/Dietary examples**
- Hamburgers, bacon, steak → Assumes meat-eating
- Pork → Excludes halal, kosher observers
- Beef → Excludes Hindu observers
- Alcohol → Excludes many religious/personal practices

**Location/Address examples**
- State, ZIP code → US-specific
- "Your home" → Assumes stable housing
- "Your car" → Assumes car ownership

**Payment examples**
- Credit card required → Excludes unbanked users
- USD prices → US-centric
- "Premium" tiers → Assumes disposable income

**Family examples**
- Mother/Father → Excludes diverse family structures
- Spouse → Assumes marriage
- "Your kids" → Assumes children; can be painful

### 4. Assess Impact

**High impact** (shapes perception):
- Onboarding flows and first-run experiences
- Marketing materials and landing pages
- Documentation that users read
- Demo data in screenshots/videos

**Medium impact** (still visible):
- Error messages and help text
- Email templates
- In-app examples and placeholders

**Lower impact** (internal):
- Unit test fixtures
- Development seed data
- Internal documentation

## Reference

For comprehensive checklists, see `references/examples-checklist.md`.

## Output Format

```markdown
## Examples Analysis: [path]

### Overview

[What kind of content is this? What story do the examples currently tell? Who is the "default user" these examples assume?]

### Patterns Found

#### [Assumption Category]

**The pattern:** [What you observed across multiple examples]

**What this assumes:** [The implicit assumption about users]

**Who this might exclude:** [Specific groups]

**Examples found:**

1. `[file]:[line]` - `[content]`
2. `[file]:[line]` - `[content]`

**Suggestions:**
- [Neutral alternative]
- [Or how to add diversity without removing everything]

#### [Next category...]

### What's Working Well

[Note any existing diversity or thoughtful choices]

### Recommendations

**Quick wins:**
- [Easy changes with high impact]

**Larger effort:**
- [Systemic changes that would help]

**Consider:**
- [Questions for the team to discuss]

### Summary

- **Assumption patterns found:** [count]
- **Visibility level:** [High / Medium / Low]
- **Recommendation:** [Overall guidance]
```

## What Makes This Different From a Linter

A linter would flag "Christmas". You should:

1. **See the pattern** - One Christmas reference vs. every example assuming Western holidays
2. **Understand the context** - Is this a greeting card app where holidays are the point?
3. **Assess visibility** - User-facing marketing vs. internal test data
4. **Suggest proportionally** - Sometimes add diversity; sometimes use neutral terms

Your value is understanding **what the examples communicate as a whole**.
