---
name: atlas-documentation
description: >
  AI-friendly documentation generation for Java services following RFC-37 standards.
  Covers documentation structure, templates, change detection, and RAG optimization.
  Use when generating or updating service documentation.
compatibility: Java services following Bitso patterns
metadata:
  version: "1.0.0"
  technology: global
  category: documentation
  tags:
    - documentation
    - rfc-37
    - atlas
    - rag
---

# Atlas Documentation

AI-friendly documentation generation for Java services following RFC-37 standards.

## When to use this skill

- Generating documentation for new services
- Updating documentation after code changes
- Setting up documentation structure for a repository
- Creating feature and concept documentation
- Integrating with RAG systems

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L23-L30)
- [Quick Start](#quick-start) (L52-L88)
- [Documentation Structure](#documentation-structure) (L89-L126)
- [Change Detection](#change-detection) (L127-L150)
- [References](#references) (L151-L159)
- [Related Skills](#related-skills) (L160-L167)

### Available Resources

**📚 references/** - Detailed documentation
- [atlas mcp usage](references/atlas-mcp-usage.md)
- [documentation workflow](references/documentation-workflow.md)
- [templates](references/templates.md)
- [troubleshooting](references/troubleshooting.md)

---

## Quick Start

### 1. Identify Services

Scan `bitso-services/` directory for deployable services:

```bash
ls -d bitso-services/*/
```

Each subdirectory is a separate service to document.

### 2. Create Documentation Structure

```plaintext
docs/
├── README.md                    # Repository overview
└── <service-name>/              # One folder per service
    ├── overview.md              # Business purpose
    ├── architecture.md          # Dependencies, data flow
    ├── concepts/                # Domain concepts
    │   └── <concept>.md
    └── features/                # Feature documentation
        └── <feature>.md
```

### 3. Use Templates

Apply RFC-37 templates from `references/templates.md` or refer to the comprehensive [rfc-37-documentation](../rfc-37-documentation/SKILL.md) skill for:
- Directory structure requirements
- Confluence metadata configuration
- Documentation linting and validation

### 4. Run with Idempotency

Only update documentation when code changes. Check existing docs first.

## Documentation Structure

### Service-Specific Focus

Document only service-specific information:

✅ **Document**:
- Business purpose and domain concepts
- Service architecture and dependencies
- Features and use cases
- gRPC APIs and contracts
- Data models (PostgreSQL, Redis)

❌ **Don't Document** (covered in platform docs):
- General local development setup
- Testing patterns
- Monitoring and logging
- Standard architecture patterns
- Deployment processes

### Folder Structure

```plaintext
docs/
├── api/                         # Human-managed
├── decisions/                   # Human-managed
├── runbooks/                    # Human-managed
└── <service-name>/              # AI-managed
    ├── overview.md
    ├── architecture.md
    ├── concepts/
    │   ├── <concept-1>.md
    │   └── <concept-2>.md
    └── features/
        ├── <feature-1>.md
        └── <feature-2>.md
```

## Change Detection

### Idempotency Rules

1. **Only update when code changes**
2. **Preserve existing content if accurate**
3. **Don't rewrite just to rephrase**
4. **Don't change formatting if content is accurate**

### What Constitutes a Change

**UPDATE documentation when**:
- New features or concepts added
- Architecture changes
- API contracts change
- Database schema changes
- Business rules change

**DON'T update when**:
- Code formatting changes
- Variable names change but behavior is same
- Tests modified but functionality unchanged
- Internal refactoring without API changes

## References

| Reference | Description |
|-----------|-------------|
| [references/atlas-mcp-usage.md](references/atlas-mcp-usage.md) | MCP queries for Atlas |
| [references/documentation-workflow.md](references/documentation-workflow.md) | Full generation workflow |
| [references/templates.md](references/templates.md) | RFC-37 document templates |
| [references/troubleshooting.md](references/troubleshooting.md) | Common issues and solutions |

## Related Skills

| Skill | Purpose |
|-------|---------|
| [rfc-37-documentation](../rfc-37-documentation/SKILL.md) | RFC-37 standards, validation rules, Confluence config |
| [doc-sync](../doc-sync/SKILL.md) | Documentation synchronization with code |

> **Note**: For RFC-37 compliance validation and Confluence mirroring setup, use the `rfc-37-documentation` skill. This skill focuses on AI-assisted content generation using Atlas MCP.
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/atlas-documentation/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

