---
name: windows-path-troubleshooting
description: "Complete Windows file path troubleshooting knowledge for Claude Code on Git Bash and Windows environments. PROACTIVELY activate for: (1) File path errors on Windows, (2) Backslash vs forward slash issues, (3) Edit/Write/Read tool failures, (4) MINGW path resolution, (5) Cross-platform path conversion."
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Windows Path Troubleshooting for Claude Code

## 🚨 CRITICAL: Always Use Backslashes on Windows for File Paths

**MANDATORY: When using Edit, Write, or Read tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).**

### The Rule

**Windows File Path Requirements:**
- ✅ **CORRECT**: `D:\repos\project\file.tsx`
- ❌ **WRONG**: `D:/repos/project/file.tsx`

**This applies to:**
- Edit tool `file_path` parameter
- Write tool `file_path` parameter
- Read tool `file_path` parameter
- All file operations on Windows systems

### Why This Matters

**Common error message when using forward slashes on Windows:**
```
Error: ENOENT: no such file or directory
```

**Root cause:**
- Windows native file system uses backslashes (`\`) as path separators
- Forward slashes (`/`) work in some Windows contexts but NOT in Claude Code file tools
- Git Bash displays paths with forward slashes but Windows APIs require backslashes
- Claude Code's Read/Write/Edit tools use Windows native APIs that expect backslashes

## 🔍 Common Windows Path Issues in Claude Code

### Issue 1: Forward Slashes in Tool Calls

**Symptom:**
```
Edit tool fails with "file not found" or "no such file or directory"
```

**Cause:**
Using forward slashes copied from Git Bash output:
```bash
# Git Bash shows:
/s/repos/claude-plugin-marketplace/file.tsx
```

**Incorrect usage:**
```
Edit(file_path="/s/repos/myproject/file.tsx")
```

**Correct usage:**
```
Edit(file_path="S:\repos\myproject\file.tsx")
```

**Solution steps:**
1. Identify the Windows drive letter (e.g., `/s/` → `S:`)
2. Replace forward slashes with backslashes
3. Add drive letter with colon
4. Use absolute Windows path format

### Issue 2: Git Bash MINGW Path Format

**Symptom:**
Paths like `/s/repos/` or `/c/Users/` don't work in Edit/Write/Read tools

**MINGW path format explained:**
- Git Bash uses POSIX-style paths on Windows
- Drive letters are represented as `/c/`, `/d/`, `/s/`, etc.
- These are MINGW virtual paths, not Windows paths
- Claude Code tools need Windows-native paths

**Conversion table:**
| Git Bash (MINGW) | Windows Native |
|------------------|----------------|
| `/c/Users/name/` | `C:\Users\name\` |
| `/d/repos/project/` | `D:\repos\project\` |
| `/s/work/code/` | `S:\work\code\` |
| `/mnt/c/Windows/` | `C:\Windows\` |

**Conversion algorithm:**
1. Extract drive letter from first path segment (e.g., `/s/` → `S`)
2. Add colon to drive letter (e.g., `S` → `S:`)
3. Replace remaining forward slashes with backslashes
4. Combine: `S:` + `\repos\project\file.tsx`

### Issue 3: Relative Paths in Git Bash

**Symptom:**
Relative paths from Git Bash don't resolve correctly in Claude Code tools

**Cause:**
Git Bash current working directory uses MINGW format, but Claude Code tools use Windows format

**Example scenario:**
```bash
# In Git Bash:
pwd
# Shows: /s/repos/my-project

# User provides relative path:
./src/components/Button.tsx
```

**Problem:**
Claude Code can't resolve `./src/` from MINGW `/s/repos/my-project`

**Solution:**
1. Get the full Windows path from Git Bash:
   ```bash
   pwd -W
   # Shows: S:/repos/my-project (Windows format with forward slashes)
   ```
2. Convert to proper Windows path: `S:\repos\my-project`
3. Append relative path with backslashes: `S:\repos\my-project\src\components\Button.tsx`

### Issue 4: Environment Variable Expansion

**Symptom:**
Paths with environment variables like `$HOME` or `%USERPROFILE%` fail

**Git Bash environment variables:**
```bash
echo $HOME
# Shows: /c/Users/username (MINGW format)
```

**Windows environment variables:**
```cmd
echo %USERPROFILE%
# Shows: C:\Users\username (Windows format)
```

**Best practice:**
- Avoid environment variables in file paths for Claude Code tools
- Use absolute Windows paths instead
- If user provides `$HOME`, ask them to run `echo $HOME` and convert the result

### Issue 5: Spaces in File Paths

**Symptom:**
Paths with spaces break or cause "file not found" errors

**Correct handling:**
```
✅ CORRECT: Edit(file_path="C:\Program Files\My App\config.json")
✅ CORRECT: Edit(file_path="D:\My Documents\project\file.txt")
```

**Notes:**
- Do NOT add quotes around the path in the parameter
- The tool call itself handles escaping
- Spaces are fine in Windows paths when using backslashes

### Issue 6: UNC Network Paths

**Symptom:**
Network paths like `\\server\share\file.txt` fail

**Windows UNC format:**
```
\\server\share\folder\file.txt
```

**Git Bash representation:**
```
//server/share/folder/file.txt
```

**Correct usage in Claude Code:**
```
Edit(file_path="\\\\server\\share\\folder\\file.txt")
```

**Note:** Backslashes must be doubled in some contexts due to escaping, but Claude Code tools handle this automatically.

## 🔧 Path Detection and Conversion Algorithm

When a user provides a file path, follow this decision tree:

### Step 1: Identify Path Format

**MINGW Path (Git Bash):**
- Starts with `/` followed by single letter and `/` (e.g., `/c/`, `/s/`)
- Example: `/s/repos/project/file.tsx`
- **Action:** Convert to Windows format

**Windows Path:**
- Starts with drive letter and colon (e.g., `C:`, `D:`)
- Uses backslashes or forward slashes
- Example: `S:\repos\project\file.tsx` or `S:/repos/project/file.tsx`
- **Action:** Ensure backslashes are used

**Relative Path:**
- Starts with `./` or `../` or just filename
- Example: `./src/components/Button.tsx`
- **Action:** Request full path from user or detect current directory

**UNC Path:**
- Starts with `\\` or `//`
- Example: `\\server\share\file.txt`
- **Action:** Ensure backslashes are used

### Step 2: Conversion Process

**For MINGW paths (`/x/...`):**
```
Input: /s/repos/myproject/src/components/Button.tsx

Process:
1. Extract drive letter: "s"
2. Uppercase: "S"
3. Add colon: "S:"
4. Replace remaining slashes: \repos\myproject\src\components\Button.tsx
5. Combine: S:\repos\myproject\src\components\Button.tsx

Output: S:\repos\myproject\src\components\Button.tsx
```

**For Windows paths with forward slashes (`X:/...`):**
```
Input: S:/repos/project/file.tsx

Process:
1. Detect drive letter already present: "S:"
2. Replace forward slashes with backslashes: \repos\project\file.tsx
3. Combine: S:\repos\project\file.tsx

Output: S:\repos\project\file.tsx
```

**For relative paths:**
```
Input: ./src/components/Button.tsx
Current directory (from user or detection): S:\repos\my-project

Process:
1. Remove ./ prefix
2. Replace forward slashes: src\components\Button.tsx
3. Combine with current directory: S:\repos\my-project\src\components\Button.tsx

Output: S:\repos\my-project\src\components\Button.tsx
```

## 🛠️ Interactive Path Fixing Workflow

When you encounter a file path error on Windows:

### Step 1: Detect the Error

**Error indicators:**
- "ENOENT: no such file or directory"
- "file not found"
- Edit/Write/Read tool failure
- User mentions "Windows" or "Git Bash"

### Step 2: Analyze the Path

**Ask yourself:**
1. Was the path provided by the user in MINGW format?
2. Does the path use forward slashes?
3. Is it a relative path?
4. Did I receive the path from a Git Bash command output?

### Step 3: Request Clarification (If Needed)

**If the path is ambiguous, ask:**
```
I see you're working on Windows with Git Bash. To ensure I use the correct path format,
could you run this command and share the output?

pwd -W

This will give me the Windows-formatted path.
```

### Step 4: Convert and Retry

**Conversion template:**
```
I'll convert the path from Git Bash format to Windows format:
- Git Bash: /s/repos/project/file.tsx
- Windows: S:\repos\project\file.tsx

Retrying with the correct Windows path...
```

### Step 5: Verify Success

After conversion, verify the operation succeeded and explain what was fixed:
```
✅ Successfully edited the file using the Windows path format (S:\repos\...).

Note: On Windows with Git Bash, always use backslashes (\) in file paths for
Claude Code's Edit/Write/Read tools, even though Git Bash displays paths with
forward slashes (/).
```

## 📋 Troubleshooting Checklist

When file operations fail on Windows:

- [ ] **Check path separator**: Are backslashes (`\`) used instead of forward slashes (`/`)?
- [ ] **Check drive letter format**: Is it `C:` not `/c/`?
- [ ] **Check MINGW conversion**: Did you convert `/x/path` to `X:\path`?
- [ ] **Check relative vs absolute**: Is the path absolute starting with drive letter?
- [ ] **Check environment variables**: Did you expand `$HOME` or `%USERPROFILE%`?
- [ ] **Check spaces**: Are spaces in the path handled correctly?
- [ ] **Check UNC paths**: Are network paths using `\\server\share` format?
- [ ] **Check file existence**: Does the file actually exist at that path?

## 🎯 Quick Reference: Path Conversion Examples

| Context | Path Format | Claude Code Tool Format |
|---------|-------------|-------------------------|
| Git Bash pwd | `/s/repos/project` | `S:\repos\project` |
| Git Bash relative | `./src/file.tsx` | `S:\repos\project\src\file.tsx` |
| Windows Explorer | `S:\repos\project\file.tsx` | `S:\repos\project\file.tsx` ✅ |
| Windows with `/` | `S:/repos/project/file.tsx` | `S:\repos\project\file.tsx` |
| MINGW full path | `/c/Users/name/file.txt` | `C:\Users\name\file.txt` |
| Network share (Git Bash) | `//server/share/file.txt` | `\\server\share\file.txt` |
| WSL path | `/mnt/c/repos/project` | `C:\repos\project` |

## 🚀 Best Practices for Windows File Operations

### 1. Always Convert Paths Proactively

**Don't wait for errors** - If you see a path that looks like MINGW format, convert it immediately:

```
User provides: /s/repos/project/file.tsx
You think: "This is MINGW format, I need to convert it to S:\repos\project\file.tsx"
You do: Convert before calling Edit/Write/Read tool
```

### 2. Use pwd -W in Git Bash

**When you need current directory on Windows:**
```bash
# Instead of:
pwd                    # Shows: /s/repos/project (MINGW format)

# Use:
pwd -W                 # Shows: S:/repos/project (Windows format with /)
```

Then convert the forward slashes to backslashes.

### 3. Communicate Path Format Changes

**Always explain when you convert paths:**
```
I'll convert the Git Bash path to Windows format for the Edit tool:
- From: /s/repos/project/file.tsx
- To: S:\repos\project\file.tsx
```

This helps users understand the requirement and learn for future interactions.

### 4. Validate Before Tool Use

**Before calling Edit/Write/Read tools on Windows:**
```
Pre-flight checklist:
✅ Path starts with drive letter and colon (e.g., C:, S:)
✅ Path uses backslashes (\) not forward slashes (/)
✅ Path is absolute, not relative
✅ No MINGW format (no /c/, /s/, etc.)
```

### 5. Handle User-Provided Paths Carefully

**User might provide paths in various formats:**
- Copy-pasted from Git Bash (MINGW format)
- Copy-pasted from Windows Explorer (Windows format)
- Typed manually (could be either)
- From command output (varies by tool)

**Always detect and convert as needed.**

## 🐛 Common Error Messages and Solutions

### Error: "ENOENT: no such file or directory"

**Most likely cause:** Forward slashes instead of backslashes

**Solution:**
1. Check if path uses forward slashes
2. Convert to backslashes
3. Verify drive letter format
4. Retry operation

### Error: "Invalid file path"

**Most likely cause:** MINGW path format

**Solution:**
1. Detect `/x/` pattern at start
2. Convert to `X:` format
3. Replace all forward slashes with backslashes
4. Retry operation

### Error: "Access denied" or "Permission denied"

**Most likely cause:** Path is correct but permissions issue

**Solution:**
1. Verify file exists and is accessible
2. Check if file is locked by another process
3. Verify user has read/write permissions
4. Consider running Git Bash as administrator

### Error: "File not found" but path looks correct

**Possible causes:**
1. Path has hidden characters (copy-paste issue)
2. File extension is hidden in Windows
3. Path has trailing spaces
4. Case sensitivity (some tools are case-sensitive)

**Solution:**
1. Ask user to run `ls -la` in Git Bash to verify exact filename
2. Check for file extensions
3. Trim whitespace from path
4. Match exact case of filename

## 📚 Platform-Specific Knowledge

### Windows File System Characteristics

**Path characteristics:**
- Drive letters: A-Z (typically C: for system, D-Z for additional drives)
- Path separator: Backslash (`\`)
- Case insensitive: `File.txt` same as `file.txt`
- Special characters: Avoid `< > : " | ? *` in filenames
- Maximum path length: 260 characters (legacy limit, can be increased)

### Git Bash on Windows

**Git Bash is a POSIX-compatible environment:**
- Uses MINGW (Minimalist GNU for Windows)
- Translates POSIX paths to Windows paths internally
- Commands like `ls`, `pwd`, `cd` use POSIX format
- Native Windows programs need Windows format paths

**Key insight:** Git Bash displays and accepts POSIX paths, but Windows APIs (used by Claude Code) require Windows paths.

### WSL (Windows Subsystem for Linux)

**WSL path mounting:**
- Windows drives mounted at `/mnt/c/`, `/mnt/d/`, etc.
- WSL path: `/mnt/c/Users/name/project`
- Windows path: `C:\Users\name\project`

**Conversion:**
1. Replace `/mnt/x/` with `X:`
2. Replace forward slashes with backslashes

## 🎓 Teaching Users

When explaining path issues to users, use this template:

```
I encountered a path format issue. Here's what happened:

**The Problem:**
Claude Code's file tools (Edit, Write, Read) on Windows require paths in Windows
native format with backslashes (\), but Git Bash displays paths in POSIX format
with forward slashes (/).

**The Path Formats:**
- Git Bash shows: /s/repos/project/file.tsx
- Windows needs: S:\repos\project\file.tsx

**The Solution:**
I've converted your path to Windows format. For future reference, when working
with Claude Code on Windows with Git Bash:
1. Use backslashes (\) in file paths
2. Use drive letter format (C:, D:, S:) not MINGW format (/c/, /d/, /s/)
3. Run `pwd -W` in Git Bash to get Windows-formatted paths

**The Fix:**
✅ Now using: S:\repos\project\file.tsx
```

## 🔍 Advanced Scenarios

### Scenario 1: Mixed Path Contexts

**User is working with both WSL and Git Bash:**
- Ask which environment they're in
- Use appropriate conversion
- Document the choice

### Scenario 2: Symbolic Links

**Windows symbolic links:**
```
mklink /D C:\link C:\target
```

**Handling:**
- Follow the link to actual path
- Use actual path in tool calls
- Inform user if link resolution needed

### Scenario 3: Docker Volumes

**Docker volume mounts on Windows:**
```
docker run -v C:\repos:/app
```

**Path translation:**
- Outside container: `C:\repos\file.txt`
- Inside container: `/app/file.txt`
- Use context-appropriate format

## ✅ Success Criteria

You've successfully handled Windows paths when:

1. ✅ All Edit/Write/Read tool calls use backslashes on Windows
2. ✅ MINGW paths are converted before tool use
3. ✅ Relative paths are resolved to absolute Windows paths
4. ✅ User understands why conversion was necessary
5. ✅ File operations succeed without path-related errors
6. ✅ Path format is consistent throughout the session

## 🆘 When to Use This Skill

**PROACTIVELY apply this knowledge when:**
1. User mentions they're on Windows
2. User mentions Git Bash or MINGW
3. You see paths starting with `/c/`, `/s/`, etc.
4. Edit/Write/Read tool fails with "file not found"
5. User provides paths with forward slashes on Windows
6. You need to read/edit/write files on Windows system

**This skill is CRITICAL for Windows users** - Path format errors are the #1 cause of file operation failures on Windows with Git Bash.
