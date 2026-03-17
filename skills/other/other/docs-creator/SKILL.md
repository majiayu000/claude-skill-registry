---
name: docs-creator
description: "Create and generate documentation for software projects including READMEs, API documentation, Javadoc (Java), and TSDoc (TypeScript). Use when: (1) Creating or updating README files, (2) Documenting REST APIs with endpoints and examples, (3) Adding or generating Javadoc comments for Java code, (4) Adding or generating TSDoc comments for TypeScript code, (5) User asks to document this code or add docs or generate documentation."
---

# Docs Creator

Generate concise, scannable documentation with code examples.

## Quick Reference

| Task | Reference |
|------|-----------|
| README files | [readme-patterns.md](references/readme-patterns.md) |
| REST API docs | [api-docs.md](references/api-docs.md) |
| Java comments | [javadoc.md](references/javadoc.md) |
| TypeScript comments | [tsdoc.md](references/tsdoc.md) |

## Workflow

### 1. Identify Documentation Type

Determine what the user needs:
- **README** → Project overview, setup, usage
- **API docs** → Endpoints, parameters, responses
- **Code comments** → Javadoc/TSDoc for functions, classes, interfaces

### 2. Analyze Existing Code

When documenting existing code:
1. Read the file(s) to understand purpose and interface
2. Identify public APIs, exported functions, key types
3. Note parameters, return types, exceptions
4. Check for existing documentation to preserve/update

### 3. Generate Documentation

Apply the appropriate pattern from references.

**For READMEs:**
- Start with template: [README-template.md](assets/README-template.md)
- Focus on: Setup → Usage → API/Configuration
- Omit: Lengthy intros, tutorials, changelogs

**For API docs:**
- Start with template: [API-template.md](assets/API-template.md)
- Document: Method, path, parameters, request/response, errors
- Include: curl example for each endpoint

**For code comments:**
- First sentence summarizes action ("Creates...", "Finds...")
- Document parameters only if purpose isn't obvious
- Always document return values
- Document all thrown exceptions

## Auto-Generation

When asked to "document this code" or "add docs":

1. **Scan for undocumented items** - Find functions/methods without comments
2. **Preserve existing docs** - Don't overwrite unless asked
3. **Generate based on signatures** - Use parameter names, types, return types
4. **Match language convention** - Javadoc for Java, TSDoc for TypeScript

### Javadoc Pattern
```java
/**
 * {Action verb} {what it does}.
 *
 * @param {name} {description}
 * @return {description}
 * @throws {Type} {when}
 */
```

### TSDoc Pattern
```typescript
/**
 * {Action verb} {what it does}.
 *
 * @param {name} - {description}
 * @returns {description}
 */
```

## Style Guidelines

- **Concise**: Minimal prose, maximum code examples
- **Scannable**: Use tables, bullet lists, code blocks
- **Actionable**: Copy-paste ready commands and examples
- **Consistent**: Match existing documentation style in project
