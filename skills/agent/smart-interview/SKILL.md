---
name: smart-interview
description: "Reset to smart interview depth (default). Use when user says '/smart-interview' or wants to reset interview mode."
allowed-tools: Read, AskUserQuestion, Task
---

# smart-interview (Interview Depth Override)

You are resetting the interview depth to SMART (default) for this session.

## When To Use

- User says "/smart-interview"
- User was in quick/full mode and wants to reset
- Starting fresh after changing context

## Effect

This session will use **smart interview depth** (the default):
- Auto-detect appropriate depth based on task
- Full depth for greenfield projects
- Shorter depth for modifications
- Bypass for truly trivial tasks (typos, renames)

## Smart Detection Logic

```
IF "new project" + no existing code:
  → Full depth (all questions)

ELIF "modify" + existing code found:
  → Medium depth (5-8 questions)

ELIF "micro" OR estimated <100 lines:
  → Quick depth (Q1, Q2, Q6, Q12)

ELIF bypass signals (typo, rename, explicit path + <10 lines):
  → Bypass with one triage question
```

## Workflow

### 1. Acknowledge Reset

```
Interview depth: SMART (reset to default)
- Will auto-detect appropriate depth
- Greenfield → full, Modify → medium, Micro → quick
```

### 2. Invoke front-door

Continue with standard front-door flow, which will use smart detection.

Use Task tool to spawn front-door:
```yaml
Task:
  subagent_type: general-purpose
  prompt: |
    INTERVIEW DEPTH: smart (default)

    Execute front-door skill with smart detection.
    Use the depth detection logic:
    - New project + no code → full depth
    - Modify existing → medium depth (5-8 questions)
    - Micro task → quick depth (Q1, Q2, Q6, Q12)

    Start by triaging the user's intent.
```

## Keywords

smart-interview, smart, default, reset, auto, normal
