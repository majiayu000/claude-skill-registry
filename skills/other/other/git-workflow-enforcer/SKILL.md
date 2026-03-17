---
name: git-workflow-enforcer
description: Enforce git commits after every phase and task to enable rollback and prevent lost work. Auto-trigger when completing phases, tasks, or when detecting uncommitted changes. Auto-commit with Conventional Commits format. Verify branch safety, check for merge conflicts, enforce clean working tree. Block completion if changes not committed.
---

<objective>
Prevent lost work and enable granular rollback by enforcing git commits after every meaningful change (phase completion, task completion) with automatic commit generation following Conventional Commits standards.
</objective>

<quick_start>
<auto_commit_workflow>
**Automatic commit generation when changes detected:**

1. **Detect uncommitted changes**: Run `git status --porcelain`
2. **Classify change type**: Phase completion, task completion, or file modification
3. **Generate commit message**: Use Conventional Commits format based on context
4. **Validate safety**: Check branch, merge conflicts, commit message format
5. **Execute commit**: Stage files and commit with generated message
6. **Provide feedback**: Show commit hash and rollback command

**Example:**
```
Context: Task T001 completed

❌ UNCOMMITTED CHANGES DETECTED
  Modified: api/models/message.py
  Created: api/tests/test_message.py

✅ AUTO-COMMITTING with generated message:
  feat(green): T001 implement Message model to pass test

  Implementation: SQLAlchemy model with validation
  Tests: 26/26 passing
  Coverage: 93% (+1%)

✅ COMMITTED: abc123f
  Rollback: git revert abc123f
```
</auto_commit_workflow>

<trigger_patterns>
**Auto-invoke when detecting:**

**Phase completion markers:**
- "Phase N complete"
- "/specify complete", "/plan complete", "/tasks complete"
- "analysis complete", "optimization complete"
- Phase command finishing

**Task completion markers:**
- "T### complete", "task ### done"
- "task-tracker mark-done" command
- "mark task complete"

**Change detection:**
- `git status --porcelain` returns non-empty
- Files created/modified/deleted
- Working tree dirty before phase transition
</trigger_patterns>

<commit_message_generation>
**Conventional Commits format:**
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Auto-detection logic:**

| Context | Type | Scope | Subject Template |
|---------|------|-------|------------------|
| Phase 0 | docs | spec | create specification for {feature} |
| Phase 0.5 | docs | clarify | resolve {n} clarifications for {feature} |
| Phase 1 | docs | plan | create implementation plan for {feature} |
| Phase 2 | docs | tasks | create task breakdown for {feature} ({n} tasks) |
| Phase 3 | docs | analyze | create cross-artifact analysis for {feature} |
| Phase 4 (RED) | test | red | {taskId} write failing test for {description} |
| Phase 4 (GREEN) | feat | green | {taskId} implement {description} to pass test |
| Phase 4 (REFACTOR) | refactor | - | {taskId} improve {description} |
| Phase 5 | docs | optimize | complete optimization review for {feature} |
| Phase 6 | docs | preview | create release notes for {feature} v{version} |

**Body generation:**
- Phase commits: Include metrics (task count, criteria count, etc.)
- Task commits: Include evidence (tests, coverage, commit hash)
- Fix commits: Include root cause and solution

See [references/commit-templates.md](references/commit-templates.md) for complete templates.
</commit_message_generation>
</quick_start>

<workflow>
<detection_phase>
**1. Monitor for Commit Triggers**

Check for uncommitted changes when:
- Phase command completes
- task-tracker mark-done-with-notes called
- User mentions "commit", "save progress", etc.

```bash
# Check for uncommitted changes
git status --porcelain

# If non-empty output → uncommitted changes exist
```
</detection_phase>

<classification_phase>
**2. Classify Change Type and Extract Context**

**Phase completion:**
- Extract phase name from workflow state or command
- Extract feature slug from current directory
- Get artifact file paths (spec.md, plan.md, etc.)

**Task completion:**
- Extract TaskId from task-tracker parameters or conversation
- Extract task description from tasks.md
- Get phase marker ([RED], [GREEN], [REFACTOR])
- Extract evidence (tests, coverage) from completion context

**File modification:**
- Analyze changed files to infer purpose
- Check git log for recent commit patterns
- Default to "chore" type if unclear
</classification_phase>

<validation_phase>
**3. Validate Safety Before Committing**

**Check 1: Branch safety**
```bash
CURRENT_BRANCH=$(git branch --show-current)

if [[ "$CURRENT_BRANCH" =~ ^(main|master)$ ]]; then
  ❌ BLOCKED: Direct commits to main/master not allowed
  Recommendation: git checkout -b feat/{feature-slug}
  Exit code: 1
fi

if [[ ! "$CURRENT_BRANCH" =~ ^(feat|feature|bugfix|fix|hotfix|chore)/ ]]; then
  ⚠️ WARNING: Branch name doesn't follow convention
  Expected: feat/*, bugfix/*, hotfix/*, chore/*
  Current: $CURRENT_BRANCH
  Proceed? (auto-yes in non-interactive mode)
fi
```

**Check 2: Merge conflicts**
```bash
# Check for conflict markers
if grep -r "<<<<<<<" . --exclude-dir=.git; then
  ❌ BLOCKED: Unresolved merge conflicts detected
  Resolve conflicts before committing
  Exit code: 1
fi

# Check git status for conflicts
if git status | grep -q "both modified"; then
  ❌ BLOCKED: Merge conflicts in git status
  Run: git status
  Exit code: 1
fi
```

**Check 3: Remote tracking**
```bash
# Check if branch has upstream
if ! git rev-parse --abbrev-ref @{upstream} &>/dev/null; then
  ⚠️ WARNING: Branch has no upstream tracking
  Recommendation: git push -u origin $(git branch --show-current)
  Continue without upstream? (auto-yes)
fi
```

**Check 4: Commit message format**
```bash
# Validate Conventional Commits format
COMMIT_MSG="$1"

# Check format: type(scope): subject
if ! [[ "$COMMIT_MSG" =~ ^(feat|fix|docs|test|refactor|perf|chore|ci|build|revert)(\([a-z0-9-]+\))?: ]]; then
  ❌ INVALID: Commit message doesn't follow Conventional Commits
  Expected: type(scope): subject
  Got: $COMMIT_MSG

  Auto-fix? (yes)
  → Prepend "chore: " to message
fi

# Check subject length (<50 chars recommended)
SUBJECT=$(echo "$COMMIT_MSG" | head -1)
if [[ ${#SUBJECT} -gt 72 ]]; then
  ⚠️ WARNING: Subject line too long (${#SUBJECT} > 72 chars)
  Recommendation: Keep under 50 chars for readability
fi
```

See [references/validation-rules.md](references/validation-rules.md) for complete validation logic.
</validation_phase>

<commit_generation_phase>
**4. Generate and Execute Commit**

**Stage files:**
```bash
# Get list of changed files
CHANGED_FILES=$(git status --porcelain | awk '{print $2}')

# Stage all changed files (auto-add for convenience)
git add $CHANGED_FILES

# Or stage all (if in feature directory)
git add specs/$FEATURE_SLUG/
```

**Generate commit message:**
```bash
# Use template based on context
if [[ "$CONTEXT" == "phase_complete" ]]; then
  TYPE="docs"
  SCOPE="$PHASE_NAME"
  SUBJECT="create $ARTIFACTS for $FEATURE_SLUG"

  BODY="- Artifacts: $(echo $ARTIFACTS | tr '\n' ', ')
- Phase: $PHASE_NAME
- Feature: $FEATURE_SLUG"

elif [[ "$CONTEXT" == "task_complete" ]]; then
  # Extract from tasks.md
  PHASE_MARKER=$(grep "$TASK_ID" tasks.md | grep -oP '\[([A-Z]+)\]' | tr -d '[]')

  if [[ "$PHASE_MARKER" == "RED" ]]; then
    TYPE="test"
    SCOPE="red"
  elif [[ "$PHASE_MARKER" == "GREEN" ]]; then
    TYPE="feat"
    SCOPE="green"
  elif [[ "$PHASE_MARKER" == "REFACTOR" ]]; then
    TYPE="refactor"
    SCOPE=""
  fi

  SUBJECT="$TASK_ID $(extract_task_description)"

  BODY="Implementation: $NOTES
Tests: $EVIDENCE
Coverage: $COVERAGE"
fi

# Construct full message
COMMIT_MESSAGE="${TYPE}(${SCOPE}): ${SUBJECT}

${BODY}"
```

**Execute commit:**
```bash
git commit -m "$(cat <<EOF
$COMMIT_MESSAGE
EOF
)"

COMMIT_HASH=$(git rev-parse --short HEAD)

echo "✅ COMMITTED: $COMMIT_HASH"
echo "  Rollback: git revert $COMMIT_HASH"
```

See [references/auto-commit-logic.md](references/auto-commit-logic.md) for detailed generation rules.
</commit_generation_phase>

<verification_phase>
**5. Verify and Provide Feedback**

**Verify commit succeeded:**
```bash
# Check that working tree is now clean
if [ -n "$(git status --porcelain)" ]; then
  ⚠️ WARNING: Working tree still dirty after commit
  Uncommitted files: $(git status --short)
  Manual review needed
fi

# Get commit details
COMMIT_HASH=$(git rev-parse --short HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_TIME=$(git log -1 --format=%ar)
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD | wc -l)
```

**Provide feedback:**
```markdown
✅ **AUTO-COMMIT SUCCESSFUL**

**Commit:** $COMMIT_HASH ($COMMIT_TIME)
**Message:** $COMMIT_MSG
**Files:** $CHANGED_FILES changed
**Branch:** $(git branch --show-current)

**Working tree:** Clean
**Rollback:** git revert $COMMIT_HASH
**Push:** git push
```

**Check for unpushed commits:**
```bash
UNPUSHED=$(git log @{u}.. --oneline 2>/dev/null | wc -l)

if [[ $UNPUSHED -gt 0 ]]; then
  ⚠️ **REMINDER: Unpushed Commits**

  You have $UNPUSHED unpushed commit(s) on this branch.

  Push to backup:
  git push
fi
```
</verification_phase>
</workflow>

<safety_checks>
**Blocking checks (prevent commit):**
- ❌ On main/master branch (unless deployment phase)
- ❌ Unresolved merge conflicts
- ❌ Invalid commit message format (auto-fixable with prompt)

**Warning checks (allow but warn):**
- ⚠️ Branch name doesn't follow conventions
- ⚠️ No upstream tracking configured
- ⚠️ Commit subject line >50 chars
- ⚠️ Unpushed commits exist

**Auto-fix attempts:**
- Branch: Suggest `git checkout -b feat/{slug}`
- Message format: Prepend "chore: " if type missing
- Upstream: Suggest `git push -u origin {branch}`

See [references/safety-checks.md](references/safety-checks.md) for complete check logic.
</safety_checks>

<anti_patterns>
**Avoid these mistakes:**

**1. Bundling multiple phases in one commit**
```bash
❌ BAD:
git commit -m "complete spec, plan, and tasks"

✅ GOOD:
git commit -m "docs(spec): create specification for user-messaging"
git commit -m "docs(plan): create implementation plan for user-messaging"
git commit -m "docs(tasks): create task breakdown for user-messaging"
```

**2. Committing to main/master directly**
```bash
❌ BAD:
(on main) git commit -m "feat: add feature"

✅ GOOD:
git checkout -b feat/user-messaging
git commit -m "feat: add message model"
```

**3. Vague commit messages**
```bash
❌ BAD:
git commit -m "fixes"
git commit -m "updates"
git commit -m "WIP"

✅ GOOD:
git commit -m "fix(api): correct message validation logic"
git commit -m "refactor: extract MessageService from controller"
```

**4. Skipping commits between tasks**
```bash
❌ BAD:
# Implement T001, T002, T003
git commit -m "implement all tasks"

✅ GOOD:
# Implement T001
git commit -m "feat(green): T001 implement Message model"
# Implement T002
git commit -m "feat(green): T002 implement MessageService"
# Implement T003
git commit -m "feat(green): T003 add /messages endpoint"
```

**5. Not checking for conflicts before commit**
```bash
❌ BAD:
git commit -m "fix: update model"
# Later: ❌ Push rejected, conflicts with remote

✅ GOOD:
git fetch
git merge origin/main
# Resolve any conflicts
git commit -m "fix: update model after merge"
```
</anti_patterns>

<success_criteria>
**Git workflow enforcement working when:**

- ✓ Uncommitted changes automatically committed after phase/task completion
- ✓ Commit messages follow Conventional Commits format
- ✓ Commits blocked on main/master (redirected to feature branch)
- ✓ Merge conflicts detected and block commit
- ✓ Branch naming conventions validated
- ✓ Unpushed commits detected and warned
- ✓ Working tree always clean between phases
- ✓ Every task has dedicated commit with hash in NOTES.md
- ✓ Rollback points available for every phase and task
- ✓ Commit subject lines concise (<50 chars recommended)

**Safety checks passing when:**
- Protected branches (main/master) have no direct commits
- All commits follow type(scope): subject format
- No unresolved merge conflict markers in codebase
- Branches have upstream tracking configured
- Clear rollback procedures available
</success_criteria>

<reference_guides>
For detailed templates, validation logic, and commit examples:

- **[references/commit-templates.md](references/commit-templates.md)** - Complete Conventional Commits templates by phase/task type
- **[references/auto-commit-logic.md](references/auto-commit-logic.md)** - Auto-commit generation rules and context extraction
- **[references/validation-rules.md](references/validation-rules.md)** - Safety checks, branch validation, conflict detection
- **[references/safety-checks.md](references/safety-checks.md)** - Blocking vs warning checks, auto-fix strategies
- **[references/rollback-procedures.md](references/rollback-procedures.md)** - Rollback commands for phases, tasks, and batches
</reference_guides>
