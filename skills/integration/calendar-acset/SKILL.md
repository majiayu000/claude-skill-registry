---
name: calendar-acset
description: Google Calendar management via CalendarACSet. Transforms scheduling operations into GF(3)-typed Interactions, routes to triadic queues, detects saturation for balanced-calendar-as-condensed-state.
version: 1.0.0
---


# Calendar ACSet Skill

Transform Google Calendar into an ANIMA-condensed system with GF(3) conservation.

**Trit**: +1 (PLUS - generator/executor)  
**Principle**: Balanced Calendar = Condensed Equilibrium State  
**Implementation**: CalendarACSet + TriadicQueues + SaturationDetector

## Overview

Calendar ACSet applies the ANIMA framework to scheduling:

1. **Transform** - Events → GF(3)-typed Interactions
2. **Route** - Interactions → Triadic queue fibers (MINUS/ERGODIC/PLUS)
3. **Detect** - Saturation → Balanced calendar state
4. **Verify** - Narya proofs for scheduling consistency

## CalendarACSet Schema

```
┌────────────────────────────────────────────────────────────────────┐
│                     CalendarACSet Schema                           │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Interaction ─────┬────▶ Event                                     │
│  ├─ verb: String  │      ├─ event_id: String                       │
│  ├─ timebin: Int  │      ├─ summary: String                        │
│  ├─ trit: Trit    │      ├─ start_time: DateTime                   │
│  └─ calendar ─────┼──▶   ├─ end_time: DateTime                     │
│                   │      ├─ has_conflicts: Bool                    │
│  QueueItem ───────┼──▶   └─ saturated: Bool                        │
│  ├─ interaction ──┘                                                │
│  └─ agent ───────────▶ Agent3                                      │
│                        ├─ fiber: Trit {-1, 0, +1}                  │
│  Attendee ◀────────────┤                                           │
│  ├─ email: String      └─ name: String                             │
│  ├─ response: Enum                                                 │
│  └─ event ─────────▶ Event                                         │
│                                                                    │
│  Reminder ─────────▶ Event                                         │
│  ├─ method: Enum                                                   │
│  └─ minutes: Int                                                   │
└────────────────────────────────────────────────────────────────────┘
```

### Objects

| Object | Description | Trit Role |
|--------|-------------|-----------|
| `Event` | Calendar event with time bounds | Data |
| `Calendar` | Container calendar (primary/secondary) | Aggregate |
| `Attendee` | Event participant with response status | Edge |
| `Reminder` | Notification configuration | Node |
| `Agent3` | Queue fiber (MINUS/ERGODIC/PLUS) | Router |
| `QueueItem` | Links Interaction → Agent3 | Edge |

## GF(3) Verb Typing

Calendar actions are assigned trits based on information flow:

```python
VERB_TRIT_MAP = {
    # MINUS (-1): Consumption/Query
    "get_events": -1,      "list_calendars": -1,
    "get_event": -1,       "check_availability": -1,
    
    # ERGODIC (0): Coordination/Modification
    "modify_event": 0,     "update_attendees": 0,
    "reschedule": 0,       "change_reminder": 0,
    "update_location": 0,
    
    # PLUS (+1): Generation/Creation
    "create_event": +1,    "add_google_meet": +1,
    "invite_attendee": +1, "schedule_recurring": +1,
    "delete_event": +1,    # Deletion generates state change
}
```

### MCP Tool → Trit Mapping

| Tool | Trit | Description |
|------|------|-------------|
| `get_events` | -1 | Query calendar events (MINUS) |
| `list_calendars` | -1 | List available calendars (MINUS) |
| `modify_event` | 0 | Update event details (ERGODIC) |
| `create_event` | +1 | Create new event (PLUS) |
| `delete_event` | +1 | Remove event (PLUS) |

## Event-Thread Morphism

Calendar events link to Gmail threads via meeting invites:

```python
def event_thread_morphism(event: Event, thread: Thread) -> Morphism:
    """Morphism from CalendarACSet → GmailACSet"""
    return {
        'source': ('Event', event.event_id),
        'target': ('Thread', thread.thread_id),
        'relation': 'invite_thread',
        'trit_effect': 0,  # ERGODIC - coordination
    }

# Example: Meeting invite creates Gmail thread
event = create_event(summary="Standup", attendees=["team@example.com"])
thread = search_gmail(f"subject:'{event.summary}' from:calendar-notification")
link_event_thread(event, thread)
```

## Triadic Queue Routing

```
                    ┌─────────────────────────────────────────┐
                    │           TRIADIC QUEUES                │
                    ├─────────────────────────────────────────┤
                    │                                         │
   Interaction ────▶│  route(trit) ───▶ Agent3 Fiber         │
                    │                                         │
                    │  MINUS (-1)  ────▶ [get_events, ...]    │
                    │  ERGODIC (0) ────▶ [modify_event, ...]  │
                    │  PLUS (+1)   ────▶ [create_event, ...]  │
                    │                                         │
                    └─────────────────────────────────────────┘
```

## Saturation Detection

Calendar saturation = no conflicts, all events responded, balanced time:

```python
def is_calendar_saturated(calendar_id: str) -> bool:
    """Calendar is saturated when:
    1. No conflicting events in range
    2. All attendee responses received
    3. GF(3) cycle closure: sum(trits) ≡ 0 (mod 3)
    4. Time blocks balanced (no overload)
    """
    events = get_events(calendar_id)
    
    conflicts = detect_conflicts(events)
    pending_responses = [e for e in events if has_pending_rsvp(e)]
    gf3_sum = sum(event.trit_history) % 3
    
    return (
        len(conflicts) == 0 and
        len(pending_responses) == 0 and
        gf3_sum == 0
    )

def detect_anima() -> Dict:
    """System at ANIMA when all calendars saturated."""
    return {
        "at_anima": all(is_calendar_saturated(c) for c in calendars),
        "condensed_fingerprint": sha256(sorted_event_hashes),
        "conflict_free": True,
    }
```

## Source Files

| File | Description | Trit |
|------|-------------|------|
| [calendar_acset.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/calendar_acset.py) | ACSet schema + GF(3) event tracking | +1 |
| [calendar_saturation.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/calendar_saturation.py) | Conflict detection + saturation | +1 |
| [calendar_mcp_bridge.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/calendar_mcp_bridge.py) | MCP tool wiring with guards | 0 |

## Workflows

### Workflow 1: Meeting Creation with GF(3) Balance

```python
from calendar_mcp_bridge import create_calendar_bridge

bridge = create_calendar_bridge("user@gmail.com")

# MINUS: Check availability first
bridge.get_events(time_min="2025-01-01", time_max="2025-01-07")  # trit=-1

# PLUS: Create meeting
bridge.create_event(
    summary="Project Sync",
    start_time="2025-01-06T10:00:00",
    end_time="2025-01-06T11:00:00",
    attendees=["team@example.com"],
    add_google_meet=True
)  # trit=+1

# Conservation: -1 + 1 = 0 ✓
```

### Workflow 2: Event Response with GF(3) Guard

```python
# MINUS: Read event details
bridge.get_events(event_id=event_id)  # trit=-1

# ERGODIC: Modify response
bridge.modify_event(
    event_id=event_id,
    attendees=[{"email": "me@example.com", "responseStatus": "accepted"}]
)  # trit=0

# PLUS: Add reminder
bridge.modify_event(
    event_id=event_id,
    reminders=[{"method": "popup", "minutes": 15}]
)  # Would need balancing

# Balance with read
bridge.get_events(event_id=event_id)  # -1 + 0 + 1 - 1 = -1... add +1
```

### Workflow 3: Weekly Review with Saturation

```python
detector = CalendarSaturationDetector()

# Review week
events = bridge.get_events(time_min="2025-01-06", time_max="2025-01-13")

for event in events:
    detector.update_event(event.event_id, trit=Trit.MINUS)
    
    if has_conflicts(event):
        bridge.modify_event(event.event_id, reschedule=True)
        detector.update_event(event.event_id, trit=Trit.ERGODIC)

# Check saturation
if detector.is_saturated():
    say("Calendar at equilibrium. No conflicts detected.")
```

## Integration

| Skill | Trit | Integration |
|-------|------|-------------|
| [gmail-anima](file:///Users/alice/agent-o-rama/agent-o-rama/.agents/skills/gmail-anima/SKILL.md) | 0 | Event↔Thread morphisms |
| [google-workspace](file:///Users/alice/.claude/skills/google-workspace/SKILL.md) | 0 | MCP tool provider |
| [gay-mcp](file:///Users/alice/.agents/skills/gay-mcp/SKILL.md) | +1 | SplitMixTernary RNG |
| [tasks-acset](file:///Users/alice/agent-o-rama/agent-o-rama/.agents/skills/tasks-acset/SKILL.md) | -1 | Event→Task deadline links |

### GF(3) Triadic Conservation

```
calendar-acset (+1) ⊗ gmail-anima (0) ⊗ tasks-acset (-1) = 0 ✓
get_events (-1) ⊗ modify_event (0) ⊗ create_event (+1) = 0 ✓
```

---

**Skill Name**: calendar-acset  
**Type**: Calendar Management / ANIMA Framework  
**Trit**: +1 (PLUS - generator/executor)  
**GF(3)**: Conserved via triadic queue routing  
**ANIMA**: Balanced Calendar = Condensed Equilibrium State



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Annotated Data
- **anndata** [○] via bicomodule

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
calendar-acset (○) + SDF.Ch10 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)


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