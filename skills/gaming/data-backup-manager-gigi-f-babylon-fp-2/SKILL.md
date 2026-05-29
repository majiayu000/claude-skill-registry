---
name: Data Backup Manager
description: Backup and manage game data including maps, NPCs, and configurations. Use when the user wants to backup data, create snapshots, export data, or restore from backups.
---

# Data Backup Manager

Backup, export, and manage game data for the Babylon.js first-person game.

## Quick Start

### Create timestamped backup
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p backups/$TIMESTAMP
cp -r public/data backups/$TIMESTAMP/
echo "Backup created: backups/$TIMESTAMP"
```

### List all backups
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
ls -lht backups/
```

### Restore from latest backup
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
LATEST=$(ls -t backups/ | head -1)
cp -r backups/$LATEST/data/* public/data/
echo "Restored from: $LATEST"
```

## Backup Operations

### Backup specific data type
```bash
# Backup maps only
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p backups/$TIMESTAMP
cp -r public/data/maps backups/$TIMESTAMP/
```

```bash
# Backup NPCs only
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p backups/$TIMESTAMP
cp -r public/data/npcs backups/$TIMESTAMP/
```

### Create compressed backup
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf backups/backup_$TIMESTAMP.tar.gz public/data
echo "Compressed backup: backup_$TIMESTAMP.tar.gz"
```

### Export as JSON
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
# Pretty print all JSON files
for file in public/data/**/*.json; do
  echo "Formatting: $file"
  node -e "console.log(JSON.stringify(JSON.parse(require('fs').readFileSync('$file')), null, 2))" > "$file.tmp" && mv "$file.tmp" "$file"
done
```

## Data Validation

### Check JSON validity
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
for file in public/data/**/*.json; do
  echo -n "Checking $file: "
  node -e "JSON.parse(require('fs').readFileSync('$file'))" && echo "✓ Valid" || echo "✗ Invalid"
done
```

### Count data files
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "Maps: $(find public/data/maps -name '*.json' | wc -l)"
echo "NPCs: $(find public/data/npcs -name '*.json' | wc -l)"
echo "Events: $(find public/data/events -name '*.json' | wc -l)"
echo "Investigations: $(find public/data/investigations -name '*.json' | wc -l)"
```

## Restore Operations

### Restore from specific backup
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
# List available backups first
ls -1 backups/

# Restore from chosen backup (replace BACKUP_NAME)
BACKUP_NAME="20250117_143000"
cp -r backups/$BACKUP_NAME/data/* public/data/
echo "Restored from: $BACKUP_NAME"
```

### Restore specific file
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
LATEST=$(ls -t backups/ | head -1)
cp backups/$LATEST/data/maps/world.json public/data/maps/
echo "Restored world.json from: $LATEST"
```

## Best Practices

1. **Backup before major changes**: Always create backup before editing data
2. **Use timestamps**: Makes it easy to track when backups were created
3. **Validate JSON**: Check JSON validity after editing
4. **Regular backups**: Create backups at end of work sessions
5. **Test restores**: Periodically test that backups work
6. **Version control**: Backups complement git, don't replace it

## Cleanup

### Remove old backups (keep last 10)
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
ls -t backups/ | tail -n +11 | xargs -I {} rm -rf backups/{}
echo "Cleaned up old backups"
```
