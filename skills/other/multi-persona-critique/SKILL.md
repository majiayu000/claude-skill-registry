---
name: multi-persona-critique
description: "Critique a written proposal or design artifact via 5 philosophical personas in parallel, with consensus synthesis."
user-invocable: true
argument-hint: "<proposals to critique, or 'generate N ideas about X'>"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Agent
context: fork
routing:
  triggers:
    - "critique these ideas"
    - "multi-persona review"
    - "philosophical critique"
    - "devil's advocate on ideas"
    - "stress test proposals"
    - "evaluate from multiple perspectives"
    - "get different viewpoints"
    - "critique proposals"
  not_for: "speaking to a person, a meeting, or pushing back in a conversation — that is professional-communication. This critiques an artifact, not interpersonal messaging."
  pairs_with:
    - roast
    - decision-helper
  complexity: Complex
  category: analysis
---

# Multi-Persona Critique: Parallel Philosophical Review of Proposals

## Overview

This skill takes a set of proposals — feature ideas, architectural decisions, design choices, strategy options — and sends ALL of them to 5 distinct intellectual personas for parallel, independent critique. Each persona brings a different philosophical lens. The skill then synthesizes all critiques into a consensus report showing where personas agree, where they disagree, and what the disagreements reveal.

**This is NOT the roast skill.** Key differences:
- `roast` critiques CODE with HackerNews personas and validates file:line claims
- This skill critiques IDEAS/PROPOSALS with philosophical/methodological personas and evaluates logical coherence, practical viability, and human impact
- `roast` is evidence-based (checking actual code); this is argument-based (evaluating reasoning)

**Key constraints baked into the workflow:**
- Every persona sees ALL proposals — no cherry-picking
- Personas run in parallel with no awareness of each other — independence is the source of value
- Ratings are mandatory: STRONG / PROMISING / WEAK / REJECT for every proposal from every persona
- Rankings are mandatory: each persona orders proposals from strongest to weakest
- Fairness mandate: genuine strengths must be acknowledged, genuine weaknesses explained with precision
- Disagreements are preserved, not averaged away — the disagreements ARE the insight
- The synthesis phase adds cross-cutting analysis, it does not edit persona outputs

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| example-driven tasks, errors | `examples-and-errors.md` | Loads detailed guidance from `examples-and-errors.md`. |
| dispatching the five critique personas (Phase 2) | `personas.md` | Loads detailed guidance from `personas.md`. |
| writing the Phase 5 synthesis report | `synthesis-template.md` | Loads detailed guidance from `synthesis-template.md`. |

## Instructions

### Phase 1: UNDERSTAND PROPOSALS

**Goal**: Extract or generate clear, numbered proposals ready for critique.

**Step 1: Determine input mode**

| Input | Action |
|-------|--------|
| User provides proposals directly | Extract and number them |
| User says "generate N ideas about X" | Research the domain, read relevant code/docs, then generate proposals |
| Ambiguous input | Ask user to clarify before proceeding |

**Step 2: Normalize proposals**

Each proposal must be a clear, self-contained description (2-4 sentences) that any of the 5 personas can evaluate independently. If user-provided proposals are vague, expand them to include:
- What the proposal does
- Why it matters (the problem it solves)
- How it differs from the status quo

If generating proposals, research the domain first:
- Use Glob and Grep to understand existing code, docs, and architecture
- Use Read to examine key files relevant to the domain
- Generate proposals grounded in actual context, not hypotheticals

**Step 3: Number and present**

Present the numbered proposal list back to the user before proceeding. Format:

```
Proposals for critique:
1. [Title] — [2-4 sentence description]
2. [Title] — [2-4 sentence description]
...
```

**Gate**: Numbered list of proposals ready. Each proposal is self-contained with 2-4 sentences. Proceed only when gate passes.

### Phase 2: BRIEF PERSONAS

**Goal**: Construct prompts for each of the 5 personas.

Load the full persona specifications from `${CLAUDE_SKILL_DIR}/references/personas.md`. For each persona, construct a prompt containing an identity block, the numbered proposals, rating and ranking requirements, a fairness mandate, and the structured output format — see `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md` (Phase 2: Persona Prompt Construction) for the complete construction recipe.

**Gate**: 5 persona prompts constructed, each containing all proposals and the full persona specification. Proceed only when gate passes.

### Phase 3: DISPATCH (Parallel)

**Goal**: Launch all 5 personas in parallel and collect independent critiques.

Launch 5 agents using the Agent tool, one per persona. Each agent runs independently with no awareness of other personas.

**The 5 parallel agents:**

1. **The Logician** (Bertrand Russell)
   Focus: Logical coherence, hidden assumptions, falsifiability, necessity vs novelty

2. **The Pragmatic Builder** (20-year staff engineer)
   Focus: Build cost vs value, maintenance burden, simpler alternatives, user need

3. **The Systems Purist** (Edsger Dijkstra)
   Focus: Accidental complexity, separation of concerns, elegance, failure modes

4. **The End User Advocate** (8-hours-a-day tool user)
   Focus: Daily impact, friction, delight, whether the problem is already solved

5. **The Skeptical Philosopher** (Illich/Postman/Franklin)
   Focus: Human agency, dependency risk, genuine vs manufactured problems, unintended consequences

**Each agent must produce:**
- A rating (STRONG / PROMISING / WEAK / REJECT) for every proposal with 2-3 sentence justification
- A ranked list of all proposals from strongest to weakest
- Any cross-cutting observations that apply to multiple proposals

**CRITICAL**: Wait for ALL 5 agents to complete before proceeding to Phase 4. Do not begin synthesis on partial results. Every persona must contribute before consensus can be determined.

**Gate**: All 5 persona reports received. Each report contains ratings for all proposals and a ranked list. Proceed only when gate passes.

### Phase 4: SYNTHESIZE

**Goal**: Build a consensus matrix and identify agreement, disagreement, and cross-cutting patterns.

**Step 1: Build the consensus matrix**

Create a matrix: proposals (rows) x personas (columns) x ratings. See the consensus matrix template in `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md`.

**Step 2: Classify consensus patterns**

For each proposal, classify:
- **CONSENSUS** (4+ personas agree within one tier): Strong signal
- **CONTESTED** (2-3 split): The disagreement itself is informative
- **OUTLIER** (1 disagrees with 4): Worth understanding why one persona sees differently

**Step 3: Extract disagreement specifics**

For CONTESTED and OUTLIER proposals, extract the specific disagreement:
- What does each side see that the other does not?
- Is the disagreement about values (what matters) or facts (what is true)?
- Does one persona have domain-relevant insight the others lack?

**Step 4: Calculate weighted consensus score**

Assign numeric values: STRONG=3, PROMISING=2, WEAK=1, REJECT=0

For each proposal: sum all 5 ratings, giving a score from 0-15.

**Step 5: Rank proposals by consensus score**

Sort proposals from highest to lowest weighted score. Note ties and what distinguishes tied proposals.

**Gate**: Consensus matrix complete with classifications, disagreement analysis, and ranked scores. Proceed only when gate passes.

### Phase 5: PRESENT

**Goal**: Deliver the synthesis report using the template from `${CLAUDE_SKILL_DIR}/references/synthesis-template.md`.

Load the synthesis template and populate all 7 sections (Consensus Matrix; Features to Build; Worth Investigating; Interesting Disagreements; Shelve; Cross-Cutting Insights; Deepest Insight). See `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md` (Phase 5: Synthesis Report Sections) for each section's purpose and score-band criteria.

**Gate**: Report complete with all sections populated. Critique done.

---

<!-- no-pair-required: section-header-only; individual failure modes below carry Do-instead blocks -->
## Examples, Error Handling, and Detection

See `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md` for:

- **Examples**: critique provided proposals, generate+critique ideas, evaluate architectural options
- **Failure modes**: averaging disagreement, post-hoc rationalization, consensus-as-truth, skipping justification, resolving contested items, sequential execution
- **Error Handling**: bare ratings, skipped proposals, uniform agreement, fewer than 2 proposals

---

## References

### Reference Files
- `${CLAUDE_SKILL_DIR}/references/personas.md`: Full persona specifications, identity, evaluation criteria, prompt templates
- `${CLAUDE_SKILL_DIR}/references/synthesis-template.md`: Consensus matrix format and synthesis report structure
- `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md`: Worked examples, failure modes, error handling

### Related Skills
- `roast`: Code critique with evidence-based validation (complementary — roast critiques code, this critiques ideas)
- `decision-helper`: Weighted decision scoring for architectural choices (narrower — single-dimension scoring vs multi-persona critique)
