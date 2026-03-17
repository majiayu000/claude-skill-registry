---
name: diff-review-doc
description: Generate comprehensive, reviewer-ready code review documents from git diffs. Use this when the user provides code changes (git diff output, file changes, or asks to review code changes) and wants a structured review document. Creates detailed analysis covering change overview, business flow, key code explanation, risk assessment, and review recommendations. Supports both manual diff input and automatic git workspace detection. Particularly useful for reviewing pull requests, feature branches, or any code changes requiring thorough documentation for reviewers.
---

# Diff Review Doc

Generate comprehensive code review documents from git diffs, providing detailed analysis with real code snippets, business flow breakdown, and actionable review recommendations.

## Workflow

### 1. Obtain Diff Content

**If user provides diff directly:**
- Accept the diff content as-is
- Parse to identify changed files and hunks

**If no diff is provided:**
- Use `scripts/get_diff.sh` to retrieve changes:
  ```bash
  # Get all uncommitted changes (default)
  ./scripts/get_diff.sh

  # Get staged changes only
  ./scripts/get_diff.sh --staged

  # Compare with a branch
  ./scripts/get_diff.sh --branch main

  # Get changes from specific commit
  ./scripts/get_diff.sh --commit abc123
  ```

### 2. Analyze the Changes

**Parse the diff to extract:**
- File paths and change types (added/modified/deleted)
- Line-level changes (+/- lines)
- Context around changes

**Read relevant files:**
- For significant changes, read the full file to understand context
- For large files (>500 lines), focus on changed sections with surrounding context
- Pay special attention to backend files and large file changes

**Identify patterns:**
- Consult `references/patterns.md` for common code issues
- Look for anti-patterns, security vulnerabilities, performance issues
- Check architectural concerns

### 3. Structure the Analysis

**Follow this analysis framework:**

1. **改动概览 (Change Summary)**
   - Count files changed, lines added/removed
   - Identify change type (feature/bugfix/refactor/performance/security)
   - List key files with brief descriptions
   - Note dependency or configuration changes

2. **业务流程分析 (Business Flow Analysis)**
   - Explain what functionality is being implemented/changed
   - Map out the complete business flow
   - Show data flow between components
   - Identify all affected modules

3. **关键代码详解 (Key Code Analysis)**
   - For each significant file:
     - Show actual diff snippets (use real code from the diff)
     - Explain what the code does and why it changed
     - Highlight logic correctness, edge cases, error handling, performance
   - Prioritize backend files and large changes (>200 lines)
   - Include file paths with line numbers for reference

4. **风险评估 (Risk Assessment)**
   - Categorize risks as High/Medium/Low
   - Identify breaking changes, security concerns, performance impacts
   - Suggest mitigation measures
   - Flag large file changes and backend-critical changes

### 4. Generate Review Recommendations

**Consult `references/review-checklist.md` for comprehensive evaluation criteria:**

- **代码质量 (Code Quality)**: Readability, complexity, best practices
- **架构设计 (Architecture)**: Modularity, coupling, extensibility, data flow
- **功能验证 (Functionality)**: Business logic, error handling, data consistency
- **安全性 (Security)**: Input validation, authentication, data protection (if applicable)
- **性能 (Performance)**: Database queries, resource usage, caching (if applicable)

**For each category:**
- Give a rating (1-5 stars)
- List strengths (what's done well)
- List issues (what needs improvement)
- Provide specific, actionable recommendations

**Final recommendation:**
- Must Fix: Critical issues that block merge
- Should Fix: Important issues to address
- Nice to Have: Optional improvements
- Merge decision: Approve / Conditional / Needs Work

### 5. Write the Review Document

**Use `assets/review-template.md` as the base structure:**
- Copy the template structure
- Fill in all sections with actual analysis from steps 2-4
- Ensure all code snippets are real (from the actual diff)
- Include complete business flow explanation
- Provide specific, actionable review suggestions

**Output:**
- Save as a Markdown file (e.g., `REVIEW.md`)
- Format for easy reading (proper headings, code blocks, lists)
- Include generation timestamp

## Key Principles

### Base on Real Code
- All code snippets must be extracted from the actual diff
- Never use placeholder or example code
- Show actual line numbers and file paths

### Complete Business Context
- Explain the full user journey and data flow
- Connect frontend changes to backend logic
- Show how pieces fit together

### Actionable Review Suggestions
- Be specific about what to check
- Identify potential risks with clear explanations
- Provide concrete improvement suggestions
- Prioritize issues by severity

### Focus on Critical Areas
- **Large file changes**: >200 lines need detailed review
- **Backend changes**: API, database, auth, integrations
- **Architectural changes**: Design patterns, module boundaries
- **Security-sensitive code**: Input validation, data access

## Resources

### scripts/get_diff.sh
Bash script to retrieve git diffs in various scenarios. Supports getting uncommitted changes, staged changes, branch comparisons, and specific commits.

### references/review-checklist.md
Comprehensive checklist covering all aspects of code review: quality, architecture, functionality, security, performance, testing, compatibility, operations, and documentation.

Load this reference when generating review recommendations to ensure thorough evaluation.

### references/patterns.md
Catalog of common code patterns to watch for, including anti-patterns, security vulnerabilities, performance issues, and architectural concerns.

Load this reference during analysis phase to identify potential issues in the code changes.

### assets/review-template.md
Structured Markdown template for the review document. Provides consistent format with sections for change summary, business flow, code analysis, risk assessment, and review recommendations.

Use as the base structure and fill in with actual analysis.
