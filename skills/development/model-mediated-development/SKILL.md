---
name: model-mediated-development
description: Use when building any system that involves AI/model calls - integrates with brainstorming, planning, and TDD to ensure model agency over hardcoded rules
---

# Model-Mediated Development

## Overview

**Model decides. Code provides inputs and executes.** This skill is a thinking lens that applies DURING other workflows, not a replacement for them.

**Core question throughout:** "What decisions exist, and who should make each?"

## Integration with Development Workflows

This skill runs ALONGSIDE other skills:

| Phase | Use With | Model-Mediated Lens |
|-------|----------|---------------------|
| Design | brainstorming | Identify decisions, propose who makes each |
| Planning | writing-plans | Distinguish pipes from decision layers |
| Implementation | TDD | TDD for pipes, but no decision logic in code |
| Verification | verification | Check for leaked heuristics |

Works with both Claude Code (superpowers) and Codex (bootstrappers).

## During Design/Brainstorming

When designing any system that might involve model calls, explore:

**Suggest possibilities:**
- "This could be model-mediated - the model could decide X based on Y"
- "What if we gave the model tools for Z and let it figure out timing?"
- "Here's a tool interface that would give the model control..."

**Ask yourself and the user:**
- "What decisions exist in this system?"
- "For each decision: should it be user-controlled, model-controlled, or hardcoded?"
- "This could go either way - do you want explicit control or model judgment?"

**Surface considerations:**
- "If the model decides this, here's what it would need..."
- "If we hardcode this, we lose flexibility for..."
- "This feels like a decision - should we discuss who makes it?"

**Not everything needs model-mediation.** A CLI that takes explicit user input and calls an API is a dumb pipe. That's fine. The question is whether there are DECISIONS being made, and if so, by whom.

## During Planning

When writing implementation plans, distinguish:

**Dumb pipes (code):**
- Fetch data, transform formats, call APIs
- Execute tool calls from model
- Provide factual inputs (time, state, history)
- Health checks, audit trails

**Decision layers (model):**
- What action to take
- When to take it
- What context to request
- How to interpret ambiguous intent

**The plan should make clear:** "Component X is a pipe - TDD applies. Component Y is a decision layer - model controls via tools."

## During Implementation (TDD)

TDD applies to pipes. Write tests for:
- Data fetching works correctly
- Tool execution is reliable
- Inputs are gathered accurately
- Error handling is robust

**But continuously ask:**
- "Am I about to write an IF that decides behavior? Stop - that's model logic."
- "Am I pre-gathering context? Should model request this instead?"
- "Am I adding a threshold/rule? Why isn't the model deciding this?"

**When uncertain, surface it:**
- "This looks like it could be model-controlled. Thoughts?"
- "I'm tempted to add a safety check here - but that's compensating for the model. Should we improve the prompt instead?"
- "This pattern looks like [anti-pattern] - intentional?"

## During Verification

Before claiming complete:

- [ ] All IF statements are execution flow, not decision logic
- [ ] Model receives tools, not pre-gathered context dumps
- [ ] Tool calls execute without filtering/modification
- [ ] No fallback logic compensating for model behavior
- [ ] Adding new behavior requires only prompt changes

**Surface anything suspicious:**
- "I notice we added X - this looks like a heuristic"
- "This threshold wasn't in the plan - should we discuss?"
- "The model's decisions are being filtered here - intentional?"

## The Right Pattern

```typescript
async execute(workItem, context) {
  // === CODE: Factual inputs ===
  const inputs = {
    currentTime: new Date().toISOString(),
    lastRunTime: await getLastRunTime(),
  };

  // === CODE: Available tools ===
  const tools = [
    { name: 'get_context', description: '...' },
    { name: 'create_work_item', description: '...' },
  ];

  // === MODEL: Reasons and decides ===
  const result = await model.run({
    system: buildPrompt(inputs), // Adversarial prompts included
    tools,
  });

  // === CODE: Execute exactly what model decided ===
  for (const toolCall of result.tool_calls) {
    await executeToolCall(toolCall); // No filtering!
  }
}
```

## Multi-Turn Model Reasoning

Don't dump context. Let model request what it needs:

```
Turn 1: Minimal seed
  Model: "What do I need to know?"
  → calls get_context(source: 'conversations')

Turn 2: Has some data, needs more
  Model: "Is he busy today?"
  → calls get_context(source: 'calendar')

Turn 3: Enough to decide
  Model: "I'll wait until after his meeting"
  → calls schedule_next(when: '11am')
```

## Adversarial Prompts for Runtime Models

Build into system prompts:

- "What makes sense here?"
- "What information would help me assess this?"
- "What should I NOT do in this setting?"
- "What would [persona] do? What would [user] want?"
- "What if action 1 vs action 2?"
- "Review what you need, request it, then decide."

## Anti-Patterns to Surface

When you see these, ask about them:

| Pattern | Surface As |
|---------|------------|
| Pre-fetching all context | "Should model request this instead?" |
| IF statements deciding behavior | "This looks like decision logic - model's job?" |
| Thresholds/time windows | "Hardcoded rule - should model judge this?" |
| Filtering model output | "We're overriding model decisions - intentional?" |
| Fallback logic | "Compensating for model - improve prompt instead?" |
| "Safety" checks | "Who defines safe? Maybe model should." |

## When Model-Mediation Doesn't Apply

Not everything needs it:

- **Pure pipes:** User provides explicit input → API call → output
- **Deterministic transforms:** Data in → format change → data out
- **User-controlled flows:** User explicitly decides each step

The question isn't "does this call a model?" but "are there decisions being made, and should a model make them?"

## Collaborative Mode

This skill is about ongoing dialogue, not checkpoints:

- **Propose** architectures and tool designs
- **Question** yourself when writing code that decides
- **Ask** the user when you're uncertain
- **Surface** anti-patterns as they emerge
- **Suggest** model-mediated alternatives

Don't wait until verification to catch problems. Think about decision ownership continuously.

## The Bottom Line

**Every decision needs an owner: user, model, or code.**

- User: Explicit control, deterministic
- Model: Judgment, context-dependent, flexible
- Code: Never for judgment calls - only execution

When in doubt, ask: "Is this a judgment call?" If yes, model decides.

## Reference

For detailed methodology, see:
- `docs/design/13-model-mediated-methodology.md` (assistant-system)
- Anthropic SDK documentation for tool-based patterns
