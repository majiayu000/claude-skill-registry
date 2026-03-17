---
name: refactor-code
description: Safely improve code quality through test-driven refactoring with automatic validation and rollback. Use during quality review to reduce technical debt while preserving behavior.
acceptance:
  - config_validated: "Configuration allows refactoring and prerequisites verified"
  - opportunities_identified: "Refactoring opportunities identified and prioritized by risk"
  - refactorings_applied: "Selected refactorings applied incrementally with test validation"
  - log_created: "Refactoring log documenting all changes with rationale"
  - tests_passing: "All tests passing after refactoring with no behavioral changes"
inputs:
  task_file:
    type: string
    required: true
    description: "Path to task specification with quality findings"
  aggressiveness:
    type: enum
    required: false
    description: "Refactoring scope: conservative, moderate, aggressive"
    default: "moderate"
  allow_refactoring:
    type: boolean
    required: false
    description: "Override config to allow/disallow refactoring"
outputs:
  refactorings_applied:
    type: number
    description: "Number of refactorings successfully applied"
  refactorings_failed:
    type: number
    description: "Number of refactorings that failed and were rolled back"
  files_modified:
    type: array
    description: "List of files modified during refactoring"
  quality_impact:
    type: object
    description: "Before/after quality metrics showing improvements"
telemetry:
  emit: "skill.refactor-code.completed"
  track:
    - refactorings_applied
    - refactorings_failed
    - refactorings_skipped
    - success_rate
    - files_modified_count
    - quality_improvement_percent
    - duration_ms
---

# Refactor Code Skill

## Purpose

Safely improve code quality through automated refactoring while maintaining behavioral correctness. This skill identifies refactoring opportunities from quality findings and applies them incrementally with continuous test validation.

**Core Capabilities:**
- Test-driven refactoring (run tests after each change)
- Automatic rollback on test failures
- Risk-based prioritization (P0-P3, Low/Medium/High risk)
- Incremental application (one refactoring at a time)
- Full traceability (log all changes with rationale)
- Quality metrics tracking (before/after comparison)

**Key Innovation:**
Safety-first approach ensures refactorings never break functionality. Each change is validated with tests before proceeding.

## Prerequisites

- Task status is "Review"
- Quality assessment has been run (quality gate exists)
- Tests exist and are currently passing
- Configuration allows refactoring (`quality.allowRefactoring: true`)

---

## Workflow

### Step 0: Load Configuration and Validate Prerequisites

**Action:** Verify refactoring is allowed and safe to proceed.

**Load configuration:** Read `.claude/config.yaml` for refactoring settings

**See:** `references/templates.md#configuration-format` for complete config structure

**Check prerequisites:**
1. Verify `allowRefactoring: true` in config (or input override)
2. Verify task status is "Review"
3. Verify quality assessment exists (`.claude/quality/gates/{task-id}-gate.yaml`)
4. Verify tests exist and are passing

**Get refactoring scope:** Ask user to choose Conservative/Moderate/Aggressive or Skip

**See:** `references/templates.md#user-decision-refactoring-scope` for prompt format

**Halt if:**
- Configuration disables refactoring and no input override
- No tests exist (can't validate safety)
- Tests are currently failing
- Quality assessment not yet run
- User chooses to skip

**Output:** Prerequisites validation summary (config, tests, scope)

**See:** `references/templates.md#step-0-output-template` for format

**See:** `references/risk-assessment-guide.md` for aggressiveness levels

---

### Step 1: Analyze Code for Refactoring Opportunities

**Action:** Identify specific refactoring opportunities based on quality findings.

**Load quality findings:**
1. Read quality gate file (`.claude/quality/gates/{task-id}-gate.yaml`)
2. Extract issues by severity (critical, high, medium, low)
3. Extract technical debt items
4. Extract code quality findings

**Scan implementation files:**
Read all files from task Implementation Record and identify patterns:
- **Extract Method**: Long methods (>50 lines)
- **Extract Variable**: Complex expressions
- **Rename**: Unclear variable/function names
- **Remove Duplication**: Repeated code blocks (2+ occurrences)
- **Simplify Conditionals**: Nested if/else chains
- **Extract Class**: Classes with too many responsibilities
- **Inline**: Unnecessary indirection
- **Move Method**: Misplaced functionality

**Prioritize refactorings:**
- **P0 (Critical):** Addresses critical/high severity quality issues
- **P1 (High):** Reduces technical debt
- **P2 (Medium):** Improves maintainability
- **P3 (Low):** Nice-to-have improvements

**Estimate risk for each:**
- **Low Risk:** Rename, extract variable, inline
- **Medium Risk:** Extract method, simplify conditionals
- **High Risk:** Extract class, move method, large-scale changes

**Filter by aggressiveness level:**
- **Conservative:** P0 only, low-risk refactorings
- **Moderate:** P0 + P1, low-to-medium risk refactorings
- **Aggressive:** P0 + P1 + P2, all risk levels

**Output:** List of refactoring opportunities with priority, risk, file location, rationale, and impact

**See:** `references/templates.md#step-1-output-template` for complete format

**Halt if:**
- No refactoring opportunities identified (already clean code)
- All refactorings exceed chosen aggressiveness level
- All refactorings are high-risk (safety concern)

**See:** `references/refactoring-patterns.md` for pattern identification

---

### Step 2: Apply Refactorings Incrementally

**Action:** Apply each refactoring one at a time with test validation.

**For each selected refactoring (in priority order):**

**For each refactoring:**
1. Announce what's being refactored (file, type, risk)
2. Apply single refactoring (read, transform, write, backup)
3. Run tests immediately (`npm test`)
4. Evaluate results:
   - If pass: Log success, keep changes, proceed
   - If fail: Rollback, log failure, skip to next
5. Update progress count (applied/skipped/failed)

**Safety rules:**
- Never apply multiple refactorings simultaneously
- Never skip test validation
- Never continue if critical (P0) refactoring fails
- Never modify tests to make them pass
- Always preserve backups until tests pass

**Output:** Refactoring completion summary with success/failure counts and test status

**See:** `references/templates.md#step-2-output-templates` for all step outputs

**Halt if:**
- Multiple consecutive failures (>3)
- Tests fail and can't be restored
- User requests halt
- Time limit exceeded (optional safety)

**See:** `references/incremental-application-guide.md` for detailed process

---

### Step 3: Create Refactoring Log

**Action:** Document all refactoring changes with rationale.

**Create/update log file:**
- Path: `.claude/quality/refactoring-log.md`
- Append new entry (preserve existing logs)

**Log structure:** Append session entry to `.claude/quality/refactoring-log.md` with:
- Session metadata (task, scope, duration, success rate)
- Each refactoring applied (file, type, risk, rationale, before/after, impact, tests)
- Refactorings failed (if any)
- Files modified with line count changes
- Test results (before/after)
- Quality impact metrics

**See:** `references/templates.md#step-3-refactoring-log-template` for complete structure

**Update quality gate file:**
- Add refactoring summary to gate file
- Update code quality metrics
- Note improvements in maintainability

**Output:** Log creation confirmation with file path and refactoring counts

**See:** `references/templates.md#step-3-output-template`

**See:** `references/refactoring-log-template.md` for complete structure

---

### Step 4: Final Test Validation and Summary

**Action:** Confirm all tests pass and provide comprehensive summary.

**Run full test suite:**
```bash
npm test
npm run test:integration  # if exists
npm run test:e2e          # if exists
```

**Generate coverage report:**
```bash
npm run test:coverage  # if configured
```

**Compare before/after metrics:** Calculate improvements in lines, complexity, duplication, coverage

**See:** `references/templates.md#step-4-metrics-comparison-template` for complete format

**Provide final summary:** Present comprehensive summary with status, counts, quality improvements, files modified, next steps

**See:** `references/templates.md#step-4-final-summary-template` for complete format

**Update task file:**
Append refactoring summary to task's Quality Review section with:
- Date and scope
- Success rate
- Refactorings applied
- Quality impact
- Test validation results

**Halt if:**
- Final test suite fails (critical issue)
- Coverage drops significantly (regression)
- User reports unexpected behavior

---

## Completion Criteria

Refactoring is complete when:

- [ ] Prerequisites validated (config, tests, quality gate)
- [ ] Refactoring opportunities identified and prioritized
- [ ] Selected refactorings applied incrementally
- [ ] All tests passing after refactoring
- [ ] Refactoring log created with full documentation
- [ ] Task file updated with summary
- [ ] Quality metrics improved or maintained
- [ ] User notified with actionable next steps

---

## Safety Guarantees

**Behavioral preservation** (no functionality changes) | **Test validation** (after each change) | **Automatic rollback** (on failures) | **Full traceability** (logged) | **Incremental** (one at a time) | **User control** (choose scope)

---

## Integration with Quality Review

Runs **after nfr-assess, before quality-gate** in quality workflow. Optional - only if user opts in and tests exist/pass. Improvements reflected in final gate decision.

---

## Routing Guidance

**Use this skill when:**
- Quality review identifies refactoring opportunities
- Technical debt needs systematic reduction
- Code quality metrics below targets
- Maintainability concerns raised in review
- User opts in for automated improvements

**Do NOT use for:**
- Feature additions (use implementation skills)
- Bug fixes (use fix-issue skill)
- Breaking changes (requires manual review)
- Experimental refactorings (too risky)
- Projects without tests (can't validate safety)

**Feeds into:**
- quality-gate skill (improved metrics inform decision)

---

## Best Practices

1. **Start Conservative:**
   - First session: Use conservative mode
   - Build confidence before moderate/aggressive

2. **Review Changes:**
   - Always review refactored code via git diff
   - Verify alignment with coding style
   - Check for unintended consequences

3. **Commit Separately:**
   - Commit refactorings separate from features
   - Message: "refactor: {description} (automated)"

4. **Monitor Impact:**
   - Track quality metrics over time
   - Verify maintainability improves
   - Identify patterns to refactor proactively

---

## Reference Files

Detailed documentation in `references/`:

- **templates.md**: All output formats, config examples, log templates
- **refactoring-patterns.md**: Common refactoring patterns with examples
- **risk-assessment-guide.md**: Risk levels, assessment, filtering by aggressiveness
- **incremental-application-guide.md**: Step-by-step application, test validation, rollback
- **refactoring-log-template.md**: Log structure and documentation format

---

*Part of BMAD Enhanced Quality Suite*
