---
name: review
description: Comprehensive code review with parallel specialist sub-agents. Analyzes requirements traceability, code quality, security, performance, accessibility, test coverage, and technical debt. Produces detailed findings and calls /qa-gate for final gate decision.
mcp_tools_available:
  - context7  # For checking current best practices
  - perplexity  # For researching security patterns and best practices
  - chrome-devtools  # For performance and network debugging
  - postgres-mcp  # For query analysis and optimization review
  - kb_search  # For project-specific patterns and past decisions
---

# /review - Comprehensive Code Review

## Description

Full-spectrum code review using parallel specialist sub-agents. Each specialist analyzes a specific dimension, findings are aggregated, and `/qa-gate` produces the final gate decision.

**Key Features:**
- Parallel specialist sub-agents for thorough analysis
- Requirements traceability (AC → tests mapping)
- Active refactoring when safe
- Technical debt identification
- Holistic findings aggregation
- Automatic gate decision via `/qa-gate`

## Usage

```bash
# Review a single story by number
/review 3.1.5

# Review a single story by file path
/review docs/stories/epic-6-wishlist/wish-2002-add-item-flow.md

# Review current branch (no story)
/review --branch

# Review all stories in an epic directory (shorthand)
/review epic-6-wishlist

# Review all stories in a directory (full path)
/review docs/stories/epic-6-wishlist/

# Review directory, only stories with specific status
/review epic-6-wishlist --status=Draft

# Quick review (skip deep specialists)
/review 3.1.5 --quick

# Review with auto-fix enabled
/review 3.1.5 --fix

# Review specific files only
/review --files src/auth/**/*.ts

# Skip gate decision (findings only)
/review 3.1.5 --no-gate
```

## Parameters

- **target** - Story number (e.g., `3.1.5`), story file path, epic directory name (e.g., `epic-6-wishlist`), or full directory path
- **--branch** - Review current branch without story reference
- **--status** - Filter stories by status (e.g., `Draft`, `In Progress`, `Approved`) - only used with directory review
- **--quick** - Run only required checks, skip deep specialists
- **--fix** - Auto-fix issues when safe (refactoring)
- **--files** - Review specific files only
- **--no-gate** - Skip `/qa-gate` call, return findings only

---

## EXECUTION INSTRUCTIONS

**CRITICAL: Use Task tool to spawn parallel sub-agents. Use TodoWrite to track progress.**

---

## Phase 0: Initialize & Determine Mode

**Auto-detect operation mode based on target argument:**

```python
# Detection logic:
if target is None or target == "--branch":
    mode = "branch_review"
elif target.endswith(".md"):
    mode = "single_story"  # File path to specific story
elif is_directory(target) or target.startswith("epic-"):
    mode = "directory_review"
elif is_story_number(target):  # e.g., "3.1.5" or "2002"
    mode = "single_story"
else:
    # Try to resolve as story number, fall back to directory
    mode = "single_story"
```

### Mode A: Single Story Review (default)
Triggered by:
- Story number (e.g., `3.1.5`, `2002`)
- Story file path (e.g., `docs/stories/epic-6-wishlist/wish-2002-add-item-flow.md`)
- `--branch` flag

### Mode B: Directory Review (new)
Triggered by:
- Epic directory name (e.g., `epic-6-wishlist`) - auto-prepends `docs/stories/`
- Full directory path (e.g., `docs/stories/epic-6-wishlist/`)
- Any path that resolves to a directory containing `.md` files

```
TodoWrite([
  { content: "Scan directory for stories", status: "in_progress", activeForm: "Scanning directory" },
  { content: "Filter stories by status", status: "pending", activeForm: "Filtering stories" },
  { content: "Review each story sequentially", status: "pending", activeForm: "Reviewing stories" },
  { content: "Generate summary report", status: "pending", activeForm: "Generating summary" }
])
```

**Directory scanning:**
1. Resolve directory path:
   - If starts with `epic-`: prepend `docs/stories/` → `docs/stories/epic-6-wishlist/`
   - If full path provided: use as-is
   - If relative path: resolve from working directory
2. Verify directory exists, error if not
3. Find all `.md` files in directory: `Glob(pattern: "*.md", path: {DIR_PATH})`
4. Filter out excluded files/directories:
   - Skip files in `_legacy/` subdirectories
   - Skip `IMPLEMENTATION_ORDER.md`
   - Skip `README.md`
   - Skip any file starting with `EPIC-` (epic definition files)
5. For each remaining file, read and extract:
   - Frontmatter (if present)
   - Status field (from frontmatter or `status:` line in file)
6. If `--status` filter provided, only include stories where status matches
7. Sort stories by filename (natural sort order)
8. Create todo list with one item per story

**Proceed to Phase 0A for single story or Phase 0B for directory.**

---

## Phase 0A: Gather Context (Single Story)

**For single story review:**

```
TodoWrite([
  { content: "Gather review context", status: "in_progress", activeForm: "Gathering context" },
  { content: "Run required checks", status: "pending", activeForm: "Running checks" },
  { content: "Spawn specialist sub-agents", status: "pending", activeForm: "Spawning specialists" },
  { content: "Aggregate findings", status: "pending", activeForm: "Aggregating findings" },
  { content: "Run qa-gate", status: "pending", activeForm: "Running qa-gate" },
  { content: "Update story file", status: "pending", activeForm: "Updating story" }
])
```

**Gather context:**
1. If story provided, read story file and extract:
   - Acceptance criteria
   - Tasks list
   - File list (if present)
   - Previous QA results
2. Get list of changed files: `git diff --name-only origin/main`
3. Read CLAUDE.md for project guidelines
4. Determine review scope (files to analyze)

**Risk assessment (determines review depth):**
Auto-escalate to deep review if:
- Auth/payment/security files touched
- No tests added
- Diff > 500 lines
- Previous gate was FAIL or CONCERNS
- Story has > 5 acceptance criteria

**Proceed to Phase 1.**

---

## Phase 0B: Process Directory (Multiple Stories)

**For directory review:**

```
stories_to_review = [{story_path}, {story_path}, ...]  # From Phase 0

TodoWrite([
  { content: "Review {story_1}", status: "in_progress", activeForm: "Reviewing {story_1}" },
  { content: "Review {story_2}", status: "pending", activeForm: "Reviewing {story_2}" },
  { content: "Review {story_3}", status: "pending", activeForm: "Reviewing {story_3}" },
  # ... one per story
  { content: "Generate summary report", status: "pending", activeForm: "Generating summary" }
])
```

**For each story in stories_to_review:**

1. **Read story file** and extract:
   - Story ID/number
   - Title
   - Status
   - Acceptance criteria
   - Tasks list
   - Previous review findings (if any)

2. **Run Phases 0A through 7 for this story** (see below for modified Phase 7)

3. **Mark todo as completed**, move to next story

4. **After all stories processed, proceed to Phase 8B (Summary Report)**

**CRITICAL: Process stories sequentially, not in parallel. This allows findings to be appended to each story file before moving to the next.**

**Proceed to Phase 0A for each story, then continue through phases.**

---

## Phase 1: Required Checks

**Run these first (blocking if they fail):**

```bash
pnpm test --filter='...[origin/main]'
pnpm check-types --filter='...[origin/main]'
pnpm lint --filter='...[origin/main]'
```

**If any fail and --fix is set:**
- Try to auto-fix lint issues: `pnpm lint --fix`
- Re-run checks

**If still failing:** Report and continue (will affect gate decision)

---

## Phase 2: Spawn Specialist Sub-Agents

**CRITICAL: Spawn all specialists in parallel using run_in_background: true**

### 2.1 Requirements Traceability Specialist

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Requirements traceability",
  run_in_background: true,
  prompt: "You are a requirements traceability specialist.

           Story file: {STORY_FILE_PATH}
           Changed files: {CHANGED_FILES}

           For each acceptance criterion in the story:
           1. Find the test(s) that validate it
           2. Document the mapping using Given-When-Then format
           3. Identify any AC without test coverage

           T-SHIRT SIZE ESTIMATE (from requirements perspective):
           Based on the number of acceptance criteria, their complexity, and test coverage gaps:
           - XS: 1-2 simple ACs, all covered
           - S: 3-4 ACs, mostly covered
           - M: 5-7 ACs, some gaps
           - L: 8-10 ACs, significant gaps
           - XL: 11+ ACs, many gaps
           - XXL: 15+ ACs, extensive gaps or highly complex criteria

           Output format:
           ```yaml
           traceability:
             t_shirt_size: XS|S|M|L|XL|XXL
             size_rationale: 'Brief explanation of size estimate'
             covered:
               - ac: 1
                 test_file: src/__tests__/auth.test.ts
                 test_name: 'should validate login credentials'
                 given_when_then: 'Given valid credentials, When login called, Then returns token'
             gaps:
               - ac: 3
                 description: 'No test for session timeout handling'
                 severity: medium
                 suggested_test: 'Add test for session expiry behavior'
           ```"
)
```

### 2.2 Code Quality Specialist

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Code quality review",
  run_in_background: true,
  prompt: "You are a code quality specialist.

           Project guidelines: {CLAUDE_MD_CONTENT}
           Changed files: {CHANGED_FILES}

           Analyze for:
           1. Architecture and design patterns
           2. Code duplication
           3. Refactoring opportunities
           4. Best practices adherence
           5. CLAUDE.md compliance (Zod schemas, @repo/ui, @repo/logger, no barrel files)

           T-SHIRT SIZE ESTIMATE (from code quality/complexity perspective):
           Based on code complexity, architectural impact, and refactoring needs:
           - XS: Simple, isolated changes, minimal complexity
           - S: Straightforward implementation, few files touched
           - M: Moderate complexity, some architectural considerations
           - L: Complex logic, multiple components/patterns involved
           - XL: Significant architectural changes, cross-cutting concerns
           - XXL: Major refactoring or system-wide impact

           For each finding:
           - id: QUAL-{NNN}
           - severity: low|medium|high
           - finding: Description
           - file: File path
           - line: Line number
           - suggested_action: How to fix
           - can_auto_fix: true|false

           Output format:
           ```yaml
           code_quality:
             t_shirt_size: XS|S|M|L|XL|XXL
             size_rationale: 'Brief explanation of size estimate'
             complexity_score: 1-10
             findings:
               - id: QUAL-001
                 severity: medium
                 finding: '...'
                 # ... rest of fields
           ```"
)
```

### 2.3 Security Specialist

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Security review",
  run_in_background: true,
  prompt: "You are a security specialist.

           Changed files: {CHANGED_FILES}

           Check for:
           - Authentication/authorization issues
           - Injection vulnerabilities (SQL, XSS, command)
           - Sensitive data exposure
           - OWASP Top 10 issues
           - Hardcoded secrets or credentials
           - Insecure dependencies

           T-SHIRT SIZE ESTIMATE (from security risk perspective):
           Based on security surface area, risk level, and required mitigations:
           - XS: No security implications, read-only operations
           - S: Minor security considerations, standard auth checks
           - M: Moderate security requirements, data validation needed
           - L: Significant security impact, auth/authz critical
           - XL: High-risk features (payments, PII, admin functions)
           - XXL: Critical security features requiring extensive hardening

           For each finding:
           - id: SEC-{NNN}
           - severity: low|medium|high
           - finding: Description
           - file: File path
           - line: Line number
           - cwe: CWE reference if applicable
           - suggested_action: How to fix

           Output format:
           ```yaml
           security:
             t_shirt_size: XS|S|M|L|XL|XXL
             size_rationale: 'Brief explanation of size estimate'
             risk_level: low|medium|high|critical
             findings:
               - id: SEC-001
                 severity: high
                 finding: '...'
                 # ... rest of fields
           ```"
)
```

### 2.4 Performance Specialist

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Performance review",
  run_in_background: true,
  prompt: "You are a performance specialist.

           Changed files: {CHANGED_FILES}

           Check for:
           - N+1 query patterns
           - Missing database indexes
           - Unnecessary re-renders in React
           - Large bundle imports
           - Missing memoization (useMemo, useCallback, React.memo)
           - Inefficient algorithms
           - Memory leaks

           T-SHIRT SIZE ESTIMATE (from performance optimization perspective):
           Based on performance complexity and optimization requirements:
           - XS: Minimal performance considerations, simple operations
           - S: Basic performance best practices sufficient
           - M: Some optimization needed (memoization, indexes)
           - L: Significant performance work (query optimization, caching)
           - XL: Complex performance requirements (real-time, large datasets)
           - XXL: Critical performance engineering (sub-second SLAs, scale challenges)

           For each finding:
           - id: PERF-{NNN}
           - severity: low|medium|high
           - finding: Description
           - file: File path
           - estimated_impact: Description of performance impact
           - suggested_action: How to fix

           Output format:
           ```yaml
           performance:
             t_shirt_size: XS|S|M|L|XL|XXL
             size_rationale: 'Brief explanation of size estimate'
             performance_risk: low|medium|high
             findings:
               - id: PERF-001
                 severity: medium
                 finding: '...'
                 # ... rest of fields
           ```"
)
```

### 2.5 Accessibility Specialist

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Accessibility review",
  run_in_background: true,
  prompt: "You are an accessibility specialist.

           Changed files: {CHANGED_FILES}

           Check for:
           - WCAG 2.1 AA compliance
           - Keyboard navigation support
           - Screen reader compatibility
           - Missing ARIA labels/roles
           - Color contrast issues
           - Focus management
           - Form labels and error messages

           T-SHIRT SIZE ESTIMATE (from accessibility perspective):
           Based on UI complexity and a11y requirements:
           - XS: No UI changes, or simple read-only content
           - S: Basic UI with standard components (buttons, text)
           - M: Interactive UI (forms, modals) requiring a11y attention
           - L: Complex UI (data tables, multi-step flows, drag-drop)
           - XL: Rich interactions (custom widgets, animations, dynamic content)
           - XXL: Highly complex UI requiring extensive a11y engineering

           For each finding:
           - id: A11Y-{NNN}
           - severity: low|medium|high
           - finding: Description
           - file: File path
           - wcag_criterion: WCAG reference (e.g., 1.4.3)
           - suggested_action: How to fix

           Output format:
           ```yaml
           accessibility:
             t_shirt_size: XS|S|M|L|XL|XXL
             size_rationale: 'Brief explanation of size estimate'
             ui_complexity: low|medium|high
             findings:
               - id: A11Y-001
                 severity: high
                 finding: '...'
                 # ... rest of fields
           ```"
)
```

### 2.6 Test Coverage Specialist

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Test coverage analysis",
  run_in_background: true,
  prompt: "You are a test coverage specialist.

           Changed files: {CHANGED_FILES}
           Test files: {TEST_FILES}

           Analyze:
           1. Test coverage for changed code
           2. Test quality and maintainability
           3. Edge cases and error scenarios
           4. Mock/stub appropriateness
           5. Test level appropriateness (unit vs integration vs e2e)

           T-SHIRT SIZE ESTIMATE (from testing perspective):
           Based on testing complexity and coverage requirements:
           - XS: Minimal testing needed, simple assertions
           - S: Basic unit tests sufficient (1-2 test files)
           - M: Moderate testing (unit + some integration tests)
           - L: Comprehensive testing (unit + integration + edge cases)
           - XL: Extensive testing (e2e, multiple scenarios, complex mocks)
           - XXL: Critical path requiring exhaustive test coverage

           For each finding:
           - id: TEST-{NNN}
           - severity: low|medium|high
           - finding: Description
           - file: File being tested (or missing tests)
           - suggested_action: What tests to add/improve

           Output format:
           ```yaml
           test_coverage:
             t_shirt_size: XS|S|M|L|XL|XXL
             size_rationale: 'Brief explanation of size estimate'
             test_complexity: low|medium|high
             findings:
               - id: TEST-001
                 severity: medium
                 finding: '...'
                 # ... rest of fields
           ```"
)
```

### 2.7 Technical Debt Specialist

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Technical debt assessment",
  run_in_background: true,
  prompt: "You are a technical debt specialist.

           Changed files: {CHANGED_FILES}

           Identify:
           1. Accumulated shortcuts or TODOs
           2. Missing tests
           3. Outdated patterns or dependencies
           4. Architecture violations
           5. Code that should be refactored
           6. Documentation gaps

           T-SHIRT SIZE ESTIMATE (from tech debt/maintenance perspective):
           Based on long-term maintenance burden and tech debt:
           - XS: Clean implementation, no debt added
           - S: Minimal debt, well-documented
           - M: Some shortcuts taken, minor debt
           - L: Notable tech debt or maintenance concerns
           - XL: Significant debt that will require future cleanup
           - XXL: Major tech debt or legacy pattern perpetuation

           For each finding:
           - id: DEBT-{NNN}
           - severity: low|medium|high
           - finding: Description
           - file: File path
           - estimated_effort: small|medium|large
           - suggested_action: How to address

           Output format:
           ```yaml
           technical_debt:
             t_shirt_size: XS|S|M|L|XL|XXL
             size_rationale: 'Brief explanation of size estimate'
             maintenance_burden: low|medium|high
             findings:
               - id: DEBT-001
                 severity: low
                 finding: '...'
                 # ... rest of fields
           ```"
)
```

---

## Phase 3: Collect Results

**Wait for all specialists to complete:**

```
results = {
  traceability: TaskOutput(task_id: "{traceability_id}"),
  code_quality: TaskOutput(task_id: "{quality_id}"),
  security: TaskOutput(task_id: "{security_id}"),
  performance: TaskOutput(task_id: "{performance_id}"),
  accessibility: TaskOutput(task_id: "{accessibility_id}"),
  test_coverage: TaskOutput(task_id: "{coverage_id}"),
  technical_debt: TaskOutput(task_id: "{debt_id}")
}
```

---

## Phase 4: Aggregate Findings

**Combine all findings into unified structure:**

```yaml
review_summary:
  story: "{STORY_NUM}"
  reviewed_at: "{ISO-8601}"
  files_analyzed: {count}

  t_shirt_sizing:
    recommended_size: M  # Synthesized from all specialists
    confidence: high|medium|low
    specialist_estimates:
      requirements: { size: M, rationale: "..." }
      code_quality: { size: L, rationale: "..." }
      security: { size: S, rationale: "..." }
      performance: { size: M, rationale: "..." }
      accessibility: { size: M, rationale: "..." }
      test_coverage: { size: L, rationale: "..." }
      technical_debt: { size: M, rationale: "..." }
    size_breakdown:
      XS: 0 specialists
      S: 1 specialist
      M: 4 specialists
      L: 2 specialists
      XL: 0 specialists
      XXL: 0 specialists
    synthesis_rationale: |
      Final size recommendation based on:
      - Modal size: M (4/7 specialists)
      - Outliers: Code Quality (L), Test Coverage (L) due to [reason]
      - Risk factors: [key considerations]
      - Recommended: M with awareness of testing complexity

  checks:
    tests: { status: PASS|FAIL }
    types: { status: PASS|FAIL }
    lint: { status: PASS|FAIL }

  findings:
    total: {count}
    by_severity:
      high: {count}
      medium: {count}
      low: {count}
    by_category:
      security: {count}
      performance: {count}
      accessibility: {count}
      code_quality: {count}
      test_coverage: {count}
      technical_debt: {count}
      requirements: {count}

  traceability:
    ac_total: {count}
    ac_covered: {count}
    ac_gaps: {count}

  all_findings:
    - id: SEC-001
      category: security
      severity: high
      finding: "..."
      file: "..."
      suggested_action: "..."
    # ... all findings sorted by severity
```

**Synthesize T-Shirt Size:**

1. **Collect all specialist estimates:**
   - Extract t_shirt_size from each specialist's output
   - Extract rationale for each estimate

2. **Calculate modal size (most common):**
   - Count occurrences of each size
   - Identify the most frequent size

3. **Identify outliers:**
   - Flag estimates more than 1 size away from modal
   - Document why specialists disagree

4. **Apply weighting logic:**
   - Security/Requirements: Higher weight if XL or XXL (risk-based)
   - Code Quality: Higher weight if architectural complexity
   - Test Coverage: Consider for effort estimation
   - Technical Debt: Lower weight unless XXL

5. **Synthesize final recommendation:**
   - Start with modal size
   - Adjust up if high-risk outliers (Security XL/XXL)
   - Adjust up if multiple specialists cite complexity
   - Set confidence based on agreement level:
     - High: 5+ specialists agree
     - Medium: 3-4 specialists agree
     - Low: Wide spread, no clear modal

6. **Document synthesis rationale:**
   - Explain final size choice
   - Call out key risk factors
   - Note any caveats or warnings

**Deduplicate findings:**
- Merge similar findings from different specialists
- Keep highest severity when duplicated

---

## Phase 5: Auto-Fix (if --fix enabled)

**For findings with can_auto_fix: true:**

```
Task(
  subagent_type: "general-purpose",
  description: "Apply safe refactoring",
  prompt: "Apply these safe fixes:

           {FIXABLE_FINDINGS}

           Project guidelines: {CLAUDE_MD_CONTENT}

           For each fix:
           1. Make the change
           2. Run tests to verify
           3. Commit with message: 'refactor: {description}'

           Report what was fixed and what was skipped."
)
```

**Re-run required checks after fixes.**

---

## Phase 6: Run QA Gate

**Unless --no-gate specified:**

```
Invoke /qa-gate skill with:
- Story number (if provided)
- Aggregated findings
- Check results

The /qa-gate skill will:
- Determine gate decision (PASS/CONCERNS/FAIL)
- Create gate file at docs/qa/gates/{story}-{slug}.yml
- Return gate status
```

---

## Phase 7: Update Story File

**Append Review Findings section to story file:**

**Check if story file already has a `## Review Findings` section:**
- If yes: Replace it with updated findings
- If no: Append to end of file

```markdown
## Review Findings

> **Review Date:** {ISO-8601}
> **Reviewed By:** Claude Code
> **Gate:** {PASS|CONCERNS|FAIL} (score: {score}/100)
> **Gate File:** docs/qa/gates/{story}-{slug}.yml

### T-Shirt Size Estimate

**Recommended Size: {M}** (Confidence: {high|medium|low})

**Specialist Breakdown:**
| Specialist | Size | Rationale |
|------------|------|-----------|
| Requirements | M | 5-7 ACs with some test gaps |
| Code Quality | L | Moderate complexity, architectural considerations |
| Security | S | Standard auth checks, low risk |
| Performance | M | Some optimization needed (memoization) |
| Accessibility | M | Interactive UI requiring a11y attention |
| Test Coverage | L | Comprehensive testing needed (unit + integration) |
| Tech Debt | M | Minor shortcuts, well-documented |

**Size Distribution:** XS: 0, S: 1, **M: 4**, L: 2, XL: 0, XXL: 0

**Synthesis:**
Modal size is M (4/7 specialists). Code Quality and Test Coverage flagged as L due to architectural complexity and comprehensive testing requirements. Overall recommendation: **M** with awareness that testing effort may push toward upper end of estimate.

---

### Summary

- **Files Analyzed:** {count}
- **Total Findings:** {count} (high: {N}, medium: {N}, low: {N})
- **Traceability:** {N}/{M} acceptance criteria have test coverage

### Required Checks

| Check | Status |
|-------|--------|
| Tests | {PASS/FAIL} |
| Types | {PASS/FAIL} |
| Lint  | {PASS/FAIL} |

### Requirements Traceability

{If traceability gaps found:}
- **[REQ-001] {severity}:** {finding}
  - **File:** {file or N/A}
  - **Action:** {suggested_action}

{If no gaps:}
✓ All acceptance criteria have test coverage

### Code Quality

{For each finding:}
- **[QUAL-001] {severity}:** {finding}
  - **File:** {file}:{line}
  - **Action:** {suggested_action}

{If no findings:}
✓ No issues found

### Security

{For each finding:}
- **[SEC-001] {severity}:** {finding}
  - **File:** {file}:{line}
  - **CWE:** {cwe_reference}
  - **Action:** {suggested_action}

{If no findings:}
✓ No issues found

### Performance

{For each finding:}
- **[PERF-001] {severity}:** {finding}
  - **File:** {file}:{line}
  - **Impact:** {estimated_impact}
  - **Action:** {suggested_action}

{If no findings:}
✓ No issues found

### Accessibility

{For each finding:}
- **[A11Y-001] {severity}:** {finding}
  - **File:** {file}:{line}
  - **WCAG:** {wcag_criterion}
  - **Action:** {suggested_action}

{If no findings:}
✓ No issues found

### Test Coverage

{For each finding:}
- **[TEST-001] {severity}:** {finding}
  - **File:** {file}
  - **Action:** {suggested_action}

{If no findings:}
✓ No issues found

### Technical Debt

{For each finding:}
- **[DEBT-001] {severity}:** {finding}
  - **File:** {file}:{line}
  - **Effort:** {estimated_effort}
  - **Action:** {suggested_action}

{If no findings:}
✓ No issues found

{If --fix was used:}
### Refactoring Applied

- **{file}:** {what was changed and why}

### Recommendation

{If PASS:}
✓ **Ready for Done** - All checks passed, no blocking issues.

{If CONCERNS:}
⚠ **Review Required** - Address medium-severity issues and proceed with awareness.

{If FAIL:}
✗ **Changes Required** - Address high-severity issues before proceeding.

---
```

**Important:**
- Use Edit tool to replace existing `## Review Findings` section if present
- Organize findings by specialist category
- Show "✓ No issues found" for categories with zero findings
- List findings in order of severity (high → medium → low)
- Include file paths and line numbers for easy navigation

---

## Phase 8A: Report to User (Single Story)

**For single story review:**

```
═══════════════════════════════════════════════════════════════════
  Code Review Complete: {STORY_NUM} - {STORY_TITLE}
═══════════════════════════════════════════════════════════════════

Files Analyzed: {N}
Time Taken: {duration}

T-SHIRT SIZE ESTIMATE
  Recommended: M (Confidence: high)
  Breakdown: XS:0 S:1 M:4 L:2 XL:0 XXL:0

  Requirements:    M  (5-7 ACs with some gaps)
  Code Quality:    L  (Moderate complexity, architectural considerations)
  Security:        S  (Standard auth, low risk)
  Performance:     M  (Some optimization needed)
  Accessibility:   M  (Interactive UI, a11y attention required)
  Test Coverage:   L  (Comprehensive testing needed)
  Tech Debt:       M  (Minor shortcuts, well-documented)

REQUIRED CHECKS
  Tests:    {PASS|FAIL}
  Types:    {PASS|FAIL}
  Lint:     {PASS|FAIL}

SPECIALIST FINDINGS ({total} total)
  Security:       {N} issues ({high}H {medium}M {low}L) → Size: S
  Performance:    {N} issues ({high}H {medium}M {low}L) → Size: M
  Accessibility:  {N} issues ({high}H {medium}M {low}L) → Size: M
  Code Quality:   {N} issues ({high}H {medium}M {low}L) → Size: L
  Test Coverage:  {N} issues ({high}H {medium}M {low}L) → Size: L
  Technical Debt: {N} issues ({high}H {medium}M {low}L) → Size: M

REQUIREMENTS TRACEABILITY
  {covered}/{total} acceptance criteria have test coverage
  {gaps} gaps identified

TOP ISSUES
  1. [SEC-001] high: {finding}
  2. [PERF-001] medium: {finding}
  ...

{If --fix was used:}
REFACTORING APPLIED
  - {file}: {change}
  ...

GATE DECISION
  Status: {PASS|CONCERNS|FAIL}
  Gate File: docs/qa/gates/{story}-{slug}.yml

{If FAIL:}
RECOMMENDATION: Address high-severity issues before proceeding.

{If CONCERNS:}
RECOMMENDATION: Review medium-severity issues and proceed with awareness.

{If PASS:}
RECOMMENDATION: Ready for merge.

FINDINGS LOCATION
  Story file updated: {STORY_FILE_PATH}

═══════════════════════════════════════════════════════════════════
```

---

## Phase 8B: Summary Report (Directory Review)

**After all stories in directory have been reviewed:**

```
═══════════════════════════════════════════════════════════════════
  Epic Review Complete: {EPIC_NAME}
═══════════════════════════════════════════════════════════════════

Stories Reviewed: {N}
Total Time: {duration}

GATE SUMMARY
  PASS:     {N} stories
  CONCERNS: {N} stories
  FAIL:     {N} stories

T-SHIRT SIZE DISTRIBUTION
  XS:  {N} stories
  S:   {N} stories
  M:   {N} stories
  L:   {N} stories
  XL:  {N} stories
  XXL: {N} stories

  Epic Effort Estimate: {sum of sizes} → ~{estimate} story points

FINDINGS BY STORY

┌─────────────────────────────────────────────────────────────────┐
│ {story-1-id} - {story-1-title}
├─────────────────────────────────────────────────────────────────┤
│ Size:     M (Confidence: high)
│ Gate:     {PASS|CONCERNS|FAIL}
│ Findings: {total} ({high}H {medium}M {low}L)
│ File:     {story_file_path}
│ Gate:     docs/qa/gates/{story-1}-{slug}.yml
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ {story-2-id} - {story-2-title}
├─────────────────────────────────────────────────────────────────┤
│ Gate:     {PASS|CONCERNS|FAIL}
│ Findings: {total} ({high}H {medium}M {low}L)
│ File:     {story_file_path}
│ Gate:     docs/qa/gates/{story-2}-{slug}.yml
└─────────────────────────────────────────────────────────────────┘

{... for each story}

AGGREGATE STATISTICS

Total Findings: {total_across_all_stories}
  High:    {N}
  Medium:  {N}
  Low:     {N}

By Category:
  Security:       {N} findings across {M} stories
  Performance:    {N} findings across {M} stories
  Accessibility:  {N} findings across {M} stories
  Code Quality:   {N} findings across {M} stories
  Test Coverage:  {N} findings across {M} stories
  Technical Debt: {N} findings across {M} stories

MOST COMMON ISSUES (Top 5)

1. {issue_type}: {N} occurrences across {M} stories
2. {issue_type}: {N} occurrences across {M} stories
3. {issue_type}: {N} occurrences across {M} stories
4. {issue_type}: {N} occurrences across {M} stories
5. {issue_type}: {N} occurrences across {M} stories

RECOMMENDATION

{If any FAIL:}
⚠ {N} stories require changes before proceeding.
  → Review findings in each story file and address blocking issues.

{If any CONCERNS but no FAIL:}
⚠ {N} stories have concerns.
  → Review findings and proceed with awareness of identified issues.

{If all PASS:}
✓ All stories passed review! Ready for implementation or merge.

NEXT STEPS

Review detailed findings in each story file:
{For each story with FAIL or CONCERNS:}
  - {story_file_path}

═══════════════════════════════════════════════════════════════════
```

**Aggregate Analysis:**
1. Count stories by gate status (PASS/CONCERNS/FAIL)
2. Sum total findings across all stories
3. Identify most common issue types across stories
4. Provide actionable next steps

---

## Sub-Agent Architecture

```
Main Orchestrator (/review)
    │
    ├─▶ Context Gathering (inline)
    │
    ├─▶ Required Checks (inline)
    │   ├── pnpm test
    │   ├── pnpm check-types
    │   └── pnpm lint
    │
    ├─▶ Specialist Sub-Agents (parallel, haiku)
    │   ├── Requirements Traceability
    │   ├── Code Quality
    │   ├── Security
    │   ├── Performance
    │   ├── Accessibility
    │   ├── Test Coverage
    │   └── Technical Debt
    │
    ├─▶ Aggregation (inline)
    │
    ├─▶ Auto-Fix (optional, general-purpose)
    │
    └─▶ /qa-gate (produces gate file)
```

---

## Issue ID Prefixes

| Prefix | Specialist |
|--------|------------|
| SEC- | Security |
| PERF- | Performance |
| A11Y- | Accessibility |
| QUAL- | Code Quality |
| TEST- | Test Coverage |
| DEBT- | Technical Debt |
| REQ- | Requirements Traceability |

---

## When to Use

### /review (comprehensive)
- Pre-merge reviews
- Story completion reviews
- Major feature reviews
- Security-sensitive changes

### /review --quick
- Small changes
- Documentation updates
- Minor fixes

### /qa-gate (standalone)
- Quick pass/fail decision
- CI/CD integration
- Automated checks only
