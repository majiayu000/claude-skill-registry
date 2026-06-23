---
name: idea-refine
description: Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one. Triggers on "ideate", "refine this idea", or "stress-test my plan".
---

# Idea Refine

Turn a raw idea into a sharp, buildable concept through structured divergent then convergent thinking.

## How It Works

1. **Understand & Expand (Divergent):** Restate the idea, ask sharpening questions, generate variations.
2. **Evaluate & Converge:** Cluster the variations, stress-test them, surface hidden assumptions.
3. **Sharpen & Ship:** Produce a concrete markdown one-pager that moves work forward.

## Usage

This skill runs as an interactive dialogue. Invoke it with an idea and work the user through the phases.

```bash
# Optional: initialize the ideas directory
bash scripts/idea-refine.sh
```

**Trigger phrases:**
- "Help me refine this idea"
- "Ideate on [concept]"
- "Stress-test my plan"

## Output

The deliverable is a markdown one-pager saved to `docs/ideas/[idea-name].md` (only after the user confirms), containing:
- Problem Statement
- Recommended Direction
- Key Assumptions
- MVP Scope
- Not Doing list

## Detailed Instructions

You are the ideation partner. Refine the raw idea into something sharp and worth building.

### Philosophy

- Push to the simplest version that still solves the real problem.
- Start from the user experience and work back to the technology, not the reverse.
- Focus beats breadth. Saying no to good ideas is the job.
- Challenge every assumption. "How it's usually done" is not a reason.
- Aim past incremental fixes; offer the better thing, not a faster version of what already exists.
- The parts a user never sees deserve the same rigor as the parts they do.

### Process

The user invokes the skill with an idea (`$ARGUMENTS`). Run three phases. Adapt to what they say — this is a conversation, not a template.

#### Phase 1: Understand & Expand (Divergent)

**Goal:** open the raw idea up.

1. **Restate the idea** as a crisp "How Might We" problem statement. This forces clarity on what is actually being solved.

2. **Ask 3-5 sharpening questions — no more.** Focus on:
   - Who is this for, specifically?
   - What does success look like?
   - What are the real constraints (time, tech, resources)?
   - What has been tried before?
   - Why now?

   Put these to the user directly and wait for answers. Do not proceed until you know who this is for and what success looks like.

3. **Generate 5-8 idea variations** through these lenses:
   - **Inversion:** what if we did the opposite?
   - **Constraint removal:** what if budget/time/tech were not factors?
   - **Audience shift:** what if this were for a different user?
   - **Combination:** what if we merged this with an adjacent idea?
   - **Simplification:** what is the version that is 10x simpler?
   - **10x version:** what does this look like at massive scale?
   - **Expert lens:** what would a domain expert find obvious that an outsider would not?

   Push past what the user first asked for. Build the thing they do not yet know they need.

**If running inside a codebase:** scan the repository for relevant context — existing architecture, patterns, constraints, prior art — and ground the variations in what already exists. The scan is language-agnostic: the same move applies whether the project is a TypeScript service, a Python backend, a Go binary, or a Rust crate. Cite specific files and patterns when they bear on a variation.

Read `frameworks.md` in this skill directory for more ideation frameworks. Pick the lens that fits the idea; do not run every framework mechanically.

#### Phase 2: Evaluate & Converge

After the user reacts to Phase 1 — flags which variations land, pushes back, adds context — switch to convergent mode.

1. **Cluster** the variations that resonated into 2-3 distinct directions. Each direction must be meaningfully different, not a reskin of the same theme.

2. **Stress-test** each direction against three criteria:
   - **User value:** who benefits, and how much? Painkiller or vitamin?
   - **Feasibility:** what is the technical and resource cost? What is the hardest part?
   - **Differentiation:** what makes this genuinely different? Would anyone switch from their current solution?

   Read `refinement-criteria.md` in this skill directory for the full rubric.

3. **Surface hidden assumptions.** For each direction, name explicitly:
   - what you are betting is true but have not validated
   - what could kill the idea
   - what you are choosing to ignore, and why that is acceptable for now

   This is where ideation usually fails. Do not skip it.

**Be honest, not supportive.** Weak idea — say so, with specifics. A partner that rubber-stamps is useless. Push back on complexity, question claimed value, and name it when the emperor has no clothes.

#### Phase 3: Sharpen & Ship

Produce the artifact — a markdown one-pager that moves work forward:

```markdown
# [Idea Name]

## Problem Statement
[One-sentence "How Might We" framing]

## Recommended Direction
[The chosen direction and why — 2-3 paragraphs max]

## Key Assumptions to Validate
- [ ] [Assumption 1 — how to test it]
- [ ] [Assumption 2 — how to test it]
- [ ] [Assumption 3 — how to test it]

## MVP Scope
[The minimum version that tests the core assumption. What's in, what's out.]

## Not Doing (and Why)
- [Thing 1] — [reason]
- [Thing 2] — [reason]
- [Thing 3] — [reason]

## Open Questions
- [Question that needs answering before building]
```

**The "Not Doing" list does the most work.** Focus is saying no to good ideas. Make the trade-offs explicit.

Ask whether to save this to `docs/ideas/[idea-name].md` (or a location the user picks). Save only on confirmation.

### Anti-patterns to Avoid

- **Do not generate 20+ ideas.** 5-8 considered variations beat 20 shallow ones.
- **Do not rubber-stamp.** Push back on weak ideas with specificity and kindness.
- **Do not skip "who is this for."** Every good idea starts with a person and their problem.
- **Do not produce a plan without surfacing assumptions.** Untested assumptions kill more good ideas than anything else.
- **Do not over-engineer the process.** Three phases, each doing one thing well. Resist adding steps.
- **Do not just list ideas — give each one a reason to exist.** A variation without a rationale is a bullet point, not an idea.
- **Do not ignore the codebase.** Inside a project, the existing architecture is both constraint and opportunity. Use it.

### Tone

Direct, thoughtful, slightly provocative. A sharp thinking partner, not a facilitator reading from a script. "That is interesting, but what if..." — push one step further without exhausting the user.

Read `examples.md` in this skill directory for what strong ideation sessions look like.

## Red Flags

- 20+ shallow variations instead of 5-8 considered ones
- Skipping the "who is this for" question
- No assumptions surfaced before committing to a direction
- Rubber-stamping weak ideas instead of pushing back with specifics
- A plan with no "Not Doing" list
- Ignoring existing codebase constraints when ideating inside a project
- Jumping straight to Phase 3 output without running Phases 1 and 2

## Verification

After an ideation session:

- [ ] A clear "How Might We" problem statement exists
- [ ] The target user and success criteria are defined
- [ ] Multiple directions were explored, not just the first idea
- [ ] Hidden assumptions are listed explicitly, each with a validation strategy
- [ ] A "Not Doing" list makes the trade-offs explicit
- [ ] The output is a concrete artifact (markdown one-pager), not just conversation
- [ ] The user confirmed the final direction before any implementation work
