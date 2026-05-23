---
name: writing-app-release-notes
description: Use when being asked to write release notes for an app
---

# Writing App Release Notes

Write customer-facing release notes in Carlo's voice for app releases.

## Trigger

Explicit request: "Write release notes for version X" or similar.

## Workflow

### 1. Discovery

**Find the changelog file:**

- Search for `WhatsNew-Production.md` in the project
- If not found, ask Carlo for the location

**Check project metadata in `CLAUDE.md`:**

- Platform situation: single-platform or multi-platform (iOS/macOS)
- Distribution channel: App Store or Keygen

If either is missing: ask Carlo, then update `CLAUDE.md` with the answer.

**Get version info from git:**

```bash
git tag --sort=-v:refname          # Find previous version
git log <prev>..<new> --oneline    # Get commits between tags
```

### 2. Analyze Commits

**Filter by commit type:**

- **Include:** `feat`, `fix`, `perf`
- **Exclude:** `chore`, `build`, `ci`, `refactor`, `style`, `test`, `docs`
- **If unsure:** Ask Carlo

**Gather context:**

- Extract ticket IDs from commits (ZCO-XXXX pattern)
- Look up Linear tickets for background
- Look up Beans for additional context
- Note any user names mentioned (for attribution)

This context informs your understanding but doesn't all go into the notes.

### 3. Interactive Checks

**Ask Carlo about (as needed):**

1. **Ambiguous commits** - "Is this customer-facing?"
2. **User attribution** - "I found these names in tickets/commits: [list]. Anyone to add or remove?"
3. **Removals/deprecations** - If breaking changes detected: "How should I message these?"
4. **Platform** (multi-platform apps only) - "Is this release for macOS, iOS, or both?"

### 4. Write the Entry

**Heading format:**

- Multi-platform, specific: `## Version 2026.1.2 (macOS), 2026-03-27`
- Multi-platform, both: `## Version 2026.2.3 (iOS/macOS), 2026-04-24`
- Single platform: `## Version 2026.1.2, 2026-03-27`

**Sections (in order, include only if applicable):**

1. **New & Exciting** - New features (`feat` commits)
2. **No Longer Broken** - Bug fixes (`fix` commits)
3. **Changes** - Modifications, performance improvements
4. **Removals** - Breaking changes, removed features (confirm messaging with Carlo first)

**Each item:**

- Bullet point with clear description
- Ticket IDs AND Beans in trailing HTML comment: `<!-- ZCO-1234, beans-abcd -->`
- Doc links as placeholders: `[Feature Name](TODO: link)`
- User thanks where applicable (confirmed with Carlo)

**Special sections (suggest when relevant):**

- Breaking changes: Offer a "Things to do for you" migration section
- App Store apps: Include promo blurb at the end

**Placement:** Prepend new entry to top of `WhatsNew-Production.md`

### 5. After Writing

1. List any `(TODO: link)` placeholders that need filling
2. **Do NOT commit** - Leave for Carlo's review

## Tone & Style

- **Voice:** First person ("I", "me", "Carlo, the author")
- **Sections:** "No Longer Broken" not "Bug Fixes"
- **Emoji:** Almost none (occasional for major releases)
- **Humor:** Occasional ridiculous puns welcome
- **Language:** Clean and inclusive
- **Attribution:** Thank users who reported issues by name

## Example Entry

```markdown
## Version 2026.1.2 (iOS/macOS), 2026-03-27

### New & Exciting

- Added dark mode support. Your eyes called; they send their thanks. <!-- ZCO-1234, beans-abc1 -->

### No Longer Broken

- Fixed a crash when opening large files. Thanks for the report, Rüdiger! <!-- ZCO-1235 -->
- The settings screen no longer forgets your preferences after a reboot. <!-- ZCO-1236, beans-def2 -->

### Changes

- Improved startup performance by about 30%. <!-- ZCO-1237 -->

---

**Did you know** I also make other macOS apps? [Check them out!](https://actions.work/?ref=app-whatsnew)
```
