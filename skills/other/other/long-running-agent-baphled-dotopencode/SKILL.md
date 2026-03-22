---
name: long-running-agent
description: Multi-session agent harness for complex projects spanning many context windows — initialiser/coding agent cycle
category: Workflow Orchestration
---

# Skill: long-running-agent

## What I do

I provide the harness pattern for agents working on projects that span multiple context windows. Based on Anthropic's research, I define the initialiser/coding agent cycle that prevents the two most common long-running failures: one-shotting everything and declaring premature victory.

## When to use me

- Starting a complex project that will take multiple sessions
- When a task cannot be completed in a single context window
- When multiple agent instances will work on the same project sequentially
- When resumability across sessions is required

## Core principles

1. **Initialiser first** — The first session sets up scaffolding, not features
2. **Feature list in JSON** — Never Markdown (models overwrite MD, not JSON)
3. **One feature at a time** — Never attempt multiple features in one session
4. **Leave clean state** — Every session ends with a git commit and progress update
5. **Verify before declaring done** — Integration testing, not just unit tests

## The Two-Agent Pattern

### Initialiser Agent (first session only)

Prompt focus: "Set up the environment for future agents — do not implement features."

Creates:
- `feature_list.json` — All features, all initially `"passes": false`
- `claude-progress.txt` — Running log of what each session accomplished
- `init.sh` — Starts dev server + runs a basic smoke test (exits 0 on success)
- Initial git commit with all scaffolding

### Coding Agent (every subsequent session)

Prompt focus: "Make incremental progress on ONE feature, leave clean state."

**Session start ritual:**
1. `pwd` — confirm working directory
2. Read `claude-progress.txt` and `git log --oneline -20`
3. Read `feature_list.json` — find highest-priority failing feature
4. Run `init.sh` — verify app works before touching anything
5. Work on ONE feature only

**Session end ritual:**
1. Run integration tests (browser automation, not just unit tests)
2. Update `feature_list.json` — only change `passes` field, never remove entries
3. Append to `claude-progress.txt` — what was done, what is next
4. Git commit with descriptive message

## Feature List Format

Use JSON, never Markdown. Models are less likely to overwrite JSON files.

```json
{
  "features": [
    {
      "category": "functional",
      "priority": 1,
      "description": "User can log in with email and password",
      "steps": [
        "Navigate to /login",
        "Enter valid credentials",
        "Verify redirect to dashboard"
      ],
      "passes": false
    }
  ]
}
```

**Critical rules:**
- Never remove entries — only change `passes`
- Never mark `passes: true` without running the actual steps
- Instruct agents: "It is unacceptable to remove or edit features"

## Progress File Format

```
## Session 3 — 2026-02-20
Agent: Senior-Engineer
Feature: User login (#1)
Status: COMPLETE — passes: true
Next: Password reset flow (#2)
Issues: None
```

## Anti-patterns to avoid

- ❌ Attempting multiple features in one session
- ❌ Using Markdown for feature tracking (models overwrite it)
- ❌ Marking features complete without integration testing
- ❌ Starting a session without reading progress file + git log
- ❌ Leaving broken code at end of session
- ❌ Declaring project done based on visual inspection alone


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Agent-Guidance/Long Running Agent.md`

## Related skills

- `task-tracker` — Per-session task management
- `memory-keeper` — Cross-session knowledge persistence
- `git-master` — Commit discipline between sessions
- `playwright` — Integration testing for web apps
- `checklist-discipline` — Rigorous feature status updates
- `context-efficient-tools` — Keep tool results lean across sessions
