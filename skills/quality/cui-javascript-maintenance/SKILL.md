---
name: cui-javascript-maintenance
description: Standards for identifying, prioritizing, and verifying JavaScript code maintenance and refactoring work
allowed-tools: [Read, Grep, Glob]
---

# CUI JavaScript Maintenance Skill

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below based on the task context.

Standards for systematic JavaScript code maintenance including violation detection, prioritization frameworks, and compliance verification.

## Purpose

This skill provides comprehensive standards for:
- **Detecting** when code needs refactoring (trigger criteria)
- **Prioritizing** maintenance work (impact-based framework)
- **Verifying** standards compliance (comprehensive checklist)
- **Improving** test quality (test standards and patterns)

## When to Use This Skill

Activate this skill when:

**Planning Maintenance Work:**
- Conducting code quality audits
- Planning refactoring sprints
- Identifying technical debt
- Analyzing codebases for violations

**During Refactoring:**
- Need trigger criteria for when to refactor
- Need prioritization guidance
- Verifying standards compliance after changes

**Code Reviews:**
- Assessing code quality systematically
- Identifying improvement opportunities
- Validating maintenance work completeness

**Test Quality Improvement:**
- Identifying test anti-patterns
- Improving test coverage
- Refactoring test code

## Workflow

### Step 1: Load Core Maintenance Standards

**Load all four standards files** (always loaded together):

```
Read: standards/refactoring-triggers.md
Read: standards/maintenance-prioritization.md
Read: standards/compliance-checklist.md
Read: standards/test-quality-standards.md
```

These standards work together as a complete maintenance framework:
1. **Triggers** - Identify WHAT needs fixing (detection criteria)
2. **Prioritization** - Decide WHEN to fix it (impact framework)
3. **Checklist** - Verify fixes are COMPLETE (compliance verification)
4. **Test Quality** - Ensure tests are EFFECTIVE (test standards)

### Step 2: Apply Standards Based on Task

**For Code Analysis Tasks:**

1. Use refactoring-triggers.md to scan for violations:
   - Vanilla JavaScript enforcement opportunities
   - Test/mock code in production files
   - Modularization issues
   - Package.json problems
   - JSDoc gaps

2. Document all findings with locations and descriptions

**For Test Analysis Tasks:**

1. Use test-quality-standards.md to identify issues:
   - Common test anti-patterns
   - Framework compliance violations
   - Mock management problems
   - Coverage gaps
   - Async handling issues

2. Document test quality findings

**For Prioritization Tasks:**

1. Use maintenance-prioritization.md to categorize findings:
   - HIGH: Critical violations (security, bugs, fundamental design)
   - MEDIUM: Maintainability issues (code quality, modernization)
   - LOW: Style and speculative optimizations

2. Consider contextual factors:
   - Impact scope
   - Technical debt interest
   - Team context
   - Risk assessment

3. Create prioritized work list

**For Verification Tasks:**

1. Use compliance-checklist.md to verify fixes:
   - Work through each checklist section
   - Mark compliant/non-compliant items
   - Address all non-compliant findings
   - Re-verify after fixes
   - Document intentional deviations

2. Execute build verification:
   - Build: `npm run build`
   - Tests: `npm test`
   - Coverage: `npm run test:coverage`
   - Lint: `npm run lint`
   - Format: `npm run format:check`

### Step 3: Load Implementation Standards (Optional)

When implementing fixes, load relevant implementation skills:

**For code implementation:**
```
Skill: pm-dev-frontend:cui-javascript
```
Provides actual implementation patterns for:
- Core patterns and modern JavaScript
- Vanilla JavaScript alternatives
- ES modules and modern features

**For linting work:**
```
Skill: pm-dev-frontend:cui-javascript-linting
```
Provides ESLint configuration and rules.

**For documentation work:**
```
Skill: pm-dev-frontend:cui-jsdoc
```
Provides JSDoc standards and patterns.

**For testing work:**
```
Skill: pm-dev-frontend:cui-javascript-unit-testing
```
Provides Jest testing standards and patterns.

**For E2E testing:**
```
Skill: pm-dev-frontend:cui-cypress
```
Provides Cypress E2E testing standards.

### Step 4: Report Findings

Provide structured output:

**For Analysis:**
```
Violations Found:
- HIGH Priority: [count] issues
  - [Category]: [specific violations]
- MEDIUM Priority: [count] issues
  - [Category]: [specific violations]
- LOW Priority: [count] issues
  - [Category]: [specific violations]

Recommended Actions:
1. Address HIGH priority items first
2. [Specific recommendations]
```

**For Verification:**
```
Compliance Verification Results:
✅ Vanilla JavaScript: Compliant
✅ Test Code Separation: Compliant
⚠️ Modularization: 3 files over 400 lines
⚠️ Package.json: 5 outdated dependencies
✅ JSDoc Coverage: Compliant
...

Next Steps:
- Fix identified non-compliant items
- Re-run verification
```

## Common Patterns and Examples

### Pattern 1: Code Quality Audit

```markdown
## Step 1: Load Maintenance Standards
Skill: cui-javascript-maintenance

## Step 2: Analyze Codebase
Use Grep/Glob to scan for violations based on trigger criteria:
- Search for jQuery usage: $ function calls
- Search for test imports in production files
- Check for missing package.json scripts
- Identify files > 400 lines

## Step 3: Categorize and Prioritize
Apply prioritization framework:
- Security issues → HIGH
- Test code in production → HIGH
- Large files → MEDIUM
- Missing scripts → MEDIUM

## Step 4: Create Action Plan
Generate prioritized list of fixes needed.
```

### Pattern 2: Refactoring Verification

```markdown
## Step 1: Load Maintenance Standards
Skill: cui-javascript-maintenance

## Step 2: Apply Compliance Checklist
Work through checklist for modified files:
- Vanilla JavaScript ✅
- Test Code Separation ✅
- Modularization ⚠️ (2 files still large)
- Package.json ✅
- JSDoc Coverage ✅

## Step 3: Fix Non-Compliant Items
Split large files to comply with standards.

## Step 4: Re-Verify
Run through checklist again and verify build passes.
```

### Pattern 3: File-by-File Maintenance

```markdown
## Step 1: Load Maintenance Standards
Skill: cui-javascript-maintenance

## Step 2: For Each File
1. Apply trigger criteria to identify violations
2. Prioritize using framework
3. Implement fixes using cui-javascript
4. Verify using compliance checklist
5. Commit file changes

## Step 3: Final Verification
Verify all files pass build and tests.
```

### Pattern 4: Test Quality Improvement

```markdown
## Step 1: Load Maintenance Standards
Skill: cui-javascript-maintenance

## Step 2: Analyze Test Files
Use test-quality-standards.md to identify:
- Overly complex setup
- Missing async handling
- Hardcoded test data
- DOM cleanup issues

## Step 3: Prioritize Improvements
Focus on business logic tests first.

## Step 4: Apply Test Patterns
Use test-quality-standards.md patterns to refactor.

## Step 5: Verify Coverage
Ensure coverage maintained or improved.
```

## Integration with Commands

This skill is designed to be used by:

**`/js-refactor-code` command:**
- Loads this skill for detection, prioritization, and verification
- Orchestrates systematic refactoring workflow
- Uses trigger criteria to identify issues
- Uses prioritization to order work
- Uses checklist to verify completeness

**`/js-maintain-tests` command:**
- Loads this skill for test quality improvement
- Uses test-quality-standards.md for detection
- Uses prioritization for test work ordering
- Ensures no production code changes

**Other maintenance commands:**
- Any command performing code quality work
- Automated refactoring commands
- Code review automation

## Relationship with Other Skills

### Complementary Skills

**cui-javascript** - Implementation standards:
- This skill identifies WHAT needs fixing
- cui-javascript provides HOW to implement fixes

**cui-jsdoc** - Documentation standards:
- This skill detects documentation gaps
- cui-jsdoc provides documentation patterns

**cui-javascript-unit-testing** - Testing standards:
- This skill identifies testing needs
- cui-javascript-unit-testing provides testing patterns

**cui-javascript-linting** - Linting standards:
- This skill detects linting violations
- cui-javascript-linting provides ESLint configuration

**cui-cypress** - E2E testing standards:
- This skill identifies E2E test quality issues
- cui-cypress provides E2E testing patterns

### Clear Separation of Concerns

**This skill (cui-javascript-maintenance):**
- ✅ Detection criteria (WHEN to refactor)
- ✅ Prioritization framework (WHAT order)
- ✅ Verification checklist (HOW to verify)
- ✅ Test quality standards (HOW to test)
- ❌ Implementation patterns (see cui-javascript)
- ❌ Workflow orchestration (see /js-refactor-code command)

**Implementation skills (cui-javascript, etc.):**
- ✅ Implementation patterns (HOW to implement)
- ✅ Code examples and templates
- ✅ Best practices for writing code
- ❌ Detection criteria
- ❌ Prioritization decisions

## Standards Organization

```
standards/
├── refactoring-triggers.md          # Detection criteria
├── maintenance-prioritization.md    # Priority framework
├── compliance-checklist.md          # Verification checklist
└── test-quality-standards.md        # Test quality standards
```

**Design principles:**
- Self-contained standards (no external references except URLs)
- Markdown format for compatibility
- Practical examples included
- Clear decision guidance
- Agent-friendly structure

## Quality Verification

Before completing maintenance work:

1. [ ] All trigger criteria have been checked
2. [ ] Violations prioritized using framework
3. [ ] High priority items addressed
4. [ ] Compliance checklist completed
5. [ ] Build verification passed
6. [ ] Tests passing with adequate coverage
7. [ ] Lint and format checks passing
8. [ ] Deviations documented with rationale

## Example Usage

### In a Command

```markdown
---
name: my-maintenance-command
---

## Step 1: Load Maintenance Standards

```
Skill: cui-javascript-maintenance
```

This loads refactoring triggers, prioritization framework, compliance checklist, and test quality standards.

## Step 2: Analyze Code

Apply trigger criteria from refactoring-triggers.md to identify violations.

## Step 3: Prioritize Work

Use maintenance-prioritization.md to order fixes by impact.

## Step 4: Implement Fixes

For implementation patterns, load cui-javascript or other implementation skills.

## Step 5: Verify Compliance

Use compliance-checklist.md to verify all standards met.
```

### In an Agent

```markdown
## Maintenance Analysis Agent

### Step 1: Load Standards
```
Read: standards/refactoring-triggers.md
Read: standards/maintenance-prioritization.md
```

### Step 2: Scan Codebase
Apply trigger criteria to identify all violations.

### Step 3: Apply Prioritization
Use prioritization framework to categorize findings.

### Step 4: Report Results
Return structured analysis with prioritized action items.
```

## Error Handling

If issues arise during maintenance:

1. **Build failures**: Use npm-builder agent to diagnose and fix
2. **Test failures**: Review test output and fix broken tests
3. **Coverage regressions**: Add tests for uncovered code paths
4. **Lint issues**: Run `npm run lint:fix` for auto-fixable issues
5. **Ambiguous violations**: Ask user for guidance on priority

## References

**Internal Standards:**
- standards/refactoring-triggers.md - Detection criteria
- standards/maintenance-prioritization.md - Priority framework
- standards/compliance-checklist.md - Verification checklist
- standards/test-quality-standards.md - Test quality standards

**Related Skills:**
- cui-javascript - Core implementation patterns
- cui-jsdoc - Documentation standards
- cui-javascript-unit-testing - Testing standards
- cui-javascript-linting - Linting standards
- cui-cypress - E2E testing standards

**Related Commands:**
- /js-refactor-code - Systematic refactoring workflow
- /js-maintain-tests - Test quality improvement workflow
- /javascript-coverage-report - Coverage analysis
