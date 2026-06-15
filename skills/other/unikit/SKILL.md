---
name: unikit
description: >-
  Set up AI agent context for a game engine project.
  Scans engine-specific package manifests, plugins, modules, and project settings
  to discover the real tech stack. Bootstraps the resolved description and
  architecture artifacts and AGENTS.md, plus the user-editable .unikit/config.yaml.
  Use when starting a new game project, setting up AI context, initializing unikit,
  or asking "set up project", "configure AI context", "initialize unikit", "scan my project".
argument-hint: "[project description] (optional)"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(mkdir *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(git *)
  - Skill
  - Agent
  - AskUserQuestion
---

# UniKit Setup — Game Project Context Initialization

Set up AI agent context for a game project by:
1. Scanning the real tech stack from engine-specific sources
2. Bootstrapping `.unikit/config.yaml` (user-editable source of truth for language, git, and workflow)
3. Generating `.unikit/DESCRIPTION.md` — project specification
4. Generating `AGENTS.md` — structural map for AI agents
5. Bootstrapping the knowledge base (`.unikit/memory/core/` + `.unikit/memory/stack/`) via the rules registry
6. Delegating architecture generation to `/unikit-architecture`
7. Printing the setup summary as the final, user-facing confirmation that all artifacts are in place

The architecture sub-skill is invoked **before** the summary so the summary can honestly list `.unikit/ARCHITECTURE.md` alongside the other artifacts. When `/unikit-architecture` returns, do not end the turn — immediately print the Step 11 summary in the same response.

This skill is the entry point for the unikit ecosystem. It creates the foundational
context that other unikit skills (`unikit-devcontext`, `unikit-plan`, `unikit-implement`, etc.)
rely on for informed decision-making, including the canonical `.unikit/config.yaml` they all
read at the start of every command.

<!-- unikit:agents codex -->
---

## Subagent Delegation — BLOCKING PRE-REQUISITE

When the workflow reaches a step that requires a subagent (`Agent`), the assistant MUST automatically spawn the
subagent if agent execution is supported by the current environment and not prohibited by higher-priority
instructions.

Only if agent execution is unavailable or blocked, the assistant MUST ask the user before proceeding with any
alternative.
<!-- unikit:end -->
---

## Execution Contract

This skill must be executed as a strict workflow, not as guidance.

1. Steps are numbered 0-11; execute in order. Do not skip, merge, reorder, or compress steps unless the step explicitly says it may be skipped.
2. Do not infer user answers from context when the workflow requires an AskUserQuestion step.
3. Do not substitute a recommendation, summary, or "seems fine" confirmation for a required question. A generic approval ("yes", "ok", "go ahead") only answers the immediately pending question — it does not retroactively authorize skipped selections or unanswered follow-ups.
4. Do not create, edit, or install anything outside `.unikit/config.yaml` and `.unikit/system/LANGUAGE_RULES.md` before Step 4 is complete. After Step 4, every write must satisfy its own step's prerequisites (e.g., Step 9 rule installs require the missing-rules list from Step 9.3 and user confirmation from Step 9.4).
5. If the environment prevents a required step (tool unavailable, file missing, subagent unreachable), stop and print `BLOCKED at Step N: <reason>`. Do not silently substitute an approximation.

---

## Workflow

**Fixed order — always.** Regardless of whether `/unikit` is invoked with or without arguments, the first three user-facing decisions are always language → git → write config. Only after `.unikit/config.yaml` exists on disk do we ask the user for a project description, load engine rules, scan, or do anything else. This guarantees that every subsequent prompt and artifact respects the user's language choice.

### Step 0: Load Existing Config (if any)

Check whether `.unikit/config.yaml` already exists. This step is a pure file read — no user interaction, no arguments parsing.

- **If it exists** — Read it. Treat its values as the source of truth for `language.*`, `git.*`, `workflow.*`. Mark Steps 1 / 2 / 3 as "merge mode": prefer existing values, prompt only when a critical field is missing or empty.
- **If it does not exist** — set "bootstrap mode": Steps 1 / 2 / 3 will collect values from the user / git and write a fresh `config.yaml`.

All unikit artifacts live under fixed default paths (`.unikit/DESCRIPTION.md`, `.unikit/ARCHITECTURE.md`, `.unikit/RULES.md`, `.unikit/memory/`, `.unikit/plans/`, etc.) — see `{{skills_dir}}/{{self_name}}/references/config-template.yaml` for the canonical `language` / `workflow` / `git` schema.

---

### Step 1: Language Resolution

Determine the language used for AI-agent communication and generated artifacts. **This runs before `$ARGUMENTS` is parsed and before the project description prompt**, so that every subsequent question in this run is asked in the user's chosen language.

**Bootstrap mode** (no existing `config.yaml`):

AskUserQuestion: What language should I use for communication and artifacts?

Options:
1. English (en) — Default
2. Russian (ru)
3. Chinese (zh)
4. Other — specify manually (2-letter ISO code)

Map the answer to an ISO code (`en`, `ru`, `zh`, or user-supplied).

**If the user selected English**, set both `language.ui = en` and `language.artifacts = en` and skip the follow-up question.

**If the user selected a non-English language (`<lang>`), ask the follow-up:**

AskUserQuestion: What should be translated?

Options:
1. Communication only — AI responds in selected language, artifacts in English
2. Communication and artifacts — Both AI responses and generated files in selected language
3. Artifacts only — AI responds in English, generates files in selected language

Map the follow-up answer to `language.ui` / `language.artifacts`:
- Communication only → `ui = <lang>`, `artifacts = en`
- Communication and artifacts → `ui = <lang>`, `artifacts = <lang>`
- Artifacts only → `ui = en`, `artifacts = <lang>`

Always set `language.technical_terms = keep` (no prompt — edit `.unikit/config.yaml` later to change).

**Merge mode** (existing `config.yaml`): keep the loaded `language.*` values, do not re-prompt.

---

### Step 2: Git Detection

Detect git presence and base branch for the project. This runs immediately after language resolution and before any description prompt.

```bash
git rev-parse --is-inside-work-tree 2>/dev/null && echo "git" || echo "no-git"
```

- **`git`** → set `git.enabled = true`. Detect the default branch in this order:

  1. `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'`
  2. `git remote show origin 2>/dev/null | grep "HEAD branch" | awk '{print $NF}'`
  3. **Fallback: `main`** — if both commands return empty or fail (e.g. no remote, offline, detached state), unconditionally use `main`. Never leave `git.base_branch` empty when `git.enabled = true`.

  After detection, confirm with the user only when the detected branch is unusual (not one of `main`, `master`, `develop`, `trunk`). For usual branches and for the `main` fallback, accept silently without asking.

  AskUserQuestion (only for unusual branches): Detected base branch `<branch>`. Use it for diff/review/merge targets?
  Options: 1. Yes, 2. Use a different branch (free text).

- **`no-git`** → set `git.enabled = false`. Skip the base-branch prompt; leave `git.base_branch` empty in the generated config.

**Merge mode**: if `config.yaml` already declared `git.enabled` / `git.base_branch`, keep those values and skip detection.

Other git keys (`create_branches`, `branch_prefix`, `skip_push_after_commit`) take their template defaults unless the user explicitly overrides them later by editing `config.yaml`.

---

### Step 3: Write `.unikit/config.yaml`

Materialize the collected values into `.unikit/config.yaml`.

**Bootstrap mode** (no existing file):

1. `mkdir -p .unikit`
2. Read `{{skills_dir}}/{{self_name}}/references/config-template.yaml`.
3. Substitute the runtime placeholders:
   - `{{LANGUAGE_UI}}` → the ISO code from Step 1 (e.g. `ru`)
   - `{{LANGUAGE_ARTIFACTS}}` → same (or split value if user chose)
   - `{{GIT_ENABLED}}` → `true` or `false` from Step 2
   - `{{GIT_BASE_BRANCH}}` → the detected/confirmed branch (or empty for no-git)
4. `Write` the substituted content to `.unikit/config.yaml`.
5. Inform the user:

   > Created `.unikit/config.yaml`. Edit it any time to customize artifact paths, language, git, or workflow settings. All unikit skills will read your changes on the next run.

**Merge mode** (file already exists):

- Do **not** overwrite. Inform the user:

  > Reusing existing `.unikit/config.yaml` (found `language.ui = <value>`, `git.enabled = <value>`).

- If the file is missing one of the recently-added keys (e.g. `workflow.research_relevance_days`, `git.branch_prefix`, `git.skip_push_after_commit`), tell the user which keys are missing and offer to append them with their template defaults (do not touch the rest of the file). Use `Edit` for the targeted append, never a full rewrite.

After Step 3, treat `.unikit/config.yaml` as the source of truth for all subsequent language / git references in this run.

---

### Step 3.1: Write `.unikit/system/LANGUAGE_RULES.md`

Install the centralized language rules file that all skills and subagents reference.

**Both bootstrap and merge mode:**

1. `mkdir -p .unikit/system`
2. Read `{{skills_dir}}/{{self_name}}/references/LANGUAGE_RULES_TEMPLATE.md`.
3. `Write` its content as-is to `.unikit/system/LANGUAGE_RULES.md`.

The file instructs skills to read `.unikit/config.yaml` at runtime for language values. No placeholder substitution is needed — the template is static.

---

### Step 4: Parse Arguments / Project Description

Only now — after language, git, and `.unikit/config.yaml` are settled — look at `$ARGUMENTS` and collect the project description. All output from this point forward is in the language chosen in Step 1.

```
Check $ARGUMENTS:
├── Has description? → save as project description, proceed to Step 5
└── No arguments? → ask user ↓
```

If no arguments:

AskUserQuestion: What kind of game are you building? Briefly describe the genre and core idea.
(e.g., "2D mobile tycoon game where you run a pawnshop", "3D first-person horror", "top-down RPG with crafting")

Save the user's answer as project description, then proceed to Step 5.

---

### Step 5: Load Engine Rules

This skill requires `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md` to exist.
It contains all engine-specific scan rules, paths, detection tables, and stack selection options.
The UniKit installer creates this file when the user selects their game engine.

If `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md` does not exist, stop and inform the user:
> "Engine rules not found. Run the UniKit installer first to select your game engine."

Read `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md` once and use it throughout all subsequent steps.

---

### Step 6: Project Scan

Check for engine project indicators listed in the **"Engine Detection"** section of `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`.

**If engine project exists** — scan it. The goal is to document what the project *actually* uses. Track every detected technology — these answers will be used to skip corresponding questions in Stack Selection.

**If no engine project** — skip to [Step 7: Interactive Stack Selection](#step-7-interactive-stack-selection).

**2.1 Project Settings**

Read the project settings file specified in the **"Project Settings"** section of `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`.
Extract the fields listed there: engine version, target platform, renderer, project name.

**2.2 Package Dependencies**

Read the package manifest specified in the **"Package Dependencies"** section of `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`.

Categorize packages according to the rules there:
- **Default/core packages** — skip (use the filter pattern from ENGINE_RULES.md)
- **Feature packages** — note as part of the stack
- **Third-party packages** — key dependencies, note them

Check the lock file if one is specified.

**2.3 Plugins**

Scan the plugin directory from the **"Plugin Directories"** section of `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`.
Use the detection table to identify known plugins by their folder indicators.

**2.4 Third-Party Assets**

Scan the third-party assets directory from the **"Third-Party Assets"** section of `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`.
Use the detection table to identify known assets. **Skip if the section says to skip.**

**2.5 Custom Modules**

Scan the modules directory from the **"Custom Modules"** section of `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`.
Skip if no modules directory convention is defined or if the directory does not exist.

**2.6 Project Scripts**

Check the common script locations listed in the **"Script Conventions"** section of `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`.
Determine the organizational pattern (by feature, by layer, by type).

**2.7 Module Definitions**

Find module definition files using the glob pattern from the **"Module Definitions"** section of `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`.
These reveal the dependency graph and module boundaries.

**2.8 Scenes**

Find scene files using the glob pattern from the **"Scene Files"** section of `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`.
Note the bootstrap/entry scene, main gameplay scene, and any additional scenes.

**After scanning, present the analysis to the user:**

```markdown
## Project Analysis

**Engine:** [use output format from ENGINE_RULES.md "Project Settings" section]
**Platform:** [target platform]

### Detected Stack

**[Section name from ENGINE_RULES.md "Package Dependencies"]:**
- [significant packages, excluding defaults per filter]

**Plugins ([path from ENGINE_RULES.md]):**
- [each plugin with purpose]

**Third-Party Assets:**
- [each asset with purpose]

**Custom Modules:**
- [each module with purpose]

**Scripts Directory:** [detected path]
**Module Definitions:** [count] files
**Scenes:** [list key scenes]
```

Then proceed to Stack Selection — the scan results pre-fill answers, so already-detected categories will be skipped.

---

### Step 7: Interactive Stack Selection

Ask each category as a separate `AskUserQuestion`. **Skip any question where the answer was already determined by the Project Scan** (e.g., if a DI framework was found during plugin scan, skip the DI Framework question). For skipped questions, note the detected value in the analysis output.

Read the **"Stack Selection Options"** section of `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md` — it contains the available options for each category with engine-specific descriptions and notes.

Based on the project description and scan results, recommend a tech stack. Show recommendations with reasoning tailored to the project type. Explain *why* each recommendation fits.

Present ALL options from ENGINE_RULES.md for each category in order. Never truncate or summarize option lists — show every row from the table exactly as written, so the user sees the complete set of choices:

**1. Architecture** — present options from the "Architecture" table.

Based on choice:
- If ECS selected → note ECS as project architecture, then ask ECS Framework follow-up (from "ECS Frameworks" table). Based on ECS choice → add chosen framework to stack. Check "Notes" column — some ECS frameworks include networking (skip Networking question if noted).
- If a non-default architecture selected (not OOP) → add to stack
- Note the chosen architecture as project architecture regardless

**2. Networking** — present the appropriate "Networking" table based on the architecture chosen in step 1 (ECS vs non-ECS have different option sets).
- **Skip entirely** if Photon Quantum was selected as ECS framework in step 1 — it already includes networking

Based on choice:
- None → skip networking setup
- Any framework → add to stack

**3. DI Framework** — present options from the "DI Frameworks" table.

Based on choice:
- None → skip DI setup
- Any framework → add to stack, note specific patterns (e.g., installer patterns for Zenject)

**4. Async Pattern** — present options from the "Async Patterns" table.

Based on choice:
- Built-in/legacy patterns → note as primary async pattern, do not add to stack
- Third-party framework → add to stack, set as primary async pattern

**5. UI Architecture:**

AskUserQuestion: UI Architecture?

Options:
1. MVVM (recommended for data-driven UI with reactive bindings)
2. MVP family (MVP / MVP Passive View / MVP Presentation Model)
3. Other (specify in text)

Based on choice:
- MVVM → note MVVM as UI architecture pattern
- MVP family → note MVP as UI architecture pattern, ask user to clarify variant if needed
- Other → add user-specified UI architecture to stack

**6. UI Framework** — present options from the "UI Framework" table.

Based on choice:
- Built-in/default framework → note as UI framework, do not add to stack
- Third-party or advanced framework → add to stack

**7. Additional engine-specific sections** — scan `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md` for a block delimited by `<!-- unikit-additional-sections -->` and `<!-- /unikit-additional-sections -->` HTML comments. If the opening tag is absent — or the block between the tags has no subsections — skip this step silently and move to step 9. Otherwise, for every subsection (`### …`) inside that block that contains a markdown table with a `| # | Option | Description |` header, ask the subsection as a separate `AskUserQuestion` in the order it appears in the file. Subsections without such a table are skipped silently.

- **Default rendering (single-select):** one numbered option per table row. User picks exactly one.
- **Multi-select rendering:** if the subsection body starts with `**Presentation:** numbered-multi-select`, present two-step interaction. **Step 1** — single `AskUserQuestion` with three options: `All` (select every row), `Select some` (pick specific numbers), `Skip` (select none). **Step 2** — only if the user chose `Select some`: a second `AskUserQuestion` asking for the list of row numbers; the user types the list (e.g. `2, 5, 9`) through the tool's built-in "Other" free-text slot. Parse comma-separated integers, look up each corresponding row's `Option` column, and treat every resolved option as a selected value.
- Every selected option (single- or multi-select) is added to the required set directly with its label as-is; `Package Display Names` is consulted only for short aliases of UPM-package rows from the Step 6 scan.

**8. Additional frameworks and plugins?**

AskUserQuestion: Any additional frameworks, plugins, or libraries you plan to use?
(e.g., inventory system, dialogue, AI trees, animation, networking — show examples from ENGINE_RULES.md "Additional Frameworks Examples")

Options:
1. Skip — proceed without adding anything
2. Specify (free text — list everything you want to add)

Based on choice:
- Skip → proceed
- Specify → add each user-listed framework/plugin to stack

---

**How to determine what is a "stack technology":**

Every Step 7 selection whose prose marks it with `add to stack`, every free-text item from Q8/Q9 (and Q1–Q7 `Other` when the surrounding prose marks the choice with `add to stack`), and every scan-detected plugin / non-default package / third-party asset from Step 6 becomes a required rule. Sentinel labels that the engine's `ENGINE_RULES.md` prose marks as `do not add to stack` (typical examples: `None`, `OOP`, `Built-in`, `Awaitable`, `Coroutines`, `ManualDI`, `IMGUI`, `uGUI`, `Pure DI`, `Signals + await`, `Built-in Control`, `None — Autoloads`) are excluded — the prose is the source of truth, the list above is illustrative.

The `Package Display Names` table in `ENGINE_RULES.md` is **not** a gate — it only maps UPM package ids to short display names (e.g. `com.unity.render-pipelines.universal → URP`). Packages absent from that table keep their id verbatim in `required`.

---

### Step 8: Generate Context

After Stack Selection is complete:

1. Generate `.unikit/DESCRIPTION.md` from description + scan results + confirmed stack — see [DESCRIPTION.md Template](#descriptionmd-template). The **Engine** field always includes the render pipeline extracted by the Step 6 Project Settings scan from the file listed in the engine's `ENGINE_RULES.md` "Project Settings" section. Use the `Output format` string declared in that same section verbatim. This is a scan-only field — the `/unikit` skill never asks the user about the renderer.
2. Generate `AGENTS.md` in project root — see [AGENTS.md Template](#agentsmd-template).

Architecture generation (`.unikit/ARCHITECTURE.md` via `/unikit-architecture`) is intentionally **not** done here — it is the very last step of this workflow (see Step 11). Do not invoke it from Step 8.

---

### Step 9: Bootstrap Memory Rules

Prepare the rules knowledge base in a few passes. Core rules are installed silently from the registry. Then — working from the authoritative installed state — the skill builds a list of truly missing stack rules, confirms with the user *what* should be created without revealing the mechanism, queries the registry to see which of those rules are available as vetted content, and only then asks *how* to create them (install from registry, generate locally, or decide per framework). A final sync pass reconciles state with disk.

#### 9.1: Ensure directory structure

Create directories and index file if they don't exist:

- Memory root → `.unikit/memory/`
- Core memory subdir → `.unikit/memory/core/`
- Stack memory subdir → `.unikit/memory/stack/`
- Rules index file → `.unikit/memory/RULES_INDEX.md`

```bash
mkdir -p .unikit/memory/core .unikit/memory/stack
```

Check whether `.unikit/memory/RULES_INDEX.md` exists. If not, create it from this template:

```markdown
# Rules Index

Knowledge base rules for the project. Located in `.unikit/memory/`.

## Override Priority (highest wins)

1. **`.unikit/RULES.md`** — project-specific overrides (always wins)
2. **`.unikit/ARCHITECTURE.md`** — project architecture decisions
3. **`.unikit/memory/core/*.md`** — universal best practices
4. **`.unikit/memory/stack/*.md`** — framework-specific knowledge

When a project rule in `RULES.md` conflicts with a template rule in `rules/`, the project rule wins.

---

Read this index to determine which rule files are relevant for the current task, then load only the needed files.

## Core — universal game development knowledge (`.unikit/memory/core/`)

| File | Description | Load When |
|------|-------------|-----------|

## Stack — framework-specific knowledge (`.unikit/memory/stack/`)

| File | Description | Load When |
|------|-------------|-----------|
```

#### 9.2: Core bootstrap

Install the whitelisted core rule set via the registry chain (primary → official → bundled). This is a quiet, idempotent step — on a re-run it will either skip everything (hash match) or pull fresh content when the registry has been updated. The no-args form of `rules install` owns the core-bootstrap contract: it fetches the manifest once, installs the whitelisted core ids, and regenerates `RULES_INDEX.md` on every invocation.

```bash
unikit-ai rules install
```

Only surface the output if the command fails (non-zero exit). On success it is safe to continue without displaying the aggregated report (the summary line `Rules: N installed, M already-installed, K failed` is emitted but not required in the skill's own output).

#### 9.3: Build the authoritative missing-rules list

The goal of this step is to produce a list of stack technologies that **need** a rule created **and** do not already have one. This list must not contain anything already installed — otherwise Step 9.7 will call `rules install` on ids that are already present and waste registry round-trips. With the variadic `rules install` handler those ids are still absorbed into the aggregated report (`↻ already installed`) instead of emitting exit 4, but building an accurate `missing` set keeps the install report clean and the flow predictable.

**Skill-side canonical form.** Define this helper once and use it at every skill↔CLI boundary:

```
toCanonicalRuleId(name) = name.trim().toLowerCase().replace(/[\s_]+/g, '-')
```

This is strictly a transform applied at the call-site (set-difference comparisons in 9.3, registry cross-reference in 9.5, args for `rules install` in 9.7). The `required` / `targets` / `missing` arrays themselves never mutate — they stay in display form. The CLI's internal `normalizeRuleId` only does `trim + toLowerCase`, so the space→hyphen pass is the skill's responsibility whenever display names contain spaces (e.g. `"Input Manager"` → `"input-manager"`).

**Three-layer principle — display raw, compare canonical, store canonical:**

- **UI layer** — Step 9.3 presenting, Step 9.4 `AskUserQuestion`, Step 9.5 `Technology` column: names stay in display-raw form (a multi-word framework like `"Input Manager"`, a plugin folder like `"Databrain"`, an aliased package id like `"URP"`).
- **Comparison layer** — Step 9.3 set-difference, Step 9.5 registry cross-reference, Step 9.7 `rules install` argv: apply `toCanonicalRuleId` to both sides. Arrays are never mutated in place.
- **Storage layer** — `.unikit/memory/stack/*.md` filenames and `.unikit.json` `entry.name` are always canonical lowercase-hyphen. The writers (`rules install` CLI and the `/unikit-memory` subagent) enforce that filename form themselves — this skill does not need to rename anything on disk.

Build the "already installed" set from **two authoritative sources** (not from `RULES_INDEX.md` — that file is derived and can lag behind reality between runs):

1. `.unikit.json` state — the real state tracked by the CLI. Read it via:

   ```bash
   unikit-ai rules status --json
   ```

   Parse the JSON output and collect every entry where `category === "stack"`. Every `name` in that list is considered installed regardless of `source` (`registry` / `local`) — both sources mean a file on disk that we must leave alone.

2. Disk scan — list `.unikit/memory/stack/*.md` (excluding `RULES_INDEX.md`). Treat every `<name>.md` filename as also installed. This catches rules that exist on disk but have not yet been reconciled into state (e.g. a rule generated in a parallel skill run that never triggered `rules sync`).

Union both sets into `already_installed`.

Next, build the `required` set as the union of three disjoint sources:

```
required = detected_from_scan ∪ picked_from_qs ∪ free_text
```

where:

- **`detected_from_scan`** — **identified framework names** derived from the Step 6 scan, not raw folder / package strings. For each scan entry, identify what framework it represents, then emit that name:
  - **Package manifest entries** — from "Package Dependencies" in `ENGINE_RULES.md`, minus the engine's `Default package filter`. For well-known package ids, the `Package Display Names` table supplies an alias (e.g. `com.unity.render-pipelines.universal → URP`). For ids outside the table, use general ecosystem knowledge to identify the framework name when obvious; otherwise keep the raw package id.
  - **Plugin folders** — from `Assets/Plugins/*/` or the engine equivalent. The `Plugin Directories` detection table provides folder → framework hints for common cases (`Sirenix/ → Odin Inspector`, `Aspid/ → ASPID MVVM`, `Demigiant/ → DOTween`). The table is **non-exhaustive** — the ecosystem has hundreds of plugins and no table can enumerate them all. For folders outside the table, use general ecosystem knowledge to infer the framework when the folder clearly matches a known third-party library; otherwise keep the folder name verbatim.
  - **Third-Party Assets folders** — same identification logic as Plugin folders.
  - `Assets/Modules/*/` is **not** included — project code, not a framework.

  Entries hold **framework names**, not raw strings. When identification is not confident, fall back to the raw folder / package name — surfacing an unknown name to the user is safer than guessing wrong. The `Plugin Directories` and `Package Display Names` tables are **hints, not gates**. No slugify, no lowercase — display form is preserved.

- **`picked_from_qs`** — every Step 7 option the user selected whose prose in the current engine's `ENGINE_RULES.md` marks the choice with `add to stack`. Options whose prose says `do not add to stack`, `note as …, do not add to stack`, or `skip …` are excluded. The source of truth is the Step 7 prose together with the actual engine's `ENGINE_RULES.md` — the sentinel set is engine-specific and is **not** hard-coded in this skill. Consult the current engine's prose every run.

  **Q1–Q7 `Other` free-text.** When the user picks `Other` in any of Q1–Q7 (Architecture, Networking, DI, Async, UI Framework, engine-specific subsections) and the step prose marks the choice with `add to stack`, the free-text content goes into `required` in display-raw form — symmetric to Q8/Q9 handling. No normalization, no slugify at this stage.

  Note: `picked_from_qs` is **not** consulted against the `Package Display Names` table — that table is display-alias-only for UPM packages from `detected_from_scan`.

- **`free_text`** — Q8 `Other` inputs from engine-specific subsections and Q9 `Additional frameworks` free-text. Q1–Q7 `Other` is already covered by `picked_from_qs` and is not duplicated here.

`required` entries stay in display-raw form throughout; canonicalization happens only at comparison / CLI-boundary sites.

Before computing `missing`, query the registry catalog so the same result feeds both the set-difference here and the informational table in Step 9.5. `rules list` returns `{ engine, rules: [{ id, category, description, version }] }` — filter to `category === "stack"`:

```bash
unikit-ai rules list --json
```

For each entry in `required`, **semantically match** it against that stack pool. See Step 9.5 for the matching criteria — the key point is that id-similarity, description match, and common aliases all count; strict canonical equality is the strongest signal but not the only one (`Odin Inspector` → registry `odin`, `ASPID MVVM` → registry `aspid-mvvm`, and so on). Record `{ display, resolved_id, resolved_version }` per entry; `resolved_id` is the registry id when match confidence is high, otherwise `null`.

Then compute the set-difference against `already_installed`. An entry counts as installed if **either** its resolved registry id **or** its canonicalized display name matches an on-disk rule — this keeps aliased installs (e.g. `odin` on disk for a scan entry `Odin Inspector`) out of the `missing` list on re-runs:

```
already_installed_canonical = {
  toCanonicalRuleId(name) for name in
    (rules_status_json.entries where category == "stack")
    ∪ disk_scan(.unikit/memory/stack/*.md)
}

def canonical_for(r):
    # Prefer the semantically-resolved registry id. Otherwise fall back to the
    # display-name canonicalization.
    return r.resolved_id or toCanonicalRuleId(r.display)

missing = [
    r for r in resolved_required
    if canonical_for(r) not in already_installed_canonical
]
# `missing` entries keep the display-raw form for Step 9.4; their resolved
# ids (when present) flow forward to Step 9.5 and Step 9.7.
```

If `missing` is empty — skip straight to Step 9.9 (final sync). Do **not** ask the user anything: there is nothing to create.

#### 9.4: Confirm which missing rules to create

Present the `missing` list in plain language. **Do not mention "registry", "agents", "install", or "generate" in this question** — the user does not yet need to know how the rules will be produced. At this point we only want to confirm *what* to create.

Before presenting the question, partition `missing` into three blocks and number items continuously across all blocks. Skip any empty block in the output:

- **(a) Frameworks** — `detected_from_scan` items that were identified as a specific framework (via the `Plugin Directories` / `Package Display Names` hints or general ecosystem knowledge). Display the **resolved framework name**, not the raw folder or package id.
- **(b) Detected dependencies** — `detected_from_scan` items that remained as raw folder / package identifiers because no confident framework identification was possible.
- **(c) Specified manually** — `picked_from_qs` and `free_text` entries (Step 7 choices marked `add to stack`, Q1–Q7 `Other` free-text, Q8/Q9 free-text).

AskUserQuestion: The following stack rules are missing and should be created. Proceed?

Frameworks:
  1. Odin Inspector
  2. ASPID MVVM
  3. UniTask
  4. DOTween

Detected dependencies:
  5. Databrain
  6. com.example.customlib
  7. Sonity

Specified manually:
  8. MyCustomPlugin

Options:
1. All — create rules for every item on the list
2. Select — pick specific items from the list (comma-separated numbers across all groups)
3. Skip — do nothing, proceed without touching stack rules

(The block above is an illustrative example — only groups that actually have entries are shown at runtime; numbering is continuous across the ones that remain.)

Based on choice, build the `targets` list:
- **Skip** → `targets = ∅`, jump to Step 9.9.
- **Select** → parse the comma-separated numbers as one continuous range across whichever blocks were rendered; `targets` = the chosen subset (display-raw labels preserved).
- **All** → `targets` = the full missing list.

#### 9.5: Registry lookup — semantic matching

`targets` carries the resolved registry metadata from Step 9.3 (skill already ran `rules list --json` and kept `resolved_id` / `resolved_version` per entry during the `missing` computation). Reuse that cached result — do **not** re-query `rules list`.

**Semantic matching — NOT strict id equality.** The matching procedure Step 9.3 applied is documented here because this step surfaces the result to the user. For each `target`, search the stack pool for the registry rule that represents the same framework. Three signals — any one at high confidence is enough, but combining them strengthens the verdict:

- **Id similarity** — the registry `id` contains the target's canonical form, is contained by it, or is a known short alias. Examples: target `ASPID MVVM` (canonical `aspid-mvvm`) → registry `aspid-mvvm` (exact); target `Odin Inspector` (canonical `odin-inspector`) → registry `odin` (short alias, **not** `odin-inspector`); target `UniTask` → registry `unitask`.
- **Description match** — the registry rule's `description` field names the target framework. Example: registry id `odin` with description `"Odin Inspector attribute patterns, validation, editor tools"` matches target `Odin Inspector` because the description explicitly names it.
- **Common naming conventions** — short aliases widely used in the ecosystem (`urp` ≡ Universal Render Pipeline, `dotween` ≡ DOTween / Demigiant, `r3` ≡ R3 reactive streams, `nodecanvas` ≡ NodeCanvas).

Do **not** require `toCanonicalRuleId(target) === registry.id`. That single-criterion check misses every aliased rule and is exactly what this flow is designed to avoid. `toCanonicalRuleId` remains the **strongest single signal** when it hits, but when it misses, continue through id-similarity, description-match, and ecosystem conventions before giving up. When in doubt (weak similarity, ambiguous candidates), prefer `unmatched` — generating a fresh rule via `/unikit-memory` is safer than installing the wrong one.

Partition `targets` into two bags using the cached `resolved_id`:

- `matched` — targets with `resolved_id != null`. Use `{ id: resolved_id, version: resolved_version }` for the Step 9.7 install call; the display-raw target label stays in the UI.
- `unmatched` — targets with `resolved_id == null`. These flow to Step 9.8 for generation via `/unikit-memory`.

Show a short informational table — **not** a decision point, just context for the next question. The `Technology` column shows the display-raw target label; the `Registry` column shows the matched registry id (or `✗ not found`):

```
Technology             Registry              Version
---------------------- --------------------- --------
URP                    ✓ urp                 1.2.0
DOTween                ✓ dotween             2.0.0
Odin Inspector         ✓ odin                1.5.0
ASPID MVVM             ✓ aspid-mvvm          1.1.0
Databrain              ✗ not found           —
```

#### 9.6: Choose how to create the rules

**If `matched` is empty** — skip this question entirely. There is nothing to install from the registry; everything in `targets` becomes `generate_set` and proceeds straight to Step 9.8.

Otherwise, ask the user how to produce the rules:

AskUserQuestion: How should I create these rules?

Options:
1. Install matches from registry, generate the rest — use the registry for {matched.length} rule(s) and generate {unmatched.length} locally. **Recommended when matched rules look appropriate.**
2. Generate everything from scratch — ignore the registry and generate all {targets.length} rules locally. Use when you want project-specific content instead of the vetted registry version.
3. Decide per framework — answer separately for each item

Based on choice:
- **Option 1** → `registry_set = matched`, `generate_set = unmatched`.
- **Option 2** → `registry_set = ∅`, `generate_set = targets` (includes matched entries — the user explicitly wants to regenerate them).
- **Option 3** → For each item in `matched`, ask a per-item AskUserQuestion:
  - Prompt: `How should I create the rule for {name}?`
  - Options: `1. Install from registry (v{version})`, `2. Generate locally`
  - Route the item into `registry_set` or `generate_set` based on the answer.
  - All items in `unmatched` go straight into `generate_set` without a per-item prompt (there is nothing to install for them).

#### 9.7: Install registry-backed stack rules

If `registry_set` is empty, skip this step. Otherwise invoke the CLI **once** with all ids as variadic arguments — the new handler fetches the manifest a single time and emits an aggregated report:

```bash
unikit-ai rules install <id1> <id2> <id3> ...
```

Parse the aggregated report line-by-line. Each id produces one of three markers:
- `✓ installed <category>/<id> v<version>` — fresh install or `--force` overwrite, count as success.
- `↻ already installed <category>/<id>` — absorbed idempotent skip. Log a short note like `{id} already installed — skipped` and continue. **Never retry with `--force`** unless the user explicitly asked for it earlier.
- `✗ failed <category>/<id>: <reason>` — per-rule failure, continue to the next id in the report.

The summary line `Rules: N installed, M already-installed, K failed` is the authoritative tally.

Exit code handling for the variadic call:
- `0` — at least one rule installed or already-installed; K failures are per-rule and have already been surfaced in the report. Continue.
- `1` — every requested id failed (no successes, no already-installed). Show the full output and ask `AskUserQuestion: "rules install {ids}" failed for every id — abort Step 9, or continue without stack rules?` with options `1. Continue without stack rules`, `2. Abort step`. Route accordingly.
- `2` — registry chain unreachable (fatal). Show the CLI output and abort the step with the same prompt as above.
- `5` — engine missing from manifest or empty core whitelist (fatal). Show the CLI output and abort.

Do not call the command once per id — the whole point of the variadic shape is to fetch the manifest once per Step 9.7 run.

#### 9.8: Generate the remaining stack rules via agents

**Invariant — always via subagent:** route every item in `generate_set` through an `Agent` call, including when `generate_set.length === 1`. Never generate a stack rule inline in this skill's own context, even for a single technology. Rule generation is token-heavy (ENGINE_RULES, templates, refs) and must not pollute the `/unikit` context before Steps 10-11 run.

The `generate_set` list contains stack technologies that either had no registry match or that the user chose to generate locally. For each, launch an `Agent` call that generates the rule:

```
Agent(
  subagent_type: "general-purpose",
  prompt: "/unikit-memory --skip-registry Add stack rules for {technology name}",
  description: "Generate {technology} rules",
  skills: ["unikit-memory"]
)
```

The `--skip-registry` flag tells `/unikit-memory` to bypass its own registry-lookup step (9.5 already covered it) and go straight to generation.

Launch up to **10 agents in parallel**. If more than 10 technologies remain, batch them: launch 10, wait for completion, launch next batch.

**Wait for all launched agents to finish** before proceeding to Step 9.9.

**Fallback** (if the `Agent` tool is unavailable in the current environment): do NOT execute `/unikit-memory` yourself inline — that violates the invariant above. Instead, print one invocation per item in `generate_set`, each on its own line, **outside any code fence**, prefixed with `Run: `, so the user can copy-paste and run them. The N=1 case takes the same path: one `Run: /unikit-memory ...` line. After printing, proceed to Step 9.9 without waiting — the user runs them asynchronously.

#### 9.9: Final reconciliation

Close the loop with a sync pass so that `.unikit/memory/RULES_INDEX.md`, `.unikit.json`, and the contents of `.unikit/memory/` end up in agreement (including rules generated in Step 9.8 which went straight to disk without touching state).

```bash
unikit-ai rules sync
```

On success continue to [Completion](#completion).

---

## DESCRIPTION.md Template

Generate `.unikit/DESCRIPTION.md` with content adapted to what was actually discovered or confirmed by user.

```markdown
# Project: [Project Name]

## Overview
[Clear description of the project — what it is, genre, target audience]

## Core Features
- [Feature 1]
- [Feature 2]
- [Feature 3]

## Tech Stack
- **Engine:** [Engine name + version / Language + version / Render pipeline] — last segment is the render pipeline from the Project Settings scan; format is the `Output format` string from the engine's `ENGINE_RULES.md` "Project Settings" section
- **DI:** [framework name / None]
- **Async:** [framework or pattern name]
- **Reactive:** [framework name / None]
- **UI Binding:** [framework name / None]
- **Inspector:** [tool name / default]
- **Animations (UI):** [framework name / None]
- **Asset Loading:** [framework name / built-in / None]
- **[category]:** [technology]

## Architecture Notes
- [Key architectural decisions discovered or planned]
- [Module/folder organization pattern]
- [Notable patterns: DI lifecycle, factory pattern, event bus, etc.]

## Architecture
See `.unikit/ARCHITECTURE.md` for detailed architecture guidelines.

## Non-Functional Requirements
- **Platform:** [target platforms]
- **Performance:** [key performance constraints]
- **Testing:** [test framework and patterns]
- **Documentation:** [documentation conventions]
```

**Rules:**
- Every technology listed must be detected by scan or confirmed by user during Stack Selection
- Do not list default engine packages (use the filter from ENGINE_RULES.md)
- Group related technologies logically
- Architecture Notes should capture real patterns, not generic advice

---

## AGENTS.md Template

Generate `AGENTS.md` in the project root as a structural map for AI agents.

Use the **"Project Structure Template"** and **"Key Entry Points"** from `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`
as the basis for the structure section, but only include directories and files that actually exist.

```markdown
# AGENTS.md

> Project map for AI agents. Keep this file up-to-date as the project evolves.

## Project Overview
[1-2 sentences from project description]

## Tech Stack
[Compact table from project description — engine, DI, async, key frameworks]

## Project Structure
[Use Project Structure Template from ENGINE_RULES.md, show only real folders]

## Key Entry Points
[Use Key Entry Points from ENGINE_RULES.md, fill with actual files]

## Scenes
| Scene | Purpose |
|-------|---------|
| [scene name] | [purpose] |

## Module Map
| Module | Path | Purpose |
|--------|------|---------|
| [module] | [path] | [purpose] |

## AI Context Files
| File | Purpose |
|------|---------|
| AGENTS.md | This file — project structure map |
| .unikit/config.yaml | User-editable unikit config (paths, language, git) |
| .unikit/DESCRIPTION.md | Project specification and tech stack |
| .unikit/ARCHITECTURE.md | Architecture decisions and guidelines |
| .unikit/RULES.md | Coding conventions and rules |
| .unikit/memory/RULES_INDEX.md | Index of framework-specific rule files |
```

**Rules:**
- Describe only what actually exists — no placeholders
- Directory tree shows real folders, not ideal ones
- Module Map lists real modules with their actual purpose
- Update `AI Context Files` to only list files that exist

---

### Step 10: Delegate Architecture Generation

After Step 9 finishes, generate `.unikit/ARCHITECTURE.md` by delegating to `/unikit-architecture`. Step 11 (Print Setup Summary) runs in the same response immediately after `/unikit-architecture` returns — do not end your turn in between.

**Invariant — always via subagent:** route `/unikit-architecture` through an `Agent()` call. Never invoke it inline in this skill's own context. Architecture generation is token-heavy (ENGINE_RULES, project scan, DESCRIPTION, RULES, RULES_INDEX, existing ARCHITECTURE) and must not pollute the `/unikit` context before Step 11 runs.

Launch the subagent:

```
Agent(
  subagent_type: "general-purpose",
  prompt: "/unikit-architecture",
  description: "Generate project architecture",
  skills: ["unikit-architecture"]
)
```

**Wait for the `Agent()` call to return** before proceeding to Step 11.

**Fallback** (only if the `Agent` tool is unavailable in the current environment): invoke `/unikit-architecture` inline in this skill's context, wait for it to return, then proceed to Step 11. Unlike Step 9.8, Step 11's summary explicitly lists `.unikit/ARCHITECTURE.md` as a generated artifact — the flow must complete in the same turn, so inline execution is the mandatory fallback here.

After the subagent (or inline invocation) returns, immediately print Step 11 in the same response.

---

### Step 11: Print Setup Summary (final action)

In the **same turn** that `/unikit-architecture` returned, print the setup summary. This is the very last action of the workflow — after it, there is nothing left to do.

```
Project context configured!

Config file:        .unikit/config.yaml (edit to customize language, git, workflow)
Project description: .unikit/DESCRIPTION.md
Project map:        AGENTS.md
Architecture:       .unikit/ARCHITECTURE.md
Memory rules:       .unikit/memory/ (see RULES_INDEX.md)

Next steps:
- /unikit-plan <feature> — Plan a feature implementation
- /unikit-implement — Execute an existing plan
- /unikit-review — Review code quality

Ready when you are!
```

**If the project already has code (scan detected existing scripts), also append:**

```
Your project already has code. You might also want:

- /unikit-review — Review existing code for conventions
```

---

## Rules

1. **Scan reality, not assumptions** — every technology listed must be found in the project
2. **Do NOT implement** — this skill only sets up context. No project code, no feature code
3. **Do NOT modify existing code** — only create/update context files
4. **Skip defaults** — don't list default engine packages (per filter in ENGINE_RULES.md)
5. **Confirm before executing** — show the analysis and plan, wait for user approval
6. **Delegate architecture** — `/unikit-architecture` for architecture doc, don't generate it here
7. **Never overwrite an existing `.unikit/config.yaml`** — merge mode only adds missing keys via targeted `Edit`, never a full rewrite

## Artifact Ownership

- **Primary:** `.unikit/config.yaml`, `.unikit/DESCRIPTION.md`, `AGENTS.md`
- **Delegated:** `.unikit/ARCHITECTURE.md` via `/unikit-architecture`
- **Read-only:** `.unikit/RULES.md`, engine project settings (per ENGINE_RULES.md)
