---
name: cpc
description: "Copy text to clipboard via pbcopy. Triggers on keywords: copy, clipboard, pbcopy, cpc"
project-agnostic: true
allowed-tools:
  - Bash
---

# CPC - Copy to Clipboard

Copies provided text to the macOS clipboard.

## Usage

```
/cpc <text to copy>
```

## Implementation

Execute:
```bash
cat << 'EOF' | pbcopy
$ARGUMENTS
EOF
```

Report: "Copied to clipboard."
