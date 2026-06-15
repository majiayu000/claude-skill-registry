---
name: unikit-docs
description: >-
  Generate and maintain project documentation for game engine projects.
  Creates a lean README as a landing page with detailed docs/ directory split by topic.
  Auto-detects engine tech stack (DI frameworks, async libraries, event systems, UI frameworks),
  folder structure, and module boundaries to generate only relevant documentation pages.
  Reads language setting from .unikit/config.yaml — all generated documentation and
  user-facing messages are written in the configured language (default: English).
  Supports docs-config.json for path and document customization. Use when user says
  "create docs", "write documentation", "update docs", "generate readme", "document project",
  or wants to document their project structure, modules, or game systems — even if they
  don't explicitly say "docs".
argument-hint: "[--web]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(mkdir,ls)
  - AskUserQuestion
  - Agent
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.1"
  category: documentation
---

# Docs — Project Documentation Generator

Generate, maintain, and improve documentation for game projects following a landing-page README + detailed docs/ structure.

## Core Principles

1. **README is a landing page, not a manual.** ~80-120 lines. First impression, tech stack, quick start, links to details.
2. **Details go to `docs/`.** Each file is self-contained — one topic, one page.
3. **No duplication.** If information lives in `docs/`, README links to it — does not repeat it.
4. **Detection-first.** Scan the project before deciding which documents to generate. Never assume specific frameworks, folder structures, or patterns — discover them.
5. **Navigation.** Every docs/ file has a header line with prev/next links following the Documentation table order. Every page ends with a "See Also" section linking to 2-3 related pages.
6. **Scannable.** Use tables, bullet lists, and code blocks. Avoid long paragraphs.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

<!-- unikit:agents codex -->
## Subagent Delegation — BLOCKING PRE-REQUISITE

When the workflow reaches a step that requires a subagent (`Agent`), the assistant MUST automatically spawn the
subagent if agent execution is supported by the current environment and not prohibited by higher-priority
instructions.

Only if agent execution is unavailable or blocked, the assistant MUST ask the user before proceeding with any
alternative.
<!-- unikit:end -->

## Skill-specific rules:
- Navigation text is translated to the configured language (`[<- Предыдущая]`, `Назад к README`, `Далее ->`, `См. также`)
- `docs-config.json` is NOT translated — it stays in English (machine-readable config)

## Workflow

### Step 0: Load Project Context

1. Read `.unikit/config.yaml` — extract `language.ui` and `language.artifacts` (all subsequent output uses these language settings)
2. Read `.unikit/DESCRIPTION.md` (if exists) — project overview, tech stack
3. Read `.unikit/ARCHITECTURE.md` (if exists) — architecture decisions, module structure
4. Read `.unikit/skill-context/unikit-docs/SKILL.md` — **MANDATORY if exists.** Project-specific overrides. Skill-context rules win over general rules on conflict.
5. Read `AGENTS.md` (if exists) — current documentation index

### Step 0.1: Parse Flags

```
--web → Also generate HTML version of documentation (see Step 6)
```

### Step 1: Auto-Detect Project

This is the heart of universality. Scan the project to understand its real structure before generating anything.

#### 1.1: Load Engine Rules

Read `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md` — this file is installed by the unikit setup and contains all engine-specific detection tables, folder structure patterns, module boundary mechanism, and deep analysis patterns for the current project's engine.

#### 1.2: Detect Tech Stack

Using the detection tables from the loaded engine rules file, scan the project's package manifest and plugin directories for known frameworks.

Record detected stack — it determines which conditional documents to generate.

#### 1.3: Detect Folder Structure

Using the folder structure patterns from the loaded engine rules file, scan the project for script locations, modular structures, special folders, scenes, and tests. Don't assume any specific structure — discover it.

Also scan for module boundary files (per engine rules) to map the project's module/assembly structure.

#### 1.4: Load or Generate docs-config.json

Check if `.unikit/docs-config.json` exists:

**If exists** → load it, then run reconciliation (Step 1.5) to sync config with reality.

**If not exists** → generate based on detection results:

```json
{
  "detected_stack": {
    "engine": "{{engine_name}} 6 (6000.0.68f1)",
    "di": "Zenject",
    "async": "UniTask",
    "events": "Custom SignalBus",
    "ui": "ASPID MVVM",
    "reactive": "R3"
  },
  "scan_paths": {
    "scripts": ["Assets/Game/Scripts"],
    "modules": ["Assets/Modules", "Assets/Modules/Pawnshop"],
    "scenes": ["Assets/Game/Scenes"],
    "editor": ["Assets/Editor", "Assets/Game/Scripts/Editor"],
    "tests": ["Assets/Game/Tests"]
  },
  "exclude_paths": [
    "Assets/Plugins",
    "Assets/Third-Party Assets"
  ],
  "documents": {
    "core": ["readme", "getting-started", "architecture", "project-map"],
    "conditional": ["di-bindings", "events", "save-system", "game-systems", "testing", "editor-tools"]
  },
  "output_dir": "docs"
}
```

Present the generated config to the user for confirmation before proceeding. This is their chance to add paths, remove documents, or adjust detection results.

**Conditional document rules — generate only if detected:**

| Document | Generate when |
|----------|--------------|
| `di-bindings` | DI framework detected (Zenject, VContainer, etc.) |
| `events` | Event/signal system detected |
| `save-system` | Save serialization classes detected |
| `game-systems` | Gameplay controllers, FSM, AI systems detected |
| `testing` | Test assembly definitions detected |
| `editor-tools` | Custom Editor scripts detected |
| `build` | Addressables or custom build pipeline detected |
| `ui-system` | UI framework beyond basic UGUI detected |

#### 1.5: Reconciliation (config vs reality)

When `docs-config.json` already exists, run a three-way comparison: **config** vs **detected state** vs **existing docs/**. This ensures the config stays in sync as the project evolves.

**a) Validate scan_paths — do configured paths still exist?**

For each path in `scan_paths`, check if it exists on disk:
- Path exists → scan it normally
- Path missing → `WARN`: "Path `Assets/OldFolder` from config not found. Remove from config?"
- Offer to remove dead paths. Don't auto-remove — the path might be temporarily missing (branch switch, pending asset import).

**b) Detect new paths — did the project grow?**

Scan `Assets/` for common script locations (same list from Step 1.2). If a new populated folder is found that isn't in `scan_paths` or `exclude_paths`:
- `INFO`: "Found `Assets/NewModule/` with scripts — not in config. Add to scan_paths?"
- Offer to add. Don't force — the user may intentionally exclude it.

**c) Reconcile tech stack — did packages change?**

Re-run detection (Step 1.1) and compare with `detected_stack` in config:

| Situation | Action |
|-----------|--------|
| New framework found (not in config) | Suggest: "Detected Mirror in manifest.json. Add `networking` document?" → update config + generate doc |
| Framework removed (in config but not detected) | Suggest: "Zenject no longer detected. Keep `di-bindings` document?" → user decides |
| Version changed | Silently update `detected_stack` in config |

**d) Reconcile documents — config vs docs/ folder**

| Situation | Action |
|-----------|--------|
| Document in config but no file in docs/ | Generate it (probably new addition by user) |
| Document NOT in config but file exists in docs/ | Do NOT delete. Skip updates. Warn: "`docs/save-system.md` exists but is not in config — it won't be updated" |
| Document in config, file exists | Update normally (State C behavior) |

**e) Present reconciliation report**

If any discrepancies found, show a summary before proceeding:

```
Config reconciliation:

Paths:
  ✅ Assets/Game/Scripts — exists
  ✅ Assets/Modules — exists
  ⚠️ Assets/OldFolder — not found (remove from config?)
  🔍 Assets/NewFeature/ — found, not in config (add?)

Tech stack:
  ✅ DI: Zenject — unchanged
  🔍 Networking: Mirror — detected, not in config
  ❌ Save: Custom SaveSerializer — no longer detected

Documents:
  ✅ 4 core + 3 conditional — in sync
  🔍 networking — suggested (Mirror detected)
  ⚠️ docs/save-system.md — exists but removed from config

Apply suggestions?
1. Apply all
2. Let me pick
3. Skip — use config as-is
```

Based on choice:
- Apply all → update `docs-config.json` with all suggestions, proceed to Step 1.6
- Let me pick → present each suggestion individually for approval, apply selected
- Skip → use config as-is, proceed to Step 1.6

After reconciliation, update `docs-config.json` with confirmed changes and proceed to Step 1.5.

### Step 1.6: Deep Code Analysis

Before generating any documents, systematically explore the codebase to build a deep understanding of how systems connect. This step transforms surface-level detection (Step 1) into the rich relationship map that makes documentation truly valuable.

**This step is mandatory.** Shallow detection produces shallow docs — catalogs of classes without explaining how they work together. The quality of documentation directly depends on the depth of analysis performed here.

Launch multiple exploration tasks in parallel using `Agent(subagent_type: Explore, model: sonnet, ...)` to cover different analysis dimensions. Each substep below (1.6.1–1.6.4) should be a separate Agent call with a focused prompt.

**Fallback:** If Agent tool is unavailable, perform analysis inline using Glob/Grep/Read.

#### 1.6.1: Bootstrap & Initialization Chain

Trace the full startup sequence from entry scene to gameplay-ready state:
- Find the entry scene → identify root GameObjects with context components
- Find ALL `*Installer.cs` files → read each one fully, extract every binding
- Map the initialization order: loading operations → IInitializable chain → NonLazy activations
- Trace loading operation dependencies (what must complete before what)

**Output:** Ordered initialization graph with dependencies between steps.

#### 1.6.2: Complete Communication Map

Build a full catalog of ALL inter-system communication — not just the obvious signals:

**SignalBus events:**
- Find ALL `ISignal` implementations (grep `: ISignal` in all project `.cs` files)
- For each signal: find every `Invoke<Signal>` (publishers) and `Subscribe<Signal>` (subscribers)
- Detect signal chains — when a signal handler triggers another signal

**R3 reactive streams:**
- Find all `ReactiveProperty<>`, `Subject<>`, `ReadOnlyReactiveProperty<>` declarations
- Trace who subscribes to each stream (`.Subscribe()`, `.Select()`, `.Where()`, `.Switch()`)
- Map the reactive data flow: Model → ViewModel → View

**Direct DI dependencies:**
- Read constructor parameters of key services to build the dependency graph
- Identify hub services (injected by 3+ consumers)

**Output:** Complete communication topology with three layers: signals, reactive streams, DI dependencies.

#### 1.6.3: End-to-End Feature Flows

Trace 2-3 key user-facing features from trigger to completion:
- Start from user action or external trigger
- Follow through every system touched: controller → service → model → view → save
- Note every signal fired, every observable updated, every state change
- Identify cross-module boundaries crossed
- Record the communication mechanism at each step (DI call, signal, R3 stream, direct call)

Pick flows that touch the most systems — these reveal the real architecture.

**Output:** Step-by-step sequence for each flow with class names and mechanisms at each boundary.

#### 1.6.4: Cross-System Interaction Matrix

Build a matrix showing how major systems interact:

```
             | Characters | Trade | MiniGames | Wallets | Save | UI
Characters   |     —      |  DI   |   Signal  |   —     |  —   | R3
Trade        |    DI      |   —   |     DI    |   DI    | Save | Signal
```

For each non-empty cell: note the mechanism (DI, Signal, R3, Direct) and direction.

**Output:** Interaction matrix with mechanism annotations + list of hub systems.

#### 1.6.5: Consolidate Analysis

Merge outputs from all parallel Agent results. This analysis is NOT published — it feeds into Step 3 to produce rich, connected documentation.

Key things to capture:
- Hub systems (many connections) vs isolated modules
- Data that flows through many systems (e.g., customer data, wallet balance)
- Recurring patterns across the codebase (Controller pattern, SaveSerializer pattern, etc.)
- Surprising or non-obvious connections between systems
- Any circular dependencies or architectural concerns

### Step 2: Determine Current State

```
State A: No README.md                → Full generation (README + docs/)
State B: README.md exists, no docs/  → Analyze README, propose split into docs/
State C: README.md + docs/ exist     → Audit and improve
```

**State C with `--web` flag** — ask the user:

```
Documentation already exists (README.md + docs/).

Options:
1. Generate HTML only — build site from current docs
2. Audit & improve first — check for issues, then generate HTML
3. Audit only — check without generating HTML
```

Based on choice:
- HTML only → skip Steps 3–5, proceed directly to Step 6 (HTML Generation) → **STOP** (do not run Steps 7, 8 — no markdown content was changed)
- Audit & improve → run State C audit (Step 3, State C), fix issues, then proceed to Step 6
- Audit only → run State C audit, report issues → **STOP**

### Step 2.1: Check for Scattered Markdown Files

Scan project root for `.md` files. Propose consolidating relevant ones into `docs/`:

| Root file | Target in docs/ | Action |
|-----------|-----------------|--------|
| `CONTRIBUTING.md` | `docs/contributing.md` | Move |
| `ARCHITECTURE.md` | `docs/architecture.md` | Move |
| `SETUP.md` | `docs/getting-started.md` | Merge |
| `TESTING.md` | `docs/testing.md` | Move |

**Files that stay in root:** `README.md`, `CHANGELOG.md`, `LICENSE`, `CODE_OF_CONDUCT.md`, `AGENTS.md`.

Always ask before moving. Never force-move files.

### Step 3: Generate Documents

#### State A: Full Generation

##### 3.1: Confirm document list

Present detected documents to the user:

```
Based on project scan:

Core documents (always generated):
  ✅ README.md — project landing page
  ✅ docs/getting-started.md — setup, prerequisites, first run
  ✅ docs/architecture.md — project structure and patterns
  ✅ docs/project-map.md — modules, assemblies, namespaces

Conditional documents (detected):
  ✅ docs/di-bindings.md — [FrameworkName] installer map
  ✅ docs/events.md — event system catalog
  ✅ docs/testing.md — test infrastructure
  ❌ docs/networking.md — no networking framework detected

Options:
1. Generate all detected
2. Let me pick
3. Add more topics
```

Based on choice:
- Generate all detected → proceed to Step 3.2 with full document list
- Let me pick → present each document individually for approval, generate only selected
- Add more topics → ask user for additional topics via AskUserQuestion, merge with detected list, re-confirm

##### 3.2: Generate README.md

For the README template and content guidelines → read `{{skills_dir}}/{{self_name}}/references/DOC-TEMPLATES.md` (README section).

Key rules:
- Tech Stack table derived from `detected_stack`
- Quick Start with real engine version (per engine rules: version detection method)
- Key Features from `.unikit/DESCRIPTION.md` or codebase scan
- Documentation table linking to all generated docs/ pages
- ~80-120 lines total

##### 3.3: Generate docs/ files

For content guidelines per document type → read `{{skills_dir}}/{{self_name}}/references/DOC-TEMPLATES.md`.

Every file follows this structure (navigation text in project language):

```markdown
[<- Previous](prev.md) . [Back to README](../README.md) . [Next ->](next.md)

# Topic Title

Content with tables, code blocks, diagrams.

## See Also

- [Related Topic](topic.md) — brief description
```

Navigation text is translated to the project language. For example, with `"language": "ru"`:
```markdown
[<- Предыдущая](prev.md) . [Назад к README](../README.md) . [Далее ->](next.md)
## См. также
```

**Navigation link order** follows the Documentation table in README.md. First page omits prev link; last page omits next link.

**Content generation approach:**
- Use the deep analysis from Step 1.6 as the primary source — it contains the communication map, dependency chains, and feature flows
- Supplement with `Agent(subagent_type: Explore, model: sonnet, ...)` for specific details not covered by the analysis. Fallback: If Agent tool is unavailable, use Glob/Grep/Read inline
- For each document, verify against actual code — don't guess at structures
- Include real class names, real file paths, real namespace examples
- Draw ASCII dependency diagrams, sequence diagrams, and interaction matrices
- Show cross-system connections: how systems communicate, what triggers what, where data flows
- Prefer "how things connect" over "what things exist" — connections are more valuable than catalogs

#### State B: Split Existing README

1. Analyze which sections should stay (landing page) vs move to docs/
2. Propose split plan to user
3. Execute with confirmation
4. Verify no content lost — every section from old README must exist somewhere

#### State C: Improve Existing Docs

1. **Audit:**
   - README length (is it still a landing page, <150 lines?)
   - Missing topics (aspects of the project not documented)
   - Stale content (references to files/APIs that no longer exist)
   - Navigation (all docs have prev/next + See Also?)
   - Broken links (verify all internal links)
   - Consistency (same formatting across all docs)
2. **Propose improvements** with status indicators per item
3. **Apply fixes** after user confirmation

### Step 4: Documentation Review

**Mandatory after any content change.** Read every generated/modified file and run the full review.

For comprehensive checklists (Technical, {{engine_name}}-Specific, "New User Eyes" readability, Standards Compliance) → read `{{skills_dir}}/{{self_name}}/references/REVIEW-CHECKLISTS.md`.

Key areas to verify:
- **Technical accuracy** — file paths, class names, framework versions, assembly references match reality
- **Readability** — prev/next navigation, "See Also" sections, proper table formatting, no placeholders
- **Language** — all prose in project language from `.unikit/config.yaml` (`language.artifacts`); code identifiers and file names in English
- **Standards compliance** — gaps detected per checklist auto-fix table

Fix issues before presenting result to the user.

### Step 5: Clean Up Moved Files

If files were moved from root into docs/ (Step 2.1) — offer to delete originals after review confirms content is preserved.

Always ask before deleting. The user may want to keep originals temporarily.

### Step 6: HTML Generation (--web)

When `--web` flag is passed:

For the complete conversion process, template placeholders, nav_links format, markdown→HTML conversion rules, and auto-features documentation → read `{{skills_dir}}/{{self_name}}/references/HTML-GENERATION.md`.

Summary of the process:

1. Create `docs-html/` directory
2. Read `templates/html-template.html` (use as base for all pages)
3. For each markdown file → convert to HTML following conversion rules from `{{skills_dir}}/{{self_name}}/references/HTML-GENERATION.md`
4. Replace template placeholders (`{project_name}`, `{page_title}`, `{nav_links}`, `{content}`, `{prev_link}`, `{next_link}`)
5. Fix `.md` links to `.html`
6. Generate navigation sidebar with `class="active"` on current page
7. Add `docs-html/` to `.gitignore` if not already there

File mapping: `README.md` → `index.html`, `docs/*.md` → `*.html`.

### Step 7: Update AGENTS.md

If `AGENTS.md` exists, update its `## Documentation` section:

```markdown
## Documentation

| Document | Path | Description |
|----------|------|-------------|
| README | README.md | Project landing page |
| Getting Started | docs/getting-started.md | Installation and setup |
| Architecture | docs/architecture.md | Project structure and patterns |
| ... | ... | ... |
```

List README first, then docs/ files in Documentation table order. Keep descriptions concise (<10 words).

### Step 8: Save docs-config.json

If config was generated in Step 1.3, save to `.unikit/docs-config.json`. This allows future runs to skip detection and respect user customizations.

### Context Cleanup

Suggest the user to free up context space if needed: `/clear` (full reset) or `/compact` (compress history).

## Important Rules

1. **Detection first** — never assume specific frameworks or folder structures. Scan, then decide.
2. **Always ask before changes** to existing documentation — show the plan first.
3. **Never delete content** without moving it somewhere else first.
4. **Detect real project info** — don't invent features; read actual files.
5. **Use project language** from `.unikit/config.yaml` (`language.artifacts`) for all prose, headings, navigation, descriptions, and user-facing messages. File names, code identifiers, and framework names stay in English.
6. **Preserve existing content** — badges, logos, custom sections in README.
7. **Ownership boundary** — this skill owns `README.md`, `docs/*`, `docs-html/*`, `.unikit/docs-config.json`, and the Documentation section in `AGENTS.md`. It does NOT own `.unikit/ARCHITECTURE.md`, `.unikit/RULES.md`, or `.unikit/DESCRIPTION.md`.
8. **Don't duplicate .unikit/ content** — if `ARCHITECTURE.md` or `DESCRIPTION.md` exist in `.unikit/`, use them as source material and enrich, don't copy verbatim.
9. **NEVER add `Co-Authored-By`** or any AI attribution trailers to commits.
10. **Agent-based delegation** — use `Agent(subagent_type: Explore, model: sonnet, ...)` for deep code analysis. If Agent tool is unavailable, fall back to inline work (Glob/Grep/Read). Lightweight Glob/Grep for quick checks is always allowed without delegation.
