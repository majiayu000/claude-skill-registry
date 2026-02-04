---
name: acc-documentation-qa-knowledge
description: Documentation QA knowledge base. Provides quality checklists, audit criteria, and metrics for documentation review.
---

# Documentation QA Knowledge Base

Quick reference for documentation quality assessment and audit criteria.

## Quality Dimensions

### Core Quality Metrics

| Dimension | Description | Weight |
|-----------|-------------|--------|
| **Completeness** | All APIs/features documented | 25% |
| **Accuracy** | Code matches documentation | 25% |
| **Clarity** | Understandable, no jargon | 20% |
| **Consistency** | Terms, style, format uniform | 15% |
| **Navigation** | Easy to find information | 10% |
| **Freshness** | Up-to-date with latest version | 5% |

### Quality Scoring

```
Score = (Completeness × 0.25) + (Accuracy × 0.25) + (Clarity × 0.20)
      + (Consistency × 0.15) + (Navigation × 0.10) + (Freshness × 0.05)

Rating:
90-100: Excellent
75-89:  Good
60-74:  Adequate
40-59:  Poor
0-39:   Critical
```

## Audit Checklists

### README Checklist

| Item | Required | Score |
|------|----------|-------|
| Project name and description | ✅ | /10 |
| Installation instructions | ✅ | /15 |
| Basic usage example | ✅ | /15 |
| Requirements/dependencies | ✅ | /10 |
| License | ✅ | /5 |
| Badges (build, coverage, version) | ⚪ | /5 |
| Contributing link | ⚪ | /5 |
| Documentation links | ⚪ | /10 |
| Changelog link | ⚪ | /5 |
| Examples work (copy-paste test) | ✅ | /20 |

**Total: /100**

### API Documentation Checklist

| Item | Required | Score |
|------|----------|-------|
| All public classes documented | ✅ | /15 |
| All public methods documented | ✅ | /15 |
| Parameters with types and descriptions | ✅ | /15 |
| Return types documented | ✅ | /10 |
| Exceptions documented | ✅ | /10 |
| Usage examples per endpoint | ✅ | /15 |
| Request/response examples | ⚪ | /10 |
| Error responses documented | ⚪ | /10 |

**Total: /100**

### Architecture Documentation Checklist

| Item | Required | Score |
|------|----------|-------|
| System overview | ✅ | /15 |
| Component descriptions | ✅ | /15 |
| Data flow diagrams | ✅ | /15 |
| Technology stack | ✅ | /10 |
| Decision records (ADRs) | ⚪ | /15 |
| Diagrams render correctly | ✅ | /10 |
| Consistent terminology | ✅ | /10 |
| Cross-references work | ⚪ | /10 |

**Total: /100**

## Detection Patterns

### Completeness Detection

```bash
# Find undocumented public classes
Grep: "^class |^final class |^abstract class " --glob "src/**/*.php"
# Compare with: Grep: "## " --glob "docs/api/**/*.md"

# Find undocumented public methods
Grep: "public function " --glob "src/**/*.php" | wc -l
# Compare with documented count

# Check README sections
Grep: "## Installation|## Usage|## Features" --glob "README.md"
```

### Accuracy Detection

```bash
# Find version mismatches
Grep: "version.*[0-9]+\.[0-9]+" --glob "README.md"
# Compare with: Grep: '"version"' --glob "composer.json"

# Find non-existent paths in docs
Grep: "src/[A-Za-z/]+" --glob "docs/**/*.md"
# Verify each path exists

# Find outdated code examples
# Extract code blocks and verify they match current API
```

### Clarity Detection

```bash
# Find undefined acronyms
Grep: "\b[A-Z]{2,}\b" --glob "docs/**/*.md"
# Check for glossary/definition nearby

# Find jargon without explanation
# Manual review of: DDD, CQRS, VO, DTO first usage

# Find walls of text (paragraphs > 5 lines)
# Manual review recommended
```

### Navigation Detection

```bash
# Find broken internal links
Grep: "\]\((?!http)[^\)]+\)" --glob "**/*.md"
# Verify each relative path exists

# Find missing TOC in long docs (> 100 lines)
wc -l docs/**/*.md | awk '$1 > 100 {print $2}'
# Check for: Grep: "## Table of Contents|## Contents" in each

# Find orphan pages (not linked from anywhere)
# Cross-reference all .md files
```

### Diagram Quality Detection

```bash
# Find diagrams with too many elements
Grep: "^\s*[A-Za-z].*\[|^\s*[A-Za-z].*\(" --glob "**/*.md" -A 50
# Count nodes in each mermaid block

# Find diagrams without labels
Grep: "A-->B|1-->2" --glob "**/*.md"
# Should have descriptive IDs

# Find non-rendering mermaid
# Test each ```mermaid block
```

## Issue Severity Levels

### Critical (Must Fix)

```markdown
❌ Missing installation instructions
❌ Broken copy-paste examples
❌ Wrong/outdated code syntax
❌ Missing license
❌ Dead links to key resources
❌ Security-sensitive info in examples
```

### Warning (Should Fix)

```markdown
⚠️ Missing API documentation
⚠️ No usage examples
⚠️ Outdated screenshots
⚠️ Inconsistent terminology
⚠️ Missing error handling docs
⚠️ Diagrams don't match code
```

### Info (Nice to Have)

```markdown
ℹ️ No badges
ℹ️ Missing contributing guide
ℹ️ No FAQ section
ℹ️ Basic diagrams could be improved
ℹ️ Could add more examples
```

## Audit Report Template

```markdown
# Documentation Audit Report

**Project:** {name}
**Date:** {date}
**Auditor:** Claude Code

## Summary

| Metric | Score | Status |
|--------|-------|--------|
| Overall | X/100 | ⚠️ |
| Completeness | X/100 | ✅ |
| Accuracy | X/100 | ❌ |
| Clarity | X/100 | ✅ |
| Consistency | X/100 | ⚠️ |
| Navigation | X/100 | ✅ |

## Critical Issues

### 1. {Issue Title}
- **Location:** {file:line}
- **Problem:** {description}
- **Impact:** {who is affected}
- **Fix:** {recommendation}

## Warnings

### 1. {Issue Title}
- **Location:** {file}
- **Problem:** {description}
- **Recommendation:** {fix}

## Recommendations

1. {Priority action 1}
2. {Priority action 2}
3. {Priority action 3}

## Detailed Findings

### README.md
- [ ] {item}: {status}

### API Documentation
- [ ] {item}: {status}

### Architecture Documentation
- [ ] {item}: {status}

## Next Steps

1. Fix critical issues immediately
2. Address warnings in next sprint
3. Consider recommendations for roadmap
```

## Quality Improvement Guide

### Quick Wins

| Action | Impact | Effort |
|--------|--------|--------|
| Fix broken links | High | Low |
| Add missing badges | Medium | Low |
| Add code examples | High | Medium |
| Create README template | High | Medium |
| Add link checker CI | Medium | Low |

### Long-term Improvements

| Action | Impact | Effort |
|--------|--------|--------|
| Generate API docs from code | High | High |
| Implement doc-as-code | High | High |
| Create style guide | Medium | Medium |
| Add example testing | High | Medium |
| Diagram automation | Medium | High |

## Automation Opportunities

### CI/CD Integration

```yaml
# Example doc validation workflow
documentation:
  checks:
    - markdown-lint
    - link-check
    - spelling
    - code-example-test
    - mermaid-validate
```

### Tools

| Tool | Purpose |
|------|---------|
| markdownlint | Markdown style |
| markdown-link-check | Broken links |
| alex | Inclusive language |
| mermaid-cli | Diagram validation |
| doctoc | TOC generation |

## References

For detailed information, load these reference files:

- `references/audit-procedures.md` — Step-by-step audit process
- `references/scoring-rubrics.md` — Detailed scoring criteria
- `references/common-issues.md` — Frequent documentation problems
- `references/automation.md` — CI/CD integration patterns
