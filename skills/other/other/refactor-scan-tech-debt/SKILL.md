---
name: refactor-scan-tech-debt
description: "[Code Quality] Scans codebase for technical debt indicators: code smells, complexity hotspots, duplications, outdated patterns, and anti-patterns. Use when starting a refactoring session to identify what needs attention."
---

# Refactor: Scan Tech Debt

Identify technical debt across the codebase systematically.

## Scan Categories

### 1. Code Smells
- Long Methods (> 50 lines)
- Large Classes (> 500 lines or > 10 public methods)
- Long Parameter Lists (> 4 parameters)
- Feature Envy, Data Clumps

### 2. Complexity Indicators
- Deep Nesting (> 3 levels)
- Cyclomatic Complexity (> 10 branches)
- God Objects
- Circular Dependencies

### 3. Duplication
- Copy-Paste Code
- Parallel Hierarchies
- Repeated Conditionals

### 4. Outdated Patterns
- Deprecated APIs
- Legacy Patterns
- Dead Code