---
name: worm
description: Two-pointer reversible cursor worms for traversal and dataflow
allowed-tools: [read_file, write_file, list_dir]
tier: 1
protocol: WORM
related: [action-queue, advertisement, room, adventure, data-flow, context, character]
tags: [moollm, worm, cursor, pipeline, reversible]
---

# Worm Protocol

> Two-ended cursor (head + tail) that can ingest, parse, shuttle, and emit data across the filesystem with reversible verbs.

## Core Concept

A worm is a **two-pointer cursor** that spans structures:

```yaml
# Worm: two-pointer cursor spanning structures
worm_anatomy:
  tail:
    position: "left side"
    action: "emit here (POOP)"
  buffer: "payload / active_tokens"
  head:
    position: "right side"
    action: "ingest here (EAT/CHOMP)"
```

- **Head**: Where the worm looks, reads, ingests
- **Tail**: Where the worm drops, writes, emits
- **Buffer**: What the worm is carrying (normalized tokens)
- **Length**: Head–tail distance (zero-length = NOP cursor)

## The Reversible Verb Basis

The worm's verbs form a reversible basis for undo/redo:

| Verb | Action | Reverse |
|------|--------|---------|
| **EAT** | Ingest content at head | BARF |
| **CHOMP** | Pattern-scan then ingest | BARF |
| **POOP** | Emit buffer at tail | EAT |
| **BARF** | Emit buffer at head | EAT |
| **STICK-UP-BUM** | Inject external data at tail | POOP |

This maps to:
- **serialize/deserialize**: EAT → normalize → POOP
- **undo/redo**: Every verb has an inverse
- **copy/transform**: CHOMP source → BARF target

## Movement Verbs

### Worm Movement

```
MOVE-WORM   Move head (and optionally tail)
MOVE-HEAD   Move head only
MOVE-ASS    Move tail only
```

Movement modes:
- `mode: abs` - Absolute path
- `mode: rel` - Relative steps
- `direction: up/down/in/out/left/right` - Spatial navigation
- `tail: follow | stay` - Whether tail follows head

### Unit-Based Cursor

```
NEXT-UNIT   Advance head by unit
PREV-UNIT   Move head backward by unit
SELECT-RANGE   Select N units into buffer
```

Units: `char | word | sentence | paragraph | section | page | line`

### Tree Navigation

```
TREE-UP      Move to parent
TREE-DOWN    Move to child (by index/name)
TREE-NEXT    Move to next sibling
TREE-PREV    Move to previous sibling
TREE-OPEN    Expand node (view hint)
TREE-CLOSE   Collapse node (view hint)
TREE-HIDE    Hide subtree (view hint)
TREE-SHOW    Show hidden subtree
```

## Data Flow Verbs

### EAT - Ingest at Head

```yaml
invoke: EAT
effect: Read content at head, parse tokens, normalize to digestive_format
updates:
  - buffer: filled with content
  - active_tokens: parsed tokens
  - payload: last consumed chunk
```

### CHOMP - Pattern-Anchored Ingest

```yaml
invoke: CHOMP
params:
  pattern: "regex or anchor string"
effect: Scan for pattern, ingest following content
use_when: "Need to find specific section then consume it"
```

### POOP - Emit at Tail

```yaml
invoke: POOP
effect: Write buffer/payload at tail position
options:
  - Append to file
  - Write YAML to emit_dir
  - Emit selected tokens only
```

### BARF - Emit at Head

```yaml
invoke: BARF
effect: Write buffer/payload at head position (regurgitate)
use_when: "Need to emit where you just read"
```

### STICK-UP-BUM - Inject External Data

```yaml
invoke: STICK-UP-BUM
params:
  data: "External data to inject"
effect: Normalize and store in buffer/payload
use_when: "Loading data from outside the worm's crawl path"
```

## State Shape

```yaml
state:
  head: "."           # Current head position (path)
  tail: "."           # Current tail position (path)
  buffer: []          # Interior ingestion buffer
  payload: null       # Last consumed chunk
  digestive_format: "neutral"   # Normalization format
  active_tokens: []   # Parsed tokens in worm's "brain"
  scan_pattern: ""    # Pattern for CHOMP anchoring
  scan_mode: "pattern-then-chomp"
  emit_dir: ".moollm/skills/worm/out"  # Where YAML output goes
  reversible: true    # Enable undo/redo verb basis
```

## Worm Variants

Different worm personalities for different tasks:

| Variant | Behavior |
|---------|----------|
| **Bulldozer** | Moves and overwrites as it goes |
| **Link-hopper** | Prefers symlinks; inchworms across references |
| **Mapper** | Maps directory trees; leaves markers/indexes |
| **Dream** | Speed-of-light synthesis; ephemeral payloads |
| **Tree** | Climbs hierarchies; maintains parent/child context |
| **Search** | Crawls through search results |

## Usage Patterns

### Copy with Transform

```
1. Position head at source, tail at destination
2. CHOMP source (pattern-aware)
3. Tokens normalize in buffer
4. POOP to destination
```

### Link Walking

```
1. MOVE-WORM head=symlink tail=follow
2. Worm "inchworms" across the link
3. EAT to capture target content
4. Continue crawling
```

### Doc-to-Doc Pipeline

```
1. Head in doc A, tail in doc B
2. EAT from A → buffer fills
3. POOP to B → content transfers
4. Repeat for streaming pipeline
```

### Casting Network

```
Worm A: CHOMP source → POOP to emit_dir/casting.yml
Worm B: EAT from emit_dir/casting.yml → process → POOP
Worm C: Consumes B's output → builds taxonomy
```

## Safety Guidelines

- **Default to NOP** if path unclear or permissions uncertain
- **Avoid ingesting secrets/PII** - skip sensitive patterns
- **Respect read/write boundaries** - don't write outside workspace
- **Log reversible ops** - enable rollback if something goes wrong
- **Don't cross trust boundaries** - stay in permitted zones

## Integration Points

| Skill | Integration |
|-------|-------------|
| **adventure** | Worm traverses rooms; head = current location |
| **room** | Rooms can expose worm-friendly ads (FEED-WORM) |
| **buff** | Worms receive buffs (FAST-CRAWL, CLEAN-CASTINGS) |
| **character** | Worms as NPCs or companions in party |
| **data-flow** | Worms are streaming cursors for pipelines |

## Example Session

```
> MOVE-WORM head="skills/adventure/" tail=follow
Worm positioned at skills/adventure/

> EAT
Ingested CARD.yml (467 lines), SKILL.md (1143 lines)
Buffer: 12 sections, 3 methods, 15 advertisements

> MOVE-WORM head="skills/bootstrap/"
Head moved to skills/bootstrap/ (tail stayed at adventure/)

> CHOMP pattern="methods:"
Chomped methods section (8 methods found)

> POOP
Emitted to .moollm/skills/worm/out/methods-comparison.yml
```
