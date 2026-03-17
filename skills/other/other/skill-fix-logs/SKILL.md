---
name: skill-fix-logs
version: 1.0.0
description: '[Skill Management] Fix the agent skill based on `logs.txt` file.'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Fix a skill based on error analysis from its `logs.txt` file.

**Workflow:**
1. **Read** — Analyze the skill's `logs.txt` for errors and failures
2. **Diagnose** — Identify root cause of skill malfunction
3. **Fix** — Apply corrections to SKILL.md, scripts, or references

**Key Rules:**
- Delegates to `skill-creator` for fix patterns
- Focus on the specific errors reported in logs
- Test the fix by running the skill again

Think harder.
Use `skill-creator` and `claude-code` skills.
Use `docs-seeker` skills to search for documentation if needed.

## Your mission

Fix the agent skill based on the current `logs.txt` file (in the project root directory).

## Requirements

<user-prompt>$ARGUMENTS</user-prompt>

## Rules of Skill Fixing:

Base on the requirements:

- If you're given nothing, use `AskUserQuestion` tool for clarifications and `researcher` subagent to research about the topic.
- If you're given an URL, it's documentation page, use `Explorer` subagent to explore every internal link and report back to main agent, don't skip any link.
- If you receive a lot of URLs, use multiple `Explorer` subagents to explore them in parallel, then report back to main agent.
- If you receive a lot of files, use multiple `Explorer` subagents to explore them in parallel, then report back to main agent.
- If you're given a Github URL, use [`repomix`](https://repomix.com/guide/usage) command to summarize ([install it](https://repomix.com/guide/installation) if needed) and spawn multiple `Explorer` subagents to explore it in parallel, then report back to main agent.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
