---
name: skill-simplify
description: SKILL.md simplification with functional integrity verification. Analyze redundancy, optimize content, check no functionality lost. Triggers on "simplify skill", "optimize skill", "skill-simplify".
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

# Skill Simplify

Three-phase pipeline: analyze functional inventory, apply optimization rules, verify integrity.

**Phase Reference Documents** (read on-demand):

| Phase | Document | Purpose |
|-------|----------|---------|
| 1 | [phases/01-analysis.md](phases/01-analysis.md) | Extract functional inventory, identify redundancy, validate pseudo-code format |
| 2 | [phases/02-optimize.md](phases/02-optimize.md) | Apply simplification rules, fix format issues |
| 3 | [phases/03-check.md](phases/03-check.md) | Verify functional integrity, validate format |

## Input Processing

```javascript
const targetPath = input.trim()
const targetFile = targetPath.endsWith('.md') ? targetPath : `${targetPath}/SKILL.md`
const originalContent = Read(targetFile)
const originalLineCount = originalContent.split('\n').length
```

## TodoWrite Pattern

```javascript
TodoWrite({ todos: [
  { content: `Phase 1: Analyzing ${targetFile}`, status: "in_progress", activeForm: "Extracting functional inventory" },
  { content: "Phase 2: Optimize", status: "pending" },
  { content: "Phase 3: Integrity Check", status: "pending" }
]})
```

## Core Rules

1. **Preserve ALL functional elements**: Code blocks with logic, agent calls, data structures, routing, error handling, input/output specs
2. **Only reduce descriptive content**: Flowcharts, verbose comments, duplicate sections, examples that repeat logic
3. **Never summarize algorithm logic**: If-else branches, function bodies, schemas must remain verbatim
4. **Classify code blocks**: Distinguish `functional` (logic, routing, schemas) from `descriptive` (ASCII art, examples, display templates) — only descriptive blocks may be deleted
5. **Merge equivalent variants**: Single/multi-perspective templates differing only by a parameter → one template with variant comment
6. **Fix format issues**: Nested backtick template literals in code fences → convert to prose; hardcoded option lists → flag for dynamic generation; workflow handoff references → ensure execution steps present
7. **Validate pseudo-code**: Check bracket matching, variable consistency, structural completeness
8. **Quantitative verification**: Phase 3 counts must match Phase 1 counts for functional categories; descriptive block decreases are expected

## Error Handling

| Error | Resolution |
|-------|------------|
| Target file not found | Report error, stop |
| Check FAIL (missing functional elements) | Show delta, revert to original, report which elements lost |
| Check WARN (descriptive decrease or merge) | Show delta with justification |
| Format issues found | Report in check, fix in Phase 2 |
