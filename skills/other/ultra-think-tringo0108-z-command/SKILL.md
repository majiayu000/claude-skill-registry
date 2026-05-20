---
name: ultra-think
description: Master advanced cognitive and analytical thinking patterns for deep problem solving, including first principles reasoning, mental models, systematic decomposition, and critical evaluation. Use PROACTIVELY for complex problems, architectural decisions, debugging, or strategic planning.
---

# Ultra Think

Master advanced cognitive and analytical thinking patterns for deep problem solving, systematic analysis, and strategic decision making.

## When to Use This Skill

- Solving complex, multi-faceted problems
- Making architectural or design decisions
- Debugging difficult issues with unknown root causes
- Analyzing trade-offs between alternatives
- Planning strategies and roadmaps
- Evaluating proposals and designs
- Breaking down ambiguous requirements
- Synthesizing information from multiple sources

## Core Thinking Frameworks

### 1. First Principles Thinking

Break problems down to fundamental truths and reason up from there.

```
FIRST PRINCIPLES PROCESS:

1. IDENTIFY THE PROBLEM
   └── What exactly are we trying to solve?
   └── What assumptions are we making?
   └── What do we "know" that might not be true?

2. BREAK DOWN TO FUNDAMENTALS
   └── What are the basic elements?
   └── What physical/logical laws apply?
   └── What are the irreducible requirements?

3. REMOVE ASSUMPTIONS
   └── Why do we do it this way?
   └── Is this constraint real or inherited?
   └── What if we started from scratch?

4. REBUILD FROM GROUND UP
   └── Given fundamentals, what's the optimal solution?
   └── What new approaches become possible?
   └── What would an expert with no context do?
```

**Example Application:**

```
PROBLEM: Database queries are slow

CONVENTIONAL THINKING:
- Add more indexes
- Upgrade to larger instance
- Add caching layer

FIRST PRINCIPLES:
1. Fundamentals:
   - Data must be read from storage
   - Query must match records
   - Results must be returned

2. Remove assumptions:
   - Do we need relational structure?
   - Do we need real-time consistency?
   - Is the data model correct for access patterns?

3. Rebuild:
   - Maybe: denormalize for read patterns
   - Maybe: use event sourcing + projections
   - Maybe: pre-compute and store results
   - Maybe: different database type entirely
```

### 2. Mental Models Library

Apply proven thinking frameworks to structure analysis.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MENTAL MODEL TOOLKIT                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  SYSTEMS THINKING                                                    │
│  ├── Feedback Loops: What reinforces or dampens behavior?           │
│  ├── Emergent Properties: What arises from component interaction?   │
│  ├── Bottlenecks: Where does the system constrain flow?             │
│  └── Leverage Points: Where can small changes have big impact?      │
│                                                                      │
│  INVERSION                                                           │
│  ├── Instead of: How do I succeed?                                  │
│  ├── Ask: How would I definitely fail?                              │
│  └── Then: Avoid those failure modes                                │
│                                                                      │
│  SECOND-ORDER EFFECTS                                                │
│  ├── First-order: What happens immediately?                         │
│  ├── Second-order: What happens as a result of that?                │
│  └── Third-order: And then what happens?                            │
│                                                                      │
│  OPPORTUNITY COST                                                    │
│  ├── What am I giving up by choosing this?                          │
│  ├── What else could I do with these resources?                     │
│  └── Is this the highest-value use of time/effort?                  │
│                                                                      │
│  PARETO PRINCIPLE (80/20)                                            │
│  ├── Which 20% of causes create 80% of effects?                     │
│  ├── Which 20% of effort produces 80% of results?                   │
│  └── Focus on the vital few, not the trivial many                   │
│                                                                      │
│  OCCAM'S RAZOR                                                       │
│  ├── Among competing hypotheses, prefer the simplest                │
│  ├── Don't add complexity without evidence                          │
│  └── Simple explanations are more likely correct                    │
│                                                                      │
│  HANLON'S RAZOR                                                      │
│  ├── Don't attribute to malice what is explained by incompetence    │
│  ├── Most failures are mistakes, not intentional                    │
│  └── Assume good intent until proven otherwise                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 3. Problem Decomposition

Systematically break complex problems into manageable pieces.

```
DECOMPOSITION STRATEGY:

┌──────────────────────────────────────────────────────────────┐
│                    ORIGINAL PROBLEM                           │
│        "System is unreliable and users complain"              │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                   CLARIFY & BOUND                             │
│  • What does "unreliable" mean specifically?                  │
│  • Which users? What do they complain about?                  │
│  • What's the scope? (time, components, severity)             │
│  • What's the success criteria?                               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    IDENTIFY DIMENSIONS                        │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │   SYMPTOMS  │  │    CAUSES   │  │   IMPACTS   │           │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤           │
│  │ • Errors    │  │ • Code bugs │  │ • Lost data │           │
│  │ • Timeouts  │  │ • Infra     │  │ • Downtime  │           │
│  │ • Slow      │  │ • Load      │  │ • Revenue   │           │
│  │ • Data loss │  │ • External  │  │ • Trust     │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    PRIORITIZE & SEQUENCE                      │
│                                                               │
│  1. [HIGH] Data loss in checkout → Fix transaction handling  │
│  2. [HIGH] API timeouts during peak → Add circuit breakers   │
│  3. [MED] Intermittent errors → Improve observability        │
│  4. [LOW] Slow dashboard → Optimize queries later            │
└──────────────────────────────────────────────────────────────┘
```

### 4. Trade-off Analysis

Structure decision-making when facing competing options.

```
TRADE-OFF ANALYSIS FRAMEWORK:

OPTION A: Microservices Architecture
OPTION B: Modular Monolith
OPTION C: Hybrid (Critical services split, rest monolith)

┌─────────────────────────┬─────────┬─────────┬─────────┐
│ CRITERIA (weighted)     │ Opt A   │ Opt B   │ Opt C   │
├─────────────────────────┼─────────┼─────────┼─────────┤
│ Development speed (3x)  │ 2       │ 4       │ 3       │
│ Scalability (2x)        │ 5       │ 2       │ 4       │
│ Operational complexity  │ 1       │ 4       │ 3       │
│ Team expertise (2x)     │ 2       │ 4       │ 3       │
│ Future flexibility      │ 5       │ 3       │ 4       │
│ Time to market (3x)     │ 1       │ 5       │ 4       │
├─────────────────────────┼─────────┼─────────┼─────────┤
│ WEIGHTED SCORE          │ 27      │ 41      │ 38      │
└─────────────────────────┴─────────┴─────────┴─────────┘

DECISION FACTORS:
├── Reversibility: Can we change our mind? (B → A easier than A → B)
├── Timing: When do we need scalability? (Not immediately)
├── Team: What can we execute well? (B most familiar)
└── Risk: What's the cost of being wrong? (A locks us in)

RECOMMENDATION: Option B (Modular Monolith)
├── Start simple, prove the product
├── Design for extractability (clear module boundaries)
├── Revisit when hitting concrete scaling limits
└── Lower operational burden with current team
```

### 5. Root Cause Analysis

Dig deep to find the true source of problems.

```
5 WHYS ANALYSIS:

SYMPTOM: Production deployment failed

WHY 1: Deployment script exited with error
       └── Because database migration failed

WHY 2: Why did migration fail?
       └── Because it tried to add NOT NULL column

WHY 3: Why was that a problem?
       └── Because existing rows had NULL values

WHY 4: Why were there NULL values?
       └── Because feature was deployed before data cleanup

WHY 5: Why was deployment before cleanup?
       └── Because there's no coordination between data and code deploys

ROOT CAUSE: No deployment checklist ensuring data readiness

SOLUTIONS:
├── Immediate: Run data cleanup, re-deploy
├── Short-term: Create deployment checklist
└── Long-term: Automate pre-deployment validations

────────────────────────────────────────────────────────────────

FISHBONE DIAGRAM (ISHIKAWA):

                          ┌─ Process ─────────────────┐
                          │  └─ No review process     │
                          │  └─ Missing checklist     │
                          │                           │
          ┌─ People ──────│        ┌─ Technology ─────│
          │  └─ Rushed    │        │  └─ No validation│
          │  └─ No training│       │  └─ Poor tooling │
          │               │        │                   │
          │               ▼        │                   │
          └────────────→ [DEPLOYMENT FAILURE] ←───────┘
                          ▲        ▲
          ┌───────────────│        │───────────────────┐
          │               │        │                   │
          │  ┌─ Environment        └─ Materials ──────│
          │  │  └─ Prod/Dev drift  │  └─ Bad data     │
          │  │  └─ Config mismatch │  └─ Missing docs │
          └──┴─────────────────────┴──────────────────┘
```

### 6. Hypothesis-Driven Investigation

Use scientific method for debugging and analysis.

```
HYPOTHESIS-DRIVEN DEBUGGING:

1. OBSERVE
   └── Symptoms: 500 errors spike at 9 AM daily
   └── Context: Coincides with batch job start
   └── Metrics: Memory usage climbs before errors

2. FORM HYPOTHESES (ranked by likelihood)
   H1: Memory leak during batch processing
   H2: Database connection exhaustion
   H3: External API rate limiting

3. TEST EACH HYPOTHESIS

   H1 TEST: [CONFIRMED]
   ├── Action: Profile memory during batch job
   ├── Prediction: Memory continuously increases
   └── Result: Found list accumulation in loop

   H2 TEST: [Not needed - H1 confirmed]
   H3 TEST: [Not needed - H1 confirmed]

4. VALIDATE FIX
   ├── Action: Stream processing instead of collect
   ├── Prediction: Memory stays flat
   └── Result: Memory stable, no more 500s

5. PREVENT RECURRENCE
   ├── Add memory limit alerts
   ├── Add to code review checklist
   └── Document pattern in wiki
```

### 7. Strategic Thinking Patterns

Think beyond immediate problems to long-term impact.

```
STRATEGIC ANALYSIS LAYERS:

┌────────────────────────────────────────────────────────────┐
│ LAYER 1: IMMEDIATE TACTICAL                                │
│ "What do we do right now?"                                 │
│ • Fix the bug                                              │
│ • Patch the security hole                                  │
│ • Handle the customer complaint                            │
└────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────┐
│ LAYER 2: OPERATIONAL                                        │
│ "How do we prevent this class of problem?"                 │
│ • Improve testing coverage                                  │
│ • Add security scanning to CI                              │
│ • Create feedback collection process                       │
└────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────┐
│ LAYER 3: STRATEGIC                                          │
│ "How does this fit our long-term direction?"               │
│ • Is our architecture supporting or hindering?             │
│ • Do we have the right team capabilities?                  │
│ • Are we solving the right problems?                       │
└────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────┐
│ LAYER 4: VISION                                             │
│ "Where are we trying to go?"                               │
│ • What does success look like in 3 years?                  │
│ • What must be true for that to happen?                    │
│ • What are we NOT going to do?                             │
└────────────────────────────────────────────────────────────┘
```

### 8. Synthesis and Integration

Combine insights from multiple sources into coherent understanding.

```
SYNTHESIS FRAMEWORK:

INPUTS:
├── Data Source 1: Performance metrics
├── Data Source 2: User feedback
├── Data Source 3: Team observations
├── Data Source 4: Market research
└── Data Source 5: Competitor analysis

PROCESS:
┌──────────────────────────────────────────────────────────┐
│ 1. EXTRACT KEY INSIGHTS                                   │
│    ├── Performance: P95 latency up 200% in 6 months      │
│    ├── Users: "App feels sluggish" top complaint         │
│    ├── Team: Frontend bundle grew 3x with new features   │
│    ├── Market: Mobile-first competitors gaining share    │
│    └── Competition: They load 2x faster on mobile        │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│ 2. FIND PATTERNS & CONNECTIONS                            │
│    ├── Bundle growth → slower loads → user complaints    │
│    ├── Mobile gap → competitive disadvantage             │
│    └── Performance debt accumulated with feature growth   │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│ 3. FORM INTEGRATED UNDERSTANDING                          │
│                                                           │
│    "We've traded performance for feature velocity,        │
│     creating a mobile experience gap that competitors     │
│     are exploiting. This threatens user retention and     │
│     market position."                                     │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│ 4. DERIVE ACTIONABLE CONCLUSIONS                          │
│    ├── Immediate: Performance budget for new features    │
│    ├── Short-term: Mobile performance sprint             │
│    ├── Medium-term: Architecture review                  │
│    └── Long-term: Performance as product north star      │
└──────────────────────────────────────────────────────────┘
```

## Application Checklist

### Before Starting Analysis

- [ ] What is the actual question I'm trying to answer?
- [ ] What would "success" look like for this analysis?
- [ ] What constraints or boundaries exist?
- [ ] Who are the stakeholders and what do they need?
- [ ] What's my deadline and how deep should I go?

### During Analysis

- [ ] Am I testing my assumptions or just confirming beliefs?
- [ ] Have I considered alternative explanations?
- [ ] Am I looking at data or just opinions?
- [ ] Have I talked to people closest to the problem?
- [ ] Am I overcomplicating or oversimplifying?

### After Analysis

- [ ] Can I explain this clearly to a non-expert?
- [ ] What's the confidence level in my conclusions?
- [ ] What would change my mind?
- [ ] What are the next steps?
- [ ] How will we know if we were right?

## Quick Reference: Thinking Triggers

| Situation                         | Framework to Apply    |
| --------------------------------- | --------------------- |
| "We've always done it this way"   | First Principles      |
| "What could go wrong?"            | Inversion, Pre-mortem |
| "It's complicated"                | Decomposition         |
| "Which option should we choose?"  | Trade-off Analysis    |
| "Why did this happen?"            | 5 Whys, Fishbone      |
| "What's really going on?"         | Root Cause Analysis   |
| "What should we do about X?"      | Strategic Layers      |
| "How does this all fit together?" | Synthesis             |

## Common Thinking Traps

| Trap               | Description                                     | Antidote                               |
| ------------------ | ----------------------------------------------- | -------------------------------------- |
| Confirmation Bias  | Seeking evidence that supports existing beliefs | Actively seek disconfirming evidence   |
| Anchoring          | Over-relying on first piece of information      | Consider multiple starting points      |
| Sunk Cost          | Continuing because of past investment           | Focus only on future costs/benefits    |
| Availability       | Overweighting recent or memorable examples      | Use base rates and data                |
| Groupthink         | Conforming to group consensus                   | Assign devil's advocate role           |
| Overconfidence     | Excessive certainty in predictions              | Calibrate with probability ranges      |
| Analysis Paralysis | Over-analyzing instead of deciding              | Set decision deadlines, bias to action |


## Parent Hub
- [_process-architecture-mastery](../_process-architecture-mastery/SKILL.md)
