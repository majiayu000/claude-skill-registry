---
name: shell-script-development
description: This skill should be used when the user asks to "create a bash script", "write a shell script", or mentions shell scripting conventions.
---

# Shell Script Development

Create shell scripts following consistent conventions.

## Template

```bash
#!/usr/bin/env bash

set -e -o pipefail

# Colors
green='\033[0;32m'
red='\033[0;31m'
yellow='\033[1;33m'
blue='\033[0;34m'
nc='\033[0m'

# Script logic here

echo -e "${green}✔${nc} completed successfully"
```

## Conventions

| Element | Convention |
|---------|------------|
| Shebang | `#!/usr/bin/env bash` |
| Safety | `set -e -o pipefail` |
| Local variables | Lowercase (`model`, `dir`, `count`) |
| Environment variables | Uppercase (`PATH`, `HOME`, `USER`) |
| Color variables | Lowercase (`green`, `red`, `nc`) |
| Status words | Lowercase (`error`, `warning`, `note`) |

## Status Output Patterns

```bash
echo -e "${green}✔${nc} task completed"           # success
echo -e "${red}error${nc}: something failed"      # error
echo -e "${yellow}warning${nc}: something to note" # warning
echo -e "${blue}info${nc}: informational message"  # info
```

## Important

After creating or modifying shell scripts, inform the user:

> **Make executable.** Run `chmod +x script.sh` before use.
