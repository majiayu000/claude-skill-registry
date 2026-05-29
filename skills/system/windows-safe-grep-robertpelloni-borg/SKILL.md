---
name: windows-safe-grep
description: Use when grep/ripgrep fails on Windows due to paths with backslash-space sequences creating malformed paths like 'nul' from \n+ul
---

# Windows-Safe Grep Skill

## Problem

On Windows, paths containing backslash-space sequences (e.g., `D:\Projects\Vibe Code\isometricid`) can cause ripgrep to fail because:
- The `\n` in `isometricid` is interpreted as a newline character
- Combined with the following `ul`, this creates a reference to the reserved Windows device name `nul`
- Error: `rg: D:\Projects\Vibe Code\isometricid\nul: Incorrect function. (os error 1)`

## Solution

Use bash commands with proper path quoting to work around this Windows-specific issue:

### Safe Grep Command Pattern

```bash
rg --fixed-strings "SEARCH_TERM" "/d/Projects/Vibe Code/isometricid"
```

Or use forward slashes and proper quoting:

```bash
rg --fixed-strings "SEARCH_TERM" "$(cygpath -u "D:\Projects\Vibe Code\isometricid")"
```

### Alternative: Use find + grep

```bash
find "/d/Projects/Vibe Code/isometricid" -type f \( -name "*.ts" -o -name "*.js" -o -name "*.tsx" -o -name "*.jsx" \) -exec grep -H --line-number "SEARCH_TERM" {} \;
```

## Usage

When grep fails with "Incorrect function (os error 1)" on Windows:

1. Use this skill
2. Replace the path with forward slashes: `D:\Projects\Vibe Code\isometricid` → `/d/Projects/Vibe Code/isometricid`
3. Or use the bash command pattern with proper quoting

## Example

```bash
rg --fixed-strings "polar_product_id" "/d/Projects/Vibe Code/isometricid/src"
```
