---
name: phase1-clarify
description: The Mileva Method (CRISP) — Phase 1: Clarify. Problem definition, eliciting, painkiller test, buy vs build, Go/No-Go. Use at the start of any AI implementation project. Triggers on "clarify", "phase 1", "start discovery", "define the problem", "what problem are we solving", or at the beginning of a new client engagement.
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

**Buy vs Build**
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
| `docs/problem-statement.md` | One-sentence problem, constraints, Go/No-Go | Always |
| `docs/buy-vs-build-matrix.md` | Tool evaluation matrix | Always |
| `docs/market-research.md` | TAM, competitors, feature standards, USP | External only |
| `docs/value-proposition-canvas.md` | USP and positioning | External only |
| `docs/swot.md` | Strengths, weaknesses, opportunities, threats | External only |

---

## Exit Checklist
- [ ] `docs/` folder created in project root
- [ ] One-sentence problem statement agreed and saved → `docs/problem-statement.md`
- [ ] Business context mirrored and confirmed
- [ ] Ideal desired state defined
- [ ] ROI / gains identified
- [ ] Internal vs external decided
- [ ] Constraints captured (budget, time, legal, scope, tech)
- [ ] Buy vs Build evaluated → `docs/buy-vs-build-matrix.md`
- [ ] **[External only]** Market research complete → `docs/market-research.md`
- [ ] **[External only]** Value Proposition Canvas pre-filled and confirmed → `docs/value-proposition-canvas.md`
- [ ] **[External only]** SWOT complete → `docs/swot.md`
- [ ] Go / No-Go called
