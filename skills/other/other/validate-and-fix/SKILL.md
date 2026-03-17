---
name: validate-and-fix
description: Run validation, parse errors, and auto-fix common skill issues like description format, orphan files, and naming mismatches
---

# Validate and Fix

Run the repository validation and automatically fix common issues.

## Usage

Run this skill when you want to check and fix all skills in the repository.

### Step 1: Run Validation

```bash
just validate-verbose
```

### Step 2: Parse and Categorize Errors

Common error types and their fixes:

#### Description contains newlines

**Error**: `description contains newline characters`

**Fix**: Edit the SKILL.md frontmatter to make the description a single line.
Remove any `\n` or `\r` characters. Do not use YAML block scalars (`|`, `>`,
`|-`, `>-`).

#### Name mismatch

**Error**: `name 'X' doesn't match directory 'Y'`

**Fix**: Edit the `name` field in frontmatter to match the parent directory name
exactly (kebab-case).

#### Orphan files

**Error**: `orphan file not referenced from SKILL.md: <path>`

**Fix**: Either:

1. Add a reference to the file in SKILL.md (markdown link or backtick), or
2. Delete the file if it's not needed

Files exempt from orphan checks: `package.json`, `bun.lock`, `.gitkeep`.

#### Invalid sources format

**Error**: `sources must use markdown link format`

**Fix**: Convert plain URLs to `[Title](url)` format in the `## Sources`
section.

#### Word count exceeded

**Error**: `word count exceeds 1500`

**Fix**: Reduce content. Move detailed reference material into `references/*.md`
files and link to them from SKILL.md.

#### Missing required fields

**Error**: `missing required field: name|description`

**Fix**: Add the missing field to the YAML frontmatter.

### Step 3: Re-validate

After applying fixes, run validation again:

```bash
just validate
```

Repeat until all errors are resolved.

### Step 4: Format

```bash
just fmt
```

### Step 5: Final Check

```bash
just check
```

This runs lint + typecheck to confirm everything passes.
