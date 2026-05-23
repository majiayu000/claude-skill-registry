---
name: docs-acset
description: Google Docs/Sheets management via ACSet condensation. Transforms documents into GF(3)-typed Interactions, tracks comments/cells, detects saturation when all comments resolved. Use for document workflows, spreadsheet automation, or applying ANIMA principles to Workspace documents.
---

# Docs ACSet Skill

Transform Google Docs/Sheets into an ACSet-condensed system with GF(3) conservation.

**Trit**: 0 (ERGODIC - coordinator)  
**Principle**: Published Document = Condensed State  
**Implementation**: DocsACSet + CommentTracker + CellSaturation

## Overview

Docs ACSet applies category-theoretic structure to documents:

1. **Transform** - Documents/Sheets → GF(3)-typed Interactions
2. **Track** - Comments/Cells → Saturation state
3. **Detect** - All resolved → ANIMA condensed state
4. **Verify** - Narya proofs for consistency

## DocsACSet Schema

```
┌────────────────────────────────────────────────────────────────────┐
│                      DocsACSet Schema                              │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Document ────────┬────▶ Section                                   │
│  ├─ doc_id: String│      ├─ heading: String                        │
│  ├─ title: String │      ├─ level: Int                             │
│  └─ published: Bool      └─ content_hash: String                   │
│                   │                                                │
│  Comment ─────────┼────▶ Thread (doc)                              │
│  ├─ content: String      ├─ resolved: Bool                         │
│  ├─ author: String       └─ reply_count: Int                       │
│  └─ trit: Trit    │                                                │
│                   │                                                │
│  Spreadsheet ─────┼────▶ Sheet                                     │
│  ├─ ss_id: String │      ├─ name: String                           │
│  └─ locale: String       └─ row_count: Int                         │
│                   │                                                │
│  Cell ────────────┴────▶ Range                                     │
│  ├─ value: String        ├─ a1_notation: String                    │
│  ├─ formula: String      └─ dirty: Bool                            │
│  └─ trit: Trit                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Objects

| Object | Description | Trit Role |
|--------|-------------|-----------|
| `Document` | Google Doc with publish state | Aggregate |
| `Section` | Heading-delimited content block | Node |
| `Comment` | Review comment with resolution state | Interaction |
| `Spreadsheet` | Google Sheets workbook | Aggregate |
| `Sheet` | Individual tab within spreadsheet | Node |
| `Cell` | Single cell with value/formula | Data |

## GF(3) Verb Typing

Docs/Sheets actions assigned trits based on information flow:

```python
VERB_TRIT_MAP = {
    # MINUS (-1): Consumption/Reading
    "get_doc_content": -1,     "read_sheet_values": -1,
    "get_spreadsheet_info": -1, "inspect_doc_structure": -1,
    "read_document_comments": -1, "debug_table_structure": -1,
    
    # ERGODIC (0): Coordination/Metadata
    "modify_doc_text": 0,      "find_and_replace_doc": 0,
    "update_doc_headers_footers": 0, "resolve_document_comment": 0,
    "create_sheet": 0,          "reply_to_document_comment": 0,
    
    # PLUS (+1): Generation/Creation
    "create_doc": +1,          "create_spreadsheet": +1,
    "insert_doc_elements": +1, "insert_doc_image": +1,
    "create_table_with_data": +1, "modify_sheet_values": +1,
    "create_document_comment": +1, "export_doc_to_pdf": +1,
}
```

### MCP Tool → Trit Mapping

| Tool | Trit | Description |
|------|------|-------------|
| `get_doc_content` | -1 | Read document (MINUS) |
| `read_sheet_values` | -1 | Read cells (MINUS) |
| `read_document_comments` | -1 | Read comments (MINUS) |
| `modify_doc_text` | 0 | Edit text (ERGODIC) |
| `resolve_document_comment` | 0 | Resolve thread (ERGODIC) |
| `create_doc` | +1 | Create document (PLUS) |
| `create_spreadsheet` | +1 | Create workbook (PLUS) |
| `modify_sheet_values` | +1 | Write cells (PLUS) |

## Doc-Thread Morphism

Documents and Gmail threads form a natural morphism:

```
┌─────────────────────────────────────────────────────────────────┐
│                   Doc-Thread Morphism                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Document ◀─────────────▶ Thread                                │
│  ├─ doc_id                 ├─ thread_id                         │
│  ├─ published              ├─ saturated                         │
│  └─ all_comments_resolved  └─ needs_action                      │
│                                                                 │
│  Functorial mapping:                                            │
│  F(doc) = thread where doc shares via gmail                     │
│  F(comment) = message in review workflow                        │
│  F(resolve) = archive/reply                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Workflow Paths

```python
# Doc → Email (share for review)
share_path = doc_read >> email_compose  # -1 + 1 = 0 ✓

# Email feedback → Doc update
feedback_path = email_read >> doc_modify >> comment_resolve
# -1 + 0 + 0 = -1 (needs PLUS balance)
balanced = feedback_path >> doc_export  # -1 + 1 = 0 ✓
```

## Saturation Detection

Saturation occurs when all comments are resolved:

```python
def is_saturated(doc_id: str) -> bool:
    """Document is saturated when:
    1. All comments resolved (no open threads)
    2. GF(3) cycle closure: sum(trits) ≡ 0 (mod 3)
    3. Published state stable
    """
    comments = get_all_comments(doc_id)
    all_resolved = all(c.resolved for c in comments)
    cycle_sum = sum(c.trit for c in comments)
    
    return all_resolved and (cycle_sum % 3) == 0
```

### ANIMA Detection

```python
def detect_anima(doc_ids: List[str]) -> Dict:
    """System at ANIMA when:
    1. All documents saturated (comments resolved)
    2. All spreadsheets consistent (no dirty cells)
    3. GF(3) conserved globally
    """
    return {
        "at_anima": all_docs_saturated and all_sheets_clean,
        "condensed_fingerprint": sha256(all_content_hashes),
        "published_count": sum(1 for d in docs if d.published),
    }
```

**Published Document as ANIMA**: When all comments are resolved and document is published, it's in condensed equilibrium.

## Source Files

| File | Description | Trit |
|------|-------------|------|
| [docs_acset.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/docs_acset.py) | ACSet schema + comment tracking | 0 |
| [sheet_saturation.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/sheet_saturation.py) | Cell dirty state + formula deps | 0 |
| [doc_thread_morphism.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/doc_thread_morphism.py) | Functorial Doc↔Gmail mapping | 0 |

## Workflows

### Workflow 1: Document Review to Saturation

```python
from docs_acset import DocsACSet

acset = DocsACSet("user@gmail.com")

# MINUS: Read document and comments
doc = acset.get_doc_content(doc_id)  # trit=-1
comments = acset.read_document_comments(doc_id)  # trit=-1

# ERGODIC: Process each comment
for comment in comments:
    acset.reply_to_document_comment(doc_id, comment.id, "Addressed")
    acset.resolve_document_comment(doc_id, comment.id)  # trit=0

# PLUS: Export final version
acset.export_doc_to_pdf(doc_id)  # trit=+1
# GF(3): -1 + -1 + 0 + 1 = -1 (needs one more PLUS)
```

### Workflow 2: Spreadsheet Update Cycle

```python
# MINUS: Read current state
values = acset.read_sheet_values(ss_id, "A1:Z100")  # trit=-1

# PLUS: Write updates
acset.modify_sheet_values(ss_id, "A1:B10", new_data)  # trit=+1

# ERGODIC: Add new sheet for audit
acset.create_sheet(ss_id, "Audit Log")  # trit=0
# GF(3): -1 + 1 + 0 = 0 ✓
```

### Workflow 3: Cross-Document Sync

```python
# Read source doc
source = acset.get_doc_content(source_id)  # -1

# Create target from template  
target = acset.create_doc("Derived Document", source.content)  # +1

# Link via comment
acset.create_document_comment(target.id, f"Derived from {source_id}")  # +1
# Balance needed: -1 + 1 + 1 = 1 → add MINUS
acset.read_document_comments(target.id)  # -1 → total = 0 ✓
```

## Integration with Other Skills

| Skill | Trit | Integration |
|-------|------|-------------|
| [google-workspace](file:///Users/alice/.claude/skills/google-workspace/SKILL.md) | 0 | MCP tool provider |
| [gmail-anima](file:///Users/alice/agent-o-rama/agent-o-rama/.agents/skills/gmail-anima/SKILL.md) | 0 | Thread↔Doc morphism |
| [gay-mcp](file:///Users/alice/.agents/skills/gay-mcp/SKILL.md) | +1 | SplitMixTernary RNG |
| [sheaf-cohomology](file:///Users/alice/.claude/skills/sheaf-cohomology/SKILL.md) | -1 | Section consistency |
| [acsets-algebraic-databases](file:///Users/alice/.agents/skills/acsets/SKILL.md) | 0 | Schema foundation |

### GF(3) Triadic Conservation

```
docs-acset (0) ⊗ gmail-anima (0) ⊗ sheaf-cohomology (-1) + gay-mcp (+1) = 0 ✓
read (-1) ⊗ modify (0) ⊗ create (+1) = 0 ✓
comment (-1) ⊗ reply (0) ⊗ resolve (0) + export (+1) = 0 ✓
```

---

**Skill Name**: docs-acset  
**Type**: Document Management / ACSet Framework  
**Trit**: 0 (ERGODIC - coordinator)  
**GF(3)**: Conserved via verb typing  
**ANIMA**: Published Document = Condensed State
