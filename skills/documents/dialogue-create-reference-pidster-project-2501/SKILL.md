---
name: dialogue-create-reference
description: Create Reference (REF) documents for conceptual models, glossaries, and catalogues. Triggers on "create reference", "document concepts", "make glossary", "catalogue these", "create lookup".
---

# Skill: Create Reference Document

Create REF (Reference) documents that provide structured knowledge for lookup and understanding.

## When to Use

Activate this skill when:
- User wants to document conceptual models or definitions
- Creating a glossary or terminology reference
- Cataloguing related items or documents
- Building structured explanations for future reference

**Trigger phrases:** "create reference", "document concepts", "make glossary", "catalogue these", "create lookup", "reference document", "document terminology"

## Implementation

**Read and follow the `/create-reference` command** at `${CLAUDE_PLUGIN_ROOT}/commands/create-reference.md` for:
- Document type explanation (catalogue vs glossary vs explainer)
- Step-by-step workflow
- Full document template with frontmatter
- Logging integration

The command contains the authoritative implementation details.

## Content Structuring Guidance

When helping populate reference documents:

**For Catalogues:** Use consistent table format:
```markdown
| ID | Name | Description |
|----|------|-------------|
| X-001 | Name | Brief description |
```

**For Glossaries:** Use definition list format:
```markdown
**Term**
: Definition with context and usage notes.
```

**For Explainers:** Build logical sections that scaffold understanding.

## Relationship to Command

| Invocation | Trigger |
|------------|---------|
| `/create-reference` | User explicitly requests |
| This skill | Claude recognises context (trigger phrases above) |

Both use the same implementation. The skill adds autonomous activation based on conversation context.
