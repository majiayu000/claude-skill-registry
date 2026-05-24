---
name: pr-description-generator
description: Auto-activates when user mentions creating pull request, PR description, or merge request. Generates comprehensive PR descriptions from git diff and commit history.
category: workflow
---

# Pull Request Description Generator

Generates comprehensive, professional PR descriptions that make reviews faster and easier.

## When This Activates

- User says: "create PR", "write PR description", "open pull request"
- User runs: `gh pr create`
- User asks: "what should my PR description say?"

## PR Description Template

```markdown
## 🎯 What

[One sentence summary of changes]

## 🔨 Changes

- [Bullet points of key changes]
- [Focus on user-visible changes]
- [Mention refactoring/technical changes]

## 🤔 Why

[Explanation of why this change is needed]
[Link to issue/ticket if applicable]

## 🧪 Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases verified

**Testing steps:**
1. [How to test this locally]
2. [What to look for]
3. [Edge cases to verify]

## 📸 Screenshots/Videos

[If UI changes: add before/after screenshots]
[If workflow changes: add demo GIF/video]

## ⚠️ Breaking Changes

[If breaking: list what breaks and migration guide]
[If not breaking: remove this section]

## 📝 Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Changelog updated (if applicable)
- [ ] No hardcoded secrets
- [ ] Follows code style guidelines
- [ ] Reviewed own code first

## 🔗 Related

Closes #[issue number]
Related: #[related PR/issue]
Depends on: #[dependency PR]
```

## Process

1. **Gather context:**
   ```bash
   git log origin/main..HEAD --oneline
   git diff origin/main..HEAD --stat
   ```

2. **Analyze changes:**
   - What's the main feature/fix?
   - What files were touched?
   - Any breaking changes?
   - UI changes?

3. **Generate description:**
   - Clear "What" summary
   - Detailed "Changes" list
   - Explain "Why" this matters
   - Testing instructions
   - Screenshots if UI changed

4. **Present to user** for review/edit

## Examples

### Feature PR

```markdown
## 🎯 What

Add user authentication with JWT tokens

## 🔨 Changes

- Implemented JWT-based authentication system
- Added login and register endpoints
- Created auth middleware for protected routes
- Added password hashing with bcrypt
- Implemented token refresh mechanism

## 🤔 Why

Users need secure authentication to access protected features.
Current system uses session cookies which don't work well with our mobile app.

Closes #123

## 🧪 Testing

- [x] Unit tests pass (18 new tests added)
- [x] Integration tests pass
- [x] Manual testing completed
- [x] Tested token expiration and refresh

**Testing steps:**
1. Run `npm test`
2. Start server: `npm run dev`
3. Register new user: POST `/api/auth/register`
4. Login: POST `/api/auth/login`
5. Access protected route with token in Authorization header
6. Verify token expires after 15 minutes

## 📸 Screenshots

![Login flow](./screenshots/login-flow.gif)

## 📝 Checklist

- [x] Tests added (18 new tests)
- [x] Documentation updated (API.md)
- [x] Changelog updated
- [x] No hardcoded secrets (all in .env.example)
- [x] Follows ESLint rules
- [x] Reviewed own code

## 🔗 Related

Closes #123
Depends on: #120 (database schema)
```

### Bug Fix PR

```markdown
## 🎯 What

Fix null pointer exception in user profile page

## 🔨 Changes

- Added null check for user.avatar before rendering
- Added default avatar fallback
- Updated ProfileCard component tests

## 🤔 Why

Users without avatars were seeing blank profile pages.
This happened when users registered via OAuth (no avatar uploaded).

Fixes #234

## 🧪 Testing

- [x] Unit tests pass (2 new tests)
- [x] Manual testing: Created user without avatar, profile renders correctly

**Test cases:**
1. User with avatar → renders avatar ✅
2. User without avatar → renders default avatar ✅
3. User with null avatar property → renders default avatar ✅

## 📝 Checklist

- [x] Tests added for null case
- [x] No breaking changes
- [x] Verified in staging environment
```

## Smart Features

### Auto-Detect Breaking Changes

```javascript
// If code diff shows:
// - Removed exports
// - Changed function signatures
// - Renamed database columns
// → Automatically mark as BREAKING CHANGE
```

### Auto-Generate Testing Steps

```javascript
// If PR adds new API endpoint:
// → Auto-generate curl commands for testing

// If PR adds UI component:
// → Auto-generate component usage example
```

### Auto-Link Issues

```javascript
// Scan commit messages for: "fixes #123", "closes #456"
// → Automatically add to PR description footer
```

## Rules

✅ **DO:**
- Write for reviewers (assume they're busy)
- Include "why" not just "what"
- Add testing instructions
- Show UI changes with screenshots
- List breaking changes prominently

❌ **DON'T:**
- Be vague ("fixed some bugs")
- Assume reviewers know context
- Skip testing section
- Forget to link related issues
- Submit without self-review

## Automation

```bash
# Generate and create PR in one command
gh pr create --title "feat: add authentication" --body "$(droid generate-pr-description)"
```

**Always show description to user before creating PR.**
