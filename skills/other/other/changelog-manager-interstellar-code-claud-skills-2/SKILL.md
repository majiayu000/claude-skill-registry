---
name: changelog-manager
description: Update project changelog with uncommitted changes and create version releases with automatic commit and push
version: 1.0.0
author: Claude Code
tags: [changelog, versioning, git, release-management]
---

# Changelog Manager Skill

A comprehensive skill for managing project changelogs, semantic versioning, and automated release workflows.

---

## 🎯 **Interactive Menu**

**If no specific command is provided, show this menu:**

```
📋 Changelog Manager - Interactive Mode
=======================================

🚀 What would you like to do?

🔹 Option 1: Update Changelog with Uncommitted Changes
   Usage: /changelog-manager "update changelog"
   Usage: /changelog-manager "prepare release"
   Analyzes uncommitted changes and updates changelog with new version

🔹 Option 2: Create Specific Version
   Usage: /changelog-manager "release v1.2.4"
   Usage: /changelog-manager "major release" (bumps to next major version)
   Usage: /changelog-manager "minor release" (bumps to next minor version)
   Creates specific version with custom entries

🔹 Option 3: Review Current Changes
   Usage: /changelog-manager "review changes"
   Shows what would be added to changelog without committing

📝 Version Types:
• Patch (default): Bug fixes and minor improvements (1.2.3 → 1.2.4)
• Minor: New features, non-breaking changes (1.2.3 → 1.3.0)
• Major: Breaking changes, major updates (1.2.3 → 2.0.0)

💡 Examples:
• /changelog-manager "I've finished the new subscription filtering feature, update changelog"
• /changelog-manager "Ready to release v1.5.0"
• /changelog-manager "Review what changes would be included"

🔒 Security & Privacy:
========================
✅ Automatically filters out admin/backend changes
✅ Excludes technical implementation details
✅ Only includes user-facing improvements
✅ Removes sensitive information from changelog

⚙️  Workflow:
========================
1. 📊 Analyze uncommitted git changes
2. 🔍 Filter out admin/internal changes
3. 📝 Generate user-friendly changelog entries
4. 📈 Determine version increment (patch/minor/major)
5. ✍️  Update CHANGELOG.md
6. 💾 Commit ALL changes
7. 🚀 Push to remote repository
```

---

## Overview

This skill automates the complete changelog update and version release process for SubsHero, ensuring:
- **User-focused changelog entries** (no technical jargon)
- **Privacy-first approach** (no internal details exposed)
- **Semantic versioning compliance**
- **Automated git commit and push workflow**

## Capabilities

### 🔍 **Change Analysis**
- Analyze uncommitted changes using git status and diff
- Identify modified, added, and deleted files
- Understand code changes and their user impact
- Filter out admin and internal changes automatically

### 🔒 **Privacy & Security**
**Automatically excludes from public changelog:**
- Admin panel improvements and backend tools
- Database migrations and schema changes
- API endpoints and middleware updates
- Configuration and environment changes
- Logging, debugging, and monitoring tools
- Authentication and security updates
- Deployment scripts and infrastructure
- Test improvements and code refactoring

**Only includes in changelog:**
- New user-facing features
- UI/UX improvements
- Bug fixes affecting user experience
- Performance improvements users can notice
- Integration with new platforms

### 📊 **Version Management**
- **Patch increment** (default): 1.2.3 → 1.2.4
- **Minor increment**: 1.2.3 → 1.3.0
- **Major increment**: 1.2.3 → 2.0.0
- Automatic version detection from CHANGELOG.md
- Semantic versioning compliance

### ✍️ **Changelog Updates**
- Standard changelog format (Keep a Changelog)
- Organized by change type:
  - **Added**: New features
  - **Changed**: Modifications to existing features
  - **Fixed**: Bug fixes
  - **Improved**: Performance and UX improvements
- User-friendly, non-technical language
- Clear dates and version numbers

### 🚀 **Git Automation**
- Stage ALL uncommitted files
- Create comprehensive commit messages
- Push changes to remote repository
- Verify successful completion
- Detailed operation summary

## Usage

### Quick Start

#### Update Changelog with Current Changes
```bash
/changelog-manager "update changelog"
```

#### Prepare a New Release
```bash
/changelog-manager "ready to release"
```

#### Create Specific Version
```bash
/changelog-manager "release v2.0.0"
```

#### Review Changes Without Committing
```bash
/changelog-manager "review changes"
```

### Advanced Usage

#### Major Version Release
```bash
/changelog-manager "major release with breaking changes to subscription API"
```

#### Minor Version with Custom Notes
```bash
/changelog-manager "minor release: added dark mode and improved search"
```

#### Patch Release for Bug Fixes
```bash
/changelog-manager "patch release: fixed notification bugs"
```

## Workflow Steps

### 1. Change Analysis

**Actions**:
- Execute `git status` to identify all uncommitted changes
- Run `git diff` to examine actual code modifications
- Analyze file paths and content changes
- Categorize changes by type and impact

**Output**: List of user-facing changes ready for changelog

### 2. Privacy Filtering

**Excluded Patterns**:
- Files in `app/Http/Controllers/Api/Admin/`
- Files in `resources/js/components/admin/`
- Files in `database/migrations/`
- Files in `config/`, `scripts/`, `bootstrap/`
- Any file containing admin, backend, API, middleware keywords
- Configuration files (.env, .config)
- Test files and documentation

**Included Patterns**:
- User-facing components
- Frontend improvements
- Visible bug fixes
- UX enhancements
- Performance improvements users notice

### 3. Version Determination

**Logic**:
```
Default: Patch increment (unless specified otherwise)
- Fixes only → Patch (1.2.3 → 1.2.4)
- New features → Minor (1.2.3 → 1.3.0)
- Breaking changes → Major (1.2.3 → 2.0.0)
```

**User can override**:
- "/changelog-manager release v2.0.0" → Use exact version
- "/changelog-manager major release" → Force major increment
- "/changelog-manager minor release" → Force minor increment

### 4. Changelog Update

**Format**:
```markdown
## [1.2.4] - 2025-10-19

### Added
- New feature descriptions from user perspective

### Changed
- Improvements to existing functionality

### Fixed
- Bug fixes that affect user experience

### Improved
- Performance enhancements users can notice
```

**File Location**: `CHANGELOG.md` in project root

### 5. Git Operations

**Commit Process**:
```bash
# Stage all changes
git add .

# Create comprehensive commit
git commit -m "Release v1.2.4: Brief summary of key changes"

# Push to remote
git push origin [current-branch]
```

**Verification**:
- Confirm all files staged successfully
- Verify commit created with correct message
- Ensure push completed to remote repository
- Display summary of committed files

## Examples

### Example 1: Feature Release

**Input**:
```
/changelog-manager "I've added browser password import feature, ready to release"
```

**Process**:
1. Analyzes git changes
2. Filters out backend/admin changes
3. Identifies: "Added browser password import feature"
4. Creates version 1.2.4 (patch increment)
5. Updates CHANGELOG.md:
   ```markdown
   ## [1.2.4] - 2025-10-19

   ### Added
   - Browser password import feature for quick subscription setup
   ```
6. Commits: "Release v1.2.4: Added browser password import"
7. Pushes to remote

**Output**:
```
✅ Successfully created release v1.2.4
📝 Changelog updated with 1 user-facing improvement
💾 Committed 15 files
🚀 Pushed to origin/main
```

### Example 2: Bug Fix Release

**Input**:
```
/changelog-manager "fixed timeout issues in import, update changelog"
```

**Process**:
1. Detects bug fixes
2. Creates patch version 1.2.5
3. Updates CHANGELOG.md:
   ```markdown
   ## [1.2.5] - 2025-10-19

   ### Fixed
   - Timeout issues during large password imports
   ```

### Example 3: Review Only

**Input**:
```
/changelog-manager "review what would be included"
```

**Output**:
```
📊 Uncommitted Changes Analysis
================================

User-Facing Changes (Will be included):
✅ Added: Browser password import modal
✅ Fixed: UI freeze after import completion
✅ Improved: Import performance (35 credentials/second)

Excluded (Admin/Internal):
❌ Updated UrlMatchingService with caching
❌ Added database query optimizations
❌ Modified CredentialImportController timeout

Suggested Version: 1.2.4 (patch)
Would you like to proceed with the release?
```

## Configuration

### Default Settings
- **Version Increment**: Patch (unless specified)
- **Changelog File**: `CHANGELOG.md`
- **Commit Message Format**: "Release v{VERSION}: {SUMMARY}"
- **Branch**: Current branch (auto-detected)

### Customization
You can customize behavior by including details in your request:
```bash
/changelog-manager "major release v2.0.0 with complete UI redesign"
```

## Error Handling

### No Uncommitted Changes
```
⚠️ No uncommitted changes found
Would you like to:
1. Review the current changelog
2. Create a version from recent commits
3. Cancel operation
```

### Changelog File Not Found
```
❌ CHANGELOG.md not found
Creating new changelog file at project root...
✅ Created CHANGELOG.md with initial structure
```

### Git Operation Failures
```
❌ Git push failed: [error details]

Suggested solutions:
1. Check remote repository connectivity
2. Verify branch permissions
3. Resolve any merge conflicts
4. Retry the operation
```

### Version Conflict
```
⚠️ Version 1.2.4 already exists in CHANGELOG.md

Options:
1. Increment to 1.2.5
2. Specify different version
3. Override existing entry (not recommended)
```

## Best Practices

### When to Use This Skill
✅ After completing a feature or bug fix
✅ Before deploying to production
✅ When preparing a release for users
✅ To document user-facing improvements

### When NOT to Use
❌ For internal/admin-only changes
❌ For work-in-progress commits
❌ For experimental features not ready for users
❌ For configuration or deployment changes only

### Writing Good Changelog Entries
**Good** ✅:
- "Added ability to import browser passwords"
- "Fixed subscription search not showing results"
- "Improved page load speed by 50%"

**Bad** ❌:
- "Updated CredentialImportService.php"
- "Fixed bug in line 234 of controller"
- "Added new API endpoint for admin panel"

## Integration with Git

### Automatic Git Detection
- Current branch name
- Current version from CHANGELOG.md
- Uncommitted changes list
- Remote repository status

### Safe Operations
- Confirms changes before committing
- Shows what will be included
- Verifies successful push
- Provides rollback guidance if needed

## Troubleshooting

### Changes Not Appearing
**Issue**: Made changes but they're not showing in changelog
**Solution**: Check if changes are in excluded paths (admin, config, etc.)

### Wrong Version Increment
**Issue**: Expected minor but got patch
**Solution**: Specify version type explicitly: "/changelog-manager minor release"

### Push Rejected
**Issue**: Git push fails with remote rejection
**Solution**: Pull latest changes first, resolve conflicts, then retry

### Multiple Changelog Files
**Issue**: Project has multiple changelog files
**Solution**: Skill uses CHANGELOG.md by default; specify different file if needed

## Version History

### v1.0.0
- Initial release
- Automatic change analysis and filtering
- User-focused changelog generation
- Semantic versioning support
- Automated git commit and push
- Privacy-first approach (excludes admin/internal changes)

## Support

For issues or questions:
- Ensure git repository is initialized
- Verify CHANGELOG.md exists (will be created if missing)
- Check git remote configuration
- Review excluded paths and patterns
