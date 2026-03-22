---
name: audit-bugs
description: Analyze historical bug patterns by mining Claude Code project logs for /investigate skill invocations since a specified date. Identifies recurring root causes, architectural gaps, and proactive detection strategies. Use when user says "audit bugs", "bug patterns", "analyze investigations", or "bug audit".
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: audit-bugs] Mining investigation logs for bug patterns...'"
          once: true
---

# Bug Pattern Audit Skill

Mine Claude Code conversation logs for `/investigate` skill invocations to identify recurring bug patterns, architectural gaps, and proactive detection strategies.

## When to Use

- User says "audit bugs", "bug patterns", "analyze investigations", or "bug audit"
- User wants to find recurring themes across past bug investigations
- User wants proactive strategies to catch bugs before they manifest

## Arguments

The user may provide a "since" date (e.g., `2/7`, `2026-02-07`, `last week`). If not specified, use `AskUserQuestion` to ask what the earliest lookback date should be before proceeding.

## Critical Constraints

**NEVER:**
- Modify any source code files
- Create files outside `temp/audit-bugs/` directory

**ALWAYS:**
- Use subagents heavily for parallel log analysis
- All output goes under `temp/audit-bugs/` (create if needed)
- Final report: `temp/audit-bugs/bug_pattern_audit_{YYYY-MM-DD_HHMMSS}.md`
- Subagents must NOT create their own files - they return findings in their response text only
- Do not change any code

## Workflow

### Step 1: Locate Project Logs

Claude Code stores conversation logs at `~/.claude/projects/` in a folder derived from the project's absolute path with `/` replaced by `-`.

Derive the log directory:
```bash
# Convert current working directory to Claude's folder naming scheme
PROJECT_PATH=$(pwd)
LOG_DIR="$HOME/.claude/projects/-${PROJECT_PATH//\//-}"
# Remove leading double dash if present
LOG_DIR="${LOG_DIR//--/-}"
```

Verify the directory exists and contains `.jsonl` files.

### Step 2: Filter by Date and Investigate Skill

1. Use `find` with `-newermt` to filter `.jsonl` files modified since the target date
2. From those, `grep -l '"skill".*"investigate"'` to find files where the investigate skill was invoked (tool invocation pattern)
3. Also `grep -l '/investigate'` to catch user-typed invocations
4. Combine and deduplicate. Only use top-level files (not subagent logs under `*/subagents/`)

### Step 3: Dispatch Subagents for Parallel Analysis

Split the matching files into batches of ~5 and dispatch general-purpose subagents in parallel. Each subagent should extract from each log file:

- **Error/Symptom**: The error message or failure the user reported
- **Root Cause**: What the investigation identified as the root cause
- **Component**: Which module/system was affected
- **Category**: Bug classification (e.g., "type boundary", "state management", "validation gap")
- **Fix**: What solution was identified or applied

**Subagent instructions for reading logs:**
- JSONL format: each line is a JSON object
- `"type": "human"` entries contain user messages (error reports)
- `"type": "assistant"` entries with text content contain investigation findings
- Look for tool calls writing to `temp/investigate/investigation_*.md` or `temp/rectify/rectify_*.md` for structured findings
- Search for keywords: "root cause", "Root Cause", "fix", "summary", "finding"
- Read the first ~500 lines for context, then search for conclusions

### Step 4: Synthesize Patterns

After subagents return, group findings into recurring patterns:

1. Identify bugs that share the same root architectural weakness
2. Count frequency of each pattern across sessions
3. For each pattern, identify:
   - Which components it affects
   - Why it keeps recurring
   - What architectural gap enables it
   - Concrete grep/search patterns that could detect latent instances today

### Step 5: Write Report

Ensure `temp/audit-bugs/` exists (`mkdir -p`).

Save to: `temp/audit-bugs/bug_pattern_audit_{YYYY-MM-DD_HHMMSS}.md`

Structure:
```markdown
# Bug Pattern Audit: Investigations Since {date}

**Analysis Date:** {today}
**Sessions Analyzed:** {count}

## Executive Summary
{2-3 sentences: top patterns, frequency, recommended investments}

## Pattern N: {Name}
**Frequency:** X of Y sessions (Z%)

### Manifestations
| Session | Date | Bug | Component |
{table of affected sessions}

### Root Architectural Gap
{Why this pattern keeps occurring}

### Proactive Detection Strategy
{Concrete scans, tests, or grep patterns to find latent instances}

---

## All Sessions Quick Reference
| # | Session ID | Date | Error Summary | Pattern(s) |
{table of all sessions}

## Recommended Proactive Scans
{Runnable grep/rg commands to find latent bugs today}
```

### Step 6: Terminal Summary

Output a concise summary: pattern count, top 3 patterns by frequency, and report location.
