---
name: downloads-organizer
description: Automatically organize and clean up downloads folder by categorizing files, removing duplicates, and optimizing storage space
license: Apache-2.0
---

# Downloads Organizer

Automatically organize and clean up your downloads folder with intelligent file categorization, duplicate detection, and storage optimization.

## Overview

Transform a chaotic downloads folder into a well-organized, searchable archive by:
- **Categorizing files** - Organize by type (documents, images, videos, installers, etc.)
- **Removing duplicates** - Detect and eliminate duplicate files
- **Cleaning old files** - Remove outdated installers and temporary files
- **Generating reports** - Provide detailed analysis of storage usage
- **Scheduled cleanup** - Set up automated maintenance

## Basic Workflow

### 1. Analyze Downloads Folder

Get current state:
```bash
cd ~/Downloads
python scripts/organizer.py --analyze
```

Output:
```
📊 Downloads Folder Analysis
Total Size: 45.2 GB
Total Files: 1,234
Total Folders: 87

Largest Files:
1. alma-0.0.204-mac-arm64.dmg (248 MB)
2. Antigravity.Tools_3.3.32_aarch64.dmg (14 MB)

File Distribution:
- Installers: 3.6 GB (8%)
- Documents: 662 MB (1.5%)
- Images: 1.2 GB (2.7%)
- Videos: 5.8 GB (12.8%)
```

### 2. Organize Files

Auto-categorize scattered files:
```bash
python scripts/organizer.py --organize --dry-run
```

Preview:
```
Would move:
- *.dmg → Installers/ (15 files)
- *.png → Images/ (42 files)
- *.pdf → Documents/PDF/ (23 files)
- *.mp4 → Videos/ (8 files)
- *.json → Documents/ (12 files)
```

Execute:
```bash
python scripts/organizer.py --organize
```

### 3. Clean Up

Remove old and duplicate files:
```bash
python scripts/organizer.py --cleanup
```

Actions:
- Remove installers older than 60 days
- Delete duplicate files
- Remove empty folders
- Clean temporary files

### 4. Generate Report

Get detailed report:
```bash
python scripts/organizer.py --report --output report.md
```

## Organization Rules

### File Type Categories

**Documents:**
- `*.pdf`, `*.doc`, `*.docx`, `*.txt`, `*.md`, `*.rtf`
- `*.xls`, `*.xlsx`, `*.csv`, `*.json`, `*.yaml`, `*.yml`

**Images:**
- `*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.svg`, `*.webp`, `*.bmp`
- `*.tiff`, `*.ico`

**Videos:**
- `*.mp4`, `*.mov`, `*.avi`, `*.mkv`, `*.webm`, `*.flv`

**Audio:**
- `*.mp3`, `*.wav`, `*.m4a`, `*.flac`, `*.aac`, `*.ogg`

**Installers:**
- `*.dmg`, `*.pkg`, `*.app`, `*.zip`, `*.tar.gz`, `*.rar`
- `*.exe`, `*.msi`

**Archives:**
- `*.zip`, `*.tar.gz`, `*.tgz`, `*.rar`, `*.7z`

**Code:**
- `*.py`, `*.js`, `*.ts`, `*.java`, `*.cpp`, `*.c`, `*.h`
- `*.html`, `*.css`, `*.scss`, `*.json`

**Data:**
- `*.csv`, `*.tsv`, `*.sql`, `*.db`, `*.sqlite`

### Folder Structure

```
~/Downloads/
├── Archives/          # Compressed archives
├── Audio/             # Audio files
├── Backups/           # Backup files and folders
├── Documents/         # Documents and text files
│   ├── PDF/
│   └── Spreadsheets/
├── Images/            # Image files
├── Installers/        # Software installers
├── Projects/          # Project-related folders
├── Videos/            # Video files
├── Software/          # Application bundles
└── Others/           # Miscellaneous files
```

## Cleanup Strategies

### Time-Based Cleanup

**Installers:**
- Remove `*.dmg`, `*.pkg` files older than 60 days
- Keep only recent installers (last 2 months)

**Temporary Files:**
- Remove `*.tmp`, `*.temp`, `*.cache` files
- Clean `~/.Trash` contents

**Empty Folders:**
- Remove directories with 0 files
- Remove directories older than 90 days with < 5 files

### Duplicate Detection

Find duplicates by:
- **File name** - Exact name match
- **File size** - Same size (quick filter)
- **Hash comparison** - MD5/SHA256 for exact duplicates

Action:
```bash
python scripts/organizer.py --find-duplicates
```

Keep strategy:
- Keep newest file
- Keep file with shortest path
- Ask user for conflicts

### Large File Analysis

Identify space hogs:
```bash
python scripts/organizer.py --large-files --min-size 100MB
```

Output:
```
📦 Large Files (>100MB):
1. alma-0.0.204-mac-arm64.dmg - 248 MB
2. recording_2026-01-10_23-22-53.mp4 - 12 MB
3. generated-1768282547017.png - 25 MB
```

## Automated Maintenance

### Schedule Cleanup

Set up cron job for automatic cleanup:

```bash
# Run cleanup every Sunday at 2 AM
0 2 * * 0 cd ~/Downloads && python scripts/organizer.py --cleanup

# Run organization daily at 9 AM
0 9 * * * cd ~/Downloads && python scripts/organizer.py --organize
```

### Automated Rules

Define custom rules in `config/rules.yaml`:

```yaml
patterns:
  - pattern: "*_recording_*.mp4"
    destination: Videos/Recordings/
    keep_days: 30

  - pattern: "generated-*.png"
    destination: Images/Generated/
    keep_days: 7

  - pattern: "Screenshot*.png"
    destination: Images/Screenshots/
    keep_days: 30
```

## Configuration

### Settings File

Create `~/.downloads-organizer/config.yaml`:

```yaml
downloads_dir: ~/Downloads
dry_run: false
verbose: true

cleanup:
  installer_age_days: 60
  temp_age_days: 7
  duplicate_action: keep_newest

organization:
  auto_categorize: true
  respect_existing_folders: true
  create_missing_folders: true

exclusions:
  - "*.locked"
  - ".*"
  - "node_modules"
  - ".git"
```

### Custom Categories

Add custom file types to categories:

```yaml
custom_categories:
  design:
    extensions: [".sketch", ".fig", ".psd", ".ai"]
    folder: "Design/"

  data_science:
    extensions: [".ipynb", ".r", ".mat", ".h5"]
    folder: "DataScience/"
```

## Usage Examples

### Example 1: Weekly Maintenance

```bash
# Full cleanup cycle
python scripts/organizer.py \
  --organize \
  --cleanup \
  --report \
  --output ~/Downloads/weekly-report.md
```

### Example 2: Quick Organize

```bash
# Just organize new files
python scripts/organizer.py --organize --new-only
```

### Example 3: Deep Clean

```bash
# Aggressive cleanup with confirmation
python scripts/organizer.py \
  --cleanup \
  --installer-age 30 \
  --remove-duplicates \
  --remove-empty-folders \
  --confirm
```

### Example 4: Project Cleanup

```bash
# Move project files to Projects/ folder
python scripts/organizer.py \
  --move-projects \
  --project-pattern "*-project*" \
  --destination Projects/
```

## Integration

### Obsidian Integration

Link organized files to Obsidian vault:

```bash
python scripts/organizer.py --link-obsidian --vault ~/Documents/ObsidianVault
```

Creates:
- `[[Downloads/Images/file.png]]` links in Obsidian
- Daily notes with new files
- Mappings for easy searching

### Cloud Sync Integration

Sync organized folders to cloud:

```bash
python scripts/organizer.py --sync-cloud \
  --provider icloud \
  --folders Documents,Images \
  --exclude-backups
```

### Notification Integration

Send cleanup notifications:

```bash
python scripts/organizer.py --cleanup --notify \
  --method slack \
  --channel #downloads
```

## Best Practices

### Organization

✅ **DO:**
- Organize regularly (daily or weekly)
- Use consistent folder structure
- Keep recent installers accessible
- Archive important files to permanent locations

❌ **DON'T:**
- Wait until downloads folder is huge
- Mix unrelated file types
- Delete files without reviewing
- Keep old installers "just in case"

### Cleanup

✅ **DO:**
- Set appropriate age thresholds
- Review duplicates before deleting
- Check large files before cleanup
- Backup important files first

❌ **DON'T::**
- Delete files blindly
- Set too aggressive cleanup
- Ignore duplicate warnings
- Skip backup checks

### Performance

✅ **DO:**
- Schedule cleanup during low activity
- Use dry-run first
- Monitor disk space after cleanup
- Keep logs for troubleshooting

❌ **DON'T:**
- Run cleanup while downloading
- Organize during file transfers
- Disable safety checks
- Ignore error messages

## Troubleshooting

### File Move Conflicts

**Problem:** "File already exists" error

**Solution:**
```bash
python scripts/organizer.py --organize --handle-conflicts ask
```

Options:
- `ask` - Prompt for each conflict
- `skip` - Skip conflicting files
- `overwrite` - Overwrite existing files
- `rename` - Add timestamp to new files

### Permission Errors

**Problem:** "Permission denied" when moving files

**Solution:**
```bash
# Fix permissions
chmod -R u+rw ~/Downloads

# Run with sudo (last resort)
sudo python scripts/organizer.py --cleanup
```

### Slow Performance

**Problem:** Organization takes too long

**Solution:**
```bash
# Exclude large directories
python scripts/organizer.py --exclude "Projects/,Backups/"

# Use parallel processing
python scripts/organizer.py --parallel --workers 4

# Skip hash comparison for duplicates
python scripts/organizer.py --find-duplicates --quick
```

## Resources

- Main script: `scripts/organizer.py`
- Configuration guide: `references/configuration.md`
- File type mappings: `references/file-types.yaml`
- Troubleshooting: `references/troubleshooting.md`

## Safety Features

### Backup Before Cleanup

Always create backup before major cleanup:
```bash
python scripts/organizer.py --backup --dest ~/Downloads-backup
```

### Undo Functionality

Roll back changes:
```bash
python scripts/organizer.py --undo --from ~/Downloads-backup
```

### Confirmation Prompts

Confirm destructive actions:
```bash
python scripts/organizer.py --cleanup --confirm
```

### Logging

Detailed logging for audit:
```bash
python scripts/organizer.py --organize --log-level debug --log-file organizer.log
```

---

**Last Updated:** 2026-01-15
**Version:** 1.0.0
