---
name: handoff
description: This skill is designed to bridge context between agents during a transition.
  It uses the philosophy of the /assess skill to generate a structured local/HANDOFF.md
  that helps a new agent understand the project's current state, what is working,
  what is broken, and what to do next.
---

---
name: handoff
description: >
  Handoff skill to assess project state and provide context for a new agent.
  Uses /assess logic to identify doc-code gaps, broken features, and next steps.
allowed-tools: Bash, Read, Grep, Glob
triggers:
  - handoff this project
  - prepare context for next agent
  - create handoff report
  - what is the status for a new agent
  - help me onboard another agent
  - give me project context
  - context check
metadata:
  short-description: Handoff briefing and project context bridge

provides:
  - handoff
composes: [, task-monitor]
---

# Handoff Skill

This skill is designed to bridge context between agents during a transition. It uses the philosophy of the `/assess` skill to generate a structured `local/HANDOFF.md` that helps a new agent understand the project's current state, what is working, what is broken, and what to do next.

## Assessment Logic (via /assess)

When triggering this skill, the agent must:

1. **Gather Facts**: Run `.pi/skills/handoff/run.sh` to get automated project data (git, docs, todos).
2. **Analyze Alignment**: Compare `README.md` and `CONTEXT.md` against the actual code.
3. **Identify "Current Broken"**: Locate failed tests, `TODO`s, and recent bug-related commits.
4. **Determine Next Steps**: Review `0N_TASKS.md` (if exists) and recently touched files.

## Output Format: HANDOFF.md

The agent should generate or update a `local/HANDOFF.md` file using the following structure:

```markdown
# Handoff Report: <Project Name>

**Timestamp**: <ISO Date>
**Active Agent**: <Current Agent Name>

## 1. Project Overview

- **Ecosystem**: <Python/Node/etc>
- **Core Purpose**: <Brief summary from README>

## 2. Current State (Doc-Code Alignment)

- **Documented Features**: <List>
- **Implemented Reality**: <Note any gaps>
- **Drift/Misalignments**: <Flag differences between docs and code>

## 3. What is Working Well

- <List passing critical paths or high-quality modules>

## 4. What is Currently Broken

- **Failed Tests**: <List>
- **Known Issues**: <From /assess findings or TODOs>
- **Recent Regressions**: <From git history>

## 5. Next Steps

1. <Highest priority task>
2. <Next task>

## 6. Project Context for Success

- **Key Files**: <Paths to core logic>
- **Recent Changes**: <Summary of last 3-5 commits>
```

## How to Use

1. Trigger with "create handoff report" or "handoff this project".
2. Run `bash .pi/skills/handoff/run.sh`.
3. Perform a supplemental `/assess` deep dive if needed.
4. **Prepare Environment**: Ensure the `local/` directory exists (create it if missing).
5. **Synthesize Findings**: Generate or update `local/HANDOFF.md` using the collected facts and `/assess` philosophy.
6. Present the summary to the user.
