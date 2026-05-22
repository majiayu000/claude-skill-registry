---
name: e2e-uuv-testing
description: End-to-end testing with UUV (Useful User Verification)
allowed-tools: [Bash, Read, Glob]
---

# E2E UUV Testing Skill

## Overview

User-centric end-to-end testing. 90%+ context savings.

## Requirements

- Playwright or Cypress installed
- UUV framework configured

## Tools (Progressive Disclosure)

### Test Execution

| Tool         | Description           |
| ------------ | --------------------- |
| run-tests    | Run E2E test suite    |
| run-scenario | Run specific scenario |
| run-tagged   | Run tests by tag      |

### Scenarios

| Tool              | Description                 | Confirmation |
| ----------------- | --------------------------- | ------------ |
| list-scenarios    | List test scenarios         | No           |
| generate-scenario | Generate scenario from spec | Yes          |
| validate-scenario | Validate scenario syntax    | No           |

### Reporting

| Tool            | Description             |
| --------------- | ----------------------- |
| get-results     | Get test results        |
| generate-report | Generate HTML report    |
| screenshots     | Get failure screenshots |

## Agent Integration

- **qa** (primary): Test execution
- **ux-expert** (secondary): User journey validation
