---
name: code-generation
description: Use go:generate effectively - mockgen, stringer, templates, reducing boilerplate
category: Code Quality
---

# Skill: code-generation

## What I do

I provide expertise in using Go's `generate` tool to automate the creation of boilerplate code. I focus on standard tools like `mockgen`, `stringer`, and custom template-based generation to improve maintainability and reduce manual coding.

## When to use me

- When adding or updating interface definitions that require new mocks
- When working with enums that need string representation methods
- When implementing repetitive patterns that can be automated via templates

## Core principles

1. **Automate repetitive tasks**: Use generation for code that follows a predictable pattern.
2. **Explicit directives**: Place `//go:generate` directives in the files where the source material is defined.
3. **Consistency**: Ensure generated code follows project style and passes all linting checks.
4. **Visibility**: Use standard file naming (e.g., `_string.go`, `_mock.go`) to distinguish generated files from manual ones.

## Patterns & examples

**Using stringer for enums:**
```go
//go:generate stringer -type=Status
type Status int

const (
    Unknown Status = iota
    Pending
    Active
)
```

**Using mockgen for interfaces:**
```go
//go:generate mockgen -destination=mocks/user_repo.go -package=mocks . UserRepository
type UserRepository interface {
    Get(id int) (*User, error)
}
```

**Custom template-based generation:**
Create a small Go tool that uses the `text/template` package to generate code from a source definition, then trigger it with `//go:generate go run generator.go`.

**Running generation:**
Run `go generate ./...` from the project root to update all generated files.

## Anti-patterns to avoid

- ❌ **Manual editing**: Never edit a generated file. Changes will be overwritten next time `go generate` runs.
- ❌ **Ignoring generated files**: Generated code should generally be committed to version control so consumers don't need to install all generation tools.
- ❌ **Too much generation**: Don't over-engineer solutions. Only generate code when manual maintenance is demonstrably costly or error-prone.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Code-Quality/Code Generation.md`

## Related skills

- `golang`: For idiomatic patterns and template usage
- `gomock`: Specifics of using the GoMock generation tools
- `automation`: For integrating generation into CI/CD pipelines
