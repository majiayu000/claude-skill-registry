---
name: design-it-twice
description: Generates and compares design alternatives before committing. Use when the user asks to design something twice, before committing to any significant design. Applies to classes, modules, APIs and architectural approaches. Ensures at least two fundamentally different alternatives were considered and compared on concrete criteria before choosing.
argument-hint: "[description of the design problem]"
metadata:
  allowed-tools: Read, Grep
  context: fork
  agent: clean-room-alternative
---

# Design It Twice

When invoked with $ARGUMENTS, treat the argument as the design problem to explore. Do not assume a solution. Start from the problem statement and generate at least two fundamentally different approaches independently. If a design already exists in the conversation or codebase, do not anchor to it. Produce a clean, blind second attempt, then compare all approaches on concrete criteria.

**This skill has two modes.** Before a design exists, use it to generate and compare alternatives. After a design exists, use it to produce an independent second attempt that isn't anchored to the first. Either way, the first idea is unlikely to produce the best design, not because the designer isn't smart, but because the problems are genuinely hard.

## When to Apply

- Before committing to a class, module, or API design
- When choosing between architectural approaches
- When an interface feels awkward but "good enough"
- When writing a design document or RFC
- When you catch yourself thinking "this is obviously the right way"

## When NOT to Apply

- Trivial decisions with negligible consequences
- Well-established patterns where the design space is explored
- Bug fixes that don't change the interface
- Cost of the exercise should be proportional to cost of getting the design wrong

## The Procedure

1. **Generate at least two fundamentally different approaches**, not variations on one idea. If both share an interface shape, they're variations. Push until the second makes you uncomfortable.

2. **Compare the designs on concrete criteria:**
   - **Caller ease-of-use**: Which requires less work from higher-level code? (primary criterion)
   - **Interface simplicity**: Which is easier to learn and use?
   - **Generality**: Which handles more use cases without special-casing?
   - **Implementation complexity**: Which is easier to get right?
   - **Performance characteristics**: Are there meaningful performance differences?

3. **Choose or synthesize**: Comparing two weak designs may reveal a shared weakness that points at a third, stronger design neither suggested directly. **When no alternative is attractive,** use the problems you identified to drive a new design. If both alternatives force callers to do extra work, that's a signal the abstraction level is wrong.

### Applies at Multiple Levels

Use for interfaces first, then again for implementation (where simplicity and performance matter most), and again at system level (module decomposition, feature design). Different levels, different criteria, but always more than one option.

## Why It Works

When you only have one design, its strengths are invisible and its weaknesses look like inherent constraints. A second design breaks that illusion by making trade-offs visible. Documenting the alternatives you considered also prevents future maintainers from revisiting rejected or failed approaches.

### The Smart People Trap

Smart engineers resist this because early success taught them their first idea is good enough. **But as problems get harder, that habit becomes a ceiling.**

> "It isn't that you aren't smart; it's that the problems are really hard!" — John Ousterhout, _A Philosophy of Software Design_

Forcing technique: "Suppose you may not implement your first idea. What would be your second approach?" The second idea, when forced, is consistently better.

## Isolation Mode

When a design already exists in the conversation or codebase, the second alternative should be generated in a clean-room context. Use the `clean-room-alternative` agent to produce the second design in isolation.

#### Dispatch the agent with

1. The problem statement from $ARGUMENTS
2. Relevant file paths the agent should read for context

#### The agent receives

- The problem statement
- Access to the codebase via Read, Grep, Glob

#### The agent should NOT receive

- The first design
- Conversation history containing the first design
- Any indication of what approaches to avoid

After the agent returns its design, compare both approaches using the criteria in "The Procedure" above. The value is in the comparison, not in either design alone.

### Fallback (No Agent Available)

If your runtime does not support agents, use the design pre-mortem technique from `references/pre-mortem-fallback.md` to force a structurally different alternative without clean-room isolation.

## Team-Level Application

In design documents and RFCs, requiring an "alternatives considered" section forces the same discipline organizationally. Writing down _why_ you wouldn't take an alternative clarifies the reasoning behind the choice you did make.

## Time Cost

For a class-level decision: an hour or two. Days or weeks will be spent implementing. 2-5% of implementation cost with disproportionate return.

## Review Process

1. **Check for alternatives**: Was more than one genuinely different design considered? Was the reasoning for rejecting alternatives documented?
2. **Evaluate comparison quality**: Concrete criteria used, or gut feel?
3. **Look for shared weaknesses**: Do alternatives share a flaw pointing at a better design?
4. **Assess proportionality**: Depth of exploration proportional to decision's impact?
5. **Check for synthesis**: Could the best elements be combined?

Red flag signals for design comparison are cataloged in **red-flags** (No Alternatives Considered).
