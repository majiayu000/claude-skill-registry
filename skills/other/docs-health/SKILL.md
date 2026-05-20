---
name: docs-health
description: Check CLAUDE.md and skills file sizes and line counts
allowed-tools: Bash(wc *), Bash(stat *)
---

# Documentation Health Check

## CLAUDE.md
!`stat -f "Size: %z bytes" CLAUDE.md`
!`wc -l < CLAUDE.md | xargs -I{} echo "Lines: {}"`

## Skills (bytes)
!`wc -c .claude/skills/*/SKILL.md 2>/dev/null`

## Guidelines
- CLAUDE.md: Keep under 35k (warning at 40k)
- Skills: Load on-demand, so size is less critical
- If CLAUDE.md grows, move detailed content to skills
