---
name: harness-import
description: Use when user invokes /harness-import or wants to install plugins from a shared harness.yaml config file. Reads the config, presents each plugin interactively, and generates the Claude Code install commands for the ones the user selects. Handles both Harness Protocol v1 format (version: "1") and the legacy format (version: 1).
disable-model-invocation: true
---

# Import a Harness Configuration

You are helping the user install plugins from a `harness.yaml` file — either all of them or a subset they choose.

This skill handles both format versions:
- **v1 protocol format** (`version: "1"` string) — uses `source: owner/repo` per plugin, may include `mcp-servers`, `env`, and `instructions` sections
- **Legacy format** (`version: 1` integer) — uses `marketplace: key` per plugin with a `marketplaces:` section

## Workflow Order (MANDATORY)

**Follow these steps in order. Do not skip any step.**

---

### Step 1: Find and read the config

Check for `harness.yaml` in this order:
1. A path provided by the user after `/harness-import` (e.g., `/harness-import ~/dotfiles/harness.yaml`)
2. `./harness.yaml` in the current directory

If no file is found at either location, tell the user:
> "No `harness.yaml` found. Get one from a teammate or generate your own with `/harness-export`."

Read and parse the file. Detect which format version it uses:
- `version: "1"` (string) → **Protocol v1 format**
- `version: 1` (integer) → **Legacy format**

---

### Step 2: Show what's available

Display the plugin list clearly before asking anything:

```
Plugins in this config:

  1. explain (harnessprotocol/harness-kit) — Layered explanations of files, functions, directories, or concepts
  2. research (harnessprotocol/harness-kit) — Process any source into a structured, compounding knowledge base
  3. superpowers (obra/superpowers-marketplace) — Structured dev workflows — TDD, systematic debugging, subagent delegation
```

For legacy format, resolve the `source` by looking up `plugins[].marketplace` → `marketplaces[key]`.

Then, if the file contains any of the following sections, mention them briefly:
- `mcp-servers:` — "This config also declares MCP servers. I'll ask about those after plugins."
- `env:` — "This config declares environment variables. I'll surface those after plugins."
- `instructions:` — "This config includes harness instructions. I'll offer to apply those after plugins."

Then ask:
> "Would you like to install all of these, pick a subset, or get more details on any before deciding?"

---

### Step 3: Handle the user's choice

**"All"** — mark all plugins as selected, skip to Step 5.

**"Details"** — for each plugin the user asks about, explain what it does based on its description. You can supplement with your knowledge of harness-kit plugins. Then return to this question.

**"Pick" or "subset"** — proceed to Step 4.

---

### Step 4: Individual selection

Walk through each plugin one at a time:

> "**explain** — Layered explanations of files, functions, directories, or concepts. Include? (yes/no)"

Wait for the answer before moving to the next plugin. Collect the selection list.

After all plugins: "Got it — you've selected: [list]. Ready to generate the install commands?"

---

### Step 5: Generate install commands

Output the complete Claude Code command sequence. **Marketplace adds come first, plugin installs second.**

For **protocol v1 format** (`source: owner/repo`), derive marketplace info from the `source` field:

```
Run these in Claude Code:

/plugin marketplace add harnessprotocol/harness-kit
/plugin marketplace add obra/superpowers-marketplace

/plugin install explain@harness-kit
/plugin install superpowers@obra
```

The marketplace short name to use in `/plugin install` commands is the **repo name** (last segment of `owner/repo`). Example: `harnessprotocol/harness-kit` → short name `harness-kit`.

For **legacy format** (`marketplace: key` + `marketplaces:` section), resolve as before:
- `marketplace: harness-kit` + `marketplaces.harness-kit: harnessprotocol/harness-kit` → `/plugin marketplace add harnessprotocol/harness-kit`

Only include marketplaces for plugins actually selected.

Close with:
> "Paste these into Claude Code and run them in order. Restart Claude Code after the installs complete."

---

### Step 5.5: Offer cross-platform setup

After generating the Claude Code install commands, scan the current directory for other AI tool indicators.

**Cursor** is present if any of these exist: `.cursor/`, `.cursor/rules/`, `.cursor/mcp.json`, `.cursor/skills/`
**GitHub Copilot** is present if any of these exist: `.github/`, `.github/skills/`, `.vscode/mcp.json`

If `.github/` is the only Copilot indicator present, ask the user: "I found a `.github/` directory but no other Copilot indicators. Are you using GitHub Copilot in this project?" Only include Copilot in the multi-select menu if the user confirms.

If neither platform is detected, skip this step silently — do not ask.

If one or more platforms are detected, show them and ask which to include:

> "I detected the following other AI tools in this project: Cursor, GitHub Copilot. Which would you like to set up?
> 1. Both
> 2. Cursor only
> 3. Copilot only
> 4. Neither (skip)"

For each confirmed platform, copy installed skill SKILL.md files:
- Only copy skills that have an installed SKILL.md at `~/.claude/skills/<name>/SKILL.md`
- Only copy skill files for the plugins the user selected in Steps 3–4. Do not copy all installed skills — only the selected subset.
- Cursor: copy to `.cursor/skills/<name>/SKILL.md`
- Copilot: copy to `.github/skills/<name>/SKILL.md`

**Frontmatter adaptation when copying:**
- If the source SKILL.md frontmatter has a `dependencies` field, rename it to `compatibility`
- Enforce that the `name` field is lowercase letters and hyphens only, max 64 characters. Truncate and slugify if needed.
- If `description` exceeds 1024 characters, truncate at the last word boundary before 1024 characters and append `…`

Create parent directories before writing (`.cursor/skills/<name>/`, `.github/skills/<name>/`, `.github/instructions/`).

Record which platforms were confirmed — Steps 6 and 8 will use this.

---

### Step 6: Handle MCP servers (if present)

If the config has a `mcp-servers:` section, walk through each server:

> "This config declares an MCP server: **postgres** (stdio, `uvx mcp-server-postgres`). Would you like me to add this to your `.mcp.json`?"

If yes, write or update `.mcp.json` in the current directory with the server definition.

If platforms were confirmed in Step 5.5, also write to platform-specific MCP configs:
- Cursor confirmed: also write `.cursor/mcp.json`
- Copilot confirmed: also write `.vscode/mcp.json`

All three files use the same `mcpServers` JSON structure:

```json
{
  "mcpServers": {
    "postgres": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-postgres", "--connection-string", "${DB_CONNECTION_STRING}"]
    }
  }
}
```

**Note the casing:** `mcpServers` (camelCase) — not `mcp-servers`, not `mcp_servers`.

**Merge behavior (applies to all target files):** If the target file already exists, add new servers but do not overwrite existing server configurations. If a server name already exists in the target file, warn:
```
Warning: <target-config-file> already defines server '<server-name>'. Existing config kept.
  To update it, edit <target-config-file> directly or remove the entry and re-run.
```
For example: `Warning: .cursor/mcp.json already defines server 'postgres'. Existing config kept.`

Create parent directories before writing (`.cursor/`, `.vscode/`).

If the server command contains `${VAR}` references, note which env vars are needed (the `env:` section will cover them in Step 7).

---

### Step 7: Surface env declarations (if present)

If the config has an `env:` section, display them clearly:

```
Environment variables required by this harness:

  DB_CONNECTION_STRING (required, sensitive) — PostgreSQL connection string for the project database.
  ANALYTICS_API_KEY (optional, sensitive) — API key for the analytics MCP server.
```

Tell the user:
> "These environment variables need to be set before using the MCP servers or skills that depend on them. Set them in your shell profile, `.env` file, or secret manager."

Do NOT ask for the values — sensitive vars must never be stored in the harness file or conversation.

---

### Step 8: Offer to apply instructions (if present)

If the config has an `instructions:` section and `import-mode: merge` (or if import-mode is absent, default to merge), offer:

> "This config includes harness instructions (operational guidance for the AI). Would you like me to append them to your `CLAUDE.md` or `AGENT.md`?"

If yes, append to the file the user specifies. If `import-mode: replace` is set, warn:
> "This config requests full replacement of existing instructions. That will overwrite your current CLAUDE.md/AGENT.md. Are you sure?"

If Cursor or Copilot was confirmed in Step 5.5, also compile instructions to those platforms using the same `import-mode` from `harness.yaml`. Use `metadata.name` from the harness.yaml as `{name}` (or `default` if absent). Wrap all generated content in section markers (exact format — do not deviate):

```
<!-- BEGIN harness:{name}:{slot} -->
...generated content...
<!-- END harness:{name}:{slot} -->
```

**Cursor operational** — write `.cursor/rules/harness.mdc` with mandatory frontmatter before the marker block:

```
---
description: Harness operational instructions
globs: **/*
alwaysApply: true
---
```

**Cursor behavioral** — if `instructions.behavioral` is present in harness.yaml, write `.cursor/rules/behavioral.mdc` with mandatory frontmatter before the marker block:

```
---
description: Harness behavioral preferences
globs: **/*
alwaysApply: true
---
```

Then content from `instructions.behavioral` in section markers `<!-- BEGIN harness:{name}:behavioral -->` / `<!-- END harness:{name}:behavioral -->`.

**GitHub Copilot operational** — write `.github/copilot-instructions.md` with mandatory frontmatter before the marker block:

```
---
applyTo: "**"
---
```

**GitHub Copilot behavioral** — if `instructions.behavioral` is present in harness.yaml, write `.github/instructions/behavioral.instructions.md` with mandatory frontmatter before the marker block:

```
---
applyTo: "**"
---
```

Then content from `instructions.behavioral` in section markers `<!-- BEGIN harness:{name}:behavioral -->` / `<!-- END harness:{name}:behavioral -->`.

**Identity slot:** Omit for both Cursor and Copilot — the `identity` slot is Claude Code-only.

Apply the same import-mode behavior for all Cursor and Copilot files:
- **`merge`** (default): If the file exists and contains matching markers, update the content between them. If no markers exist yet, append the marker block at the end (creating the file if it does not exist).
- **`replace`**: Before overwriting any Cursor or Copilot instruction file, warn the user and require confirmation, the same as for CLAUDE.md:
  > "This config requests full replacement of existing [file]. That will overwrite your current [file] content. Are you sure?"
  Never apply `replace` without confirmation.
- **`skip`**: Do not write or modify the file.

Create parent directories before writing (`.cursor/rules/`, `.github/`, `.github/instructions/`).

---

### Step 9: Offer shell fallback

After all the above, add:

> "If you'd rather install without Claude Code, use the shell script:
> ```bash
> curl -fsSL https://raw.githubusercontent.com/harnessprotocol/harness-kit/main/harness-restore.sh | bash -s -- harness.yaml
> ```
> This installs skill files directly (no scripts or hooks — those require the marketplace install)."

---

### Step 9.5: Cross-platform compilation report

If cross-platform setup was performed (at least one platform confirmed in Step 5.5), print a summary after all steps complete:

```
Cross-platform setup complete:

  Cursor:
    Skills:  explain, research  (.cursor/skills/)
    MCP:     postgres  (.cursor/mcp.json)
    Instructions:  harness.mdc (operational), behavioral.mdc (behavioral)

  GitHub Copilot:
    Skills:  explain, research  (.github/skills/)
    MCP:     (none declared in harness.yaml)
    Instructions:  copilot-instructions.md (operational), behavioral.instructions.md (behavioral)
```

Omit any row where nothing was written for that category (e.g., omit `MCP:` if the harness has no `mcp-servers:` section). Omit a platform block entirely if that platform was not confirmed or nothing was written for it. If cross-platform setup was skipped (Step 5.5 produced no confirmations), do not print this report.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Including marketplaces for plugins the user didn't select | Only add `marketplace add` lines for marketplaces that have at least one selected plugin |
| Forgetting to explain the `@name` convention | The `@name` in `/plugin install` must match the marketplace short name (repo name), not the owner |
| Skipping the marketplace add commands | They must come before the plugin installs, or the installs will fail |
| Ignoring `mcp-servers`, `env`, `instructions` sections | Always check for these sections and handle them in the appropriate steps |
| Prompting the user for sensitive env var values | Never ask for secret values — just tell the user which vars to set and where |
| Asking about cross-platform setup when no other platforms are detected | Only prompt for cross-platform setup if Cursor or Copilot indicators are found; skip silently otherwise |
| Copying skill SKILL.md files that aren't installed | Only copy skills that have a SKILL.md at `~/.claude/skills/<name>/SKILL.md` |
| Using `mcp_servers` or `mcp-servers` in MCP JSON files | JSON key must be `mcpServers` (camelCase) in all target files |
| Silently skipping MCP server key collisions in Cursor/Copilot configs | Always warn when a server name already exists in the target file — never skip silently |
| Omitting Cursor `.mdc` frontmatter | Always add `description`, `globs`, `alwaysApply` frontmatter — it is mandatory for Cursor to recognize the file |
| Omitting Copilot `copilot-instructions.md` frontmatter | Always add `applyTo: "**"` frontmatter to Copilot instructions files |
| Using wrong section marker format | Markers must be exact: `<!-- BEGIN harness:{name}:{slot} -->` — any deviation breaks merge logic |
| Skipping parent directory creation | Always create parent dirs (`.cursor/skills/<name>/`, `.github/skills/<name>/`, `.cursor/rules/`, `.vscode/`) before writing |
| Printing the cross-platform report when nothing was set up | Only print Step 9.5 report if at least one platform was confirmed in Step 5.5 |
