---
name: write-reference
description: >
  Create information-oriented documentation for lookup and reference.
  PROACTIVELY activate for: (1) API documentation, (2) configuration reference,
  (3) glossaries and terminology, (4) technical specifications, (5) parameter documentation.
  Triggers: "write reference", "create reference docs", "API documentation", "config reference",
  "document parameters", "glossary", "specification"
argument-hint: [api, system, or configuration to document]
---

# Write Reference

Generate information-oriented documentation optimized for quick lookup and accuracy.

## When to Use

Use this skill when you need documentation that:
- Provides accurate, complete information for lookup
- Describes APIs, configurations, or system parameters
- Serves as authoritative source of truth
- Is structured for quick scanning and finding

## Workflow

Invoke the `create-documentation` skill for: "$ARGUMENTS"

### Parameters to Apply

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `doc_type` | reference | Information-oriented, lookup-focused |
| `persona` | developer | Technical reader seeking specific answers |
| `reading_level` | professional | Technical accuracy over accessibility |
| `include_examples` | true | Examples clarify usage |
| `validation_depth` | comprehensive | Reference docs must be accurate |

### Required Elements

1. **Consistent structure** - Every entry follows the same format
2. **Complete coverage** - All items documented, no gaps
3. **Self-contained entries** - Each entry understandable in isolation
4. **Accurate types/constraints** - Precise technical specifications
5. **Default values documented** - What happens if not specified
6. **Examples for each item** - Concrete usage demonstrations

### Cognitive Load Management

- **Intrinsic**: Accept it - readers are technical professionals
- **Extraneous**: Minimize - no unnecessary prose, consistent format
- **Germane**: Focus on - examples, edge cases, gotchas

### Reference Documentation Patterns

**API Endpoint Pattern:**
```markdown
### `POST /api/v1/resource`

Create a new resource.

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Resource name (max 255 chars) |
| config | object | No | Configuration options |

**Response:**
| Status | Description |
|--------|-------------|
| 201 | Created successfully |
| 400 | Validation error |
| 401 | Unauthorized |

**Example:**
\`\`\`bash
curl -X POST /api/v1/resource \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "example"}'
\`\`\`
```

**Configuration Parameter Pattern:**
```markdown
### `max_connections`

Maximum number of simultaneous connections.

| Property | Value |
|----------|-------|
| Type | integer |
| Default | 100 |
| Range | 1-10000 |
| Environment | `APP_MAX_CONNECTIONS` |

**Behavior:**
- Values below 10 may cause timeouts under load
- Values above 1000 require tuning OS limits

**Example:**
\`\`\`yaml
database:
  max_connections: 500
\`\`\`
```

**Glossary Entry Pattern:**
```markdown
### Term Name

**Definition:** One-sentence definition.

**Context:** Where/when this term is used.

**Related:** [Link to related terms]

**Example:** Usage in a sentence.
```

## Output Format

The generated reference should follow this structure:

```markdown
# [System/API/Configuration] Reference

> Version: [version] | Last updated: [date]

## Overview

[Brief context - what this documents and when to use it]

## Quick Reference

[Table or list of all items for scanning]

## Detailed Reference

### [Category 1]

#### `item_name`

[Consistent documentation following pattern]

### [Category 2]

#### `item_name`

[Same pattern repeated]

## Common Patterns

[Frequently used combinations or configurations]

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|

## Changelog

| Version | Changes |
|---------|---------|
```

## Quality Gates

- [ ] Every item follows consistent format
- [ ] No missing items (complete coverage)
- [ ] Types and constraints accurate
- [ ] Default values documented
- [ ] Examples provided for each item
- [ ] Self-contained entries (no assumed context)
- [ ] Quick reference table for scanning
- [ ] Version and update date included

## Documentation Type Selection Guide

| Need | Doc Type | Skill |
|------|----------|-------|
| Teach a concept | Tutorial | `/write-tutorial` |
| Help accomplish task | How-To | `/write-howto` |
| Explain why/how | Explanation | (use create-documentation directly) |
| Look up information | Reference | `/write-reference` |

## Related Skills

After creating reference documentation, consider:
- Run `/write-tutorial` for onboarding new users
- Run `/write-howto` for common tasks
- Run `/optimize-prompt` if documenting AI/prompting features
