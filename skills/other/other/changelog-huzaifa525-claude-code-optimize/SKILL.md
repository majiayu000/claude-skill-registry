---
name: changelog
description: Use when the user wants a changelog, release notes, or asks what changed since the last release.
disable-model-invocation: true
allowed-tools: Bash, Read, Write
---

Generate a changelog from git history.

## Steps

1. **Find the last tag**
   ```
   git describe --tags --abbrev=0 2>/dev/null || echo "no-tags"
   ```

2. **Get commits since last tag**
   ```
   git log [last-tag]..HEAD --oneline --no-merges
   ```
   If no tags, get last 50 commits.

3. **Categorize commits by prefix:**

   | Category | Prefixes |
   |----------|---------|
   | Features | feat:, feature:, add: |
   | Bug Fixes | fix:, bugfix:, hotfix: |
   | Performance | perf: |
   | Refactoring | refactor: |
   | Documentation | docs:, doc: |
   | Testing | test:, tests: |
   | CI/CD | ci:, cd:, build: |
   | Chores | chore:, deps:, bump: |
   | Breaking Changes | any commit with BREAKING CHANGE in body |

   If commits don't use conventional prefixes, categorize by content.

4. **Generate CHANGELOG.md entry:**

   ```markdown
   ## [version] - YYYY-MM-DD

   ### Features
   - Description ([commit-hash])

   ### Bug Fixes
   - Description ([commit-hash])

   ### Performance
   - Description ([commit-hash])

   ### Breaking Changes
   - Description ([commit-hash])
   ```

5. **If CHANGELOG.md exists**, prepend the new entry at the top (after the title).
   If it doesn't exist, create it.

6. **Show the generated changelog** to the user.

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
