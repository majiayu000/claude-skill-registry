---
name: first-principles-thinking
description: "Break down problems to fundamental truths. Use when conventional solutions fail, you need innovation, or want to challenge assumptions. Not for standard problems with known solutions or minor optimizations."
---

# First Principles Thinking

Break down complex problems to their fundamental truths and rebuild from scratch. Strip away assumptions and existing solutions to find root causes and innovative approaches.

## Core Pattern

Apply first principles reasoning in four steps:

```
1. DEFINE → Problem Statement
2. STRIP → Assumptions
3. TRUTH → Fundamental Truths
4. REBUILD → Novel Solutions
```

## When to Use

Use this thinking methodology when:

- Stuck with conventional solutions that don't work
- Need to innovate beyond existing approaches
- Problem seems unsolvable with current methods
- Want to understand the root nature of a problem
- Challenging industry assumptions

**Recognition test:** "Would first principles help here?" If conventional approaches have failed, strip to fundamentals.

## Step-by-Step Process

### Step 1: Define the Problem

Clearly state what you're trying to solve:

```
**Problem Statement:**
[What is the core issue or challenge?]
```

**Example**: "How do we reduce the cost of space travel?"

### Step 2: Strip Assumptions

List all assumptions and existing "solutions":

```
**Current Assumptions:**
- [Assumption 1]
- [Assumption 2]
- [Existing solution 1]
- [Industry standard approach]
```

**Example**:

- Space travel requires rockets
- Rockets are expensive because they're single-use
- Fuel costs are the main expense
- We need NASA-level budgets

**Recognition**: What do we accept as "the way things are done" without questioning?

### Step 3: Find Fundamental Truths

Break down to what is fundamentally true (cannot be argued):

```
**Fundamental Truths:**
- [Truth 1] (physics law, constraint, etc.)
- [Truth 2]
- [Truth 3]
```

**Example**:

- Rockets are physics (action/reaction)
- Materials have mass
- Gravity exists
- We need to get payloads to orbit

**Recognition**: What remains when we strip away all conventions and assumptions?

### Step 4: Rebuild from Fundamentals

Create new solutions starting from fundamental truths only:

```
**Rebuilt Solutions:**
1. [Solution based on truth 1]
2. [Solution based on truth 2]
3. [Novel approach not constrained by assumptions]
```

**Example**: If rockets are physics, can we make them reusable? If materials have mass, can we use lighter materials? If we need orbit, can we refuel there?

**Recognition**: What solutions become possible when we ignore "how it's done"?

## Application Examples

### Example 1: Software Architecture

**Problem**: "Our monolith is too slow, how do we scale?"

**Assumptions**:

- Microservices are the answer
- Need to break everything into services
- Must use Kubernetes
- Need complex orchestration

**Fundamental Truths**:

- Code executes on CPUs
- Memory is finite
- Network has latency
- Some operations depend on others

**Rebuilt Solutions**:

- Identify actual bottleneck (is it CPU, memory, or I/O?)
- Can we optimize the slow parts without splitting everything?
- Maybe we need modular monolith, not microservices
- Perhaps we just need better caching

### Example 2: Product Feature

**Problem**: "Users aren't using our reporting feature"

**Assumptions**:

- Need more features in reports
- Need better UI
- Users don't understand how to use it
- Need tutorials

**Fundamental Truths**:

- Users act on what provides value
- Time is limited
- Reports serve decision-making
- Different users need different information

**Rebuilt Solutions**:

- What decisions do users actually make?
- Do we have the RIGHT data, not just MORE data?
- Maybe reports should be actionable, not informational
- Perhaps we need dashboards, not traditional reports

### Example 3: Team Process

**Problem**: "Sprint planning takes too long"

**Assumptions**:

- Need 2-week sprints
- Must estimate every story
- Planning poker is required
- Full team must be present

**Fundamental Truths**:

- Teams need shared understanding
- Some coordination is necessary
- Uncertainty exists in estimates
- Time is valuable

**Rebuilt Solutions**:

- Do we need sprints at all? (continuous delivery?)
- Can we estimate only larger items?
- Maybe planning should be just-in-time, not batched
- Perhaps only relevant people attend

## Output Format

After analysis, produce structured output:

```markdown
# First Principles Analysis: [Problem]

## Problem Statement

[What we're trying to solve]

## Assumptions Identified

- [Assumption 1] - [why this might be wrong]
- [Assumption 2] - [why this might be wrong]

## Fundamental Truths

1. [Truth that cannot be broken down further]
2. [Another fundamental truth]
3. [Another fundamental truth]

## Rebuilt Solutions

1. [Novel solution based on truth 1]
2. [Alternative approach based on truth 2]
3. [Non-obvious insight from rebuilding]

## Key Insight

[The most important realization from this analysis]

## Next Steps

1. [Action to explore solution 1]
2. [Experiment to test assumption]
```

## Recognition Questions

**Before applying**:

- "Am I starting from existing solutions or fundamental truths?"
- "Which of my 'facts' are actually assumptions?"

**During analysis**:

- "Can this be broken down further?"
- "Is this true by definition or just conventional wisdom?"

**After rebuilding**:

- "Does this solution challenge conventional approaches?"
- "Is this truly novel or just a variation of existing solutions?"

## Common Mistakes

**❌ Wrong**: Stopping at "best practices" instead of going deeper
**✅ Correct**: Question why best practices are best

**❌ Wrong**: Accepting industry constraints as fundamental truths
**✅ Correct**: Distinguish between real constraints and self-imposed ones

**❌ Wrong**: Rebuilding with the same assumptions in different words
**✅ Correct**: Start only from what is provably true

## Key Innovation

First principles thinking bypasses conventional thinking to find innovative solutions that aren't constrained by existing approaches.

**The breakthrough**: When you strip away assumptions, solutions emerge that were invisible when constrained by "how things are done."

**Trust intelligence** - First principles thinking is cognitively expensive but yields insights that assumption-based thinking cannot.

---

<critical_constraint>
MANDATORY: Challenge all assumptions, not just surface ones
MANDATORY: Identify fundamental truths before rebuilding solutions
MANDATORY: Rebuild from truths, not from modified assumptions
MANDATORY: Document assumptions and why they may be wrong
No exceptions. First principles requires going deeper than conventions.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
