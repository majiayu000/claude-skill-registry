---
name: stress-testing
description: Stress-test plans, proposals, and strategies. Use for pre-mortems, assumption audits, risk registers, evaluating business ideas, identifying failure modes, or when you need devil's advocate analysis before committing resources.
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebFetch
  - WebSearch
---

# Stress Testing

Finding the flaws before they find you.

## When to Use

- Before committing engineering time
- Before choosing a roadmap direction
- Before betting on an architecture
- When evaluating a business proposal
- When something "feels risky" but you can't articulate why

## Process

1. **Summarize the plan** - Neutral wording, 2-4 bullets
2. **Extract assumptions** - What must be true for this to work?
3. **Run pre-mortem** - Imagine failure, work backward
4. **Build risk register** - Likelihood, impact, mitigation
5. **Define kill criteria** - When should we stop?
6. **Propose experiments** - Cheap ways to validate

## Output Contract

Structure every stress-test as:

```markdown
## Plan Summary
[2-4 bullets, neutral wording]

## Must-Be-True Assumptions
| Assumption | How to Verify | Fastest Disproof |
|------------|---------------|------------------|
| ... | ... | ... |

## Pre-Mortem: It's 1 Year Later, This Failed
| Failure Mode | Warning Signal | Prevention |
|--------------|----------------|------------|
| ... | ... | ... |

## Risk Register
| Risk | Likelihood | Impact | Mitigation | Fallback |
|------|------------|--------|------------|----------|
| ... | H/M/L | H/M/L | ... | ... |

## Kill Criteria
- [ ] [Condition that should stop this plan]
- [ ] [Another stop condition]

## Experiments to Run
- [ ] [Cheap test] - Success metric: [...]
- [ ] [Another test] - Success metric: [...]
```

## Fundamental Questions

### For Any Idea
- What would have to be true for this to work?
- What are we assuming that we haven't validated?
- What's the weakest link in this chain?
- If this fails, what's the most likely cause?
- Who has tried this before, and what happened?

### For Claims
- What's the evidence?
- Is the source credible and disinterested?
- What would change my mind?
- What's the null hypothesis?
- Am I being told what I want to hear?

### For Plans
- What's the first thing that will go wrong?
- What dependencies are we not seeing?
- What happens if it takes 2x longer or costs 2x more?
- Who's accountable if this fails?
- What's the rollback plan?

## Pre-Mortem Technique

### The Method
Imagine it's one year from now. The project has failed spectacularly. Now:
1. What went wrong?
2. What were the warning signs we ignored?
3. What did we assume that turned out to be false?
4. What did we not plan for?
5. Who saw this coming and wasn't heard?

### Why It Works
- Gives permission to voice concerns
- Overcomes optimism bias
- Surfaces hidden risks
- Generates specific failure modes
- Removes social pressure to be positive

### Questions to Ask
- "What's the most likely way this fails?"
- "What's the most catastrophic way this fails?"
- "What assumption, if wrong, kills this?"
- "What's the thing we're not talking about?"

## Common Failure Patterns

### Planning Fallacies
- **Optimism bias**: Best case becomes the plan
- **Anchoring**: First estimate becomes the baseline
- **Conjunction fallacy**: Plan requires everything to go right
- **Survivorship bias**: We only see what succeeded

**Ask:** What if every step takes 50% longer? What if three things go wrong simultaneously?

### Assumption Traps
- **Untested assumptions**: "Users will love this"
- **Implicit assumptions**: Things so obvious no one states them
- **Stale assumptions**: True once, maybe not now
- **Borrowed assumptions**: "That's how [BigCo] does it"

**Ask:** Can we list every assumption? Which have we actually validated?

### Complexity Blindness
- **Hidden dependencies**: A needs B needs C needs...
- **Integration risk**: Parts work, whole doesn't
- **Second-order effects**: Solving X creates Y
- **Coordination costs**: More people ≠ faster

**Ask:** What's the real dependency graph? What happens at the interfaces?

### Market Delusions
- **"Build it and they will come"**: They won't
- **"We just need 1% of the market"**: That 1% is fought over fiercely
- **"No competition"**: Either you're wrong or there's no market
- **"First mover advantage"**: Often means first to make mistakes

**Ask:** Who specifically will buy this? Why haven't they bought the alternatives?

## Red Flags

### In Communication
- "Trust me on this"
- "It's obvious that..."
- "Everyone knows..."
- "There's no downside"
- "This can't fail"
- "We'll figure it out later"
- Confident timelines for unprecedented work

### In Planning
- No contingency budget (time or money)
- Single points of failure
- Success requires perfect execution
- No one is explicitly responsible
- Risks acknowledged but not mitigated
- "We'll move fast and iterate"

### In Reasoning
- Confirming evidence only
- Dismissing counterexamples
- Moving goalposts
- Circular logic
- Appeal to authority without substance
- "It worked at [other company]"

### In Teams
- No one plays devil's advocate
- Dissent is discouraged
- The loudest voice wins
- Sunk cost driving decisions
- Groupthink in action
- "We've always done it this way"

## Stress Tests

### The 10x Test
- What if usage is 10x what we expect?
- What if it takes 10x longer?
- What if it costs 10x more?
- What if we have 1/10 the resources?

### The Adversary Test
- What would a competitor do to beat this?
- What would a malicious actor exploit?
- What would a hostile regulator target?
- What would a disgruntled user complain about?

### The Scalability Test
- Does this work with 10 users? 1000? 1M?
- Does this work with 1 person? 10? 100?
- Does this work in 1 market? 10? 50?
- What breaks first at scale?

### The Time Test
- Will this still make sense in 6 months?
- What changes in the environment could invalidate this?
- Are we building for now or for then?
- What's the shelf life of this decision?

### The Dependency Test
- What external factors must remain true?
- What happens if [key partner] disappears?
- What happens if [key person] leaves?
- What happens if [key assumption] changes?

## Constructive Skepticism

### How to Challenge Without Crushing
- "Help me understand..."
- "What if we're wrong about..."
- "I want to stress-test this assumption..."
- "Let's imagine this fails—why did it fail?"
- "What would the skeptic in the room ask?"

### Pairing Problems with Possibilities
- "This seems risky because X. Could we mitigate by Y?"
- "I'm worried about A. Have we considered B?"
- "This fails if C. What's our plan for C?"

### Knowing When to Stop
- Don't block, flag
- Skepticism serves the decision, not itself
- Once risks are surfaced and considered, step back
- "I've raised my concerns; I'll support whatever we decide"

## Biases to Watch

### In Others
- **Confirmation bias**: Seeking only supporting evidence
- **Sunk cost fallacy**: Continuing because of past investment
- **Availability heuristic**: Overweighting recent or vivid examples
- **Authority bias**: Believing because of who said it
- **Bandwagon effect**: Believing because others do

### In Yourself
- **Contrarian bias**: Disagreeing for its own sake
- **Status quo bias**: Favoring inaction
- **Pessimism bias**: Overweighting negative outcomes
- **Negativity bias**: Remembering failures more than successes
- **Cynicism**: Assuming bad faith

### The Antidote
- "What would change my mind?"
- "Am I being skeptical or just negative?"
- "Is this a real risk or a rationalized fear?"
- "Have I given this idea a fair hearing?"

## Decision Points

### When to Kill an Idea
- Core assumption is invalidated
- Risk/reward is unfavorable
- Better alternatives exist
- Resources are better spent elsewhere
- The team doesn't believe in it

### When to Proceed Despite Concerns
- Risks are known and accepted
- Mitigations are in place
- Upside justifies downside
- We'll learn something valuable either way
- Not deciding is worse than deciding

### When to Investigate More
- Key assumptions are untested
- Risks are unclear
- We're missing information
- Expert opinion is divided
- Stakes are high

## The Skeptic's Toolkit

### Questions
- "What's the evidence?"
- "What are we assuming?"
- "What could go wrong?"
- "Who disagrees, and why?"
- "What would change our mind?"

### Techniques
- Pre-mortem analysis
- Red team exercises
- Assumption mapping
- Risk registers
- Devil's advocate role

### Outputs
- List of assumptions (tested/untested)
- Risk register with severity and likelihood
- Failure modes and mitigations
- Questions that need answers
- Conditions that would change the decision

## The Balance

### Skepticism Needs a Counterweight
- Dreaming without skepticism is fantasy
- Skepticism without dreaming is paralysis
- The goal is not to kill ideas but to strengthen them
- Some ideas should survive scrutiny

### When to Switch Modes
- **Dreaming phase**: Suspend skepticism, expand possibilities
- **Evaluation phase**: Apply skepticism, test rigorously
- **Execution phase**: Skepticism becomes risk management
- Know which phase you're in

### The Ultimate Test
A good skeptic asks:
- "Is this idea stronger for having been challenged?"
- "Are the remaining risks acceptable?"
- "Would a reasonable person proceed?"

If yes, the skeptic's job is done.

## Mantras

- "What am I not seeing?"
- "Hope is not a strategy"
- "The market doesn't care about your intentions"
- "Reality is not optional"
- "Better to find the flaw than have it find you"
- "Strong opinions, loosely held"
- "Doubt is not disloyalty"
- "The goal is truth, not comfort"
