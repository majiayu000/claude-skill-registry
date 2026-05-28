---
name: find
description: File search and manipulation utility for locating files by name, type, size, permissions, and time.
---

# find

**Basic Search**

```bash
# Find files by name (case-sensitive)
find . -name '*.txt'

# Find files by name (case-insensitive)
find . -iname '*.jpg'

# Find directories
find . -type d

# Find files (not directories, links, etc.)
find . -type f

# Find in specific path
find /path/to/search -name '*.txt'
```

**Size-Based**

```bash
# Files bigger than 100MB
find ./ -type f -size +100M

# Files bigger than 5MB
find . -size +5M -type f

# Files bigger than 2MB and list them
find . -type f -size +20000k -exec ls -lh {} \; | awk '{ print $9 ": " $5 }'

# Files exactly 1MB
find . -size 1M

# Files less than 100KB
find . -size -100K
```

**Time-Based**

```bash
# Files modified in last 3 days
find ./ -type f -mtime +3 -exec rm {} +

# Files modified more than 365 days ago
find ./ -type f -name "*.log" -mtime +365 -delete

# Files accessed in last 7 days
find . -type f -atime -7

# Files modified in last 24 hours
find . -type f -mtime 0

# Files changed in last 5 minutes
find . -type f -cmin -5
```

**Permission-Based**

```bash
# Files with 777 permissions
find . -type f -perm 777

# Files with setuid bit
find . -xdev -perm -4000 -type f -print0 | xargs -0 ls -l

# World-writable files
find . -type f -perm -002

# Files writable by owner
find . -type f -perm -200

# Files owned by specific user
find . -user username
```

**Owner & Group**

```bash
# Files owned by root
find . -user root

# Files owned by specific group
find . -group groupname

# Find files not owned by current user
find . -type f ! -user $(whoami)
```

**Advanced Search**

```bash
# Find and remove files
find [PATH] -name '*.txt' -delete

# Find and execute command
find . -name '*.txt' -exec rm {} \;

# Find and grep for string
find ./path/ -name '*.txt' | xargs grep 'string'

# Find files bigger than 5MB and sort by size
find . -size +5M -type f -print0 | xargs -0 ls -Sh | sort -z

# Find empty files
find . -type f -empty

# Find empty directories
find . -type d -empty

# Find files by extension (case-insensitive)
find . -type f -iname '*.log'

# Limit search depth
find . -maxdepth 2 -name '*.txt'

# Skip specific directories
find . -name 'node_modules' -prune -o -name '*.js' -print

# Find and show file types
find . -type f -exec file {} \;
```

**Combined Operations**

```bash
# Find and copy files
find . -name '*.jpg' -exec cp {} /destination \;

# Find and move files by date
find . -type f -mtime +30 -exec mv {} /old-files/ \;

# Find and change permissions
find . -type f -name '*.sh' -exec chmod +x {} \;

# Find and change ownership
find . -type f -user olduser -exec chown newuser {} \;

# Find broken symlinks
find . -type l ! -exec test -e {} \; -print

# Find recently modified files and sort by date
find . -type f -mtime -1 -exec ls -lt {} + | head -20
```

**Original Examples**

```bash
find ./ -type f -size +100M
find ./ -type f -name '*.log' -exec rm {} +
find ./ -type f -name "*.log" -mtime +3 -exec rm {} +
find ./ -type f -name "*.log" -mtime +365 -delete
```