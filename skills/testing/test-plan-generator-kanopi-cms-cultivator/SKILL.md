---
name: test-plan-generator
description: Automatically generate comprehensive QA test plans when user mentions testing requirements, QA needs, or asks what should be tested. Analyzes code changes and features to create structured test scenarios. Invoke when user mentions "test plan", "QA", "what to test", "testing requirements", or "test scenarios".
---

# Test Plan Generator

Automatically generate comprehensive QA test plans based on features and changes.

## When to Use This Skill

Activate this skill when the user:
- Asks "what should QA test?"
- Says "I need a test plan"
- Mentions "testing requirements" or "test scenarios"
- Shows a new feature and asks "how should this be tested?"
- Asks "what test cases do I need?"
- References QA, testing coverage, or manual testing

## Quick Reference

See `/test-plan` command documentation for detailed test plan structure and examples.

This skill provides the same comprehensive test plan generation but is automatically invoked during conversation when the user expresses a need for test planning.

## Integration with /test-plan Command

- **This Skill**: Auto-invoked conversationally
  - "What should I test for this feature?"
  - "Need test scenarios"

- **`/test-plan` Command**: Explicit comprehensive generation
  - Full project test plan generation
  - Git history analysis
  - Structured documentation output
