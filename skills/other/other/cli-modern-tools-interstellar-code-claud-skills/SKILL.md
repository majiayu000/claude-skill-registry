---
name: cli-modern-tools
description: Auto-suggest modern CLI tool alternatives (bat, eza, fd, ripgrep) for faster, more efficient command-line operations with 50%+ speed improvements
version: 1.1.0
author: Generic Claude Code Framework
tags: [cli, productivity, performance, tools, bat, eza, fd, ripgrep, watchexec]
activation_keywords: cat, ls, find, grep, file viewing, directory listing, file search, watch files
auto-activate: true
feature_config:
  bat: enabled
  eza: enabled
  fd: enabled
  ripgrep: enabled
  watchexec: enabled
---

# CLI Modern Tools Skill

**Purpose**: Automatically suggest and use modern CLI alternatives for 50%+ speed improvements and better UX

## ⚠️ **CRITICAL: Claude's Internal Tool Usage**

**Before Claude executes ANY bash command internally, MUST check:**

| If Claude wants to use... | Use this instead | Tool Type |
|---|---|---|
| `bash find . -name "*.js"` | **Glob** tool `pattern="**/*.js"` | Claude Code Tool |
| `bash grep -r "pattern"` | **Grep** tool `pattern="pattern"` | Claude Code Tool |
| `bash cat file.txt` | **Read** tool `file_path="file.txt"` | Claude Code Tool |
| `bash ls -la` | `bash eza --long --git` (if available) | Bash Command |

**Why this matters:**
- Skills only auto-activate on user messages, NOT on Claude's internal tool calls
- Claude must consciously check this table before executing bash commands
- Prevents bypassing token-efficient Claude Code tools

**See CLAUDE.md "Tool Usage Guidelines" for complete replacement rules.**

---

## 🎯 Core Concept

Replace traditional Unix commands with modern, faster, feature-rich alternatives:
- **bat** > cat (syntax highlighting)
- **eza** > ls (git status, icons)
- **fd** > find (18x faster)
- **ripgrep** > grep (10x faster) *[Note: Use Grep tool in Claude Code]*
- **watchexec** for automation

## 🔧 **BASH COMMAND ATTRIBUTION PATTERN**

**CRITICAL: Before executing EACH bash command, MUST output:**
```
🔧 [cli-modern-tools] Running: <command>
```

**Examples:**
```
🔧 [cli-modern-tools] Running: bat app.js
🔧 [cli-modern-tools] Running: eza --long --git
🔧 [cli-modern-tools] Running: fd "\.tsx$"
🔧 [cli-modern-tools] Running: watchexec -e php ./vendor/bin/pest
```

**Why:** This pattern helps users identify which skill is executing which command, improving transparency and debugging.

## 🎨 **VISUAL OUTPUT FORMATTING**

**IMPORTANT: Use MINIMAL colored output (2-3 calls max) to prevent screen flickering!**

### Use Colored-Output Skill

**Example formatted output (MINIMAL PATTERN):**
```bash
# START: Header only
bash .claude/skills/colored-output/color.sh skill-header "cli-modern-tools" "Replacing traditional CLI commands..."

# MIDDLE: Regular text (no colored calls)
Using bat instead of cat for syntax highlighting...
Using eza instead of ls for git status integration...
Using fd instead of find for faster file search...

# END: Result only
bash .claude/skills/colored-output/color.sh success "" "Modern CLI tools applied"
```

**WHY:** Each bash call creates a task in Claude CLI, causing screen flickering. Keep it minimal!

---

## 🚀 Auto-Activation Triggers

**CRITICAL: This skill auto-activates on traditional command detection and AUTOMATICALLY replaces them.**

**⚙️ FEATURE TOGGLE CONTROL:**
Before suggesting any replacement, CHECK the `feature_config` in the frontmatter above:
- If `bat: enabled` → Suggest bat
- If `bat: disabled` → Use traditional cat (no suggestion)
- Same logic for eza, fd, ripgrep, watchexec

### Pattern 1: File Viewing
**Triggers**: `cat`, `view file`, `show file`, `display contents`
**Action**: IF `bat: enabled` → use `bat` instead of `cat`, ELSE use `cat`
**Implementation**:
```bash
# ❌ Traditional
cat app.js

# ✅ Automatic replacement (IF bat: enabled)
bat app.js  # Syntax highlighting, line numbers

# ⬜ Fallback (IF bat: disabled)
cat app.js  # Use traditional command
```

### Pattern 2: Directory Listing
**Triggers**: `ls`, `list files`, `show directory`, `list dir`
**Action**: IF `eza: enabled` → use `eza --long --git` instead of `ls`, ELSE use `ls`
**Implementation**:
```bash
# ❌ Traditional
ls -la app/Models/

# ✅ Automatic replacement (IF eza: enabled)
eza --long --git app/Models/  # Git status, icons, colors

# ⬜ Fallback (IF eza: enabled)
ls -la app/Models/  # Use traditional command
```

### Pattern 3: File Search (Bash Tool Only)
**Triggers**: `find`, `search files`, `locate file`, `find file named`
**Action**: IF `fd: enabled` → use `fd` instead of `find`, ELSE use `find`
**Implementation**:
```bash
# ❌ Traditional
find . -name "*.tsx"

# ✅ Automatic replacement (IF fd: enabled, Bash tool only)
fd "\.tsx$"

# ⬜ Fallback (IF fd: disabled)
find . -name "*.tsx"

# ✅ For Claude Code tools (NOT bash)
# Use Glob tool instead
```

### Pattern 4: Content Search
**Triggers**: `grep`, `search in files`, `search content`, `find text`
**Action**: **ALWAYS use Grep tool**, NEVER bash grep/ripgrep (ripgrep setting ignored for Claude Code tools)
**Implementation**:
```
❌ bash -c "grep -r 'TODO' app/"
✅ [Use Grep tool with pattern="TODO" path="app/"]

Note: ripgrep feature toggle only affects bash command suggestions, not Claude Code tools
```

### Pattern 5: File Watching
**Triggers**: `watch files`, `auto-run`, `continuous testing`, `on file change`
**Action**: IF `watchexec: enabled` → use `watchexec` for automation, ELSE suggest manual approach
**Implementation**:
```bash
# ❌ Traditional (manual)
# Run tests manually after each change

# ✅ Automatic replacement (IF watchexec: enabled)
watchexec -e php ./vendor/bin/pest

# ⬜ Fallback (IF watchexec: disabled)
# Suggest manual approach
```

### Pattern 6: Tree View
**Triggers**: `tree`, `show tree`, `directory structure`
**Action**: IF `eza: enabled` → use `eza --tree` instead of `tree`, ELSE use `tree`
**Implementation**:
```bash
# ❌ Traditional
tree -L 3

# ✅ Automatic replacement (IF eza: enabled)
eza --tree --level=3

# ⬜ Fallback (IF eza: enabled)
tree -L 3
```

## 🎯 Automatic Replacement Rules

### Rule 1: Direct Command Replacement
When user says "cat app.js", Claude should:
1. Detect "cat" keyword → Auto-activate skill
2. Replace with `bat app.js`
3. Execute immediately (no suggestion, just do it)
4. Mention replacement: "Using bat for syntax highlighting"

### Rule 2: Wrapper Script Usage
For explicit automation, use wrapper:
```bash
bash .claude/skills/cli-modern-tools/cli-wrapper.sh view app.js
bash .claude/skills/cli-modern-tools/cli-wrapper.sh list app/
bash .claude/skills/cli-modern-tools/cli-wrapper.sh find "*.tsx"
bash .claude/skills/cli-modern-tools/cli-wrapper.sh check
```

### Rule 3: Fallback Safety
Always check tool availability:
```bash
command -v bat &> /dev/null && bat file.txt || cat file.txt
```

### Rule 4: Context-Aware Replacement
- **Bash Tool**: Replace `find` with `fd`
- **Claude Code Tools**: Use `Glob` tool (not fd, not find)
- **Content Search**: Always use `Grep` tool (never bash grep/rg)

## 📊 Tool Comparison Matrix

| Operation | Traditional | Modern Alternative | Speed Improvement | UX Improvement |
|-----------|-------------|-------------------|-------------------|----------------|
| **View file** | `cat app.js` | `bat app.js` | Same speed | ✅ Syntax highlighting, line numbers |
| **List directory** | `ls -la` | `eza --long --git` | Same speed | ✅ Git status, icons, colors |
| **Find files** | `find . -name "*.js"` | `fd "\.js$"` | **18x faster** | ✅ Simpler syntax, respects .gitignore |
| **Search content** | `grep -r "TODO"` | Grep tool | N/A | ✅ Token efficiency, proper permissions |
| **Watch files** | Manual re-run | `watchexec -e js npm test` | ∞ (automation) | ✅ Auto-run on changes |

## 🔧 Tool Details

### 1. bat (Better cat)

**Install**:
```bash
# Windows
scoop install bat

# Mac
brew install bat

# Linux
apt install bat
```

**Usage**:
```bash
# Basic file viewing with syntax highlighting
bat app/Models/User.php

# Specific line range
bat routes/api.php --line-range 1:50

# Pipe with syntax highlighting
curl http://api.example.com | bat -l json

# Multiple files
bat src/*.js
```

**Features**:
- ✅ Automatic syntax highlighting (200+ languages)
- ✅ Line numbers by default
- ✅ Git diff indicators
- ✅ Non-printable character visibility
- ✅ Automatic paging for long files

**When to Use**:
- ✅ Viewing code files (always prefer over cat)
- ✅ API response inspection (pipe JSON/XML)
- ✅ Log file viewing with highlighting
- ✅ Quick code review

---

### 2. eza (Better ls)

**Install**:
```bash
# Windows
scoop install eza

# Mac
brew install eza

# Linux
cargo install eza
```

**Usage**:
```bash
# Git-aware listing with stats
eza --long --git app/Models/

# Tree view with depth limit
eza --tree --level=3 resources/js/

# Recently modified files
eza --long --sort=modified --reverse

# With icons and colors
eza --long --icons --color=always
```

**Features**:
- ✅ Git status integration (modified, staged, untracked)
- ✅ Human-readable file sizes
- ✅ Icons for file types
- ✅ Color-coded output
- ✅ Extended attributes display

**When to Use**:
- ✅ Exploring git repositories
- ✅ Finding recently modified files
- ✅ Understanding directory structure
- ✅ Visual directory navigation

---

### 3. fd (Better find)

**Install**:
```bash
# Windows
scoop install fd

# Mac
brew install fd

# Linux
apt install fd-find
```

**Usage**:
```bash
# Find TypeScript files
fd "\.tsx$" resources/js/

# Find controller files
fd Controller.php app/Http/Controllers/

# Multiple extensions
fd -e php -e js

# Case-insensitive
fd -i readme

# Ignore .gitignore patterns
fd --no-ignore "test"
```

**Features**:
- ✅ **18x faster than find**
- ✅ Smart case-insensitive search
- ✅ Respects .gitignore by default
- ✅ Simpler syntax than find
- ✅ Parallel execution

**When to Use (in Bash tool only)**:
- ✅ Quick file discovery by name/pattern
- ❌ **NOT for Claude Code tool use** (use Glob tool instead)

**Important**: When using Claude Code tools (not bash), **always prefer Glob tool** over fd.

---

### 4. Grep Tool (NOT bash grep/ripgrep)

**Critical Rule**: In Claude Code, **ALWAYS use Grep tool**, NEVER bash grep or ripgrep.

**Why**:
- ✅ Optimized permissions and access
- ✅ Token-efficient output
- ✅ Proper error handling
- ✅ Integrated with Claude Code

**Usage**:
```
[Use Grep tool with pattern="TODO" path="app/"]
[Use Grep tool with pattern="function" type="ts"]
```

**When to Use**:
- ✅ ANY content search operation in Claude Code
- ✅ Finding code patterns
- ✅ Searching for TODOs, FIXMEs
- ✅ Cross-file text search

---

### 5. watchexec (File Watching Automation)

**Install**:
```bash
# Windows
scoop install watchexec

# Mac
brew install watchexec

# Linux
cargo install watchexec-cli
```

**Usage**:
```bash
# Auto-run PHP tests on changes
watchexec -e php -c ./vendor/bin/pest

# Auto-lint TypeScript on save
watchexec -e tsx,ts -w resources/js/ npm run lint

# Auto-migrate and verify schema
watchexec -w database/migrations/ "php artisan migrate && bash .claude/skills/sql-cli/sql-cli.sh tables"

# Multiple commands with debouncing
watchexec -w src/ "npm run build && npm run test"
```

**Features**:
- ✅ Intelligent file watching
- ✅ Debouncing (prevents multiple rapid runs)
- ✅ Cross-platform support
- ✅ Pattern-based filtering
- ✅ Clear screen between runs

**When to Use**:
- ✅ Continuous testing during development
- ✅ Auto-formatting on save
- ✅ Live documentation generation
- ✅ Database migration monitoring

---

## 🎬 Workflow Examples

### Example 1: Code Review Workflow

**Traditional Approach**:
```bash
cat app/Models/User.php          # No syntax highlighting
ls -la app/Models/               # No git status
find app/ -name "*Controller*"   # Slow, complex syntax
```

**Modern Approach**:
```bash
bat app/Models/User.php                    # ✅ Syntax highlighted
eza --long --git app/Models/               # ✅ Git status visible
fd Controller app/Http/Controllers/        # ✅ 18x faster
```

**Savings**: 50% faster, significantly better UX

---

### Example 2: Development Automation

**Traditional Approach**:
```bash
# Manually re-run tests after each change
./vendor/bin/pest
# ... edit file ...
./vendor/bin/pest
# ... edit file ...
./vendor/bin/pest
```

**Modern Approach**:
```bash
# Set up once, runs automatically
watchexec -e php -c -w tests/,app/ ./vendor/bin/pest
# ... edit file ... tests run automatically
# ... edit file ... tests run automatically
```

**Savings**: Infinite time saved through automation

---

### Example 3: API Response Inspection

**Traditional Approach**:
```bash
curl http://api.example.com/users | cat
# Output: {"users":[{"id":1,"name":"John"}]}
# Hard to read, no formatting
```

**Modern Approach**:
```bash
curl http://api.example.com/users | bat -l json
# Output: Syntax-highlighted, formatted JSON
```

**Savings**: Instant readability

---

## 📈 Performance Benchmarks

### File Search (10,000 files in directory)

| Tool | Time | Result |
|------|------|--------|
| `find . -name "*.js"` | 1.8 seconds | Baseline |
| `fd "\.js$"` | **0.1 seconds** | **18x faster** |

### Directory Listing (500 files)

| Tool | Features | UX Score |
|------|----------|----------|
| `ls -la` | Basic info | ⭐⭐ |
| `eza --long --git` | Git status, icons, colors | ⭐⭐⭐⭐⭐ |

### File Viewing

| Tool | Features | UX Score |
|------|----------|----------|
| `cat` | Plain text | ⭐⭐ |
| `bat` | Syntax highlighting, line numbers, git diff | ⭐⭐⭐⭐⭐ |

---

## 🔄 Auto-Suggestion Logic

### When User Uses Traditional Command

**Pattern**: User mentions `cat <file>`
```
Claude detects "cat" keyword
→ Auto-activate cli-modern-tools skill
→ Suggest: "I'll use bat instead for syntax highlighting"
→ Execute: bat <file>
```

**Pattern**: User mentions `ls` or `ls -la`
```
Claude detects "ls" keyword
→ Auto-activate cli-modern-tools skill
→ Suggest: "I'll use eza with git status"
→ Execute: eza --long --git
```

**Pattern**: User mentions `find . -name`
```
Claude detects "find" keyword
→ Auto-activate cli-modern-tools skill
→ Check context: Bash tool or Claude tool?
→ If Bash tool: Suggest fd
→ If Claude tool: Use Glob tool
```

---

## ⚠️ Important Rules

### ✅ DO Use Modern Tools When:
- User mentions traditional command names
- Better UX significantly helps user
- Tools are available on system
- Speed improvement matters (large directories/files)

### ❌ DON'T Use When:
- Tool not available (fallback to traditional)
- POSIX compliance required (portable scripts)
- Non-development environment
- One-off operation where setup overhead > benefit

### 🔍 Tool Availability Check Pattern:
```bash
# Check if modern tool available, fallback to traditional
command -v bat &> /dev/null && bat file.txt || cat file.txt
command -v eza &> /dev/null && eza -la || ls -la
command -v fd &> /dev/null && fd pattern || find . -name pattern
```

---

## 🎯 Integration with Other Skills

### Works Well With:
- **markdown-helper**: Use bat to view markdown with highlighting before parsing
- **sql-cli**: Use bat to syntax-highlight SQL query results
- **watchexec**: Auto-run markdown-helper on file changes

### Example Combined Workflow:
```bash
# Watch markdown files, auto-lint on changes
watchexec -e md "node ~/.claude/skills/markdown-helper/md-helper.js lint *.md"

# View SQL results with syntax highlighting
bash .claude/skills/sql-cli/sql-cli.sh query "SELECT * FROM users LIMIT 10" | bat -l sql
```

---

## 📦 Installation Guide

### Windows (Scoop)
```powershell
# Install Scoop if not installed
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install tools
scoop install bat eza fd watchexec
```

### Mac (Homebrew)
```bash
# Install tools
brew install bat eza fd ripgrep watchexec
```

### Linux (APT)
```bash
# Install tools
sudo apt install bat fd-find ripgrep
cargo install eza watchexec-cli
```

---

## 🎓 Quick Reference

| I want to... | Use | Instead of |
|--------------|-----|------------|
| View code file | `bat app.js` | `cat app.js` |
| List with git status | `eza --long --git` | `ls -la` |
| Find files by name | `fd "pattern"` (in Bash) | `find . -name "pattern"` |
| Search file contents | Grep tool | `grep -r` or `rg` |
| Auto-run tests | `watchexec -e php ./vendor/bin/pest` | Manual re-run |
| View API response | `curl ... \| bat -l json` | `curl ... \| cat` |
| Recently modified | `eza --sort=modified --reverse` | `ls -lt` |

---

## 📊 Token & Time Savings

### Typical Development Day (10 operations)

**Traditional Approach**:
- 10x `cat` commands: No highlighting, harder to read
- 10x `ls -la`: No git status, manual checking
- 5x `find` commands: 9 seconds total
- Manual test re-runs: 10 minutes context switching

**Modern Approach**:
- 10x `bat` commands: Instant code comprehension
- 10x `eza --long --git`: Instant git status awareness
- 5x `fd` commands: 0.5 seconds total
- `watchexec` automation: 0 context switching

**Daily Savings**:
- **Time**: ~15 minutes/day = 1.25 hours/week
- **Cognitive Load**: Significantly reduced through better UX
- **Speed**: 50-90% faster file operations

---

## 🐛 Troubleshooting

### "Command not found: bat"
**Solution**: Install bat using package manager for your OS

### "Command not found: eza"
**Solution**: Install eza using Cargo or package manager

### "Command not found: fd"
**Solution**: Install fd (may be named `fd-find` on some systems)

### bat shows `cat` behavior
**Solution**: On some Linux systems, bat is installed as `batcat`:
```bash
alias bat='batcat'  # Add to ~/.bashrc
```

---

## 📝 Summary

**This skill provides:**
- ✅ **50%+ speed improvements** for file operations
- ✅ **Automatic modern tool suggestions** when detecting traditional commands
- ✅ **Better UX** through syntax highlighting, git integration, icons
- ✅ **Automation** via watchexec for continuous workflows
- ✅ **Cross-platform** support (Windows, Mac, Linux)
- ✅ **Fallback safety** to traditional tools when modern tools unavailable

**Use modern CLI tools for all file operations in development workflows!**
