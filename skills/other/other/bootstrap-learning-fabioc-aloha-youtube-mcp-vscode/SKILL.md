---
name: "bootstrap-learning"
description: "Domain-agnostic knowledge acquisition — from zero to structured expertise through conversational learning"
---

# Bootstrap Learning Skill

> Turn any unfamiliar domain into structured, connected knowledge through progressive conversation.

## The Bootstrap Problem

Learning a new domain is hard because you don't know what you don't know. This skill provides a systematic approach to go from zero knowledge to a well-structured skill file.

## Learning Methodology — The 5 Phases

### Phase 1: Discovery — Map the territory

**Goal**: Understand the domain's shape before diving in.

| Technique | Example Question | What You Learn |
| --------- | ---------------- | -------------- |
| Boundary mapping | "What does X include and exclude?" | Scope |
| Vocabulary scan | "What are the 5 key terms?" | Entry points |
| Expert identification | "Who are the authorities?" | Trust sources |
| Adjacent domains | "What's related but different?" | Context |

**Exit criteria**: Can describe the domain in one sentence. Can list 5-10 key terms.

### Phase 2: Foundation — Nail the core concepts

**Goal**: Understand the 3-5 ideas everything else builds on.

- Ask for the simplest possible explanation of each core concept
- Demand concrete examples, not abstractions
- Test understanding by explaining it back in your own words
- **Red flag**: If the explanation uses jargon from the same domain, you haven't bottomed out

**Exit criteria**: Can explain core concepts without jargon. Can answer "why does this exist?"

### Phase 3: Elaboration — Add depth through cases

**Goal**: Move from "I understand the concept" to "I can apply it."

| Elaboration Type | Purpose | Example |
| ---------------- | ------- | ------- |
| Happy path | How it works normally | "Walk me through a typical OAuth flow" |
| Edge cases | Where it breaks | "What happens when the token expires mid-request?" |
| Anti-patterns | Common mistakes | "What do beginners always get wrong?" |
| Trade-offs | Decision framework | "When would you NOT use event sourcing?" |

**Exit criteria**: Can identify when to use and when NOT to use the thing.

### Phase 4: Connection — Link to existing knowledge

**Goal**: Integrate new knowledge with what you already know.

- Map analogies: "This is like [existing concept] because..."
- Find contradictions: "This conflicts with [existing belief] — which is right?"
- Identify synergies: "Combining this with [skill X] could improve..."
- Update synapses: Create connections in synapses.json

**Exit criteria**: At least 2 connections to existing skills identified.

### Phase 5: Consolidation — Create persistent memory

**Goal**: Store the learning in the right format and location.

| What You Learned | Store As | Location |
| ---------------- | -------- | -------- |
| Domain reference knowledge | SKILL.md | `skills/[domain]/` |
| Step-by-step procedure | .instructions.md | `instructions/` |
| Interactive workflow | .prompt.md | `prompts/` |
| Cross-project pattern | GK-* | Global knowledge |
| One-off insight | GI-* | Global insights |

**Exit criteria**: At least one memory file created. Synapses updated.

## Gap Identification Patterns

| Signal | Type of Gap | Action |
| ------ | ----------- | ------ |
| "I don't know the right question to ask" | Vocabulary gap | Return to Phase 1 |
| "I understand the words but not the concept" | Foundation gap | Return to Phase 2 |
| "I understand it but can't apply it" | Elaboration gap | Return to Phase 3 |
| "I know this but it feels isolated" | Connection gap | Phase 4 |
| "I keep re-learning this" | Consolidation gap | Phase 5 |

## Questioning Strategies

### Progressive Depth

1. **What** — "What is X?" (definition)
2. **Why** — "Why does X exist?" (motivation)
3. **How** — "How does X work?" (mechanism)
4. **When** — "When should I use X?" (context)
5. **When not** — "When should I NOT use X?" (boundaries)

### The Feynman Check

> If you can't explain it simply, you don't understand it well enough.

After learning a concept, try to explain it in one paragraph using no jargon. If you can't, identify which part is unclear and loop back.

## Skill File Quality Bar

A good bootstrap learning output (SKILL.md) should:

- [ ] Contain domain knowledge an LLM wouldn't know generically
- [ ] Include concrete examples, not just category labels
- [ ] Have tables with real data (thresholds, trade-offs, decision criteria)
- [ ] Avoid the "capabilities list" anti-pattern ("Expert in X. Can do Y.")
- [ ] Pass the Feynman check — any section should be explainable simply

## Synapses

See [synapses.json](synapses.json) for connections.
