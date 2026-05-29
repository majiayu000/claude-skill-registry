---
name: simplification-principles
description: "Apply simplification principles (Occam's Razor) when debugging complex issues, evaluating competing theories, or simplifying designs. Not for ignoring necessary complexity or oversimplifying."
---

# Simplification Principles

Find the simplest explanation that accounts for all the facts. Among competing hypotheses, prefer the one with the fewest assumptions.

## Core Pattern

Apply Occam's Razor by:

1. Identifying the problem or phenomenon to explain
2. Listing all possible explanations
3. Counting assumptions required for each explanation
4. Preferring the explanation with the fewest assumptions
5. Verifying the simple explanation actually explains everything

**Key Innovation**: Avoid overcomplicating problems. Simple explanations are more likely to be correct and more likely to be actionable.

## When to Use

Use this principle when:

- Debugging complex issues
- Diagnosing problems
- Evaluating competing theories
- Designing solutions
- Analyzing user behavior

**Recognition test:** "Are there multiple explanations?" If yes, find the simplest one that fits all facts.

## The Principle

"Entities should not be multiplied without necessity."

**In simpler terms**: The simplest explanation that fits all the facts is probably the right one.

## Step-by-Step Process

### Step 1: List all facts

```
**Known Facts:**
1. [Observable fact 1]
2. [Observable fact 2]
3. [Observable fact 3]
```

### Step 2: Generate explanations

```
**Explanation A**: [Description]
Assumptions: [List assumptions]

**Explanation B**: [Description]
Assumptions: [List assumptions]

**Explanation C**: [Description]
Assumptions: [List assumptions]
```

### Step 3: Count assumptions

- Fewer assumptions = more likely to be correct

### Step 4: Verify the simple explanation

- Does it actually explain all the facts?
- Any contradictions or gaps?

### Step 5: Choose the simplest sufficient explanation

## Application Examples

### Example 1: Debugging

**Facts**:

1. API returns 500 error
2. Error occurs only for requests with > 100 items
3. Error started after recent deployment
4. No other endpoints are affected

**Explanations**:

_A) Complex conspiracy_:

- Database was compromised
- Hacker is targeting large requests specifically
- Security team knows and hasn't told us
  Assumptions: 4 (very unlikely)

_B) Configuration issue_:

- Request size limit was lowered in recent deployment
- Large requests exceed new limit
- Error handler returns 500 for size limit
  Assumptions: 3 (possible)

_C) Simple bug_:

- Recent deployment added code that crashes on large arrays
- The bug is in the endpoint handler only
- No other endpoints have this code path
  Assumptions: 2 (most likely)

**Winner**: Explanation C - Simple bug in recent deployment

**Action**: Review recent code changes to the endpoint, look for array operations.

### Example 2: User Behavior

**Facts**:

1. Users are abandoning checkout at payment step
2. Abandonment rate increased last week
3. No UI changes were made
4. Competitors haven't changed pricing

**Explanations**:

_A) Market shift_:

- Economy changed last week
- Users suddenly can't afford products
- This affects only checkout step
  Assumptions: 4 (unconvincing)

_B) Technical issue_:

- Payment provider had outage last week
- Some users experienced errors
- They're now hesitant to complete payment
  Assumptions: 3 (possible)

_C) Simple change_:

- Payment processing time increased last week
- Users think it's broken and leave
- Nothing else changed
  Assumptions: 2 (most likely)

**Winner**: Explanation C - Payment got slower

**Action**: Check payment provider logs for processing time changes.

### Example 3: System Design

**Problem**: We need to send notifications to users

**Explanations**:

_A) Build notification microservice with queue, workers, retry logic, multiple channels, templates, preferences, scheduling, analytics_:

- Complex architecture
- Multiple systems to build and maintain
- Many moving parts
  Assumptions: Many (complexity for its own sake)

_B) Use existing email service, add simple notification table_:

- Single database table
- Simple cron job to send
- Email service handles delivery
  Assumptions: Few (sufficient for current needs)

**Winner**: Explanation B - Simple solution

**Action**: Start simple, add complexity only when needed.

## Output Format

After analysis, produce structured output:

```markdown
# Occam's Razor Analysis: [Problem]

## Known Facts

1. [Observable fact 1]
2. [Observable fact 2]
3. [Observable fact 3]

## Possible Explanations

### Explanation A: [Name]

**Description**: [What this explanation proposes]
**Assumptions** (count: N):

- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

### Explanation B: [Name]

**Description**: [What this explanation proposes]
**Assumptions** (count: M):

- [Assumption 1]
- [Assumption 2]

### Explanation C: [Name]

**Description**: [What this explanation proposes]
**Assumptions** (count: P):

- [Assumption 1]

## Simplest Explanation

**[Winning explanation]** - [X assumptions]

**Why it's simplest**: [Fewest assumptions, most direct]

**Verification**:

- ✓ Explains fact 1
- ✓ Explains fact 2
- ✓ Explains fact 3

## Recommended Action

[What to do based on this explanation]

## Confidence

[High/Medium/Low] - [Reason for confidence level]
```

## Recognition Questions

**Before applying**:

- "What are the observable facts?"
- "Am I distinguishing facts from assumptions?"

**During analysis**:

- "How many assumptions does this explanation require?"
- "Is there evidence for each assumption?"

**After choosing**:

- "Does this actually explain ALL the facts?"
- "Am I choosing simple because it's easy or because it's correct?"

## Common Mistakes

**❌ Wrong**: Choosing the simplest explanation that doesn't actually explain everything
**✅ Correct**: Simplest explanation that accounts for ALL facts

**❌ Wrong**: Ignoring evidence to fit a simple explanation
**✅ Correct**: If evidence doesn't fit, explanation is wrong (no matter how simple)

**❌ Wrong**: Using Occam's Razor to avoid necessary complexity
**✅ Correct**: Some problems are inherently complex - don't oversimplify

**❌ Wrong**: Counting assumptions incorrectly (grouping many assumptions into one)
**✅ Correct**: Each independent assumption counts separately

## When NOT to Use

Don't use this principle when:

- You have clear evidence of complex causes
- The simple explanation leaves important facts unexplained
- Time horizons are long (complex systems emerge over time)
- Human behavior is involved (often irrational, not simple)

## Related Principles

**Hanlon's Razor**: Never attribute to malice what can be explained by stupidity (or error)

**Hume's Razor**: Explanation must be based on evidence, not speculation

**Popper's Falsifiability**: Explanations must be testable

**Pareto Principle**: 80% of effects come from 20% of causes (related simplicity)

## Quotes

"Simplicity is the ultimate sophistication." - Leonardo da Vinci

"Everything should be made as simple as possible, but not simpler." - Albert Einstein

"If you can't explain it simply, you don't understand it well enough." - Albert Einstein

**Trust intelligence** - Occam's Razor is a heuristic, not a law. Simple explanations are usually right, but not always. Verify before committing.

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

<critical_constraint>
MANDATORY: Verify simple explanation actually explains ALL facts
MANDATORY: Count assumptions explicitly for each explanation
MANDATORY: Don't oversimplify when complexity is necessary
MANDATORY: Each independent assumption counts separately
No exceptions. The simplest explanation must account for all evidence.
</critical_constraint>
