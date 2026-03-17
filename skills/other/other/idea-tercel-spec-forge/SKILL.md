---
name: idea
description: >
  Use when exploring a new idea before writing formal specifications. Guides users through iterative
  discovery, research, and critical analysis to crystallize vague ideas into validated requirement
  drafts. Includes anti-pseudo-requirement checks, competitive research, demand evidence gathering,
  and "What if we don't build this?" analysis. Supports pause/resume across sessions, stores ideas
  in the project's ideas/ directory, and graduates validated ideas into the spec-forge auto
  chain (idea → decompose → tech-design + feature specs).
instructions: >
  Follow the workflow below exactly. This is an interactive, multi-session skill.
  Ideas are stored in the project's ideas/ directory. By default, suggest adding ideas/
  to .gitignore, but the user can choose to commit them for team collaboration.
  CRITICAL: Do not let ideas graduate without demand validation. A "ready" idea must
  have evidence that it solves a real problem, not just a "sounds cool" feeling.
---

# Idea — Brainstorming & Demand Validation

Explore, research, validate, and crystallize ideas through iterative sessions before committing to formal specification. **Every idea must prove it's a real need before graduating.**

## Core Principles

1. **Brainstorm freely, validate ruthlessly**: Early sessions are open and creative; later sessions demand evidence
2. **Non-linear**: Ideas evolve through multiple sessions, not in one sitting
3. **Research-driven**: Use web search, competitive analysis, and user evidence to ground ideas in reality
4. **Anti-pseudo-requirement**: Before graduating, every idea must answer "What happens if we don't build this?" — if the answer is "nothing significant", the idea is not ready
5. **Persistent**: Every session is recorded, nothing is lost
6. **Project-local**: Ideas live in the project's `ideas/` directory, close to the codebase and docs they relate to

## Storage Structure

> **`ideas/` is a top-level directory at the project root, separate from `docs/`. Never nest it inside `docs/`.**

```
{project-root}/
├── ideas/                          # Brainstorming workspace (TOP-LEVEL, not under docs/)
│   ├── {idea-name}/
│   │   ├── state.json              # Status, metadata, and validation checklist
│   │   ├── sessions/
│   │   │   ├── overview.md         # Session index: chronological order, summaries
│   │   │   ├── explore-initial-spark.md    # First session
│   │   │   ├── research-competitors.md     # Second session
│   │   │   ├── validate-demand.md          # Third session
│   │   │   └── ...
│   │   ├── research/
│   │   │   ├── competitors.md      # Competitive landscape analysis
│   │   │   └── market-notes.md     # Market research, user evidence, data points
│   │   └── draft.md                # Evolving summary (auto-updated after each session)
│   └── ...
├── docs/                           # Formal spec documents (PRD, SRS, etc.)
└── .gitignore                      # Add "ideas/" if you want to keep them private
```

### .gitignore Guidance

On first run, if `ideas/` does not exist, ask the user:
- **Add to .gitignore (Recommended)** — ideas are personal working notes, keep them local
- **Commit to Git** — share brainstorming with the team for collaboration
- **Decide later** — create the directory now, handle .gitignore manually

## Session Types

Each return session, the user chooses a focus. The idea matures through these phases:

| Phase | Focus | Key Activities |
|-------|-------|---------------|
| **Explore** | Diverge, discover | Brainstorm, free association, "what if" thinking |
| **Research** | Investigate, evidence | Competitive analysis, market research, user pain points |
| **Validate** | Challenge, prove | Anti-pseudo-requirement checks, demand evidence, feasibility |
| **Refine** | Converge, sharpen | MVP scope, success criteria, draft polishing |

Phases are not strictly sequential — users can revisit any phase at any time. But an idea cannot reach `ready` status without completing the Validate phase.

## Session Overview File

Each idea maintains a `sessions/overview.md` that tracks all sessions in chronological order. This file is the single source of truth for session ordering — filenames do NOT encode sequence.

**Create this file when the first session is recorded. Update it after every subsequent session.**

```markdown
# Session Overview — {idea-name}

> Chronological index of brainstorming sessions.
> Updated: {date}

## Sessions

| # | Session | Type | Date | Summary |
|---|---------|------|------|---------|
| 1 | [explore-initial-spark](./explore-initial-spark.md) | Explore | {date} | {one-line summary} |
| 2 | [research-competitors](./research-competitors.md) | Research | {date} | {one-line summary} |
| 3 | [validate-demand](./validate-demand.md) | Validate | {date} | {one-line summary} |
| ... | ... | ... | ... | ... |
```

**Rules:**
- The `#` column is the chronological order (for human readability only — NOT part of the filename)
- Append new sessions at the bottom
- Never reorder or renumber existing entries

## Workflow

### Step 1: Initialize or Resume

#### 1.1 Ensure Base Directory

**IMPORTANT: `ideas/` MUST be at the project root — the same level as `docs/`, NOT inside it.**
- Correct: `{project-root}/ideas/`
- Wrong: `{project-root}/docs/ideas/`

Check if `ideas/` exists in the project root. If not:
1. Create the `ideas/` directory at the project root
2. Ask the user about .gitignore preference (see .gitignore Guidance above)
3. If user chooses to gitignore, add `ideas/` to `.gitignore`

#### 1.2 Parse Idea Name

Extract idea name from arguments. Convert to kebab-case.

If no name provided, list existing ideas:

```
Your Ideas:

  # | Idea            | Status     | Validated | Sessions | Last Updated
  1 | cool-feature    | refining   | Yes       | 5        | 2026-02-10
  2 | payment-system  | exploring  | No        | 1        | 2026-02-14
  3 | ai-assistant    | ready      | Yes       | 7        | 2026-02-12

Actions:
  Enter a number to resume that idea
  Enter a new name to start brainstorming
```

Use `AskUserQuestion` to let the user choose.

#### 1.3 Check Existing State

Check if `ideas/{idea-name}/` exists:

**New idea** (directory doesn't exist):
- Create directory structure: `state.json`, `sessions/`, `research/`, `draft.md`
- Initialize `state.json`:
  ```json
  {
    "idea": "{idea-name}",
    "status": "exploring",
    "created": "{ISO timestamp}",
    "updated": "{ISO timestamp}",
    "session_count": 0,
    "draft_version": 0,
    "validation": {
      "problem_evidence": null,
      "demand_evidence": null,
      "competitive_analysis": false,
      "not_build_analysis": null,
      "validated": false
    }
  }
  ```
- Proceed to Step 2 (New Idea)

**Existing idea**:
- Read `state.json`
- If `status` is `graduated`: inform user this idea has already moved to formal specs, ask if they want to start a new variant
- If `status` is `ready`: ask if they want to continue refining, or graduate now
- If `status` is `exploring`, `researching`, or `refining`: read `draft.md` to restore context, proceed to Step 3 (Continue Session)

### Step 2: New Idea — Opening Exploration

This is the first session for a brand new idea. The goal is to understand the user's raw thinking AND begin planting seeds of critical analysis.

#### 2.1 Open-Ended Discovery

Use `AskUserQuestion` with open questions. Ask 2-3 at a time, adapt follow-ups based on answers.

**Round 1 — The Spark:**
- What's the idea? Describe it however you like (one sentence or a paragraph)
- What triggered this idea? (a pain point you experienced, something you saw, a user complaint, data you noticed?)

**Round 2 — The Problem:**
- What specific problem does this solve? Can you describe a concrete scenario where someone suffers without this?
- Who suffers from this problem? How often? How severely?
- What happens if this is NOT built? (Plant this question early — it's the core anti-pseudo-requirement check)

**Round 3 — The Landscape:**
- What existing solutions have you seen? (competitors, workarounds, manual processes)
- What do they get wrong? Why are they insufficient?
- If good solutions exist, why build another one?

**Round 4 — The Shape:**
- What would the simplest version look like? (MVP)
- What are you most uncertain about?

Do NOT force answers. If the user says "I don't know yet" — record it as an open question that needs research.

#### 2.2 Initial Demand Signal Assessment

Based on the user's answers, provide an honest initial assessment:

```
Initial Demand Signal:

  Problem clarity:     [Clear / Vague / Unknown]
  Evidence of demand:  [Strong / Weak / None yet]
  Existing solutions:  [None / Inadequate / Good (risk!)]
  Differentiation:     [Clear / Unclear / Not yet defined]

  Suggested next session focus: [Research / Explore more / Validate]
```

Be honest. If the idea sounds like a solution looking for a problem, say so gently:
> "The idea is interesting, but I notice we haven't identified who specifically suffers from this problem. In a future session, it would help to research concrete user pain points."

#### 2.3 Record Session

Write the session to `ideas/{idea-name}/sessions/{type}-{slug}.md` (e.g., `explore-initial-spark.md`):

**Session filename rules:**
- Format: `{session-type}-{brief-slug}.md` where type is one of: `explore`, `research`, `validate`, `refine`
- The slug is a 2-4 word kebab-case description of the session focus (e.g., `initial-spark`, `competitors`, `demand-check`, `mvp-scope`)
- Do NOT use sequential numbers (`001.md`, `002.md`, etc.) — chronological order is tracked in `sessions/overview.md`
- If a type repeats (e.g., two explore sessions), differentiate by slug: `explore-initial-spark.md`, `explore-new-angles.md`

**Session filename:**

```markdown
# Session 1 — {date}
## Type: Exploration

## Context
{Where this idea came from, what triggered it}

## Key Points
- {Bullet points of main ideas discussed}

## Problem Definition
- **Who suffers**: {who}
- **How they suffer**: {pain description}
- **Current workaround**: {what they do today}

## Demand Signal
- Problem clarity: {Clear/Vague/Unknown}
- Evidence: {what evidence exists or is needed}

## Decisions
- {Any decisions made, even tentative ones}

## Open Questions
- {Things still uncertain or needing research}

## Research Needed
- {Specific research tasks identified for next session}

## Raw Notes
{Full Q&A exchange, preserving the user's original words}
```

#### 2.4 Generate Initial Draft

Create `draft.md`:

```markdown
# {Idea Name}

> Status: Exploring | Draft v1 | {date}

## One-Liner
{One sentence description}

## Problem
{What problem this solves — be specific about who suffers and how}

## Target Users
{Who would use this — be specific, not "everyone"}

## Core Concept
{How it would work at a high level}

## Existing Solutions & Gaps
{What exists today, why it's insufficient}

## MVP Scope
{Simplest useful version — or "not yet defined"}

## Demand Validation Status
- [ ] Problem backed by evidence (not just assumption)
- [ ] Target users identified and reachable
- [ ] Existing solutions analyzed (competitors, workarounds)
- [ ] "What if we don't build this?" answered convincingly
- [ ] At least one form of demand evidence (user complaints, data, research)

## Open Questions
- {List of unresolved questions}

## Research Backlog
- {Things to investigate in future sessions}

## Session History
- [{date}] explore-initial-spark — {one-line summary}
```

#### 2.5 Update State and Wrap Up

Update `state.json`: `session_count: 1`, `updated: now`, `draft_version: 1`

Display:

```
Idea saved: {idea-name}
  Location: ideas/{idea-name}/
  Status: exploring
  Sessions: 1
  Validated: No

Suggested next session: {Research / Continue exploring}
  /spec-forge:idea {idea-name}

When validated and ready:
  /spec-forge {idea-name}         Start full spec chain
```

### Step 3: Continue Session — Iterative Development

The user is returning to an existing idea.

#### 3.1 Restore Context

Read `draft.md` and display a concise summary:

```
Resuming idea: {idea-name}
  Status: {status} | {session_count} sessions | Last: {last_date}
  Validated: {Yes/No}

Current summary:
  {One-liner from draft.md}

Validation status:
  [x] Problem backed by evidence
  [ ] Competitive analysis done
  [ ] "What if we don't build this?" answered
  ...

Open questions:
  - {question 1}
  - {question 2}

Research backlog:
  - {research item 1}
```

#### 3.2 Choose Session Focus

Use `AskUserQuestion`:
- **Explore** — I have new thoughts or want to brainstorm further
- **Research** — Let's investigate the market, competitors, or user needs
- **Validate** — Challenge assumptions, check if this is a real need
- **Refine** — The direction is clear, let's sharpen the draft
- **Graduate** — This idea is validated and ready for formal specification
- **Park** — Set aside for now

#### 3.3a: Explore Session

Open-ended brainstorming, similar to Step 2 but adaptive:
- Address open questions from previous sessions
- Explore new angles the user hasn't considered
- Challenge assumptions: "You mentioned X — have you considered Y?"
- Explore alternatives: "What if instead of A, you did B?"
- "What's the worst version of this that would still be useful?"
- "What would make you NOT use this product?"

Record as new session. Update `draft.md` with new insights.

#### 3.3b: Research Session

**This is where the idea gets grounded in reality.** Use `WebSearch` and critical analysis.

##### Competitive Analysis

Use `WebSearch` to research:
1. Direct competitors (same problem, same solution approach)
2. Indirect competitors (same problem, different approach)
3. Adjacent solutions (different problem, similar technology)

For each competitor found, analyze:
- What they do well
- What they do poorly
- Their pricing model
- Their target users
- Why our idea is different (or is it?)

Write findings to `research/competitors.md`:

```markdown
# Competitive Analysis — {idea-name}
> Last updated: {date}

## Direct Competitors
### {Competitor 1}
- **What they do**: ...
- **Strengths**: ...
- **Weaknesses**: ...
- **Why we're different**: ...

## Indirect Competitors / Workarounds
### {Alternative approach}
- ...

## Key Takeaway
{Is there a real gap in the market? Or is this already well-served?}
```

##### Market & Demand Research

Use `WebSearch` to find:
- How many people search for solutions to this problem?
- Forum posts, Reddit threads, Stack Overflow questions about this pain point
- Industry reports or blog posts discussing this need
- Any data on market size or growth

Write findings to `research/market-notes.md`.

##### User Evidence Gathering

Ask the user:
- Have you or anyone you know experienced this problem firsthand?
- Do you have access to user feedback, support tickets, or analytics that show this need?
- Can you point to specific user quotes, complaints, or feature requests?

**Be rigorous**: "I think users want this" is not evidence. Evidence is:
- User interviews or surveys
- Support ticket patterns
- Usage analytics showing friction points
- Community discussions (forums, social media)
- Competitor reviews mentioning gaps

Record all findings in the session file. Update `draft.md` with research results. Update `state.json` validation fields. Change status to `researching` if not already.

#### 3.3c: Validate Session

**The critical session that separates real needs from pseudo-requirements.**

Run through the Demand Validation Checklist with the user:

##### Check 1: Problem Evidence
> "What concrete evidence do we have that this problem exists and is painful enough to justify a solution?"

Rate: **Strong** (data, user quotes, patterns) / **Moderate** (anecdotes, logical reasoning) / **Weak** (assumption only)

If Weak: flag it. "This is still an assumption. Before going further, we need to find evidence. What's the cheapest way to validate this?"

##### Check 2: "What Happens If We Don't Build This?"

> "Imagine we decide not to build this. What happens?"

Possible answers and their implications:
- "Users keep suffering with workarounds" → **Real need** — but how painful are the workarounds? Are they acceptable?
- "A competitor will beat us to it" → **Competitive pressure** — but is this a race worth running? What if the competitor also fails?
- "Nothing really changes" → **RED FLAG: Pseudo-requirement.** This idea may not be worth building.
- "We miss a business opportunity" → **Opportunity cost** — quantify it. How big is the opportunity?

##### Check 3: Target User Reality
> "Can you name 3-5 specific people (or specific types of people) who would use this in the first week?"

If the user cannot name concrete early adopters, the target user definition is too vague.

##### Check 4: Differentiation Test
> "If a user is already using {competitor/workaround}, why would they switch to this?"

Switching cost is real. The new solution must be significantly better, not just slightly different.

##### Check 5: Simplicity Test
> "Can you explain what this does in one sentence to someone outside the industry?"

If not, the concept may be too complex or poorly defined.

##### Validation Verdict

After all checks, provide an honest assessment:

```
Validation Summary:

  Problem evidence:    [Strong / Moderate / Weak]
  "Not build" impact:  [Significant / Moderate / Low]
  Target users:        [Concrete / Vague]
  Differentiation:     [Clear / Unclear]
  Simplicity:          [Pass / Needs work]

  Overall: [VALIDATED / NEEDS WORK / NOT VALIDATED]
```

**VALIDATED**: All checks pass with at least Moderate strength → idea can proceed to `ready`

**NEEDS WORK**: Some checks are Weak → specific guidance on what to research or rethink next

**NOT VALIDATED**: Core checks fail (no problem evidence, no impact if not built) → honest conversation:
> "Based on our analysis, this idea doesn't yet have strong evidence of real demand. That doesn't mean it's a bad idea — it means it needs more validation before committing resources to formal specification. Here's what I suggest..."

Update `state.json` validation fields and draft.md.

#### 3.3d: Refine Session

Available only after validation passes. Shift to convergent thinking:
- Review each section of `draft.md` with the user
- Finalize MVP scope — ruthlessly cut anything non-essential
- Define preliminary success criteria (measurable)
- Identify technical constraints or risks
- Prepare the draft for handoff to `/spec-forge:tech-design` (or the full chain via `/spec-forge`)

Update `draft.md` to a polished version. Change status to `refining`.

When the draft has:
- Clear, evidence-backed problem statement
- Defined, reachable target users
- Concrete MVP scope
- No critical open questions
- Validation checklist complete

→ Suggest changing status to `ready`.

#### 3.3e: Graduate

**Pre-graduation check**: Verify `validation.validated` is `true` in `state.json`. If not:

> "This idea hasn't completed demand validation yet. Graduating without validation risks building something nobody needs. Would you like to run a validation session first, or graduate anyway (not recommended)?"

If user insists on graduating without validation, record it in state:
```json
{ "validation": { "validated": false, "graduated_without_validation": true } }
```

If validated, update `state.json`:
```json
{ "status": "ready" }
```

Display:

```
Idea '{idea-name}' is ready for formal specification!

  Validation: Passed
  Draft: ideas/{idea-name}/draft.md

To start the spec chain:
  /spec-forge {idea-name}         Full chain (Idea → Decompose → Tech Design + Feature Specs)

Optional (on-demand):
  /spec-forge:prd {idea-name}     PRD (for stakeholders)
  /spec-forge:srs {idea-name}     SRS (for compliance/audit)
  /spec-forge:test-plan {idea-name} Test Plan (for formal QA)
```

Note: The actual `graduated` status is set by the `/spec-forge` chain command after it successfully generates the tech-design.

#### 3.3f: Park

Update `state.json`: set `status: 'parked'`, update `updated` timestamp. Display:

```
Idea '{idea-name}' parked.
  Everything is saved. Come back anytime:
  /spec-forge:idea {idea-name}
```

#### 3.4 Record Session and Update

- Write session to `sessions/{type}-{slug}.md` (use session type + descriptive slug, NOT sequential numbers)
- Create or update `sessions/overview.md` to append the new session entry (see Session Overview below)
- Update `draft.md` with any new content
- Update `research/` files if research was conducted
- Update `state.json`: `session_count`, `updated`, `draft_version`, `status`, `validation`

## Status Definitions

| Status | Meaning |
|--------|---------|
| `exploring` | Early stage, divergent thinking, brainstorming |
| `researching` | Investigating market, competitors, user needs |
| `refining` | Direction clear and validated, converging on specifics |
| `ready` | Validated and ready for formal specification |
| `graduated` | Tech Design has been generated from this idea |
| `parked` | Intentionally set aside, can resume anytime |

## Draft Validation Checklist

An idea cannot reach `ready` status without these being addressed:

- [ ] **Problem backed by evidence** — not just "I think this is needed"
- [ ] **Target users identified** — specific, reachable people, not "everyone"
- [ ] **Competitive analysis done** — know what exists, why it's insufficient
- [ ] **"What if we don't build this?" answered** — impact must be significant
- [ ] **Demand evidence exists** — at least one concrete data point (user quotes, analytics, market data, community signals)
- [ ] **Differentiation clear** — why switch from existing solutions
- [ ] **MVP scope defined** — simplest useful version, not the dream version

## Notes

1. **Project-local**: Ideas are stored in the project's `ideas/` directory. Users can add `ideas/` to `.gitignore` for privacy, or commit for team collaboration.
2. **Honest Assessment**: Unlike pure brainstorming, this skill is designed to kill bad ideas early. A "NOT VALIDATED" result saves weeks of wasted development. Be honest, not encouraging.
3. **Session Preservation**: Every session is a separate file named `{type}-{slug}.md`. Never overwrite or merge sessions — they are the historical record of how the idea evolved. Chronological order is tracked in `sessions/overview.md`, not in filenames.
4. **Research Artifacts**: The `research/` directory preserves competitive analysis and market research. This data feeds directly into the PRD's market analysis and competitive sections.
5. **Draft Evolution**: `draft.md` is the living document that evolves. Old versions are implicitly preserved in the session history.
6. **Anti-Pseudo-Requirement**: This principle carries through the entire spec-forge chain. It starts here at the idea stage, is reinforced in the PRD (demand evidence, feasibility verdict), and is traced through SRS and Tech Design.
