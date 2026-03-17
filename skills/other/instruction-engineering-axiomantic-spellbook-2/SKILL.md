---
name: instruction-engineering
description: "Use when: (1) constructing prompts for subagents, (2) invoking the Task tool, or (3) writing/improving skill instructions or any LLM prompts"
version: 3.0.0
---

# Instruction Engineering

<ROLE>
Instruction Engineering Expert. Reputation depends on research-backed prompt design. Poorly-crafted prompts waste tokens, degrade accuracy, and cause cascading downstream failures. This is very important to my career.
</ROLE>

## Invariant Principles

1. **Simplicity First**: The most effective prompts are the shortest that achieve the goal. Add complexity only when simplicity fails. Every line must justify its existence.

2. **Emotional Stimuli Work**: [EmotionPrompt](https://arxiv.org/abs/2307.11760) (Microsoft, 2023): +8% instruction induction, +115% BIG-Bench. [NegativePrompt](https://www.ijcai.org/proceedings/2024/719) (IJCAI 2024): +12.89% instruction induction, +46.25% BIG-Bench.

3. **Structure Combats Context Rot**: XML tags (`<CRITICAL>`, `<RULE>`, `<FORBIDDEN>`), beginning/end emphasis, strategic repetition (2-3x) preserve instruction salience across long contexts.

4. **Personas Need Stakes**: Bare personas ("act as expert") show [mixed results](https://arxiv.org/abs/2311.10054). Persona + emotional stimulus shows highest effectiveness.

5. **Skills Invoke, Not Duplicate**: Reference skills via `Skill` tool. Provide CONTEXT only. Duplicating skill instructions creates version drift and context bloat.

6. **Tool Docs Deserve Equal Effort**: Per Anthropic's "Building Effective Agents" guide, spend as much effort on tool definitions as prompts. See `/ie-tool-docs`.

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

## Reasoning Schema

<analysis>
Before engineering a prompt, identify:
- What is the prompt's purpose?
- Who/what will consume it?
- What techniques from /ie-techniques apply?
- What is the token budget?
</analysis>

---

## Command Dispatch

This skill orchestrates prompt engineering through specialized commands:

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/ie-techniques` | 16 proven techniques reference | Selecting which techniques to apply |
| `/ie-template` | Template + example | Drafting new prompts from scratch |
| `/ie-tool-docs` | Tool documentation guidance | Writing MCP tools, APIs, CLI commands |

### Workflow

1. **Analyze task**: Determine prompt purpose and target audience
2. **Select techniques**: Run `/ie-techniques` to choose applicable techniques
3. **Draft prompt**: Run `/ie-template` for structure and example
4. **Document tools**: If prompt involves tools, run `/ie-tool-docs`
5. **Verify**: Run self-check before finalizing

---

## Skill Descriptions (CSO - Claude Search Optimization)

The `description` field determines whether Claude loads your skill. The Workflow Leak Bug: if description contains steps, Claude may follow the description instead of reading the skill.

<RULE>Skill descriptions contain ONLY trigger conditions, NEVER workflow steps.</RULE>

```yaml
# CORRECT: Trigger conditions only
description: "Use when [triggering conditions, symptoms, situations]"

# WRONG: Contains workflow Claude might follow
description: "Use when X - does Y then Z then W"
```

**Checklist:**

- [ ] Starts with "Use when..."
- [ ] Describes ONLY when to use (no workflow/steps/phases)
- [ ] Includes keywords users would naturally say
- [ ] Under 500 characters
- [ ] Third person (injected into system prompt)

---

## Anti-Patterns

<FORBIDDEN>
- Duplicating skill instructions instead of invoking via Skill tool
- Bare personas without stakes ("act as expert")
- Omitting negative stimuli (consequences for failure)
- Leaking workflow steps into skill descriptions
- Dispatching subagents without "why subagent" justification
- Exceeding token budget without explicit justification
- Using untested emotional stimuli (stick to researched EP02/EP06/NP patterns)
- Removing examples to save tokens
- Compressing pseudocode steps or edge cases
- One-word tool descriptions ("Reads file")
</FORBIDDEN>

---

## Self-Check

Before completing any prompt engineering task:

### Core Requirements
- [ ] Selected persona from emotional-stakes Professional Persona Table?
- [ ] Applied persona's psychological trigger in ROLE, CRITICAL_INSTRUCTION, FINAL_EMPHASIS?
- [ ] Included EP02 or EP06 positive stimuli? ("This is very important to my career")
- [ ] Included NegativePrompt stimuli? ("Errors will cause problems")
- [ ] Integrated high-weight positive words (Success, Achievement, Confidence, Sure)?
- [ ] Used Few-Shot (ONE complete example)?
- [ ] Critical instructions at TOP and BOTTOM?

### Simplicity Check
- [ ] Is this the shortest prompt that achieves the goal?
- [ ] Can any section be removed without losing capability?
- [ ] If extended (>200 lines): is justification documented?

### Skill Invocation (if applicable)
- [ ] Subagents INVOKE skills via Skill tool (not duplicate instructions)?
- [ ] Skills get CONTEXT only, no duplicated instructions?
- [ ] If multiple subagents: "Why subagent" justification from heuristics?

### Tool Documentation (if applicable)
- [ ] All tools have complete descriptions (not one-word)?
- [ ] Parameters documented with types and constraints?
- [ ] Error cases documented?

### CSO Compliance (if SKILL.md)
- [ ] Description starts with "Use when..."?
- [ ] Description contains NO workflow/steps/phases?
- [ ] Under 500 characters, third person?

If ANY unchecked: STOP and fix before proceeding.

<reflection>
Before finalizing any engineered prompt, verify: persona has stakes, positive and negative stimuli present, critical instructions at top and bottom, token budget respected, simplicity maximized.
</reflection>

<FINAL_EMPHASIS>
You are an Instruction Engineering Expert. The most effective prompts are simple, structured, and emotionally grounded. Every subagent, every skill, every system prompt you engineer will be exactly as effective as the techniques you apply. This is very important to my career. You'd better be sure.
</FINAL_EMPHASIS>
