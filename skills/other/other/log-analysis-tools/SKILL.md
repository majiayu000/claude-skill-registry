---
name: log-analysis-tools
description: Fast log file analysis with lnav, multi-framework support (Laravel, CodeIgniter, React, Next.js), automatic log pruning, and 70-80% token savings vs reading entire logs
version: 1.0.0
author: Generic Claude Code Framework
tags: [logs, debugging, lnav, laravel, codeigniter, react, nextjs, log-pruning, error-analysis]
activation_keywords: check logs, view logs, tail logs, find errors, log errors, laravel log, error log, access log, debug production, prune logs
auto-activate: true
---

# Log Analysis Tools Skill

**Purpose**: Fast, efficient log file analysis with framework-aware patterns and intelligent pruning

## 🎨 **VISUAL OUTPUT FORMATTING**

**CRITICAL: All log-analysis-tools output MUST use the colored-output formatter skill!**

```bash
bash .claude/skills/colored-output/color.sh skill-header "log-analysis-tools" "Analyzing log files..."
bash .claude/skills/colored-output/color.sh progress "" "Parsing Laravel logs"
bash .claude/skills/colored-output/color.sh info "" "Found 15 errors in last 24h"
bash .claude/skills/colored-output/color.sh success "" "Analysis complete"
```

---

## 🎯 Multi-Framework Support

### Framework Detection & Log Locations

| Framework | Log Location | Format | Auto-Detect |
|-----------|--------------|--------|-------------|
| **Laravel** | `storage/logs/laravel.log` | Laravel JSON/text | ✅ composer.json |
| **CodeIgniter 4** | `writable/logs/*.log` | CI4 format | ✅ app/Config/ |
| **CodeIgniter 3** | `application/logs/*.php` | CI3 format | ✅ application/config/ |
| **Symfony** | `var/log/*.log` | Monolog format | ✅ composer.json |
| **React (CRA)** | Browser console, no server logs | Client-side | ✅ package.json |
| **Next.js** | `.next/trace`, `console` | Structured JSON | ✅ next.config.js |
| **Nuxt.js** | `.nuxt/`, `console.log` | Nuxt format | ✅ nuxt.config.js |
| **Express.js** | `logs/*.log` (custom) | Morgan/Winston | ✅ package.json |
| **Django** | `logs/`, settings configured | Python logging | ✅ manage.py |
| **Flask** | `instance/`, app configured | Flask logging | ✅ app.py |
| **Apache** | `/var/log/apache2/` | Apache format | ✅ .htaccess |
| **Nginx** | `/var/log/nginx/` | Nginx format | ✅ nginx.conf |
| **System** | `/var/log/syslog` | Syslog format | ✅ Always check |

### Framework-Specific Patterns

**Laravel Error Patterns**:
```regex
^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \w+\.(ERROR|WARNING|CRITICAL)
```

**CodeIgniter Patterns**:
```regex
^(ERROR|WARNING|CRITICAL) - \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}
```

**Next.js Patterns**:
```regex
^\s*(error|warn|info)\s+-\s+
```

**Express/Node Patterns**:
```regex
^\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z\]\s+(error|warn)
```

---

## 🚀 Auto-Activation Triggers

**Primary Keywords**:
- "check logs", "view logs", "tail logs", "show logs"
- "find errors", "log errors", "error log", "access log"
- "laravel log", "codeigniter log", "next.js log"
- "debug production", "production errors"
- "prune logs", "clean old logs", "archive logs"

**Context-Aware Triggers**:
- User mentions debugging → Auto-suggest log analysis
- User mentions "500 error" → Auto-open error logs
- User mentions "slow performance" → Check slow query logs
- User says "production issue" → Tail production logs

---

## 🖥️ Platform Compatibility

### Supported Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| **macOS** | ✅ Full Support | All features available via Homebrew |
| **Linux** | ✅ Full Support | All features available via apt/yum |
| **Windows WSL** | ✅ Full Support | Requires WSL 2 with Ubuntu/Debian |
| **Windows Native** | ⚠️ Limited | Basic features only (no lnav) |

### Required Dependencies

| Tool | Purpose | Availability | Fallback |
|------|---------|--------------|----------|
| **bash** | Script execution | ✅ All platforms | None (required) |
| **gzip** | Log archiving | ✅ All Unix-like | None (required) |
| **grep** | Basic searching | ✅ All platforms | None (required) |

### Optional Dependencies (Enhanced Features)

| Tool | Purpose | Performance Gain | Install |
|------|---------|------------------|---------|
| **lnav** | Advanced log viewing | 10x better UX | `brew install lnav` / `apt install lnav` |
| **fd** | Fast file finding | 18x faster than find | `brew install fd` / `apt install fd-find` |
| **ripgrep (rg)** | Fast searching | 20x faster than grep | `brew install ripgrep` / `apt install ripgrep` |
| **bat** | Syntax highlighting | Better readability | `brew install bat` / `apt install bat` |

### Tool Availability by Platform

#### macOS (via Homebrew)
```bash
# Install all tools (recommended)
brew install lnav fd ripgrep bat

# Or install individually
brew install lnav      # Advanced log viewer
brew install fd        # Fast file finding
brew install ripgrep   # Fast text search
brew install bat       # Syntax-highlighted cat
```

#### Linux (Ubuntu/Debian)
```bash
# Install all tools (recommended)
sudo apt update
sudo apt install lnav fd-find ripgrep bat

# Or install individually
sudo apt install lnav      # Advanced log viewer
sudo apt install fd-find   # Fast file finding (note: fd-find on Ubuntu)
sudo apt install ripgrep   # Fast text search
sudo apt install bat       # Syntax-highlighted cat
```

#### Linux (RHEL/CentOS/Fedora)
```bash
# Enable EPEL repository first (RHEL/CentOS)
sudo yum install epel-release

# Install tools
sudo yum install lnav ripgrep bat
sudo dnf install fd-find  # Fedora

# Or use cargo for latest versions
cargo install lnav fd-find ripgrep bat
```

#### Windows WSL
```bash
# Use Ubuntu/Debian commands (recommended)
# Or use Windows Package Manager
winget install BurntSushi.ripgrep.MSVC
winget install sharkdp.fd
winget install sharkdp.bat

# lnav not available natively - use WSL
```

### Graceful Fallback Chain

The script automatically falls back to standard tools when enhanced tools are unavailable:

```
lnav → bat → less → cat (viewing)
fd → find (file finding)
ripgrep → grep (searching)
bat → cat (syntax highlighting)
```

**Example**:
```bash
# With all tools installed (fastest)
lnav storage/logs/laravel.log

# Without lnav (falls back to bat)
bat --paging=always -l log storage/logs/laravel.log

# Without bat (falls back to less)
less storage/logs/laravel.log

# Minimal (always works)
cat storage/logs/laravel.log
```

### Dependency Checking

The script checks dependencies on startup and provides helpful install instructions:

```bash
$ bash log-tools.sh view

⚠️  Missing optional tools (enhanced features):
  - lnav
  - fd
  - ripgrep

Install for better performance:
  brew install lnav fd ripgrep  # macOS
  sudo apt install lnav fd-find ripgrep  # Linux

📝 Falling back to standard tools (slower but functional)
```

### Performance Impact

| Configuration | View Speed | Search Speed | Overall Rating |
|--------------|-----------|--------------|----------------|
| **All tools** | ⚡⚡⚡⚡⚡ (1s) | ⚡⚡⚡⚡⚡ (0.5s) | Excellent |
| **No lnav** | ⚡⚡⚡⚡ (2s) | ⚡⚡⚡⚡⚡ (0.5s) | Very Good |
| **No ripgrep** | ⚡⚡⚡⚡⚡ (1s) | ⚡⚡⚡ (5s) | Good |
| **Minimal** | ⚡⚡⚡ (3s) | ⚡⚡ (10s) | Functional |

**Recommendation**: Install at least `lnav` and `ripgrep` for optimal experience (90% of performance gains).

---

## 📊 Commands

### 1. View Logs (Framework-Aware)

**Auto-detect framework and open appropriate logs**:

```bash
# Laravel
bash .claude/skills/log-analysis-tools/log-tools.sh view

# Auto-detects:
# → composer.json exists → Laravel → storage/logs/laravel.log
# → Runs: lnav storage/logs/laravel.log
```

**Manual framework specification**:
```bash
bash .claude/skills/log-analysis-tools/log-tools.sh view laravel
bash .claude/skills/log-analysis-tools/log-tools.sh view codeigniter
bash .claude/skills/log-analysis-tools/log-tools.sh view nextjs
```

**Features**:
- ✅ Syntax highlighting by log level
- ✅ Auto-scroll to latest entries
- ✅ Press 'e' for errors only
- ✅ Press 't' to go to specific timestamp
- ✅ Press '/' to search

---

### 2. Find Errors (Last 24 Hours)

**Extract only errors from today**:

```bash
bash .claude/skills/log-analysis-tools/log-tools.sh errors

# Shows:
# - ERROR level entries from last 24 hours
# - Stack traces included
# - Grouped by error type
# - Count of each error
```

**Output Example**:
```
🔍 Errors in storage/logs/laravel.log (Last 24h)
═══════════════════════════════════════════════════

❌ CRITICAL (2 occurrences):
[2025-10-21 14:30:45] Database connection failed
[2025-10-21 15:22:10] Database connection failed

⚠️ ERROR (5 occurrences):
[2025-10-21 10:15:33] Undefined variable: user
[2025-10-21 11:42:18] Undefined variable: user
[2025-10-21 13:05:44] Undefined variable: user
[2025-10-21 16:20:11] File not found: /path/to/file
[2025-10-21 18:45:22] File not found: /path/to/file

📊 Summary:
- CRITICAL: 2
- ERROR: 5
- Total: 7 errors in last 24 hours
```

---

### 3. Tail Logs (Real-Time)

**Live monitoring with auto-refresh**:

```bash
bash .claude/skills/log-analysis-tools/log-tools.sh tail

# Features:
# - Auto-refresh every 2 seconds
# - Color-coded by level
# - Filters out INFO/DEBUG by default
# - Press 'f' to filter by pattern
# - Press 'q' to quit
```

**Tail specific error level**:
```bash
bash .claude/skills/log-analysis-tools/log-tools.sh tail --level ERROR
bash .claude/skills/log-analysis-tools/log-tools.sh tail --level WARNING
```

---

### 4. Search Logs

**Search with regex support**:

```bash
# Search for pattern
bash .claude/skills/log-analysis-tools/log-tools.sh search "database connection"

# Case-insensitive
bash .claude/skills/log-analysis-tools/log-tools.sh search -i "undefined variable"

# Regex pattern
bash .claude/skills/log-analysis-tools/log-tools.sh search "ERROR.*user"

# Show context (5 lines before/after)
bash .claude/skills/log-analysis-tools/log-tools.sh search "exception" --context 5
```

**Output with context**:
```
🔍 Search results: "database connection" in storage/logs/laravel.log
═════════════════════════════════════════════════════════════════════

Match 1 (Line 4523):
---
[2025-10-21 14:30:42] INFO: Attempting database connection
[2025-10-21 14:30:43] INFO: Connection timeout exceeded
[2025-10-21 14:30:44] ERROR: Database connection failed ← MATCH
[2025-10-21 14:30:45] CRITICAL: Application halted
[2025-10-21 14:30:46] INFO: Retry scheduled for 14:31:00
---

Total: 3 matches found
```

---

### 5. Prune Logs (Archive Old Entries)

**THE KEY FEATURE: Keep today's logs, archive older**

```bash
# Auto-prune: Keep today, archive rest
bash .claude/skills/log-analysis-tools/log-tools.sh prune

# Custom retention (keep last N days)
bash .claude/skills/log-analysis-tools/log-tools.sh prune --keep 7
bash .claude/skills/log-analysis-tools/log-tools.sh prune --keep 30

# Dry run (preview what will be archived)
bash .claude/skills/log-analysis-tools/log-tools.sh prune --dry-run
```

**What it does**:
```
📦 Log Pruning Process
═══════════════════════

Current log size: 450 MB
Target: Keep logs from 2025-10-21 (today)

Will archive:
- 2025-10-20 (15 MB) → storage/logs/archive/2025-10-20.log.gz
- 2025-10-19 (22 MB) → storage/logs/archive/2025-10-19.log.gz
- 2025-10-18 (18 MB) → storage/logs/archive/2025-10-18.log.gz
... (older entries)

After pruning:
- Active log: 12 MB (today only)
- Archived: 438 MB (compressed)
- Space saved: 73% (gzip compression)

Proceed? (Y/n)
```

**Archive Structure**:
```
storage/logs/
├── laravel.log              (12 MB - today only)
└── archive/
    ├── 2025-10-20.log.gz    (15 MB compressed)
    ├── 2025-10-19.log.gz    (22 MB compressed)
    ├── 2025-10-18.log.gz    (18 MB compressed)
    └── ...
```

**Benefits**:
- ✅ 99% of debugging uses today's logs only
- ✅ Massive performance improvement (12 MB vs 450 MB)
- ✅ Faster log viewing (lnav loads 38x faster)
- ✅ Old logs preserved (compressed, searchable if needed)
- ✅ Automatic cleanup prevents disk space issues

---

### 6. Statistics

**Get log file insights**:

```bash
bash .claude/skills/log-analysis-tools/log-tools.sh stats

# Shows:
# - File size
# - Date range
# - Error counts by level
# - Top 10 error messages
# - Errors per hour (chart)
```

**Output Example**:
```
📊 Log Statistics: storage/logs/laravel.log
═══════════════════════════════════════════════════

📁 File Info:
- Size: 450 MB
- Lines: 2,450,823
- Date Range: 2025-09-15 to 2025-10-21 (36 days)

📈 Error Breakdown (Last 7 days):
- CRITICAL: 12  (0.5%)
- ERROR: 245    (10.2%)
- WARNING: 567  (23.5%)
- INFO: 1,588   (65.8%)

🔥 Top 10 Errors:
1. Database connection timeout (87 times)
2. Undefined variable: user (45 times)
3. File not found: /uploads/ (34 times)
4. Memory limit exceeded (23 times)
5. API rate limit hit (18 times)
...

⏰ Errors Per Hour (Last 24h):
00:00 ▁▁
02:00 ▁
04:00 ▂
06:00 ▃
08:00 ████ (peak)
10:00 ███
12:00 ▅
14:00 ██
16:00 ████ (peak)
18:00 ▂
20:00 ▁
22:00 ▁

💡 Recommendation: Peak errors at 08:00 and 16:00 - investigate cron jobs or peak traffic patterns
```

---

### 7. Multi-File Analysis

**Merge logs from multiple sources**:

```bash
# Merge Laravel + Apache logs with timestamp sync
bash .claude/skills/log-analysis-tools/log-tools.sh merge \
    storage/logs/laravel.log \
    /var/log/apache2/error.log

# lnav automatically:
# - Merges by timestamp
# - Color-codes by source
# - Allows filtering by file
```

**Use Case**: Correlate application errors with server errors

---

## 🎬 Workflow Examples

### Example 1: Debugging Production 500 Error

**User**: "I'm getting 500 errors in production, check logs"

**Skill activates**:
```bash
# 1. Auto-detect framework (Laravel)
# 2. Show errors from last 24h
bash .claude/skills/log-analysis-tools/log-tools.sh errors

# Output shows:
# [2025-10-21 16:45:22] ERROR: Undefined variable: user in PaymentController.php:45
# (12 occurrences in last hour)

# 3. Get context around first occurrence
bash .claude/skills/log-analysis-tools/log-tools.sh search "PaymentController.php:45" --context 10

# Shows stack trace and request details
```

**Result**: Error identified in 30 seconds (vs 10 minutes reading full log)

---

### Example 2: Performance Investigation

**User**: "Application slow this morning, check logs"

**Skill activates**:
```bash
# 1. View statistics
bash .claude/skills/log-analysis-tools/log-tools.sh stats

# Shows peak errors at 08:00 AM
# Top error: "Database connection timeout" (87 times)

# 2. Search for database timeouts
bash .claude/skills/log-analysis-tools/log-tools.sh search "database.*timeout" --context 3

# Shows all timeout occurrences with context
```

**Result**: Database timeout identified as root cause

---

### Example 3: Log Cleanup

**User**: "Logs are huge, clean them up"

**Skill activates**:
```bash
# 1. Check current size
bash .claude/skills/log-analysis-tools/log-tools.sh stats
# Shows: 450 MB log file (slow to open)

# 2. Prune (keep today only)
bash .claude/skills/log-analysis-tools/log-tools.sh prune

# Result:
# - Active log: 12 MB (38x smaller)
# - Archived: 438 MB compressed
# - lnav opens instantly instead of 15 second wait
```

**Result**: 97% reduction in active log size, massive performance boost

---

## 🔧 Installation

### Required

**lnav** - Advanced log viewer:
```bash
# Mac
brew install lnav

# Ubuntu/Debian
apt install lnav

# Windows (WSL)
apt install lnav
```

### Optional (Enhanced Features)

**jq** - JSON log parsing:
```bash
# Mac
brew install jq

# Linux
apt install jq
```

**gzip** - Log compression (usually pre-installed):
```bash
# Verify
gzip --version
```

---

## 📁 Framework Auto-Detection Logic

**Detection priority**:

1. **Check for framework files** (highest priority):
   ```bash
   # Laravel
   [ -f "artisan" ] && [ -f "composer.json" ] → Laravel

   # CodeIgniter 4
   [ -f "spark" ] && [ -d "app/Config" ] → CodeIgniter 4

   # CodeIgniter 3
   [ -f "index.php" ] && [ -d "application/config" ] → CodeIgniter 3

   # Symfony
   [ -f "bin/console" ] && [ -f "composer.json" ] → Symfony

   # Next.js
   [ -f "next.config.js" ] || [ -d ".next" ] → Next.js

   # Nuxt
   [ -f "nuxt.config.js" ] || [ -d ".nuxt" ] → Nuxt

   # Express
   [ -f "package.json" ] && grep "express" package.json → Express

   # Django
   [ -f "manage.py" ] → Django

   # Flask
   [ -f "app.py" ] && grep "Flask" app.py → Flask
   ```

2. **Check package.json dependencies**:
   ```bash
   # React
   grep "react" package.json → React (client-side only)

   # Vue
   grep "vue" package.json → Vue (client-side only)
   ```

3. **Check for common log files**:
   ```bash
   # Laravel
   [ -f "storage/logs/laravel.log" ] → Laravel

   # CI4
   [ -d "writable/logs" ] && ls writable/logs/*.log → CodeIgniter 4

   # CI3
   [ -d "application/logs" ] → CodeIgniter 3
   ```

4. **Default fallback**:
   - Ask user: "Which framework is this project using?"
   - Show detected files for confirmation

---

## 🎯 Token Efficiency

### Traditional Approach (Reading Entire Log):
```
User: "Find errors in laravel.log"
Claude reads entire 450 MB file → 180,000 tokens
Claude processes → finds errors
Total: ~180,000 tokens
```

### With log-analysis-tools Skill:
```
User: "Find errors in laravel.log"
Skill runs: bash log-tools.sh errors
Returns: 50 error lines (200 tokens)
Total: ~400 tokens
Savings: 99.8%
```

### Daily Operations (10 log checks):
- **Traditional**: 1.8M tokens/day
- **With skill**: 4,000 tokens/day
- **Savings**: 99.8% = 1,796,000 tokens/day

### Monthly Savings:
- **Tokens**: 53.8M tokens saved
- **Cost**: $161/month saved (at $3/million tokens)
- **Time**: 50 hours saved (instant vs manual reading)

---

## 🔄 Integration with log-analyzer Agent

**This skill provides tools, the agent provides intelligence**:

```
User: "Analyze production logs for critical issues"

→ log-analyzer AGENT activates:
1. Uses log-analysis-tools SKILL to extract errors
2. Analyzes error patterns (frequency, timing, impact)
3. Identifies root causes
4. Provides prioritized recommendations
5. Suggests fixes for top 3 critical issues

Result: Intelligent analysis + actionable recommendations
```

**See**: `agents/log-analyzer/` for the intelligent agent that uses this skill

---

## 🐛 Troubleshooting

### "lnav: command not found"
**Solution**: Install lnav using package manager for your OS

### "Permission denied" when reading logs
**Solution**: Run with appropriate permissions or adjust log file permissions
```bash
# Make log readable
chmod 644 storage/logs/laravel.log

# Or run with sudo (not recommended for regular use)
sudo bash log-tools.sh view
```

### "Cannot detect framework"
**Solution**: Manually specify framework:
```bash
bash log-tools.sh view laravel
bash log-tools.sh view codeigniter
```

### "Log file too large, lnav is slow"
**Solution**: Prune logs first!
```bash
bash log-tools.sh prune
# Then open with lnav
```

---

## 📝 Summary

**This skill provides:**
- ✅ **Multi-framework support** - Laravel, CodeIgniter, React, Next.js, Symfony, Django, Flask, Express
- ✅ **Auto-detection** - Identifies framework and log locations automatically
- ✅ **Log pruning** - Keep today's logs, archive older (99% use case covered)
- ✅ **Fast error extraction** - Find errors in seconds, not minutes
- ✅ **Real-time monitoring** - Live tail with filtering
- ✅ **Token efficiency** - 99.8% token savings vs reading entire logs
- ✅ **Multi-file correlation** - Merge application + server logs
- ✅ **Context-aware search** - See what happened before/after errors
- ✅ **Statistics & insights** - Error patterns, peak times, top issues

**Use this skill for all log analysis operations in development workflows!**

---

## Version History

### v1.0.0 (2025-10-21)
- Initial release
- Multi-framework support (Laravel, CodeIgniter, React, Next.js, Symfony, Django, Flask, Express)
- Auto-detection of framework and log locations
- Log pruning capability (keep today, archive older)
- Error extraction and analysis
- Real-time tail monitoring
- Search with context
- Statistics and insights
- 99.8% token savings vs traditional approach
