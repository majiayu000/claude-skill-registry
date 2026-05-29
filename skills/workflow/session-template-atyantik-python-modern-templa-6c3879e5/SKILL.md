---
name: session-template
description: Apply task-specific templates to AI session plans using ai-update-plan. Use when starting a new task to load appropriate plan structure (feature, bugfix, refactor, documentation, security).
---

# Session Template Applier

## ⚠️ MANDATORY: Read Project Documentation First

**BEFORE applying session templates, you MUST read and understand the following project documentation:**

### Core Project Documentation

1. **README.md** - Project overview, features, and getting started
2. **AI_DOCS/project-context.md** - Tech stack, architecture, development workflow
3. **AI_DOCS/code-conventions.md** - Code style, formatting, best practices
4. **AI_DOCS/tdd-workflow.md** - TDD process, testing standards, coverage requirements

### Session Context (if available)

5. **.ai-context/ACTIVE_TASKS.md** - Current tasks and priorities
6. **.ai-context/CONVENTIONS.md** - Project-specific conventions
7. **.ai-context/RECENT_DECISIONS.md** - Recent architectural decisions
8. **.ai-context/LAST_SESSION_SUMMARY.md** - Previous session summary

### Additional AI Documentation

9. **AI_DOCS/ai-tools.md** - Session management workflow (CRITICAL for this skill)
10. **AI_DOCS/ai-skills.md** - Other specialized skills/agents available

### Why This Matters

- **Workflow Integration**: Understand how ai-update-plan fits into session management
- **Template Selection**: Choose appropriate template based on project patterns
- **Customization**: Adapt templates to match project-specific requirements
- **Task Context**: Consider active tasks and recent decisions when planning

**After reading these files, proceed with your template application task below.**

---

## Overview

Automatically apply task-specific planning templates to AI sessions, customizing generic steps with task-specific details.

## When to Use

- Starting a new AI session with `ai-start-task`
- Need structured plan for common task types
- Want to ensure all important steps are included
- Standardizing workflow across team
- Complex tasks needing comprehensive planning

## Available Templates

### 1. Feature Development (`feature`)
For adding new functionality

### 2. Bug Fix (`bugfix`)
For fixing existing issues

### 3. Refactoring (`refactor`)
For code improvement without behavior changes

### 4. Documentation (`documentation`)
For doc updates and improvements

### 5. Security Fix (`security`)
For security vulnerabilities and hardening

## Usage Examples

### Apply Template at Session Start

```bash
# Start session with feature template
apply feature development template for "Add OAuth2 authentication"
```

**Output:** Creates session with:
- Research & design phase
- TDD test-writing phase
- Implementation phase
- Security review phase
- Documentation phase

### Apply Template to Existing Session

```bash
# Mid-session, realize you need structured plan
apply refactoring template for current session
```

### Custom Template Selection

```bash
# Let skill analyze task and choose template
suggest template for "Fix memory leak in data processor"
# → Skill suggests: "bugfix" template
```

## Template Structures

### Feature Template

**File:** `templates/feature.md`

```markdown
### Phase 1: Research & Design
- [ ] Review related code in the codebase
- [ ] Identify integration points
- [ ] Design data models and interfaces
- [ ] Document API contracts
- [ ] Consider edge cases and error scenarios

### Phase 2: Write Tests (TDD)
- [ ] Write tests for happy path scenarios
- [ ] Write tests for edge cases
- [ ] Write tests for error handling
- [ ] Write integration tests
- [ ] Ensure tests fail initially (red phase)

### Phase 3: Implementation
- [ ] Implement core functionality
- [ ] Add error handling
- [ ] Add input validation
- [ ] Add logging
- [ ] Run tests - should pass (green phase)

### Phase 4: Refactoring
- [ ] Remove duplication (DRY)
- [ ] Simplify complex logic
- [ ] Improve naming
- [ ] Add type hints where missing
- [ ] Keep tests passing

### Phase 5: Quality Check
- [ ] Run make check (format, lint, test, security)
- [ ] Fix all quality issues
- [ ] Verify coverage ≥ 80%
- [ ] Review with tdd-reviewer agent
- [ ] Apply quality-fixer for auto-fixable issues

### Phase 6: Documentation
- [ ] Update README if user-facing changes
- [ ] Add/update docstrings
- [ ] Update API documentation
- [ ] Add usage examples
- [ ] Document configuration changes

### Phase 7: Final Review
- [ ] Review all changes with git diff
- [ ] Test manually in development
- [ ] Verify all edge cases work
- [ ] Check performance implications
- [ ] Ready for PR/commit
```

### Bugfix Template

**File:** `templates/bugfix.md`

```markdown
### Phase 1: Reproduction
- [ ] Reproduce the bug reliably
- [ ] Document steps to reproduce
- [ ] Identify affected components
- [ ] Check if regression (previously working)
- [ ] Review related issues

### Phase 2: Root Cause Analysis
- [ ] Add debug logging
- [ ] Trace execution flow
- [ ] Identify exact failure point
- [ ] Understand why it fails
- [ ] Document root cause

### Phase 3: Write Reproduction Test (TDD)
- [ ] Write test that reproduces the bug
- [ ] Verify test fails (confirms bug exists)
- [ ] Test should be specific to the bug
- [ ] Include edge cases related to bug
- [ ] Document expected vs actual behavior

### Phase 4: Fix Implementation
- [ ] Implement minimal fix for root cause
- [ ] Avoid over-engineering the fix
- [ ] Add defensive checks if needed
- [ ] Add logging for future debugging
- [ ] Verify test now passes

### Phase 5: Regression Prevention
- [ ] Add tests for related scenarios
- [ ] Check if bug exists elsewhere
- [ ] Add validation to prevent recurrence
- [ ] Update error messages if applicable
- [ ] Document why bug occurred

### Phase 6: Quality & Testing
- [ ] Run full test suite (no regressions)
- [ ] Run make check
- [ ] Verify coverage maintained/improved
- [ ] Test manually with original report steps
- [ ] Check performance not degraded

### Phase 7: Documentation
- [ ] Update changelog
- [ ] Document fix in commit message
- [ ] Add code comments explaining fix
- [ ] Update docs if behavior changed
- [ ] Reference issue number if applicable
```

### Refactoring Template

**File:** `templates/refactor.md`

```markdown
### Phase 1: Establish Safety Net
- [ ] Ensure tests exist for code being refactored
- [ ] Run tests - all must pass (baseline)
- [ ] Run make check - must pass
- [ ] Commit current state (safety checkpoint)
- [ ] Document current behavior

### Phase 2: Identify Improvements
- [ ] Identify code smells (duplication, complexity)
- [ ] Find violations of SOLID principles
- [ ] Look for unclear naming
- [ ] Identify missing abstractions
- [ ] List specific improvements needed

### Phase 3: Plan Refactoring Steps
- [ ] Break into small, safe steps
- [ ] Prioritize by risk/impact
- [ ] Identify dependencies between steps
- [ ] Plan to keep tests green throughout
- [ ] Consider breaking into multiple commits

### Phase 4: Refactor Incrementally
- [ ] Make one small change at a time
- [ ] Run tests after each change
- [ ] Keep tests passing (always green)
- [ ] Commit after each successful step
- [ ] If tests fail, revert and adjust approach

### Phase 5: Improve Design
- [ ] Extract methods/functions
- [ ] Remove duplication (DRY)
- [ ] Improve naming (clarity)
- [ ] Simplify complex conditionals
- [ ] Add type hints for clarity

### Phase 6: Quality Verification
- [ ] Run make check (must pass)
- [ ] Verify no behavior changes
- [ ] Check performance not degraded
- [ ] Review with tdd-reviewer agent
- [ ] Ensure coverage maintained

### Phase 7: Documentation
- [ ] Update docstrings for changed interfaces
- [ ] Add comments for complex logic
- [ ] Document why refactoring was needed
- [ ] Update architecture docs if applicable
- [ ] Record design decisions
```

### Documentation Template

**File:** `templates/documentation.md`

```markdown
### Phase 1: Content Audit
- [ ] Review existing documentation
- [ ] Identify outdated content
- [ ] Find missing documentation
- [ ] Check for broken links
- [ ] Review user feedback/questions

### Phase 2: Content Planning
- [ ] Define documentation scope
- [ ] Identify target audience
- [ ] Plan document structure
- [ ] Prioritize sections to update
- [ ] Gather technical details needed

### Phase 3: Write/Update Content
- [ ] Write clear, concise content
- [ ] Add code examples
- [ ] Include usage scenarios
- [ ] Add diagrams/visuals if helpful
- [ ] Follow documentation style guide

### Phase 4: Code Examples
- [ ] Ensure all code examples work
- [ ] Test code examples actually run
- [ ] Add comments to examples
- [ ] Show both basic and advanced usage
- [ ] Include error handling examples

### Phase 5: Review & Polish
- [ ] Check spelling and grammar
- [ ] Verify technical accuracy
- [ ] Ensure consistent terminology
- [ ] Check formatting and layout
- [ ] Validate all links work

### Phase 6: Sync with Code
- [ ] Update docstrings in code
- [ ] Ensure API docs match implementation
- [ ] Update type hints documentation
- [ ] Sync version numbers
- [ ] Update changelog

### Phase 7: Validation
- [ ] Have someone else review
- [ ] Test following docs from scratch
- [ ] Verify examples in clean environment
- [ ] Check docs render correctly
- [ ] Update AI_DOCS if relevant
```

### Security Fix Template

**File:** `templates/security.md`

```markdown
### Phase 1: Vulnerability Assessment
- [ ] Understand the security issue
- [ ] Assess severity and impact
- [ ] Identify affected versions
- [ ] Check if actively exploited
- [ ] Review security advisories

### Phase 2: Impact Analysis
- [ ] Identify all affected code paths
- [ ] Determine data exposure risk
- [ ] Check for similar issues elsewhere
- [ ] Assess authentication/authorization impact
- [ ] Review compliance implications

### Phase 3: Security Test (TDD)
- [ ] Write test demonstrating vulnerability
- [ ] Test should fail (exploits vulnerability)
- [ ] Test common attack vectors
- [ ] Test boundary conditions
- [ ] Document attack scenarios

### Phase 4: Implement Fix
- [ ] Apply principle of least privilege
- [ ] Use secure coding practices
- [ ] Validate all inputs
- [ ] Sanitize outputs
- [ ] Add rate limiting if applicable

### Phase 5: Security Hardening
- [ ] Add additional security checks
- [ ] Implement defense in depth
- [ ] Add security logging
- [ ] Update authentication/authorization
- [ ] Review encryption/hashing

### Phase 6: Security Testing
- [ ] Run security scan (Bandit)
- [ ] Test with malicious inputs
- [ ] Verify authentication works
- [ ] Test authorization boundaries
- [ ] Check for information disclosure

### Phase 7: Security Review
- [ ] Review with security-focused perspective
- [ ] Check OWASP Top 10 compliance
- [ ] Verify no new vulnerabilities introduced
- [ ] Test error messages don't leak info
- [ ] Document security measures

### Phase 8: Quality & Documentation
- [ ] Run make check
- [ ] Update security documentation
- [ ] Add security comments in code
- [ ] Document security assumptions
- [ ] Plan coordinated disclosure if needed
```

## How It Works

### Step 1: Analyze Task Description

Extract keywords to determine task type:

**Feature indicators:**
- "add", "implement", "create", "build", "new"
- "feature", "functionality", "capability"

**Bugfix indicators:**
- "fix", "bug", "issue", "error", "broken"
- "crash", "fail", "regression"

**Refactor indicators:**
- "refactor", "improve", "clean up", "reorganize"
- "simplify", "optimize", "restructure"

**Documentation indicators:**
- "document", "docs", "README", "guide"
- "explain", "describe", "instructions"

**Security indicators:**
- "security", "vulnerability", "exploit", "CVE"
- "authentication", "authorization", "XSS", "SQL injection"

### Step 2: Load Template

Read appropriate template from `templates/` directory:

```bash
# Load template file
template_file=".claude/skills/session-template/templates/${template_type}.md"
cat "$template_file"
```

### Step 3: Customize Template

Customize generic steps with task-specific details:

```markdown
# Generic template:
- [ ] Review related code in the codebase

# Customized for "Add OAuth2 authentication":
- [ ] Review related authentication code for OAuth2 integration
```

### Step 4: Apply to Session

Use `ai-update-plan` to add items to the current session:

```bash
# Add each phase item to plan
uv run ai-update-plan --add "Review related authentication code" --phase "Phase 1"
uv run ai-update-plan --add "Identify OAuth2 provider integration" --phase "Phase 1"
# ... etc
```

### Step 5: Display Plan

Show the complete plan with progress tracking:

```bash
uv run ai-update-plan --show
```

## Integration with ai-update-plan

This skill leverages `ai-update-plan` features:

### Add Items by Phase

```bash
# Add to specific phase
uv run ai-update-plan --add "Write OAuth2 tests" --phase "Phase 2"
```

### Customize After Application

```bash
# Rename generic item to specific
uv run ai-update-plan --rename "Review related code" \
  --to "Review existing OAuth implementation"

# Remove irrelevant items
uv run ai-update-plan --remove "Add diagrams/visuals"
```

### Track Progress

```bash
# Check off completed items
uv run ai-update-plan "Review related authentication code"

# Show progress
uv run ai-update-plan --show
```

## Customization Guide

### Creating Custom Templates

1. Create new template file in `templates/`
2. Follow standard phase structure
3. Use checkbox format `- [ ]`
4. Group related items in phases
5. Include all quality gates

**Example custom template:**

```markdown
### Phase 1: API Design
- [ ] Define API endpoints
- [ ] Document request/response formats
- [ ] Choose authentication method
- [ ] Plan rate limiting strategy

### Phase 2: Implementation (TDD)
- [ ] Write API endpoint tests
- [ ] Implement endpoints
- [ ] Add validation middleware
- [ ] Add error handling

### Phase 3: Integration
- [ ] Test with client application
- [ ] Update API documentation
- [ ] Add usage examples
- [ ] Deploy to staging
```

### Template Variables

Templates can include placeholders:

```markdown
- [ ] Review {module_name} module
- [ ] Test {function_name} with various inputs
- [ ] Update {doc_file} documentation
```

Skill will replace these based on task description analysis.

## Output Format

After applying template:

```markdown
## Session Template Applied: Feature Development

**Template:** feature.md
**Task:** Add OAuth2 authentication
**Items Added:** 28

### Plan Structure:
- Phase 1: Research & Design (5 items)
- Phase 2: Write Tests (5 items)
- Phase 3: Implementation (5 items)
- Phase 4: Refactoring (5 items)
- Phase 5: Quality Check (4 items)
- Phase 6: Documentation (3 items)
- Phase 7: Final Review (5 items)

### Customizations Applied:
- Replaced "Review related code" → "Review existing authentication for OAuth2"
- Added "Research OAuth2 providers (Google, GitHub, Auth0)"
- Added "Test token refresh mechanism"
- Removed generic placeholder items

### View Your Plan:
```bash
uv run ai-update-plan --show
```

### Start Working:
Begin with Phase 1, checking off items as you complete them:
```bash
uv run ai-update-plan "Review existing authentication for OAuth2"
```

### Customize Plan:
Add task-specific items:
```bash
uv run ai-update-plan --add "Test SSO integration" --phase "Phase 2"
```

Remove irrelevant items:
```bash
uv run ai-update-plan --remove "Generic item"
```
```

## Best Practices

1. **Apply template early** - Start session with template for comprehensive planning
2. **Customize immediately** - Adjust generic items to be specific to your task
3. **Remove irrelevant steps** - Don't keep items that don't apply
4. **Add missing steps** - Template is starting point, not gospel
5. **Track progress** - Check off items as you complete them
6. **Update as you learn** - Adjust plan based on discoveries

## Template Selection Guide

**Use "feature" when:**
- Adding new user-facing functionality
- Building new API endpoints
- Creating new modules/components
- Adding new configuration options

**Use "bugfix" when:**
- Fixing reported issues
- Resolving test failures
- Addressing regressions
- Patching security vulnerabilities (minor)

**Use "refactor" when:**
- Improving code structure
- Reducing complexity
- Removing duplication
- Modernizing code patterns

**Use "documentation" when:**
- Updating README
- Writing API docs
- Creating usage guides
- Improving code comments

**Use "security" when:**
- Fixing CVEs
- Hardening authentication
- Addressing OWASP issues
- Implementing security features

## Advanced Features

### Multi-Template Application

For complex tasks, combine templates:

```bash
# Security fix that needs refactoring
apply security template
# Then add refactoring items:
uv run ai-update-plan --add "Refactor auth module for clarity" --phase "Phase 9"
```

### Template Inheritance

Create specialized templates that extend base templates:

```markdown
<!-- templates/api-feature.md -->
<!-- Extends feature.md with API-specific items -->

### Phase 1: API Research & Design
- [ ] Review related API endpoints
- [ ] Define OpenAPI/Swagger spec
- [ ] Plan versioning strategy
- [ ] Design request/response schemas
- [ ] Plan rate limiting

[... rest of feature template ...]
```

### Conditional Sections

Templates can include conditional guidance:

```markdown
### Phase X: Database Changes (if applicable)
- [ ] Design schema changes
- [ ] Write migration scripts
- [ ] Test migration rollback
- [ ] Update ORM models

*Skip this phase if no database changes needed*
```

## Integration with Other Tools

### With ai-start-task

```bash
# Start session and apply template atomically
uv run ai-start-task "Add OAuth2 authentication" --template=feature
```

### With TDD Reviewer

Template includes TDD-specific phases:
- Phase 2: Write Tests (TDD)
- Phase 5: Quality Check (includes tdd-reviewer)

### With Quality Enforcer

Template includes quality gates:
- Phase 5: Quality Check (make check)
- Phase 7: Final Review (quality verification)

## Remember

Templates are **starting points**, not rigid requirements:
- Customize for your specific task
- Add missing items unique to your situation
- Remove items that don't apply
- Adjust phases as you learn more

The goal is **structured flexibility** - enough structure to ensure quality, enough flexibility to adapt to reality.
