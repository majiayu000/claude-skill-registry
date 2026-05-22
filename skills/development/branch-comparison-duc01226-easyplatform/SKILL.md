---
name: branch-comparison
description: Use when the user asks to compare branches, analyze git diffs, review changes, update specifications based on code changes, or sync specs with implementation. Triggers on keywords like "compare branches", "git diff", "what changed", "branch comparison", "spec update", "sync specs".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

# Branch Comparison & Specification Update

Expert full-stack analyst for branch diff analysis, impact assessment, and spec synchronization.

**⚠️ MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` — validation checkpoints, evidence chains, confidence levels

---

## Phase 1: Branch Analysis

Build structured analysis in `.ai/workspace/analysis/[comparison-name].md`.

### Git Change Detection
```bash
git diff --name-status [source]..[target]
git diff --stat [source]..[target]
git log --oneline [source]..[target]
```

### Change Classification
For each changed file, document:
- `filePath`, `changeType` (A/M/D), `impactLevel` (Critical/High/Medium/Low)
- `serviceContext` (Frontend/Backend/Config/DB)
- Purpose: Feature, Bug Fix, Refactor

### Related Files Discovery
For each changed file, find: importers, dependencies, test files, API consumers, UI components.

> If file list exceeds 75, prioritize by impactLevel (Critical > High > Medium > Low).

## Phase 2: Analysis & Planning

### Code Review Analysis
- Strengths, weaknesses, security concerns, performance implications

### Refactoring Recommendations
- Immediate improvements, structural changes, technical debt

### Specification Update Plan
- New requirements discovered, test spec updates needed, documentation gaps

## Phase 3: Approval Gate

**CRITICAL**: Present analysis and plan for approval before executing updates.

## Phase 4: Execution

Update specification documents with: requirements, test specs, architecture docs, review findings.

### Spec Update Mode
**⚠️ MUST READ** `.claude/skills/branch-comparison/references/spec-update-workflow.md`

Provides:
- **Pattern-based discovery** - grep patterns for finding spec files and cross-referencing
- **Gap analysis template** - Component | Specified | Implemented | Gap
- **Update checklist** - Entities, commands, queries, events, API endpoints
- **3 update patterns** - Entity spec, command spec, API endpoint spec

## Phase 5: Validation

Verify updated specifications accurately reflect all changes. Cross-reference:
```bash
# Verify all commands are documented
grep -r "class.*Command" --include="*.cs" -l  # Find implementations
grep -r "CommandName" docs/specifications/     # Check in specs
```

## Guidelines

- **Evidence-based**: All updates grounded in concrete `git diff` output
- **Comprehensive impact**: Analyze direct and indirect effects, including cross-service
- **Platform-aware**: Respect CQRS, Clean Architecture, platform patterns
- **Full traceability**: Ensure links between code, requirements, and tests


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
