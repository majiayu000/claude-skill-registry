---
name: discover
description: >-
  Phase 1 of the prd-taskmaster pipeline: brainstorm-driven discovery. Delegates
  to superpowers:brainstorming in Interactive Mode (one adaptive question at a
  time), or self-brainstorms in Autonomous Mode when no user is present.
  Intercepts before the brainstorming chain hands off to writing-plans — this
  skill owns the exit. Extracts constraints, calibrates scale
  (Solo / Team / Enterprise), and advances the pipeline to GENERATE.
user-invocable: false
allowed-tools:
  - Read
  - Skill
  - AskUserQuestion
  - Write
  - ToolSearch
  - mcp__atlas-engine
  - mcp__plugin_prd_go
  - mcp__plugin_prd-taskmaster_go
  - mcp__plugin_atlas-go_go
---

# Phase 1: Discover

Declarative phase skill. Invoked by the prd-taskmaster orchestrator when
`current_phase` is `DISCOVER`. Never called directly by a user.

The one rule: **invoke `superpowers:brainstorming` for discovery, intercept
before it chains to `writing-plans` — we control the exit, not the brainstorm
skill.**

## Entry gate

1. Call `mcp__plugin_prd_go__check_gate(phase="DISCOVER", evidence={})`.
   If the call returns `{gate_passed: false, violations: [...]}`, report the
   violations and stop. The gate protects against re-entering a completed
   phase or skipping ahead from SETUP.

   **Known issue (Mum dogfood feedback [4]):** check_gate is structurally
   an EXIT gate. On first DISCOVER entry, evidence=`{}` will fail the
   `user_approved=true OR auto_classification=CLEAR with assumptions_documented`
   requirement (which the User Approval Gate / Self-Approval Gate below
   produces). State machine LEGAL_TRANSITIONS already prevents illegal
   entry — proceed past this gate on first entry. Semantic fix in flight
   (see morning brief).
2. Detect execution context. If any of the following signals are present,
   switch to Autonomous Mode:
   - `.claude/ralph-loop.local.md` exists in the project root
   - An `auto-enter` / `auto-approve` daemon is running against this session
   - The skill was invoked with an explicit `--autonomous` flag
   - Parent orchestrator is a cron, `/pentest-wtf`, or `/ralph-loop`
   Otherwise proceed in Interactive Mode (default).

## Discovery checklist

Copy into your response before running the procedure:

```
DISCOVERY CHECKLIST:
- [ ] Mode detected (Interactive vs Autonomous)
- [ ] Goal captured from skill args or soul purpose
- [ ] Adaptive questions completed (one at a time)
- [ ] Constraints extracted and listed
- [ ] Scale classified (Solo / Team / Enterprise)
- [ ] Discovery summary captured for GENERATE phase
- [ ] User approved (Interactive) or summary committed (Autonomous)
```

## Interactive Mode (default — user present)

1. Take the user's goal / description from the skill invocation args.
2. Invoke `superpowers:brainstorming` with the goal as input.
3. Brainstorming runs its adaptive question flow — one domain-agnostic question
   at a time. Let it drive the Q&A rhythm.
4. **INTERCEPT POINT**: when brainstorming signals readiness to chain to
   `writing-plans`, STOP. Do NOT let it invoke `writing-plans`. Capture the
   brainstorm output (design, requirements, decisions) into local state
   instead. The prd-taskmaster orchestrator owns the handoff — not
   `superpowers:brainstorming`.
5. Present the summary to the user for approval via `AskUserQuestion` (see
   User Approval Gate below).

## Autonomous Mode (no user present)

**Do NOT invoke `superpowers:brainstorming`** — it blocks on user input and
will stall an unattended session. Instead, self-brainstorm using this
template:

1. Read the goal statement from skill args or
   `session-context/CLAUDE-soul-purpose.md`.
2. Read `session-context/CLAUDE-activeContext.md` for project context.
3. Write discovery notes directly to
   `session-context/discovery-{timestamp}.md` answering every question the
   interactive flow would ask:
   - Who is this for?
   - What problem does it solve?
   - What are the success metrics?
   - What are the constraints (tech stack, timeline, team, budget,
     integrations, regulatory)?
   - What's explicitly out of scope?
   - What's the scale (Solo / Team / Enterprise)?
4. Self-approve: the skill acts as both interrogator and approver. Document
   assumptions explicitly so the user can audit them on wake-up.
5. Commit the discovery file. The git history becomes the audit trail — if
   the user later disagrees, they can reset to that commit and re-run.

**Autonomous mode is first-class, not degraded.** A well-run autonomous
discovery produces a spec the user reads on wake-up and says "yes, that's
what I meant" without edits. If you find yourself needing to ask more than
two questions the user didn't anticipate, the discovery is under-specified —
stop and write a handoff note instead of proceeding.

## User Approval Gate (Interactive Mode)

After brainstorming completes, present via `AskUserQuestion`:

```
Discovery Complete:
  Goal: [one sentence]
  Audience: [who it's for]
  Approach: [proposed solution]
  Key decisions: [list]
  Constraints: [known limitations]
  Scale: [Solo | Team | Enterprise]

Proceed to generate spec? (or refine further)
```

- If user says "refine" → ask what to change, update the summary, re-present.
- If user approves → capture as the discovery output and proceed to exit gate.

## Self-Approval Gate (Autonomous Mode)

Write the discovery summary to `session-context/discovery-{timestamp}.md` and
commit it. No interactive approval is required, but assumptions MUST be
explicit in the written summary so the user can audit on wake-up.

## Smart Defaults

If brainstorming (or self-brainstorming) produces thin answers, fill gaps
with reasonable assumptions instead of forcing extra questions:

- Target audience: small team (< 10 users) unless specified otherwise.
- Timeline: MVP in 4–6 weeks.
- Tech stack: inferred from requirements — do not pick arbitrarily.
- Scale: moderate (hundreds of users, not millions).

Document every assumption in the discovery summary so GENERATE can surface
them in the spec.

## Constraint Extraction (MANDATORY before advancing)

Before moving to GENERATE, explicitly extract and list all constraints
mentioned during discovery. Emit this block:

```
CONSTRAINTS CAPTURED:
- Tech stack: [e.g., "must use Python", "React frontend", "no new dependencies"]
- Timeline: [e.g., "MVP in 2 weeks", "no deadline"]
- Team: [e.g., "solo developer", "3-person team"]
- Budget: [e.g., "free tier only", "$500/month max"]
- Integration: [e.g., "must work with existing Postgres DB", "connects to Stripe"]
- Regulatory: [e.g., "HIPAA compliant", "GDPR", "none specified"]
- Domain-specific: [e.g., "authorized pentest scope: 10.0.0.0/24 only",
  "learning goal: intermediate level"]
```

Present this list alongside the discovery summary. These constraints MUST be
passed to GENERATE — they inform spec content, task decomposition depth, and
acceptance criteria. If a constraint is mentioned in discovery but missing
from the spec, that's a bug.

## Scope Calibration

Infer project scale from discovery answers and set decomposition guidance:

| Scale      | Signal                                          | Task Cap    | Subtask Depth    |
|------------|-------------------------------------------------|-------------|------------------|
| Solo       | "just me", "side project", "learning"           | 8–12 tasks  | 2–3 subtasks each |
| Team       | "small team", "MVP", "product", "startup"       | 12–20 tasks | 3–5 subtasks each |
| Enterprise | "compliance", "multiple teams", "platform"      | 20–30 tasks | 5–8 subtasks each |

Pass the scale classification to GENERATE so task count is calibrated, not
arbitrary.

## Exit gate

After approval (Interactive) or commit (Autonomous), constraints captured,
and scale classified:

1. Call `mcp__plugin_prd_go__advance_phase(expected_current="DISCOVER", target="GENERATE", evidence={"user_approved": True, "constraints_captured": True, "scale": "<Solo|Team|Enterprise>", "assumptions_documented": True})`.
   The call atomically transitions `pipeline.json` from DISCOVER to GENERATE.
   The `expected_current` field is the compare-and-swap guard;
   `evidence` is stored under `phase_evidence[GENERATE]` for audit.
2. Return control to the orchestrator (`prd-taskmaster` skill). Do NOT invoke
   GENERATE directly — the orchestrator re-reads `current_phase` and routes.

## Red flags (stop and report, do not paper over)

- "Brainstorming wants to call writing-plans — I'll let it" → NO. Intercept.
  The prd-taskmaster pipeline owns the exit, not `superpowers:brainstorming`.
- "User hasn't answered, I'll pick for them in Interactive Mode" → NO. If
  stalled, ask one more targeted question or write a handoff note — don't
  silently self-approve in Interactive Mode.
- "Autonomous mode — I'll invoke superpowers:brainstorming anyway" → NO.
  It blocks on user input and will stall the session. Self-brainstorm with
  the template above.
- "Constraints are obvious, I'll skip the CONSTRAINTS CAPTURED block" → NO.
  GENERATE reads this block — missing constraints become missing spec
  sections downstream.
- "I can call advance_phase without check_gate" → NO. Gate first, always.

## Non-exits

This skill does not use explicit process termination. A hard block reports
the reason and returns control to the orchestrator; the orchestrator decides
whether to surface to the user.
