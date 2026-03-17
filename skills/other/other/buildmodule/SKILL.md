---
name: BuildModule
version: 0.1.0
description: "Design, build, and validate forge modules. USE WHEN create module, new module, scaffold module, validate module, check module, audit module, module structure, module conventions, module architecture."
---

# BuildModule

Guide for creating robust forge modules. Focuses on the three-layer concern architecture and ensures modules are portable across AI coding tools.

## Module Structure

Every forge module follows this standard layout:

```
module-name/
    module.yaml         Metadata and event registration
    defaults.yaml       Default configuration (committed)
    config.yaml         User overrides (gitignored)
    agents/             Agent markdown files
    skills/             SKILL.md files for AI capabilities
    hooks/              Bash scripts triggered by events
    bin/                Entry points or build scripts
    src/                Source code (typically Rust)
    lib/                forge-lib submodule (shared tooling)
    .claude-plugin/     Claude Code plugin manifest
    Makefile            Multi-provider install/verify/test
    CLAUDE.md           Project instructions for Claude Code (generated)
    AGENTS.md           Project overview for Codex/OpenCode (generated)
    GEMINI.md           Project context for Gemini CLI (generated)
    README.md           Human-facing documentation
    INSTALL.md          Installation guide
    VERIFY.md           Post-installation checklist
```

Not all directories are required. A skills-only module (no hooks, no Rust) only needs: `skills/`, `module.yaml`, `defaults.yaml`, `.claude-plugin/plugin.json`, `Makefile`.

## Core Mandates

1. **Config Convention**: Ship `defaults.yaml` (committed) with reasonable defaults + `config.yaml` (gitignored override). Users create `config.yaml` only when they need overrides. Loader falls back: `config.yaml` > `defaults.yaml` > compiled `Default` impl. Never commit user-specific paths.

2. **Separation of Concerns**: Keep parsing logic "pure" (no I/O) in library modules. Let binaries handle the environment and file reads.

3. **Lazy Compilation**: Use `bin/_build.sh` to compile binaries on first hook invocation, ensuring low overhead.

4. **Validation Driven**: Always provide a `VERIFY.md` that allows an AI agent to confirm the module is functional without manual intervention.

## Three-Layer Architecture

Every module addresses one or more of these concerns:

| Layer | Question | Examples |
|-------|----------|----------|
| **Identity** | Does it store user-specific knowledge? | forge-avatar (goals, preferences, beliefs) |
| **Behaviour** | Does it change how the AI responds? | forge-steering (rules), forge-tlp (access control) |
| **Knowledge** | Does it provide new tools or skills? | forge-council (specialists), forge-core (build skills) |

Don't mix layers. Rules go in behaviour modules. Skills go in knowledge modules. User data goes in identity modules.

## module.yaml

```yaml
name: forge-example
version: 0.1.0
description: One-line description of what this module does.
events: []
```

`events: []` means no hooks. For hook-using modules, list the events:
```yaml
events: [SessionStart, PreToolUse, Stop]
```

## defaults.yaml

```yaml
# Module-specific configuration.
# Override: create config.yaml (gitignored) with only the fields you want to change.

skills:
    claude:
        SkillName:
    gemini:
        SkillName:
    codex:
        SkillName:
    opencode:
        SkillName:

agents:
    AgentName:
        model: fast
        tools: Read, Grep, Glob

providers:
    claude:
        fast: claude-sonnet-4-6
        strong: claude-opus-4-6
    gemini:
        fast: gemini-2.0-flash
        strong: gemini-2.5-pro
    codex:
        fast: o4-mini
        strong: o4-mini
    opencode:
        fast: claude-sonnet-4-6
        strong: claude-opus-4-6
```

The `skills:` section uses provider-keyed allowlists. `install-skills` reads this to decide which skills deploy to which provider. Skills omitted from a provider's list are skipped. This allows Claude-only skills (e.g., those using agent teams) to be excluded from Gemini/Codex without per-skill configuration.

**Critical**: The `providers:` section drives agent deployment. `install-agents` reads provider keys from this section to determine target directories. A provider missing from `providers:` means agents will NOT deploy there, even if the `agents:` section is correct.

## plugin.json

```json
{
    "name": "forge-example",
    "version": "0.1.0",
    "description": "Module description.",
    "author": {"name": "Author Name"},
    "skills": ["./skills"]
}
```

Add `"hooks": "./hooks/hooks.json"` only if the module has hooks.

## Makefile Pattern

Modules use forge-lib's mk/ include fragments for shared targets. Declare roster variables, include fragments, and wire top-level targets:

```makefile
AGENTS   = AgentName
SKILLS   = SkillOne SkillTwo SkillThree
AGENT_SRC = agents
SKILL_SRC = skills
LIB_DIR  = $(or $(FORGE_LIB),lib)

# Fallbacks when common.mk is not yet available (uninitialized submodule)
INSTALL_AGENTS  ?= $(LIB_DIR)/bin/install-agents
INSTALL_SKILLS  ?= $(LIB_DIR)/bin/install-skills
VALIDATE_MODULE ?= $(LIB_DIR)/bin/validate-module

.PHONY: help install clean verify test lint check init

init:
	@if [ ! -f $(LIB_DIR)/Cargo.toml ]; then \
	  echo "Initializing forge-lib submodule..."; \
	  git submodule update --init $(LIB_DIR); \
	fi

ifneq ($(wildcard $(LIB_DIR)/mk/common.mk),)
  include $(LIB_DIR)/mk/common.mk
  include $(LIB_DIR)/mk/skills/install.mk
  include $(LIB_DIR)/mk/skills/verify.mk
  include $(LIB_DIR)/mk/agents/install.mk
  include $(LIB_DIR)/mk/agents/verify.mk
  include $(LIB_DIR)/mk/lint.mk
endif

install: install-agents install-skills
clean: clean-agents clean-skills
verify: verify-skills verify-agents
test: $(VALIDATE_MODULE)
	@$(VALIDATE_MODULE) $(CURDIR)
lint: lint-schema lint-shell
```

**SKILLS variable**: Lists skills for verification and cleanup only. `install-skills` reads `defaults.yaml` directly to decide what deploys where. Provider-specific skills (e.g., Claude-only) should be excluded from the global SKILLS list since `verify` checks all providers. The skill will still install correctly via defaults.yaml.

For skills-only modules (no agents), omit `AGENTS`, `AGENT_SRC`, and the agent mk includes.

## Platform Documentation

Every module ships platform-specific instruction files at its root:

| File | Platform | Generate | Reference |
|------|----------|----------|-----------|
| `CLAUDE.md` | Claude Code | `claude` (manual or `/Init`) | -- |
| `AGENTS.md` | Codex, OpenCode | `codex init` / `opencode init` | @Codex.md, @OpenCode.md |
| `GEMINI.md` | Gemini CLI | `gemini init` | @Gemini.md |

Generate these files by running each platform's CLI init command inside the module directory. The CLI analyzes the codebase and produces platform-appropriate instructions. To update an existing file, rename it to `.bak`, re-run init, and diff.

These files are the primary way AI agents understand the module when working inside it. Generate them after the module structure is complete and before first commit.

## Validation Flow

1. **Unit Tests**: `cargo test` (or equivalent) for Rust modules
2. **Module Conventions**: `validate-module .` checks structure
3. **Skill Verification**: `make verify` confirms deployment
4. **Binary Availability**: Check binaries respond to `--help` or `--version`

## Validate

Run this checklist against any module to audit compliance. Report pass/fail per section.

### 1. Structure

| Check | Pass criteria |
|-------|---------------|
| `module.yaml` exists | Has `name`, `version`, `description` |
| `.claude-plugin/plugin.json` exists | Has `name`, `version`, `description`, `skills` |
| Version match | `module.yaml` version == `plugin.json` version |
| `Makefile` exists | Has `install`, `verify`, `test`, `lint`, `check`, `clean` targets |
| `lib/` submodule | Points to forge-lib, not pinned to ancient commit |
| `defaults.yaml` | Exists if module has configurable behaviour |

### 2. Documentation

| Check | Pass criteria |
|-------|---------------|
| `README.md` | Exists, not empty |
| `INSTALL.md` | Exists, starts with `> **For AI agents**: This guide covers installation of [module].` |
| `VERIFY.md` | Exists, starts with `> **For AI agents**: Complete this checklist after installation.` |
| `CLAUDE.md` | Exists (Claude Code project instructions) |
| `AGENTS.md` | Exists (Codex/OpenCode project overview) |
| `GEMINI.md` | Exists (Gemini CLI project context) |
| `.github/copilot-instructions.md` | Exists (Copilot project context) |

### 3. Skills

For each directory in `skills/`:

| Check | Pass criteria |
|-------|---------------|
| `SKILL.md` exists | Has YAML frontmatter with `name`, `version`, `description` |
| `SKILL.yaml` exists | Has `sources:` field (no `name:` or `description:` -- those live in SKILL.md) |
| Name match | `SKILL.md` frontmatter `name` matches directory name |
| USE WHEN | `description` contains "USE WHEN" trigger phrases |

### 4. Shell Scripts

For each `.sh` file (excluding `target/` and `lib/`):

| Check | Pass criteria |
|-------|---------------|
| Strict mode | `set -euo pipefail` present |
| Alias safety | Uses `command` prefix for `cd`, `cp`, `mv`, `rm` -- never bare |
| No `builtin` keyword | `command` works for everything, `builtin` causes problems |

### 5. Versions

| Check | Pass criteria |
|-------|---------------|
| module.yaml == plugin.json | Version strings match exactly |
| Cargo.toml (if Rust) | Note version -- may differ from module version |

### 6. Configuration

| Check | Pass criteria |
|-------|---------------|
| `config.yaml` in `.gitignore` | User overrides never committed |
| Provider dirs in `.gitignore` | Pattern: `.claude/agents/*`, `.claude/skills/*`, etc. for all 4 providers |
| .gitkeep exclusions | Each provider dir has `.gitkeep` excluded from ignore (`!.claude/agents/.gitkeep`) |
| `.codex/config.toml` ignored | Generated by `install-agents` for Codex provider |
| No committed provider dirs | `.claude/`, `.gemini/`, `.codex/`, `.opencode/` are generated by `make install` -- only .gitkeep files tracked |

### 7. Report

Output a summary table:

```
Section          Status
─────────────────────────
Structure        PASS / FAIL (N issues)
Documentation    PASS / FAIL (N issues)
Skills           PASS / FAIL (N issues)
Shell            PASS / FAIL (N issues)
Versions         PASS / FAIL (N issues)
Configuration    PASS / FAIL (N issues)
```

List specific failures with file paths and remediation hints.

## Constraints

- ALL CAPS filenames = system-provided (SYSTEM.md, CONVENTIONS.md). Title Case = user-authored.
- `config.yaml` is always gitignored at every level
- forge-lib is consumed as a git submodule in `lib/`
- Modules must work standalone -- no dependency on a parent monorepo
