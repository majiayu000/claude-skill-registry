---
name: branch-comparison
description: Use when the user asks to compare branches, analyze git diffs, review changes between branches, update specifications based on code changes, or analyze what changed. Triggers on keywords like "compare branches", "git diff", "what changed", "branch comparison", "code changes", "spec update".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

# Branch Comparison & Specification Update

You are to operate as an expert full-stack dotnet angular principle developer, software architect, and technical analyst to analyze all file changes between branches, perform comprehensive impact analysis, and update specification documents.

**IMPORTANT**: Always thinks hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation.

---

## Core Anti-Hallucination Protocols

### ASSUMPTION_VALIDATION_CHECKPOINT
Before every major operation:
1. "What assumptions am I making about [X]?"
2. "Have I verified this with actual code evidence?"
3. "Could I be wrong about [specific pattern/relationship]?"

### EVIDENCE_CHAIN_VALIDATION
Before claiming any relationship:
- "I believe X calls Y because..." → show actual code
- "This follows pattern Z because..." → cite specific examples
- "Service A owns B because..." → grep for actual boundaries

### TOOL_EFFICIENCY_PROTOCOL
- Batch multiple Grep searches into single calls with OR patterns
- Use parallel Read operations for related files

### CONTEXT_ANCHOR_SYSTEM
Every 10 operations:
1. Re-read the original task description
2. Verify the current operation aligns with original goals
3. Update the `Current Focus` in `## Progress` section

---

## PHASE 1: EXTERNAL MEMORY-DRIVEN BRANCH ANALYSIS

Build a structured knowledge model in `.ai/workspace/analysis/[comparison-name].md`.

### PHASE 1A: INITIALIZATION AND DISCOVERY

1. **Initialize** the analysis file with standard headings

### GIT BRANCH ANALYSIS DISCOVERY

**GIT_DIFF_COMPREHENSIVE_ANALYSIS**: Start with systematic git change detection:

1. **Primary Change Detection Commands**:
```bash
git diff --name-status [source-branch]..[target-branch]
git diff --stat [source-branch]..[target-branch]
git log --oneline [source-branch]..[target-branch]
```
Document results under `## Git Diff Analysis` and `## Commit History`.

2. **Change Impact & Scope Classification**: Document under `## Change Classification` and `## Change Scope Analysis`:
   - Types: Frontend, Backend, Config, DB
   - Purpose: Feature, Bug Fix, Refactor

**RELATED_FILES_COMPREHENSIVE_DISCOVERY**: For each changed file, discover all related components:
- Importers
- Dependencies
- Test files
- API consumers
- UI components

Save ALL changed files AND related files to `## Comprehensive File List` with:
- `filePath`
- `changeType`
- `relationshipType`
- `impactLevel`
- `serviceContext`

**INTELLIGENT_SCOPE_MANAGEMENT**: If file list exceeds 75, prioritize by impactLevel (Critical > High > Medium > Low).

### PHASE 1B: KNOWLEDGE GRAPH CONSTRUCTION

**IMPORTANT: MUST DO WITH TODO LIST**

For each file, document in `## Knowledge Graph`:
- All standard fields from feature-implementation skill
- Focus on change-specific context

### PHASE 1C: OVERALL ANALYSIS

Write comprehensive summary showing:
- Complete end-to-end workflows discovered
- Key architectural patterns and relationships
- Business logic workflows affected
- Integration points and dependencies

---

## PHASE 2: COMPREHENSIVE ANALYSIS AND PLANNING

Generate detailed analysis under these headings:

### 1. Code Review Analysis
- Strengths
- Weaknesses
- Security concerns
- Performance implications
- Maintainability

### 2. Refactoring Recommendations
- Immediate improvements
- Structural changes
- Technical debt items

### 3. Specification Update Plan
- New Requirements Discovery
- Test Specification Updates
- Documentation Strategy

---

## PHASE 3: APPROVAL GATE

**CRITICAL**: Present comprehensive analysis, code review, refactoring recommendations, and specification update plan for explicit approval. **DO NOT** proceed without it.

---

## PHASE 4: SPECIFICATION UPDATE EXECUTION

Once approved, read existing specification document and update with:
- Requirements
- Test Specifications
- Architecture Documentation
- Code Review findings

---

## SUCCESS VALIDATION

Verify updated specification accurately reflects all changes. Document under `## Specification Validation`.

---

## Branch Comparison Guidelines

- **Evidence-Based Analysis**: Start with `git diff` and base all updates on concrete code changes
- **Comprehensive Impact Assessment**: Analyze direct and indirect effects, including cross-service impacts
- **Enterprise Architecture Awareness**: Respect platform patterns, CQRS, and Clean Architecture
- **Quality-Focused Approach**: Perform thorough code review and identify refactoring opportunities
- **Specification Completeness**: Ensure full traceability between code, requirements, and tests
