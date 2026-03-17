---
name: drift-detect
description: Detect architectural drift and pattern violations
argument-hint: "[--strict]"
tags: [quality, architecture, drift, governance]
user-invocable: true
---

# Architecture Drift Detection

Detect when code deviates from established patterns and conventions.

## What To Do

1. **Check layer violations**: Controllers calling repositories directly
2. **Check naming conventions**: Missing I prefix on interfaces, wrong suffixes
3. **Check dependency direction**: Domain depending on infrastructure
4. **Check pattern consistency**: Some entities use DTOs, others do not
5. **Generate drift report** with specific file:line references

## Rules Checked
- Controller -> Service -> Repository (no shortcuts)
- DTOs have static ToDomain()/FromDomain()
- All public service methods are async
- Repository returns domain models (not DTOs)
- No business logic in controllers

## Arguments
- `--strict`: Fail on any violation (default: warn only)