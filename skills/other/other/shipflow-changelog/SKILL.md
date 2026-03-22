---
name: shipflow-changelog
description: Auto-generate CHANGELOG.md from git history — Keep a Changelog format, grouped and categorized
argument-hint: [since-tag | since-date | "all"] (omit for since last entry)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -50 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Existing CHANGELOG: !`head -30 CHANGELOG.md 2>/dev/null || echo "no CHANGELOG.md"`
- Git tags: !`git tag --sort=-v:refname 2>/dev/null | head -10 || echo "no tags"`
- Recent commits: !`git log --oneline -20 2>/dev/null || echo "no git"`
- Current branch: !`git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"`

## Mode detection

- **`$ARGUMENTS` is a tag** (e.g., `v1.0.0`) → Generate changelog since that tag.
- **`$ARGUMENTS` is a date** (e.g., `2026-01-15`) → Generate changelog since that date.
- **`$ARGUMENTS` is "all"** → Generate changelog from entire git history.
- **`$ARGUMENTS` is empty** → Generate changelog since last CHANGELOG.md entry date (or last tag, or last 2 weeks if neither exists).

---

## Flow

### Step 1: Determine scope

Based on the argument and context:
- If a tag is given: `git log [tag]..HEAD --format="%H|%s|%b|%an|%aI" --reverse`
- If a date is given: `git log --since="[date]" --format="%H|%s|%b|%an|%aI" --reverse`
- If "all": `git log --format="%H|%s|%b|%an|%aI" --reverse`
- If empty: detect last entry date from CHANGELOG.md, or use last tag, or default to `--since="2 weeks ago"`

### Step 2: Read git log

Read the full git log with complete messages (not just oneline):

```bash
git log [scope] --format="--- COMMIT ---%nHash: %H%nDate: %aI%nAuthor: %an%nSubject: %s%n%b" --reverse
```

### Step 3: Categorize commits

Group each commit into [Keep a Changelog](https://keepachangelog.com/) categories:

| Category | Commit patterns |
|----------|----------------|
| **Added** | `feat:`, `add:`, new files, new features |
| **Changed** | `refactor:`, `update:`, `improve:`, behavior changes |
| **Fixed** | `fix:`, `bug:`, `hotfix:`, corrections |
| **Security** | `security:`, CVE fixes, auth changes |
| **Deprecated** | `deprecate:`, removal warnings |
| **Removed** | `remove:`, `delete:`, feature removal |

### Step 4: Group related commits

Multiple commits about the same feature or fix should be consolidated into a single changelog entry:
- "Fix typo in login" + "Fix another typo in login" → single entry
- "Add user profile page" + "Add avatar to profile" + "Add bio to profile" → single "Add user profile page with avatar and bio"

### Step 5: Generate changelog entry

Format as Keep a Changelog:

```markdown
## [Unreleased] — [date]

### Added
- User profile page with avatar and bio editing
- Dark mode toggle in settings

### Changed
- Improved navigation menu responsiveness
- Updated homepage hero section copy

### Fixed
- Login redirect loop on expired sessions
- Missing alt text on product images

### Security
- Upgrade dependencies to patch CVE-2026-XXXX
```

### Step 6: Write CHANGELOG.md

- If CHANGELOG.md exists: **prepend** the new entry after the header (never delete existing entries).
- If CHANGELOG.md doesn't exist: create it with the standard header:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased] — [date]
...
```

### Step 7: Optional tag

Use **AskUserQuestion**:
- Question: "Create a git tag for this release?"
- Options:
  - **No tag** — "Just update the changelog" (Recommended)
  - **Tag as patch** — "e.g., v1.0.1"
  - **Tag as minor** — "e.g., v1.1.0"
  - **Tag as major** — "e.g., v2.0.0"

If tagging: replace `[Unreleased]` with the version number and create the tag.

---

## Important

- **Keep a Changelog** format strictly. No other format.
- Group related commits into single human-readable entries. Don't list every commit individually.
- Skip internal commits: CI config changes, formatting-only commits, merge commits, changelog updates.
- French language for French projects (GoCharbon, claiire, plaisirsurprise FR content).
- Never delete existing changelog entries — only prepend new ones.
- Each entry should be understandable by a user, not a developer. "Fix login issue" > "Fix auth token refresh in useSession hook".
- If there are no meaningful changes to report, say so instead of creating an empty entry.
- **Accents français obligatoires.** Lors de toute création ou modification de contenu en français, vérifier systématiquement que TOUS les accents sont présents et corrects (é, è, ê, à, â, ù, û, ô, î, ï, ç, œ, æ). Les accents manquants sont une faute d'orthographe. Relire chaque texte produit pour s'assurer qu'aucun accent n'a été oublié — c'est une erreur très fréquente à corriger impérativement.
