---
name: ln-012-mcp-configurator
description: "Installs MCP packages, registers servers in Claude Code, configures hooks, permissions, IDE extension permission mode, and migrations. Use when MCP needs setup or reconfiguration."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# MCP Configurator

**Type:** L3 Worker
**Category:** 0XX Shared

Configures MCP servers in Claude Code: installs npm packages, registers servers, installs hooks and output style, migrates allowed-tools, updates instruction files, grants permissions.

---

## Input / Output

| Direction | Content |
|-----------|---------|
| **Input** | OS info, `dry_run` flag, optional `apply_ide_override` flag (default `false` — Phase 7b is detection-only without it), optional `runId`, optional `summaryArtifactPath` |
| **Output** | Structured summary envelope with `payload.status` = `completed` / `skipped` / `error`, plus per-server outcomes in `changes` / `detail`, plus IDE extension state in `payload.ide_extension` |

If `summaryArtifactPath` is provided, write the same summary JSON there. If not provided, return the summary inline and remain fully standalone. If `runId` is not provided, generate a standalone `run_id` before emitting the summary envelope.

---

## Server Registry

Two transport types: **stdio** (local process) and **HTTP** (cloud endpoint).

| Server | Transport | Install | Required | API Key |
|--------|-----------|---------|----------|---------|
| hex-line | stdio | `npx -y @levnikolaevich/hex-line-mcp` | Yes | No |
| hex-ssh | stdio | `npx -y @levnikolaevich/hex-ssh-mcp` | No | No |
| hex-graph | stdio | `npx -y @levnikolaevich/hex-graph-mcp` | No | No |
| context7 | HTTP | `https://mcp.context7.com/mcp` | Yes | Optional |
| Ref | HTTP | `https://api.ref.tools/mcp` | Yes | Yes (prompt user) |
| linear | HTTP | `https://mcp.linear.app/mcp` | Ask user | No (OAuth) |


---

## Workflow

```
Check Status & Version → Register & Configure → Verify Graph Provider Deps → Hooks → Permissions → IDE Extension Mode → Migrate → Report
```

### Phase 1: Check Status & Version

Smart install: check MCP status AND package drift. npx -y caches aggressively — a connected server may still be backed by an older cached package.

**Step 1a: Check MCP server status**

Run `claude mcp list` -> parse each hex server:

| Server | Status | Action |
|--------|--------|--------|
| Registered + Connected | Working | Check version (Step 1b) |
| Registered + Disconnected | Broken | Re-register (Phase 2) |
| Not registered | Missing | Register in Phase 2 |

**Step 1b: Version check for connected hex-* servers**

For each connected hex server, run in parallel:
```bash
npm view @levnikolaevich/${PKG} version 2>/dev/null
```

Then compare npm latest against the running local version:
1. **npx cache probe:** `npm config get cache` -> scan `{cacheRoot}/_npx/**/node_modules/@levnikolaevich/${PKG}/package.json` -> pick newest by semver/mtime

Use the npx cache version. If probe returns nothing, report `running=unknown` and treat the server as refresh-recommended rather than claiming it is current.

Note: hex packages run via `npx -y`, NOT global install. Never probe global npm paths.

| npm latest | cached local version | Action |
|------------|---------|--------|
| Same | Same | SKIP |
| Newer | Older | Mark "needs update" -> Phase 2 re-registers |
| Unknown | Any | WARN, proceed |

**Skip conditions:**

| Condition | Action |
|-----------|---------|
| `disabled: true` | SKIP |
| `dry_run: true` | Show planned commands |
| Connected + cached local version matches npm latest | SKIP, report version |

### Phase 2: Register & Configure

One pass: use Phase 1 state (do NOT re-run `claude mcp list`) -> remove deprecated -> register/update -> verify.

1. **Reuse Phase 1 state** — server map from Step 1a already has registration + connection status
   - Fallback (standalone only): read `~/.claude.json` + `~/.claude/settings.json`
2. Remove deprecated servers:

| Deprecated Server | Action |
|-------------------|--------|
| hashline-edit | Remove if found |
| pencil | Remove if found |
| lighthouse | Remove if found |
| playwright | Remove if found |
| browsermcp | Remove if found |

3. Register missing OR update outdated servers:
   - IF already configured AND connected AND cached local version matches -> SKIP
   - IF connected but outdated -> remove + re-add (forces npx to fetch latest)
   - IF `dry_run: true` -> show planned command
   - IF **linear** -> ask user: "Do you use Linear?" -> no -> SKIP

Registration commands (OS-dependent prefix):

| OS | Prefix | Why |
|----|--------|-----|
| Windows (bash/MSYS2) | `MSYS_NO_PATHCONV=1 claude mcp add ... -- cmd /c npx` | MSYS2/Git Bash converts `/c` -> `C:/` in args. `MSYS_NO_PATHCONV=1` prevents this |
| Windows (PowerShell/cmd) | `cmd /c npx` | No path conversion issue in native shells |
| macOS / Linux | `npx` | Direct execution |

| Server | Command (Windows bash — always prefix with `MSYS_NO_PATHCONV=1`) |
|--------|----------|
| hex-line | `MSYS_NO_PATHCONV=1 claude mcp add -s user hex-line -- cmd /c npx -y @levnikolaevich/hex-line-mcp` |
| hex-ssh | `MSYS_NO_PATHCONV=1 claude mcp add -s user hex-ssh -- cmd /c npx -y @levnikolaevich/hex-ssh-mcp` |
| hex-graph | `MSYS_NO_PATHCONV=1 claude mcp add -s user hex-graph -- cmd /c npx -y @levnikolaevich/hex-graph-mcp` |
| context7 | `claude mcp add -s user --transport http context7 https://mcp.context7.com/mcp` |
| Ref | `claude mcp add -s user --transport http Ref https://api.ref.tools/mcp` |
| linear | `claude mcp add -s user --transport http linear-server https://mcp.linear.app/mcp` |

4. Verify: `claude mcp list` -> check all registered show `Connected`. This is the only second `claude mcp list` call (post-mutation verify). Retry + report failures.

**Windows MSYS2 path validation (MANDATORY on win32):**
After registration, read `~/.claude.json` -> verify each hex server's `args[0]` is `"/c"` not `"C:/"`.
If corrupted: fix via `mcp__hex-line__edit_file` (set_line the arg to `"/c"`).


**Error handling:**

| Error | Response |
|-------|----------|
| `claude` CLI not found | FAIL, report "Claude CLI not in PATH" |
| Server already exists | SKIP, report "already configured" |
| Connection failed after add | WARN, report detail from `claude mcp list` |
| API key missing (Ref) | Prompt user for key, skip if declined |


### Phase 2b: Verify Graph Provider Dependencies

**MANDATORY READ:** Load `skills-catalog/ln-012-mcp-configurator/references/hex_graph_provider_matrix.md` and `skills-catalog/ln-700-project-bootstrap/references/stack_detection.md`.

After registration + connection, verify only the extra system binaries or packages needed for fuller MCP behavior. Assume the project already has its own runtimes and app dependencies. This phase does NOT install project dependencies, framework packages, or runtimes.

**Step 1: Identify which servers are connected**
Reuse Phase 2 verification state. Only check deps for connected hex-* servers.

**Step 2: Verify hex-line-mcp dependencies**

| Dependency | Check | Required | Auto-fix | Fallback |
|-----------|-------|----------|----------|----------|
| ripgrep | `rg --version` | Yes | See install table | grep_search fails |
| git | `git --version` | No | Inform only | `changes` tool disabled |

Ripgrep install by platform:

| Platform | Command |
|----------|--------|
| Linux (apt) | `sudo apt-get install -y ripgrep` |
| Linux (yum) | `sudo yum install -y ripgrep` |
| macOS | `brew install ripgrep` |
| Windows (winget) | `winget install BurntSushi.ripgrep.MSVC` |
| Windows (scoop) | `scoop install ripgrep` |
| Fallback (npm) | `npm exec --yes -- @vscode/ripgrep-postinstall` |

If `rg --version` fails: ask user whether to auto-install (suggest platform-appropriate command). If user declines, WARN but continue — hex-line will degrade on grep.

**Step 2a: EOL-risk advisory for hex-line**

Inspect repo and user EOL policy, but do not rewrite it here:
- `.gitattributes` for `eol=` / `text=auto`
- `.editorconfig` for `end_of_line`
- `git config --get core.autocrlf`
- `git config --get core.eol`
- `git config --get core.safecrlf`

Report `WARN` when repo policy and user working-tree policy are likely to churn line endings during normal edits. This is advisory only — do not auto-edit repo policy files in `ln-012`.

**Step 3: Detect current project language(s) for hex-graph**

Detect from the current project root only:

1. `docs/project/tech_stack.md` if present
2. marker files in the project root
3. fallback source-extension scan

Use framework markers only to confirm language:

| Framework hint | Language |
|-----------|----------|
| FastAPI, Django, Flask | Python |
| ASP.NET Core | C# |
| Laravel | PHP |
| React, Next.js, Express, NestJS | JavaScript / TypeScript |

If no relevant language is detected for `hex-graph`, skip the optional provider checks and report `SKIP`.

**Step 4: Verify hex-graph-mcp graph-specific providers and SCIP exporters**

Use the MCP tool `install_graph_providers` from `hex-graph-mcp` as the source of truth:

- First call it with `mode: "check"`
- Reuse its `instructions_for_agent` output as the remediation text
- Only if the user agrees, rerun it with `mode: "install"`
- Treat the matrix below as reference policy, not as a second implementation source

| Detected project language | Tool | Check | Required | Auto-fix | Fallback |
|-----------|------|-------|----------|----------|----------|
| JavaScript / TypeScript | None | None | No | None | Embedded TypeScript precise overlay and SCIP export are already available |
| Python | `basedpyright` | `basedpyright-langserver --version` | No | `pip install basedpyright` | Python precise analysis skipped |
| Python | `scip-python` | `scip-python index --help` | No | Windows: `npm install -g github:levnikolaevich/scip-python#fix/windows-path-sep-regex`; macOS/Linux: `npm install -g @sourcegraph/scip-python` | Python `export_scip` skipped |
| C# | `csharp-ls` | `csharp-ls --version` | No | `dotnet tool install -g csharp-ls` | C# precise analysis skipped |
| C# | `scip-dotnet` | `scip-dotnet --help` | No | `dotnet tool install -g scip-dotnet` | C# `export_scip` skipped |
| PHP | `phpactor` | `phpactor --version` | No | Project-specific PHP install path | PHP precise analysis skipped |
| PHP | `scip-php` | `scip-php --help` or `php vendor/bin/scip-php --help` | No | `composer global config repositories.levnikolaevich-scip-php vcs https://github.com/levnikolaevich/scip-php` then `composer global require davidrjenni/scip-php:dev-fix/windows-runtime-fixes --prefer-source` | PHP `export_scip` skipped |

For `hex-graph`, think only about graph-specific providers and optional SCIP exporters:

- DO install or recommend `basedpyright`, `csharp-ls`, `phpactor`, `scip-python`, `scip-dotnet`, and `scip-php` when their language is detected
- DO prefer the patched `scip-python` install on Windows until the upstream Windows fix is released
- DO mention `HEX_GRAPH_SCIP_PYTHON_BINARY` when a patched Python SCIP binary lives outside the default `PATH`
- DO prefer the isolated patched `scip-php` fork for PHP SCIP export when project-local Composer install is blocked or the upstream binary emits an empty artifact
- DO NOT install `python`, `.NET`, `php`, `fastapi`, `django`, `laravel`, `nestjs`, or any project dependency
- DO NOT install anything for framework overlays alone; Stage 4 framework support is parser/convention-based
- Ask the user before any provider install command

**Step 5: Verify hex-ssh-mcp dependencies**

No system dependencies (pure JS ssh2). Skip.

**Step 6: Report dependency table**

Print table with columns: Server | Dependency | Status | Action.

| Status | Meaning |
|--------|---------|
| OK | Available and functional |
| INSTALLED | Was missing, auto-installed |
| WARN | Missing, user declined install |
| SKIP | Not needed for detected project language(s) |
| FAIL | Required, cannot install |

**Error handling:**

| Error | Response |
|-------|----------|
| Required dep missing + user declines | WARN, continue with degraded functionality |
| Auto-install fails | WARN, show manual install instructions |
| Optional dep missing | INFO, note in report |

For `hex-graph`, also report the detected language(s) that drove the provider/exporter checks.
### Phase 3: Hooks & Output Style [CRITICAL]

Do NOT call `setup_hooks`. `hex-line` now auto-syncs hooks and output style on MCP server startup.

After all Phase 2 registrations complete:
1. Trigger one harmless `hex-line` call to start the server, for example `mcp__hex-line__inspect_path({ path: "{project_path}" })`
2. Verify the startup sync results below

**Hooks** (in `~/.claude/settings.json`):
1. `PreToolUse` hook — redirects built-in Read/Edit/Write/Grep to hex-line equivalents
2. `PostToolUse` hook — compresses verbose tool output (RTK filter)
3. `SessionStart` hook — injects MCP Tool Preferences reminder
4. **`disableAllHooks`:** After verifying hooks are synced, read `~/.claude/settings.json`, set `disableAllHooks: false` (merge, preserve all other fields), write back. This is appropriate here because the user explicitly invoked setup and wants hooks active. autoSync does NOT manage this flag — it only syncs hook file content and entries.

**Output Style:**
5. Copies `output-style.md` to `~/.claude/output-styles/hex-line.md`
6. Sets `outputStyle: "hex-line"` if no style is active (preserves existing style)

**Verification:** Confirm all of the following after the first `hex-line` tool call:
- `~/.claude/settings.json` contains the 3 `hex-line` hook entries with current command path
- `disableAllHooks: false` (set explicitly by this skill, not by autoSync)
- `~/.claude/output-styles/hex-line.md` exists and matches package content
- `outputStyle: "hex-line"` is set only when no other style was already active

**Hex-line workflow reminder:** the synced output style must teach all of the following:
- carry `revision` into same-file follow-up edits as `base_revision`
- run `verify` before delayed or mixed-tool follow-up edits on the same file
- reuse `retry_edit`, `retry_edits`, `retry_checksum`, and `retry_plan` directly
- treat line-ending policy as preserved file state, not something `edit_file` should silently normalize

**Note:** autosync is idempotent. Any later `hex-line` startup re-checks installed hook and style content and updates only when they drift.

### Phase 4: Graph Indexing

After hex-graph registration + connected status:
1. `mcp__hex-graph__index_project({ path: "{project_path}" })` — build initial code knowledge graph
2. If graph-backed reads or edits later look stale, rerun `mcp__hex-graph__index_project({ path: "{project_path}" })` — the indexing path is idempotent and refreshes changed files only

Skip if hex-graph not registered or not connected.

### Phase 5: Migrate allowed-tools [CRITICAL]

Scan project commands/skills to replace built-in tools with hex-line equivalents in `allowed-tools` frontmatter.

**Tool mapping:**

| Built-in | Hex equivalent |
|----------|----------------|
| `Read` | `mcp__hex-line__read_file` |
| `Edit` | `mcp__hex-line__edit_file` |
| `Write` | `mcp__hex-line__write_file` |
| `Grep` | `mcp__hex-line__grep_search` |

**Steps:**

1. Glob `.claude/commands/*.md` + `.claude/skills/*/SKILL.md` in current project
2. For each file: parse YAML frontmatter, extract `allowed-tools`
3. For each mapping entry:
   a. If built-in present AND hex equivalent absent -> add hex equivalent, remove built-in (except `Read` and `Bash`)
   b. If built-in present AND hex equivalent already present -> remove built-in (except `Read` and `Bash`)
   c. Preserve ALL existing `mcp__*` tools not in the replacement table
4. Write back updated frontmatter (preserve quoting style)


**Skip conditions:**

| Condition | Action |
|-----------|--------|
| No `.claude/` directory | Skip entire phase |
| File has no `allowed-tools` | Skip file |
| All hex equivalents present | Skip file, report "already migrated" |
| `dry_run: true` | Show planned changes |

### Phase 6: Update Instruction Files [CRITICAL]

Ensure instruction files have MCP Tool Preferences section.

**MANDATORY READ:** Load `mcp/hex-line-mcp/output-style.md` -> use its `# MCP Tool Preferences` section as template.

**Steps:**

1. For each file: CLAUDE.md, GEMINI.md, AGENTS.md (if exists in project)
2. Search for `## MCP Tool Preferences` or `### MCP Tool Preferences`
3. If MISSING -> insert before `## Navigation` (or at end of conventions/rules block)
4. If PRESENT but OUTDATED -> update table rows to match template
5. For GEMINI.md: adapt tool names (`Read` -> `read_file`, `Edit` -> `edit_file`, `Grep` -> `search_files`)
6. Preserve the template's guidance about `base_revision`, `verify`, retry helpers, and preserving existing file line endings

**Skip conditions:**

| Condition | Action |
|-----------|--------|
| File doesn't exist | Skip |
| Section already matches template | Skip, report "up to date" |

### Phase 7: Grant Permissions

Ensure built-in tools and MCP server prefixes are in `~/.claude/settings.json` -> `permissions.allow[]`.

**Built-in tools (ensure present):**

| Tool | Permission entry |
|------|------------------|
| Bash | `Bash` |
| Read | `Read` |
| Write | `Write` |
| Edit | `Edit` |
| Grep | `Grep` |
| WebSearch | `WebSearch` |
| WebFetch | `WebFetch` |

**MCP servers (per configured):**

| Server | Permission entry |
|------|------------------|
| hex-line | `mcp__hex-line` |
| hex-ssh | `mcp__hex-ssh` |
| hex-graph | `mcp__hex-graph` |
| context7 | `mcp__context7` |
| Ref | `mcp__Ref` |
| linear | `mcp__linear-server` |

1. Read `~/.claude/settings.json` (create if missing: `{"permissions":{"allow":[]}}`)  
2. **Consolidate existing entries:** For each universal tool (`Bash`, `Read`, `Write`, `Edit`, `Grep`, `WebSearch`, `WebFetch`, and each `mcp__{name}`):
   - If specific variants exist (e.g. `Bash(gh repo:*)`, `Bash(node ...)`, `WebFetch(domain:docs.github.com)`), remove them — the universal entry covers all
   - Pattern: `entry.startsWith("Tool(")` → remove if universal `Tool` will be added
3. Add universal entries that are not already present
4. Write back (2-space indent JSON)

**Idempotent:** existing universal entries skipped. Only specific sub-entries are consolidated into universal ones.

### Phase 7b: Verify IDE Extension Permission Mode

The Claude Code IDE extension (Cursor / VSCode) has its own `claudeCode.initialPermissionMode` setting that **overrides** `permissions.defaultMode` from `~/.claude/settings.json` when Claude runs through the IDE. Default value is `"default"` — this silently ignores any project-level `bypassPermissions` from `.claude/settings.local.json`. To actually enable bypass when running through the IDE, two extension settings must be set together.

**This phase is detection-first.** It does NOT modify IDE settings without explicit user consent because permission mode is a security decision and IDE settings are vendor-specific.

**Step 1: Detect installed Claude Code IDE extensions**

| IDE | Extensions directory | User settings path (Windows) | User settings path (macOS) | User settings path (Linux) |
|-----|---------------------|------------------------------|----------------------------|----------------------------|
| Cursor | `~/.cursor/extensions/anthropic.claude-code-*` | `%APPDATA%/Cursor/User/settings.json` | `~/Library/Application Support/Cursor/User/settings.json` | `~/.config/Cursor/User/settings.json` |
| VSCode | `~/.vscode/extensions/anthropic.claude-code-*` | `%APPDATA%/Code/User/settings.json` | `~/Library/Application Support/Code/User/settings.json` | `~/.config/Code/User/settings.json` |

For each IDE: glob the extensions directory for `anthropic.claude-code-*`. If at least one match exists, the extension is installed.

**Step 2: Read `package.json` from extension to enumerate `claudeCode.*` settings**

The relevant keys (verified against extension package.json contributes.configuration.properties):

| Setting key | Type | Default | Effect |
|-------------|------|---------|--------|
| `claudeCode.initialPermissionMode` | string enum | `"default"` | Sets `--permission-mode` flag at session start. Enum: `default`, `acceptEdits`, `plan`, `bypassPermissions` |
| `claudeCode.allowDangerouslySkipPermissions` | boolean | `false` | Hard gate — must be `true` for `bypassPermissions` to actually engage. Anthropic's explicit guard for IDE contexts |

**Step 3: Read user settings JSON for each detected IDE and report current state**

| Detected state | Effective behavior | Reported as |
|----------------|--------------------|-------------|
| `initialPermissionMode` absent OR `"default"`, `allowDangerouslySkipPermissions` absent OR `false` | Standard prompt-based permissions, project `defaultMode` IGNORED | `default-prompt` |
| `initialPermissionMode = "acceptEdits"` | File ops auto-approve, Bash still prompts | `accept-edits` |
| `initialPermissionMode = "plan"` | Plan mode forced (no execution) | `plan-only` |
| `initialPermissionMode = "bypassPermissions"`, `allowDangerouslySkipPermissions = true` | Bypass active | `bypass-active` |
| `initialPermissionMode = "bypassPermissions"`, `allowDangerouslySkipPermissions = false` | **Misconfigured** — user wanted bypass but gate is closed; falls back to default | `bypass-blocked` |

Always include in the report: a one-line explanation of why `.claude/settings.local.json defaultMode` is silently ignored when running via IDE extension.

**Step 4: Cross-check against `.claude/settings.json` and `.claude/settings.local.json defaultMode`**

If user's project settings declare `permissions.defaultMode = "bypassPermissions"` but the IDE extension is in `default-prompt` or `bypass-blocked` state → emit a `WARN` in the summary explaining the override:

> WARN: Project `.claude/settings.local.json` declares `defaultMode: bypassPermissions`, but the Claude Code IDE extension for {IDE} forces `--permission-mode {detected}` at session start. The project setting is ignored when running through the IDE. To align them, run this skill with `apply_ide_override=true` and confirm at the prompt, or manually set `claudeCode.initialPermissionMode` and `claudeCode.allowDangerouslySkipPermissions` in {settings_path}.

**Step 5: Optional remediation (only with explicit user consent)**

This phase only writes IDE settings when the caller passes `apply_ide_override=true` (a separate flag distinct from the main `dry_run`). Even with the flag, the skill MUST prompt the user with a single confirmation question listing exactly which keys will change in which file.

When applying changes:

1. **Backup first:** copy settings.json to `settings.json.bak.{timestamp}` before any write
2. **Read → deep-merge → write:** preserve every other `claudeCode.*` key (`preferredLocation`, `useTerminal`, `respectGitIgnore`, etc.) and every non-`claudeCode.*` key
3. **Write only the two keys** dictated by the desired mode:
   - For `bypassPermissions`: set `claudeCode.allowDangerouslySkipPermissions: true` AND `claudeCode.initialPermissionMode: "bypassPermissions"`
   - For `acceptEdits`: set `claudeCode.initialPermissionMode: "acceptEdits"` (gate not required)
   - For `default`: remove both keys (or set to `false` / `"default"`)
4. **Instruct full restart:** print "IDE restart required (full Quit + reopen, NOT Reload Window) — extension reads settings only at activation"
5. **Record in summary:** include before/after values, backup path, and the explicit user consent timestamp

**Skip conditions:**

| Condition | Action |
|-----------|--------|
| No Claude Code IDE extension found | SKIP entire phase, report `no-ide` |
| `dry_run: true` | Detect + report only, no writes (same as default behavior) |
| `apply_ide_override` flag absent | Detect + report only, do NOT prompt user |
| User declines remediation prompt | SKIP write, log decision in summary |
| Project `.claude/settings*.json` does not declare `defaultMode` | INFO: report extension state but no WARN (no conflict to resolve) |

**Why this phase is detection-first by default:**

- IDE settings are per-IDE-vendor and per-user — auto-modifying them across machines is intrusive
- `bypassPermissions` is a security-sensitive choice; Anthropic explicitly guarded it with `allowDangerouslySkipPermissions` for IDE contexts (intended for sandboxes without internet)
- Users may legitimately want different modes per IDE (e.g. `acceptEdits` in Cursor for daily work, `bypassPermissions` in a separate VSCode profile for sandbox automation)
- Aligns with the no-agent-config-modification rule from the host project memory: detection always, writes only on explicit consent

### Phase 8: Report

**Status table:**

```
MCP Configuration:
| Server    | Transport | Version | Status        | Permission | Detail                  |
|-----------|-----------|---------|---------------|------------|-------------------------|
| hex-line  | stdio     | 1.5.0   | configured    | granted    | global npm (hex-line-mcp) |
| hex-ssh   | stdio     | 1.2.0   | updated       | granted    | was 1.1.6, now 1.2.0     |
| context7  | HTTP      | —       | configured    | granted    | mcp.context7.com        |
| Ref       | HTTP      | —       | configured    | granted    | api.ref.tools (key set) |
| linear    | HTTP      | —       | skipped       | skipped    | user declined           |

IDE Extension Permission Mode:
| IDE     | Extension Version | initialPermissionMode | allowDangerouslySkipPermissions | Effective State | Conflict with project defaultMode |
|---------|-------------------|-----------------------|---------------------------------|-----------------|-----------------------------------|
| Cursor  | 2.1.92            | bypassPermissions     | true                            | bypass-active   | aligned                           |
| VSCode  | (not installed)   | —                     | —                               | no-ide          | n/a                               |
```

---

## Critical Rules

1. **Write only via sanctioned paths.** Register servers via `claude mcp add`. Write to `~/.claude/settings.json` ONLY for permissions (`permissions.allow[]`) or when explicit hook/style verification requires correction after autosync fails
2. **Verify after add.** Always run `claude mcp list` after registration to confirm connection
3. **Ask before optional servers.** Linear requires explicit user consent
4. **npx -y for all hex MCP.** Never `npm i -g` — npx provides process isolation and avoids EBUSY on Windows. On Windows, wrap with `cmd /c npx` (see Phase 2 OS prefix table)
5. **Remove deprecated servers.** Clean up servers no longer in the registry
6. **Grant permissions.** After registration, add `mcp__{server}` to user settings
7. **Minimize `claude mcp list` calls.** Phase 1 runs it once (discovery). Phase 2 reuses that data. Only Phase 2 Step 4 runs it again (post-mutation verify). Max 2 calls total
8. **Always check npm drift.** Connected != up to date. Compare npm latest against the newest locally cached npx package version before skipping
9. **MSYS2 path safety.** On Windows with Git Bash/MSYS2, always prefix `claude mcp add` with `MSYS_NO_PATHCONV=1`. After registration, verify `args[0]` in `.claude.json` is `"/c"` not `"C:/"`. Fix inline if corrupted.
10. **Verify graph-specific deps after install.** After Phase 2 registration, check system binaries for hex-line, graph-specific optional providers, and optional SCIP exporters for detected project languages. Auto-install only with user consent. Never install project runtimes or framework packages here.
11. **Report EOL churn risk, do not hide it.** If `.gitattributes`, `.editorconfig`, or Git config suggest working-tree line-ending rewrites, warn explicitly instead of silently changing repo policy here.
12. **Non-destructive config writes.** Always read → merge → edit. Never overwrite config files from scratch. Preserve all keys/sections not owned by this skill.
13. **IDE extension settings are detection-first.** Phase 7b reads `claudeCode.*` keys from Cursor / VSCode user settings and reports the effective permission mode, but never writes IDE settings without `apply_ide_override=true` AND an explicit user prompt confirmation. IDE settings are vendor-specific and changing `bypassPermissions` is a security decision the user must own.

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Write arbitrary fields to `~/.claude.json` | Use `claude mcp add` for servers; rely on `hex-line` startup autosync for hooks/style |
| Skip verification after add | Always check `claude mcp list` after mutations |
| Auto-add optional servers | Ask user for Linear and other optional servers |
| Leave deprecated servers | Remove hashline-edit, pencil, etc. |
| Calculate token budget | Not this worker's responsibility |
| Run `claude mcp list` in every phase | Run once in Phase 1, reuse in Phase 2, verify once after mutations |
| Assume connected = up to date | Check `npm view` version vs newest cached npx package version |
| Assume hooks/style are ready right after registration | Trigger one harmless `hex-line` tool call, then verify autosync results |
| Run `claude mcp add` without MSYS_NO_PATHCONV on Windows bash | Always `MSYS_NO_PATHCONV=1 claude mcp add ...` or verify+fix args after |
| Skip provider verification for hex-graph | Detect project language(s) first, then verify only relevant graph-specific providers and SCIP exporters |
| Auto-install project/framework/runtime packages | Limit this phase to MCP-relevant graph providers and SCIP exporters, and ask user before install |
| Overwrite entire config file with only known fields | Read existing → deep-merge only owned fields → edit back |
| Silently flip `claudeCode.initialPermissionMode` to `bypassPermissions` because the project asked for it | Detect, WARN about the override, require `apply_ide_override=true` AND explicit user confirmation before writing IDE settings |
| Set `initialPermissionMode = "bypassPermissions"` without also setting `allowDangerouslySkipPermissions = true` | Both keys are required together — without the gate the mode silently degrades to default |
| Tell user to use Reload Window after changing IDE settings | Always tell user to fully Quit + reopen — extension reads settings only at activation, not on Reload Window |

---

## Definition of Done

- [ ] MCP packages installed and versions verified against npm registry (Phase 1)
- [ ] Missing servers registered and verified connected (Phase 2)
- [ ] Outdated servers re-registered with latest version (Phase 2)
- [ ] Graph-specific dependencies verified: ripgrep available, detected hex-graph providers and SCIP exporters reported (Phase 2b)
- [ ] Hooks auto-synced after first `hex-line` startup (PreToolUse, PostToolUse, SessionStart) and `disableAllHooks: false` (Phase 3)
- [ ] Output style installed (Phase 3)
- [ ] Permissions granted for all configured servers (Phase 7)
- [ ] IDE extension permission mode detected for installed Cursor / VSCode and reported with WARN if it overrides project `defaultMode` (Phase 7b). Writes only with `apply_ide_override=true` AND user consent.
- [ ] Project allowed-tools migrated (Phase 5)
- [ ] MCP Tool Preferences in all instruction files (Phase 6)
- [ ] Status table with version column displayed (Phase 8) including IDE extension permission mode row

---

**Version:** 1.7.0
**Last Updated:** 2026-04-07
