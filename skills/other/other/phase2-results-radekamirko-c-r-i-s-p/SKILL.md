---
name: phase2-results
description: The Mileva Method (CRISP) — Phase 2: Results. Outcome alignment, stakeholder register, baseline measurement, success metrics, tradeoff negotiation. Use after problem definition is complete. Triggers on "results", "phase 2", "define success", "success metrics", "what does done look like", or after Phase C exit checklist is complete.
---

# R — Results: Outcome Alignment

> "We don't know if we succeeded unless we defined what success looks like before we started."

## Project State

> At the start of Phase R: read `docs/crisp-state.json`. Check `phases.C` is complete. Use `phases.C.oneSentence`, `phases.C.constraints`, and `project.type` for context — do not re-read all Phase C docs from scratch.
>
> At the end of Phase R (before exit checklist): update `docs/crisp-state.json`:
> - Set `phases.current` to `"I"`
> - Add `"R"` to `phases.complete`
> - Set `phases.R.complete` to `true`
> - Fill `phases.R.baseline`, `phases.R.successTarget`, `phases.R.hitlZones`, `phases.R.stakeholders`
> - Add any unresolved items to `phases.R.openQuestions`

Do not discuss solutions or architecture until this phase is complete.

## Step 1: Stakeholder Register — Pre-fill, Elicit, Confirm

Do not open a blank register and ask "who are the stakeholders?" — you already have what you need to start.

**Pre-fill from existing docs:**

| Register section | Source |
|---|---|
| Primary users | `docs/problem-statement.md` — who the problem belongs to |
| Adjacent teams / employees | `docs/problem-statement.md` — business context, who touches the process |
| External users / customers | `docs/value-proposition-canvas.md` — customer profile (external projects) |
| Impact per stakeholder | `docs/problem-statement.md` — what changes for each group when the problem is solved |
| Human-in-the-loop zones | `docs/problem-statement.md` — constraints; `docs/swot.md` — threats (external) |

Draft the register, then work through it with three elicitation moves before confirming:

**Move 1 — Surface the hidden stakeholders**
> "Here's everyone I see being affected. [Primary user], [adjacent team], [sponsor]. Before we go further — who else touches this process, even occasionally? The person who only shows up when something goes wrong. The team that gets the output but has no say in the input."

People forget about downstream consumers, compliance reviewers, support staff. Get them on the register now.

**Move 2 — Challenge the impact ratings**
For each stakeholder, name the impact and let them push back:
> "I've marked [team X] as neutral — they're not doing the work differently, just receiving better output. Does that feel right, or are there ways this actually makes their life harder before it gets better?"

Neutral is often wrong. Changes create transition friction even when the end state is better. Flush that out.

**Move 3 — Elicit the HITL zones**
> "For each of these groups — where in this process would you be uncomfortable with a fully automated decision? Where does a human need to stay in the loop, even if the AI could technically handle it?"

Don't pre-fill HITL zones — let the client name them. Their discomfort is the signal, not your inference.

Confirm the completed register:
> "Here's the full picture. Does anything feel wrong before we lock this and move to baselines?"

Save to `docs/stakeholder-register.md`

---

## Step 2: Baseline Measurement

Measure the current state before anything is built. This is the "before" that Phase P will measure against.

- Time to complete the action
- Cost / money spent on process
- Error rate / rework frequency
- Frustration level (survey or 1-10 interview score)
- Tools used, open tabs, manual steps — the "friction inventory"

Pre-fill what you can from Phase C process walkthrough and constraints. Ask the client to fill any gaps:
> "I've estimated the current baseline at [X time / Y cost / Z errors]. Does that match your experience, or are you seeing different numbers?"

> If you can't measure the baseline, you can't prove the outcome.

> **The Jokić principle:** Nikola Jokić is the least athletic MVP in NBA history. He just sees the floor better than anyone. Baseline measurement is seeing the floor. Nobody wants to do it. It's unglamorous, slow, and the client always thinks it's unnecessary. Do it anyway. It's what separates builders who prove their value from builders who hope the client forgets to measure.

Save to `docs/success-metrics.md` (Baseline Measurements section)

---

## Step 3: Desired Projection

Define where metrics should land post-implementation.

Pre-fill with reasonable targets derived from:
- Phase C ROI / gains identified
- Market research benchmarks (external projects)
- Industry standards for the problem type

Then present:
> "Based on what you told me in Phase C, I'd expect this to get us to [X% improvement / Y time / Z cost]. Does that feel ambitious enough, or are you aiming higher?"

- Prefer relative metrics (% improvement) over absolute values
- Map second-order effects — one metric often has downstream impact
  > "Checkout <1min" → reduces cart abandonment → increases revenue
- Set both quantitative and qualitative targets

Save to `docs/success-metrics.md` (Success Targets + Second-Order Effects sections)

---

## Alignment Negotiation

Client sponsor speaks money and risk — use that language.
- Present tradeoffs explicitly: metric target ↑ = scope/budget/timeline ↑
- Flag human-in-the-loop zones proactively (legal, security, high-stakes)
- *"Everything is possible. Not everything is worth it. Here's what each option costs."*
- Iterate until aligned — do not proceed without sign-off

> **Watch for inat.** In Serbia we have a word: inat — stubborn spite so pure someone would cut off their nose to prove a point. You'll see it in clients too. They've already decided the solution before walking in. You show them the data, the tradeoffs, the better path — and they dig in harder. Recognise it. Don't fight it head-on. Name the tradeoff calmly, put it in writing, and let them own the decision. Their inat, their accountability.

---


## Agent Permission Scoping — Run when an AI agent is in scope

> **Trigger:** Run this section if `docs/problem-statement.md` indicates an AI agent is in scope.
> Standard HITL elicitation is not enough for agents. Agents act autonomously, access systems, and persist state.
> You need to define the permission boundary explicitly — not just where humans stay in the loop, but what the agent is and isn't allowed to touch.

This feeds directly into `docs/agent-security.md` in Phase S. Elicit it here while you have the client in the room.

---

**Step 1: Map what the agent touches**

> "Walk me through every system this agent needs access to. For each one — is it reading, writing, or both? And are there any records or fields it should never touch, even if it technically could?"

Build a list: system → access type → explicit limits.

**Step 2: Define the hard boundaries**

> "Are there any actions this agent must never take on its own — no matter what? Things that should always require a human to approve or confirm first?"

Common ones to surface:
- Deleting records
- Financial transactions above a threshold
- Sending external communications (email, SMS)
- Modifying records that affect multiple users
- Actions that are irreversible

Write these down explicitly. Not "use good judgment" — specific prohibitions.

**Step 3: Set the approval gates**

> "For the grey areas — not a hard no, but not fully autonomous either — what's the threshold where you'd want a human to sign off? A value over X? More than Y records affected? Anything touching [sensitive system]?"

Map each gate: action → condition → who approves.

**Step 4: Ask about data sensitivity**

> "Does this agent touch any personal data — names, emails, financial records, health information? And will it log or store what it processes?"

If yes: flag for AIUC-1 data handling rules in Phase S agent-security.md.

**Step 5: Ask about failure**

> "When this agent can't complete its task — what should happen? Should it fail silently, alert someone, or hand off to a human? What's the fallback?"

Document the expected failure behaviour now. It's much harder to define after the code is written.

---

Save all elicited details to `docs/stakeholder-register.md` in the HITL zones section, tagged clearly as agent-specific. They will be the primary input for `docs/agent-security.md` in Phase S.

## Phase 2 Outputs

> Save both files before closing Phase R. They are inputs to Phases I, S, and P.

| File | Contents | Required? |
|---|---|---|
| `docs/stakeholder-register.md` | All impacted parties, their stakes, HITL zones | Always |
| `docs/success-metrics.md` | Baseline measurements, success targets, second-order effects, qualitative targets, client sign-off | Always |
| `docs/decisions.md` | Updated with Phase R decisions | Always |

---

## Decision Logging — Phase R

> Update `docs/decisions.md` with decisions made in this phase before closing.

**Log these decisions in Phase R:**

- **HITL zones** — every zone the client named, and why
- **Baseline measurement method** — how you measured the current state, what data sources were used
- **Success targets** — what was agreed and any tradeoffs discussed to get there
- **Stakeholder impact ratings** — any that were challenged and revised, with the reason

---

## Exit Checklist
- [ ] Stakeholder register pre-filled, elicited (3 moves), confirmed → `docs/stakeholder-register.md`
- [ ] Hidden stakeholders surfaced (downstream consumers, compliance, support)
- [ ] Impact ratings challenged — neutral validated, not assumed
- [ ] HITL zones elicited from client, not inferred → saved in `docs/stakeholder-register.md`
- [ ] Baseline measured across all key dimensions → `docs/success-metrics.md`
- [ ] Desired projections defined — relative where possible → `docs/success-metrics.md`
- [ ] Second-order impacts identified → `docs/success-metrics.md`
- [ ] Tradeoffs presented and discussed
- [ ] Quant and qual success criteria agreed and signed off by client sponsor → `docs/success-metrics.md`
- [ ] Key decisions logged → `docs/decisions.md`
- [ ] **[Agent in scope]** Agent permission scoping complete — permissions, hard boundaries, approval gates, data sensitivity, failure behaviour all elicited and saved to `docs/stakeholder-register.md`
