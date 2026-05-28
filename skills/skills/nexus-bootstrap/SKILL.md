---
name: nexus-bootstrap
description: Enables your AI agent to discover and install skills from the Nexus Skills Marketplace. Install this skill first to unlock self-service skill management.
---

# Nexus Skills Manager

## Overview
You have access to the Nexus Skills Marketplace. Use these instructions to discover and install skills for the user.

## Configuration
- API Base URL: {{NEXUS_API_URL}}
- Authentication: Use the user's Nexus JWT token from the Authorization header
- Default IDE: {{USER_IDE}}
- Authentication Hint: {{AUTH_HINT}}

## Discovering Skills

Use the MCP tool `nexus__list_skills` with optional parameters:
- `tags`: array of tag strings to filter by
- `search`: text query to search names and descriptions

## Fetching a Skill

Use the MCP tool `nexus__get_skill` with parameter:
- `name`: the skill identifier (e.g., "kubernetes-troubleshooting")

## Installing a Skill

**IMPORTANT: You MUST follow these exact steps. Do NOT deviate from the file paths below.**

### Step 1: Detect the current IDE

Check which IDE directories exist:

- `~/.cursor/skills/` exists → **Cursor**
- `.claude/skills/` exists in project root → **Claude Code** (project-level)
- `~/.claude/skills/` exists → **Claude Code** (global)
- `.windsurf/rules/` exists → **Windsurf**
- `.codex/skills/` exists → **Codex CLI**

### Step 2: Fetch the skill content

Call `nexus__get_skill` with the skill name to get the SKILL.md content.

### Step 3: Create the directory and write the file

**CRITICAL: Each skill MUST be installed in its own subdirectory. The file MUST be named `SKILL.md`. Never use a flat file.**

The exact path pattern is: `{ide-skills-dir}/{skill-name}/SKILL.md`

| IDE | Exact install path |
|-----|-------------------|
| Cursor | `~/.cursor/skills/{skill-name}/SKILL.md` |
| Claude Code (project) | `.claude/skills/{skill-name}/SKILL.md` |
| Claude Code (global) | `~/.claude/skills/{skill-name}/SKILL.md` |
| Windsurf | `.windsurf/rules/{skill-name}/SKILL.md` |
| Codex CLI | `.codex/skills/{skill-name}/SKILL.md` |

For example, to install the "pdf" skill in Cursor:
1. Create directory: `~/.cursor/skills/pdf/`
2. Write file: `~/.cursor/skills/pdf/SKILL.md`

**Do NOT write to `~/.cursor/skills/pdf.md`. Always create a subdirectory first, then write `SKILL.md` inside it.**

### Step 4: Confirm installation

Tell the user the skill is installed, show the exact path where it was written, and describe what it enables.

## Example Conversations

**Discovery:**
```
User: "What skills do you have for Kubernetes?"
→ Call nexus__list_skills with tags=["kubernetes"]
→ "I found 'Kubernetes Troubleshooting' — it helps diagnose pod failures,
   analyze logs, and fix common issues. Want me to install it?"
```

**Installation:**
```
User: "Yes, install it"
→ Call nexus__get_skill with name="kubernetes-troubleshooting"
→ Detect IDE → Cursor detected
→ Create directory ~/.cursor/skills/kubernetes-troubleshooting/
→ Write SKILL.md to ~/.cursor/skills/kubernetes-troubleshooting/SKILL.md
→ "Installed kubernetes-troubleshooting to
   ~/.cursor/skills/kubernetes-troubleshooting/SKILL.md
   I can now help you diagnose Kubernetes issues."
```

**Listing installed:**
```
User: "What skills do I have?"
→ List subdirectories in ~/.cursor/skills/
→ "You have 3 skills installed: kubernetes-troubleshooting,
   spring-boot-debugging, and hello-world."
```
