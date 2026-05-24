---
name: agentskill-expertise
description: "Agent Skill design knowledge base — mechanisms, philosophy, patterns, pitfalls. Use when: designing new skills, reviewing skill quality, or deciding whether something should be a skill."
version: 202603
context: fork
---

# AgentSkill Expertise - Agent Skill Knowledge System

## Overview

The complete knowledge system for Agent Skills. Not a how-to guide (that's what official docs are for) — this focuses on three things: **why** Skills are designed the way they are, **what good design looks like**, and **where the common pitfalls are**.

Any work involving Skills — creating, adjusting, reviewing, splitting, merging — should use this as the decision framework.

---

## Core Understanding: What a Skill Actually Is

### Three Levels of Understanding

| Level | Understanding | What You Can Do | Common Issue |
|-------|--------------|-----------------|--------------|
| Surface | "Skills are a way to make AI remember instructions" | Write syntactically correct Skills | Treats Skills as fancy System Prompts |
| Mechanical | "Skills implement Progressive Disclosure" | Understands trigger mechanism and load flow | Technically correct but poorly designed |
| **Essential** | **"Skills externalize knowledge into a format that AI can actively discover and load on demand"** | **Design Skills that actually work** | — |

### Key Insights

- **Not a rule set**: A single value covers a wide range of rules. Give principles, not rules.
- **Not a prompt wrapper**: Skills have a metadata pre-loading mechanism — they're in context before conversation starts. Fundamentally different from prompts.
- **Not a tool feature**: It's a standardized format for knowledge management. Write once, works across platforms, and the accumulated knowledge only grows in value.
- **Official positioning**: "Domain Expertise" — not instructions, not workflows, but knowledge.

---

## Underlying Mechanisms

### Progressive Disclosure

```
Level 1: metadata (name + description, ~100 tokens)
         → Present from session start, always in context
         → The only thing AI uses to decide whether to load a Skill

Level 2: SKILL.md full content (<5k tokens)
         → Loaded only when AI judges it relevant

Level 3+: references/, scripts/, assets/
         → Loaded only when more detail is needed
```

### State Difference at Conversation Start

| | Traditional Approach | Skill Architecture |
|--|---------------------|-------------------|
| When conversation starts | AI starts with an empty slate | AI has already loaded all Skill metadata |
| What the user needs to do | Copy-paste every time / write "remember to read X" / stuff everything into CLAUDE.md | Nothing |
| Principle | Not mentioned = not known | Before the conversation starts, AI is already prepared |

**This is the fundamental difference** — not what happens during the conversation, but that the state is already different before it begins.

### The Description Mechanism

- AI uses **semantic matching** to decide whether to load, not keyword comparison
- Description is the only content read at Level 1
- The system enforces a **15,000 character** budget for the `<available_skills>` block (shared across all Skills)

**Known bias**: AI will err on the side of not triggering rather than over-triggering. A conservative description = a Skill that effectively doesn't exist.

> **Anthropic skill-creator**:
> "Currently Claude has a tendency to 'undertrigger' skills — to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit 'pushy'."

**Writing principles**:
- ❌ Feature-oriented: "This is a writing skill" → Too vague, AI will skip it
- ✅ Situation-oriented: "Trigger when conclusion-first, scannable, professional-tone technical writing is needed" → Clear trigger condition
- ✅ Explicitly enumerate trigger scenarios: "even if they don't explicitly ask for X" → Reduces missed triggers
- ✅ Include update triggers: "AI should proactively update when: X happens → update Y" → AI knows when to iterate

### Less Is More

> "Find the smallest set of high-signal tokens that maximize likelihood of desired outcome."
> — Anthropic official
>
> "The biggest performance gains didn't come from adding complex RAG pipelines. The gains came from removing things."
> — Manus team (100+ tools causes Context Confusion — AI hallucinates parameters or calls the wrong tool)
>
> "Keep the prompt lean. Remove things that aren't pulling their weight."
> — Anthropic skill-creator

**Conclusion**: The design principle for Skills is lean, chunked, and loaded on demand. Every instruction should pull its weight — if it can't justify its existence, remove it.

---

## Design Principles

### Principle 1: Give Principles, Not Rules

| Approach | Example | Result |
|----------|---------|--------|
| Rule | "Don't use words like 'explosive' or 'shocking'" | AI finds another way to write it; the anxiety-inducing tone remains |
| Principle | "I don't want the writing to feel anxious" | AI understands the why, automatically avoids all anxiety-inducing patterns |
| Deeper | "Be straightforward and factual" (underlying value) | One value covers a wide range of rules |

> **Anthropic skill-creator**:
> "Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are *smart*. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen... If you find yourself writing ALWAYS or NEVER in all caps, that's a yellow flag — reframe and explain the reasoning."

**Instant diagnostic**: Writing ALWAYS / NEVER in all caps? Stop. Step back and ask "what outcome do I want? Why?" Write the why instead of the imperative.

**Diagnostic test**: If your SKILL.md has 50+ specific rules, they can probably be distilled into a few principles.

### Principle 2: Passive Loading > Active Guidance

Writing a long list of "remember to read X" and "remember to read Y" in CLAUDE.md means if you forget to write it, it won't be read — and CLAUDE.md keeps growing. Better approach: turn it into a Skill, let metadata pre-load naturally — AI automatically judges when it's needed and loads on demand.

**Application**: Any "remember to read X" need should be considered for conversion into Skill references.

### Principle 3: Design Method > Copying Templates

- Other people's Skills solve other people's problems — copying them wholesale may not fit you
- Correct approach: start from your own collaboration pain points, use the five-stage design process

### Principle 4: Split First, Merge Later

- When uncertain about granularity, create a separate Skill for each scenario first
- As you work, if you discover overlapping core principles → merge into one Skill with situation-based branching
- Don't try to figure out the "optimal granularity" upfront

### Principle 5: Protocol and Persona Separation

When building an AI assistant, "how to behave" and "who it is" should be two independent Skills:

```
CLAUDE.md (lean, only the entry point)
└── "Before responding, invoke /agent-protocols"

.claude/skills/
├── agent-protocols/  ← how to behave (protocols)
│   ├── SKILL.md (description: "Required reading at session start...")
│   └── references/ (startup.md, memory.md, safety.md)
└── persona/          ← who it is (persona) ← can be copied wholesale to other projects
    ├── SKILL.md
    └── references/ (soul.md, identity.md)
```

Benefits: lean CLAUDE.md, portable persona, protocols and persona can be flexibly combined.

---

## Design Process: Five Stages

| Stage | Core Question | Right Approach | Common Mistake |
|-------|--------------|----------------|----------------|
| 1. Empathize | When does AI lose its way? | Start from "collaboration pain points" | Start from "what I want" |
| 2. Define | What problem does this Skill solve? | Clear, measurable design goal | Vague wish |
| 3. Ideate | How to write metadata and principles? | Generate 3+ options, then pick the best | Accept the first idea |
| 4. Prototype | Does the MV Skill work? | Minimum viable version, test first then iterate | Perfectionism |
| 5. Test | Found? Understood? Solved? | Validate all three design assumptions | Only ask "are there bugs?" |

### MV Skill Standard

A v1.0 only needs:
1. A clear description
2. Coverage of the core scenario (80% of cases)
3. One concrete example
4. Something you can actually test

### The Three Test Questions

1. Can AI **find** this Skill? (is the description clear enough?)
2. Can AI **understand** this Skill? (are the instructions clear enough?)
3. Does this Skill **solve the problem**? (does the design assumption hold?)

All three "yes" → success. Any "no" → iterate.

### Comparative Testing Method

The Three Test Questions tell you *what* to ask. Comparative testing tells you *how* to test.

**Method**: Run the same task twice — with Skill vs without Skill, then compare.

| Dimension | What to Observe |
|-----------|----------------|
| **Behavioral difference** | How different is AI's behavior with vs without the Skill? Larger difference = higher Skill impact |
| **Quality difference** | Is the output with the Skill actually better? Or just different? |
| **Trigger reliability** | Run 2-3 times — does the Skill get loaded every time? |

**When to use**:
- When you finish the first version of a new Skill — confirm it actually has an effect
- After editing the description — confirm trigger rate hasn't degraded
- When a connection in the system is unreliable — pinpoint which Skill broke

### Iterative Debugging: Read the Process, Not Just the Output

The Three Test Questions and comparative testing both focus on **outputs**. But Skill problems often hide in AI's **working process**.

> **Anthropic skill-creator**:
> "Make sure to read the transcripts, not just the final outputs — if it looks like the skill is making the model waste a bunch of time doing things that are unproductive, you can try getting rid of the parts of the skill that are making it do that."

**How to look**: Observe AI's thinking process or working steps —
- AI doing things the Skill requires but that aren't actually useful? → Remove that instruction
- AI repeatedly hesitating on a decision? → The principle isn't written clearly enough
- AI taking a roundabout path to reach the result? → The workflow can be simplified

**Core judgment**: Correct output but bloated process = Skill has room to slim down.

---

## Application Judgment: What Should Become a Skill

### Decision Criteria

> "Is this knowledge, method, or workflow something I want AI to always remember?"
> If yes, it should be externalized as a Skill.

### Good Candidates for Skills

| Type | Examples |
|------|---------|
| Process planning | SOPs, customer service flows, review workflows |
| Learning methods | Your personal learning approach, thinking frameworks |
| Values and principles | Response style, decision frameworks, personal principles |
| Knowledge systems | Book knowledge → callable consultant, project technical decisions |
| Multi-Skill collaboration | Conversation close → auto-trigger memory update |
| Project knowledge | Technical decisions, architecture choices, design standards |

### Poor Candidates for Skills

| Type | Reason | Better Approach |
|------|--------|----------------|
| One-time instructions | No reuse value | Say it directly in conversation |
| Rapidly changing information | Maintenance cost too high | Keep in conversation context or documents |
| Very long content (>10k tokens) | Loading consumes too much context | Split into multiple Skills or put in references |

---

## Skill Evolution Patterns

Every Skill typically goes through a similar evolution:

```
v1: Rule/case-driven
    └── A list of rules, AI executes mechanically
         │
    Problem discovered: fails on new situations, or results feel "off"
         │
v2: Principle/worldview-driven
    └── Give core principles, AI judges for itself
         │
    Validated: AI can handle unforeseen situations
         │
v3+: Continuous iteration
    └── Fine-tune principles based on real usage, add edge cases
```

**Empirical examples**:

| Skill | v1 (rule-driven) | Problem | v2 (principle-driven) |
|-------|-----------------|---------|----------------------|
| Digital secretary | If A, do X; if B, do Y | Unwritten cases don't get handled | Core principles of a good secretary (proactive anticipation, let owner focus) |
| Writing style | Don't use certain words, format headings this way | AI gets boxed in, output has no soul | Worldview-driven (I hate anxiety-inducing tone, be straightforward) |
| AI assistant architecture | Everything stuffed into CLAUDE.md, 500+ lines | Keeps growing, forgotten entries don't get read | Protocol vs persona separation, two independent Skills |

---

## Common Misconceptions

| Misconception | Wrong Understanding | Correct Understanding |
|--------------|--------------------|-----------------------|
| Skill = advanced prompt | Just wrap a prompt in Skill format | Skills have metadata pre-loading; fundamentally different |
| More rules = better | SKILL.md with 50+ rules is thorough | Principles replace rules; lean is more effective |
| Description doesn't matter | It's just descriptive text | It's the only thing AI uses to decide whether to load |
| More Skills = more powerful | Installing 100 Skills makes you strong | Tool overload causes AI hallucinations |
| Copying templates is fine | Find someone else's and copy it | Their pain points aren't your pain points |
| CLAUDE.md must be exhaustive | Write all guidance in CLAUDE.md | Passive loading > active guidance |
| Skills are static | Write it once and done | Good Skills continuously evolve with use |

---

## Skill Review Checklist

Use this checklist when designing new Skills or adjusting existing ones:

### Frontmatter (Required)
- [ ] SKILL.md opens with YAML frontmatter (surrounded by `---`)
- [ ] Contains `name` field (the Skill's identifier)
- [ ] Contains `description` field (Progressive Disclosure Level 1)

### Description Quality
- [ ] Describes "usage scenarios" not "feature categories"
- [ ] After reading the description, AI can judge "when to load this"
- [ ] Concise but sufficiently informative (doesn't waste the 15,000 character budget)
- [ ] Includes proactive update triggers (when to iterate this Skill)

### Content Design
- [ ] Primarily principles/values, not rule enumeration
- [ ] Has concrete examples (at least one)
- [ ] Long content is in references/, not stuffed into SKILL.md
- [ ] SKILL.md < 5k tokens

### Architectural Soundness
- [ ] Appropriate granularity (one Skill solves one class of problems)
- [ ] No significant overlap with other Skills
- [ ] If multi-Skill collaboration, rules include clear cross-Skill linkage guidance

### Maintainability
- [ ] Has a clear "when to update" statement
- [ ] Structure allows appending without requiring a rewrite
- [ ] References are independent documents that can be updated separately

---

## When to Update This Skill

> **AI proactive update rule**: When the following situations occur, AI should proactively propose updates.

| Situation | Update What |
|-----------|------------|
| Discovered new patterns or pitfalls while designing a Skill | `references/design-patterns.md` |
| Discovered a new common misconception | "Common Misconceptions" section |
| New findings on technical mechanisms (official updates, new research) | "Underlying Mechanisms" section |
| Review checklist needs new items | "Skill Review Checklist" section |
| New empirical examples for evolution patterns | "Skill Evolution Patterns" section |

### Update Principles

1. **Evidence-driven**: Only document insights validated through practice
2. **Preserve evolution context**: When updating, note "when and what prompted this discovery"
3. **Lean is paramount**: This Skill itself must follow "less is more"

---

## Reference Resources

| File | Contents | When to Read |
|------|----------|-------------|
| `references/design-patterns.md` | Design patterns (P1-P6) and anti-patterns (A1-A6) quick reference | When designing new Skills or during review |
| `references/skill-template.md` | Creation template based on this Skill's principles | When building a new Skill from scratch |
