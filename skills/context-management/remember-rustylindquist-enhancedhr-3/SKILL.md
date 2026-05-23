---
name: remember
description: Reloads critical instructions when behavior degrades. Use when forgetting tools, not delegating, or missing safety rules. Refreshes orchestration mode, tool awareness, and safety constraints.
allowed-tools: Read
---

# Remember

Forcefully reload critical instructions without losing session state.

## When to Use

- Agent doing work directly instead of delegating
- Forgetting tools (Supabase CLI, Playwright MCP)
- Missing safety rules or not spawning agents
- User says "you forgot" or "remember to..."
- Every 30-45 min in long sessions

## Immediate Actions

### 1. Confirm Safety
- NO destructive DB commands (`supabase db reset`, `DROP TABLE`, `TRUNCATE`)
- Use targeted SQL, `createAdminClient()`, incremental migrations instead
- Inject safety rules into any spawned agents

### 2. Confirm Orchestration
- I am the **ORCHESTRATOR** — I plan, coordinate, synthesize
- I **DELEGATE** implementation to specialized agents
- Frontend work → @frontend-agent
- Backend work → @backend-agent
- Code exploration → @research-agent
- Testing → @test-agent

### 3. Confirm Tool Awareness
- **Supabase CLI** — Use for ALL database questions
- **Playwright MCP** — Use AFTER any UI changes
- **Agent spawning** — Use for implementation work

### 4. Confirm Process
- 2-gate flow: doc-informed plan → execute with doc updates
- Context management: spawn agents, query lazily, checkpoint regularly

## Output

```
## Instructions Refreshed

Safety: ACTIVE | Orchestration: ACTIVE | Tools: LOADED

Behavioral Check:
- [ ] Delegate frontend → @frontend-agent
- [ ] Delegate backend → @backend-agent
- [ ] Use Supabase CLI for database
- [ ] Use Playwright MCP for UI
- [ ] NO destructive commands

Ready to continue.
```

## Related

- Full instruction tiers: `CLAUDE.md` sections 2-4
- Degradation fixes: See [reference/degradation-fixes.md](reference/degradation-fixes.md)
- When to use /remember vs /compact: See [reference/decision-guide.md](reference/decision-guide.md)
