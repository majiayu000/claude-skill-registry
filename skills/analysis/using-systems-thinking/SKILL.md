---
name: using-systems-thinking
description: Router for systems thinking methodology - patterns, leverage points, archetypes, stocks-flows, causal loops, BOT graphs
---

# Using Systems-Thinking (Meta-Skill Router)

**Your entry point to systems thinking methodology.** This skill routes you to the right combination of systems analysis skills for understanding complex, interconnected problems.

## Purpose

This is a **meta-skill** that:
1. ✅ **Routes** you to the correct systems thinking skills
2. ✅ **Combines** multiple skills for comprehensive analysis
3. ✅ **Provides** workflows for common problem types
4. ✅ **Explains** when to use systems thinking vs other approaches

**You should use this skill:** When facing complex problems with feedback loops, delays, unintended consequences, or persistent failures despite interventions.

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-systems-thinking/SKILL.md`

Reference sheets like `causal-loop-diagramming.md` are at:
  `skills/using-systems-thinking/causal-loop-diagramming.md`

NOT at:
  `skills/causal-loop-diagramming.md` ← WRONG PATH

When you see a link like `[causal-loop-diagramming.md](causal-loop-diagramming.md)`, read the file from the same directory as this SKILL.md.

---

## Core Philosophy: Think in Systems

### The Central Idea

**Linear Thinking**: Problem → Solution → Fixed
- Assumes cause and effect are close in time and space
- Ignores feedback loops and delays
- Leads to "fixes that fail" and escalation
- Symptoms return or move elsewhere

**Systems Thinking**: Structure → Behavior → Intervention
- Recognizes feedback loops create behavior
- Delays cause intuition failures
- Small interventions at leverage points beat brute force
- Address root causes, not symptoms

### When This Pack Applies

**✅ Use systems-thinking when:**
- Problems persist despite repeated fixes
- Solutions create new problems (unintended consequences)
- System behavior is counter-intuitive
- Multiple stakeholders with conflicting incentives
- Long delays between action and result
- "The harder we push, the harder the system pushes back"

**❌ Don't use systems-thinking when:**
- Simple, isolated problems with clear cause-effect
- One-time decisions with immediate results
- Pure optimization (no feedback dynamics)
- Well-understood linear processes

---

## Pack Overview: 6 Core Skills

### Wave 1: Foundation and Pattern Recognition

#### 1. recognizing-system-patterns
**When to use:** ANY complex problem - start here
**Teaches:** S-curves, feedback loops (reinforcing/balancing), delays, stock-flow thinking
**Examples:** Viral growth, technical debt, burnout spirals
**Time:** 45-60 min
**Key insight:** Behavior patterns reveal underlying structure

#### 2. systems-archetypes-reference
**When to use:** Recognize recurring problem patterns
**Teaches:** 10 classic archetypes (Fixes that Fail, Shifting the Burden, Escalation, etc.)
**Examples:** Feature factory, hero culture, arms race
**Time:** 60-90 min
**Key insight:** Most problems match known patterns with known solutions

#### 3. leverage-points-mastery
**When to use:** Design interventions, prioritize where to act
**Teaches:** Donella Meadows' 12 leverage points hierarchy
**Examples:** Constants (weak) vs rules vs paradigms (powerful)
**Time:** 60-75 min
**Key insight:** Small changes at high leverage points beat large changes at low points

### Wave 2: Quantitative Analysis

#### 4. stocks-and-flows-modeling
**When to use:** Predict future states, calculate equilibrium, analyze accumulation dynamics
**Teaches:** Formal notation, equilibrium analysis, time constants, delay analysis
**Examples:** Customer churn, bug backlog, burnout accumulation
**Time:** 75-90 min
**Key insight:** Quantification elevates from "will get worse" to "6.7 weeks to crisis"

#### 5. causal-loop-diagramming
**When to use:** Map system structure, communicate feedback dynamics, find root causes
**Teaches:** 6-step construction process, polarity testing, loop identification
**Examples:** Death spirals, virtuous cycles, balancing processes
**Time:** 60-75 min
**Key insight:** Systematic construction prevents polarity errors that change diagnosis

#### 6. behavior-over-time-graphs
**When to use:** Show trajectories, compare scenarios, communicate dynamics over time
**Teaches:** 7-step construction, 70-80% scale rule, ASCII standards, validation
**Examples:** S-curve adoption, crisis timing, intervention impact
**Time:** 60-75 min
**Key insight:** "What happens over time" with concrete numbers and dates

---

## Routing Logic: Which Skills Do I Need?

### Decision Tree

```
START: What's your goal?

├─ UNDERSTAND A PROBLEM (First time encountering complexity)
│  ├─ Start here → recognizing-system-patterns
│  ├─ Does it match a known pattern? → systems-archetypes-reference
│  └─ What behavior over time? → behavior-over-time-graphs
│
├─ MAP SYSTEM STRUCTURE (How does this work?)
│  ├─ Identify feedback loops → causal-loop-diagramming
│  ├─ Calculate accumulation → stocks-and-flows-modeling
│  └─ Show dynamics → behavior-over-time-graphs
│
├─ DESIGN INTERVENTIONS (What should we do?)
│  ├─ Identify leverage points → leverage-points-mastery
│  ├─ Predict outcomes → stocks-and-flows-modeling + behavior-over-time-graphs
│  └─ Match to archetype solution → systems-archetypes-reference
│
├─ COMMUNICATE TO STAKEHOLDERS (Convince others)
│  ├─ Executive version → behavior-over-time-graphs (with $ impacts)
│  ├─ Technical version → causal-loop-diagramming + stocks-and-flows-modeling
│  └─ Pattern recognition → systems-archetypes-reference ("We're in Fixes that Fail")
│
└─ QUANTITATIVE PREDICTION (When will crisis hit? How many?)
   ├─ Calculate trajectory → stocks-and-flows-modeling
   ├─ Visualize scenarios → behavior-over-time-graphs
   └─ Validate structure → causal-loop-diagramming
```

---

## Common Problem Types and Skill Combinations

### Scenario 1: "Our Solution Keeps Failing"

**Symptoms:**
- Applied fix multiple times
- Problem returns or gets worse
- "We tried everything"

**Routing Sequence:**
1. **systems-archetypes-reference** → Recognize "Fixes that Fail" or "Shifting the Burden"
2. **causal-loop-diagramming** → Map the reinforcing loop keeping problem alive
3. **leverage-points-mastery** → Find intervention point (probably addressing root cause, not symptom)
4. **behavior-over-time-graphs** → Show "with fix" vs "without fix" vs "address root cause"

**Why this sequence:**
- Archetypes give you the pattern (quick recognition)
- CLD maps the specific instance
- Leverage points guide where to intervene
- BOT graphs communicate to stakeholders

### Scenario 2: "Growth is Slowing / Hitting Limits"

**Symptoms:**
- Initial success, now plateauing
- S-curve behavior
- Limits to growth

**Routing Sequence:**
1. **recognizing-system-patterns** → Identify S-curve, find the balancing loop
2. **stocks-and-flows-modeling** → Calculate time to saturation, equilibrium capacity
3. **systems-archetypes-reference** → "Limits to Growth" archetype
4. **leverage-points-mastery** → Options: expand limit, find new growth, stabilize
5. **behavior-over-time-graphs** → Show trajectory with/without limit expansion

**Why this sequence:**
- Pattern recognition confirms S-curve
- Stock-flow gives you numbers (when hits limit?)
- Archetype provides intervention options
- Leverage points prioritize options
- BOT graphs show impact

### Scenario 3: "We're in a Vicious Spiral"

**Symptoms:**
- Self-reinforcing decline
- "The harder we work, the worse it gets"
- Death spiral, burnout, quality collapse

**Routing Sequence:**
1. **recognizing-system-patterns** → Identify reinforcing loop (R)
2. **causal-loop-diagramming** → Map the specific reinforcing structure
3. **systems-archetypes-reference** → Match to "Escalation" or "Success to the Successful"
4. **stocks-and-flows-modeling** → Calculate time to crisis (when does morale hit 0?)
5. **leverage-points-mastery** → Break the loop (add balancing feedback)
6. **behavior-over-time-graphs** → Show crisis timing + intervention impact

**Why this sequence:**
- Pattern recognition identifies reinforcing dynamic
- CLD maps exact structure (what's reinforcing what?)
- Archetype gives tested solutions
- Stock-flow calculates urgency
- Leverage points find where to break loop
- BOT graphs communicate stakes

### Scenario 4: "Delay Between Action and Result"

**Symptoms:**
- Decisions based on old information
- Overshooting, oscillation
- "We keep over/under correcting"

**Routing Sequence:**
1. **recognizing-system-patterns** → Identify delay, oscillation pattern
2. **stocks-and-flows-modeling** → Calculate delay time constant, D/R ratio
3. **causal-loop-diagramming** → Mark delays on causal links (||)
4. **systems-archetypes-reference** → "Shifting the Burden to the Intervenor" (long-term fix delayed)
5. **behavior-over-time-graphs** → Show overshoot/undershoot pattern

**Why this sequence:**
- Pattern recognition confirms delay issue
- Stock-flow quantifies delay danger (D/R > 0.5 = crisis)
- CLD visualizes where delays are
- Archetype matches delay-based patterns
- BOT graphs show oscillation

### Scenario 5: "Presenting to Executives"

**Goal:** Get buy-in for systems-based solution

**Routing Sequence:**
1. **behavior-over-time-graphs** → LEAD with this (clear, visual, $$ impacts)
   - "Current trajectory: 6.7 weeks to crisis"
   - "With intervention: stabilizes at 80% capacity"
2. **systems-archetypes-reference** → Frame as known pattern ("We're in Fixes that Fail")
3. **leverage-points-mastery** → Justify intervention choice ("This is a high-leverage point")
4. **causal-loop-diagramming** → BACKUP ONLY (if asked "why does this happen?")

**Why this sequence:**
- Executives want impact first (BOT graphs)
- Pattern names create shared language (archetypes)
- Leverage points justify resource allocation
- CLDs available if deep dive needed

### Scenario 6: "Multi-Variable System (Technical Debt, Velocity, Morale)"

**Symptoms:**
- Many interacting variables
- Hard to see connections
- Non-obvious causality

**Routing Sequence:**
1. **causal-loop-diagramming** → Map all variables and causal links
2. **stocks-and-flows-modeling** → Calculate multi-stock dynamics (debt, morale, velocity all accumulate)
3. **behavior-over-time-graphs** → Show multi-variable trajectories (separate panels or dual-axis)
4. **leverage-points-mastery** → Identify highest leverage variable

**Why this sequence:**
- CLD handles many variables well
- Stock-flow models accumulation of each
- BOT graphs show multiple trajectories
- Leverage points prioritize where to act

---

## Step-by-Step Workflows

### Workflow 1: Systematic Problem Analysis (80% of use cases)

**Process:**
1. **recognizing-system-patterns** (15 min) - What patterns appear? S-curve? Reinforcing loop?
2. **systems-archetypes-reference** (20 min) - Does this match a known archetype?
3. **causal-loop-diagramming** (30 min) - Map the specific structure
4. **stocks-and-flows-modeling** (45 min) - Quantify key stocks, calculate time constants
5. **leverage-points-mastery** (20 min) - Identify high-leverage interventions
6. **behavior-over-time-graphs** (30 min) - Show current trajectory + intervention scenarios

**Total time:** ~2.5-3 hours
**Output:** Complete systems analysis with quantitative predictions and intervention design

### Workflow 2: Quick Pattern Recognition (When time-limited)

**Process:**
1. **recognizing-system-patterns** (15 min) - Quick pattern ID
2. **systems-archetypes-reference** (20 min) - Match to archetype, use archetype's standard solution

**Total time:** ~35 min
**Output:** Pattern diagnosis + known solution approach
**Trade-off:** No quantification, no custom structure mapping

### Workflow 3: Executive Presentation Prep

**Process:**
1. **stocks-and-flows-modeling** (45 min) - Calculate key numbers (crisis timing, costs, ROI)
2. **behavior-over-time-graphs** (40 min) - Create executive-friendly graphs ($$ impact)
3. **leverage-points-mastery** (15 min) - Justify intervention choice
4. **systems-archetypes-reference** (10 min) - Frame with archetype name

**Total time:** ~110 min
**Output:** Executive presentation with quantified impact

### Workflow 4: Deep Technical Analysis

**Process:**
1. **recognizing-system-patterns** (15 min) - Pattern confirmation
2. **causal-loop-diagramming** (60 min) - Detailed structure mapping, polarity validation
3. **stocks-and-flows-modeling** (90 min) - Multi-stock equations, sensitivity analysis
4. **behavior-over-time-graphs** (45 min) - Multi-scenario comparison
5. **leverage-points-mastery** (30 min) - Evaluate intervention points

**Total time:** ~4 hours
**Output:** Comprehensive technical analysis with validated structure and quantified scenarios

---

## Skill Dependencies and Learning Path

### Learning Path for Beginners

**Start here if new to systems thinking:**

1. **recognizing-system-patterns** (REQUIRED FIRST)
   - Foundation for all other skills
   - Teaches core concepts: stocks, flows, feedback, delays
   - Builds intuition for system behavior

2. **systems-archetypes-reference** (LEARN SECOND)
   - Pattern library accelerates analysis
   - Provides vocabulary (names for patterns)
   - Gives tested solutions

3. Choose path based on needs:
   - **Quantitative path** → stocks-and-flows-modeling → behavior-over-time-graphs
   - **Structural path** → causal-loop-diagramming → leverage-points-mastery

### Skill Dependencies

**No prerequisites:**
- recognizing-system-patterns (START HERE)

**Requires recognizing-system-patterns:**
- systems-archetypes-reference (builds on patterns)
- causal-loop-diagramming (uses feedback loop concepts)
- stocks-and-flows-modeling (uses stock/flow distinction)
- leverage-points-mastery (uses system structure concepts)
- behavior-over-time-graphs (uses pattern recognition)

**Works better together:**
- stocks-and-flows-modeling + behavior-over-time-graphs (calculate, then visualize)
- causal-loop-diagramming + leverage-points-mastery (map structure, find intervention)
- systems-archetypes-reference + leverage-points-mastery (pattern → known leverage points)

---

## Rationalization Resistance Table

| Rationalization | Reality | Counter-Guidance | Red Flag |
|-----------------|---------|------------------|----------|
| "Just add more resources" | Resource additions often activate balancing loops | "Route to leverage-points-mastery - this is lowest-leverage point (constants)" | Ignoring system structure |
| "This isn't a system, it's a simple bug" | Bugs that persist are symptoms of system structure | "Route to systems-archetypes-reference - likely 'Fixes that Fail'" | Linear thinking on complex problems |
| "We don't have time for analysis" | Crisis timing requires stock-flow calculation | "Route to stocks-and-flows-modeling - 15 min calculation vs wrong 6-month commitment" | Analysis paralysis fear |
| "Our situation is unique" | 90% match archetypes | "Route to systems-archetypes-reference - most 'unique' problems aren't" | Not invented here syndrome |
| "Just draw a quick diagram" | Polarity errors change diagnosis (R vs B) | "Route to causal-loop-diagramming - use systematic 6-step process" | Skipping validation |
| "Intuition says it will get worse" | Intuition fails on delays, non-linear dynamics | "Route to stocks-and-flows-modeling - calculate, don't guess" | Overconfidence in intuition |
| "We need to act NOW" | Acting without understanding wastes resources | "Route to recognizing-system-patterns - 15 min pattern ID prevents months of wrong solution" | Action bias |
| "Too complicated to model" | Most systems can be modeled simply | "Route to stocks-and-flows-modeling - start with 1-2 stocks" | Complexity avoidance |
| "Graphs are for presentations, not analysis" | Graphs reveal patterns invisible in tables | "Route to behavior-over-time-graphs - construction process IS analysis" | Separating analysis from communication |

---

## Red Flags Checklist

Watch for these signs of incorrect approach:

- [ ] **Linear Thinking**: "X causes Y, so fix X" (ignoring feedback loops)
- [ ] **Symptom Treating**: Addressing symptoms without mapping structure
- [ ] **Resource Obsession**: Only considering "add more people/money" solutions
- [ ] **Analysis Paralysis**: Trying to model everything instead of starting simple
- [ ] **Skipping Validation**: Drawing CLDs without polarity double-test
- [ ] **Gut-Feel Quantification**: "Probably double in 6 months" without calculation
- [ ] **Graph Manipulation**: Tweaking scale to make problems look bigger/smaller
- [ ] **Archetype Forcing**: Forcing problem into wrong archetype
- [ ] **Ignoring Delays**: Not marking delays on CLDs or calculating time constants
- [ ] **Single-Skill Fixation**: Using only one tool (e.g., only CLDs, no quantification)

**If any red flag triggered → STOP → Route to appropriate skill(s)**

---

## When NOT to Use This Pack

Clarify boundaries with other approaches:

| Problem Type | Use Instead | Reason |
|--------------|-------------|--------|
| Well-understood algorithm optimization | Standard profiling/optimization | No feedback dynamics |
| One-time decision with immediate result | Decision analysis, expected value | No time dynamics |
| Pure data analysis / statistics | Data science methods | Not about system structure |
| Legal/compliance requirements | Ordis security-architect | Different domain |
| Pure UX research | Lyra ux-designer | Different methodology |
| Code architecture | Axiom system-architect | Code structure, not system dynamics |

**Edge case:** Software architecture CAN have systems dynamics (technical debt accumulation, team coordination). Use **both** system-architect (structure) AND systems-thinking (dynamics).

---

## Integration with Other Packs

### Simulation-Foundations (Yzmir)
- **Use together when:** Need to implement simulation based on systems model
- **Workflow:** systems-thinking (design) → simulation-foundations (implementation)
- **Example:** Model ecosystem with stocks-and-flows → implement with differential-equations-for-games

### System-Architect (Axiom)
- **Use together when:** Software architecture decisions have feedback dynamics
- **Workflow:** system-architect (code structure) + systems-thinking (team/process dynamics)
- **Example:** Microservices architecture (static) + team coordination dynamics (systems thinking)

### Deep-RL (Yzmir)
- **Use together when:** Training RL agents in systems with feedback
- **Workflow:** systems-thinking (environment analysis) → deep-rl (agent design)
- **Example:** Understand ecosystem dynamics with causal-loop-diagramming → train agents with actor-critic-methods

---

## Summary: Start Here

**First time with systems thinking?**
→ **recognizing-system-patterns** (foundation skill, 45-60 min)

**Problem keeps returning despite fixes?**
→ **systems-archetypes-reference** → Find "Fixes that Fail" or "Shifting the Burden"

**Need to predict future states?**
→ **stocks-and-flows-modeling** → Calculate time to crisis, equilibrium

**Need to map system structure?**
→ **causal-loop-diagramming** → Visualize feedback loops

**Need to design intervention?**
→ **leverage-points-mastery** → Find high-leverage points

**Need to communicate dynamics?**
→ **behavior-over-time-graphs** → Show trajectories over time

**Not sure where to start?**
→ Use this router skill! Ask diagnostic questions:
- "Is this problem persisting despite fixes?"
- "Are there delays between action and result?"
- "Do we understand the feedback loops?"
- "What's the goal: understand, map, intervene, or communicate?"

**Most common workflow:**
recognizing-system-patterns → systems-archetypes-reference → causal-loop-diagramming → stocks-and-flows-modeling → leverage-points-mastery → behavior-over-time-graphs

**Time for complete analysis:** 2.5-4 hours (depending on complexity)

**Key principle:** Start with patterns, match to archetypes, map structure, quantify dynamics, find leverage, visualize scenarios.

---

## Systems Thinking Specialist Skills Catalog

After routing, load the appropriate specialist skill for detailed guidance:

1. [recognizing-system-patterns.md](recognizing-system-patterns.md) - Foundation: S-curves, feedback loops, delays, stock-flow thinking, pattern recognition
2. [systems-archetypes-reference.md](systems-archetypes-reference.md) - 10 classic archetypes: Fixes that Fail, Shifting the Burden, Escalation, recurring patterns
3. [leverage-points-mastery.md](leverage-points-mastery.md) - Donella Meadows' 12 leverage points, intervention design, prioritization
4. [stocks-and-flows-modeling.md](stocks-and-flows-modeling.md) - Quantitative modeling: equilibrium analysis, time constants, accumulation dynamics
5. [causal-loop-diagramming.md](causal-loop-diagramming.md) - Structure mapping: 6-step construction, polarity testing, loop identification
6. [behavior-over-time-graphs.md](behavior-over-time-graphs.md) - Trajectory visualization: 7-step construction, scenario comparison, communication
