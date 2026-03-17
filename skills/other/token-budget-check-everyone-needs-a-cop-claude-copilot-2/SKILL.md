---
skill_name: token-budget-check
skill_category: documentation
description: Analyze markdown files for token budget compliance
allowed_tools: [Read, Bash, Glob]
token_estimate: 850
version: 1.0
last_updated: 2025-12-21
owner: Claude Copilot
status: active
tags: [tokens, documentation, budget, validation, shared-docs]
related_skills: [frontmatter-validation, link-validation]
trigger_files: ["*.md", "**\/docs/**\/*.md", "**\/documentation/**\/*.md"]
trigger_keywords: [token, budget, documentation, word-count, tokens, over-budget]
---

# Token Budget Check

Analyze markdown files to ensure they comply with token budget guidelines.

## Purpose

Shared-docs files have token budgets to optimize AI ingestion. This skill checks files against those budgets and suggests optimizations when over budget.

## Token Budgets by Document Type

| Document Type | Max Tokens | Max Words |
|---------------|------------|-----------|
| Skill (SKILL.md) | 2,000 | 1,400 |
| Product overview | 800 | 560 |
| Product architecture | 1,200 | 840 |
| Product API summary | 1,000 | 700 |
| Product integration | 800 | 560 |
| Operational guide | 4,000 | 2,800 |
| Agent profile | 2,000 | 1,400 |
| Index/navigation | 400 | 280 |

## Procedure

### 1. Identify Target Files

If a specific file is provided, check that file. Otherwise, scan the directory:

```bash
find . -name "*.md" -type f | head -20
```

### 2. Calculate Token Estimate

For each file, estimate tokens (words × 1.4):

```bash
file="path/to/file.md"
words=$(wc -w < "$file" | tr -d ' ')
tokens=$((words * 14 / 10))
echo "$file: ~$tokens tokens ($words words)"
```

### 3. Determine Document Type

Infer type from:
- Filename: `SKILL.md` → skill, `00-overview.md` → overview
- Path: `02-products/` → product doc, `03-ai-enabling/02-profiles/` → agent profile
- Frontmatter: `doc_type` field if present

### 4. Compare Against Budget

| Status | Condition | Action |
|--------|-----------|--------|
| OK | Under budget | Report as compliant |
| WARNING | 80-100% of budget | Suggest review |
| OVER | Exceeds budget | Analyze and suggest cuts |

### 5. If Over Budget, Analyze Content

Identify optimization opportunities:
- Prose that could be tables (30-50% savings)
- Redundant explanations
- Examples that could be shortened
- Content that belongs in linked docs

## Output Format

```markdown
## Token Budget Report

### Summary
- Files checked: N
- Compliant: N
- Warnings: N
- Over budget: N

### Details

| File | Type | Tokens | Budget | Status |
|------|------|--------|--------|--------|
| path/to/file.md | skill | 1,850 | 2,000 | OK |
| path/to/doc.md | overview | 950 | 800 | OVER (+150) |

### Recommendations

#### path/to/doc.md (950 tokens, budget 800)
- Lines 45-60: Convert feature list to table (-80 tokens)
- Lines 72-85: Remove redundant introduction (-50 tokens)
```

## Efficiency Patterns Reference

| Pattern | Token Savings |
|---------|---------------|
| Tables over prose | 30-50% |
| Bullet points over paragraphs | 20-30% |
| Omit articles in table cells | 5-10% |
| Use abbreviations (env, config, auth) | 5-10% |
| Remove redundant headers | 5-10% |
