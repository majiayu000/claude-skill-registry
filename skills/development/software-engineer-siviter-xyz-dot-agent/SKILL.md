---
name: software-engineer
description: Core software engineering principles for code style, documentation, and development workflow. Applies when editing code, working in software repositories, or performing software development tasks.
---

# Software Engineering Principles

Core principles and preferences for code style, documentation, and development workflow.

## Code Style and Patterns

- **Avoid unnecessary comments**: Code should be self-documenting. Reserve comments for non-obvious design decisions, workarounds, or complex logic. Avoid comments that restate what the code obviously does.

- **Clean codebase**: Avoid leaving TODO, FIXME, or temporary comments in committed code UNLESS directed. Either implement the feature, create an issue, or remove the comment. Ignore existing ones.

- **Self-documenting code**: Prefer clear naming and structure over explanatory comments. Method, class, and member documentation should use language/stack best practices. Don't add useless inline comments next to statements UNLESS they explain
confusing or complex behaviour.

## Documentation

- **Concise and useful**: Documentation should be informative but not verbose. READMEs should focus on essential information without unnecessary elaboration.

- **Structure over verbosity**: Prefer well-organized, scannable documentation with clear headings over long paragraphs. Use short examples to illustrate concepts.

## Development Workflow

- **Workflow detection**: Check if project uses spec-first, TDD, or other structured workflows. Look for:
  - `docs/` or `specs/` directories with specs
  - Test-first patterns in codebase
  - Plan files or structured documentation
  - Follow existing workflow patterns when present

- **No git modifications**: Do not use Git commands that modify the repository state (such as `git add`, `git commit`, `git push`) UNLESS directed. Focus on code edits directly. Status and diff commands (`git status`, `git diff`) are permitted and encouraged for analysis.

- **Fact-based approach**: Do not hallucinate or assume. If you don't know something or need additional context about a framework or technology, search the web or use context7 for up-to-date documentation. If clarification is needed, ask the user before making changes.

- **Constructive disagreement**: Do not just accept user direction if a better alternative exists. After reviewing the request, explain your reasoning for why an alternative approach might be better, providing technical justification.

- **Stop and ask**: Stop and ask user if:
  - Uncertain how to proceed
  - About to add type ignores, suppressions, or `any` types
  - Requirements are unclear
  - Better approach exists but needs confirmation

- **Backward compatibility**: Only consider backward compatibility for public-facing interfaces (APIs, libraries). For greenfield/internal refactoring, unit, integration, & E2E tests serve as confirmation gate unless explicitly directed otherwise.

## Code Organization

- **Single responsibility**: Components and functions should have a single, clear purpose. Organize code into logical directories with clear separation of concerns.

- **Consistent patterns**: Follow established patterns in the codebase. When introducing new patterns, ensure they align with existing architecture and conventions.

- **Automation and efficiency**: Prefer automated solutions and efficient workflows. Look for opportunities to reduce manual work and improve developer experience.

## Output Formatting

- **No emojis**: Do not use emojis in code or output unless explicitly directed
- **Unicode symbols**: Unicode symbols (✓, ✗, →, ⚠) are acceptable for user-facing output
- **Color and formatting**: Color and formatting encouraged for user-facing output
- **NO_COLOR support**: Always respect `NO_COLOR` environment variable
- **No hardcoded ANSI**: Never use hardcoded ANSI color codes - use color libraries (chalk, colors, etc.)

## Best Practices

- **Framework conventions**: Follow framework and language best practices. Use framework features as intended rather than working around them.

- **Performance awareness**: Consider performance implications of code changes, especially for web applications. Prefer static generation and minimal JavaScript when possible.

- **Accessibility**: Ensure code is accessible by default. Use semantic HTML, proper ARIA attributes, and test keyboard navigation.

## References

For detailed guidance, see:
- `references/workflow-patterns.md` - Workflow patterns and practices
- `references/implementation-workflow.md` - Unified implementation workflow
