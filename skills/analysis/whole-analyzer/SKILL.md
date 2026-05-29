---
name: whole-analyzer
description: |
  Pre-editing analysis for Whole documentation. Use when: (1) Starting new editing session,
  (2) Checking for duplicates across domains, (3) Analyzing section completeness,
  (4) Validating structure before bulk edits, (5) Generating analysis reports.
version: 2.1.0
license: MIT
allowed-tools:
  - Grep
  - Read
  - Glob
  - Task
metadata:
  author: "Whole Project"
  category: "documentation"
  updated: "2026-01-02"
---

# Whole Content Analyzer

## Purpose
Run comprehensive analysis on Whole documentation sections before editing begins.

## Integration with Agents

### When to Invoke Agents
Use Task tool to invoke specialized analysis agents for deep analysis:

```javascript
// For deep duplicate semantic analysis
Task(subagent_type: 'whole-translator',
     prompt: 'Analyze semantic similarity and cultural context for potential duplicates in CF[N]')

// For cross-reference graph analysis before editing
Task(subagent_type: 'whole-cross-reference',
     prompt: 'Build reference graph and analyze connectivity patterns for CF[N]')

// For comprehensive content structure validation
Task(subagent_type: 'whole-content-validator',
     prompt: 'Pre-validate content structure and identify gaps in CF[N]')
```

### When NOT to Use Agents
- Simple concept counting → Use Grep directly
- Basic duplicate detection (exact matches) → Use Grep with concept names
- Format checking → Use shared utilities from `.claude/skills/shared`
- Quick inventory → Use Grep pattern matching

## Analysis Types

### 1. Content Inventory
- Count concepts per section
- Identify incomplete 4-point descriptions
- Count cross-references

### 2. Duplicate Detection
- Exact matches across domains
- Similar concepts (>70% overlap)
- Classify: meaningful diversity vs redundancy

### 3. Structural Check
- Domain-function alignment
- Distribution across 5 functions
- Bilingual format compliance
- Cross-reference integrity

### 4. Gap Analysis
- Missing function categories
- Incomplete descriptions
- Weak integration points

## Analysis Workflow

### Phase 1: Quick Analysis (Scripts & Grep)
Run automated analysis first for basic metrics:
```bash
# Basic structure and format checks
grep -n "^#### \*\*[0-9]" Whole.md | wc -l  # Count concepts
grep -n "→ \*\*Liên kết:" Whole.md | wc -l   # Count cross-refs
```

### Phase 2: Agent-Based Deep Analysis
For complex analysis requiring semantic understanding:
1. **Invoke whole-content-validator** - Get comprehensive structure validation
2. **Invoke whole-cross-reference** - Build reference graph and identify patterns
3. **Invoke whole-translator** (if needed) - Semantic duplicate detection

### Phase 3: Report Generation
Synthesize findings from both automated and agent-based analysis.

## Agent Integration Guide

### whole-content-validator
**When to use**: Pre-validate structure and identify gaps before editing
**Command**: `Task(subagent_type='whole-content-validator', prompt='Pre-validate CF[N]')`
**Expected output**: Structure validation report with gap analysis

### whole-cross-reference
**When to use**: Analyze reference patterns and identify weak/strong connectivity
**Command**: `Task(subagent_type='whole-cross-reference', prompt='Analyze reference patterns in CF[N]')`
**Expected output**: Reference graph, connectivity analysis, strategic recommendations

### whole-translator
**When to use**: Detect semantic duplicates across bilingual concepts
**Command**: `Task(subagent_type='whole-translator', prompt='Analyze semantic similarity for duplicates in CF[N]')`
**Expected output**: Semantic similarity report, cultural context analysis

## Output Format

```markdown
# Analysis Report: CHỨC NĂNG [N]

## Summary
- Total Concepts: [N]
- Complete: [N] ([%])
- Cross-Refs: [N]
- Issues: [N]

## Automated Analysis Results

### Quick Metrics:
- Concept count: [N]
- Cross-references: [N]
- Format compliance: [%]

### Agent Analysis:
- ✅ **whole-content-validator**: [Summary]
- ✅ **whole-cross-reference**: [Summary]
- ⚠️ **whole-translator**: [Summary]

## Findings

### Strengths
[List]

### Issues
[List with severity: Critical/Warning/Info]

### Potential Duplicates
[Table: name, locations, similarity %, classification, agent recommendation]

### Connectivity Analysis
- High-connectivity concepts: [List]
- Isolated concepts: [List]
- Recommended new links: [List]

## Recommendations
[Prioritized actions based on both automated and agent findings]

---
**Analyzer**: whole-analyzer v2.1.0
**Agents Invoked**: [List]
**Date**: [timestamp]
```

## Critical Rules

### ✅ MUST
- Run quick analysis first before invoking agents
- Use agents for deep semantic analysis, not simple checks
- Document agent findings in analysis report
- Use shared utilities from `.claude/skills/shared`
- Provide actionable recommendations

### ❌ NEVER
- Invoke agents for simple metrics (use Grep/scripts)
- Skip quick analysis phase
- Modify content (analysis only)
- Analyze without clear purpose
