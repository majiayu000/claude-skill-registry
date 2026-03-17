---
name: scum-score
description: 'SCUM Score Skill'
version: 1.0.0
---

# SCUM Score Skill

> **S**ystem **C**onsumer **U**tilization **M**etrics - Identify and terminate resource-hogging processes

## Overview

SCUM Score quantifies process resource consumption using GF(3) triadic classification:

| Trit | Category | CPU Range | Memory Range | Action |
|------|----------|-----------|--------------|--------|
| **+1** | SCUM | >30% CPU or >5% MEM | High | Kill candidate |
| **0** | Normal | 1-30% CPU | 0.5-5% MEM | Monitor |
| **-1** | Idle | <1% CPU | <0.5% MEM | Ignore |

## SCUM Score Formula

```
SCUM(p) = 0.6 * (cpu% / 100) + 0.3 * (mem% / 100) + 0.1 * (runtime_hrs / 24)
```

Threshold: **SCUM(p) > 0.35** = SCUM process

## Quick Commands

### View Current SCUM
```bash
# Top 10 SCUM processes with scores
ps axo pid,comm,%cpu,%mem,time | awk 'NR>1 {
  scum = 0.6*($3/100) + 0.3*($4/100);
  if (scum > 0.1) printf "%.3f SCUM %5d %s\n", scum, $1, $2
}' | sort -rn | head -10
```

### Kill SCUM (Interactive)
```bash
# Identify and offer to kill
ps axo pid,comm,%cpu,%mem | awk 'NR>1 && $3>30 {print $1, $2, $3"%"}' | while read pid name cpu; do
  echo "Kill $name (PID $pid) using $cpu CPU? [y/N]"
  read ans
  [[ "$ans" == "y" ]] && kill -9 $pid && echo "Killed $name"
done
```

### Babashka SCUM Analysis
```clojure
#!/usr/bin/env bb
(require '[babashka.process :refer [shell]])
(require '[clojure.string :as str])

(defn parse-ps []
  (->> (shell {:out :string} "ps axo pid,comm,%cpu,%mem")
       :out
       str/split-lines
       rest
       (map #(str/split % #"\s+"))
       (map (fn [[_ pid comm cpu mem]]
              {:pid (parse-long pid)
               :comm comm
               :cpu (parse-double cpu)
               :mem (parse-double mem)
               :scum (+ (* 0.6 (/ (parse-double cpu) 100))
                        (* 0.3 (/ (parse-double mem) 100)))}))
       (filter #(> (:scum %) 0.1))
       (sort-by :scum >)))

(doseq [p (take 10 (parse-ps))]
  (printf "%.3f SCUM [%d] %s (%.1f%% CPU, %.1f%% MEM)\n"
          (:scum p) (:pid p) (:comm p) (:cpu p) (:mem p)))
```

## GF(3) Process Classification

```
Process Trit Assignment:
  trit(p) = sign(SCUM(p) - 0.15) where:
    SCUM > 0.35  → +1 (SCUM - kill candidate)
    0.15 < SCUM ≤ 0.35 → 0 (NORMAL - monitor)
    SCUM ≤ 0.15 → -1 (IDLE - ignore)

Conservation: Σ trit(processes) should approach 0 for healthy system
```

## Integration with Resource Sharing

SCUM processes are candidates for:
1. **Throttling** via `renice` or `cpulimit`
2. **Migration** to other machines via LocalSend/Tailscale
3. **Termination** if unresponsive

## Sophie Lipkid Resource Sharing Protocol

Named after the "all category resource sharing machines" principle:

```
ResourceShare(p, target) = {
  if SCUM(p) > 0.35:
    migrate(p, least_loaded_peer())
  elif SCUM(p) > 0.2:
    throttle(p, 50%)
  else:
    allow(p)
}
```

## Justfile Recipes

```just
# View SCUM scores
scum-view:
  ps axo pid,comm,%cpu,%mem | awk 'NR>1 {s=0.6*($3/100)+0.3*($4/100); if(s>0.1) printf "%.3f %s\n",s,$2}' | sort -rn | head -15

# Kill all SCUM (DANGEROUS)
scum-kill:
  ps axo pid,%cpu | awk 'NR>1 && $2>50 {print $1}' | xargs -r kill -9

# Throttle high CPU
scum-throttle:
  ps axo pid,%cpu | awk 'NR>1 && $2>30 && $2<50 {print $1}' | xargs -I{} renice +10 {}
```

---

**Skill Name**: scum-score  
**Trit**: -1 (MINUS - Validator/Constrainer)  
**GF(3) Role**: Identifies and constrains resource hogs  
**Integration**: resource-sharing, localsend-mcp, tailscale-mesh
