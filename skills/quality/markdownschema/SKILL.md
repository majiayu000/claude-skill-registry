---
name: MarkdownSchema
description: "Create, derive, and validate .mdschema files for markdown documents. USE WHEN create schema, add schema, derive schema, validate schema, check schema, mdschema, lint schema, heading rules, frontmatter validation."
version: 0.1.0
---

# MarkdownSchema

Create and validate `.mdschema` files that enforce frontmatter fields and heading structure across forge artifacts. Wraps the `mdschema` CLI with forge-specific conventions.

## Workflow Routing

| Workflow | Trigger | Section |
|----------|---------|---------|
| **Create** | "create schema", "add schema", "new schema" | [Create Workflow](#create-workflow) |
| **Derive** | "derive schema", "infer schema" | @Derive.md |
| **Validate** | "validate", "check", "lint schema" | @Validate.md |

## Conventions

### Schema Filename

Always `.mdschema` (no `.yml` extension). Lives alongside the files it validates:

```
skills/.mdschema          # validates skills/*/SKILL.md
agents/.mdschema          # validates agents/*.md
.mdschema                 # validates *.md in current directory
```

### Field Requirements by Artifact Type

| Artifact | Required fields | Optional fields | max_depth |
|----------|----------------|-----------------|-----------|
| Skill | `name`, `description`, `version` | `argument-hint` | 3 |
| Agent | `name`, `description`, `version` | -- | 3 |
| Project docs | (frontmatter optional) | -- | 4 |

All schemas enforce `no_skip_levels: true`.

### Reference Schemas

Skill schema:

```yaml
frontmatter:
    fields:
        - name: name
        - name: description
        - name: version

heading_rules:
    no_skip_levels: true
    max_depth: 3
```

Agent schema:

```yaml
frontmatter:
    fields:
        - name: name
        - name: description
        - name: version

heading_rules:
    no_skip_levels: true
    max_depth: 3
```

Project docs schema:

```yaml
frontmatter:
    optional: true

heading_rules:
    no_skip_levels: true
    max_depth: 4
```

---

## Create Workflow

### Step 1: Determine target

Identify the directory and artifact type:
- `skills/` directory with `*/SKILL.md` files → skill schema
- `agents/` directory with `*.md` files → agent schema
- Project root or doc directory → project docs schema

If ambiguous, ask the user.

### Step 2: Check for existing schema

Look for `.mdschema` in the target directory. If one exists, show it and ask whether to replace or update.

### Step 3: Write the schema

Use the reference schema for the detected artifact type from the [conventions table](#field-requirements-by-artifact-type).

Write `.mdschema` to the target directory using the Write tool.

### Step 4: Validate

Run validation immediately to confirm the schema works:

```bash
mdschema check "<glob>" --schema <path>/.mdschema
```

Glob patterns by artifact type:
- Skills: `"skills/*/SKILL.md"`
- Agents: `"agents/*.md"`
- Project docs: `"*.md"`

Report results. If violations are found, present them and ask whether to fix the documents or adjust the schema.

---

@Derive.md

@Validate.md

## Constraints

- Schema files are always named `.mdschema` -- never `.mdschema.yml` or `.mdschema.yaml`
- Never make frontmatter fields optional unless the artifact type genuinely doesn't use them -- `version` should be required for skills and agents to catch nesting errors
- `no_skip_levels` is always `true` -- no exceptions
- If `mdschema` is not installed, tell the user: `brew install jackchuka/tap/mdschema`
