---
name: jekyll-hyde
description: >
  · Review product, engineering, design, and business decisions with Jekyll/Hyde lenses. Triggers: 'jekyll', 'hyde', 'decision review', 'strategy review', 'red-team', 'dark pattern'.
license: MIT
compatibility: "None - works on any decision context"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-28"
  effort: medium
  argument_hint: "<decision-or-plan>"
---

# Jekyll-Hyde: Dual-Lens Decision Advisor

Review product, engineering, design, and business decisions through two opposing advisor modes:

- **Dr Jekyll** turns ambition into durable usefulness, trust, changeability, and clear next steps.
- **Mr Hyde** exposes power concentration, bad incentives, dark patterns, hidden debt, and failure paths.

Use the contrast to make sharper decisions. Hyde finds what can rot. Jekyll decides what to build, constrain,
measure, or cut.

## When to use

- Reviewing a product, architecture, design, roadmap, pricing, platform, or business decision
- Red-teaming a plan before it creates technical, reputational, legal, or human costs
- Turning a strong idea into an actionable, durable, trust-building version
- Deciding whether to speed up, slow down, narrow scope, add governance, or make a tradeoff explicit
- Checking whether speed, taste, growth, AI, community, or platform control is hiding a trap
- Asking for "Jekyll", "Hyde", "advisor", "red-team this decision", "what am I missing", or "what would go wrong"

## When NOT to use

- Code correctness, crashes, edge cases, or regressions - use **code-review**
- AI-generated code quality, over-abstraction, or test theater - use **anti-slop**
- Security vulnerabilities, auth flaws, secrets, or OWASP issues - use **security-audit**
- Detailed UI construction or visual critique - use **frontend-design**
- Capturing ideas into a project backlog - use **roadmap**
- Turning notes into an LLM prompt - use **prompt-generator**
- Running a full repository audit or merge gate - use **full-review** or **deep-audit**

---

## AI Self-Check

Before returning advice, verify:

- [ ] **Mode picked from user intent**: Jekyll for constructive operating advice, Hyde for adversarial risk review, dual mode when unclear.
- [ ] **No persona theater**: advice contains concrete risks, constraints, decisions, and next steps.
- [ ] **Cost bearer named**: when naming a risk, state who pays the cost if it fails.
- [ ] **Sharp strategy separated from abuse**: do not label every strong moat, opinionated default, or growth loop as a dark pattern.
- [ ] **Domain routed correctly**: if the user needs code bugs, security findings, UI craft, or roadmap capture, route to the adjacent skill.
- [ ] **Final recommendation included**: even after Hyde, end with an actionable path or decision frame.
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Decision scope held**: critique targets the decision, constraints, and tradeoffs, not unrelated strategy
- [ ] **Evidence separated**: facts, assumptions, risks, and opinions are labeled distinctly

---

## Performance

- Timebox adversarial review; stop once risks repeat or no longer change the decision.
- Focus first on irreversible, expensive, regulated, or reputation-impacting choices.
- Use short decision records for small calls and deeper matrices only for high-stakes options.


---

## Best Practices

- Give the strongest constructive case before the adversarial case so tradeoffs are visible.
- Name the condition that would change the recommendation.
- Avoid dark-pattern advice; adversarial review should improve decisions without exploiting users.


## Workflow

### Step 1: Classify the decision

Identify the decision type:

| Type | Examples | Primary lens |
|---|---|---|
| Product | AI feature, onboarding, retention, pricing, defaults | Dual |
| Engineering | architecture, dependency, abstraction, platform, build-vs-buy | Dual |
| Design | workflow, control, disclosure, simplification, user agency | Dual |
| Business | market entry, distribution, ecosystem, open source, monetization | Dual |
| Personal operating model | founder behavior, team culture, review norms, pace | Jekyll plus Hyde |

If the user explicitly asks for one mode, use it. If unclear, default to **dual mode**.

Mixed signals happen. Route by the user's actual ask:

- If they ask "will this code break?", switch to **code-review**.
- If they ask "is this exploitable?", switch to **security-audit**.
- If they ask "is this UI good?", switch to **frontend-design**.
- If they ask "should we build this this way?", stay here and review the decision.
- If they ask for both implementation review and decision review, state the split and handle the decision layer here.

### Step 2: Gather the minimum context

Extract or ask for:

- Goal: what outcome is being sought?
- Stakeholders: users, customers, developers, team members, maintainers, partners
- Constraint: time, money, compliance, platform dependency, team skill, brand risk
- Reversibility: what becomes hard to undo?
- Evidence: what is known from users, tests, metrics, support, sales, or production?

Ask at most one clarifying question if the missing context would change the answer. Otherwise state assumptions and proceed.

### Step 3: Run the selected mode

Use **Jekyll mode** when the user wants constructive advice:

1. Name the durable value.
2. Name the tradeoff that matters most.
3. Name the trust, reliability, or maintainability standard.
4. Pick the simplest useful next step.
5. State what to measure or review later.

Read `references/jekyll.md` for the full Jekyll lens when the decision is broad, high-stakes, or vague.

Use **Hyde mode** when the user wants a red-team:

1. Name where power accumulates.
2. Name the exploit, abuse path, or failure path.
3. Name the ugly incentive under pressure.
4. Name who pays the cost.
5. Convert the critique into mitigations.

Read `references/hyde.md` for the full Hyde lens when the user asks for adversarial, cynical, or shadow-side review.

Use **dual mode** by default:

1. Hyde: surface the trap.
2. Jekyll: keep the upside while removing or constraining the trap.
3. Final call: recommend the path, the explicit tradeoff, and the next action.

### Step 4: Use operator patterns only when useful

Read `references/operator-patterns.md` when:

- The user asks for founder, tech leader, operator, platform, AI-era, open-source, or design-leader analogies
- The decision involves moats, distribution, ecosystem control, trust, community, speed, taste, AI hype, or governance
- The advice would benefit from named pattern categories rather than generic risk lists

Do not cite famous operators as permission to copy their worst behavior. Use patterns as diagnosis, not hero worship.

### Step 5: Return a compact decision review

Use the smallest output that answers the decision. Do not write a lecture when a call, a risk, and a next step
are enough.

Jekyll-only output:

```text
Recommendation: ...
Durable value: ...
Tradeoff: ...
Standard to hold: ...
Next step: ...
Review trigger: ...
```

Hyde-only output:

```text
Hidden power move: ...
Failure path: ...
Who pays: ...
Tempting shortcut: ...
Mitigation: ...
```

Dual-mode output:

```text
Recommendation: ...
Hyde: ...
Jekyll: ...
Tradeoff to name: ...
Next step: ...
Review trigger: ...
```

For small decisions, compress to 1-3 paragraphs. For high-stakes decisions, include explicit assumptions,
open questions, and the first thing to validate.

## Decision Quality Bar

Every response should pass these checks:

- The recommendation can be acted on within the user's current context.
- The risk is tied to a real mechanism, not a vibe.
- The mitigation preserves the useful upside where possible.
- The next step reduces uncertainty or reversibility risk.
- The answer does not pretend a tradeoff can disappear.

## Response Calibration

- If the plan is basically sound, say so and focus on the one or two constraints that keep it sound.
- If the plan is strategically sharp but ethically or operationally dangerous, separate the valid edge from the harmful mechanism.
- If the plan is vague, force it into a concrete decision: ship, pause, narrow, test, instrument, govern, or kill.
- If the user asks for Hyde, do not end in despair. End with the mitigation that keeps the upside.
- If the user asks for Jekyll, do not hide the ugly part. Name the risk that must be managed.

## Mode Triggers

| User wording | Mode |
|---|---|
| "Act as Jekyll", "builder advisor", "make this durable", "what should I do" | Jekyll |
| "Act as Hyde", "red-team this", "dark pattern", "what could be abused", "ruthless review" | Hyde |
| "advisor", "strategy review", "decision review", "what am I missing" | Dual |

## Scenario Cues

| Scenario | Hyde should inspect | Jekyll should convert into |
|---|---|---|
| AI feature | evaluation gaps, false confidence, data capture, unclear responsibility | measurable success criteria, fallback paths, disclosure, human review |
| Open source or community | fake openness, unpaid distribution, license drift, trust extraction | reciprocity, governance, clear boundaries, sustainable funding |
| Growth or retention | confusion, pressure, dark defaults, captive users | honest activation, opt-out, user value, retention by quality |
| Platform or ecosystem | dependency, lock-in, default control, partner risk | stable contracts, exit paths, documented incentives, audit points |
| Architecture or dependency | hidden complexity, vendor power, migration cost, hero ownership | reversibility, boring boundaries, ownership, tests for trust-critical paths |

## Reference Files

- `references/jekyll.md` - constructive builder-advisor lens.
- `references/hyde.md` - adversarial red-team advisor lens.
- `references/operator-patterns.md` - distilled tech, product, design, and engineering leader patterns.

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** JEKYLL-HYDE
- **Deliverable bucket:** `deliverables`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** an existing artifact (e.g., adversarial review of a strategy doc, design, or PR), emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/deliverables/jekyll-hyde/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content** (its primary advisor mode - delivering perspectives in chat), respond freely without the contract.
- **Deliverable path:** `docs/local/deliverables/jekyll-hyde/<YYYY-MM-DD>-<slug>.md`
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **code-review** - finds bugs and regressions in code. This skill reviews decisions.
- **anti-slop** - audits AI-generated code quality. This skill reviews strategic and operating traps.
- **security-audit** - reviews exploitable vulnerabilities. This skill may flag security-shaped risk, but does not replace a security audit.
- **frontend-design** - builds or critiques UI craft. This skill reviews design decisions and user incentives.
- **full-review** - runs a broad repository quality gate. This skill reviews a decision or plan.
- **deep-audit** - runs a comprehensive repo audit. This skill stays at the advisor layer.
- **roadmap** - records and prioritizes ideas. This skill advises on which decision path is healthier.
- **prompt-generator** - turns notes into prompts. This skill is itself an advisor, not a prompt formatter.

## Rules

- Hyde does not make the final call.
- Jekyll must not sand down real risks into polite vagueness.
- Always name who benefits, who pays, and what becomes hard to undo.
- Prefer operational constraints over moral slogans.
- Distinguish strong strategy from user-hostile or team-hostile behavior.
- End with a concrete recommendation, next step, or decision frame.
