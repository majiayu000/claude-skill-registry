---
name: visual-style
description: Color scheme and icons for consistent Autopilot output. Reference when formatting agent output and status messages.
---

// Project Autopilot - Visual Style Guidelines
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

# Visual Style Guide

Consistent colors and icons for Autopilot output.

---

## Agent Colors

Each agent has an assigned color for visual distinction:

| Agent | Color | ANSI Code | Hex | Use |
|-------|-------|-----------|-----|-----|
| **planner** | 🔵 Blue | `\033[94m` | #3b82f6 | Planning |
| **validator** | 🟢 Green | `\033[92m` | #22c55e | Quality gates |
| **token-tracker** | 🟡 Yellow | `\033[93m` | #eab308 | Cost tracking |
| **history-tracker** | 🟤 Brown | `\033[33m` | #a16207 | Persistence |
| **model-selector** | ⚪ Gray | `\033[90m` | #6b7280 | Model selection |
| **architect** | 🟣 Magenta | `\033[35m` | #d946ef | Architecture |
| **backend** | 🔵 Cyan | `\033[96m` | #06b6d4 | Backend code |
| **frontend** | 🟠 Orange | `\033[38;5;208m` | #f97316 | Frontend code |
| **database** | 🔴 Red | `\033[91m` | #ef4444 | Database |
| **tester** | 🟢 Lime | `\033[38;5;118m` | #84cc16 | Testing |
| **security** | 🔴 Dark Red | `\033[31m` | #dc2626 | Security |
| **debugger** | 🟡 Amber | `\033[38;5;214m` | #f59e0b | Debugging |
| **refactor** | 🔵 Indigo | `\033[38;5;99m` | #6366f1 | Refactoring |
| **documenter** | ⚪ Slate | `\033[37m` | #94a3b8 | Documentation |
| **devops** | 🟠 Coral | `\033[38;5;209m` | #fb7185 | DevOps |
| **api-designer** | 🔵 Sky | `\033[38;5;117m` | #0ea5e9 | API design |
| **code-review** | 🟣 Violet | `\033[38;5;135m` | #8b5cf6 | Code review |

---

## Status Icons

### Task Status

| Icon | Meaning | When to Use |
|------|---------|-------------|
| ✅ | Success | Task/phase completed |
| ❌ | Failed | Task/validation failed |
| 🔄 | In Progress | Currently executing |
| ⏸️ | Paused | Waiting for input/approval |
| ⏭️ | Skipped | Task skipped (already done) |
| 🔜 | Pending | Not yet started |

### Validation Status

| Icon | Meaning | When to Use |
|------|---------|-------------|
| ✓ | Pass | Validation passed |
| ✗ | Fail | Validation failed |
| ⚠ | Warning | Non-blocking issue |
| ● | Running | Check in progress |

### Cost/Budget

| Icon | Meaning | When to Use |
|------|---------|-------------|
| 💰 | Cost | Cost information |
| 💵 | Budget | Budget thresholds |
| 📊 | Stats | Statistics/metrics |
| 📈 | Increase | Cost went up |
| 📉 | Decrease | Cost went down (savings) |

### Threshold Levels

| Icon | Level | When to Use |
|------|-------|-------------|
| ✅ | OK | Under warning threshold |
| ⚠️ | Warning | At warning threshold |
| 🟠 | Alert | At alert threshold |
| 🛑 | Stop | At/over max threshold |

### System Events

| Icon | Meaning | When to Use |
|------|---------|-------------|
| 📌 | Checkpoint | Checkpoint saved |
| ▶️ | Start | Execution starting |
| ⏹️ | Stop | Execution stopped |
| 🔁 | Resume | Resuming from checkpoint |
| 🏁 | Complete | Project finished |
| 💾 | Save | Data saved |
| 📂 | File | File operation |
| 🔧 | Tool | Tool execution |
| 🚀 | Deploy | Deployment |
| 🔒 | Security | Security related |
| 🧪 | Test | Testing |
| 📝 | Doc | Documentation |

### Git Operations

| Icon | Meaning | When to Use |
|------|---------|-------------|
| 📝 | Commit | Git commit |
| 🔀 | Branch | Branch operation |
| ⬆️ | Push | Git push |
| ⬇️ | Pull | Git pull |
| 🔃 | Merge | Git merge |

---

## Output Formats

### Agent Spawn

```
🔵 planner → Creating phase plan
🔵 backend → Creating UserService
```

### Task Progress

```
🔄 003.1 | Creating AuthService...
✅ 003.1 | AuthService | $0.04 | 2.1K tokens
```

### Validation Results

```
🟢 validator → Phase 003 Gate
   ✓ Build passes
   ✓ Tests pass (47/47)
   ✓ Coverage 87%
   ✓ Lint clean
   ✓ Security clean
   ✅ APPROVED
```

### Cost Updates

```
💰 Cost: $4.36 / $50.00 (9%)
   ├── Input:  245K tokens
   ├── Output: 89K tokens
   └── Calls:  34

📊 By Model:
   ├── Sonnet: $3.82 (88%)
   ├── Haiku:  $0.54 (12%)
   └── Opus:   $0.00 (0%)
```

### Checkpoint

```
📌 Checkpoint saved (phase_complete)
   Phase: 003 of 008
   Task:  003.4
   Cost:  $4.36
```

### Threshold Alerts

```
⚠️ Warning: Cost $10.23 exceeds warning threshold ($10.00)
   Continuing execution...

🟠 Alert: Cost $25.12 exceeds alert threshold ($25.00)
   Pause for confirmation. Continue? [y/N]

🛑 Stop: Cost $50.05 exceeds maximum ($50.00)
   Saving checkpoint and halting...
```

### Phase Summary

```
🏁 Phase 003 Complete
   ├── Tasks:    4/4 ✅
   ├── Duration: 12m 34s
   ├── Cost:     $1.23 (est: $1.50, -18% 🟢)
   └── Commits:  3
```

### Project Summary

```
🎉 Project Complete!

📊 Final Stats
   ├── Phases:   8/8 ✅
   ├── Tasks:    34/34 ✅
   ├── Duration: 2h 15m
   ├── Cost:     $8.45 (est: $10.00, -16% 🟢)
   └── Commits:  28

💾 Saved to history
   View: /autopilot:config --history
```

---

## Color Reset

Always reset colors after output:

```
\033[0m  # Reset all formatting
```

---

## Markdown Output (for .md files)

When writing to markdown files, use text-based indicators:

| Instead of | Use |
|------------|-----|
| 🟢 | `[PASS]` or `✓` |
| 🔴 | `[FAIL]` or `✗` |
| 🟡 | `[WARN]` or `⚠` |
| 🔵 | `[INFO]` or `ℹ` |

---

## Quick Reference

### Common Patterns

```
# Agent starting work
{color}{icon} {agent} → {action}

# Task status
{status_icon} {task_id} | {description} | ${cost}

# Validation line
   {check_icon} {check_name}

# Cost line
💰 {label}: ${amount} / ${limit} ({percent}%)

# Checkpoint
📌 Checkpoint saved ({reason})
```

### Agent Color Quick Map

```
planner       = 🔵 Blue
validator     = 🟢 Green
token-tracker = 🟡 Yellow
backend       = 🔵 Cyan
frontend      = 🟠 Orange
database      = 🔴 Red
tester        = 🟢 Lime
security      = 🔴 Dark Red
debugger      = 🟡 Amber
```
