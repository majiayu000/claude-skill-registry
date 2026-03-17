---
skill_id: cfn-backlog-management
name: CFN Backlog Management
version: 1.0.0
category: coordination
tags: [backlog, documentation, sprint-planning, technical-debt]
dependencies: []
---

# CFN Backlog Management Skill

## Purpose
Systematically capture and track backlogged items during CFN sprints to prevent work from being forgotten. Provides centralized documentation of deferred tasks with context, rationale, and proposed solutions.

## Problem Solved
During CFN Loop execution, agents frequently identify improvements, optimizations, or edge cases that should be addressed but are out of scope for the current sprint. Without systematic capture, these items are lost in chat history or forgotten entirely.

## When to Use
- **During CFN sprints** when identifying work that should be deferred
- **After consensus** when validators identify future improvements
- **During retrospectives** when documenting technical debt
- **Architecture reviews** when noting long-term refactoring needs

## Interface

### Primary Script: `add-backlog-item.sh`

**Required Parameters:**
- `--item`: Brief description of backlogged work (1-2 sentences)
- `--why`: Rationale for deferring (why not now?)
- `--solution`: Proposed implementation approach

**Optional Parameters:**
- `--sprint`: Sprint identifier (default: auto-detected from context)
- `--priority`: P0-P3 (default: P2)
- `--tags`: Comma-separated tags (e.g., "optimization,redis,testing")
- `--category`: Feature/Bug/Technical-Debt/Optimization (default: Technical-Debt)

**Usage:**
```bash
./.claude/skills/cfn-backlog-management/add-backlog-item.sh \
  --sprint "Sprint 10" \
  --item "Implement Redis connection pooling for multi-agent coordination" \
  --why "Current single-connection model causes bottlenecks with 10+ agents, but Sprint 10 scope limited to 3-agent validation" \
  --solution "Use ioredis library with configurable pool size (min: 5, max: 20). Add pool metrics to monitoring dashboard" \
  --priority "P2" \
  --tags "optimization,redis,performance" \
  --category "Optimization"
```

### Output Location
All backlog items are appended to: `readme/BACKLOG.md`

## Backlog File Structure

```markdown
# Claude Flow Novice - Backlog

Last Updated: 2025-10-31

## Active Items

### P0 - Critical
[Items requiring immediate attention in next sprint]

### P1 - High Priority
[Items to address within 2-3 sprints]

### P2 - Medium Priority
[Items to address when capacity allows]

### P3 - Low Priority / Nice-to-Have
[Items for future consideration]

## Completed Items
[Moved here when implemented, with resolution sprint noted]

---

## Item Template

**[PRIORITY] - [Item Title]**
- **Sprint Backlogged**: Sprint X
- **Category**: Feature/Bug/Technical-Debt/Optimization
- **Description**: What needs to be done
- **Rationale**: Why it was deferred
- **Proposed Solution**: How to implement
- **Tags**: `tag1`, `tag2`, `tag3`
- **Status**: Backlogged | In Progress | Completed
- **Date Added**: YYYY-MM-DD
```

## Validation Rules

The skill enforces:
1. **All required fields present** (item, why, solution)
2. **Item description clarity** (≥10 characters, ≤500 characters)
3. **Rationale specificity** (must explain deferral reason, not just "out of scope")
4. **Solution actionability** (must include concrete implementation approach)
5. **No duplicates** (checks existing BACKLOG.md for similar items)

## Integration with CFN Loops

### Loop 2 Validators
When validators identify improvements outside current scope:
```bash
# In validator agent
./.claude/skills/cfn-backlog-management/add-backlog-item.sh \
  --item "Add integration tests for Redis failure scenarios" \
  --why "Current sprint validates happy path only; failure testing requires additional test infrastructure" \
  --solution "Create test-redis-failures.sh with Docker-based Redis crash simulation" \
  --tags "testing,redis,edge-cases"
```

### Product Owner Decision
When Product Owner defers work for future sprint:
```bash
# In product-owner agent
./.claude/skills/cfn-backlog-management/add-backlog-item.sh \
  --item "Migrate coordination from Redis to etcd for production scale" \
  --why "Redis sufficient for current 10-agent limit; etcd needed for 100+ agent deployments" \
  --solution "Abstract coordination layer behind interface, implement etcd adapter" \
  --priority "P3" \
  --category "Technical-Debt"
```

### Coordinator Context
Coordinators can query backlog for related items before spawning agents:
```bash
# Check if backlog contains relevant context
grep -i "redis pooling" readme/BACKLOG.md
# Use results to inform agent context injection
```

## Query Interface

**Search by tag:**
```bash
grep -A 10 "Tags:.*redis" readme/BACKLOG.md
```

**Filter by priority:**
```bash
sed -n '/^### P1/,/^### P2/p' readme/BACKLOG.md
```

**List all optimization items:**
```bash
grep -B 2 "Category: Optimization" readme/BACKLOG.md
```

## Maintenance

**Weekly Review**: Product Owner reviews P0-P1 items for sprint planning
**Monthly Cleanup**: Archive completed items, reassess P3 priorities
**Quarterly Audit**: Remove stale items (>6 months old, no activity)

## Best Practices

1. **Be specific**: "Add caching" → "Implement Redis LRU cache for agent context with 1h TTL"
2. **Explain constraints**: "Not enough time" → "Requires 8h estimation work; current sprint has 2h budget"
3. **Provide actionable solutions**: "Fix later" → "Refactor using Strategy pattern from planning/PATTERNS.md"
4. **Tag appropriately**: Enables filtering and sprint planning
5. **Update status**: Move to "Completed" when resolved, note resolution sprint

## Anti-Patterns

❌ **Vague items**: "Improve performance" (What component? How much improvement?)
❌ **No rationale**: "Backlog this" (Why defer? What's the blocker?)
❌ **Solution-less**: "Fix Redis issues" (What's the approach? What research is needed?)
❌ **Duplicate entries**: Check BACKLOG.md before adding
❌ **Scope creep**: Backlog is for deferred work, not scope expansion

## Example Backlog Item

```markdown
**[P1] - Implement Adaptive Validator Scaling**
- **Sprint Backlogged**: Sprint 9 - CFN v3 Implementation
- **Category**: Optimization
- **Description**: Dynamically adjust number of Loop 2 validators (2-5) based on task complexity. Currently fixed at 3-4 validators regardless of task size.
- **Rationale**: Sprint 9 focused on dual-mode architecture validation. Adaptive scaling requires task complexity classifier (NLP or heuristic-based), estimated 12h implementation vs 4h sprint budget.
- **Proposed Solution**: Create task-classifier skill that analyzes task description (file count, domain keywords, integration points) and returns complexity score (0.0-1.0). Map score to validator count: <0.3 → 2 validators, 0.3-0.7 → 3-4 validators, >0.7 → 5 validators. Reference: CFN_LOOP_TASK_MODE.md section on adaptive validator scaling.
- **Tags**: `optimization`, `cfn-loop`, `validation`, `adaptive-scaling`
- **Status**: Backlogged
- **Date Added**: 2025-10-31
```

## Success Metrics

- **Backlog utilization**: ≥30% of backlog items addressed within 3 sprints
- **Item clarity**: 0 items missing required fields
- **Discovery rate**: ≥50% of technical debt captured vs lost in chat
- **Sprint planning efficiency**: Backlog queries reduce planning time by 20%

## References

- **STRAT-025**: Explicit Deliverable Tracking (adaptive context)
- **CFN Loop Documentation**: `.claude/commands/CFN_LOOP_TASK_MODE.md`
- **Sprint Execution**: CLAUDE.md Section 6 - Sprint Context Injection
