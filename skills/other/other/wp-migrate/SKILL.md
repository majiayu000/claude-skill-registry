---
name: wp-migrate
description: WordPress site migration and deployment using wp-migrate.sh. Use when migrating WordPress sites, syncing databases, managing backups, testing migrations, debugging migration issues, or working with WordPress deployment workflows including Duplicator, Jetpack Backup, and Solid Backups archives. Also use for code modifications, testing, git workflows, PR creation, and release management for this project.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Task
  - TodoWrite
---

# WordPress Migration Skill

This skill provides expertise for working with the wp-migrate.sh WordPress migration tool.

## Project Overview

wp-migrate.sh is a comprehensive WordPress migration tool that operates in two modes:

1. **Push Mode**: Migrates WordPress sites between servers via SSH (source → destination)
2. **Archive Mode**: Imports WordPress backup archives (Duplicator, Jetpack Backup, Solid Backups) on destination server

**Current Version**: Check the latest release

```bash
git describe --tags --abbrev=0  # Get current version from git
```

**Latest Release**: See [GitHub Releases](https://github.com/BWBama85/wp-migrate.sh/releases/latest)

**Repository**: BWBama85/wp-migrate.sh

**Main Branch**: main

## Core Capabilities

### Migration Modes

#### Push Mode
- Transfers wp-content and database from source to destination via SSH
- Enables maintenance mode on both servers during migration
- Creates timestamped backups before overwriting
- Performs URL search-replace to align destination domain
- Excludes object-cache.php to preserve destination caching infrastructure
- Supports StellarSites managed hosting compatibility (--stellarsites flag)

#### Archive Mode
- Auto-detects archive format (Duplicator, Jetpack Backup, Solid Backups)
- Extracts archives to temporary directory
- Validates disk space (requires 3x archive size)
- Creates backups of destination database and wp-content before import
- Automatically aligns table prefixes if different from wp-config.php
- Performs URL search-replace to align with destination URLs
- Provides rollback instructions with exact commands

### Key Features
- **Migration preview with confirmation**: Pre-migration summary with detailed stats and confirmation prompt (v2.6.0)
- **Rollback command**: Automatic restoration from backups with --rollback flag (v2.6.0)
- **Progress indicators**: Real-time progress bars for long-running operations when pv is installed (v2.6.0)
- **Dry-run mode**: Preview all operations without making changes (--dry-run)
- **Verbose logging**: Show detailed diagnostic information (--verbose)
- **Trace mode**: Show every command before execution (--trace)
- **Plugin preservation**: Preserve destination plugins/themes not in source (--preserve-dest-plugins)
- **StellarSites mode**: Managed hosting compatibility with mu-plugins exclusion (--stellarsites)
- **Skip search-replace**: Fast migrations that only update home/siteurl options (--no-search-replace)
- **Automation support**: Skip confirmation prompts with --yes flag for CI/CD (v2.6.0)
- **Quiet mode**: Suppress progress indicators for non-interactive scripts with --quiet (v2.6.0)

## Common Tasks

### Running Migrations

**Push Mode:**
```bash
./wp-migrate.sh --dest-host user@dest.example.com --dest-root /var/www/site
```

**Archive Mode:**
```bash
./wp-migrate.sh --archive /path/to/backup.zip
./wp-migrate.sh --archive /path/to/backup.tar.gz --archive-type jetpack
```

**Dry Run:**
```bash
./wp-migrate.sh --dest-host user@dest --dest-root /var/www/site --dry-run --verbose
```

**Rollback (v2.6.0):**
```bash
./wp-migrate.sh --rollback  # Auto-detects latest backups
./wp-migrate.sh --rollback --rollback-backup /path/to/specific/backup  # Specific backup
./wp-migrate.sh --rollback --yes  # Skip confirmation for automation
```

**Automation-Friendly (v2.6.0):**
```bash
./wp-migrate.sh --archive /path/to/backup.zip --yes --quiet  # CI/CD: skip prompts, no progress bars
```

### Testing

**Run all tests:**
```bash
make test
```

**Run specific test:**
```bash
./test-wp-migrate.sh
```

**ShellCheck validation:**
```bash
shellcheck wp-migrate.sh
```

### Development Workflow

#### Code Structure (v2+)
The project uses a modular source structure:

```
src/
├── header.sh           # Shebang, defaults, variable declarations
├── lib/
│   ├── core.sh         # Core utilities (log, err, validate_url)
│   ├── functions.sh    # All other functions
│   └── adapters/       # Archive format adapters
│       ├── README.md
│       ├── duplicator.sh
│       ├── jetpack.sh
│       └── solidbackups.sh
└── main.sh             # Argument parsing and main execution
```

**IMPORTANT**: Modifications should be made in `src/` files, NOT in `wp-migrate.sh` directly.

#### Build Process

After modifying source files:
```bash
make build
```

This will:
1. Run shellcheck on concatenated source
2. Concatenate src/ files into dist/wp-migrate.sh
3. Copy to ./wp-migrate.sh (repo root)
4. Generate SHA256 checksum

#### Pre-commit Hook
A pre-commit hook prevents committing source changes without rebuilding:
```bash
ln -s ../../.githooks/pre-commit .git/hooks/pre-commit
```

### Git Workflow

1. **Branching**: Create from main using descriptive names:
   - `feature/<slug>` for enhancements
   - `fix/<slug>` for bug fixes
   - `docs/<slug>` for documentation
   - `chore/<slug>` for maintenance

2. **Commits**: Use .gitmessage template format:
   ```
   type: short imperative summary

   Longer explanation if needed
   ```

   Types: feat, fix, docs, chore, refactor, test

3. **Changelog**: Update CHANGELOG.md under [Unreleased] section with every feature or fix

4. **Pull Requests**:
   - Use .github/pull_request_template.md checklist
   - Include comprehensive summary based on ALL commits (not just latest)
   - Include test plan with verification steps
   - Reference related issues

5. **Merging**: Keep main release-ready with `git merge --no-ff` or squash after review

6. **Releases**: Tag with semantic versioning (e.g., `git tag v2.7.0`)

### Creating Pull Requests

When creating PRs, ensure:
- Review ALL commits in the branch (use `git log main..HEAD` and `git diff main...HEAD`)
- Summary covers complete scope of changes
- Test plan verifies all functionality
- CHANGELOG.md is updated
- ShellCheck passes
- Tests pass (make test)

### Common Files to Check

- [wp-migrate.sh](wp-migrate.sh) - Main script (built artifact, don't edit directly)
- [src/](src/) - Modular source files (edit these)
- [src/lib/adapters/](src/lib/adapters/) - Archive format adapters
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [README.md](README.md) - User documentation
- [Makefile](Makefile) - Build and test targets
- [test-wp-migrate.sh](test-wp-migrate.sh) - Test script

## Troubleshooting Guide

### Common Issues

**Permission Errors on Managed Hosts (StellarSites)**
- Symptom: "Permission denied" when syncing wp-content
- Solution: Use `--stellarsites` flag to exclude protected mu-plugins
- Details: Managed hosts protect certain mu-plugins directories (e.g., `stellarsites-cloud`)

**Database Import Fails**
- Check table prefix alignment (script auto-detects and updates wp-config.php)
- Verify sufficient disk space (3x archive size for archive mode)
- Check MySQL max_allowed_packet size for large imports

**URL Search-Replace Issues**
- Use `--verbose` to see detected URLs
- Override with `--dest-home-url` or `--dest-site-url` if detection fails
- Use `--no-search-replace` for faster migrations that only need home/siteurl updated

**Archive Detection Fails**
- Use explicit `--archive-type` to specify format (duplicator, jetpack, solidbackups)
- Verify archive structure matches adapter expectations (see src/lib/adapters/)
- Check detailed validation errors with --verbose (v2.6.0+)

**Non-Interactive Context Failures (v2.6.0)**
- Symptom: Script exits with "This script requires a TTY for confirmation prompts"
- Solution: Add `--yes` flag when running in CI/CD, cron, or pipeline contexts
- Details: Migration preview and rollback require confirmation by default; use --yes to bypass

**Rollback Issues (v2.6.0)**
- Auto-detection looks for latest timestamped backups in db-backups/ and wp-content.backup-*
- If backups aren't found, use `--rollback-backup /path/to/backup` to specify explicitly
- Rollback only works for archive mode migrations (restores from local backups)

**SSH Connection Issues**
- Add custom SSH options with `--ssh-opt` (can be repeated)
- Examples: `--ssh-opt 'Port=2222'` or `--ssh-opt 'ProxyJump=bastion'`

**ShellCheck Errors**
- Install ShellCheck: `brew install shellcheck` (macOS) or see https://www.shellcheck.net/
- Run: `shellcheck wp-migrate.sh`
- All code must be ShellCheck-clean before merging

### Debugging Commands

**Show verbose migration preview:**
```bash
./wp-migrate.sh --dest-host user@dest --dest-root /var/www/site --dry-run --verbose
```

**Show every command (trace mode):**
```bash
./wp-migrate.sh --dest-host user@dest --dest-root /var/www/site --dry-run --trace
```

**Check archive structure:**
```bash
unzip -l /path/to/backup.zip | head -50
tar -tzf /path/to/backup.tar.gz | head -50
```

**Verify wp-cli on destination:**
```bash
ssh user@dest 'cd /var/www/site && wp core version'
```

## Archive Adapter System

The script uses an extensible adapter system for different backup formats.

### Supported Formats

1. **Duplicator**: ZIP archives with `dup-installer/dup-database__*.sql` structure
2. **Jetpack Backup**: ZIP/TAR.GZ archives with `sql/*.sql` multi-file structure
3. **Solid Backups**: ZIP archives with split SQL in `wp-content/uploads/backupbuddy_temp/{ID}/`

### Adding New Adapters

See [src/lib/adapters/README.md](src/lib/adapters/README.md) for contributor guide.

Each adapter must implement:
- `validate_<adapter>()` - Check if file matches format
- `extract_<adapter>()` - Extract archive to temp directory
- `detect_db_<adapter>()` - Find database file(s)
- `detect_wp_content_<adapter>()` - Find wp-content directory

## Best Practices

### When Assisting with Code Changes

1. **Always check if source files need modification** (src/) not wp-migrate.sh directly
2. **Run `make build` after any source changes** to regenerate wp-migrate.sh
3. **Run ShellCheck validation** before committing
4. **Update CHANGELOG.md** for all features and fixes
5. **Use TodoWrite** to track multi-step tasks
6. **Create focused PRs** addressing single concerns

### When Testing Migrations

1. **Always start with dry-run** to preview operations
2. **Use verbose mode** for troubleshooting (--verbose or --trace)
3. **Verify backups** before destructive operations
4. **Test rollback procedures** in safe environments
5. **Check logs** in logs/ directory after migrations

### When Creating Releases

1. **Update CHANGELOG.md** with version number and date
2. **Create git tag** with semantic version (e.g., v2.7.0)
3. **Generate GitHub release** with changelog excerpt
4. **Verify tests pass** on clean checkout
5. **Update README** if user-facing changes exist

## Common Patterns

### Searching Code
Use Grep tool for code searches:
```
pattern: "function_name"
output_mode: "content"
-n: true (show line numbers)
```

### Reading Source Files
Use Read tool for file contents:
```
file_path: /Volumes/personal/codeprojects/bash/wp-migrate/src/lib/functions.sh
```

### Editing Code
Use Edit tool for precise changes:
```
file_path: /Volumes/personal/codeprojects/bash/wp-migrate/src/lib/functions.sh
old_string: "exact match from file"
new_string: "replacement text"
```

### Running Git Commands
```bash
git status
git diff main...HEAD  # See all changes in branch
git log main..HEAD    # See all commits in branch
```

## Critical Reminders

- **NEVER edit wp-migrate.sh directly** - edit files in src/ instead
- **ALWAYS run `make build`** after source changes
- **ALWAYS update CHANGELOG.md** for features and fixes
- **ALWAYS run ShellCheck** before committing (make test)
- **ALWAYS commit both source AND built files** together
- **ALWAYS review ALL commits** when creating PRs (not just latest commit)
- **ALWAYS use TodoWrite** for multi-step tasks to track progress
