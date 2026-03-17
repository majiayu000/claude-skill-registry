---
name: project-guidelines
description: This skill documents the standard process for reading and applying project-specific guidelines during SDD workflow phases. Use this when an agent needs to understand and follow project conventions for error handling, logging, naming, and testing.
version: 0.1.0
---

# Project Guidelines Reading

This skill defines the standard process for reading and applying project-specific guidelines. Multiple SDD agents (technical-architect, design-reviewer, developer) must follow this process to ensure consistency with project conventions.

## When to Use This Skill

Use this skill when:
- Starting the design phase (technical-architect)
- Reviewing a design for compliance (design-reviewer)
- Beginning implementation (developer)
- Validating that work follows project conventions

## The Project Guidelines File

Project guidelines are stored at `.sdd/project-guidelines.md` (referenced as `SDD_PROJECT_GUIDELINES`).

This file can:
1. **Reference existing documentation** - List paths to docs, READMEs, or other files containing conventions
2. **Define inline guidelines** - Specify conventions directly in the file

## Standard Reading Process

### Step 1: Check for Project Guidelines

```
Check if `.sdd/project-guidelines.md` exists
```

If the file does not exist:
- Note that no project-specific guidelines are defined
- Proceed with general best practices
- Consider recommending that guidelines be created

### Step 2: Read the Guidelines File

If the file exists, read it thoroughly using the Read tool.

### Step 3: Read All Referenced Documentation

The guidelines file may contain a "Referenced Documentation" section listing paths to other files. **You MUST read ALL referenced files.**

Common referenced files include:
- Error handling documentation
- Logging standards
- Coding style guides
- Architecture decision records (ADRs)
- README sections on conventions
- CLAUDE.md or CONSTITUTION.md files

### Step 4: Extract Key Conventions

From the guidelines and referenced documentation, identify conventions in these categories:

**Error Handling:**
- Error types/classes to use
- Error propagation patterns
- What information errors should contain
- How to categorize errors

**Logging:**
- Logging framework/approach
- Log levels and when to use them
- Required context in logs
- Structured logging requirements

**Naming Conventions:**
- File naming patterns
- Class/module naming patterns
- Function/method naming patterns
- Variable naming patterns

**Testing Conventions:**
- Test file locations and naming
- Test framework and assertion style
- Mocking/stubbing patterns
- Test data management


## What to Do When Guidelines Are Missing

If `.sdd/project-guidelines.md` does not exist but the project has established patterns:

1. **Explore the codebase** to discover implicit conventions
2. **Document discovered patterns** in your output
3. **Consider recommending** that guidelines be formalized

If guidelines are incomplete or ambiguous:

1. **Use AskUserQuestion** to clarify conventions
2. **Document assumptions** you're making
3. **Note gaps** that should be filled in the guidelines
