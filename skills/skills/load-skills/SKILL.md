---
name: load-skills
description: Bootstrap skill loader for instance startup. Pulls fresh skills from plurigrid/asi and loads GF(3)-balanced startup triads. MUST run at beginning of every new instance.
version: 1.0.0
---


# Load Skills (Instance Bootstrap)

**MANDATORY first action on every new Claude Code instance.**

## Startup Protocol

```bash
# Step 1: Pull fresh skills (Rule -1 from AGENTS.md)
npx ai-agent-skills install plurigrid/asi --agent claude

# Step 2: Verify installation
ls ~/.claude/skills | wc -l  # Should be 280+
```

## Critical Startup Triads

Load these 9 skills in 3 GF(3)-balanced triads:

### Triad 1: Infrastructure (Σ = 0)

| Skill | Trit | Role | Purpose |
|-------|------|------|---------|
| gay-mcp | +1 | PLUS | Deterministic color/seed generation |
| ruler-maximal | 0 | ERGODIC | Skill loading orchestration |
| skill-validation-gf3 | -1 | MINUS | GF(3) conservation verification |

### Triad 2: Dispersal (Σ = 0)

| Skill | Trit | Role | Purpose |
|-------|------|------|---------|
| parallel-fanout | +1 | PLUS | Maximum parallelization (Rule 1) |
| bisimulation-game | 0 | ERGODIC | Skill dispersal across agents |
| spi-parallel-verify | -1 | MINUS | Parallelism safety verification |

### Triad 3: Execution (Σ = 0)

| Skill | Trit | Role | Purpose |
|-------|------|------|---------|
| aptos-agent | +1 | PLUS | Chain transaction execution |
| mcp-spec-checker | 0 | ERGODIC | Protocol validation |
| say-narration | -1 | MINUS | Voice announcements (constraints) |

## Voice Announcement (Rule 2)

After loading each triad, announce via `_` (say-narration resolves voice):

```bash
# All announcements use _ - say-narration picks non-English voice
say -v _ "Triad one loaded. Infrastructure ready."
say -v _ "Triad two loaded. Dispersal active."
say -v _ "Triad three loaded. Execution enabled."
```

**Note:** This skill DEPENDS on say-narration for voice selection.

## Verification

```bash
# Verify GF(3) conservation
# Sum of all 9 skill trits = (+1+0-1) + (+1+0-1) + (+1+0-1) = 0 ✓
echo "GF(3) sum: 0 (conserved)"
```

## Load Order

1. `gay-mcp` - Seeds all color assignments
2. `ruler-maximal` - Orchestrates subsequent loading
3. `skill-validation-gf3` - Validates before proceeding
4. `parallel-fanout` - Enables parallelism
5. `bisimulation-game` - Disperses to other agents
6. `spi-parallel-verify` - Verifies parallelism safety
7. `aptos-agent` - Ready for chain operations
8. `mcp-spec-checker` - Validates MCP protocols
9. `say-narration` - Announces completion

## Integration with ruler-maximal

This skill bootstraps ruler-maximal, which then handles:
- Loading 3 NEW skills per interaction (Rule 0)
- Maximum parallelization (Rule 1)
- Say narration (Rule 2)
- GF(3) color logic (Rule 3)

## Babashka Bootstrap Script

```clojure
#!/usr/bin/env bb
(ns load-skills
  (:require [babashka.process :refer [shell]]))

(def startup-triads
  [{:name "Infrastructure"
    :skills [{:name "gay-mcp" :trit 1}
             {:name "ruler-maximal" :trit 0}
             {:name "skill-validation-gf3" :trit -1}]}
   {:name "Dispersal"
    :skills [{:name "parallel-fanout" :trit 1}
             {:name "bisimulation-game" :trit 0}
             {:name "spi-parallel-verify" :trit -1}]}
   {:name "Execution"
    :skills [{:name "aptos-agent" :trit 1}
             {:name "mcp-spec-checker" :trit 0}
             {:name "say-narration" :trit -1}]}])

(defn verify-gf3 [triad]
  (let [sum (reduce + (map :trit (:skills triad)))]
    (zero? (mod sum 3))))

(defn load-triad! [triad]
  (println (format "Loading %s triad..." (:name triad)))
  (assert (verify-gf3 triad) "GF(3) violation!")
  (doseq [skill (:skills triad)]
    (println (format "  %s (%+d)" (:name skill) (:trit skill))))
  (shell "say" "-v" "_" (format "Triad %s loaded." (:name triad))))

(defn -main []
  ;; Step 1: Fresh pull
  (println "Pulling fresh skills from plurigrid/asi...")
  (shell "npx" "ai-agent-skills" "install" "plurigrid/asi" "--agent" "claude")

  ;; Step 2: Load triads
  (doseq [triad startup-triads]
    (load-triad! triad))

  ;; Step 3: Verify total
  (let [total-sum (reduce + (mapcat #(map :trit (:skills %)) startup-triads))]
    (println (format "\nTotal GF(3) sum: %d ≡ %d (mod 3)" total-sum (mod total-sum 3)))
    (assert (zero? (mod total-sum 3)) "Total GF(3) violation!")))

(when (= *file* (System/getProperty "babashka.file"))
  (-main))
```

## Related Skills

- `ruler-maximal` (0): Post-bootstrap orchestration
- `plurigrid-asi-integrated` (0): Unified skill lattice
- `skill-creator` (0): Creating new skills



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

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