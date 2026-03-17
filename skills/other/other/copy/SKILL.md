---
name: copy
description: Copy content to my clipboard using `pbcopy`.
argument-hint: [content | file path | "last response"]
disable-model-invocation: true
allowed-tools:
  - Bash(pbcopy:*)
  - Read
---

# Copy to Clipboard

## Arguments

```
$ARGUMENTS
```

## Instructions

### No Arguments / "last response"
Copy Claude's last response to the clipboard.

### File Path
If arguments look like a file path (starts with `/`, `~`, `./`, or contains common extensions):
1. Read the file with Read tool
2. Pipe contents to `pbcopy`

### Literal Content
Copy the provided text directly to clipboard.

## Implementation

```bash
pbcopy << 'EOF'
[content to copy]
EOF
```

## Examples

```
/copy                     → copy last response
/copy last response       → copy last response
/copy ~/notes.txt         → copy file contents
/copy Hello, world!       → copy literal text
/copy the function above  → copy referenced code block
```
