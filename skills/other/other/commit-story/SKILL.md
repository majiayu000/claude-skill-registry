---
name: commit-story
description: |
  Reads git log between two points and generates human-readable changelogs or release
  notes. Groups commits by type, links to relevant files, and summarizes what changed
  and why. Output as a narrative changelog or user-facing release notes.
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Glob
  - Write
---

# Commit Story

Turn a pile of commits into something a human would actually read.

---

## Why This Exists

Git logs are written for machines. Each commit message is a fragment: "fix: handle null user," "refactor: extract payment service," "feat: add export button." Reading 50 of these tells you nothing about what actually happened to the product. Someone still has to write the changelog, the release notes, the "what's new" section. Usually nobody does, and the knowledge stays buried in the log.

This skill reads the commits, groups them, reads the changed files for context, and writes a document that tells the story.

---

## Commands

### `/commit-story`

Generate from the most recent tag to HEAD. If no tags exist, use the last 50 commits.

### `/commit-story [from] [to]`

Generate from a specific range. Accepts tags, branches, commit hashes, or dates.

```
/commit-story v1.2.0 v1.3.0
/commit-story main feature/payments
/commit-story HEAD~20 HEAD
/commit-story 2026-01-01 2026-02-01
```

### `/commit-story --format changelog`

Output in `CHANGELOG.md` format (Keep a Changelog convention).

### `/commit-story --format release-notes`

Output in user-facing release notes format. No file paths, no technical jargon. Written for end users who do not read code.

---

## How It Works

### Step 1: Get the commit range

```bash
# Find the last tag
git describe --tags --abbrev=0 2>/dev/null

# Get log with stats
git log [from]..[to] --pretty=format:"%H|%h|%an|%ad|%s" --date=short --stat
```

If `[from]` is a date, convert:
```bash
git log --after="2026-01-01" --before="2026-02-01" --pretty=format:"%H|%h|%an|%ad|%s" --date=short --stat
```

### Step 2: Parse and categorize commits

Group by conventional commit prefix:

| Prefix | Category | Label in output |
|---|---|---|
| `feat:` | Features | New |
| `fix:` | Bug Fixes | Fixed |
| `refactor:` | Refactoring | Improved |
| `perf:` | Performance | Faster |
| `docs:` | Documentation | Docs |
| `test:` | Tests | Tests |
| `chore:` | Maintenance | Maintenance |
| `style:` | Formatting | Style |
| `ci:` | CI/CD | CI |
| `build:` | Build | Build |
| (no prefix) | Uncategorized | Other |

If commits don't follow conventional format, fall back to keyword detection:
- Contains "add" or "new" or "create" -> Features
- Contains "fix" or "bug" or "patch" or "resolve" -> Bug Fixes
- Contains "refactor" or "clean" or "restructure" -> Refactoring
- Everything else -> Other

### Step 3: Enrich with file context

For the most significant commits (features and fixes), read the diff to understand what actually changed:

```bash
git show [hash] --stat
git show [hash] -- [key files]  # only for important commits
```

Limit this to the top 10 commits by lines changed. Reading every diff in a 200-commit range would blow the context budget.

### Step 4: Identify the narrative

Look for patterns in the commits:
- Are most commits touching the same directory? That is the focus area.
- Is there a sequence of commits building toward one feature? Group them as a story.
- Are there many small fixes? Summarize as "stability improvements."
- Did a refactor precede a feature? Mention the groundwork.

### Step 5: Write the document

Choose format based on `--format` flag. Default is changelog.

---

## Output Formats

### Changelog Format (default)

Follows [Keep a Changelog](https://keepachangelog.com/) conventions.

```markdown
# Changelog

## [v1.3.0] - 2026-02-10

### New
- Export functionality for transaction reports. Users can now download CSV and PDF
  exports from the reports page. (`src/features/export/`)
- Email notifications for failed payments. Triggers after 3 consecutive failures.
  (`src/services/notifications/`)

### Fixed
- Dashboard loading spinner stuck when API returned empty dataset.
  Previously showed infinite loading; now shows empty state. (a3f2b1c)
- Currency formatting inconsistency between KRW and USD display.
  Was showing decimal places for KRW, which doesn't use them. (b7d4e2f)

### Improved
- Payment processing service extracted from monolithic controller into
  dedicated service layer. No behavior change. (`src/services/payment/`)
- Database queries for user list now use cursor pagination instead of
  offset. Reduces query time from ~800ms to ~50ms on large datasets.

### Maintenance
- Updated React from 18.2 to 18.3
- Removed unused `moment` dependency (replaced by `date-fns` in v1.2.0)
- Added TypeScript strict mode to 12 files

---

**Commits**: 47 | **Contributors**: 3 | **Files changed**: 89
**Period**: 2026-01-15 to 2026-02-10
```

### Release Notes Format

Written for end users. No commit hashes, no file paths, no internal architecture.

```markdown
# What's New in v1.3.0

February 10, 2026

## Export Your Reports

You can now download your transaction reports as CSV or PDF files.
Go to Reports, pick a date range, and click the export button in the top right.

## Payment Failure Alerts

If a scheduled payment fails three times in a row, you will get an email notification.
You can manage notification preferences in Settings > Notifications.

## Bug Fixes

- The dashboard no longer shows an endless loading spinner when there is no data
  for the selected period. It now shows an empty state with a message.
- Currency display for KRW transactions no longer shows decimal places.

## Performance

- The customer list page loads noticeably faster for accounts with 10,000+ customers.
```

---

## Output Location

Save to: `docs/commit-story-[date].md`

If the `docs/` directory does not exist, create it. Tell the user where the file was saved.

For changelog format, if a `CHANGELOG.md` already exists in the project root, ask the user whether to prepend to it or create a separate file.

---

## Handling Edge Cases

If there are no conventional commit prefixes at all:
- Do not force-fit categories. Use "Changes" as a single group.
- Mention that adopting conventional commits would improve future changelogs.

If there are merge commits mixed in:
- Skip merge commits (`Merge branch 'x' into 'y'`) unless they carry useful information.
- Use `--no-merges` flag by default.

If the range is very large (200+ commits):
- Summarize instead of listing every commit.
- Group small fixes as "N bug fixes including..." and list only the top 5.

If the range is very small (under 5 commits):
- List each one with full detail. No need to group.

---

## Important Constraints

- Read actual diffs for feature and fix commits. Commit messages often lie or understate. A commit that says "fix: update handler" might have changed 15 files and rewritten the auth logic.
- Keep changelog entries to one or two sentences each. The goal is scanning, not reading.
- For release notes, test every sentence against the question: "Would a non-developer understand this?" If no, rewrite.
- Never fabricate information. If a commit message is unclear and the diff is too large to read, say "Various internal improvements" rather than guessing.
- Include the commit hash (short form) for changelog entries so developers can look them up. Omit hashes from release notes.
- Respect the user's language. If commit messages are in Korean, write the output in Korean. If mixed, default to the project's primary language.
