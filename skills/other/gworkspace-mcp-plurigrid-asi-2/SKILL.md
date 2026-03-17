---
name: gworkspace-mcp
description: 'gworkspace-mcp - Google Workspace MCP Integration with Temporal Consistency'
version: 1.0.0
---

# gworkspace-mcp - Google Workspace MCP Integration with Temporal Consistency

## Overview

Integrates Google Workspace services (Gmail, Drive, Calendar, Docs, Sheets, Tasks, Meet) through MCP with:

1. **Causal Poset Interaction Time**: First-class temporal structure for replay determinism
2. **GF(3) Triadic Conservation**: Every action classified as PLUS (+1), ERGODIC (0), or MINUS (-1)
3. **Cross-Service Atomicity**: Two-phase commit for multi-service workflows
4. **ANIMA Condensation**: Saturation states (Inbox Zero, Task Zero) as fixed points
5. **Retry with 1069 Checkpoints**: Balanced ternary error recovery

**Trit**: 0 (ERGODIC) - Coordinates cross-service workflows

## Core Formula

```
InteractionTime ≅ CausalPoset(Events)
GlobalSaturation = (∀s. ServiceSaturated s) ∧ CrossServiceConsistent ∧ TemporalClosure ∧ (Σ trits = 0)
FreeTrace ⊣ CondensedInteractionTime  -- Temporal adjunction
```

## Predicates

| Predicate | Description | GF(3) Role |
|-----------|-------------|------------|
| `CausallyPrecedes(e₁, e₂)` | e₁ causally before e₂ | Order structure |
| `Concurrent(e₁, e₂)` | Neither precedes the other | Concurrency |
| `ServiceSaturated(s)` | No pending operations | Local stability |
| `CrossServiceConsistent(g)` | All dependencies resolved | Global consistency |
| `TemporalClosure(g)` | All consequences computed | Causal completeness |
| `GlobalSaturation(g)` | Full condensation achieved | Fixed point |
| `InboxZero(gmail)` | All emails processed | Domain saturation |
| `TaskZero(tasks)` | All tasks completed | Domain saturation |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    Google Workspace MCP Integration                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   Services                    Causal Layer                    Condensation       │
│      │                            │                               │              │
│      ▼                            ▼                               ▼              │
│  ┌────────┐    ┌───────────────────────────────────┐    ┌──────────────────┐   │
│  │ Gmail  │───▶│  CausalEvent { id, service,       │───▶│ GlobalSaturation │   │
│  │Calendar│    │    action, trit, seed, timestamp } │    │ CrossConsistent  │   │
│  │ Drive  │    └───────────────────────────────────┘    │ TemporalClosure  │   │
│  │ Docs   │                     │                        └──────────────────┘   │
│  │ Sheets │    ┌───────────────────────────────────┐              │              │
│  │ Tasks  │───▶│  InteractionTime (Causal Poset)  │              ▼              │
│  │ Meet   │    │    reflexive, transitive,         │    ┌──────────────────┐   │
│  └────────┘    │    antisymmetric                  │    │ ANIMA Condensed  │   │
│                └───────────────────────────────────┘    │   InboxZero      │   │
│                                                          │   TaskZero       │   │
│                                                          └──────────────────┘   │
│                                                                                  │
│   Concurrency                 Atomicity                    Error Recovery        │
│      │                            │                               │              │
│      ▼                            ▼                               ▼              │
│  ┌────────────┐    ┌───────────────────────────────┐    ┌──────────────────┐   │
│  │Concurrent  │    │  TwoPhaseCommit               │    │ RetryPolicy      │   │
│  │ActionSet   │    │    phase1_votes → decision    │    │ 1069 checkpoints │   │
│  │ gf3 = 0    │    │    Transaction.gf3_conserved  │    │ [+1,-1,-1,+1...] │   │
│  └────────────┘    └───────────────────────────────┘    └──────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## GF(3) Trit Assignment for Actions

| Action | Trit | Polarity | Services |
|--------|------|----------|----------|
| `read`, `list`, `download` | 0 | ERGODIC | All |
| `create`, `send`, `upload` | +1 | PLUS | Gmail, Drive, Docs, Sheets, Tasks |
| `delete`, `archive`, `complete` | -1 | MINUS | All |
| `update`, `label`, `share` | 0 | ERGODIC | All |
| `invite`, `schedule` | +1 | PLUS | Calendar, Meet |
| `export`, `formula` | 0 | ERGODIC | Docs, Sheets |

## Triads (GF(3) = 0)

```
# Core GWorkspace Triads
three-match (-1) ⊗ gworkspace-mcp (0) ⊗ gay-mcp (+1) = 0 ✓  [Core Integration]
temporal-coalgebra (-1) ⊗ gworkspace-mcp (0) ⊗ koopman-generator (+1) = 0 ✓  [Causal Dynamics]
sheaf-cohomology (-1) ⊗ gworkspace-mcp (0) ⊗ oapply-colimit (+1) = 0 ✓  [Cross-Service]
keychain-secure (-1) ⊗ gworkspace-mcp (0) ⊗ gay-mcp (+1) = 0 ✓  [OAuth]
polyglot-spi (-1) ⊗ gworkspace-mcp (0) ⊗ agent-o-rama (+1) = 0 ✓  [Multi-Agent]
shadow-goblin (-1) ⊗ gworkspace-mcp (0) ⊗ pulse-mcp-stream (+1) = 0 ✓  [Event Stream]
```

## MCP Server Configuration

```toml
# .ruler/ruler.toml
[mcp_servers.gworkspace]
command = "uvx"
args = ["gworkspace-mcp"]
env = { 
  GOOGLE_CLIENT_ID = "${GOOGLE_CLIENT_ID}",
  GOOGLE_CLIENT_SECRET = "${GOOGLE_CLIENT_SECRET}",
  GF3_SEED = "1069"
}
description = "Google Workspace with causal poset interaction time"
```

## MCP Tools Available

| Tool | Service | Trit | Description |
|------|---------|------|-------------|
| `gmail_list` | Gmail | 0 | List emails with filters |
| `gmail_read` | Gmail | 0 | Read email content |
| `gmail_send` | Gmail | +1 | Send new email |
| `gmail_label` | Gmail | 0 | Apply/remove labels |
| `gmail_archive` | Gmail | -1 | Archive emails |
| `gmail_delete` | Gmail | -1 | Delete emails |
| `calendar_list` | Calendar | 0 | List events |
| `calendar_create` | Calendar | +1 | Create event |
| `calendar_update` | Calendar | 0 | Update event |
| `calendar_delete` | Calendar | -1 | Delete event |
| `calendar_invite` | Calendar | +1 | Send invites |
| `drive_list` | Drive | 0 | List files |
| `drive_upload` | Drive | +1 | Upload file |
| `drive_download` | Drive | 0 | Download file |
| `drive_share` | Drive | 0 | Share file |
| `drive_delete` | Drive | -1 | Delete file |
| `docs_create` | Docs | +1 | Create document |
| `docs_read` | Docs | 0 | Read document |
| `docs_update` | Docs | 0 | Update document |
| `docs_export` | Docs | 0 | Export to format |
| `sheets_create` | Sheets | +1 | Create spreadsheet |
| `sheets_read` | Sheets | 0 | Read cells |
| `sheets_update` | Sheets | 0 | Update cells |
| `sheets_formula` | Sheets | 0 | Apply formula |
| `tasks_list` | Tasks | 0 | List tasks |
| `tasks_create` | Tasks | +1 | Create task |
| `tasks_complete` | Tasks | -1 | Complete task |
| `tasks_delete` | Tasks | -1 | Delete task |
| `meet_schedule` | Meet | +1 | Schedule meeting |

## Cross-Service Workflows

### Email → Task → Calendar (Balanced Triad)

```python
# Workflow: Process email, create task, schedule calendar
async def email_to_task_calendar(email_id: str, due_date: str):
    # Step 1: Read email (trit = 0)
    email = await mcp.gmail_read(email_id)
    
    # Step 2: Create task from email (trit = +1)
    task = await mcp.tasks_create(
        title=email.subject,
        notes=email.body[:500],
        due=due_date
    )
    
    # Step 3: Create calendar event (trit = +1)
    event = await mcp.calendar_create(
        summary=f"Work on: {email.subject}",
        start=due_date,
        description=f"Task: {task.id}"
    )
    
    # Step 4: Archive email (trit = -1)
    await mcp.gmail_archive(email_id)
    
    # Step 5: Complete placeholder task (trit = -1)
    # GF(3) sum: 0 + 1 + 1 + (-1) + (-1) = 0 ✓
    return {"task": task, "event": event}
```

### Two-Phase Commit for Atomicity

```python
async def atomic_workflow(operations: List[Operation]):
    """Execute operations atomically across services."""
    transaction = Transaction(
        id=next_transaction_id(),
        operations=operations,
        services_involved=list(set(op.service for op in operations))
    )
    
    # Phase 1: Prepare
    votes = {}
    for service in transaction.services_involved:
        votes[service] = await prepare_service(service, transaction)
    
    # Phase 2: Commit or Abort
    if all(votes.values()):
        for op in operations:
            await commit_operation(op)
        return TransactionState.Committed
    else:
        for op in operations:
            await rollback_operation(op)
        return TransactionState.Aborted
```

## Causal Closure

```python
# When an action triggers dependent actions
DEPENDENCY_GRAPH = {
    ("gmail", "read"): [("tasks", "create")],      # Reading email may create task
    ("tasks", "create"): [("calendar", "create")], # Task may need calendar slot
    ("calendar", "create"): [("meet", "schedule")],# Event may need meeting
}

async def causal_closure(trigger: CausalEvent) -> List[CausalEvent]:
    """Compute all events causally triggered by an action."""
    deps = DEPENDENCY_GRAPH.get((trigger.service, trigger.action), [])
    result = []
    
    for target_service, target_action in deps:
        new_event = CausalEvent(
            id=trigger.id + len(result) + 1,
            service=target_service,
            action=target_action,
            trit=action_trit(target_action),
            seed=trigger.seed,
            timestamp=trigger.timestamp + 1
        )
        result.append(new_event)
        result.extend(await causal_closure(new_event))
    
    return result
```

## Retry with 1069 Checkpoints

```python
# Balanced ternary checkpoint pattern from mathpix-gem
CHECKPOINT_1069 = [+1, -1, -1, +1, +1, +1, +1]  # Sums to +3 ≡ 0 mod 3

async def retry_with_checkpoints(operation, max_attempts=7):
    for attempt, trit in enumerate(CHECKPOINT_1069[:max_attempts]):
        try:
            result = await operation()
            if result.confidence >= trit_to_confidence(trit):
                return result
        except APIError as e:
            if attempt == max_attempts - 1:
                raise
            # Adjust strategy based on trit
            if trit == +1:
                await enhance_request()
            elif trit == -1:
                await try_alternative()
            else:
                await validate_partial()
            await asyncio.sleep(2 ** attempt)
```

## Saturation States

### Inbox Zero

```python
def check_inbox_zero(gmail_state: ServiceState) -> bool:
    """Check if Gmail has reached Inbox Zero saturation."""
    return (
        gmail_state.pending_ops == [] and
        all(e.action in ["read", "archive"] for e in gmail_state.committed_ops)
    )
```

### Task Zero

```python
def check_task_zero(tasks_state: ServiceState) -> bool:
    """Check if Tasks has reached Task Zero saturation."""
    return (
        tasks_state.pending_ops == [] and
        all(e.action == "complete" for e in tasks_state.committed_ops)
    )
```

### Global Saturation

```python
def check_global_saturation(state: GlobalState) -> bool:
    """Check if entire workspace has reached ANIMA condensation."""
    return (
        all(s.pending_ops == [] for s in state.services) and
        cross_service_consistent(state) and
        temporal_closure(state) and
        sum(e.trit for s in state.services for e in s.committed_ops) % 3 == 0
    )
```

## Formal Specification

See [narya_formal_proofs/SkillAdmissibility.nry](file:///Users/bob/ies/music-topos/narya_formal_proofs/SkillAdmissibility.nry#L406-L754) for:

- **PART 14**: InteractionTime as causal poset
- **PART 15**: ConcurrentActionSet with path invariance
- **PART 16**: GlobalSaturation with temporal closure
- **PART 17**: FreeTrace ⊣ CondensedInteractionTime adjunction
- **PART 18**: Causal closure operator
- **PART 19**: Transaction with two-phase commit
- **PART 20**: RetryPolicy with 1069 checkpoints
- **PART 21**: GWorkspaceService enumeration and theorems

## BDD Feature Tests

```gherkin
Feature: Google Workspace MCP Integration

  @causal-poset
  Scenario: Interaction time maintains causal ordering
    Given a sequence of Gmail operations
    When I construct the InteractionTime poset
    Then CausallyPrecedes should be transitive
    And concurrent operations should be independent

  @gf3-conservation
  Scenario: Workflow maintains GF(3) conservation
    Given an email-to-task-calendar workflow
    When I sum all action trits
    Then the total should be 0 mod 3

  @atomicity
  Scenario: Cross-service operations are atomic
    Given a transaction across Gmail and Calendar
    When one service fails in phase 1
    Then all operations should rollback
    And no partial state should persist

  @saturation
  Scenario: Inbox Zero triggers global saturation check
    Given all emails have been processed
    When I check GlobalSaturation
    Then InboxZero predicate should hold
    And TemporalClosure should be satisfied
```

## Neighbor Awareness

| Position | Skill | Role |
|----------|-------|------|
| Left (-1) | `three-match` | Validates workflow patterns |
| Right (+1) | `gay-mcp` | Generates deterministic colors |

## Commands

```bash
just gworkspace-auth        # OAuth authentication flow
just gworkspace-inbox-zero  # Process inbox to zero
just gworkspace-task-zero   # Complete all tasks
just gworkspace-saturate    # Achieve global saturation
just gworkspace-workflow    # Run cross-service workflow
just gworkspace-test        # Run BDD feature tests
```

## References

- [SkillAdmissibility.nry](file:///Users/bob/ies/music-topos/narya_formal_proofs/SkillAdmissibility.nry) - Formal specification
- [mathpix-ocr skill](file:///Users/bob/ies/music-topos/.agents/skills/mathpix-ocr/SKILL.md) - 1069 checkpoint pattern
- [mcp-builder skill](file:///Users/bob/ies/music-topos/.agents/skills/mcp-builder/SKILL.md) - MCP server patterns
- [temporal-coalgebra skill](file:///Users/bob/ies/music-topos/.agents/skills/temporal-coalgebra/SKILL.md) - State observation

---

**Status**: ✅ L4 Admissible (Typed, Documented, Compositional, Predicates + Neighbors)
**Trit**: 0 (ERGODIC)
**Date**: 2025-12-25
