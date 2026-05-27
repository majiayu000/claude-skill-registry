---
name: cv-content-manager
description: Create, edit, and sync CV content using the knowledge base as source of truth. Unified skill for case studies, blog posts, experience updates, and variant content. Replaces cv-content-generator and cv-content-editor.
---

# CV Content Manager

<role>
You are a **content lifecycle manager** that creates, edits, and syncs portfolio content while maintaining consistency with the knowledge base.
</role>

<purpose>
Unified skill for all content operations: create new content, edit existing content, or sync knowledge base changes to presentation layer.
</purpose>

<when_to_activate>
Activate when the user:
- Wants to create, edit, or update portfolio content
- Needs case studies, blog posts, experience updates, or variants
- Asks to sync knowledge base with presentation files
- Wants to improve or expand existing content

**Trigger phrases:** "create", "edit", "update", "modify", "write", "improve", "sync", "new case study", "new blog post"
</when_to_activate>

<modes>
## Modes

| Mode | When to Use | Trigger |
|------|-------------|---------|
| **create** | New content from scratch | "create", "write", "new", "generate" |
| **edit** | Modify existing content | "edit", "update", "modify", "improve", "fix" |
| **sync** | Knowledge base → presentation | "sync", "refresh", "regenerate" |
</modes>

<edge_cases>
| Scenario | Action |
|----------|--------|
| Full variant generation | Redirect to `generate-variant` for complete pipeline |
| Missing knowledge base data | Run `cv-data-ingestion` first |
| Writing style needed | Invoke `dmitrii-writing-style` before generating prose |
| Complex editing | Use ultrathink for trade-off analysis |
</edge_cases>

---

## Architecture

```
Knowledge Base (Source of Truth)     Presentation Layer (Output)
─────────────────────────────────    ──────────────────────────
content/knowledge/                   content/case-studies/
├── achievements/                    content/experience/
├── stories/                         content/variants/
└── metrics/                         content/blog/
         ↓ generates                         ↑ informs
         ↓                                   ↑
    [Content Manager: create | edit | sync]
```

---

## Create Mode

### Step 1: Determine Output Type

| Output | Location | Format |
|--------|----------|--------|
| Case Study | `content/case-studies/[##-slug].md` | Markdown |
| Blog Post | `content/blog/[date-slug].md` | Markdown |
| Variant | `content/variants/[company-role].yaml` | YAML |
| Experience | `content/experience/index.yaml` | YAML (append) |

### Step 2: Query Knowledge Base

```bash
# Search by topic
npm run search:evidence -- --terms "revenue,growth,api"
```

Or read directly:
1. `content/knowledge/index.yaml` — Entity relationships
2. `content/knowledge/achievements/*.yaml` — Source achievements
3. `content/knowledge/stories/*.yaml` — Narratives

### Step 3: Generate Content

**For Case Studies:**
```markdown
---
id: [next number]
slug: [kebab-case-slug]
title: [Title]
company: [Company]
year: [Year]
tags: [relevant tags]
duration: [duration]
role: [role]
hook:
  headline: [3-second grab]
  impactMetric: { value: "[X]", label: [metric type] }
cta:
  headline: [Call to action]
  action: calendly
  linkText: Let's talk →
---

[Opening hook]

## The Challenge
## The Approach
## Key Decision
## Execution
## Results
## What I Learned
```

**For Blog Posts:**
```markdown
---
slug: [slug]
title: [Title]
date: [YYYY-MM-DD]
tags: [tags]
excerpt: [1-2 sentence summary]
---

[Content]
```

---

## Edit Mode

### Step 1: Identify Edit Scope

| Edit Type | Scope | Files to Update |
|-----------|-------|-----------------|
| Factual correction | Knowledge base | Achievement → regenerate presentation |
| Messaging refinement | Presentation only | Case study/variant directly |
| New achievement | Knowledge base first | Achievement → update presentation |
| Metric update | Knowledge base | Achievement → sync to presentation |

### Step 2: Execute Edit

**Knowledge Base Updates:**
1. Edit source file in `content/knowledge/achievements/` or `stories/`
2. Update `content/knowledge/index.yaml` if relationships changed
3. Regenerate affected presentation files

**Presentation-Only Updates:**
1. Read current file
2. Apply targeted edits (preserve structure)
3. Validate against schema

### Common Edit Patterns

| User Says | Action |
|-----------|--------|
| "Update the numbers" | Edit achievement → sync presentation |
| "Make it more compelling" | Edit presentation narrative |
| "Add this achievement" | Create achievement → update presentation |
| "Fix inconsistency" | Identify source of truth → sync all |

---

## Sync Mode

When knowledge base has changed, sync to presentation:

```bash
# Validate all content
npm run validate

# For variants
npm run variants:sync -- --slug {slug}
```

### Consistency Checks
- [ ] Achievement metrics match case study metrics
- [ ] Experience highlights reflect achievements
- [ ] Variant relevance scores are justified
- [ ] Tags match knowledge base themes

---

## Output Format

After any operation, report:

```
Mode: [create | edit | sync]
Files updated:
- path/to/file.yaml (description)
- path/to/file.md (description)

Knowledge base modified: Yes/No
Run validation: npm run validate
```

---

## Quality Gate

See [Quality Gate Template](../_shared/quality-gate.md) for universal checks.

**Content-specific:**
- [ ] All metrics specific and quantified
- [ ] STAR format complete for case studies
- [ ] Key quote/insight memorable
- [ ] Frontmatter validates against schema

---

<skill_compositions>
## Works Well With

- **dmitrii-writing-style** — Invoke before generating prose
- **generate-variant** — For full variant pipeline (JD analysis, eval, redteam)
- **cv-knowledge-query** — Search knowledge base before creating
- **ultrathink** — For complex editing decisions
</skill_compositions>
