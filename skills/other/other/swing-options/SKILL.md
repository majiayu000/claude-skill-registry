---
name: swing-options
description: Generate probability-weighted alternative options that challenge default thinking. Forces unconventional alternatives and exposes hidden assumptions behind the "obvious" choice. For decision-point analysis, NOT full design exploration (use brainstorming for that). Triggers on "대안", "alternatives", "옵션 뽑아", "options", "어떤 방법이", "아이디어", "다른 방법", "선택지".
argument-hint: "[decision or question to explore]"
---

# Creativity Sampler

Probability-weighted option generator that fights typicality bias and surfaces unconventional alternatives. The core value is **exposing hidden assumptions** behind the "obvious" choice.


## Rules (Absolute)

1. **Generate exactly 5 options by default.** If the decision space has fewer than 4 genuinely distinct approaches, generate all distinct approaches plus at least 1 unconventional reframing of the problem itself. Never pad with trivially different variations of the same idea. If the user specifies a different count, respect it.
2. **At least 1 option must be unconventional** (Unconventional or Wild card zone). This is the whole point — surface ideas that would normally be suppressed.
3. **Assign relative probability zones** that indicate typicality, not quality. Base estimates on observable signals where possible: community adoption, tutorial prevalence, StackOverflow frequency, conference talk frequency. When precise probabilities cannot be grounded, use zone labels instead:
   - **Conventional** (p > 40%) — the "obvious" choice most would pick
   - **Mainstream** (p 20-40%) — commonly considered alternative
   - **Uncommon** (p 10-20%) — valid but often overlooked
   - **Unconventional** (p 5-10%) — challenges assumptions
   - **Wild card** (p < 5%) — radical rethink
   At least one option must come from the bottom two zones.
4. **Lower probability = more creative**, not worse. Explicitly frame low-p options as valuable exploration.
5. **No default recommendation.** Present all options as viable. Let the user decide after seeing trade-offs.
6. **Trade-off analysis is mandatory.** Each option must have concrete pros/cons, not vague descriptions.
7. **Ambiguous inputs require clarification.** If the decision question is too vague to determine what "unconventional" means, ask one clarifying question about constraints before generating options. Constraints determine the boundary between conventional and unconventional.

## Process

### Step 1: Check Input Clarity

Before generating options, verify:
- Is the decision clearly stated?
- Are enough constraints known to distinguish conventional from unconventional?

If not, ask **one** targeted question. Example: "What's your biggest constraint — timeline, budget, or team expertise? This determines which options count as unconventional for your situation."

### Step 2: Frame the Decision Space

Identify:
- What is being decided? (technology, architecture, approach, design, strategy)
- What are the constraints? (time, budget, team skill, existing stack)
- What would the "obvious" answer be? (this is what we want to challenge)

### Step 3: Generate Options (Distribution-First)

Sample across the full probability distribution, NOT just the top-1 most likely answer.

```
Probability zones (use zone labels when precise % cannot be grounded):
  Conventional  (p > 40%)  — the "obvious" choice most would pick
  Mainstream    (p 20-40%) — commonly considered alternative
  Uncommon      (p 10-20%) — valid but often overlooked
  Unconventional (p 5-10%) — challenges assumptions
  Wild card     (p < 5%)   — radical rethink, paradigm shift
```

Force at least one option from each of the bottom two zones.

### Step 4: Analyze Each Option

For every option, provide:
1. **What it is** (1 sentence)
2. **Why it might be the best choice** (strongest argument FOR)
3. **Why it might fail** (strongest argument AGAINST)
4. **Best suited when...** (specific scenario where this option wins)
5. **Estimated effort** relative to other options (Low / Medium / High)

### Step 5: Surface Hidden Assumptions

After presenting all options, explicitly state:
- "The conventional choice assumes [X]. If that assumption is wrong, consider options [Y, Z]."
- Identify which constraints, if removed, would change the ranking.

## Output Format

```markdown
## Decision: [The question being decided]

### Constraints
- [constraint 1]
- [constraint 2]

### Options

#### 1. [Option Name] — Conventional (p ~ XX%)
> [One-line description]

| Dimension | Assessment |
|-----------|------------|
| Best argument FOR | [concrete reason] |
| Best argument AGAINST | [concrete reason] |
| Best suited when | [specific scenario] |
| Effort | Low / Medium / High |
| Risk level | Low / Medium / High |

#### 2. [Option Name] — Mainstream (p ~ XX%)
> ...

#### 3. [Option Name] — Uncommon (p ~ XX%)
> ...

#### 4. [Option Name] — Unconventional (p ~ XX%)
> ...

#### 5. [Option Name] — Wild card (p ~ XX%)
> ...

### Hidden Assumptions
- The conventional choice (Option 1) assumes: [assumption]
- If [condition changes], reconsider: Option [N]
- Constraint "[X]" was taken as fixed — but is it really?

### Decision Matrix

| Criteria | Opt 1 | Opt 2 | Opt 3 | Opt 4 | Opt 5 |
|----------|-------|-------|-------|-------|-------|
| [user constraint 1] | Strong / Moderate / Weak | ... | ... | ... | ... |
| [user constraint 2] | Strong / Moderate / Weak | ... | ... | ... | ... |
| [user constraint 3] | Strong / Moderate / Weak | ... | ... | ... | ... |
| **Hidden criterion:** [X] | Strong / Moderate / Weak | ... | ... | ... | ... |

### Decision Matrix Rules
- Derive 3-5 criteria **directly from the user's stated constraints** (budget, timeline, team size, etc.)
- Add exactly 1 criteria the user did NOT mention but should consider (label it "Hidden criterion")
- Rate each option per criterion: **Strong** / **Moderate** / **Weak** (relative to the other options)
- Do NOT use numerical scores — they imply false precision for qualitative assessment
- If one option dominates across all criteria, explicitly note this in Hidden Assumptions — the criteria selection may be biased toward the conventional choice
```

## Quality Calibration

### BAD Output (what to avoid)

```markdown
## Decision: Which database for our new service?

#### 1. PostgreSQL — p ≈ 35%
#### 2. MySQL — p ≈ 25%
#### 3. MariaDB — p ≈ 20%
#### 4. CockroachDB — p ≈ 12%
#### 5. Amazon Aurora — p ≈ 8% ⚡ Unconventional

### Hidden Assumptions
- PostgreSQL is probably the best choice for most use cases.
```

Problems:
- Options 1-3 are trivially different (all traditional SQL, same paradigm)
- Probabilities are ungrounded — why 35% vs 25%?
- "Unconventional" option (Aurora) is just a managed version of the same thing
- Hidden Assumptions section adds nothing — restates the obvious
- No real diversity of approach

### GOOD Output (what to aim for)

```markdown
## Decision: Which database for our new service?

### Constraints
- Team of 3, familiar with SQL
- Read-heavy analytics + some transactional writes
- Budget: < $500/mo infra

#### 1. PostgreSQL — Conventional (p ~ 50%)
> Battle-tested relational DB with strong analytics extensions (pg_analytics, TimescaleDB).

#### 2. ClickHouse + SQLite — Uncommon (p ~ 15%)
> Split reads (ClickHouse for analytics) from writes (SQLite for transactions). Optimizes for actual access pattern.

#### 3. DuckDB embedded — Unconventional (p ~ 8%)
> In-process analytical DB. Zero infrastructure. Handles the read-heavy workload at zero cost; pair with any simple write store.

#### 4. Managed Supabase — Mainstream (p ~ 22%)
> PostgreSQL with auth/APIs built-in. Trades control for development speed.

#### 5. Event sourcing + materialized views — Wild card (p ~ 5%)
> Don't pick a database — design the data flow. Events are the source of truth; views are disposable projections. Database becomes an implementation detail you can swap later.

### Hidden Assumptions
- The conventional choice assumes your read and write patterns are similar enough for one DB. If analytics queries are 10x more frequent than writes, a split architecture (Opt 2, 3) may cost less and perform better.
- "Team knows SQL" is treated as a constraint, but DuckDB (Opt 3) is also SQL — the real constraint is operational complexity, not query language.
- If the service grows past the team of 3, Option 5's event sourcing makes future database migrations trivial — worth considering if you expect growth.
```

Why this is better:
- Each option represents a **fundamentally different approach** (single DB, split architecture, embedded, managed, paradigm shift)
- Zone labels are grounded in observable adoption patterns
- Hidden Assumptions section **challenges the framing** and links back to specific options
- Wild card option reframes the problem itself, not just picks an obscure technology

## When to Use

- Architecture decisions: "monolith vs microservices vs..."
- Technology selection: "which database/framework/language"
- Design approaches: "how should we structure this feature"
- Strategy: "how should we launch/market/scale this"
- Problem-solving: "how can we fix/improve/optimize this"
- Any moment where you catch yourself defaulting to one obvious answer

## When NOT to Use

- Factual questions with one correct answer (use `swing-research`)
- Tasks with clear requirements and no decision points
- Simple implementation where the approach is obvious and uncontested
- When user has already decided and just wants execution

## Integration Notes

- **With swing-clarify:** Run swing-clarify first on ambiguous requests before invoking this skill. Clarified scope produces better results.
- **With brainstorming:** Can replace the "Propose 2-3 approaches" phase with deeper divergent options
- **With swing-review:** Feed the chosen option into adversarial review for stress-testing
- **Standalone:** Invoke directly with `/swing-options [question]` for quick decision support

## Anti-Patterns to Avoid

- **False diversity:** Don't generate options that are minor variations of the same thing. Each option should represent a fundamentally different approach or paradigm.
- **Probability theater:** Don't assign specific percentages you can't ground. Use zone labels when you lack observable data. "Conventional" is honest; "p = 37.2%" is not.
- **Burying the lead:** If one option is dramatically better given the constraints, say so in Hidden Assumptions — but still present all options fairly.
- **Ignoring constraints:** Wild card options should still be achievable within stated constraints, just via unexpected paths.
- **Toothless Hidden Assumptions:** "Option 1 is probably best" is not an assumption analysis. Name the specific assumption, state what would break it, and point to which options benefit.
- **Criteria laundering:** Don't pick Decision Matrix criteria that naturally favor the conventional choice. If Option 1 wins every row, your criteria are biased — call it out.
