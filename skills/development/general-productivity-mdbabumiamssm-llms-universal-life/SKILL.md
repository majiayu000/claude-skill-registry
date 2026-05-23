---
name: code-reviewer
description: Provides comprehensive code review feedback based on best practices, style guides, and potential bug detection. Use when the user requests a code review, asks for improvements to code, or needs to ensure code quality.
license: MIT
metadata:
  author: Agent Skills Community
  version: "1.1.0"
compatibility:
  - product: VS Code
  - product: Claude Desktop
  - system: Python 3.9+
allowed-tools:
  - read_file
  - run_shell_command
---

# Code Review Skill

This skill helps to perform thorough code reviews, focusing on readability, maintainability, performance, security, and adherence to project-specific coding standards.

## When to Use This Skill

*   When a user explicitly asks for a "code review" of a file or set of files.
*   When a user asks to "improve the quality" or "refactor" a piece of code.
*   When a user submits code and asks for "feedback" or "suggestions".

## Core Capabilities

1.  **Syntax and Style Check**: Verify adherence to established coding standards (e.g., PEP 8 for Python, ESLint rules for JavaScript).
2.  **Best Practices**: Identify deviations from common best practices for the given language/framework.
3.  **Potential Bugs/Errors**: Highlight common pitfalls, edge cases, or logical errors.
4.  **Performance Optimization**: Suggest areas where code could be made more efficient.
5.  **Security Vulnerabilities**: Point out potential security risks.
6.  **Readability and Maintainability**: Provide feedback on code clarity, comments, variable naming, and overall structure.
7.  **Testability**: Assess if the code is easily testable and suggest improvements.

## Workflow

1.  **Identify Scope**: Determine which files or code snippets are part of the review request.
2.  **Read Code**: Use `read_file` to access the content of the specified files.
3.  **Analyze**:
    *   Apply language-specific linting/static analysis tools if available (e.g., `pylint`, `flake8`, `eslint`).
    *   Perform a semantic analysis based on the description and context.
    *   Cross-reference with project-specific style guides or documentation if linked in `references/`.
4.  **Generate Feedback**:
    *   Structure feedback clearly, categorizing by type (e.g., "Style", "Potential Bug", "Suggestion").
    *   Provide specific line numbers or code snippets for each piece of feedback.
    *   Explain *why* a change is suggested and, if possible, offer a concrete example of how to fix it.
    *   Prioritize critical issues (bugs, security) over stylistic suggestions.
5.  **Present Review**: Output the comprehensive review to the user.

## Example Usage

**User Prompt**: "Please review `src/main.py` for any issues."

**Agent Action**:
1.  `read_file("src/main.py")`
2.  Run `pylint src/main.py` (if configured).
3.  Analyze code content.
4.  Generate a markdown-formatted review with findings.
