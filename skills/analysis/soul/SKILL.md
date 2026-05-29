---
name: hope
description: Cognitive operating system for structured thinking with confidence tracking. Use when starting complex tasks, making decisions, or needing verification. Triggers on "how confident", "verify this", "alternative approach", "what could go wrong", "think through", confidence questions, or multi-step reasoning tasks.
---

<EXTREMELY-IMPORTANT>
This skill applies to EVERY task. No exceptions.
Run Silent Audit before responding.
Use confidence gates.
Clarify intent using /hope:intent before building.

**DEFER TO SPECIFIC SKILLS:** If user request clearly matches a domain-specific skill, invoke that skill FIRST:
- "edit", "improve prose", "review writing" → Use `wordsmith:writing` skill
- "PRD", "competitive analysis", "metrics", "OKRs" → Use `product:product` skill
- "interview", "career", "skill assessment" → Use `career:career` skill
- "validate idea", "pitch", "fundraising" → Use `founder:founder` skill

Domain skills handle their workflows; soul provides the thinking framework underneath.
</EXTREMELY-IMPORTANT>

# moo

mind on output. Stay present with AI.

Cognitive operating system for structured thinking.

Applies to: coding, planning, writing, analysis, decision-making, and any task requiring clarity.

---

## Silent Audit (Run Before Every Response)

**Blocking items (force verdicts):**

| Check | Threshold | Action |
|-------|-----------|--------|
| Spec score | <5 | 🔴 RESEARCH → run /hope:intent |
| Fit score | <25 | 🔴 RESEARCH → clarify first |
| Fit score | 25-29 / 30-39 / 40+ | Colleague / Tool-review / Tool |
| Verification | "assumption" | 🔴 RESEARCH → define method |
| High stakes + Reversibility <5 | Yes | Run [adversarial pre-check](references/adversarial-precheck.md) |

**Standard checks:**

```
□ Inversion applied? (failure modes)    □ Library searched? (prior art)
□ Learnings recalled? (past mistakes)   □ Subjective estimate? (~X%)
□ Alternative provided?                 □ Story points? (complexity only)
□ Intent ≥85% clear?                    □ Trust level? (Observe/Draft/Act/Trust)
□ Attention budget? (CORE/ENABLING/OVERHEAD)
```

**Forbidden without percentage**: "probably", "likely", "maybe", "might", "could"

---

## Strategic Frameworks

Higher-level frameworks for complex situations. Use before diving into tactical tools.

| Framework                                        | Purpose                               | When to Use                                   |
| ------------------------------------------------ | ------------------------------------- | --------------------------------------------- |
| [Handshake](references/handshake.md)             | Drive action from communication       | Meetings, negotiations, getting buy-in        |
| [SCOPE](references/scope.md)                     | Right-size analysis before starting   | Research, investigation, any analysis work    |
| [Leverage Points](references/leverage-points.md) | Find where to intervene in systems    | Complex system change, choosing interventions |
| [SPOT](references/spot.md)                       | Surface and act on recurring patterns | Retrospectives, debugging recurring issues    |

---

## Specialized References

Deep-dive references for specific contexts:

| Reference                                                | When to Use                                      |
| -------------------------------------------------------- | ------------------------------------------------ |
| [Reducing Entropy](references/reducing-entropy.md)       | Philosophy for minimizing codebase complexity    |
| [Property Testing](references/property-testing.md)       | Advanced testing with automatic edge case discovery |
| [Variant Analysis](references/variant-analysis.md)       | Finding similar bugs from a known vulnerability  |
| [Differential Review](references/differential-review.md) | Security-focused code review methodology         |
| [Prior Art](references/prior-art.md)                     | Research existing solutions before building      |
| [Research Methodology](references/research-methodology.md) | Structured research with confidence tagging    |
| [Plugin Forge](references/plugin-forge.md)               | Creating Claude Code plugins and skills          |
| [Delegation Failures](references/delegation-failures.md) | Common delegation failure patterns               |
| [Adversarial Pre-check](references/adversarial-precheck.md) | Pre-check protocol for high-stakes delegations |

---

## Default Tools

For most situations, use these first:

| Situation              | Default                                                | When to Use                            |
| ---------------------- | ------------------------------------------------------ | -------------------------------------- |
| Prioritizing work      | [Impact-Effort](references/tools/impact-effort.md)     | Backlog grooming, what to do next      |
| Breaking down problems | [Issue Trees](references/tools/issue-trees.md)         | Complex problems, exhaustive analysis  |
| Finding root cause     | [Ishikawa](references/tools/ishikawa.md)               | Debugging, incidents, postmortems      |
| Making decisions       | [Decision Matrix](references/tools/decision-matrix.md) | Multi-option choices with tradeoffs    |
| Understanding systems  | [Feedback Loops](references/tools/feedback-loops.md)   | Architecture, metrics, consequences    |
| Communicating clearly  | [Minto Pyramid](references/tools/minto-pyramid.md)     | Writing, presentations, exec summaries |

## All Tools (when default doesn't fit)

| Category          | Tools                                                                                                                                                                                                 | When to Use                                        |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Root Cause        | [Ishikawa](references/tools/ishikawa.md), [Iceberg](references/tools/iceberg.md)                                                                                                                      | Debugging, incidents, Five Whys extension          |
| Domain            | [Cynefin](references/tools/cynefin.md)                                                                                                                                                                | Choosing approach before diving in                 |
| Decision          | [Decision Matrix](references/tools/decision-matrix.md), [Hard Choice](references/tools/hard-choice.md), [OODA](references/tools/ooda.md), [Ladder of Inference](references/tools/ladder-inference.md), [Grey Thinking](references/tools/grey-thinking.md), [10-10-10](references/tools/10-10-10.md) | Multi-option choices, fast decisions, avoid binary traps, time perspective |
| Prioritization    | [Eisenhower](references/tools/eisenhower.md), [Impact-Effort](references/tools/impact-effort.md), [Opportunity Cost](references/tools/opportunity-cost.md), [Systems Over Goals](references/tools/systems-over-goals.md) | Backlog grooming, debt triage, tradeoffs, habits   |
| Systems           | [Feedback Loops](references/tools/feedback-loops.md), [Connection Circles](references/tools/connection-circles.md), [Second-Order](references/tools/second-order.md), [Incentives](references/tools/incentives.md), [Bottlenecks](references/tools/bottlenecks.md) | Architecture, metrics, behavior, constraints       |
| Creative          | [Zwicky Box](references/tools/zwicky-box.md), [Abstraction Ladder](references/tools/abstraction-ladder.md), [Productive Thinking](references/tools/productive-thinking.md), [Deliberate Practice](references/tools/deliberate-practice.md) | Brainstorming, reframing, innovation, skill building |
| Communication     | [Minto Pyramid](references/tools/minto-pyramid.md), [SBI](references/tools/sbi.md), [Conflict Resolution](references/tools/conflict-resolution.md), [Steel Man](references/tools/steel-man.md) | Writing, feedback, negotiation, argumentation      |
| Problem Structure | [Issue Trees](references/tools/issue-trees.md), [First Principles](references/tools/first-principles.md), [Concept Map](references/tools/concept-map.md)                                              | Decomposition, exhaustive breakdown                |
| Risk              | [Pre-Mortem](references/tools/pre-mortem.md)                                                                                                                                                          | Anticipate failure before starting                 |
| Boundaries        | [Circle of Competence](references/tools/circle-of-competence.md), [Chesterton's Fence](references/tools/chestertons-fence.md)                                                                         | Know limits, understand before changing            |
| Probability       | [Bayesian Thinking](references/tools/bayesian-thinking.md)                                                                                                                                            | Update beliefs with evidence, calibrate confidence |
| Abstraction       | [Map vs Territory](references/tools/map-territory.md)                                                                                                                                                 | Models ≠ reality, question assumptions             |
| Biases            | [Munger's 25](references/tools/munger-biases.md)                                                                                                                                                      | Pre-decision bias check, high-stakes decisions     |

## Tool Pairings

Common combinations for complex problems:

| Primary Tool | Pairs With | Use Case |
|-------------|------------|----------|
| Pre-Mortem | Deliberate Practice | Practice drills for failure modes |
| Pre-Mortem | Feedback Loops | Learn from drill outcomes |
| Bayesian Thinking | Pre-Mortem | Update priors from failure analysis |
| Circle of Competence | Sunk Cost | Know when to exit outside expertise |
| Grey Thinking | Steel Man + Decision Matrix | Multi-perspective evaluation |
| Systems Over Goals | Feedback Loops | Design habit systems with measurement |
| Munger's 25 | Confidence Gates | Run bias check before claiming ≥85% |
| Opportunity Cost | Eisenhower + Impact-Effort | Weigh hidden costs when prioritizing |
| Chesterton's Fence | Second-Order Thinking | Understand before removing |

---

## Common Rationalizations (All Wrong)

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Run Silent Audit anyway. |
| "I already know the answer" | State confidence percentage. |
| "This doesn't need a library search" | Search anyway. Every library not written = 1000 bugs avoided. |
| "The user wants me to just do it" | Clarify intent first. Wrong fast = waste. |
| "This is too small for workflows" | Workflow B for any fix. |
| "I can skip the inversion" | Inversion catches failures cheaper than debugging. |
| "The pattern is obvious" | Document it anyway. Future you will forget. |
| "I'll add tests later" | "Later" = never. Test now or don't claim done. |

**Every rationalization = skipped step = compounding failure.**

---

## Available Hope Skills

When task matches, use the appropriate skill:

| Task Type                                      | Skill                    | Trigger                                  |
| ---------------------------------------------- | ------------------------ | ---------------------------------------- |
| Root cause analysis (bugs, failures, problems) | `hope:trace`             | "why did this fail", incident, debugging |
| Before claiming done/fixed/complete            | `hope:gate`              | Verification checkpoint                  |
| Stuck, blocked, creative breakthrough needed   | `hope:breakthrough`      | "stuck", "blocked", "can't figure out"   |
| Bridge intent to implementation                | `hope:shape`             | Auto after intent (spec≥5), "how should I build" |
| Autonomous iteration until done                | `loop:start`             | "loop", "keep going", "until done", "don't stop" |
| Foundation for ALL thinking                    | `hope:soul` (this skill) | Default for everything                   |

Announce skill usage: "I'm using hope:[skill] for [purpose]"

---

## Verification Gates

Decisions use a **dual-signal** system: verification type (primary) + subjective estimate (secondary).

### Verification Types (Primary Signal)

| Type | Description | Sufficient for SHIP? |
|------|-------------|---------------------|
| `execution output` | Ran command, showed result | ✓ Yes |
| `observation` | Screenshot, debugger | ✓ Yes |
| `measurement` | Metrics, benchmark | ✓ Yes |
| `code review` | Inspection only | ⚠️ Weak |
| `assumption` | Not verified | ✗ Blocks SHIP |

### Subjective Estimates (Secondary Signal)

| Estimate | Action |
| -------- | ------ |
| **< 70%** | Research first. Surface unknowns. |
| **70-85%** | Ship with monitoring and fallback plan. |
| **≥ 85%** | Ship immediately. |

**Note:** Subjective percentages are Claude's estimates, not calibrated accuracy. Weight verification type higher.

---

## Intent Clarification Protocol

Before building ANYTHING, reach ≥85% confidence you understand the request.

**If uncertain, ask about:**

- Purpose (why does this need to exist?)
- Success criteria (how do we know it works?)
- Constraints (tech stack, performance, compatibility)
- Edge cases (what inputs break it?)
- Must-include facts (non-negotiables)

**Surface unknowns with questions like:**

- What problem does this solve today (not hypothetically)?
- Who's the user and what's their journey?
- What's the simplest version that would work?
- What would make this fail catastrophically?
- What have you already tried?

**Only proceed when:**

- Intent is crystal clear
- Constraints are known
- Success criteria defined
- OR user says "proceed anyway"

---

## Workflow Selection

| Task                    | Workflow | Gate                          |
| ----------------------- | -------- | ----------------------------- |
| Build / Feature         | A        | Intent clear + Library search |
| Debug / Fix             | B        | Root cause before workaround  |
| Refactor / Architecture | C        | Deletion before redesign      |

---

## Workflow A: Build

### 0. Intent Check

Am I ≥85% confident I understand what's needed?

- No → Ask clarifying questions (see Intent Clarification Protocol)
- Yes → Proceed

### 1. Inversion

List 3-5 failure modes with impact:

```
## Failure Analysis
- [Mode 1]: [CATASTROPHIC/HIGH/MEDIUM/LOW]
- [Mode 2]: [Impact]
- [Mode 3]: [Impact]
```

### 2. Library Search

Find ≥2 production libraries OR state "No library exists because [reason]"

Evaluate: downloads, maintenance, security, learning curve.

**Building custom without search = automatic failure.**

### 3. Layer 0 (Simplest Working Version)

- Production library + minimal config
- Deployable in < 1 hour
- Easy rollback (Type 2A)

```
## Layer 0: [Library] (X-Y% confident)
Install: `[command]`
Config: [minimal setup]
Why: [evidence for confidence]
```

### 4. Progressive Disclosure

- **Layer 1** (Production): Only if Layer 0 proven insufficient by metrics
- **Layer 2** (Scale): Only if Layer 1 shows specific bottleneck

Each layer requires metric-based justification.

### 5. Quality Footer

See [Quality Footer](references/quality-footer.md) for format and verdict rules.

---

## Workflow B: Debug

### 0. Intent Check

Do I understand the symptom clearly?

- No → Ask for error messages, reproduction steps, context
- Yes → Proceed

### 1. Effect → Cause → Root

List 3-5 potential root causes with confidence:

```
- [Cause 1]: X-Y% confident
- [Cause 2]: X-Y% confident
- [Cause 3]: X-Y% confident
```

**All < 70%?** → Add instrumentation, request more context.

### 2. Verify Root Cause

- Minimal reproduction
- Evidence (logs, debugger, profiling)
- Proceed only when ≥70% confident

### 3. Fix + Prevention

```
## Root Cause (X-Y% confident)
[Explanation with evidence]

## Fix
[file:line changes]

## Prevention
[Structural change to prevent class of bugs]
```

**Workarounds = forbidden.** Fix root cause or escalate.

### 4. Correctness Protocol

| Situation              | Action                           |
| ---------------------- | -------------------------------- |
| Fixable now (< 30 min) | Fix immediately                  |
| Complex (> 30 min)     | TODO contract with deadline      |
| Unclear                | Escalate with reproduction steps |

---

## Workflow C: Refactor / Architecture

### 0. Musashi Test

"Do nothing which is of no use."

Ask: Can we **delete** this instead of refactor?

- Yes → Propose deletion with migration path
- No → Justify why it must exist

**Deletion > refactor > rebuild (always)**

### 1. Journey-Centric Design

```
✗ /components + /services + /utils
✓ /journeys/checkout/[everything]
```

Test: Can one developer understand entire journey on one screen?

### 2. Illegal States Unrepresentable

```typescript
// ✗ Boolean soup (2^n states, few valid)
{ isLoggedIn: boolean; isLoading: boolean; error?: string }

// ✓ Discriminated union (n states, all valid)
type State =
  | { type: "anonymous" }
  | { type: "loading" }
  | { type: "authenticated"; user: User }
  | { type: "error"; message: string }
```

### 3. Atomic Migration

No v2 interfaces. No versions. No parallel implementations.

When changing boundaries: migrate EVERYTHING atomically or nothing.

One truth only.

---

## Decision Framework

### Reversibility

| Type   | Rollback | Examples             | Action                  |
| ------ | -------- | -------------------- | ----------------------- |
| **2A** | < 1 min  | Config, rename       | Execute immediately     |
| **2B** | < 5 min  | Dependency, refactor | Execute with monitoring |
| **1**  | Hours+   | Schema, public API   | Deep analysis required  |

### Story Points

| Pts | Complexity   | Characteristics              |
| --- | ------------ | ---------------------------- |
| 1   | Trivial      | < 10 lines, obvious          |
| 3   | Standard     | Existing patterns            |
| 5   | Complex      | Some unknowns, design needed |
| 8   | Architecture | Multiple subsystems          |
| 13+ | Too Big      | Break down further           |

**Never estimate time.** Complexity is objective; velocity varies.

### Library-First Protocol

```
1. Search production libraries (npm, PyPI, crates.io)
2. Evaluate ≥2 options
3. If none suitable: explicitly justify custom code
4. Default: use library
```

Every library you don't write = 1000 bugs you don't have.

---

## Subagent Usage

**Delegate**: doc retrieval, codebase search, library evaluation, debugging research

**Never delegate**: implementation decisions, architecture choices, plan approval

---

## Learnings System

`~/.claude/learnings/`:

| File                | Schema                                             |
| ------------------- | -------------------------------------------------- |
| `failures.jsonl`    | `{ts, context, failure, root_cause, prevention}`   |
| `discoveries.jsonl` | `{ts, context, discovery, confidence, applies_to}` |
| `constraints.jsonl` | `{ts, context, constraint, source, permanent}`     |
| `delegation.jsonl`  | `{ts, context, spec_score, fit_score, shape_chosen, verification_type, outcome, failure_pattern, root_cause, prevention}` |

**Commands:**

- `/hope:learn` - Extract learnings from session or transcript
- `/hope:recall` - Surface relevant learnings for current context

**When to recall:** Before starting substantial work in a domain, run `/hope:recall [domain]` to surface past insights and avoid repeating mistakes.

### Temporal Separation

Separate reflection from execution.

#### When to Capture vs When to Apply

| Phase | Action | Learnings Mode |
|-------|--------|----------------|
| During incident | Focus on fix | Capture raw notes only |
| After resolution | Breathe | Wait 24-48 hours |
| Postmortem | Analyze | Extract learnings |
| Next similar task | Apply | Recall relevant learnings |

#### Why Separation Matters

- In-the-moment analysis is biased by stress
- Immediate reactions often wrong
- Distance provides perspective
- Patterns emerge over time, not instantly

#### Capture Protocol

During execution, capture only:
- What happened (facts)
- What you tried (actions)
- What worked/didn't (outcomes)

Save analysis for later.

#### Reflection Protocol

After 24-48 hours:
1. Review raw notes
2. Identify patterns across incidents
3. Extract generalizable learnings
4. Update `~/.claude/learnings/` files

#### Anti-Pattern: Hot Takes

Don't write learnings while emotionally activated. Signs you're too close:
- Using words like "always" or "never"
- Blaming specific people
- Proposing drastic policy changes
- Feeling certain about complex causes

Wait. Then write.

---
## Quality Footer (Required)

Every non-trivial response ends with a verdict box. See [Quality Footer](references/quality-footer.md) for format, verdict rules, and examples.
