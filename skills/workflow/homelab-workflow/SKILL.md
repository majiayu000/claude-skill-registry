---
name: homelab-workflow
description: Enforce homelab-proxmox workflow patterns including single source of truth documentation, prompt logging, git commits, environment variables, and phase tracking. Use this skill when completing tasks, updating docs/ or CLAUDE.md files, or when workflow compliance validation is needed. Provides AI-powered fixes for violations.
---

# Homelab Workflow Enforcer

Enforce workflow patterns for the homelab-proxmox project with AI-powered validation and fixes.

## When to Use

- User runs `/validate` command
- Making changes to CLAUDE.md or docs/ files
- Completing significant tasks
- Checking workflow compliance

## Automated Systems

**Prompt Logging**: Automatic via Stop hook (`.claude/hooks/stop`). Logs to `logs/prompts.log` after every response.

## Core Checks

### 1. Documentation Compliance (Single Source of Truth)

| File | Contains |
|------|----------|
| `docs/HARDWARE.md` | Physical hardware specs, exact models, capacities |
| `docs/NETWORK.md` | Network config, VLANs, IP addressing |
| `docs/SOFTWARE.md` | Software stack, versions |
| `docs/LINKS.md` | Reference links |
| `CLAUDE.md` | Project plan, phases, architecture decisions |

**Violation**: Specs duplicated in CLAUDE.md (e.g., listing "MS-01 with 96GB RAM")
**Fix**: Remove specs from CLAUDE.md, reference docs/ instead

### 2. Git Commit Status

Check for uncommitted changes:
```bash
git status --porcelain
```

When uncommitted changes found, commit with standard format.

### 3. CLAUDE.md Status

Verify:
- "Last Updated" date is today (if changes made)
- Phase checkboxes match actual progress
- "Current Status" reflects reality

### 4. Environment Variables

Scan for hardcoded values (IPs, secrets, URLs) that should be in `.envrc`.

**Violation**: Hardcoded IP `10.20.11.80` in terraform
**Fix**: Add to `.envrc` and `.envrc.example`, use `${VARIABLE_NAME}`

## Validation Process

1. Run `git status` for uncommitted changes
2. Read CLAUDE.md for status accuracy
3. Check for duplication between CLAUDE.md and docs/
4. Scan for hardcoded values
5. Report violations and offer fixes

## Quick Reference

**After completing work:**
1. Update docs/ files with new information
2. Update CLAUDE.md status and checkboxes
3. Check for duplication (AI reads both and compares)
4. Commit changes

**Validation command:** `/validate`
