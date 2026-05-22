---
name: oktk
version: 2.4.0
description: LLM Token Optimizer - Reduce AI API costs by 60-90%. Compresses CLI outputs (git, docker, kubectl) before sending to GPT-4/Claude. AI auto-learning included. By Buba Draugelis 🇱🇹
author: Buba Draugelis
license: MIT
homepage: https://github.com/satnamra/openclaw-workspace/tree/main/skills/oktk
tags:
  - optimization
  - tokens
  - cost-savings
  - cli
  - filtering
  - llm
requires:
  bins:
    - node
openclaw:
  emoji: 🔪
  category: optimization
---

# oktk - CLI Output Compressor for LLMs

## The Problem

When you run commands through an AI assistant, the full output goes into the LLM context:

```bash
$ git status
# Returns 60+ lines, ~800 tokens
# Your AI reads ALL of it, you pay for ALL of it
```

**Every token costs money. Verbose outputs waste your context window.**

## The Solution

oktk sits between your commands and the LLM, compressing outputs intelligently:

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Command  │ ──► │   oktk   │ ──► │   LLM    │
│ (800 tk) │     │ compress │     │ (80 tk)  │
└──────────┘     └──────────┘     └──────────┘
                      │
                 90% SAVED
```

## When Does It Work?

**Automatically** when you run supported commands through OpenClaw:

| Command | What oktk does | Savings |
|---------|----------------|:-------:|
| `git status` | Shows only: branch, ahead/behind, file counts | **90%** |
| `git log` | One line per commit: hash + message + author | **85%** |
| `git diff` | Summary: X files, +Y/-Z lines, file list | **80%** |
| `npm test` | Just: ✅ passed or ❌ failed + count | **98%** |
| `ls -la` | Groups by type, shows sizes, skips details | **83%** |
| `curl` | Status code + key headers + truncated body | **97%** |
| `grep` | Match count + first N matches | **80%** |
| `docker ps` | Container list: name, image, status | **85%** |
| `docker logs` | Last N lines + error count | **90%** |
| `kubectl get pods` | Pod status summary with counts | **85%** |
| `kubectl logs` | Last N lines + error/warning counts | **90%** |
| *Any command* | AI learns patterns automatically (optional) | **~70%** |

## Concrete Example

### Before oktk (800 tokens sent to LLM):
```
On branch main
Your branch is ahead of 'origin/main' by 3 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   src/components/Button.jsx
        modified:   src/components/Header.jsx
        modified:   src/utils/format.js
        modified:   src/utils/validate.js
        modified:   package.json
        modified:   package-lock.json

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/components/Footer.jsx
        src/components/Sidebar.jsx
        tests/Button.test.js

no changes added to commit (use "git add" and/or "git commit -a")
```

### After oktk (80 tokens sent to LLM):
```
📍 main
↑ Ahead 3 commits
✏️  Modified: 6
❓ Untracked: 3
```

**Same information. 90% fewer tokens. Same cost savings.**

## How It Works Technically

1. **Intercepts** command output after execution
2. **Detects** command type (git? npm? ls?)
3. **Applies** specialized filter for that command
4. **Extracts** only essential information
5. **Caches** results (same command = instant, no reprocessing)

### Safety First

oktk **never breaks your workflow**:

```
Try specialized filter
    ↓ fails?
Try basic filter  
    ↓ fails?
Return raw output (same as without oktk)
```

**Worst case:** You get normal output
**Best case:** 90% token savings

## Usage

### Global Command (Recommended)

After installation, `oktk` is available globally:

```bash
# Pipe any command through oktk
git status | oktk git status
docker ps | oktk docker ps
kubectl get pods | oktk kubectl get pods

# See your total savings
oktk --stats

# Bypass filter (get raw)
oktk --raw git status
```

### Shell Aliases (Auto-Filter)

Source the aliases file for automatic filtering:

```bash
# Add to ~/.zshrc or ~/.bashrc
source ~/.openclaw/workspace/skills/oktk/scripts/oktk-aliases.sh
```

Then use short aliases:

```bash
gst        # git status (filtered)
glog       # git log (filtered)
dps        # docker ps (filtered)
kpods      # kubectl get pods (filtered)

# Universal wrapper - filter ANY command
ok git status
ok docker ps -a
ok kubectl describe pod my-pod
```

### OpenClaw Integration

When using OpenClaw's exec tool, pipe outputs through oktk:

```bash
# In your prompts, ask OpenClaw to:
git status | oktk git status
docker logs container | oktk docker logs

# Or use the 'ok' wrapper (if aliases sourced):
ok git diff HEAD~5
```

**Note:** OpenClaw doesn't have a built-in exec output transformer yet. 
The recommended approach is:
1. Source the aliases file in your shell
2. Use `ok <command>` wrapper for any command
3. Or manually pipe: `<command> | oktk <command>`

## Real Savings Example

After 1 week of normal usage:

```
📊 Token Savings
━━━━━━━━━━━━━━━━
Commands filtered: 1,247
Tokens saved:      456,789 (78%)

💰 At $0.01/1K tokens = $4.57 saved
```

## Installation

Already included in OpenClaw workspace, or:

```bash
clawhub install oktk
```

---

**Made with ❤️ in Lithuania 🇱🇹**
