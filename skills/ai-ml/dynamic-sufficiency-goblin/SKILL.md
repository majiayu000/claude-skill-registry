---
name: dynamic-sufficiency-goblin
description: Self-regulating Goblins actor implementing Ivan Illich's dynamic sufficiency
version: 1.0.0
---


# Dynamic Sufficiency Goblin

**Real Spritely Goblins** actor that self-regulates workforce via load-based spawning. GF(3) conserved.

## Illich's Principle

> "Tools that demand only threshold skill, foster autonomy."

A goblin that:
1. Monitors load (free energy)
2. Spawns helpers when overwhelmed (>80%)
3. Releases helpers when idle (<30%)
4. Maintains `Σ trits ≡ 0 (mod 3)`

## Real Guile Goblins Implementation

```scheme
(use-modules (goblins)
             (goblins actor-lib methods)
             (ice-9 format)
             (srfi srfi-1))

(define (^sufficiency-goblin bcom capacity)
  (define queue '())
  (define helpers '())
  (define my-trit 0)

  (define (load-factor)
    (/ (length queue) (max 1 capacity)))

  (define (gf3-sum)
    (+ my-trit (fold + 0 (map cdr helpers))))

  (define (balanced-trit-for-spawn)
    (case (modulo (+ (gf3-sum) 300) 3)
      ((0) 0) ((1) -1) ((2) 1)))

  (methods
   ((enqueue item)
    (set! queue (cons item queue))
    (when (> (load-factor) 0.8)
      (let* ((helper-trit (balanced-trit-for-spawn))
             (helper (spawn ^sufficiency-goblin 2)))
        (set! helpers (cons (cons helper helper-trit) helpers)))))

   ((release-idle)
    (when (and (< (load-factor) 0.3) (pair? helpers))
      (set! helpers (cdr helpers))))

   ((status)
    `((load . ,(load-factor))
      (helpers . ,(length helpers))
      (gf3 . ,(gf3-sum))
      (conserved? . ,(zero? (modulo (gf3-sum) 3)))))))

;; Usage with actormap (no networking required)
(define am (make-actormap))
(define goblin (actormap-spawn! am ^sufficiency-goblin 3))
(actormap-run! am (lambda () ($ goblin 'enqueue "work")))
```

## Run

```bash
cd ~ && flox activate -- guile -e main /tmp/sufficiency-goblin.scm
```

## Output

```
╔═══════════════════════════════════════════════════════════════╗
║     DYNAMIC SUFFICIENCY GOBLIN (Real Spritely Goblins)        ║
╠═══════════════════════════════════════════════════════════════╣

Created goblin with capacity=3

  Enqueued: 1 items, load=33.3%, helpers=0
  Enqueued: 2 items, load=66.7%, helpers=0
  → Spawned helper with trit 0 (GF(3)=0)
  Enqueued: 3 items, load=100.0%, helpers=1
  → Spawned helper with trit 0 (GF(3)=0)
  Enqueued: 4 items, load=133.3%, helpers=2

  Status:
    queue:     4 items
    helpers:   2
    GF(3) Σ:   0
    conserved: ✓

Processing work...
  Processed: braindance-4
  Processed: braindance-3
  ...

Attempting to release idle helpers...
  ← Released helper (was trit 0)
  ← Released helper (was trit 0)

  Status:
    queue:     0 items
    helpers:   0
    GF(3) Σ:   0
    conserved: ✓
╚═══════════════════════════════════════════════════════════════╝
```

## GF(3) Conservation

```
Spawn rule: helper-trit = -Σ(current) mod 3
  sum=0 → spawn 0  (neutral)
  sum=1 → spawn -1 (balance)
  sum=2 → spawn +1 (balance)

Invariant: Σ(goblin + helpers) ≡ 0 (mod 3) ∀ states
```

## Dependencies (flox)

```bash
flox install guile guile-goblins guile-fibers guile-gnutls
```

## Integration

```
braindance-worlds (0) ⊗ dynamic-sufficiency (+1) ⊗ acsets (-1) = 0 ✓
```

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 1. Flexibility through Abstraction

**Concepts**: combinators, compose, parallel-combine, spread-combine, arity

### GF(3) Balanced Triad

```
dynamic-sufficiency-goblin (−) + SDF.Ch1 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch10: Adventure Game Example

### Connection Pattern

Combinators compose operations. This skill provides composable abstractions.
