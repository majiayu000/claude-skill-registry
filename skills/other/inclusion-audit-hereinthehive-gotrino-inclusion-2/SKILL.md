---
name: inclusion-audit
description: Comprehensive inclusion analysis of code, examining language, internationalization, assumptions, and who might be excluded. Thorough review for releases or major features.
allowed-tools: Read, Grep, Glob
user-invocable: true
---

# Inclusion Audit

Comprehensive inclusion analysis that examines code through the lens of who it serves and who it might exclude.

## Philosophy

This is not a checklist to pass. It's a way of seeing:

> "Every line of code makes assumptions about who will use it. What are ours?"

The goal isn't to find problems—it's to understand your code from the perspective of users who aren't like you. Users in different countries. Users with different abilities. Users with different family structures, beliefs, and circumstances.

**Note:** This is a thorough review. For quick checks, use the focused skills: `/language-check`, `/i18n-check`, `/names-check`, `/examples-audit`.

## Scope

The user may specify a file path, glob pattern, or directory. If not specified, ask what they'd like to check.

## Config Integration

Before starting, check for `.inclusion-config.md` in the project root.

If it exists:
1. **Read** scope decisions, priorities, and acknowledged findings
2. **Skip sections** that are out of scope (e.g., skip i18n section if US-only)
3. **Skip** acknowledged findings (note count in output)
4. **Respect** priorities when ordering recommendations
5. **Note** at the top of output:
   ```
   **Config loaded:** .inclusion-config.md
   **Skipped:** i18n (out of scope), 3 acknowledged findings
   ```

Core dignity checks (slurs, hostile language) always run regardless of config.

## Process

### 1. Understand the Context

Before analyzing, understand:
- What does this code do? Who uses it?
- What's the target audience? (Global? Specific regions? Enterprise? Consumer?)
- What's the visibility? (Internal tool? Public-facing app?)

This shapes what matters most.

### 2. The Core Question

Throughout your analysis, keep asking:

> **"What am I assuming about the person using this?"**

Every assumption is a potential exclusion.

### 3. Analysis Areas

#### Language

Read the code, comments, documentation, and UI text. Look for:
- Language that assumes gender, ability, or identity
- Terms with harmful history or associations
- Tone that might make some users feel unwelcome

**Your job:** Understand who reads this and how it might land.

#### Internationalization

Trace the user experience for someone outside the US. Look for:
- Dates, times, numbers, currency—how are they formatted?
- Layouts—do they assume left-to-right?
- Forms—do they require US-specific information?
- Text—can it expand for longer languages?

**Your job:** Identify where the experience breaks for international users.

#### Examples and Data

Look at mock data, test fixtures, and documentation examples:
- Who is the "default user" in these examples?
- What do the examples assume about holidays, food, family, location?
- How diverse are the names and scenarios?

**Your job:** Understand what the examples communicate about who the product is for.

#### Assumptions

Look at forms, flows, and features:
- What does onboarding assume about users?
- What do forms require users to disclose?
- Are there opt-outs for sensitive features?
- Do defaults respect user agency?

**Your job:** Find where assumptions become barriers.

#### Privacy and Choice

Look at data collection:
- Is personal information collected? Is it necessary?
- Can users decline to answer? Is "prefer not to say" available?
- Can users edit or delete their information?

**Your job:** Assess whether the code respects user autonomy.

### 4. Assess Holistically

After reviewing each area, step back:
- What's the overall inclusion posture of this code?
- What are the biggest gaps?
- What's working well?

## Reference

For detailed checklists:
- `references/language-terms.md` - Language issues
- `references/i18n-checklist.md` - Internationalization
- `references/diverse-names.md` - Name diversity
- `references/examples-checklist.md` - Example assumptions
- `references/assumption-test.md` - Assumption analysis

## Output Format

```markdown
## Inclusion Audit: [path]

**Scope:** [what was reviewed]
**Context:** [what this code does, who uses it]

### TL;DR

[2-3 sentences max. Summarize: how many critical/high issues, the main theme or pattern, where to look first. Example:]

> 3 critical issues, 6 high-priority. Main theme: the "default user" is assumed American, binary-gendered, and using a credit card. Start with the registration form's gender field and address handling.

---

### Language ([count] issues)

**Why this matters:** The words we use shape how people feel about our products. Non-inclusive language can make people feel unwelcome, excluded, or harmed.

[Findings with context and suggestions.]

### Internationalization ([count] issues)

**Why this matters:** Your users aren't all in the US. Hardcoded formats, layouts, and assumptions break the experience for international users.

[Findings by impact level. Note existing i18n infrastructure.]

### Examples and Data ([count] issues)

**Why this matters:** Examples reveal our assumptions. They signal who we think our "real" users are.

[Pattern analysis. What do the examples assume? Who's the "default user"?]

### Assumptions ([count] issues)

**Why this matters:** Every assumption is a potential exclusion. The question "What am I assuming?" uncovers hidden barriers.

[Analysis of forms, flows, and features. Who might be excluded?]

### Privacy and Choice ([count] issues)

**Why this matters:** Forcing users to disclose personal information without justification is invasive. Respecting user agency is foundational.

[Assessment of data collection and user control.]

### Accessibility Note

Technical accessibility (screen readers, keyboard navigation, etc.) is best tested with dedicated tools:
- **axe-core** or **pa11y** for runtime testing
- **eslint-plugin-jsx-a11y** for React linting
- **Lighthouse** for browser auditing

[Note if project has these tools. Recommend adding if not.]

---

### Summary

#### What's Working Well
[Only include this section if there are genuine positive patterns to reinforce. Don't force it—if everything needs work, skip this section and focus on priorities.]

#### Priority Issues

**Critical** (blocks access or causes harm):
[List with count]

**High** (excludes significant user groups):
[List with count]

**Medium** (enhances inclusion):
[List with count]

#### Recommended Next Steps
1. [Prioritized action]
2. [Prioritized action]
3. [Prioritized action]

#### Questions for the Team
- [Things that need discussion or decisions]
```

## Output Guidelines

- **Consolidate duplicates**: If the same issue (e.g., Christmas references) appears in multiple categories, mention it once in the most relevant section and reference it elsewhere rather than repeating the full analysis.
- **TL;DR is mandatory**: Busy readers need the headline first. Make it specific to this audit.
- **Counts help prioritization**: Include issue counts in section headers so readers can quickly see where the work is.
- **Skip empty sections**: If a category has no issues, note it briefly ("No i18n issues found") rather than padding.

## What Makes This Different

This isn't a compliance checklist. It's a lens for seeing your code differently.

A checklist asks: "Did we avoid bad words?"
This audit asks: "Who did we build this for? Who might we have left out?"

Your value is **perspective**, not detection.
