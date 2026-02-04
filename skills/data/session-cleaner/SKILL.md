---
name: session-cleaner
description: Clean up and manage OpenClaw sessions - kill all sub-agents, clear context, and reset the system to a clean state. Use when user says "close all sessions", "clear context", "kill all agents", "clean up sessions", "reset everything", "关掉所有子agent", "清空上下文", "关闭所有session", or similar cleanup requests.
---

# Session Cleaner

Clean up OpenClaw sessions and reset to a clean state. This skill handles:
- Closing all sub-agent sessions
- Clearing current context
- Killing background processes
- Resetting the system

## Triggers (Keywords)

**English:**
- "close all sessions"
- "kill all agents"
- "clear context"
- "clean up sessions"
- "reset everything"
- "start fresh"
- "wipe everything"

**Chinese:**
- "关掉所有子agent"
- "关闭所有会话"
- "清空上下文"
- "关闭所有session"
- "清理会话"
- "重置系统"
- "重新开始"
- "全部关掉"

## Usage

### Quick Cleanup (Keep Current Session)

```bash
# 1. List all sessions
openclaw sessions list

# 2. Stop Gateway
pkill -9 -f "openclaw-gateway"

# 3. Clean sessions.json (Python script)
python3 ~/clawd/skills/session-cleaner/scripts/clean_sessions.py

# 4. Restart Gateway
openclaw gateway start
```

### Full Reset (Including Current Session)

```bash
# User should send: /new
# Then run the cleanup above
```

## Manual Steps

### Step 1: Check Current Sessions
```bash
openclaw sessions list
```

### Step 2: Stop Gateway (kills all session processes)
```bash
pkill -9 -f "openclaw-gateway"
```

### Step 3: Clean Session Registry
```bash
python3 ~/clawd/skills/session-cleaner/scripts/clean_sessions.py
```

### Step 4: Restart Gateway
```bash
openclaw gateway start
```

### Step 5: Clear Current Context (User Action)
Tell user to send: `/new` or `/reset`

## Important Notes

1. **Always backup** `sessions.json` before cleaning
2. **Current session** is preserved by default (`agent:main:main`)
3. **Sub-agents, cron jobs, group chats** are all cleaned
4. **Gateway restart** is required to fully clear memory
5. **Context reset** (`/new`) is a separate user action

## Safety Checklist

- [ ] Backup sessions.json
- [ ] Confirm with user before destructive operations
- [ ] Preserve current session unless user says "clear everything"
- [ ] Restart Gateway after cleaning
- [ ] Instruct user to send `/new` for context reset

## Examples

**Example 1: Clean all other sessions**
```
User: "关掉所有子agent"
Agent: "正在清理... [执行 cleanup 脚本]"
```

**Example 2: Full reset**
```
User: "重置所有，包括当前会话"
Agent: "确认？这将清除所有历史。[用户确认后执行]"
```

## Files

- `scripts/clean_sessions.py` - Python script to clean sessions.json
- `SKILL.md` - This documentation

## Version

v1.0.0 - Initial release
