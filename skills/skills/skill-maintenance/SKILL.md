---
name: skill-maintenance
description: Use when creating, updating, auditing, or validating Agent Skills. Provides validation scripts and guidance for keeping skills accurate and compliant with the Agent Skills specification.
---

# Skill Maintenance

**When to use:** When creating new skills, updating outdated skills, or auditing skill quality.

---

## Validation Script

**Purpose:** Check skills for format compliance and invalid references.

**Usage:**

```bash
# Validate all skills
python scripts/validate_skills.py

# Validate one skill
python scripts/validate_skills.py layer-helpers

# JSON output
python scripts/validate_skills.py --format=json

# Also check if code references exist
python scripts/validate_skills.py --check-refs
```

**Checks performed:**
- YAML frontmatter starts with `---`
- Required fields: `name`, `description`
- `name` matches directory name, lowercase with hyphens
- `name` ≤ 64 chars, no consecutive hyphens
- `description` ≤ 1024 chars, non-empty
- Line count ≤ 500 (warning if exceeded)
- Code references exist (with `--check-refs`)

---

## Creating a New Skill

1. **Create directory:** `.github/skills/<skill-name>/`
2. **Create `SKILL.md`** with frontmatter:

```markdown
---
name: skill-name
description: Use when [trigger conditions]. Provides [capabilities].
---

# Skill Title

**When to use:** [Clear trigger description]

---

## Section 1

Instructions...

---

## Validation Checklist

- [ ] Check 1 **→ Consequence**
- [ ] Check 2 **→ Consequence**
```

3. **Validate:** `python scripts/validate_skills.py skill-name`

---

## Updating an Existing Skill

**When:** Architecture changed, code moved, or skill guidance is stale.

**Process:**

1. **Identify what changed** — code location, API, or rules
2. **Read the current skill** — understand existing structure
3. **Update ONLY affected sections** — don't reformat unrelated content
4. **Validate:** `python scripts/validate_skills.py <skill-name> --check-refs`
5. **Test:** Does the skill trigger correctly? Are examples still valid?

**Rules:**
- Keep changes minimal and precise
- Don't add historical context or migration notes
- Update validation checklists if rules changed
- Maintain existing tone and verbosity

---

## Skill Format Requirements

### Frontmatter (Required)

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | 1-64 chars, lowercase alphanumeric + hyphens, must match directory |
| `description` | Yes | 1-1024 chars, describe WHAT and WHEN |

### Name Rules

- Lowercase letters, numbers, hyphens only
- No leading/trailing hyphens
- No consecutive hyphens (`--`)
- Must match parent directory name exactly

### Description Guidelines

Good:
```yaml
description: Use when creating or modifying code in nomarr/helpers/. Helpers are pure utilities with NO nomarr.* imports.
```

Poor:
```yaml
description: Helper layer rules.
```

### Body Guidelines

- Keep under 500 lines (move details to `references/`)
- Use clear section headers with `---` separators
- Include code examples for patterns
- End with a **Validation Checklist**
- Reference files with relative paths

---

## Checking Reference Validity

Code references in skills can become stale when code moves.

```bash
# Find invalid references
python scripts/validate_skills.py --check-refs

# Check specific skill
python scripts/validate_skills.py layer-components --check-refs
```

**Fix invalid references:**
1. Identify the new location of the referenced code
2. Update the reference in the skill
3. Re-run validation to confirm

---

## Periodic Audit Workflow

Run monthly or after major refactors:

```bash
# 1. Validate all skills
python scripts/validate_skills.py --check-refs

# 2. Review any invalid references
# 3. Update stale skills
# 4. Re-validate
python scripts/validate_skills.py
```

---

## Skill Locations

Nomarr skills are organized by purpose:

| Skill | Purpose |
|-------|---------|
| `layer-*` | Architecture layer guidance |
| `code-discovery` | Codebase exploration tools |
| `code-generation` | Boilerplate generation |
| `quality-analysis` | QC and linting tools |
| `skill-maintenance` | This skill (meta) |

---

## Validation Checklist

Before committing skill changes, verify:

- [ ] Does frontmatter have `name` and `description`? **→ Required**
- [ ] Does `name` match directory name? **→ Required**
- [ ] Is `name` lowercase with hyphens only? **→ Required**
- [ ] Does `description` explain WHAT and WHEN? **→ Required**
- [ ] Are code references still valid? **→ Run `--check-refs`**
- [ ] Is the skill under 500 lines? **→ Move to `references/` if not**
- [ ] Does skill end with a validation checklist? **→ Recommended**
