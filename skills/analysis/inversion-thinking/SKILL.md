---
name: inversion-thinking
description: "Solve problems by thinking backwards. Use when forward thinking is stuck, you need to identify risks, or find non-obvious solutions. Not for straightforward implementation tasks or simple bug fixes."
---

# Inversion Thinking

Solve problems by working backwards - think about what guarantees failure, then avoid those things.

## Core Pattern

Apply inversion by:

1. Inverting the problem - think about the opposite
2. Listing what would guarantee failure
3. Inverting those failures to find success
4. Identifying what to avoid, not just what to do

**Key Innovation**: Finding non-obvious solutions by approaching from the opposite direction. Often easier to agree on what causes failure than what causes success.

## When to Use

Use this approach when:

- Forward thinking isn't yielding solutions
- Want to identify risks and failure modes
- Consensus on "what to do" is difficult
- Problem seems too complex to solve directly
- Want to find non-obvious approaches

**Recognition test:** "Is forward thinking stuck?" If solutions aren't emerging, invert the problem.

## The Inversion Process

### Step 1: State the original goal

```
Original Goal: [What you want to achieve]
```

### Step 2: Invert the problem

```
Inverted Problem: How do I guarantee FAILURE?
```

### Step 3: List failure modes

```
Failure Modes:
1. [What would definitely cause failure]
2. [Another guaranteed way to fail]
3. [Third way to ensure failure]
```

### Step 4: Invert failures to find success

```
Success Strategies:
1. [Avoid failure mode 1] → [Success strategy]
2. [Avoid failure mode 2] → [Success strategy]
3. [Avoid failure mode 3] → [Success strategy]
```

## Two Types of Inversion

### Type 1: Avoid Stupidity

Instead of trying to be brilliant, avoid being stupid:

- What would make this definitely fail?
- Don't do those things

### Type 2: Reverse the Problem

Think about the opposite of what you want:

- How do I make users hate this product?
- Reverse those to make users love it

## Application Examples

### Example 1: Product Design

**Original Goal**: How do we create a great user onboarding experience?

**Inverted**: How do we make users hate our onboarding?

**Failure Modes**:

1. Make them read 10 pages of text
2. Ask for 20 pieces of information upfront
3. Don't show them any value for 15 minutes
4. Force them through a tutorial they can't skip
5. Make them create an account before trying anything

**Success Strategies (Inverted)**:

1. Make onboarding visual and interactive, not text-heavy
2. Ask for minimal info, collect more as needed
3. Show value within 30 seconds
4. Make tutorial skippable or just-in-time
5. Let users try before signing up

### Example 2: Project Management

**Original Goal**: How do we deliver projects on time?

**Inverted**: How do we guarantee late delivery?

**Failure Modes**:

1. Start without clear requirements
2. Add features throughout the project
3. Ignore technical debt until the end
4. Don't communicate about delays
5. Set unrealistic deadlines based on optimism

**Success Strategies (Inverted)**:

1. Never start without clear, signed-off requirements
2. Freeze scope after planning, any changes go through change request
3. Allocate time for technical debt in every sprint
4. Communicate delays immediately, not at deadline
5. Set deadlines based on historical velocity, not optimism

### Example 3: System Reliability

**Original Goal**: How do we make our system reliable?

**Inverted**: How do we guarantee system failures?

**Failure Modes**:

1. Have single points of failure everywhere
2. Don't monitor anything
3. Make every component dependent on every other
4. Never test failover scenarios
5. Push all changes directly to production

**Success Strategies (Inverted)**:

1. Eliminate single points of failure, add redundancy
2. Monitor everything, set up alerts
3. Decouple components, use async communication
4. Regularly test failure scenarios (chaos engineering)
5. Use staging environments and canary deployments

### Example 4: Team Culture

**Original Goal**: How do we build a great team culture?

**Inverted**: How do we make talented people quit?

**Failure Modes**:

1. Micromanage every decision
2. Take credit for their work
3. Provide no growth opportunities
4. Never give feedback until performance review
5. Make them work on things they hate

**Success Strategies (Inverted)**:

1. Give autonomy, trust decisions to experts
2. Publicly credit team members for their work
3. Provide growth opportunities and learning budget
4. Give regular, constructive feedback
5. Align work with interests when possible

## Output Format

After analysis, produce structured output:

```markdown
# Inversion Analysis: [Goal]

## Original Goal

[What you want to achieve]

## Inverted Problem

[How to guarantee the opposite - failure]

## Guaranteed Failure Strategies

1. [Strategy that would cause failure]
2. [Another way to ensure failure]
3. [Third way to guarantee failure]

## Success Strategies (Inverted)

1. **Avoid [failure 1]**
   → [Success strategy derived from avoiding failure]

2. **Avoid [failure 2]**
   → [Success strategy derived from avoiding failure]

3. **Avoid [failure 3]**
   → [Success strategy derived from avoiding failure]

## Key Insights

- [Non-obvious insight from backward thinking]
- [Another insight]

## Immediate Actions

1. [First action based on inverted strategy]
2. [Second action]
```

## Recognition Questions

**Before inversion**:

- "What would I agree is definitely a bad idea?"
- "What would everyone agree causes failure?"

**During inversion**:

- "Is this failure mode genuine or contrived?"
- "Can I actually avoid this failure mode?"

**After inversion**:

- "Are these strategies more actionable than forward-thinking solutions?"
- "Did I discover anything non-obvious?"

## Common Mistakes

**❌ Wrong**: Inversion that's just the opposite of good ideas (not genuine failure modes)
**✅ Correct**: Think about genuine, realistic ways to fail

**❌ Wrong**: Inverting failures that don't actually happen
**✅ Correct**: Focus on realistic failure modes from experience

**❌ Wrong**: Using inversion alone without forward thinking
**✅ Correct**: Combine inversion with forward thinking for complete picture

## Why Inversion Works

**Easier to agree on failure**: People often disagree on "best" approach but agree on "worst" approach

**Uncovers hidden assumptions**: Thinking about failures reveals risks that forward thinking misses

**Less cognitive bias**: Forward thinking is prone to optimism bias; inversion is naturally skeptical

**Complete perspective**: Combining forward and backward thinking gives fuller picture

## Quotes on Inversion

"Invert, always invert." - Carl Jacobi (mathematician)

"Tell me where I'm going to die so I never go there." - Charlie Munger

"It is remarkable how much long-term advantage people like us have gotten by trying to be consistently not stupid, instead of trying to be very intelligent." - Charlie Munger

**Trust intelligence** - Inversion is powerful because failure is often more obvious than success. Start with what you know doesn't work.

---

<critical_constraint>
MANDATORY: Identify genuine failure modes (not just opposites of good ideas)
MANDATORY: Focus on realistic, actionable failure modes from experience
MANDATORY: Combine inversion with forward thinking for complete analysis
MANDATORY: Derive actionable strategies from avoiding each failure
No exceptions. Inversion without genuine failure modes is wasted effort.
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
