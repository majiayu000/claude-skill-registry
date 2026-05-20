---
name: mcp-doc-sync
description: >
  Sync the git-doc-mcp manifest with current project state. Adds new
  docs not yet indexed, removes stale entries, refreshes descriptions
  and search index, and regenerates tool actions.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
argument-hint: ""
---

# MCP Doc Sync

Sync the `.mcp/manifest.yml` with the current project state. Detect new documentation files, stale entries, and updated content. Apply changes to the manifest and regenerate tool action scripts with fresh index data. Preserve any custom tools created by `/mcp-doc-add-tool`.

## Step 1: Load Manifest

Read `.mcp/manifest.yml` from the project root.

If the file does not exist, tell the user:

```
No manifest found at .mcp/manifest.yml.
Run /mcp-doc-init to initialize the documentation manifest first.
```

Stop here if no manifest exists.

Parse the manifest and extract:
- **Resources** — all resource entries with name, uri, description, mimeType
- **Tools** — all tool entries with name, action path, actionHash
- **Project metadata** — schemaVersion, name, version, description, instructions

Resolve each resource URI to a project-relative path (URIs are relative to `.mcp/`, so `../src/api/README.md` resolves to `src/api/README.md`).

## Step 2: Detect Changes

Compare the manifest against the current file system. Classify every difference into one of three categories.

### Category: NEW

Documentation files that exist on disk but are NOT listed as resources in the manifest.

Discovery process:
1. Scan the project with the same Glob patterns and exclude rules as `/mcp-doc-init`:
   - `**/*.md`, `**/*.rst`, `**/*.txt` (doc-like only)
   - Base excludes: `node_modules, .git, dist, build, coverage, __pycache__, .pytest_cache, target, vendor, .venv, .next, .nuxt, .cache, .turbo, tmp, .output, out`
   - Ecosystem-specific excludes from root files
2. Compare found files against manifest resource URIs
3. Any file found on disk but not in the manifest is classified as NEW

For each NEW file, pre-compute:
- Resource name (using path-to-name rules: replace `/` with `_`, remove extension, lowercase)
- URI relative to `.mcp/`
- Scope and tags (using the scope assignment rules below)
- Description (first paragraph after H1, or synthesized)

### Scope assignment rules for new entries

| Doc type | Scope value | Tags |
|---|---|---|
| `{dir}/README.md` | `{dir}` | — |
| Root `README.md` | `""` | `global` |
| Root `CONTRIBUTING.md`, `ARCHITECTURE.md`, `CHANGELOG.md` | `""` | `global` |
| `docs/*.md` at project root | `""` | `global`, plus auto-tagged by content |
| `docs/*.md` inside a subtree (e.g., `packages/auth/docs/guide.md`) | parent of `docs/` (e.g., `packages/auth`) | — |
| `ADR-*.md` or `adr-*.md` | their directory path | `adr` |
| Any other `*.md` | their directory path | — |
| `*.rst`, `*.txt` (doc-like) | their directory path | — |

### Category: STALE

Manifest resource entries whose files no longer exist on disk.

Detection process:
1. For each resource entry in the manifest, resolve its URI to a file path
2. Check if the file exists on disk
3. If the file does not exist, classify the entry as STALE

### Category: UPDATE

Manifest resource entries whose files still exist but whose content has changed in ways that affect the index.

Detection process:
1. For each resource entry whose file exists, read the file
2. Compare the current content against what the manifest/index has:
   - **Title changed** — the first H1 heading differs from the stored title
   - **Sections changed** — H2/H3 headers have been added, removed, or renamed
   - **Content changed** — section content excerpts differ significantly from stored excerpts
   - **Description outdated** — the file's first paragraph no longer matches the stored description
3. If any of the above changed, classify as UPDATE

For each UPDATE entry, pre-compute the refreshed values (new title, new sections, new description).

## Step 3: Present Changes

Show the user a table of all detected changes:

```
Manifest sync — changes detected:

| # | Type   | Resource Name          | Path                        | Proposed Action |
|---|--------|------------------------|-----------------------------|-----------------|
| 1 | NEW    | src_auth_readme        | src/auth/README.md          | Add to manifest |
| 2 | NEW    | docs_deployment        | docs/deployment.md          | Add to manifest |
| 3 | STALE  | src_legacy_readme      | src/legacy/README.md        | Remove from manifest |
| 4 | UPDATE | src_api_readme         | src/api/README.md           | Refresh description & sections |
| 5 | UPDATE | docs_coding-standards  | docs/coding-standards.md    | Refresh sections |

Total: 2 new, 1 stale, 2 updated
```

Ask the user via AskUserQuestion: "Apply all changes, or deselect specific items? (Enter item numbers to exclude, or 'all' to apply everything)"

Allow the user to deselect individual changes by number. Only apply the changes the user confirms.

If there are no changes detected, tell the user:

```
Manifest is up to date. No changes needed.
```

Stop here if nothing to do.

## Step 4: Apply Changes

Apply the confirmed changes to `.mcp/manifest.yml`:

### Applying NEW entries

For each confirmed NEW file:

1. Read the file and extract full index data:
   - Title (first H1 or filename)
   - Section headers and content excerpts (all paragraphs + bullets + tables, capped at ~500 chars per section)
   - Description (one-sentence summary)
   - Scope and tags (from scope assignment rules)
2. Add a resource entry to the manifest:

   ```yaml
     - name: src_auth_readme
       uri: ../src/auth/README.md
       description: "Authentication module with JWT tokens and OAuth2 integration"
       mimeType: text/markdown
   ```

3. Detect resource name collisions with existing entries and append `-2` suffix if needed.

### Applying STALE removals

For each confirmed STALE entry:
- Remove the resource entry from the manifest's `resources` list

### Applying UPDATE refreshes

For each confirmed UPDATE entry:
- Update the `description` field in the manifest resource entry
- The section-level data will be refreshed when tools are regenerated in Step 5

## Step 5: Regenerate Default Tools

Regenerate the three default action scripts with current data from all manifest resources.

### Which tools to regenerate

Only regenerate these three default tools:
- `search_docs` → `.mcp/actions/search-docs.js`
- `get_applicable_docs` → `.mcp/actions/get-applicable-docs.js`
- `get_doc_tree` → `.mcp/actions/get-doc-tree.js`

### Preserving custom tools

**Any tool NOT named `search_docs`, `get_applicable_docs`, or `get_doc_tree` is a custom tool** created by `/mcp-doc-add-tool` (or manually by the user). These tools must be preserved:

- Do NOT overwrite their action files in `.mcp/actions/`
- Do NOT modify their tool entries in the manifest
- Do NOT remove them from the manifest
- Do NOT recalculate their hashes

### Regeneration process

1. **Build fresh index** — for every resource in the manifest (after applying Step 4 changes), read the file and extract:
   - name, path, scope, title, description, tags
   - sections array: heading + content excerpt for each H2/H3 section (H4+ folded into parent, ~500 char cap)

2. **Regenerate `search-docs.js`** — write the full action script with the updated INDEX array embedded. Use the same code structure as generated by `/mcp-doc-init` (see that skill's Step 6a for the template).

3. **Regenerate `get-applicable-docs.js`** — write the full action script with the updated INDEX array embedded. Use the same code structure as `/mcp-doc-init` Step 6b.

4. **Regenerate `get-doc-tree.js`** — rebuild the DIRS array by scanning all significant directories and checking which have documentation. Write the full action script. Use the same code structure as `/mcp-doc-init` Step 6c.

5. **Recompute SHA-256 hashes:**

   ```bash
   sha256sum .mcp/actions/search-docs.js | awk '{print "sha256:" $1}'
   sha256sum .mcp/actions/get-applicable-docs.js | awk '{print "sha256:" $1}'
   sha256sum .mcp/actions/get-doc-tree.js | awk '{print "sha256:" $1}'
   ```

6. **Update tool entries** in the manifest with the new `actionHash` values for each of the three default tools.

7. **Rewrite default tool metadata** — update the `description` and `title` fields on the three default tool entries (`search_docs`, `get_applicable_docs`, `get_doc_tree`) in the manifest to use the structured format:

   ```yaml
   - name: search_docs
     title: Search Project Documentation
     description: |
       Search project documentation by keyword across titles, section headers, and content.

       USE THIS WHEN:
       - The user asks a question about the project and you need to find relevant docs
       - You need to discover what documentation exists on a topic
       - You want to search by keyword, tag, or path fragment

       DO NOT USE WHEN:
       - You already know the exact doc path (read the resource directly)
       - You need docs for a specific source file (use get_applicable_docs)
   ```

   **Custom tools** (any tool NOT named `search_docs`, `get_applicable_docs`, or `get_doc_tree`) must NOT have their `description` or `title` fields rewritten.

8. **Rewrite the top-level `instructions` field** in the manifest with the imperative format — ALWAYS/NEVER rules plus a decision tree:

   ```yaml
   instructions: |
     ALWAYS read relevant documentation before writing or modifying code.
     ALWAYS use search_docs when the user asks a question about the project.
     ALWAYS use get_applicable_docs before editing a file to check for applicable standards or conventions.
     NEVER guess at project conventions — search the docs first.

     Decision tree:
     - Need docs for a specific file? → get_applicable_docs
     - Looking for a topic or keyword? → search_docs
     - Want to see what's documented? → get_doc_tree
   ```

9. **Add welcome prompt if missing** — check if the manifest has a `prompts` section with a `welcome` entry. If not, add it:

   ```yaml
   prompts:
     - name: welcome
       title: Welcome - Get Started
       description: Introduction to project documentation and available tools
       messages:
         - role: user
           content:
             type: text
             text: |
               I'm exploring this project. Give me a brief overview of what documentation
               is available and what tools I can use, then ask what I'd like to learn about.
   ```

10. **Pin git-doc-mcp version** — read `.mcp.json` and check if the server command uses an unpinned `git-doc-mcp` (e.g., `npx git-doc-mcp` without a version). If so, update it to `npx git-doc-mcp@0.2.2`. If it already has a pinned version, leave it unchanged.

## Step 6: Report

Present what was done:

```
Manifest synced successfully.

Changes applied:
  - Added 2 new resources: src_auth_readme, docs_deployment
  - Removed 1 stale resource: src_legacy_readme
  - Refreshed 2 updated resources: src_api_readme, docs_coding-standards

Resource count: N total (was M before sync)

Tools regenerated:
  - search_docs — N entries, M total sections
  - get_applicable_docs — N entries
  - get_doc_tree — N directories
  - Hashes updated

Custom tools preserved (not modified):
  - get_coding_standards
  - get_team_api_docs

Next steps:
  - Run /mcp-doc-scan to check remaining coverage gaps
  - Run /mcp-doc-generate <path> to create docs for undocumented areas
```

If custom tools were preserved, always list them by name so the user knows they were not touched.
