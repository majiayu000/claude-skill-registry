---
name: open-source-contributions
description: |
  Create maintainer-friendly pull requests with clean code and professional communication. Prevents 16 common mistakes that cause PR rejection.

  Use when: contributing to open source, submitting PRs, or troubleshooting PR rejection, CI failures, or personal artifacts in commits.
user-invocable: true
---

# Open Source Contributions Skill

**Version**: 1.2.0 | **Last Verified**: 2026-01-09 | **Production Tested**: ✅

---

## When to Use This Skill

**Auto-triggers**: "submit PR to", "contribute to", "pull request for", "open source contribution"

Create maintainer-friendly PRs while avoiding the 16 common mistakes that cause rejection.

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


### Commit Message Format

**Conventional Commits**: `<type>(<scope>): <subject>`

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `ci`, `chore`

Example: `feat(auth): add OAuth2 support for Google and GitHub`

See `references/commit-message-guide.md` for complete guide.

---

## PR Sizing Best Practices

**Research-backed guidelines:**
- **Ideal**: 50 lines
- **Good**: <200 lines
- **Maximum**: 400 lines
- **Beyond 400**: Defect detection drops significantly

**Keep PRs small:**
- One change per PR
- Use feature flags for incomplete work:
  ```typescript
  if (featureFlags.newAuth) {
    // New OAuth flow (incomplete but behind flag)
  } else {
    // Existing flow
  }
  ```
- Break by layer: schema → API → frontend → tests

---

## Following Project Conventions

**Before contributing:**
1. Read CONTRIBUTING.md (check `/`, `/.github/`, `/docs/`)
2. Run formatters: `npm run lint`, `npm run format`
3. Match existing patterns (review recent merged PRs)
4. Test before submitting:
   ```bash
   npm test && npm run lint && npm run build
   ```

---

## Communication Best Practices

**Response templates:**
- Implemented: "Good idea! Implemented in [commit hash]"
- Disagreement: "I see your point. I went with X because Y. Open to alternatives."
- Clarification: "Could you help me understand what you mean by Z?"
- Ping (after 1-2 weeks): "Gently pinging this PR. Happy to make changes!"

---

## Common Mistakes That Annoy Maintainers (16 Errors Prevented)

**See Critical Workflow Rules section for detailed guidance on Rules 1-3**

1. **Not Reading CONTRIBUTING.md** - ALWAYS read first, follow exactly
2. **Including Personal Artifacts** - SESSION.md, planning/*, screenshots, temp tests (use pre-PR check script)
3. **Massive Pull Requests** - Break into <200 lines ideal, <400 max
4. **Not Testing Before Submitting** - Run full test suite, test manually, capture evidence (violates RULE 2)
5. **Working on Assigned Issues** - Check assignments, comment to claim work
6. **Not Discussing Large Changes First** - Open issue or comment before coding
7. **Being Impatient/Unresponsive** - Be responsive, ping after 1-2 weeks
8. **Not Updating Documentation** - Update README, API docs, inline comments
9. **Ignoring Code Style** - Use project's linters/formatters
10. **Ignoring CI Failures** - Fix immediately, ask for help if stuck
11. **Including Unrelated Changes** - One PR = One Feature (violates RULE 3)
12. **Not Linking Issues** - Use "Closes #123" or "Fixes #456"
13. **Committing Secrets** - Never commit .env, scan for secrets
14. **Force-Pushing Without Warning** - Avoid after review starts
15. **Not Running Build/Tests Locally** - Always run before pushing
16. **Working on main/master** - ALWAYS use feature branches (violates RULE 1)

---

## GitHub-Specific Best Practices

### Critical Workflow Rules (NEVER SKIP)

**RULE 1: ALWAYS Work on a Feature Branch**

```bash
# ✅ CORRECT
git checkout main
git pull upstream main
git checkout -b feature/add-oauth-support
# make changes on feature branch
git commit -m "feat(auth): add OAuth support"
```

**Branch naming**: `feature/name`, `fix/issue-123`, `docs/update-readme`, `refactor/utils`, `test/add-tests`

---

**RULE 2: Test Thoroughly BEFORE Submitting PR**

Never submit without:
1. Running full test suite: `npm test && npm run lint && npm run build`
2. Testing manually (run app, test feature, edge cases)
3. Capturing evidence (screenshots/videos for visual changes - add to PR description, NOT commits)
4. Checking CI will pass

**Testing checklist template:**
```markdown
## Testing Performed
### Automated Tests
- ✅ All existing tests pass
- ✅ Added 12 new tests for OAuth flow
- ✅ Coverage increased from 85% to 87%

### Manual Testing
- ✅ Tested Google/GitHub OAuth flows end-to-end
- ✅ Verified error handling
- ✅ Tested on Chrome, Firefox, Safari
```

---

**RULE 3: Keep PRs Focused and Cohesive**

**One PR = One Feature/Fix**

- Ideal: <200 lines
- Acceptable: 200-400 lines
- Large: 400-800 lines (needs justification)
- Too large: >800 lines (split it)

**Keep focused:**
- Plan: What ONE thing does this PR do?
- During dev: Unrelated bug? Separate branch
- Before commit: `git diff` - Is every change necessary for THIS feature?

**Break large features into phases:**
```
PR #1: Database schema and models
PR #2: API endpoints
PR #3: Frontend components
PR #4: Integration and tests
```

---

### Using Draft PRs

**Create**: `gh pr create --draft`
**Mark ready**: `gh pr ready` (when code complete, tests passing, CI passing)

### Linking Issues

**Auto-closing keywords** (in PR description):
```markdown
Closes #123
Fixes #456
Resolves #789

# Multiple: Fixes #10, closes #20, resolves #30
# Cross-repo: Fixes owner/repo#123
```

### GitHub CLI Essentials

```bash
gh pr create --fill                    # Auto-fill from commits
gh pr create --draft                   # Draft PR
gh pr status                           # See your PRs
gh pr checks                           # View CI status
gh pr ready                            # Mark draft as ready
```

---

## Pre-Submission Checklist

See `references/pr-checklist.md` for complete version.

**Pre-Contribution:**
- [ ] Read CONTRIBUTING.md, CODE_OF_CONDUCT.md
- [ ] Commented on issue to claim work
- [ ] Created feature branch (NEVER work on main)

**Development:**
- [ ] **RULE 1**: Working on feature branch
- [ ] **RULE 2**: Tested thoroughly with evidence
- [ ] **RULE 3**: PR focused on single feature
- [ ] All tests pass: `npm test && npm run lint && npm run build`
- [ ] Updated documentation

**Cleanup:**
- [ ] Ran `./scripts/pre-pr-check.sh`
- [ ] No personal artifacts (SESSION.md, planning/*, debug screenshots, temp tests)
- [ ] No secrets (.env, credentials)

**PR Quality:**
- [ ] Focused on one change (<200 lines ideal, <400 max)
- [ ] Title: Conventional Commits format
- [ ] Description: What/Why/How structure
- [ ] Links to issues (Closes #123)
- [ ] Screenshots for visual changes (in PR description)

**Post-Submission:**
- [ ] Monitor CI, fix failures immediately
- [ ] Respond to feedback promptly

---

## Bundled Resources

See bundled examples and scripts:
- `scripts/pre-pr-check.sh` - Scan for artifacts before submission
- `scripts/clean-branch.sh` - Remove common personal artifacts
- `references/pr-template.md` - PR description template
- `references/pr-checklist.md` - Complete checklist
- `references/commit-message-guide.md` - Conventional commits guide
- `assets/good-pr-example.md` - Well-structured PR example
- `assets/bad-pr-example.md` - Common mistakes to avoid

---

## Key Takeaways

1. **RULE 1**: ALWAYS use feature branches (never main)
2. **RULE 2**: Test thoroughly before submitting (automated + manual + evidence)
3. **RULE 3**: Keep PRs focused (<200 lines ideal, one change per PR)
4. **Clean PRs**: Remove personal artifacts (SESSION.md, planning/*, debug screenshots)
5. **Read CONTRIBUTING.md**: Always read first, follow exactly
6. **Link Issues**: Use "Closes #123" to auto-close
7. **Use `./scripts/pre-pr-check.sh`**: Scan for artifacts before submission

---

**Production Tested**: Real-world open source contributions and maintainer feedback

**Token Efficiency**: ~70% savings vs trial-and-error

**Errors Prevented**: 16 common mistakes

**Last Verified**: 2026-01-09
