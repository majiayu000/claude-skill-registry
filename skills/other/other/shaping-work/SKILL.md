---
name: shaping-work
description: Shape rough ideas into clear, actionable work definitions. Use this skill whenever someone has an unstructured idea that needs to become a concrete work definition — feature requests, bug reports, PRDs, customer feedback, Slack threads, stakeholder asks, or vague "we should do X" statements. Trigger phrases include "shape this", "scope this", "write a PRD", "define this work", "turn this into a ticket", "flesh this out", "spec this out", "what should we build for X", "I have an idea for...", or any rough input that needs structure before implementation can begin.
---

# Shaping Work

Shape ambiguous ideas into clear work definitions. Focus on clarity, not process theater.

## Principles

- **No jargon** — write so anyone can understand
- **Product-focused** — define *what*, not *how* to build it
- **Right level of detail** — enough to act on, not a specification
- **Flag unknowns** — surface risks and questions early

## Process

1. **Understand the request** — Read the input (could be anything: a Slack thread, a rough idea, a customer complaint, a formal PRD). If intent is unclear, ask up to 3 targeted questions, then shape with stated assumptions.
2. **Understand the context** — If working in a codebase, read CLAUDE.md or similar to understand what the application does (the product, not technical details).
3. **Shape the work** — Write the definition using the output format below. Pick the template variant that fits the type of work.
4. **Surface unknowns** — List anything that needs clarification before implementation.
5. **Save the document** — Save to `thoughts/research/YYYY-MM-DD-descriptive-name.md`.

## Output Format

The core structure adapts to the type of work. Always include: title, description, acceptance criteria, and risks/unknowns. The middle sections flex based on what you're shaping.

### Feature work

```markdown
## [Clear, descriptive title]

[1-2 sentence description of what this feature does and why it matters]

**User Story**: As a [user type], I want [goal], so that [benefit].

### Acceptance Criteria

- [Observable behavior, not implementation detail]
- [What triggers this feature/flow]
- [What the user sees or experiences]
- [Key states and edge cases]

### Designs

[Link to Figma/designs if provided, or "N/A"]

### Risks & Unknowns

- [Questions, dependencies, or unclear areas]
```

### Bug fix

```markdown
## Fix: [what's broken]

[1-2 sentence description of the bug and its user impact]

**Current behavior**: [what happens now]
**Expected behavior**: [what should happen]
**Reproduction**: [steps or conditions to trigger]

### Acceptance Criteria

- [The specific broken behavior that should be fixed]
- [Any related edge cases to verify]

### Risks & Unknowns

- [Unclear scope, possible regressions, missing reproduction info]
```

### Improvement / tech debt

```markdown
## Improve: [what's being improved]

[1-2 sentence description of the improvement and why it matters now]

**Current state**: [what exists today and what's wrong with it]
**Desired state**: [what it should look like after]

### Acceptance Criteria

- [Measurable outcomes — what changes for the user or the system]

### Risks & Unknowns

- [Migration concerns, backwards compatibility, scope creep]
```

Use the variant that fits best. For work that doesn't fit neatly, adapt — the acceptance criteria and risks sections are the essential parts.

## Examples

### Small work (single ticket)

**Input**: "We need to show users how many items are in their cart in the header"

**Output**:

```markdown
## Cart item count in header

Display a badge on the cart icon showing the number of items currently in the user's cart.

**User Story**: As a shopper, I want to see how many items are in my cart at a glance, so that I don't have to open the cart to check.

### Acceptance Criteria

- Display a numeric badge on the cart icon in the site header
- Badge shows total quantity of items (not unique products)
- Badge is hidden when cart is empty (not "0")
- Count updates immediately when items are added/removed
- Badge is visible on all pages where the header appears

### Designs

N/A — follow existing badge patterns in the UI

### Risks & Unknowns

- Should the count persist across sessions for logged-out users?
- Max display value? (e.g., "99+" for large carts)
```

### Bug fix

**Input**: "Users are complaining that the search doesn't find products by SKU"

**Output**:

```markdown
## Fix: search doesn't match product SKUs

Users expect to find products by entering a SKU in the search bar, but search currently only matches product names and descriptions.

**Current behavior**: Searching "SKU-12345" returns no results even when the product exists.
**Expected behavior**: SKU search returns the exact matching product.
**Reproduction**: Go to search → enter any valid SKU → observe zero results.

### Acceptance Criteria

- Search matches against the product SKU field in addition to name/description
- Exact SKU match ranks first in results
- Partial SKU matches are included but ranked lower

### Risks & Unknowns

- Does the search index include the SKU field, or does the index need rebuilding?
- Are SKUs unique across all product types?
```

### Larger work (PRD-style)

**Input**: "Partners aren't completing onboarding. We want to remind them."

**Output**:

```markdown
## Onboarding reminder modal

Display a reminder modal when a Partner logs into the Back Office without completing all onboarding steps. The modal lists what's missing and guides them to finish.

**User Story**: As a Partner, I want to be reminded when I haven't finished onboarding, so that I can complete the required steps and start earning.

### Acceptance Criteria

**When it appears:**
- Partner logs into Back Office
- Partner has at least one incomplete onboarding step

**Modal content:**
- Title: "Complete Your Profile To Start Earning"
- Supporting text: "You're just a step away from unlocking your Back Office and getting paid."
- Dynamic list of incomplete steps with clear labels:
  - Missing DOB → "Add your Date of Birth"
  - Missing SSN → "Add your SSN"
  - Missing Bank Info → "Add bank details"
- Primary button: Takes user to Settings page to complete info
- Close/dismiss icon to skip for now

**Behavior:**
- Modal appears on each login until onboarding is complete
- Dismissing the modal does not block access to the Back Office

### Designs

[Link to Figma designs]

### Risks & Unknowns

- Should we limit how often the modal appears? (e.g., once per day vs. every login)
- What happens if a Partner dismisses repeatedly — do we escalate messaging?
- Are there any steps that should block Back Office access entirely?
```

## Design Thinking

When shaping, consult [references/software-design-philosophy.md](references/software-design-philosophy.md) for principles that help define work in ways that avoid unnecessary complexity. Key lenses: define errors out of existence, design the common case to be simple, flag information leakage risks.

## What NOT to include

- Technical implementation details (database schemas, API designs, code patterns)
- Time estimates or sprint planning
- Assigned developers or teams
- Detailed test cases (those come later)

Keep it focused on *what* needs to exist and *why*, not *how* to build it.

## Handoffs

- If the work is clearly too large for a single ticket, note that in Risks & Unknowns and suggest running `/dev-skills:backlog-grooming` to decompose it.
- Shaped work feeds into `/dev-skills:implementation-planning` for technical design.
