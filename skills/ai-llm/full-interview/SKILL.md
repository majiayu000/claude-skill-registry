---
name: full-interview
description: "Force full interview depth for this session. Use when user says '/full-interview' or 'full interview mode'."
allowed-tools: Read, AskUserQuestion, Task
---

# full-interview (Interview Depth Override)

You are setting the interview depth to FULL for this session.

## When To Use

- User says "/full-interview"
- User wants comprehensive requirements gathering
- Building greenfield project where missing requirements = rework

## Effect

This session will use **full interview depth**:
- All 13+ questions asked
- No Smart Bypass (even for "trivial" requests)
- No auto-delegation during interview
- Complete coverage of all topic categories

## Workflow

### 1. Acknowledge Depth Setting

```
Interview depth: FULL
- All questions will be asked
- No bypass, no shortcuts
- Complete requirements coverage
```

### 2. Invoke front-door

After acknowledging, immediately invoke the front-door skill with full depth context.

Use Task tool to spawn front-door:
```yaml
Task:
  subagent_type: general-purpose
  prompt: |
    INTERVIEW DEPTH: full

    Execute front-door skill with full interview depth.
    - Ask ALL questions (Q0-Q12 + domain-specific)
    - Do NOT bypass for any reason
    - Do NOT use auto-delegation during interview
    - Cover all topic categories before proceeding

    Start by asking what the user wants to build.
```

## Keywords

full-interview, full interview, comprehensive, all questions, thorough, detailed interview
