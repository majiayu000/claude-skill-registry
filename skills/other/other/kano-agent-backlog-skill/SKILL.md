---
name: kano-agent-backlog-skill
description: Local-first backlog workflow. Use when planning work, creating/updating backlog items, writing ADRs, enforcing Ready gate, generating views, or maintaining derived indexes (SQLite/FTS/embeddings).
metadata:
  short-description: Local backlog system
  version: pre-alpha
  stability: experimental

---

# Kano Agent Backlog Skill (local-first)

## Pre-alpha Status

**This skill is in pre-alpha (experimental) stage:**
- Breaking changes are expected and frequent
- No backward compatibility guarantees
- CLI commands, config schema, and file formats may change without notice
- When implementing new features or refactoring, **do not add backward compatibility layers**
- Simply replace old implementations with new ones
- Update documentation to reflect current state only

**For agents:** When you see deprecated patterns or inconsistent interfaces, refactor them directly. Do not preserve old code paths "for compatibility."

## Scope

Use this skill to:
- Plan new work by creating backlog items before code changes.
- Maintain hierarchy and relationships via `parent` links, as defined by the active process profile.
- Record decisions with ADRs and link them to items.
- Keep a durable, append-only worklog for project evolution.

## Agent compatibility: read the whole skill

- Always load the entire `SKILL.md` before acting; some agent shells only fetch the first ~100 lines by default.
- If your client truncates, fetch in chunks (e.g., lines 1-200, 200-400, …) until you see the footer marker `END_OF_SKILL_SENTINEL`.
- If you cannot confirm the footer marker, stop and ask for help; do not proceed with partial rules.
- When generating per-agent guides, preserve this read-all requirement so downstream agents stay in sync.

## Quick Start for Agents

**If you're helping a user set up this skill from a cloned repository:**

1. **Install in development mode:**
   ```bash
   cd skills/kano-agent-backlog-skill
   pip install -e ".[dev]"
   ```

2. **Verify installation:**
   ```bash
   kano-backlog --version
   kano-backlog doctor
   ```

3. **Initialize backlog:**
   ```bash
   cd /path/to/user/project
   kano-backlog admin init --product <product-name> --agent <your-agent-id>
   ```

**See [docs/agent-quick-start.md](docs/agent-quick-start.md) for complete setup instructions.**

## Non-negotiables

- Planning before coding: create/update items and meet the Ready gate before making code changes.
- Worklog is append-only; never rewrite history.
- Update Worklog whenever:
  - a discussion produces a clear decision or direction,
  - an item state changes,
  - scope/approach changes,
  - or an ADR is created/linked.
- Archive by view: hide `Done`/`Dropped` items in views by default; do not move files unless explicitly requested.
- Backlog volume control:
  - Only create items for work that changes code or design decisions.
  - Avoid new items for exploratory discussion; record in existing Worklog instead.
  - Keep Tasks/Bugs sized for a single focused session.
  - Avoid ADRs unless a real architectural trade-off is made.
- Ticketing threshold (agent-decided):
  - Open a new Task/Bug when you will change code/docs/views/scripts.
  - Open an ADR (and link it) when a real trade-off or direction change is decided.
  - Otherwise, record the discussion in an existing Worklog; ask if unsure.
- Ticket type selection (keep it lightweight):
  - Epic: multi-release or multi-team milestone spanning multiple Features.
  - Feature: a new capability that delivers multiple UserStories.
  - UserStory: a single user-facing outcome that requires multiple Tasks.
  - Task: a single focused implementation or doc change (typically one session).
  - Example: "End-to-end embedding pipeline" = Epic; "Pluggable vector backend" = Feature; "MVP chunking pipeline" = UserStory; "Implement tokenizer adapter" = Task.
- Bug vs Task triage (when fixing behavior):
  - If you are correcting a behavior that was previously marked `Done` and the behavior violates the original intent/acceptance (defect or regression), open a **Bug** and link it to the original item.
  - If the change is a new requirement/scope change beyond the original acceptance, open a **Task/UserStory** (or Feature) instead, and link it for traceability.
- Bug origin tracing (when diagnosing a defect/regression):
  - Record **when the issue started** and the **evidence path** you used to determine it.
  - Prefer VCS-backed evidence when available:
    - last-known-good revision (commit hash or tag)
    - first-known-bad revision (commit hash or tag)
    - suspected introducing change(s) (commit hash) and why (e.g., `git blame` on specific lines)
  - If git history is unavailable (zip export, shallow clone, missing remote), explicitly record that limitation and what alternative evidence you used (e.g., release notes, timestamps, reproduction reports).
  - Keep evidence lightweight: record commit hashes + 1–2 line summaries; avoid pasting large diffs into Worklog. Attach artifacts when needed.
  - Suggested Worklog template:
    - `Bug origin: last_good=<sha|tag>, first_bad=<sha|tag>, suspect=<sha> (reason: blame <path>:<line>), evidence=<git log/blame/bisect|other>`
- State ownership: the agent decides when to move items to InProgress or Done; humans observe and can add context.
- State semantics:
  - Proposed: needs discovery/confirmation.
  - Planned: approved but not started.
  - Ready gate applies before InProgress: Context, Goal, Approach, Acceptance Criteria, Risks must be filled.
  - InProgress: active work; strict Ready gate enforcement unless `--force` is used.
- Hierarchy is in frontmatter links, not folder nesting; avoid moving files to reflect scope changes.
- Filenames stay stable; use ASCII slugs.
- Never include secrets in backlog files or logs.
- Language: backlog and documentation content must be English-only (no CJK), to keep parsing and cross-agent collaboration deterministic.
- Agent Identity: In Worklog and audit logs, use your own identity (e.g., `[agent=antigravity]`), never copy `[agent=codex]` blindly.
- Always provide an explicit `--agent` value for auditability (some commands currently default to `cli`, but do not rely on it).
- Model attribution (optional but preferred): provide `--model <name>` (or env `KANO_AGENT_MODEL` / `KANO_MODEL`) when it is known deterministically.
  - Do not guess model names; if unknown, omit the `[model=...]` segment.
- **Agent Identity Protocol**: Supply `--agent <ID>` with your real product name (e.g., `cursor`, `copilot`, `windsurf`, `antigravity`).
  - **Forbidden (Placeholders)**: `auto`, `user`, `assistant`, `<AGENT_NAME>`, `$AGENT_NAME`.
- File operations for backlog/skill artifacts must go through the `kano-backlog` CLI
  (`python skills/kano-agent-backlog-skill/scripts/kano-backlog <command>`) so audit logs capture the action.
- Skill scripts only operate on paths under `_kano/backlog/` or `_kano/backlog_sandbox/`;
  refuse other paths.
- After modifying backlog items, refresh the plain Markdown views immediately using
  `python skills/kano-agent-backlog-skill/scripts/kano-backlog view refresh --agent <agent-id> --backlog-root <path>` so the dashboards stay current.
  - Persona summaries/reports are available via `python skills/kano-agent-backlog-skill/scripts/kano-backlog admin persona summary|report ...`.
- `python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem update-state ...` auto-syncs parent states forward-only by default; use `--no-sync-parent`
  for manual re-plans where parent state should stay put.
- Add Obsidian `[[wikilink]]` references in the body (e.g., a `## Links` section) so Graph/backlinks work; frontmatter alone does not create graph edges.
- Artifacts storage: Demo reports, implementation summaries, analysis documents, and other work outputs should be stored in `artifacts/<item-id>/` for the corresponding work item to maintain traceability and context.

## Agent compatibility: read the whole skill

- Always load the entire `SKILL.md` before acting; some agent shells only fetch the first ~100 lines by default.
- If your client truncates, fetch in chunks (e.g., lines 1-200, 200-400, …) until you see the footer marker `END_OF_SKILL_SENTINEL`.
- If you cannot confirm the footer marker, stop and ask for help; do not proceed with partial rules.
- When generating per-agent guides, preserve this read-all requirement so downstream agents stay in sync.

## First-run bootstrap (prereqs + initialization)

Before using this skill in a repo, the agent must confirm:
1) Python prerequisites are available (or install them), and
2) the backlog scaffold exists for the target product/root.

If the backlog structure is missing, propose the bootstrap commands and wait for user approval before writing files.

### Developer vs user mode (where to declare it)

- **Preferred source of truth**: project config in `.kano/backlog_config.toml`.
  - `[defaults]` applies to all products.
  - `[shared.*]` applies to all products (global defaults).
  - `[products.<name>]` defines each product and its product-specific settings (flattened keys like `vector_enabled`, `analysis_llm_enabled`, `embedding_provider`, etc.).
- **Secondary**: agent guide files (e.g., `AGENTS.md` / `CLAUDE.md`) can document expectations, but are agent-specific and not script-readable.

### Skill developer gate (architecture compliance)

**If `mode.skill_developer=true`**, before writing any skill code (in `scripts/` or `src/`), you **must**:
1. Read **ADR-0013** ("Codebase Architecture and Module Boundaries") in the product decisions folder.
2. Follow the folder rules defined in ADR-0013:
   - `scripts/` is **executable-only**: no reusable module code.
   - `src/` is **import-only**: core logic lives here, never executed directly.
   - All agent-callable operations go through `scripts/kano-backlog` CLI.
3. Place new code in the correct package:
   - Models/config/errors → `src/kano_backlog_core/`
   - Use-cases (create/update/view) → `src/kano_backlog_ops/`
   - Storage backends → `src/kano_backlog_adapters/`
   - CLI commands → `src/kano_backlog_cli/commands/`

Violating these boundaries will be flagged in code review.

### Prerequisite install (Python)

Detect:
- Run `python skills/kano-agent-backlog-skill/scripts/kano-backlog doctor --format plain`.

If packages are missing, install once (recommended):
- **Default**: `python -m pip install -e skills/kano-agent-backlog-skill`
- **Skill contributors**: `python -m pip install -e skills/kano-agent-backlog-skill[dev]`
- Optional heavy dependencies (FAISS, sentence-transformers) should be installed manually per platform requirements before running the CLI against embedding features.

### Container/Docker environments (agents)

If you run inside a restricted container (no `pip`, no build tools), `admin init` will fail because
the CLI cannot install its Python dependencies. In that case, use a prebuilt image or rebuild the
image with Python + pip available.

**Minimum requirements in the container**:
- Python 3.11+
- `pip` (or an equivalent package manager)
- Ability to install the skill dependencies

**Recommended flow (container)**:
```bash
python -m venv .venv
./.venv/Scripts/python -m pip install -e skills/kano-agent-backlog-skill
./.venv/Scripts/python skills/kano-agent-backlog-skill/scripts/kano-backlog admin init --product <product> --agent <agent-id>
```

If your container cannot install packages (no pip / no build tools), do **not** run the CLI there.
Instead, run the CLI in a proper Python environment and mount the generated `_kano/backlog` and
`.kano/backlog_config.toml` into the container.

**Say this to your agent**:
"I'm in a container without pip. Please run `kano-backlog admin init` in a Python environment that has pip, then copy/mount `_kano/backlog` and `.kano/backlog_config.toml` into the container. If pip is available, install the skill in a venv and run `admin init` inside the container."

### Backlog initialization (file scaffold + config + dashboards)

Detect (multi-product / platform layout):
- Product is initialized if:
  - `.kano/backlog_config.toml` exists, and
  - `[products.<product>]` is present with a valid `backlog_root` pointing at an existing directory.

Bootstrap:
- Run `kano-backlog admin init --product <product> --agent <agent-id> [--backlog-root <path>]` to scaffold backlog directories and write/update `.kano/backlog_config.toml`.
- Manual fallback (only if automation is unavailable): follow `_kano/backlog/README.md` to copy the template scaffold, then refresh views via `kano-backlog view refresh`.

## Optional LLM analysis over deterministic reports

This skill can optionally append an LLM-generated analysis to a deterministic report.
The deterministic report is the SSOT; analysis is treated as a derived artifact.

- Deterministic report: `views/Report_<persona>.md`
- Derived LLM output: `views/_analysis/Report_<persona>_LLM.md` (gitignored by default)
- Deterministic prompt artifact: `views/_analysis/Report_<persona>_analysis_prompt.md`

Enable by config (per product):
- `analysis.llm.enabled = true`

Execution:
- The **default workflow** is: generate the deterministic report → use it as SSOT → fill in the analysis template.
  - The skill generates a deterministic prompt file to guide the analysis, and a derived markdown file with placeholder headings.
- Optional automation: when `analysis.llm.enabled = true` in config, view refresh generates `views/snapshots/_analysis/Report_<persona>_analysis_prompt.md` (deterministic prompt) and `Report_<persona>_LLM.md` (template or LLM output)
- Never pass API keys as CLI args; keep secrets in env vars to avoid leaking into audit logs.

## ID prefix derivation

- Source of truth:
  - Product config: `_kano/backlog/products/<product>/_config/config.toml` (`product.name`, `product.prefix`), or
  - Repo config (single-product): `_kano/backlog/_config/config.toml` (`product.name`, `product.prefix`).
- Derivation:
  - Split `product.name` on non-alphanumeric separators and camel-case boundaries.
  - Take the first letter of each segment.
  - If only one letter, take the first letter plus the next consonant (A/E/I/O/U skipped).
  - If still short, use the first two letters.
  - Uppercase the result.
- Example: `product.name=kano-agent-backlog-skill-demo` -> `KABSD`.

## ID allocation and sequence management

### Understanding IDs vs UIDs

The backlog system uses two types of identifiers:

- **UID (UUID)**: The true unique identifier for each work item (e.g., `019c11e6-de87-7218-b89b-38c2e4e9cabd`).
  - Immutable - never changes throughout the item's lifecycle.
  - Guaranteed unique - no collisions possible.
  - Used internally by the system for all operations.
  - Stored in frontmatter: `uid: 019c11e6-de87-7218-b89b-38c2e4e9cabd`

- **Display ID**: Human-readable identifier (e.g., `KABSD-TSK-0335`).
  - Derived from DB sequence counter (auto-incremented).
  - Used in filenames and for human reference.
  - May have collisions if DB sequence is stale.
  - Format: `<PREFIX>-<TYPE>-<NUMBER>` (e.g., `KABSD-TSK-0335`)

**System behavior**: All CLI operations accept both UID and Display ID. When ambiguous (multiple items with same Display ID), the system requires UID.

### ID allocation mechanism

IDs are allocated from a SQLite database sequence to prevent collisions:

1. **DB Sequence**: Tracks the next available ID for each type (EPIC, FTR, USR, TSK, BUG).
2. **Auto-increment**: `item create` queries the DB for the next available ID.
3. **File-first**: Markdown files are the source of truth; the DB is a derived index that must be kept in sync.

### Sequence synchronization workflow

The DB sequence must be synchronized with the filesystem after certain operations.

**When to sync** (run `admin sync-sequences`):
- After cloning the repository (DB doesn't exist yet).
- After pulling changes that add/remove items (DB is out of sync).
- Before bulk item creation (ensure no collisions).
- When seeing "Ambiguous item reference" errors (multiple items with same Display ID).
- After manually creating/deleting item files outside the CLI.

**How to sync**:

```bash
# Preview changes (dry run)
python skills/kano-agent-backlog-skill/scripts/kano-backlog admin sync-sequences --product <product> --dry-run

# Apply synchronization
python skills/kano-agent-backlog-skill/scripts/kano-backlog admin sync-sequences --product <product>
```

Output example:
```
Updated sequences:
  EPIC: 15
  FTR: 64
  USR: 44
  TSK: 336
  BUG: 10
```

### Correct workflow for creating items

**Always follow this order**:

```bash
# Step 1: Sync sequences (if not done recently)
python skills/kano-agent-backlog-skill/scripts/kano-backlog admin sync-sequences --product <product>

# Step 2: Create item (system auto-assigns next available ID)
python skills/kano-agent-backlog-skill/scripts/kano-backlog item create \
  --type task \
  --title "Your task title" \
  --agent <agent-id> \
  --product <product>

# Output: OK: Created: KABSD-TSK-0336
#         Path: KABSD-TSK-0336_your-task-title.md
```

The system automatically:
- Queries the DB for the next sequence number.
- Allocates the Display ID (e.g., `KABSD-TSK-0336`).
- Generates a unique UID (UUID v7).
- Creates the file with both identifiers.

### Handling ID conflicts

If you encounter "Ambiguous item reference" errors (multiple items with same Display ID):

**Option 1: Use UID instead of Display ID**
```bash
# Reference by UID (always unambiguous)
python skills/kano-agent-backlog-skill/scripts/kano-backlog item update-state \
  019c11e6-de87-7218-b89b-38c2e4e9cabd \
  --state Done \
  --agent <agent-id> \
  --product <product>
```

**Option 2: Trash the incorrect item**
```bash
# Move incorrect item to _trash/ (recoverable)
python skills/kano-agent-backlog-skill/scripts/kano-backlog admin items trash \
  <UID> \
  --agent <agent-id> \
  --reason "ID conflict - incorrect duplicate" \
  --product <product> \
  --apply
```

**Option 3: Find which items have the same ID**
```bash
# Identify duplicates
find _kano/backlog/products/<product>/items -name "KABSD-TSK-0001*.md"
```

### Best practices

**DO**:
- ✅ Run `sync-sequences` after cloning or pulling changes.
- ✅ Let the system allocate IDs automatically (never manually assign).
- ✅ Use UID when scripting or in ambiguous situations.
- ✅ Use the `trash` command instead of deleting files directly.
- ✅ Check `admin validate uids` periodically to detect UID collisions.

**DON'T**:
- ❌ Manually assign Display IDs in frontmatter.
- ❌ Delete item files directly (use `admin items trash`).
- ❌ Assume Display ID is unique (always be prepared to use UID).
- ❌ Skip `sync-sequences` after repository operations.
- ❌ Create items without running `sync-sequences` first (if DB might be stale).

### Conflict resolution policy

The system provides configurable conflict handling via product config:

```toml
# _kano/backlog/products/<product>/_config/config.toml
[conflict_policy]
id_conflict = "rename"           # Rename duplicate Display IDs
uid_conflict = "trash_shorter"   # Move shorter duplicate to _trash/
```

See `admin links normalize-ids` and `admin validate uids` commands for conflict detection and resolution.

## Recommended layout

This skill supports both single-product and multi-product layouts:

- Single-product (repo-level): `_kano/backlog/`
- Multi-product (monorepo): `_kano/backlog/products/<product>/`

Within each backlog root:
- `_meta/` (schema, conventions)
- `items/<type>/<bucket>/` (work items)
- `decisions/` (ADR files)
- `views/` (dashboards / generated Markdown)

## Item bucket folders (per 100)

- Store items under `_kano/backlog/items/<type>/<bucket>/`.
- Bucket names use 4 digits for the lower bound of each 100 range.
  - Example: `0000`, `0100`, `0200`, `0300`, ...
- Example path:
  - `_kano/backlog/items/task/0000/KABSD-TSK-0007_define-secret-provider-validation.md`

## Index/MOC files

- For Epic, create an adjacent index file:
  - `<ID>_<slug>.index.md`
- Index files should render a tree using Dataview/DataviewJS and rely on `parent` links.
- Track epic index files in `_kano/backlog/_meta/indexes.md` (type, item_id, index_file, updated, notes).

## References

- Reference index: `REFERENCE.md`
- Schema and rules: `references/schema.md`
- Templates: `references/templates.md`
- Workflow SOP: `references/workflow.md`
- View patterns: `references/views.md`
- Obsidian Bases (plugin-free): `references/bases.md`
- Context Graph + Graph-assisted retrieval: `references/context_graph.md`
- Multi-corpus hybrid search: `docs/multi-corpus-search.md`

If the backlog structure is missing, propose creation and wait for user approval before writing files.

## Search Strategy: When to Use Semantic Search vs File Tools

### Use semantic/hybrid search when:
- **Conceptual queries**: "Find items about authentication strategy" (concept-based, not exact string)
- **Cross-file patterns**: "Where do we handle token expiration?" (logic scattered across multiple files)
- **Historical context**: "What decisions were made about embedding models?" (ADRs + items + topics)
- **Fuzzy matching**: "error handling for database connections" (various phrasings, synonyms)
- **Discovery phase**: Exploring unfamiliar codebase or backlog areas

**Commands (unified interface):**
- Backlog corpus: `python skills/kano-agent-backlog-skill/scripts/kano-backlog search hybrid "text" --corpus backlog --product <product> --k 10`
- Repo corpus: `python skills/kano-agent-backlog-skill/scripts/kano-backlog search hybrid "text" --corpus repo --k 10 --fts-k 200`

**Note**: The `--corpus` parameter provides extensibility for future corpus types (logs, metrics, external-docs, etc.).

### Use find/grep/glob when:
- **Exact strings**: Error messages, function names, class names, specific identifiers
- **File patterns**: "Find all test files", "List all .toml configs", "Locate README files"
- **Quick lookups**: Known file paths or specific code locations
- **Structural search**: AST-based patterns (use ast_grep for code structure)
- **No index available**: Indexes not yet built or known to be stale

**Tools:**
- Glob: File pattern matching (`*.py`, `**/*.md`, `test_*.py`)
- Grep: Content search with regex (`class.*Adapter`, `def test_`)
- AST Grep: Code structure patterns (`function $NAME($$$)`, `class $CLASS`)

### Hybrid approach (recommended):
1. **Start with semantic search** for discovery and conceptual understanding
2. **Verify with grep/glob** to find exact locations and confirm results
3. **Rebuild indexes when stale**: Use `--force` flag if results seem outdated

### Index maintenance:
- **Build backlog index**: `python skills/kano-agent-backlog-skill/scripts/kano-backlog embedding build --product <product> --force`
- **Build repo index**: `python skills/kano-agent-backlog-skill/scripts/kano-backlog chunks build-repo-vectors --force`
- **Check status**: `ls -lh _kano/backlog/products/<product>/.cache/chunks.sqlite3 .cache/repo_chunks.sqlite3`
- **When to rebuild**: After major refactoring, file moves, or when search results seem outdated

**Unified CLI:**
- Backlog: `kano-backlog search hybrid "text" --corpus backlog --product <product> --k 10`
- Repo: `kano-backlog search hybrid "text" --corpus repo --k 10 --fts-k 200`
- Both commands: `kano-backlog search {query|hybrid} "text" --corpus {backlog|repo} [options]`
- Future: `--corpus all` for cross-corpus search

**See also**: `docs/multi-corpus-search.md` for detailed hybrid search documentation.

## Kano CLI entrypoints (current surface)

`scripts/` exposes a single executable: `scripts/kano-backlog`. The CLI is intentionally organized as nested command groups so agents can discover operations via `--help` on-demand (instead of hard-coding the full command surface into this skill).

## Profile overlays (user-facing config presets)

This skill supports **optional, file-based profile overlays** for end users who want
simple presets (for example, switching between `noop`, local Hugging Face, or a hosted
embedding provider) without editing the repo’s main `.kano/backlog_config.toml`.

**Where profiles live**
- `<repo>/.kano/backlog_config/<group>/<name>.toml`
  - Example: `.kano/backlog_config/embedding/local-sentence-transformers-minilm.toml`

**How to use a profile**
- Pass `--profile <group>/<name>` to `scripts/kano-backlog` (global option).
  - Example:
    - `python skills/kano-agent-backlog-skill/scripts/kano-backlog --profile embedding/local-noop config show --product <product> --agent <agent-id>`
    - `python skills/kano-agent-backlog-skill/scripts/kano-backlog --profile embedding/local-sentence-transformers-minilm embedding build --product <product>`
    - `python skills/kano-agent-backlog-skill/scripts/kano-backlog --profile embedding/gemini-embedding-001 embedding build --product <product>`

**Optional: set a default profile in `.kano/backlog_config.toml`**
- Add either:
  - `[defaults] profile = "embedding/local-noop"`, or
  - `[shared.profiles] active = "embedding/local-noop"`
- CLI `--profile ...` always overrides the default.

**Env file loading (local dev convenience)**
- By default, the CLI will auto-load `env/local.secrets.env` if it exists.
- Override the location with `--env-file <path>` or `KANO_ENV_FILE`.
- Override behavior is path-only; existing environment variables are not replaced.

**Config vs backlog storage locations (intentional separation)**
- The **product list in config** is authoritative; it does not have to match folder names under `_kano/backlog/products/`.
- A product can point to a **backlog stored elsewhere**: another repo, another drive, a mounted NAS path, or a DB-backed store.
- Treat config as the registry of products; the physical backlog location is an implementation detail chosen per product.

**Precedence**
- Profile overlays are merged on top of the effective config (higher priority than repo defaults and topic/workset overlays in the current implementation).
- Explicit CLI flags still have the highest priority.

### Help-driven discovery (preferred)

Run these in order, expanding only what you need:

- `python skills/kano-agent-backlog-skill/scripts/kano-backlog --help`
  - Shows top-level groups (e.g., `backlog`, `item`, `state`, `worklog`, `view`) and global options.
- `python skills/kano-agent-backlog-skill/scripts/kano-backlog <group> --help`
  - Shows subcommands for that group.
- `python skills/kano-agent-backlog-skill/scripts/kano-backlog <group> <command> --help`
  - Shows required args/options for that command.

Guideline: do not paste large `--help` output into chat; inspect it locally and run the command.

### Canonical examples (keep these few memorized)

- Bootstrap:
  - `python skills/kano-agent-backlog-skill/scripts/kano-backlog doctor --format plain`
  - `python skills/kano-agent-backlog-skill/scripts/kano-backlog admin init --product <name> --agent <id>`
- Daily workflow:
  - `python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem create --type task --title "..." --agent <id> --product <name>`
  - `python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem set-ready <item-id> --context "..." --goal "..." --approach "..." --acceptance-criteria "..." --risks "..." --product <name>`
  - `python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem check-ready <item-id> --product <name>`
  - `python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem update-state <item-ref> --state InProgress --agent <id> --message "..." --product <name>`
  - `python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem attach-artifact <item-id> --path <file> --shared --agent <id> --product <name> [--note "..."]`
  - `python skills/kano-agent-backlog-skill/scripts/kano-backlog view refresh --agent <id> --product <name>`
- Backlog integrity checks:
  - `python skills/kano-agent-backlog-skill/scripts/kano-backlog admin validate uids --product <name>`

## Conflict handling policy (configurable)

Use product config to control how duplicate IDs and UIDs are handled by maintenance commands
such as `admin links normalize-ids`.

- Config keys (product `_config/config.toml`):
  - `conflict_policy.id_conflict`: default `rename` (rename duplicate IDs).
  - `conflict_policy.uid_conflict`: default `trash_shorter` (move shorter duplicate content to `_trash/`).
- `trash_shorter` uses `_trash/<YYYYMMDD>/...` under the product root; items get a Worklog entry.

### Sandbox workflow (isolated experimentation)

For testing, prototyping, or demos without affecting production backlog:
- Create: `python skills/kano-agent-backlog-skill/scripts/kano-backlog admin sandbox init <sandbox-name> --product <source-product> --agent <id>`
- Use: `python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem create --product <sandbox-name> ...` (same CLI, different product)
- Cleanup: `rm -rf _kano/backlog_sandbox/<sandbox-name>` (git will ignore this directory)
- Rationale: Sandboxes mirror production structure but live in `_kano/backlog_sandbox/`, so changes never leak into `_kano/backlog/`.

## Artifacts policy (local-first)

- Storage locations:
  - Shared across products: `_kano/backlog/_shared/artifacts/<ITEM_ID>/` (use `--shared`).
  - Product-local: `_kano/backlog/products/<product>/artifacts/<ITEM_ID>/` (use `--no-shared`).
- Usage:
  - Attach via `workitem attach-artifact` — copies the file and appends a Worklog link.
  - Prefer lightweight, text-first artifacts (Markdown, Mermaid, small images). Use Git LFS for large binaries if needed.
- Git policy:
  - Commit human-readable artifacts that aid review. Avoid committing generated binaries unless justified.
  - Sandboxes under `_kano/backlog_sandbox/` are gitignored; artifacts there are ephemeral.
  - For derived analysis, store under `views/_analysis/` (gitignored by default), and keep deterministic reports in `views/`.
- Linking:
  - The CLI appends a Markdown link relative to the item file. Optionally add a `## Links` section for richer context.

## State update helper

- Use `python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem update-state ...` to update state + append Worklog.
- Prefer `--action` on `kano-backlog state transition` for the common transitions (`start`, `ready`, `review`, `done`, `block`, `drop`).
- Use `python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem validate <item-id>` to check the Ready gate explicitly.

## Topic and Workset workflow (context management)

### When to use Topics

**Topics** are shareable context buffers for multi-step work that spans multiple work items or requires exploratory research before creating formal backlog items.

Use Topics when:
- Exploring a complex problem that may result in multiple work items
- Collecting code snippets, logs, and materials across multiple sessions
- Collaborating across agents/sessions with a shared context
- Refactoring work that requires tracking multiple code locations

#### Topic creation triggers (practical rubric)

Topics are a shared, mid-term context buffer. Create a Topic when the context is likely
to be reused, revisited, handed off, or split into multiple work items.

Hard triggers (agent MAY create immediately):
- 2+ backlog work items are expected (or likely to be created) to complete the effort.
- Cross-module / multi-file work requires tracking multiple code locations or snippet refs.
- Work is expected to span multiple sessions or be handed off across agents.
- You are collecting durable evidence/materials (logs, snippet refs, pinned docs) that
  should be preserved.

Soft triggers (ask the human once before creating):
- You have entered an explore -> adjust -> re-explore loop 2+ times (context is no longer
  linear).
- The thread references 3+ distinct information sources that should stay linked (files,
  ADRs/docs, external links).
- There are 2+ unresolved decisions (A vs B) that will change the downstream plan.
- The user keeps appending new constraints/scope in the same thread (for example: 3+
  follow-ups).

Anti-triggers (prefer Workset or no Topic):
- Single-item execution where a clear Task/Bug exists and you are ready to implement
  (use a Workset).
- Small, single-file change with low risk of handoff or revisiting.
- Pure Q&A / explanation with no need to preserve artifacts or evidence.

#### Post-create human notification (required)

After creating a Topic, always print this (fill in values):
- Topic: <topic-name>
- Path: _kano/backlog/topics/<topic-name>/
- Human brief: _kano/backlog/topics/<topic-name>/brief.md (and brief.generated.md)
- List: python skills/kano-agent-backlog-skill/scripts/kano-backlog topic list --agent <agent-id>

**Topic lifecycle**:
1. **Create**: `python skills/kano-agent-backlog-skill/scripts/kano-backlog topic create <topic-name> --agent <id>`
   - Creates `_kano/backlog/topics/<topic>/` with `manifest.json`, `brief.md`, `brief.generated.md`, `notes.md`, and `materials/` subdirectories
2. **Collect materials**:
   - Add items: `topic add <topic-name> --item <ITEM_ID>`
   - Add code snippets: `topic add-snippet <topic-name> --file <path> --start <line> --end <line> --agent <id>`
   - Pin docs: `topic pin <topic-name> --doc <path>`
3. **Distill**: `python skills/kano-agent-backlog-skill/scripts/kano-backlog topic distill <topic-name>`
  - Generates/overwrites deterministic `brief.generated.md` from collected materials
  - `brief.md` is a stable, human-maintained brief (do not overwrite it automatically)
4. **Switch context**: `python skills/kano-agent-backlog-skill/scripts/kano-backlog topic switch <topic-name> --agent <id>`
   - Sets active topic (affects config overlays and workset behavior)
5. **Close**: `python skills/kano-agent-backlog-skill/scripts/kano-backlog topic close <topic-name> --agent <id>`
   - Marks topic as closed; eligible for TTL cleanup
6. **Cleanup**: `python skills/kano-agent-backlog-skill/scripts/kano-backlog topic cleanup --ttl-days <N> [--dry-run]`
   - Removes raw materials from closed topics older than TTL

**Topic snapshots (retention policy)**:
- Snapshots are intended for **milestone checkpoints** (pre-merge/split/restore, risky bulk edits), not every small edit.
- To prevent noise, keep only the **latest snapshot per topic** in this demo repo.
- After creating a snapshot (or periodically), prune all but the newest snapshot:
  - `python skills/kano-agent-backlog-skill/scripts/kano-backlog topic snapshot cleanup <topic-name> --ttl-days 0 --keep-latest 1 --apply`

**Topic structure**:
```
_kano/backlog/topics/<topic>/
  manifest.json          # refs to items/docs/snippets, status, timestamps
  brief.md               # stable, human-maintained brief (do not overwrite automatically)
  brief.generated.md     # deterministic distilled brief (generated/overwritten by `topic distill`)
  notes.md               # freeform notes (backward compat)
  materials/             # raw collection (gitignored by default)
    clips/               # code snippet refs + cached text
    links/               # urls / notes
    extracts/            # extracted paragraphs
    logs/                # build logs / command outputs
  synthesis/             # intermediate drafts
  publish/               # prepared write-backs (patches/ADRs)
  config.toml            # optional topic-specific config overrides
```

### When to use Worksets

**Worksets** are per-item working directories (cached, derived data) for a single backlog item.

Use Worksets when:
- Starting work on a specific Task/Bug/UserStory
- Need scratch space for deliverables (patches, test artifacts, etc.)
- Want item-specific config overrides (rare)

**Workset lifecycle**:
1. **Initialize**: `python skills/kano-agent-backlog-skill/scripts/kano-backlog workset init <ITEM_ID> --agent <id> [--ttl-hours <N>]`
   - Creates `_kano/backlog/.cache/worksets/items/<ITEM_ID>/` with `meta.json`, `plan.md`, `notes.md`, `deliverables/`
2. **Work**: Store scratch files in `deliverables/` (patches, test outputs, etc.)
3. **Refresh**: `python skills/kano-agent-backlog-skill/scripts/kano-backlog workset refresh <ITEM_ID> --agent <id>`
   - Updates `refreshed_at` timestamp
4. **Cleanup**: `python skills/kano-agent-backlog-skill/scripts/kano-backlog workset cleanup --ttl-hours <N> [--dry-run]`
   - Removes stale worksets older than TTL

**Workset structure**:
```
_kano/backlog/.cache/worksets/items/<ITEM_ID>/
  meta.json              # workset metadata (item_id, agent, timestamps, ttl)
  plan.md                # execution plan template
  notes.md               # work notes with Decision: marker guidance
  deliverables/          # scratch outputs (patches, logs, test artifacts)
  config.toml            # optional item-specific config overrides
```

### Topic vs Workset decision guide

| Scenario | Use Topic | Use Workset |
|----------|-----------|-------------|
| Exploring before creating items | ✅ Yes | ❌ No |
| Multi-item refactor | ✅ Yes | ❌ No |
| Collecting code snippets across files | ✅ Yes | ❌ No |
| Shared context for collaboration | ✅ Yes | ❌ No |
| Single item scratch space | ❌ No | ✅ Yes |
| Item-specific deliverables | ❌ No | ✅ Yes |
| Version-controlled distillation | ✅ Yes (brief.generated.md) | ❌ No |

**Best practice**: Start exploration in a Topic, create work items as scope clarifies, then use Worksets for individual item execution.

### Active topic and config overlays

- Active topic state is shared across agents: `_kano/backlog/.cache/worksets/state.json`
- When an agent has an active topic, config resolution includes topic overrides:
  - Layer order: defaults → product → profile → **topic** → workset → runtime
  - Topic config: `_kano/backlog/topics/<topic>/config.toml`
  - Use for temporary overrides (e.g., switch `default_product` during exploration)

### Named profiles (pipeline experiments)

- Profiles are file-based overrides stored at: `.kano/backlog_config/<profile>.toml` (supports subfolders)
- `--profile` supports two forms:
  - **Path mode (recommended)**: repo-root relative or absolute path to a `.toml` file
    - `--profile .kano/backlog_config/embedding/local-noop.toml`
  - **Shorthand mode**: profile ref resolved under `.kano/backlog_config/`
    - `--profile embedding/local-noop`
- Precedence rule:
  - **Explicit paths** (absolute, or starting with `.` or ending in `.toml`) are honored directly.
  - **Shorthand** prefers `.kano/backlog_config/<ref>.toml` first.
  - If no project-local profile exists, shorthand falls back to `<repo_root>/<ref>.toml`.
- Use `--profile ...` on commands like:
  - `kano-backlog config show --product <product> --profile .kano/backlog_config/embedding/local-noop.toml`
  - `kano-backlog embedding build --product <product> --profile embedding/local-noop`
- List and inspect profiles:
  - `kano-backlog config profiles list --product <product>`
  - `kano-backlog config profiles show <profile> --product <product>`
- Inspect active topic: `python skills/kano-agent-backlog-skill/scripts/kano-backlog topic list --agent <id>`
- Inspect shared topic state: `python skills/kano-agent-backlog-skill/scripts/kano-backlog topic show-state --agent <id> --format json`

### Materials buffer (Topic-specific)

- **Reference-first snippet collection**: Avoid large copy-paste; store file+line+hash+optional snapshot
- **Snippet refs** include:
  - `file`: relative path from workspace root
  - `lines`: `[start, end]` (1-based inclusive)
  - `hash`: `sha256:...` of content for staleness check
  - `cached_text`: optional snapshot (use `--snapshot` to include)
  - `revision`: git commit hash if available

### Human decision materials vs. machine manifest

**Dual-Readability Design**: Every artifact checks against both human and agent readability:
- **Human-Readable**: High-level summaries, clear checklists, "manager-friendly" reports for rapid decision-making
- **Agent-Readable**: Structural precision, file paths, line numbers, explicit markers for action without hallucination

**Implementation in Topics**:
- Treat `manifest.json` as **machine-oriented** metadata:
  - `seed_items`: UUID list for precise agent reference
  - `snippet_refs`: file+line+hash for deterministic loading
  - `pinned_docs`: absolute paths for unambiguous reference
- Keep `brief.generated.md` **deterministic** and **tool-owned** (generated/overwritten by `topic distill`):
  - Readable item titles (e.g., "KABSD-TSK-0042: Implement tokenizer adapter")
  - If available, include item path and keep UID in a hidden HTML comment for deterministic mapping
  - Materials index with items/docs/snippets sorted for repeatability
- Keep `brief.md` **human-oriented** and **stable** (do not overwrite automatically):
  - Context summary and key decisions
  - Optional: include a human-friendly materials list (do not duplicate raw snippet text)
- Put human-facing decision support in `_kano/backlog/topics/<topic>/notes.md` (and/or pinned docs), e.g.:
  - Decision to make
  - Options + trade-offs
  - Evidence (ADR links, snippet refs, benchmark/log artifacts)
  - Recommendation + follow-ups
- **Staleness detection**: Compare current file hash with stored hash to detect if code changed
- **Distillation**: `topic distill` generates deterministic `brief.generated.md` with a repeatable materials index

---
END_OF_SKILL_SENTINEL

