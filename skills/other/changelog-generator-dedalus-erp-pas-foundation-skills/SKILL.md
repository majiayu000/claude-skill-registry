---
name: changelog-generator
description: Automatically creates user-facing changelogs from git commits by analyzing commit history, categorizing changes, and transforming technical commits into clear, customer-friendly release notes. Turns hours of manual changelog writing into minutes of automated generation.
---

# Changelog Generator

This skill transforms technical git commits into polished, user-friendly changelogs that your customers and users will actually understand and appreciate.

## When to Use This Skill

- Preparing release notes for a new version
- Creating weekly or monthly product update summaries
- Documenting changes for customers
- Writing changelog entries for app store submissions
- Generating update notifications
- Creating internal release documentation
- Maintaining a public changelog/product updates page

## What This Skill Does

1. **Scans Git History**: Analyzes commits from a specific time period or between versions
2. **Categorizes Changes**: Groups commits into logical categories (features, improvements, bug fixes, breaking changes, security)
3. **Translates Technical → User-Friendly**: Converts developer commits into customer language
4. **Formats Professionally**: Creates clean, structured changelog entries
5. **Filters Noise**: Excludes internal commits (refactoring, tests, etc.)
6. **Follows Best Practices**: Applies changelog guidelines and your brand voice

## How to Use

### Basic Usage

From your project repository:

```
Create a changelog from commits since last release
```

```
Generate changelog for all commits from the past week
```

```
Create release notes for version 2.5.0
```

### With Specific Date Range

```
Create a changelog for all commits between March 1 and March 15
```

### With Custom Guidelines

```
Create a changelog for commits since v2.4.0, using my changelog 
guidelines from CHANGELOG_STYLE.md
```

## Instructions

When creating a changelog:

1. **Analyze Git History**
   - Use `git log` to retrieve commit messages for the specified time period
   - Default to commits since the last tag if no range specified
   - Look for commit conventions (Conventional Commits, semantic versioning tags)

2. **Categorize Commits**
   - **✨ New Features**: New capabilities or functionality
   - **🔧 Improvements**: Enhancements to existing features
   - **🐛 Bug Fixes**: Corrections to defects
   - **⚠️ Breaking Changes**: Changes that require user action
   - **🔒 Security**: Security-related fixes or improvements
   - **📚 Documentation**: Documentation updates (usually exclude from user-facing changelog)
   - **🧹 Internal**: Refactoring, tests, build changes (exclude from user-facing changelog)

3. **Transform Technical → User Language**
   - Focus on **what changed for the user**, not how it was implemented
   - Use active voice and present tense
   - Explain the benefit, not the implementation
   - Replace technical jargon with plain language
   
   **Examples:**
   - ❌ "Refactored authentication service to use JWT tokens"
   - ✅ "Faster, more secure login experience"
   
   - ❌ "Added Redis caching layer to API endpoints"
   - ✅ "Pages load 50% faster"
   
   - ❌ "Implemented debounce on search input component"
   - ✅ "Search now responds instantly as you type"

4. **Format the Changelog**
   - Use clear section headers with emojis for visual scanning
   - Start with most impactful changes (features, breaking changes)
   - Use bold for the feature name, then explain in plain language
   - Keep entries concise (1-2 sentences)
   - Group related changes together

5. **Apply Filters**
   - Exclude commits marked as `chore:`, `test:`, `docs:`, `refactor:` (unless user-facing)
   - Skip merge commits and version bump commits
   - Combine multiple commits about the same feature into one entry
   - Remove developer-only changes

6. **Add Context**
   - Include the date or version number in the title
   - Add a brief introduction if it's a major release
   - Link to detailed documentation for breaking changes
   - Include migration guides when relevant

## Example

**User**: "Create a changelog for commits from the past 7 days"

**Output**:
```markdown
# Updates - Week of March 10, 2024

## ✨ New Features

- **Team Workspaces**: Create separate workspaces for different 
  projects. Invite team members and keep everything organized.

- **Keyboard Shortcuts**: Press ? to see all available shortcuts. 
  Navigate faster without touching your mouse.

## 🔧 Improvements

- **Faster Sync**: Files now sync 2x faster across devices
- **Better Search**: Search now includes file contents, not just titles

## 🐛 Fixes

- Fixed issue where large images wouldn't upload
- Resolved timezone confusion in scheduled posts
- Corrected notification badge count
```

**Inspired by:** Manik Aggarwal's use case from Lenny's Newsletter

## Changelog Best Practices

### Writing Style
- **User-focused**: Explain what changed for the user, not the code
- **Benefit-oriented**: Lead with why this matters
- **Concise**: Keep entries to 1-2 sentences
- **Scannable**: Use formatting to help users find what they care about

### Structure
- **Consistent categorization**: Use the same categories every time
- **Most important first**: Features and breaking changes before bug fixes
- **Chronological within categories**: Newest changes first
- **Visual hierarchy**: Use headers, bold text, and emojis effectively

### Content Guidelines
- **Be specific**: "Fixed login issues" → "Fixed issue where login failed with Google accounts"
- **Quantify when possible**: "Faster loading" → "Pages load 50% faster"
- **Include context**: Explain why changes were made for major updates
- **Link to details**: Reference documentation or migration guides for complex changes

## Tips

- Run from your git repository root
- Specify date ranges for focused changelogs
- Use your CHANGELOG_STYLE.md for consistent formatting
- Review and adjust the generated changelog before publishing
- Save output directly to CHANGELOG.md

## Related Use Cases

- Creating GitHub release notes
- Writing app store update descriptions
- Generating email updates for users
- Creating social media announcement posts

## Example Transformations

### Technical Commit → User-Friendly Entry

| Technical Commit | User-Friendly Entry |
|-----------------|---------------------|
| "Add OAuth2 support for SSO integration" | "**Single Sign-On**: Log in with your company account" |
| "Optimize database queries with indexes" | "Dashboard loads 3x faster" |
| "Implement WebSocket connection for real-time updates" | "See changes instantly without refreshing" |
| "Add validation for email input fields" | "Helpful error messages when entering invalid emails" |
| "Fix memory leak in background sync worker" | "Improved app stability during long sessions" |

### Category Examples

**✨ New Features**
- New capabilities that didn't exist before
- Major additions to functionality
- New integrations or platform support

**🔧 Improvements**
- Performance enhancements
- UI/UX refinements
- Expanded existing functionality
- Better error messages

**🐛 Bug Fixes**
- Corrections to existing features
- Resolution of reported issues
- Fixes to edge cases

**⚠️ Breaking Changes**
- Changes requiring user action
- Removed features or APIs
- Changes to default behavior
- Migration steps required

**🔒 Security**
- Security patches
- Permission improvements
- Authentication enhancements
- Data protection updates
