---
name: style-guide
description: Style guide enforcement and documentation conventions
category: Code Quality
---

# Skill: style-guide

## What I do

I help you maintain a consistent and readable codebase by enforcing coding standards and documentation conventions. I focus on making the code easy for any team member to understand and modify. I ensure that your style guide is a living document that improves the quality of every commit.

## When to use me

- When you're setting up a new project and defining its coding standards.
- When you're configuring linters or formatting tools.
- When you're reviewing code for naming and formatting consistency.
- When you're writing documentation or comments.

## Core principles

1. **Automate enforcement**, use tools like linters and formatters to catch style issues automatically.
2. **Naming clarity**, choose descriptive names for variables, functions, and files that reveal their purpose.
3. **Consistent formatting**, ensure that all code looks like it was written by a single person.
4. **Purposeful comments**, write comments that explain the "why" rather than the "what".

## Patterns & examples

### Linter configuration
Use industry-standard tools for automated checks.
- **Go**, Use `golangci-lint` with a comprehensive `.golangci.yml` configuration.
- **JavaScript**, Use `ESLint` with a shared config like Airbnb or Standard.

### Naming conventions
Follow language-specific idioms.
- **Go**, Use camelCase for internal symbols and PascalCase for exported symbols. Keep names concise.
- **JavaScript**, Use camelCase for variables and functions, PascalCase for classes and components.

### Comment style
Use standard formats for automated documentation.
- **Go**, Use `godoc` style comments for exported functions.
- **JavaScript**, Use `JSDoc` for providing type and purpose information in untyped files.

### Import ordering
Organise imports to reduce noise.
- **Pattern**, Group standard library imports, then third-party libraries, then internal modules. Separate groups with a blank line.

## Anti-patterns to avoid

- ❌ **Style disagreements over logic**, spending too much time arguing about trivial style details instead of meaningful code improvements.
- ❌ **Inconsistent names**, using multiple naming patterns for the same concept across the project.
- ❌ **Useless comments**, comments that just restate what the code is doing without providing context.
- ❌ **Ignoring linter warnings**, allowing linter errors to accumulate until they are ignored by everyone.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Code-Quality/Style Guide.md`

## Related skills

- `clean-code`, for broader coding best practices.
- `static-analysis`, for automated quality checks.
- `documentation-writing`, for better comments and guides.
- `writing-style`, for a consistent tone in docs.
