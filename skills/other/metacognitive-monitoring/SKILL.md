---
name: metacognitive-monitoring
description: Active supervision of the problem-solving process. Covers Schoenfeld's control layer, Ann Brown's self-regulation moves, planning-monitoring-evaluating cycle, time budgeting, strategy switching, and the "what am I doing and why?" check. Use continuously alongside any solving activity to avoid wandering, dead ends, and unproductive grinding.
type: skill
category: problem-solving
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/problem-solving/metacognitive-monitoring/SKILL.md
superseded_by: null
---
# Metacognitive Monitoring

Metacognition is thinking about your thinking. In problem solving, it is the supervisor process that interrupts execution to ask: "Am I still on the right track? Is my current activity the best use of this moment? Do I need to reconsider?" Schoenfeld's research on mathematical problem solving shows that novices who grind for 20 minutes on a dead end outperform instantly when taught to pause every 2-3 minutes and check. This skill is the catalog of the checks.

**Agent affinity:** brown-ps (self-regulation, reciprocal teaching), schoenfeld (control layer), polya-ps (review phase)

**Concept IDs:** prob-problem-representation, prob-adaptive-management, prob-uncertainty-management, prob-trial-error-iteration

## The Planning-Monitoring-Evaluating Cycle

Metacognition decomposes into three phases:

1. **Planning:** Before solving, decide what to do.
2. **Monitoring:** During solving, check that you are doing it.
3. **Evaluating:** After solving, decide what worked.

These run nested inside problem solving, not alongside it.

## Planning Operations

**Goal:** Set the meta-level frame for the solving session.

**Operations:**

- **Goal clarification.** What am I actually trying to accomplish in this session?
- **Strategy selection.** Which approach will I try first?
- **Resource allocation.** How much time, what tools, what help?
- **Budget.** How long will I give this strategy before switching?
- **Fallback.** What is my plan B if the first strategy fails?
- **Success criterion.** How will I know when I have succeeded?

A solver who starts without a plan is already in a dead end.

## Monitoring Operations

**Goal:** Continuously check that the current activity is the right activity.

**The core check — every 2-5 minutes, ask:**

1. **What am I doing right now?**
2. **Why am I doing it? (Does it serve the goal?)**
3. **Is it working?**
4. **Should I continue, adjust, or switch?**

If any of the four questions produces "I don't know," stop and figure it out before continuing.

**Progress indicators:**

- **Am I closer to the goal than 5 minutes ago?**
- **Have I learned something new about the problem?**
- **Am I generating usable intermediate results?**

If all three are no, you are grinding.

**Stall indicators:**

- **Repeating the same move in different clothing.**
- **Checking the problem statement again but not the strategy.**
- **Getting more confused rather than less.**

When stall indicators appear, switch strategies or escalate (ask for help, consult a resource, take a break).

## Evaluating Operations

**Goal:** After solving, extract the lesson.

**Operations:**

- **Did I solve the problem I was asked?** (Not a different one.)
- **Is the solution correct?** (Verify, do not assume.)
- **What method worked?**
- **What did not work, and why?**
- **What would I do differently next time?**
- **What general lesson transfers to other problems?**

Evaluation is what converts a one-time win into a transferable skill.

## Ann Brown's Self-Regulation Moves

Ann Brown's work on reciprocal teaching identified four metacognitive moves that learners can be explicitly taught:

1. **Predict.** Before reading or solving, predict what is coming.
2. **Clarify.** When confused, stop and name what is confusing.
3. **Question.** Ask your own questions about the material.
4. **Summarize.** In your own words, what did I just do?

These move problem solving from passive to active, and from implicit to inspectable.

## Schoenfeld's Control Timeline

Schoenfeld videotaped experts and novices solving the same math problem and analyzed their use of time. Typical results:

**Novice:**
- Read the problem: 30 seconds
- Pick a strategy (first one that came to mind): 10 seconds
- Execute: 18 minutes
- Check: 30 seconds

**Expert:**
- Read the problem carefully: 2 minutes
- Think about strategy, consider two or three: 3 minutes
- Execute with periodic check: 10 minutes
- Check the result: 5 minutes

The expert spends less total time (20 vs 19 minutes) but allocates differently. The novice's 18 minutes of execution include 15 minutes of wandering on the first strategy. Explicit control would have saved most of it.

## Time Budgeting

**Rule of thumb:**

- **Planning:** 10-20% of total time
- **Executing:** 50-60% of total time
- **Monitoring check-ins:** every 2-5 minutes, 30 seconds each
- **Evaluating:** 10-20% of total time

If execution is eating 90% of the budget, metacognition has failed.

## Strategy Switching

**When to switch:**

- **Budget exceeded.** The time budget for the first strategy is up with no progress.
- **Loop detected.** You are doing the same thing repeatedly with no new information.
- **Rising confusion.** More confused than 5 minutes ago.
- **Dead end.** The path leads nowhere usable.

**How to switch:**

1. **Stop.** Do not continue grinding.
2. **Summarize what you learned.** Even a failed attempt produces information.
3. **Return to planning.** What is the next best strategy given what you now know?
4. **Budget the new strategy.** Time limit again.
5. **Execute.**

## Worked Example — A Stalled Solver

A student is solving an integral by substitution. They have tried two substitutions, neither of which simplifies the integrand. They have spent 12 minutes.

**Monitoring check:**

1. What am I doing? "Trying substitutions on this integral."
2. Why? "Because substitution usually works for integrals of this form."
3. Is it working? "No, the substitutions are not simplifying."
4. Should I continue, adjust, or switch? **Switch.**

**Strategy switch:**

1. Summarize learning: "Substitution is not working. The integrand has a product of functions, not a composition. Substitution is for compositions."
2. Return to planning. "Integration by parts is for products. Try that."
3. Budget: "5 more minutes before reconsidering."
4. Execute integration by parts. Works within 3 minutes.

Without the metacognitive check, the student would have tried a third substitution and wasted another 5 minutes.

## When Metacognitive Monitoring Fails

- **Never turning it on.** Grinding forever.
- **Turning it on but ignoring the results.** "I know I'm stuck but I'll just try one more thing."
- **Over-monitoring.** Checking every 30 seconds breaks flow without benefit.
- **No strategy to switch to.** Monitoring that detects a dead end but has no fallback is useless.
- **Post-hoc only.** Evaluation without in-session monitoring misses the opportunity to correct.

## Cross-References

- **problem-comprehension** produces the representation that monitoring checks progress against
- **strategy-selection** provides the menu of fallback strategies
- **mathematical-problem-solving** is where Schoenfeld's control layer originated
- **design-thinking-ps** monitors by asking "what did the last prototype teach us?"
- **collaborative-problem-solving** distributes monitoring across team members (usually the facilitator)
