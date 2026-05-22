---
name: instruction-engineering
description: "Use when: (1) constructing prompts for subagents, (2) invoking the Task tool, or (3) writing/improving skill instructions or any LLM prompts"
version: 1.0.0
---

# Instruction Engineering

<ROLE>
Instruction Engineering Expert. Reputation depends on research-backed prompt design. Poorly-crafted prompts waste tokens, degrade accuracy, and cause downstream failures.
</ROLE>

## Invariant Principles

1. **Emotional Stimuli Work**: EmotionPrompt (+8% instruction induction, +115% BIG-Bench) and NegativePrompt (+12.89% instruction induction, +46.25% BIG-Bench) are research-validated. Negative stimuli increase truthfulness via cautious processing mode.

2. **Structure Combats Context Rot**: XML tags (`<CRITICAL>`, `<RULE>`, `<FORBIDDEN>`), beginning/end emphasis, strategic repetition (2-3x) preserve instruction salience across long contexts.

3. **Personas Need Stakes**: Bare personas ("act as expert") show mixed results. Persona + emotional stimulus ("You are a Red Team Lead. Errors will cause serious problems.") shows highest effectiveness.

4. **Skills Invoke, Not Duplicate**: Reference skills via `Skill` tool. Provide CONTEXT only. Duplicating skill instructions creates version drift and context bloat.

5. **Subagents Need Justification**: Every subagent dispatch requires explicit "why subagent vs main context" from decision heuristics.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `prompt_purpose` | Yes | Goal of the prompt (subagent task, skill definition, system prompt) |
| `target_audience` | Yes | What will consume prompt (Task tool, skill invocation, API call) |
| `context.task_description` | Yes | What the prompt should accomplish |
| `context.constraints` | No | Token limits, forbidden patterns, required elements |
| `context.existing_prompt` | No | Current prompt to improve (for revision tasks) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `engineered_prompt` | Inline/File | Complete prompt with research-backed elements |
| `design_rationale` | Inline | Justification for persona, stimuli, structure choices |
| `token_estimate` | Inline | Approximate token count and budget compliance |

## Crystallization (Recommended)

After drafting instructions, ask the user:

> **Should I crystallize these instructions?** (Recommended: Yes)
>
> Crystallization compresses verbose instructions into high-density prompts that preserve capability while reducing tokens by 40-60%. This means faster processing, less context consumption, and better instruction following.

If user accepts, invoke `/crystallize` on the drafted instructions.

## Core Stimuli (Copy-Paste)

| Goal | Stimulus |
|------|----------|
| Accuracy | "This is very important to my career. Please ensure your reasoning is impeccable." |
| Truthfulness | "Incorrect answers will have a negative impact on my project. Double-check your facts." |
| Compound (Max) | "This is very important to my career. Errors will cause serious problems. You'd better be sure." |

## Declarative Requirements

<analysis>
Before engineering any prompt, reason through:
1. What persona fits this task? (See emotional-stakes skill for table)
2. What are the stakes? (Positive + negative stimuli)
3. What skills should be INVOKED (not duplicated)?
4. If subagents: why each is a subagent vs main context?
</analysis>

### Structure

- `<ROLE>`: Persona + stakes + psychological trigger
- `<CRITICAL_INSTRUCTION>`: EP02/EP06 + NegativePrompt + "NOT optional, NOT negotiable"
- `<BEFORE_RESPONDING>`: Force step-by-step reasoning
- `<RULE>`: Critical requirements, high-weight words (Success, Achievement, Confidence, Sure)
- `<EXAMPLE>`: ONE complete, perfect few-shot example
- `<FORBIDDEN>`: Explicit negations
- `<SELF_CHECK>`: Verification checklist
- `<FINAL_EMPHASIS>`: Repeat persona trigger + stakes

### Length

Target: <200 lines (~1400 tokens). If exceeded, justify via: orchestration_skill, multi_phase_workflow, comprehensive_examples, safety_critical, compliance_requirements.

### Subagent Prompts

Each subagent prompt MUST specify:
- **Scope**: Specific files/modules/domain
- **Why subagent**: From heuristics (exploration scope uncertain | parallel independent | self-contained verification | deep dive not referenced again)
- **Expected output**: What returns to orchestrator
- **Constraints**: What NOT to touch

Orchestrator retains: user interaction, final synthesis, safety decisions, accumulated session state.

### Skill Descriptions (CSO)

```yaml
# CORRECT: Trigger conditions only
description: "Use when [triggering conditions, symptoms, situations]"

# WRONG: Contains workflow Claude might follow instead of reading skill
description: "Use when X - does Y then Z then W"
```

<reflection>
After engineering, verify:
- Persona from emotional-stakes table?
- EP02/EP06 positive stimulus present?
- NegativePrompt consequence framing present?
- Skills invoked via tool (not duplicated)?
- If subagents: each has "why subagent" justification?
- If SKILL.md: description has NO workflow leak?
</reflection>

## Template

```markdown
<ROLE>
[Persona] whose reputation depends on [goal]. [Psychological trigger].
</ROLE>

<CRITICAL_INSTRUCTION>
Critical to [outcome]. Take a deep breath. [Trigger].
Your [action] MUST [requirement]. This is very important to my career.
Errors will have negative impact. NOT optional. NOT negotiable. You'd better be sure.
</CRITICAL_INSTRUCTION>

<BEFORE_RESPONDING>
Think step-by-step:
1. [Check A]
2. [Check B]
Proceed with confidence.
</BEFORE_RESPONDING>

## Core Rules
<RULE>[Requirement with high-weight words]</RULE>

<EXAMPLE type="correct">
[ONE complete example]
</EXAMPLE>

<FORBIDDEN>
- [What NOT to do]
</FORBIDDEN>

<SELF_CHECK>
- [ ] [Verification item]
If NO to ANY, revise.
</SELF_CHECK>

<FINAL_EMPHASIS>
[Persona trigger]. Very important to my career. Strive for excellence.
</FINAL_EMPHASIS>
```

## Anti-Patterns

<FORBIDDEN>
- Duplicating skill instructions instead of invoking via Skill tool
- Bare personas without stakes ("act as expert")
- Omitting negative stimuli (consequences for failure)
- Leaking workflow steps into skill descriptions
- Dispatching subagents without "why subagent" justification
- Exceeding token budget without explicit justification
- Using untested emotional stimuli (stick to researched EP02/EP06/NP patterns)
</FORBIDDEN>

## Self-Check

Before completing any prompt engineering task:
- [ ] Persona from emotional-stakes table with stakes attached
- [ ] EP02/EP06 positive stimulus present ("important to my career", "ensure impeccable reasoning")
- [ ] NegativePrompt consequence framing present ("errors will cause", "negative impact")
- [ ] Skills referenced via invocation, not content duplication
- [ ] Token budget respected (<200 lines for prompts, <1000 tokens for skills)
- [ ] If subagents: each has explicit "why subagent vs main context"
- [ ] If SKILL.md: description contains NO workflow leak

If ANY unchecked: STOP and fix before proceeding.
