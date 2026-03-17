# Skill Bonds Registry

> Discovered via 3× triadic random walk across **467 skills**
> Seeds: 0xDEAD (MINUS), 0xBEEF (ERGODIC), 0xCAFE (PLUS)

## Bond Categories (Full Skill Graph)

| Rank | Bond | Count | Coverage |
|------|------|-------|----------|
| 1 | **GF(3)** | 456 | 97.6% |
| 2 | **DuckDB** | 361 | 77.3% |
| 3 | **Category** | 222 | 47.5% |
| 4 | **Gay.jl** | 147 | 31.5% |
| 5 | **Babashka** | 137 | 29.3% |
| 6 | **ACSet** | 133 | 28.5% |
| 7 | **MCP** | 89 | 19.1% |
| 8 | **Sheaf** | 84 | 18.0% |
| 9 | **Random Walk** | 75 | 16.1% |
| 10 | **SICP** | 4 | 0.9% |

## Top 5 Compatible Skill Bonds

| Bond | Skills | Strength | Integration |
|------|--------|----------|-------------|
| **lisp-unity** | babashka ↔ sicp | 0.95 | Shared Lisp/functional paradigm |
| **execution-bridge** | babashka ↔ duckdb | 0.93 | bb scripts drive DuckDB queries |
| **determinism** | duckdb ↔ random-walk-fusion | 0.92 | SplitMix64 PRNG seeding |
| **schema-first** | acsets ↔ duckdb | 0.90 | Both use declarative schemas |
| **derivational** | sicp ↔ random-walk-fusion | 0.88 | Substitution = derivation chains |

## Known Conflicts (42 total)

| Category | Count | Severity | Remediation |
|----------|-------|----------|-------------|
| **duckdb-path-mismatch** | 20 | 🔴 CRITICAL | Replace `/Users/bob` → `/Users/alice` |
| **multi-trit-identity** | 10 | 🔵 LOW | Skills claim multiple trits (ok) |
| **gf3-violation-noted** | 4 | 🟡 MEDIUM | Add rebalancing skill to triad |
| **voice-saturation** | 4 | 🔵 LOW | Limit `say -v` voices per skill |
| **mcp-multi-world-collision** | 2 | 🟠 HIGH | Separate world_X refs |
| **schema-redefinition** | 2 | 🟡 MEDIUM | Consolidate @acset_type |

### Critical Path Conflicts (Top 10)

| Skill | Conflict |
|-------|----------|
| duck-agent | duckdb-path-mismatch |
| duckdb-ies | duckdb-path-mismatch |
| ies-triadic | duckdb-path-mismatch |
| naturality-factor | duckdb-path-mismatch |
| pun-decomposition | duckdb-path-mismatch |
| sense | duckdb-path-mismatch |
| browser-history-acset | duckdb-path-mismatch |
| duck-time-travel | duckdb-path-mismatch |
| hyjax-relational | duckdb-path-mismatch |
| wev-liquidity-monitor | mcp-multi-world-collision |

## GF(3) Conserved Triads (15 verified)

| MINUS (-1) | ERGODIC (0) | PLUS (+1) |
|------------|-------------|-----------|
| hvm-runtime | rama-gay-clojure | scheme |
| topos-of-music | rama-gay-clojure | file-organizer |
| topos-of-music | protocol-acset | scheme |
| godel-machine | rama-gay-clojure | scheme |
| topos-of-music | rama-gay-clojure | joker-lint |
| turing-chemputer | zig-programming | trifurcated-transfer |
| topos-of-music | terminal | triadic-skill-orchestrator |
| invoice-organizer | rama-gay-clojure | scheme |
| ocaml | directed-interval | scheme |
| topos-of-music | stellogen | self-validation-loop |
| ocaml | amp-team-usage | scheme |
| topos-of-music | rama-gay-clojure | curiosity-driven |
| ocaml | influence-propagation | scheme |
| babashka | duck-agent | acsets |
| sicp | random-walk-fusion | duckdb |

## Integration Patterns

### 1. ACSet-DuckDB Bridge
```clojure
(defn acset->duckdb [acset db-path]
  (duck/execute! db-path
    "INSERT INTO acset_morphisms VALUES (?, ?)"
    [(:src acset) (:tgt acset)]))
```

### 2. SICP Chapter Walker
```clojure
(defn sicp-walk [seed chapters]
  (let [walk-fn (random-walk-fusion seed)]
    (take 5 (iterate walk-fn {:chapter 1}))))
```

### 3. Functional Schema Pipeline
```clojure
(def sicp-schema
  '{:Ob [Procedure Data]
    :Hom {:apply [Procedure Data]
          :eval [Data Procedure]}})
```

## Usage

Load balanced triads:
```bash
skill acsets babashka duck-agent  # GF(3) = 0
skill sicp random-walk-fusion duck-agent  # GF(3) = 0
```

---
**Generated**: 2026-01-01 via random-walk-fusion  
**Seeds**: 0xDEAD (MINUS), 0xBEEF (ERGODIC), 0xCAFE (PLUS)
