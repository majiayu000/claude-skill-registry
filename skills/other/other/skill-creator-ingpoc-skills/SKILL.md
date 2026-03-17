---
name: skill-creator
description: "Use when creating a new skill, updating an existing skill, or learning skill best practices. Load for extending Claude's capabilities with specialized workflows, tool integrations, or domain expertise. Covers skill anatomy, progressive disclosure (98% token savings), and the critical description-as-trigger pattern."
keywords: skill, create, template, workflow, progressive-disclosure
license: Complete terms in LICENSE.txt
---

# Skill Creator

Create modular, token-efficient skills that extend Claude's capabilities.

## Critical: Description = Trigger

The `description` field in frontmatter is how Claude decides when to load a skill.

| Location | Claude Sees | Timing |
|----------|-------------|--------|
| `description` (frontmatter) | Always in context | Before trigger |
| "When to Use" (body) | Only after triggered | Too late! |

**Pattern:**

```yaml
---
name: pdf-toolkit
# GOOD - trigger info in description
description: "Use when processing PDFs, extracting forms, merging documents, or filling PDF forms. Load for any PDF manipulation task."
keywords: pdf, extract, merge, forms
---
```

**Anti-pattern:**

```yaml
---
name: pdf-toolkit
# BAD - trigger info only in body (Claude can't see until AFTER trigger)
description: "PDF manipulation toolkit"
---

## When to Use  ← Claude never sees this before deciding to trigger!
```

## Skill Anatomy

```
skill-name/
├── SKILL.md (required)      # Workflow + metadata (<5k words)
├── scripts/ (optional)      # Executable code (0 tokens when run)
├── references/ (optional)   # Docs loaded as needed
└── assets/ (optional)       # Output resources (never loaded)
```

### Resource Types

| Type | When to Use | Token Cost | Examples |
|------|-------------|------------|----------|
| scripts/ | Repeated code, deterministic | **0** (executes) | rotate_pdf.py, validate.sh |
| references/ | Schemas, APIs, patterns | On-demand | schema.md, api_docs.md |
| assets/ | Templates, images | **0** (output only) | logo.png, template.docx |

**Key insight:** Scripts execute WITHOUT loading into context = 0 tokens.

## Progressive Disclosure (3 Levels)

| Level | What | When Loaded | Token Budget |
|-------|------|-------------|--------------|
| 1. Metadata | name + description | Always | ~100 words |
| 2. SKILL.md body | Instructions | On trigger | <5k words |
| 3. Resources | scripts/references/assets | As needed | Unlimited |

**Result:** 98% token savings vs loading everything upfront.

## Skill Creation Workflow

### 1. Gather Examples

Ask user:
- What functionality should the skill support?
- Example usage scenarios?
- What triggers this skill?

### 2. Plan Resources

| Question | Maps To |
|----------|---------|
| What code gets rewritten? | scripts/ |
| What schemas get rediscovered? | references/ |
| What boilerplate gets recreated? | assets/ |

### 3. Initialize

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

### 4. Write SKILL.md

**Order:**
1. Write description (with ALL trigger scenarios)
2. Add keywords
3. Write concise body (<5k words)
4. Reference bundled resources

**Frontmatter checklist:**
- [ ] `name`: lowercase, hyphens
- [ ] `description`: starts with "Use when...", includes ALL triggers
- [ ] `keywords`: discovery tags

**Body checklist:**
- [ ] Instructions (imperative form)
- [ ] Resource table (what to load when)
- [ ] Quick reference (common commands)

### 5. Validate & Package

```bash
scripts/quick_validate.py <path/to/skill>
scripts/package_skill.py <path/to/skill> [output-dir]
```

### 6. Iterate

Test on real tasks → identify gaps → update → test again.

## Key Rules

| Rule | Why |
|------|-----|
| Description = trigger | Claude decides from metadata, not body |
| Scripts = 0 tokens | Execute without loading into context |
| Tables over prose | 30-50% token savings |
| <5k words in SKILL.md | Move details to references/ |
| keywords for discovery | Helps Claude find relevant skills |

## References

| File | Load When |
|------|-----------|
| references/best_practices.md | Writing style, organization |
| references/progressive_disclosure.md | Token efficiency patterns |
| references/examples.md | Skill structure examples |
