---
name: context-status
description: Checks current context window usage and provides recommendations. Use when sessions feel slow, responses seem degraded, or before starting complex work.
allowed-tools: Read
---

# Context Status

Monitor context window health. Saturation causes degraded performance, forgotten instructions, and tool neglect.

## When to Use

- Session feels "slow" or less sharp
- Before complex multi-step task
- After loading many files
- Noticing instructions being forgotten
- Periodically (every 30-60 minutes)

## Saturation Symptoms

| Symptom | Severity |
|---------|----------|
| Forgetting earlier instructions | High |
| Not using mentioned tools | High |
| Repeating completed work | Medium |
| Simplified responses | Medium |
| Missing analysis details | Critical |

## Context Levels

| Level | Indicators | Action |
|-------|-----------|--------|
| **Low** | Session <15min, few files | Continue normally |
| **Medium** | 15-45min, moderate files | Monitor, delegate more |
| **High** | 45-90min, many files | /checkpoint, strongly delegate |
| **Critical** | >90min, heavy loading | /compact immediately |

## Quick Self-Test

- [ ] Can recall safety rules?
- [ ] Can recall available tools?
- [ ] Can recall agent spawn criteria?
- [ ] Remember current task objective?

If any unclear → context likely saturated.

## Output

```markdown
## Context Status

**Level**: [Low/Medium/High/Critical]
**Session Duration**: [estimate]

### Retention Check
- Safety rules: [clear/fuzzy]
- Tool awareness: [clear/fuzzy]
- Task objective: [clear/fuzzy]

### Recommendation
[continue/checkpoint/compact]

### Suggested Action
[specific next step]
```

## Preservation Strategies

- **Delegate**: Spawn agents → receive summaries (not raw content)
- **Query lazily**: Ask Doc Agent questions (don't load full docs)
- **Progressive disclosure**: Return structure + excerpts (not full files)
- **Checkpoint regularly**: Every major milestone

## Related

| If Level | Action |
|----------|--------|
| Low | Continue normally |
| Medium | `/checkpoint` before complex work |
| High | Consider `/compact`, delegate heavily |
| Critical | `/compact` immediately |
