---
name: github-issue-creator
description: "Creates well-structured GitHub issues for the MCPSpy project using the gh CLI tool. Use when asked to create issues, report bugs, or document features. Follows conventional naming with feat/chore/fix prefixes and maintains appropriate detail levels."
allowed-tools:
  - Bash(gh issue:*)
---

# GitHub Issue Creator Skill

Automates the creation of well-structured GitHub issues for the MCPSpy project.

## Tools and Usage

Use the `gh issue` CLI tool to create GitHub issues. If the issue body is rather long, write it to a temporary markdown file and use the `gh issue create --body-file <file>` option.

## Issue Naming Convention

- Use standard prefixes: `feat(component):`, `chore:`, `fix(component):`
- Component examples: `library-manager`, `ebpf`, `mcp`, `http`, `output`
- Brackets are optional but recommended for clarity
- Keep titles concise and descriptive

### Examples

- `feat(library-manager): add support for container runtime detection`
- `chore: update dependencies to latest versions`
- `fix(ebpf): handle kernel version compatibility issues`

## Issue Content Guidelines

### What to Include

- **High-level design notes** - focus on the "what" and "why"
- **POC-level details** - enough to get started, not exhaustive
- **Actionable scope** - should be implementable by a developer familiar with the codebase

### What NOT to Include

- Detailed test plans
- Exhaustive acceptance criteria
- Deep technical specifications
- Code examples (unless absolutely necessary for clarity)

## When to Use This Skill

- Creating new feature requests
- Reporting bugs and issues
- Documenting technical debt
- Planning work items for the MCPSpy project
