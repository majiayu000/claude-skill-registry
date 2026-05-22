---
name: you-might-not-need-an-effect
description: Review React code for unnecessary useEffect usage based on react.dev guidelines. Analyses code for useEffect anti-patterns and optionally applies fixes. Use when reviewing React code quality or refactoring effects.
---

<!--
Example prompts:
  /you-might-not-need-an-effect
  /you-might-not-need-an-effect scope=diff to main
  /you-might-not-need-an-effect fix=false
-->

Arguments:

- scope: what to analyze (default: your current changes). Examples: "diff to main", "PR #123", "src/components/", "whole codebase"
- fix: whether to apply fixes (default: true). Set to false to only propose changes.

Steps:

1. Read https://react.dev/learn/you-might-not-need-an-effect to understand the guidelines
2. Analyze the specified scope for useEffect anti-patterns
3. If fix=true, apply the fixes. If fix=false, propose the fixes without applying.
