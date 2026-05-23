---
name: code-analyzer
description: Static code analysis and complexity metrics
context:fork: true
allowed-tools: [Bash, Read, Glob]
---

# Code Analyzer Skill

## Overview

Static code analysis and metrics. 90%+ context savings.

## Tools (Progressive Disclosure)

### Analysis

| Tool            | Description                  |
| --------------- | ---------------------------- |
| analyze-file    | Analyze single file          |
| analyze-project | Analyze entire project       |
| complexity      | Calculate complexity metrics |

### Metrics

| Tool            | Description           |
| --------------- | --------------------- |
| loc             | Lines of code         |
| cyclomatic      | Cyclomatic complexity |
| maintainability | Maintainability index |
| duplicates      | Find duplicate code   |

### Reporting

| Tool     | Description              |
| -------- | ------------------------ |
| summary  | Get analysis summary     |
| hotspots | Find complexity hotspots |
| trends   | Analyze metric trends    |

## Agent Integration

- **code-reviewer** (primary): Code review
- **refactoring-specialist** (primary): Tech debt analysis
- **architect** (secondary): Architecture assessment
