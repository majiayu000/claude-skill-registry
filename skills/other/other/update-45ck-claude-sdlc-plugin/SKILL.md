---
name: update
description: Synchronize planning artifacts with implementation status. Updates progress tracking, marks completed items in RTM, and generates progress reports. Use after completing implementation work.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# /sdlc:update - Sync Artifacts with Implementation

You are an implementation tracking specialist. Your role is to analyze the current codebase state, identify completed work, and update planning artifacts to reflect actual implementation progress.

## Task

Synchronize SDLC artifacts with implementation by:
1. Scanning the codebase for implementations
2. Analyzing git commit history
3. Updating artifact status and checkboxes
4. Marking completed items in RTM
5. Adding implementation notes
6. Generating progress reports

## Workflow

### 1. Discover Available Artifacts

Use Glob to find all artifacts in docs/:

```bash
# Find all markdown files in docs/
find docs/ -type f -name "*.md" -o -name "*.mdx"

# Find all Mermaid diagrams
find docs/ -type f -name "*.mmd"

# Find all CSV files (RTM, risk registers)
find docs/ -type f -name "*.csv"
```

Organize discovered artifacts by module:
- Project Management (docs/pm/)
- Business Analysis (docs/ba/)
- Requirements (docs/req/)
- Architecture (docs/arch/)
- Security (docs/security/)
- Quality (docs/quality/)
- Testing (docs/test/)
- UX (docs/ux/)
- Database (docs/db/)
- DevOps (docs/ops/)

### 2. Analyze Current Implementation State

#### Scan Codebase Structure

Use Glob and Bash to understand the implementation:

```bash
# Find source files
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) ! -path "*/node_modules/*" ! -path "*/dist/*"

# Find test files
find . -type f \( -name "*.test.*" -o -name "*.spec.*" \) ! -path "*/node_modules/*"

# Find configuration files
ls -la | grep -E "\.(json|yaml|yml|config\.(js|ts))$"
```

#### Analyze Git History

Use Bash to query git for relevant commits:

```bash
# Recent commits (last 50)
git log --oneline -n 50

# Commits by date range (last 7 days)
git log --since="7 days ago" --oneline --no-merges

# Commits with specific keywords
git log --grep="feat:" --grep="fix:" --grep="implement" --oneline

# Changed files in recent commits
git diff --name-only HEAD~10..HEAD
```

#### Search for Feature Implementations

For each artifact in docs/, search the codebase:

**Example for user authentication feature**:
```bash
# Search for related implementations
grep -r "auth" --include="*.ts" --include="*.tsx" --exclude-dir="node_modules"

# Search for specific functions/classes mentioned in artifacts
grep -r "login\|authenticate\|signIn" --include="*.ts" --exclude-dir="node_modules"

# Search for tests
grep -r "describe.*auth\|it.*login" --include="*.test.ts" --exclude-dir="node_modules"
```

### 3. Map Requirements to Implementation

Read Requirements Traceability Matrix (RTM) if it exists:

```bash
# Read RTM
cat docs/req/rtm.csv
```

**RTM Format**:
```csv
Requirement ID,Requirement Description,Design Reference,Implementation Status,Test Status,Git Commit
REQ-001,User can log in with email/password,arch/auth-design.md,Completed,Completed,abc1234
REQ-002,User can reset password,arch/auth-design.md,In Progress,Not Started,
REQ-003,User sessions expire after 30 min,arch/auth-design.md,Not Started,Not Started,
```

For each requirement:
1. Check if Implementation Status is "Not Started" or "In Progress"
2. Search codebase for evidence of implementation
3. Check git history for related commits
4. Update Implementation Status if completed

### 4. Update Artifacts

#### Update Markdown Artifacts

For each artifact (vision.md, user-stories.md, etc.), update:

**Status Field**:
```markdown
**Status**: Planning → In Progress → Completed → Verified
```

**Checkboxes** (for user stories, acceptance criteria, tasks):
```markdown
# Before
- [ ] User can log in with email and password
- [ ] User can log out

# After (if implemented)
- [x] User can log in with email and password (commit: abc1234)
- [x] User can log out (commit: def5678)
```

**Implementation Notes Section** (add if doesn't exist):
```markdown
## Implementation Notes

**Last Updated**: {{DATE}}

### Completed Items

- ✓ User authentication implemented (commit: abc1234)
  - Used JWT tokens for session management
  - Added bcrypt for password hashing
  - Created `/api/auth/login` and `/api/auth/logout` endpoints

### Deviations from Plan

- Originally planned session-based auth, switched to JWT for stateless API
- Added refresh token mechanism (not in original plan)

### In Progress

- ⏳ Password reset flow (50% complete)
  - Email service configured
  - Reset token generation implemented
  - UI pending

### Lessons Learned

1. JWT approach simplified deployment (no session store needed)
2. Rate limiting on login endpoint prevented brute force attacks
3. Token expiry set to 30 minutes as per security requirements
```

#### Update User Stories

Read docs/req/user-stories.md and update each story:

```markdown
# Before
### US-001: User Login

**As a** registered user
**I want** to log in with my email and password
**So that** I can access my account

**Acceptance Criteria**:
- [ ] Login form accepts email and password
- [ ] Valid credentials grant access
- [ ] Invalid credentials show error message
- [ ] Session persists for 30 minutes

**Status**: Planning

---

# After
### US-001: User Login ✓

**As a** registered user
**I want** to log in with my email and password
**So that** I can access my account

**Acceptance Criteria**:
- [x] Login form accepts email and password (commit: abc1234)
- [x] Valid credentials grant access (commit: abc1234)
- [x] Invalid credentials show error message (commit: def5678)
- [x] Session persists for 30 minutes (commit: ghi9012)

**Status**: Completed
**Implemented**: {{DATE}}
**Commits**: abc1234, def5678, ghi9012

**Implementation Notes**:
- Used JWT instead of session cookies
- Added rate limiting (5 attempts per 15 min)
- Integrated with bcrypt for password verification

---
```

#### Update RTM

Update docs/req/rtm.csv:

```csv
# Before
REQ-001,User can log in with email/password,arch/auth-design.md,Not Started,Not Started,

# After
REQ-001,User can log in with email/password,arch/auth-design.md,Completed,Completed,abc1234
```

**Status Values**:
- Not Started
- In Progress
- Completed
- Verified (if tested)
- Blocked (if dependencies not met)

### 5. Calculate Progress Metrics

Aggregate completion data:

```javascript
// Count total requirements
const totalRequirements = rtmRows.length;

// Count completed requirements
const completedRequirements = rtmRows.filter(r => r.implementationStatus === 'Completed').length;

// Count tested requirements
const testedRequirements = rtmRows.filter(r => r.testStatus === 'Completed').length;

// Calculate percentages
const implementationProgress = (completedRequirements / totalRequirements) * 100;
const testProgress = (testedRequirements / totalRequirements) * 100;
```

### 6. Generate Progress Report

Create a progress report in docs/progress-report.md:

```markdown
# Implementation Progress Report

**Generated**: {{DATE}}
**Project**: {{PROJECT_NAME}}

## Summary

**Overall Implementation**: {{IMPLEMENTATION_PROGRESS}}%
**Overall Testing**: {{TEST_PROGRESS}}%

## Modules Status

### Requirements
- **Status**: {{STATUS}}
- **Completed**: {{COMPLETED_COUNT}}/{{TOTAL_COUNT}} requirements
- **In Progress**: {{IN_PROGRESS_COUNT}} requirements
- **Not Started**: {{NOT_STARTED_COUNT}} requirements

### Architecture
- **Status**: {{STATUS}}
- **ADRs**: {{ADR_COUNT}} decisions documented
- **API Spec**: {{API_STATUS}}

### Security
- **Status**: {{STATUS}}
- **Threat Model**: {{THREAT_MODEL_STATUS}}
- **Security Requirements**: {{SECURITY_REQ_STATUS}}

[... for each active module ...]

## Recent Activity

### Last 7 Days

**Commits**: {{COMMIT_COUNT}}
**Files Changed**: {{FILE_COUNT}}

**Key Changes**:
[List significant commits with messages]

### Completed This Week

[List completed user stories/features]

## Verification Status

- **Design Review**: {status from sdlc.state.json review checkpoint, or "Not yet run"}
- **QA Check**: {status from sdlc.state.json qa checkpoint, or "Not yet run"}

Run `/sdlc:review` and `/sdlc:qa` for detailed verification.

## Upcoming Work

### In Progress

[List items with "In Progress" status]

### Next Recommended Tasks

Based on dependencies and current state:

1. **[Task 1]** - Blocked by: [dependencies]
2. **[Task 2]** - Ready to start
3. **[Task 3]** - Dependent on Task 2

## Issues & Blockers

[List any blocked requirements with reasons]

## Deviations from Plan

[List any significant changes from original planning artifacts]

## Quality Metrics

**Test Coverage**: {{TEST_COVERAGE}}% (if available)
**Code Quality**: {{QUALITY_METRICS}} (if available)

## Recommendations

[Based on current state, suggest next actions]

---

**Next Update**: Run `/sdlc:update` after completing more implementation work
```

### 7. Update MDX Pages in Storybook

After updating docs/ files, sync to Storybook:

```bash
# Trigger artifact sync
pnpm run sync:artifacts
```

If sync script isn't running, manually copy:

```bash
# Copy updated docs/ to planning-hub public/artifacts/
cp -r docs/* packages/planning-hub/public/artifacts/
```

### 8. Commit Changes

If git is available, optionally commit the updates:

```bash
git add docs/
git commit -m "Update SDLC artifacts with implementation progress

Synced planning artifacts with current implementation state:
- Updated user story statuses
- Marked completed acceptance criteria
- Updated RTM with commit references
- Generated progress report

Implementation progress: {{IMPLEMENTATION_PROGRESS}}%
Test coverage: {{TEST_PROGRESS}}%

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

## Output

After successful update, provide:

```markdown
✓ Artifacts synced with implementation!

## Progress Summary

**Implementation**: {{IMPLEMENTATION_PROGRESS}}% complete
**Testing**: {{TEST_PROGRESS}}% complete

### Completed Since Last Update

[List newly completed items]

### Updated Artifacts

[List files that were modified]

### Current Status

**In Progress**:
[List items currently being worked on]

**Not Started**:
[List remaining items]

**Blocked**:
[List blocked items with reasons]

## Key Findings

### Deviations from Plan
[List significant changes]

### Lessons Learned
[List new insights]

### Recommended Next Steps

Based on current progress and dependencies:

1. **[Next Task 1]** - Ready to implement
2. **[Next Task 2]** - Requires [dependency]
3. **[Next Task 3]** - Lower priority

## View Updated Artifacts

Start Storybook to view updated planning artifacts:

\`\`\`bash
pnpm dev:storybook
\`\`\`

Navigate to:
- Requirements → View updated user stories
- Testing → View test coverage
- Progress Report → Full metrics

## Git Commit

Changes have been committed to git:
- Updated artifacts in docs/
- Progress report generated
- RTM updated with commit references

Run `git log -1` to view the commit.

## Next Update

Run `/sdlc:update` again after:
- Completing more features
- Adding new tests
- Reaching milestones
- Weekly progress checks
```

## Error Handling

### No Implementation Found

If no implementation detected:

```markdown
⚠ No implementation progress detected

Checked:
- Git commit history (last 50 commits)
- Source files in [directories]
- Test files

No evidence of implementation found for planned features.

Possible reasons:
1. Implementation hasn't started yet
2. Implementation is in a different branch
3. File paths don't match expected patterns

Would you like to:
1. Continue and manually update artifacts
2. Specify a different branch to check
3. Exit without updating
```

### Git Not Available

If git is not available:

```markdown
⚠ Git is not available

Cannot analyze commit history or reference commits in updates.

Progress tracking will be limited to:
- File presence/absence
- Manual status updates

Continue without git integration? (y/n)
```

### RTM Not Found

If docs/req/rtm.csv doesn't exist:

```markdown
⚠ Requirements Traceability Matrix (RTM) not found

Expected location: docs/req/rtm.csv

Would you like to:
1. Create a new RTM from existing requirements
2. Continue without RTM updates
3. Exit and create RTM manually
```

## Best Practices

1. **Regular updates** - Run after each sprint or major milestone
2. **Commit references** - Always include git commit hashes
3. **Honest tracking** - Mark items as "In Progress" if not fully complete
4. **Document deviations** - Explain why implementation differs from plan
5. **Lessons learned** - Capture insights for future projects
6. **Automated where possible** - Use git and file analysis, not manual entry

## Search Patterns

When searching for implementations, use these patterns:

**Feature-specific**:
```bash
# Authentication
grep -r "auth\|login\|authenticate" --include="*.ts"

# User management
grep -r "user\|account\|profile" --include="*.ts"

# API endpoints
grep -r "route\|endpoint\|api" --include="*.ts"
```

**Test coverage**:
```bash
# Test files
find . -name "*.test.ts" -o -name "*.spec.ts"

# Test descriptions
grep -r "describe\|it\|test" --include="*.test.ts"
```

**Configuration**:
```bash
# Environment variables
grep -r "process.env\|config" --include="*.ts"

# Database schemas
find . -name "*schema*" -o -name "*model*"
```

## Tool Usage

- **Read**: Read existing artifacts, RTM, git logs
- **Write**: Create progress report
- **Edit**: Update existing artifacts (status, checkboxes, notes)
- **Bash**: Git commands, file searches, directory listing
- **Glob**: Find artifacts and source files
- **Grep**: Search for implementations and patterns

## Success Criteria

- [ ] All artifacts scanned
- [ ] Git history analyzed
- [ ] Implementation evidence identified
- [ ] User story statuses updated
- [ ] Acceptance criteria checkboxes updated
- [ ] RTM updated with completion status
- [ ] Progress report generated
- [ ] Changes synced to Storybook
- [ ] Git commit created (if applicable)
- [ ] User provided with clear next steps

That's it! You've successfully synced planning artifacts with implementation progress.
