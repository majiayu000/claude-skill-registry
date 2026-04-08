---
name: swing-trace
description: Exposes Claude's reasoning chain as an auditable, decomposable artifact. Quick mode (default) gives assumption inventory + weakest-link in 2 stages. Full mode (--full) adds decision branching, confidence decomposition, and falsification conditions. Triggers on "왜 그렇게 생각해", "reasoning", "근거", "show your work", "어떻게 그 결론이", "trace", "판단 근거", "why do you think that".
argument-hint: "[question to trace] [--full for complete 5-stage analysis]"
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# Reasoning Tracer

Anti-black-box engine that makes reasoning chains visible, auditable, and decomposable.

> Addresses the cognitive failure mode of **black-box reasoning** -- Claude gives an answer but the user cannot see what assumptions were relied on, what alternatives were rejected, or which part of the reasoning is weakest.


## Rules (Absolute)

1. **Never present a single-path narrative.** Every trace must show at least one rejected alternative at a meaningful decision fork. "I considered X but chose Y because Z" is the minimum; two rejected alternatives is preferred.
2. **Confidence decomposition requires 3+ sub-components.** Overall confidence is always broken into at least three independent dimensions, each with its own percentage and justification.
3. **Every assumption gets rated.** Each assumption must have an explicit criticality rating (High/Medium/Low) and verifiability rating (Directly Verifiable / Indirectly Verifiable / Unverifiable). No unrated assumptions.
4. **Weakest Link is MANDATORY.** Never skip it. This is the highest-value section -- it tells the user exactly where to focus their own verification effort.
5. **No confidence theater.** Do not assign high confidence (>80%) without specific justification. Vague appeals to "experience" or "common knowledge" are banned. Every confidence level must cite a concrete basis.
6. **Distinguish evidence types.** Separate empirical evidence (benchmarks, data, test results) from theoretical reasoning (design principles, heuristics) from authority (docs, expert consensus). Label which type supports each claim.
7. **Trace must be falsifiable.** Every conclusion must include conditions under which it would be wrong. If you cannot state what would disprove your conclusion, the reasoning is insufficiently rigorous.


## Mode Selection

### Quick Mode (Default)
When invoked without `--full`, execute only:
1. **Stage 1: Claim Isolation** — break into atomic claims
2. **Stage 2: Assumption Inventory** — enumerate assumptions with criticality/verifiability
3. **Stage 5: Weakest Link & Alternative Conclusion** — identify the single most fragile assumption

Skip Stages 3 (Decision Tree) and 4 (Confidence Decomposition).

Quick mode output format:

```markdown
## Reasoning Trace: [Claim]

### Atomic Claims
1. [Claim 1]
2. [Claim 2]

### Assumption Inventory
| # | Assumption | Criticality | Verifiability |
|---|-----------|-------------|---------------|
| A1 | ... | High/Med/Low | Direct/Indirect/Unverifiable |

### Weakest Link
**Assumption [A#]:** [restate]
- **Why weakest:** [explanation]
- **If wrong:** [alternative conclusion]
- **How to verify:** [concrete steps]
```

### Full Mode (--full)
When invoked with `--full`, execute all 5 stages as documented below.


## Process

Execute these 5 stages sequentially. Do NOT skip stages.

### Stage 1: Claim Isolation

Identify the exact claim(s) being traced. Separate compound questions into atomic claims.

```
Input: "Why did you recommend microservices over a monolith?"
Atomic claims:
  1. Microservices are a better architectural fit for this project
  2. The team can handle microservices operational complexity
  3. The migration cost is justified by long-term benefits
```

Each atomic claim gets its own assumption inventory and confidence score.

### Stage 2: Assumption Inventory

For each atomic claim, enumerate every assumption the reasoning depends on. Each assumption gets three attributes:

| # | Assumption | Criticality | Verifiability |
|---|-----------|-------------|---------------|
| A1 | [Statement] | **High** -- conclusion changes if wrong | Directly Verifiable -- can test/measure |
| A2 | [Statement] | **Medium** -- conclusion weakens if wrong | Indirectly Verifiable -- can infer from proxy data |
| A3 | [Statement] | **Low** -- conclusion survives if wrong | Unverifiable -- must be accepted or rejected on judgment |

**Criticality scale:**
- **High:** If this assumption is wrong, the conclusion flips or becomes unjustifiable.
- **Medium:** If wrong, the conclusion weakens significantly but may still hold with caveats.
- **Low:** If wrong, the conclusion is largely unaffected.

**Verifiability scale:**
- **Directly Verifiable:** Can be tested, measured, or confirmed from authoritative sources.
- **Indirectly Verifiable:** Can be inferred from related data, benchmarks, or analogies.
- **Unverifiable:** Requires judgment, prediction, or depends on future unknowns.

### Stage 3: Decision Tree with Branch Justifications

At each significant fork in the reasoning, document:

1. **Decision point:** What question needed answering?
2. **Options considered:** At least 2 (the chosen path + minimum 1 rejected alternative).
3. **Evaluation criteria:** What factors determined the choice?
4. **Chosen path:** Which option was selected?
5. **Rejection rationale:** Why each alternative was rejected -- with specifics, not hand-waving.
6. **Reversal condition:** What would need to be true for the rejected alternative to become the better choice?

```
Decision Point: Database selection
  ├─ Option A: PostgreSQL [CHOSEN]
  │   Strengths: ACID compliance, JSON support, ecosystem maturity
  │   Evidence type: Empirical (benchmarks) + Authority (industry adoption data)
  │
  ├─ Option B: SQLite [REJECTED]
  │   Strengths: Zero-config, embedded, fast for reads
  │   Rejection: Write concurrency limit (~5 writers) incompatible with
  │              multi-instance deployment requirement (Assumption A2)
  │   Reversal: If deployment is single-instance AND write volume < 100/sec,
  │             SQLite becomes the simpler, better choice
  │
  └─ Option C: MongoDB [REJECTED]
      Strengths: Schema flexibility, horizontal scaling
      Rejection: Data has strong relational structure (7 FK relationships);
                 denormalization cost outweighs flexibility benefit
      Reversal: If schema changes weekly or data is primarily document-shaped
```

### Stage 4: Confidence Decomposition

Break overall confidence into independent sub-components. Minimum 3, recommended 4-6.

Each sub-component gets:
- A percentage (0-100%)
- The evidence type supporting it (Empirical / Theoretical / Authority / Mixed)
- A 1-2 sentence justification citing the specific basis

```
Overall Confidence: 72%

Sub-components:
  Technical Feasibility:   90% [Empirical] -- proven in similar systems (refs: X, Y benchmarks)
  Timeline Estimate:       45% [Theoretical] -- based on analogy to past project, but team composition differs
  Cost Projection:         60% [Mixed] -- infrastructure costs are empirical, opportunity cost is estimated
  Team Capability Match:   75% [Authority] -- based on stated team skills; not independently verified
  Risk Assessment:         80% [Theoretical] -- standard failure modes well-understood; novel integration untested

Weighted Overall: (90*0.3 + 45*0.25 + 60*0.15 + 75*0.15 + 80*0.15) = 71.5% ≈ 72%
```

The overall confidence is NOT the average. Weight sub-components by their importance to the conclusion.

### Stage 5: Weakest Link & Alternative Conclusion

**Weakest Link Identification:**
Which single assumption or sub-conclusion, if wrong, would MOST change the final answer?

Criteria for selecting the weakest link:
1. Highest criticality among assumptions
2. Lowest verifiability (hardest to confirm)
3. Lowest confidence among sub-components
4. The intersection of these three factors is the weakest link

**Alternative Conclusion:**
"If [weakest link assumption] is wrong, then the conclusion changes to [X]."

This is not hypothetical filler -- it must be a genuinely reasoned alternative conclusion that follows logically from negating the weakest assumption.


## Output Format

```markdown
## Reasoning Trace: [Claim/Question]

### Atomic Claims
1. [Claim 1]
2. [Claim 2]
3. [Claim N]

### Assumption Inventory
| # | Assumption | Criticality | Verifiability | Tied to Claim |
|---|-----------|-------------|---------------|---------------|
| A1 | [Statement] | High | Directly Verifiable | Claim 1 |
| A2 | [Statement] | High | Unverifiable | Claim 2 |
| A3 | [Statement] | Medium | Indirectly Verifiable | Claim 1, 3 |
| ... | ... | ... | ... | ... |

### Decision Forks

#### Fork 1: [Decision Point]
- **Chosen:** [Option] -- [rationale with evidence type label]
- **Rejected:** [Option] -- [specific rejection reason]
  - *Reversal condition:* [what would make this the right choice]
- **Rejected:** [Option] -- [specific rejection reason]
  - *Reversal condition:* [what would make this the right choice]

#### Fork 2: [Decision Point]
...

### Confidence Decomposition
| Dimension | Confidence | Evidence Type | Basis |
|-----------|-----------|---------------|-------|
| [Dimension 1] | XX% | Empirical | [specific justification] |
| [Dimension 2] | XX% | Theoretical | [specific justification] |
| [Dimension 3] | XX% | Authority | [specific justification] |
| [Dimension N] | XX% | Mixed | [specific justification] |

**Overall Confidence: XX%** (weighted by dimension importance)

### Weakest Link
**Assumption [A#]:** [restate the assumption]
- **Criticality:** High
- **Verifiability:** [rating]
- **Current confidence in this assumption:** XX%
- **Why this is the weakest link:** [explanation]
- **How to verify:** [concrete steps the user can take]

### Alternative Conclusion
> If **[weakest assumption]** is wrong, then:
> [Alternative conclusion with reasoning -- not a throwaway sentence but a genuinely traced alternative]

### Falsification Conditions
The main conclusion is wrong if ANY of these turn out to be true:
1. [Condition 1]
2. [Condition 2]
3. [Condition N]
```


## Quality Calibration

### BAD Example (Do NOT produce this)

```
Q: "Why did you recommend React over Vue?"

I recommended React because it has a larger ecosystem, more job
postings, and better TypeScript support. It's the safer choice
for most teams because it's battle-tested at scale by Meta and
many other companies.

Confidence: High.
```

Problems:
- No assumptions stated -- what is this "high confidence" based on?
- No alternatives explored -- was Vue even seriously considered?
- No weakest link -- where should the user push back?
- No decision forks -- what criteria determined "larger" or "better"?
- "Battle-tested at scale" is an appeal to authority without specifics
- Reads like a marketing pitch, not a reasoning trace

### GOOD Example (Target this quality)

```
## Reasoning Trace: Why React over Vue for this project?

### Atomic Claims
1. React is a better framework fit for this project's requirements
2. The team will be more productive with React than Vue
3. React's ecosystem advantage outweighs Vue's simplicity advantage

### Assumption Inventory
| # | Assumption | Criticality | Verifiability | Tied to Claim |
|---|-----------|-------------|---------------|---------------|
| A1 | Team has 2+ engineers with React experience | High | Directly Verifiable | Claim 2 |
| A2 | Project requires complex state management | Medium | Directly Verifiable | Claim 1 |
| A3 | Hiring pipeline will favor React candidates | High | Indirectly Verifiable | Claim 2 |
| A4 | Project will need SSR capabilities | Medium | Directly Verifiable | Claim 1 |
| A5 | TypeScript will be used project-wide | Low | Directly Verifiable | Claim 3 |

### Decision Forks

#### Fork 1: Framework Selection
- **Chosen:** React -- larger component ecosystem (npm: 90k+ packages
  tagged "react" vs 25k+ "vue"), more mature SSR story (Next.js 15 stable
  vs Nuxt 4 recent), team has existing React experience (A1)
- **Rejected:** Vue -- lower learning curve, better developer ergonomics
  for smaller teams, Composition API is excellent
  - *Reversal condition:* If team has 0 React experience AND project is
    < 6 month lifespan AND no SSR needed, Vue's faster onboarding wins
- **Rejected:** Svelte -- best DX, smallest bundle, genuinely better
  reactivity model
  - *Reversal condition:* If team is greenfield (no framework experience),
    project is performance-critical consumer app, and hiring is not a
    constraint (small, stable team)

### Confidence Decomposition
| Dimension | Confidence | Evidence Type | Basis |
|-----------|-----------|---------------|-------|
| Framework capability match | 85% | Empirical | Feature comparison against requirements doc |
| Team productivity | 55% | Mixed | Based on stated skills (A1); not observed |
| Ecosystem longevity | 80% | Authority | Meta backing, npm download trends, State of JS 2025 |
| Hiring advantage | 50% | Indirectly Empirical | LinkedIn job postings (3:1 React:Vue ratio, but market shifts) |

**Overall Confidence: 68%** (productivity and hiring are uncertain
but heavily weighted)

### Weakest Link
**Assumption A1:** Team has 2+ engineers with React experience
- **Criticality:** High
- **Verifiability:** Directly Verifiable
- **Current confidence:** 70% (stated by PM, not verified via code review)
- **Why this is the weakest link:** If the team lacks real React
  experience, the productivity advantage evaporates and Vue's lower
  learning curve becomes the dominant factor
- **How to verify:** Review team members' recent commits; conduct
  brief technical screen on React patterns (hooks, context, suspense)

### Alternative Conclusion
> If **team React experience (A1)** is overstated, then Vue is the
> better choice: its gentler learning curve (Composition API maps
> well to React hooks mental model but with less boilerplate),
> better documentation, and faster time-to-productive offset the
> smaller ecosystem. The recommendation flips to Vue with Nuxt.

### Falsification Conditions
1. Team has < 2 engineers genuinely proficient in React (not just "used it once")
2. Project scope shrinks to < 6 months with no SSR requirement
3. Hiring is not a concern (stable team, no growth planned)
```


## When to Use

- After any recommendation: "Why Postgres?" "Why microservices?" "Why this library?"
- After any estimate: "Why 2 weeks?" "Why $50k?" "Why 3 engineers?"
- During architecture decisions where stakeholders need to audit the reasoning
- Code review rationale: "Why did you flag this as a security issue?"
- When the user says "convince me" or "I'm not sure about this"
- Post-mortem analysis: "Why did we think X would work?"
- Any high-stakes decision where the reasoning must survive scrutiny

## When NOT to Use

- Simple factual lookups with clear answers ("What port does Postgres use?")
- Creative brainstorming where structured reasoning kills ideation (use `swing-options`)
- When the user wants a quick answer and explicitly says so
- Exhaustive code/system analysis without a specific claim to trace
- Stress-testing someone else's reasoning (use `swing-review` -- it attacks; this skill *exposes*)
- Research requiring external source verification (use `swing-research` for facts; this skill traces *reasoning about* facts)

## Gotchas

1. **Quick mode is the default.** Unless `--full` is specified, only run Stages 1, 2, and 5. Don't produce Decision Trees or Confidence Decomposition in quick mode — it wastes context.
2. **Never assign >80% confidence without citing specific evidence.** "Common knowledge", "well-known", "generally accepted" are not justifications. Name the benchmark, the doc, the test result.
3. **Weakest Link is mandatory in ALL modes.** Even quick mode. This is the single highest-value output — if you skip it, the entire trace is pointless.
4. **Rate every assumption.** An assumption without Criticality and Verifiability ratings is incomplete. No exceptions, no "obvious" ones that skip rating.
5. **Alternative Conclusion must be genuinely reasoned.** "If X is wrong, reconsider" is filler. Trace the actual alternative logic: "If X is wrong, then Y follows because Z."

## Integration Notes

- **With swing-clarify:** Run swing-clarify first on ambiguous requests before invoking this skill. Clarified scope produces better results.
- **Before swing-review:** Trace your reasoning first, then stress-test it. The assumption inventory from swing-trace feeds directly into swing-review's attack vectors.
- **After swing-research:** Research gathers verified facts; swing-trace then makes the *logic connecting those facts to a conclusion* transparent.
- **With swing-options:** When swing-options generates options, swing-trace can trace why one option was selected over others.
