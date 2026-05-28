---
name: skillmeat-cli
description: |
  Manage Claude Code environments using natural language. Use this skill when:
  - User wants to add, deploy, or manage Claude Code artifacts (skills, commands, agents, MCP servers)
  - User asks about available skills or capabilities ("what skills exist for X?")
  - User wants to search for artifacts to solve a problem ("I need something for PDF processing")
  - Agent needs to discover or deploy capabilities for a development task
  - User wants to create, import, or share artifact bundles
  - User mentions "skillmeat", "claudectl", or managing their Claude Code setup
  Supports conversational requests and the claudectl power-user alias.
---

# SkillMeat CLI Skill

Natural language interface for managing Claude Code artifacts and environments.

## Quick Start

### Common Operations

| User Says | What Happens |
|-----------|--------------|
| "Add the PDF skill" | Adds `ms-office-suite:pdf` to collection |
| "Deploy canvas to this project" | Deploys canvas-design skill to `.claude/skills/` |
| "What skills do I have?" | Lists artifacts in current collection |
| "Search for database skills" | Searches all sources for database-related skills |
| "Update all my skills" | Syncs collection with upstream sources |
| "Remove the xlsx skill" | Removes artifact from collection |

### For AI Agents

When you identify a capability gap during development:

1. **Search** for relevant artifacts (don't announce this)
2. **Suggest** to user: "This task would benefit from the X skill. Would you like me to add it?"
3. **Wait** for explicit permission before deploying
4. **Deploy** only what was approved

**Never auto-deploy artifacts without user permission.**

---

## Workflows

### Discovery: Finding Artifacts

When user needs a capability or asks what's available:

```bash
# Search all sources
skillmeat search "<query>" --type skill

# Search with JSON output (for parsing)
skillmeat search "<query>" --type skill --json

# List what's in collection
skillmeat list --type skill

# Show artifact details
skillmeat show <artifact-name>
```

**Artifact Types**: `skill`, `command`, `agent`, `mcp`, `hook`

**Common Sources**:
- `anthropics/skills/*` - Official Anthropic skills
- `anthropics/example-skills/*` - Example/template skills
- Community sources (user-configured)

### Deployment: Adding Artifacts

When user wants to add or deploy an artifact:

**Step 1: Add to Collection**
```bash
# Add from official source
skillmeat add skill anthropics/skills/canvas-design

# Add specific version
skillmeat add skill anthropics/skills/canvas-design@v1.0.0

# Add from any GitHub repo
skillmeat add skill username/repo/path/to/skill
```

**Step 2: Deploy to Project**
```bash
# Deploy to current project
skillmeat deploy <artifact-name>

# Deploy to specific project
skillmeat deploy <artifact-name> --project /path/to/project

# Check what's deployed
skillmeat list --project .
```

### Management: Updating & Removing

```bash
# Check for updates
skillmeat diff <artifact-name>

# Update specific artifact
skillmeat update <artifact-name>

# Update all artifacts
skillmeat sync --all

# Remove from collection
skillmeat remove <artifact-name>

# Undeploy from project
skillmeat undeploy <artifact-name> --project .
```

### Bundles: Sharing Setups

```bash
# Create bundle from current collection
skillmeat bundle create my-setup

# Sign bundle for distribution
skillmeat sign create my-setup.zip

# Import bundle
skillmeat bundle import setup.zip

# Verify bundle signature
skillmeat sign verify setup.zip
```

---

## claudectl Alias

Power users can use `claudectl` for simplified commands with smart defaults:

```bash
claudectl add pdf              # → skillmeat add skill anthropics/skills/pdf
claudectl deploy pdf           # → skillmeat deploy pdf --project .
claudectl search database      # → skillmeat search database --type skill
claudectl status               # → skillmeat list --project . --json
claudectl sync                 # → skillmeat sync --all
claudectl bundle my-setup      # → skillmeat bundle create my-setup
```

### Setup claudectl

Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias claudectl='skillmeat'
```

Or for smart defaults wrapper, see [claudectl-setup.md](./references/claudectl-setup.md).

---

## AI Agent Guidelines

### When to Suggest Artifacts

**DO suggest** when:
- User explicitly asks about capabilities
- Clear capability gap identified (e.g., "process this PDF" but no PDF skill)
- User asks for help with a task that has a well-known skill

**DON'T suggest** when:
- Task can be completed without additional skills
- User is in the middle of focused work
- Suggestion would be redundant (skill already deployed)

### Suggestion Format

```
I notice this task involves [capability]. The [artifact-name] skill
could help with this. Would you like me to add it to the project?

It provides: [brief description]
Source: [source path]
```

### Permission Protocol

1. **Always ask** before deploying
2. **Show what will change** (files to be created)
3. **Confirm success** after deployment
4. **Suggest related artifacts** only if relevant

---

## Command Reference

For complete command documentation, see [command-quick-reference.md](./references/command-quick-reference.md).

### Most Used Commands

| Command | Purpose |
|---------|---------|
| `skillmeat search <query>` | Find artifacts |
| `skillmeat add <type> <source>` | Add to collection |
| `skillmeat deploy <name>` | Deploy to project |
| `skillmeat list` | List in collection |
| `skillmeat list --project .` | List deployed in project |
| `skillmeat show <name>` | Show artifact details |
| `skillmeat sync` | Sync with upstream |
| `skillmeat remove <name>` | Remove from collection |

### Artifact Resolution

The skill resolves fuzzy names to full identifiers:

| User Says | Resolves To |
|-----------|-------------|
| "pdf" | `ms-office-suite:pdf` or `example-skills:pdf` |
| "canvas" | `canvas-design` |
| "xlsx" | `ms-office-suite:xlsx` |
| "docx" | `ms-office-suite:docx` |

When ambiguous, present options and ask user to choose.

---

## Project Context Analysis

When recommending artifacts, analyze project context:

| Project Indicator | Recommended Artifacts |
|-------------------|----------------------|
| `package.json` with React | `frontend-design`, `webapp-testing` |
| `pyproject.toml` | Python-related skills |
| FastAPI imports | `openapi-expert`, backend skills |
| `.claude/` directory | Check what's already deployed |
| `tests/` directory | Testing-related skills |

See [analyze-project.js](./scripts/analyze-project.js) for analysis script.

---

## Error Handling

### Common Issues

| Error | Solution |
|-------|----------|
| "Artifact not found" | Check spelling, try `search` first |
| "Already in collection" | Use `deploy` to deploy existing artifact |
| "Permission denied" | Check directory permissions |
| "Rate limited" | Set GitHub token: `skillmeat config set github-token <token>` |

### Getting Help

```bash
skillmeat --help              # General help
skillmeat <command> --help    # Command-specific help
skillmeat web doctor          # Diagnose environment issues
```

---

## Related Skills

- **skill-builder**: Create new skills
- **skill-creator**: Design skill workflows
- **chrome-devtools**: Browser automation (example of CLI wrapper skill)
