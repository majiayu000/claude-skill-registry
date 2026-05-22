---
name: confluence-docs
description: Documentation templates for ADRs, runbooks, and architecture docs. Use when creating architectural decision records, operational runbooks, or technical documentation.
---

# Confluence Documentation Skill

## Purpose

Provide standardized templates for creating technical documentation. These templates ensure consistent, high-quality documentation across the project.

## When This Skill Applies

- Creating Architecture Decision Records (ADRs)
- Writing operational runbooks
- Documenting system architecture
- Creating technical specifications
- Writing knowledge transfer (KT) documents

## Existing ADRs (Reference)

| ADR     | Location                                                   | Topic                     |
| ------- | ---------------------------------------------------------- | ------------------------- |
| ADR-002 | `docs/adr/ADR-002-constants-unification.md`                | Constants organization    |
| ADR-003 | `docs/adr/ADR-003-dependency-upgrade-typescript-fixes.md`  | Dependency upgrades       |
| ADR-004 | `docs/adr/ADR-004-server-component-data-access-pattern.md` | Server component patterns |
| ADR-005 | `docs/adr/ADR-005-ci-infrastructure-services.md`           | CI infrastructure         |
| ADR-006 | `docs/adr/ADR-006-bonus-pdf-private-bucket-security.md`    | Security patterns         |
| ADR-007 | `docs/adr/ADR-007-rendertrust-marketing-pages.md`          | Marketing architecture    |

## ADR Template (Architecture Decision Record)

```markdown
# ADR-XXX: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded]

## Context

What is the issue that we're seeing that motivates this decision?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

### Positive

- [Benefit 1]
- [Benefit 2]

### Negative

- [Tradeoff 1]
- [Tradeoff 2]

### Neutral

- [Observation]

## Implementation Notes

How should this decision be implemented?

## Related Decisions

- ADR-XXX: [Related decision]

## References

- [Link to relevant documentation]
```

## Runbook Template

```markdown
# Runbook: [Operation Name]

## Overview

Brief description of what this runbook covers.

## Prerequisites

- [ ] Access to [system]
- [ ] Required permissions
- [ ] Tools installed

## Procedure

### Step 1: [Action Name]

\`\`\`bash

# Command to execute

\`\`\`

**Expected output**: Description of what you should see

**If error**: What to do if something goes wrong

### Step 2: [Action Name]

...

## Verification

How to verify the operation was successful.

## Rollback

Steps to undo the operation if needed.

## Troubleshooting

### Issue: [Common problem]

**Symptoms**: What you see
**Cause**: Why it happens
**Solution**: How to fix it

## Contacts

- Primary: [Name/Role]
- Escalation: [Name/Role]

## Revision History

| Date       | Author | Changes         |
| ---------- | ------ | --------------- |
| YYYY-MM-DD | Name   | Initial version |
```

## Architecture Document Template

```markdown
# [System/Component] Architecture

## Overview

High-level description of the system/component.

## Goals and Non-Goals

### Goals

- [What this system should do]

### Non-Goals

- [What this system should NOT do]

## Architecture Diagram

\`\`\`
[ASCII diagram or link to diagram]
\`\`\`

## Components

### Component 1: [Name]

- **Purpose**: What it does
- **Location**: Where it lives
- **Dependencies**: What it needs

### Component 2: [Name]

...

## Data Flow

How data moves through the system.

## Security Considerations

- Authentication
- Authorization (RLS)
- Data protection

## Performance Considerations

- Caching strategy
- Database optimization
- API response times

## Monitoring and Observability

- Key metrics
- Alerting thresholds
- Log locations

## Future Considerations

What might change or be improved.

## References

- Related ADRs
- External documentation
```

## Knowledge Transfer (KT) Document Template

```markdown
# KT: [Topic Name] - {TICKET_PREFIX}-XXX

## Summary

What was done and why it matters.

## Context

Background information needed to understand this work.

## Key Decisions Made

1. [Decision 1]: [Reasoning]
2. [Decision 2]: [Reasoning]

## Implementation Details

### What Changed

- File: `path/to/file.ts`
  - Change description

### How It Works

Explanation of the implementation.

## Gotchas and Lessons Learned

Things that might trip up future developers.

## Testing

How to verify everything works.

## Related Tickets

- {TICKET_PREFIX}-XXX: [Related work]

## Future Work

What should be done next.
```

## Documentation Output Locations

| Doc Type       | Location                             | Naming                                 |
| -------------- | ------------------------------------ | -------------------------------------- |
| ADRs           | `docs/adr/`                          | `ADR-XXX-{description}.md`             |
| Runbooks       | `docs/runbooks/`                     | `{operation}-runbook.md`               |
| Architecture   | `docs/architecture/`                 | `{system}-architecture.md`             |
| KT Docs        | `docs/`                              | `KT-{TICKET_PREFIX}-XXX-{topic}.md`    |
| Technical Docs | `docs/agent-outputs/technical-docs/` | `{TICKET_PREFIX}-XXX-{description}.md` |

## Documentation Checklist

Before publishing any documentation:

- [ ] Clear, descriptive title
- [ ] Proper heading hierarchy (H1 > H2 > H3)
- [ ] Code blocks with language tags
- [ ] Links to related documents
- [ ] Author and date included
- [ ] No sensitive data (secrets, passwords)
- [ ] Spell-checked
- [ ] Markdown lint passes
