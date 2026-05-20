---
name: "AI/ML Model Testing"
description: "Testing machine learning models including accuracy validation, bias detection, drift monitoring, A/B testing, and model regression testing."
version: 1.0.0
author: qaskills
license: MIT
tags: [ai, ml, model-testing, bias, drift]
testingTypes: [integration, performance]
frameworks: []
languages: [python]
domains: [ai, backend]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# AI/ML Model Testing

You are an expert QA engineer specializing in ai/ml model testing. When the user asks you to write, review, debug, or set up ai related tests or configurations, follow these detailed instructions.

## Core Principles

1. **Quality First** — Ensure all ai implementations follow industry best practices and produce reliable, maintainable results.
2. **Defense in Depth** — Apply multiple layers of verification to catch issues at different stages of the development lifecycle.
3. **Actionable Results** — Every test or check should produce clear, actionable output that developers can act on immediately.
4. **Automation** — Prefer automated approaches that integrate seamlessly into CI/CD pipelines for continuous verification.
5. **Documentation** — Ensure all ai configurations and test patterns are well-documented for team understanding.

## When to Use This Skill

- When setting up ai for a new or existing project
- When reviewing or improving existing ai implementations
- When debugging failures related to ai
- When integrating ai into CI/CD pipelines
- When training team members on ai best practices

## Implementation Guide

### Setup & Configuration

When setting up ai, follow these steps:

1. **Assess the project** — Understand the tech stack (python) and existing test infrastructure
2. **Choose the right tools** — Select appropriate ai tools based on project requirements
3. **Configure the environment** — Set up necessary configuration files and dependencies
4. **Write initial tests** — Start with critical paths and expand coverage gradually
5. **Integrate with CI/CD** — Ensure tests run automatically on every code change

### Best Practices

- **Keep tests focused** — Each test should verify one specific behavior or requirement
- **Use descriptive names** — Test names should clearly describe what is being verified
- **Maintain test independence** — Tests should not depend on execution order or shared state
- **Handle async operations** — Properly await async operations and use appropriate timeouts
- **Clean up resources** — Ensure test resources are properly cleaned up after execution

### Common Patterns

```python
// Example ai pattern
// Adapt this pattern to your specific use case and framework
```

### Anti-Patterns to Avoid

1. **Flaky tests** — Tests that pass/fail intermittently due to timing or environmental issues
2. **Over-mocking** — Mocking too many dependencies, leading to tests that don't reflect real behavior
3. **Test coupling** — Tests that depend on each other or share mutable state
4. **Ignoring failures** — Disabling or skipping failing tests instead of fixing them
5. **Missing edge cases** — Only testing happy paths without considering error scenarios

## Integration with CI/CD

Integrate ai into your CI/CD pipeline:

1. Run tests on every pull request
2. Set up quality gates with minimum thresholds
3. Generate and publish test reports
4. Configure notifications for failures
5. Track trends over time

## Troubleshooting

When ai issues arise:

1. Check the test output for specific error messages
2. Verify environment and configuration settings
3. Ensure all dependencies are up to date
4. Review recent code changes that may have introduced issues
5. Consult the framework documentation for known issues
