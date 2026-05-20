---
name: transformation-workflow
description: Practical application guide for HUMMBL's 6 transformations (Perspective, Inversion, Composition, Decomposition, Recursion, Meta-Systems). Includes when to use each transformation, combination patterns, analysis templates, output formats, real-world examples, and common pitfalls. Essential for applying mental models effectively in problem-solving and analysis.
---

# Transformation Workflow Skill

Practical guide for applying HUMMBL's 6 transformations to real-world problems. Provides step-by-step workflows, combination patterns, templates, and examples for effective mental model usage.

## Overview

The 6 HUMMBL transformations represent different cognitive operations:

1. **Perspective (P):** Frame and name what is
2. **Inversion (IN):** Reverse assumptions  
3. **Composition (CO):** Combine parts into wholes
4. **Decomposition (DE):** Break wholes into components
5. **Recursion (RE):** Iterate, feedback, self-reference
6. **Meta-Systems (SY):** Coordinate systems-of-systems

## When to Use Each Transformation

### Perspective (P) - Use When:

**Problem Indicators:**
- ✅ Problem statement unclear or ambiguous
- ✅ Stakeholders have conflicting views
- ✅ Need to understand different viewpoints
- ✅ Framing feels wrong or limiting
- ✅ Context not fully understood

**Trigger Questions:**
- "How do different people see this?"
- "What am I missing in how I frame this?"
- "Whose perspective matters here?"
- "What context am I ignoring?"

**Best For:**
- Requirements gathering
- Stakeholder analysis
- Problem definition
- User research
- Strategic framing

### Inversion (IN) - Use When:

**Problem Indicators:**
- ✅ Stuck with conventional thinking
- ✅ Need fresh perspective
- ✅ Want to avoid failure
- ✅ Looking for non-obvious solutions
- ✅ Need to challenge assumptions

**Trigger Questions:**
- "What's the opposite approach?"
- "What if this fails - why?"
- "What should we NOT do?"
- "What assumptions can we reverse?"

**Best For:**
- Brainstorming
- Risk analysis
- Innovation
- Assumption testing
- Creativity boost

### Composition (CO) - Use When:

**Problem Indicators:**
- ✅ Have multiple components to integrate
- ✅ Need to build cohesive solution
- ✅ Want synergies between parts
- ✅ Creating system from pieces
- ✅ Assembling team/resources

**Trigger Questions:**
- "How do these parts work together?"
- "What synergies exist?"
- "How to integrate this?"
- "What's the whole picture?"

**Best For:**
- Solution design
- System architecture
- Team formation
- Strategy synthesis
- Product development

### Decomposition (DE) - Use When:

**Problem Indicators:**
- ✅ System too complex to understand
- ✅ Need to find root cause
- ✅ Looking for bottlenecks
- ✅ Want to prioritize efforts
- ✅ Debugging or troubleshooting

**Trigger Questions:**
- "What are the parts?"
- "Why is this happening?"
- "Where's the constraint?"
- "What's essential vs nice-to-have?"

**Best For:**
- Problem diagnosis
- System analysis
- Prioritization
- Root cause analysis
- Debugging

### Recursion (RE) - Use When:

**Problem Indicators:**
- ✅ Dealing with feedback loops
- ✅ Iterative process needed
- ✅ Self-reinforcing dynamics present
- ✅ Need progressive improvement
- ✅ Growth/decline accelerating

**Trigger Questions:**
- "What's feeding back into itself?"
- "How do we iterate?"
- "What cycles exist here?"
- "What's the second-order effect?"

**Best For:**
- Growth strategy
- Process improvement
- System dynamics
- Iterative development
- Feedback management

### Meta-Systems (SY) - Use When:

**Problem Indicators:**
- ✅ Strategic decision needed
- ✅ Multiple systems interacting
- ✅ Long-term consequences matter
- ✅ Systemic intervention needed
- ✅ Choosing which model to use

**Trigger Questions:**
- "What's the systems view?"
- "What are second/third-order effects?"
- "Where's the leverage point?"
- "Which mental model applies?"

**Best For:**
- Strategic planning
- System design
- Leverage point identification
- Model selection
- Long-term thinking

## Transformation Workflows

### Workflow 1: Perspective Analysis

**Input:** Problem statement, context

**Steps:**
1. **State the problem** (1 sentence)
2. **List stakeholders** (P2: Stakeholder Mapping)
   - Who is affected?
   - Who has power?
   - Who has information?
3. **Apply multiple lenses** (P4: Lens Shifting)
   - Technical lens
   - Business lens
   - User lens
   - Ethical lens
4. **Identify first principles** (P1)
   - What must be true?
   - What are non-negotiables?
   - What are fundamental constraints?
5. **Document context** (P8: Context Awareness)
   - Time constraints
   - Resource constraints
   - Political/cultural factors

**Output Format:**
```markdown
## Perspective Analysis

**Problem:** [1-sentence problem statement]

**Stakeholders:**
- [Stakeholder 1]: [Their perspective/interest]
- [Stakeholder 2]: [Their perspective/interest]
- [Stakeholder 3]: [Their perspective/interest]

**Multiple Lenses:**
- **Technical:** [Technical view]
- **Business:** [Business view]
- **User:** [User view]
- **Ethical:** [Ethical considerations]

**First Principles:**
1. [Fundamental truth 1]
2. [Fundamental truth 2]
3. [Fundamental truth 3]

**Context:**
- **Time:** [Timeline factors]
- **Resources:** [Resource constraints]
- **Environment:** [External factors]

**Insights:**
- [Key insight 1]
- [Key insight 2]
```

**Example:** Software architecture decision
- **Problem:** Choose between microservices vs monolith
- **Stakeholders:** Engineering (prefers interesting tech), Product (wants speed), Operations (wants stability)
- **Lenses:** Technical (complexity trade-offs), Business (cost/time), User (performance)
- **First Principles:** Team size matters more than technology
- **Output:** Decision framework based on team constraints, not tech fashion

### Workflow 2: Inversion Analysis

**Input:** Problem, current approach

**Steps:**
1. **State current approach**
2. **Apply inversion** (IN1)
   - What if we did the opposite?
   - What would the inverse solution look like?
3. **Run premortem** (IN8)
   - Assume total failure in 6 months
   - Why did it fail?
   - What went wrong?
4. **Apply via negativa** (IN3)
   - What should we STOP doing?
   - What to remove, not add?
5. **Seek disconfirmation** (IN15)
   - What evidence contradicts our plan?
   - Who disagrees and why?

**Output Format:**
```markdown
## Inversion Analysis

**Current Approach:** [Description]

**Inverted Approach:**
- Instead of [X], what if we [opposite of X]?
- Result: [Insights from inversion]

**Premortem (Assume Failure):**
- **Failure Scenario:** [What failed]
- **Root Cause:** [Why it failed]
- **Warning Signs:** [Early indicators we missed]

**Via Negativa (What to STOP):**
- Stop: [Thing 1]
- Stop: [Thing 2]
- Stop: [Thing 3]

**Disconfirming Evidence:**
- [Evidence against our approach]
- [Counterargument]
- [Risk we're underestimating]

**Revised Approach:**
- [Improvements based on inversion]
```

**Example:** Product launch strategy
- **Current:** Big launch event, lots of marketing
- **Inversion:** What if we did quiet launch to small group?
- **Premortem:** Event flops because nobody cares, spent budget wrong
- **Via Negativa:** Stop assuming launch is most important thing
- **Output:** Phased launch, test with early adopters first

### Workflow 3: Composition Strategy

**Input:** Components, requirements

**Steps:**
1. **List all components**
2. **Identify synergies** (CO1)
   - Where do parts enhance each other?
   - What emergent properties arise?
3. **Design synthesis** (CO4)
   - How to merge into coherent whole?
   - What's the unifying concept?
4. **Plan orchestration** (CO19)
   - How to coordinate components?
   - What's the execution sequence?
5. **Create holistic integration** (CO20)
   - Complete unified system
   - No loose ends

**Output Format:**
```markdown
## Composition Strategy

**Components:**
1. [Component 1] - [Purpose]
2. [Component 2] - [Purpose]
3. [Component 3] - [Purpose]

**Synergies:**
- [Comp A] + [Comp B] = [Synergy]
- [Comp B] + [Comp C] = [Synergy]

**Synthesis Design:**
- **Unifying Concept:** [Central idea that ties everything]
- **Integration Points:** [Where components connect]
- **Emergent Properties:** [New capabilities from combination]

**Orchestration Plan:**
1. [Phase 1]: [Components + actions]
2. [Phase 2]: [Components + actions]
3. [Phase 3]: [Components + actions]

**Holistic Integration:**
- [How all pieces form complete system]
- [Quality properties of whole]
```

**Example:** Building product ecosystem
- **Components:** Core product, API, marketplace, analytics
- **Synergies:** API enables marketplace, marketplace drives analytics, analytics improves product
- **Synthesis:** Platform strategy
- **Output:** Integrated ecosystem with network effects

### Workflow 4: Decomposition Analysis

**Input:** Complex system or problem

**Steps:**
1. **Define the whole**
2. **Find root cause** (DE1)
   - 5 Whys technique
   - Causal chain analysis
3. **Apply divide & conquer** (DE2)
   - Break into logical subsystems
   - Identify interfaces
4. **Identify bottleneck** (DE6)
   - Theory of Constraints
   - What's the limiting factor?
5. **Pareto analysis** (DE7)
   - What's the vital 20%?
   - Where to focus effort?

**Output Format:**
```markdown
## Decomposition Analysis

**System:** [Description of whole]

**Root Cause Analysis:**
- Why? [Reason 1]
  - Why? [Reason 2]
    - Why? [Reason 3]
      - Why? [Reason 4]
        - Why? [ROOT CAUSE]

**Component Breakdown:**
├── [Component A]
│   ├── [Subcomponent A1]
│   └── [Subcomponent A2]
├── [Component B]
│   ├── [Subcomponent B1]
│   └── [Subcomponent B2]
└── [Component C]

**Bottleneck:**
- **Constraint:** [Limiting factor]
- **Impact:** [How it limits system]
- **Intervention:** [How to address]

**Pareto (80/20):**
- **Vital Few (20%):**
  - [Critical element 1]
  - [Critical element 2]
- **Trivial Many (80%):**
  - [Less critical elements]

**Action Plan:**
1. [Address root cause]
2. [Remove bottleneck]
3. [Focus on vital 20%]
```

**Example:** Website performance issues
- **Root Cause:** Inefficient database queries (not server capacity)
- **Breakdown:** Frontend, API, Database, Cache, CDN
- **Bottleneck:** Database query on user table
- **Pareto:** 3 queries cause 80% of slow responses
- **Output:** Optimize those 3 queries first

### Workflow 5: Recursion Analysis

**Input:** System with dynamics over time

**Steps:**
1. **Map feedback loops** (RE1)
   - Positive (reinforcing)
   - Negative (balancing)
2. **Identify virtuous cycles** (RE7)
   - What creates growth?
   - How to amplify?
3. **Identify vicious cycles** (RE8)
   - What creates decline?
   - How to break?
4. **Design iteration** (RE2)
   - How to improve progressively?
   - What's the learning loop?
5. **Analyze second-order** (RE19)
   - Effects of effects
   - Compound dynamics

**Output Format:**
```markdown
## Recursion Analysis

**System Dynamics:**

**Feedback Loops:**
- ➕ **Virtuous Cycle:** [A] → [B] → [C] → [More A]
- ➖ **Vicious Cycle:** [X] → [Y] → [Z] → [More X]
- ⚖️ **Balancing Loop:** [M] → [N] → [Less M]

**Virtuous Cycles (Amplify These):**
1. [Positive cycle 1]
   - Trigger: [What starts it]
   - Amplify: [How to strengthen]
2. [Positive cycle 2]

**Vicious Cycles (Break These):**
1. [Negative cycle 1]
   - Cause: [What perpetuates it]
   - Intervention: [How to break]
2. [Negative cycle 2]

**Iterative Improvement:**
- **Version 1:** [Initial state]
- **Learn:** [What to measure]
- **Improve:** [What to adjust]
- **Repeat:** [Cycle time]

**Second-Order Effects:**
- First-order: [Direct effect]
- Second-order: [Effect of effect]
- Third-order: [Effect of effect of effect]

**Leverage Points:**
- [Where small change creates big impact]
```

**Example:** SaaS growth
- **Virtuous Cycle:** Good product → Happy users → Referrals → More users → More feedback → Better product
- **Vicious Cycle:** Bugs → Bad reviews → Fewer signups → Less revenue → Less engineering → More bugs
- **Iteration:** Weekly releases, measure NPS, improve top complaint
- **Output:** Strategy to amplify virtuous, break vicious cycles

### Workflow 6: Meta-Systems Strategy

**Input:** Strategic question or complex system

**Steps:**
1. **Apply systems thinking** (SY1)
   - See whole system
   - Identify interconnections
2. **Second-order thinking** (SY2)
   - Consequences of consequences
   - Nth-order effects
3. **Find leverage points** (SY4)
   - Where to intervene?
   - High-impact, low-effort
4. **Anticipate unintended consequences** (SY5)
   - What could go wrong?
   - Side effects?
5. **Model selection** (SY19)
   - Which other models apply?
   - What's the right analytical approach?

**Output Format:**
```markdown
## Meta-Systems Strategy

**Strategic Question:** [Question]

**Systems View:**
┌─────────────────────────────────┐
│  [System Component 1]           │
│    ↓ ↑                          │
│  [System Component 2]           │
│    ↓ ↑                          │
│  [System Component 3]           │
└─────────────────────────────────┘

**Interconnections:**
- [A] affects [B] via [mechanism]
- [B] affects [C] via [mechanism]
- [C] feeds back to [A] via [mechanism]

**Second-Order Analysis:**
| Action | 1st Order | 2nd Order | 3rd Order |
|--------|-----------|-----------|-----------|
| [Action 1] | [Direct effect] | [Effect of effect] | [Further effect] |
| [Action 2] | [Direct effect] | [Effect of effect] | [Further effect] |

**Leverage Points** (Highest to Lowest Impact):
1. **[Point 1]:** [Why high leverage]
2. **[Point 2]:** [Why medium leverage]
3. **[Point 3]:** [Why low leverage]

**Unintended Consequences:**
- Risk: [Potential negative outcome]
- Mitigation: [How to prevent]

**Model Selection:**
- Primary: [Model code + name]
- Secondary: [Model code + name]
- Why: [Justification]

**Recommended Strategy:**
- [Strategic approach based on analysis]
```

**Example:** Market expansion decision
- **Systems View:** Current market, new market, competitors, resources
- **Second-Order:** Enter new market → Spread resources thin → Lose focus in current market → Competitors gain ground
- **Leverage:** Instead of new market, deepen penetration in current (10x ROI)
- **Output:** Stay focused strategy, not expansion

## Combination Patterns

### Pattern 1: P → DE → CO (Understand → Analyze → Build)

**Use Case:** Building new solution  
**Steps:**
1. **Perspective:** Understand problem from multiple angles
2. **Decomposition:** Break down into components
3. **Composition:** Integrate into solution

**Example:** Designing new feature
- P: Stakeholder needs (users want X, business wants Y)
- DE: Break into sub-features, identify dependencies
- CO: Integrate into cohesive feature with good UX

### Pattern 2: P → IN → SY (Frame → Challenge → Strategy)

**Use Case:** Strategic decision  
**Steps:**
1. **Perspective:** Frame the situation
2. **Inversion:** Challenge assumptions
3. **Meta-Systems:** Strategic synthesis

**Example:** Business model pivot
- P: Current model's perspective, customer viewpoint
- IN: What if opposite? What to stop?
- SY: Strategic choice based on systems thinking

### Pattern 3: DE → IN → CO (Analyze → Invert → Rebuild)

**Use Case:** Innovation/redesign  
**Steps:**
1. **Decomposition:** Understand current system
2. **Inversion:** Challenge how it works
3. **Composition:** Build new solution

**Example:** Process improvement
- DE: Map current process, find bottleneck
- IN: What if we removed steps? Did opposite?
- CO: Redesigned process

### Pattern 4: All 6 in Sequence (Complete Analysis)

**Use Case:** Major strategic initiative  
**Steps:**
1. **P:** Frame problem
2. **IN:** Challenge assumptions
3. **DE:** Analyze components
4. **CO:** Build solution
5. **RE:** Plan iteration
6. **SY:** Strategic integration

**Example:** Company transformation
- Use all 6 transformations systematically
- Comprehensive, robust analysis
- Takes longer but minimizes blind spots

### Pattern 5: RE wrapping any other (Iterative Application)

**Use Case:** Continuous improvement  
**Structure:** RE(P/IN/CO/DE/SY)

**Example:** Product development
- Week 1: P (understand users)
- Week 2: DE (analyze feedback)
- Week 3: CO (build improvements)
- Week 4: RE (iterate based on results)
- Repeat

## Common Pitfalls & Solutions

### Pitfall 1: Using Wrong Transformation

**Error:** Applying Decomposition when need Perspective  
**Symptom:** Breaking down problem doesn't help because problem not understood  
**Solution:** Start with P (frame first), then DE (analyze)

### Pitfall 2: Skipping Inversion

**Error:** Going straight to solution without challenging assumptions  
**Symptom:** Conventional thinking, missing creative options  
**Solution:** Always apply IN before finalizing approach

### Pitfall 3: Decomposition Without Recomposition

**Error:** Breaking things down but never synthesizing  
**Symptom:** Analysis paralysis, no actionable solution  
**Solution:** DE must be followed by CO (analyze then build)

### Pitfall 4: Ignoring Feedback Loops

**Error:** Linear thinking in dynamic system  
**Symptom:** Interventions don't work as expected  
**Solution:** Apply RE to understand dynamics

### Pitfall 5: Local Optimization

**Error:** Optimizing parts without seeing whole  
**Symptom:** Suboptimization, missing systemic issues  
**Solution:** Use SY (systems view) before optimizing

### Pitfall 6: Single-Model Thinking

**Error:** Using only one model/transformation  
**Symptom:** One-dimensional analysis, blind spots  
**Solution:** Combine multiple transformations (patterns above)

### Pitfall 7: Overcomplication

**Error:** Applying all 6 when 2 would suffice  
**Symptom:** Slow progress, diminishing returns  
**Solution:** Start simple (1-2 transformations), add if needed

## Transformation Selection Flowchart

```
START: What's your primary need?

├─ "Understand the problem"
│  → Use PERSPECTIVE (P)
│  → Then consider: DE (analyze) or IN (challenge)

├─ "Stuck or need creativity"
│  → Use INVERSION (IN)
│  → Then consider: P (reframe) or CO (rebuild)

├─ "Build/integrate solution"
│  → Use COMPOSITION (CO)
│  → Likely needed: DE first (analyze parts)

├─ "Analyze complex system"
│  → Use DECOMPOSITION (DE)
│  → Then consider: CO (reintegrate) or SY (systems view)

├─ "Handle dynamics/feedback"
│  → Use RECURSION (RE)
│  → Then consider: SY (systemic) or DE (analyze loops)

└─ "Strategic/systemic decision"
   → Use META-SYSTEMS (SY)
   → Then consider: P (perspectives) + IN (challenge)
```

## Quick Templates

### 5-Minute Quick Analysis

1. **P:** Who are stakeholders? (30 sec)
2. **IN:** What's the opposite? (30 sec)
3. **DE:** What's the bottleneck? (1 min)
4. **CO:** How to integrate? (1 min)
5. **RE:** What's the feedback? (1 min)
6. **SY:** What's the leverage? (1 min)

### One-Page Strategy

**Problem:** [1 sentence]  
**Perspective:** [Key stakeholders, key lens]  
**Inversion:** [What NOT to do]  
**Decomposition:** [Critical components]  
**Composition:** [How they integrate]  
**Recursion:** [Key feedback loop]  
**Systems:** [Leverage point]  
**Action:** [Next step]

## Resources

- **HUMMBL Framework Skill:** Complete model reference
- **Model Codes:** P1-P20, IN1-IN20, CO1-CO20, DE1-DE20, RE1-RE20, SY1-SY20
- **Quality Standard:** 9.0/10 minimum for application
- **Validation:** Oct 29, 2025 Base120 specification

## Success Criteria

**Effective transformation application achieves:**
- ✅ Clear process followed
- ✅ Appropriate transformation selected
- ✅ Insights generated (not just analysis)
- ✅ Actionable outputs
- ✅ Documented reasoning

**Application fails if:**
- ❌ Wrong transformation chosen
- ❌ Process skipped/rushed
- ❌ No insights emerged
- ❌ Can't act on results
- ❌ Reasoning not documented
