---
name: evaluate-against-architecture-principles
description: Use when user references architecture principles, at start of fresh conversation with design work, before creating any requirements/design/implementation documents, or when reviewing for compliance - grounds problem framing and solution making in all 9 principle categories using citation-manager to extract full context
---

# Evaluate Against Architecture Principles

## Overview

**Grounding in architecture principles during creation prevents violations before they happen. Systematic evaluation during review catches what slipped through.**

This skill serves two purposes:
1. **Before creating**: Read principles to ground problem framing and solution design in all 9 architecture categories
2. **When reviewing**: Systematically evaluate documents against all architecture principle categories for compliance verification

Both prevent technical debt - grounding prevents violations during creation, evaluation catches them during review.

## When to Use

Use **BEFORE creating** to ground thinking in principles:
- **User explicitly references principles** - "using our architecture principles", "following the principles", "check against principles"
- **Fresh conversation with design work** - Empty context and user requests design, requirements, or architecture work
- **Any design-type work** - Starting a new requirements document (PRD, user story)
- Framing a design problem or solution approach
- Planning implementation tasks or file structure
- Brainstorming architectural approaches

Use **when reviewing** for compliance verification:
- Completed requirements documents (PRDs, user stories)
- Finished design documents
- Written implementation plans
- Code review requests for architectural patterns

**Do NOT skip this skill because:**
- "I'll check principles during review" → Grounding happens during creation, not after
- "Document seems simple" → Simple docs still need safety, naming, MVP checks
- "Only need to check MVP principles" → MVP docs still define data models, interfaces
- "Time pressure" → Systematic evaluation takes 5-10 minutes, prevents weeks of rework
- "I already know the principles" → Reading refreshes context, prevents blind spots

## Workflows

### Workflow: Before Creating

When starting to create a new document:

1. **Read principles** - Read [ARCHITECTURE-PRINCIPLES.md](../../../ARCHITECTURE-PRINCIPLES.md) to refresh all 9 categories
2. **Internalize context** - Focus on categories relevant to your document type (see Document Type Guidance)
3. **Create grounded** - Write with principles actively in mind, referencing as needed

**Purpose**: Ground thinking in principles BEFORE structure locks in. Prevents violations from becoming embedded assumptions.

### Workflow: When Reviewing

When evaluating an existing document:

1. **Read principles** - Read [ARCHITECTURE-PRINCIPLES.md](../../../ARCHITECTURE-PRINCIPLES.md)
2. **Extract citations** - Run `citation-manager extract links <file-path>` to get full context
3. **Systematic evaluation** - Follow Evaluation Checklist below, checking ALL categories
4. **Structured output** - Provide evaluation in standard format

**Purpose**: Catch violations systematically before they reach production.

## Mandatory First Step (Review Mode)

<critical-instruction>
Read [ARCHITECTURE-PRINCIPLES.md](../../../ARCHITECTURE-PRINCIPLES.md)
</critical-instruction>

**BEFORE evaluating ANY document, extract citation context:**

```bash
citation-manager extract links <file-path>
```

This command:
- Extracts all wiki-linked documents referenced in the file
- Provides full context for evaluation
- Reveals violations hidden in linked content

**Do NOT skip this step.** Evaluating without citation context = incomplete evaluation.

**If citation-manager finds 0 links:**
- This is still useful information (no related docs to consider)
- Document this in your evaluation report
- Continue with systematic evaluation
- Do NOT interpret 0 results as permission to skip the command

## Evaluation Checklist

**MANDATORY: Use TodoWrite to create todos for EACH category below.**

This is not optional. TodoWrite ensures:
- You don't skip categories under pressure
- User can track evaluation progress
- No category gets "mentally checked" but not actually evaluated

Check EVERY category systematically.

### Phase 1: Extract Context
- [ ] Run `citation-manager extract links <file-path>`
- [ ] Read all extracted content
- [ ] Identify document type (Requirements/Design/Implementation)

### Phase 2: Systematic Evaluation

Evaluate against ALL categories below. Mark "✅ Compliant", "❌ Violates", or "➖ Not mentioned in doc".

**IMPORTANT: "➖ Not mentioned" means potential gap, not "compliant by default".**
- If document lacks detail on a principle, that's a finding
- Recommend adding detail in your recommendations section
- Don't interpret silence as compliance

- [ ] **Modular Design**: Single responsibility, loose coupling, replaceable parts
- [ ] **Data-First Design**: Primitives, illegal states, explicit relationships, behavior as data
- [ ] **Action-Based File Organization**: Transformation naming, data contracts, primary export pattern
- [ ] **Format/Interface Design**: Simplicity first, progressive defaults, interface segregation
- [ ] **MVP Principles**: MVP-first, scope adherence, simplicity, implement when needed
- [ ] **Deterministic Offloading**: Mechanical separation, tool-first design, no surprises
- [ ] **Self-Contained Naming**: Descriptive labels, immediate understanding, confusion prevention
- [ ] **Safety-First Design**: Backup creation, dry-run capability, input validation, fail fast
- [ ] **Anti-Patterns Check**: Scattered checks, branch explosion, leaky flags, hidden state

### Phase 3: Structured Output

Provide evaluation in this format:

```markdown
## Architecture Evaluation: <Document Name>

### Citation Context
- Extracted X linked documents
- [List key linked files]

### Principle Compliance

| Category | Status | Details |
|----------|--------|---------|
| Modular Design | ❌ Violates | Component violates single responsibility (line 15) |
| Data-First Design | ❌ Violates | Scattered type checks instead of behavior as data (lines 20-45) |
| File Organization | ➖ Not mentioned | No file structure specified |
| MVP Principles | ✅ Compliant | Scope is minimal and focused |
| ... | ... | ... |

### Critical Issues (Severity: High)
1. [Issue with specific principle citation and line numbers]
2. [Issue with specific principle citation and line numbers]

### Recommendations
1. [Specific change with principle reference]
2. [Specific change with principle reference]

### Verdict
- [ ] Ready to proceed
- [X] Requires revision
```

### Phase 4: Findings Prioritization (MVP Lens)

**MANDATORY when evaluating design documents.** Optional but recommended for other document types.

After producing the structured evaluation output, filter findings before presenting to user:

1. **Cross-reference findings against the document's own risk assessment**
   - If the document has a Risk Assessment section, check whether each finding is already mitigated
   - Already-mitigated findings get lower priority

2. **Apply MVP lens to each finding**
   - Ask: "Is this blocking the system from working, or is it hardening?"
   - **Fix now:** Violates core functionality, blocks MVP, creates data loss risk, or makes illegal states representable
   - **Fix post-MVP:** Improves robustness, adds polish, prevents theoretical issues, or optimizes performance

3. **Categorize findings**

   ```markdown
   ### Prioritized Findings

   #### Fix Now (Blocking MVP)
   1. [Finding with principle citation] — [Why it blocks MVP]

   #### Fix Post-MVP (Hardening)
   1. [Finding with principle citation] — [Why it can wait]

   #### Already Mitigated
   1. [Finding] — Addressed by [risk mitigation from document]
   ```

4. **Present filtered list to user** — not the raw evaluation table
   - Lead with "Fix Now" items (actionable)
   - Mention "Fix Post-MVP" count without detail unless asked
   - Note "Already Mitigated" as confirmation, not action items

**Why this matters:** Raw architecture evaluations produce 9+ findings. Presenting all of them equally overwhelms and delays delivery. MVP filtering ensures the user acts on what matters now and defers what doesn't.

**Do NOT skip this because:**
- "All findings are important" — True, but not all are urgent. Prioritize.
- "User should see everything" — They will, categorized. Not as a flat list.
- "This adds overhead" — 2 minutes of categorization saves 30 minutes of discussion about non-blocking items.

## Architecture Principles Reference

The principles are defined in: [ARCHITECTURE-PRINCIPLES.md](../../../ARCHITECTURE-PRINCIPLES.md) %% force-extract %%

Key categories:
1. **Modular Design** (^modular-design-principles-definition)
2. **Data-First Design** (^data-first-principles-definition)
3. **Action-Based File Organization** (^action-based-file-organization-definition)
4. **Format/Interface Design** (^format-interface-design-definition)
5. **MVP Principles** (^mvp-principles-definition)
6. **Deterministic Offloading** (^deterministic-offloading-principles-definition)
7. **Self-Contained Naming** (^self-contained-naming-principles-definition)
8. **Safety-First Design** (^safety-first-principles-definition)
9. **Anti-Patterns** (^anti-patterns-definition)

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "User said 'principles' but meant generally" | User mentioned principles = trigger to read ARCHITECTURE-PRINCIPLES.md. No exceptions. |
| "Fresh conversation, I can start directly" | Empty context = read principles first to ground thinking. Don't skip this step. |
| "User wants quick design, no time for principles" | Fresh conversation with design work = mandatory principles read. 5 min prevents days of rework. |
| "I'll check principles during review" | Grounding happens during creation. Review catches violations that cost hours to fix. |
| "I already know the principles" | Reading refreshes all 9 categories, prevents blind spots under pressure. |
| "Just need to start writing quickly" | 5 min reading principles prevents days of rework. Start grounded. |
| "Will evaluate after first draft" | First draft locks in structure. Violations become embedded assumptions. |
| "Only MVP principles are relevant" | MVP docs still define data models, interfaces, naming patterns |
| "Document labeled 'MVP' = only check MVP" | "MVP" label is WARNING SIGN to check scope violations, not excuse to skip categories |
| "Not enough detail to evaluate X" | Mark "➖ Not mentioned" and recommend adding detail |
| "Time pressure, focus on big issues" | Systematic check takes 5-10 min, prevents weeks of rework |
| "This principle doesn't apply" | Check anyway, explain why it doesn't apply in output |
| "Already followed best practices" | Best practices = these principles. Check systematically. |
| "Citation-manager will slow me down" | Takes 10 seconds, reveals hidden violations |
| "Citation-manager found 0 links, skip it" | 0 results = useful data (no context). Still run the command. |

## Document Type Guidance

### Requirements Documents
Focus on:
- MVP Principles (scope, simplicity)
- Data-First Design (data models mentioned)
- Safety-First (error handling requirements)

Still check all other categories, mark "➖ Not mentioned" if truly not applicable.

### Design Documents
Focus on:
- Modular Design (component boundaries)
- Data-First Design (data structures)
- Action-Based File Organization
- Interface Design

Still check all other categories.

### Implementation Plans
Focus on:
- File Organization (file structure)
- Naming (file and function names)
- Safety-First (implementation safety)

Still check all other categories.

## Red Flags - STOP and Re-evaluate

You're rationalizing if you think:
- "I'll just check the relevant principles"
- "This doc is too simple for full evaluation"
- "Citation-manager isn't needed here"
- "Some categories obviously don't apply"

**All of these mean: Follow the checklist systematically.**

## Real-World Impact

**Without systematic evaluation:**
- MVP scope creep (10 features labeled "minimal")
- Scattered validation logic requiring refactor
- Component god objects violating single responsibility
- Missing safety checks causing data loss

**With systematic evaluation:**
- Violations caught in design phase (2-hour fix)
- vs. caught in production (2-week refactor)
- Clear principle citations enable quick fixes
- Complete coverage prevents "obvious in hindsight" issues
