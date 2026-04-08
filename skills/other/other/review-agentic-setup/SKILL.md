---
name: review-agentic-setup
description: "Detect agentic coding infrastructure in a project: CLAUDE.md, AGENTS.md, installed skills, MCP servers, hooks, and cross-tool compatibility (Claude Code and Codex CLI). Returns structured findings about agentic readiness without applying changes. Use when the user asks to \"review agentic setup\", \"check agentic setup\", \"agentic readiness\", \"is this project set up for AI coding\", or \"review AI coding setup\"."
---

# Review Agentic Setup

Detect agentic coding infrastructure and flag gaps across Claude Code and Codex CLI conventions. Analysis only. Does not install or configure anything.

## Scope

Agentic setup review always operates at the project level. Scope parameters (diff commands, file lists) are accepted but ignored.

When called standalone, use the git repository root as the project root (fall back to the current working directory if not in a git repo).

## Step 1: Detect Infrastructure

Search for agentic coding configuration in the project. Classify findings into five categories:

### Agent Instructions

| File | Read by | What to check |
|---|---|---|
| `CLAUDE.md` (project root) | Claude Code | Exists? Sections present (project structure, conventions, build commands, rules)? |
| `CLAUDE.md` (subdirectories) | Claude Code | Any nested CLAUDE.md files for sub-module guidance? |
| `AGENTS.md` (root and subdirectories) | Codex | Exists? Content areas (setup, conventions, testing, architecture)? |
| `AGENTS.override.md` | Codex | Exists? Overrides AGENTS.md at the same directory level. |
| `README.md` | Both | Mentions AI-assisted development, agent workflows, or prompting guidance? |

Read each file that exists and summarize its coverage areas. Note which tools can use it.

Claude Code does not read AGENTS.md directly. Projects share instructions across both tools by:

- **Import**: CLAUDE.md includes `@AGENTS.md` to pull in shared content
- **Symlink**: `CLAUDE.md` symlinked to `AGENTS.md` (or vice versa) so both tools read the same file

Check for both patterns when the project has agent instruction files.

### Installed Skills

Check both skill locations. For each skill directory, read the SKILL.md frontmatter to extract `name` and `description`. Group skills by type:

| Location | Used by |
|---|---|
| `.claude/skills/` | Claude Code |
| `.agents/skills/` | Codex |

Skill types:

- **Analysis** — review, audit, or inspection skills
- **Workflow** — multi-step process skills
- **Pipeline** — skills that compose other skills
- **Utility** — formatting, staging, committing, or other focused tools

Both tools use the same SKILL.md format (YAML frontmatter with `name` and `description`). Projects can symlink one location to the other (e.g., `.agents/skills/` → `.claude/skills/`) to share skills across both tools. Check for symlinks.

### MCP Servers

| File | Used by | What to check |
|---|---|---|
| `.mcp.json` (project root) | Claude Code | Configured MCP servers with their types (stdio, http) |
| `.claude/settings.json` | Claude Code | MCP server entries in project settings |
| `.claude/settings.local.json` | Claude Code | MCP server entries in local settings (gitignored) |
| `.codex/config.toml` (`[mcp_servers]`) | Codex | MCP server entries in project config |

List each detected server by name, type, and which tool configuration it belongs to.

### Hooks

| File | Used by | What to check |
|---|---|---|
| `.claude/settings.json` | Claude Code | Hook configurations (PreToolUse, PostToolUse, etc.) |
| `.claude/settings.local.json` | Claude Code | Hook configurations in local settings (gitignored) |
| `.codex/hooks.json` | Codex | Hook configurations (PreToolUse, PostToolUse, etc.) |

List each detected hook with its trigger event, command, and which tool configuration it belongs to.

### Documentation References

Search CLAUDE.md and AGENTS.md content for file paths, URLs, or section headings that reference documentation. Also check the project root for:

| File or directory | What it indicates |
|---|---|
| `docs/` directory | Project documentation |
| `CONTRIBUTING.md` | Contributing guidelines |
| `TROUBLESHOOTING.md` | Known issues and fixes |
| `ARCHITECTURE.md` | Architecture or design docs |
| API docs or schema files referenced in agent instructions | API reference material |

## Step 2: Analyze Gaps and Compatibility

For each category, assess agentic readiness:

- **Present and configured** — infrastructure detected with meaningful content
- **Partially configured** — file exists but content is minimal or boilerplate
- **Missing** — no infrastructure detected for this category

Gap analysis considers the project's complexity. A single-file script doesn't need installed skills. A multi-module application benefits from CLAUDE.md with build commands and architecture notes.

### Cross-Tool Compatibility

After detection, assess which agentic tools the project supports:

| Signal | Compatibility |
|---|---|
| Has `AGENTS.md` but no `CLAUDE.md` | Codex-ready only. Claude Code does not read AGENTS.md. |
| Has `CLAUDE.md` but no `AGENTS.md` | Claude Code-ready only. Codex does not read CLAUDE.md. |
| Has both, but CLAUDE.md lacks `@AGENTS.md` import | Both files exist but instructions are siloed. Claude Code misses AGENTS.md content. |
| Has both, and CLAUDE.md imports `@AGENTS.md` | Both tools supported. Shared instructions with tool-specific additions. |
| Instruction files are symlinked | Both tools supported. Identical instructions. |
| Has `.claude/skills/` but no `.agents/skills/` | Skills available to Claude Code only. |
| Has `.agents/skills/` but no `.claude/skills/` | Skills available to Codex only. |
| Skill directories are symlinked | Both tools supported. Shared skill set. |
| MCP configured in one tool's config only | MCP servers available to that tool only. |

Flag any compatibility gaps as findings. A project that invests in one tool's config but not the other has a portability gap that may matter for teams using both.

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, <=80 chars)>

**Category:** <Agent Instructions | Installed Skills | MCP Servers | Hooks | Documentation References | Compatibility>

<one paragraph: what is missing or underdeveloped and why it matters for agentic workflows>
```

After all findings, add:

```
## Agentic Setup Summary

| Category | Status | Details |
|---|---|---|
| Agent Instructions | <Present/Partial/Missing> | <detected files or "—"> |
| Installed Skills | <Present/Partial/Missing> | <N skills or "—"> |
| MCP Servers | <Present/Partial/Missing> | <detected servers or "—"> |
| Hooks | <Present/Partial/Missing> | <detected hooks or "—"> |
| Documentation References | <Present/Partial/Missing> | <referenced docs or "—"> |

## Tool Support

| Tool | Supported | Key config |
|---|---|---|
| Claude Code | <Yes/Partial/No> | <detected Claude Code files> |
| Codex CLI | <Yes/Partial/No> | <detected Codex files> |

## Overall Verdict

**Agentic readiness:** <well-equipped | gaps found | not configured>

<1-3 sentence summary>
```

If all categories are adequately covered, report that and highlight what the project does well.

## Priority Levels

- **P0** — No agent instruction files (CLAUDE.md, AGENTS.md) in a project with meaningful source code
- **P1** — CLAUDE.md exists but missing build/test commands or project structure
- **P2** — No installed skills, or agent instructions don't reference available documentation
- **P3** — No MCP servers, no hooks, or minor coverage gaps
