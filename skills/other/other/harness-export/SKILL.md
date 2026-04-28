---
name: harness-export
description: Use when user invokes /harness-export or wants to save their current harness-kit plugin setup to a shareable harness.yaml file. Detects installed skills, collects source info, and writes the config in Harness Protocol v1 format. Do NOT use for importing or restoring a harness — use /harness-import instead.
disable-model-invocation: true
---

# Export Your Harness Configuration

You are helping the user capture their current harness-kit setup into a `harness.yaml` file they can share with teammates or commit to their dotfiles repo.

This file follows the **Harness Protocol v1 format** — the open spec at harnessprotocol.io. It is backward-compatible with harness-import (which handles both old and new formats).

## Workflow Order (MANDATORY)

**Follow these steps in order. Do not skip any step.**

---

### Step 1: Detect installed skills

Scan all four skill directories. Each subdirectory inside these directories is an installed skill:

- `~/.claude/skills/` — Claude Code global skills
- `.cursor/skills/` — Cursor project-local skills
- `.github/skills/` — Copilot project-local skills
- `.agents/skills/` — agentskills.io standard shared location

```bash
ls ~/.claude/skills/ 2>/dev/null
ls .cursor/skills/ 2>/dev/null
ls .github/skills/ 2>/dev/null
ls .agents/skills/ 2>/dev/null
```

Collect the directory names from each location. Deduplicate by skill name across locations — if the same skill name appears in multiple directories, count it once. Track which platforms each skill was found in.

Show the user the combined result:

```
Found skills across AI tools:

  Claude Code (~/.claude/skills/):  research, explain, orient
  Cursor (.cursor/skills/):         research, explain
  Copilot (.github/skills/):        research
  Shared (.agents/skills/):         (none)

  Unique skills: research, explain, orient
```

Use this deduplicated list as your list of installed plugin names for the steps that follow.

If all four directories are empty or missing, tell the user: "No installed skills found in any supported location. Nothing to export." and stop.

---

### Step 2: Ask about sources and metadata

Tell the user what skills you found, then ask:

> "I found these installed skills: [list]. A couple of quick questions:
>
> 1. For each plugin, which repo is it from? Format: `owner/repo` — for example `harnessprotocol/harness-kit`. If a plugin is from harness-kit, just say so and I'll fill it in.
> 2. What name and description should I give this harness profile? (optional — press enter to skip)
> 3. Do you have any MCP servers, env variables, or CLAUDE.md instructions you'd like to include? (optional)
>
>    Note: MCP server detection is automatic — Step 2.6 will scan `.mcp.json`, `.cursor/mcp.json`, and `.vscode/mcp.json` and ask you separately. You only need to answer about MCP here if you have MCP servers in a non-standard location not covered by those files.
>
> If you've only added harness-kit plugins, just say so."

Wait for the user's response before proceeding.

---

### Step 2.5: Detect cross-platform instruction content

Check whether any cross-platform instruction files exist and contain harness-generated marker blocks:

```bash
grep -l "<!-- BEGIN harness:" .cursor/rules/harness.mdc .github/copilot-instructions.md 2>/dev/null
```

Claude Code instruction files (CLAUDE.md, AGENT.md, SOUL.md) are intentionally excluded — they are managed by the user directly and are not cross-platform sources for export.

If any matching files are found, tell the user what was found and ask. List all slots found in each file — a file may contain multiple harness marker blocks:

> "I also found harness-generated instruction content in these files:
>   - `.cursor/rules/harness.mdc` (contains `my-harness:operational` and `my-harness:behavioral` blocks)
>   - `.github/copilot-instructions.md` (contains `my-harness:operational` block)
>
> Would you like me to include the `operational` and `behavioral` instruction content in the export?"

(List only the files that actually exist and contain marker blocks — substitute the real profile name from the markers in place of `my-harness`.)

If the user says **yes**:
- Extract the content between each `<!-- BEGIN harness:{name}:{slot} -->` and `<!-- END harness:{name}:{slot} -->` marker from those files.
- If the same profile + slot block appears in multiple files with **identical content**, use it once.
- If the same profile + slot block appears in multiple files with **different content**, show the user both versions and ask which to use.
- Store the extracted content to include as the `instructions:` section in harness.yaml (Step 4).

If the user says **no**, skip — do not include instruction content from cross-platform files.

If no harness marker blocks are found in any cross-platform file, skip this step silently.

---

### Step 2.6: Detect cross-platform MCP servers

Scan these three files for MCP server definitions:

```bash
cat .mcp.json 2>/dev/null
cat .cursor/mcp.json 2>/dev/null
cat .vscode/mcp.json 2>/dev/null
```

Each file uses the same JSON structure with a top-level `mcpServers` key. Merge all `mcpServers` entries across all files found. Deduplicate by server name:

- If the same server name appears in multiple files with the **same config**, note that it is shared and count it once.
- If the same server name appears in multiple files with **different configs**, show the user both configs and ask which to keep.

Show the user a summary:

```
Found MCP servers:

  postgres   (in .mcp.json and .cursor/mcp.json — same config)
  filesystem (in .mcp.json only)
```

> "Would you like to include these in the export? (all / pick / none)"

If the user selects **all** or **pick** (and picks at least one), store the chosen servers to write to the `mcp-servers:` section in harness.yaml (Step 4). Convert from JSON format back to harness YAML format: JSON key `type` → YAML key `transport`.

If the user selects **none**, or if no MCP config files are found, skip this step.

---

### Step 3: Build the plugin entries

For each installed skill, determine its source repo:

**Known harness-kit plugins** (source: `harnessprotocol/harness-kit`):
| Plugin | Description |
|--------|-------------|
| explain | Layered explanations of files, functions, directories, or concepts |
| research | Process any source into a structured, compounding knowledge base |
| lineage | Column-level lineage tracing through SQL, Kafka, Spark, and JDBC |
| orient | Topic-focused session orientation across graph, knowledge, and research |
| capture | Capture session information into a staging file for later reflection |
| review | Code review for a branch, PR, or path — severity labels and cross-file analysis |
| docgen | Generate or update README, API docs, architecture overview, or changelog |
| harness-export | Export your installed plugins to a shareable harness.yaml |
| harness-import | Import a harness.yaml and interactively select plugins to install |
| harness-validate | Validate a harness.yaml file against the Harness Protocol v1 JSON Schema |
| harness-compile | Compile harness.yaml to native config files for Claude Code, Cursor, and Copilot |
| harness-sync | Sync AI tool configuration across Claude Code, Cursor, and Copilot |
| open-pr | Pre-flight checks and PR creation: run tests, open a PR, code review, and check CI |
| merge-pr | PR merge workflow: verify CI and review status, sync with base, confirm, squash merge, and clean up |
| pr-sweep | Cross-repo PR sweep: triage all open PRs, run code reviews, merge what's ready, fix quick CI blockers, and report |

For any installed skill **not in this table**, ask the user:
> "I see `[name]` installed but don't recognize it. What `owner/repo` is it from, and what does it do in one sentence?"

---

### Step 4: Write harness.yaml

Write `harness.yaml` to the current directory (or a path the user specifies). Use the **Harness Protocol v1 format**:

```yaml
$schema: https://harnessprotocol.io/schema/v1/harness.schema.json
version: "1"

# Profile identity (optional but recommended)
metadata:
  name: my-harness
  description: My personal harness configuration.

plugins:
  - name: explain
    source: harnessprotocol/harness-kit
    description: Layered explanations of files, functions, directories, or concepts
  # additional plugins follow the same structure
```

**With MCP servers** (include only if user provided them):
```yaml
mcp-servers:
  postgres:
    transport: stdio
    command: uvx
    args:
      - mcp-server-postgres
      - ${DB_CONNECTION_STRING}
```

**With env declarations** (include only if user has env vars):
```yaml
env:
  - name: DB_CONNECTION_STRING
    description: PostgreSQL connection string.
    required: true
    sensitive: true
```

**With instructions** (include only if user wants to bundle CLAUDE.md/AGENT.md content):
```yaml
instructions:
  operational: |
    Your operational instructions here.
  import-mode: merge
```

Rules:
- `version` must be the string `"1"` (quoted), not the integer `1`
- `source` is `owner/repo` — no `marketplace:` key, no `marketplaces:` section
- Only include `mcp-servers`, `env`, `instructions`, and `permissions` sections if the user provided content for them
- If instruction content was collected in Step 2.5, include it as the `instructions:` section
- If MCP servers were collected in Step 2.6, include them as the `mcp-servers:` section (using YAML `transport:` key, not JSON `type:`)
- Omit `metadata` if the user skipped the name/description questions
- Do NOT include `harness-export` or `harness-import` in the output unless the user explicitly asks

---

### Step 5: Confirm and suggest next steps

Tell the user where the file was written:

> "Saved to `harness.yaml`. To compile it to Cursor and Copilot config files, run `/harness-compile`.
>
> To share with teammates: commit it to your dotfiles repo. They can import it with `/harness-import` inside Claude Code, or with the shell fallback:
>
> ```bash
> curl -fsSL https://raw.githubusercontent.com/harnessprotocol/harness-kit/main/harness-restore.sh | bash -s -- harness.yaml
> ```"

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `version: 1` (integer) | Must be `version: "1"` (string) — this is what distinguishes the protocol format |
| Using `marketplace: harness-kit` | Protocol format uses `source: harnessprotocol/harness-kit` — no `marketplaces:` section |
| Including `harness-export` and `harness-import` in the output | Only include plugins the user actually uses |
| Writing to a path without confirming | Write to `./harness.yaml` by default. If user specified a path in the invocation, use that |
| Adding `mcp-servers:` / `env:` / `instructions:` as empty sections | Only include these sections when the user has actual content to put in them |
