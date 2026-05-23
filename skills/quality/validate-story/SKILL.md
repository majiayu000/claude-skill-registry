---
name: validate-story
description: Pre-implementation story validation with 10-step comprehensive assessment including template compliance, anti-hallucination verification, and implementation readiness scoring. This skill should be used before handing story to development agent.
acceptance:
  - validation_complete: "All 10 validation steps executed successfully"
  - go_no_go_decision: "Clear GO or NO-GO decision with confidence level"
  - report_generated: "Validation report created with findings and recommendations"
  - critical_issues_identified: "All blocking issues identified and documented"
inputs:
  story_file:
    type: string
    required: true
    description: "Path to story file in .claude/stories/{epic-id}/{story-id}.md format"
  validation_mode:
    type: enum
    values: ["full", "quick", "critical_only"]
    default: "full"
    description: "Validation depth: full (all 10 steps), quick (critical steps only), critical_only (blocking issues)"
outputs:
  validation_passed:
    type: boolean
    description: "GO (true) or NO-GO (false) decision"
  readiness_score:
    type: number
    description: "Implementation readiness score (1-10)"
  confidence_level:
    type: enum
    values: ["High", "Medium", "Low"]
    description: "Confidence in successful implementation"
  critical_issues:
    type: array
    description: "Must-fix issues blocking implementation"
  should_fix_issues:
    type: array
    description: "Important quality improvements (recommended)"
  nice_to_have:
    type: array
    description: "Optional enhancements"
  anti_hallucination_findings:
    type: array
    description: "Unverifiable claims or invented details"
telemetry:
  emit: "skill.validate-story.completed"
  track:
    - story_id
    - validation_passed
    - readiness_score
    - confidence_level
    - critical_issues_count
    - should_fix_count
    - anti_hallucination_count
    - duration_ms
---

# Validate Story

Pre-implementation story validation with comprehensive 10-step assessment to catch issues before development begins.

## Purpose

Before handing a story to James (Developer Agent), validate that the story is complete, accurate, and implementable. Catch template gaps, hallucinated details, and missing context that would cause implementation failures.

**Core Principles:**
- **Comprehensive** - 10 validation steps cover all critical aspects
- **Anti-hallucination** - Verify all technical claims against source documents
- **Actionable** - Every issue has clear fix guidance
- **GO/NO-GO clarity** - Binary decision with confidence level
- **Educational** - Report teaches story creators what to improve

**Integration:**
- **Input:** Story markdown file from story creation process
- **Processing:** 10-step validation → Issue identification → Report generation
- **Output:** Validation report with GO/NO-GO decision + issues + recommendations

## When to Use This Skill

**This skill should be used when:**
- Story just created, before implementation
- Story updated, needs re-validation
- Pre-sprint planning (validate backlog stories)
- Story handed from PO → Dev team

**This skill should NOT be used when:**
- Story already in implementation
- Quick review needed (use quick mode)
- Story is template/draft only

## Prerequisites

- Story file exists in `.claude/stories/{epic-id}/{story-id}.md`
- Story template available (for comparison)
- Parent epic file exists (if story references epic)
- Architecture/project docs available (for anti-hallucination checks)

---

## 10-Step Validation Workflow

### Step 0: Load Configuration and Story

**Purpose:** Load project configuration, story file, template, and related documents.

**Actions:**

1. **Load Story File:**

   Use Claude Code Read tool:
   ```
   Read: .claude/stories/{epic-id}/{story-id}.md
   ```

   Extract metadata:
   - Story ID
   - Epic ID (if referenced)
   - Title
   - Status
   - All sections

2. **Load Story Template:**

   ```
   Read: .claude/skills/planning/create-story/references/templates.md
   ```

   Extract template structure:
   - Required sections
   - Optional sections
   - Expected placeholders

3. **Load Parent Epic (if applicable):**

   If story references epic:
   ```
   Read: .claude/epics/{epic-id}.md
   ```

   Verify story aligns with epic objectives.

4. **Load Project Structure:**

   ```
   Read: docs/unified-project-structure.md
   ```

   For validating file paths and directory structure.

5. **Load Architecture Docs (for anti-hallucination):**

   ```
   Read: docs/architecture/*.md
   ```

   For verifying technical claims.

**Outputs:**
- `story_content` - Full story text
- `template_sections[]` - Required sections from template
- `epic_context` - Parent epic details
- `project_structure` - Expected file/directory layout
- `architecture_docs[]` - Technical reference docs

**See:** `references/templates.md` for story template structure

---

### Step 1: Template Completeness Validation

**Purpose:** Ensure all required template sections present and no unfilled placeholders.

**Actions:**

1. **Extract Story Sections:**

   Parse story markdown to extract sections:
   - Objective
   - Context
   - Acceptance Criteria
   - Tasks/Subtasks
   - Dev Notes
   - Testing & Validation
   - File List
   - Dependencies
   - etc.

2. **Compare with Template:**

   For each required section in template:
   - ✅ Section exists in story
   - ✅ Section has content (not empty)
   - ✅ Section content is meaningful (not placeholder text)

3. **Check for Unfilled Placeholders:**

   Search for placeholder patterns:
   - `{{EpicNum}}`, `{{StoryNum}}`, `{{var}}`
   - `_TBD_`, `[TBD]`, `TODO`
   - `...`, `[more details needed]`

4. **Report Missing/Incomplete Sections:**

   ```
   Critical Issues:
   - Missing section: "Testing & Validation"
   - Unfilled placeholder: {{EpicNum}} in Objective
   - Empty section: "Dependencies"

   Should-Fix:
   - Section "Dev Notes" has only 2 lines (expected detailed technical context)
   ```

**Validation Criteria:**
- ✅ All required sections present
- ✅ No unfilled placeholders (`{{var}}`, `_TBD_`)
- ✅ Sections have meaningful content (>3 lines for substantial sections)

**Outputs:**
- `missing_sections[]` - Required sections not found
- `unfilled_placeholders[]` - Placeholder patterns still in story
- `empty_sections[]` - Sections with no/minimal content

**See:** `references/validation-checklist.md` for detailed template requirements

---

### Step 2: File Structure and Source Tree Validation

**Purpose:** Verify file paths, directory structure, and source tree references are accurate and consistent.

**Actions:**

1. **Extract File References:**

   From story sections (File List, Tasks, Dev Notes):
   - New files to create
   - Existing files to modify
   - Directories mentioned

2. **Validate File Paths:**

   For each file path:
   - ✅ Matches project structure (src/, tests/, docs/)
   - ✅ Uses consistent separators (forward slashes)
   - ✅ No absolute paths (only relative to project root)
   - ✅ File extensions correct (.ts, .js, .md, .yaml)

3. **Check Directory Consistency:**

   - ✅ All files in same directory use consistent structure
   - ✅ Test files in test directory
   - ✅ Source files in source directory
   - ✅ No mixing of unrelated files

4. **Verify Source Tree References:**

   If story mentions project structure:
   - ✅ References valid directories from `docs/unified-project-structure.md`
   - ✅ Directory names match exactly (case-sensitive)
   - ✅ No invented directories not in project

5. **Report File Structure Issues:**

   ```
   Critical Issues:
   - File path uses Windows separators: "src\auth\login.ts" (should be "src/auth/login.ts")
   - Referenced directory doesn't exist: "src/services/auth/" (project has "src/auth/")

   Should-Fix:
   - Test file in source directory: "src/api/user.test.ts" (should be "tests/api/user.test.ts")
   ```

**Validation Criteria:**
- ✅ File paths match project structure
- ✅ Consistent directory naming
- ✅ Appropriate file locations (tests in tests/, src in src/)
- ✅ No invented directories

**Outputs:**
- `invalid_paths[]` - File paths that don't match project structure
- `inconsistent_dirs[]` - Directory naming issues
- `file_location_issues[]` - Files in wrong locations

**See:** `references/validation-checklist.md` for file structure rules

---

### Step 3: UI/Frontend Completeness (if applicable)

**Purpose:** For frontend/UI stories, ensure design, components, and interactions are fully specified.

**Actions:**

1. **Detect UI Story:**

   Check if story involves frontend:
   - Keywords: "UI", "component", "page", "view", "styling", "responsive"
   - File references: `.tsx`, `.vue`, `.jsx`, `.html`, `.css`
   - Tasks mention UI/UX work

2. **If UI Story, Validate:**

   **Component Specifications:**
   - ✅ Component names specified
   - ✅ Component hierarchy clear (parent/child)
   - ✅ Props/inputs documented

   **Styling/Design:**
   - ✅ Design guidance provided (colors, spacing, layout)
   - ✅ Responsive behavior specified (mobile, tablet, desktop)
   - ✅ Accessibility requirements mentioned (ARIA, keyboard nav)

   **User Interactions:**
   - ✅ User flows documented (click → modal → submit)
   - ✅ Form validation specified
   - ✅ Error states defined

   **Frontend-Backend Integration:**
   - ✅ API endpoints specified
   - ✅ Data models documented
   - ✅ Loading states defined

3. **Report UI Completeness Issues:**

   ```
   Critical Issues:
   - No responsive design guidance (mobile/tablet behavior undefined)

   Should-Fix:
   - Missing accessibility requirements (ARIA labels, keyboard navigation)
   - Form validation rules not specified
   ```

**Validation Criteria (for UI stories):**
- ✅ Component specifications sufficient
- ✅ Styling/design guidance clear
- ✅ User interaction flows specified
- ✅ Responsive/accessibility addressed
- ✅ Frontend-backend integration clear

**Outputs:**
- `ui_component_issues[]` - Component specification gaps
- `ui_design_issues[]` - Design/styling gaps
- `ui_interaction_issues[]` - User flow gaps

**See:** `references/validation-checklist.md` for UI validation details

---

### Step 4: Acceptance Criteria Satisfaction

**Purpose:** Ensure tasks will actually satisfy all acceptance criteria when implemented.

**Actions:**

1. **Extract Acceptance Criteria:**

   From story "Acceptance Criteria" section:
   - List all ACs with IDs (AC1, AC2, AC3, ...)

2. **Extract Tasks:**

   From story "Tasks/Subtasks" section:
   - List all tasks with descriptions

3. **Map Tasks to ACs:**

   For each AC:
   - Find tasks that address this AC
   - Verify tasks are sufficient to satisfy AC

4. **Identify Gaps:**

   ```
   Coverage Analysis:
   AC1 "User can log in" → Task 1.1, Task 1.2 ✅
   AC2 "Password reset works" → Task 2.1 ✅
   AC3 "Session timeout" → No tasks found ❌

   Gaps:
   - AC3 has no implementing tasks
   - AC4 partially covered (only happy path, no error cases)
   ```

5. **Verify AC Testability:**

   For each AC:
   - ✅ Measurable (can verify success/failure)
   - ✅ Specific (not vague like "should work well")
   - ✅ Has success criteria

6. **Report AC Issues:**

   ```
   Critical Issues:
   - AC3 "Session timeout" has no implementing tasks
   - AC5 too vague: "System should be secure" (not measurable)

   Should-Fix:
   - AC2 missing error case testing
   - AC4 missing edge case handling
   ```

**Validation Criteria:**
- ✅ All ACs have implementing tasks
- ✅ Tasks sufficient to satisfy ACs
- ✅ ACs are testable and measurable
- ✅ Edge cases covered

**Outputs:**
- `uncovered_acs[]` - ACs with no implementing tasks
- `partial_coverage_acs[]` - ACs partially covered
- `vague_acs[]` - ACs not measurable/testable

**See:** `references/validation-checklist.md` for AC validation rules

---

### Step 5: Validation and Testing Instructions

**Purpose:** Ensure testing approach is clear and comprehensive.

**Actions:**

1. **Extract Testing Section:**

   From "Testing & Validation" section:
   - Test approach
   - Test scenarios
   - Validation steps
   - Testing tools

2. **Validate Test Approach:**

   - ✅ Testing strategy clear (unit, integration, e2e)
   - ✅ Test scenarios identified
   - ✅ Validation steps specific (not just "test it")
   - ✅ Testing tools specified (Jest, Pytest, Mocha, etc.)

3. **Check Test Coverage:**

   For each AC:
   - ✅ Has corresponding test scenarios
   - ✅ Happy path tested
   - ✅ Error cases tested
   - ✅ Edge cases tested

4. **Verify Test Data Requirements:**

   - ✅ Test data needs identified (fixtures, mocks, seeds)
   - ✅ Test environment specified (local, staging, CI)

5. **Report Testing Issues:**

   ```
   Critical Issues:
   - No test scenarios for AC3
   - Testing section says "test manually" (not specific)

   Should-Fix:
   - Missing integration test scenarios
   - No test data requirements specified
   ```

**Validation Criteria:**
- ✅ Test approach clarity
- ✅ Test scenarios identified
- ✅ Validation steps clear
- ✅ Testing tools specified
- ✅ Test data requirements identified

**Outputs:**
- `missing_test_scenarios[]` - ACs without test scenarios
- `vague_testing[]` - Non-specific testing instructions
- `test_data_gaps[]` - Missing test data requirements

**See:** `references/validation-checklist.md` for testing validation

---

### Step 6: Security Considerations (if applicable)

**Purpose:** For security-critical stories, ensure security requirements are identified and addressed.

**Actions:**

1. **Detect Security-Critical Story:**

   Keywords: "auth", "password", "token", "encryption", "secure", "permission", "access control"

2. **If Security-Critical, Validate:**

   **Security Requirements:**
   - ✅ Authentication/authorization specified
   - ✅ Data protection requirements clear (encryption, hashing)
   - ✅ Input validation requirements specified
   - ✅ Vulnerability prevention addressed (SQL injection, XSS, CSRF)

   **Compliance:**
   - ✅ Regulatory requirements mentioned (GDPR, PCI-DSS, HIPAA)
   - ✅ Security best practices referenced

3. **Report Security Issues:**

   ```
   Critical Issues:
   - Story involves password storage but no hashing requirements specified
   - No input validation mentioned for user registration

   Should-Fix:
   - Missing rate limiting requirements
   - No mention of HTTPS enforcement
   ```

**Validation Criteria (for security stories):**
- ✅ Security requirements identified
- ✅ Authentication/authorization specified
- ✅ Data protection clear
- ✅ Vulnerability prevention addressed
- ✅ Compliance requirements addressed

**Outputs:**
- `security_gaps[]` - Missing security requirements
- `compliance_issues[]` - Compliance gaps

**See:** `references/validation-checklist.md` for security validation

---

### Step 7: Tasks/Subtasks Sequence Validation

**Purpose:** Ensure tasks are in logical order with clear dependencies.

**Actions:**

1. **Extract Task Sequence:**

   From "Tasks/Subtasks":
   - List tasks in order
   - Identify dependencies

2. **Validate Logical Order:**

   - ✅ Prerequisites before dependent tasks (e.g., create model before controller)
   - ✅ Setup tasks before implementation tasks
   - ✅ Implementation before testing
   - ✅ No circular dependencies

3. **Check Task Granularity:**

   - ✅ Tasks are appropriately sized (not too broad, not too granular)
   - ✅ Each task is actionable (clear what to do)
   - ✅ Tasks are testable (can verify completion)

4. **Verify Completeness:**

   - ✅ All necessary tasks present
   - ✅ No missing steps between tasks
   - ✅ All ACs covered by tasks (cross-check with Step 4)

5. **Report Task Sequence Issues:**

   ```
   Critical Issues:
   - Task 3 depends on Task 5 (circular dependency)
   - Task 2 "Implement controller" before Task 1 "Create model" (wrong order)

   Should-Fix:
   - Task granularity too broad: "Implement entire auth system" (break down)
   - Missing task: "Add integration tests" (not in task list)
   ```

**Validation Criteria:**
- ✅ Logical order (dependencies before dependents)
- ✅ Appropriate granularity
- ✅ Complete (all steps present)
- ✅ Actionable (clear instructions)

**Outputs:**
- `task_order_issues[]` - Tasks in wrong order
- `task_dependency_issues[]` - Circular or unclear dependencies
- `task_granularity_issues[]` - Tasks too broad or too fine

**See:** `references/validation-checklist.md` for task validation

---

### Step 8: Anti-Hallucination Verification

**Purpose:** Verify all technical claims are traceable to source documents, not invented.

**Actions:**

1. **Extract Technical Claims:**

   From story (Dev Notes, Tasks, File List):
   - File/directory names
   - Library/framework names
   - API endpoints
   - Database tables/columns
   - Architecture patterns
   - Configuration settings

2. **Verify Against Sources:**

   **File/Directory Claims:**
   - ✅ Check against `docs/unified-project-structure.md`
   - ❌ Flag files/dirs not in project structure

   **Library/Framework Claims:**
   - ✅ Check against `package.json`, `requirements.txt`, architecture docs
   - ❌ Flag libraries not in dependencies

   **API Endpoint Claims:**
   - ✅ Check against `docs/architecture/api-spec.md`
   - ❌ Flag endpoints not documented

   **Database Claims:**
   - ✅ Check against `docs/architecture/database-schema.md`
   - ❌ Flag tables/columns not in schema

   **Architecture Pattern Claims:**
   - ✅ Check against `docs/architecture/` docs
   - ❌ Flag patterns not documented

3. **Identify Hallucinations:**

   ```
   Anti-Hallucination Findings:

   Critical:
   - Story claims "bcrypt library" but not in package.json dependencies
   - References "auth-service.ts" but no such file in project structure
   - Mentions "Redis cache" but architecture docs don't specify Redis

   Should-Fix:
   - Claims "JWT authentication" but architecture uses sessions
   - References "/api/users" endpoint not in API spec
   ```

4. **Flag Unverifiable Claims:**

   - Claims with no source reference
   - Details too specific to be general knowledge
   - Technical choices not documented in architecture

**Validation Criteria:**
- ✅ Source verification (all claims traceable)
- ✅ Architecture alignment (matches specs)
- ✅ No invented details (all backed by sources)
- ✅ Reference accuracy (sources correct and accessible)

**Outputs:**
- `hallucinated_files[]` - Files/dirs not in project
- `hallucinated_libs[]` - Libraries not in dependencies
- `hallucinated_apis[]` - API endpoints not documented
- `hallucinated_patterns[]` - Patterns not in architecture

**See:** `references/validation-checklist.md` for anti-hallucination checks

---

### Step 9: Dev Agent Implementation Readiness

**Purpose:** Assess if story provides sufficient context for developer agent to implement without external docs.

**Actions:**

1. **Check Self-Contained Context:**

   - ✅ All necessary technical details in story (not requiring external doc reading)
   - ✅ Dev Notes section comprehensive
   - ✅ File structure clear
   - ✅ Implementation approach specified

2. **Verify Clear Instructions:**

   - ✅ Tasks are unambiguous (developer knows exactly what to do)
   - ✅ No vague instructions ("implement as needed", "use best practices")
   - ✅ Technical choices specified (which library, which pattern)

3. **Assess Complete Technical Context:**

   From Dev Notes:
   - ✅ Technical approach explained
   - ✅ Key implementation details provided
   - ✅ Potential gotchas mentioned
   - ✅ Integration points documented

4. **Identify Missing Information:**

   ```
   Implementation Readiness Issues:

   Critical:
   - Dev Notes missing: No technical approach specified
   - Vague task: "Implement authentication" (which method? OAuth? JWT? Sessions?)

   Should-Fix:
   - Missing integration details: How does this connect to existing auth system?
   - No error handling guidance
   ```

5. **Score Implementation Readiness:**

   **Readiness Score (1-10):**
   - 9-10: Fully ready, developer can start immediately
   - 7-8: Minor gaps, easily filled during implementation
   - 5-6: Significant gaps, requires clarification before starting
   - 3-4: Major gaps, story needs substantial rework
   - 1-2: Not ready, critical information missing

**Validation Criteria:**
- ✅ Self-contained context (no external docs needed)
- ✅ Clear instructions (unambiguous steps)
- ✅ Complete technical context (all details in Dev Notes)
- ✅ All tasks actionable

**Outputs:**
- `readiness_score` - Score 1-10
- `missing_context[]` - Missing technical details
- `vague_instructions[]` - Ambiguous tasks
- `external_refs_needed[]` - References to external docs required

**See:** `references/validation-checklist.md` for readiness assessment

---

### Step 10: Generate Validation Report

**Purpose:** Synthesize all validation findings into actionable report with GO/NO-GO decision.

**Actions:**

1. **Categorize Issues:**

   **Critical Issues (Must Fix - Story Blocked):**
   - Missing required sections
   - Unfilled placeholders
   - Uncovered acceptance criteria
   - Hallucinated technical details
   - Circular task dependencies

   **Should-Fix Issues (Important Quality):**
   - Vague testing instructions
   - Missing security considerations
   - Incomplete file structure
   - Poor task granularity

   **Nice-to-Have (Optional Enhancements):**
   - Additional test scenarios
   - More detailed Dev Notes
   - Better task descriptions

2. **Calculate Readiness Score:**

   ```
   Readiness Score Calculation:
   Base: 10 points

   Deductions:
   - Critical issues: -2 points each
   - Should-fix issues: -0.5 points each
   - Anti-hallucination findings: -1 point each

   Score = max(1, 10 - total_deductions)
   ```

3. **Determine Confidence Level:**

   - **High:** Readiness ≥ 8, no critical issues, ≤2 should-fix
   - **Medium:** Readiness 5-7, ≤3 critical issues, ≤5 should-fix
   - **Low:** Readiness ≤4, >3 critical issues, or >5 should-fix

4. **Make GO/NO-GO Decision:**

   **GO Criteria:**
   - No critical issues, OR
   - ≤2 critical issues AND readiness ≥ 7

   **NO-GO Criteria:**
   - >2 critical issues, OR
   - Readiness < 7, OR
   - Any critical anti-hallucination findings

5. **Generate Report:**

   ```markdown
   # Story Validation Report

   **Story:** {epic-id}/{story-id} - {title}
   **Validated:** {date}
   **Validator:** validate-story skill

   ## Summary

   **Decision:** GO / NO-GO
   **Readiness Score:** {score}/10
   **Confidence Level:** High / Medium / Low

   ## Validation Results

   ### Template Compliance: ✅ PASS / ❌ FAIL
   - All required sections present
   - No unfilled placeholders

   ### File Structure: ✅ PASS / ⚠️ CONCERNS / ❌ FAIL
   - File paths match project structure
   - Consistent directory naming

   [... continue for all 10 validation steps ...]

   ## Critical Issues (Must Fix): {count}

   1. [SECTION] Description
      - Location: {section name or line number}
      - Fix: {how to fix}

   ## Should-Fix Issues (Recommended): {count}

   1. [SECTION] Description
      - Recommendation: {how to improve}

   ## Anti-Hallucination Findings: {count}

   1. Claim "{detail}" not verified in {source}
      - Fix: Remove or source from architecture docs

   ## Recommendation

   {GO/NO-GO} - {rationale}

   {If NO-GO}: Fix {count} critical issues before handing to James.
   {If GO}: Proceed to implementation. Address {count} should-fix issues during development.

   ## Next Steps

   {If GO}:
   - Hand to James: @james *implement {story-id}
   - Monitor for should-fix issues during implementation

   {If NO-GO}:
   1. Fix critical issues listed above
   2. Re-validate: @validate-story {story-file}
   3. Proceed once validation passes
   ```

**Outputs:**
- `validation_report` - Full markdown report
- `validation_passed` - Boolean GO/NO-GO
- `readiness_score` - Number 1-10
- `confidence_level` - High/Medium/Low
- `critical_issues[]`, `should_fix_issues[]`, `nice_to_have[]`

**See:** `references/templates.md` for full report template

---

## Execution Complete

Skill complete when:

- ✅ All 10 validation steps executed
- ✅ Issues categorized (critical/should-fix/nice-to-have)
- ✅ Readiness score calculated
- ✅ GO/NO-GO decision made
- ✅ Validation report generated
- ✅ Telemetry emitted

## Integration with Workflow

**Story Creation → Validation → Implementation Flow:**

```bash
# Step 1: Create story
@create-story epic-001 story-003 "User Authentication"

# Step 2: Validate story
@validate-story .claude/stories/epic-001/story-003.md

# If GO:
@james *implement story-003

# If NO-GO:
# Fix critical issues, re-validate
@validate-story .claude/stories/epic-001/story-003.md
```

**Who Invokes:**
- Product Owner (before accepting story)
- Scrum Master (during sprint planning)
- Story creator (self-validation)
- James (auto-validate before implementation - optional)

## Best Practices

1. **Always validate before implementation** - Catch issues early
2. **Fix critical issues first** - Don't proceed with NO-GO stories
3. **Address should-fix during implementation** - Don't block on minor issues
4. **Re-validate after fixes** - Ensure issues resolved
5. **Track anti-hallucination patterns** - Learn common mistakes
6. **Use quick mode for drafts** - Full mode for final validation

## When to Escalate

**Escalate to user when:**
- Multiple anti-hallucination findings (>5)
- Architecture mismatch (story conflicts with architecture)
- Unclear requirements (story too vague to validate)
- Missing epic context (epic file not found)
- Template version mismatch (story uses old template)

## References

- `references/templates.md` - Validation report format, story template schema
- `references/validation-checklist.md` - Detailed checklist for all 10 steps
- `references/examples.md` - GO and NO-GO validation examples

---

*Part of BMAD Enhanced Planning Suite - Ensures quality stories before implementation*
