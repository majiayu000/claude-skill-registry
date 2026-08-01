---
name: search-analyze-report-template
description: '[REPLACE] Search for patterns, analyze findings, generate structured
  reports. Use when [REPLACE with specific triggers].'
---

---
name: search-analyze-report-template
description: [REPLACE] Search for patterns, analyze findings, generate structured reports. Use when [REPLACE with specific triggers].
allowed-tools: Grep, Glob, Read, TodoWrite
---

# Search-Analyze-Report Template

## Purpose

This template demonstrates the Search → Analyze → Report workflow pattern for skills that systematically examine codebases and provide structured findings.

**Use this template when:**
- Skill searches codebase for specific patterns
- Analysis categorizes or prioritizes findings
- Output is a structured report with recommendations

## Workflow

### Phase 1: Search

<search>
1. Define search criteria
2. Use Grep/Glob to find matching files
3. Collect all findings systematically
4. Track locations for reporting
</search>

### Phase 2: Analyze

<analyze>
1. Categorize findings by severity/type
2. Identify patterns across findings
3. Prioritize issues
4. Determine impact and recommendations
</analyze>

### Phase 3: Report

<report>
1. Structure findings by category
2. Provide actionable recommendations
3. Include examples with file:line references
4. Summarize key takeaways
</report>

## Progressive Disclosure

**Core workflow (this file):**
- Search → Analyze → Report phases
- High-level guidance

**Detailed guidance (references/):**
- @references/security-analysis-example.md - Complete security audit example
- Domain-specific patterns loaded when needed

## Example Usage

```xml
<search>
Found 15 SQL injection vulnerabilities
Found 8 XSS vulnerabilities
Found 3 CSRF issues
</search>

<analyze>
Critical: 5 issues (immediate data exposure)
High: 12 issues (potential exploitation)
Medium: 9 issues (defense-in-depth)
</analyze>

<report>
## Critical Issues
1. Direct SQL concatenation at src/db.ts:45
   - Recommendation: Use parameterized queries

## High Priority Issues
...
</report>
```

## See Also

- @references/security-analysis-example.md - Full workflow demonstration
