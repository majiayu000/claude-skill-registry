---
name: docs-manager
description: Documentation management workflow for MkDocs sites and standalone markdown files — initialize, generate, update docs, and create change summaries.
dependencies:
  - deep-analysis
  - docs-writer
---

# Documentation Manager Workflow

Execute a structured 6-phase workflow for managing documentation. Supports two documentation formats (MkDocs sites and standalone markdown files) and three action types (generate, update, change summary).

## Phase Overview

Execute these phases in order, completing all applicable phases:

1. **Interactive Discovery** — Determine documentation type, format, and scope through user interaction
2. **Project Detection & Setup** — Detect project context, conditionally scaffold MkDocs
3. **Codebase Analysis** — Deep codebase exploration using the deep-analysis skill
4. **Documentation Planning** — Translate analysis findings into a concrete plan for user approval
5. **Documentation Generation** — Delegate to docs-writer to generate content
6. **Integration & Finalization** — Write files, validate, present results

---

## Phase 1: Interactive Discovery

**Goal:** Determine through user interaction what documentation to create and in what format.

### Step 1 — Infer intent from inputs

Parse the user's input to pre-fill selections:
- Keywords like "README", "CONTRIBUTING", "ARCHITECTURE" -> infer `basic-markdown`
- Keywords like "mkdocs", "docs site", "documentation site" -> infer `mkdocs`
- Keywords like "changelog", "release notes", "what changed" -> infer `change-summary`

If the intent is clear, present a summary for quick confirmation before proceeding (skip to Step 4). If ambiguous, proceed to Step 2.

### Step 2 — Q1: Documentation type

If the documentation type is ambiguous or needs confirmation, prompt the user:

```
What type of documentation would you like to create?
```

Options:
- **"MkDocs documentation site"** — Full docs site with mkdocs.yml, Material theme
- **"Basic markdown files"** — Standalone files like README.md, CONTRIBUTING.md, ARCHITECTURE.md
- **"Change summary"** — Changelog, release notes, commit message

Store as `DOC_TYPE` = `mkdocs` | `basic-markdown` | `change-summary`.

### Step 3 — Conditional follow-up questions

**If `DOC_TYPE = mkdocs`:**

Prompt the user — Existing project or new setup?
- **"Existing MkDocs project"** -> `MKDOCS_MODE = existing`
- **"New MkDocs setup"** -> `MKDOCS_MODE = new`

If `existing`: Prompt the user — What to do?
- **"Generate new pages"**
- **"Update existing pages"**
- **"Both — generate and update"**
Store as `ACTION`.

If `new`: Prompt the user — Scope?
- **"Full documentation"**
- **"Getting started only (minimal init)"**
- **"Custom pages"**
Store as `MKDOCS_SCOPE`. If custom, ask for desired pages (free text).

**If `DOC_TYPE = basic-markdown`:**

Prompt the user — Which files?
- **"README.md"**
- **"CONTRIBUTING.md"**
- **"ARCHITECTURE.md"**
- **"API documentation"**
Store as `MARKDOWN_FILES`. If "Other" is selected, ask for custom file paths/descriptions.

**If `DOC_TYPE = change-summary`:**

Prompt the user — What range?
- **"Since last tag"**
- **"Between two refs"**
- **"Recent changes"**
Follow up for specific range details (tag name, ref pair, etc.).

### Step 4 — Confirm selections

Present a summary of all selections and prompt the user:
- **"Proceed"**
- **"Change selections"**

If the user wants to change, loop back to the relevant question. Then proceed to Phase 2.

---

## Phase 2: Project Detection & Setup

**Goal:** Detect project context automatically, conditionally scaffold MkDocs.

### Step 1 — Detect project metadata (all paths)

- Check manifests: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`
- Execute: `git remote get-url origin 2>/dev/null`
- Note primary language and framework

### Step 2 — Check existing documentation (all paths)

- Search for files matching `docs/**/*.md`, `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`
- For MkDocs: check for `mkdocs.yml`/`mkdocs.yaml`, read if found

### Step 3 — MkDocs Initialization (only if `DOC_TYPE = mkdocs` AND `MKDOCS_MODE = new`)

1. Use this MkDocs configuration template:

   ```yaml
   site_name: PROJECT_NAME
   site_description: PROJECT_DESCRIPTION
   site_url: ""
   repo_url: REPO_URL
   repo_name: REPO_NAME

   theme:
     name: material
     features:
       - navigation.tabs
       - navigation.sections
       - navigation.expand
       - navigation.top
       - search.suggest
       - search.highlight
       - content.code.copy
       - content.tabs.link
     palette:
       - scheme: default
         primary: indigo
         accent: indigo
         toggle:
           icon: material/brightness-7
           name: Switch to dark mode
       - scheme: slate
         primary: indigo
         accent: indigo
         toggle:
           icon: material/brightness-4
           name: Switch to light mode

   markdown_extensions:
     - admonition
     - pymdownx.details
     - pymdownx.superfences:
         custom_fences:
           - name: mermaid
             class: mermaid
             format: !!python/name:pymdownx.superfences.fence_code_format
     - pymdownx.highlight:
         anchor_linenums: true
         line_spans: __span
         pygments_lang_guess: false
     - pymdownx.inlinehilite
     - pymdownx.tabbed:
         alternate_style: true
     - pymdownx.snippets
     - attr_list
     - md_in_html
     - toc:
         permalink: true

   nav:
     - Home: index.md
     - Getting Started: getting-started.md
   ```

   Field population:
   - `site_name`: From manifest (`name` in package.json, pyproject.toml, etc.) or directory name
   - `site_description`: From manifest `description` field, or summarize from README
   - `repo_url`: From `git remote get-url origin` (convert SSH to HTTPS if needed)
   - `repo_name`: Extract `owner/repo` from the remote URL
   - If not a git repository, omit `repo_url` and `repo_name`

2. Fill template with detected metadata (prompt the user if incomplete)
3. Generate `mkdocs.yml`, create `docs/index.md` and `docs/getting-started.md`
4. Present scaffold for confirmation before writing

If `MKDOCS_SCOPE = minimal` (getting started only): write the scaffold files and skip to Phase 6.

### Step 4 — Set action-specific context (for update/change-summary)

For **update** modes, determine the approach:
- **git-diff** — Update docs affected by recent code changes
- **full-scan** — Compare all source code against all docs for gap analysis
- **targeted** — Update specific pages or sections

For **change-summary**, execute: `git log` and `git diff --stat` for the determined range.

Proceed to Phase 3.

---

## Phase 3: Codebase Analysis

**Goal:** Deep codebase exploration using the deep-analysis skill.

**Skip conditions:**
- Skip for `change-summary` (uses git-based analysis instead — see below)
- Skip for MkDocs minimal init-only (`MKDOCS_SCOPE = minimal`)

### Step 1 — Build documentation-focused analysis context

Construct a specific context string based on Phase 1 selections:

| Selection | Analysis Context |
|-----------|-----------------|
| MkDocs generate | "Documentation generation — find all public APIs, architecture, integration points, and existing documentation..." |
| MkDocs update | "Documentation update — identify changes to public APIs, outdated references, documentation gaps..." |
| Basic markdown README | "Project overview — understand purpose, architecture, setup, key features, configuration, and dependencies..." |
| Basic markdown ARCHITECTURE | "Architecture documentation — map system structure, components, data flow, design decisions, key dependencies..." |
| Basic markdown API docs | "API documentation — find all public functions, classes, methods, types, their signatures and usage patterns..." |
| Basic markdown CONTRIBUTING | "Contribution guidelines — find dev workflow, testing setup, code style rules, commit conventions, CI process..." |
| Multiple files | Combine relevant contexts from above |

### Step 2 — Run deep-analysis

Refer to the **deep-analysis** skill (from the core-tools package) and follow its workflow. Pass the documentation-focused analysis context from Step 1.

### Step 3 — Supplemental analysis for update with git-diff mode

After deep-analysis, additionally:
1. Execute: `git diff --name-only [base-ref]` for changed files
2. Search file contents in existing docs for references to changed files/functions
3. Cross-reference with synthesis findings

### For change-summary path (instead of deep-analysis)

1. Execute: `git log --oneline [range]` and `git diff --stat [range]`
2. Delegate to an exploration specialist to analyze the changed files:
   ```
   Analysis context: Change summary for [range]
   Focus area: These files changed in the specified range:
   [list from git diff --stat]

   For each significant change, identify:
   - What was added, modified, or removed
   - Impact on public APIs and user-facing behavior
   - Whether any changes are breaking
   Return a structured report of your findings.
   ```

Proceed to Phase 4.

---

## Phase 4: Documentation Planning

**Goal:** Translate analysis findings into a concrete documentation plan.

### Step 1 — Produce plan based on doc type

**MkDocs:**
- Pages to create (with `docs/` paths)
- Pages to update (with specific sections)
- Proposed `mkdocs.yml` nav updates
- Page dependency ordering (independent pages first, then pages that cross-reference them)

**Basic Markdown:**
- Files to create/update (with target paths)
- Proposed structure/outline for each file
- Content scope per file

**Change Summary:**
- Output formats to generate (Format 1: Changelog, Format 2: Commit message, Format 3: MkDocs page — only if MkDocs site exists)
- Range confirmation
- Scope of changes

### Step 2 — User approval

Prompt the user:
- **"Approve the plan as-is"**
- **"Modify the plan"** (describe changes)
- **"Reduce scope"** (select specific items only)

Proceed to Phase 5.

---

## Phase 5: Documentation Generation

**Goal:** Generate content using the docs-writer skill.

### Step 1 — Load templates

- If `DOC_TYPE = change-summary`: Use the change summary formats:
  - **Format 1: Markdown Changelog** — Keep a Changelog conventions. Imperative mood, one entry per change, focus on user impact.
  - **Format 2: Git Commit Message** — Conventional Commits style. Subject max 72 chars, imperative mood, explain "why" in body.
  - **Format 3: MkDocs Page** — Full documentation page with highlights, features, improvements, breaking changes (only if MkDocs site exists).

- If `DOC_TYPE = basic-markdown`: See **references/markdown-file-templates.md** for structural templates.

### Step 2 — Group by dependency

- **Independent pages/files** — Can be written without referencing other new content
- **Dependent pages/files** — Reference or summarize content from other pages

### Step 3 — Delegate to docs-writer

Delegate to the **docs-writer** skill for each page/file. Launch independent pages/files in parallel, then sequential for dependent ones.

**MkDocs prompt template:**
```
Documentation task: [page type]
Target file: [docs/path/to/page.md]
Output format: MkDocs
Project: [project name] at [project root]

MkDocs site context:
- Theme: Material for MkDocs
- Extensions available: admonitions, code highlighting, tabbed content, Mermaid diagrams
- Diagram guidance: Use Mermaid for all diagrams with dark text on nodes for readability.
- Existing pages: [list]

Exploration findings: [relevant findings]
Existing page content: [current content or "New page"]

Generate the complete page content in MkDocs-flavored Markdown.
```

**Basic Markdown prompt template:**
```
Documentation task: [file type]
Target file: [path/to/file.md]
Output format: Basic Markdown
Project: [project name] at [project root]

File type guidance: [relevant template from markdown-file-templates.md]
Exploration findings: [relevant findings]
Existing file content: [current content or "New file"]

Generate the complete file content in standard GitHub-flavored Markdown.
Do NOT use MkDocs-specific extensions.
Diagram guidance: Use Mermaid for all diagrams with dark text on nodes. GitHub renders Mermaid natively.
```

### Step 4 — Review generated content

- Verify structure, check for unfilled placeholders
- Validate cross-references use correct relative paths

Proceed to Phase 6.

---

## Phase 6: Integration & Finalization

**Goal:** Write files, validate, present results.

### Step 1 — Write files

**MkDocs:** Write pages under `docs/`, update `mkdocs.yml` nav.
**Basic Markdown:** Write files to target paths. For updates, modify existing files.
**Change Summary:** Present outputs inline, write files as applicable.

### Step 2 — Validate

**MkDocs:** Verify all nav-referenced files exist. Check cross-references. Optionally run `mkdocs build --strict`.
**Basic Markdown:** Validate internal cross-references. Check referenced paths exist.

### Step 3 — Present results

Summarize: files created/updated, navigation changes, validation warnings. For change-summary, present outputs inline.

### Step 4 — Next steps

Prompt the user with relevant options:

**MkDocs:**
- **"Preview the site"**
- **"Commit the changes"**
- **"Generate additional pages"**
- **"Done"**

**Basic Markdown:**
- **"Commit the changes"**
- **"Generate additional files"**
- **"Review a specific file"**
- **"Done"**

---

## Error Handling

If any phase fails:
1. Explain what went wrong
2. Offer retry/skip/abort options

### Non-Git Projects
- Skip git remote detection; omit `repo_url`/`repo_name`
- `update` with git-diff mode is unavailable — fall back to full-scan or targeted
- `change-summary` is unavailable

### Basic Markdown on Non-Git Projects
- CONTRIBUTING.md still viable — focus on code style, testing, setup (skip git workflow sections)

---

## Additional Resources

- For standalone markdown file templates, see **references/markdown-file-templates.md**

---

## Integration Notes

This skill was converted from the dev-tools plugin package. It orchestrates documentation management across 6 phases. It depends on deep-analysis (from core-tools) for codebase exploration and delegates content generation to docs-writer. The MkDocs config template and change summary templates have been inlined. The markdown-file-templates reference remains as a separate file due to its size (316 lines).
