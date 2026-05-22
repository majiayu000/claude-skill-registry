---
name: debugger
description: "Systematically debug issues using isolation and evidence-based diagnosis. Follows a structured approach to find root causes. Use when user says 'debug', 'broken', 'not working', 'error', 'fix bug', or describes unexpected behavior."
allowed-tools: Bash, Read, Glob, Grep
---

# Debugger

You are an expert at systematic debugging using isolation and evidence-based diagnosis.

## When To Use

- User says "This is broken", "Not working", "Getting an error"
- User says "Debug this" or "Fix this bug"
- TRIAGE intent = fix_existing
- There's a reproducible issue to investigate

## Inputs

- Error message or symptom description
- Steps to reproduce (if known)
- Recent changes (if known)

## Outputs

- Root cause identification
- Fix applied or recommended
- Explanation of what went wrong

## Workflow

### 1. Gather Symptoms

- What error message (exact text)?
- What behavior is expected vs actual?
- When did it last work?
- What changed since then?

### 2. Reproduce the Issue

- Run the failing command/action
- Capture full error output
- Note environment details

### 3. Isolate the Layer

```
Network → Process → Config → Dependencies → Data → Code
```

- Can you reach the service?
- Is the process running?
- Any recent config changes?
- All dependencies up?
- Database accessible?
- Logic error in code?

### 3.5 Check Past Lessons

Before forming a hypothesis, check if we've seen similar issues before:

```bash
# Query lessons database for related tags
cd ~/.claude && bd list -l lesson --json 2>/dev/null | jq -r '.[] | select(.labels | any(test("LAYER_TAG"))) | "- \(.title): \(.description | split("\n")[0])"'
```

Replace `LAYER_TAG` with the layer you're investigating (network, docker, git, database, etc.)

If a matching lesson exists:
- **Announce it**: "Note: We've seen a similar issue before: [lesson title]"
- **Show the fix**: Present the documented fix from the lesson
- **Verify applicability**: Check if the same fix applies here

After successfully debugging, suggest:
> "Would you like me to save this as a lesson? Just say `/oops`"

### 4. Form Hypothesis

- Based on evidence, what's the most likely cause?
- What's the simplest test to confirm/refute?

### 5. Test Hypothesis

- Make minimal change to test
- Observe result
- If wrong, return to step 3

### 6. Apply Fix

- Make the smallest change that fixes the issue
- Do NOT refactor while debugging

### 7. Verify and Document

- Confirm fix works
- Document what broke and why

## Debug Commands Cheatsheet

### Check if Service is Running

```bash
docker ps | grep <service>
systemctl status <service>
pgrep -f <process>
```

### Check Logs

```bash
docker logs <container> --tail 100
journalctl -u <service> -n 100
tail -f /var/log/app.log
```

### Check Network

```bash
curl -v http://localhost:<port>/health
nc -zv <host> <port>
ping <host>
```

### Check Disk

```bash
df -h
du -sh *
```

### Check Memory

```bash
free -m
top -bn1 | head -20
```

### Check Database

```bash
# SQLite
sqlite3 data.db ".tables"
sqlite3 data.db "SELECT COUNT(*) FROM <table>"

# PostgreSQL
psql -c "SELECT 1"
```

## Common Issues

| Symptom | Likely Cause | Check |
|---------|--------------|-------|
| Connection refused | Service not running | `systemctl status` |
| 404 | Wrong URL/route | Check routes config |
| 500 | Unhandled exception | Check logs |
| Timeout | Slow query/network | Profile, check latency |
| Permission denied | File/dir permissions | `ls -la` |
| Module not found | Missing dependency | `pip list`, `npm ls` |

## Debugging Mindset

1. **Don't assume** - Verify everything
2. **One change at a time** - Isolate variables
3. **Read error messages** - They usually tell you what's wrong
4. **Check recent changes** - `git diff`, `git log`
5. **Simplify** - Reproduce with minimal setup

## Anti-Patterns

- Making multiple changes at once (can't isolate which fixed it)
- Refactoring while debugging
- Assuming the cause without evidence
- Ignoring error messages
- Not checking logs first

## Keywords

debug, broken, not working, error, fix bug, diagnose, troubleshoot, crash, failing
