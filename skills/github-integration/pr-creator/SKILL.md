---
name: pr-creator
description: Create comprehensive pull requests with detailed descriptions, test plans,
  and proper git workflow. Use when finalizing features to ensure high-quality PRs.
allowed-tools: Read, Bash, Grep
---

# Pull Request Creator Skill

## Purpose

This skill provides systematic guidance for creating high-quality pull requests with comprehensive descriptions, proper commit messages, and complete test plans following conventional commits and project standards.

## When to Use

- After implementation, validation, documentation, and CHANGELOG updates
- Ready to create pull request for code review
- Need comprehensive PR description
- Following git workflow best practices
- Ensuring PR quality standards

## PR Creation Workflow

### 1. Pre-Flight Checks

**Objective**: Verify everything is ready for PR creation.

**Checklist**:
```bash
# 1. All changes committed
git status
# Should show: "nothing to commit, working tree clean"

# 2. All tests passing
pytest
# All tests should be green

# 3. Code quality checks passed
black src/ tests/ --check
mypy src/
# Should have no errors

# 4. Documentation updated
# Verify docs/ has implementation docs
ls docs/implementation/

# 5. CHANGELOG updated
# Verify CHANGELOG.md has new entry
head -50 CHANGELOG.md

# 6. Version numbers synced
grep -r "version.*=.*[0-9]" pyproject.toml src/__init__.py
# Should all show same version

# 7. No merge conflicts with main
git fetch origin main
git merge-base --is-ancestor origin/main HEAD
# Exit code 0 means no conflicts
```

**If any check fails**:
- Fix the issue before proceeding
- Re-run checks until all pass
- Don't create PR with failing checks

**Deliverable**: All pre-flight checks passed

---

### 2. Review Changes

**Objective**: Understand full scope of changes for PR description.

**Review commit history**:
```bash
# View all commits in feature branch
git log --oneline main..HEAD

# View detailed commit messages
git log main..HEAD

# View files changed
git diff --stat main..HEAD

# View actual changes
git diff main..HEAD
```

**Analyze changes**:
- What was implemented?
- What files were modified/added?
- Are there breaking changes?
- What tests were added?
- What documentation was updated?

**Review validation results**:
- Test coverage percentage
- Performance benchmark results
- Security scan results
- Code quality metrics

**Deliverable**: Complete understanding of changes

---

### 3. Create Comprehensive Commit

**Objective**: Create commit with full feature changes and proper message.

**Commit Message Format** (Conventional Commits):
```
<type>: <short summary> (#<issue>)

<detailed description>

<body paragraphs>

<footers>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Commit Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style/formatting
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Build, dependencies, configs

**Example Commit Message**:
```
feat: implement user authentication system (#123)

Implement comprehensive user authentication with JWT tokens,
OAuth providers, and session management. Includes password
reset flow, email verification, and role-based access control.

Implementation:
- JWT-based authentication with refresh tokens
- Support for email/password and OAuth (Google, GitHub)
- Session management with configurable timeout
- Password reset flow with email verification
- Role-based access control (RBAC) system

Security:
- Bcrypt password hashing (cost factor: 12)
- Rate limiting for login attempts (5 per minute)
- CSRF protection for all authenticated endpoints
- Input validation at all entry points
- Secure session storage with HttpOnly cookies

Performance:
- Redis caching for session data
- Database query optimization with proper indexing
- Response time < 200ms for auth endpoints
- Concurrent request handling with async/await

Testing:
- Unit test coverage: 92%
- Integration tests for all auth flows
- Security tests for XSS, CSRF, injection
- Performance tests verify <200ms response times
- Edge cases: invalid tokens, expired sessions, concurrent logins

Features:
- User registration with email verification
- Login with email/password or OAuth
- Password reset with secure token
- Session management with refresh tokens
- Role-based permissions system
- User profile management

Breaking Changes:
None - This is a new feature

Migration:
No migration needed - New feature, no existing data

Closes #123

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Create commit**:
```bash
# Stage all changes
git add .

# Commit with comprehensive message
git commit -m "$(cat <<'EOF'
feat: implement user authentication system (#123)

Implement comprehensive user authentication with JWT tokens,
OAuth providers, and session management.

Implementation: [details]
Security: [measures]
Performance: [optimizations]
Testing: [coverage and types]

Features:
- [feature 1]
- [feature 2]

Closes #123

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Deliverable**: Comprehensive commit created

---

### 4. Push to Remote

**Objective**: Push feature branch to remote repository.

**Push with upstream tracking**:
```bash
# Push to remote with -u flag to set upstream
git push -u origin feature/issue-123-user-auth

# Verify push succeeded
git status
# Should show: "Your branch is up to date with 'origin/feature/...'"
```

**Handle push errors**:

**Error: Remote branch exists**
```bash
# Fetch and check
git fetch origin
git status

# If behind, pull first
git pull origin feature/issue-123-user-auth

# Then push again
git push -u origin feature/issue-123-user-auth
```

**Error: Branch name doesn't start with 'claude/'**
```bash
# May need to follow project branch naming convention
# Check if project requires specific prefix
# Rename branch if needed:
git branch -m new-branch-name
git push -u origin new-branch-name
```

**Retry logic for network errors**:
```bash
# Retry up to 4 times with exponential backoff
# Try 1: git push (wait 2s if failed)
# Try 2: git push (wait 4s if failed)
# Try 3: git push (wait 8s if failed)
# Try 4: git push (wait 16s if failed)
```

**Deliverable**: Code pushed to remote branch

---

### 5. Generate PR Description

**Objective**: Create comprehensive PR description.

**PR Title Format**:
```
<type>: <brief description> (#<issue>)
```

**Examples**:
- `feat: implement user authentication system (#123)`
- `fix: resolve memory leak in cache manager (#124)`
- `docs: update API documentation for v2.0 (#125)`

**PR Description Template**:
```markdown
## Feature Summary

[2-3 sentence overview of what was implemented and why it matters]

## Implementation Details

**Architecture**: [Pattern used - e.g., service layer, repository pattern]

**Key Components**:
- **ComponentName**: [Purpose and responsibility]
- **AnotherComponent**: [Purpose and responsibility]

**Dependencies Added**:
- `package-name==version`: [Why it was added]

**Files Modified/Added**:
- `src/module/file.py`: [What changed]
- `tests/test_module.py`: [Tests added]
- `docs/guides/guide.md`: [Documentation]

## Security & Performance

### Security
- ✅ Input validation at all entry points
- ✅ Authentication/authorization implemented
- ✅ Output sanitization (XSS prevention)
- ✅ Parameterized queries (SQL injection prevention)
- ✅ Rate limiting configured
- ✅ Secrets managed securely (no hardcoded credentials)
- ✅ Security tests passing

**Security Measures**:
- [Specific measure 1]: [Details]
- [Specific measure 2]: [Details]

### Performance
- ✅ Performance targets met
- ✅ Caching strategy implemented
- ✅ Database queries optimized
- ✅ Async operations where appropriate
- ✅ Resource usage acceptable
- ✅ Performance tests passing

**Performance Metrics**:
- Response time: [actual vs target]
- Throughput: [requests per second]
- Resource usage: [CPU/memory]
- Database queries: [optimizations applied]

## Testing

### Coverage
- **Unit Tests**: [X]% coverage
- **Integration Tests**: [X endpoints/flows covered]
- **Security Tests**: [what's tested]
- **Performance Tests**: [benchmarks met]

### Test Types
- ✅ Unit tests for all business logic
- ✅ Integration tests for API endpoints
- ✅ Security tests for auth and validation
- ✅ Edge case and error handling tests
- ✅ Performance benchmarks

### Test Results
```bash
# All tests passing
pytest --cov=src --cov-report=term
Coverage: 92%
Tests: 156 passed, 0 failed
```

## Documentation

- ✅ Implementation docs: `docs/implementation/issue-123-user-auth.md`
- ✅ User guide: `docs/guides/authentication-guide.md`
- ✅ API documentation: `docs/api/auth-api.md`
- ✅ Architecture docs: `docs/architecture/auth-architecture.md`
- ✅ CHANGELOG updated with v[X.Y.Z] entry
- ✅ README updated (if applicable)

**Documentation Links**:
- [Implementation Details](docs/implementation/issue-123-user-auth.md)
- [User Guide](docs/guides/authentication-guide.md)
- [API Documentation](docs/api/auth-api.md)

## Breaking Changes

[If yes, list them with migration instructions]
[If no, state: "None"]

**Migration Required**:
[If yes, provide step-by-step migration guide]
[If no, state: "None required"]

## Configuration Changes

**New Environment Variables**:
```bash
AUTH_JWT_SECRET=your_secret_here
AUTH_SESSION_TIMEOUT=3600
AUTH_RATE_LIMIT=100
```

**Updated Configuration Files**:
- `.env.example`: Added AUTH_* variables
- `config.yaml`: Added auth section

## Validation Results

### Code Quality
- ✅ Black formatting: Passed
- ✅ mypy type checking: Passed
- ✅ flake8 linting: Passed (or score)
- ✅ No code smells

### Security Scan
- ✅ Dependency vulnerabilities: None found
- ✅ Secrets detection: No secrets in code
- ✅ Security best practices: All followed

### Performance Benchmarks
- ✅ Response times within SLA
- ✅ Resource usage acceptable
- ✅ No memory leaks
- ✅ Database queries optimized

## Test Plan for Reviewers

Please verify the following:

### Code Review
- [ ] Review code changes for quality and maintainability
- [ ] Check adherence to project coding standards
- [ ] Verify error handling is comprehensive
- [ ] Ensure no security vulnerabilities
- [ ] Check for code duplication or complexity

### Testing
- [ ] Run test suite: `pytest`
- [ ] Verify all tests pass
- [ ] Check test coverage meets 80%+ threshold
- [ ] Review test quality and completeness

### Documentation
- [ ] Read implementation docs for accuracy
- [ ] Verify user guide is clear and helpful
- [ ] Check API docs match implementation
- [ ] Ensure CHANGELOG entry is accurate

### Integration
- [ ] Test integration with existing features
- [ ] Verify no regressions introduced
- [ ] Check backward compatibility
- [ ] Test in staging environment (if applicable)

### Manual Testing
- [ ] Test happy path scenarios
- [ ] Test error scenarios
- [ ] Test edge cases
- [ ] Verify security measures work

## Acceptance Criteria

From issue #123:

- [x] User can register with email and password
- [x] User can login with email and password
- [x] User can reset password via email
- [x] User can login with OAuth (Google, GitHub)
- [x] Session management with configurable timeout
- [x] Role-based access control system
- [x] 80%+ test coverage
- [x] Comprehensive documentation

All acceptance criteria met ✅

## Related Issues/PRs

- Closes #123
- Related to #100 (authentication epic)
- Depends on #110 (email service)
- Blocks #130 (user profiles)

## Screenshots/Demos

[If UI changes, add screenshots or GIFs]
[If CLI tool, add terminal output examples]

## Deployment Notes

**Deploy Requirements**:
- Run database migrations: `alembic upgrade head`
- Update environment variables in production
- Restart application servers
- Clear Redis cache (if applicable)

**Rollback Plan**:
- Revert database migrations: `alembic downgrade -1`
- Restore previous environment variables
- Rollback to previous deployment

## Additional Notes

[Any other context, decisions, or information reviewers should know]

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Deliverable**: Comprehensive PR description

---

### 6. Create Pull Request

**Objective**: Create PR on GitHub with gh CLI.

**Using gh CLI**:
```bash
# Create PR with title and body
gh pr create \
  --title "feat: implement user authentication system (#123)" \
  --body "$(cat <<'EOF'
## Feature Summary

[Your comprehensive PR description here]
EOF
)"

# Alternative: Create PR interactively
gh pr create
# Will prompt for title, body, reviewers, etc.

# Alternative: Use file for body
cat > pr-body.md <<'EOF'
[Your PR description]
EOF
gh pr create --title "feat: ..." --body-file pr-body.md
```

**Add labels and reviewers**:
```bash
# Create PR with labels
gh pr create \
  --title "feat: user authentication (#123)" \
  --body "..." \
  --label "enhancement,security" \
  --reviewer username1,username2 \
  --assignee @me

# Or add after creation
gh pr edit 123 --add-label "documentation"
gh pr edit 123 --add-reviewer username
```

**Set base branch**:
```bash
# If targeting non-default branch
gh pr create \
  --base develop \
  --head feature/issue-123 \
  --title "..." \
  --body "..."
```

**Handle PR creation errors**:

**Error: gh not authenticated**
```bash
# Authenticate gh CLI
gh auth login
# Follow prompts
```

**Error: Repository not found**
```bash
# Verify remote URL
git remote -v

# If wrong, update
git remote set-url origin https://github.com/user/repo.git
```

**Error: Branch not pushed**
```bash
# Push branch first
git push -u origin feature/issue-123

# Then create PR
gh pr create ...
```

**Deliverable**: Pull request created on GitHub

---

### 7. Update Project Tracking

**Objective**: Update project documentation to reflect PR creation.

**Update TASK.md**:
```bash
# Read TASK.md
Read TASK.md

# Update to mark issue completed with PR link
Edit TASK.md
old_string: "- [ ] Issue #123: User authentication system"
new_string: "- [x] Issue #123: User authentication system (PR #456)"
```

**Example TASK.md update**:
```markdown
## Sprint 2: Authentication

### Completed
- [x] Issue #123: User authentication system (PR #456) ✅
  - Status: PR created, awaiting review
  - Completed: 2024-01-15

### In Progress
- [ ] Issue #124: User profiles

### Upcoming
- [ ] Issue #125: Password policies
```

**Add follow-up tasks** (if identified):
```markdown
## Follow-up Tasks

From PR #456 (Issue #123):
- [ ] Add OAuth provider for Microsoft
- [ ] Implement 2FA support
- [ ] Add session activity logging
```

**Deliverable**: TASK.md updated

---

### 8. Verify PR Quality

**Objective**: Ensure PR meets all quality standards.

**Quality Checklist**:
- [ ] PR title follows conventional commits format
- [ ] PR description is comprehensive
- [ ] All sections filled out (summary, implementation, security, testing, etc.)
- [ ] Test coverage details included
- [ ] Documentation links work
- [ ] Breaking changes documented (if any)
- [ ] Migration notes provided (if needed)
- [ ] Acceptance criteria listed and checked
- [ ] Issue references included (Closes #123)
- [ ] Test plan for reviewers provided
- [ ] All CI checks passing
- [ ] No merge conflicts
- [ ] Labels appropriate
- [ ] Reviewers assigned

**View PR to verify**:
```bash
# View PR in browser
gh pr view --web

# View PR in terminal
gh pr view

# Check CI status
gh pr checks
```

**Deliverable**: High-quality PR ready for review

---

## Git Workflow Best Practices

### Branch Naming

**Convention**: `<type>/<issue-number>-<brief-description>`

**Examples**:
- `feature/123-user-authentication`
- `fix/124-memory-leak`
- `docs/125-api-documentation`
- `refactor/126-database-layer`

**Create feature branch**:
```bash
# From main branch
git checkout main
git pull origin main
git checkout -b feature/123-user-auth
```

### Commit Messages

**Follow Conventional Commits**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Examples**:
```
feat(auth): add JWT authentication

Implement JWT-based authentication with refresh tokens.

Closes #123

fix(cache): resolve memory leak in cache manager

The cache manager was not properly releasing memory
when items expired, causing gradual RAM increase.

Fixes #124

docs(api): update authentication API documentation

Add examples and clarify error responses.
```

### Keeping Branch Updated

**Rebase on main** (if no conflicts):
```bash
# Update main
git checkout main
git pull origin main

# Rebase feature branch
git checkout feature/123-user-auth
git rebase main

# Force push (if already pushed)
git push --force-with-lease origin feature/123-user-auth
```

**Merge main** (if conflicts or team prefers merge):
```bash
# Update main
git checkout main
git pull origin main

# Merge into feature
git checkout feature/123-user-auth
git merge main

# Resolve conflicts if any
# Then push
git push origin feature/123-user-auth
```

---

## PR Templates

### Minimal PR Template

```markdown
## Summary
[What was done]

## Changes
- [Change 1]
- [Change 2]

## Testing
[How it was tested]

## Checklist
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Ready for review

Closes #[issue]
```

### Standard PR Template

```markdown
## Summary
[Brief overview]

## Implementation
[Key technical details]

## Testing
- Coverage: [X]%
- Test types: [unit, integration, etc.]

## Documentation
- [ ] Updated
- Links: [doc links]

## Breaking Changes
[Yes/No - with details if yes]

## Checklist
- [ ] Tests passing
- [ ] Code quality checks passed
- [ ] Documentation updated
- [ ] CHANGELOG updated

Closes #[issue]
```

### Comprehensive PR Template

[Use the full template from section 5]

---

## Common Issues and Solutions

### Issue: PR too large

**Problem**: PR has too many changes, hard to review

**Solution**:
1. Break into smaller PRs
2. Create epic issue for tracking
3. Submit incremental PRs

```bash
# Create separate branches for each part
git checkout -b feature/123-auth-part1-models
# Implement models only, create PR

git checkout main
git checkout -b feature/123-auth-part2-service
# Implement service, create PR

# etc.
```

### Issue: Merge conflicts

**Problem**: Branch conflicts with main

**Solution**:
1. Update main
2. Rebase or merge main into feature
3. Resolve conflicts
4. Test everything still works
5. Push updated branch

```bash
git checkout main
git pull origin main
git checkout feature/123-auth
git rebase main
# Resolve conflicts
git add .
git rebase --continue
# Test
pytest
git push --force-with-lease origin feature/123-auth
```

### Issue: CI checks failing

**Problem**: PR created but CI checks fail

**Solution**:
1. View check details
2. Fix issues locally
3. Commit and push fixes
4. Verify checks pass

```bash
# View checks
gh pr checks

# Fix issues
# Commit fixes
git add .
git commit -m "fix: resolve CI check failures"
git push origin feature/123-auth

# Verify
gh pr checks
```

### Issue: Missing information in PR

**Problem**: Reviewer asks for more details

**Solution**:
Update PR description

```bash
# Edit PR description
gh pr edit 456 --body "$(cat <<'EOF'
[Updated comprehensive description]
EOF
)"

# Or edit in browser
gh pr edit 456
# Opens editor
```

---

## Supporting Resources

### Git Commands Reference

```bash
# Branch operations
git branch                          # List branches
git checkout -b feature/123        # Create and switch
git branch -d feature/123          # Delete branch
git push -u origin feature/123     # Push with upstream

# Status and diff
git status                         # Working tree status
git diff                           # Unstaged changes
git diff --staged                  # Staged changes
git diff main..HEAD                # Changes vs main

# Commit operations
git add .                          # Stage all changes
git commit -m "message"            # Commit with message
git commit --amend                 # Amend last commit

# Remote operations
git fetch origin                   # Fetch from remote
git pull origin main               # Pull main branch
git push origin feature/123        # Push branch
git push --force-with-lease        # Safe force push

# Log and history
git log --oneline                  # Compact log
git log --graph --all              # Graph view
git log main..HEAD                 # Commits not in main
```

### GitHub CLI Reference

```bash
# PR creation
gh pr create                       # Interactive
gh pr create --title "..." --body "..."  # Direct

# PR management
gh pr list                         # List PRs
gh pr view 123                     # View PR
gh pr view --web                   # View in browser
gh pr edit 123                     # Edit PR
gh pr close 123                    # Close PR
gh pr merge 123                    # Merge PR

# PR checks
gh pr checks                       # View check status
gh pr diff                         # View PR diff

# Reviews
gh pr review 123 --approve         # Approve PR
gh pr review 123 --comment "..."   # Add comment
gh pr review 123 --request-changes # Request changes
```

---

## Integration with Deployment Flow

**Input**: Completed feature with documentation and CHANGELOG
**Process**: Systematic PR creation with comprehensive description
**Output**: High-quality pull request ready for review
**Next Step**: Code review and merge

---

## Quality Standards

PR is ready when:
- All pre-flight checks passed
- Commit message comprehensive and follows conventions
- Code pushed to remote
- PR title follows conventional commits
- PR description complete with all sections
- Test coverage details included
- Documentation links work
- Breaking changes documented
- Acceptance criteria checked
- Issue references included
- Test plan provided
- TASK.md updated
- No merge conflicts
- All CI checks passing