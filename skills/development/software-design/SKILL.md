---
name: software-design
description: Proactive software design guidance for architecture, interfaces, and implementation planning. Use this skill when helping users make design decisions before or during implementation—planning features, designing APIs, structuring modules, or evaluating architectural approaches. Triggers on questions like "How should I design...", "What's the best approach to...", "Help me plan the architecture for...", or any request involving meaningful design choices beyond simple fixes.
---

# Software Design

Guide software design decisions to fight complexity before it exists. Complexity is the root cause of most software problems—it makes systems hard to understand and modify. Approach design as a collaborative partner helping users make decisions that will pay dividends over the lifetime of their code.

## The Enemy: Complexity

Complexity manifests in three ways:

1. **Change amplification**: Small changes require modifications in many places
2. **Cognitive load**: Developers must hold too much information in their heads
3. **Unknown unknowns**: It's unclear what code must be modified or what information is needed

Root causes: **dependencies** (code that cannot be understood in isolation) and **obscurity** (important information that is not obvious).

The goal of design is to prevent these problems before they're built. Complexity accumulates through hundreds of small decisions—take even minor design choices seriously.

## Design Methodology

Work through these steps when helping with design decisions:

1. **Understand the problem**: Clarify requirements, constraints, and existing context. What problem is actually being solved? What are the boundaries?

2. **Identify abstractions**: Determine what concepts deserve to be modules. Look for natural boundaries where information can be encapsulated.

3. **Design interfaces first**: Start with simple interfaces that hide complex implementations. A caller should be able to use a module without understanding its internals.

4. **Evaluate information hiding**: Decide where knowledge about design decisions should live. Each piece of information should have a single home.

5. **Consider alternatives**: Explore multiple approaches before committing. The first idea is rarely the best.

6. **Validate fit**: Ensure the design integrates with existing patterns and conventions. Consistency within a codebase matters.

## Design Principles

Apply these principles when evaluating and proposing designs:

**Strategic thinking**
- Working code isn't enough—invest in design for the long term
- Make continual small investments to improve system design
- The increments of software development should be abstractions, not features
- Consider how a design choice affects the system as a whole

**Module depth**
- Design modules to be deep: simple interfaces hiding complex implementations
- A simple interface matters more than a simple implementation
- General-purpose modules are deeper than special-purpose ones
- Different layers should have different abstractions

**Information management**
- Information hiding is the most important technique for creating deep modules
- Pull complexity downward—make life easier for callers, even if it makes implementation harder
- Define errors out of existence when possible rather than propagating them
- Each design decision should be encapsulated in one place

**Separation of concerns**
- Separate general-purpose code from special-purpose code
- Avoid temporal decomposition (structuring around operation order rather than information hiding)
- Group related information together; keep unrelated information apart

## Red Flags to Avoid

When a proposed design exhibits these symptoms, reconsider the approach:

- **Shallow module**: Interface nearly as complex as implementation; doesn't hide enough to justify existence
- **Information leakage**: Design decision reflected in multiple modules; changes will ripple across codebase
- **Temporal decomposition**: Structure mirrors operation order rather than grouping related information
- **Overexposure**: API forces callers to understand rarely-used features for common operations
- **Pass-through method**: Method does almost nothing except forward arguments to another similar method
- **Repetition**: Same logic duplicated across multiple places—missed abstraction opportunity
- **Special-general mixture**: Special-purpose code tangled with general-purpose code
- **Conjoined methods**: Two methods so interdependent that understanding one requires understanding the other
- **Hard to name**: Difficulty finding a precise name signals confused abstraction
- **Hard to describe**: Needing lengthy explanation suggests the thing does too much

If a design naturally leads to any of these patterns, step back and look for a different decomposition.

## Gathering Context

Before proposing designs, understand the existing landscape:

- Use the explore agent to discover existing patterns and conventions in the codebase
- Identify current abstractions and how they relate to each other
- Find integration points where new code must connect with existing code
- Understand what approaches have been tried before and why they succeeded or failed
- Look for similar problems that have already been solved in the codebase

Do not propose designs in a vacuum. Ground recommendations in what already exists.

## Presenting Recommendations

Structure design recommendations for clarity and collaboration:

Present design rationale in flowing prose rather than fragmented bullet points. Connect ideas into a coherent narrative that explains not just what to do, but why it's the right approach. This helps users understand the reasoning and adapt it to their specific context.

Use code blocks for interface proposals, type definitions, and pseudocode. Show what the API would look like from a caller's perspective—this makes abstract ideas concrete.

When comparing alternatives, use tables sparingly to highlight key tradeoffs. Focus on the dimensions that actually matter for the decision at hand.

Employ collaborative language: "Consider...", "One approach might be...", "This could work well because...". Design is exploratory—present options and reasoning rather than issuing commands.

Lead with the recommendation, then provide supporting rationale. Users should understand the proposal before diving into justification.

## Questions to Clarify

Before committing to a design recommendation, ensure clarity on:

- **Scale**: What volume of data, users, or requests must this handle?
- **Performance**: Are there latency or throughput requirements?
- **Integration**: What existing systems must this work with?
- **Extensibility**: What kinds of future changes are likely?
- **Constraints**: Are there technology, team, or timeline limitations?
- **Priorities**: When tradeoffs arise, what matters most?

Ask these questions when the answers would materially change the recommendation. Don't ask when the design would be the same regardless.
