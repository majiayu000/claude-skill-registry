---
name: skill-creator
description: >-
  Create, update, and package Claude Code skills from scratch or from existing
  content. Use when the user wants to build a new skill directory with SKILL.md,
  scripts, references, and assets; update an existing skill; or package a skill
  into a distributable .skill file. Covers the full lifecycle: gather
  requirements, plan reusable resources, initialize via init_skill.py, implement
  SKILL.md and bundled resources, validate, package via package_skill.py, and
  iterate based on real usage.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Glob
  - Grep
  - Read
  - Write
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - builder
    - skill-authoring
    - claude-code
    - developer-tools
  provenance:
    upstream_source: "skill-creator"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T15:20:15Z"
    generator_version: "1.0.0"
    intent_confidence: 0.83
---

# Skill Creator

Create production-ready Claude Code skills with proper structure, bundled resources, and validation.

## Overview

Skills are self-contained packages that extend Claude with specialized knowledge, workflows, and tools. Each skill has a required SKILL.md (frontmatter + instructions) and optional bundled resources (scripts/, references/, assets/).

**What it creates:**
- Complete skill directories with SKILL.md and bundled resources
- Python/Bash helper scripts for deterministic operations
- Reference documentation for domain expertise
- Distributable `.skill` packages (zip format)

**Design principles:**
- Context window is shared; keep SKILL.md under 500 lines
- Claude is already smart; only add knowledge Claude lacks
- Match freedom level to task fragility (high/medium/low)
- Progressive disclosure: metadata always loaded, body on trigger, resources on demand

## Skill Anatomy

Every skill has this structure:

- `SKILL.md` (required) -- Frontmatter (name + description, always in context ~100 words) plus body (instructions, loaded on trigger, under 5k words)
- `scripts/` (optional) -- Executable helpers (Python/Bash). Token-efficient; runs without loading into context.
- `references/` (optional) -- Domain docs Claude reads while working. Structure files over 100 lines with a ToC.
- `assets/` (optional) -- Output files (templates, images, fonts). Never loaded into context.

**Frontmatter rules:**
- `name`: Hyphen-case, max 64 chars
- `description`: Primary trigger. Include WHAT and WHEN. All trigger conditions here, not in body.

## Workflow

Six steps in order. Skip only with clear justification.

### Step 1: Gather Requirements

Ask for concrete usage examples (3-4 questions max per message):
- What functionality should the skill support?
- What are 2-3 example requests that trigger this skill?
- Are there specific tools, APIs, or file formats?

### Step 2: Plan Reusable Resources

For each example: (1) How to execute from scratch, (2) What helps when repeating.
- Repeated code -> `scripts/` (e.g., `scripts/rotate_pdf.py`)
- Reference knowledge -> `references/` (e.g., `references/schema.md`)
- Output templates -> `assets/` (e.g., `assets/hello-world/`)

### Step 3: Initialize

For new skills run the initializer script:

    python3 scripts/init_skill.py <name> --path <dir>

Creates directory with template SKILL.md and example resource dirs. Skip for existing skills.

### Step 4: Implement

1. **Scripts** -- Write and test helpers. Run each to verify.
2. **References** -- Add domain docs. See `references/output-patterns.md` and `references/workflow-patterns.md`.
3. **SKILL.md** -- Set name/description (triggers in description), write imperative instructions, reference bundled resources, delete unused example files.

**Progressive disclosure:** Keep SKILL.md lean. Move details to references/ and link them. For multi-domain skills, organize references by domain so Claude loads only what is needed.

### Step 5: Package

Run the packaging script:

    python3 scripts/package_skill.py <skill-folder> [output-dir]

Validates then creates `.skill` file. Fix errors and re-run if needed.

### Step 6: Iterate

Use on real tasks, note inefficiencies, update resources, test again.

## Freedom Levels

| Level | When | Approach |
|-------|------|----------|
| High | Multiple valid approaches | Text instructions |
| Medium | Preferred pattern exists | Pseudocode / parameterized scripts |
| Low | Fragile / consistency-critical | Specific scripts, few params |

## Exclusions

Do not create: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, or any user-facing documentation. Only include files an AI agent needs.

## Examples

### Example 1: Create a new skill

    User: Create a skill for editing PDFs -- rotate, merge, extract text.

    Assistant: I will create a pdf-editor skill.
    1. Requirements: rotate pages, merge files, extract text
    2. Resources planned: scripts/rotate_pdf.py, scripts/merge_pdf.py,
       scripts/extract_text.py, references/pypdf-api.md
    3. Initialize: python3 scripts/init_skill.py pdf-editor --path ./skills
    4. Implement scripts, test each, write SKILL.md
    5. Package: python3 scripts/package_skill.py skills/pdf-editor

    Created: skills/pdf-editor/ with SKILL.md, 3 scripts, 1 reference

### Example 2: Update an existing skill

    User: My bigquery skill triggers too rarely. Fix the description.

    Assistant: The description lacks trigger keywords. Updating frontmatter:
      Before: "Query BigQuery databases"
      After:  "Query BigQuery databases and analyze data. Use when the user
      asks to run SQL queries, explore tables, check schemas, or generate
      reports from BigQuery datasets."

    Updated SKILL.md frontmatter with expanded trigger conditions.

### Example 3: Add references to a skill

    User: My api-client skill keeps forgetting the auth flow. Add a reference.

    Assistant: I will add references/auth-flow.md with the OAuth2 flow:
    1. Read the current SKILL.md to understand the auth context
    2. Create references/auth-flow.md with token exchange steps
    3. Add a link in SKILL.md: "For auth details: See references/auth-flow.md"

    Created references/auth-flow.md (47 lines, ~350 tokens).

## Output Checklist

After creating or updating a skill, verify:

- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] `name` is hyphen-case, max 64 chars
- [ ] `description` includes what AND when to use, max 1024 chars
- [ ] Body is under 500 lines with real content (no placeholders)
- [ ] Scripts are tested and executable
- [ ] References contain actual domain expertise
- [ ] No extraneous files (README.md, CHANGELOG.md, etc.)
- [ ] Packaging succeeds via package_skill.py
