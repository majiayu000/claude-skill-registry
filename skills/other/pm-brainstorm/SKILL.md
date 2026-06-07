---
name: pm-brainstorm
description: Проводит структурированный сеанс дивергенции вокруг конкретной продуктовой проблемы или возможности. Встроены SCAMPER (7 ракурсов), 5 Whys для поиска корневой причины, кросс-доменное вдохновение, ограничивающие инновации, обратный брейншторм и матрица Impact/Effort для отбора. На выходе — ≥10 идей с детально проработанным Top-3. User-invoked only — do NOT auto-trigger. Triggers on /pm-brainstorm, "идеи для продукта", "продуктовый брейншторм", "дивергенция идей", "How Might We", "SCAMPER", "product brainstorm", "feature ideas".
---

# pm-brainstorm — Structured product brainstorm


Part of the Personal Corp framework — running a one-person business through AI agents.
Run a structured creative-divergence session on a specific product problem or opportunity. Not just listing ideas — challenges assumptions, borrows across domains, helps reach options you wouldn't have otherwise. Output is a screened idea list ready for next-step action.

## Inputs

| Field | Required | Notes |
|---|---|---|
| Topic | yes | Problem to solve or opportunity to explore — more specific = better |
| Background | no | Persona, current data, known constraints |
| Mode | no | Full divergence / single framework only; default full |
| Constraints | no | Tech, time, resource limits |

> **Good topic:** "How might we make new users feel value within the first 5 minutes of first use?"
> **Bad topic:** "How do we improve the product?" (too vague)

## Step 1 — Problem focus

Before diverging, sharpen the problem.

**Probing checklist:**
1. **Who has this problem?** Specific user types and scenarios
2. **How is it solved today?** Current alternative or workaround
3. **Why does it matter?** Consequence of inaction
4. **What does success look like?** What does a good solution look like
5. **What constraints?** Tech / time / resource bounds

Restate as a **How Might We**:
- "How might we let {target user} more easily {achieve goal} in {scenario}?"

## Step 2 — SCAMPER (7 lenses)

Run each lens once; aim for 1-2 ideas per lens.

| Lens | Core question | Direction |
|---|---|---|
| **S — Substitute** | What component can be substituted? | Different tech / interaction / entry point? |
| **C — Combine** | Can we merge two features? | Merge steps / contexts / bundle features |
| **A — Adapt** | What from elsewhere can we borrow? | Method from social apps? From productivity tools? |
| **M — Modify** | What if we 10×'d or 0.1×'d this? | Minimal version? Maximal version? |
| **P — Put to other use** | What other context could this serve? | Other personas? Other scenarios? |
| **E — Eliminate** | What if we remove something? | Cut steps / fields / signup / friction? |
| **R — Rearrange** | What if we reorder? | Try first / signup later? Reverse order? |

Total: 7-14 initial ideas.

## Step 3 — 5-Whys root-cause divergence

From a user pain, descend to the root, then ideate from each layer.

**Example:**

**Pain:** new users churn on day 2
- **Why 1:** They didn't find what they wanted on day 1
  - **Why 2:** Feature entries are too deep
    - **Why 3:** Navigation is structured by product architecture, not user task
      - **Why 4:** No user-task analysis was done
        - **Why 5 (root):** Product design is detached from actual user scenarios
        - **Idea:** Run user-task analysis, restructure navigation by task
      - **Idea:** Add search / smart-recommendations entry point
    - **Idea:** Onboarding leads users directly to core feature
  - **Idea:** Ask intent at signup, personalize home

**Rules:**
- Probe to at least Why 3
- Each Why can fork (one symptom may have multiple causes)
- Generate 1-2 solutions per Why layer

## Step 4 — Cross-domain inspiration

Don't copy competitors — look at what they do, then think "what could we do that's different".

**Cross-domain prompts:**
1. List 3-5 products that are not direct competitors but solve a similar user need
2. Note what's notable about each
3. Ask: if we transplanted this approach to our context, what would adapt? What would change?

**Differentiation prompts:**
1. Everyone does X → what if we do Y instead?
2. Competitor's X is criticized for Z → could we cut into the pain at Z?
3. Need users discuss heavily on social media but no competitor has shipped → opportunity?

## Step 5 — Constraint-innovation

Deliberately set constraints to spark creativity.

| Constraint | Setup | Stimulus |
|---|---|---|
| **Time** | "Only 1 week of dev time" | Forces minimum viable approach |
| **Tech** | "Use only existing stack" | Reveals new uses of existing capabilities |
| **Cost** | "Zero dev investment" | Ops moves, config changes, copy tweaks |
| **Extreme** | "Change one line of code" | Find the highest-leverage single point |
| **Inversion** | "Let users design it" | Switch perspective |

1-2 ideas per constraint. Tighter constraints often produce more elegant ideas.

## Step 6 — Reverse brainstorm

First think "how could we make this worse", then invert each idea.

**Steps:**
1. Restate as the inverse: "How might we make new users uninstall on day 1?"
2. List everything that would worsen the problem (often easier than positive ideation)
3. Invert each "make-worse" idea into an improvement

**Example:**

| Make-worse | Inverted |
|---|---|
| Require 20 fields at signup | Phone-only signup, progressive profile fill |
| Home is full of ads | Home shows only goal-relevant content |
| Hide all help entries | Surface guidance proactively at confusion points |

> Reverse-brainstorm bypasses the "find the right answer" pressure — the divergence stage gets freer.

## Step 7 — Impact / Effort screening

Drop all ideas into a 2×2:

| Quadrant | Impact | Effort | Strategy | Ideas |
|---|---|---|---|---|
| **Quick Wins** | High | Low | Validate first | {list} |
| **Big Bets** | High | High | Worth investing, plan carefully | {list} |
| **Fill-ins** | Low | Low | When idle | {list} |
| **Money Pits** | Low | High | Drop | {list} |

**Scoring:**
- **Impact:** size of pain solved × users affected
- **Effort:** dev + design + integration test

## Step 8 — Output

```markdown
# Product Brainstorm

**Topic:** {problem}
**HMW:** How might we {restated as HMW}
**Date:** {today}
**Ideas generated:** {N} (kept after screening: {M})

## Idea List

| # | Idea | Pain solved | Source framework | Expected value | Effort | Quadrant | Validation |
|---|---|---|---|---|---|---|---|
| 1 | {desc} | {pain} | SCAMPER-Eliminate | High/Med/Low | High/Med/Low | Quick Win | {validation} |

## Top 3 Recommendations

### Idea 1: {name}
- **Description:** {detail}
- **Pain solved:** {specific pain}
- **Expected impact:** {quantified, e.g. "+5-10% D1 retention"}
- **Implementation path:** {brief tech / design approach}
- **Validation:** {how to validate fast — A/B test, gradual rollout, etc.}
- **Risk:** {risks and mitigation}

### Idea 2: {name}
…

### Idea 3: {name}
…

## Dropped Ideas (archived)
- {idea X}: dropped because — {reason}
- {idea Y}: dropped because — {reason}

## Next Actions
- [ ] {action 1}
- [ ] {action 2}
```

## Brainstorm principles

1. **Diverge before converge** — no judgment during divergence; screen during convergence
2. **Quantity drives quality** — first hit 15+ ideas, then screen
3. **Concrete beats abstract** — "add a progress bar at signup step 3" beats "improve signup UX"
4. **Allow extremes** — extreme ideas, refined, often become great
5. **Challenge assumptions** — push back on "impossible" / "we've always done it this way"

## Quality bar

1. ≥ 10 ideas generated (sufficient divergence)
2. Each idea has a concrete description (not vague "optimize X")
3. Ideas come from ≥ 3 different frameworks
4. Top 3 have explicit validation methods
5. Output is decision-ready as input to the next step

## Red lines

1. **No rejection during divergence** — never say "can't" / "impossible" while ideating
2. **No empty advice** — "improve UX" is fluff, not an idea
3. **Doesn't replace decision** — outputs options, not the choice

## When input is incomplete

- **Topic too broad** → narrow it (probe scenario and user)
- **Missing background** → ideate on generic product logic, tag "recommend specific data for sharper output"
- **Single framework specified** → use only that one, but suggest "more frameworks = more dimensions"

## Related skills

- `/pm-prd` — Top idea → PRD
- `/pm-prioritize` — Idea list → formal ranking
- `/pm-user-stories` — Ideas → developable Stories
- `/pm-feedback` — Pain points from feedback → brainstorm fuel
- `/pm-competitive` — Validate differentiation level

