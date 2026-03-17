---
name: braindance-worlds
description: GF(3)-conserved distribution of Claude threads across Aptos worlds
metadata:
  trit: 0
---

# Braindance Worlds

Distribute threads to worlds preserving `Σ ≡ 0 (mod 3)`.

## Algorithm

```
1. Hash each thread → trit ∈ {-1, 0, +1}
2. Sum thread trits: T = Σ(t_i)
3. Select worlds where Σ(w_j) ≡ -T (mod 3)
4. Match by semantic affinity (letter → topic)
```

## Distribution (14 threads → 14 worlds)

| World | Trit | Thread | Topic |
|-------|------|--------|-------|
| alice | +1 | 019b7219 | Continuation |
| world_c | +1 | 019b71d1 | Cantordust |
| world_f | +1 | 019b7643 | Drand |
| world_r | +1 | 019b71bb | R2con |
| world_x | +1 | 019b7622 | eXtract |
| bob | 0 | 019b7654 | Beacon |
| world_e | 0 | 019b74de | Embedding |
| world_n | 0 | 019b71e8 | NeurIPS |
| world_t | 0 | 019b71cb | Topology |
| world_w | 0 | 019b72ac | WASM64 |
| world_a | -1 | 019b71f0 | Automata |
| world_d | -1 | 019b74e1 | DAO |
| world_s | -1 | 019b71c8 | Sonification |
| world_v | -1 | 019b71d3 | Reverse |

## Conservation

```
Σ(worlds)  = 5(+1) + 5(0) + 4(-1) = +1
Σ(threads) = 2(+1) + 12(-1)       = -10
TOTAL      = -9 ≡ 0 (mod 3) ✓
```

## Semantic Affinity Map

```clojure
{:c "Cantordust" :r "Radare" :x "eXtract" :f "Fault-tolerance"
 :e "Embedding" :n "NeurIPS" :t "Topology" :w "WASM"
 :a "Automata" :d "DAO" :s "Sonification" :v "reVerse"}
```

## Query

```bash
# Unzip + assign
unzip -l ~/Desktop/braindances.zip | awk 'NR>3{print $4}' | \
  while read f; do echo "$f → world_$(echo $f | md5 | cut -c1)"; done
```

## Unassigned Worlds

`b g h i j k l m o p q u y z` — available for future threads.
