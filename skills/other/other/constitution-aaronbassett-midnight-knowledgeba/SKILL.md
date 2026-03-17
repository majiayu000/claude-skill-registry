---
name: dapp-sdd:constitution
description: Use when implementing any Midnight example dApp to ensure compliance with quality standards and project conventions.
---

# Midnight Example DApp Constitution

This constitution defines non-negotiable standards for all example dApps built with the dapp-sdd plugin.

## Stack (Non-Negotiable)

- **Runtime:** Node.js ≥22.0.0
- **Language:** TypeScript 5.9+ (strict mode enabled)
- **Contracts:** Compact smart contracts in `contracts/` directory
- **SDK:** Midnight SDK packages (`@midnight-ntwrk/*`)
- **Scaffold:** Project structure from `create-mn-app`

## Code Quality (Zero Tolerance)

All code must pass quality checks with **zero warnings or errors**:

| Check | Command | Requirement |
|-------|---------|-------------|
| Linting | `npm run lint` | No errors, no warnings |
| Formatting | `npm run format:check` | No formatting issues |
| TypeScript | `tsc --noEmit` | No type errors |
| Compact | `compact compile` | Clean compilation |

**Quality gates are mandatory before every commit.**

## Example App Standards

### Educational Focus
- README.md must explain what the dApp demonstrates
- Code should be readable and educational (clarity over cleverness)
- Include inline comments explaining Midnight-specific concepts
- Keep scope minimal - demonstrate ONE concept well

### Documentation
- README.md follows `readme-and-co:documentation-standards`
- Include "How to Run" section with exact commands
- Document environment setup requirements
- Explain the Compact contract's purpose and circuits

## Git Workflow

### Commits
- Follow `git-lovely:useful-commits` skill for commit messages
- Commit and push after each completed task
- All work on feature branch, PR to main

### Branch Naming
- Format: `{feature-name}` (provided by user)
- Example: `counter-example`, `token-transfer`

## Phase Reviews (Mandatory)

After each implementation phase, run BOTH reviews:

### 1. Compact Code Review
```
Use compact-reviewer:compact-reviewer agent

Instructions: "You are reviewing an example dApp for the Midnight Network.
This project is intended to demonstrate concepts to developers learning Midnight.

Be pragmatic with suggestions:
- Focus on correctness and clarity over production concerns
- Flag anything that would confuse learners
- Flag bad practices that learners might copy
- Accept reasonable shortcuts that keep the example focused
- Ensure educational comments are accurate"
```

### 2. TypeScript Code Review
```
Use devs:code-reviewer agent

Instructions: "You are reviewing an example dApp for the Midnight Network.
This project is intended to demonstrate concepts to developers learning Midnight.

Be pragmatic with suggestions:
- Focus on correctness and clarity over production concerns
- Flag anything that would confuse learners
- Flag bad practices that learners might copy
- Accept reasonable shortcuts that keep the example focused
- Ensure educational comments are accurate"
```

**All review issues must be addressed before proceeding to next phase.**

## Testing Requirements

- Include basic happy-path tests for main functionality
- Test contract circuits with `TestContext`
- Document how to run tests in README
- Tests must pass before PR can be marked ready

## State Management

Plugin state is stored in `.dapp-sdd/` directory (gitignored):

```
.dapp-sdd/
├── spec.md           # Expanded specification
├── plan.md           # Implementation plan
├── tasks.md          # Task list with checkboxes
└── pr-context.json   # PR metadata
```

## Skill References

During implementation, leverage these skills:

| Phase | Skills |
|-------|--------|
| Specify | `compact-core:language-reference`, `midnight-dapp:*` |
| Plan | `compact-core:contract-patterns`, `compact-core:typescript-integration`, `midnight-proofs:*` |
| Implement | `compact-core:standard-library`, `compact-core:privacy-disclosure`, `compact-core:testing-debugging`, `midnight-tooling:*` |
| Commits | `git-lovely:useful-commits` |
| Docs | `readme-and-co:documentation-standards` |
