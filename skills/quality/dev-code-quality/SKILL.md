---
name: dev-code-quality
description: Code Quality Standards. Use it everytime you plan or implement any code.
---

# Universal Code Quality Standards

## Naming Conventions (adapt to language case style)

- Classes/Types: nouns that represent concepts
- Functions/Methods: verbs that describe actions
- Booleans: questions (is/has/can/should)
- Constants: descriptive, not abbreviated
- Avoid: abbreviations, single letters (except i,j for loops), mental mapping

## Function Design

- Single responsibility
- Maximum 3-4 parameters
- One level of abstraction
- No side effects unless name indicates
- Early returns for guard clauses
- Pure functions when possible

## Code Organization

- Group related code together
- Order: public before private
- Most important/high-level code first
- Dependencies at top

## Comments

- Why, not what (code explains what)
- Explain non-obvious business rules
- Document gotchas and workarounds
- Keep comments updated with code
- Prefer self-documenting code over comments

## Error Handling

- Fail fast, fail clearly
- Specific error types
- Include context in error messages
- Don't swallow exceptions
- Log appropriately

## Magic Numbers

- Extract to named constants
- Explain the meaning, not just the value
