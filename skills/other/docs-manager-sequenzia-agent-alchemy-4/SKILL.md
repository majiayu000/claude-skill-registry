---
name: docs-manager
description: >-
  Documentation management workflow for MkDocs sites and standalone markdown files —
  initialize, generate, update docs, and create change summaries. Use when asked to
  "create docs", "write README", "update documentation", "generate docs site",
  "write CONTRIBUTING", "manage documentation", or "docs changelog".
dependencies:
  - deep-analysis (core-tools)
---

# Documentation Manager Workflow

Execute a structured 6-phase workflow for managing documentation. Supports two documentation formats (MkDocs sites and standalone markdown files) and three action types (generate, update, change summary).

## Phase Overview

Execute these phases in order (some phases are conditional):

1. **Interactive Discovery** -- Determine documentation type, format, and scope through user interaction
2. **Project Detection & Setup** -- Detect project context, conditionally scaffold MkDocs
3. **Codebase Analysis** -- Deep codebase exploration using the deep-analysis skill
4. **Documentation Planning** -- Translate analysis findings into a concrete plan for user approval
5. **Documentation Generation** -- Launch docs-writer agents to generate content
6. **Integration & Finalization** -- Write files, validate, present results

---

## Phase 1: Interactive Discovery

**Goal:** Determine through user interaction what documentation to create and in what format.

### Step 1 -- Infer intent from `$ARGUMENTS`

Parse the user's input to pre-fill selections:
- Keywords like "README", "CONTRIBUTING", "ARCHITECTURE" -> infer `basic-markdown`
- Keywords like "mkdocs", "docs site", "documentation site" -> infer `mkdocs`
- Keywords like "changelog", "release notes", "what changed" -> infer `change-summary`

If the intent is clear, present a summary for quick confirmation before proceeding (skip to Step 4). If ambiguous, proceed to Step 2.

### Step 2 -- Q1: Documentation type

If the documentation type is ambiguous or needs confirmation, prompt the user:

> What type of documentation would you like to create?

- "MkDocs documentation site" -- Full docs site with mkdocs.yml, Material theme
- "Basic markdown files" -- Standalone files like README.md, CONTRIBUTING.md, ARCHITECTURE.md
- "Change summary" -- Changelog, release notes, commit message

Store as `DOC_TYPE` = `mkdocs` | `basic-markdown` | `change-summary`.

### Step 3 -- Conditional follow-up questions

**If `DOC_TYPE = mkdocs`:**

Q2: Prompt the user -- Existing project or new setup?
- "Existing MkDocs project" -> `MKDOCS_MODE = existing`
- "New MkDocs setup" -> `MKDOCS_MODE = new`

Q3 (if `existing`): Prompt the user -- What to do?
- "Generate new pages"
- "Update existing pages"
- "Both -- generate and update"
Store as `ACTION`.

Q3 (if `new`): Prompt the user -- Scope?
- "Full documentation"
- "Getting started only (minimal init)"
- "Custom pages"
Store as `MKDOCS_SCOPE`. If custom, ask for desired pages (free text).

**If `DOC_TYPE = basic-markdown`:**

Q2: Prompt the user -- Which files?
- "README.md"
- "CONTRIBUTING.md"
- "ARCHITECTURE.md"
- "API documentation"
Store as `MARKDOWN_FILES`. If "Other" is selected, ask for custom file paths/descriptions.

**If `DOC_TYPE = change-summary`:**

Q2: Prompt the user -- What range?
- "Since last tag"
- "Between two refs"
- "Recent changes"
Follow up for specific range details (tag name, ref pair, etc.).

### Step 4 -- Confirm selections

Present a summary of all selections and prompt the user:
- "Proceed"
- "Change selections"

If the user wants to change, loop back to the relevant question.

Immediately proceed to Phase 2.

---

## Phase 2: Project Detection & Setup

**Goal:** Detect project context automatically, conditionally scaffold MkDocs.

### Step 1 -- Detect project metadata (all paths)

- Check manifests: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`
- Run `git remote get-url origin 2>/dev/null`
- Note primary language and framework

### Step 2 -- Check existing documentation (all paths)

- Search for `docs/**/*.md`, `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`
- For MkDocs: check for `mkdocs.yml`/`mkdocs.yaml`, read if found

### Step 3 -- MkDocs Initialization (only if `DOC_TYPE = mkdocs` AND `MKDOCS_MODE = new`)

1. Load the MkDocs configuration template (see MkDocs Config Template section below)
2. Fill template with detected metadata (ask the user if incomplete)
3. Generate `mkdocs.yml`, create `docs/index.md` and `docs/getting-started.md`
4. Present scaffold for confirmation before writing

If `MKDOCS_SCOPE = minimal` (getting started only): write the scaffold files and skip to Phase 6.

### Step 4 -- Set action-specific context (for update/change-summary)

For **update** modes, determine the approach:
- **git-diff** -- Update docs affected by recent code changes (default if user mentions "recent changes" or a branch/tag)
- **full-scan** -- Compare all source code against all docs for gap analysis (default if user says "full update" or "sync all")
- **targeted** -- Update specific pages or sections (default if user specifies file paths or page names)

For **change-summary**, run `git log` and `git diff --stat` for the determined range.

Immediately proceed to Phase 3.

---

## Phase 3: Codebase Analysis

**Goal:** Deep codebase exploration using the deep-analysis skill.

**Skip conditions:**
- Skip for `change-summary` (uses git-based analysis instead -- see below)
- Skip for MkDocs minimal init-only (`MKDOCS_SCOPE = minimal`)

### Step 1 -- Build documentation-focused analysis context

Construct a specific context string based on Phase 1 selections:

| Selection | Analysis Context |
|-----------|-----------------|
| MkDocs generate | "Documentation generation -- find all public APIs, architecture, integration points, and existing documentation..." |
| MkDocs update | "Documentation update -- identify changes to public APIs, outdated references, documentation gaps..." |
| Basic markdown README | "Project overview -- understand purpose, architecture, setup, key features, configuration, and dependencies..." |
| Basic markdown ARCHITECTURE | "Architecture documentation -- map system structure, components, data flow, design decisions, key dependencies..." |
| Basic markdown API docs | "API documentation -- find all public functions, classes, methods, types, their signatures and usage patterns..." |
| Basic markdown CONTRIBUTING | "Contribution guidelines -- find dev workflow, testing setup, code style rules, commit conventions, CI process..." |
| Multiple files | Combine relevant contexts from above |

### Step 2 -- Run deep-analysis

Refer to the **deep-analysis** skill (from the core-tools package) and follow its workflow.

Pass the documentation-focused analysis context from Step 1.

Deep-analysis handles all agent orchestration (reconnaissance, team planning, code-explorers + code-synthesizer). When invoked by another skill, cache hits are auto-accepted to avoid redundant exploration.

### Step 3 -- Supplemental analysis for update with git-diff mode

After deep-analysis, additionally:
1. Run `git diff --name-only [base-ref]` for changed files
2. Search existing docs for references to changed files/functions
3. Cross-reference with synthesis findings

### For change-summary path (instead of deep-analysis)

1. Run `git log --oneline [range]` and `git diff --stat [range]`
2. Launch 1 exploration agent (refer to the **code-explorer** agent from the core-tools package) to analyze the changed files:
   - Analysis context: Change summary for [range]
   - Focus area: the files changed in the specified range
   - Instructions: for each significant change, identify what was added/modified/removed, impact on public APIs and user-facing behavior, whether any changes are breaking
   - Return a structured report

Immediately proceed to Phase 4.

---

## Phase 4: Documentation Planning

**Goal:** Translate analysis findings into a concrete documentation plan.

### Step 1 -- Produce plan based on doc type

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
- Output formats to generate (Format 1: Changelog, Format 2: Commit message, Format 3: MkDocs page -- only if MkDocs site exists)
- Range confirmation
- Scope of changes

### Step 2 -- User approval

Prompt the user:
- "Approve the plan as-is"
- "Modify the plan" (describe changes)
- "Reduce scope" (select specific items only)

Immediately proceed to Phase 5.

---

## Phase 5: Documentation Generation

**Goal:** Generate content using docs-writer agents.

### Step 1 -- Load templates

- If `DOC_TYPE = change-summary`: Load the change summary templates (see Change Summary Templates section below)
- If `DOC_TYPE = basic-markdown`: Load the markdown file templates from `references/markdown-file-templates.md`

### Step 2 -- Group by dependency

- **Independent pages/files** -- Can be written without referencing other new content (API reference, standalone guides, individual markdown files)
- **Dependent pages/files** -- Reference or summarize content from other pages (index pages, overview pages, README that links to CONTRIBUTING)

### Step 3 -- Launch docs-writer agents

Launch docs-writer agents for content generation.

Launch independent pages/files in parallel, then sequential for dependent ones (include generated content from independent pages in the prompt context).

**MkDocs prompt template:**
```
Documentation task: [page type — API reference / architecture / how-to / change summary]
Target file: [docs/path/to/page.md]
Output format: MkDocs
Project: [project name] at [project root]

MkDocs site context:
- Theme: Material for MkDocs
- Extensions available: admonitions, code highlighting, tabbed content, Mermaid diagrams
- Diagram guidance: Follow technical-diagrams conventions — use Mermaid for all diagrams with dark text on nodes.
- Existing pages: [list of current doc pages]

Exploration findings:
[Relevant findings from Phase 3 for this page]

Existing page content (if updating):
[Current content of the page, or "New page — no existing content"]

Generate the complete page content in MkDocs-flavored Markdown.
```

**Basic Markdown prompt template:**
```
Documentation task: [file type — README / CONTRIBUTING / ARCHITECTURE / API docs]
Target file: [path/to/file.md]
Output format: Basic Markdown
Project: [project name] at [project root]

File type guidance:
[Relevant structural template from markdown-file-templates.md]

Exploration findings:
[Relevant findings from Phase 3 for this file]

Existing file content (if updating):
[Current content, or "New file — no existing content"]

Generate the complete file content in standard GitHub-flavored Markdown.
Do NOT use MkDocs-specific extensions (admonitions, tabbed content, code block titles).
Diagram guidance: Follow technical-diagrams conventions — use Mermaid for all diagrams with dark text on nodes. GitHub renders Mermaid natively.
```

### Step 4 -- Review generated content

- Verify structure, check for unfilled placeholders
- Validate cross-references between pages/files use correct relative paths

Immediately proceed to Phase 6.

---

## Phase 6: Integration & Finalization

**Goal:** Write files, validate, present results.

### Step 1 -- Write files

**MkDocs:**
- Write pages under `docs/`
- Update `mkdocs.yml` nav -- read current config, add new pages in logical positions, preserve existing structure

**Basic Markdown:**
- Write files to their target paths (project root or specified directories)
- For updates, use incremental editing to modify existing files

**Change Summary:**
- Present outputs inline for review
- Write files as applicable (e.g., append to CHANGELOG.md)

### Step 2 -- Validate

**MkDocs:**
- Verify all files referenced in `nav` exist on disk
- Check for broken cross-references between pages
- If `mkdocs` CLI is available, run `mkdocs build --strict 2>&1` to check for warnings (non-blocking)

**Basic Markdown:**
- Validate internal cross-references between files (e.g., README links to CONTRIBUTING)
- Check that referenced paths exist

### Step 3 -- Present results

Summarize what was done:
- Files created (with paths)
- Files updated (with description of changes)
- Navigation changes (if MkDocs)
- Any validation warnings

For **change-summary**, present generated outputs directly inline.

### Step 4 -- Next steps

Prompt the user with relevant options:

**MkDocs:**
- "Preview the site" (if `mkdocs serve` is available)
- "Commit the changes"
- "Generate additional pages"
- "Done -- no further action"

**Basic Markdown:**
- "Commit the changes"
- "Generate additional files"
- "Review a specific file"
- "Done -- no further action"

---

## Error Handling

If any phase fails:
1. Explain what went wrong
2. Ask the user how to proceed:
   - Retry the phase
   - Skip to next phase (with partial results)
   - Abort the workflow

### Non-Git Projects
If the project is not a git repository:
- Skip git remote detection in Phase 2 (omit `repo_url` and `repo_name` from mkdocs.yml)
- The `update` action with git-diff mode is unavailable -- fall back to full-scan or targeted mode
- The `change-summary` action is unavailable -- inform the user and suggest alternatives

### Basic Markdown on Non-Git Projects
- CONTRIBUTING.md is still viable -- use project conventions instead of git workflow sections
- Skip branch naming and PR process sections; focus on code style, testing, and setup

### Phase Failure
- Explain the error clearly
- Offer retry/skip/abort options

---

## Agent Coordination

- **Phase 3**: Exploration and synthesis handled by the deep-analysis skill, which manages parallel exploration agents and a synthesis agent.
- **Phase 5**: docs-writer agents launched for high-quality content generation. Parallel for independent files, sequential for dependent files.

---

## Change Summary Templates

### Format 1: Markdown Changelog

Follows [Keep a Changelog](https://keepachangelog.com/) conventions:

```markdown
## [Unreleased]

### Added
- Add [feature] with [key capability]

### Changed
- Update [component] to [new behavior]

### Fixed
- Fix [bug] that caused [symptom]

### Removed
- Remove [deprecated feature] in favor of [replacement]
```

Guidelines: Use imperative mood. One entry per distinct change. Group related changes. Focus on user-facing impact.

### Format 2: Git Commit Message

Follows [Conventional Commits](https://www.conventionalcommits.org/) style:

```
type(scope): summary of changes

Detailed description of what changed and why.

Changes:
- List specific modifications
- Include file paths for significant changes

BREAKING CHANGE: Description of breaking change (if applicable)
```

Types: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`

### Format 3: MkDocs Documentation Page

> This format applies only when the documentation target is an MkDocs site.

A full documentation page with highlights, features, improvements, bug fixes, breaking changes with migration guidance, affected files table, and contributors.

### Choosing Formats

| Format | Best For |
|--------|----------|
| **Markdown Changelog** | Appending to an existing CHANGELOG.md |
| **Git Commit Message** | Describing changes in a commit or PR |
| **MkDocs Page** | Publishing release notes in the documentation site |

## MkDocs Config Template

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

Populate `PROJECT_NAME`, `PROJECT_DESCRIPTION`, `REPO_URL`, `REPO_NAME` from detected metadata. Omit `repo_url` and `repo_name` if not in a git repository.

---

## Integration Notes
**What this component does:** Orchestrates a complete documentation management workflow supporting MkDocs sites, standalone markdown files, and change summaries -- from interactive discovery through codebase analysis, planning, generation, and validation.
**Capabilities needed:** Shell execution (git commands, mkdocs CLI), file reading/writing/editing, pattern search, sub-agent spawning (deep-analysis from core-tools, code-explorer from core-tools, docs-writer), user interaction.
**Adaptation guidance:** This skill relies on deep-analysis (core-tools) for codebase exploration in Phase 3 and spawns docs-writer agents for content generation in Phase 5. The MkDocs config template and change summary templates are inlined. The markdown-file-templates reference file provides structural templates for standalone files.
**Sub-agent capabilities:** Docs-writer agents need file reading, search, and shell execution for producing complete documentation pages. They draw on knowledge from the technical-diagrams skill (core-tools) for Mermaid diagram conventions.
