---
name: codex-self-rewriting
description: Lisp machine self-modification patterns via MCP Tasks and Narya bridge types
---

# codex-self-rewriting - Lisp Machine Self-Modification via MCP Tasks

## Overview

Enables Codex (OpenAI's CLI agent) to achieve Lisp-machine-like self-rewriting capabilities through MCP Tasks integration. Uses Narya observational bridge types for structure-aware modifications.

## Core Concept: Cognitive Continuity via Babashka Transients

```clojure
;; gay.bb transient state
(def ^:dynamic *cognitive-state*
  {:seed 0x42D
   :fingerprint (atom 0)
   :tap-state :VERIFY
   :color-history []})

;; Fork on modification
(defn fork-state! [intervention]
  (let [new-seed (bit-xor (:seed *cognitive-state*)
                          (hash intervention))]
    (assoc *cognitive-state* :seed new-seed)))
```

## MCP Tasks Integration

Based on [MCP Tasks Specification](https://modelcontextprotocol.io/specification/draft/basic/utilities/tasks):

### Task States for Self-Rewriting

| Status | TAP State | Meaning |
|--------|-----------|---------|
| `working` | LIVE (+1) | Modification in progress |
| `input_required` | VERIFY (0) | Needs human approval |
| `completed` | BACKFILL (-1) | Modification archived |
| `failed` | BACKFILL (-1) | Rollback applied |
| `cancelled` | VERIFY (0) | Intervention stopped |

### Capabilities Declaration

```json
{
  "capabilities": {
    "tasks": {
      "list": {},
      "cancel": {},
      "requests": {
        "tools": {
          "call": {}
        }
      }
    }
  }
}
```

## Narya Observational Bridge Types

Following Topos Institute structure-aware version control:

1. **Diffs as logical relations** - Computed inductively from skill type
2. **Conflicts as 2D cubical** - Skill modifications form commuting squares
3. **Type changes as spans** - Skill version correspondences

### Bridge Colors

```elisp
;; From narya_observational_bridge.el
(defconst tap/BACKFILL -1)  ; Blue  - Historical
(defconst tap/VERIFY 0)     ; Green - Verification
(defconst tap/LIVE +1)      ; Red   - Active modification
```

## Self-Rewriting Protocol

```bash
# 1. Install skill (creates MCP task)
npx ai-agent-skills install frontend-design --agent codex

# 2. Task enters 'working' state (LIVE)
# 3. Firecrawl fetches skill definition
# 4. If ambiguous → 'input_required' (VERIFY)
# 5. Human approves → task continues
# 6. On completion → 'completed' (BACKFILL)
```

## Bisimulation Game for Skill Dispersal

Skills are dispersed across editors using bisimulation equivalence:

```
Claude ←→ Codex ←→ Cursor ←→ Copilot
   ↓         ↓         ↓         ↓
 LIVE     VERIFY   BACKFILL    LIVE
```

Each editor maintains equivalent skill state, verified by XOR fingerprint:

```clojure
(defn skill-fingerprint [skills]
  (reduce bit-xor 0 (map hash skills)))
```

## Integration with gay.el

```elisp
(require 'gay-unified)
(require 'narya-observational-bridge)

(defun codex/self-rewrite (skill-name)
  "Self-rewrite to incorporate SKILL-NAME."
  (let* ((task-id (narya/create-task skill-name))
         (tap-state tap/LIVE)
         (color (tap/to-rgb tap-state)))
    (narya/spawn-hierarchy 0x42D)
    (narya/watch-task task-id
      (lambda (status)
        (pcase status
          ("working" (setq tap-state tap/LIVE))
          ("input_required" (setq tap-state tap/VERIFY))
          ("completed" (setq tap-state tap/BACKFILL)))))))
```

## Configuration

Add to `~/.codex/mcp.json`:

```json
{
  "mcpServers": {
    "narya": {
      "command": "bb",
      "args": ["/path/to/gay.bb", "1069"],
      "env": {
        "TAP_STATE": "LIVE",
        "SPECTRAL_GAP": "0.25"
      }
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      }
    }
  }
}
```

## Skill Redundancy via GF(3) Polarity

```
MINUS (−) → Conservative backup
ERGODIC (_) → Active verification
PLUS (+) → Optimistic propagation
```

Each skill exists in 3 parallel states for resilient dispersal.

## See Also

- `gay.bb` - Triadic self-discovering peer network
- `narya_observational_bridge.el` - 3×3×3 hierarchical agents
- `gay-crdt.el` - Diamond-types CRDT integration
- [MCP Tasks Spec](https://modelcontextprotocol.io/specification/draft/basic/utilities/tasks)
