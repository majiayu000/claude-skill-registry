---
name: plugin-script-architecture
description: Script development standards covering implementation patterns, testing, and output contracts
user-invocable: false
allowed-tools: Read, Bash
---

# Plugin Script Architecture Skill

## What This Skill Provides

- **Python Implementation**: Stdlib-only patterns, argparse, error handling
- **Testing Standards**: pytest infrastructure, test organization, fixtures
- **Output Contract**: TOON format, exit codes, error patterns

For script execution patterns, see: `plan-marshall:tools-script-executor`

## When to Activate

Activate when:
- Creating new scripts for skills
- Implementing test suites for scripts
- Reviewing script code quality

## Standards

### 1. Python Implementation
Load: `standards/python-implementation.md`

### 2. Testing Standards
Load: `standards/testing-standards.md`

### 3. Output Contract
Load: `standards/output-contract.md`

### 4. Cross-Skill Integration
Load: `standards/cross-skill-integration.md`

**CRITICAL**: Scripts run via the executor must follow cross-skill integration patterns for imports, logging, and error handling.

## References

- `references/notation-spec.md` - Full notation specification
- `references/stdlib-modules.md` - Allowed Python standard library modules

## Related Skills

- `plan-marshall:tools-script-executor` - Script execution, notation resolution, plan-marshall command
