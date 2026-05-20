---
name: update-history
description: Update .claude/HISTORY.md with entries for recent commits that changed agent infrastructure files. Use after committing changes to skills, agents, rules, hooks, or CLAUDE.md.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
hooks:
  Stop:
    - command: "bash .claude/hooks/log-skill-usage.sh update-history"
---

# Update Agent Infrastructure Change History

Spawn the `history-keeper` agent to process recent commits. The agent has the full workflow and constraints — no additional instructions needed.
