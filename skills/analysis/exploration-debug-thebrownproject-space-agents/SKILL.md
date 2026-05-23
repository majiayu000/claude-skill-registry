---
name: exploration-debug
description: "Interactive debugging through conversation. HOUSTON guides through 4 phases, asks questions, and suggests agents for investigation."
---

# /exploration-debug - Interactive Debugging

Debug issues through conversation. This is collaborative investigation, not a checklist. You guide through the 4 phases, ask questions, have opinions, and work toward root cause together.

## The Process

1. **Acknowledge issue, ask first question** - Don't jump to solutions
2. **Multi-round dialogue through 4 phases** - Adapt pace to complexity
3. **Suggest agents when useful** - "Want me to send an agent to trace X while we talk?"
4. **If agent spawned** - Continue talking, check results between questions with `TaskOutput block: false`
5. **Weave in results naturally** - Brief summaries, not dumps
6. **When root cause found** - Offer choice: fix now OR create bug Bead

## The Four Phases

Guide conversation through these phases. Don't rush - some issues need multiple rounds per phase.

### Phase 1: Understand the Issue

Ask about:
- What exactly is happening? (symptoms, error messages)
- Can you reproduce it? How consistently?
- What changed recently? (code, config, environment)
- When did it start?

**Red flags to watch for:**
- User already has a fix in mind - slow down, verify root cause first
- "It's probably X" - investigate, don't assume

### Phase 2: Gather Evidence

Ask about or investigate:
- Exact error messages and stack traces
- Logs around the failure point
- State of system when it fails
- What works vs what doesn't

**Suggest agent when:** You need to trace code paths, check logs, or gather evidence while continuing conversation.

### Phase 3: Find Root Cause

Ask about:
- Where does bad data originate?
- What's different between working and broken cases?
- Are there similar patterns elsewhere that work?

**Key principle:** Trace backward from symptom to source. Fix at source, not symptom.

### Phase 4: Resolution

When root cause is confirmed, ask user:

```
AskUserQuestion:
  "We've found the root cause. How do you want to proceed?"
  Options:
  - "Fix it now" - Apply the fix in this session
  - "Create bug Bead" - Track for /mission to handle later
  - "Need more investigation" - Continue exploring
```

**If fixing now:**
1. Create failing test case (use TDD)
2. Implement single fix addressing root cause
3. Verify fix works
4. Offer to create Bead to track the fix

**If creating Bead:**
1. Create bug issue with root cause analysis
2. Include reproduction steps, evidence gathered
3. Offer next step: `/mission` when ready to fix

## Your Role

- **Ask questions** - Understand before proposing
- **Have opinions** - "That sounds like X, let's verify"
- **Suggest agents, don't auto-spawn** - Always ask first
- **Guide through phases** - Don't let user jump to fixes without investigation
- **Keep talking** - Never wait silently for agent results

## Available Agents

Spawn with `run_in_background: true`, continue conversation immediately:

- `space-agents:debug` - Trace code paths, gather evidence, check logs

## AskUserQuestion (Required)

**Always use `AskUserQuestion`** for every question in debugging. Prefer multiple choice when you can anticipate likely answers.

## Red Flags - Slow Down

If you catch yourself or the user:
- Proposing fixes before understanding root cause
- "Just try X and see if it works"
- Skipping evidence gathering
- "It's obvious, let's just fix it"

**STOP. Return to Phase 1 or 2.**

## Output

When debugging reaches resolution:

**If fixed:** Offer to create task Bead to track the work done

**If creating bug Bead:** Use `bd create --type=bug` with:
- Clear title describing the issue
- Root cause analysis in description
- Reproduction steps
- Evidence gathered (logs, traces, etc.)
