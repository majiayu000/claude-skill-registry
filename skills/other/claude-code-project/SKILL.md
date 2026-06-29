---
name: claude-code-project
description: >
  Use this skill when the user wants to update their project's CLAUDE.md or AGENTS.md, verify their Claude Code setup,
  or check for improvements to their project configuration. Triggers on requests like:
  "update my project docs", "verify my claude setup", "check my project configuration",
  "audit my .claude directory", "improve my CLAUDE.md", "is my setup correct",
  "/update-project", "/verify-project", or "/check".
metadata:
  author: zebbern
  version: "1.1"
---

# Claude Code Project Manager

Manage and maintain Claude Code project configuration files. This skill provides three
invokable workflows for keeping your Claude Code setup optimized and in sync with your
project.

## When to Use Each Command

| Command | Use When |
|---------|----------|
| `/update-project` | Project changed (new stack, tools, conventions). User is unsure if CLAUDE.md/AGENTS.md need updates. |
| `/verify-project` | Want to validate entire .claude setup is correct and functional. Before major changes or periodically. |
| `/check` | Want to discover what could be improved. Looking for missing tools, MCPs, skills, or config gaps. |

## Prerequisites

Before running any command, understand the current project state:

1. Check if `.claude/` directory or `CLAUDE.md` exists in the project root
2. Check if `AGENTS.md` exists (may be imported by CLAUDE.md)
3. Identify the project stack (language, framework, build tools) by examining:
   - `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.
   - `Dockerfile`, `docker-compose.yml`, `Makefile`, `justfile`
   - CI/CD configs (`.github/workflows/`, `.gitlab-ci.yml`)
   - Test runner configs (`vitest.config.*`, `jest.config.*`, `pytest.ini`)
4. Run `ls -la .claude/` or check for `.claude/` directory structure

## `/update-project`: Update CLAUDE.md and AGENTS.md

Review the current project state and update documentation to reflect reality.

### Workflow

1. **Read existing files**: Read current `CLAUDE.md`, `AGENTS.md`, and `.claude/` contents
2. **Analyze project**: Detect the actual stack, tools, commands, and conventions currently in use
3. **Identify gaps**: Compare actual state vs documented state using the checklist in `references/update-project-checklist.md`
4. **Update CLAUDE.md**: Rewrite or patch to reflect current reality. Follow the template in `assets/claude-md-template.md`
5. **Update AGENTS.md**: If used, ensure it imports correctly and covers agent conventions
6. **Summarize changes**: Report what changed and why

### CLAUDE.md Best Practices (from code.claude.com/docs)

- **Be comprehensive but concise**. Every line should earn its place — prefer specific rules over vague ones, but do not omit important conventions just to stay short
- **Target under 200 lines** as a guideline. If you need more, use `.claude/rules/` for path-scoped instructions and `@imports` for detailed guides
- **Load every session** — only include broadly-applicable rules
- **List all commands**: build, test, lint, format, dev, db commands Claude should know
- **Be specific**: "Use 2-space indentation" not "Format code properly"
- **Use @imports**: Pull in README, package.json with `@README`, `@package.json`
- **Keep personal prefs in CLAUDE.local.md** (gitignored, not committed)
- **Use .claude/rules/** for path-scoped instructions that load only when needed
- **Place at project root** or `.claude/CLAUDE.md` — both work

### CLAUDE.md Required Sections

A high-quality CLAUDE.md should cover these categories. Adapt to the project's stack:

**Commands** (always include):
- Dev server, build, start (production)
- Test (once + watch mode if available)
- Lint, format (write + check modes)
- Type check
- Database commands (generate, migrate, seed, studio)
- Any other frequently-used scripts

**Stack** (always include):
- Language + version + strict mode status
- Framework + version + key features (e.g., App Router)
- Database / ORM
- Key libraries (validation, styling, testing)
- Build tool / bundler

**Code Style**:
- Indentation (spaces/tabs, count)
- Naming conventions (files, components, functions, variables)
- Import/export style (ES modules vs CommonJS, named vs default)

**Rules** (specific and verifiable):
- File organization (directory structure, test colocation)
- Component patterns (Server Components vs Client Components)
- API conventions (request/response shapes, error handling)
- Validation rules (input validation library, schemas)
- Git workflow (branch naming, commit style, pre-commit checks)
- Security rules (secrets handling, auth patterns)

**Testing**:
- Test runner and location
- Mocking policy (what to mock, what not to mock)
- Coverage expectations

### AGENTS.md Notes

- Claude Code reads `CLAUDE.md`, not `AGENTS.md` directly
- If AGENTS.md exists for other agents, import it from CLAUDE.md: `@AGENTS.md`
- Add Claude-specific instructions after the import
- AGENTS.md is optional — only create if other tools need it too

### What to Check

Read `references/update-project-checklist.md` for the full checklist.

## `/verify-project`: End-to-End Verification

Run a comprehensive audit of the entire Claude Code project setup.

### Workflow

1. **Read all config files**: `.claude/`, `CLAUDE.md`, `AGENTS.md`, `.mcp.json`, `settings.json`, `settings.local.json`
2. **Check file structure**: Validate directory layout follows conventions
3. **Validate syntax**: Ensure all markdown frontmatter, JSON, and configs parse correctly
4. **Check cross-references**: Verify imports (`@file`) point to existing files
5. **Verify hooks**: Check hook scripts are executable and reference valid commands
6. **Test MCP connectivity**: Verify `.mcp.json` servers are accessible if possible
7. **Check skills**: Verify `.claude/skills/*/SKILL.md` files have valid frontmatter
8. **Check subagents**: Verify `.claude/agents/*.md` files have valid frontmatter
9. **Validate rules**: Ensure `.claude/rules/*.md` have proper globs and content
10. **Report findings**: Output pass/fail for each check with specific issues

Read `references/verify-project-checklist.md` for the full checklist.

### Common Issues to Flag

- CLAUDE.md > 200 lines without path-scoped rules
- Missing build/test/format commands in CLAUDE.md
- `@import` references to non-existent files
- Subagents with duplicate `name` fields
- Hooks referencing commands not in PATH
- skills without YAML frontmatter or missing `name`/`description`
- AGENTS.md not imported in CLAUDE.md (if both exist)

## `/check`: Discover Improvements

Audit the project setup and suggest improvements for tools, MCPs, skills, hooks, and configuration.

### Workflow

1. **Analyze the project**: Read package.json, README, Dockerfile, CI configs, source structure
2. **Check current .claude/ setup**: List all existing configuration
3. **Identify gaps**: Compare against the improvement categories in `references/check-improvements-guide.md`
4. **Search for skills**: If skill recommendations needed, use the `npx skills` CLI (see Skill Discovery below)
5. **Propose improvements**: Deliver prioritized, actionable recommendations

### Improvement Categories

1. **CLAUDE.md quality**: Length, specificity, command coverage, import usage
2. **Missing tools**: Build, test, lint, format tools not documented
3. **MCP opportunities**: External services (databases, APIs, cloud) that could benefit from MCP
4. **Skill gaps**: Workflows that could be automated with skills
5. **Subagent opportunities**: Tasks that would benefit from specialized subagents
6. **Hook opportunities**: Automated actions (format-on-save, lint checks, notifications)
7. **Rules organization**: Path-scoped rules for monorepos or multi-language projects
8. **Settings optimization**: Permission modes, model selection, context management

### Skill Discovery with `npx skills` CLI

Use the Skills CLI for all skill operations. Do NOT browse the website — use the terminal.

**Key commands:**

```bash
# Search for skills by keyword
npx skills find <keyword>
# Example: npx skills find react
# Example: npx skills find testing

# Interactive search (opens fzf-style picker, no arguments)
npx skills find

# List currently installed skills (project + global)
npx skills list

# List only globally installed skills
npx skills ls -g

# Check for skill updates
npx skills check

# Update all installed skills
npx skills update

# Install a skill
npx skills add <owner/repo>
# Example: npx skills add vercel-labs/agent-skills

# Install a specific skill from a multi-skill repo
npx skills add <owner/repo> --skill <skill-name>

# Remove a skill
npx skills remove <skill-name>

# Create a new skill scaffold
npx skills init <skill-name>
```

**How to recommend skills in `/check`:**

1. Run `npx skills list` to see what the user already has installed
2. Identify gaps based on the project stack (e.g., React project missing React skills)
3. Run `npx skills find <keyword>` to search for relevant skills (e.g., `npx skills find react`)
4. Verify quality: prefer 1K+ installs, official sources (`anthropics`, `vercel-labs`, `microsoft`)
5. Report: skill name, purpose, install command, why it fits

**Common skills by category** (use `npx skills find <keyword>` to discover):
- **React/Next.js**: Search `npx skills find react` or `npx skills find nextjs`
- **Testing**: Search `npx skills find testing` or `npx skills find tdd`
- **Design**: Search `npx skills find design` or `npx skills find frontend`
- **Code review**: Search `npx skills find review`
- **Architecture**: Search `npx skills find architecture`
- **Security**: Search `npx skills find security`

### Output Format

Use this structure for `/check` results:

```markdown
# Project Configuration Check: <project-name>

## Summary
<brief overview of current state and top 3 recommendations>

## Current Setup
<what exists today>

## Recommendations (prioritized)
### High Impact
1. **<recommendation>** - <why>
2. ...

### Medium Impact
1. ...

### Low Impact / Nice to Have
1. ...

## Missing Tools/Integrations
- <tool> - <purpose> - <how to add>

## Suggested Skills
- `<owner/repo>` - <purpose> - `npx skills add <owner/repo>`

## Quick Wins
<3 things to do right now for immediate improvement>
```

## Managing Installed Skills

When the user needs to manage existing skills (list, update, remove):

```bash
# See all installed skills
npx skills list

# Check which skills have updates available
npx skills check

# Update everything
npx skills update

# Remove a skill no longer needed
npx skills remove <skill-name>

# Install skill globally (available in all projects)
npx skills add <owner/repo> -g

# Install skill to project only (committed to repo)
npx skills add <owner/repo>
```

## Reference: .claude Directory Structure

```
project/
├── CLAUDE.md              # or .claude/CLAUDE.md - main instructions
├── CLAUDE.local.md        # personal prefs (gitignored)
├── AGENTS.md              # shared agent instructions (imported by CLAUDE.md)
├── .mcp.json              # MCP server configuration
├── .claude/
│   ├── CLAUDE.md          # alternative location for main instructions
│   ├── settings.json      # project-level settings
│   ├── settings.local.json # personal overrides (gitignored)
│   ├── .mcp.json          # alternative MCP location
│   ├── hooks/             # hook scripts (optional)
│   ├── skills/            # custom skills
│   │   └── <skill-name>/
│   │       └── SKILL.md
│   ├── agents/            # custom subagents
│   │   └── <agent-name>.md
│   ├── workflows/         # dynamic workflow scripts (optional)
│   ├── commands/          # custom slash commands (optional)
│   ├── rules/             # path-scoped rules
│   │   └── <rule-name>.md
│   └── agent-memory/      # per-agent memory (auto-managed)
```

For full details, read `references/claude-directory-structure.md`.

## Key Resources

- Claude Code docs: https://code.claude.com/docs
- Skills CLI: `npx skills --help`
- Skills directory: https://www.skills.sh/
- Documentation index: https://code.claude.com/docs/llms.txt
