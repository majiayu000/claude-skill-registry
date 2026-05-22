---
name: privacy-consent
version: "0.1"
description: >
  [STUB - Not implemented] Privacy compliance with GDPR/CCPA consent management and data minimization.
  PROACTIVELY activate for: [TODO: Define on implementation].
  Triggers: [TODO: Define on implementation]
core-integration:
  techniques:
    primary: ["[TODO]"]
    secondary: []
  contracts:
    input: "[TODO]"
    output: "[TODO]"
  patterns: "[TODO]"
  rubrics: "[TODO]"
---

# Privacy and Consent

> **STUB: This skill is not yet implemented**
>
> This placeholder preserves the documented plugin structure.
> See parent plugin README for planned capabilities.

## Planned Capabilities

- **GDPR Compliance**: Consent management, data subject rights
- **CCPA Compliance**: California Consumer Privacy Act requirements
- **Data Minimization**: Collect only necessary data
- Consent tracking and audit trails
- Cookie consent implementation
- Privacy policy generation guidance

## Critical Pattern

```typescript
// WRONG - track before consent
analytics.init();
analytics.track('page_view');

// CORRECT - check consent first
if (await userConsent.hasAnalyticsConsent()) {
  analytics.init();
  analytics.track('page_view');
}
```

## Implementation Status

- [ ] Core implementation
- [ ] References documentation
- [ ] Output templates
- [ ] Integration tests
