---
name: gmail-anima
description: Gmail inbox management via ANIMA condensation. Transforms messages into GF(3)-typed Interactions, routes to triadic queues, detects saturation for inbox-zero-as-condensed-state. Use for email triage, workflow automation, or applying ANIMA principles to Gmail.
version: 1.0.0
---


# Gmail ANIMA Skill

Transform Gmail into an ANIMA-condensed system with GF(3) conservation.

**Trit**: 0 (ERGODIC - coordinator)  
**Principle**: Inbox Zero = Condensed Equilibrium State  
**Implementation**: GmailACSet + TriadicQueues + AnimaDetector

## Overview

Gmail ANIMA applies the ANIMA framework to email:

1. **Transform** - Messages → GF(3)-typed Interactions
2. **Route** - Interactions → Triadic queue fibers (MINUS/ERGODIC/PLUS)
3. **Detect** - Saturation → ANIMA condensed state
4. **Verify** - Narya proofs for consistency

## GmailACSet Schema

```
┌────────────────────────────────────────────────────────────────────┐
│                      GmailACSet Schema                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Interaction ─────┬────▶ Thread                                   │
│  ├─ verb: String  │      ├─ thread_id: String                     │
│  ├─ timebin: Int  │      ├─ needs_action: Bool                    │
│  ├─ trit: Trit    │      ├─ last_action_bin: Int                  │
│  └─ person ───────┼──▶   └─ saturated: Bool                       │
│                   │                                                │
│  QueueItem ───────┼────▶ Agent3                                   │
│  ├─ interaction ──┘      ├─ fiber: Trit {-1, 0, +1}               │
│  └─ agent ───────────▶   └─ name: String                          │
│                                                                    │
│  Person ◀─────────────── Partner ────────────────▶ Person         │
│  ├─ email: String        ├─ src                                   │
│  └─ name: String         ├─ tgt                                   │
│                          └─ weight: Int                            │
└────────────────────────────────────────────────────────────────────┘
```

### Objects

| Object | Description | Trit Role |
|--------|-------------|-----------|
| `Interaction` | Single email action with verb + trit | Data |
| `Thread` | Gmail conversation with saturation state | Aggregate |
| `Agent3` | Queue fiber (MINUS/ERGODIC/PLUS) | Router |
| `QueueItem` | Links Interaction → Agent3 | Edge |
| `Person` | Email contact | Node |
| `Partner` | Relationship edge in contact graph | Edge |

## GF(3) Verb Typing

Gmail actions are assigned trits based on information flow:

```python
VERB_TRIT_MAP = {
    # MINUS (-1): Consumption/Validation
    "read": -1,      "search": -1,     "view": -1,
    "fetch": -1,     "list": -1,
    
    # ERGODIC (0): Coordination/Metadata
    "label": 0,      "archive": 0,     "snooze": 0,
    "star": 0,       "mark_read": 0,   "mark_unread": 0,
    "move": 0,
    
    # PLUS (+1): Generation/Execution
    "send": +1,      "forward": +1,    "reply": +1,
    "schedule": +1,  "draft": +1,      "compose": +1,
}
```

### MCP Tool → Trit Mapping

| Tool | Trit | Description |
|------|------|-------------|
| `search_gmail_messages` | -1 | Search inbox (MINUS) |
| `get_gmail_message_content` | -1 | Read message (MINUS) |
| `get_gmail_thread_content` | -1 | Read thread (MINUS) |
| `list_gmail_labels` | -1 | List labels (MINUS) |
| `modify_gmail_message_labels` | 0 | Change labels (ERGODIC) |
| `batch_modify_gmail_message_labels` | 0 | Bulk labels (ERGODIC) |
| `send_gmail_message` | +1 | Send email (PLUS) |
| `draft_gmail_message` | +1 | Create draft (PLUS) |

## Triadic Queue Routing

Interactions route to disjoint queue fibers:

```
                    ┌─────────────────────────────────────────┐
                    │           TRIADIC QUEUES                │
                    ├─────────────────────────────────────────┤
                    │                                         │
   Interaction ────▶│  route(trit) ───▶ Agent3 Fiber         │
                    │                                         │
                    │  MINUS (-1)  ────▶ [read, search, ...]  │
                    │  ERGODIC (0) ────▶ [label, archive, ...]│
                    │  PLUS (+1)   ────▶ [send, reply, ...]   │
                    │                                         │
                    └─────────────────────────────────────────┘
```

### Invariants

1. **No duplication**: Each interaction in exactly one fiber
2. **Route invariant**: `agent_of(i) = route(trit(i))`
3. **Ordering**: PLUS must be preceded by MINUS in same thread
4. **Conservation**: Thread trit sum ≡ 0 (mod 3) at cycle close

### Queue Depth Balance

```python
def saturation_metrics(queues: Dict[Agent3, deque]) -> Dict:
    depths = [len(q) for q in queues.values()]
    return {
        'balance_ratio': min(depths) / max(depths),  # 1.0 = perfect
        'gf3_residue': sum(i.trit for q in queues for i in q) % 3,
    }
```

## Saturation Detection → ANIMA State

Saturation occurs when a thread reaches stable equilibrium:

```python
def is_saturated(thread_id: str) -> bool:
    """Thread is saturated when:
    1. No change in needs_action for N steps
    2. GF(3) cycle closure: sum(trits) ≡ 0 (mod 3)
    3. History window shows identical states
    """
    history = detector.history[thread_id][-N:]
    cycle_sum = sum(t for t in thread.gf3_cycle[-3:])
    
    return (
        all(s == history[0] for s in history) and  # Stable
        (cycle_sum % 3) == 0                        # Conserved
    )
```

### ANIMA Detection

```python
def detect_anima() -> Dict:
    """System at ANIMA when:
    1. All threads saturated
    2. GF(3) conserved globally
    3. Equivalence classes stable
    4. Replay invariance holds
    """
    return {
        "at_anima": all_saturated and gf3_conserved and stable_impacts,
        "condensed_fingerprint": sha256(sorted_equiv_classes),
        "persistence_bars_stable": True,
    }
```

**Inbox Zero as ANIMA**: When all threads reach saturation with GF(3) conservation, the inbox is in condensed equilibrium.

## Narya Proof Integration

Proofs in [`src/narya_proofs/`](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/):

### 1. Queue Consistency ([queue_consistency.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/queue_consistency.py))

```python
def prove_queue_consistency(system: TriadicQueueSystem) -> bool:
    """Verify no duplication and route invariant."""
    return (
        system.verify_no_duplication() and
        system.verify_route_invariant()
    )
```

### 2. Replay Determinism ([replay_determinism.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/replay_determinism.py))

```python
def prove_replay_determinism(schedule1, schedule2) -> bool:
    """Different schedules → identical condensed state."""
    fp1 = replay(schedule1).condensed_fingerprint
    fp2 = replay(schedule2).condensed_fingerprint
    return fp1 == fp2
```

### 3. Non-Leakage ([non_leakage.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/non_leakage.py))

```python
def prove_non_leakage(bridge: GmailMCPBridge) -> bool:
    """No interaction leaks between fibers."""
    for agent, queue in bridge.queues.items():
        for item in queue:
            if bridge._route(item.trit) != agent:
                return False
    return True
```

### 4. GF(3) Conservation ([gf3_conservation.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/gf3_conservation.py))

```python
def prove_gf3_conservation(bridge: GmailMCPBridge) -> bool:
    """All closed cycles satisfy sum ≡ 0 (mod 3)."""
    for cycle in bridge.cycle_tracker.closed_cycles:
        if sum(cycle.trits) % 3 != 0:
            return False
    return True
```

## Source Files

| File | Description | Trit |
|------|-------------|------|
| [gmail_acset.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/gmail_acset.py) | ACSet schema + GF(3) thread tracking | 0 |
| [anima_detector.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/anima_detector.py) | Saturation + equilibrium detection | 0 |
| [gmail_mcp_bridge.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/gmail_mcp_bridge.py) | MCP tool wiring with guards | 0 |
| [triadic_queues.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/triadic_queues.py) | Three disjoint queue fibers | 0 |
| [narya_proofs/](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/) | Formal verification proofs | -1 |

## Workflows

### Workflow 1: Triage Inbox to ANIMA

```python
from gmail_mcp_bridge import create_gmail_bridge
from anima_detector import AnimaDetector

# Create bridge
bridge = create_gmail_bridge("user@gmail.com")
detector = AnimaDetector(saturation_threshold=5)

# MINUS: Read unread messages
bridge.search_gmail_messages("is:unread")
for msg in results:
    bridge.get_gmail_message_content(msg.id, thread_id=msg.thread_id)
    detector.update_thread(msg.thread_id, trit=Trit.MINUS)

# ERGODIC: Label/archive processed
for msg in processed:
    bridge.modify_gmail_message_labels(
        msg.id,
        add_label_ids=["Label_Processed"],
        remove_label_ids=["INBOX"],
        thread_id=msg.thread_id
    )
    detector.update_thread(msg.thread_id, trit=Trit.ERGODIC)

# Check ANIMA
anima = detector.detect_anima()
if anima["at_anima"]:
    say("Inbox at ANIMA. Condensed state achieved.")
```

### Workflow 2: Reply with GF(3) Guard

```python
# MINUS first: Read the thread
bridge.get_gmail_thread_content(thread_id)  # trit=-1

# PLUS: Reply (requires prior MINUS)
try:
    bridge.send_gmail_message(
        to="reply@example.com",
        subject="Re: Topic",
        body="Response...",
        thread_id=thread_id,
        in_reply_to=original_message_id
    )  # trit=+1
except GF3ConservationError:
    # Must read before sending
    bridge.get_gmail_thread_content(thread_id)  # Retry after MINUS
    bridge.send_gmail_message(...)
```

### Workflow 3: Batch Triage with Saturation

```python
# Create balanced batch
batch = create_triadic_batch(
    payloads=["read_1", "label_1", "archive_1"],  # Will balance to 0
    thread_id="batch_thread",
    seed=1069
)

system = TriadicQueueSystem()
for interaction in batch:
    if system.enqueue(interaction):
        print(f"✓ {interaction.payload} → {interaction.agent.name}")

# Check metrics
stats = system.full_statistics()
print(f"GF(3) Residue: {stats['saturation']['gf3_residue']}")  # 0
print(f"Cycles Closed: {stats['operations']['cycles_closed']}")
```

### Workflow 4: Sheaf Cohomology Verification

```python
# After processing
h1 = bridge.verify_h1_obstruction()
print(f"H¹ obstructions: {h1['h1']}")
print(f"Globally consistent: {h1['globally_consistent']}")

# Obstructions = threads not at GF(3) = 0
for v in h1['violations']:
    print(f"  Thread {v['thread_id']}: residue={v['mod_3']}")
```

## Commands

```bash
# Run Gmail ANIMA demo
python src/gmail_acset.py

# Test triadic queues
python src/triadic_queues.py

# Run ANIMA detector
python src/anima_detector.py

# Run Narya proofs
python -m src.narya_proofs.runner
```

## Integration with Other Skills

| Skill | Trit | Integration |
|-------|------|-------------|
| [google-workspace](file:///Users/alice/.claude/skills/google-workspace/SKILL.md) | 0 | MCP tool provider |
| [gay-mcp](file:///Users/alice/.agents/skills/gay-mcp/SKILL.md) | +1 | SplitMixTernary RNG |
| [sheaf-cohomology](file:///Users/alice/.claude/skills/sheaf-cohomology/SKILL.md) | -1 | H¹ obstruction verification |
| [bisimulation-game](file:///Users/alice/.agents/skills/bisimulation-game/SKILL.md) | -1 | State equivalence proofs |
| [ordered-locale](file:///Users/alice/.agents/skills/ordered-locale-proper/SKILL.md) | 0 | Thread ordering topology |

### GF(3) Triadic Conservation

```
gmail-anima (0) ⊗ sheaf-cohomology (-1) ⊗ gay-mcp (+1) = 0 ✓
gmail-anima (0) ⊗ bisimulation-game (-1) ⊗ send (+1) = 0 ✓
read (-1) ⊗ label (0) ⊗ reply (+1) = 0 ✓
```

## Cross-Skill Integration

Gmail-ANIMA integrates with the full workspace via `WorkspaceACSet`:

### Morphisms from Gmail

| Morphism | Target | Trigger | GF(3) Effect |
|----------|--------|---------|--------------|
| `thread_file` | DriveFile | Attachment detected | 0 (ERGODIC) |
| `thread_event` | CalendarEvent | Meeting scheduled | +1 (PLUS) |
| `thread_task` | Task | Action item identified | +1 (PLUS) |

### Workflow Paths

```python
# Gmail → Task (balanced)
path = gmail_read >> task_create  # -1 + 1 = 0 ✓

# Full workflow (needs balancing)
full = gmail_read >> drive_create >> calendar_create >> task_create
balanced = balance_path(full)  # Auto-adds ERGODIC steps
```

### MCP ↔ API Equivalence

Gmail operations can be executed via MCP tools or direct API:

```python
# Equivalent executions
mcp_result = bridge.execute_mcp("send_gmail_message", params)
api_result = bridge.execute_api("gmail_send", params)
assert mcp_result.state == api_result.state
```

## Source Files (Extended)

| File | Description |
|------|-------------|
| [workspace_acset.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/workspace_acset.py) | Unified schema with cross-skill morphisms |
| [mcp_api_equivalence.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/mcp_api_equivalence.py) | MCP↔API behavioral equivalence |
| [path_invariance.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/path_invariance.py) | Workflow path verification |
| [workflow_validator.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/workflow_validator.py) | End-to-end validation |

## ANIMA Principles Applied

| ANIMA Concept | Gmail Implementation |
|---------------|---------------------|
| **Saturation** | Thread trit sum ≡ 0 (mod 3) |
| **Condensation** | Equivalence class collapse |
| **MaxEnt Default** | needs_action=False initially |
| **Persistence** | Only flip when forced |
| **Replay Invariance** | Schedule-independent fingerprint |

## Say Narration Integration

```python
from gmail_mcp_bridge import NaryaLogger

logger = NaryaLogger(voice="Ava (Premium)")

# Announces: "Gmail bridge: MINUS transition"
logger.log(before, after, Trit.MINUS, impact=False)

# Announces: "Gmail bridge: PLUS transition, impact detected"
logger.log(before, after, Trit.PLUS, impact=True)
```

---

**Skill Name**: gmail-anima  
**Type**: Email Management / ANIMA Framework  
**Trit**: 0 (ERGODIC - coordinator)  
**GF(3)**: Conserved via triadic queue routing  
**ANIMA**: Inbox Zero = Condensed Equilibrium State



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
gmail-anima (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch6: Layering
- Ch1: Flexibility through Abstraction

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.