---
name: planning
description: |
  Planning lifecycle umbrella: spec, pre-plan ambiguity resolution, file-backed
  planning, plan validation, plan-lifecycle management, and session pause/resume.
  Use for "write spec", "define requirements", "before we plan", "discuss
  ambiguities", "create plan", "task plan", "working memory", "check plan",
  "validate plan", "is this plan ready", "list plans", "plan status",
  "complete plan", "pause", "save progress", "session handoff", "resume",
  "continue work", or "where did I leave off".
user-invocable: true
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Skill
routing:
  force_route: true
  not_for: "city/financial/meeting/travel planning; and personal prioritization like 'what should I work on next' — that is productivity. Only for software task planning, specs, and plan-lifecycle management."
  triggers:
    - "write spec"
    - "user stories"
    - "define requirements"
    - "scope this"
    - "what should this do"
    - "acceptance criteria"
    - "define scope"
    - "spec out"
    - "discuss ambiguities"
    - "resolve gray areas"
    - "clarify before planning"
    - "assumptions mode"
    - "what are the gray areas"
    - "before we plan"
    - "pre-planning discussion"
    - "interview me"
    - "grill me"
    - "depth-first review"
    - "depth-first interview"
    - "not sure"
    - "i'm not sure"
    - "not exactly sure"
    - "unsure"
    - "where do i start"
    - "where do i even start"
    - "want clarity on"
    - "need clarity on"
    - "what am i missing"
    - "poke holes in"
    - "challenge my assumptions"
    - "think this through with me"
    - "lots of moving parts"
    - "many decisions"
    - "create plan"
    - "task plan"
    - "working memory"
    - "persistent plan"
    - "file-backed planning"
    - "check plan"
    - "validate plan"
    - "plan checker"
    - "review plan"
    - "is this plan ready"
    - "plan-checker"
    - "pre-execution check"
    - "list plans"
    - "show plan"
    - "complete plan"
    - "plan status"
    - "manage plans"
    - "pause"
    - "save progress"
    - "handoff"
    - "stopping for now"
    - "end session"
    - "pick this up later"
    - "session handoff"
    - "wrap up session"
    - "resume"
    - "continue"
    - "pick up where I left off"
    - "what was I doing"
    - "continue work"
    - "where did I leave off"
    - "what's next"
  category: process
  complexity: medium
  pairs_with:
    - workflow
    - feature-lifecycle
    - decision-helper
---

# Planning Skill

Umbrella skill for the planning lifecycle. Routes to the correct reference based on the intent requested: write a spec, resolve ambiguities before planning, create a file-backed plan, validate a plan, manage plan lifecycle, pause a session, or resume from handoff artifacts.

## Routing

Detect the user's intent and load the appropriate reference file:

| Intent | Trigger phrases | Reference |
|--------|----------------|-----------|
| **Spec** | "write spec", "user stories", "define requirements", "scope this", "acceptance criteria", "define scope", "spec out" | `${CLAUDE_SKILL_DIR}/references/spec.md` |
| **Pre-plan** | "discuss ambiguities", "resolve gray areas", "clarify before planning", "assumptions mode", "before we plan", "pre-planning discussion" | `${CLAUDE_SKILL_DIR}/references/pre-plan.md` |
| **Interview** | depth-first decision-tree, one question at a time, recommendation per question. Triggers: "interview me", "grill me", "depth-first review", "depth-first interview", "not sure", "i'm not sure", "where do i start", "want clarity on", "need clarity on", "what am i missing", "poke holes in", "challenge my assumptions", "think this through with me", "lots of moving parts", "many decisions" | `${CLAUDE_SKILL_DIR}/references/depth-first-interview.md` |
| **Plan-files** | "create plan", "task plan", "working memory", "persistent plan", "file-backed planning" | `${CLAUDE_SKILL_DIR}/references/plan-files.md` |
| **Check** | "check plan", "validate plan", "plan checker", "review plan", "is this plan ready", "pre-execution check" | `${CLAUDE_SKILL_DIR}/references/check.md` |
| **Manage** | "list plans", "show plan", "complete plan", "plan status", "manage plans" | `${CLAUDE_SKILL_DIR}/references/manage.md` |
| **Pause** | "pause", "save progress", "handoff", "stopping for now", "end session", "session handoff", "wrap up session" | `${CLAUDE_SKILL_DIR}/references/pause.md` |
| **Resume** | "resume", "continue", "pick up where I left off", "what was I doing", "continue work", "where did I leave off", "what's next" | `${CLAUDE_SKILL_DIR}/references/resume.md` |

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| "write spec", "user stories", "define requirements", "scope this", "acceptance criteria", "define scope", "spec out" | `spec.md` | **Spec** |
| "discuss ambiguities", "resolve gray areas", "clarify before planning", "assumptions mode", "before we plan", "pre-planning discussion" | `pre-plan.md` | **Pre-plan** |
| "interview me", "grill me", "depth-first review", "depth-first interview", "not sure", "i'm not sure", "where do i start", "want clarity on", "need clarity on", "what am i missing", "poke holes in", "challenge my assumptions", "think this through with me", "lots of moving parts", "many decisions" | `depth-first-interview.md` | **Interview** |
| "create plan", "task plan", "working memory", "persistent plan", "file-backed planning" | `plan-files.md` | **Plan-files** |
| "check plan", "validate plan", "plan checker", "review plan", "is this plan ready", "pre-execution check" | `check.md` | **Check** |
| "list plans", "show plan", "complete plan", "plan status", "manage plans" | `manage.md` | **Manage** |
| "pause", "save progress", "handoff", "stopping for now", "end session", "session handoff", "wrap up session" | `pause.md` | **Pause** |
| "resume", "continue", "pick up where I left off", "what was I doing", "continue work", "where did I leave off", "what's next" | `resume.md` | **Resume** |

## Instructions

1. Identify the user's planning task from their message
2. Load the matching reference file from the table above
3. Follow the instructions in that reference file exactly
