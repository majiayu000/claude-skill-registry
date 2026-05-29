---
created_at: 2026-01-27T02:10:00+09:00
author: a@qmu.jp
type: refactoring
layer: [Config]
effort: 0.25h
commit_hash: f1670e0
category: Changed
---

# Extract story metrics skill from story-writer agent

## Overview

Extract the performance metrics calculation logic from story-writer agent into a dedicated skill with bash script. The agent will preload this skill for calculating commit counts, timestamps, duration, and velocity.

## Key Files

- `plugins/core/agents/story-writer.md` - Simplify to preload skill
- `plugins/core/skills/story-metrics/SKILL.md` - New skill definition (create)
- `plugins/core/skills/story-metrics/scripts/calculate.sh` - Bash script for metrics calculation (create)

## Implementation Steps

1. Create `plugins/core/skills/story-metrics/SKILL.md` with instructions for using the metrics script
2. Create `plugins/core/skills/story-metrics/scripts/calculate.sh` that:
   - Takes base branch as argument (default: main)
   - Calculates commit count: `git rev-list --count <base>..HEAD`
   - Gets first/last commit timestamps
   - Calculates duration in hours
   - Determines velocity unit (hours vs business days)
   - Outputs JSON with all metrics for easy parsing
3. Update `plugins/core/agents/story-writer.md`:
   - Add `skills: [story-metrics]` to frontmatter
   - Replace inline bash commands with reference to skill script
   - Keep narrative writing instructions in agent

## Considerations

- Script output should be JSON for reliable parsing
- Duration unit logic (hours vs business days) belongs in script
- Story narrative generation stays in agent (requires LLM reasoning)

## Final Report

Development completed as planned.
