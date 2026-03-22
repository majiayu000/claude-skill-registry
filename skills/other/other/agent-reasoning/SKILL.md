---
name: Agent Reasoning & Decision-Making
description: Design effective reasoning processes for AI agents and optimize decision-making strategies. Use when designing agent prompts, improving decision quality, implementing specialized reasoning modes, creating reasoning traces, or debugging agent mistakes. Covers prompting, chain-of-thought, reasoning depth, and decision evaluation.
---

# Agent Reasoning & Decision-Making

The quality of an agent's decisions depends on how well its reasoning is structured, prompted, and evaluated. This skill covers designing effective reasoning systems.

## Reasoning Quality Foundations

### What Makes Reasoning Effective?

1. **Explicit**: Agent states assumptions and reasoning steps
2. **Transparent**: Humans can follow and audit the logic
3. **Justified**: Decisions grounded in evidence, not guessing
4. **Adaptive**: Agent adjusts reasoning based on situation complexity
5. **Verifiable**: Outputs can be checked against facts
6. **Efficient**: Doesn't over-think simple decisions or under-think complex ones

### Reasoning vs. Task Complexity

**Match reasoning depth to task complexity**:

```
SIMPLE TASK (routine, low stakes)
Example: "Classify customer email"
Reasoning needed: Quick classification
Prompt: "Classify as complaint/inquiry/feedback"
Cost: ~0.1 seconds

MODERATE TASK (needs consideration, medium stakes)
Example: "Recommend product to customer"
Reasoning needed: Consider preferences, history, fit
Prompt: "Review customer profile, similar customers, suggest with reasoning"
Cost: ~2-5 seconds

COMPLEX TASK (ambiguous, high stakes)
Example: "Design feature architecture for new product"
Reasoning needed: Multiple considerations, trade-offs, validation
Prompt: Chain-of-thought + structured framework
Cost: ~10-30 seconds

CRITICAL TASK (irreversible, strategic)
Example: "Recommend major organizational change"
Reasoning needed: Deep analysis, multiple perspectives, risk assessment
Prompt: Full reasoning trace + stakeholder consideration + alternatives
Cost: ~1-5 minutes
```

**Key principle**: Over-reasoning simple tasks wastes resources. Under-reasoning complex tasks causes errors.

## Prompting Strategies for Better Reasoning

### Strategy 1: Chain-of-Thought Prompting

**Basic**: Ask agent to show reasoning

```
USER PROMPT (Basic):
"Analyze this customer complaint and recommend resolution"

USER PROMPT (Better - Chain-of-Thought):
"Analyze this customer complaint and recommend resolution.
Before your recommendation, think through:
1. What is the customer's core issue?
2. Why did this happen?
3. What are possible resolutions?
4. What are pros/cons of each?
5. Which resolution best balances fairness and cost?"
```

**Effect**: Forces explicit reasoning, improves decision quality by 30-50% in many cases.

**When to use**:
- Moderate to complex decisions
- Where mistakes are visible and costly
- When auditability matters

**Cost**: Extra inference time (2-5x longer prompts)

---

### Strategy 2: Tree-of-Thought (Exploring Multiple Paths)

**Use when**: Multiple valid approaches exist; need to explore options

```
AGENT REASONING:
"How should we handle this customer return?"

TREE STRUCTURE:
├─ Path 1: Full refund
│  ├─ Pro: Highest customer satisfaction
│  ├─ Con: ~$200 cost
│  └─ Risk: Sets precedent for similar claims
├─ Path 2: Partial refund + replacement
│  ├─ Pro: Balanced approach
│  ├─ Con: More complex
│  └─ Risk: Customer may want full refund
└─ Path 3: Replacement only
   ├─ Pro: Lower cost
   ├─ Con: Customer may dissatisfied
   └─ Risk: Negative review

DECISION: Path 2 recommended because...
```

**Implementation**:
```
PROMPT:
"Consider this decision from multiple angles.
For each major approach:
1. Describe the approach
2. When is it appropriate?
3. What are risks?
4. What are benefits?

Then recommend the best approach and explain why."
```

**Cost**: Higher (explores multiple branches)
**Benefit**: Reduces decision errors by forcing consideration of alternatives

---

### Strategy 3: Structured Framework Prompting

**Use when**: Consistent decision criteria exist

```
DECISION FRAMEWORK FOR FEATURE PRIORITIZATION:

Evaluate each feature on:
1. IMPACT (scale 1-10)
   - How many users affected?
   - How much value created?

2. EFFORT (scale 1-10)
   - Development cost?
   - Maintenance burden?

3. RISK (scale 1-10)
   - Could it break existing features?
   - Security implications?
   - Dependencies?

4. STRATEGIC (scale 1-10)
   - Alignment with roadmap?
   - Competitive advantage?
   - Customer requests?

SCORING: (Impact * Strategic) / (Effort * Risk) = Priority Score

DECISION: Implement features with Priority Score > 5
```

**Advantage**: Consistency across decisions
**Disadvantage**: Requires upfront framework design; can be rigid

---

### Strategy 4: Devil's Advocate Prompting

**Use when**: Need to catch blind spots or overconfidence

```
AGENT REASONING (without devil's advocate):
"We should adopt this vendor because they're cheaper"

AGENT REASONING (with devil's advocate):
"We should adopt this vendor because they're cheaper.

But consider: What could go wrong?
- Vendor lock-in: Hard to switch later?
- Quality: Is cheaper because they cut corners?
- Support: Will support quality suffer?
- Reliability: Any red flags in reviews?
- Hidden costs: Onboarding, training, integration work?

After considering counterarguments, the recommendation is:
[Revised reasoning that accounts for concerns]"
```

**Implementation**:
```
PROMPT:
"Make your recommendation.
Then, play devil's advocate: What are the strongest
objections to your recommendation?
After considering objections, does your recommendation hold?"
```

**Effect**: Reduces overconfidence, catches oversights

---

### Strategy 5: Analogical Reasoning

**Use when**: Similar situations have been solved before

```
CURRENT SITUATION:
"How should we handle declining market share in Asia?"

ANALOGICAL REASONING:
"This is similar to our situation in Europe in 2018 when
market share dropped from 15% to 10%.

What we did then:
1. Analyzed competitors' strategies
2. Adjusted pricing model
3. Increased local hiring
4. Built partnerships with local distributors

Results: Market share recovered to 12% within 18 months.

How to apply to Asia situation:
- Asia competitors: [analysis]
- Adjust pricing for: [local factors]
- Local hiring focus: [regions]
- Partnership opportunities: [specific partners]"
```

**Advantage**: Grounds reasoning in concrete experience
**Disadvantage**: Requires maintaining analogies database; analogy might not fit

## Specialized Reasoning Modes

### Mode 1: Analytical (Breaking Down)

**Use for**: Complex problems that need decomposition

```
PROMPT: "Analyze this situation by breaking it into components.
For each component:
1. What is it?
2. Why does it matter?
3. How does it relate to other components?
4. What's our lever/influence?"
```

**Output structure**:
```
Component 1: Market Demand
  - Details
  - Importance: High (drives revenue)
  - Relationship: Drives pricing decisions
  - Levers: Marketing spend, product features

Component 2: Team Capacity
  - Details
  - Importance: High (limits delivery)
  - Relationship: Constrains timeline
  - Levers: Hiring, outsourcing, priorities

Component 3: Competitive Landscape
  - Details
  - Importance: Medium (affects positioning)
  - Relationship: Influences feature choices
  - Levers: Differentiation, timing
```

### Mode 2: Generative (Exploring Possibilities)

**Use for**: Creative decisions, brainstorming, multiple options

```
PROMPT: "Generate 10 completely different approaches to this challenge.
For each approach, don't evaluate—just describe it.
Then select the most promising 3 for deeper analysis."
```

**Benefit**: Avoids premature closure on first idea

### Mode 3: Evaluative (Judging Options)

**Use for**: Making choices between alternatives

```
PROMPT: "We're choosing between these 3 options: A, B, C.
Create a comparison matrix with criteria: cost, time, quality, risk.
Score each 1-5 and explain scores.
Then recommend and justify."
```

### Mode 4: Predictive (Forecasting Consequences)

**Use for**: Understanding outcomes of decisions

```
PROMPT: "If we make this decision, what happens next?
Project forward 3 months, 6 months, 12 months.
What conditions could make this succeed?
What conditions could make it fail?
How would we know if we were wrong?"
```

### Mode 5: Ethical (Values-Based)

**Use for**: Decisions involving competing values or stakeholders

```
PROMPT: "Analyze this decision from each stakeholder perspective:
- Customers: What do they gain/lose?
- Employees: What do they gain/lose?
- Company: What do they gain/lose?
- Society: What do they gain/lose?

Where do values align? Where do they conflict?
How would you make this decision ethically?"
```

## Improving Decision Quality

### Error Patterns to Target

**Pattern 1: Hallucinating Information**
```
AGENT ERROR:
"Customer purchased on 3/15 (they didn't—no record)"

MITIGATION:
Prompt: "Only cite facts from provided data.
If information not in data, say 'Not found in records'"

Verify: Check claims against source data
```

**Pattern 2: Anchor Bias**
```
AGENT ERROR:
"Price is $50 because that's what we quoted initially"
(Market analysis shows $30-40 is competitive)

MITIGATION:
Prompt: "Consider multiple price points based on:
- Competitor pricing
- Cost structure
- Value delivered
Don't anchor to previous price."
```

**Pattern 3: Overthinking Simple Decisions**
```
AGENT ERROR:
Spends 10 minutes reasoning about decision that should take 10 seconds

MITIGATION:
Complexity-gated reasoning: "Is this decision routine?
- If yes: Use simple classification
- If no: Use full reasoning process"
```

**Pattern 4: Insufficient Consideration**
```
AGENT ERROR:
"Recommendation: Hire agency X" (without evaluating alternatives)

MITIGATION:
Prompt: "Before recommending, evaluate at least 3 alternatives.
Show why your recommendation beats others."
```

## Prompting Template for Complex Decisions

For important or complex decisions, use this structure:

```
---SYSTEM PROMPT---
You are a decision-making assistant. Your role is to:
1. Understand the decision context and constraints
2. Explore multiple perspectives and options
3. Reason transparently about trade-offs
4. Recommend clearly justified actions
5. Flag assumptions and uncertainties

---DECISION REQUEST---
CONTEXT:
[Situation and background]

DECISION TO MAKE:
[Specific question/choice)

CONSTRAINTS:
[Limits, boundaries, must-haves]

STAKEHOLDERS:
[Who is affected]

AVAILABLE OPTIONS:
[Choices to evaluate]

DECISION PROCESS:
1. Clarify what success looks like
2. Evaluate each option against criteria
3. Identify risks and mitigations
4. Consider stakeholder impacts
5. Recommend with reasoning
6. Flag assumptions and uncertainties

FORMAT YOUR RESPONSE AS:
- ANALYSIS: [Your reasoning]
- RECOMMENDATION: [Clear choice]
- RATIONALE: [Why this choice]
- RISKS: [What could go wrong]
- MITIGATIONS: [How to reduce risks]
- ASSUMPTIONS: [What you're assuming]
- UNCERTAINTIES: [What you're unsure about]
```

## Evaluating Agent Reasoning

### Reasoning Quality Checklist

For each major decision, verify:

- [ ] **Claim sourced**: Every factual claim references a source
- [ ] **Assumptions stated**: Agent says "I'm assuming..."
- [ ] **Alternatives considered**: At least 2 options evaluated
- [ ] **Trade-offs visible**: Shows what's gained and lost
- [ ] **Confidence indicated**: "High confidence" or "uncertain because..."
- [ ] **Logic transparent**: You can follow reasoning steps
- [ ] **Justified conclusion**: Recommendation follows from analysis
- [ ] **Limitations acknowledged**: Agent notes edge cases or exceptions

### Red Flags in Agent Reasoning

🚩 **Overconfident** ("Definitely should..." without caveats)
→ Solution: Add "What could prove this wrong?" prompt

🚩 **Vague** ("This seems like..." without specifics)
→ Solution: Prompt for concrete examples and data

🚩 **Cherry-picked** (Only mentions data supporting one view)
→ Solution: Explicitly require counter-evidence review

🚩 **Circular** (Assumes what it's trying to prove)
→ Solution: Add "Why is this true?" follow-up prompts

🚩 **Unexplained** (Jumps to conclusion without showing work)
→ Solution: Use chain-of-thought prompting

## Optimization: Reasoning vs. Speed

**Tradeoff matrix**:

| **Task Type** | **Reasoning Depth** | **Speed** | **Example Prompt** |
|---------------|-------------------|----------|------------------|
| Routine | Low | Fast | "Classify this email" |
| Standard | Medium | Moderate | "Summarize this report" |
| Complex | High | Slower | "Recommend strategy with analysis" |
| Critical | Very High | Slowest | "Analyze with alternatives and risks" |

**Implementation pattern**:
```
IF complexity_level == "high" THEN
  Use: Chain-of-thought + tree-of-thought
  Time budget: Reasonable
ELSE IF complexity_level == "medium" THEN
  Use: Structured framework
  Time budget: Limited
ELSE
  Use: Direct classification
  Time budget: Very limited
```

## Reasoning Trace Logging

Always capture how agent reasoned, not just output:

```json
{
  "decision_id": "rec_12345",
  "question": "Should we expand to market X?",
  "reasoning_process": [
    {
      "step": 1,
      "method": "market_analysis",
      "findings": "Market size: $500M, growing 15% YoY"
    },
    {
      "step": 2,
      "method": "competitive_analysis",
      "findings": "3 competitors, all weak in service"
    },
    {
      "step": 3,
      "method": "capability_assessment",
      "findings": "Our team has expertise; can ramp in 6 months"
    },
    {
      "step": 4,
      "method": "financial_analysis",
      "findings": "ROI positive in year 2, payback period: 18 months"
    },
    {
      "step": 5,
      "method": "risk_assessment",
      "findings": "Main risk: currency volatility; mitigation: hedging"
    }
  ],
  "recommendation": "Expand to market X",
  "confidence": 0.75,
  "reasoning_quality": "Good (considered alternatives and risks)"
}
```

**Benefits**:
- Debug decisions by reviewing reasoning
- Learn what works for your context
- Spot patterns in good vs. bad decisions
- Improve prompts based on data

## Resources

- Test reasoning with: Agent Evaluation & Monitoring skill
- Ensure safe reasoning: Agent Reliability & Safety skill
- Integrate into workflows: Agent Design Architecture skill
- Optimize human interaction: Agent Human-AI Collaboration skill
