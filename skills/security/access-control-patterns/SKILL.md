---
name: access-control-patterns
version: "0.1"
description: >
  [STUB - Not implemented] Access control auditing with IDOR detection, RBAC/ABAC patterns, and privilege escalation prevention.
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

# Access Control Patterns

> **STUB: This skill is not yet implemented**
>
> This placeholder preserves the documented plugin structure.
> See parent plugin README for planned capabilities.

## Planned Capabilities

- **IDOR Detection**: Identify Insecure Direct Object Reference vulnerabilities
- **RBAC Patterns**: Role-Based Access Control implementation guidance
- **ABAC Patterns**: Attribute-Based Access Control strategies
- **Privilege Escalation Prevention**: Detect and prevent unauthorized privilege elevation
- Ownership verification patterns
- Resource authorization best practices

## Critical Pattern

```typescript
// WRONG - no ownership check
const post = await db.posts.findById(params.id);

// CORRECT - verify ownership
const post = await db.posts.findById(params.id);
if (post.authorId !== session.userId) {
  throw new ForbiddenError();
}
```

## Implementation Status

- [ ] Core implementation
- [ ] References documentation
- [ ] Output templates
- [ ] Integration tests
