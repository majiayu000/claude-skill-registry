---
name: website-copywriting
description: Website copy creation for CMS implementation. Use when writing website copy, page content, creating new pages, or rewriting existing pages. Triggers on "write copy", "website copy", "page content", "rewrite page", "create page".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# Website Copywriting Skill

This skill covers website copy creation optimized for CMS implementation and AEO extraction.

## Pre-Writing Checklist (CRITICAL)

Before writing ANY copy, complete these steps:

### 1. Check Existing Site Structure

```bash
# Fetch and review sitemap
curl -s [domain]/sitemap.xml
curl -s [domain]/sitemap_index.xml
```

Or use WebFetch to check actual live pages. NEVER create imaginary URLs.

### 2. Review Client Playbook/Brief

Always check for existing documentation:
- `clients/[client]/[client]-aeo-playbook.md`
- `clients/[client]/[client]-website-copy.md`
- Any style guides or brand guidelines

### 3. Understand CMS Requirements

Ask or determine:
- What CMS? (WordPress, Webflow, etc.)
- Copy-paste workflow or direct integration?
- Character limits for titles/meta?

## Formatting Rules (MANDATORY)

### No Em Dashes

**NEVER use em dashes (—)**. They trigger AI-detection paranoia.

| Bad | Good |
|-----|------|
| `clients — from CEOs to celebrities — trust us` | `clients, from CEOs to celebrities, trust us` |
| `results that are undetectable — guaranteed` | `results that are undetectable. Guaranteed.` |
| `€50,000 — worth every euro` | `€50,000: worth every euro` |

Replace em dashes with:
- Commas for parenthetical clauses
- Periods for emphasis breaks
- Colons for explanations

### Single-Line Backticks Only

**NEVER use multi-line code blocks** (triple backticks) for copy. They break CMS copy-paste.

❌ **Bad:**
```
This is paragraph one.

This is paragraph two.
```

✅ **Good:**
`This is paragraph one.`

`This is paragraph two.`

### Section Structure

Every section MUST have:
1. **Headline** - Short, punchy (2-6 words)
2. **Subheadline** - One sentence context
3. **Body** - The actual content

```markdown
## Section Name

**Headline:** `Your Headline Here`

**Subheadline:** `One sentence that provides context.`

**Body:** `The main content goes here in single-line backticks.`
```

### Page Metadata

Every page MUST include at top:

```markdown
# Page Name

**URL:** `/actual-url-from-sitemap/`
**Status:** NEW PAGE | REWRITE | LIVE
**Title:** `60 chars max | Brand | Key Phrase`
**Meta:** `155 chars max. Include key facts, pricing if applicable.`

---
```

## Content Density Rules

### No Thin Pages

Every page must have SUBSTANTIAL content:
- Minimum 5-6 sections
- Minimum 500 words
- Multiple subsections with real content
- FAQ section where appropriate

If a page would be thin, either:
1. Combine with another page
2. Add more valuable sections
3. Don't create it

### Headline + Subheadline for ALL Sections

No exceptions. Every section needs both:

❌ **Bad:**
```markdown
## Our Process

We have a great process...
```

✅ **Good:**
```markdown
## Process Section

**Headline:** `The FueGenix Experience`

**Subheadline:** `A bespoke journey from consultation to final result.`
```

## File Operations

### NEVER Delete Without Confirmation

When asked to "improve" or "update" pages:
- Edit existing files
- Do NOT delete and recreate
- Do NOT run `rm -rf` on directories

### Improving vs Replacing

- "Improve this" = Edit the existing file
- "Rewrite this" = Can replace content but keep file
- "Delete this" = Only then remove (with confirmation)

## Copy Checklist

Before delivering any page copy:

- [ ] URL matches actual sitemap/site structure
- [ ] Title tag present (60 chars max)
- [ ] Meta description present (155 chars max)
- [ ] No em dashes anywhere
- [ ] All copy in single-line backticks
- [ ] Every section has headline + subheadline
- [ ] Page has 5+ substantial sections
- [ ] Pricing mentioned if applicable
- [ ] First 50 words contain key facts
- [ ] CTA present at end

## Page Templates

### Standard Page

```markdown
# Page Name

**URL:** `/url/`
**Status:** NEW PAGE
**Title:** `Title | Brand | Category`
**Meta:** `155 char description with key facts and pricing.`

---

## Hero Section

**Headline:** `Main Page Headline`

**Subheadline:** `One sentence that summarizes the page purpose.`

---

## Introduction Section

**Heading:** `Section Heading`

**Subheadline:** `Context for this section.`

**Paragraph 1:** `First paragraph content.`

**Paragraph 2:** `Second paragraph content.`

---

## [Content Sections...]

---

## FAQ Section

**Q:** `Question one?`
**A:** `Answer one.`

**Q:** `Question two?`
**A:** `Answer two.`

---

## CTA Section

**Heading:** `Call to Action Headline`

**Paragraph:** `Compelling reason to take action.`

**CTA:** `Button Text`
```

### Comparison Page

```markdown
# Brand vs Competitor

**URL:** `/vs/competitor/`
**Status:** NEW PAGE - Critical for AEO
**Title:** `Brand vs Competitor | Comparison`
**Meta:** `Balanced comparison of Brand and Competitor. Key differences, pricing, and which is right for you.`

---

## Hero Section

**Headline:** `Brand vs Competitor`

**Subheadline:** `Choosing Between Premium Options`

---

## Introduction Section

**Paragraph 1:** `Context about both options.`

**Paragraph 2:** `Why this comparison matters.`

**Paragraph 3:** `Fair and balanced positioning.`

---

## Comparison Table Section

**Heading:** `Quick Comparison`

| Factor | Brand | Competitor |
|--------|-------|------------|
| **Location** | X | Y |
| **Specialization** | X | Y |
| **Investment** | €X | €Y |

---

## Decision Guide Section

**Heading:** `When to Choose Brand`

**Choose Brand if:**
- Reason 1
- Reason 2
- Reason 3

**Heading:** `When to Choose Competitor`

**Choose Competitor if:**
- Reason 1
- Reason 2
- Reason 3

---

## The Verdict Section

**Heading:** `The Verdict`

**Paragraph 1:** `Balanced conclusion.`

**Paragraph 2:** `Brand recommendation with specific criteria.`

---

## CTA Section

**Heading:** `Ready for Assessment?`

**CTA:** `Request Consultation`
```

## Common Mistakes to Avoid

1. **Creating imaginary URLs** - Always check sitemap first
2. **Em dashes** - Never use them
3. **Multi-line code blocks** - Use single backticks
4. **Missing meta tags** - Every page needs title + meta
5. **Thin pages** - Minimum 500 words, 5+ sections
6. **Missing subheadlines** - Every section needs headline + subheadline
7. **Deleting without asking** - Edit, don't delete
8. **Not checking playbook** - Reference existing docs first
9. **Duplicate content** - Don't repeat same info across pages
10. **Hedged language** - Use definitive statements

## Reference

- See `aeo-protocol-sop.md` for AEO methodology
- See `premium-aeo` skill for luxury brand specifics
- See `content-optimizer` agent for optimization workflow
- See `clients/fuegenix/pages/` for complete examples
