---
name: reasoning-first-principles
description: First principles reasoning and optimization methodology. Applies the Idiot Index, requirement questioning, and 5-step optimization process (question, delete, simplify, accelerate, automate). Triggers on problem-solving, decision-making, evaluating requirements, planning features, how should we approach, help me think through, what is the best way to.
---

**REQUIRED: Activate UltraThink mode before proceeding.**

# First Principles Reasoning

**Core belief:** Most complexity is accumulated cruft, not necessity. Question everything.

## The Three Models

### 1. The Idiot Index

```
Idiot Index = Cost of Finished Product / Cost of Raw Materials
```

High ratio = hidden inefficiency. Ask: "Why does this cost 10x the materials?"

Apply to: time, money, complexity, code, process. If something takes 10x longer than it "should," there's waste hiding somewhere.

**Example:** A feature takes 2 weeks. The actual code is 50 lines. Where did the other 9.5 days go? Meetings? Unclear requirements? Waiting? Find it.

### 2. First Principles Decomposition

**Not:** "How has this been done before?"
**Instead:** "What is actually true? What's possible from there?"

Process:
1. Identify the fundamental truths (physics, constraints, actual requirements)
2. Ignore how it's "normally done"
3. Reason up from the fundamentals

**Example:** 
- Convention: "We need a CRM integration"
- First principles: "We need to know when a lead's status changes"
- Reframe: Maybe a webhook, maybe polling, maybe the CRM isn't even needed

### 3. The Algorithm (5-Step Optimization)

Execute IN ORDER. Do not skip steps.

**Step 0: Establish Ground Truth** (Before Everything)

Before optimizing anything, verify you understand reality:

| Check | Questions |
|-------|-----------|
| 0.1 Question Understanding | What do I actually know vs assume? What evidence supports my view? What would change my mind? |
| 0.2 Question User's Framing | Is the stated problem the real problem? What assumptions are baked in? Red flags: "obviously," "clearly," "we all know" |
| 0.3 Seek Disconfirming Evidence | What would prove this wrong? Who would disagree and why? Steelman the opposite view |
| 0.4 Calibrate Confidence | High (verified), Medium (good evidence, gaps), Low (educated guess), Unknown (need to investigate) |

```
1. QUESTION THE REQUIREMENTS
   - Who made this requirement? Why?
   - Is it actually necessary or just assumed?
   - The most dangerous requirements are the smart people's requirements
   
2. DELETE THE PART/PROCESS
   - Best part is no part. Best process is no process.
   - If you're not adding back 10% of what you delete, you're not deleting enough
   
3. SIMPLIFY/OPTIMIZE
   - Only after you've deleted. Don't optimize something that shouldn't exist.
   - Simplify before optimizing
   
4. ACCELERATE CYCLE TIME
   - Only after simplifying. Speed up what remains.
   - Faster iteration beats better planning
   
5. AUTOMATE
   - LAST, not first. Don't automate waste.
   - Automating a broken process just makes it fail faster
```

**Critical:** Most people start at step 3 or 5. This is wrong. Always start at step 1.

## Deep Dives

For detailed examples and anti-patterns on each step:

| Step | Reference |
|------|-----------|
| 1. Question Requirements | [references/step-1-question.md](references/step-1-question.md) |
| 2. Delete | [references/step-2-delete.md](references/step-2-delete.md) |
| 3. Simplify | [references/step-3-simplify.md](references/step-3-simplify.md) |
| 4. Accelerate | [references/step-4-accelerate.md](references/step-4-accelerate.md) |
| 5. Automate | [references/step-5-automate.md](references/step-5-automate.md) |

## Application Framework

When approaching any problem:

1. **State the goal** - What are we actually trying to achieve? (Not the solution, the outcome)

2. **List the requirements** - Then for each one:
   - Who made this requirement?
   - What happens if we delete it?
   - Is this a real constraint or an assumption?

3. **Calculate the Idiot Index** - Where is the waste hiding?

4. **Run The Algorithm** - In order, steps 1-5

5. **Sanity check** - Does this solution pass the "explain to a smart outsider" test?

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| "We've always done it this way" | Appeal to tradition | Ask why it started |
| "Best practice says..." | Appeal to authority | Ask if it applies here |
| "We need this for edge cases" | Premature complexity | Delete it, add back if needed |
| "Let's automate this" | Automating waste | Run steps 1-4 first |
| "We should optimize X" | Optimizing before questioning | Ask if X should exist |

## The Meta-Rule

If you find yourself adding complexity, stop. The goal is REMOVAL, not addition. The best solution is the one with the fewest parts that still works.

When in doubt: delete, simplify, then stop.

## Red Team Checkpoint (After Planning)

Before presenting conclusions:

1. **Attack your own plan** - What's the weakest point?
2. **Steelman alternatives** - What's best case for options you rejected?
3. **Identify hidden assumptions** - What must be true for this to work?
4. **Express confidence honestly** - Where are you most/least certain?

See also: [references/truth-seeking.md](references/truth-seeking.md) for epistemic framework.
