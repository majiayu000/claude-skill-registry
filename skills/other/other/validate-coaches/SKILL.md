---
name: validate-coaches
description: Validates coach markdown files for required frontmatter fields, sections, and naming conventions
user-invocable: true
---

# Validate Coaches Skill

**CLAUDE: When this skill is invoked with `/validate-coaches`, validate all coach files in the coaches/ directory.**

## Purpose
Validates coach definition markdown files for schema compliance, required fields, section structure, and naming conventions.

## Usage
```bash
/validate-coaches
```

## Validation Steps

### Step 1: Find All Coach Files
```bash
find coaches -name "*-coach.md" -type f
```

### Step 2: For Each File, Validate

**CLAUDE: Read each coach file and verify:**

#### Frontmatter Validation (Required Fields)
- `name`: Must be kebab-case, must match filename (without `-coach.md`)
- `title`: Must be present and non-empty
- `category`: Must be one of: `training`, `nutrition`, `recovery`, `mobility`, `recipes`, `custom`

#### Frontmatter Validation (Optional Fields)
- `tags`: Must be an array if present
- `visibility`: Must be one of: `tenant`, `public`, `private` (defaults to `tenant`)
- `prerequisites.providers`: Array of provider names if present
- `prerequisites.min_activities`: Number if present
- `prerequisites.activity_types`: Array of activity types if present

#### Section Validation (Required)
- `## Purpose` - Must exist, must have content
- `## Instructions` - Must exist, must have content

#### Section Validation (Optional)
- `## When to Use`
- `## Example Inputs`
- `## Example Outputs`
- `## Success Criteria`
- `## Related Coaches`

### Step 3: Category Directory Check
```bash
# Each file should be in the correct category directory
# training/*.md should have category: training
# nutrition/*.md should have category: nutrition
# etc.
```

## Manual Validation Commands

### List All Coach Files
```bash
find coaches -name "*-coach.md" -type f | sort
```

### Check Frontmatter Syntax
```bash
# For each file, extract and validate YAML frontmatter
head -20 coaches/training/marathon-coach.md
```

### Verify Naming Convention
```bash
# Filename should be: {name}-coach.md
# Frontmatter name should match
```

### Load Coaches into Database
```bash
cargo run --bin seed-coaches
```
This command will fail if any coach file is malformed.

## Validation Checklist

For each coach file:
- [ ] Filename follows `{name}-coach.md` pattern
- [ ] Has valid YAML frontmatter between `---` markers
- [ ] `name` field matches filename (without `.md`)
- [ ] `title` field is present
- [ ] `category` field is valid
- [ ] `## Purpose` section exists with content
- [ ] `## Instructions` section exists with content
- [ ] File is in correct category directory

## Success Criteria
- All coach files pass validation
- `cargo run --bin seed-coaches` completes without errors
- No orphaned coach files (files without proper frontmatter)
- Category directories match frontmatter category values

## Example Valid Coach File

```markdown
---
name: example-coach
title: Example Coach
category: training
tags: [example, demo]
visibility: tenant
---

## Purpose
Brief description of what this coach specializes in.

## Instructions
You are an expert coach specializing in [area].
```

## Related Skills
- `test-intelligence-algorithms` - Algorithm validation
