---
name: mcp-doc-scan
description: >
  Scan project and report documentation coverage. Finds undocumented
  directories, stale manifest entries, and prioritized recommendations.
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[path]"
---

# MCP Doc Coverage Scan

Scan the project (or a subtree) and report documentation coverage. Compares the current file system against the `.mcp/manifest.yml` to identify undocumented directories, stale entries, and missing index entries. Produces a prioritized recommendation list.

## Step 1: Load Manifest

Read `.mcp/manifest.yml` from the project root.

If the file does not exist, tell the user:

```
No manifest found at .mcp/manifest.yml.
Run /mcp-doc-init to initialize the documentation manifest first.
```

Stop here if no manifest exists.

Parse the manifest and extract:
- All resource entries (name, uri, description)
- Resolve each URI to a project-relative path (URIs are relative to `.mcp/`, so `../src/api/README.md` becomes `src/api/README.md`)

## Step 2: Scan Project

Find all documentation files and significant directories in the project.

### Subtree argument

If `$ARGUMENTS` is provided and non-empty, scope the scan to that subtree path only. For example, if `$ARGUMENTS` is `src/api`, only scan within `src/api/`.

If `$ARGUMENTS` is empty, scan the entire project.

### Documentation file discovery

Use Glob with the same patterns and exclude rules as `/mcp-doc-init`:

- `**/*.md`, `**/*.rst`, `**/*.txt` (doc-like only)
- Base excludes: `node_modules, .git, dist, build, coverage, __pycache__, .pytest_cache, target, vendor, .venv, .next, .nuxt, .cache, .turbo, tmp, .output, out`
- Ecosystem-specific excludes detected from root files

### Significant directory detection

A directory is "significant" (worth documenting) if it contains:
- Source code files (`.ts`, `.js`, `.py`, `.go`, `.rs`, `.java`, `.kt`, `.swift`, `.rb`, `.cs`, `.cpp`, `.c`, `.h`)
- Configuration files that define module boundaries (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`)
- Other directories with source code (i.e., is a parent of source dirs)

Skip directories that only contain generated output, test fixtures, or static assets (images, fonts).

## Step 3: Categorize

For each significant directory and documentation file, assign one of four categories:

### Category: Documented & Indexed

The directory has a documentation file (README.md or other doc) AND that file is listed as a resource in the manifest.

### Category: Documented, Not Indexed

The directory has a documentation file but it is NOT in the manifest. This means it was added after `/mcp-doc-init` was run, or was excluded during init.

Action: Suggest running `/mcp-doc-sync` to add these.

### Category: Undocumented

The directory is significant (contains source code or modules) but has no documentation file at all. Prioritize by importance:

| Priority | Directory characteristics | Examples |
|---|---|---|
| **Critical** | API/route directories, entry point directories, main source directories, core module directories | `src/api/`, `src/routes/`, `src/`, `app/`, `lib/`, `core/` |
| **High** | Business logic directories, shared utilities, auth/security modules, data model directories | `src/services/`, `src/utils/`, `src/auth/`, `src/models/`, `shared/` |
| **Medium** | Configuration directories, internal/private modules, middleware, helpers | `src/config/`, `src/middleware/`, `src/helpers/`, `internal/` |
| **Low** | Test directories, script directories, tooling, examples, fixtures | `tests/`, `scripts/`, `tools/`, `examples/`, `__tests__/` |

Use directory names and contents to assign priority. When in doubt, use these heuristics:
- Directories with more files = higher priority
- Directories imported by many other modules = higher priority
- Directories closer to the project root = higher priority

### Category: Stale

A manifest resource entry whose file no longer exists on disk. The URI resolves to a path that returns a file-not-found error.

Action: Suggest running `/mcp-doc-sync` to remove these.

## Step 4: Report

Present the coverage report with the following sections.

### Summary

```
Documentation Coverage Report
==============================
Scope: {entire project | subtree path}

Total significant directories: N
Documented & indexed:          M  (X%)
Documented, not indexed:       K
Undocumented:                  J
Stale manifest entries:        S
```

### Coverage table

```
| Directory | Status | Priority | Doc File | In Manifest |
|-----------|--------|----------|----------|-------------|
| src/ | Documented & indexed | — | src/README.md | Yes |
| src/api/ | Documented & indexed | — | src/api/README.md | Yes |
| src/utils/ | Undocumented | High | — | — |
| src/auth/ | Documented, not indexed | — | src/auth/README.md | No |
| src/legacy/ | Stale | — | (deleted) | Yes (stale) |
```

Sort the table: Stale entries first, then Undocumented (by priority: Critical > High > Medium > Low), then Documented not indexed, then Documented & indexed.

### Non-markdown docs

If any non-markdown documentation files were detected (`openapi.yaml`, `swagger.json`, `*.api.md`), list them:

```
Non-markdown documentation detected (not indexed):
  - openapi.yaml (src/api/)
  - swagger.json (src/api/)
```

### Recommendations

Provide prioritized next steps:

```
Recommendations:
  1. [Critical] Create documentation for: src/api/routes/, src/core/
  2. [High] Create documentation for: src/services/, src/auth/
  3. [Sync needed] Run /mcp-doc-sync to add K new docs and remove S stale entries
  4. [Medium] Consider documenting: src/config/, src/middleware/
  5. [Low] Optional: src/scripts/, tests/

Quick actions:
  - /mcp-doc-generate src/api/routes  — generate README for a specific directory
  - /mcp-doc-generate all             — generate READMEs for all undocumented directories
  - /mcp-doc-sync                     — sync manifest with current project state
```
