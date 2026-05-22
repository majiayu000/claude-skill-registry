---
name: playtest
description: Run automated playtesting to find bugs. Deploys Claude as a player to interact with SENTINEL through the bridge API.
allowed-tools: Bash, Read, Glob, Grep
user-invocable: true
proactive: false
---

# Playtest Agent

Deploy Claude as an AI player to find bugs in SENTINEL. The agent interacts with the game through the Bridge API (`localhost:3333`) and systematically tests game mechanics.

## Prerequisites

The Bridge must be running with Claude as the backend. Start it from the project root:
```bash
cd sentinel-bridge && deno task start --backend claude

**IMPORTANT**: Always use Claude as the backend for playtesting. This ensures consistent, high-quality GM responses and proper tool handling.

## How to Run

When the user invokes `/playtest`, follow this protocol:

### Step 1: Check Bridge Status and Backend

```bash
# Check if bridge is running
curl -s http://localhost:3333/health

# Check current backend
curl -s http://localhost:3333/state | jq -r '.sentinel.backend // "not running"'
```

If the bridge isn't running:
1. Start it in a separate terminal: `cd C:\dev\SENTINEL\sentinel-bridge && deno task start --backend claude`
2. Wait for "Bridge API listening on http://localhost:3333"
3. Return and continue

If the bridge is running but using a different backend, switch to Claude:
```bash
curl -s -X POST http://localhost:3333/command \
  -H "Content-Type: application/json" \
  -d '{"cmd": "slash", "command": "/backend", "args": ["claude"]}'
```

Verify the backend switched:
```bash
curl -s http://localhost:3333/state | jq -r '.sentinel.backend'
# Should output: claude
```

### Step 2: Read the Test Protocol

Read `C:\dev\SENTINEL\.claude\skills\playtest\PROTOCOL.md` for the testing checklist.

### Step 3: Execute Tests

Run through the test scenarios using curl commands. For each test:

1. **Execute the action** via the Bridge API
2. **Verify the response** contains expected fields
3. **Check state consistency** with `campaign_state` command
4. **Log any anomalies**

### API Commands Reference

```bash
# Check health
curl -s http://localhost:3333/health

# Get full state
curl -s http://localhost:3333/state

# Create new campaign
curl -s -X POST http://localhost:3333/command \
  -H "Content-Type: application/json" \
  -d '{"cmd": "slash", "command": "/new", "args": ["Playtest Session"]}'

# Create character (minimal)
curl -s -X POST http://localhost:3333/command \
  -H "Content-Type: application/json" \
  -d '{"cmd": "slash", "command": "/char", "args": ["quick"]}'

# Get campaign state
curl -s -X POST http://localhost:3333/command \
  -H "Content-Type: application/json" \
  -d '{"cmd": "campaign_state"}'

# Start session (triggers GM)
curl -s -X POST http://localhost:3333/command \
  -H "Content-Type: application/json" \
  -d '{"cmd": "slash", "command": "/start", "args": []}'

# Say something to GM
curl -s -X POST http://localhost:3333/command \
  -H "Content-Type: application/json" \
  -d '{"cmd": "say", "text": "I approach the contact cautiously"}'

# Run any slash command
curl -s -X POST http://localhost:3333/command \
  -H "Content-Type: application/json" \
  -d '{"cmd": "slash", "command": "/status", "args": []}'

# Save campaign
curl -s -X POST http://localhost:3333/command \
  -H "Content-Type: application/json" \
  -d '{"cmd": "save"}'

# Load campaign
curl -s -X POST http://localhost:3333/command \
  -H "Content-Type: application/json" \
  -d '{"cmd": "load", "campaign_id": "playtest-session"}'
```

### Step 4: Generate Bug Report

After running tests, create a bug report summarizing:
- **Passed tests**: Commands that worked as expected
- **Failed tests**: Commands that returned errors or unexpected results
- **State inconsistencies**: Mismatches between expected and actual state
- **Crashes**: Any unhandled exceptions or process failures
- **Edge cases**: Boundary conditions that behaved unexpectedly

## Test Scenarios

### Scenario 1: Happy Path
1. Create campaign
2. Create character
3. Start session
4. Make a few player actions
5. Run /debrief
6. Verify state persistence

### Scenario 2: Edge Cases
1. Social energy at 0 - try social actions
2. Hostile faction - try favor request
3. Invalid commands - verify error handling
4. Rapid command spam - check for race conditions

### Scenario 3: State Consistency
1. After each major action, compare `campaign_state` output
2. Verify faction standings update correctly
3. Verify social energy changes are reflected
4. Verify gear/loadout changes persist

## Bug Severity Levels

- **CRITICAL**: Crash, data loss, game-breaking
- **HIGH**: Incorrect mechanics, state corruption
- **MEDIUM**: UI/output issues, confusing behavior
- **LOW**: Minor inconsistencies, polish issues

## Example Output

```markdown
# Playtest Report - 2026-01-24

## Summary
- Tests run: 15
- Passed: 12
- Failed: 3
- Warnings: 2

## Critical Issues
None

## High Priority
- `/favor` command fails when NPC has no personal_standing field (KeyError)

## Medium Priority
- `/jobs accept` returns success but job not added to active_jobs list
- Social energy display shows 75 but campaign_state shows 70

## Low Priority
- Typo in Nexus faction description: "surveilance" -> "surveillance"

## Test Details
[Full test log...]
```

## Tips

- Run tests in a fresh campaign to avoid state pollution
- Check both the command response AND the campaign_state after each action
- Pay attention to error messages - they often reveal edge cases
- If something feels wrong, it probably is - investigate further
