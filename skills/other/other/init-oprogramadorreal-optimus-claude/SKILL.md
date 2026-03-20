---
description: Prepares a project for Claude Code — generates CLAUDE.md with progressive disclosure docs, auto-format hooks, code-quality agents (code-simplifier, test-guardian), and test infrastructure (framework, coverage tooling, testing docs). Detects empty directories and offers new-project scaffolding via official stack tooling before setup. Also audits and syncs existing documentation against source code. Replaces /init. Supports single projects, monorepos, and multi-repo workspaces (separate git repos under a shared parent directory). Use to bootstrap a new or existing project for Claude Code, or re-run to update an outdated setup.
disable-model-invocation: true
---

# Initialize Project for Claude Code

Analyze the project and set up Claude Code for optimal performance: generate CLAUDE.md with supporting docs (WHAT/WHY/HOW, progressive disclosure), install auto-format hooks per detected stack, deploy code-simplifier and test-guardian agents, set up test infrastructure (framework, coverage tooling, testing docs), and sync existing documentation against source code. Supports single projects, monorepos, and multi-repo workspaces.

## Before You Start

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/claude-md-best-practices.md`. Key constraints:
- Every CLAUDE.md <= 60 lines
- Use file:line references, not code snippets
- Only universally-applicable instructions
- Preserve user content: when re-running on an existing project, never silently drop content from CLAUDE.md that cannot be derived from the codebase. When unsure whether content is outdated, preserve it. Only mark content as outdated when source code directly contradicts it — and confirm with the user before removing user-added items.

**Write generated files directly.** Files under `.claude/` (docs, hooks, agents, CLAUDE.md) are plugin-generated content. Write new files immediately without asking for permission or confirming with the user — do not use `AskUserQuestion` for file writes. Only pause to confirm when **replacing** a file that contains user-customized content (identified as "User-added" in the audit). Generated content (agents, hooks, `coding-guidelines.md`, templates) is always overwritten silently — these are not user-authored files. Exception: `settings.json` must always be merged, never overwritten — see Step 5. The same rule applies to subproject docs in monorepos and per-repo `.claude/` files in multi-repo workspaces.

## Step 1: Detect Project Context

### Empty-directory detection

Before any project detection, check if the current directory is empty or near-empty. A directory is **near-empty** when it contains at most `.git/`, `.gitignore`, `LICENSE`, and/or a stub `README.md` (under 5 lines of non-empty content) — and **no manifest files** (`package.json`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `*.csproj`, `*.sln`, `pubspec.yaml`, `pyproject.toml`, `CMakeLists.txt`) exist at any depth, and **no directories commonly used for source code** (`src/`, `lib/`, `app/`, `pkg/`, `cmd/`) are present.

If the directory is empty or near-empty, use `AskUserQuestion` — header "Empty Project", question "This directory appears to be empty. Would you like to scaffold a new project?":
- **Scaffold new project** — "Set up a new project from scratch (choose stack, generate hello-world app, then continue with full init setup)"
- **Continue anyway** — "Proceed with init as-is (I'll add code myself later)"

If the user chooses **Scaffold new project**: read and execute `$CLAUDE_PLUGIN_ROOT/skills/init/references/new-project-scaffolding.md`. If the scaffolding procedure returns an **unsupported-stack signal**, read and apply `$CLAUDE_PLUGIN_ROOT/skills/init/references/unsupported-stack-fallback.md` (steps 1–4) — search the web for the user's chosen stack's official scaffolding CLI command, apply the validation and approval rules from the fallback reference. If the fallback reaches step 5 (graceful skip), instead of skipping, create a minimal project manually (manifest file + entry point with hello-world code + `.gitignore`) with user approval. After scaffolding completes, discard all prior detection state and restart Step 1 from "Project detection" below — re-detect the now-populated project from scratch.

If the user chooses **Continue anyway**: proceed with normal Step 1 detection below.

### Project detection

**Identify project type and package manager:** Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/tech-stack-detection.md` for the manifest-to-type table, package manager detection table, and command prefix rules. Apply those tables to the current project. For the .NET note in that reference, list all solution projects and their roles in the CLAUDE.md Project Structure section. For the Dart/Flutter note, document the commands in CLAUDE.md.

**Extract**: Project name, tech stack, build system, available scripts.

**Analyze structure and extract doc insights:**
- Top-level directories for architecture pattern
- Entry points (main.ts, index.ts, app.module.ts, main.dart, etc.)
- README.md, CONTRIBUTING.md, ARCHITECTURE.md, docs/ directory files
- Monorepo: also each subproject's README.md

**Source code is the source of truth.** Manifests and actual project files always override what documentation claims. When reading existing docs:
1. **Extract non-code insights** — information not derivable from source code alone:
   - Architecture rationale and design decisions ("why" content for CLAUDE.md)
   - Contributor workflow conventions (branching strategy, PR process, commit format)
   - Coding conventions not enforced by linters (naming schemes, architectural boundaries)
2. **Discard** any insight **from project docs (README, CONTRIBUTING, etc.)** that directly contradicts source code (e.g., doc says "we use Redux" but only Zustand is in dependencies). Keep insights that are neither confirmed nor contradicted — non-code conventions and rationale are inherently unverifiable from source alone. This discard rule applies only to insight extraction from project documentation — content in existing CLAUDE.md files is handled separately by the Step 1b audit, where the standard of proof is stricter.

Factual contradictions in existing docs (wrong commands, outdated tech references, etc.) are detected and addressed in Step 6b.

These insights flow into generated files in Steps 4–6b. The Detection Summary confirms doc reading occurred, but do not narrate insights during analysis.

**Check for project structure:** Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/project-detection.md` for the full detection algorithm — multi-repo workspace detection (Step 0), workspace configs (Step A), manifest scanning with depth-2 checks (Step B), supporting signals (Step C), and subproject enumeration rules.

**Decision summary:**
- No `.git/` in current dir + 2+ child dirs with `.git/` → confirmed multi-repo workspace
- Workspace config found → confirmed monorepo
- 2+ projects with manifests → confirmed monorepo (but see .NET consolidation below)
- Supporting signals + 1 manifest dir → likely monorepo, ask user to confirm
- Supporting signals only → insufficient evidence, ask user to identify subproject dirs
- No signals → single project (one repo, one codebase — not a monorepo)

**.NET solution consolidation:** When a single root `.sln` references all discovered `.csproj` files, collapse them into 1 project before applying the matrix above. Non-`.csproj` manifests still count separately.

**If monorepo detected:** Inform user of detection signals and identified subprojects with tech stacks in the Detection Summary (Step 1 Checkpoint).

**If multi-repo workspace detected:** List each repo with its path and detected tech stack in the Detection Summary (Step 1 Checkpoint). For each repo, also report whether it is internally a monorepo or single project.

**Nested project handling:** When a repo has no manifest at its git root, but exactly 1 qualifying project in a subdirectory (via depth-2 check), and the root-as-project check fails for that repo — treat it as a **single project with a nested app root**. This applies both when running init directly in a repo and when processing repos within a multi-repo workspace. Note the subdirectory path; all commands in the generated CLAUDE.md must reference it (e.g., `cd ngapp && npm run build`).

### Step 1 Checkpoint

Before proceeding, confirm you have all of the following. If any are missing, re-examine the project:

- **Project name** (from manifest or README)
- **Tech stack(s)** (languages, frameworks, from manifest dependencies)
- **Package manager** (detected from lock files / config — e.g., npm, pnpm, yarn, uv, poetry, pip)
- **Build/test/lint commands** (from manifest scripts, prefixed with the detected package manager)
- **Project structure**: single project, confirmed monorepo, multi-repo workspace, or ambiguous (awaiting user input)
- If monorepo: **subproject list** with each subproject's path, purpose, and tech stack
- If monorepo: **workspace tool** (if any)
- If multi-repo workspace: **repo list** with each repo's path, tech stack, and internal structure (single project or monorepo)
- If nested app root detected: **app root path** (e.g., `ngapp/`)
- **Existing files inventory** (existence check only — content of docs is read in Step 1b; agents, hooks, and `coding-guidelines.md` are never audited, always overwritten): which of `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/docs/*`, `.claude/agents/code-simplifier.md`, `.claude/agents/test-guardian.md`, root `CLAUDE.md`, subproject `CLAUDE.md` files already exist
- **Test infrastructure detected** (yes/no): test framework in dependencies, test command in scripts, or test directory present. This determines the flow of Step 5c (test infrastructure setup).
- **Doc-sourced insights** (if any documentation found): verified conventions, architecture rationale, workflow rules — all cross-checked against source code

Print this as a **Detection Summary** to the user. Then use `AskUserQuestion` — header "Detection", question "Does the detection summary look correct?":
- **Proceed** — "Everything looks right — continue with setup"
- **Correct** — "I need to fix something before continuing"
- **Abort** — "Cancel init"

If the user selects **Correct**, ask what needs to be changed, update the detection results accordingly, and re-present the updated Detection Summary with the same `AskUserQuestion`.

If no test infrastructure was detected, include this note in the Detection Summary output:

> **Tests:** No test framework, test script, or test directory detected — you will be asked whether to install a test framework in Step 5c. Strongly recommended: multiple optimus skills depend on test infrastructure.

### Step 1b: Documentation Audit (only when existing docs found)

**Skip this step entirely if no existing documentation files were found in the inventory.** Proceed directly to Step 2.

**Plugin version check:** Read `$CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json` to get the current plugin version. Then check if `.claude/.optimus-version` exists in the project. If it does, read its content (a semver string, e.g., `1.11.0`). Compare the two:
- **Current plugin version is newer than stored version (compare major, minor, patch as integers)** → the plugin has been updated since the last run. Include this in the Audit Report header: "Plugin updated from vX.Y.Z to vA.B.C — templates may have improved." During the audit below, do **not** shortcut any file as "Accurate" without also comparing it against the current template — plugin-side template improvements should surface as findings.
- **Same version or no `.optimus-version` file** → proceed with normal audit behavior.

If existing docs were found, analyze them to identify what needs updating:

1. **Read all existing doc files** from the inventory (CLAUDE.md, settings.json, all `.claude/docs/*.md` except `coding-guidelines.md`, and for monorepos each subproject's CLAUDE.md and `docs/*.md`).

2. **Compare documented state vs detected state:**

| Dimension | Check |
|-----------|-------|
| **Commands** | Do build/test/lint commands in CLAUDE.md match current manifest scripts? |
| **Tech stack** | Does the documented stack match current dependencies in manifest files? |
| **Structure** | Do folder names, entry points, and architecture references in docs match the actual filesystem? |
| **Doc coverage** | Are there detected project aspects (test framework, UI deps, complex architecture) with no corresponding doc? Are there docs for aspects no longer present? |
| **Monorepo** | Do subproject tables match current workspace members? Any added/removed subprojects? |
| **Custom content** | Does CLAUDE.md contain sections, bullets, or instructions not matching any template section or detected project aspect (e.g., deployment notes, workflow conventions, known gotchas)? Classify as **User-added**. |

3. **Present an Audit Report** to the user, organized as:
   - **Outdated** — items in docs that no longer match the project (with specific before/after)
   - **Missing** — project aspects that should have docs but don't
   - **Accurate** — items that are still correct (brief summary, no action needed)
   - **User-added** — content not derivable from the codebase (custom conventions, workflow rules, architecture decisions). Preserved by default. If source code **directly contradicts** a user-added item (e.g., user wrote "deploy with Docker" but no Dockerfile or Docker dependency exists), classify it as Outdated instead — but flag it in the audit report as "previously user-added" so the user can confirm before removal.

**Standard of proof:** Only classify content as Outdated when source code **directly contradicts** a specific claim. Content that is neither confirmed nor contradicted is **not outdated** — classify it as Accurate or User-added as appropriate. When a user-added item appears outdated, use `AskUserQuestion` to confirm before discarding — the user may have context that isn't visible in the codebase.

4. Use `AskUserQuestion` — header "Audit", question "How would you like to handle the documentation audit findings?":
   - **Update all** — "Apply all recommended changes"
   - **Selective** — "Pick which findings to apply by number"
   - **Fresh start** — "Regenerate template content from scratch, but carry forward user-added sections"

   If the user selects **Selective**, ask which finding numbers to apply. Unapproved findings are left as-is (existing content preserved).

Remember the user's choice and approved findings. Steps 2–6 will reference them to make targeted updates rather than full overwrites. (Step 6b runs independently — see Step 6b.)

**Fresh start preservation:** Before regenerating, extract all User-added content from existing CLAUDE.md. After generating from template, re-insert user-added content in the most appropriate section. Present the merged result to the user before writing.

## Step 2: Handle Existing Files

**Audit-aware rule (applies to Steps 2–6, not Step 6b):** If user chose "Fresh start", regenerate all template-based content from scratch — but always carry forward items classified as **User-added** in the audit report, re-inserting them into the appropriate sections. Otherwise: if Step 1b marked a file as Accurate, skip it. If Outdated, apply only user-approved changes — preserve everything else. If Missing or no audit was run, create normally. For "Selective" updates, only act on approved findings. **Exception:** agents, hooks, and `coding-guidelines.md` are generated content (verbatim templates or fallback hooks) — always overwrite regardless of audit status.

**Default for ambiguous content:** When unsure whether content is outdated or user-intentional, preserve it. Only update or remove user-added content when source code provides clear contradicting evidence **and** the user has confirmed via the audit report or `AskUserQuestion`. Information that cannot be re-derived from the codebase must not be discarded to meet formatting or size targets.

**Before creating any file**, check if it already exists. If it does not exist, write it directly — no confirmation needed (see "Write generated files directly" in Before You Start). If it does exist, read it first. For generated content (agents, hooks, `coding-guidelines.md`), overwrite silently. For files that may contain user-customized content (CLAUDE.md, styling.md, architecture.md, testing.md), inform the user what was preserved vs changed.

**Relocate when scope changes:** If docs need to move (e.g., root `.claude/docs/testing.md` → subproject-scoped in a monorepo), move content to the new location and remove the old file. Keep only `coding-guidelines.md` at root.

If root `CLAUDE.md` exists (not in `.claude/`), suggest removing it after `.claude/CLAUDE.md` is created.

## Step 3: Create Directory Structure

```bash
mkdir -p .claude/docs .claude/hooks .claude/agents
# Monorepo: also mkdir -p <subproject>/docs for each subproject from Step 1
# Multi-repo workspace: run this inside each repo (each gets its own .claude/)
```

After creating directories, proceed directly to writing files in subsequent steps — do not pause for confirmation between file writes.

## Step 4: Create CLAUDE.md

### Single project

Use template from `$CLAUDE_PLUGIN_ROOT/skills/init/templates/single-project-claude.md`. Fill in all placeholders:
- Replace `[PROJECT NAME]` with the actual project name
- Replace `[One-line description]` with purpose from README or manifest
- Replace `[TECH STACK]` with detected languages and frameworks
- Fill the Conventions section with 2-5 bullets drawn from doc-sourced insights (Step 1): architectural patterns, naming conventions, key entry points, and non-obvious rules. If no insights were found, infer conventions from the project structure (e.g., "Express routes in `src/routes/`, middleware in `src/middleware/`", "CLI entry point at `src/index.ts` using Commander.js").
- Replace command placeholders with real commands using the detected package manager
- Replace directory placeholders with actual project directories
- Keep the "Before Writing Code" section exactly as templated — do not modify or remove it
- In the Documentation section, list only non-guideline docs that were actually created (testing.md, styling.md, architecture.md) using `.claude/docs/` prefix. The coding-guidelines.md reference is in the "Before Writing Code" section.
- In the Agents section, list only agents that were actually installed: code-simplifier is always listed; test-guardian only if test infrastructure exists after Step 5c (pre-existing or just installed)

**When updating an existing CLAUDE.md** (not Fresh start): edit the existing file in-place — do not regenerate from template. Update only sections where the audit found approved Outdated changes. Preserve all user-added content verbatim unless the audit classified specific user-added items as Outdated and the user approved their removal.

The template follows WHAT/WHY/HOW structure. Target 60 lines. If preserving user-added content would exceed this, first try to condense template-generated content (shorter descriptions, abbreviate stacks). If still over 60 lines, the limit may be exceeded — never discard user content to meet the line count. Note the overage in Step 7 summary. If no manifest was detected, use generic placeholders and inform user that manual customization is recommended.

### Monorepo

Use template from `$CLAUDE_PLUGIN_ROOT/skills/init/templates/monorepo-claude.md` instead. Fill in:
- Subproject table with all detected subprojects (path, purpose, tech stack)
- Root-level / workspace-wide commands only (not subproject-specific commands)
- References to each subproject's CLAUDE.md
- If a workspace tool was detected (Step A), include "managed by [tool]" in the description line
- If no workspace tool was detected (Step B only), use "Monorepo with [N] packages" or "Multi-project repository with [N] components" without referencing a workspace tool

Keep the "Before Writing Code" section exactly as templated — do not modify or remove it. If root-as-project: also list root-scoped docs from `.claude/docs/` (testing.md, styling.md, architecture.md as applicable) in the Documentation section. The coding-guidelines.md reference is in the "Before Writing Code" section.

In the Agents section, list only agents that were actually installed: code-simplifier is always listed; test-guardian only if test infrastructure exists after Step 5c (pre-existing or just installed).

If more than 6 subprojects, group by category (apps, libs, services) in the root CLAUDE.md and move the full subproject table to `.claude/docs/architecture.md`. Keep descriptions concise (abbreviate stacks, e.g., "TS/React" not "TypeScript, React, Vite, Tailwind") to stay under 60 lines (same user-content preservation rule as single-project applies).

### Multi-repo workspace

For multi-repo workspaces, **run the full init flow (Steps 3–7) independently inside each repo** — each repo gets its own complete, self-contained `.claude/` as if you had run init inside that repo directly. Use the single-project template (or monorepo template if the repo is internally a monorepo). Each repo's `.claude/` is version-controlled within that repo — a teammate cloning a single repo gets the full Claude Code experience without the plugin or the workspace.

After all repos are initialized, create a lightweight `CLAUDE.md` file at the workspace root (NOT inside a `.claude/` directory) using the template from `$CLAUDE_PLUGIN_ROOT/skills/init/templates/multi-repo-claude.md`. This file provides cross-repo context (repo table, API contracts, shared conventions) but contains no agents, hooks, or guidelines — repos do not depend on it. Note in the Detection Summary that this file is local-only and not version-controlled.

If a nested app root was detected for a repo (Step 1), ensure that repo's CLAUDE.md notes the nested structure and all commands reference the correct subdirectory.

## Step 4b: Create Subproject CLAUDE.md Files (monorepo only)

For each detected subproject (except root-as-project/root-as-member — the root CLAUDE.md already covers it), create `<subproject>/CLAUDE.md` using template from `$CLAUDE_PLUGIN_ROOT/skills/init/templates/subproject-claude.md`:
- Scope WHAT/WHY/HOW to that subproject's tech stack and purpose
- Include only commands specific to this subproject (run from its directory)
- Reference its local `docs/` folder for detailed documentation
- Mention parent monorepo name in the opening line
- Keep under 60 lines (same user-content preservation rule as single-project applies)

## Step 5: Install Formatter Hooks

Add auto-format hooks so files stay consistently formatted after every Edit/MultiEdit/Write. Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/formatter-setup.md` for the full hook template table, Python command detection, installation steps, and settings.json creation rules. For stacks without a built-in formatter template, also read `$CLAUDE_PLUGIN_ROOT/skills/init/references/unsupported-stack-fallback.md`.

Always overwrite existing hooks (both template-based and custom fallback hooks) — these are generated content, not project-customized.

Supported stacks: Python (black + isort), Node.js (prettier), Rust (rustfmt), Go (gofmt), C#/.NET (csharpier), Java (google-java-format), C/C++ (clang-format), Dart/Flutter (dart format). Other stacks are handled via best-effort fallback (see formatter-setup.md). Templates are in `$CLAUDE_PLUGIN_ROOT/skills/init/templates/hooks/`.

Key rules:
- External formatters not in deps → ask user before installing
- If no hooks installed → do not create settings.json (unless it already exists with other content)
- Preserve existing settings.json sections (permissions, custom config) — merge, never overwrite

## Step 5b: Install Code Simplifier Agent

Copy `$CLAUDE_PLUGIN_ROOT/skills/init/templates/agents/code-simplifier.md` to `.claude/agents/code-simplifier.md`.

Always overwrite — this is a verbatim template, not project-customized content.

## Step 5c: Test Infrastructure Setup

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/test-infra-provisioning.md` for the complete provisioning procedure.

**If test infrastructure was detected in Step 1** (test framework in dependencies, `test`/`test:*` script in manifest, or `tests/`/`test/`/`spec/`/`__tests__/`/`integration_test/` directory exists):

Run the full provisioning procedure from the reference: health check (run test suite, fix build/bootstrap failures with user approval), install test-guardian agent, create testing.md, add CLAUDE.md test references, append README testing section, update .gitignore. Also check for coverage tooling gaps — if framework exists but coverage tooling is missing, recommend installing it per the reference.

**If test infrastructure was NOT detected:**

Use `AskUserQuestion` — header "Test Infrastructure", question "No test framework was detected. Would you like to install one?":
- **Yes (strongly recommended)** — "Install test framework and coverage tooling — strongly recommended. Multiple optimus skills depend on test infrastructure: `/optimus:tdd` is non-functional without it, `/optimus:code-review` and `/optimus:refactor` lose deep mode, and `/optimus:verify` loses automated checks."
- **No** — "Skip test infrastructure setup — some optimus skills will have reduced functionality"

If the user chooses **Yes**: follow the "Framework and Coverage Tooling Installation" section of the reference (consult `$CLAUDE_PLUGIN_ROOT/skills/init/references/test-framework-recommendations.md`, ask user approval for specific framework, install, then run health check). After installation, run the full Optimus Infrastructure Provisioning from the reference (test-guardian, testing.md, CLAUDE.md refs, README section, .gitignore).

If the user chooses **No**: skip all test infrastructure provisioning. In Step 7 summary, include: "⚠ Test infrastructure was not installed — `/optimus:tdd` will not work, and `/optimus:code-review`, `/optimus:refactor`, and `/optimus:verify` will have reduced functionality. Re-run `/optimus:init` to install test infrastructure later."

## Step 6: Create Documentation Files

**Always create in `.claude/docs/`:**
- `coding-guidelines.md` - Use template from `$CLAUDE_PLUGIN_ROOT/skills/init/templates/docs/coding-guidelines.md` (replace [PROJECT NAME]). Shared across the entire repo. Always overwrite — this is a verbatim template, not project-customized content.

**Create based on these detection rules** (`testing.md` is handled by Step 5c, not here):

| File | Template | Create when ANY of these are true |
|------|----------|-----------------------------------|
| `styling.md` | `$CLAUDE_PLUGIN_ROOT/skills/init/templates/docs/styling.md` | Manifest lists a UI framework (react, vue, angular, svelte, solid) OR lists CSS tooling (tailwindcss, styled-components, sass, less, postcss) OR `.css`/`.scss`/`.less` files exist in `src/` OR manifest is `pubspec.yaml` with Flutter SDK dependency (Flutter apps are UI applications with theme, widget, and styling conventions) |
| `architecture.md` | `$CLAUDE_PLUGIN_ROOT/skills/init/templates/docs/architecture.md` | Project has 3+ top-level source directories (excluding config, tests, docs, build output) OR uses recognized pattern directories (controllers/, services/, repositories/, handlers/, models/) |

Use each template as a skeleton — fill in all placeholders with actual project details (framework names, commands, directory paths, conventions). Don't leave any `[placeholder]` text in the final output.

**Placement rules:**
- **Single project:** All files go in `.claude/docs/`.
- **Monorepo:** `styling.md` and `architecture.md` go in each subproject's `docs/` folder, scoped to that subproject's stack. Apply the detection rules above **per subproject** (e.g., skip `styling.md` for a subproject with no UI deps). `testing.md` placement is handled by Step 5c's provisioning reference. For root-as-project, its scoped docs go in `.claude/docs/` alongside the shared `coding-guidelines.md`. Each subproject can also get its own `coding-guidelines.md` only if its conventions differ significantly from root.

## Step 6b: Sync Existing Documentation

**Skip this step** if no project documentation exists (no README.md, CONTRIBUTING.md, ARCHITECTURE.md, or docs/ files). Proceed to Step 7.

This step runs independently of the Step 1b audit choice (including "Fresh start," which only governs `.claude/` files). It operates on project-owned files, not Claude-generated files.

Cross-check existing project documentation against the source code (manifests, lock files, directory structure). Fix **genuinely contradictory or outdated content** only — do not rewrite documents.

**Scope — only if they already exist:**
- README.md (root, and each subproject's for monorepos)
- CONTRIBUTING.md, ARCHITECTURE.md
- Files in docs/ that overlap with generated `.claude/docs/` topics

**Check for contradictions against source code (manifests, lock files, directory structure):**

| Type | Example |
|------|---------|
| Wrong command | README says `npm test`, but lock file and manifest show pnpm |
| Outdated tech ref | CONTRIBUTING references Webpack, but `vite.config.ts` exists and no Webpack in deps |
| Incorrect structure | README describes `src/controllers/`, but actual dir is `src/handlers/` |
| Stale subproject list | README lists 3 services, but workspace config has 4 |
| Removed dependency | Docs reference a library no longer in manifest dependencies |

The goal is surgical correction of factual errors, not editorial improvement. Only change content where source code directly contradicts a specific claim. Leave prose, tone, structure, and imprecise-but-not-wrong descriptions (e.g., "JavaScript" when project uses TypeScript with JS interop) untouched. Do not add sections, create files, or touch files outside the project root.

**If contradictions found:** Present a Sync Report (file, current content, proposed fix, source code evidence). Use `AskUserQuestion` — header "Sync", question "How would you like to handle the documentation sync findings?":
- **Apply all** — "Apply all proposed corrections"
- **Selective** — "Pick which corrections to apply by number"
- **Skip sync** — "No changes to project documentation"

If the user selects **Selective**, ask which correction numbers to apply. Apply only approved changes.

**If no contradictions found:** report this and proceed to Step 7.

## Step 7: Verify and Report

Run through this checklist. **Fix any failures before reporting to the user.**

**File existence** — verify every expected file was created. List all files in `.claude/` matching `*.md`, `*.json`, or `hooks/*`, and for monorepos also check each subproject path from Step 1 for `CLAUDE.md` and `docs/*.md`.

**Content checks** — verify each file has real content, not placeholders:
- `.claude/CLAUDE.md`: Actual project name, real commands, Conventions section (single project), Documentation section. Line count <= 60 (soft limit — may exceed if user-added content requires it; verify overage is not caused by template bloat).
- `.claude/settings.json` (if created): `hooks.PostToolUse` references every installed hook file and vice versa. If file had custom sections (permissions, etc.), verify they're preserved.
- `.claude/docs/coding-guidelines.md`: `[PROJECT NAME]` replaced with actual name.
- Each `testing.md`, `styling.md`, `architecture.md`: References the project's actual frameworks, tooling, and directory names.
- Monorepo: each subproject's `CLAUDE.md` exists, mentions subproject name, and is <= 60 lines (soft limit — same user-content preservation rule applies).
- `.claude/hooks/*`: Each template-based hook matches its template. Each custom hook (unsupported stack) follows the pattern of existing shell-based hooks (e.g., `format-rust.sh`) and satisfies `unsupported-stack-fallback.md` step 3 validation rules.
- `.claude/agents/code-simplifier.md`: File exists and matches template.
- `.claude/agents/test-guardian.md` (if test infrastructure exists after Step 5c — pre-existing or just installed): File exists and matches template.
- **Sync changes (Step 6b)**: If sync changes were applied, verify each modified file still has valid markdown and no truncated content.

**Cross-reference checks:**
- Every doc listed in a CLAUDE.md Documentation section actually exists as a file.
- Every agent listed in a CLAUDE.md Agents section actually exists as a file in `.claude/agents/`.
- Monorepo: every subproject in root CLAUDE.md's Architecture table has a corresponding `CLAUDE.md` file.
- Multi-repo workspace (if workspace root `CLAUDE.md` was created): every repo listed in it has its own `.claude/CLAUDE.md` file. Each repo's `.claude/` is self-contained (has its own coding-guidelines, hooks, agents).

**If any check fails:** Fix the issue, then re-verify. Do not proceed to the summary until all checks pass.

**Write plugin version:** After all checks pass, write the current plugin version (from `$CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json`) to `.claude/.optimus-version`. This file contains only the version string (e.g., `1.12.0`) with no other content. For multi-repo workspaces, write `.claude/.optimus-version` inside each repo.

**Summary:** Present the final report using this exact format:

```
---

### ✅ Optimus Init Complete

| Category | Details |
|----------|---------|
| **Project** | [project name] — [tech stack summary] |
| **Structure** | [Single project / Monorepo with N packages / Multi-repo workspace with N repos] |
| **Files created** | [count] files ([list: CLAUDE.md, settings.json, docs created, hooks, agents]) |
| **Formatters** | [which formatter hooks were installed, or "None"] |
| **Test infra** | [Pre-existing: framework name / Installed: framework name / Not installed] |
| **Doc sync** | [N corrections applied / No contradictions found / Skipped] |

[If monorepo: add subproject breakdown rows. If multi-repo: per-repo results and reminder to commit each repo's `.claude/` separately.]
```

After the table, include conditional warnings:

If test infrastructure was installed from scratch in Step 5c (no pre-existing test framework — the user chose "Yes" to install one), include a strong warning:

> ⚠ **Important:** Test framework was installed but the project has no test files yet. The test command will pass with 0 tests — this is a false safety net. Other optimus skills (`/optimus:code-review` deep mode, `/optimus:refactor` deep mode, `/optimus:verify`) rely on tests to validate changes. **Run `/optimus:unit-test` next** to write initial tests and establish real coverage.

If the user declined test infrastructure in Step 5c, include:

> ⚠ **Note:** Test infrastructure was not installed — `/optimus:tdd` will not work, and `/optimus:code-review`, `/optimus:refactor`, and `/optimus:verify` will have reduced functionality. Re-run `/optimus:init` to install test infrastructure later.

**Next step:** If the project's root `README.md` lacks a development setup section (no heading matching the patterns defined in `$CLAUDE_PLUGIN_ROOT/skills/init/references/readme-section-detection.md`), recommend running `/optimus:dev-setup` first to ensure the project has comprehensive human-readable setup instructions, then `/optimus:unit-test` to write tests. Otherwise, recommend `/optimus:unit-test` directly.

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.

End the report with:

> **Setup complete** — your project now has the foundation for effective AI-assisted development. To reach optimal performance, build on this foundation: strengthen test coverage with `/optimus:unit-test` and refine code quality with `/optimus:refactor`.

---
