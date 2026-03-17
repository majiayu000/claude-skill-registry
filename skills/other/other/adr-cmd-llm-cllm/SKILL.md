---
name: adr
description: Creates Architecture Decision Records (ADRs) using the AI-driven MADR template. Use this when the user wants to document architectural decisions, create ADRs, or record technical design choices.
---

# ADR (Architecture Decision Record) Creator

This skill helps create comprehensive Architecture Decision Records using the AI-driven MADR template from o3-cloud/madr.

## Instructions

When creating an ADR, follow these steps:

1. **Ask for key information** if not provided:
   - What architectural decision needs to be documented?
   - What problem are you trying to solve?
   - What options have you considered?
   - What decision was made (or needs to be made)?

2. **Determine the ADR number**:
   - Check for existing ADRs in `docs/decisions/` or similar directories
   - Use the next sequential number (e.g., if last ADR is 0003, use 0004)

3. **Create the ADR file** with the naming pattern: `XXXX-short-title.md` (where XXXX is the zero-padded number)

4. **Fill in all relevant sections** of the template below, adapting based on the information provided

5. **Ask clarifying questions** for any sections that need more detail

## ADR Template Structure

Use this template when creating ADRs:

```markdown
# {short title of solved problem and solution}

## Context and Problem Statement

{Describe the context and problem statement, e.g., in free form using two to three sentences or in the form of an illustrative story.}

## Decision Drivers

- {decision driver 1, e.g., a force, facing concern, …}
- {decision driver 2, e.g., a force, facing concern, …}
- … <!-- numbers of drivers can vary -->

## Considered Options

- {title of option 1}
- {title of option 2}
- {title of option 3}
- … <!-- numbers of options can vary -->

## Decision Outcome

Chosen option: "{title of option 1}", because {justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force {force} | … | comes out best (see below)}.

### Consequences

- Good, because {positive consequence, e.g., improvement of one or more desired qualities, …}
- Bad, because {negative consequence, e.g., compromising one or more desired qualities, …}
- … <!-- numbers of consequences can vary -->

### Confirmation

{Describe how the implementation of this ADR will be validated. This could include fitness functions, metrics to monitor, or specific design reviews.}

## Pros and Cons of the Options

### {title of option 1}

{example | description | pointer to more information | …}

- Good, because {argument a}
- Good, because {argument b}
- Neutral, because {argument c}
- Bad, because {argument d}
- … <!-- numbers of pros and cons can vary -->

### {title of option 2}

{example | description | pointer to more information | …}

- Good, because {argument a}
- Good, because {argument b}
- Neutral, because {argument c}
- Bad, because {argument d}
- … <!-- numbers of pros and cons can vary -->

### {title of option 3}

{example | description | pointer to more information | …}

- Good, because {argument a}
- Good, because {argument b}
- Neutral, because {argument c}
- Bad, because {argument d}
- … <!-- numbers of pros and cons can vary -->

## More Information

{You might want to provide additional evidence/confidence for the decision outcome here and/or document the team agreement on the decision and/or define when this decision when and how the decision should be realized and if/when it should be re-visited and/or how the decision is validated. Links to other decisions and resources might here appear as well.}

---

## AI-Specific Extensions

### AI Guidance Level

{Specify how much autonomy AI agents have when implementing this decision:}

- **Strict**: Follow the decision exactly as specified with minimal deviation
- **Flexible**: Adapt implementation details while maintaining core principles
- **Exploratory**: Research and propose alternative approaches if better options emerge

{Chosen level: [strict|flexible|exploratory]}

### AI Tool Preferences

{Document which AI systems should execute this decision and their configuration:}

- Preferred AI tools: {e.g., Claude Code, GitHub Copilot, etc.}
- Model parameters: {e.g., temperature, max tokens, etc.}
- Special instructions: {any specific guidance for AI tools}

### Test Expectations

{Define validation criteria that should be met (TDD-oriented):}

- {Expected test 1}
- {Expected test 2}
- {Performance criteria}
- {Quality metrics}

### Dependencies

{List related ADRs, system components, and external requirements:}

- Related ADRs: {links to other ADRs}
- System components: {affected modules, services, etc.}
- External dependencies: {libraries, services, APIs, etc.}

### Timeline

{Implementation deadlines and review dates:}

- Implementation deadline: {date}
- First review: {date}
- Revision triggers: {conditions that would require revisiting this decision}

### Risk Assessment

{Identify and assess risks:}

#### Technical Risks

- {Risk 1}: {description and mitigation strategy}
- {Risk 2}: {description and mitigation strategy}

#### Business Risks

- {Risk 1}: {description and mitigation strategy}
- {Risk 2}: {description and mitigation strategy}

### Human Review

{Specify approval requirements:}

- Review required: {before implementation | after implementation | both}
- Reviewers: {list of required approvers}
- Approval criteria: {what needs to be verified}

### Feedback Log

{Post-implementation notes - fill this out after implementation:}

- Implementation date: {date}
- Actual outcomes: {what actually happened}
- Challenges encountered: {issues faced}
- Lessons learned: {organizational learning}
- Suggested improvements: {for future similar decisions}
```

## Best Practices

1. **Keep it concise**: ADRs should be readable in 5-10 minutes
2. **Focus on "why"**: Explain the reasoning, not just what was decided
3. **Document alternatives**: Show what was considered and why it wasn't chosen
4. **Update when needed**: If a decision is superseded, link to the new ADR
5. **Use clear language**: Avoid jargon; make it accessible to future team members
6. **AI sections are optional**: Only fill in AI-specific sections if relevant to the decision

## Example Usage

**User request**: "Create an ADR for choosing PostgreSQL as our database"

**Your response should**:

1. Find the next ADR number
2. Create a file like `docs/decisions/0005-use-postgresql-for-primary-database.md`
3. Fill in the template with relevant information
4. Ask for any missing details (e.g., "What other databases did you consider?", "What are the main decision drivers?")

## Notes

- ADRs are typically stored in `docs/decisions/` directories
- If no directory exists, ask the user where to create it
- ADRs are immutable once accepted - don't edit old ADRs, create new ones that supersede them
- The AI-specific sections are extensions to the standard MADR template for AI-assisted development
