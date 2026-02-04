---
name: running-windows-commands-majo
description: |
  Translate Unix commands to Windows equivalents when working on Windows systems. Use when
  paths start with drive letters (B:\, C:\), commands fail with "not recognized" errors, or
  when needing to avoid Unix-specific tools like tail, head, grep, or mkdir -p. Maps common
  Unix commands to PowerShell and CMD alternatives.
metadata:
  author: Mark Joshwel <mark@joshwel.co>
  version: "2026.2.2"
---

# Windows Development Standards (Mark)

**Goal**: Write cross-platform compatible code that recognizes Windows-specific paths and avoids Unix-isms when working on Windows systems.

## When to Use This Skill

- **Working on Windows (win32) systems**
- **Path starts with drive letter** (e.g., `B:\`, `C:\`)
- **Using backslashes in paths** (`\` not `/`)
- **Commands fail with "not recognized" errors**
- **Need to avoid Unix-specific tools** (tail, head, mkdir -p, etc.)
- **Writing cross-platform scripts** that must work on Windows
- **Using PowerShell or cmd.exe**

## When NOT to Use This Skill

- **Working on macOS or Linux exclusively**
- **Using WSL (Windows Subsystem for Linux)** - Unix commands work there
- **Using Git Bash** - Provides Unix tools on Windows
- **Writing Unix-only scripts** for deployment to Linux servers

## Process

1. **Check platform first** - Verify if running on Windows (`win32`)
2. **Identify Windows paths** - Look for drive letters (`B:`, `C:`) and backslashes
3. **Map Unix commands to Windows equivalents**:
   - `mkdir -p` → `New-Item -ItemType Directory -Path "path" -Force`
   - `tail` → `Get-Content file -Tail N`
   - `head` → `Get-Content file -TotalCount N`
   - `cat` → `Get-Content` or `type`
   - `grep` → `Select-String`
   - `find` → `Get-ChildItem -Recurse`
   - `ls` → `Get-ChildItem` or `dir`
   - `rm -rf` → `Remove-Item -Recurse -Force`
   - `cp/mv` → `Copy-Item/Move-Item`
   - `touch` → `New-Item -ItemType File`
   - `which` → `Get-Command` or `where`
   - `pwd` → `Get-Location`
4. **Quote paths with spaces** - Use `"path with spaces"`
5. **Use backslashes** - Even though forward slashes often work
6. **Prefer cross-platform tools** - Python, Node.js when possible
7. **Update AGENTS.md** - Document Windows-specific requirements

## Constraints

- **ALWAYS check platform** before using Unix commands
- **ALWAYS use backslashes** for Windows paths (even though forward slashes often work)
- **ALWAYS quote paths with spaces** to avoid errors
- **NEVER use Unix-isms on Windows**: `tail`, `head`, `mkdir -p`, `grep`, `find` (Unix style)
- **NEVER use `cd` with forward slashes** on Windows cmd (PowerShell is more flexible)
- **Prefer PowerShell** for modern Windows development
- **Prefer Python** for cross-platform scripts over shell

Guidelines for working on Windows systems and avoiding Unix-isms.

## Recognizing Windows Paths

**Windows paths look like:**
```
B:\understanding-skills\majo-skills
C:\Users\Mark\Documents
D:\Projects\my-app
```

**Key indicators:**
- Drive letter followed by colon (`B:`, `C:`, `D:`)
- Backslashes as separators (`\`)
- No leading `/` (that's Unix)

## Common Unix-isms to Avoid

### 1. `mkdir -p`

**❌ WRONG on Windows:**
```bash
mkdir -p B:\path\to\directory
```

**✅ CORRECT on Windows:**
```powershell
# PowerShell
New-Item -ItemType Directory -Path "B:\path\to\directory" -Force

# Or cmd
mkdir "B:\path\to\directory"
```

**Note**: Windows `mkdir` doesn't have `-p` flag. Use `-Force` in PowerShell or just `mkdir` (it creates parent directories by default in PowerShell).

### 2. `tail` and `head`

**❌ WRONG on Windows:**
```bash
tail -n 20 file.txt
head -n 10 file.txt
```

**✅ CORRECT on Windows:**

**PowerShell:**
```powershell
# tail -n 20
Get-Content file.txt -Tail 20

# head -n 10
Get-Content file.txt -TotalCount 10

# Alternative: Select-Object
Get-Content file.txt | Select-Object -Last 20
Get-Content file.txt | Select-Object -First 10
```

**Or use Python:**
```python
# tail -n 20
with open('file.txt') as f:
    lines = f.readlines()
    print(''.join(lines[-20:]))

# head -n 10
with open('file.txt') as f:
    for i, line in enumerate(f):
        if i >= 10:
            break
        print(line, end='')
```

### 3. `cat`

**❌ WRONG on Windows:**
```bash
cat file.txt
```

**✅ CORRECT on Windows:**
```powershell
Get-Content file.txt
# or
type file.txt  # cmd
```

### 4. `grep`

**❌ WRONG on Windows:**
```bash
grep "pattern" file.txt
```

**✅ CORRECT on Windows:**
```powershell
Select-String -Pattern "pattern" -Path file.txt
# or
Get-Content file.txt | Select-String "pattern"
```

### 5. `find`

**❌ WRONG on Windows:**
```bash
find . -name "*.txt"
```

**✅ CORRECT on Windows:**
```powershell
Get-ChildItem -Recurse -Filter "*.txt"
# or
Get-ChildItem -Path . -Recurse -Include "*.txt"
```

### 6. `ls`

**❌ WRONG on Windows:**
```bash
ls -la
```

**✅ CORRECT on Windows:**
```powershell
Get-ChildItem
# or
Get-ChildItem -Force  # includes hidden files
# or
dir  # cmd
```

### 7. `rm -rf`

**❌ WRONG on Windows:**
```bash
rm -rf directory
```

**✅ CORRECT on Windows:**
```powershell
Remove-Item -Recurse -Force directory
# or
rd /s /q directory  # cmd
```

### 8. `cp` and `mv`

**❌ WRONG on Windows:**
```bash
cp file.txt backup.txt
mv old.txt new.txt
```

**✅ CORRECT on Windows:**
```powershell
Copy-Item file.txt backup.txt
Move-Item old.txt new.txt
```

### 9. `touch`

**❌ WRONG on Windows:**
```bash
touch newfile.txt
```

**✅ CORRECT on Windows:**
```powershell
New-Item newfile.txt -ItemType File
# or
"" | Out-File newfile.txt
```

### 10. `chmod`

**❌ WRONG on Windows:**
```bash
chmod +x script.sh
```

**✅ CORRECT on Windows:**
Windows uses ACLs (Access Control Lists) instead of Unix permissions:
```powershell
# View permissions
Get-Acl file.txt

# Set permissions (complex - usually not needed for dev work)
# Use icacls for command-line ACL management
```

**Note**: For scripts, use file extensions (.ps1, .bat, .cmd) instead of chmod.

### 11. `which`

**❌ WRONG on Windows:**
```bash
which python
```

**✅ CORRECT on Windows:**
```powershell
Get-Command python
# or
where python  # cmd
```

### 12. `pwd`

**❌ WRONG on Windows:**
```bash
pwd
```

**✅ CORRECT on Windows:**
```powershell
Get-Location
# or
$PWD  # automatic variable
```

### 13. `cd` with forward slashes

**❌ WRONG on Windows:**
```bash
cd B:/path/to/directory
```

**✅ CORRECT on Windows:**
```powershell
cd B:\path\to\directory
# or
cd "B:\path\to\directory"
```

Windows accepts forward slashes in `cd`, but backslashes are preferred for consistency.

### 14. `&&` and `||`

**❌ WRONG on Windows (cmd):**
```cmd
command1 && command2
```

**✅ CORRECT on Windows:**

**PowerShell:**
```powershell
command1; if ($?) { command2 }
# or use -and/-or operators
```

**cmd:**
```cmd
command1 && command2  # actually works in cmd
```

**Note**: `&&` works in cmd but not in PowerShell. Use semicolons or proper PowerShell syntax.

## Path Handling

### Path Separators

**Always use backslashes for Windows paths:**
```powershell
# ✅ CORRECT
"B:\understanding-skills\majo-skills"

# ❌ WRONG (Unix style)
"B:/understanding-skills/majo-skills"
```

### Quoting Paths

**Quote paths with spaces:**
```powershell
# ✅ CORRECT
cd "C:\Program Files\My App"
Copy-Item "file with spaces.txt" destination

# ❌ WRONG (will fail)
cd C:\Program Files\My App
```

### Environment Variables

**Windows uses `%VAR%` in cmd, `$env:VAR` in PowerShell:**
```powershell
# PowerShell
$env:USERPROFILE
$env:PATH

# cmd
%USERPROFILE%
%PATH%
```

## Cross-Platform Alternatives

When possible, use tools that work on both platforms:

### Python

```python
# Works on Windows, macOS, Linux
import os
import shutil

# mkdir -p equivalent
os.makedirs("path/to/dir", exist_ok=True)

# File operations
shutil.copy("source.txt", "dest.txt")
shutil.move("old.txt", "new.txt")

# Read file
with open("file.txt") as f:
    content = f.read()

# Write file
with open("file.txt", "w") as f:
    f.write("content")
```

### Git Bash

If available, Git Bash provides Unix tools on Windows. However, prefer native PowerShell/cmd when working with Windows paths.

## Quick Reference Table

| Unix Command | Windows PowerShell | Windows cmd |
|--------------|-------------------|-------------|
| `mkdir -p dir` | `New-Item -ItemType Directory dir -Force` | `mkdir dir` |
| `tail -n 20 file` | `Get-Content file -Tail 20` | N/A |
| `head -n 10 file` | `Get-Content file -TotalCount 10` | N/A |
| `cat file` | `Get-Content file` | `type file` |
| `grep pattern file` | `Select-String pattern file` | `findstr pattern file` |
| `find . -name "*.txt"` | `Get-ChildItem -Recurse -Filter "*.txt"` | `dir /s *.txt` |
| `ls -la` | `Get-ChildItem -Force` | `dir /a` |
| `rm -rf dir` | `Remove-Item -Recurse -Force dir` | `rd /s /q dir` |
| `cp src dst` | `Copy-Item src dst` | `copy src dst` |
| `mv src dst` | `Move-Item src dst` | `move src dst` |
| `touch file` | `New-Item file -ItemType File` | `type nul > file` |
| `which cmd` | `Get-Command cmd` | `where cmd` |
| `pwd` | `Get-Location` | `cd` |

## Testing Skills

- **Platform check**: Verify commands work on Windows (`win32`)
- **Path format test**: Use backslashes (`\`) not forward slashes (`/`)
- **Command mapping**: Test Unix → Windows command equivalency
- **Quote handling**: Test paths with spaces are properly quoted
- **Cross-platform**: Verify Python scripts work on both Windows and Unix
- **PowerShell vs cmd**: Know which syntax works in which shell
- **WSL detection**: Don't use Windows workarounds when in WSL (Unix works there)

## Integration

This skill extends `dev-standards-majo`. Always ensure `dev-standards-majo` is loaded for:
- AGENTS.md maintenance
- Universal code principles
- Documentation policies

Works alongside:
- `python-majo` — For Python development on Windows
- `js-bun-majo` — For JavaScript/Bun development on Windows
- `shell-majo` — For shell scripting on Windows (Git Bash/WSL)
- `git-majo` — For git operations on Windows
- `writing-docs-majo` — For writing documentation on Windows

## Important Notes

1. **Always check the platform** before using Unix commands
2. **Use PowerShell** for modern Windows development
3. **Use Python** for cross-platform scripts
4. **Quote paths with spaces** to avoid errors
5. **Use backslashes** for Windows paths (even though forward slashes often work)
