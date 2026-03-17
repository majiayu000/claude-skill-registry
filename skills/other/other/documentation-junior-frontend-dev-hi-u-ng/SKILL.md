---
name: documentation
description: Generate and update documentation from code.
  Use after successful implementation.
---

# Documentation Skill

## Purpose
Maintain accurate, helpful documentation.

## Templates

### README Template
Reference: [templates/readme-template.md](templates/readme-template.md)

### API Documentation Template
Reference: [templates/api-doc-template.md](templates/api-doc-template.md)

### Changelog Template
Reference: [templates/changelog-template.md](templates/changelog-template.md)

## JSDoc Standards

```typescript
/**
 * Brief description of what the function does.
 *
 * @param {string} name - Description of name parameter
 * @param {Options} options - Description of options
 * @returns {Result} Description of return value
 * @throws {ValidationError} When validation fails
 * @example
 * const result = myFunction('test', { flag: true });
 */
function myFunction(name: string, options: Options): Result {
  // ...
}
```

## Documentation Types

### README
- Project overview
- Installation instructions
- Quick start guide
- Configuration options
- Contributing guidelines

### API Documentation
- Endpoint descriptions
- HTTP methods
- Request/response formats
- Authentication requirements
- Error codes

### Code Documentation
- JSDoc/docstrings
- Inline comments (why, not what)
- Type annotations
- Example usage

### Changelog
- Version history
- Breaking changes
- Migration steps
- Deprecation notices

## Documentation Checklist

- [ ] README up to date
- [ ] API endpoints documented
- [ ] Code examples work
- [ ] Changelog updated
- [ ] JSDoc on public APIs
- [ ] Links are valid
- [ ] Spelling/grammar correct

## Documentation Generation

Run: [scripts/generate-docs.py](scripts/generate-docs.py)

## Best Practices

### Do
- Keep examples up to date
- Document breaking changes
- Use consistent formatting
- Include common use cases
- Explain the "why" not just "how"

### Don't
- Document implementation details
- Let examples become stale
- Skip error scenarios
- Use jargon without explanation
- Assume reader knowledge

## Storage Location
Save reports to: `docs/reviews/documentation-{session}.md`
