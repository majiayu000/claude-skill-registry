---
name: repo-changelog
description: Generates end-user friendly release notes and changelogs by analyzing git diffs, consolidating changes, and formatting for Slack and documentation
---

# Release Notes & Changelog Generator

This skill analyzes git repositories to generate **end-user friendly** release notes and changelogs. It reads actual code diffs (not just commit messages), understands what changed, consolidates related changes, and produces clean markdown suitable for Slack updates and program documentation.

## Key Differentiators

- **Diff-Based Analysis**: Reads actual code changes, not just commit messages
- **End-User Focus**: No technical jargon, functions, or variables in output
- **Smart Consolidation**: If something changed back and forth with no net result, it's not mentioned
- **Final State Only**: Shows what the end result is, not intermediate steps
- **Breaking Change Detection**: Automatically flags breaking changes from commits and diffs
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Multi-Remote Support**: GitHub, Bitbucket, and local git repositories

## Capabilities

- **Tag-to-Tag Analysis**: Generate notes between any two release tags (e.g., v1.0.0 to v1.1.0)
- **Since-Last-Tag**: Automatically detect last tag and show changes since then
- **Recent Commits**: Analyze last N commits for quick updates
- **Full Diff Reading**: Understand actual code changes, not vague commit messages
- **Change Consolidation**: Merge related changes, eliminate flip-flop changes
- **Category Bucketing**: Organize into Features, Enhancements, Bug Fixes, Changes, Breaking Changes, Others
- **Slack-Ready Output**: Formatted markdown with bullet points and optional footnotes
- **Footnotes Support**: Add setup notes or important info without exposing secrets

## Output Categories

Changes are organized into these buckets:

| Category | Description | When Used |
|----------|-------------|-----------|
| **New Features** | Brand new functionality | New screens, new buttons, new capabilities |
| **Enhancements** | Improvements to existing features | Faster, better, more options |
| **Bug Fixes** | Issues that were resolved | Things that weren't working now work |
| **Changes** | Modifications to behavior | Something works differently now |
| **Breaking Changes** | Changes requiring user action | Must update settings, data migration needed |
| **Others** | Miscellaneous updates | Documentation, internal improvements users might notice |

## Input Requirements

The skill needs:

1. **Repository Path** (optional): Defaults to current directory
2. **Range Specification** (one of):
   - `from_tag` and `to_tag`: Compare between two tags
   - `since_tag`: Everything since a specific tag to HEAD
   - `last_n_commits`: Analyze recent N commits (default: 50)
3. **Remote Type** (optional): `github`, `bitbucket`, or `local` (auto-detected)

**Input Formats Accepted**:

Natural language:
- "Generate release notes from v1.0.0 to v1.1.0"
- "What changed since the last release?"
- "Show me what's new in the last 30 commits"

Structured JSON:
```json
{
  "repo_path": "C:\\Projects\\MyApp",
  "from_tag": "v1.0.0",
  "to_tag": "v1.1.0"
}
```

## Output Format

Markdown file with this structure:

```markdown
# Release Notes - v1.1.0

## New Features
- Added dark mode toggle in settings
- New export to PDF option in reports

## Enhancements
- Improved loading speed when opening large files
- Search now finds partial matches

## Bug Fixes
- Fixed issue where login would fail on slow connections
- Resolved crash when uploading files over 10MB

## Changes
- Settings menu has been reorganized for clarity
- Default file format changed from CSV to Excel

## Breaking Changes
- Database format updated - run migration tool before upgrading

---

**Notes:**
- Dark mode requires display driver update on Windows 7
- PDF export needs Adobe Reader installed
```

## How the Analysis Works

### Step 1: Gather Commits
Collects all commits in the specified range from the git repository.

### Step 2: Read Full Diffs
For each commit, reads the actual code changes (additions, deletions, modifications).

### Step 3: Interpret Changes
Translates technical changes into plain English descriptions:
- `+ showWelcomeMessage = true` → "Welcome message now displays when app starts"
- Deleted login retry logic → "Removed automatic login retry"

### Step 4: Consolidate Changes
Groups related changes and eliminates noise:
- If a feature was added then removed, it's not mentioned
- If a value changed multiple times, only the final state matters
- Related commits are merged into single descriptions

### Step 5: Categorize
Assigns each change to the appropriate bucket based on:
- Commit message keywords (feat, fix, enhancement, etc.)
- Type of code change (new files = feature, deleted code = removal)
- Breaking change indicators

### Step 6: Format Output
Generates clean markdown with:
- Clear category headings
- Brief bullet points
- Optional footnotes for important notes
- No technical details, secrets, or jargon

## Scripts

- `git_analyzer.py`: Cross-platform git operations (Windows/macOS/Linux compatible)
- `diff_parser.py`: Reads and interprets code diffs in plain English
- `change_consolidator.py`: Merges related changes, detects net-zero changes
- `changelog_formatter.py`: Generates Slack-ready markdown output
- `breaking_change_detector.py`: Identifies breaking changes from commits and diffs

## Best Practices

1. **Use Meaningful Tags**: Tag releases with semantic versions (v1.0.0, v1.1.0)
2. **Run Before Release**: Generate notes as part of your release process
3. **Review Output**: AI interpretation is good but human review ensures accuracy
4. **Add Footnotes**: Use the notes section for setup instructions or warnings
5. **Keep It Brief**: Bullet points should be one line each
6. **No Secrets**: Never include passwords, API keys, or internal URLs in notes

## Limitations

- **Requires Git Repository**: Only works with valid git repos
- **Tag Must Exist**: Specified tags must exist in the repository
- **Diff Size Limits**: Very large diffs (1000+ files) may be summarized
- **Language Detection**: Best results with common programming languages
- **Interpretation Accuracy**: Complex changes may need human refinement
- **No Real-Time**: Analyzes existing commits, not live changes

## When to Use This Skill

**Perfect for:**
- Release announcements to support teams (Slack)
- Customer-facing changelog updates
- Sprint review summaries
- Version upgrade documentation
- Non-technical stakeholder updates

**Not Ideal for:**
- Technical developer documentation
- Detailed code review
- Security audit reports
- Debugging commit history
