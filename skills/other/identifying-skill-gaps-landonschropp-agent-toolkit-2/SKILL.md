---
name: identifying-skill-gaps
description: Use when analyzing Claude Code conversation logs to find patterns in repeated user instructions that could become skills. Ask for date range first.
---

# Identifying Skill Gaps

Analyze Claude Code conversation logs to identify areas where the user repeatedly gives similar instructions that could be turned into skills.

## Step 1: Ask for Date Range

**FIRST**: Ask the user what date range they want to analyze.

Example: "What date range would you like me to analyze? (e.g., December 1-15, 2024)"

## Step 2: Extract User Messages

Claude Code stores conversation logs in `~/.claude/projects/` as JSONL files.

**NEVER assume logs aren't accessible.** They ARE stored locally.

Run the extraction script with the date range:

```bash
scripts/extract-user-messages.ts --after YYYY-MM-DD
```

This filters out tool calls, assistant responses, and metadata—keeping only what the user said.

## Step 3: Analyze for Patterns

Analyze the output and apply the waste analysis framework from [references/wastes.md](references/wastes.md).

1. **Apply each lens** to identify waste patterns
2. **Look for repetition across conversations** - the same waste appearing multiple times signals high-value skill opportunities
3. **Quantify the waste** - count how many messages/characters users spend on each pattern
4. **Prioritize by frequency and cost** - repeated, lengthy wastes are the best skill candidates

**What counts as a pattern**: The user giving similar instructions in 3+ separate conversations.

Focus on identifying waste where users repeatedly spend conversation time on things that could be eliminated by a skill.

## Step 4: Output Prioritized List

Create a markdown list with:

```markdown
## Potential Skills

### 1. [Skill Name] - HIGH PRIORITY

**Frequency**: Found in [X] conversations
**Rationale**: [Why this would be useful]
**Example instructions**:

- "[Quote from conversation]"
- "[Another quote]"

### 2. [Skill Name] - MEDIUM PRIORITY

...
```

**Priority levels**:

- HIGH: 5+ occurrences, affects workflow significantly
- MEDIUM: 3-4 occurrences, clear pattern
- LOW: 2 occurrences, worth noting
