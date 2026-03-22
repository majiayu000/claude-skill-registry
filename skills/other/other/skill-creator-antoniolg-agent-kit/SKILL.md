---
name: skill-creator
description: Guide for creating or updating Agent Skills using the standardized SKILL.md specification, including naming rules, optional frontmatter fields, validation, packaging, and best practices for structuring scripts, references, and assets.
license: Apache-2.0
---

# Skill Creator

This skill provides a practical, spec-aligned workflow for creating and maintaining Agent Skills.

## Specification (Required Format)

### Directory structure

A skill is a directory containing at minimum a `SKILL.md` file:

```
skill-name/
└── SKILL.md
```

Optional directories: `scripts/`, `references/`, and `assets/`.

### SKILL.md frontmatter (required)

```
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

Optional fields:

```
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
compatibility: Requires git, python3, and internet access
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

| Field           | Required | Constraints |
| --------------- | -------- | ----------- |
| `name`          | Yes      | 1-64 chars; lowercase letters, numbers, hyphens; no leading/trailing or consecutive hyphens; must match parent directory |
| `description`   | Yes      | 1-1024 chars; must describe what the skill does and when to use it |
| `license`       | No       | Short license name or reference to bundled license file |
| `compatibility` | No       | 1-500 chars; environment requirements if needed |
| `metadata`      | No       | Arbitrary key/value mapping |
| `allowed-tools` | No       | Space-delimited list of pre-approved tools (experimental) |

#### `name` field rules

- Must be 1-64 characters
- Only lowercase letters, digits, and hyphens (`a-z`, `0-9`, `-`)
- Must not start or end with `-`
- Must not contain `--`
- Must match the skill directory name

Valid:

```
name: pdf-processing
name: data-analysis
name: code-review
```

Invalid:

```
name: PDF-Processing
name: -pdf
name: pdf--processing
```

#### `description` field rules

- Must be 1-1024 characters
- Should include both what the skill does and when to use it
- Include keywords that help agents route relevant tasks

Good:

```
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDFs, forms, or document extraction.
```

Poor:

```
description: Helps with PDFs.
```

## Core Principles

### Be concise

The context window is shared across system prompt, conversation, skill metadata, and task input. Assume the agent is capable and only include non-obvious, high-value information.

### Set appropriate degrees of freedom

- **High freedom**: heuristics and decision guidance
- **Medium freedom**: pseudocode or scripts with parameters
- **Low freedom**: deterministic scripts and strict sequences

Use tighter constraints when tasks are fragile, error-prone, or require high consistency.

## Anatomy of a Skill

A skill includes a required `SKILL.md` plus optional bundled resources:

```
skill-name/
├── SKILL.md
├── scripts/        # Executable helpers
├── references/     # Docs loaded on demand
└── assets/         # Templates, images, data
```

### scripts/

Use for repeatable code or fragile operations that benefit from deterministic execution.

### references/

Use for large or detailed docs that should load only on demand (schemas, API docs, policies).

### assets/

Use for static resources that get copied or reused in outputs (templates, images, fonts, boilerplate).

### What not to include

Avoid extra docs that do not directly help an agent complete tasks (README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, etc.).

## Progressive Disclosure

1. **Metadata** (name + description) always loads
2. **SKILL.md body** loads when the skill triggers
3. **Resources** load only when needed

Keep `SKILL.md` under 500 lines. Move deep references to `references/` and link them from SKILL.md.

### Patterns

**Pattern 1: High-level guide with references**

```
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- Form filling: See references/FORMS.md
- API reference: See references/REFERENCE.md
- Examples: See references/EXAMPLES.md
```

**Pattern 2: Domain-specific organization**

```
bigquery-skill/
├── SKILL.md
└── references/
    ├── finance.md
    ├── sales.md
    ├── product.md
    └── marketing.md
```

**Pattern 3: Conditional details**

```
# DOCX Processing

## Creating documents

Use docx-js for new documents. See references/DOCX-JS.md.

## Editing documents

For simple edits, modify the XML directly.

For tracked changes: references/REDLINING.md
For OOXML details: references/OOXML.md
```

Guidelines:

- Keep references one level deep from `SKILL.md`
- Add a table of contents for reference files over ~100 lines

## Skill Creation Process

1. Understand the skill with concrete examples
2. Plan reusable contents (scripts, references, assets)
3. Initialize a new skill
4. Edit SKILL.md and bundled resources
5. Validate and package
6. Iterate based on real usage

### Step 1: Understand with examples

Gather representative user requests and clarify edge cases. Avoid too many questions per message; start with the highest-impact unknowns.

### Step 2: Plan reusable contents

For each example, identify what should be scripted, documented, or templated. Convert repeated logic into scripts or reusable assets.

### Step 3: Initialize the skill

Use the initializer script (from this skill directory):

```
./scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates a new skill folder with a template `SKILL.md` plus example `scripts/`, `references/`, and `assets/` directories. Remove any unused examples.

### Step 4: Edit the skill

Write concise, action-oriented instructions. Use imperative language. Ensure the frontmatter matches the spec and the directory name.

Consult references if you need patterns:

- `references/workflows.md`
- `references/output-patterns.md`

### Step 5: Validate

Preferred validator (spec reference library):

```
skills-ref validate ./my-skill
```

Quick local validator (bundled with this skill):

```
./scripts/quick_validate.py ./my-skill
```

### Step 6: Package

```
./scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

The packager validates first, then creates `<skill-name>.skill` (zip format).

### Step 7: Iterate

Run the skill on real tasks, note failures or friction, and update SKILL.md or resources accordingly.

## File references

Use relative paths from the skill root:

```
See references/REFERENCE.md for details.
Run scripts/extract.py for extraction.
```

Avoid deeply nested reference chains.
