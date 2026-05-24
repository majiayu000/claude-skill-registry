---
description: Validate a convert-X-Y skill against meta-convert-dev (structure) and meta-convert-guide (content), create issues for gaps, update reference tables
argument-hint: <skill-name>
---

# Validate Language Conversion Skill

Validate a `convert-X-Y` skill against `meta-convert-dev` (structure) and `meta-convert-guide` (content quality) standards, automatically create GitHub issues for deviations/gaps, and update reference tables in the meta-skills.

## Arguments

- `$1` - Skill name (e.g., `convert-python-rust`, `convert-typescript-golang`)

## Quick Reference

| Step | Action                         | Output             |
| ---- | ------------------------------ | ------------------ |
| 1    | Validate skill exists          | Error if not found |
| 2    | Check structure compliance     | Deviations list    |
| 3    | Validate 8 Pillars coverage    | Coverage score     |
| 4    | Check content quality          | Quality report     |
| 5    | Create issues for gaps         | Issue links        |
| 6    | Update meta-convert-dev tables | Diff of changes    |
| 7    | Report summary                 | Validation report  |

## Workflow

### Step 1: Locate and Read Skill

1. Construct skill path: `components/skills/$1/SKILL.md`
2. Verify file exists
3. Read the skill file completely
4. Extract source and target languages from skill name

```bash
SKILL_PATH="components/skills/$1/SKILL.md"
# Extract languages: convert-python-rust → python, rust
SOURCE=$(echo "$1" | sed 's/convert-//' | cut -d'-' -f1)
TARGET=$(echo "$1" | sed 's/convert-//' | cut -d'-' -f2-)
```

If skill not found, report error and exit:

```markdown
## Error: Skill Not Found

Skill `$1` not found at `components/skills/$1/SKILL.md`

**Available conversion skills:**
[List from components/skills/convert-*/]
```

### Step 2: Read Meta-Skills for Comparison

Read both meta-skills to understand validation criteria:

1. **`components/skills/meta-convert-dev/SKILL.md`** - Skill structure:
   - Required sections
   - Naming conventions
   - Reference tables to update

2. **`components/skills/meta-convert-guide/SKILL.md`** - Content quality:
   - APTV workflow coverage
   - 8 Pillars content expectations (see `reference/` directory)
   - Example quality standards (see `examples/` directory)

### Step 3: Validate Structure Compliance

Check for required sections (each must exist as `## Section Name`):

| Section                         | Required    | Check                               |
| ------------------------------- | ----------- | ----------------------------------- |
| Frontmatter (name, description) | Yes         | Valid YAML                          |
| This Skill Extends              | Yes         | References meta-convert-dev         |
| This Skill Adds                 | Yes         | Lists additions                     |
| This Skill Does NOT Cover       | Yes         | Scope boundaries                    |
| Quick Reference                 | Yes         | Type mapping table                  |
| Type System Mapping             | Yes         | Primitives, Collections, Composites |
| Idiom Translation               | Yes         | At least 3 patterns                 |
| Error Handling                  | Yes         | Error model translation             |
| Concurrency Patterns            | Yes         | Async model translation             |
| Memory & Ownership              | Conditional | If GC↔ownership conversion         |
| Paradigm Translation            | Conditional | If paradigm shift                   |
| Common Pitfalls                 | Yes         | At least 5 pitfalls                 |
| Examples                        | Yes         | Simple, Medium, Complex             |
| See Also                        | Yes         | Related skills                      |

**Record deviations:**

```markdown
### Structure Deviations

| Section   | Status             | Issue         |
| --------- | ------------------ | ------------- |
| <section> | Missing/Incomplete | <description> |
```

### Step 4: Validate 8 Pillars Coverage

For each pillar, check if the skill addresses the translation.

> **See:** [meta-skill-validation-dev/checklists/8-pillars.md](../skills/meta-skill-validation-dev/checklists/8-pillars.md) for pillar definitions, detection patterns, and scoring rubric.

**Automated check:**

```bash
just validate-pillars $1
```

**Record coverage:**

```markdown
### 8 Pillars Coverage

| Pillar | Status | Score | Notes   |
| ------ | ------ | ----- | ------- |
| Module | ✓/~/✗  | X.X   | <notes> |
| ...    |        |       |         |
| **Total** | | **X.X/8** | |
```

### Step 5: Validate Content Quality

Check quality indicators against `meta-convert-guide` examples as reference:

| Quality Check       | Criteria                                              | Pass/Fail |
| ------------------- | ----------------------------------------------------- | --------- |
| Type mappings       | At least 15 primitive/composite mappings              |           |
| Idiom examples      | Each has source, target, and "why"                    |           |
| Code correctness    | Examples use valid syntax                             |           |
| Pitfalls            | Specific to language pair, not generic                |           |
| Example progression | Simple (5-15 lines), Medium (20-40), Complex (50-100) |           |

### Step 6: Create Issues for Gaps

For each deviation or gap found, create a GitHub issue.

> **See:** [meta-skill-validation-dev/templates/issue-templates.md](../skills/meta-skill-validation-dev/templates/issue-templates.md) for issue body templates and batch strategy.

**Issue title format:**

```
feedback($1): <gap-description>
```

**Create issues using:**

```bash
gh issue create --repo aRustyDev/ai \
  --title "feedback($1): <gap>" \
  --body "<body>"
```

**Collect all created issue URLs for the report.**

### Step 7: Update Meta-Convert-Dev Tables

Update the following tables in `components/skills/meta-convert-dev/SKILL.md`:

#### 7.1 Existing Conversion Skills Table

Locate the table under "Existing Conversion Skills" and ensure this skill is listed:

```markdown
| Skill | Description                            |
| ----- | -------------------------------------- |
| `$1`  | <Source> → <Target> (<key challenges>) |
```

#### 7.2 Skill Categories Table

Determine the category and add if not present:

| Category           | Criteria                      |
| ------------------ | ----------------------------- |
| Static → Static    | Both statically typed         |
| Dynamic → Static   | Source dynamic, target static |
| Static → Dynamic   | Source static, target dynamic |
| Dynamic → Dynamic  | Both dynamic                  |
| GC → Ownership     | Source GC, target ownership   |
| OOP → Functional   | Paradigm shift                |
| Platform Migration | Different runtime platforms   |

#### 7.3 Difficulty Assessment (if Step 3.5 exists in create-lang-conversion-skill)

Calculate difficulty score using the matrix:

| Factor       | Source→Target Analysis  | Score    |
| ------------ | ----------------------- | -------- |
| Type System  | same/mixed/opposite     | +0/+1/+2 |
| Paradigm     | same/related/opposite   | +0/+1/+2 |
| Memory Model | same/different/opposite | +0/+1/+2 |
| Concurrency  | same/related/different  | +0/+1/+2 |
| Ecosystem    | same/related/different  | +0/+1/+2 |

Add to difficulty examples table if not present.

### Step 8: Report Summary

Generate final validation report:

```markdown
## Validation Report: $1

### Overview

| Metric          | Value                           |
| --------------- | ------------------------------- |
| Skill           | `$1`                            |
| Source → Target | <Source> → <Target>             |
| Validation Date | <date>                          |
| Overall Status  | ✓ Pass / ⚠ Needs Work / ✗ Fail |

### Structure Compliance

| Required Sections | Present | Missing |
| ----------------- | ------- | ------- |
| Count             | X/Y     | [list]  |

### 8 Pillars Score

**Score: X.X/8**

| Pillar | Status |
| ------ | ------ |
| ...    | ✓/~/✗  |

### Quality Metrics

| Metric         | Value | Target |
| -------------- | ----- | ------ |
| Type mappings  | X     | ≥15    |
| Idiom patterns | X     | ≥4     |
| Pitfalls       | X     | ≥5     |
| Examples       | X     | 3      |

### Issues Created

| Issue | Title   | Severity   |
| ----- | ------- | ---------- |
| #XXX  | <title> | <severity> |

### Tables Updated

- [ ] Existing Conversion Skills table
- [ ] Skill Categories table
- [ ] Difficulty Assessment table

### Recommendations

1. <recommendation 1>
2. <recommendation 2>
```

## Examples

```
/validate-lang-conversion-skill convert-python-rust
/validate-lang-conversion-skill convert-typescript-golang
/validate-lang-conversion-skill convert-clojure-elixir
```

## Notes

- This command may modify `meta-convert-dev/SKILL.md` tables - changes should be committed
- Validates structure against `meta-convert-dev` and content quality against `meta-convert-guide`
- Issues are created with the `feedback($1):` prefix for easy filtering
- Run after creating a new conversion skill or after major updates
- Use with `/create-lang-conversion-skill` for a complete workflow

## References

| Resource | Purpose |
|----------|---------|
| [meta-skill-validation-dev](../skills/meta-skill-validation-dev/) | Shared validation checklists and templates |
| [meta-convert-dev](../skills/meta-convert-dev/) | Structure requirements for conversion skills |
| [meta-convert-guide](../skills/meta-convert-guide/) | Content quality standards |
