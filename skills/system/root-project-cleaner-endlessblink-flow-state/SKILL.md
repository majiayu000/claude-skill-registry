---
name: Root Project File Cleaner
description: CLEAN root directory of temporary files, build artifacts, and development clutter ONLY. This skill is exclusively for removing unwanted files from the project root directory - not for code organization, refactoring, or general project cleanup.
keywords: root directory, temporary files, build artifacts, file cleanup, development clutter
category: specialized
triggers: root directory cleanup, temporary files removal, build artifacts cleanup, development clutter removal, unwanted files cleanup
---

# Root Project File Cleaner Skill

**A specialized skill for safely removing temporary files, build artifacts, and unwanted clutter FROM THE PROJECT ROOT DIRECTORY ONLY.**

## ⚠️ IMPORTANT: SCOPE LIMITATION

**THIS SKILL ONLY CLEANS FILES FROM THE PROJECT ROOT DIRECTORY**
- ✅ **Cleans**: `node_modules/.cache`, `dist`, `.vite`, `*.tmp`, `*.log` in root
- ❌ **Does NOT**: Refactor code, organize source files, clean src/ directory
- ❌ **Does NOT**: Restructure project architecture or move source files
- ❌ **Does NOT**: Handle code organization or file management in `src/`

For code organization and refactoring, use `🧹 ts-architectural-cleanup` or `📁 safe-project-organizer` instead.

## Purpose

This skill provides intelligent, safe cleanup **OF THE PROJECT ROOT DIRECTORY ONLY** by identifying and removing:
- **Root-level temporary files**: `*.tmp`, `*.temp`, `*.swp`, `*.swo`
- **Root-level build artifacts**: `dist/`, `build/`, `.vite/`
- **Root-level cache directories**: `node_modules/.cache/`, `.cache/`
- **Root-level system files**: `.DS_Store`, `Thumbs.db` (in root only)
- **Root-level logs**: `*.log`, `logs/` (in root only)

## 🚫 OUT OF SCOPE - DO NOT USE FOR:

### Code Organization (Use other skills)
- ❌ **File refactoring**: Moving or organizing source code files
- ❌ **Directory restructuring**: Reorganizing `src/` directory structure
- ❌ **Import path fixes**: Updating import statements after file moves
- ❌ **Component reorganization**: Moving Vue components to new locations

### General Project Cleanup (Use appropriate skills)
- ❌ **Code cleanup**: Removing unused code or dead code elimination
- ❌ **Dependency cleanup**: Removing unused npm packages
- ❌ **Architecture cleanup**: Fixing architectural issues or patterns

**For these tasks, use:**
- 🧹 `ts-architectural-cleanup` - Code refactoring and architecture
- 📁 `safe-project-organizer` - Project structure reorganization
- 🎛️ `skills-manager` - Skills ecosystem management

## Key Features

### 🔒 **Safety First**
- **Git-aware cleanup** - Never deletes tracked files
- **Dry-run mode** - Preview changes before execution
- **Automatic backups** - Rollback capability for all deletions
- **Interactive confirmation** - Required for dangerous operations

### 🧠 **Intelligent Detection**
- **Pattern-based matching** - Configurable file/directory patterns
- **Size-based filtering** - Target files larger than specified threshold
- **Age-based filtering** - Remove files older than X days
- **Type categorization** - Separate handling for different file types

### 📊 **Comprehensive Reporting**
- **Detailed cleanup reports** - File counts, sizes, categories
- **Before/after comparisons** - Disk usage improvement metrics
- **Cleanup history** - Track all cleanup operations
- **Visual analytics** - Charts and statistics

## Usage

### Basic Cleanup
```javascript
// Quick safe cleanup with dry-run
await rootProjectCleaner.cleanup({
  dryRun: true,
  patterns: ['temp', 'cache', 'logs']
});
```

### Advanced Cleanup with Rules
```javascript
// Comprehensive cleanup with custom rules
await rootProjectCleaner.cleanup({
  dryRun: false,
  rules: {
    maxAge: 7, // days
    maxSize: '50MB',
    patterns: {
      include: ['*.tmp', '*.log', '.cache', 'dist'],
      exclude: ['*.config.js', '.gitkeep']
    }
  },
  backup: true,
  interactive: true
});
```

### Configuration Options
```javascript
const config = {
  // Safety settings
  gitAware: true,
  createBackup: true,
  interactiveMode: true,

  // Cleanup rules
  rules: {
    maxAge: 30,           // days
    maxSize: '100MB',     // file size limit
    patterns: {
      include: [
        '*.tmp', '*.temp', '*.swp', '*.swo',
        '*.log', 'logs/', '.cache/',
        'dist/', 'build/', '.vite/',
        'node_modules/.cache/', '.DS_Store',
        'Thumbs.db', '*.bak', '*.backup'
      ],
      exclude: [
        '*.config.*', '*.env.*', '.gitignore',
        'package.json', 'package-lock.json',
        '*.md', 'README.*', '.gitkeep'
      ]
    }
  },

  // Reporting
  verbose: true,
  generateReport: true,
  saveHistory: true
};
```

## Safety Mechanisms

### Git Integration
- Scans `.gitignore` for additional ignore patterns
- Checks git status to avoid deleting staged/committed changes
- Preserves all tracked files regardless of patterns

### Backup System
- Creates timestamped backups before deletion
- Supports full restoration from backup
- Backup location: `.claude/backups/root-cleanup/`

### Interactive Prompts
- Confirmation required for file deletions
- Summary preview before execution
- Option to skip specific files/directories

## Cleanup Categories

### 1. Build Artifacts
- `dist/`, `build/`, `.vite/`
- Compiled assets and bundles
- Static site generation output

### 2. Development Caches
- `node_modules/.cache/`
- `.cache/`, `tmp/`, `temp/`
- Framework and tool caches

### 3. Temporary Files
- `*.tmp`, `*.temp`, `*.swp`, `*.swo`
- Editor backup files
- System temporary files

### 4. System Files
- `.DS_Store`, `Thumbs.db`
- Desktop service files
- OS-specific metadata

### 5. Logs and Debug
- `*.log`, `logs/`, `debug/`
- Console output files
- Error logs and traces

## Integration with Existing Tools

### Pomo-Flow Integration
- Respects `npm run kill` process cleanup
- Works alongside existing cache clearing skills
- Integrates with project's established patterns

### Development Workflow
```bash
# Before major refactoring
npm run kill
npx @claude/root-cleaner --dry-run

# After build testing
npx @claude/root-cleaner --artifacts-only

# Weekly maintenance
npx @claude/root-cleaner --full-sweep
```

## Examples

### Scenario 1: Pre-Deployment Cleanup
```javascript
await rootProjectCleaner.cleanup({
  dryRun: false,
  rules: {
    patterns: {
      include: ['dist/', '.vite/', '*.log']
    }
  },
  backup: false
});
```

### Scenario 2: Development Cache Reset
```javascript
await rootProjectCleaner.cleanup({
  dryRun: false,
  rules: {
    maxAge: 1, // only today's cache
    patterns: {
      include: ['.cache/', 'node_modules/.cache/']
    }
  },
  backup: true
});
```

### Scenario 3: Large File Cleanup
```javascript
await rootProjectCleaner.cleanup({
  dryRun: true,
  rules: {
    maxSize: '50MB',
    patterns: {
      include: ['*.mp4', '*.zip', '*.tar.gz']
    }
  },
  interactive: true
});
```

## Reporting Output

### Summary Report
```
🧹 Root Project Cleanup Report
================================

📊 Cleanup Summary:
   • Files analyzed: 1,247
   • Files deleted: 89
   • Space recovered: 156.7 MB
   • Directories cleaned: 12

📂 Categories:
   • Build artifacts: 45 files (124.3 MB)
   • Cache files: 23 files (18.9 MB)
   • Temp files: 15 files (8.2 MB)
   • System files: 6 files (5.3 MB)

⏰ Time elapsed: 2.3 seconds
📦 Backup created: .claude/backups/root-cleanup/2024-01-15_14-30-25/
```

### Detailed File List
```
📋 Deleted Files:
   dist/assets/app.a1b2c3d4.js    (45.2 MB)
   .vite/deps/chunk-YZ4X5W6D.js   (12.8 MB)
   node_modules/.cache/eslint/     (8.9 MB)
   temp/compilation.tmp            (2.1 MB)
   .DS_Store                      (15.6 KB)
   ...
```

## Error Handling

### Common Issues
- **Permission denied** - Skips files without delete permissions
- **File in use** - Marks for retry on next run
- **Git conflicts** - Preserves files, logs warnings
- **Backup failures** - Continues with cleanup, logs error

### Recovery Options
```javascript
// Restore from backup
await rootProjectCleaner.restore({
  backupId: '2024-01-15_14-30-25',
  interactive: true
});

// List available backups
await rootProjectCleaner.listBackups();

// Cleanup old backups (keep last 5)
await rootProjectCleaner.cleanupBackups({ keepCount: 5 });
```

## Best Practices

1. **Always dry-run first** - Preview changes before actual cleanup
2. **Check git status** - Ensure no uncommitted changes
3. **Use interactive mode** - Review each deletion
4. **Keep backups** - Enable backup for important cleanups
5. **Review reports** - Check what was actually removed
6. **Schedule regularly** - Weekly maintenance prevents buildup

## Configuration File

Create `.claude/root-cleaner.config.js` in your project:

```javascript
export default {
  rules: {
    maxAge: 7,
    maxSize: '50MB',
    patterns: {
      include: [
        '*.tmp', '*.log', '.cache', 'dist',
        'node_modules/.cache', '.DS_Store'
      ],
      exclude: [
        '*.config.js', '.gitignore',
        'package.json', 'README.md'
      ]
    }
  },
  safety: {
    gitAware: true,
    createBackup: true,
    interactiveMode: true
  },
  reporting: {
    verbose: true,
    generateReport: true,
    saveHistory: true
  }
};
```

---

**Created for Pomo-Flow Vue.js project**
*Intelligent, safe project directory cleanup*

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
