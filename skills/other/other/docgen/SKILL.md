---
name: docgen
description: Use when user invokes /docgen to generate or update documentation. Also triggers on "generate docs", "update the README", "write the changelog". Accepts a doc type (readme, api, architecture, changelog) and optional scope. Always outputs to conversation first and asks before writing to disk. Do NOT use for explaining code behavior — use /explain instead.
---

# Documentation Generator

## Overview

Generate or update project documentation from the codebase — READMEs, API references, architecture overviews, and changelogs. Designed to produce accurate, non-padded docs that match the project's existing style.

**Core principles:**
1. **Generate to conversation first.** Never write a file without asking. Always: "Want me to write this to [path]?"
2. **Preserve manual content.** If a doc already exists, identify what's outdated vs. what to keep. Don't blow away prose that was written by hand.
3. **Detect existing style.** Match the formatting, heading levels, and tone of existing docs in the project.
4. **No filler.** Omit empty or generic sections rather than padding them with boilerplate.

## Invocation Examples

```
/docgen readme                          # generate or update project README
/docgen readme src/auth/                # README for a subdirectory or package
/docgen api src/routes/                 # API endpoint documentation
/docgen architecture                    # architecture overview from codebase structure
/docgen changelog v0.2.0..v0.3.0       # changelog from git history for a version range
```

## Workflow Order (MANDATORY)

**You MUST follow this order. No skipping steps.**

---

### Step 1: Parse Input

Determine doc type and scope:

| Doc Type | Detection | Scope Default |
|----------|-----------|---------------|
| `readme` | First arg is "readme" | Project root or specified path |
| `api` | First arg is "api" | Specified path (required); error if missing |
| `architecture` | First arg is "architecture" | Project root |
| `changelog` | First arg is "changelog" | Optional git range (e.g. `v0.2.0..v0.3.0`); defaults to recent history |

If no argument or unrecognized type: say "Usage: `/docgen readme`, `/docgen api src/routes/`, `/docgen architecture`, `/docgen changelog [range]`." Then stop.

If `api` is invoked without a path: say "Please provide a path. Example: `/docgen api src/routes/`." Then stop.

---

### Step 2: Gather Context

Context to gather varies by doc type:

**readme:**
- List the project root (or specified subdirectory) to understand structure
- Read `package.json`, `go.mod`, `pyproject.toml`, or equivalent (for name, version, description, dependencies)
- Read entry point files (main, index, cmd/) — top 3-5 most important
- If a CLAUDE.md exists at the project root, read it (especially Architecture and Commands sections)
- Read any existing README to understand what's already there

**api:**
- List and read the specified directory (routers, handlers, controllers)
- Identify route definitions: look for patterns like `router.GET`, `app.post`, `@app.route`, `r.HandleFunc`
- Read the top 5-10 route-defining files
- Note authentication patterns, request/response shapes (from types, schemas, or inline validation)

**architecture:**
- Get the directory tree (2-3 levels deep)
- Read CLAUDE.md if it exists (Architecture section)
- Read the primary entry point(s)
- Identify key packages/modules and their roles from structure + names

**changelog:**
- Run `git log --oneline [range]` to get commits
- If no range given, use recent commits since last tag: `git log $(git describe --tags --abbrev=0)..HEAD --oneline`
- Group commits by conventional commit type (feat, fix, docs, refactor, chore, perf, test)
- Deduplicate: merge commit messages, fixup commits, and WIP commits are filtered out

---

### Step 3: Check Existing Docs

Before generating, check whether the target doc already exists:

- If **no existing doc**: generate from scratch
- If **existing doc found**: read it fully, then identify:
  - Sections that are outdated (version numbers, stale API descriptions, removed commands)
  - Sections that look manually written (custom prose, examples, migration notes) — **preserve these**
  - Sections that can be regenerated cleanly (install commands, dependency lists, endpoint tables)
  - State your preservation plan: "I'll keep the Deployment section as-is and regenerate Install and API sections."

---

### Step 4: Generate Document

Produce the document in the conversation. Structure by type:

**readme:**
```
# <project name>

<1-2 sentence description — what it does and who it's for>

## Install
<install command(s)>

## Usage
<primary usage pattern with example>

## Architecture  (omit if trivial)
<brief description of key components>

## Configuration  (omit if none)
<key config options>

## License
<license name>
```

**api:**
```
# API Reference

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /api/users | JWT | List users |
...

## <Endpoint Group Name>

### GET /api/users/:id
<description>

**Request**
- Path params: `id` (string) — user UUID

**Response**
- 200: `{ id, name, email, createdAt }`
- 404: `{ error: "not found" }`
```

**architecture:**
```
# Architecture

## Overview
<2-3 sentences: what the system does, how it's structured>

## Components
<table or list of top-level packages/modules with one-line descriptions>

## Data Flow
<how data moves through the system — input → processing → output>

## Key Files
<table: file/path → purpose>
```

**changelog:**
```
## <version or date range>

### Added
- <feat: commits>

### Fixed
- <fix: commits>

### Changed
- <refactor:, perf: commits>

### Internal
- <docs:, chore:, test: commits — summarized, not listed verbatim>
```

Apply style matching: if the existing project uses `##` for top-level sections, match that. If it uses sentence case headings, use sentence case.

---

### Step 5: Present for Review

After outputting the document to the conversation, ask:

```
Want me to write this to [path]?
```

If the user says yes: write the file using the Write or Edit tool.
- If updating an existing doc: use Edit for targeted changes, Write only for full replacement.
- Prefer Edit when preserving large sections of existing content.

If the user requests changes: make them in the conversation first, then ask again before writing.

---

## Scope Controls

- Output to conversation first — always ask before writing to disk
- Do not modify files that weren't specified in the invocation
- Preserve manually written prose — only regenerate stale or mechanical sections
- No file writes without explicit user confirmation ("Want me to write this to [path]?")

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing files without asking | Always confirm with "Want me to write this to [path]?" before writing. |
| Blowing away manual content | Read existing doc first. Identify what to preserve. State preservation plan before generating. |
| Padding empty sections | If there's no configuration, omit the Configuration section. No filler. |
| Dumping git log verbatim into changelog | Group by type. Deduplicate. Filter noise. The changelog should be readable, not a raw log. |
| Using wrong heading style | Match the project's existing doc style — check for `#` vs `##` top-level, title case vs sentence case. |
| Generating api docs without reading routes | Always read the actual route definition files, not just a description. |
