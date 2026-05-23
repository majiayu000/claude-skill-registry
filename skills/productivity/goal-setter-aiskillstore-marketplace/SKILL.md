---
name: goal-setter
description: Transform objectives into structured goals with plans. Use when user declares intent ("I want to...", "Goal is to...", "Achieve X by Y"). Decomposes into subgoals, milestones, success criteria.
---

# Goal Setter

Transform vague or precise objectives into structured, actionable goals.

## Operating Model

Goals are the **primary** operating mode for LeanOS. All work should be goal-driven.

```
PROACTIVE (primary):  Goal → Plan → Threads → Artifacts → Learning → Canvas
REACTIVE (fallback):  Signal → Thread → Link to Goal (or create new goal)
```

**Goal-setter reads:**
- Canvas (`strategy/canvas/*`) - strategic context, assumptions, constraints
- Existing goals (`strategy/goals/active/*`) - avoid conflicts, find linkages

**Goal-setter does NOT read:**
- Threads (execution output, not input)
- Artifacts (deliverables, not context)

## Canvas Reference

Goal-setter uses Canvas sections for context, constraints, and success criteria alignment.

### Canvas Sections (15 files)

| Section | Purpose | Goal-setter Use |
|---------|---------|-----------------|
| `00.mode.md` | VENTURE/BOOTSTRAP mode | **Required** - determines metrics, decomposition |
| `01.context.md` | Product, market context (KBOS) | Goal alignment check |
| `02.constraints.md` | Budget, time, resources | Goal constraints |
| `03.opportunity.md` | TAM/SAM/SOM, timing | Business goal sizing |
| `04.segments.md` | Customer segments | Target audience for goals |
| `05.problem.md` | Top 3 problems | Problem-focused goals |
| `06.competitive.md` | Competitors, positioning | Competitive goals |
| `07.uvp.md` | Unique Value Proposition | Messaging alignment |
| `08.unfair.md` | Unfair advantages, moats | Strategic goals |
| `09.solution.md` | MVP features | Product goals |
| `10.assumptions.md` | Hypotheses, validation status | **Key** - link goals to assumptions |
| `11.channels.md` | Acquisition channels | Channel strategy |
| `12.revenue.md` | Revenue model, tiers | Revenue goal targets |
| `13.metrics.md` | Key metrics, targets | Success criteria source |
| `14.costs.md` | Cost structure, burn | Profitability constraints |
| `15.gtm.md` | GTM strategy | Marketing/sales goals |

### Canvas Reading by Goal Type

```
business goals:
  Required: 00-mode, 11-pricing, 12-costs, 13-metrics
  Context:  01-context, 03-opportunity, 04-segments
  Link to:  10-assumptions (revenue/growth hypotheses)

brand goals:
  Required: 01-context, 07-uvp
  Context:  04-segments, 14-growth
  Link to:  10-assumptions (audience/positioning hypotheses)

product goals:
  Required: 09-solution, 05-problem
  Context:  01-context, 02-constraints
  Link to:  10-assumptions (product/market fit hypotheses)

learning goals:
  Context:  01-context (what skills needed)
  Link to:  10-assumptions (capability hypotheses)
```

### Linking Goals to Canvas Assumptions

Every goal should link to Canvas assumptions (`10.assumptions.md`):

```markdown
## Canvas Links

**Validates assumptions:**
- A3: "Enterprise customers will pay $500/month" (10.assumptions.md)
- A7: "Content marketing drives qualified leads" (10.assumptions.md)

**Informs sections:**
- 13.metrics.md (success updates metrics)
- 12.revenue.md (if revenue assumption validated)
```

When goal completes:
1. Update linked assumption status in `10.assumptions.md`
2. Update relevant Canvas section if assumption validated/invalidated
3. Log learning in goal file

## Type Signature

```
GoalSetter : Objective × CanvasContext × Mode × ExistingGoals → Goal

Where:
  Objective     : string (user's stated intent)
  CanvasContext : strategy/canvas/* (beliefs, constraints, segments)
  Mode          : VENTURE | BOOTSTRAP (from strategy/canvas/00.mode.md)
  ExistingGoals : strategy/goals/active/* (avoid conflicts)
  Goal          : Objective × SuccessCriteria × Plan × Autonomy × State
  Plan          : [Subgoal] × [Milestone] × [Dependency]
  Subgoal       : Objective × SuccessCriterion × ThreadType
```

## When to Use

- User expresses intent: "I want to...", "Goal is to...", "Need to achieve..."
- Starting a new initiative without clear structure
- Breaking down a large objective into actionable pieces
- Reviewing/refining existing goals

## Process

### 1. Capture Objective

Extract from user input:
- **What**: The desired outcome
- **Why**: Motivation/context (optional but valuable)
- **When**: Deadline or timeline (required)
- **Constraints**: Budget, resources, dependencies

**If vague, ask:**
```
What does success look like specifically?
By when do you need this achieved?
What resources/constraints should I know about?
```

### 2. Determine Goal Type

Infer from context or ask:

| Type | Signals | Example |
|------|---------|---------|
| `business` | Revenue, customers, growth, market | "Reach $50K MRR" |
| `brand` | Followers, reach, authority, audience | "Build LinkedIn presence" |
| `product` | Features, launches, technical milestones | "Ship v2.0" |
| `learning` | Skills, certifications, knowledge | "Learn Rust" |
| `custom` | Anything else | User-defined |

### 3. Apply Mode (Business Goals)

For `business` type goals, read mode from `strategy/canvas/00.mode.md`:

| Aspect | VENTURE | BOOTSTRAP |
|--------|---------|-----------|
| **Primary metrics** | ARR, MAU, market share, runway | MRR, profit, cash flow, payback |
| **Success focus** | Growth rate, scale | Profitability, sustainability |
| **Decomposition** | Users → Activation → Monetization | Revenue → Margin → Reinvest |
| **Timeline** | 7-10 year exit horizon | Profitable in 3 months |
| **Risk tolerance** | Higher (burn for growth) | Lower (preserve cash) |

**Mode-specific defaults:**

```
VENTURE mode:
  Success criteria emphasize:
  - ARR growth rate (>100% YoY)
  - User/customer acquisition
  - Market share expansion
  - Acceptable burn for growth

  Subgoal order: Acquire → Activate → Retain → Monetize

  Autonomy default: hybrid (speed matters, but stakes high)

BOOTSTRAP mode:
  Success criteria emphasize:
  - MRR and monthly profit
  - Positive cash flow
  - LTV:CAC > 5:1
  - CAC payback < 6 months

  Subgoal order: First revenue → Unit economics → Scale

  Autonomy default: ask (cash preservation critical)
```

**Non-business goals:** Mode has minimal impact on brand, product, learning goals.

### 4. Define Success Criteria

Transform objective into measurable criteria:

**Good criteria:**
- Specific number or state
- Independently verifiable
- Time-bound (inherits from goal deadline)

**Examples:**
```
Objective: "Grow revenue"
Criteria:
- [ ] MRR >= $50,000
- [ ] Customer count >= 10
- [ ] Net revenue retention >= 100%

Objective: "Build LinkedIn presence"
Criteria:
- [ ] Followers >= 10,000
- [ ] Average post impressions >= 5,000
- [ ] 2+ inbound leads/month from content
```

### 5. Decompose into Plan

**Subgoals** - intermediate objectives that lead to main goal:
- Each subgoal has its own success criterion
- Identify dependencies between subgoals
- Link to thread types (business, sales, marketing, engineering)

**Milestones** - checkpoints with dates:
- Evenly distributed toward deadline
- Each milestone = measurable progress marker

**Decomposition reasoning:**
```
Goal: Achieve X by deadline D
  ↓
Ask: What must be true for X to happen?
  ↓
Identify 3-5 necessary conditions (subgoals)
  ↓
For each subgoal: What threads/actions achieve this?
  ↓
Order by dependencies
  ↓
Set milestones at 25%, 50%, 75%, 100% progress points
```

### 6. Set Autonomy Level

| Mode | When to Use | Behavior |
|------|-------------|----------|
| `auto` | Low-risk, well-understood domain | AI creates threads and executes without asking |
| `ask` | High-risk, novel, or user preference | AI recommends, waits for approval |
| `hybrid` | Default | Auto for impact <0.5, ask for impact ≥0.5 |

**Default: `hybrid`** unless user specifies otherwise.

### 7. Initialize State

Create initial state section:
- All metrics start at current values (0 or baseline)
- Gap = target - current
- Trend = "→" (neutral, no data yet)
- Trajectory = "Unknown" (insufficient data)

## Output

Create file: `strategy/goals/active/{goal-id}.md`

### Goal File Schema

```markdown
---
id: g-{kebab-case-short-name}
type: business | brand | product | learning | custom
mode: VENTURE | BOOTSTRAP  # For business goals only
status: active
autonomy: auto | ask | hybrid
created: {YYYY-MM-DD}
deadline: {YYYY-MM-DD}
canvas_refs: ["{section}.md", ...]  # Optional Canvas links
---

# {Goal Title}

## Objective
{Single sentence describing desired outcome}

## Success Criteria
- [ ] {Measurable criterion 1}
- [ ] {Measurable criterion 2}
- [ ] {Measurable criterion 3}

## Plan

### Subgoals

#### SG1: {Subgoal Title}
- **Success:** {Specific criterion}
- **Depends on:** {None | SG#}
- **Thread type:** {business | sales | marketing | engineering}
- **Threads:** {None yet | thread-id, ...}
- **Status:** pending | in_progress | completed

#### SG2: {Subgoal Title}
- **Success:** {Specific criterion}
- **Depends on:** SG1
- **Thread type:** {type}
- **Threads:** {None yet}
- **Status:** pending

### Milestones
- [ ] M1: {25% progress marker} (by {date})
- [ ] M2: {50% progress marker} (by {date})
- [ ] M3: {75% progress marker} (by {date})
- [ ] M4: {Goal achieved} (by {deadline})

### Dependencies
{External dependencies, blockers, or prerequisites}

## State

### Metrics
| Metric | Current | Target | Gap | Trend |
|--------|---------|--------|-----|-------|
| {Primary metric} | {value} | {value} | {value} | → |
| {Secondary metric} | {value} | {value} | {value} | → |

### Execution
- **Active threads:** 0
- **Completed threads:** 0
- **Blocked:** 0

### Trajectory
- **On track:** Unknown (insufficient data)
- **Projected completion:** TBD
- **Risk level:** Low

## Canvas Links

**Validates assumptions:**
- {assumption-id}: "{assumption text}" (10.assumptions.md)

**Informs sections:**
- {section}.md (what updates on success)

## Log
- {created date}: Goal created
```

## Integration

### With Canvas
- Read relevant sections before creating goal (see Canvas Reference)
- Reference sections in `canvas_refs` frontmatter
- Link to assumptions in Canvas Links section
- Goal completion triggers Canvas updates (assumptions, metrics)

### With Threads
- Subgoals spawn threads when activated
- Thread completion updates subgoal status
- Thread Stage 6 (Learning) feeds back to goal state

### With Reasoning Gateway
- Complex decomposition may route through reasoning modes
- Causal: For operational goals with clear cause-effect
- Analogical: For novel goals ("this is like...")
- Dialectical: For goals with competing priorities

## Examples

### Business Goal (BOOTSTRAP)
```
User: "I want to hit $50K MRR by end of Q2"

Canvas read:
- 00-mode: BOOTSTRAP
- 11-pricing: $500/mo average, 3 tiers
- 12-costs: $5K/mo burn, need profitability
- 13-metrics: Current MRR $8K, 16 customers
- 04-segments: SMB primary, Enterprise secondary

Goal created:
- id: g-mrr-50k
- type: business
- mode: BOOTSTRAP
- deadline: 2025-06-30
- canvas_refs: [00-mode, 11-pricing, 12-costs, 13-metrics]
- Success criteria: MRR >= $50K, Profit margin >= 30%, CAC payback < 6 months
- Subgoals (revenue-first order):
  - SG1: Close first 3 paying customers
  - SG2: Validate unit economics (LTV:CAC > 5:1)
  - SG3: Scale acquisition (pipeline of 20 leads)
- Canvas Links:
  - A2: "SMB customers convert at 5%" (validates)
  - A5: "$500/mo price point acceptable" (validates)
- Autonomy: ask (cash preservation)
```

### Business Goal (VENTURE)
```
User: "I want to hit $500K ARR by end of year"

Canvas read:
- 00-mode: VENTURE
- 03-opportunity: TAM $2B, growing 40% YoY
- 13-metrics: Current ARR $50K, 500 MAU
- 14-growth: PLG primary, content secondary

Goal created:
- id: g-arr-500k
- type: business
- mode: VENTURE
- deadline: 2025-12-31
- canvas_refs: [00-mode, 03-opportunity, 13-metrics, 14-growth]
- Success criteria: ARR >= $500K, MAU >= 10K, Growth >= 100% YoY
- Subgoals (growth-first order):
  - SG1: Acquire 5K users (product-led)
  - SG2: Activate 50% to active usage
  - SG3: Convert 5% to paid
- Canvas Links:
  - A1: "PLG drives user acquisition" (validates)
  - A4: "5% free-to-paid conversion achievable" (validates)
- Autonomy: hybrid (speed matters)
```

### Brand Goal
```
User: "Build my LinkedIn presence for thought leadership"

Canvas read:
- 01-context: B2B SaaS, technical audience
- 07-uvp: "AI-native operations for startups"
- 04-segments: Technical founders, solo operators
- 14-growth: Content marketing as key channel

Goal created:
- id: g-linkedin-authority
- type: brand
- deadline: 2025-06-30 (asked user)
- canvas_refs: [01-context, 07-uvp, 04-segments, 14-growth]
- Success criteria: 10K followers, 5K avg impressions, 2 leads/month
- Subgoals:
  - SG1: Define content pillars (aligned with 07-uvp)
  - SG2: Establish posting cadence (3x/week)
  - SG3: Build engagement network (04-segments audience)
- Canvas Links:
  - A8: "Content drives inbound leads" (validates)
```

### Product Goal
```
User: "Ship the mobile app"

Canvas read:
- 09-solution: MVP = core workflow + notifications
- 05-problem: "Users need mobile access to approve decisions"
- 01-context: Web app exists, mobile requested by 60% of users
- 02-constraints: 2 developers, Q1 deadline

Goal created:
- id: g-mobile-app-launch
- type: product
- deadline: 2025-03-31 (asked user)
- canvas_refs: [09-solution, 05-problem, 01-context, 02-constraints]
- Success criteria: App in stores, 100 beta users, <1% crash rate
- Subgoals:
  - SG1: Core features complete (09-solution scope)
  - SG2: Beta testing (recruit from existing users)
  - SG3: Store submission
- Canvas Links:
  - A6: "Mobile increases engagement 2x" (validates)
```

## Constraints

### Must Have
- Clear success criteria (measurable)
- Deadline
- At least 2 subgoals
- Autonomy level set

### Must Ask If Missing
- Deadline not specified
- Success criteria ambiguous
- Type unclear from context

### Must NOT
- Create goals without user confirmation of structure
- Set autonomy to `auto` for high-impact goals without asking
- Create duplicate goals (check existing first)

## Error Handling

**Objective too vague:**
```
Ask: "What does '{objective}' look like when achieved?
     Give me 2-3 specific outcomes I can measure."
```

**No deadline:**
```
Ask: "By when do you want to achieve this?
     Options: specific date, relative (3 months), or milestone-based"
```

**Conflicting with existing goal:**
```
Flag: "This overlaps with existing goal '{goal-id}'.
      Should I: (1) Merge as subgoal, (2) Replace existing, (3) Keep both?"
```