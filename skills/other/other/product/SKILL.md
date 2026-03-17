---
name: adr-writer
description: Generate Architecture Decision Records for significant technical decisions
triggers: [architecture decision, ADR, why did we choose, why are we using, architectural choice]
context_cost: low
---

# ADR Writer Skill

## Goal
Document significant architectural decisions in a structured format so that future developers (and agents) understand the context, options considered, and reasoning behind each decision.

## When to Create an ADR
- Adopting a new library, framework, or service
- Choosing between multiple valid architectural approaches
- Any decision that would be hard or expensive to reverse
- Any decision affecting security or data handling
- Deviating from patterns established in AGENTS.md

## Steps

1. **Identify the decision**
   - What problem is being solved?
   - What are the constraints and requirements driving this decision?
   - What is the current state (status quo)?

2. **Research options**
   - List all viable options (minimum 2, ideally 3)
   - For each option: use research.skill to verify claims against official sources
   - Gather: pros, cons, community adoption, security track record, maintenance status

3. **Evaluate options** against project constraints
   - Which option best fits the tech stack in AGENTS.md?
   - Which option is most compatible with the architecture rules?
   - What are the performance and security implications?
   - What is the migration cost if we change later?

4. **Write the ADR** using templates/architecture/ADR_TEMPLATE.md

   ```markdown
   # ADR-[NUMBER]: [Title]

   Date: [YYYY-MM-DD]
   Status: Proposed | Accepted | Deprecated | Superseded by ADR-[N]
   Deciders: [names or roles]

   ## Context
   [The problem we're solving. Background. Constraints. Forces at play.]

   ## Options Considered

   ### Option A: [Name]
   **Pros:** [...]
   **Cons:** [...]

   ### Option B: [Name]
   **Pros:** [...]
   **Cons:** [...]

   ## Decision
   We will use **[Option X]** because [clear, specific reasoning].

   ## Consequences
   **Positive:**
   - [benefit 1]
   **Negative:**
   - [trade-off or risk 1]
   **Neutral:**
   - [things that change but aren't clearly positive or negative]

   ## Y-Statement Summary
   For [context] who need [goal], [solution] is a [category]
   that [key benefit], unlike [alternative], our solution [differentiator].
   ```

5. **Store the ADR**
   - Create: `docs/architecture/decisions/ADR-[NNN]-[title].md`
   - Create the directory if it doesn't exist
   - Number ADRs sequentially (ADR-001, ADR-002, ...)

6. **Update the ADR index**
   - If `docs/architecture/decisions/README_FULL.md` exists, add the new ADR to the table
   - If not, create it with a table of all ADRs

7. **Log to AUDIT_LOG.md**
   - Add entry with action type: ADR_CREATED
   - Reference: `docs/architecture/decisions/ADR-[NNN].md`

## Constraints
- ADRs are append-only — never delete, only supersede with a new ADR
- ADR must be human-approved before proceeding with implementation
- Options section must have at least 2 options (never "we considered only X")
- All factual claims about libraries must cite official sources

## Output Format
Completed ADR file at `docs/architecture/decisions/ADR-[NNN]-[slug].md`. Report the file path.
