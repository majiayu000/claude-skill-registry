---
name: mcp-doc-generate
description: >
  Generate AI-written documentation for a specific directory or all
  undocumented directories. Creates structured READMEs optimized for
  both human and AI consumption, and updates the manifest.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
argument-hint: "<path> | all"
---

# MCP Doc Generate

Generate structured README documentation for a target directory (or all undocumented directories in bulk mode). Each generated README is optimized for both human developers and AI assistants. After writing, the manifest and tool action scripts are updated automatically.

## Step 1: Validate Target

Check `$ARGUMENTS` to determine the mode.

### Single path mode

If `$ARGUMENTS` is a directory path (e.g., `src/api`, `packages/auth`):

1. Verify the directory exists. If not, tell the user and stop.
2. Check if a README.md (or other doc file) already exists in that directory.
   - If yes, ask the user: "A README.md already exists at `{path}/README.md`. Overwrite, or skip?"
   - If overwrite, proceed to Step 3.
   - If skip, stop here.
3. Proceed to Step 3 with this single directory.

### Bulk mode (`all`)

If `$ARGUMENTS` is `all`, or if `$ARGUMENTS` is empty/not provided:

1. Scan the project for all undocumented significant directories (same logic as `/mcp-doc-scan` Step 2 and Step 3 "Undocumented" category).
2. Present the list to the user, grouped by priority:

   ```
   Undocumented directories found:

   Critical:
     - src/api/routes/
     - src/core/

   High:
     - src/services/
     - src/auth/

   Medium:
     - src/config/
     - src/middleware/

   Low:
     - scripts/
     - tests/helpers/
   ```

3. Ask the user via AskUserQuestion: "Generate READMEs for all of these, or select specific ones?"
   - If all, proceed with the full list.
   - If specific, let the user provide the subset.
4. Process directories **sequentially** using Step 4 (sequential bulk mode).

## Step 2: Load Manifest

Read `.mcp/manifest.yml`. If the file does not exist, tell the user:

```
No manifest found at .mcp/manifest.yml.
Run /mcp-doc-init to initialize the documentation manifest first.
```

Stop here if no manifest exists.

Parse the manifest to get the current resource list and project name.

## Step 3: Analyze Directory

For the target directory, read and analyze source files to understand what the directory contains.

### File sampling

- If the directory has 20 or fewer files, read all of them.
- If the directory has more than 20 files, sample strategically:
  - Always read: `index.*`, `main.*`, `app.*`, `mod.*`, `lib.*` (entry points)
  - Always read: `package.json`, `pyproject.toml`, `Cargo.toml` (module definition files)
  - Read files with the most imports/exports (use Grep to find `export` or `from` statements and pick the top files)
  - Read a representative sample of the remaining files (aim for ~20 total)

### What to extract

From each source file, note:
- **Exports** — public functions, classes, types, constants
- **Imports** — what this file depends on (internal and external)
- **Patterns** — design patterns used (factory, singleton, middleware chain, event-driven, etc.)
- **Framework usage** — Express routes, React components, database models, etc.
- **Key logic** — what the file does in one sentence

From the directory as a whole, determine:
- **Purpose** — what this directory is responsible for
- **Architecture** — how components relate to each other
- **Dependencies** — what it depends on and what depends on it
- **Patterns** — coding conventions specific to this directory

## Step 4: Sequential Bulk Mode

When processing multiple directories (bulk mode from Step 1), handle each directory one at a time:

1. Analyze the directory (Step 3).
2. Generate the README (Step 5).
3. Show the generated README content to the user.
4. Ask via AskUserQuestion: "Accept this README, edit it, or skip this directory?"
   - **Accept** — write the file and update the manifest. Continue to next directory.
   - **Edit** — let the user describe changes, regenerate or edit the README, then ask again.
   - **Skip** — do not write the file. Continue to next directory.
5. After processing all directories, proceed to Step 6 (manifest update) and Step 7 (tool regeneration) once for all accepted READMEs.

## Step 5: Generate README

Write a structured README.md to the target directory. Use the following template, adapting sections based on what the directory actually contains.

```markdown
# {Directory Name}

{One-paragraph purpose statement. What this directory is responsible for
and why it exists. Written for both humans and AI assistants.}

## Key Files

| File | Purpose |
|------|---------|
| handler.ts | HTTP request handlers for user endpoints |
| service.ts | Business logic for user CRUD operations |
| types.ts | TypeScript interfaces and type definitions |

## Architecture

{How components in this directory relate to each other and to the rest
of the project. Describe the data flow, layering, or module boundaries.}

## Patterns & Conventions

{Coding patterns specific to this directory. Error handling approach,
naming conventions, module organization rules, etc.}

## Dependencies

**Depends on:** {internal modules this directory imports from}
**Used by:** {other directories/modules that import from here}
**External:** {key third-party packages used}

## Usage

{Example imports, initialization, and common operations. Show how other
parts of the codebase use this module.}
```

### Template adaptation rules

- **Omit sections** that have no meaningful content (e.g., skip "Dependencies" if there are none)
- **Add sections** when the directory warrants them:
  - `## API` — for directories that define HTTP endpoints, list routes with methods
  - `## Configuration` — for directories with environment variables or config options
  - `## Testing` — if the directory has specific testing patterns or fixtures
  - `## Migration Notes` — if there are migration scripts or version-specific logic
- Keep the README **concise but complete** — prefer tables and bullet lists over long prose
- Include **code examples** only when they genuinely help understanding (e.g., initialization patterns, typical usage)

## Step 6: Update Manifest

For each newly created README:

1. Generate a resource name using the path-to-name conversion rules (replace `/` with `_`, remove extension, lowercase, detect collisions).
2. Generate a URI relative to `.mcp/` (prefix with `../`).
3. Write a one-sentence description based on the README content.
4. Add the resource entry to `.mcp/manifest.yml`:

```yaml
  - name: src_api_routes_readme
    uri: ../src/api/routes/README.md
    description: "HTTP route handlers for user, auth, and admin endpoints"
    mimeType: text/markdown
```

## Step 7: Regenerate Tools

After all manifest changes are complete, regenerate all three default action scripts with the updated index data:

1. **Rebuild the full index** — re-read all resources listed in the manifest (including newly added ones). Extract title, sections, scope, tags, description for each.

2. **Regenerate action files:**
   - `.mcp/actions/search-docs.js` — updated INDEX array with new entries
   - `.mcp/actions/get-applicable-docs.js` — updated INDEX array
   - `.mcp/actions/get-doc-tree.js` — updated DIRS array reflecting new documentation coverage

3. **Recompute SHA-256 hashes** for each action file:

   ```bash
   sha256sum .mcp/actions/search-docs.js | awk '{print "sha256:" $1}'
   sha256sum .mcp/actions/get-applicable-docs.js | awk '{print "sha256:" $1}'
   sha256sum .mcp/actions/get-doc-tree.js | awk '{print "sha256:" $1}'
   ```

4. **Update tool entries** in `.mcp/manifest.yml` with the new hashes.

5. **Rewrite default tool metadata** — when regenerating, also update the `title` and `description` fields on the three default tool entries in the manifest to use the structured `USE THIS WHEN` / `DO NOT USE WHEN` pattern (same format as `/mcp-doc-init` generates). Do not rewrite metadata for custom tools.

**Important:** Only regenerate the three default tools (`search_docs`, `get_applicable_docs`, `get_doc_tree`). Do not touch any custom tools created by `/mcp-doc-add-tool`.

## Step 8: Report

Present what was done:

```
Documentation generated:

  Created:
    - src/api/routes/README.md (analyzed 12 files)
    - src/services/README.md (analyzed 8 files)

  Skipped:
    - src/config/ (user chose to skip)

Manifest updated:
  - Added 2 new resource entries
  - Total resources: N

Tools regenerated:
  - search_docs (index: N entries, M sections)
  - get_applicable_docs (index: N entries)
  - get_doc_tree (N directories)
  - Hashes updated in manifest

Next steps:
  - Review the generated READMEs and edit as needed
  - Run /mcp-doc-sync if you modify any documentation files
  - Run /mcp-doc-scan to check remaining coverage gaps
```
