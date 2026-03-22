---
name: mcp-doc-init
description: >
  Initialize documentation manifest for git-doc-mcp. Scans the project for
  documentation files (*.md, READMEs, ADRs, etc.), creates .mcp/manifest.yml
  with resource entries and search tools, and configures .mcp.json for the
  git-doc-mcp MCP server. Run this once when setting up project documentation.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
argument-hint: ""
---

# MCP Doc Initialization

Create a `.mcp/manifest.yml` with documentation resources and embedded-index tools, generate action scripts in `.mcp/actions/`, and configure `.mcp.json` with a git-doc-mcp server entry. The manifest indexes existing documentation files wherever they live in the project.

## Step 1: Check for Existing Config

Read `.mcp/manifest.yml` and `.mcp.json` from the project root.

| manifest.yml exists | .mcp.json has entry | Action |
|:---:|:---:|---|
| Yes | Yes | Show current config (resource count, tool count, server name), ask if user wants to reconfigure or keep. If keep, stop here. |
| Yes | No | Skip to Step 7 (.mcp.json generation only). |
| No | * | Full init (Steps 2-8). |

## Step 2: Scan Project for Documentation Files

Use Glob to find all documentation files. Apply base exclude patterns plus ecosystem-specific excludes.

### Base exclude patterns

Always exclude these directories from scanning:

```
node_modules, .git, dist, build, coverage, __pycache__, .pytest_cache,
target, vendor, .venv, .next, .nuxt, .cache, .turbo, tmp, .output, out
```

### Ecosystem-specific excludes

Detect the project ecosystem from root files and add extra excludes:

| Root file detected | Additional excludes |
|---|---|
| `package.json` | `node_modules/**`, `.next/**`, `.nuxt/**`, `.turbo/**` |
| `pyproject.toml` or `requirements.txt` | `__pycache__/**`, `.pytest_cache/**`, `.venv/**`, `venv/**`, `.mypy_cache/**` |
| `Cargo.toml` | `target/**` |
| `go.mod` | `vendor/**` |
| `pom.xml` or `build.gradle` | `target/**`, `build/**`, `.gradle/**` |
| `Gemfile` | `vendor/bundle/**` |

### Glob patterns

Search for these patterns in non-excluded directories:

1. `**/*.md` — all markdown files
2. `**/*.rst` — reStructuredText files
3. `**/*.txt` — text files that may be documentation (filter to only doc-like ones: those containing headings, sections, or located in `docs/` directories)

### Prioritized files

Flag these as high-value documentation when found:

- `README.md` (at any level)
- `CONTRIBUTING.md`
- `ARCHITECTURE.md`
- `CHANGELOG.md`
- `docs/**/*.md`
- `ADR-*.md`, `adr-*.md`

### Non-markdown docs

Detect but do **not** index these — list them in the final report as "non-markdown docs found" for user awareness:

- `openapi.yaml`, `openapi.json`
- `swagger.yaml`, `swagger.json`
- `*.api.md` (API spec files)

## Step 2b: Large Project Detection

If >50 doc files found OR >100 directories scanned:

1. Tell the user: "This is a large project with N documentation files across M directories."

2. Ask via AskUserQuestion how to scope. Present these options:

   - **Scan everything** — index all docs found (may produce a large manifest)
   - **Specify include roots** — user provides paths (e.g., `packages/my-team`, `src/api`) and only docs under those roots are indexed
   - **Use CODEOWNERS/ownership file** — if a `CODEOWNERS` file exists, offer to filter by team pattern
   - **Other** — let user describe their scoping strategy

3. Re-scan with the chosen scope applied. Only docs matching the scope are carried forward to Step 3.

## Step 3: Build Documentation Map

For each documentation file found in the scan, read the file and extract structured data.

### Content extraction

For each file:

1. **Title** — the first H1 heading (`# ...`). If no H1 exists, use the filename without extension (e.g., `setup.md` becomes `Setup`).

2. **Section headers** — all H2, H3, and H4 headings.

3. **Section content excerpts** — for each H2/H3 section:
   - Include ALL paragraphs, bullet lists, and table content within the section
   - Cap at ~500 characters per section to control index size
   - Preserve bullet list items and table rows (these often contain requirements and key details)
   - Include H4+ subsections as part of their parent H2/H3 section content (do not create separate entries for H4+)

4. **Description** — a one-sentence summary of the file. Use the first paragraph after the H1, or synthesize from the content if no suitable paragraph exists.

### Scope assignment rules

Assign each file a `scope` and `tags` based on its location and type:

| Doc type | Scope value | Tags |
|---|---|---|
| `{dir}/README.md` | `{dir}` (e.g., `src/api`) | — |
| Root `README.md` | `""` (empty string) | `global` |
| Root `CONTRIBUTING.md`, `ARCHITECTURE.md`, `CHANGELOG.md` | `""` | `global` |
| `docs/*.md` at project root | `""` | `global`, plus auto-tagged by content |
| `docs/*.md` inside a subtree (e.g., `packages/auth/docs/guide.md`) | parent of `docs/` (e.g., `packages/auth`) | — |
| `ADR-*.md` or `adr-*.md` | their directory path | `adr` |
| Any other `*.md` | their directory path | — |
| `*.rst`, `*.txt` (doc-like) | their directory path | — |

### Auto-tagging

Generate tags from:
- Directory name (e.g., `src/api` adds `api`)
- Doc type keywords (CONTRIBUTING adds `contributing`, ADR adds `adr`)
- Content keywords — scan section headers for common topics: `auth`, `security`, `api`, `database`, `testing`, `deployment`, `config`, `standards`, `setup`, `migration`

### Resource naming

Convert file paths to resource names:
- Replace `/` with `_`
- Remove the file extension
- Lowercase everything

Examples:
- `README.md` → `readme`
- `src/api/README.md` → `src_api_readme`
- `docs/coding-standards.md` → `docs_coding-standards`

**Collision detection:** If two paths normalize to the same resource name, append `-2`, `-3` suffixes to subsequent entries.

### Index entry structure

Each file produces an index entry:

```js
{
  name: "src_api_readme",           // resource name
  path: "src/api/README.md",        // file path from project root
  scope: "src/api",                 // directory scope
  title: "API Module",              // first H1 or filename
  description: "REST API endpoints, middleware, and authentication",
  tags: ["api", "rest", "express", "middleware"],
  sections: [
    {
      heading: "Authentication",
      content: "JWT-based auth using passport.js. All routes require Bearer token. Tokens expire after 24h. Refresh tokens stored in httpOnly cookies."
    },
    {
      heading: "Error Handling",
      content: "All endpoints return structured errors:\n- 400: validation failures with field-level details\n- 401: missing or expired token\n- 403: insufficient permissions\n- 500: internal errors logged, generic message returned"
    }
  ]
}
```

## Step 4: Confirm with User

Present a summary of what was found:

```
Found N documentation files:
- M READMEs across directories
- K standalone docs (CONTRIBUTING, architecture, standards, etc.)
- J in docs/ directories
- P ADRs

Top-level directories: src/, docs/, packages/, ...
Non-markdown docs detected (not indexed): openapi.yaml, swagger.json, ...
```

Ask the user:
1. **Project name** — used in the manifest `name` field (suggest based on directory name or package.json `name`)
2. **Review the file list** — let user add or remove files from the index
3. **Confirm** — proceed with generation

Wait for explicit confirmation before proceeding.

## Step 5: Generate `.mcp/manifest.yml`

Create the `.mcp/` directory if it does not exist. Write `.mcp/manifest.yml` with:

```yaml
schemaVersion: "1.0"
name: {project-name}-docs
version: 1.0.0
description: "Documentation index for {project-name}"
instructions: |
  You are a documentation assistant for {project-name}.
  You MUST use the tools below to answer questions — do NOT rely on prior knowledge.

  MANDATORY RULES:
  - ALWAYS use at least one tool BEFORE answering any question about this project.
  - NEVER answer from memory alone — the documentation is the source of truth.
  - If a tool returns no results, try different keywords or a different tool before giving up.

  DECISION TREE — match the user's intent to a tool:
  User asks a specific question or has a keyword → search_docs
  User asks "what docs cover this file/directory?" → get_applicable_docs
  User wants to see documentation coverage or structure → get_doc_tree
  User wants to read a specific doc → use Resources directly
  If unsure which tool to use → search_docs (safest default)

prompts:
  - name: welcome
    title: Welcome - Get Started
    description: Introduction to {project-name} documentation and available tools
    messages:
      - role: user
        content:
          type: text
          text: |
            I'm exploring this project. Give me a brief overview of what documentation
            is available and what tools I can use, then ask what I'd like to learn about.

resources:
  - name: root_readme
    uri: ../README.md
    description: "Project overview, architecture, and getting started"
    mimeType: text/markdown
  - name: src_api_readme
    uri: ../src/api/README.md
    description: "REST API endpoints, middleware, and authentication"
    mimeType: text/markdown
  # ... one entry per indexed doc file
```

**URI paths:** All URIs are relative to the `.mcp/` directory. A file at `src/api/README.md` (relative to project root) gets URI `../src/api/README.md`. A file at project root gets URI `../README.md`.

Do NOT add tool entries yet — those are added in Step 6 after action files are generated and hashed.

## Step 6: Generate Tools (Embedded-Index Actions)

Create the `.mcp/actions/` directory. Generate three action scripts, each embedding the full index data built in Step 3.

### 6a: `search-docs.js`

Section-level search across all indexed documentation. The embedded INDEX array contains entries with title, description, tags, path, scope, and sections (headings + content excerpts).

Search logic:
- Match the query against: title, description, tags (array items), path, and each section's heading + content
- Case-insensitive matching
- Return matching docs with the specific sections that matched and the matched excerpt
- Sort results by relevance (title match > section heading match > content match)

```js
// Auto-generated by mcp-doc-init — do not edit manually
// Regenerate with /mcp-doc-sync
const INDEX = [
  // ... full index entries with sections
];

export default async function(input, ctx) {
  const q = (input.query || "").toLowerCase();
  if (!q) return { content: [{ type: "text", text: "Please provide a search query." }] };

  const results = [];
  for (const doc of INDEX) {
    const matchedSections = [];
    const titleMatch = doc.title.toLowerCase().includes(q);
    const descMatch = doc.description.toLowerCase().includes(q);
    const tagMatch = doc.tags.some(t => t.toLowerCase().includes(q));
    const pathMatch = doc.path.toLowerCase().includes(q);

    for (const sec of doc.sections) {
      if (sec.heading.toLowerCase().includes(q) || sec.content.toLowerCase().includes(q)) {
        matchedSections.push(sec);
      }
    }

    if (titleMatch || descMatch || tagMatch || pathMatch || matchedSections.length > 0) {
      results.push({
        name: doc.name,
        path: doc.path,
        title: doc.title,
        description: doc.description,
        matchedSections: matchedSections.length > 0
          ? matchedSections.map(s => `### ${s.heading}\n${s.content}`).join("\n\n")
          : null,
        relevance: (titleMatch ? 3 : 0) + (descMatch ? 2 : 0) + (tagMatch ? 2 : 0) + matchedSections.length
      });
    }
  }

  results.sort((a, b) => b.relevance - a.relevance);

  if (results.length === 0) {
    return { content: [{ type: "text", text: `No documentation found matching "${input.query}".` }] };
  }

  const text = results.map(r => {
    let entry = `- **${r.title}** (${r.path})\n  ${r.description}`;
    if (r.matchedSections) entry += `\n  Matched sections:\n${r.matchedSections}`;
    return entry;
  }).join("\n\n");

  const footer = `\n\n---\nNext steps:\n- Read a specific doc above using its resource URI\n- Use get_applicable_docs to find docs for a specific source file\n- Refine your search with different keywords`;
  return { content: [{ type: "text", text: `Found ${results.length} result(s) for "${input.query}":\n\n${text}${footer}` }] };
}
```

### 6b: `get-applicable-docs.js`

Given a source file path, returns all documentation that applies to it: direct parent docs, scope-matched docs, and global docs.

```js
// Auto-generated by mcp-doc-init — do not edit manually
// Regenerate with /mcp-doc-sync
const INDEX = [
  // ... entries with name, scope, tags, path, title, description
];

export default async function(input, ctx) {
  const p = (input.path || "").replace(/\\/g, "/");
  if (!p) return { content: [{ type: "text", text: "Please provide a file or directory path." }] };

  const results = INDEX.filter(doc =>
    doc.tags.includes("global") ||
    p === doc.scope ||
    p.startsWith(doc.scope + "/")
  );

  // Sort: most specific scope first, then globals at the end
  results.sort((a, b) => {
    const aGlobal = a.tags.includes("global") ? 1 : 0;
    const bGlobal = b.tags.includes("global") ? 1 : 0;
    if (aGlobal !== bGlobal) return aGlobal - bGlobal;
    return b.scope.length - a.scope.length;
  });

  if (results.length === 0) {
    return { content: [{ type: "text", text: `No documentation found applicable to "${p}".` }] };
  }

  const text = results.map(r => {
    const scopeNote = r.tags.includes("global") ? " (global)" : ` (scope: ${r.scope || "root"})`;
    return `- **${r.title}** (${r.path})${scopeNote}\n  ${r.description}`;
  }).join("\n\n");

  const footer = `\n\n---\nNext steps:\n- Read any doc above using its resource URI\n- Use search_docs to find specific topics within these docs\n- Use get_doc_tree to see the full documentation structure`;
  return { content: [{ type: "text", text: `Documentation applicable to "${p}":\n\n${text}${footer}` }] };
}
```

### 6c: `get-doc-tree.js`

Filterable documentation tree with coverage status. Embeds the full directory tree data.

```js
// Auto-generated by mcp-doc-init — do not edit manually
// Regenerate with /mcp-doc-sync
const DIRS = [
  // { path: "src", depth: 1, documented: true, docFile: "src/README.md" },
  // { path: "src/api", depth: 2, documented: true, docFile: "src/api/README.md" },
  // { path: "src/utils", depth: 2, documented: false, docFile: null },
];

export default async function(input, ctx) {
  const root = input.root || "";
  const maxDepth = input.maxDepth || 3;
  const undocOnly = input.undocumentedOnly || false;

  const rootDepthOffset = root === "" ? 0 : root.split("/").length;

  let filtered = DIRS.filter(d =>
    (root === "" || d.path === root || d.path.startsWith(root + "/")) &&
    d.depth <= maxDepth + rootDepthOffset &&
    (!undocOnly || !d.documented)
  );

  if (filtered.length === 0) {
    return { content: [{ type: "text", text: root ? `No directories found under "${root}".` : "No directories found." }] };
  }

  const total = filtered.length;
  const documented = filtered.filter(d => d.documented).length;
  const coverage = total > 0 ? Math.round((documented / total) * 100) : 0;

  const lines = filtered.map(d => {
    const indent = "  ".repeat(d.depth - rootDepthOffset - (root === "" ? 0 : 0));
    const icon = d.documented ? "[documented]" : "[no docs]";
    const docNote = d.docFile ? ` <- ${d.docFile}` : "";
    return `${indent}${d.path}/ ${icon}${docNote}`;
  });

  const header = `Documentation coverage: ${documented}/${total} directories (${coverage}%)\n`;
  const footer = `\n\n---\nNext steps:\n- Use search_docs to find specific topics\n- Use get_applicable_docs to find docs for a specific source file\n- Filter with undocumentedOnly: true to find gaps`;
  const text = header + "\n" + lines.join("\n") + footer;

  return { content: [{ type: "text", text }] };
}
```

### Hash computation

After writing each action file, compute its SHA-256 hash and add the tool entry to `.mcp/manifest.yml`:

```bash
sha256sum .mcp/actions/search-docs.js | awk '{print "sha256:" $1}'
sha256sum .mcp/actions/get-applicable-docs.js | awk '{print "sha256:" $1}'
sha256sum .mcp/actions/get-doc-tree.js | awk '{print "sha256:" $1}'
```

Add tool entries to the manifest with the computed hashes:

```yaml
tools:
  - name: search_docs
    title: Search Documentation
    description: |
      Search project documentation by keyword.
      Searches titles, section headers, summaries, tags, and file paths.

      USE THIS WHEN:
      - The user asks a question about the project
      - The user mentions a keyword, error, or concept
      - You need to find relevant documentation before answering
      - You're unsure which tool to use (this is the safest default)

      DO NOT USE WHEN:
      - You know the exact file path (use get_applicable_docs instead)
      - The user wants to see the documentation tree/structure (use get_doc_tree)

      Example: "How does authentication work?" / "What is the API rate limit?"
    inputSchema:
      type: object
      properties:
        query:
          type: string
          description: "Search keyword or phrase"
      required: [query]
    action: ./actions/search-docs.js
    actionHash: sha256:{computed-hash}
    annotations:
      readOnlyHint: true

  - name: get_applicable_docs
    title: Get Applicable Documentation
    description: |
      Given a source file or directory path, find all documentation that applies to it.
      Returns parent READMEs, scope-matched docs, and global docs sorted by specificity.

      USE THIS WHEN:
      - The user asks "what documentation covers this file/directory?"
      - You need context before modifying a specific file
      - The user provides a file path and wants related docs

      DO NOT USE WHEN:
      - The user has a general question without a specific file (use search_docs)
      - The user wants to browse the doc tree (use get_doc_tree)

      Example: "What docs apply to src/api/routes/users.ts?" / "Show me docs for the auth module"
    inputSchema:
      type: object
      properties:
        path:
          type: string
          description: "Source file or directory path (e.g., src/api/routes/users.ts)"
      required: [path]
    action: ./actions/get-applicable-docs.js
    actionHash: sha256:{computed-hash}
    annotations:
      readOnlyHint: true

  - name: get_doc_tree
    title: Documentation Tree
    description: |
      Get the project documentation tree with coverage status.
      Supports filtering by subtree, depth, and undocumented-only mode.

      USE THIS WHEN:
      - The user wants to see what documentation exists
      - The user asks about documentation coverage or gaps
      - The user wants to browse the project structure

      DO NOT USE WHEN:
      - The user has a specific question (use search_docs)
      - The user asks about a specific file (use get_applicable_docs)

      Example: "What directories have documentation?" / "Show me the doc tree" / "Which areas are undocumented?"
    inputSchema:
      type: object
      properties:
        root:
          type: string
          description: "Subtree root path (default: project root)"
        maxDepth:
          type: number
          description: "Maximum depth to display (default: 3)"
        undocumentedOnly:
          type: boolean
          description: "Only show undocumented directories (default: false)"
    action: ./actions/get-doc-tree.js
    actionHash: sha256:{computed-hash}
    annotations:
      readOnlyHint: true
```

## Step 7: Generate/Update `.mcp.json`

Read the existing `.mcp.json` if present. Preserve any existing MCP server entries. Add (or update) the git-doc-mcp entry using the project name from Step 4.

```json
{
  "mcpServers": {
    "{project-name}-docs": {
      "command": "npx",
      "args": ["-y", "git-doc-mcp@0.2.2", "--manifest", ".mcp/manifest.yml"]
    }
  }
}
```

If `.mcp.json` already exists with other servers, merge the new entry into the existing `mcpServers` object. Do not overwrite other entries.

## Step 8: Report

Present the final summary:

```
MCP Doc initialized for {project-name}.

Manifest:    .mcp/manifest.yml
MCP config:  .mcp.json
Server name: {project-name}-docs

Resources:   N documentation files indexed
Tools:       3 (search_docs, get_applicable_docs, get_doc_tree)

Indexed documentation:
  - M READMEs
  - K standalone docs
  - J docs/ directory files
  - P ADRs

Undocumented directories: X (run /mcp-doc-scan for details)

Next steps:
  - Run /mcp-doc-scan to see coverage report
  - Run /mcp-doc-generate <path> to create docs for undocumented areas
  - Run /mcp-doc-sync after adding or changing documentation files
  - Run /mcp-doc-add-tool to create custom search/filter tools
```
