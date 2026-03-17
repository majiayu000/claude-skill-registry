---
name: release-notes
description: Analyzes git commit and PR history to generate structured release notes (RELEASE_NOTES.md). Automatically categorizes changes, identifies contributors, and produces a polished release document through a brief confirmation interview.
---

# Release Notes

## Overview
This skill generates structured release notes by analyzing git history. It determines the version range from git tags, categorizes commits by type, identifies contributors, and produces a comprehensive `RELEASE_NOTES.md`. A brief interview confirms version number, highlights, and breaking changes before final output.

## Instructions

### Phase 1: Discovery & Analysis
1. Determine the version range to document:
   - Run `git tag --sort=-version:refname` to find existing tags.
   - If tags exist, use the range from the most recent tag to HEAD.
   - If no tags exist, use `AskUserQuestion` to ask the user for the range (e.g., a specific commit SHA, "last 20 commits", or "all history").
   - The user may also specify a custom range as an argument (e.g., `/release-notes v1.0.0..v1.1.0`).

2. Collect commit history for the determined range:
   - Run `git log <range> --pretty=format:"%H|%an|%ae|%s|%b" --no-merges` to get commit details.
   - Run `git log <range> --pretty=format:"%H|%an|%ae|%s|%b" --merges` to identify PR merges.
   - Run `git shortlog -sne <range>` to gather contributor information.

3. Categorize each commit based on its message prefix or content:
   - **Features**: Messages starting with `feat`, `add`, `new`, or containing "added", "implement"
   - **Bug Fixes**: Messages starting with `fix`, `bugfix`, or containing "fixed", "resolve"
   - **Breaking Changes**: Messages containing `BREAKING CHANGE`, `BREAKING:`, or using `!` after type (e.g., `feat!:`)
   - **Improvements**: Messages starting with `refactor`, `improve`, `update`, `perf`, `enhance`
   - **Documentation**: Messages starting with `docs`, `doc`
   - **Other**: Messages starting with `chore`, `ci`, `build`, `test`, `style`, or anything else

4. For each category, extract a clean one-line summary from the commit message subject line. Strip conventional commit prefixes (e.g., `feat: add login` becomes `Add login`).

5. Identify potential highlights by looking for:
   - Commits with long bodies (detailed explanations suggest significance)
   - Breaking changes
   - Features with multiple related commits
   - Merge commits from PRs (often represent larger changes)

### Phase 2: Brief Interview
6. Present the analysis summary to the user via `AskUserQuestion` and confirm:

   **Round 1 - Version & Highlights:**
   - "What version number should this release be?" (suggest based on changes: major if breaking, minor if features, patch if fixes only)
   - "Here are the auto-detected highlights: [list]. Would you like to adjust, add, or remove any?" (provide options: "Looks good", "I'll adjust", with space for custom input)

   **Round 2 - Breaking Changes & Extras (only if applicable):**
   - If breaking changes were detected: "The following breaking changes were found: [list]. Do any of these need a migration guide?"
   - "Any additional notes to include in the release? (e.g., deprecation notices, known issues, acknowledgments)"

### Phase 3: Output
7. Read the template file at `skills/release-notes/output-template.md` and use it as the structure for generating `RELEASE_NOTES.md` in the project root.
   - Replace `vX.Y.Z` with the confirmed version number.
   - Replace `YYYY-MM-DD` with today's date.
   - Fill each section with the categorized commit data from Phase 1 and interview answers from Phase 2.
8. Omit sections that have no entries (e.g., if there are no breaking changes, skip that section entirely).
9. Write the file and inform the user of the output location.

## Examples

### Input
```
/release-notes
```
(In a project with git tag `v1.2.0` and 15 commits since that tag)

### Phase 1 Output (internal analysis)
```
Range: v1.2.0..HEAD (15 commits)

Categorized:
- Features (3): Add OAuth login, Add user avatar upload, Add dark mode toggle
- Bug Fixes (5): Fix session timeout, Fix mobile nav overlap, ...
- Improvements (4): Refactor auth middleware, Improve query performance, ...
- Other (3): Update CI config, Add unit tests for auth, ...

Contributors: alice (7), bob (5), charlie (3)
Suggested version: v1.3.0 (minor - new features, no breaking changes)
```

### Interview Round 1
```
Questions:
1. "Based on the changes (3 new features, no breaking changes), the suggested
    version is v1.3.0. What version should this release be?"
    Options: ["v1.3.0 (Recommended)", "v1.2.1 (patch)", "v2.0.0 (major)"]

2. "Auto-detected highlights: OAuth login support, dark mode toggle, and
    significant auth middleware refactoring. Would you like to adjust these?"
    Options: ["Looks good", "I'll provide my own"]
```

### Output
```markdown
# Release Notes - v1.3.0

> Released: 2025-01-15

## Highlights
- OAuth login support enabling Google and GitHub authentication
- Dark mode toggle with system preference detection
- Significant performance improvements in authentication flow

## Features
- Add OAuth login with Google and GitHub providers
- Add user avatar upload with image cropping
- Add dark mode toggle with system preference detection

## Bug Fixes
- Fix session timeout not redirecting to login page
- Fix mobile navigation menu overlapping content
- Fix password reset email not sending in production
- Fix race condition in concurrent API requests
- Fix incorrect timezone display in user profile

## Improvements
- Refactor auth middleware for better extensibility
- Improve database query performance for user listings
- Update error messages to be more descriptive
- Enhance logging format for production debugging

## Contributors
- @alice (7 commits)
- @bob (5 commits)
- @charlie (3 commits)
```

## Guidelines
- Commit messages are the primary data source. If they are poor quality (e.g., "fix", "wip", "update"), do your best to infer meaning from the diff summary or group them under "Other".
- Never fabricate changes. Every item in the release notes must correspond to an actual commit.
- Keep descriptions concise but informative. Transform terse commit messages into readable sentences where possible (e.g., `fix: nav overlap on mobile` becomes "Fix mobile navigation menu overlapping content").
- If the project uses GitHub PRs, prefer PR titles over individual commit messages when available, as they tend to be more descriptive.
- The interview should be brief (1-2 rounds maximum). The value is in automation, not interrogation.
- If the user passes a file path argument, write the output to that path instead of the project root.
- Respect existing `RELEASE_NOTES.md` or `CHANGELOG.md` files. If one exists, ask whether to append, prepend, or create a new file.
- Use the contributor's git name as-is. Don't attempt to resolve GitHub usernames unless the information is available in the commit metadata.
- Date in the release notes should be the date of generation (today), not the date of the last commit.
