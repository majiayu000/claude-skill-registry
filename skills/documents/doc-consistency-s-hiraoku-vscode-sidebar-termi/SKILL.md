---
name: doc-consistency
description: This skill provides guidance for maintaining documentation consistency with implementation in the vscode-sidebar-terminal project. Use this skill when creating or updating documentation, verifying documentation accuracy, preparing releases, or when the codebase has changed and documentation may need updates. This skill should be used proactively after implementing features or bug fixes.
---

# Documentation Consistency Skill

This skill ensures project documentation accurately reflects the current implementation.

## When to Use This Skill

- After implementing a new feature
- After fixing a bug that changes behavior
- Before creating a release
- When adding or modifying configuration options
- When adding or modifying keyboard shortcuts
- When updating architecture or patterns
- When reviewing documentation quality

## Documentation Update Workflow

### 1. Identify Changed Components

After code changes, determine which documentation needs updates:

| Change Type | Documents to Update |
|-------------|---------------------|
| New feature | README.md, CHANGELOG.md |
| Bug fix | CHANGELOG.md |
| Config change | README.md (Configuration), CHANGELOG.md |
| Shortcut change | README.md (Keyboard Shortcuts), CHANGELOG.md |
| Architecture change | CLAUDE.md, possibly domain CLAUDE.md files |
| WebView change | src/webview/CLAUDE.md, CLAUDE.md |
| Test pattern change | src/test/CLAUDE.md |

### 2. Update Documentation in Order

1. **CHANGELOG.md** - Always update first
   - Add entry under `[Unreleased]` section
   - Use correct section (Added/Changed/Fixed/etc.)
   - Include issue/PR number if applicable

2. **README.md** - If user-visible changes
   - Features table if new feature
   - Configuration section if settings changed
   - Keyboard Shortcuts if bindings changed

3. **CLAUDE.md** - If development process affected
   - Commands section if new npm scripts
   - Architecture section if patterns changed
   - Guidelines if best practices updated

4. **Domain-specific docs** - If specialized area changed
   - src/webview/CLAUDE.md for WebView changes
   - src/test/CLAUDE.md for testing changes

### 3. Verify Consistency

Run verification checks from `references/verification-checklist.md`:

```bash
# Version check
node -p "require('./package.json').version"

# Commands check
node -p "require('./package.json').contributes.commands.map(c => c.command).join('\n')"

# Config check
node -p "Object.keys(require('./package.json').contributes.configuration.properties).join('\n')"
```

## Pre-Release Documentation Checklist

Before each release, verify:

- [ ] CHANGELOG.md has entry for new version with correct date
- [ ] All new features documented in README.md
- [ ] All changed configurations documented correctly
- [ ] All keyboard shortcuts documented with correct platforms
- [ ] Version numbers consistent across files
- [ ] No TODO items left in documentation
- [ ] Links are working

## Quick Reference Commands

### Check Undocumented Commands

```bash
node -e "
const pkg = require('./package.json');
const fs = require('fs');
const readme = fs.readFileSync('README.md', 'utf8');
pkg.contributes.commands.forEach(cmd => {
  const shortName = cmd.command.replace('secondaryTerminal.', '');
  if (!readme.includes(shortName)) {
    console.log('Undocumented:', cmd.command);
  }
});
"
```

### Check Undocumented Configs

```bash
node -e "
const pkg = require('./package.json');
const fs = require('fs');
const readme = fs.readFileSync('README.md', 'utf8');
Object.keys(pkg.contributes.configuration.properties).forEach(key => {
  if (!readme.includes(key)) {
    console.log('Undocumented config:', key);
  }
});
"
```

### Check CHANGELOG Version

```bash
VERSION=$(node -p "require('./package.json').version")
grep -q "## \[$VERSION\]" CHANGELOG.md && echo "Version documented" || echo "Version missing in CHANGELOG"
```

## Document Structures

### README.md Structure

```
# Product Name
[Badges]
**Description**
[Hero Image]
## Quick Start
## Key Features
## Keyboard Shortcuts
## Command Palette
## Configuration
## Architecture
## Performance
## Troubleshooting
## Development
## Known Limitations
## Privacy
## Contributing
## Links
## License
```

### CHANGELOG.md Entry Format

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- **Feature Name**: Description (#issue-number)

### Fixed
- **Bug Name**: Fix description (#issue-number)
  - Technical detail if helpful

### Changed
- **Component Name**: What changed
```

### CLAUDE.md Structure

```
## Development Flow
## Essential Development Commands
## Architecture Overview
## Development Guidelines
## Known Issues & Workarounds
## Performance Optimization
## Testing Strategy
## Emergency Response
```

## Reference Files

For detailed information, read the following reference files:

| Reference | Use When |
|-----------|----------|
| `references/documentation-structure.md` | Understanding project documentation layout |
| `references/verification-checklist.md` | Running consistency checks |
| `references/writing-guidelines.md` | Writing or improving documentation |

## Common Issues and Solutions

### Issue: Feature in code but not documented

**Solution**:
1. Add feature description to README.md Key Features table
2. Add CHANGELOG.md entry under appropriate section
3. If architecture changed, update CLAUDE.md

### Issue: Configuration default changed

**Solution**:
1. Update README.md Configuration section
2. Add CHANGELOG.md entry under Changed
3. Verify package.json description matches

### Issue: Keyboard shortcut modified

**Solution**:
1. Update README.md Keyboard Shortcuts table
2. Include both Mac and Win/Linux bindings
3. Add CHANGELOG.md entry

### Issue: Japanese docs out of sync

**Solution**:
1. Compare README.md with docs/README_ja.md
2. Update Japanese version with new content
3. Consider whether domain CLAUDE.md files should be translated

## Writing Style Quick Reference

- **Concise**: Users skim documentation
- **Accurate**: Match current implementation exactly
- **User-centric**: Focus on "how to use" not "how it works"
- **Consistent**: Follow existing patterns in each file
- **Actionable**: Include commands and examples
