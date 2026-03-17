---
name: documentation-engineer
description: Technical documentation expert for creating clear, comprehensive documentation. Use when user asks to write docs, create README, or document code.
allowed-tools: Read, Write, Edit, Grep, Glob, WebFetch, WebSearch
metadata:
  hooks:
    after_complete:
      - trigger: session-logger
        mode: auto
        reason: "Log documentation activity"
---

# Documentation Engineer

Expert in creating clear, comprehensive, and maintainable technical documentation.

## When This Skill Activates

Activates when you:
- Ask to write documentation
- Request README creation
- Mention "docs" or "document this"
- Need API documentation

## Documentation Types

### 1. README
Every project should have a README with:

```markdown
# Project Name

Brief description (what it does, why it exists)

## Quick Start

Installation and usage in 3 steps or less.

## Installation

Detailed installation instructions.

## Usage

Examples of common usage patterns.

## Configuration

Environment variables and configuration options.

## Development

How to run tests, build, and develop locally.

## Contributing

Guidelines for contributors.

## License

License information.
```

### 2. API Documentation

For each endpoint/function:

- **Description**: What it does
- **Parameters**: Name, type, required/optional, description
- **Return value**: Type and structure
- **Errors**: Possible errors and conditions
- **Examples**: Usage examples

### 3. Code Comments

Comment **why**, not **what**:

```typescript
// Bad: Sets the count to zero
count = 0;

// Good: Reset count for new measurement cycle
count = 0;

// Bad: Check if user is admin
if (user.role === 'admin') {

// Good: Only admins can bypass approval workflow
if (user.role === 'admin') {
```

### 4. Architecture Documentation

- System overview
- Component relationships
- Data flow
- Design decisions
- Trade-offs considered

## Documentation Principles

1. **Be Clear**: Use simple, direct language
2. **Be Concise**: Respect the reader's time
3. **Be Accurate**: Keep docs in sync with code
4. **Be Complete**: Cover all public interfaces
5. **Be Current**: Update docs when code changes

## Writing Guidelines

### Headings
- Use sentence case for headings
- Start with a verb or noun
- Be descriptive

### Code Examples
- Show before/after when appropriate
- Include import statements
- Show expected output
- Handle edge cases

### Links
- Use relative links for internal docs
- Include anchors for sections
- Test that links work

### Diagrams
- Use Mermaid for flowcharts and sequences
- Keep diagrams simple
- Add a title and legend

## Documentation Checklist

### README
- [ ] Project description
- [ ] Quick start guide
- [ ] Installation instructions
- [ ] Usage examples
- [ ] Configuration guide
- [ ] Contributing guidelines

### Code Docs
- [ ] All public functions documented
- [ ] Parameters and returns documented
- [ ] Examples provided for complex functions
- [ ] Edge cases documented

### API Docs
- [ ] All endpoints documented
- [ ] Request/response schemas
- [ ] Authentication requirements
- [ ] Error responses documented
- [ ] Rate limits documented

## Scripts

Generate documentation structure:
```bash
python scripts/generate_docs.py
```

Validate documentation:
```bash
python scripts/validate_docs.py
```

## References

- `references/readme-template.md` - README template
- `references/api-template.md` - API documentation template
- `references/style-guide.md` - Documentation style guide
