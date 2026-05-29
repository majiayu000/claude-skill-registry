---
name: ai-dev-tools-sync
description: Synchronize and update Claude Code and GitHub Copilot development tool configurations to work similarly. Use when asked to update Claude Code setup, update Copilot setup, sync AI dev tools, add new skills/prompts/agents across both platforms, or ensure Claude and Copilot configurations are aligned. Covers skills, prompts, agents, instructions, workflows, and chat modes.
infer: true
---

# AI Dev Tools Sync

Synchronize Claude Code and GitHub Copilot configurations to maintain feature parity.

## When to Use

Activate this skill when:

- User asks to update Claude Code or Copilot setup
- User wants to add/modify skills, prompts, agents, or instructions
- User wants both tools to work similarly
- User asks about AI dev tool configuration

## Quick Reference

| Claude Code    | GitHub Copilot          | Location                                   |
| -------------- | ----------------------- | ------------------------------------------ |
| SKILL.md       | SKILL.md                | `.claude/skills/` + `.github/skills/`      |
| commands/*.md  | prompts/*.prompt.md     | `.claude/commands/` + `.github/prompts/`   |
| agents/*.md    | agents/*.md             | `.github/agents/` (shared)                 |
| workflows/*.md | -                       | `.claude/workflows/`                       |
| CLAUDE.md      | copilot-instructions.md | Root + `.github/`                          |
| -              | instructions/*.md       | `.github/instructions/` (applyTo patterns) |
| -              | chatmodes/*.chatmode.md | `.github/chatmodes/`                       |

## GitHub Copilot Features Catalog

Complete catalog of GitHub Copilot customization features (as of 2026).

### Configuration Files

#### Repository-Level (`.github/`)

| File/Folder | Purpose | Format |
| --- | --- | --- |
| `copilot-instructions.md` | Global instructions for all Copilot interactions | Markdown |
| `instructions/*.instructions.md` | Path-scoped instructions with `applyTo` frontmatter | Markdown + YAML |
| `prompts/*.prompt.md` | Reusable prompts (slash commands) | Markdown + YAML |
| `agents/*.md` | Agent definitions | Markdown + YAML |
| `skills/*/SKILL.md` | Agent skills with bundled resources | Markdown + YAML |
| `chatmodes/*.chatmode.md` | Custom chat personalities | Markdown + YAML |
| `AGENTS.md` | Master agent routing file | Markdown |

#### Also Supported (Backward Compatibility)

- `.claude/skills/` - Copilot auto-reads Claude skills
- `CLAUDE.md` - Copilot reads if present
- `GEMINI.md` - Gemini CLI format

### Feature Details

#### Custom Instructions (`copilot-instructions.md`)

Root instructions auto-included in every request.

```markdown
# Project Guidelines
- Use TypeScript for all new files
- Follow BEM naming for CSS classes
```

#### Path-Scoped Instructions (`.github/instructions/`)

Apply to specific file patterns via `applyTo`:

```yaml
---
applyTo: "src/Services/**/*.cs"
excludeAgent: ["code-review"] # Optional: exclude specific agents
---
# Backend C# Guidelines
Use PlatformValidationResult for validation...
```

#### Prompts (`.github/prompts/`)

Reusable via `/prompt-name` in chat:

```yaml
---
mode: agent # Optional: agent, chat, edit
---
# Debug this issue
1. Analyze the error
2. Find root cause
3. Propose fix
```

#### Agent Skills (`.github/skills/`)

Folder structure with SKILL.md + bundled resources:

```
skills/my-skill/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

#### Chat Modes (`.github/chatmodes/`)

Custom chat personalities with tool restrictions:

```yaml
---
name: security-reviewer
tools: ["read", "grep", "glob"] # Restrict tools
---
# Security Review Mode
Focus only on security vulnerabilities...
```

#### Agents (`.github/agents/`)

Specialized agent definitions:

```yaml
---
name: frontend-developer
description: UI/UX implementation specialist
---
# Frontend Developer Agent
Specializes in React, TypeScript, CSS...
```

## Sync Patterns

Patterns for keeping Claude Code and GitHub Copilot configurations synchronized.

### Skill Sync

Both platforms support skills in `.github/skills/`. Copilot also reads `.claude/skills/`.

**Best Practice**: Create skills in `.github/skills/` for maximum compatibility.

```
.github/skills/my-skill/
├── SKILL.md          # Both platforms read
├── scripts/          # Executable scripts
├── references/       # Progressive disclosure docs
└── assets/           # Templates, images
```

### Prompt/Command Sync

| Claude Code                  | GitHub Copilot                             |
| ---------------------------- | ------------------------------------------ |
| `.claude/commands/my-cmd.md` | `.github/prompts/my-cmd.prompt.md`         |
| Invoked via `/my-cmd`        | Invoked via `/my-cmd` or `#prompt:my-cmd`  |

**Sync Strategy**:

1. Create in `.github/prompts/` (both read)
2. Or maintain duplicates if behavior differs

### Instructions Sync

| Claude Code         | GitHub Copilot                      |
| ------------------- | ----------------------------------- |
| `CLAUDE.md` (root)  | `.github/copilot-instructions.md`   |
| Single file         | Multi-file with `applyTo` patterns  |

**Sync Strategy**:

1. Keep core rules in both files
2. Use `.github/instructions/` for path-scoped rules (Copilot-specific)
3. Reference detailed docs from both files

### Agent Sync

Both platforms read `.github/agents/*.md`.

**Single Source**: Maintain agents in `.github/agents/` only.

### Workflow Sync

Claude has workflow orchestration. Copilot uses chat modes.

| Claude Workflow          | Copilot Equivalent   |
| ------------------------ | -------------------- |
| Sequential agent chains  | Chat mode switching  |
| `.claude/workflows/`     | `.github/chatmodes/` |

### Decision Matrix

| Feature | Location | Reason |
| --- | --- | --- |
| Skills | `.github/skills/` | Maximum compatibility |
| Prompts | `.github/prompts/` | Both platforms read |
| Agents | `.github/agents/` | Shared location |
| Instructions | Both files | Platform-specific nuances |
| Workflows | `.claude/workflows/` | Claude-specific |
| Chat Modes | `.github/chatmodes/` | Copilot-specific |

### Common Sync Tasks

#### Add New Skill

```bash
mkdir -p .github/skills/new-skill
# Create SKILL.md with frontmatter
# Add references/ and scripts/ as needed
```

#### Add New Prompt

```bash
# Create in .github/prompts/ for both platforms
touch .github/prompts/new-prompt.prompt.md
```

#### Update Core Instructions

1. Edit `CLAUDE.md`
2. Edit `.github/copilot-instructions.md`
3. Keep essential rules in sync

#### Add Path-Scoped Instructions (Copilot)

```bash
# Copilot-specific feature
touch .github/instructions/backend-cqrs.instructions.md
# Add applyTo: "src/Services/**/*Command*.cs"
```

## Sync Process

### Step 1: Understand Current Setup

Read these files to understand current configuration:

```
.claude/workflows/orchestration-protocol.md
.claude/workflows/primary-workflow.md
.github/copilot-instructions.md
.github/AGENTS.md
CLAUDE.md
```

### Step 2: Research Latest Features

Search web for:

- "GitHub Copilot features setup 2026"
- "GitHub Copilot custom instructions agents skills prompts"
- "GitHub Copilot agent mode workspace context"

See the GitHub Copilot Features Catalog section above for the full feature catalog.

### Step 3: Identify Sync Opportunities

Compare capabilities and identify gaps:

- Skills missing in one platform
- Inconsistent prompt/instruction behavior
- Agent definitions that differ

### Step 4: Implement Changes

For each change:

1. **Skills**: Create in both `.claude/skills/` and `.github/skills/`
2. **Prompts**: Create in both `.claude/commands/` and `.github/prompts/`
3. **Instructions**: Update both `CLAUDE.md` and `.github/copilot-instructions.md`
4. **Agents**: Update `.github/agents/` (shared by both)

## Compatibility Notes

- Copilot reads `.claude/skills/` automatically (backward compatibility)
- Both read `.github/prompts/*.prompt.md`
- Both read `.github/agents/*.md`
- Both read `AGENTS.md` in root or `.github/`
- Both support path-based instruction files via `applyTo` in frontmatter

## Sources

- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Custom Instructions](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Awesome Copilot](https://github.com/github/awesome-copilot)

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
