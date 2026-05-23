---
name: gsd:map-codebase
description: Analyze codebase with parallel mapper agents
version: 1.0.0
triggers: [map codebase, analyze codebase]
tools: [Bash, Glob, Grep, Write]
---

# GSD Map Codebase

Analyzes existing codebase using parallel mapper agents.

## When to Use

- Understanding an existing codebase structure
- Starting work on a brownfield project
- Documenting technology stack and architecture

## Process

1. Check for existing .planning/codebase/ directory
2. Create directory structure if needed
3. Spawn 4 parallel mapper agents (tech, arch, quality, concerns)
4. Wait for all agents to complete
5. Verify all 7 documents exist
6. Commit codebase map to git

## Output Documents

- STACK.md, INTEGRATIONS.md (tech focus)
- ARCHITECTURE.md, STRUCTURE.md (arch focus)
- CONVENTIONS.md, TESTING.md (quality focus)
- CONCERNS.md (concerns focus)

## Success Criteria

All 7 documents written with content and committed to git.
