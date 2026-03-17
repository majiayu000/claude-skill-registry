---
name: tdd
description: Use when the user wants test-driven development, asks to write tests first, or requests red-green-refactor discipline for a feature or bugfix.
invocation: agent
---

# TDD — Test-Driven Development

Run a structured TDD workflow using the `persona-tdd-orchestrator` agent.

## Step 1: Clarify Test Strategy

Use AskUserQuestion to gather context before starting:

```
questions: [
  {
    question: "What's your test coverage goal?",
    header: "Coverage",
    multiSelect: false,
    options: [
      {label: "Critical paths only", description: "Focus on business-critical flows"},
      {label: "Standard ~80%", description: "Industry-standard coverage target"},
      {label: "Comprehensive >90%", description: "High coverage for safety-critical code"},
      {label: "Full mutation testing", description: "Maximum rigor with mutation tests"}
    ]
  },
  {
    question: "What test style fits this feature?",
    header: "Test Style",
    multiSelect: false,
    options: [
      {label: "Unit tests focus", description: "Isolated component testing"},
      {label: "Integration tests", description: "Module interaction testing"},
      {label: "E2E tests", description: "Full user flow testing"},
      {label: "Mix of all", description: "Test pyramid approach"}
    ]
  },
  {
    question: "What's the complexity level?",
    header: "Complexity",
    multiSelect: false,
    options: [
      {label: "Simple CRUD", description: "Basic create/read/update/delete"},
      {label: "Moderate logic", description: "Conditional logic and validation"},
      {label: "Complex algorithms", description: "Significant computation"},
      {label: "Distributed systems", description: "Multiple services, async, eventual consistency"}
    ]
  }
]
```

## Step 2: Execute TDD Cycle

After receiving answers, run the red-green-refactor cycle:

1. **Red**: Write a failing test for the next requirement
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve code quality while keeping tests green
4. **Repeat**: Continue until all requirements are covered

Use the `persona-tdd-orchestrator` agent perspective for discipline enforcement.

## Step 3: Report

```
## TDD Complete

**Feature**: <description>
**Coverage Goal**: <selected>
**Test Style**: <selected>
**Tests Written**: <count>
**All Passing**: Yes/No

Next Steps:
- `/arc:core:verify --post` to run full verification
- `/arc:core:execute` if part of a larger plan
```
