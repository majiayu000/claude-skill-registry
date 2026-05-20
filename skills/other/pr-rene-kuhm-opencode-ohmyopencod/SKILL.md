---
description: "Crear Pull Requests con template, descripción automática y checklist. Integración con GitHub."
user-invocable: true
argument-hint: "[--draft] [--base branch] [título]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Pull Request Skill

Eres un experto en crear Pull Requests profesionales. Tu rol es generar PRs bien documentados con descripciones claras y checklists completos.

## Flujo de Trabajo

### 1. Analizar Branch Actual

```bash
# Branch actual
git branch --show-current

# Commits desde base branch
git log origin/main..HEAD --oneline

# Archivos cambiados vs main
git diff origin/main --name-only

# Diff completo
git diff origin/main
```

### 2. Verificar Estado

```bash
# Verificar si hay cambios sin commit
git status

# Verificar si estamos adelante del remote
git status -uno

# Push si es necesario
git push -u origin $(git branch --show-current)
```

### 3. Crear PR

```bash
gh pr create \
  --title "feat(scope): description" \
  --body "$(cat <<'EOF'
## Summary

Brief description of what this PR does.

## Changes

- Change 1
- Change 2
- Change 3

## Type of Change

- [ ] 🐛 Bug fix
- [x] ✨ New feature
- [ ] 💥 Breaking change
- [ ] 📝 Documentation
- [ ] ♻️ Refactoring

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Checklist

- [x] Code follows project style guidelines
- [x] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings

## Screenshots (if applicable)

N/A

## Related Issues

Closes #123

---
🤖 Generated with [Claude Code](https://claude.com/code)
EOF
)"
```

## Plantilla de PR

### PR de Feature

```markdown
## Summary

Add [feature name] that allows users to [capability].

## Motivation

[Why is this change needed? What problem does it solve?]

## Changes

### Added
- New component `FeatureName.tsx`
- API endpoint `/api/feature`
- Database migration for `feature_table`

### Modified
- Updated `useFeature` hook with new methods
- Extended `FeatureService` with additional logic

### Removed
- Deprecated `oldFeature` component

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [x] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that causes existing functionality to change)
- [ ] 📝 Documentation update
- [ ] ♻️ Refactoring (no functional changes)

## Testing

### Unit Tests
- [x] `FeatureComponent.test.tsx` - Component rendering
- [x] `featureService.test.ts` - Service methods

### Integration Tests
- [x] `feature.e2e.test.ts` - Full user flow

### Manual Testing
1. Navigate to /feature
2. Click on "Create New"
3. Fill form and submit
4. Verify success message appears

## Screenshots

| Before | After |
|--------|-------|
| N/A | ![Feature Screenshot](url) |

## Checklist

- [x] My code follows the project's style guidelines
- [x] I have performed a self-review of my code
- [x] I have commented my code where necessary
- [x] I have updated the documentation
- [x] My changes generate no new warnings
- [x] I have added tests that prove my fix/feature works
- [x] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged

## Related Issues

Closes #123
Relates to #456

## Additional Notes

[Any additional context or notes for reviewers]

---
🤖 Generated with [Claude Code](https://claude.com/code)
```

### PR de Bug Fix

```markdown
## Summary

Fix [bug description] that was causing [symptom].

## Root Cause

[Technical explanation of what was wrong]

## Solution

[How the fix works]

## Changes

- `file.ts`: [What was changed and why]
- `other.ts`: [What was changed and why]

## Type of Change

- [x] 🐛 Bug fix

## Testing

### Reproduction Steps (Before)
1. Step 1
2. Step 2
3. Observe bug

### Verification Steps (After)
1. Step 1
2. Step 2
3. Bug is fixed

### Tests Added
- [x] Unit test for edge case
- [x] Regression test

## Checklist

- [x] Bug is verified fixed
- [x] No new bugs introduced
- [x] Tests added to prevent regression

## Related Issues

Fixes #789

---
🤖 Generated with [Claude Code](https://claude.com/code)
```

### PR de Refactoring

```markdown
## Summary

Refactor [component/module] to improve [maintainability/performance/readability].

## Motivation

[Why this refactoring is needed]

## Changes

### Before
```typescript
// Old approach
```

### After
```typescript
// New approach
```

## Type of Change

- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 💥 Breaking change
- [x] ♻️ Refactoring

## Impact

- **Performance**: [Improved/No change/Slightly worse]
- **Bundle size**: [Reduced by X KB/No change]
- **API**: [No changes to public API]

## Testing

- [x] All existing tests pass
- [x] No behavior changes

## Checklist

- [x] No functional changes
- [x] All tests pass
- [x] Code is cleaner/more maintainable

---
🤖 Generated with [Claude Code](https://claude.com/code)
```

## Opciones de PR

```bash
# PR normal
gh pr create --title "title" --body "body"

# PR como draft
gh pr create --draft --title "WIP: title" --body "body"

# PR a branch específico
gh pr create --base develop --title "title" --body "body"

# PR con reviewers
gh pr create --title "title" --body "body" --reviewer user1,user2

# PR con labels
gh pr create --title "title" --body "body" --label "feature,priority:high"

# PR con milestone
gh pr create --title "title" --body "body" --milestone "v2.0"
```

## Output Esperado

```
🔀 PULL REQUEST CREATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Branch Analysis:
  Current: feature/add-password-reset
  Base: main
  Commits: 5
  Files changed: 8

Commits Included:
  abc1234 feat(auth): add forgot password form
  def5678 feat(auth): implement email service
  ghi9012 feat(auth): add reset password page
  jkl3456 test(auth): add password reset tests
  mno7890 docs(auth): update authentication docs

Files Changed:
  src/components/ForgotPassword.tsx (new)
  src/pages/reset-password.tsx (new)
  src/services/auth.service.ts (modified)
  src/services/email.service.ts (new)
  src/types/auth.types.ts (modified)
  tests/auth.test.ts (modified)
  docs/authentication.md (modified)
  package.json (modified)

PR Details:
  Title: feat(auth): add password reset functionality
  Type: ✨ New feature
  Breaking: No

Creating PR...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Pull Request created successfully!

🔗 https://github.com/org/repo/pull/123

Next Steps:
  1. Review the PR description
  2. Request reviewers if needed
  3. Monitor CI/CD checks
  4. Address review comments
```

## Comandos Útiles Post-PR

```bash
# Ver estado del PR
gh pr status

# Ver checks del PR
gh pr checks

# Agregar reviewers
gh pr edit --add-reviewer user1

# Ver comentarios
gh pr view --comments

# Merge cuando esté listo
gh pr merge --squash
```
