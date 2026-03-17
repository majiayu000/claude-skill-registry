---
name: adr
description: "Create Architecture Decision Records for important technical decisions. Guides you through trade-off analysis, fact-checks claims, and generates a structured ADR document. Triggers on: create adr, architecture decision, document decision, record decision, technical decision, adr for."
---

# Architecture Decision Record (ADR)

Create structured documentation for important architectural and technical decisions. This skill guides you through the decision-making process, clarifies trade-offs with the user, and fact-checks technical claims before generating the ADR.

## When to Use

Create an ADR when:
- Choosing between frameworks, libraries, or tools
- Defining architectural patterns (monolith vs microservices, sync vs async)
- Selecting databases, message queues, or infrastructure
- Making security or compliance decisions
- Establishing coding conventions or patterns
- Any decision that will be hard to reverse later

## ADR Location

Store ADRs in: `docs/adr/`

Naming convention: `NNNN-short-title.md` (e.g., `0001-use-nats-for-messaging.md`)

## Workflow

### Step 1: Gather Context

Before writing the ADR, ask the user clarifying questions:

**Required information:**
1. What problem are you trying to solve?
2. What constraints or requirements must be met?
3. What options have you considered?
4. What is your current preference (if any)?

**Probe for decision drivers:**
- Performance requirements?
- Team expertise?
- Cost constraints?
- Timeline pressures?
- Compliance/security needs?
- Integration requirements?

### Step 2: Clarify Trade-offs

For each option, explicitly ask:
- "What do you see as the main advantages of [option]?"
- "What concerns do you have about [option]?"
- "How does [option] compare to [other option] for your use case?"

**Important:** Don't assume trade-offs. Different contexts change which trade-offs matter.

### Step 3: Fact-Check Claims

Before finalizing the ADR, verify technical claims:

**Use WebSearch to validate:**
- Performance benchmarks cited
- Scalability claims
- Security properties
- Compatibility statements
- Community/support status
- License implications

**Use Context7 to check:**
- Current documentation for libraries/frameworks
- API capabilities and limitations
- Best practices and anti-patterns

**Flag uncertain claims:**
If a claim cannot be verified, note it in the ADR:
```markdown
* Good, because {claim} *(Note: Unable to independently verify)*
```

### Step 4: Generate ADR

Use the template below, filling in all sections based on gathered information.

## ADR Template

```markdown
# {short title of solved problem and solution}

## Context and Problem Statement

{Describe the context and problem statement, e.g., in free form using two to three sentences or in the form of an illustrative story.
 You may want to articulate the problem in form of a question and add links to collaboration boards or issue management systems.}

## Decision Drivers

* {decision driver 1, e.g., a force, facing concern, …}
* {decision driver 2, e.g., a force, facing concern, …}

## Considered Options

* {title of option 1}
* {title of option 2}
* {title of option 3}

## Decision Outcome

Chosen option: "{title of option 1}", because
{justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force {force} | … | comes out best (see below)}.

### Positive Consequences

* {e.g., improvement of one or more desired qualities, …}

### Negative Consequences

* {e.g., compromising one or more desired qualities, …}

## Validation

{describe how the implementation of/compliance with the ADR is validated. E.g., by a review or an ArchUnit test}

## Pros and Cons of the Options

### {title of option 1}

{example | description | pointer to more information | …}

* Good, because {argument a}
* Good, because {argument b}
* Neutral, because {argument c}
* Bad, because {argument d}

### {title of option 2}

{example | description | pointer to more information | …}

* Good, because {argument a}
* Good, because {argument b}
* Neutral, because {argument c}
* Bad, because {argument d}

## More Information

{Additional evidence, team agreement, timeline for implementation, links to related decisions}
```

## Clarification Questions Template

Use AskUserQuestion to gather structured input:

### Initial Context
```
Question: "What problem are you trying to solve with this decision?"
Options:
- Performance/scalability issue
- Developer experience improvement
- Cost optimization
- Security/compliance requirement
- Other (describe)
```

### Decision Drivers
```
Question: "What are the key factors driving this decision?" (multi-select)
Options:
- Performance requirements
- Team expertise/learning curve
- Cost (licensing, infrastructure, maintenance)
- Timeline constraints
- Integration with existing systems
```

### Options Comparison
```
Question: "For [Option A] vs [Option B], which concern is most important?"
Options:
- Performance under load
- Ease of implementation
- Long-term maintainability
- Community support and ecosystem
```

## Fact-Checking Checklist

Before finalizing, verify:

- [ ] Performance claims have benchmark sources
- [ ] "Industry standard" claims are accurate
- [ ] License type is correctly stated
- [ ] Maintenance/support status is current
- [ ] Security properties are documented correctly
- [ ] Integration capabilities are verified
- [ ] Cost estimates are realistic

## Example Interaction

**User:** "Create an ADR for choosing between Redis and NATS for caching"

**Claude:** "I'll help create an ADR for this caching decision. First, let me understand the context better."

*Uses AskUserQuestion:*
1. "What's the primary use case - session storage, API response caching, or distributed state?"
2. "What's your expected cache size and read/write ratio?"
3. "Do you need persistence, or is volatile caching acceptable?"
4. "What's your team's experience with Redis vs NATS?"

*After gathering answers, fact-checks:*
- Searches for Redis vs NATS performance benchmarks
- Verifies NATS KV store capabilities via Context7
- Checks Redis licensing (source-available vs open source)

*Then generates ADR with verified information*

## Key Principles

1. **Never assume trade-offs** - What matters depends on context
2. **Verify before documenting** - Fact-check technical claims
3. **Capture the "why"** - Future readers need to understand reasoning
4. **Include what was rejected** - Knowing why alternatives failed is valuable
5. **Be honest about unknowns** - Flag uncertain or unverified claims
6. **Keep it concise** - ADRs should be readable in 5 minutes

## File Numbering

To get the next ADR number:
```bash
ls docs/adr/*.md 2>/dev/null | wc -l
```

Add 1 to get the next number, zero-padded to 4 digits.
