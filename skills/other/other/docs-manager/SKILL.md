---
name: docs-manager
description: >-
  Documentation management workflow for MkDocs sites and standalone markdown files —
  initialize, generate, update docs, and create change summaries. Use when asked to
  "create docs", "write README", "update documentation", "generate docs site",
  "write CONTRIBUTING", "manage documentation", or "docs changelog".
argument-hint: <action-or-description> [--teams]
model: inherit
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

# Documentation Manager Workflow

Execute a structured 6-phase workflow for managing documentation. Supports two documentation formats (MkDocs sites and standalone markdown files) and three action types (generate, update, change summary).

**CRITICAL: Complete ALL applicable phases.** Some phases are conditional. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Phase Overview

Execute these phases in order, completing ALL of them:

1. **Interactive Discovery** — Determine documentation type, format, and scope through user interaction
2. **Project Detection & Setup** — Detect project context, conditionally scaffold MkDocs
3. **Codebase Analysis** — Deep codebase exploration using the deep-analysis skill
4. **Documentation Planning** — Translate analysis findings into a concrete plan for user approval
5. **Documentation Generation** — Launch docs-writer agents to generate content
6. **Integration & Finalization** — Write files, validate, present results

---

## Phase 1: Interactive Discovery

**Goal:** Determine through user interaction what documentation to create and in what format.

### Step 1 — Infer intent from `$ARGUMENTS`

Parse the user's input to pre-fill selections:
- Keywords like "README", "CONTRIBUTING", "ARCHITECTURE" → infer `basic-markdown`
- Keywords like "mkdocs", "docs site", "documentation site" → infer `mkdocs`
- Keywords like "changelog", "release notes", "what changed" → infer `change-summary`

If the intent is clear, present a summary for quick confirmation before proceeding (skip to Step 4). If ambiguous, proceed to Step 2.

### Step 2 — Q1: Documentation type

If the documentation type is ambiguous or needs confirmation, use `AskUserQuestion`:

```
What type of documentation would you like to create?
1. "MkDocs documentation site" — Full docs site with mkdocs.yml, Material theme
2. "Basic markdown files" — Standalone files like README.md, CONTRIBUTING.md, ARCHITECTURE.md
3. "Change summary" — Changelog, release notes, commit message
```

Store as `DOC_TYPE` = `mkdocs` | `basic-markdown` | `change-summary`.

### Step 3 — Conditional follow-up questions

**If `DOC_TYPE = mkdocs`:**

Q2: `AskUserQuestion` — Existing project or new setup?
- "Existing MkDocs project" → `MKDOCS_MODE = existing`
- "New MkDocs setup" → `MKDOCS_MODE = new`

Q3 (if `existing`): `AskUserQuestion` — What to do?
- "Generate new pages"
- "Update existing pages"
- "Both — generate and update"
Store as `ACTION`.

Q3 (if `new`): `AskUserQuestion` — Scope?
- "Full documentation"
- "Getting started only (minimal init)"
- "Custom pages"
Store as `MKDOCS_SCOPE`. If custom, use `AskUserQuestion` for desired pages (free text).

**If `DOC_TYPE = basic-markdown`:**

Q2: `AskUserQuestion` (multiSelect) — Which files?
- "README.md"
- "CONTRIBUTING.md"
- "ARCHITECTURE.md"
- "API documentation"
Store as `MARKDOWN_FILES`. If "Other" is selected, use `AskUserQuestion` for custom file paths/descriptions.

**If `DOC_TYPE = change-summary`:**

Q2: `AskUserQuestion` — What range?
- "Since last tag"
- "Between two refs"
- "Recent changes"
Follow up for specific range details (tag name, ref pair, etc.).

### Step 4 — Confirm selections

Present a summary of all selections and use `AskUserQuestion`:
- "Proceed"
- "Change selections"

If the user wants to change, loop back to the relevant question.

**Immediately proceed to Phase 2.**

---

## Phase 2: Project Detection & Setup

**Goal:** Detect project context automatically, conditionally scaffold MkDocs.

### Step 1 — Detect project metadata (all paths)

- Check manifests: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`
- Run `git remote get-url origin 2>/dev/null`
- Note primary language and framework

### Step 2 — Check existing documentation (all paths)

- Glob for `docs/**/*.md`, `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`
- For MkDocs: check for `mkdocs.yml`/`mkdocs.yaml`, read if found

### Step 3 — MkDocs Initialization (only if `DOC_TYPE = mkdocs` AND `MKDOCS_MODE = new`)

1. Load `${CLAUDE_PLUGIN_ROOT}/skills/docs-manager/references/mkdocs-config-template.md`
2. Fill template with detected metadata (ask via `AskUserQuestion` if incomplete)
3. Generate `mkdocs.yml`, create `docs/index.md` and `docs/getting-started.md`
4. Present scaffold for confirmation before writing

If `MKDOCS_SCOPE = minimal` (getting started only): write the scaffold files and skip to Phase 6.

### Step 4 — Set action-specific context (for update/change-summary)

For **update** modes, determine the approach:
- **git-diff** — Update docs affected by recent code changes (default if user mentions "recent changes" or a branch/tag)
- **full-scan** — Compare all source code against all docs for gap analysis (default if user says "full update" or "sync all")
- **targeted** — Update specific pages or sections (default if user specifies file paths or page names)

For **change-summary**, run `git log` and `git diff --stat` for the determined range.

**Immediately proceed to Phase 3.**

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

### Step 2 — Run deep-analysis (or teams-deep-analysis)

Check if `$ARGUMENTS` contains the `--teams` flag:

- **If `--teams`:** Read `${CLAUDE_PLUGIN_ROOT}/skills/teams-deep-analysis/SKILL.md` and follow its workflow
- **Otherwise:** Read `${CLAUDE_PLUGIN_ROOT}/skills/deep-analysis/SKILL.md` and follow its workflow

Pass the documentation-focused analysis context from Step 1.

Deep-analysis handles all agent orchestration (code-explorers + codebase-synthesizer). Since docs-manager is the calling skill, deep-analysis returns control without standalone summary.

### Step 3 — Supplemental analysis for update with git-diff mode

After deep-analysis, additionally:
1. Run `git diff --name-only [base-ref]` for changed files
2. Use Grep to search existing docs for references to changed files/functions
3. Cross-reference with synthesis findings

### For change-summary path (instead of deep-analysis)

1. Run `git log --oneline [range]` and `git diff --stat [range]`
2. Launch 1 code-explorer agent using Task tool with `subagent_type: "claude-alchemy-tools:code-explorer"` to analyze the changed files:
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

**Immediately proceed to Phase 4.**

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

Use `AskUserQuestion`:
- "Approve the plan as-is"
- "Modify the plan" (describe changes)
- "Reduce scope" (select specific items only)

**Immediately proceed to Phase 5.**

---

## Phase 5: Documentation Generation

**Goal:** Generate content using docs-writer agents.

### Step 1 — Load templates

- If `DOC_TYPE = change-summary`: Read `${CLAUDE_PLUGIN_ROOT}/skills/docs-manager/references/change-summary-templates.md`
- If `DOC_TYPE = basic-markdown`: Read `${CLAUDE_PLUGIN_ROOT}/skills/docs-manager/references/markdown-file-templates.md`

### Step 2 — Group by dependency

- **Independent pages/files** — Can be written without referencing other new content (API reference, standalone guides, individual markdown files)
- **Dependent pages/files** — Reference or summarize content from other pages (index pages, overview pages, README that links to CONTRIBUTING)

### Step 3 — Launch docs-writer agents

Launch agents using Task tool with `subagent_type: "claude-alchemy-tools:docs-writer"` and `model: "opus"`.

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
```

### Step 4 — Review generated content

- Verify structure, check for unfilled placeholders
- Validate cross-references between pages/files use correct relative paths

**Immediately proceed to Phase 6.**

---

## Phase 6: Integration & Finalization

**Goal:** Write files, validate, present results.

### Step 1 — Write files

**MkDocs:**
- Write pages under `docs/`
- Update `mkdocs.yml` nav — read current config, add new pages in logical positions, preserve existing structure

**Basic Markdown:**
- Write files to their target paths (project root or specified directories)
- For updates, use the Edit tool to modify existing files

**Change Summary:**
- Present outputs inline for review
- Write files as applicable (e.g., append to CHANGELOG.md)

### Step 2 — Validate

**MkDocs:**
- Verify all files referenced in `nav` exist on disk using Glob
- Check for broken cross-references between pages using Grep
- If `mkdocs` CLI is available, run `mkdocs build --strict 2>&1` to check for warnings (non-blocking)

**Basic Markdown:**
- Validate internal cross-references between files (e.g., README links to CONTRIBUTING)
- Check that referenced paths exist

### Step 3 — Present results

Summarize what was done:
- Files created (with paths)
- Files updated (with description of changes)
- Navigation changes (if MkDocs)
- Any validation warnings

For **change-summary**, present generated outputs directly inline.

### Step 4 — Next steps

Use `AskUserQuestion` with relevant options:

**MkDocs:**
- "Preview the site" (if `mkdocs serve` is available)
- "Commit the changes"
- "Generate additional pages"
- "Done — no further action"

**Basic Markdown:**
- "Commit the changes"
- "Generate additional files"
- "Review a specific file"
- "Done — no further action"

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
- The `update` action with git-diff mode is unavailable — fall back to full-scan or targeted mode
- The `change-summary` action is unavailable — inform the user and suggest alternatives

### Basic Markdown on Non-Git Projects
- CONTRIBUTING.md is still viable — use project conventions instead of git workflow sections
- Skip branch naming and PR process sections; focus on code style, testing, and setup

### Phase Failure
- Explain the error clearly
- Offer retry/skip/abort options via `AskUserQuestion`

---

## Agent Coordination

- **Phase 3**: Exploration and synthesis handled by the deep-analysis skill (or teams-deep-analysis with `--teams`). Deep-analysis orchestrates its own code-explorer and codebase-synthesizer agents.
- **Phase 5**: docs-writer agents launched with `model: "opus"` for high-quality content generation. Parallel for independent files, sequential for dependent files.

---

## Additional Resources

- For MkDocs configuration template, see [references/mkdocs-config-template.md](references/mkdocs-config-template.md)
- For change summary formats, see [references/change-summary-templates.md](references/change-summary-templates.md)
- For standalone markdown file templates, see [references/markdown-file-templates.md](references/markdown-file-templates.md)
