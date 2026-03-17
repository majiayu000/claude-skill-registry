---
# VERSION: 2.87.0
name: glm5
description: GLM-5 Agent Teams skill for spawning teammates with thinking mode
allowed-tools:
  - Bash
  - Read
  - Write
---

# GLM-5 Agent Teams Skill

Spawn GLM-5 powered teammates with native thinking mode.

## Quick Usage

```
# Spawn single teammate
/glm5 coder "Implement auth"

# Spawn for review
/glm5 reviewer "Review this code"

# Spawn for testing
/glm5 tester "Generate tests"
```

## Integration with Other Commands

This skill integrates with:
- `/orchestrator` - GLM-5 as teammate option
- `/parallel` - GLM-5 for parallel review
- `/loop` - GLM-5 for iterative tasks

## Agent Types

| Type | Role | Best For |
|------|------|----------|
| `coder` | Implementation | Features, refactoring, bugs |
| `reviewer` | Code Review | Security, quality, patterns |
| `tester` | Test Generation | Unit tests, coverage |
| `planner` | Architecture | Design, planning |
| `researcher` | Documentation | Docs, exploration |

## Execution

When this skill is invoked:

1. **Parse Arguments**: Extract role and task from `$ARGUMENTS`
2. **Generate Task ID**: `task-{timestamp}`
3. **Call GLM-5 API**: With thinking mode enabled
4. **Capture Output**: Reasoning + result
5. **Fire Hooks**: SubagentStop (native Claude Code hook)

## Bash Commands

### Spawn Teammate
```bash
.claude/scripts/glm5-teammate.sh <role> "<task>" "<task_id>"
```

### Check Status
```bash
cat .ralph/team-status.json
```

### View Logs
```bash
tail -f .ralph/logs/teammates.log
```

## Output Files

| File | Content |
|------|---------|
| `.ralph/teammates/{id}/status.json` | Task status & metadata |
| `.ralph/reasoning/{id}.txt` | GLM-5 reasoning |
| `.ralph/logs/teammates.log` | Activity log |

## Example Session

```
User: /glm5 coder "Implement factorial in TypeScript"

[GLM-5 thinking...]
Reasoning: The user wants a TypeScript factorial function...
Output: function factorial(n: number): number { ... }

✅ Task completed
📁 Status: .ralph/teammates/task-123/status.json
🧠 Reasoning: .ralph/reasoning/task-123.txt
```
