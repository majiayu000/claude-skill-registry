---
name: gemini-code-review
description: AI-powered code review using Gemini models
allowed-tools: [Bash, Read, Glob]
---

# Gemini Code Review Skill

## Overview

Gemini-powered code review automation. 90%+ context savings.

## Requirements

- GOOGLE_API_KEY environment variable

## Tools (Progressive Disclosure)

### Review

| Tool        | Description         |
| ----------- | ------------------- |
| review-file | Review single file  |
| review-diff | Review git diff     |
| review-pr   | Review pull request |

### Analysis

| Tool                 | Description                 |
| -------------------- | --------------------------- |
| find-bugs            | Find potential bugs         |
| security-scan        | Security vulnerability scan |
| suggest-improvements | Suggest code improvements   |

### Quality

| Tool                | Description             |
| ------------------- | ----------------------- |
| check-style         | Check code style        |
| complexity-analysis | Analyze complexity      |
| test-coverage-gaps  | Find test coverage gaps |

## Agent Integration

- **code-reviewer** (primary): Code review
- **gemini-validator** (primary): Gemini validation
- **qa** (secondary): Quality gates
