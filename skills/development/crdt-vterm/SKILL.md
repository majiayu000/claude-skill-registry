---
name: crdt-vterm
description: Collaborative terminal session sharing using CRDT-style s-expressions
version: 1.0.0
---


# CRDT-VTerm - Collaborative Terminal Sharing

Collaborative terminal session sharing using CRDT-style s-expressions with GF(3) trifurcated conflict resolution.

## Components

### Emacs Bridge
- **File**: `crdt-vterm-bridge.el`
- **Purpose**: Connect vterm.el to crdt.el via shadow buffers

### Babashka Recorder
- **File**: `vterm_crdt_recorder.bb`
- **Purpose**: Record/replay terminal sessions as CRDT sexps

### P2P Sharing
- **File**: `vterm_localsend_share.bb`  
- **Purpose**: Live terminal sharing via localsend multicast

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    CRDT-VTerm System                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────┐     remote-insert     ┌───────────────┐             │
│  │ vterm   │ ───────────────────▶  │ shadow buffer │             │
│  │  PTY    │      (GF3 trit)       │  (crdt.el)    │             │
│  └────┬────┘                       └───────┬───────┘             │
│       │                                    │                     │
│       │ script(1)                          │ sexp file           │
│       ▼                                    ▼                     │
│  ┌─────────┐                       ┌───────────────┐             │
│  │ raw log │                       │ .sexp log     │             │
│  └────┬────┘                       └───────┬───────┘             │
│       │                                    │                     │
│       │ vterm_crdt_recorder.bb             │ localsend UDP       │
│       ▼                                    ▼                     │
│  ┌─────────────────────────────────────────────────┐             │
│  │              P2P Peer Network                   │             │
│  │  ┌───────┐   ┌───────┐   ┌───────┐              │             │
│  │  │ MINUS │   │ERGODIC│   │ PLUS  │  ← GF(3)     │             │
│  │  └───────┘   └───────┘   └───────┘    routing   │             │
│  └─────────────────────────────────────────────────┘             │
└──────────────────────────────────────────────────────────────────┘
```

## CRDT Sexp Format

```clojure
;; Session header
(crdt-terminal-session
  (version "0.1.0")
  (session-id "T-abc123")
  (site-id 42)
  (gf3-assignment :ERGODIC))

;; Terminal output
(remote-insert "0a1b2c3d" 42 "$ ls -la\n"
  (props :type :terminal-output
         :trit :MINUS
         :timestamp 1234567890))

;; User input
(remote-input "0a1b2c3e" 42 "ls -la"
  (props :trit :PLUS
         :timestamp 1234567891))

;; Conflict resolution
(conflict-resolution
  :type :concurrent-input
  :strategy :gf3-ordering)
```

## Usage

### Record Session
```bash
bb vterm_crdt_recorder.bb record session.sexp
```

### Replay Session
```bash
bb vterm_crdt_recorder.bb replay session.sexp 2.0
```

### Live P2P Share
```bash
bb vterm_localsend_share.bb share output.sexp 192.168.1.5
```

### Emacs Replay
```elisp
M-x crdt-vterm-replay RET session.sexp RET 1.0 RET
```

## GF(3) Trifurcated Input

Multi-user input is routed through three queues:

| Queue | Trit | Processing Order |
|-------|------|------------------|
| MINUS | -1 | First |
| ERGODIC | 0 | Second |
| PLUS | +1 | Third |

This prevents conflicts in "no-longer-optimistic waiting" scenarios by deterministically ordering concurrent inputs.

```elisp
;; Cycle through queues
(crdt-vterm-trifurcate-cycle)
```

## Integration

### With gay-mcp
Each terminal session gets a deterministic color based on session ID.

### With localsend-mcp
P2P discovery and file transfer for session sharing.

### With duckdb-ies
Terminal sessions can be indexed in DuckDB for time-travel queries.

## Related Skills
- `gay-mcp` - Deterministic colors
- `spi-parallel-verify` - GF(3) conservation
- `triad-interleave` - Three-stream scheduling
- `bisimulation-game` - Session equivalence



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `distributed-systems`: 3 citations in bib.duckdb

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