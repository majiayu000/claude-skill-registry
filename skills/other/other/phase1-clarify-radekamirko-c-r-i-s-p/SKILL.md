---
name: phase1-clarify
description: The Mileva Method (CRISP) — Phase 1: Clarify. Problem definition, eliciting, painkiller test, buy vs build, AI justification gate, Go/No-Go. Use at the start of any AI implementation project. Triggers on "clarify", "phase 1", "start discovery", "define the problem", "what problem are we solving", or at the beginning of a new client engagement.
---

## Pacing Rule — One Section at a Time

> Present one section, deliverable, or elicitation move at a time.
> After presenting — stop. Wait for the client to respond.
> Do not pre-fill and present multiple sections in one message.
> Do not move to the next step until the client confirms, corrects, or gives a clear go-ahead.
>
> The goal is a conversation, not a document dump.
> If you've written more than one section without a client response in between — you've gone too far.

---


# C — Clarify: Problem Definition

Do not discuss technology, solutions, or tools until this phase is complete.

> Nikola Tesla had 300 patents and died broke. Vision without validation is just expensive art.
> Clients arrive with solutions. Your job is to find the problem underneath.

## Output Convention

Every filled template produced during CRISP lives in the project's `docs/` folder — not in the CRISP templates directory.

> At the start of any CRISP engagement: create `docs/` in the project root if it doesn't exist.
> Blank templates live in `/templates/` (CRISP repo). Filled project outputs live in `[project]/docs/`.
> Never overwrite blank templates. Always write filled versions to `docs/`.

## Project State

> At the start of Phase C: check if `docs/crisp-state.json` exists.
> If yes — read it. Use `project` and `phases.C` fields for context.
> If no — copy `templates/crisp-state.json` to `docs/crisp-state.json` and fill in `project.name`, `project.client`, `project.startedAt`, `project.type` as soon as these are known.
>
> At the end of Phase C (before exit checklist): update `docs/crisp-state.json`:
> - Set `phases.current` to `"R"`
> - Add `"C"` to `phases.complete`
> - Set `phases.C.complete` to `true`
> - Fill `phases.C.goNoGo`, `phases.C.oneSentence`, `phases.C.painkiller`, `phases.C.constraints`
> - Set `project.type` to `"internal"` or `"external"`
> - Set `project.agentInScope` and `project.memoryOwnershipRequired` if known
> - Add any unresolved items to `phases.C.openQuestions`

---

## The 3 Moves

**Move 1: Business Mirroring**
Reconstruct their core business or idea back at them until confirmed correct.
> "Okay, let me make sure I'm not about to solve the wrong problem — you do X, it works kind of like Y and Z, right? Tell me where I'm off."

**Move 2: Eliciting**
Suggest the ideal state — let them correct you into the real need.
> "So in a perfect world, X happens automatically, Y follows, nobody has to touch it — is that roughly the dream? Or am I undershooting?"
People react better than they originate. Corrections surface real pain faster than open questions.

**Move 3: Roleplay / Process Walkthrough**
Act as the user living the current process. Narrate it out loud step by step.
> "Walk me through it like I'm the new hire on day one. The underwriter opens what, clicks where, copies what into where... go."
Exposes friction they've become blind to.

**Move 4: Magic Wand**
Remove all constraints — budget, time, tech, team — and ask what they'd actually want.
> "Forget what's possible for a second. If you had a magic wand and could fix one thing in this business tomorrow, what would it be?"
Use this early, before they've started self-editing. The answer is almost always the real problem — or points directly at it. Then bring constraints back in and work backwards from there.

---

## Key Assessments

**Painkiller vs Multivitamin**
- Painkiller = costs them daily in time/money/risk → proceed
- Multivitamin = nice to have, life slightly better → deprioritize or kill

> **War story:** Had a client dead serious about a streaming platform for amateur boxing. USP? "Nobody's doing it." Well. Maybe there's a reason. ESPN+ adds a category and you're done. We went back to the real problem — nobody is connecting amateur fighters with promoters and matchmakers. Pivoted to a matchmaking platform. That's where the leverage actually lived.
> The absence of competition isn't a green light. Sometimes it's a warning sign.

**Internal vs External**
- Internal: stakeholders, ROI measurement, employee ideal state
- External: competitors, TAM, USP → run Market Research + SWOT (see below)

**Constraints Capture**
- Budget, Time, Legal/Compliance, Scope, Technical stack
- Constraints direct architecture — capture before any solution talk

**Buy vs Build — with AI Justification Gate**

> Run Buy vs Build in two stages. Stage 1 checks off-the-shelf AI products first — before evaluating any SaaS or custom build. Most "AI projects" don't need custom AI.

**Stage 1 — Off-the-Shelf AI Check (mandatory, run first)**

Before anything else: can an existing AI product solve this?

| Product | What it covers | Monthly cost |
|---|---|---|
| Claude.ai / Claude Pro | General AI assistant, reasoning, document work | ~$20 |
| ChatGPT / GPT-4o | General AI assistant, coding, analysis | ~$20 |
| Copilot (Microsoft) | Office, email, Teams integration | ~$30 |
| Notion AI | Knowledge base, docs, writing assistance | ~$10 |

Present the relevant options to the client. If any of them cover the need adequately → direct the client there and stop. This is a No-Go for custom build, and that's the right outcome.

> **The personal assistant trap.** Someone wants a "personal AI assistant." Sounds like a project. Often it's just Claude Pro. If what they're describing is a private chat interface with some instructions — that's $20/month, not six weeks of build. The fact that they'll pay more for a worse version of something that already exists is not a business case.
> Always ask: "What does this need to do that Claude.ai can't do for $20 a month?" If they can't answer — you have your answer.

**Stage 2 — AI Justification Gate**

If off-the-shelf doesn't cover the need, answer these three questions before evaluating any custom build:

1. **What does custom AI do that off-the-shelf products cannot?**
   _(Be specific. "More control" or "our own branding" are not answers. "Processes data from our internal CRM in real-time and routes decisions back into it" is an answer.)_

2. **What is the total cost: custom build + ongoing running costs vs. best off-the-shelf alternative?**
   _(Include dev time, hosting, API costs, maintenance overhead.)_

3. **Does the delta justify it?**

If Q1 can't be answered specifically → No-Go. Save the client the cost.
Save the AI justification answer to `docs/problem-statement.md` (AI Justification section) and to `docs/buy-vs-build-matrix.md`.

**Stage 3 — Standard Buy vs Build**
- Tool solves it for $50/month? → Buy it
- Needs config on top of existing tools? → Configure it
- Genuinely needs custom? → Build it
- Deliverable: `docs/buy-vs-build-matrix.md`

---

## The One Sentence
> "Currently, [who] are spending [cost/time/money] doing [thing] because [root cause]."

Both sides must agree on this sentence before Phase C closes. If they can't agree on the sentence, they definitely can't agree on the solution.

---

## Go / No-Go

Before closing Phase C, call it explicitly.

**The CEO test:**
> "'The CEO wants this built.' Why? 'Competitors have it.' So what? Does it serve your objectives — your vision, your mission, what you're actually trying to achieve? No? We don't build it."

Features justified by "competitors have it" and nothing else are the most expensive features you'll ever ship. They solve the competitor's problem, not yours.

No-Go is not failure. It's the fastest possible win. Lose the project, save the client six weeks.

**No-Go is a feature.** If a free tool solves it, say so. Lose the project, win the trust.

---

## External Product Extensions (run after Internal vs External decision)

If the project is an **external product**, two additional steps are mandatory before Phase C closes:

### 1. Market Research → `market-research.md`
Run full market research: TAM sizing, competitor mapping, feature standards (must-have vs differentiator vs gap), review mining (Reddit, G2, Product Hunt), USP gap analysis.
Output → `docs/market-research.md`

This feeds directly into:
- Phase R: success metrics (market context shapes what "good" looks like)
- Phase S: MVP baseline (competitor must-haves), backlog, USP

### 2. SWOT → `swot.md`
Run after market research. Pre-fill S/W from problem statement and constraints. Pre-fill O/T from market research findings, competitor intelligence, and industry trends.
Elicit client input — let them correct, not originate.
Output → `docs/swot.md`

### 3. Value Proposition Canvas — Pre-fill and Confirm

Run after market research and SWOT are complete. Do not ask the client to fill this in from scratch — everything needed is already in prior documents.

**Pre-fill from existing docs:**

| VPC section | Source |
|---|---|
| Customer Jobs | `docs/problem-statement.md` — who has the problem and what they're trying to do |
| Pains | `docs/problem-statement.md` — root cause, friction; `docs/market-research.md` — review mining complaints |
| Gains | `docs/problem-statement.md` — desired outcome, ROI; `docs/market-research.md` — what reviewers wish existed |
| Products & Services | What you've agreed to build in Phase C scope |
| Pain Relievers | Map your solution directly to each pain identified above |
| Gain Creators | Map your solution directly to each gain identified above |
| USP | `docs/market-research.md` — positioning gap recommendation |
| Competitive Landscape | `docs/market-research.md` — competitor table |
| TAM | `docs/market-research.md` — TAM estimate |

Pre-fill the entire canvas, then present it:
> "I've pulled this together from everything we've discussed and what I found in the market. The core customer job is [X], the main pain is [Y], and our edge is [Z]. Does that hold up, or are you seeing gaps?"

One round of corrections is enough. If they want to add a pain or reframe the USP — update it. Do not turn this into a brainstorm.

Output → `docs/value-proposition-canvas.md`

---

## Phase 1 Outputs

> Save all of these to `docs/` before closing Phase C. These files are inputs to every subsequent phase.

| File | Contents | Required? |
|---|---|---|
| `docs/problem-statement.md` | One-sentence problem, AI justification, constraints, Go/No-Go | Always |
| `docs/buy-vs-build-matrix.md` | Off-the-shelf AI check, AI justification gate, tool evaluation matrix | Always |
| `docs/market-research.md` | TAM, competitors, feature standards, USP | External only |
| `docs/value-proposition-canvas.md` | USP and positioning | External only |
| `docs/swot.md` | Strengths, weaknesses, opportunities, threats | External only |
| `docs/decisions.md` | Log of key decisions made in Phase C | Always |

---

## Decision Logging — Phase C

> Create `docs/decisions.md` using `/templates/decisions.md` at the start of Phase C if it doesn't exist.
> Log every significant decision as it happens — do not batch at the end.

**Log these decisions in Phase C:**

- **Go/No-Go** — what was called and why
- **AI Justification** — what custom AI does that off-the-shelf cannot, and the cost delta
- **Internal vs External** — which it is and the reason
- **Buy vs Build choices** — every item in the matrix with the rationale
- **Constraints** — any hard constraint that ruled out an option
- **Scope decisions** — anything explicitly included or excluded

Format:
```
### Go/No-Go — [Project Name]
**Phase:** C
**Decision:** Go / No-Go
**Why:** [reason — constraint, painkiller test result, CEO test outcome, AI justification result]
**Alternatives considered:** [what else was discussed]
**Source:** Client / You / Both
```

---

## Exit Checklist
- [ ] `docs/` folder created in project root
- [ ] One-sentence problem statement agreed and saved → `docs/problem-statement.md`
- [ ] Business context mirrored and confirmed
- [ ] Ideal desired state defined
- [ ] ROI / gains identified
- [ ] Internal vs external decided
- [ ] Constraints captured (budget, time, legal, scope, tech)
- [ ] Off-the-shelf AI products checked (Stage 1) → if any cover the need, No-Go called
- [ ] AI Justification Gate answered (Stage 2) → Q1 answered specifically, cost delta calculated → `docs/buy-vs-build-matrix.md` + `docs/problem-statement.md`
- [ ] Buy vs Build evaluated (Stage 3) → `docs/buy-vs-build-matrix.md`
- [ ] **[External only]** Market research complete → `docs/market-research.md`
- [ ] **[External only]** Value Proposition Canvas pre-filled and confirmed → `docs/value-proposition-canvas.md`
- [ ] **[External only]** SWOT complete → `docs/swot.md`
- [ ] Go / No-Go called
- [ ] Key decisions logged → `docs/decisions.md`
