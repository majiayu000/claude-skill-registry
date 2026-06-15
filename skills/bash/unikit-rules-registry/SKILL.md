---
name: unikit-rules-registry
description: >-
  Orchestrate the external rules registry (create / update / sync). Scaffold a new local registry,
  promote mature rules from .unikit/memory/ into the registry with automatic semver bumps, or pull
  registry updates back into memory. Use when user says "create rules registry", "init rules registry",
  "promote rule to registry", "push memory to registry", "update rules registry", "sync rules registry",
  "publish local rules", "создать реестр правил", "обновить реестр правил", "синхронизировать правила".
  This skill ONLY orchestrates CLI — it NEVER edits .unikit.json or .unikit/memory/ sources.
  All state mutations go through `unikit-ai rules *`.
argument-hint: "[create | update | sync]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
---

# UniKit Rules Registry — External Registry Orchestrator

Manage the external rules registry lifecycle from the project side. This skill owns three modes:

- **create** — scaffold a new local registry repository, seed it with rules currently in `.unikit/memory/`, and optionally switch the project to use it.
- **update** — diff `.unikit/memory/` against the currently configured **local** registry and push changes back (new rules, content updates with automatic semver bumps, stale deletions).
- **sync** — pull registry-side updates into `.unikit/memory/` via `unikit-ai rules sync` (direction: registry → memory).

Direction matters:
- `create` and `update` flow **memory → registry**.
- `sync` flows **registry → memory**.

## Boundaries

**This skill MUST NOT:**
- Write to `.unikit.json` directly via the `Write`/`Edit` tools. All config mutations go through CLI commands: `unikit-ai rules registry set` / `rules registry reset` in create mode, and `unikit-ai rules install ... --force` in update mode (`update.7b`).
- Edit or create files inside `.unikit/memory/` directly via the `Write`/`Edit` tools. Memory sources are authored by `unikit-memory` and `unikit-rules`; this skill may only cause indirect memory writes by delegating to `unikit-ai rules install ... --force` in `update.7b`, which re-fetches registry copies and overwrites memory files as part of the force-install path.
- Parse `config.rulesRegistry` as a string to guess `url` vs `local` — always read `kind` from `unikit-ai rules registry show --json` or `unikit-ai rules status --json`.

**This skill MAY:**
- Run `unikit-ai rules *` CLI commands via `Bash`.
- Mirror the entire `.unikit/memory/<core|stack>/` subtree into the registry — rule files **and** reference files under nested folders like `references/`. The skill owns **writes** to the registry file tree in both create and update modes.
- Delete reference `.md` files under `<registry>/<engine>/<core|stack>/references/` in update mode, and only when the reference-graph check in `update.6b` proves the file is not referenced by any rule (memory or registry). Rule `.md` files in `<registry>/<engine>/<core|stack>/` are **never** deleted by update — rule removal is a manual operation in the registry repository.
- Run `scripts/build-manifest.js` inside the registry repository to regenerate `manifest.json`.
- Compute semver bumps from content diffs and inject or update `version:` in the **registry copy** of rule files via `Edit` after copying (never in memory sources, never in reference files). Files are always copied via `cp` shell command — never via `Read` + `Write`.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

## Step 0: Mode Selector

Read `$ARGUMENTS` and resolve the mode:

```
$ARGUMENTS?
├── "create"  → Mode: create
├── "update"  → Mode: update
├── "sync"    → Mode: sync
└── empty or unrecognized → AskUserQuestion
```

When the mode is missing, ask the user:

```
AskUserQuestion: Which registry operation should run?

Options:
1. Create — scaffold a new local rules registry and seed it from .unikit/memory/
2. Update — push changes from .unikit/memory/ into the currently configured local registry
3. Sync   — pull registry updates back into .unikit/memory/ (memory ← registry)
```

Once the mode is known, read `.unikit/system/cli-contract.md` (if present) to confirm the exact CLI surface and exit codes before dispatching Bash commands. If the file is missing — proceed assuming the documented interface below is correct and surface a `WARN` if any command returns an unexpected exit code.

Then jump to the matching section.

---

## Mode: create

Scaffold a new local registry and seed it with the rules currently installed in `.unikit/memory/`.

### create.1: Ask for target path

```
AskUserQuestion: Where should the new rules registry be created?

Options:
1. Project subfolder — ./rules-registry
2. Custom path — I will ask next (relative or absolute)
3. Cancel
```

- Option 1 → `pathArg = "./rules-registry"`. Pass this verbatim to the CLI in `create.2`. `rulesRegistryInitCommand` in `src/cli/commands/rules.ts` resolves it against `process.cwd()` and auto-creates the target directory via `fs.ensureDir`.
- Option 2 → ask a follow-up `AskUserQuestion` for the path as free-form text input. Trim the input; if the result is empty, re-prompt the same text input. Then compute the absolute path via `path.resolve(<cwd>, <trimmed-input>)` **for display only** and ask a second `AskUserQuestion` of this shape:
  - Question: `Target directory will be: <resolved-absolute-path>. Proceed?`
  - Options: `Yes, proceed` / `No, enter a different path` / `Cancel`
  - Yes → use the original (pre-resolve) input string as `pathArg` in `create.2`.
  - No → loop back to the text-input prompt.
  - Cancel → stop the skill.
- Option 3 → stop the skill.

Do **not** pre-check path existence, expand `~`, normalize the path, or reject relative paths on the skill side. `rulesRegistryInitCommand` is the single authority on path validation: it calls `path.resolve(cwd, pathArg)` itself, auto-creates missing directories via `fs.ensureDir`, and signals problems through exit codes 3 (INVALID_ARGS), 6 (REGISTRY_ALREADY_INITIALIZED), and 7 (PATH_OCCUPIED) — all handled in `create.2` below.

### create.2: Scaffold the registry

Run:

```bash
unikit-ai rules registry init <target-path>
```

Exit-code handling:

| Exit | Meaning | Action |
|------|---------|--------|
| 0 | Scaffold OK | Continue to create.3 |
| 3 | INVALID_ARGS (relative path, etc.) | Report stderr and stop |
| 5 | VALIDATION_FAILED (build-manifest.js failed) | Report stderr and stop |
| 6 | REGISTRY_ALREADY_INITIALIZED | Ask the user: `reuse existing scaffold and continue?` → Yes proceeds to create.3, No stops |
| 7 | PATH_OCCUPIED | Report `target path is not empty and is not a registry`, stop |
| other | Unexpected | Report stderr and stop |

### create.3: Resolve current engine

```bash
unikit-ai rules status --json
```

Parse the JSON and read `.engine`. Never open `.unikit.json` directly — the CLI is the source of truth.

If the CLI exits non-zero (project not initialized), stop the skill with an ERROR referencing `unikit-ai init`.

### create.4: Seed registry with memory rules

For each category in `core`, `stack`:

1. Use `Glob: .unikit/memory/<category>/**/*` to enumerate the **entire subtree** — not just top-level `*.md`. This captures nested folders like `references/` that hold reference files referenced by rule headers (quickrefs, catalogs, indexes).
2. For every file discovered:
   - Compute `relPath` relative to `.unikit/memory/<category>/`.
   - Target path = `<target-path>/<engine>/<category>/<relPath>`.
   - **Classify the file:**
     - **Top-level rule file** (`relPath` contains no `/`, extension `.md`) → copy via shell, then inject version into the **registry copy only** if absent:
       1. `Bash: mkdir -p "$(dirname "<target>")" && cp "<src>" "<target>"`
       2. `Bash: grep -q "^version:" "<target>"` — if exit 1 (not found), use `Edit` to insert `version: 1.0.0` into the frontmatter of `<target>`. The source in `.unikit/memory/` stays untouched.
     - **Reference file** (anything under a subdirectory, or non-`.md` extension) → copy via shell verbatim. Never touch frontmatter — reference files are plain docs and must travel with their parent rule as-is:
       1. `Bash: mkdir -p "$(dirname "<target>")" && cp "<src>" "<target>"`
3. If the category directory yields zero files, continue silently.

Track per-category totals: `rulesCopied` (top-level rule files) and `referencesCopied` (everything else). These feed the final table in `create.7`.

Why recursive: rule files reference reference files via `> **References**:` headers (e.g. `.unikit/memory/stack/references/aspid-mvvm-binders-full.md`). A seed that copies only `*.md` at the top level would publish rules pointing at paths that do not exist in the registry. Mirroring the full tree keeps the references intact.

### create.5: Regenerate registry manifest

```bash
node <target-path>/scripts/build-manifest.js
```

- On non-zero exit: print stderr, stop the skill, and advise the user to inspect the rule files — the most common cause is missing `> **Load when**:` blocks or invalid frontmatter.
- On success: continue.

### create.6: Offer to switch the project registry

The scaffold mirrors `.unikit/memory/` bit-for-bit on disk — content-wise the new registry agrees with memory. But the **state metadata** in `.unikit.json.rules.installed` still points at the old provenance: every rule entry is tagged with its original `source` (`installer` / `registry`) and `origin` (`official` / old primary). Flipping `rulesRegistry` alone does not rewrite those tags, so the project would still look like it is "using the old registry" on the next `rules status --json`.

To make the switch complete, the skill pairs `registry set` with a follow-up `rules sync --replace --prune`. `--replace` bypasses the `source !== 'registry'` guard in `syncRulesState` (see `src/core/installer.ts:1343`) so installer-sourced rules get walked; the sync loop rewrites `source`, `version`, `installed_hash`, and `origin` (via `HybridRegistry.getResolvedOrigin()`) against the new primary registry (`:1409-1412`). `--prune` removes obsolete stack rules that are not in the new manifest. The HARD GUARD at `:1337` still prevents discovery of previously-uninstalled rules — only already-installed entries get reclassified.

```
AskUserQuestion: Switch the current project to this new registry now?

Options:
1. Yes — point .unikit.json at the new registry and reclassify installed rules as primary
2. No — keep the current registry
```

Mapping to CLI commands (order matters — `registry set` must succeed before `sync` runs):

| Choice | Commands |
|--------|----------|
| 1 | `unikit-ai rules registry set <target-path>` then `unikit-ai rules sync --replace --prune` |
| 2 | (skip — do not touch `.unikit.json`) |

Exit-code handling:

- `rules registry set` exit 3 (INVALID_ARGS) or 5 (VALIDATION_FAILED) → report stderr and stop the skill. Do **not** run `rules sync`; the URL has not been written.
- `rules sync --replace --prune` exit 2 (NETWORK — local path disappeared between the two commands) or 5 (VALIDATION_FAILED — registry manifest broken) → report stderr and warn the user that `.unikit.json.rulesRegistry` has already been rewritten to the new path, but rule metadata is still on the old provenance. Instruct them to fix the registry and re-run `unikit-ai rules sync --replace --prune` manually. Do not attempt to roll back `registry set` automatically.
- Both commands exit 0 → continue to `create.7`.

Stream stdout/stderr of both commands to the user so the per-rule event log from `syncRulesState` is visible.

### create.7: Report

Produce a **compact** final report — no prose paragraphs, no step-by-step narrative, no CLI echoes. Just one table of the rules that were transferred, followed by two direction reminders. Anything longer than a dozen lines means you are over-reporting.

Table format:

```
| Category | Rule | Version |
|----------|------|---------|
| core     | folders-structure | 1.0.0 |
| core     | code-style        | 1.0.0 |
| stack    | aspid-mvvm        | 1.0.0 |
| stack    | node-canvas       | 1.0.0 |
```

- One row per top-level rule file copied (the files counted by `rulesCopied`).
- Do not list reference files individually — mention them only as a single trailing line: `+ N reference files under references/` (omit the line if `referencesCopied == 0`).
- Version column shows the version that ended up in the registry copy (either the existing frontmatter value or the injected `1.0.0`).

After the table, print exactly these two reminders (adapt to the configured language):

- `/unikit-rules-registry update` — push later local edits from `.unikit/memory/` into this registry.
- `/unikit-rules-registry sync` — pull registry-side updates back into `.unikit/memory/` (opposite direction).

If the project was switched to the new registry in `create.6`, add exactly two lines after the reminders:

- `✅ rules registry set: <target-path>`
- `✅ rules sync --replace --prune: N rules reclassified as primary`

`N` is the number of rules touched by the sync — count the `phase2:updating` events from the `syncRulesState` event log (every such event flips one rule's `source`/`origin` to the new primary). If the switch was declined, add nothing.

---

## Mode: update

Push changes from `.unikit/memory/` into the currently configured **local** registry and regenerate its manifest.

### update.1: Verify registry kind

```bash
unikit-ai rules registry show --json
```

Parse JSON fields `configured`, `url`, `kind`.

- `kind` is not `"local"` → ERROR: `update requires a local registry — run /unikit-rules-registry create first`. Stop.
- `configured` is `false` → ERROR: `no registry configured`. Stop.
- Otherwise: `registryPath = <url>`.

### update.2: Resolve engine

```bash
unikit-ai rules status --json
```

Read `.engine`. Abort on non-zero exit.

### update.3: Diff memory vs registry

For each category in `core`, `stack`:

1. `Glob: .unikit/memory/<category>/**/*` — walk the full subtree so reference files under `references/` (and any other nested folders) are diffed alongside their parent rules.
2. For every file `src` found in memory, compute `relPath` relative to `.unikit/memory/<category>/` and classify it:
   - **Rule file** if `relPath` has no `/` and ends with `.md` (top-level markdown).
   - **Reference file** otherwise (nested file, or non-`.md`). Reference files carry no `version:` frontmatter — they travel with their parent rule as plain content.
3. For every `src`:
   - target = `<registryPath>/<engine>/<category>/<relPath>`
   - If target does not exist → mark as **add**.
   - Else run `Bash: diff -q --strip-trailing-cr "<src>" "<target>"`:
     - exit 0 → identical, **skip**.
     - exit 1 → differs, continue to bump classification (rule files only) or mark as **reference-update** (reference files).
     - other exit → report and stop.
4. Walk the registry side the same way: `Glob: <registryPath>/<engine>/<category>/**/*`. Any file present in the registry but not in memory becomes a **delete** candidate (handled in update.5). Tag each orphan as rule vs reference file so the prompt can display them in two groups.

**Why recursive:** rule files reference reference files via `> **References**:` headers. If `update` diffs only top-level `*.md`, edits to reference docs (quickrefs, full catalogs) silently stay behind and the registry drifts out of sync with the project's actual knowledge base. Walking the subtree is the simplest way to guarantee every referenced file reaches the registry.

### update.4: Classify bumps for `differs` rule files

Reference files (`reference-update` from update.3) have no frontmatter version to bump — skip this step for them and handle them directly in update.6.

For every `differs` **rule file**, run `Bash: diff -u --strip-trailing-cr "<src>" "<target>"`. Parse the output:

- `added = number of lines starting with "+" excluding the "+++" header`
- `removed = number of lines starting with "-" excluding the "---" header`
- `oldTotal = wc -l of <target>` (used for the `removed > 30% oldTotal` rule)

Apply the heuristic **in order** — the first matching row wins:

| Condition | Bump |
|-----------|------|
| `removed > 0.3 * oldTotal` | **major** |
| `removed == 0` AND `added <= 5` | **patch** |
| `removed == 0` AND `added > 5` | **minor** |
| `removed <= 3` AND `added <= 10` | **patch** |
| `removed > 3` AND `added > removed` | **minor** |
| otherwise | **patch** |

Compute the new version:

- Read the current `version:` from the target file's frontmatter (if missing, assume `1.0.0`).
- Apply the bump:
  - `patch` → `x.y.(z+1)`
  - `minor` → `x.(y+1).0`
  - `major` → `(x+1).0.0`
- This heuristic is fully automatic — do **not** ask the user to approve each bump.

### update.5: Collect orphan rule files (informational)

Update is **strictly push-only** for rule files — it never removes them from the registry. For every rule `.md` file present in the registry and missing from memory (i.e. top-level `*.md` under `<registryPath>/<engine>/<category>/` with no counterpart in `.unikit/memory/<category>/`), append `{ category, filename }` to an `orphanRuleFiles` list. That list is consumed purely by `update.8` as a WARN block — no prompt, no delete, no cascade.

Do **not** walk reference files under `references/` here. Reference file reconciliation is a separate concern handled in `update.6b` via the real `rule → references` graph; orphan detection at the file level would miss shared reference files and produce false positives.

If `orphanRuleFiles` is empty after the walk, the WARN block is skipped entirely in `update.8`.

### update.6: Apply changes

For each **rule file** `add`:
- Copy via shell, then inject version into the **registry copy only** if absent:
  1. `Bash: cp "<src>" "<target>"`
  2. `Bash: grep -q "^version:" "<target>"` — if exit 1 (not found), use `Edit` to insert `version: 1.0.0` into the frontmatter of `<target>`. The source in `.unikit/memory/` stays untouched.

For each **rule file** `differs`:
- Copy via shell, then replace the version in the **registry copy**:
  1. `Bash: cp "<src>" "<target>"`
  2. Use `Edit` to replace the `version:` line in `<target>` with the bumped version from update.4 (insert if absent). The source in `.unikit/memory/` stays untouched.

For each **reference file** `add` or `reference-update`:
- Copy via shell verbatim. Do not inject or alter any frontmatter — reference files are plain docs and must reach the registry byte-identical to the memory source (modulo the path):
  1. `Bash: mkdir -p "$(dirname "<target>")" && cp "<src>" "<target>"`

Track `touchedRuleFiles = [...]` — every rule file classified as `add` or `differs` in this step, stored as `{ category, ruleId }` (ruleId = filename without `.md`). This list is consumed by `update.7b` to drive the post-write `rules install --force` batch. Reference files are **not** tracked — `installOneRule` re-fetches a parent rule's declared references automatically during force install.

There is **no `delete` branch** in this step — update never removes rule files from the registry (see `## Boundaries`). Companion deletions happen separately in `update.6b` via the reference-graph check; that step runs after all writes here so it sees the final set of registry files.

All writes happen inside the registry tree only — never touch memory sources.

### update.6b: Reference file cleanup (reference-graph based)

Reconcile reference files in the registry against the real `rule → references` graph. Remove any reference `.md` under `<registryPath>/<engine>/<category>/references/` that no rule (in memory or in the registry) references anymore. The algorithm covers four scenarios:

| Scenario | `referencedByAnyone`? | Action |
|----------|----------------------|--------|
| Parent rule dropped a ref, nobody else holds it | No | Delete |
| Shared — another memory rule still references it | Yes | Keep (protected) |
| Orphan parent rule in registry still references it | Yes | Keep (protected) |
| Zombie — no rule references it anywhere | No | Delete |

Run the algorithm **per category** — `core` and `stack` are independent namespaces and never share reference filenames across the divide.

For each category in `core`, `stack`:

1. Initialise `referencedByAnyone` as an empty `Set<string>` of reference filenames.
2. Walk `<registryPath>/<engine>/<category>/*.md` (top-level rule files only — do not recurse into `references/` here). For every rule file found:
   - Let `ruleId = basename without .md`.
   - If `.unikit/memory/<category>/<ruleId>.md` exists → `parseTarget = memory` (memory wins for rules present in both).
   - Else → `parseTarget = registry` (orphan parent rule — protect its own references using the on-disk registry header).
   - Read the chosen file, locate the `> **References**:` header line, and extract every reference filename with the regex `references\/([^\s,)]+\.md)/g`. This is the exact regex used by `rules-registry/scripts/build-manifest.js:43-49` — stay byte-for-byte aligned so `update.6b` and the manifest rebuild in `update.7` never disagree about what is referenced.
   - Add every extracted filename to `referencedByAnyone`.
3. Enumerate physical reference files: `Glob: <registryPath>/<engine>/<category>/references/*.md` → `physical` (set of filenames only, strip paths).
4. Compute `safeToDelete = physical \ referencedByAnyone` (set difference by filename).
5. For every filename in `safeToDelete`:
   - `Bash: rm "<registryPath>/<engine>/<category>/references/<filename>"` (single-file delete, never recursive, never glob).
   - Append `{ category, filename }` to a top-level `deletedReferences` list consumed by `update.8`.

Documented edge cases (**not** special-cased — the algorithm handles them naturally):

- **Memory rule without a `> **References**:` header.** The regex returns an empty set for that rule. If nobody else references its former reference files, they become part of `safeToDelete`. This is the user's explicit intent — removing the header is the signal.
- **Header contains a dangling filename** (names a file that does not physically exist). The filename still joins `referencedByAnyone`, so the delete check stays consistent with manifest generation. Nothing is fabricated — this step only deletes.
- **Two rules in the same category with identical references** — the set union on `referencedByAnyone` handles this: a shared file is recorded once and protected by both rules.

This step runs **before** `update.7` — the manifest rebuild must see the final physical layout of `references/`, otherwise it would list reference filenames that no longer exist on disk.

### update.7: Regenerate registry manifest

```bash
node <registryPath>/scripts/build-manifest.js
```

On non-zero exit: print stderr, stop the skill. The most common cause is a rule missing `> **Load when**:` or invalid frontmatter; the user must fix the rule source in `.unikit/memory/` (via `/unikit-memory`) before re-running `/unikit-rules-registry update`.

### update.7b: Reconcile project state after registry bumps

`update.6` wrote new and bumped rule files into the registry, but `.unikit.json.rules.installed[...]` still points at the pre-update `version` and `installed_hash` for every touched rule. Without reconciliation:

- `unikit-ai rules status` will lie about installed versions.
- The next `unikit-ai rules sync` (Safe mode) will mark disk files as `locally-modified` and **skip** the version update (`src/core/installer.ts:1382-1396`), so the drift never heals on its own.

Force-install every touched rule in a single variadic CLI call. Reference files are **not** listed — `installOneRule` re-fetches a parent rule's declared references automatically during force install (see `src/cli/commands/rules.ts:379-385`).

1. Collect `installTargets = [ruleId for each entry in touchedRuleFiles]`, deduplicated. Read the list tracked in `update.6`.
2. If `installTargets` is empty → **skip this step entirely**. No rule file changed in this run, so there is nothing to reconcile.
3. Otherwise run one variadic invocation:

   ```bash
   unikit-ai rules install <id1> <id2> ... --force
   ```

   Stream stdout/stderr to the user so the per-rule report (`✓ installed …`, `↻ already installed …`, `✗ failed …`) surfaces as events occur.

4. Exit-code handling:

   | Exit | Meaning | Action |
   |------|---------|--------|
   | 0 | At least one rule installed (aggregated report may still contain `failed` rows) | Parse the report, forward any failures into `update.8` as a WARN block, continue |
   | 2 | NETWORK — registry chain unreachable | Report stderr and stop the skill |
   | 4 | NOT_FOUND — every rule failed | Capture the aggregated report, continue to `update.8` and surface as a WARN block; **do not** roll back `update.6` writes |
   | 5 | VALIDATION_FAILED — registry manifest broken | Report stderr and stop the skill |
   | other | Unexpected | Report stderr and stop the skill |

   Do **not** attempt to roll back the writes `update.6` already made to the registry. The registry-side update has already succeeded; partial install failures are recoverable by re-running `unikit-ai rules install <id> --force` manually against specific ids once the root cause is fixed.

`installOneRule` with `force=true` covers all three state branches deterministically (see `src/cli/commands/rules.ts:340-469`):

- **Existing entry with `source: registry` and stale version** → in-place update of `source`, `version`, `installed_hash`, `origin`.
- **Existing entry with `source: local`** → transition to `source: registry, version: <from registry>` (first-time publication path). This is how a rule that was previously authored locally and just pushed to the registry in this run becomes "owned" by the registry in `.unikit.json`.
- **No existing entry** → push a new entry with `source: registry, version: <from registry>`.

A free bonus: `rulesInstallCommand` always regenerates `RULES_INDEX.md` at the end of its invocation (`src/cli/commands/rules.ts:566`), so the skill does not need a separate index refresh after this step.

### update.8: Report

Produce a **compact** final report — same style as `create.7`. No prose paragraphs, no step-by-step narrative, no CLI echoes. One table of rule changes, optional tallies, optional WARN blocks, one direction reminder. Anything longer than a dozen lines (plus WARN blocks, which can grow if the situation warrants) means you are over-reporting.

Table format:

```
| Action | Category | Rule | Version |
|--------|----------|------|---------|
| add    | stack    | aspid-mvvm  | 1.0.0          |
| update | stack    | node-canvas | 1.2.0 → 1.3.0  |
| skip   | core     | code-style  | 1.1.0          |
```

- One row per top-level rule file touched. Rows are grouped by action in the order: `add`, `update`, `skip`. Omit the `skip` rows entirely if every unchanged rule would otherwise bloat the table — keep them only when useful for verification.
- There is **no `delete` row for rule files** — update is strictly push-only for `.md` rule files (see `## Boundaries`). A rule that only exists in the registry surfaces in the orphan WARN block below, never as a table row.
- `Version` column: for `add` and `skip` shows the current registry version; for `update` shows `old → new`.
- Do not list reference files in the main table. Add a single trailing line directly under the table: `+ N reference files: X added · Y updated · Z deleted · W unchanged` (omit the line if all four counts are zero). `Z` comes from the `deletedReferences` list populated in `update.6b`.
- If `Z > 0`, print a separate deletion table directly under the tally line:

  ```
  | Action | Category | File                         |
  |--------|----------|------------------------------|
  | delete | stack    | aspid-mvvm-binders-full.md   |
  | delete | core     | old-reference.md             |
  ```

  Rows come from `deletedReferences`, sorted by `category` then `filename`. Do not inline the list on one line — the table is both the primary signal and the full record.

If `update.5` collected any entries into `orphanRuleFiles`, print one WARN block before the final two lines. Skip the block entirely when the list is empty:

```
⚠️ WARN: registry contains orphan rule files not mirrored in .unikit/memory/:
  - stack/legacy-rule.md
  - core/retired-guidelines.md
update is push-only; rule deletion must be done in the registry repo directly
(rm + scripts/build-manifest.js + commit).
```

If `update.7b` surfaced any `failed` rows in the `rules install --force` report (either partial failures on exit 0 or total failure on exit 4), print a second WARN block directly after the orphan block:

```
⚠️ WARN: state reconcile partially failed — the registry was updated but these rules
stayed on their pre-update versions in .unikit.json:
  - stack/aspid-mvvm — <reason from the install report>
Re-run `unikit-ai rules install <id>... --force` manually after fixing the cause.
```

After the table, the reference files tally, and any WARN blocks, print exactly these two lines (adapt to the configured language):

- `✅ manifest: ok` or `❌ manifest: failed — <one-line reason>`
- `/unikit-rules-registry sync` — pull registry-side updates back into `.unikit/memory/` (opposite direction of this run).

---

## Mode: sync

Pull registry-side updates back into `.unikit/memory/` by delegating to `unikit-ai rules sync`. Direction is registry → memory (the opposite of `update`).

### sync.1: Ask about the sync intensity

The CLI exposes two composable flags that used to live behind the single `--force`:

- `--replace` — overwrite rules already in state (same-version refresh AND local modifications).
- `--prune` — remove obsolete stack rules that vanished from the manifest.

The question below maps each user choice to a concrete flag combination.

```
AskUserQuestion: How should the sync run?

Options:
1. Safe — update rules already marked source: registry whose version changed (no rewrite of local modifications, no prune)
2. Replace — also overwrite rules that are up-to-date but locally modified (no prune)
3. Mirror — full parity with the registry: replace AND prune obsolete stack rules (equivalent to the legacy `--force`)
```

### sync.2: Run the CLI

| Choice | Command |
|--------|---------|
| Safe    | `unikit-ai rules sync` |
| Replace | `unikit-ai rules sync --replace` |
| Mirror  | `unikit-ai rules sync --replace --prune` |

Stream stdout/stderr to the user so the per-rule event log from `syncRulesState` is visible.

Handle exit codes:

- 0 → success, continue to sync.3.
- 2 → registry unreachable, report stderr, stop.
- 5 → registry validation failed, report stderr, stop.
- other non-zero → report and stop.

### sync.3: Report

Produce a **compact** final report — same style as `create.7` and `update.8`. No prose paragraphs, no CLI echoes. Parse the per-rule event log from `syncRulesState` into a single table of what happened in memory, followed by one direction reminder.

Table format:

```
| Action | Category | Rule | Version |
|--------|----------|------|---------|
| add    | stack    | aspid-mvvm  | 1.0.0          |
| update | stack    | node-canvas | 1.2.0 → 1.3.0  |
| delete | stack    | odin        | —              |
```

- One row per rule touched in `.unikit/memory/`. Group by action in the order: `add`, `update`, `delete`. Do not include `skip` rows — on sync they are noise.
- `Version` column: for `add` shows the installed version; for `update` shows `old → new`; for `delete` shows `—`.
- If the registry ships reference files under `references/`, add a single trailing line: `+ N reference files refreshed` (omit if zero).
- If `RULES_INDEX.md` was regenerated, print one line: `✅ RULES_INDEX.md: regenerated`.

After the table, print exactly one reminder (adapt to the configured language):

- `/unikit-rules-registry update` — push local edits from `.unikit/memory/` back into the registry (opposite direction of this run).

---

## Access Rules

**Writable** (this skill may create and edit these, strictly inside the registry target path):
- `<registry-path>/<engine>/core/**` — rule files and any nested reference files
- `<registry-path>/<engine>/stack/**` — rule files and any nested reference files (e.g. `references/*.md`)
- `<registry-path>/manifest.json` (only as a side effect of running `build-manifest.js`)

**Deletable** (update mode only, under the conditions below):
- `<registry-path>/<engine>/<core|stack>/references/*.md` — reference files. Only when the reference-graph check in `update.6b` proves the file is not referenced by any rule in memory or in the registry (shared-reference protection).
- Rule `.md` files in `<registry-path>/<engine>/<core|stack>/` are **never** deleted by update — rule removal is a manual operation in the registry repository.

**Read-only** (this skill MUST NEVER modify these files directly via Write/Edit):
- `.unikit/memory/**` — owned by `unikit-memory`. Mutated only indirectly when `unikit-ai rules install --force` re-fetches registry copies in `update.7b`.
- `.unikit.json` — mutated only via `unikit-ai rules registry set` / `unikit-ai rules registry reset` / `unikit-ai rules install --force`.
- `.unikit/system/cli-contract.md` — regenerated by the build pipeline
- `.unikit/config.yaml` — project settings

Each mode ends at its own per-mode report (`create.7`, `update.8`, `sync.3`). Do not add a second summary on top of them, and never auto-invoke another skill.
