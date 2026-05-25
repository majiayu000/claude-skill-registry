---
name: agents-md-manager
description: >-
  This skill should be used when creating, auditing, or maintaining AGENTS.md files
  and Codex CLI configuration for any project—including initializing AGENTS.md for
  cross-agent compatibility (Codex, Cursor, Copilot, Devin, Jules, Amp, Gemini CLI),
  generating config.toml or .rules files, scaffolding .agents/skills/, converting
  CLAUDE.md to AGENTS.md, or auditing existing agent configs for bloat and staleness.
  Complementary to codex-orchestrator (which executes subagents; this skill creates
  the config files they consume).
---

# AGENTS.md Manager

Create and maintain AGENTS.md files and Codex CLI configuration for any project.

## Core Workflow

Determine the mode:

| Mode | When | Script |
|------|------|--------|
| **Create** | New project needs AGENTS.md | `scripts/analyze_project.py` then write |
| **Refresh** | Existing AGENTS.md needs audit | `scripts/validate_agents_md.py` |
| **Convert** | Migrate from CLAUDE.md | `scripts/convert_claude_to_agents.py` |
| **Config** | Generate config.toml | `scripts/generate_config_toml.py` |
| **Rules** | Create .rules files | See `references/starlark-rules-spec.md` |
| **Skills** | Scaffold .agents/skills/ | `scripts/scaffold_codex_skill.py` |

## 1. Project Analysis

Run analysis to detect stack, existing config, and gaps:

```bash
python3 ~/.claude/skills/agents-md-manager/scripts/analyze_project.py [project_path]
```

Output: JSON report with tech stack, commands, directory structure, and Codex artifact inventory (AGENTS.md, config.toml, .rules, .agents/skills/, CLAUDE.md conversion candidates).

## 2. AGENTS.md Generation

Apply the WHAT/WHY/HOW framework in **plain markdown only**—no `@import` syntax, no YAML frontmatter.

### Recommended Sections

```markdown
# Project Name

Brief description.

## Commands
- Dev: `pnpm dev`
- Test: `pnpm test`
- Build: `pnpm build`
- Lint: `pnpm lint`

## Structure
- `/src` — Application source
- `/tests` — Test suites

## Conventions
- [Critical convention 1]
- [Critical convention 2]

## Boundaries
- Always: Run tests before committing
- Ask: Before adding production dependencies
- Never: Modify migration files directly

## Troubleshooting
- [Common issue and fix]
```

### Constraints
- Target under 200 lines per file, under 100 for nested subdirectory files
- Respect 32 KiB limit (`project_doc_max_bytes`)
- Plain markdown only—no `@import`, no YAML frontmatter
- Include a "Boundaries" section (Always/Ask/Never) for agent guardrails
- See `references/templates.md` for project-type-specific templates
- See `references/agents-md-spec.md` for discovery and concatenation rules

## 3. CLAUDE.md Conversion

Convert existing CLAUDE.md to AGENTS.md format:

```bash
python3 ~/.claude/skills/agents-md-manager/scripts/convert_claude_to_agents.py <claude_md_path> [output_path]
```

Outputs AGENTS.md plus `conversion_report.json` listing transformations and manual review items.

Key transformations: `@import` inlined or nested; hooks become `.rules` suggestions; skill invocations become prose; Claude-specific commands stripped.

See `references/conversion-mapping.md` for the complete field-by-field mapping.

## 4. Config Generation

Generate `~/.codex/config.toml` (global) or `.codex/config.toml` (project-scoped):

```bash
python3 ~/.claude/skills/agents-md-manager/scripts/generate_config_toml.py [--global | --project <path>] [--model MODEL] [--sandbox MODE]
```

Covers: model, reasoning effort, personality, sandbox mode, MCP servers, profiles, trusted projects, writable roots.

See `references/config-toml-reference.md` for the complete field reference.

## 5. Rules Files

Create `.rules` files in Starlark for command approval. Location: `~/.codex/rules/` (global) or `.codex/rules/` (project). Rules files are authored manually—no generation script exists for this format. All `.rules` files in the directory are loaded and merged.

Common patterns:
- Allow package manager commands (`npm`, `pip`, `cargo`)
- Block destructive operations (`rm -rf`, `git push --force`)
- Prompt for review on sensitive commands (`git commit`, `gh pr create`)

See `references/starlark-rules-spec.md` for syntax and examples.

## 6. Codex Skills

Scaffold `.agents/skills/<name>/` in Codex format (different from Claude `.claude/skills/`):

```bash
python3 ~/.claude/skills/agents-md-manager/scripts/scaffold_codex_skill.py <name> [--path <dir>]
```

Creates SKILL.md with `name` + `description` frontmatter (both required for Codex), plus `agents/openai.yaml` for UI metadata.

See `references/codex-skills-format.md` for format differences from Claude skills.

## 7. Audit Checklist

When refreshing existing AGENTS.md, validate:

- [ ] Under 32 KiB? (`project_doc_max_bytes` limit)
- [ ] No `@import` syntax? (not supported in AGENTS.md)
- [ ] No YAML frontmatter? (not used in AGENTS.md)
- [ ] All documented commands verified against project config?
- [ ] Directory references match actual structure?
- [ ] No secrets or credentials?
- [ ] Nested hierarchy consistent with root?
- [ ] No AGENTS.override.md conflicts?
- [ ] Under 200 lines? (warn >200, error >400)

Run automated audit:
```bash
python3 ~/.claude/skills/agents-md-manager/scripts/validate_agents_md.py [project_path]
```

## 8. Nested AGENTS.md (Monorepos)

For monorepos, place AGENTS.md at multiple levels:

```
/AGENTS.md              # Repo-wide conventions
/services/
  payments/
    AGENTS.override.md  # Payments-specific overrides
  search/
    AGENTS.md           # Search service conventions
```

- One file per directory maximum
- Codex concatenates root to CWD (closer-to-CWD appears later, overrides earlier)
- `AGENTS.override.md` takes precedence over `AGENTS.md` in the same directory
- Keep each nested file focused and under 100 lines

## Integration Notes

- **codex-orchestrator**: This skill creates config files; codex-orchestrator executes subagents with them
- **claude-md-manager**: Sister skill for Claude Code's CLAUDE.md; use conversion mode to bridge
- For subagent profile management, use `codex-orchestrator`

## Reference Documentation

| File | Contents |
|------|----------|
| `references/agents-md-spec.md` | AGENTS.md discovery, concatenation, override, size limits, cross-agent compatibility |
| `references/config-toml-reference.md` | Complete config.toml field reference |
| `references/starlark-rules-spec.md` | .rules file syntax, prefix_rule(), decision types |
| `references/codex-skills-format.md` | .agents/skills/ format, openai.yaml, Claude skill differences |
| `references/conversion-mapping.md` | CLAUDE.md to AGENTS.md field-by-field mapping |
| `references/templates.md` | AGENTS.md templates by project type |
