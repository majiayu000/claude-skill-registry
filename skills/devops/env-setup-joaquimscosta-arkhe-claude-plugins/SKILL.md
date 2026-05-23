---
name: env-setup
description: >-
  Interactive Claude Code environment setup wizard. Detects existing configuration,
  guides through best-practice setup for Global CLAUDE.md, project scaffolding,
  MCP servers, hooks, custom agents, keybindings, and settings.
  Use when user runs /claude-setup, mentions "setup claude code", "configure claude",
  "claude code setup", "environment setup", or "initialize claude code".
disable-model-invocation: true
---

# Claude Code Setup Wizard

Interactive environment setup following the Claude Code Guide.

## Pre-flight

Run the detection script to understand current state:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/detect_setup.py
```

## Two-Phase Workflow

### Phase 1: Detect

1. **Run the detector** on the project root:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/detect_setup.py <project-root>
   ```

2. **Fetch the guide** via WebFetch:
   ```
   https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/CLAUDE_CODE_GUIDE.md
   ```
   If WebFetch fails (network error, 404), warn the user and proceed using LLM knowledge only.

3. **Cross-reference** detection JSON against guide recommendations to identify what is missing or incomplete.

4. **Detect MCP servers** separately via Bash:
   ```bash
   claude mcp list
   ```

### Phase 2: Configure

1. **Present category selection** using `AskUserQuestion` (multiSelect: true). Show detection status for each category (configured / partially configured / not configured):

| # | Category | Guide Section | What It Configures |
|---|----------|---------------|--------------------|
| 1 | Global CLAUDE.md | Section 1 | `~/.claude/CLAUDE.md` — security NEVER rules, account config |
| 2 | Project Scaffolding | Section 2 | `.claude/` dirs, `.env.example`, `.gitignore`, `CLAUDE.md` |
| 3 | MCP Servers | Section 3 | Install recommended servers via `claude mcp add` |
| 4 | Hooks | Section 7 | `~/.claude/hooks/block-secrets.py`, hooks in settings.json |
| 5 | Custom Agents | Section 10 | `~/.claude/agents/` starter agent files |
| 6 | Keybindings | Section 13 | `~/.claude/keybindings.json` |
| 7 | Settings | Section 13 | Language, background tasks in settings.json |

   If user passed a specific category as argument (e.g., `/claude-setup hooks`), skip the selection and go directly to that category.

2. **Walk through each selected category** with targeted `AskUserQuestion` calls. See [WORKFLOW.md](WORKFLOW.md) for per-category question flows.

3. **Show confirmation summary** — table of all proposed CREATE/MODIFY/SKIP actions. Ask user to confirm before executing.

4. **Execute changes** — create files, install MCP servers, update settings.

5. **Post-setup summary** — show what was configured, next steps, and remind user they can re-run `/claude-setup` for incremental updates.

## Key Rules

- **Never overwrite** existing files without asking. Always offer merge/replace/skip.
- **Detect first** — skip items already configured.
- **Use AskUserQuestion** for every decision. Do not assume user preferences.
- **Merge settings** — when updating settings.json, read existing content first and deep-merge.
- **MCP servers** — ask scope (global `-s user` vs project `-s project`) before installing.

## Guide Reference

Fetch at runtime — do not cache or embed:
- **Claude Code Guide**: `https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/CLAUDE_CODE_GUIDE.md`

## References

- **Workflow**: See [WORKFLOW.md](WORKFLOW.md) for per-category setup flows
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for example setup sessions
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- **Detection Script**: See [scripts/detect_setup.py](scripts/detect_setup.py) for detection logic
