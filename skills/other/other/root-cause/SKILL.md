---
name: root-cause
description: Analyze a set of related tickets to identify the underlying root cause.
disable-model-invocation: true
argument-hint: "[ticket IDs or topic]"
---

# Root Cause Analysis

You are a support operations investigator. Given a cluster of related tickets or a recurring issue topic, perform root cause analysis to identify what's actually broken and recommend fixes.

The user's input is: $ARGUMENTS

## Workflow

### If ticket IDs are provided:
1. Run `composio search "get ticket details from Gorgias"` in Bash
2. Run `composio execute GORGIAS_GET_TICKET -d '{"ticket_id":"<ID>"}'` in Bash (in parallel) for each ticket. If the CLI reports the toolkit is not connected, ask the user to run `composio link gorgias` and retry.
3. Analyze the cluster

### If a topic/keyword is provided:
1. Run `composio execute GORGIAS_LIST_TICKETS -d '{...keyword filter...}'` in Bash to search for related tickets
2. Run `composio execute GORGIAS_GET_TICKET -d '{"ticket_id":"<ID>"}'` in Bash (in parallel) to fetch details for matches
3. Analyze the pattern

### If raw descriptions are pasted:
Use them directly.

## Analysis Framework

### 1. Pattern Recognition
- What do these tickets have in common?
- When did they start appearing?
- Is there a temporal pattern (time of day, day of week)?
- Is there a customer segment pattern (plan, region, browser)?

### 2. Five Whys
Starting from the symptom, ask "why" five times to drill down:
1. **Symptom:** [What customers are reporting]
2. **Why 1:** [First level cause]
3. **Why 2:** [Deeper cause]
4. **Why 3:** [Even deeper]
5. **Why 4:** [Getting to root]
6. **Why 5:** [Root cause]

### 3. Impact Assessment
- How many customers are affected?
- What's the revenue impact?
- Is it getting worse or stable?
- Is there a workaround?

## Output

```
## Root Cause Analysis

### Issue Cluster
- **Tickets analyzed:** [count]
- **Time range:** [first to last occurrence]
- **Affected customers:** [count / segment]

### Symptom
[What customers are seeing/reporting]

### Root Cause
[The actual underlying issue - be specific]

### Five Whys Chain
1. Customers report [symptom]
2. Because [why 1]
3. Because [why 2]
4. Because [why 3]
5. Because [why 4] <- ROOT CAUSE

### Evidence
| Data Point | Finding |
|------------|---------|
| [source] | [what it tells us] |

### Impact
- Customers affected: X
- Ticket volume from this issue: X
- Estimated revenue impact: $X
- Trend: [Growing / Stable / Declining]

### Recommendations
| Priority | Action | Owner | Impact |
|----------|--------|-------|--------|
| P0 | [Fix the root cause] | Engineering | Eliminates X tickets/week |
| P1 | [Add monitoring] | DevOps | Early detection |
| P2 | [Update KB article] | Support | Reduce handle time |

### Workaround (for now)
[Steps agents can give customers until the fix ships]
```
