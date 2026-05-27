---
name: captp
description: "CapTP: Capability Transfer Protocol"
version: 1.0.0
---

# CapTP: Capability Transfer Protocol

**Trit**: 0 (ERGODIC - transports capabilities without amplification)
**Color**: #46F27F (Coordinator stream)
**Source**: Spritely Goblins (codeberg.org/spritely/goblins)

---

## Overview

CapTP (Capability Transfer Protocol) enables distributed object programming with capability security. Objects can live anywhere on the network; CapTP abstracts location so programmers focus on object interaction, not protocol architecture.

**Core principle**: Capabilities are unforgeable references. You can only invoke what you've been given.

---

## Key Concepts

### Vats (Actor Containers)

```scheme
;; Guile Goblins
(define vat (spawn-vat))
(define greeter (vat-spawn vat ^greeter))
```

| Concept | Description | Trit Mapping |
|---------|-------------|--------------|
| **Vat** | Transactional actor container | 0 (ergodic boundary) |
| **Actor** | Encapsulated object with behavior | +1 (generative) |
| **Capability** | Unforgeable reference | -1 (constraining) |

### Promise Pipelining

```scheme
;; Don't wait for result - pipeline through promises
(<- (<- alice 'get-friend) 'greet "Hello")
```

Reduces round-trips: send message to promise, network resolves.

### Sturdy vs Live References

| Reference | Persistence | Use Case |
|-----------|-------------|----------|
| **Live** | Session only | Active communication |
| **Sturdy** | Survives restart | Reconnection, storage |

---

## CapTP Message Types

```
op:deliver-only  → Fire-and-forget message
op:deliver       → Message expecting response
op:pick          → Select from multiple promises
op:abort         → Cancel pending operation
op:listen        → Subscribe to updates
op:gc            → Garbage collection hint
```

---

## GF(3) Triads

```
# Core CapTP Bundle
keychain-secure (-1) ⊗ captp (0) ⊗ gay-mcp (+1) = 0 ✓  [Secure Transport]
shadow-goblin (-1) ⊗ captp (0) ⊗ agent-o-rama (+1) = 0 ✓  [Distributed Actors]
polyglot-spi (-1) ⊗ captp (0) ⊗ pulse-mcp-stream (+1) = 0 ✓  [Cross-Lang Objects]
temporal-coalgebra (-1) ⊗ captp (0) ⊗ koopman-generator (+1) = 0 ✓  [State Observation]

# Goblins Integration
three-match (-1) ⊗ captp (0) ⊗ gay-mcp (+1) = 0 ✓  [Colored Capabilities]
sheaf-cohomology (-1) ⊗ captp (0) ⊗ operad-compose (+1) = 0 ✓  [Compositional]
```

---

## Implementation Bridge

### Mapping to Our Goblins

| Spritely | Our System | Function |
|----------|------------|----------|
| `spawn-vat` | `SplitMixTernary.new(seed)` | Create isolated generator |
| `<-` (send) | `next_color!` | Advance state, get result |
| `$` (call) | `color_at(idx)` | Synchronous access |
| Sturdy ref | `(seed, index)` tuple | Reconstructable reference |
| Promise | Derivation chain | Future state determined by seed |

### Ruby Integration

```ruby
require 'captp'

# Create vat (generator with transactional boundary)
vat = CapTP::Vat.new(seed: 0x42D)

# Spawn actor (color stream)
actor = vat.spawn(:color_stream)

# Send message (advance stream)
promise = actor.send(:next_color)

# Pipeline (derive without waiting)
result = actor.send(:palette, 5).then { |colors| colors.map(&:hex) }
```

### Scheme Integration (Hoot target)

```scheme
(use-modules (goblins) (goblins actor-lib cell))

;; Define actor constructor
(define (^color-stream bcom seed)
  (define idx (spawn ^cell 0))
  (lambda (method . args)
    (case method
      ((next-color)
       (let ((i ($ idx)))
         ($ idx (+ i 1))
         (color-at seed i)))
      ((palette)
       (map (lambda (i) (color-at seed i))
            (iota (car args)))))))

;; Spawn in vat
(define stream (spawn ^color-stream 1069))
(<- stream 'next-color)  ;; => promise of color
```

---

## Netlayers

| Layer | Transport | Use Case |
|-------|-----------|----------|
| **Tor Onion** | .onion addresses | Anonymous, censorship-resistant |
| **TCP Direct** | IP:port | Local network, low latency |
| **WebSocket** | wss:// | Browser-based (Hoot target) |
| **NATS** | nats:// | High-throughput pub/sub |
| **Tailscale** | 100.x.y.z | Mesh VPN, zero-config |

---

## Security Model

### Principle of Least Authority (POLA)

```
You can only:
1. Use capabilities you were given
2. Create new objects (that you then have caps to)
3. Introduce objects you have caps to, to each other
```

### Attenuation

```ruby
# Full capability
full_stream = vat.spawn(:color_stream, seed: 0x42D)

# Attenuated: read-only, no advance
read_only = full_stream.attenuate(:color_at)

# Attenuated: limited palette size
limited = full_stream.attenuate(:palette, max: 10)
```

---

## Commands

```bash
just captp-vat seed=1069        # Create vat with seed
just captp-spawn actor_type     # Spawn actor in vat
just captp-send actor method    # Send message
just captp-pipeline expr        # Pipeline expression
just captp-sturdy actor         # Get sturdy reference
```

---

## Related Skills

| Skill | Relation |
|-------|----------|
| **localsend-mcp** | P2P file transfer via CapTP-like protocol |
| **tailscale-file-transfer** | Mesh VPN netlayer |
| **keychain-secure** | Credential capabilities |
| **shadow-goblin** | Validates capability boundaries |
| **agent-o-rama** | Generates actor proposals |

---

## References

- [Spritely Goblins](https://spritely.institute/goblins/)
- [Racket Goblins Docs](https://docs.racket-lang.org/goblins/)
- [Heart of Spritely Whitepaper](https://files.spritely.institute/papers/spritely-core.html)
- [Hoot: Scheme on WebAssembly](https://spritely.institute/hoot/)
- [E Language (historical)](http://erights.org/)

---

**Skill Name**: captp
**Type**: Distributed Object Protocol
**Trit**: 0 (ERGODIC)
**GF(3)**: Transports capabilities without amplification
**Invariant**: Capabilities unforgeable, only invoke what you're given



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
captp (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch7: Propagators
- Ch3: Variations on an Arithmetic Theme
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch6: Layering
- Ch2: Domain-Specific Languages

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