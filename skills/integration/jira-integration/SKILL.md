---
name: jira-integration
description: "Agent Skill: Comprehensive Jira integration through lightweight Python scripts. AUTOMATICALLY TRIGGER when user mentions Jira URLs like 'https://jira.*/browse/*', 'https://*.atlassian.net/browse/*', or issue keys like 'PROJ-123'. Use when searching issues (JQL), getting/updating issue details, creating issues, transitioning status, adding comments, logging worklogs, managing sprints and boards, creating issue links, or formatting Jira wiki markup. If authentication fails, offer to configure credentials interactively. Supports both Jira Cloud and Server/Data Center with automatic authentication detection. By Netresearch."
---

# Jira Integration Skill

Comprehensive Jira integration through lightweight Python CLI scripts.

> **Note:** Run scripts from `skills/jira-communication/`, or use full paths from repo root.

## Auto-Trigger Patterns

**AUTOMATICALLY ACTIVATE** when user mentions:
- **Jira URLs**: `https://jira.*/browse/*`, `https://*.atlassian.net/browse/*`
- **Issue keys**: Pattern like `PROJ-123`, `NRS-4167`, `ABC-1`
- **Keywords**: "Jira issue", "Jira ticket", "search Jira"

## Authentication Failure Handling

**CRITICAL**: When authentication fails, DO NOT just display the error. Instead:

1. **Detect failure** - Look for "Missing required variable" or 401/403 responses
2. **Offer help** - Ask: "Would you like me to help configure Jira credentials?"
3. **Run interactive setup** - `uv run skills/jira-communication/scripts/core/jira-setup.py`

## Sub-Skills

| Skill | Purpose |
|-------|---------|
| `jira-communication` | API operations via Python CLI scripts |
| `jira-syntax` | Wiki markup syntax, templates, validation |

## Scripts Reference

### Core Operations
| Script | Purpose |
|--------|---------|
| `jira-setup.py` | Interactive credential setup |
| `jira-validate.py` | Verify connection |
| `jira-issue.py` | Get/update issue details |
| `jira-search.py` | Search with JQL |
| `jira-worklog.py` | Time tracking |
| `jira-attachment.py` | Download attachments |

### Workflow Operations
| Script | Purpose |
|--------|---------|
| `jira-create.py` | Create issues |
| `jira-transition.py` | Change status |
| `jira-comment.py` | Comments |
| `jira-link.py` | Issue links |
| `jira-sprint.py` | Sprint management |
| `jira-board.py` | Board operations |

## Syntax Note

Jira uses wiki markup, NOT Markdown. See `skills/jira-syntax/SKILL.md` for syntax guide.

---

> **Contributing:** https://github.com/netresearch/jira-skill
