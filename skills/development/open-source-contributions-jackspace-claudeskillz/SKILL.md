---
name: open-source-contributions
description: |
  Use this skill when contributing code to open source projects. The skill covers proper pull request creation, avoiding common mistakes that annoy maintainers, cleaning up personal development artifacts before submission, writing effective PR descriptions, following project conventions, and communicating professionally with maintainers. It prevents 16 common contribution mistakes including working on main branch, not testing before PR submission, including unrelated changes, submitting planning documents, session notes, temporary test files, screenshots, and other personal artifacts. Includes 3 Critical Workflow Rules that must NEVER be skipped: (1) Always work on feature branches, (2) Test thoroughly with evidence before PR, (3) Keep PRs focused on single feature. The skill includes automation scripts to validate PRs before submission, templates for PR descriptions and commit messages, and comprehensive checklists. This skill should be used whenever creating pull requests for public repositories, contributing to community projects, or submitting code to projects you don't own.

  Keywords: open source contributions, github pull request, PR best practices, contribution guidelines, feature branch workflow, PR description, commit messages, open source etiquette, maintainer-friendly PR, PR checklist, clean PR, avoid personal artifacts, session notes cleanup, planning docs cleanup, test before PR, unrelated changes, working on main branch, focused PR, single feature PR, professional communication, community contributions, public repository contributions, fork workflow, upstream sync
license: MIT
metadata:
  version: "1.1.0"
  author: "Jeremy Dawes - Jezweb"
  repository: "https://github.com/jezweb/claude-skills"
  last_verified: "2025-11-06"
  production_tested: true
  token_savings: "~70%"
  errors_prevented: 16
---

# Open Source Contributions Skill

**Version**: 1.1.0 | **Last Verified**: 2025-11-06 | **Production Tested**: ✅

---

## Overview

Contributing to open source projects requires understanding etiquette, conventions, and what maintainers expect. This skill helps create professional, maintainer-friendly pull requests while avoiding common mistakes that waste time and cause rejections.

**Key Focus**: Cleaning personal development artifacts, writing proper PR descriptions, following project conventions, and communicating professionally.

---

## When to Use This Skill

Use this skill when:
- Creating pull requests for public repositories
- Contributing to community open source projects
- Submitting code to projects you don't maintain
- First-time contributor to a new project
- Want to increase PR acceptance rate
- Need guidance on PR best practices

**Auto-triggers on phrases**: "submit PR to", "contribute to", "pull request for", "open source contribution"

---

## What NOT to Include in Pull Requests

### Personal Development Artifacts (NEVER Include)

**Planning & Notes Documents:**
```
❌ SESSION.md              # Session tracking notes
❌ NOTES.md                # Personal development notes
❌ TODO.md                 # Personal todo lists
❌ planning/*              # Planning documents directory
❌ IMPLEMENTATION_PHASES.md # Project planning
❌ DATABASE_SCHEMA.md      # Unless adding new schema to project
❌ ARCHITECTURE.md         # Unless documenting new architecture
❌ SCRATCH.md              # Temporary notes
❌ DEBUGGING.md            # Debugging notes
❌ research-logs/*         # Research notes
```

**Screenshots & Visual Assets:**
```
❌ screenshots/debug-*.png     # Debugging screenshots
❌ screenshots/test-*.png      # Testing screenshots
❌ screenshot-*.png            # Ad-hoc screenshots
❌ screen-recording-*.mp4      # Screen recordings
❌ before-after-local.png      # Local comparison images

✅ screenshots/feature-demo.png   # IF demonstrating feature in PR description
✅ docs/assets/ui-example.png     # IF part of documentation update
```

**Test Files (Situational):**
```
❌ test-manual.js          # Manual testing scripts
❌ test-debug.ts           # Debugging test files
❌ quick-test.py           # Quick validation scripts
❌ scratch-test.sh         # Temporary test scripts
❌ example-local.json      # Local test data

✅ tests/feature.test.js   # Proper test suite additions
✅ tests/fixtures/data.json # Required test fixtures
✅ __tests__/component.tsx  # Component tests
```

**Build & Dependencies:**
```
❌ node_modules/           # Dependencies (in .gitignore)
❌ dist/                   # Build output (in .gitignore)
❌ build/                  # Build artifacts (in .gitignore)
❌ .cache/                 # Cache files (in .gitignore)
❌ package-lock.json       # Unless explicitly required by project
❌ yarn.lock               # Unless explicitly required by project
```

**IDE & OS Files:**
```
❌ .vscode/                # VS Code settings
❌ .idea/                  # IntelliJ settings
❌ .DS_Store               # macOS file system
❌ Thumbs.db               # Windows thumbnails
❌ *.swp, *.swo            # Vim swap files
❌ *~                      # Editor backup files
```

**Secrets & Sensitive Data:**
```
❌ .env                    # Environment variables (NEVER!)
❌ .env.local              # Local environment config
❌ config/local.json       # Local configuration
❌ credentials.json        # Credentials (NEVER!)
❌ *.key, *.pem            # Private keys (NEVER!)
❌ secrets/*               # Secrets directory (NEVER!)
```

**Temporary & Debug Files:**
```
❌ temp/*                  # Temporary files
❌ tmp/*                   # Temporary directory
❌ debug.log               # Debug logs
❌ *.log                   # Log files
❌ dump.sql                # Database dumps
❌ core                    # Core dumps
❌ *.prof                  # Profiling output
```

### What SHOULD Be Included

```
✅ Source code changes      # The actual feature/fix
✅ Tests for changes        # Required tests for new code
✅ Documentation updates    # README, API docs, inline comments
✅ Configuration changes    # If part of the feature
✅ Migration scripts        # If needed for the feature
✅ Package.json updates     # If adding/removing dependencies
✅ Schema changes           # If part of feature (with migrations)
✅ CI/CD updates            # If needed for new workflows
```

---

## Pre-PR Cleanup Process

### Step 1: Run Pre-PR Check Script

Use the bundled `scripts/pre-pr-check.sh` to scan for artifacts:

```bash
./scripts/pre-pr-check.sh
```

**What it checks:**
- Personal documents (SESSION.md, planning/*, NOTES.md)
- Screenshots not referenced in PR description
- Temporary test files
- Large files (>1MB)
- Potential secrets in file content
- PR size (warns if >400 lines)
- Uncommitted changes

### Step 2: Review Git Status

```bash
git status
git diff --stat
```

**Ask yourself:**
- Is every file change necessary for THIS feature/fix?
- Are there any unrelated changes?
- Are there files I added during development but don't need?

### Step 3: Clean Personal Artifacts

**Manual removal:**
```bash
git rm --cached SESSION.md
git rm --cached -r planning/
git rm --cached screenshots/debug-*.png
git rm --cached test-manual.js
```

**Or use the clean script:**
```bash
./scripts/clean-branch.sh
```

### Step 4: Update .gitignore

Add personal patterns to `.git/info/exclude` (affects only YOUR checkout):
```
# Personal development artifacts
SESSION.md
NOTES.md
TODO.md
planning/
screenshots/debug-*.png
test-manual.*
scratch.*
```

---

## Writing Effective PR Descriptions

### Use the What/Why/How Structure

**Template** (see `references/pr-template.md`):

```markdown
## What?
[Brief description of what this PR does]

## Why?
[Explain the reasoning, business value, or problem being solved]

## How?
[Describe the implementation approach and key decisions]

## Testing
[Step-by-step instructions for reviewers to test]

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CI passing
- [ ] Breaking changes documented

## Related Issues
Closes #123
Relates to #456
```

### Example Good PR Description

```markdown
## What?
Add OAuth2 authentication support for Google and GitHub providers

## Why?
Users have requested social login to reduce friction during signup.
This implements Key Result 2 of Q4 OKR1.

## How?
- Implemented OAuth2 flow using passport.js
- Added provider configuration in environment variables
- Created callback routes for each provider
- Updated user model to link social accounts

## Testing
1. Set up OAuth apps in Google/GitHub developer consoles
2. Add credentials to `.env` (see `.env.example`)
3. Run `npm start`
4. Click "Login with Google" and verify flow
5. Verify user profile merges correctly

## Breaking Changes
None - this is additive functionality

## Related Issues
Closes #234
Relates to #156 (social login epic)
```

### Titles: Follow Conventional Commits

**Format**: `<type>(<scope>): <description>`

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Formatting (no code change)
- `refactor:` - Code restructuring (no behavior change)
- `perf:` - Performance improvement
- `test:` - Adding/updating tests
- `build:` - Build system changes
- `ci:` - CI configuration changes
- `chore:` - Other changes (no src/test changes)

**Examples:**
```
✅ feat(auth): add OAuth2 support for Google and GitHub
✅ fix(api): resolve memory leak in worker shutdown
✅ docs(readme): update installation instructions for v2.0
✅ refactor(utils): extract validation logic to separate module

❌ Fixed stuff
❌ Updates
❌ Working on authentication (too vague)
```

---

## Commit Message Best Practices

### Structure

See `references/commit-message-guide.md` for complete guide.

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Subject line rules:**
- 50 characters max
- Imperative mood ("Add" not "Added")
- Capitalize first word
- No period at end
- Describe WHAT changed

**Body rules (optional):**
- 72 characters per line
- Explain WHY (code shows WHAT)
- Separate from subject with blank line

**Footer (optional):**
- Reference issues: `Closes #123`
- Note breaking changes: `BREAKING CHANGE: ...`

### Examples

**Good:**
```
fix: prevent race condition in cache invalidation

The cache invalidation logic wasn't thread-safe, causing
occasional race conditions when multiple workers tried to
invalidate the same key simultaneously.

Added mutex locks around the critical section and tests
to verify thread-safety.

Fixes #456
```

**Bad:**
```
Fixed bug                          # Too vague
WIP                               # Not descriptive
asdf                              # Meaningless
Updated auth.js                   # Describes file, not change
Fixed the issue with the thing    # No specifics
```

---

## PR Sizing Best Practices

### Ideal Sizes

**Research-backed guidelines:**
- **Ideal**: 50 lines of code
- **Good**: Under 200 lines
- **Maximum**: 400 lines
- **Beyond 400**: Defect detection drops significantly

**Why small PRs matter:**
- Faster reviews (maintainers can review in one sitting)
- Easier to find bugs
- Simpler to revert if needed
- Reduced merge conflicts
- More focused discussions

### How to Keep PRs Small

**1. One Change = One PR**
```
❌ BAD: Refactor auth module + add OAuth + fix bug + update docs (800 lines)

✅ GOOD:
  PR #1: Refactor auth module (150 lines)
  PR #2: Add OAuth support (200 lines)
  PR #3: Fix authentication bug (50 lines)
  PR #4: Update authentication docs (80 lines)
```

**2. Separate Refactoring from Features**
```
❌ BAD: Add feature X + refactor related code (500 lines)

✅ GOOD:
  PR #1: Refactor to prepare for feature X (200 lines)
  PR #2: Add feature X (150 lines)
```

**3. Use Feature Flags**
Ship incomplete features behind flags, merge early and often:
```typescript
if (featureFlags.newAuth) {
  // New OAuth flow (incomplete but behind flag)
} else {
  // Existing flow
}
```

**4. Break Down by Layer**
```
For "User Authentication" feature:
  PR #1: Database schema + migrations (100 lines)
  PR #2: API endpoints (150 lines)
  PR #3: Frontend components (200 lines)
  PR #4: Tests + documentation (150 lines)
```

### When Large PRs Are Acceptable

- Initial project scaffolding
- Generated code (clearly marked as such)
- Large refactors that can't be split (explain why in description)
- Documentation rewrites
- Dependency updates (automated)

**If unavoidable**: Add clear section headers in PR description to guide review.

---

## Following Project Conventions

### Step 1: Read CONTRIBUTING.md

**Always read this FIRST** - it's the project's law. Common locations:
- `/CONTRIBUTING.md`
- `/.github/CONTRIBUTING.md`
- `/docs/CONTRIBUTING.md`

**Key sections to check:**
- Development setup
- Testing requirements
- Code style guidelines
- Commit message format
- PR process
- Review expectations

**Tip**: Add `/contribute` to repository URL to find beginner-friendly issues.

### Step 2: Check for Style Guides

**Files to look for:**
- `.eslintrc`, `.eslintrc.js` (JavaScript/TypeScript linting)
- `.prettierrc` (Code formatting)
- `.editorconfig` (Editor settings)
- `STYLE.md` (Style guide documentation)
- `rustfmt.toml` (Rust formatting)
- `pyproject.toml` (Python formatting)

**Run formatters before committing:**
```bash
npm run lint                # Check for style issues
npm run lint:fix            # Auto-fix style issues
npm run format              # Format code (Prettier, Black, etc.)
```

### Step 3: Match Existing Patterns

**Look at recent merged PRs:**
- How are files organized?
- What naming conventions are used?
- How verbose are comments?
- What testing patterns exist?
- How are imports ordered?

**The Golden Rule**: "Do things the way the project maintainers would want it done."

### Step 4: Test Requirements

**Before submitting:**
```bash
# Run full test suite
npm test                    # Node projects
cargo test                  # Rust projects
pytest                      # Python projects
go test ./...               # Go projects

# Check coverage (if required)
npm run test:coverage

# Run linters
npm run lint

# Build the project
npm run build
```

**Never submit a PR with:**
- Failing tests
- Failing lints
- Build errors
- Untested new code (if tests are required)

---

## Communication Best Practices

### Before Starting Work

**Comment on the issue:**
```
Hi! I'd like to work on this issue. My approach would be to:
1. [Brief outline of approach]
2. [Key implementation detail]

Does this sound good? Any guidance before I start?
```

**Why this matters:**
- Prevents duplicate work
- Gets early feedback on approach
- Shows respect for maintainers' time
- Establishes communication

**Wait for acknowledgment** on significant changes before investing time.

### Writing PR Comments

**When submitting:**
```
@maintainer I've implemented the feature as discussed in #123.
I went with approach A instead of B because [reason].

Ready for review when you have time. Happy to make changes!
```

**When responding to feedback:**
```
Good catch! I've updated this in commit abc1234.
```

```
I considered that approach, but went with X because Y.
Happy to discuss alternatives if you prefer a different direction.
```

```
Could you elaborate on what you mean by Z?
I want to make sure I understand correctly.
```

### Responding to Review Comments

**Key principles:**
1. **Address every comment** - Even if just "Done" or "Acknowledged"
2. **Never respond in anger** - Walk away if needed, respond when calm
3. **Use GitHub's review tools**:
   - Mark conversations as resolved when addressed
   - Request re-review after changes
   - Use "suggestion" feature for quick fixes
4. **Keep discussion on-topic** - Take tangents elsewhere
5. **Be thankful** - Reviews are valuable, time-consuming work

**Response templates:**
- Implemented: "Good idea! Implemented in [commit hash]"
- Question: "Thanks for asking - I did X because Y. Thoughts?"
- Disagreement: "I see your point. I went with X because Y. Open to alternatives if you feel strongly."
- Clarification needed: "Could you help me understand what you mean by Z?"

### Handling PR Rejections

**Mental framework:**
- It's a learning experience, not a personal failure
- Rejection is normal and happens to everyone
- The project's vision might differ from your approach

**Steps to take:**
1. **Seek clarification** - Ask why the PR was rejected politely
2. **Review feedback carefully** - Identify specific concerns
3. **Learn from it** - What would you do differently next time?
4. **Options**:
   - Rework based on feedback
   - Fork and maintain your changes
   - Move on to other contributions

**What NOT to do:**
- Don't keep commenting on declined PRs
- Don't take it personally
- Don't argue aggressively
- Don't abandon the project entirely (unless it's truly not a fit)

### Be Patient (But Know When to Ping)

**Maintainers are often volunteers:**
- They have day jobs, families, lives
- They may be reviewing dozens of PRs
- They may be dealing with complex project issues

**Timeline expectations:**
- Small PRs: 1-7 days
- Large PRs: 1-2 weeks
- Complex/controversial: Weeks to months

**When to ping:**
- After 1 week for small PRs
- After 2 weeks for larger PRs
- When CI is failing due to external changes (rebase needed)

**How to ping:**
```
Hi! Just wanted to gently ping this PR.
No rush at all, just making sure it's on your radar.
Happy to answer any questions or make changes!
```

---

## Common Mistakes That Annoy Maintainers

### The Top 16 Mistakes

**See Critical Workflow Rules section for detailed guidance on Rules 1-3**

**1. Not Reading CONTRIBUTING.md**
- Impact: Wasted effort, rejected PRs, frustrated maintainers
- Fix: ALWAYS read this file first, follow instructions exactly

**2. Including Personal Development Artifacts**
- Impact: Messy PRs, reveals internal workflow, unprofessional
- Fix: Use pre-PR check script, clean artifacts before submission
- Examples: SESSION.md, planning/*, screenshots, temp test files

**3. Submitting Massive Pull Requests**
- Impact: Overwhelming to review, harder to find bugs, delays merge
- Fix: Break into smaller PRs (<200 lines ideal)

**4. Not Testing Code Before Submitting (Violates RULE 2)**
- Impact: CI failures, bugs in production, maintainer has to fix, loss of trust
- Fix: See **RULE 2** - Run full test suite, test manually, capture evidence (screenshots/videos), verify CI will pass

**5. Working on Already Assigned Issues**
- Impact: Duplicate work, wasted time for both contributors
- Fix: Check issue assignments, comment to claim work

**6. Not Discussing Changes First (for large changes)**
- Impact: Unwanted features, rejected PRs, wasted development time
- Fix: Open issue or comment to discuss before coding

**7. Being Impatient or Unresponsive**
- Impact: PRs stall, maintainers move on, contributions abandoned
- Fix: Be responsive but patient, ping respectfully after 1-2 weeks

**8. Not Updating Documentation**
- Impact: Users and developers confused by undocumented changes
- Fix: Update README, API docs, inline comments as needed

**9. Ignoring Code Style Standards**
- Impact: Messy codebase, maintainer has to fix formatting
- Fix: Use project's linters/formatters, match existing style

**10. Ignoring CI Failures**
- Impact: Can't merge, blocks progress, maintainer has to investigate
- Fix: Monitor CI, fix failures immediately, ask for help if stuck

**11. Including Unrelated Changes (Violates RULE 3)**
- Impact: Difficult review, harder to revert, scope creep, confusing git history
- Fix: See **RULE 3** - One PR = One Feature. Keep focused, split unrelated changes into separate branches/PRs

**12. Not Linking Issues Properly**
- Impact: Lost context, manual issue closing, harder to track
- Fix: Use "Closes #123" or "Fixes #456" in PR description

**13. Committing Secrets or Sensitive Data**
- Impact: Security risk, requires emergency response, potential breach
- Fix: Use .gitignore, scan for secrets, never commit .env files

**14. Force-Pushing Without Warning**
- Impact: Breaks reviewer's local copies, loses comments
- Fix: Avoid force-push after review starts, warn if necessary

**15. Not Running Build/Tests Locally**
- Impact: CI failures for obvious issues, wastes CI resources
- Fix: Always run `npm run build` and `npm test` before pushing

**16. Working Directly on main/master Branch (Violates RULE 1)**
- Impact: Messy git history, conflicts with upstream, can't work on multiple features, difficult to sync fork
- Fix: See **RULE 1** - ALWAYS create feature branches (`git checkout -b feature/my-feature`), NEVER commit to main

---

## GitHub-Specific Best Practices

### Fork Workflow (Standard for Open Source)

**Initial setup:**
```bash
# 1. Fork repository on GitHub (click Fork button)

# 2. Clone YOUR fork
git clone https://github.com/YOUR-USERNAME/project-name.git
cd project-name

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/project-name.git

# 4. Verify remotes
git remote -v
# origin    https://github.com/YOUR-USERNAME/project-name.git (fetch)
# origin    https://github.com/YOUR-USERNAME/project-name.git (push)
# upstream  https://github.com/ORIGINAL-OWNER/project-name.git (fetch)
# upstream  https://github.com/ORIGINAL-OWNER/project-name.git (push)
```

**Creating feature branch:**
```bash
# NEVER work on main/master directly!
git checkout -b feature/add-oauth-support

# Make changes...
git add .
git commit -m "feat(auth): add OAuth2 support"

# Push to YOUR fork
git push origin feature/add-oauth-support
```

**Keeping fork in sync:**
```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

### Critical Workflow Rules (NEVER SKIP)

**RULE 1: ALWAYS Work on a Feature Branch**

```bash
# ❌ NEVER DO THIS
git checkout main
# make changes directly on main
git commit -m "add feature"  # BAD!

# ✅ ALWAYS DO THIS
git checkout main
git pull upstream main  # Sync first
git checkout -b feature/add-oauth-support  # Descriptive branch name
# make changes on feature branch
git commit -m "feat(auth): add OAuth support"
```

**Why this matters:**
- Keeps main clean and in sync with upstream
- Allows working on multiple features simultaneously
- Makes it easy to abandon or restart work
- Required by most open source projects
- Prevents conflicts and messy git history

**Branch naming conventions:**
```
feature/descriptive-name    # New features
fix/issue-123               # Bug fixes
docs/update-readme          # Documentation
refactor/extract-utils      # Refactoring
test/add-unit-tests         # Test additions
```

---

**RULE 2: Test Thoroughly BEFORE Submitting PR**

Never submit a PR without:

1. **Running the full test suite locally:**
   ```bash
   npm test              # Node.js
   cargo test            # Rust
   pytest                # Python
   go test ./...         # Go
   ```

2. **Testing manually** (hands-on verification):
   - Run the application
   - Test the specific feature you added
   - Test edge cases and error conditions
   - Verify it works as intended

3. **Capturing evidence** (for visual/UI changes):
   - Take screenshots showing the feature working
   - Record a short demo video if complex
   - Include in PR description to demonstrate functionality

4. **Checking CI will pass:**
   ```bash
   npm run lint          # Linting
   npm run build         # Build succeeds
   npm run type-check    # TypeScript checks
   ```

**Example testing checklist for a new OAuth feature:**
```markdown
## Testing Performed

### Automated Tests
- ✅ All existing tests pass
- ✅ Added 12 new tests for OAuth flow
- ✅ Coverage increased from 85% to 87%

### Manual Testing
- ✅ Tested Google OAuth flow end-to-end
- ✅ Tested GitHub OAuth flow end-to-end
- ✅ Verified error handling (invalid tokens, network failures)
- ✅ Confirmed user profile merging works correctly
- ✅ Tested on Chrome, Firefox, Safari

### Evidence
See screenshots below showing successful login flow.
```

**Why this matters:**
- Prevents CI failures that waste maintainer time
- Shows you care about code quality
- Demonstrates the feature actually works
- Builds trust with maintainers
- Catches bugs before review

**Screenshots for PR descriptions:**
```
✅ Include: Working feature demonstration
✅ Include: Before/after comparisons for changes
✅ Include: Error state handling

❌ Don't include: Debug screenshots in code commits
❌ Don't include: Personal testing screenshots in repo
❌ Don't include: Unrelated screenshots

Location: Add to PR description on GitHub, NOT as files in commits
```

---

**RULE 3: Keep PRs Focused and Cohesive**

**One PR = One Feature/Fix**

```
✅ GOOD: Single PR adding OAuth support
  - OAuth provider configuration
  - Login/callback routes
  - User model updates
  - Tests for OAuth flow
  - Documentation for setup

❌ BAD: PR with multiple unrelated changes
  - OAuth support
  - + Unrelated bug fix in validation
  - + Random formatting changes
  - + Update to README for different feature
```

**Why cohesive PRs matter:**
- Easier to review and understand
- Can be merged/rejected independently
- Simpler to revert if issues found
- Faster review cycles
- Clear git history

**How to keep PRs focused:**

1. **Plan before coding:**
   - What is the ONE thing this PR does?
   - What files MUST be changed for this feature?
   - What's the minimal set of changes needed?

2. **During development:**
   - If you notice an unrelated bug, create a separate branch
   - If you're tempted to fix formatting, do it in a separate PR
   - Stay focused on the single goal

3. **Before committing:**
   - Review your changes: `git diff`
   - Ask: "Is this file change necessary for THIS feature?"
   - Move unrelated changes to stash: `git stash`

4. **Size guidelines:**
   - Ideal: <200 lines changed
   - Acceptable: 200-400 lines
   - Large: 400-800 lines (needs justification)
   - Too large: >800 lines (should be split)

**Breaking up large features:**

If a feature is naturally large, break it into phases:

```
PR #1: Database schema and models
PR #2: API endpoints
PR #3: Frontend components
PR #4: Integration and tests
```

Each PR:
- Builds on the previous
- Is independently reviewable
- Adds working functionality (or is clearly marked as WIP/foundational)

**Handling accidental scope creep:**

```bash
# You added OAuth + accidentally fixed a bug
# Split them into separate commits and PRs:

# 1. Create bug fix branch from main
git checkout main
git checkout -b fix/validation-bug

# 2. Cherry-pick just the bug fix commits
git cherry-pick <commit-hash-of-bug-fix>

# 3. Submit bug fix PR separately
git push origin fix/validation-bug

# 4. Continue with OAuth PR
git checkout feature/add-oauth-support
# Remove bug fix commits if needed
git rebase -i main
```

---

### Using Draft PRs

**When to use:**
- Code is work-in-progress, not ready for review
- You want early feedback on approach
- Starting conversation about implementation
- Sharing incomplete code for collaboration

**Benefits:**
- Prevents accidental merging
- Suppresses reviewer notifications
- Clearly signals "not ready yet"

**Create draft PR:**
```bash
gh pr create --draft --title "WIP: Add OAuth support"
```

**Mark ready when:**
- Code is complete and tested
- CI is passing
- Documentation is updated
- Ready for formal review

```bash
gh pr ready
```

### Linking Issues Properly

**Automatic closing keywords** (in PR description or commits):
```markdown
Closes #123
Fixes #456
Resolves #789

# Also works:
Close #123
Fix #123
Resolve #123

# Case insensitive:
CLOSES #123
fixes #123

# Multiple issues:
Fixes #10, closes #20, resolves #30

# Cross-repo:
Fixes owner/repo#123
```

**Important**: Only works when merging to DEFAULT branch (usually main).

### Using GitHub CLI

**Creating PRs efficiently:**
```bash
# Interactive (prompts for title/body)
gh pr create

# Auto-fill from commits
gh pr create --fill

# Complete non-interactive
gh pr create \
  --title "feat(auth): add OAuth support" \
  --body "$(cat <<'EOF'
## What?
Add OAuth2 authentication

## Why?
User request for social login

## Testing
1. Set up OAuth apps
2. Run npm start
3. Test login flow
EOF
)"

# With reviewers
gh pr create --reviewer username1,username2

# Draft PR
gh pr create --draft
```

**Other useful commands:**
```bash
gh pr status              # See your PRs
gh pr checks              # View CI status
gh pr view                # View current PR
gh pr diff                # See PR diff
gh pr ready               # Mark draft as ready
gh pr merge               # Merge PR (when approved)
```

---

## Pre-Submission Checklist

Use this checklist before submitting ANY pull request (see `references/pr-checklist.md`).

### Pre-Contribution

- [ ] Read CONTRIBUTING.md thoroughly
- [ ] Read CODE_OF_CONDUCT.md if present
- [ ] Checked if issue should be created first
- [ ] Commented on issue to claim work
- [ ] Maintainer acknowledged work (for significant changes)
- [ ] Forked repository (if no write access)
- [ ] Set up upstream remote
- [ ] Created feature branch (NEVER work on main)

### Development

**Critical Workflow Rules** (see detailed section above):
- [ ] **RULE 1**: Working on feature branch (NOT main/master)
- [ ] **RULE 2**: Tested thoroughly with evidence ready
- [ ] **RULE 3**: PR is focused on single feature/fix

**Code Quality:**
- [ ] Code follows project style guidelines
- [ ] Ran linters and formatters
- [ ] All tests pass locally (`npm test`, `cargo test`, etc.)
- [ ] Added tests for new functionality
- [ ] Manual testing performed (run app, test feature)
- [ ] Evidence captured (screenshots/videos for visual changes)
- [ ] Updated relevant documentation
- [ ] Commit messages follow conventions
- [ ] No merge conflicts with base branch
- [ ] Built project successfully (`npm run build`, etc.)

### Cleanup

- [ ] Ran pre-PR check script (`./scripts/pre-pr-check.sh`)
- [ ] Removed personal artifacts:
  - [ ] No SESSION.md or notes files
  - [ ] No planning/* documents
  - [ ] No debug screenshots
  - [ ] No temporary test files
  - [ ] No personal workflow files
- [ ] Reviewed git status for unwanted files
- [ ] No secrets or sensitive data
- [ ] No IDE/OS-specific files
- [ ] No build artifacts or dependencies

### PR Quality

- [ ] PR is focused on one change/issue
- [ ] PR is reasonably sized (<200 lines ideal, <400 max)
- [ ] No unrelated changes included
- [ ] Reviewed own diff for accidental changes
- [ ] Title follows conventions (Conventional Commits)
- [ ] Description uses What/Why/How structure
- [ ] Testing instructions included
- [ ] Links to related issues (Closes #123)
- [ ] Screenshots for visual changes (if demonstrating feature)
- [ ] Breaking changes noted
- [ ] Reviewers can understand without asking questions

### Submission

- [ ] CI/checks passing
- [ ] Pushed to feature branch on fork
- [ ] Created PR with proper description
- [ ] Assigned labels (if permitted)
- [ ] Requested reviewers (if known)
- [ ] Linked to project/milestone (if applicable)

### Post-Submission

- [ ] Monitoring CI for failures
- [ ] Responsive to feedback
- [ ] Addressing review comments promptly
- [ ] Marking conversations as resolved
- [ ] Requesting re-review after changes
- [ ] Thanking reviewers
- [ ] Being patient while waiting

---

## Quick Command Reference

### Git Workflow

```bash
# Setup
git clone https://github.com/YOUR-USERNAME/project.git
git remote add upstream https://github.com/ORIGINAL/project.git

# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to your fork
git push origin feature/my-feature

# Keep fork synced
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Rebase feature branch if needed
git checkout feature/my-feature
git rebase main
git push origin feature/my-feature --force-with-lease
```

### GitHub CLI

```bash
# Create PR
gh pr create --title "feat: ..." --body "..."

# Check status
gh pr status
gh pr checks

# View PR
gh pr view
gh pr diff

# Manage PR
gh pr ready              # Mark draft as ready
gh pr review --approve   # Approve (if reviewer)
gh pr merge             # Merge (when approved)
```

### Pre-PR Validation

```bash
# Run checks
npm run lint
npm test
npm run build

# Use skill script
./scripts/pre-pr-check.sh

# Check git status
git status
git diff --stat

# Review changes
git diff
git log --oneline -5
```

---

## Examples

See bundled examples for complete before/after comparisons:
- `assets/good-pr-example.md` - Well-structured PR
- `assets/bad-pr-example.md` - Common mistakes to avoid

---

## Key Takeaways

1. **Clean Your PRs** - Remove all personal development artifacts before submission
2. **Read CONTRIBUTING.md** - Always read this first, follow instructions exactly
3. **Keep PRs Small** - <200 lines ideal, one change per PR
4. **Test Everything** - Locally before submitting, fix CI failures immediately
5. **Follow Conventions** - Style, commits, testing, documentation
6. **Communicate Well** - Be respectful, responsive, patient, and professional
7. **Link Issues** - Use "Closes #123" to auto-close related issues
8. **Be Patient** - Maintainers are often volunteers with limited time
9. **Learn from Feedback** - Every review is a learning opportunity
10. **Use Automation** - Scripts, templates, and checklists prevent mistakes

---

## Resources

**Bundled Resources:**
- `scripts/pre-pr-check.sh` - Scan for artifacts before submission
- `scripts/clean-branch.sh` - Remove common personal artifacts
- `references/pr-template.md` - PR description template
- `references/pr-checklist.md` - Complete pre-submission checklist
- `references/commit-message-guide.md` - Conventional commits guide
- `references/files-to-exclude.md` - Comprehensive exclusion list
- `assets/good-pr-example.md` - Example of well-structured PR
- `assets/bad-pr-example.md` - Common mistakes to avoid

**External Resources:**
- GitHub Open Source Guides: https://opensource.guide/
- How to Contribute: https://opensource.guide/how-to-contribute/
- Conventional Commits: https://www.conventionalcommits.org/
- GitHub CLI: https://cli.github.com/manual/

---

**Production Tested**: ✅ Based on real-world open source contributions and maintainer feedback

**Token Efficiency**: ~70% savings vs learning through trial-and-error

**Errors Prevented**: 15 common mistakes documented with solutions

**Last Verified**: 2025-11-05
