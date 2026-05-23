---
name: code-analysis
description: Provides methodologies, metrics, and best practices for analyzing code structure, complexity, and quality
version: 1.0.0
---

## Overview

This skill provides comprehensive knowledge for code analysis including complexity metrics, anti-pattern detection, refactoring strategies, and code quality assessment across multiple programming languages.

## Complexity Metrics

### Cyclomatic Complexity
- **Low**: 1-10 (simple, easy to test)
- **Medium**: 11-20 (moderate complexity, acceptable)
- **High**: 21-50 (complex, needs refactoring)
- **Very High**: 51+ (critical, must refactor)

### Cognitive Complexity
Measures how difficult code is to understand based on nesting, control flow breaks, and recursion.

## Code Smells to Detect

- **Long Methods**: >50 lines
- **Large Classes**: >300 lines
- **Duplicate Code**: Repeated blocks
- **Long Parameter Lists**: >5 parameters
- **Deep Nesting**: >4 levels
- **God Objects**: Classes doing too much
- **Dead Code**: Unused functions/variables

## Refactoring Strategies

- **Extract Method**: Break long methods into smaller ones
- **Extract Class**: Split large classes by responsibility
- **Replace Conditional with Polymorphism**
- **Simplify Conditional Expressions**
- **Remove Duplicate Code**

## When to Apply

Use when analyzing codebase structure, identifying refactoring opportunities, or assessing code quality.
