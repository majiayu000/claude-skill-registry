---
name: file-operations
description: Linux file and directory operations
version: 1.0.0
author: terminal-skills
tags: [linux, file, directory, find, permissions]
---

# File and Directory Operations

## Overview
Linux file system operation skills, including file search, batch operations, permission management, etc.

## File Search

### find Command
```bash
# Search by name
find /path -name "*.log"
find /path -iname "*.LOG"           # Case insensitive

# Search by type
find /path -type f                  # Files
find /path -type d                  # Directories
find /path -type l                  # Symbolic links

# Search by time
find /path -mtime -7                # Modified within 7 days
find /path -mtime +30               # Modified more than 30 days ago
find /path -mmin -60                # Modified within 60 minutes

# Search by size
find /path -size +100M              # Larger than 100MB
find /path -size -1k                # Smaller than 1KB

# Combined conditions
find /path -name "*.log" -mtime +7 -size +10M
```

### locate Command
```bash
# Quick search (requires database update)
locate filename
updatedb                            # Update database

# Case insensitive
locate -i filename
```

## File Operations

### Basic Operations
```bash
# Copy
cp file1 file2
cp -r dir1 dir2                     # Recursive copy directory
cp -p file1 file2                   # Preserve attributes

# Move/Rename
mv file1 file2
mv file1 /path/to/dest/

# Delete
rm file
rm -rf dir                          # Recursive force delete
rm -i file                          # Interactive confirmation

# Create
touch file                          # Create empty file
mkdir -p dir1/dir2/dir3             # Recursive create directories
```

### Batch Operations
```bash
# Batch rename
rename 's/old/new/' *.txt
for f in *.txt; do mv "$f" "${f%.txt}.md"; done

# Batch delete
find /path -name "*.tmp" -delete
find /path -name "*.log" -mtime +30 -exec rm {} \;

# Batch copy
find /src -name "*.conf" -exec cp {} /dest/ \;
```

## File Content

### View Files
```bash
cat file                            # Full content
head -n 20 file                     # First 20 lines
tail -n 20 file                     # Last 20 lines
tail -f file                        # Real-time follow
less file                           # Paginated view

# Statistics
wc -l file                          # Line count
wc -w file                          # Word count
wc -c file                          # Byte count
```

### File Comparison
```bash
diff file1 file2
diff -u file1 file2                 # Unified format
diff -r dir1 dir2                   # Compare directories

# Side-by-side comparison
sdiff file1 file2
vimdiff file1 file2
```

## Permission Management

### View Permissions
```bash
ls -la
stat file
```

### Modify Permissions
```bash
# Numeric mode
chmod 755 file                      # rwxr-xr-x
chmod 644 file                      # rw-r--r--

# Symbolic mode
chmod u+x file                      # Add execute for user
chmod g-w file                      # Remove write for group
chmod o=r file                      # Set read-only for others
chmod a+r file                      # Add read for all

# Recursive modify
chmod -R 755 dir
```

### Modify Owner
```bash
chown user file
chown user:group file
chown -R user:group dir             # Recursive modify
```

## Common Scenarios

### Scenario 1: Clean Up Large Files
```bash
# Find files larger than 100MB
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null

# Find and sort by size
du -ah /path | sort -rh | head -20
```

### Scenario 2: Find Recently Modified Files
```bash
# Files modified within 24 hours
find /path -type f -mtime -1

# Sort by modification time
ls -lt /path | head -20
```

### Scenario 3: Batch Replace File Content
```bash
# Single file replacement
sed -i 's/old/new/g' file

# Batch replacement
find /path -name "*.conf" -exec sed -i 's/old/new/g' {} \;
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Permission denied | Use `sudo` or check file permissions |
| Disk space full | `df -h`, `du -sh *` to find large files |
| Special characters in filename | Use quotes or escape `rm "file name"` |
| Slow deletion of many files | Use `rsync --delete` or `find -delete` |
