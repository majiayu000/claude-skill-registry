---
name: skill-create
description: Analyze git history and codebase patterns to automatically generate SKILL.md files that teach Claude your team's development practices. Creates skills from recurring workflows, naming conventions, and coding patterns.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Skill Create — Generate Skills from Codebase Patterns

Analyze the corbat-coco git history and source code to extract recurring patterns and generate reusable skill files.

## Analysis Process

### Step 1: Git History Analysis

```bash
# Recent commit patterns
git log --oneline -50 2>&1

# Most frequently changed files
git log --pretty=format: --name-only -100 | sort | uniq -c | sort -rn | head -20

# Commit message patterns (conventional commits)
git log --pretty=format:"%s" -100 | sed 's/:.*//' | sort | uniq -c | sort -rn

# Co-change patterns (files that change together)
git log --pretty=format: --name-only -50 | awk 'NF>0{print}' | paste - - | sort | uniq -c | sort -rn | head -20
```

### Step 2: Code Pattern Analysis

```bash
# Most common import patterns
grep -rh "^import" src/ --include="*.ts" | sort | uniq -c | sort -rn | head -20

# Zod schema patterns
grep -rn "z\.object\|z\.string\|z\.number" src/ --include="*.ts" | wc -l

# Tool registration patterns
grep -rn "registry\.register\|registerAllTools" src/ --include="*.ts"

# Error handling patterns
grep -rn "catch.*error\|instanceof Error" src/ --include="*.ts" | wc -l
```

### Step 3: Test Patterns

```bash
# Test file structure
find src/ -name "*.test.ts" | head -20

# Mock patterns used
grep -rn "vi\.mock\|vi\.fn\|vi\.spyOn" src/ --include="*.test.ts" | head -20

# Describe/it structure
grep -rn "^describe\|^  it\(" src/ --include="*.test.ts" | head -30
```

## Skill Templates to Generate

Based on the analysis, generate skills for patterns found. Examples:

### Detected: Conventional Commits Pattern
If `feat:`, `fix:`, `chore:` appear consistently → generate `commit-convention` skill

### Detected: Tool Registration Pattern
If tools follow `registerXxx(registry)` → generate `new-tool` skill

### Detected: Zod Config Pattern
If config schemas follow the same structure → generate `add-config-option` skill

### Detected: Quality Analyzer Pattern
If analyzers in `src/quality/analyzers/` follow a pattern → generate `new-quality-analyzer` skill

## Skill Output Format

Generate each skill in `.claude/skills/generated/<skill-name>/SKILL.md`:

```markdown
---
name: [detected-pattern-name]
description: [Inferred from pattern frequency and context]
---

# [Pattern Name]

*Auto-generated from git history analysis on [date]*
*Based on [N] occurrences in [N] commits*

## Pattern

[Describe the recurring workflow or convention]

## When to Apply

[Inferred trigger conditions]

## Steps

[Extracted from the most common execution sequence]

## Example from this codebase

\`\`\`typescript
// Actual example from src/...
[real code]
\`\`\`

## Related Files
- [files most commonly involved in this pattern]
```

## Usage Options

```
/skill-create                     # analyze full history (last 100 commits)
/skill-create --commits 50        # analyze last 50 commits
/skill-create --focus tools       # focus on tool-related patterns
/skill-create --focus tests       # focus on testing patterns
/skill-create --focus config      # focus on configuration patterns
```

## Output

After analysis, report:
```markdown
## Skill Create Report

### Patterns Detected
| Pattern | Occurrences | Skill Generated |
|---------|-------------|-----------------|
| tool-registration | 12 | .claude/skills/generated/new-tool/ |
| zod-config-schema | 8 | .claude/skills/generated/add-config/ |
| vitest-mock-pattern | 15 | .claude/skills/generated/vitest-mocks/ |

### Skipped (insufficient data)
- [patterns with <3 occurrences]

### Review Recommended
- .claude/skills/generated/new-tool/SKILL.md
```

Generated skills are drafts — review and edit before using.
