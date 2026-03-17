---
name: creating-skills
description: How to create new Agent Skills following the open standard. Use when authoring new skills, extending agent capabilities, or packaging specialized knowledge into reusable formats.
---

# Creating Skills

This skill teaches you how to create new Agent Skills following the [Agent Skills open standard](https://agentskills.io).

## What Is a Skill?

A skill is a folder containing a `SKILL.md` file that gives agents specialized capabilities. Skills can include:

- **Instructions** — How to perform a specific task
- **Scripts** — Executable code agents can run
- **References** — Additional documentation loaded on demand
- **Assets** — Templates, schemas, or other resources

## Directory Structure

At minimum, a skill is a directory with a `SKILL.md` file:

```
skill-name/
└── SKILL.md          # Required
```

For more complex skills:

```
skill-name/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

## SKILL.md Format

Every `SKILL.md` must have YAML frontmatter followed by Markdown content.

### Required Frontmatter

```yaml
---
name: skill-name
description: What this skill does and when to use it.
---
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | 1-64 chars, lowercase letters, numbers, hyphens only. Must match folder name. |
| `description` | Yes | 1-1024 chars. Describes what the skill does AND when to use it. |
| `license` | No | License name or reference to bundled license file. |
| `compatibility` | No | Environment requirements (runtime, tools, network access). |
| `metadata` | No | Arbitrary key-value pairs for additional properties. |

### Name Rules

The `name` field:
- Must be lowercase alphanumeric with hyphens (`a-z`, `0-9`, `-`)
- Must NOT start or end with `-`
- Must NOT contain consecutive hyphens (`--`)
- Must match the parent directory name

**Valid:** `git`, `code-review`, `pdf-processing`
**Invalid:** `Git`, `-git`, `git-`, `code--review`

### Description Best Practices

The description should include:
1. **What** the skill does
2. **When** to use it (trigger keywords)

Good:
```yaml
description: Git hygiene for multi-agent collaborative work. Use when performing version control operations, syncing with remote, committing changes, or ensuring work is properly shared with the team.
```

Poor:
```yaml
description: Helps with git.
```

## Body Content

The Markdown body after frontmatter contains the skill instructions. There are no format restrictions—write whatever helps agents perform the task effectively.

### Recommended Sections

1. **Core Principle** — The single most important concept
2. **When to Use** — Specific triggers or scenarios
3. **Step-by-Step Instructions** — How to perform the task
4. **Examples** — Inputs, outputs, edge cases
5. **Quick Reference** — Commands or checklists

## Progressive Disclosure

Skills should be structured for efficient context use:

| Layer | Size | When Loaded |
|-------|------|-------------|
| Metadata | ~100 tokens | At agent startup |
| Instructions | <5000 tokens | When skill is activated |
| References | As needed | Only when required |

**Keep your main SKILL.md under 500 lines.** Move detailed reference material to separate files in `references/`.

## File References

When referencing other files in your skill, use relative paths from the skill root:

```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
```

Keep file references one level deep from SKILL.md.

## Creating a New Skill

### Step 0: Check the existing skills

**Before creating a new skill, check if one already exists in the existing skills:**

```bash
# Option 1: Check the GitHub repository
# Visit: the skills directory
# Browse .claude/skills/ directories

# Option 2: Use WebFetch or WebSearch to check
# Search for skills related to your need
```

**What to check:**

1. **Browse by category:**
   - `core/` — Fundamental skills (git, bd, subagent, etc.)
   - `engineering/` — Software development (refactoring, tdd, etc.)
   - `devops/` — Infrastructure and deployment (ci-cd, etc.)
   - `documentation/` — Writing and docs (technical-writing, etc.)
   - `research/` — Investigation and analysis (technical-research, etc.)

2. **Search for keywords:**
   - Use the skill catalog's README or search the repository
   - Look for skills with similar names or descriptions

3. **Evaluate existing skills:**
   - If a skill exists that does what you need → Use it!
   - If a skill is close but needs enhancement → Consider extending it
   - If no skill exists → Proceed to create a new one

**Benefits of checking first:**

- ✅ Avoid duplicating work
- ✅ Discover related skills you didn't know existed
- ✅ Learn from existing skill patterns
- ✅ Maintain consistency across the catalog

**If you find a similar skill but need modifications:**

Consider contributing to the catalog instead of creating a project-specific version:
1. Fork the vibecoding-starter repository
2. Enhance the existing skill
3. Submit a pull request
4. Everyone benefits from the improvement!

---

### Step 1: Create the Directory

```bash
mkdir -p skills/my-skill-name
```

### Step 2: Create SKILL.md

```bash
cat > skills/my-skill-name/SKILL.md << 'EOF'
---
name: my-skill-name
description: Describe what this skill does and when to use it.
---

# My Skill Name

## Core Principle

[The single most important concept]

## When to Use

Use this skill when:
- [Trigger condition 1]
- [Trigger condition 2]

## Instructions

[Step-by-step instructions]

## Quick Reference

[Commands or checklists]
EOF
```

### Step 3: Update AGENTS.md

Add the skill to the Required Skills table in AGENTS.md:

```markdown
| [skills/my-skill-name](skills/my-skill-name) | Brief description | `first command` |
```

### Step 3.5: Update skills-index.json

Add the skill to `.claude/skills-index.json` in the appropriate category:

```json
{"id":"my-skill-name","desc":"Brief description of what it does and when to use it","path":".claude/category/my-skill-name"}
```

Then increment the `n` count at the top of the file.

### Step 4: Commit

```bash
git add skills/my-skill-name
git commit -m "feat: add my-skill-name skill"
git push
```

## Skill Quality Checklist

Before committing a new skill:

- [ ] **Checked skills catalog** — Verified no similar skill exists
- [ ] `name` is lowercase with hyphens only
- [ ] `name` matches the folder name
- [ ] `description` explains WHAT and WHEN
- [ ] Body has clear, actionable instructions
- [ ] Examples are included for complex tasks
- [ ] SKILL.md is under 500 lines
- [ ] Referenced in AGENTS.md if all agents need it
- [ ] **Consider contributing** — If skill is reusable, submit to vibecoding-starter repo
