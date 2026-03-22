---
name: kb-update
description: Safely write and link knowledge to the kb/** directory. Use when storing customer insights, patterns, or durable knowledge extracted from meetings, CRM, or research.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# kb-update (Knowledge Base Update)

Use this Skill when:
- You've extracted durable knowledge worth persisting (customer insight, pattern, playbook)
- The user explicitly asks to store something in the knowledge base
- You need to link new knowledge to existing entities

Do NOT use when:
- The information is transient or already in raw/canon
- You're unsure if the knowledge is stable (ask the user first)

## KB Structure

```
kb/
├── customers/          # One file per customer/company
│   └── {slug}.md
├── insights/           # Reusable observations and patterns
│   └── {slug}.md
├── playbooks/          # Repeatable processes
│   └── {slug}.md
├── decisions/          # Key decisions with rationale
│   └── {slug}.md
└── glossary.md         # Terms and positioning language
```

## Entry Templates

### Customer Entry (`kb/customers/{slug}.md`)

```markdown
---
type: customer
customer_id: {crm_id or null}
company: {company name}
contacts: [{name, role}]
tags: [industry, segment, status]
sources: [canon/meetings/..., canon/crm/...]
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---

# {Company Name}

## Snapshot
One paragraph: who they are, what they care about, current status.

## Timeline
- **{YYYY-MM-DD}**: {event}

## Key Insights
- {insight with link to source}

## Next Best Actions
- [ ] {action}
```

### Insight Entry (`kb/insights/{slug}.md`)

```markdown
---
type: insight
tags: [topic, domain]
sources: [file paths that support this]
confidence: high|medium|low
created: {YYYY-MM-DD}
---

# {Insight Title}

## Observation
What you noticed.

## Evidence
- {source}: {what it showed}

## Implication
What this means for decisions or actions.
```

### Playbook Entry (`kb/playbooks/{slug}.md`)

```markdown
---
type: playbook
tags: [process-type]
triggers: [when to use this]
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---

# {Playbook Title}

## When to Use
Conditions that trigger this playbook.

## Steps
1. {step}
2. {step}

## Checklist
- [ ] {item}

## Examples
Link to past instances where this was applied.
```

### Decision Entry (`kb/decisions/{slug}.md`)

```markdown
---
type: decision
tags: [domain]
status: active|superseded
decided: {YYYY-MM-DD}
superseded_by: {path if applicable}
---

# {Decision Title}

## Context
What prompted this decision.

## Decision
What was decided.

## Rationale
Why this option was chosen.

## Consequences
What this means going forward.
```

## Procedure

### Step 1: Classify the knowledge type
Determine: customer, insight, playbook, decision, or glossary update.

### Step 2: Check for existing entry
```
Glob: kb/{type}s/*.md
Grep: search for company name, topic, or key terms
```
If an entry exists, UPDATE it rather than creating a duplicate.

### Step 3: Generate slug
- Lowercase, hyphens, no special chars
- Customers: `{company-name}` (e.g., `acme-corp`)
- Insights: `{topic-keyword}` (e.g., `pricing-objection-pattern`)
- Playbooks: `{process-name}` (e.g., `discovery-call-prep`)
- Decisions: `{YYYY-MM}-{topic}` (e.g., `2025-01-pricing-model`)

### Step 4: Prepare content
- Use the appropriate template
- Fill `sources` with actual file paths from raw/canon that support this
- Set `created` to today if new, update `updated` if editing
- Keep content concise - link to sources rather than duplicating

### Step 5: Write or edit
- New entry: `Write` to `kb/{type}s/{slug}.md`
- Existing entry: `Edit` to update specific sections
- Always preserve existing content unless explicitly replacing

### Step 6: Cross-link (if applicable)
If this entry relates to other kb entries, add links:
- In customer files: link to relevant insights/decisions
- In insights: link to customers who exhibited the pattern

## Guardrails

- **Never duplicate** - always check for existing entries first
- **Always source** - every fact needs a file path in `sources`
- **Keep it stable** - only store knowledge that won't change next week
- **Respect privacy** - no PII in kb entries; use customer_id references
- **British English** - per house style
