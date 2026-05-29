/opt/homebrew/Library/Homebrew/cmd/shellenv.sh: line 18: /bin/ps: Operation not permitted
name: os-dev-knowledge-skill
description: >
  Skill providing structured knowledge about OS 4.1 / Claude Code configuration
  patterns, safety constraints, and common orchestration pitfalls. Intended for
  os-dev-grand-architect, os-dev-architect, and OS-Dev specialists.
  LOCAL to claude-vibe-config repo only.
---

# OS-Dev Knowledge Skill – OS 4.1 Configuration & Safety

**NOTE: This skill is LOCAL to claude-vibe-config repo only.**

This skill captures key knowledge for working on OS 4.1 / Claude Code config:
lanes, commands, agents, skills, MCPs, hooks, and memory integration.

Use this skill when:

- Planning changes to orchestration lanes or phase configs.
- Adding or modifying commands/agents/skills for OS 2.x.
- Configuring MCPs, hooks, or memory behavior that affect all lanes.

## Configuration Surfaces

- Lanes and pipelines:
  - `docs/pipelines/*.md`
  - `docs/reference/phase-configs/*.yaml`
- Agents and commands:
  - `agents/*.md`, `agents/dev/*.md`
  - `commands/*.md`
- Skills and MCPs:
  - `skills/*/SKILL.md`
  - `mcp/*` (MCP configs, server docs)
- Memory and orchestration:
  - `.claude/memory/` (Workshop + vibe.db)
  - `.claude/orchestration/` (phase_state, evidence, playbooks)

## Core Principles

1. **Orchestrators never implement**
   - `/orca-*` and `*-grand-architect` agents only coordinate.
2. **Specs before complex changes**
   - Requirements specs in `.claude/requirements/<id>` are required for complex, global changes.
3. **Memory-first**
   - Workshop and vibe.db should be queried before expensive context.
4. **Safety over convenience**
   - Never default to dangerous flags or uncontrolled hooks.
5. **Edit-not-rewrite**
   - Minimal diffs in config files; respect existing patterns where safe.

## Common Pitfalls

- Introducing CLI flags (like `--dangerously-skip-permissions`) as defaults.
- Adding hooks that run on every session and execute arbitrary shell commands.
- Scattering temporary logs and config fragments outside `.claude/`.
- Using YAML arrays for `tools:` in agents, causing silent tool failures.

## Best Practices

- Keep OS-Dev agents and commands **lightweight**:
  - Focused scopes, minimal tool lists, clearly documented behaviors.
- Treat standards as evolving:
  - When recurring problems are found, codify them in OS-Dev standards and enforce via gates.
- Integrate Response Awareness:
  - Use RA tags to document assumptions and path choices, especially around safety and global behavior.

Agents and orchestrators should reference this skill when reasoning about OS-Dev
changes to stay aligned with the overall OS 4.1 design philosophy.
