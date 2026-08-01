---
name: auto-review-agent
description: Manages and monitors the autonomous agent system for code implementation
  tasks. Provides progress checking, issue diagnosis, and automatic fixing capabilities.
---

# Claude Skill: Agent System Manager

## Skill Description
Manages and monitors the autonomous agent system for code implementation tasks. Provides progress checking, issue diagnosis, and automatic fixing capabilities.

## Commands

### 1. Check Progress
```bash
/Users/mchaouachi/agent-system/check-agent-progress.sh
```
Shows complete status including:
- Current agent status (idle/awaiting_review/approved/implementing)
- Test progress (X/183 tests passing)
- Recent activity from logs
- Files recently modified
- Agent communication status
- Recommendations for next steps

### 2. Auto-Fix Issues
```bash
/Users/mchaouachi/agent-system/agent-autofix.sh /Users/mchaouachi/IdeaProjects/StockMonitor
```
Automatically diagnoses and fixes common issues:
- Creates proposals if missing
- Triggers reviewer if stuck
- Starts implementation if approved but not running
- Fixes communication issues between agents
- Only restarts as last resort

### 3. Quick Status
```bash
cat /Users/mchaouachi/IdeaProjects/StockMonitor/coordination/task_proposals.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Status: {d.get(\"status\")}, Proposals: {len(d.get(\"proposals\", []))}, Chosen: {d.get(\"chosen_approach\", \"none\")}')"
```

### 4. Force Implementation
```bash
tmux send-keys -t agent_system_spec:planner C-c Enter && sleep 2 && tmux send-keys -t agent_system_spec:planner "claude" Enter && sleep 3 && tmux send-keys -t agent_system_spec:planner "Read /Users/mchaouachi/IdeaProjects/StockMonitor/coordination/task_proposals.json. Implement the approved approach to fix 75 tests. Work autonomously." Enter
```

### 5. View Live Agents
```bash
tmux attach -t agent_system_spec
```
Then use:
- Ctrl+b 0 for planner
- Ctrl+b 1 for reviewer
- Ctrl+b 2 for monitor

### 6. Check Test Results
```bash
cd /Users/mchaouachi/IdeaProjects/StockMonitor && mvn test | grep "Tests run:"
```

### 7. Emergency Restart
```bash
tmux kill-session -t agent_system_spec && cd /Users/mchaouachi/agent-system && ./launch-agents-from-spec.sh /Users/mchaouachi/IdeaProjects/StockMonitor 999
```

## Usage Examples

### When to use each command:

**Nothing happening?**
```bash
/Users/mchaouachi/agent-system/check-agent-progress.sh
```
Then follow recommendations.

**Agents stuck?**
```bash
/Users/mchaouachi/agent-system/agent-autofix.sh
```
Automatically diagnoses and applies fixes.

**Want to see what agents are doing?**
```bash
tmux attach -t agent_system_spec
```

**Need test status?**
```bash
cd /Users/mchaouachi/IdeaProjects/StockMonitor && mvn test | grep "Tests run:"
```

## File Locations

- **Project**: `/Users/mchaouachi/IdeaProjects/StockMonitor`
- **Agent System**: `/Users/mchaouachi/agent-system`
- **Proposals**: `/Users/mchaouachi/IdeaProjects/StockMonitor/coordination/task_proposals.json`
- **Logs**: `/Users/mchaouachi/IdeaProjects/StockMonitor/coordination/logs/`
- **Specs**: `/Users/mchaouachi/IdeaProjects/StockMonitor/specs/`

## Status Meanings

- **idle**: No activity, needs to start
- **awaiting_review**: Proposals created, reviewer should evaluate
- **approved**: Ready for implementation
- **implementing**: Currently fixing tests

## Troubleshooting Quick Guide

| Problem | Solution |
|---------|----------|
| No proposals | Run agent-autofix.sh |
| Stuck on "awaiting_review" | Run agent-autofix.sh |
| Approved but not implementing | Run agent-autofix.sh |
| Want fresh start | Kill session, delete task_proposals.json, restart |
| Need to see errors | Check planner window in tmux |

## Integration with Claude

When called from Claude, I can:
1. Run check-agent-progress.sh to get current status
2. Analyze the output and recommend next steps
3. Run agent-autofix.sh if issues detected
4. Monitor progress and report back
5. Provide specific commands to fix identified issues

This skill enables Claude to act as a supervisor for the autonomous agent system, ensuring smooth operation and fixing issues automatically.
