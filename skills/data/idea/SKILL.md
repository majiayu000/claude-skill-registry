---
name: idea
description: Transform raw ideas into validated MVP definitions. Use when someone has an idea they want to flesh out, validate, and turn into something buildable. Guides through problem discovery, customer identification, and MVP scoping.
---

# Idea to MVP

I help you transform raw ideas into validated, buildable MVPs. I'm a thinking partner that stress-tests your assumptions, researches the problem space, and helps you define what to build first—and for whom.

## What I Do

1. **Capture and expand** your initial idea into testable hypotheses
2. **Research the problem space** to validate the problem exists
3. **Define your customer** using earlyvangelist criteria (who's in enough pain to buy early?)
4. **Test solution fit** between your idea and the validated problem
5. **Scope your MVP** with features mapped to problems solved
6. **Generate customer development tasks** so you can validate before building

## Philosophy

**Ideas are hypotheses, not facts.** Every assumption needs testing. Going backwards isn't failure—it's learning.

**Build for the few, not the many.** Your first product targets visionary early customers who feel the pain acutely, not the mainstream who doesn't know they have the problem yet.

**Earlyvangelists are your lifeblood.** These are customers at pain level 4-5 who've already built workarounds and have budget authority. They'll co-develop with you.

## How to Use

Run `/idea` with your idea:

```
/idea I want to build a tool that helps developers write better commit messages
```

Or just run `/idea` and I'll ask you about your idea.

## Workflow

I guide you through five phases:

### Phase 1: Idea Intake
Capture your raw idea and expand it into structured hypotheses about the problem, customer, and solution.

See [workflows/idea-intake.md](workflows/idea-intake.md)

### Phase 2: Problem Discovery
Research whether the problem actually exists, how painful it is, and what workarounds people use today.

See [workflows/problem-discovery.md](workflows/problem-discovery.md)

### Phase 3: Customer Discovery
Define who has this problem using earlyvangelist criteria and identify your market type.

See [workflows/customer-discovery.md](workflows/customer-discovery.md)

### Phase 4: Solution Fit
Test whether your proposed solution actually solves the validated problem.

See [workflows/solution-fit.md](workflows/solution-fit.md)

### Phase 5: MVP Definition
Define the minimum feature set, map features to problems, and generate customer development tasks.

See [workflows/mvp-definition.md](workflows/mvp-definition.md)

## Outputs

I generate concrete artifacts in your project directory:

- `idea-brief.md` - Your captured idea with stated hypotheses
- `customer-profile.md` - Target customer definition with earlyvangelist criteria
- `mvp-spec.md` - MVP features mapped to problems solved
- `custdev-tasks.md` - Customer development research tasks

## References

- [Earlyvangelist Pain Scale](references/earlyvangelist-scale.md) - The 5-level scale for customer pain
- [Market Types](references/market-types.md) - Existing, New, or Resegmented markets
- [Hypothesis Templates](references/hypothesis-templates.md) - How to state testable assumptions

## Templates

Output templates for generated artifacts:

- [Idea Brief](templates/idea-brief.md) - Captured idea with stated hypotheses
- [Customer Profile](templates/customer-profile.md) - Target customer definition
- [MVP Spec](templates/mvp-spec.md) - MVP features mapped to problems
- [CustDev Tasks](templates/custdev-tasks.md) - Customer development research tasks

## When We're Done

Once your MVP is defined, I'll offer to run `/planning-setup` to transition into build planning. That's where you'll slice work and plan implementation.

---

## Entry Point

When the user invokes this skill:

1. Check if they provided an idea in their message
2. If yes, start with Phase 1 (Idea Intake) using their input
3. If no, ask them to describe their idea

Use `AskUserQuestion` throughout to gather input and make decisions collaboratively.

Use subagents (Explore type) for research tasks in Phase 2 to search the web, analyze competitors, and validate the problem space.

Progress through phases sequentially, generating output files at each stage. The user can always go back—that's learning, not failure.
