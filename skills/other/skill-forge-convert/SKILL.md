---
name: skill-forge-convert
description: >
  Convert Claude Code skills to work on OpenAI Codex, Google Gemini CLI, Google
  Antigravity, and Cursor. Analyzes platform-specific features, generates target
  files (openai.yaml, AGENTS.md, GEMINI.md, .mdc rules), adapts frontmatter,
  converts MCP config, and produces compatibility reports. Use when user says
  "convert skill", "port skill", "multi-platform", "skill for codex",
  "skill for gemini", "skill for antigravity", "skill for cursor",
  "cross-platform skill", "convert to codex", "convert to gemini",
  "convert to antigravity", or "convert to cursor".
---

# Skill Conversion — Multi-Platform

Convert Claude Code skills to work on OpenAI Codex, Google Gemini CLI, Google
Antigravity, and Cursor while maintaining quality and following each platform's
best practices.

## Process

### Step 1: Read Source Skill

1. Read the source `SKILL.md` and parse frontmatter
2. Detect skill complexity tier (1-4)
3. Inventory all files: scripts/, references/, agents/, sub-skills
4. Identify MCP config (`.mcp.json`) if present

### Step 2: Analyze Platform Compatibility

Run dry-run analysis first:
```bash
python scripts/convert_skill.py <path> --dry-run --target all
```

Review the compatibility report:
- **Portable fields**: Transfer directly (name, description, license)
- **Adaptable fields**: Need platform-specific handling
- **Claude-only fields**: Will be stripped with warnings

### Step 3: Convert to Target Platforms

Run the conversion:
```bash
python scripts/convert_skill.py <path> --target codex,gemini,antigravity,cursor --output dist/
```

For MCP config conversion:
```bash
python scripts/convert_skill.py <path> --target all --output dist/ --include-mcp
```

### Step 4: Handle Claude-Only Features

Features that need manual adaptation per platform:

| Claude Feature | Codex | Gemini/Antigravity | Cursor |
|---------------|-------|-------------------|--------|
| `allowed-tools` | Supported | Remove; all tools available | Remove; no equivalent |
| `context: fork` | No equivalent | No equivalent | No equivalent |
| `hooks` | 1 event (notify) | Partial (CLI) | 6 events (beta) |
| `model` selection | No equivalent | No equivalent | No equivalent |
| `Task` delegation | Break into separate skills | Break into separate skills | Background Agents (Ultra plan) |
| `/slash` commands | `$mention` syntax | Description-based activation | Description-based + `@rule` |
| Sub-skill routing | Separate skills with `$mention` | Separate skills, LLM-routed | Separate skills, LLM-routed |

### Step 5: Validate Converted Skills

Run validation on each generated output:
```bash
python scripts/validate_skill.py dist/codex/<skill-name>/
python scripts/validate_skill.py dist/gemini/<skill-name>/
python scripts/validate_skill.py dist/antigravity/<skill-name>/
python scripts/validate_skill.py dist/cursor/<skill-name>/
```

Fix any critical or high-priority issues before proceeding.

### Step 6: Generate Deployment Report

Present the user with a summary:

```
## Conversion Report: {skill-name}

| Platform | Score | Files | Warnings | Manual Steps |
|----------|-------|-------|----------|-------------|
| Codex | 92% | 4 | 2 | 1 |
| Gemini | 88% | 3 | 3 | 1 |
| Antigravity | 88% | 3 | 3 | 1 |
| Cursor | 88% | 3 | 3 | 1 |

### Generated Files
[list per platform]

### Warnings
[list per platform]

### Manual Steps Required
[list per platform]
```

### Step 7: Generate Multi-Platform Install Script

When converting for all platforms (`--target all`), the script auto-generates
`install-multiplatform.sh` that:
- Auto-detects the current agent platform
- Installs to the correct skill path
- Supports `--platform` flag for explicit selection

## Platform Quick Reference

| Platform | Skill Path | Instruction File | Config Format |
|----------|-----------|-----------------|---------------|
| Claude Code | `.claude/skills/` | `CLAUDE.md` | JSON (`.mcp.json`) |
| OpenAI Codex | `.agents/skills/` | `AGENTS.md` | TOML (`config.toml`) |
| Gemini CLI | `.gemini/skills/` | `GEMINI.md` | JSON (`settings.json`) |
| Antigravity | `.agent/skills/` | `GEMINI.md` | JSON (`mcp_config.json`) |
| Cursor | `.cursor/skills/` | `.cursor/rules/*.mdc` | JSON (`mcp.json`) |

For full platform specs, load `references/platforms.md`.

## Tier Conversion Guidelines

- **Tier 1** (single SKILL.md): Converts cleanly. Auto-convert recommended.
- **Tier 2** (skill + scripts): Converts well. Verify script paths.
- **Tier 3** (multi-skill): Partial. Each sub-skill converts independently. Routing needs manual work.
- **Tier 4** (ecosystem): Manual review required. Subagent delegation needs platform adaptation.
