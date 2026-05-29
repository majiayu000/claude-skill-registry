---
name: crisp-orchestrator
description: CRISP session manager — detects project state and routes to the right phase. Use /crisp to start or resume any CRISP engagement. Reads docs/crisp-state.json to know where you are. Falls back to Phase C if no state exists.
---

# CRISP — Session Orchestrator

Before doing anything else, output this exact text verbatim:

  C — Clarify  ·  R — Results  ·  I — Investigate
        S — Spec  ·  P — Prove

        Outcome first. Always.

---

## Step 1: Detect project state

Check if `docs/crisp-state.json` exists.

---

### If `docs/crisp-state.json` does NOT exist → New project

This is a fresh engagement. Start exactly as `/crisp-start` does:

- Copy `templates/crisp-state.json` to `docs/crisp-state.json`
- Read `.claude/skills/phase1-clarify/SKILL.md`
- Begin Phase C immediately with:

> "Tell me about the project — what are you trying to solve, or what did the client brief say?"

Do not explain the methodology. Do not list the phases. Do not narrate what you're about to do. Just ask.

---

### If `docs/crisp-state.json` EXISTS → Resuming a project

Read `docs/crisp-state.json`. Then do the following:

**1. Report current status**

Print a brief status block:

```
Project: [project.name] · Client: [project.client]
─────────────────────────────────────────
Phases complete: [phases.complete joined with " · " — or "None" if empty]
Current phase:   [phases.current]
─────────────────────────────────────────
```

Then summarise the state of the current phase in 2-3 lines. Pull from the relevant `phases.[X]` fields. For example:
- Phase C: "Problem defined as [oneSentence]. Go/No-Go: [goNoGo]. Type: [type]."
- Phase R: "Baseline: [baseline]. Target: [successTarget]. [N] HITL zones defined."
- Phase I: "Process track: [processTrack]. User types: [userTypes]. Data mapping: [dataMappingRequired]."
- Phase S: "[sprintCount] sprints planned. Stack: [stack.layers summary]."
- Phase P: "Outcome: [outcome]."

If the current phase has open questions, list them:
> "Open questions in this phase: [phases.[X].openQuestions]"

**2. Ask what to do next**

> "Want to continue with Phase [current], jump to a specific phase, or start a new project?"

Wait for their answer.

**3. Route accordingly**

| User says | Action |
|---|---|
| Continue / yes / Phase [X] | Read the relevant phase SKILL.md and proceed |
| New project | Reset — ask if they want to overwrite state or create a new docs/ folder |
| Show me the full state | Print the full crisp-state.json in a readable format |
| What's left to do | List incomplete phases and open questions across all phases |

---

## Phase routing

| Phase | Skill to load |
|---|---|
| C — Clarify | `.claude/skills/phase1-clarify/SKILL.md` |
| R — Results | `.claude/skills/phase2-results/SKILL.md` |
| I — Investigate | `.claude/skills/phase3-investigate/SKILL.md` |
| S — Spec | `.claude/skills/phase4-spec/SKILL.md` |
| P — Prove | `.claude/skills/phase5-prove/SKILL.md` |

Load the relevant SKILL.md and follow it from the beginning. Do not summarise or abbreviate the phase — run it fully.

---

## Rules

- Never skip a phase without explicit user instruction.
- If a phase is marked complete in `crisp-state.json` but the user wants to re-run it — allow it, but flag: *"Phase [X] is marked complete. Running it again won't reset the state automatically — update crisp-state.json manually if needed."*
- If `crisp-state.json` has open questions — surface them before starting the next phase, not after.
- If phases are out of order (e.g. S is complete but R is not) — flag it: *"Phase R isn't marked complete yet. Running Phase S without it means some pre-fills will be missing. Continue anyway?"*
- Keep responses tight. Status reporting is a tool, not a presentation.
