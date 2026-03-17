---
name: reference-documentation
description: >-
  Create exhaustive technical references, API documentation, and searchable
  reference materials. Use when building API docs, configuration references,
  or complete technical specifications.
version: 1.0.0
tags: [documentation, reference, api, specification]
triggers:
  - API documentation
  - reference docs
  - configuration reference
  - technical specification
  - schema documentation
  - parameter reference
dependencies:
  skills: [documentation-production]
  tools: [Read, Write, Grep, Glob]
token_estimate: ~2500
---

# Reference Documentation

Create exhaustive, searchable, and precisely organized technical reference documentation
that serves as the definitive source of truth for APIs, configurations, and system interfaces.

## When to Use This Skill

- Building API reference documentation (REST, GraphQL, gRPC)
- Creating configuration guides with every parameter documented
- Writing schema documentation for databases or data models
- Producing CLI reference with all commands, flags, and examples
- Generating complete technical specifications
- Documenting error codes, status codes, and exception catalogs
- Creating migration guides for version upgrades

## Quick Reference

| Resource | Purpose | Load when |
|----------|---------|-----------|
| `references/documentation-patterns.md` | API doc structure, glossary patterns, cross-referencing, versioned docs, parameter tables, configuration guides | Structuring any reference document |

---

## Workflow Overview

```
Phase 1: Inventory    → Catalog all public interfaces, parameters, and constraints
Phase 2: Author       → Draft structured entries with examples and cross-links
Phase 3: Verify       → Validate against implementation and tests
Phase 4: Organize     → Structure for optimal retrieval and searchability
Phase 5: Maintain     → Version tracking, deprecation, and update cadence
```

---

## Phase 1: Inventory

Enumerate everything that needs documentation before writing anything.

### Inventory Checklist

- [ ] All public API endpoints / methods / functions
- [ ] All configuration parameters and their defaults
- [ ] All error codes and exception types
- [ ] All environment variables
- [ ] All CLI commands and flags
- [ ] All schema fields and constraints
- [ ] All event types and payloads
- [ ] Deprecation timeline for removed features

### Source of Truth Priority

1. Implementation code (actual behavior)
2. Tests (expected behavior with assertions)
3. Type definitions / schemas (declared contracts)
4. Existing documentation (may be stale — verify)

---

## Phase 2: Author

### Entry Format

Every documented item uses a consistent structure:

```markdown
### methodName

**Type**: `(param1: string, param2?: number) => Promise<Result>`
**Since**: v2.1.0
**Deprecated**: No

**Description**:
Brief explanation of purpose and behavior.

**Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `param1` | `string` | Yes | — | What this parameter controls |
| `param2` | `number` | No | `10` | What this parameter controls |

**Returns**: `Promise<Result>` — description of return value

**Throws**:
- `ValidationError` — when param1 is empty
- `TimeoutError` — when operation exceeds 30s

**Examples**:

Basic usage:
\`\`\`typescript
const result = await methodName("value");
\`\`\`

With options:
\`\`\`typescript
const result = await methodName("value", 20);
\`\`\`

**See Also**: [relatedMethod](#relatedmethod), [Configuration Guide](#configuration)
```

### Writing Rules

1. **Document behavior, not implementation** — what it does, not how
2. **Every parameter gets a row** — no exceptions, even obvious ones
3. **Every entry gets an example** — at least one working code sample
4. **State constraints explicitly** — valid ranges, length limits, format requirements
5. **Cross-reference related items** — link to related methods, configs, and error codes

---

## Phase 3: Verify

### Verification Methods

| What to verify | How |
|---------------|-----|
| Method signatures | Compare against source code type definitions |
| Default values | Check source code initializers |
| Error conditions | Read implementation and test assertions |
| Examples | Run them or trace them against the code |
| Deprecated items | Check for deprecation markers in source |

### Accuracy Checklist

- [ ] All signatures match current implementation
- [ ] All default values are correct
- [ ] All error conditions are documented
- [ ] All examples work against current version
- [ ] No removed features are still documented
- [ ] No new features are undocumented

---

## Phase 4: Organize

### Document Hierarchy

```
1. Overview          — What this API/system does, quick orientation
2. Quick Reference   — Cheat sheet of common operations with examples
3. Authentication    — How to authenticate (if applicable)
4. Detailed Reference — Complete documentation, grouped logically
5. Error Reference   — All error codes with causes and fixes
6. Glossary          — Terms specific to this system
7. Changelog         — What changed in each version
```

### Navigation Aids

- **Table of contents** with deep linking at the top
- **Alphabetical index** for large reference sets
- **Category grouping** for logical discovery
- **Search keywords** embedded in headings and descriptions
- **Version badges** on entries added or changed in recent versions

---

## Phase 5: Maintain

### Versioning Strategy

- Tag every entry with the version it was introduced (`**Since**: v2.1.0`)
- Mark deprecations with migration guidance (`**Deprecated**: v3.0 — use newMethod instead`)
- Maintain a changelog section at the bottom of reference docs
- Separate docs by major version when breaking changes accumulate

### Update Triggers

Reference documentation must be updated when:
- A public API signature changes
- A new parameter, endpoint, or command is added
- Default values or constraints change
- Features are deprecated or removed
- Error codes or behaviors change

---

## Content Patterns

### Parameter Tables

Always use tables for parameters — never inline lists:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `timeout` | `number` | No | `30000` | Request timeout in milliseconds |
| `retries` | `number` | No | `3` | Number of retry attempts |

### Status Code Tables

| Code | Name | Description | Resolution |
|------|------|-------------|------------|
| `400` | Bad Request | Invalid input parameters | Check request body against schema |
| `401` | Unauthorized | Missing or invalid auth token | Re-authenticate and retry |
| `429` | Rate Limited | Too many requests | Back off and retry after `Retry-After` header |

### Configuration Blocks

```yaml
# config.yaml
server:
  port: 3000          # Port to listen on (1024-65535)
  host: "0.0.0.0"     # Bind address
  timeout: 30000      # Request timeout in ms
  max_body_size: "1mb" # Maximum request body size
```

## Anti-Patterns

- Documenting internal/private interfaces that can change without notice
- Using "obvious" or "self-explanatory" instead of writing a real description
- Omitting error documentation because "it's clear from the types"
- Copy-pasting examples without verifying they still work
- Mixing tutorial-style narrative into reference entries (keep them separate)
- Letting documentation fall behind implementation for more than one release
