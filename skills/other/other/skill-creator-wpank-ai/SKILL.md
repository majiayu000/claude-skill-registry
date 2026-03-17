---
name: skill-creator
model: standard
description: |
  WHAT: Guide for creating effective AI agent skills - modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools.
  
  WHEN: User wants to create, write, author, or update a skill. User asks about skill structure, SKILL.md format, or how to package domain knowledge for AI agents.
  
  KEYWORDS: "create a skill", "make a skill", "new skill", "skill template", "SKILL.md", "agent skill", "write a skill", "skill structure", "package a skill"
---

# Skill Creator

Skills are modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a specialized one equipped with procedural knowledge.

## Core Principle: Concise is Key

The context window is a public good. Only add context Claude doesn't already have. Challenge each piece: "Does this justify its token cost?"

**Prefer concise examples over verbose explanations.**


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install skill-creator
```


---

## Skill Anatomy

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/      - Executable code
    ├── references/   - Documentation loaded as needed
    └── assets/       - Files used in output
```

### SKILL.md Frontmatter (required)

```yaml
---
name: skill-name
description: |
  WHAT: One sentence describing what this skill does.
  WHEN: When to use it (contexts, user phrases).
  KEYWORDS: trigger phrases in quotes
---
```

The description is the **only** thing Claude reads to decide if the skill triggers. Be comprehensive.

### Body (Markdown)

Instructions and guidance. Only loaded AFTER skill triggers. Keep under 500 lines.

---

## Bundled Resources

### scripts/
Executable code for deterministic or repeated tasks.
- Use when: Same code is rewritten repeatedly, or reliability is critical
- Example: `scripts/rotate_pdf.py`

### references/
Documentation loaded into context as needed.
- Use when: Claude should reference while working
- Examples: schemas, API docs, domain knowledge, detailed guides
- If >10k words, include grep patterns in SKILL.md
- Keep information in EITHER SKILL.md OR references, not both

### assets/
Files used in output, not loaded into context.
- Use when: Output needs these files
- Examples: templates, images, icons, boilerplate code

---

## Creation Workflow

### Step 1: Understand with Examples

Skip only if usage patterns are clearly understood.

Ask:
- "What functionality should this skill support?"
- "Give examples of how this skill would be used?"
- "What would a user say to trigger this skill?"

### Step 2: Plan Reusable Contents

For each example, identify:
1. What scripts would help? (repeated code)
2. What references would help? (domain knowledge)
3. What assets would help? (templates, files)

### Step 3: Initialize the Skill

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Creates:
- SKILL.md template with proper frontmatter
- Example `scripts/`, `references/`, `assets/` directories

### Step 4: Edit the Skill

**Implement resources first** (scripts, references, assets). May require user input for domain-specific content.

**Test scripts** by running them to ensure no bugs.

**Write SKILL.md** with:
- Clear frontmatter description
- Workflow steps in imperative form ("Run X", not "You should run X")
- Links to references with when-to-read guidance

### Step 5: Package the Skill

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Validates structure and creates `.skill` file for distribution.

### Step 6: Iterate

Use the skill on real tasks. Notice struggles. Update and test again.

---

## Progressive Disclosure Patterns

Keep SKILL.md lean. Split content when approaching 500 lines.

**Pattern 1: High-level guide with references**
```markdown
## Advanced features
- **Form filling**: See [FORMS.md](FORMS.md)
- **API reference**: See [REFERENCE.md](REFERENCE.md)
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

**Pattern 3: Framework/variant organization**
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

---

## Degrees of Freedom

Match specificity to task fragility:

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| High (text) | Multiple valid approaches | General guidelines |
| Medium (pseudocode) | Preferred pattern exists | Scripts with parameters |
| Low (specific scripts) | Fragile, consistency critical | Exact command sequences |

---

## Quality Checklist

- [ ] Description includes WHAT, WHEN, KEYWORDS
- [ ] SKILL.md under 500 lines
- [ ] References are one level deep (not nested)
- [ ] Long references have table of contents
- [ ] Scripts are tested and work
- [ ] No README.md, CHANGELOG.md, or extra documentation
- [ ] Information lives in ONE place (SKILL.md or references, not both)

---

## NEVER

- Create README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, or auxiliary docs
- Duplicate information between SKILL.md and references
- Include "When to Use" sections in the body (put in description)
- Create deeply nested reference hierarchies
- Add scripts without testing them
- Exceed 500 lines in SKILL.md
