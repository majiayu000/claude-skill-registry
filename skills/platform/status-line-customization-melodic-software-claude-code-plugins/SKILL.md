---
name: status-line-customization
description: Central authority for Claude Code status line configuration. Covers custom status line creation, /statusline command, status line settings (statusLine in settings.json), JSON input structure (model, workspace, cost, session info), status line scripts (Bash, Python, Node.js), terminal color codes, git-aware status lines, helper functions, and status line troubleshooting. Supports creating custom status lines, configuring status line behavior, and displaying contextual session information. Delegates 100% to docs-management skill for official documentation.
user-invocable: false
allowed-tools: Read, Glob, Grep, Skill
---

# Status Line Meta Skill

> ## 🚨 MANDATORY: Invoke docs-management First
>
> **STOP - Before providing ANY response about status line configuration:**
>
> 1. **INVOKE** `docs-management` skill
> 2. **QUERY** for the user's specific topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded
>
> **Skipping this step results in outdated or incorrect information.**
>
> ### Verification Checkpoint
>
> Before responding, verify:
>
> - [ ] Did I invoke docs-management skill?
> - [ ] Did official documentation load?
> - [ ] Is my response based EXCLUSIVELY on official docs?
>
> If ANY checkbox is unchecked, STOP and invoke docs-management first.

## Overview

Central authority for Claude Code status line configuration. This skill uses **100% delegation to docs-management** - it contains NO duplicated official documentation.

**Architecture:** Pure delegation with keyword registry. All official documentation is accessed via docs-management skill queries.

## When to Use This Skill

**Keywords:** status line, statusline, /statusline command, custom status line, status line configuration, statusLine setting, status line script, status line JSON input, model display, workspace info, cost tracking display, session info display, ANSI colors status line, git-aware status line, PS1-style prompt

**Use this skill when:**

- Creating custom status lines
- Configuring status line settings
- Understanding status line JSON input structure
- Writing status line scripts (Bash, Python, Node.js)
- Adding git information to status line
- Styling status lines with ANSI colors
- Troubleshooting status line issues
- Displaying model, cost, or workspace information

## Keyword Registry for docs-management Queries

Use these keywords when querying docs-management skill for official documentation:

### Status Line Fundamentals

| Topic | Keywords |
| --- | --- |
| Overview | "status line", "statusline", "custom status line" |
| Purpose | "status line purpose", "contextual information display" |
| Behavior | "status line update", "status line refresh rate" |

### Configuration Methods

| Topic | Keywords |
| --- | --- |
| Slash Command | "/statusline command", "statusline setup" |
| Settings | "statusLine setting", "settings.json statusLine" |
| Command Type | "statusLine type command", "status line command config" |
| Padding | "statusLine padding", "status line edge" |

### JSON Input Structure

| Topic | Keywords |
| --- | --- |
| Input Format | "status line JSON input", "statusline stdin JSON" |
| Model Info | "status line model", "model display_name", "model id" |
| Workspace Info | "status line workspace", "current_dir", "project_dir" |
| Session Info | "status line session_id", "transcript_path" |
| Cost Info | "status line cost", "total_cost_usd", "lines_added" |
| Version Info | "status line version", "output_style" |
| Context Usage | "used_percentage", "remaining_percentage", "context window usage", "context capacity" |

### Script Examples

| Topic | Keywords |
| --- | --- |
| Bash Scripts | "status line bash script", "statusline.sh" |
| Python Scripts | "status line python", "statusline python example" |
| Node.js Scripts | "status line nodejs", "statusline javascript" |
| Helper Functions | "status line helper functions", "statusline helpers" |

### Git Integration

| Topic | Keywords |
| --- | --- |
| Git-Aware Status | "git-aware status line", "git branch status line" |
| Git Branch Display | "status line git branch", "show git branch" |

### Styling and Display

| Topic | Keywords |
| --- | --- |
| ANSI Colors | "status line ANSI", "status line colors", "styling status line" |
| Emojis | "status line emojis", "status line icons" |
| Concise Display | "status line concise", "fit on one line" |

### Troubleshooting

| Topic | Keywords |
| --- | --- |
| Not Appearing | "status line not appearing", "statusline troubleshooting" |
| Executable Issues | "status line chmod", "script not executable" |
| Output Issues | "status line stdout", "statusline stderr" |
| Testing | "test status line script", "mock JSON input" |

## Quick Decision Tree

**What do you want to do?**

1. **Create a status line quickly** -> Query docs-management: "/statusline command", "statusline setup"
2. **Configure status line in settings** -> Query docs-management: "statusLine setting", "settings.json statusLine"
3. **Understand JSON input** -> Query docs-management: "status line JSON input", "statusline stdin JSON"
4. **Show model information** -> Query docs-management: "status line model", "model display_name"
5. **Show cost/usage** -> Query docs-management: "status line cost", "total_cost_usd"
6. **Add git branch** -> Query docs-management: "git-aware status line", "git branch status line"
7. **Write bash script** -> Query docs-management: "status line bash script", "statusline.sh"
8. **Write Python script** -> Query docs-management: "status line python", "statusline python example"
9. **Add colors** -> Query docs-management: "status line ANSI", "status line colors"
10. **Fix status line issues** -> Query docs-management: "statusline troubleshooting", "status line not appearing"

## Topic Coverage

### Status Line Configuration

- /statusline slash command for quick setup
- statusLine setting in settings.json
- Command type configuration
- Padding configuration (edge alignment)
- Script path specification

### JSON Input Data

- hook_event_name (always "Status")
- session_id (current session identifier)
- transcript_path (path to transcript file)
- cwd (current working directory)
- model object (id and display_name)
- workspace object (current_dir and project_dir)
- version (Claude Code version)
- output_style object (current style name)
- cost object (usage metrics)

### Cost Tracking Fields

- total_cost_usd (session cost)
- total_duration_ms (session duration)
- total_api_duration_ms (API call time)
- total_lines_added (lines added)
- total_lines_removed (lines removed)

### Script Implementation Patterns

- Bash with jq for JSON parsing
- Python with json module
- Node.js with JSON.parse
- Helper function patterns for complex scripts
- Reading from stdin
- Outputting to stdout (first line only)

### Git Integration Patterns

- Detecting git repository
- Reading current branch
- Branch display formatting
- Error handling for non-git directories

### Styling Approaches

- ANSI color code support
- Emoji usage for visual indicators
- Concise formatting (one line)
- Information density considerations

### Update Behavior

- Updates on conversation message changes
- 300ms rate limiting
- First line of stdout becomes status text
- ANSI color code preservation

## Delegation Patterns

### Standard Query Pattern

```text
User asks: "How do I create a custom status line?"

1. Invoke docs-management skill
2. Use keywords: "/statusline command", "custom status line"
3. Load official documentation
4. Provide guidance based EXCLUSIVELY on official docs
```

### Multi-Topic Query Pattern

```text
User asks: "I want a status line showing git branch and cost"

1. Invoke docs-management skill with multiple queries:
   - "git-aware status line", "git branch status line"
   - "status line cost", "total_cost_usd"
2. Synthesize guidance from official documentation
```

### Troubleshooting Pattern

```text
User reports: "My status line script isn't showing up"

1. Invoke docs-management skill
2. Use keywords: "statusline troubleshooting", "status line not appearing"
3. Check official docs for common issues
4. Guide user through troubleshooting steps
```

## Troubleshooting Quick Reference

| Issue | Keywords for docs-management |
| --- | --- |
| Status line not appearing | "statusline troubleshooting", "status line not appearing" |
| Script not executable | "status line chmod", "script not executable" |
| Wrong output | "status line stdout", "first line output" |
| JSON parsing errors | "status line JSON input", "jq parsing" |
| Colors not working | "status line ANSI", "terminal colors" |
| Git branch not showing | "git-aware status line", "git branch display" |
| Slow updates | "status line update", "rate limiting" |
| Settings not applied | "statusLine setting", "settings.json" |

## Repository-Specific Notes

This repository does not currently use custom status lines. Status line documentation is relevant for:

- Understanding status line customization options
- Potential custom status line creation for development workflows
- Understanding session information available via JSON input

When working with status line topics, always use the docs-management skill to access official documentation.

## Auditing Status Lines

This skill provides the validation criteria used by the `statusline-auditor` agent for formal audits.

### Audit Resources

| Resource | Location | Purpose |
| --- | --- | --- |
| Audit Framework | `references/audit-framework.md` | Query guides and scoring criteria |

### Scoring Categories

| Category | Points | Key Criteria |
| --- | --- | --- |
| Script Structure | 25 | Valid script, shebang, executable |
| JSON Handling | 25 | Correct JSON input parsing |
| Output Format | 25 | Proper terminal formatting, colors |
| Cross-Platform | 25 | Works on Windows, macOS, Linux |

**Thresholds:** 85+ = PASS, 70-84 = PASS WITH WARNINGS, <70 = FAIL

### Related Agent

The `statusline-auditor` agent (Haiku model) performs formal audits using this skill:

- Auto-loads this skill via `skills: status-line-customization`
- Uses audit framework and docs-management for rules
- Generates structured audit reports
- Invoked by `/audit-statuslines` command

### External Technology Validation

When auditing status line scripts that use external technologies (scripts, packages, runtimes), the auditor MUST validate claims using MCP servers before flagging findings.

**Technologies Requiring MCP Validation:**

- .NET/C# scripts: Validate with microsoft-learn + perplexity
- Node.js/npm packages: Validate with context7 + perplexity
- Python scripts/packages: Validate with context7 + perplexity
- Shell scripts: Validate with perplexity
- Any version-specific claims: ALWAYS validate with perplexity

**Validation Rule:**

Never flag a technology usage as incorrect without first:

1. Querying appropriate MCP server(s) for current documentation
2. Verifying with perplexity for recent changes (especially .NET 10+)
3. Documenting MCP sources in the finding

**Stale Data Warning:**

- microsoft-learn can return cached/outdated documentation
- ALWAYS pair microsoft-learn with perplexity for version verification
- Trust perplexity for version numbers and recently-released features

## References

**Official Documentation (via docs-management skill):**

- Primary: "statusline" documentation
- Related: "settings", "terminal-config", "output-styles"

**Repository-Specific:**

- Status line settings: `.claude/settings.json` (statusLine setting)
- Custom scripts: `~/.claude/statusline.sh` (user-level)

## Version History

- **v1.1.0** (2026-01-16): Added v2.1.6+ keyword registry entries
  - Added context usage fields (used_percentage, remaining_percentage)

- **v1.0.0** (2025-11-26): Initial release
  - Pure delegation architecture
  - Comprehensive keyword registry
  - Quick decision tree
  - Topic coverage for all status line features
  - Troubleshooting quick reference

---

## Last Updated

**Date:** 2026-01-16
**Model:** claude-opus-4-5-20251101
