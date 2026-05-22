---
name: release-notes-writer
description: Automatically generate user-facing release notes from git commits, pull requests, changelogs, and code changes. Use when preparing software releases, creating version announcements, documenting what changed between versions, or communicating updates to users. Analyzes commit messages, PR descriptions, and code diffs to produce categorized markdown release notes organized by New Features, Improvements, Bug Fixes, and Breaking Changes. Focuses on user-visible changes while filtering out internal/technical details. Triggers when users ask to generate release notes, create changelog, write version announcement, or summarize changes for a release.
---

# Release Notes Writer

## Overview

Generate polished, user-facing release notes from git history, pull requests, and code changes, automatically categorizing and summarizing changes in a clear, accessible format.

## Workflow

### 1. Gather Release Information

Collect the scope and sources for the release notes:

**Define the release scope:**
- What version is being released? (e.g., v2.1.0)
- What's the version range? (e.g., v2.0.0 to v2.1.0)
- Which commits/PRs should be included?
- Is this a major, minor, or patch release?

**Quick commands to get started:**
```bash
# Get commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Get commits between two tags
git log v2.0.0..v2.1.0 --oneline

# Get commits since specific date
git log --since="2024-01-01" --oneline

# List all tags
git tag -l

# Get merged PRs (if using GitHub)
gh pr list --state merged --limit 50
```

### 2. Extract Change Information

Gather details from available sources:

#### From Git Commits

```bash
# Get commit messages with details
git log v2.0.0..v2.1.0 --pretty=format:"%h - %s (%an)" --no-merges

# Get commits by author
git log v2.0.0..v2.1.0 --author="AuthorName" --oneline

# Get commit messages with full body
git log v2.0.0..v2.1.0 --format="%h %s%n%b%n"
```

**Parse commit message conventions:**
- `feat:` or `feature:` → New Feature
- `fix:` or `bugfix:` → Bug Fix
- `perf:` or `performance:` → Performance Improvement
- `docs:` or `doc:` → Documentation
- `refactor:` → Code Quality/Refactoring
- `test:` → Testing
- `chore:` → Internal/Maintenance
- `BREAKING:` or `!:` → Breaking Change

#### From Pull Requests

If using GitHub CLI:
```bash
# Get merged PRs
gh pr list --state merged --limit 100 --json number,title,body,labels,mergedAt

# Get PR details
gh pr view <PR-NUMBER>
```

**Extract from PR:**
- Title (often more user-friendly than commit message)
- Description (may contain user-facing summary)
- Labels (feature, bug, breaking-change, etc.)
- Linked issues

#### From Changelog Files

Check for existing changelog entries:
```bash
# Look for changelog files
find . -name "CHANGELOG.md" -o -name "HISTORY.md" -o -name "RELEASES.md"

# Check for unreleased section
grep -A 20 "Unreleased" CHANGELOG.md
```

#### From Code Diffs

Infer changes from code when commits lack detail:
```bash
# See what files changed
git diff --stat v2.0.0..v2.1.0

# See what functions/classes were added
git diff v2.0.0..v2.1.0 --unified=0 | grep "^+def\|^+class"

# See API changes
git diff v2.0.0..v2.1.0 -- "*.py" | grep -E "^[+-]def |^[+-]class "
```

### 3. Categorize Changes

Organize changes into standard categories:

#### Category: ✨ New Features

User-visible new capabilities:
- New API endpoints
- New UI components
- New configuration options
- New supported platforms
- New integrations

**Examples:**
- "Added dark mode support"
- "Introduced batch processing for large datasets"

#### Category: 🐛 Bug Fixes

Corrections to existing functionality:
- Fixed crashes or errors
- Corrected unexpected behavior
- Resolved data inconsistencies
- Fixed security vulnerabilities

#### Category: 🚀 Improvements

Enhancements to existing features:
- Performance optimizations
- Better error messages
- Improved UX/UI
- Enhanced reliability

#### Category: ⚠️ Breaking Changes

Changes requiring user action:
- API signature changes
- Removed features
- Changed default behavior
- Migration required

### 4. Filter for User-Facing Changes

**Include:**
- Changes users will notice
- Changes users need to know about
- Changes that affect how they use the product
- Security fixes (user-facing impact)

**Exclude or minimize:**
- Internal refactoring
- Test additions
- Build configuration changes
- Code style updates
- Developer tooling changes

**Transform technical to user-friendly:**
```
❌ "Refactored AuthService to use dependency injection"
✅ "Improved authentication reliability"

❌ "Updated webpack config for tree shaking"
✅ "Reduced bundle size by 20%"

❌ "Fixed race condition in concurrent processing"
✅ "Improved stability when processing multiple items simultaneously"
```

### 5. Generate Release Notes

Create formatted markdown output:

## Template Structure

```markdown
# Release Notes - Version X.Y.Z

**Release Date:** YYYY-MM-DD

## Summary

[1-3 sentence overview of the release]

---

## ✨ New Features

- **[Feature Title]**: [User-friendly description]
- **[Feature Title]**: [Description with benefit]

## 🚀 Improvements

- **[Improvement Title]**: [How this makes things better]
- **[Improvement Title]**: [Description]

## 🐛 Bug Fixes

- Fixed [issue description]
- Resolved [problem users were experiencing]

## ⚠️ Breaking Changes

- **[Breaking Change Title]**: [What changed and what users need to do]
  - **Migration:** [Step-by-step guidance]
  - **Before:** `code example`
  - **After:** `code example`

---

## 📊 Statistics

- X features added
- Y bugs fixed
- Z improvements made

## 🙏 Contributors

Thank you to all contributors who made this release possible:
- @username1
- @username2
```

### 6. Write User-Friendly Descriptions

Make each change clear and valuable:

**Use active, benefit-focused language:**
```
❌ "Added pagination to API"
✅ "You can now request data in pages, making it easier to work with large datasets"

❌ "Implemented OAuth2 authentication"
✅ "Sign in with your Google, GitHub, or Microsoft account"

❌ "Optimized database queries"
✅ "Reports now load 3x faster"
```

**Be specific about impact:**
```
❌ "Performance improvements"
✅ "Search results now appear in under 100ms, down from 2 seconds"

❌ "Better error handling"
✅ "Error messages now include specific suggestions for fixing the issue"
```

**Include code examples for API changes:**
```markdown
### Breaking Change: Authentication Method Updated

**Before:**
```python
client = APIClient(session_token="abc123")
```

**After:**
```python
client = APIClient(api_key="sk-abc123")
```

**Migration:** Update your initialization code to use the new `api_key` parameter.
```

### 7. Review and Polish

Before finalizing:

**Check completeness:**
- ✅ All significant changes included?
- ✅ Breaking changes clearly marked?
- ✅ User action items specified?
- ✅ Version number correct?

**Check clarity:**
- ✅ Descriptions are user-friendly, not technical?
- ✅ Benefits are clear?
- ✅ No internal jargon?
- ✅ Examples provided where helpful?

**Check organization:**
- ✅ Changes grouped logically?
- ✅ Most important changes listed first?
- ✅ Breaking changes prominently displayed?

## Example Output

```markdown
# Release Notes - Version 2.3.0

**Release Date:** February 15, 2026

## Summary

Version 2.3.0 brings enhanced search capabilities, performance improvements, and several bug fixes.

---

## ✨ New Features

- **Advanced Search Filters**: Filter search results by date, category, and status for more precise results
- **Keyboard Shortcuts**: Navigate the app faster with new keyboard shortcuts (press `?` to see all)
- **Export to Excel**: Export your data to Excel format in addition to CSV

## 🚀 Improvements

- **Faster Search**: Search results now appear instantly (improved from 2s to <100ms)
- **Better Mobile Experience**: Optimized interface for mobile devices
- **Smarter Autocomplete**: Autocomplete suggestions now learn from your previous searches

## 🐛 Bug Fixes

- Fixed issue where saving large files would occasionally fail
- Resolved problem with date picker not working in Safari
- Corrected timezone display for users in Asia-Pacific regions

---

## 📊 Statistics

- 3 new features
- 4 bugs fixed
- 3 improvements
- 47 commits
- 8 contributors

## 🙏 Contributors

Thank you to: @alice, @bob, @charlie, @diana, @eve, @frank, @grace, @henry
```

## Tips for Effective Release Notes

**Focus on user value:**
- What can users now do?
- What problems were solved?
- What's better/faster/easier?

**Be honest about breaking changes:**
- Mark them prominently
- Provide clear migration paths
- Explain why the change was made

**Use consistent language:**
- Present tense: "You can now..." not "You will be able to..."
- Active voice: "Added feature" not "Feature was added"
- User-centric: "You can" not "The system allows"

**Group related changes:**
- Don't list every commit separately
- Combine related fixes/features
- Summarize multiple small improvements

**Credit contributors:**
- Acknowledge community contributions
- Thank external contributors
- Build goodwill and engagement
