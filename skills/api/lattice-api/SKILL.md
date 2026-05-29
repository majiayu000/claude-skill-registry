---
name: lattice-api
description: API quick-reference for key lattice subsystems (FP, Game Theory, SAT, Optics, Statistics, CLP). Use when you need function signatures, module contents, or usage examples for a specific subsystem. Invoke when working with game theory, constraint solving, optics, parsers, or other advanced lattice features.
allowed-tools: Bash(./fold:*), Read, Grep, Glob
---

# Lattice API Quick Reference

Detailed API documentation for the major lattice subsystems. Use `/lattice-search` for discovery; use this skill for API details once you know what subsystem you need.

## FP Toolkit (`lattice/fp/`)

Monads, parsers, streams, zippers, game theory, symbolic math, control systems (state-space, Kalman filters, PID, stability analysis), term rewriting.

```scheme
(li 'fp)   ; Full description
(le 'fp)   ; All exports
```

### Regex/FSM (`lattice/fp/parsing/`)

Regex→NFA compilation via Thompson's construction.

**Features:**
- Quantifier ranges `{n,m}`
- Anchors `^`/`$`
- Lookahead `(?=...)`/`(?!...)`

**Note:** Anchors and lookahead require position-aware NFA execution; `nfa->dfa` and `fsm-minimize` skip conversion when assertions present. Use `regex-accepts?` or `fsm-accepts?` which auto-detect and use appropriate runner.

```scheme
(regex-accepts? "^foo" "foobar")  ; #t
(regex-accepts? "foo$" "foobar")  ; #f
```

## Game Theory (`lattice/fp/game/`)

Rich set of ready-to-use algorithms for cooperative games, voting, matching, and fair division.

| Module | Contents |
|--------|----------|
| `coop-games.ss` | `make-coop-game`, `shapley-value`, `core`, `nucleolus` |
| `voting-games.ss` | `banzhaf-index`, `shapley-shubik-index`, `make-weighted-voting-game` |
| `voting.ss` | `schulze-ranking`, `borda-scores-all`, `condorcet-winner` |
| `multi-winner.ss` | `pav-winners` (proportional approval), `stv-winners` |
| `matching.ss` | Gale-Shapley stable matching, hospital-residents |
| `fair-division.ss` | Envy-free allocation, proportional division |

These are pure functions — import them into boundary code for applications like QA triage, resource allocation, or voting systems.

### Example: Shapley Value

```scheme
(load "lattice/fp/game/coop-games.ss")

;; Define a cooperative game: 3 players, characteristic function
(define game (make-coop-game 3
  (lambda (coalition)
    (cond
      [(equal? coalition '(1 2 3)) 100]  ; Grand coalition
      [(equal? coalition '(1 2)) 70]
      [(equal? coalition '(1 3)) 50]
      [(equal? coalition '(2 3)) 60]
      [else 0]))))

(shapley-value game)  ; => fair allocation to each player
```

## Statistics (`lattice/statistics/`)

| Category | Functions |
|----------|-----------|
| Regression | Linear, GLM (IRLS), ridge, lasso, elastic net |
| Time Series | AR, MA, exponential smoothing |
| Hypothesis Testing | t-test, F-test, ANOVA, chi-squared |

```scheme
(li 'statistics)  ; Full description
(le 'statistics)  ; All exports
```

## CLP(FD) (`lattice/fp/clp/`)

cKanren-style constraint logic programming with finite domains.

**Features:**
- Finite domain constraints
- Arithmetic constraints (`fd-<`, `fd-+`, etc.)
- Global constraints (`all-different`)
- Intelligent search strategies

**Classic problems:** N-Queens, Sudoku, cryptarithmetic

```scheme
(load "lattice/fp/clp/clpfd.ss")

;; N-Queens
(run* (q)
  (fresh (q1 q2 q3 q4)
    (== q (list q1 q2 q3 q4))
    (fd-dom q1 '(1 2 3 4))
    (fd-dom q2 '(1 2 3 4))
    (fd-dom q3 '(1 2 3 4))
    (fd-dom q4 '(1 2 3 4))
    (all-different q)
    (queens-safe q)))
```

## SAT/MaxSAT (`lattice/fp/sat/`)

CDCL SAT solver with clause learning, Two-Watched Literals, VSIDS branching. MaxSAT extension for optimization.

| Function | Purpose |
|----------|---------|
| `sat-solve` | Check satisfiability, returns `'sat`, `'unsat`, or `'unknown` |
| `sat-model` | Get satisfying assignment |
| `graph-coloring` | Encode k-coloring as SAT |
| `n-queens-sat` | Encode N-Queens as SAT |
| `make-maxsat` | Create MaxSAT with hard/soft clauses |
| `maxsat-solve` | Find minimum-cost assignment |
| `min-vertex-cover` | Encode as MaxSAT |
| `max-independent-set` | Encode as MaxSAT |
| `min-correction-set` | Diagnosis: find clauses to remove |

### Example: Graph Coloring

```scheme
(load "lattice/fp/sat/sat.ss")
(load "lattice/fp/sat/applications.ss")

;; 3-color a graph
(define edges '((1 . 2) (2 . 3) (3 . 1)))
(define coloring-cnf (graph-coloring 3 3 edges))
(sat-solve coloring-cnf)  ; => 'sat or 'unsat
(sat-model coloring-cnf)  ; => variable assignments
```

## Optics (`lattice/fp/optics/`)

Complete optics tower for composable data access.

| Module | Contents |
|--------|----------|
| `optics.ss` | Core tower: Iso, Lens, Prism, Affine, Traversal, Fold, Getter, Setter, Grate |
| `block-optics.ss` | CAS block optics: `block-tag-lens`, `block-refs-each`, `follow-ref`, type prisms |
| `profunctor-optics.ss` | Profunctor encoding: Strong/Choice/Closed/Wander, `p-lens`, `p-prism`, `p-traversal`, `p-fold` |
| `bidirectional.ss` | Reversible migrations: `make-migration`, `migrate`, `rollback`, `migration-compose` |
| `schema.ss` | Field DSL: `field-rename-iso`, `field-add-iso`, `field-transform-iso` |
| `block-migration.ss` | CAS migrations: `make-block-migration`, `block-migrate-payload`, bottom-up tree traversal |

### Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `^.` | view | `(^. body body-pos-lens)` |
| `^?` | preview (Maybe) | `(^? either left-prism)` |
| `^..` | to-list | `(^.. world (>>> world-all-bodies body-vel-lens))` |
| `.~` | set | `(.~ body-pos-lens new-pos body)` |
| `%~` | modify | `(%~ body-pos-lens add1 body)` |
| `&` | pipe (left-to-right) | `(& body (%~ lens f))` |
| `>>>` | compose (left-to-right) | `(>>> outer-lens inner-lens)` |

### Example: Nested Access

```scheme
(load "lattice/fp/optics/optics.ss")

;; View nested position
(^. body body-pos-lens)

;; Modify x-coordinate of position
(& body (%~ (>>> body-pos-lens vec2-x-lens) add1))

;; Get all velocities from world
(^.. world (>>> world-all-bodies body-vel-lens))
```

## Traced Optics (`lattice/autodiff/traced-optics.ss`)

Compute gradients through optic-focused paths — combines autodiff with optics.

```scheme
(load "lattice/autodiff/traced-optics.ss")

;; Gradient of loss w.r.t. nested parameter via optic composition
(optic-gradient loss-fn (>>> outer-lens inner-lens) structure)

;; Gradient descent step at optic focus
(optimize-at lens-fst '(5.0 . ignored) (lambda (p) (traced-sq (car p))) 0.1)
;; => (4.0 . ignored)  ; 5 - 0.1 * 2 * 5 = 4

;; Gradients for all traversal targets
(optic-gradient-list loss-fn traversal-each '(1 2 3))
```

## Skill Manifests

Each lattice skill has a `manifest.sexp` declaring metadata:

```scheme
(skill <name>
  (version "x.y.z")
  (tier 0-2)                       ; 0=foundational, 1=intermediate, 2+=advanced
  (path "lattice/<name>")
  (purity total|partial)           ; total=pure, partial=may have effects
  (stability stable|experimental)
  (fuel-bound "O(...)")            ; Complexity bound
  (deps (<skill> ...))             ; Skill-level dependencies
  (description "...")
  (keywords (<keyword> ...))       ; For search
  (aliases (<alias> ...))          ; Alternative names
  (exports (<module> <symbol> ...) ...)
  (modules (<name> "<file>" "<desc>") ...))
```
