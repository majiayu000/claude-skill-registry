---
name: design-document
description: Technical design document format and conventions for implementation planning. Use when creating or reviewing a technical design that translates a spec into an implementation plan.
---

# Design Document — Skill

## Purpose

Define the format and conventions for a technical design document that translates spec requirements into concrete architecture and implementation steps.

## When to Use

- Creating a technical design from a specification
- Reviewing a design document for completeness
- Planning implementation steps with verification criteria

## Output Template

```markdown
# DESIGN.md — [Project Name]

## 1. Architecture Overview
[One paragraph describing the system's structure and data flow.]

## 2. File Structure
[Tree diagram of all files to be created, with one-line purpose for each.]

## 3. Module Responsibilities

### 3.N [Module Name] — `path/to/file`
- **Purpose**: [One sentence]
- **Inputs**: [What it receives]
- **Outputs**: [What it produces]
- **Key decisions**: [Why this approach]
- **Fulfills**: [REQ-XX-NNN list]

## 4. Data Flow
[Step-by-step description of how a request flows through the system, referencing modules by name.]

## 5. Implementation Plan

### Step N: [Step Title]
- **Branch**: `feature/<branch-name>`
- **Files**: [files created or modified]
- **What**: [What to implement]
- **Fulfills**: [REQ-XX-NNN list]
- **Definition of Done**: `<command>` → `<expected output>`

## 6. Demo Functions
[Table of demo routes with file path, behavior, and which requirements they validate.]

## 7. Test Plan
[How E2E tests are structured, what scenarios they cover, how to run them.]
```

## Conventions

1. **Every module must trace to at least one requirement.** If a module cannot cite a REQ, it may be unnecessary.
2. **Implementation steps are ordered by dependency.** Later steps can depend on earlier steps but not vice versa.
3. **Each step has exactly one feature branch.** Steps may be combined only if they are tightly coupled and small.
4. **Definition of Done is a literal command with expected output.** Not prose — a runnable verification.
5. **File structure is complete.** Every file that will exist after implementation is listed, including test files and config files.
6. **No speculative architecture.** Only design what the spec requires. If the spec doesn't mention it, don't design it.

## Quality Checklist

- [ ] Every requirement (REQ-RTG, REQ-CON, REQ-RCV) is covered by at least one module
- [ ] Every requirement appears in at least one implementation step's Fulfills list
- [ ] Every implementation step has a runnable Definition of Done
- [ ] File structure includes all source files, test files, and config files
- [ ] Implementation steps are ordered by dependency (no forward references)
- [ ] Data flow description matches the module responsibilities
- [ ] No modules or files exist that cannot trace to a requirement
