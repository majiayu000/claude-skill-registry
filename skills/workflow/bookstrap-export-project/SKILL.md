---
name: bookstrap-export-project
description: Export complete project including manuscript, database, and configuration
invoke: skill
category: export
---

# Project Export Command

Export the entire Bookstrap project for backup, sharing, or archiving.

## What It Does

Creates a complete project export including:
- Manuscript files
- Database backup
- Configuration files
- Source documents
- Research notes
- Edit reports
- Git history (optional)

## Usage

```bash
/bookstrap-export-project --output project-export.zip
```

### Options

```bash
/bookstrap-export-project \
  --output export.zip \
  --include-git \
  --include-sources \
  --format zip
```

## Export Contents

### Always Included

- `manuscript/` - All written sections
- `BRD.md` - Book Requirements Document
- `bookstrap.config.json` - Project configuration
- `database-backup.surql` - Full database export
- `export-manifest.json` - Metadata about the export

### Optional Inclusions

- `--include-git`: Include `.git` directory (version history)
- `--include-sources`: Include ingested source documents
- `--include-logs`: Include edit reports and logs
- `--include-schema`: Include database schema files

## Export Formats

### ZIP Archive (default)

```bash
/bookstrap-export-project --output my-book.zip
```

Creates a compressed ZIP file.

### TAR.GZ Archive

```bash
/bookstrap-export-project --output my-book.tar.gz --format tar.gz
```

Creates a compressed tarball.

### Directory

```bash
/bookstrap-export-project --output my-book-export --format directory
```

Exports to a directory (no compression).

## Export Manifest

Each export includes `export-manifest.json`:

```json
{
  "project_name": "My Book",
  "exported_at": "2026-02-01T12:00:00Z",
  "bookstrap_version": "1.0.0",
  "export_format": "zip",
  "contents": {
    "manuscript": {
      "chapters": 12,
      "sections": 48,
      "total_words": 75420,
      "status": "draft"
    },
    "database": {
      "sources": 42,
      "entities": 156,
      "relationships": 384
    },
    "configuration": {
      "embedding_provider": "openai",
      "search_provider": "tavily"
    }
  },
  "checksums": {
    "manuscript": "sha256:abc123...",
    "database": "sha256:def456..."
  }
}
```

## Implementation

```bash
#!/bin/bash

OUTPUT=$1
FORMAT=${2:-zip}

# Create temporary export directory
EXPORT_DIR=$(mktemp -d)
PROJECT_NAME=$(basename $(pwd))

echo "Exporting project to: $OUTPUT"

# Export manuscript
cp -r manuscript/ $EXPORT_DIR/manuscript/

# Export configuration
cp BRD.md $EXPORT_DIR/
cp bookstrap.config.json $EXPORT_DIR/

# Backup database
./scripts/backup-db.sh $EXPORT_DIR/database-backup.surql

# Generate manifest
python ./scripts/generate-export-manifest.py \
  --output $EXPORT_DIR/export-manifest.json

# Optional: Include git history
if [[ "$INCLUDE_GIT" == "true" ]]; then
  cp -r .git $EXPORT_DIR/
fi

# Create archive
if [[ "$FORMAT" == "zip" ]]; then
  cd $EXPORT_DIR && zip -r $OUTPUT *
elif [[ "$FORMAT" == "tar.gz" ]]; then
  tar -czf $OUTPUT -C $EXPORT_DIR .
else
  mv $EXPORT_DIR $OUTPUT
fi

echo "Export complete: $OUTPUT"
```

## Import/Restore

To restore from an export:

```bash
/bookstrap-import-project --input project-export.zip
```

This will:
1. Extract archive
2. Restore database from backup
3. Copy manuscript files
4. Restore configuration
5. Verify integrity using checksums

## Best Practices

1. **Export regularly** for backup
2. **Include git history** for version control
3. **Exclude sources** if large files (can re-ingest)
4. **Verify export** before deleting originals
5. **Use semantic versioning** for export filenames

## Use Cases

### Backup

```bash
/bookstrap-export-project \
  --output backups/my-book-$(date +%Y%m%d).zip \
  --include-git
```

### Sharing with Collaborators

```bash
/bookstrap-export-project \
  --output my-book-collab.zip \
  --include-sources \
  --include-logs
```

### Archiving Final Version

```bash
/bookstrap-export-project \
  --output my-book-final-v1.0.zip \
  --include-git \
  --include-sources \
  --include-logs
```

## Example Output

```
Exporting Bookstrap project...

Preparing export directory...
├─ Copying manuscript (48 sections, 75,420 words)
├─ Copying configuration files
├─ Backing up database (42 sources, 156 entities)
├─ Generating export manifest
├─ Calculating checksums
└─ Creating ZIP archive

Export complete!

File: my-book-export.zip
Size: 12.4 MB
Contents:
  - Manuscript: 48 sections
  - Database: 42 sources, 156 entities
  - Configuration: bookstrap.config.json
  - Git history: 127 commits

Verify with: unzip -l my-book-export.zip
```
