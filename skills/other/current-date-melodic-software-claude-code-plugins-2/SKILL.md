---
name: current-date
description: Gets, checks, and verifies the current UTC date and time for unambiguous temporal reference. Use when starting tasks, verifying temporal context, ensuring date awareness before time-sensitive operations, or when incorrect date assumptions are detected.
allowed-tools: Bash
---

# Current Date

Get the current UTC date and time to ensure correct temporal context for all operations.

## CRITICAL EXECUTION REQUIREMENT

**This skill requires COMMAND EXECUTION, not assumption-based answers.**

When this skill loads, you MUST:

1. **EXECUTE** the bash command shown in Quick Start section below
2. **REPORT** the actual command output (not an assumed date)
3. **NEVER** state a date from memory or assumptions
4. **NEVER** skip execution thinking "I know the date"

**Why this matters:** This skill exists precisely because date assumptions are unreliable. Model training cutoffs, context issues, and stale information mean assumptions about "today" are frequently wrong. The ONLY reliable source is executing the date command and reporting actual output.

## Overview

This skill provides a simple, reliable way to verify the current date and time. It addresses situations where Claude Code or subagents may have incorrect assumptions about the current date due to model training cutoffs.

**Why a dedicated skill?**

- Date/time assumptions are unreliable due to model training cutoffs
- This skill enforces execution-based verification instead of guessing
- Essential for time-sensitive operations (deadlines, versioning, temporal ordering)

**What this skill does NOT do:**

- Time zone conversions
- Time arithmetic or duration calculations
- Date parsing or validation

## When to Use This Skill

**IMPORTANT**: This is an execution-only skill. Always run the command; never state dates from memory.

Use this skill when:

- Starting a new task or conversation
- Working on time-sensitive operations (deadlines, schedules, versioning)
- Verifying temporal context before making date-based decisions
- Correcting date misunderstandings during a conversation
- Needed by subagents to establish correct date context
- Creating timestamps or version numbers
- Writing documentation with "Last Verified" dates

## Quick Start

**Get current UTC date and time:**

```bash
date -u +"%Y-%m-%d %H:%M:%S UTC (%A)"
```

**Expected output:**

```text
2025-11-09 18:31:10 UTC (Sunday)
```

**Format explanation:**

- `2025-11-09` - ISO 8601 date format (YYYY-MM-DD)
- `18:31:10` - 24-hour time with seconds (UTC)
- `UTC` - Coordinated Universal Time
- `(Sunday)` - Day of week

**Execution Checklist:**

- [ ] Execute the command (don't assume the date)
- [ ] Verify output includes UTC timezone
- [ ] Report actual output (not paraphrased)

## Usage Patterns

### At Task Start

```bash
date -u +"%Y-%m-%d %H:%M:%S UTC (%A)"
# Then proceed with task...
```

### For Documentation

```bash
date -u +"%Y-%m-%d"
# Use for "Last Verified" dates
```

### For Timestamps

```bash
date -u +"%Y%m%d-%H%M%S"
# Use in filenames
```

## Best Practices

1. **Always use UTC**: Avoid timezone confusion
2. **Run at task start**: Verify date when beginning time-sensitive work
3. **Share with subagents**: Include current UTC date in Task agent prompts
4. **Use ISO 8601 format**: Unambiguous, internationally recognized

## Reference Loading Guide

**Load on demand based on context:**

| Reference | When to Load |
| --- | --- |
| [references/platform-alternatives.md](references/platform-alternatives.md) | Windows users, PowerShell needed |
| [references/format-reference.md](references/format-reference.md) | Need alternative output formats |
| [references/troubleshooting.md](references/troubleshooting.md) | Errors or issues occur |
| [references/testing/evaluations.md](references/testing/evaluations.md) | During skill testing or audit |
| [references/testing/model-notes.md](references/testing/model-notes.md) | Multi-model testing |

## Version History

- v1.3.0 (2025-11-25): Refactored to hub + references architecture
  - Extracted platform alternatives, format reference, troubleshooting to references/
  - Extracted evaluations and model testing notes to references/testing/
  - SKILL.md reduced from ~420 lines to ~140 lines (67% reduction)
- v1.2.0 (2025-11-19): Added Table of Contents, enhanced Overview
- v1.1.1 (2025-11-17): Added evaluations, multi-model testing notes
- v1.1.0 (2025-11-17): Added PowerShell alternatives, cross-platform docs
- v1.0.1 (2025-11-12): Added action verbs to description
- v1.0.0 (2025-11-09): Initial release

---

## Last Updated

**Date:** 2025-11-28
**Model:** claude-opus-4-5-20251101
