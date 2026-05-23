---
name: kit-agents
description: (ePost) Use when creating, modifying, or auditing agents, skills, commands, hooks, or planning kit ecosystem changes
user-invocable: false
metadata:
  keywords:
    - agent
    - ecosystem
    - which-agent
    - agent-list
    - subagent
  agent-affinity:
    - epost-fullstack-developer
    - epost-kit-designer
  platforms:
    - all
---

# Agent Ecosystem Reference

Persistent reference for the epost_agent_kit Claude Code ecosystem. Use this when planning changes, creating new components, or auditing the agent system.

## Claude Code Official Components

| Component | Location | Auto-discovered | Purpose |
|-----------|----------|----------------|---------|
| **Agents** | `.claude/agents/` | Yes | Autonomous subprocesses for complex tasks |
| **Skills** | `.claude/skills/` | Yes (nested) | Domain knowledge and workflows |
| **Commands** | `.claude/commands/` | Yes (nested) | User-triggered slash commands (merged into skills) |
| **Hooks** | `.claude/settings.json` | Yes | Event-triggered actions (PreToolUse, PostToolUse, Stop, etc.) |
| **Output Styles** | `.claude/output-styles/` | Yes | Custom response formatting |
| **MCP Servers** | `.mcp.json` (project) / `settings.json` (user) | Yes | External tool integrations |
| **Plugins** | `.claude-plugin/plugin.json` | Via `--plugin-dir` | Distributable component bundles |

**NOT official:** `.claude/workflows/` — Custom reference documentation only, not auto-discovered by Claude Code.

## Commands & Skills Merge

Commands and skills are functionally equivalent and share the same frontmatter fields. Both create `/slash-command` entries. Skills are the preferred format for new additions. Commands in `.claude/commands/` continue to work.

**Key difference:** Skills use `SKILL.md` in a directory; commands are standalone `.md` files in `commands/`.

## Nested Directory Support

Skills support nested directories. Claude Code auto-discovers `SKILL.md` files at any depth under `.claude/skills/`. All skills in this ecosystem use flat names (e.g., `kit-agent-development/SKILL.md`, `web-nextjs/SKILL.md`).

## Agent Frontmatter Reference

| Field | Required | Source | Type | Description |
|-------|----------|--------|------|-------------|
| `name` | Yes | Official | string | Identifier (lowercase, hyphens, 3-50 chars) |
| `description` | Yes | Official | string | Triggering conditions with `<example>` blocks |
| `model` | Yes | Official | string | `inherit`, `sonnet`, `opus`, `haiku` |
| `color` | Yes | Official | string | `blue`, `cyan`, `green`, `yellow`, `magenta`, `red` |
| `tools` | No | Official | array | Restrict available tools (default: all) |
| `skills` | No | Ecosystem | array | Preload skills into agent context at startup |
| `memory` | No | Ecosystem | string | Persistent learning: `user`, `project`, `local` |
| `permissionMode` | No | Ecosystem | string | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `hooks` | No | Ecosystem | object | Per-agent scoped hooks (same format as settings.json hooks) |
| `disallowedTools` | No | Ecosystem | string | Comma-separated tools to deny (advisory) |
| `allowedTools` | No | Ecosystem | string | Comma-separated tools to allow |

**Source legend:** *Official* = confirmed in upstream `anthropics/claude-code` plugin-dev docs. *Ecosystem* = documented in our reference and observed working but not confirmed upstream.

## Skill Frontmatter Reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Skill identifier |
| `description` | Yes | string | When to use (third-person with trigger phrases) |
| `context` | No | string | `fork` — run in isolated subagent |
| `agent` | No | string | Which subagent type for `context: fork` |
| `user-invocable` | No | boolean | `false` hides from `/` menu |
| `disable-model-invocation` | No | boolean | `true` prevents auto-trigger |
| `allowed-tools` | No | array | Restrict tools in forked context |
| `hooks` | No | object | Per-skill hooks |
| `model` | No | string | Override model for this skill |
| `argument-hint` | No | string | Placeholder text for skill argument |

**epost-kit metadata extensions (nested under `metadata:`):**

| Field | Type | Description |
|-------|------|-------------|
| `keywords` | array | Search terms for skill discovery |
| `platforms` | array | Target platforms: ios, android, web, backend, cli, all |
| `triggers` | array | File patterns that trigger skill (e.g., `.kt`, `.swift`) |
| `agent-affinity` | array | Preferred agents for this skill |
| `connections.extends` | array | Parent skills this inherits from |
| `connections.requires` | array | Skills that must be co-loaded |
| `connections.conflicts` | array | Skills that cannot coexist |
| `connections.enhances` | array | Optional complementary skills |

**Invalid fields:** `version` (not recognized by Claude Code)

## Directory Structure

```
.claude/
├── agents/                           # 17 specialized agents
│   ├── epost-project-manager.md      # Progress tracking & roadmaps
│   ├── epost-planner.md              # Planning & research coordination
│   ├── epost-fullstack-developer.md  # Fullstack development
│   ├── epost-code-reviewer.md        # Quality assurance & security
│   ├── epost-debugger.md             # Root cause debugging
│   ├── epost-tester.md               # Test orchestration
│   ├── epost-researcher.md           # Technology research
│   ├── epost-docs-manager.md         # Auto-updating documentation
│   ├── epost-git-manager.md          # Git workflow automation
│   ├── epost-brainstormer.md         # Creative ideation
│   ├── epost-kit-designer.md         # Kit authoring specialist
│   ├── epost-a11y-specialist.md      # Multi-platform accessibility (WCAG 2.1 AA)
│   ├── epost-muji.md                 # MUJI UI library
│   ├── epost-code-simplifier.md      # Code simplification
│   ├── epost-journal-writer.md       # Development journals
│   ├── epost-mcp-manager.md          # MCP integration
│   └── epost-ui-ux-designer.md       # UI/UX design
├── skills/                           # Domain knowledge (flat layout)
│   ├── kit-agents/                   # Ecosystem hub (this file)
│   ├── kit-agent-development/        # Agent creation guide
│   ├── kit-skill-development/        # Skill creation guide
│   ├── kit-hooks/                    # Hook authoring
│   ├── kit-cli/                      # CLI tool patterns
│   ├── core/                         # Operational rules
│   ├── data-store/                   # Agent persistent data store convention
│   ├── cook/                         # Build/implement features
│   ├── fix/                          # Fix issues and errors
│   ├── plan/                         # Planning workflow
│   ├── test/                         # Test orchestration
│   ├── debug/                        # Debug workflow
│   ├── scout/                        # Codebase exploration
│   ├── review-code/                  # Code review
│   ├── git-commit/                   # Git commit workflow
│   ├── git-push/                     # Git push workflow
│   ├── git-pr/                       # Git PR creation
│   ├── web-nextjs/                   # Next.js patterns
│   ├── web-frontend/                 # React/frontend patterns
│   ├── figma/                        # Figma MCP + extraction (all platforms)
│   ├── design-tokens/                # Vien 2.0 token architecture (all platforms)
│   ├── web-ui-lib/                   # UI component library (web, in platform-web)
│   ├── ui-lib-dev/                   # UI library pipeline + integration guidance (all platforms)
│   ├── web-a11y/                     # Web accessibility (WCAG 2.1 AA)
│   ├── ios-development/              # Swift/SwiftUI patterns
│   ├── ios-a11y/                     # iOS accessibility
│   ├── simulator/                    # iOS simulator management
│   ├── android-development/          # Kotlin/Compose patterns
│   ├── android-a11y/                 # Android accessibility
│   ├── backend-javaee/               # Jakarta EE patterns
│   ├── a11y/                         # Cross-platform a11y foundation
│   ├── knowledge-retrieval/          # Knowledge lookup + base management
│   ├── knowledge-capture/            # Post-task knowledge capture
│   └── ...                           # (other cross-cutting skills)
├── workflows/                        # Reference docs (NOT auto-discovered)
│   ├── feature-development.md
│   ├── bug-fixing.md
│   └── project-init.md
├── output-styles/                    # Response formatting (5 styles)
└── settings.json                     # Hooks, permissions, env vars
```

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Agent files | `epost-<role>.md` | `epost-planner.md` |
| Commands | `<category>/<action>.md` | `web/cook.md` |
| Skills | `<name>/SKILL.md` | `web-nextjs/SKILL.md` |
| Kit skills | `kit-<topic>/SKILL.md` | `kit-agent-development/SKILL.md` |

## Description Patterns

| Component | Pattern |
|-----------|---------|
| **Agents** | `[Role] agent that [does X]. Use for [contexts].` |
| **Skills** | `[Domain] [description]. Use when [contexts].` |
| **Commands** | `[Imperative verb] [object/scope]` |

## Plugin System

Distributable via `.claude-plugin/plugin.json`:

```json
{
  "name": "plugin-name",
  "description": "Plugin description",
  "version": "1.0.0",
  "commands": ["./.claude/commands/"],
  "agents": ["./.claude/agents/"],
  "skills": ["./.claude/skills/"]
}
```

Load with: `claude --plugin-dir /path/to/plugin`

## Sub-Skills

- `kit-agent-development` — Agent creation, frontmatter, system prompts, triggering
- `kit-skill-development` — Skill creation, progressive disclosure, validation

## Related Documents

- `CLAUDE.md` — Project overview and guidelines
- `.claude/skills/core/SKILL.md` — Operational rules
- `.claude/agents/` — Agent definitions
