---
name: workspace-unified
description: Unified Google Workspace management via WorkspaceACSet. Transforms operations into GF(3)-typed Interactions across Gmail, Drive, Calendar, Tasks, Docs with cross-skill morphisms and MCP↔API equivalence. Use for multi-service workflows or applying ACSet principles to workspace automation.
---

# Workspace Unified Skill

Transform Google Workspace into an ACSet-structured system with GF(3) conservation and cross-skill morphisms.

**Trit**: 0 (ERGODIC - coordinator)  
**Principle**: Workflow Completion = Condensed Equilibrium State  
**Implementation**: WorkspaceACSet + PathInvariance + MCPAPIBridge

## Overview

Workspace Unified applies categorical database principles to workspace:

1. **Transform** - Operations → GF(3)-typed Interactions
2. **Route** - Interactions → Service-specific ACSet objects
3. **Compose** - Cross-skill morphisms with path commutativity
4. **Verify** - MCP↔API equivalence and Narya proofs

## WorkspaceACSet Schema

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              WorkspaceACSet Schema                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  Interaction ───────────┬──────▶ Thread ◀───────────────── DriveFile                    │
│  ├─ verb: String        │        ├─ thread_id: String       ├─ file_id: String          │
│  ├─ timebin: Int        │        ├─ needs_action: Bool      ├─ mime_type: String        │
│  ├─ trit: Trit          │        ├─ last_action_bin: Int    └─ saturated: Bool          │
│  ├─ service: Service    │        └─ saturated: Bool                                      │
│  └─ person ─────────────┼──▶                                                             │
│                         │                                                                │
│  CalendarEvent ◀────────┼──────── TaskList ◀────────────── Task                         │
│  ├─ event_id: String    │         ├─ list_id: String        ├─ task_id: String          │
│  ├─ summary: String     │         └─ title: String          ├─ title: String            │
│  ├─ start: DateTime     │                                   ├─ status: String           │
│  └─ saturated: Bool     │                                   └─ due: DateTime            │
│                         │                                                                │
│  Document ◀─────────────┼──────── Sheet                                                  │
│  ├─ doc_id: String      │         ├─ sheet_id: String                                   │
│  ├─ title: String       │         ├─ title: String                                      │
│  └─ content: Text       │         └─ values: Matrix                                     │
│                         │                                                                │
│  QueueItem ─────────────┼──────▶ Agent3                                                  │
│  ├─ interaction ────────┘        ├─ fiber: Trit {-1, 0, +1}                              │
│  └─ agent ───────────────▶       └─ name: String                                         │
│                                                                                          │
│  Person ◀─────────────────────── Partner ─────────────────▶ Person                       │
│  ├─ email: String                ├─ src                                                  │
│  └─ name: String                 ├─ tgt                                                  │
│                                  └─ weight: Int                                          │
│                                                                                          │
│  Service                                                                                 │
│  ├─ name: String {gmail, drive, calendar, tasks, docs, sheets}                          │
│  └─ default_trit: Trit                                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### Objects

| Object | Description | Trit Role |
|--------|-------------|-----------|
| `Interaction` | Single workspace action with verb + trit + service | Data |
| `Thread` | Gmail conversation with saturation state | Gmail Aggregate |
| `DriveFile` | File or folder in Drive | Drive Aggregate |
| `CalendarEvent` | Meeting or event | Calendar Aggregate |
| `TaskList` | Container for tasks | Tasks Container |
| `Task` | Individual action item | Tasks Aggregate |
| `Document` | Google Doc content | Docs Aggregate |
| `Sheet` | Spreadsheet data | Sheets Aggregate |
| `Agent3` | Queue fiber (MINUS/ERGODIC/PLUS) | Router |
| `QueueItem` | Links Interaction → Agent3 | Edge |
| `Person` | User or contact | Node |
| `Partner` | Relationship edge in contact graph | Edge |
| `Service` | Workspace service identifier | Metadata |

## GF(3) Service Typing

Workspace actions are assigned trits based on information flow:

```python
VERB_TRIT_MAP = {
    # ═══════════════════════════════════════════════════════════════
    # GMAIL
    # ═══════════════════════════════════════════════════════════════
    # MINUS (-1): Consumption/Validation
    "gmail_read": -1,     "gmail_search": -1,    "gmail_get_thread": -1,
    "gmail_list_labels": -1,
    
    # ERGODIC (0): Coordination/Metadata
    "gmail_label": 0,     "gmail_archive": 0,    "gmail_snooze": 0,
    "gmail_star": 0,      "gmail_mark_read": 0,  "gmail_move": 0,
    
    # PLUS (+1): Generation/Execution
    "gmail_send": +1,     "gmail_forward": +1,   "gmail_reply": +1,
    "gmail_draft": +1,    "gmail_compose": +1,
    
    # ═══════════════════════════════════════════════════════════════
    # DRIVE
    # ═══════════════════════════════════════════════════════════════
    # MINUS (-1)
    "drive_get_content": -1, "drive_list": -1,   "drive_search": -1,
    "drive_get_permissions": -1,
    
    # ERGODIC (0)
    "drive_share": 0,     "drive_move": 0,       "drive_rename": 0,
    "drive_update_metadata": 0,
    
    # PLUS (+1)
    "drive_create": +1,   "drive_upload": +1,    "drive_copy": +1,
    
    # ═══════════════════════════════════════════════════════════════
    # CALENDAR
    # ═══════════════════════════════════════════════════════════════
    # MINUS (-1)
    "calendar_get_events": -1, "calendar_list": -1, "calendar_get_event": -1,
    
    # ERGODIC (0)
    "calendar_modify": 0, "calendar_reschedule": 0, "calendar_update_attendees": 0,
    
    # PLUS (+1)
    "calendar_create": +1, "calendar_invite": +1, "calendar_duplicate": +1,
    
    # ═══════════════════════════════════════════════════════════════
    # TASKS
    # ═══════════════════════════════════════════════════════════════
    # MINUS (-1)
    "tasks_list": -1,     "tasks_get": -1,       "tasks_list_lists": -1,
    
    # ERGODIC (0)
    "tasks_update": 0,    "tasks_move": 0,       "tasks_complete": 0,
    
    # PLUS (+1)
    "tasks_create": +1,   "tasks_create_list": +1,
    
    # ═══════════════════════════════════════════════════════════════
    # DOCS
    # ═══════════════════════════════════════════════════════════════
    # MINUS (-1)
    "docs_get_content": -1, "docs_read_comments": -1, "docs_inspect": -1,
    
    # ERGODIC (0)
    "docs_find_replace": 0, "docs_update_headers": 0, "docs_format": 0,
    
    # PLUS (+1)
    "docs_create": +1,    "docs_insert_text": +1, "docs_create_table": +1,
    
    # ═══════════════════════════════════════════════════════════════
    # SHEETS
    # ═══════════════════════════════════════════════════════════════
    # MINUS (-1)
    "sheets_read": -1,    "sheets_get_info": -1,
    
    # ERGODIC (0)
    "sheets_clear": 0,
    
    # PLUS (+1)
    "sheets_write": +1,   "sheets_create": +1,   "sheets_create_sheet": +1,
}
```

### MCP Tool → Trit Mapping

| Tool | Trit | Service | Description |
|------|------|---------|-------------|
| `search_gmail_messages` | -1 | Gmail | Search inbox (MINUS) |
| `get_gmail_message_content` | -1 | Gmail | Read message (MINUS) |
| `get_gmail_thread_content` | -1 | Gmail | Read thread (MINUS) |
| `list_gmail_labels` | -1 | Gmail | List labels (MINUS) |
| `modify_gmail_message_labels` | 0 | Gmail | Change labels (ERGODIC) |
| `batch_modify_gmail_message_labels` | 0 | Gmail | Bulk labels (ERGODIC) |
| `send_gmail_message` | +1 | Gmail | Send email (PLUS) |
| `draft_gmail_message` | +1 | Gmail | Create draft (PLUS) |
| `list_drive_items` | -1 | Drive | List files (MINUS) |
| `get_drive_file_content` | -1 | Drive | Read file (MINUS) |
| `search_drive_files` | -1 | Drive | Search files (MINUS) |
| `share_drive_file` | 0 | Drive | Share file (ERGODIC) |
| `update_drive_file` | 0 | Drive | Update metadata (ERGODIC) |
| `create_drive_file` | +1 | Drive | Create file (PLUS) |
| `get_events` | -1 | Calendar | Get events (MINUS) |
| `modify_event` | 0 | Calendar | Modify event (ERGODIC) |
| `create_event` | +1 | Calendar | Create event (PLUS) |
| `list_tasks` | -1 | Tasks | List tasks (MINUS) |
| `get_task` | -1 | Tasks | Get task (MINUS) |
| `update_task` | 0 | Tasks | Update task (ERGODIC) |
| `create_task` | +1 | Tasks | Create task (PLUS) |
| `get_doc_content` | -1 | Docs | Read doc (MINUS) |
| `create_doc` | +1 | Docs | Create doc (PLUS) |
| `read_sheet_values` | -1 | Sheets | Read sheet (MINUS) |
| `modify_sheet_values` | +1 | Sheets | Write sheet (PLUS) |

## Cross-Skill Morphisms

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        CROSS-SKILL MORPHISM DIAGRAM                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                            thread_file                                       │
│            Thread ─────────────────────────────▶ DriveFile                   │
│              │                                       │                       │
│              │ thread_event                          │ file_event            │
│              ▼                                       ▼                       │
│        CalendarEvent ◀───── event_file ─────── DriveFile                     │
│              │                                       │                       │
│              │ event_task                            │ file_task             │
│              ▼                                       ▼                       │
│            Task ◀──────────────────────────────── Task                       │
│              │                                       │                       │
│              │ task_doc                              │ file_doc              │
│              ▼                                       ▼                       │
│          Document ◀───────────────────────────── Document                    │
│              │                                                               │
│              │ doc_sheet                                                     │
│              ▼                                                               │
│           Sheet                                                              │
│                                                                              │
│   GF(3) Conservation: All morphism paths preserve trit balance               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Morphism Table

| Morphism | Source | Target | Trigger | GF(3) Effect |
|----------|--------|--------|---------|--------------|
| `thread_file` | Thread | DriveFile | Attachment detected | 0 (ERGODIC) |
| `thread_event` | Thread | CalendarEvent | Meeting scheduled | +1 (PLUS) |
| `thread_task` | Thread | Task | Action item identified | +1 (PLUS) |
| `file_event` | DriveFile | CalendarEvent | File-linked meeting | +1 (PLUS) |
| `file_task` | DriveFile | Task | File review needed | +1 (PLUS) |
| `file_doc` | DriveFile | Document | Content extraction | 0 (ERGODIC) |
| `event_task` | CalendarEvent | Task | Event followup | +1 (PLUS) |
| `event_doc` | CalendarEvent | Document | Meeting notes | +1 (PLUS) |
| `task_doc` | Task | Document | Task documentation | +1 (PLUS) |
| `doc_sheet` | Document | Sheet | Data extraction | 0 (ERGODIC) |

### Path Commutativity

```
                     thread_task
Gmail.Thread ─────────────────────────────────▶ Tasks.Task
     │                                              │
     │ thread_event                                 │ (identity)
     ▼                                              ▼
Calendar.Event ────────────────────────────────▶ Tasks.Task
                      event_task

INVARIANT: thread_task == event_task ∘ thread_event
```

```
                      thread_file
Gmail.Thread ─────────────────────────────────▶ Drive.File
     │                                              │
     │ thread_event                                 │ file_event
     ▼                                              ▼
Calendar.Event ◀─────── event_file ─────────── Calendar.Event

INVARIANT: thread_event == event_file⁻¹ ∘ file_event ∘ thread_file
```

## Saturation Detection → ANIMA State

```python
def is_workspace_saturated() -> bool:
    """Workspace is saturated when:
    1. All services reach their saturation threshold
    2. GF(3) global conservation: sum(trits) ≡ 0 (mod 3)
    3. All cross-skill morphism paths commute
    4. No pending interactions in any queue
    """
    service_states = {
        'gmail': gmail_saturated(),
        'drive': drive_saturated(),
        'calendar': calendar_saturated(),
        'tasks': tasks_saturated(),
        'docs': docs_saturated(),
        'sheets': sheets_saturated(),
    }
    
    global_trit_sum = sum(
        interaction.trit 
        for service in services 
        for interaction in service.interactions
    )
    
    return (
        all(service_states.values()) and           # All saturated
        (global_trit_sum % 3) == 0 and             # GF(3) conserved
        verify_path_commutativity() and            # Morphisms commute
        all_queues_empty()                         # No pending work
    )

def detect_anima() -> Dict:
    """System at ANIMA when workspace is condensed."""
    return {
        "at_anima": is_workspace_saturated(),
        "condensed_fingerprint": sha256(workspace_state_hash()),
        "service_states": get_all_service_states(),
        "gf3_balance": compute_global_gf3_balance(),
        "pending_interactions": count_pending_interactions(),
    }
```

### Per-Service Saturation Thresholds

```python
SATURATION_THRESHOLDS = {
    'gmail_threads': 1000,
    'drive_files': 500,
    'calendar_events': 200,
    'tasks': 300,
    'docs': 100,
    'sheets': 50,
}

def service_saturated(service: str) -> bool:
    count = get_service_object_count(service)
    threshold = SATURATION_THRESHOLDS.get(service, 100)
    return count >= threshold
```

## Narya Proof Integration

Proofs in [`src/narya_proofs/`](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/):

### 1. Path Commutativity ([path_commutativity.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/path_commutativity.py))

```python
def prove_path_commutativity(workspace: WorkspaceACSet) -> bool:
    """Verify all morphism paths commute."""
    # thread_task == event_task ∘ thread_event
    for thread in workspace.threads:
        direct = workspace.thread_task(thread)
        composed = workspace.event_task(workspace.thread_event(thread))
        if direct != composed:
            return False
    return True
```

### 2. GF(3) Global Conservation ([gf3_global.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/gf3_global.py))

```python
def prove_gf3_global_conservation(workspace: WorkspaceACSet) -> bool:
    """All cross-service workflows satisfy sum ≡ 0 (mod 3)."""
    for workflow in workspace.workflows:
        trit_sum = sum(op.trit for op in workflow.operations)
        if trit_sum % 3 != 0:
            return False
    return True
```

### 3. MCP↔API Equivalence ([mcp_api_equiv.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/mcp_api_equiv.py))

```python
def prove_mcp_api_equivalence(bridge: WorkspaceBridge) -> bool:
    """MCP and API executions produce identical states."""
    for operation in bridge.supported_operations:
        mcp_state = bridge.execute_mcp(operation, test_params)
        api_state = bridge.execute_api(operation, test_params)
        if normalize(mcp_state) != normalize(api_state):
            return False
    return True
```

### 4. Cross-Service Integrity ([cross_service.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/cross_service.py))

```python
def prove_cross_service_integrity(workspace: WorkspaceACSet) -> bool:
    """Thread IDs, file IDs consistent across all services."""
    for morphism in workspace.morphisms:
        source_id = morphism.source.id
        target_id = morphism.target.id
        if not workspace.verify_id_consistency(source_id, target_id):
            return False
    return True
```

## Source Files

| File | Description | Trit |
|------|-------------|------|
| [workspace_acset.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/workspace_acset.py) | ACSet schema + cross-skill morphisms | 0 |
| [workspace_detector.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/workspace_detector.py) | Saturation + equilibrium detection | 0 |
| [workspace_bridge.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/workspace_bridge.py) | MCP tool wiring with guards | 0 |
| [triadic_queues.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/triadic_queues.py) | Three disjoint queue fibers | 0 |
| [path_invariance.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/path_invariance.py) | Morphism commutativity checks | -1 |
| [mcp_api_equivalence.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/mcp_api_equivalence.py) | Equivalence verification | -1 |
| [narya_proofs/](file:///Users/alice/agent-o-rama/agent-o-rama/src/narya_proofs/) | Formal verification proofs | -1 |

## Workflows

### Workflow 1: Email-to-Task with Full Morphism Chain

```python
from workspace_bridge import create_workspace_bridge
from workspace_detector import WorkspaceDetector

# Create bridge
bridge = create_workspace_bridge("user@gmail.com")
detector = WorkspaceDetector()

# MINUS: Search for actionable emails
results = bridge.search_gmail_messages("is:unread label:action-required")
for msg in results:
    thread = bridge.get_gmail_thread_content(msg.thread_id)
    detector.update_service('gmail', trit=Trit.MINUS)
    
    # PLUS: Create task via thread_task morphism
    task = bridge.create_task(
        title=f"Follow up: {thread.subject}",
        notes=thread.snippet,
        task_list_id=default_list_id
    )
    detector.update_service('tasks', trit=Trit.PLUS)
    
    # ERGODIC: Label as processed
    bridge.modify_gmail_message_labels(
        msg.id,
        add_label_ids=["Label_Processed"],
        remove_label_ids=["INBOX"]
    )
    detector.update_service('gmail', trit=Trit.ERGODIC)

# GF(3) check: -1 + 1 + 0 = 0 ✓
```

### Workflow 2: Meeting Notes with Cross-Service Morphisms

```python
# MINUS: Get calendar events
events = bridge.get_events(time_min=today, time_max=tomorrow)
detector.update_service('calendar', trit=Trit.MINUS)

for event in events:
    # PLUS: Create meeting notes doc via event_doc morphism
    doc = bridge.create_doc(
        title=f"Notes: {event.summary}",
        content=generate_template(event)
    )
    detector.update_service('docs', trit=Trit.PLUS)
    
    # ERGODIC: Update event with doc link
    bridge.modify_event(
        event_id=event.id,
        description=f"{event.description}\n\nNotes: {doc.url}"
    )
    detector.update_service('calendar', trit=Trit.ERGODIC)

# GF(3) check: -1 + 1 + 0 = 0 ✓
```

### Workflow 3: File Review with Task Creation

```python
# MINUS: Search for files needing review
files = bridge.search_drive_files("modifiedTime > '2024-01-01' and mimeType = 'application/pdf'")
detector.update_service('drive', trit=Trit.MINUS)

for file in files:
    # MINUS: Get file content
    content = bridge.get_drive_file_content(file.id)
    detector.update_service('drive', trit=Trit.MINUS)
    
    # PLUS: Create review task via file_task morphism
    task = bridge.create_task(
        title=f"Review: {file.name}",
        notes=f"File: {file.webViewLink}"
    )
    detector.update_service('tasks', trit=Trit.PLUS)
    
    # PLUS: Share file with reviewer
    bridge.share_drive_file(file.id, share_with="reviewer@example.com")
    detector.update_service('drive', trit=Trit.ERGODIC)

# Auto-balance if needed
if detector.gf3_residue() != 0:
    bridge.list_tasks(task_list_id=default_list_id)  # MINUS to balance
```

### Workflow 4: Weekly Digest with Condensation Check

```python
# Create digest from all services
digest = WorkspaceDigest()

# MINUS: Gather data
digest.gmail_threads = bridge.search_gmail_messages("newer_than:7d")
digest.drive_files = bridge.search_drive_files("modifiedTime > '2024-01-01'")
digest.events = bridge.get_events(time_min=week_ago, time_max=now)
digest.tasks = bridge.list_tasks(task_list_id=default_list_id)

# PLUS: Create digest doc
doc = bridge.create_doc(
    title=f"Weekly Digest: {week_start} - {week_end}",
    content=render_digest(digest)
)

# ERGODIC: Update shared folder
bridge.update_drive_file(doc.id, add_parents="shared_digests_folder_id")

# Check ANIMA
anima = detector.detect_anima()
if anima["at_anima"]:
    say("Workspace at ANIMA. Condensed state achieved.")
    print(f"Fingerprint: {anima['condensed_fingerprint'][:16]}...")
```

## Commands

```bash
# Run workspace ACSet demo
python src/workspace_acset.py

# Test cross-skill morphisms
python src/path_invariance.py

# Run MCP↔API equivalence tests
python src/mcp_api_equivalence.py

# Run Narya proofs
python -m src.narya_proofs.runner

# Check workspace saturation
python src/workspace_detector.py
```

## Integration with Other Skills

| Skill | Trit | Integration |
|-------|------|-------------|
| [gmail-anima](file:///Users/alice/agent-o-rama/agent-o-rama/.agents/skills/gmail-anima/SKILL.md) | 0 | Gmail-specific ACSet with thread saturation |
| [google-workspace](file:///Users/alice/.claude/skills/google-workspace/SKILL.md) | 0 | MCP tool provider |
| [gay-mcp](file:///Users/alice/.agents/skills/gay-mcp/SKILL.md) | +1 | SplitMixTernary RNG for deterministic colors |
| [sheaf-cohomology](file:///Users/alice/.claude/skills/sheaf-cohomology/SKILL.md) | -1 | H¹ obstruction verification |
| [bisimulation-game](file:///Users/alice/.agents/skills/bisimulation-game/SKILL.md) | -1 | State equivalence proofs |
| [ordered-locale](file:///Users/alice/.agents/skills/ordered-locale-proper/SKILL.md) | 0 | Service ordering topology |
| [acsets-algebraic-databases](file:///Users/alice/.agents/skills/acsets/SKILL.md) | 0 | ACSet foundations |

### GF(3) Triadic Conservation

```
workspace-unified (0) ⊗ gmail-anima (0) ⊗ gay-mcp (+1) ⊗ sheaf-cohomology (-1) = 0 ✓
gmail_read (-1) ⊗ drive_create (+1) ⊗ calendar_modify (0) = 0 ✓
thread_file (0) ⊗ file_event (+1) ⊗ event_task (+1) ⊗ tasks_get (-1) ⊗ docs_get (-1) = 0 ✓
```

## MCP ↔ API Equivalence

| # | Operation | MCP Tool | REST API Equivalent |
|---|-----------|----------|---------------------|
| 1 | Gmail Search | search_gmail_messages | GET /gmail/v1/users/me/messages |
| 2 | Gmail Read | get_gmail_message_content | GET /gmail/v1/users/me/messages/{id} |
| 3 | Gmail Send | send_gmail_message | POST /gmail/v1/users/me/messages/send |
| 4 | Gmail Label | modify_gmail_message_labels | POST /gmail/v1/users/me/messages/modify |
| 5 | Drive List | list_drive_items | GET /drive/v3/files |
| 6 | Drive Get | get_drive_file_content | GET /drive/v3/files/{id}?alt=media |
| 7 | Drive Create | create_drive_file | POST /upload/drive/v3/files |
| 8 | Drive Share | share_drive_file | POST /drive/v3/files/{id}/permissions |
| 9 | Calendar Events | get_events | GET /calendar/v3/calendars/{id}/events |
| 10 | Calendar Create | create_event | POST /calendar/v3/calendars/{id}/events |
| 11 | Tasks List | list_tasks | GET /tasks/v1/lists/{id}/tasks |
| 12 | Tasks Create | create_task | POST /tasks/v1/lists/{id}/tasks |
| 13 | Docs Get | get_doc_content | GET /docs/v1/documents/{id} |
| 14 | Docs Create | create_doc | POST /docs/v1/documents |
| 15 | Sheets Read | read_sheet_values | GET /sheets/v4/spreadsheets/{id}/values |

### Equivalence Verification

```python
@dataclass
class MCPAPIEquivalence:
    operation: str
    mcp_result: WorkspaceState
    api_result: WorkspaceState
    
    def verify(self) -> bool:
        """Verify bitwise equivalence after normalization."""
        mcp_normalized = normalize(self.mcp_result)
        api_normalized = normalize(self.api_result)
        return mcp_normalized == api_normalized
    
    def diff(self) -> Optional[StateDiff]:
        """Return diff if not equivalent."""
        if self.verify():
            return None
        return compute_diff(self.mcp_result, self.api_result)

def verify_all_equivalences(bridge: WorkspaceBridge) -> Dict:
    """Run full equivalence suite."""
    results = {}
    for op in bridge.supported_operations:
        equiv = MCPAPIEquivalence(
            operation=op,
            mcp_result=bridge.execute_mcp(op, test_params[op]),
            api_result=bridge.execute_api(op, test_params[op])
        )
        results[op] = {
            'equivalent': equiv.verify(),
            'diff': equiv.diff()
        }
    return results
```

## Say Narration Integration

```python
from workspace_bridge import NaryaLogger

logger = NaryaLogger(voice="Ava (Premium)")

# Announces: "Workspace bridge: MINUS transition on gmail"
logger.log(before, after, Trit.MINUS, service="gmail", impact=False)

# Announces: "Workspace bridge: PLUS transition on drive, impact detected"
logger.log(before, after, Trit.PLUS, service="drive", impact=True)

# Cross-skill morphism announcement
logger.log_morphism("thread_task", thread, task, Trit.PLUS)
```

---

**Skill Name**: workspace-unified  
**Type**: Workspace Management / ACSet Framework  
**Trit**: 0 (ERGODIC - coordinator)  
**GF(3)**: Conserved via cross-skill morphism routing  
**ANIMA**: Workflow Completion = Condensed Equilibrium State
