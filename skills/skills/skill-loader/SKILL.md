---
name: skill-loader
description: Dynamic skill loading via polynomial functor arrangements. Loads skills as interfaces p = A^y^B where state changes rewire the system.
metadata:
  trit: 0
  category: meta
---

# Skill Loader

**Dynamic Skill Loading via Polynomial Functor Arrangements**

Based on Samantha Jarvis & David Spivak's work on dynamic structures, this skill treats skill loading as dynamic arrangement morphisms in the category **Poly**.

## Polynomial Semantics

Each skill is an interface polynomial:
```
p_skill = Outputs^y^Inputs
```

Loading skills creates composite arrangements:
```
p₁ ⊗ p₂ → System
```

The **state** `S` determines which arrangement is active. Loading a skill updates `s : S`, rewiring the system dynamically.

## Usage

```bash
# Load a single skill
bb ~/.claude/skills/skill-loader/load.bb skill-name

# Load multiple skills with GF(3) trit assignment
bb ~/.claude/skills/skill-loader/load.bb skill1:-1 skill2:0 skill3:+1

# List loadable skills
bb ~/.claude/skills/skill-loader/load.bb --list

# Query skill lattice
bb ~/.claude/skills/skill-loader/load.bb --lattice

# Reverse derivative: find skills that influence current state
bb ~/.claude/skills/skill-loader/load.bb --reverse
```

## Dynamic Arrangement Protocol

### State Space

```
State = (M, move, f, m)
```
Where:
- `M` = Parameterizing object (skill configuration space)
- `move : F(M) × F(M) → F(M)` = State update function
- `f : M × A → B` = Skill morphism (input → output transformation)
- `m : F(M)` = Current parameter (loaded skill configuration)

### Load Operation

Loading skill `s` creates arrangement morphism:
```
F(A) --[m × id]--> F(M) × F(A) --[F(f)]--> F(B)
```

### Update Rule

After skill execution, update state via reverse derivative:
```
F(A) × F(B) --[R[f]]--> F(M) × F(A) --[π; move]--> F(M)
```

## GF(3) Trit Assignment

Skills loaded in triads conserve:
```
Σ trits ≡ 0 (mod 3)
```

| Trit | Role | Hue Range |
|------|------|-----------|
| -1 (MINUS) | Validator/Constrainer | 180°-300° (cold) |
| 0 (ERGODIC) | Coordinator/Synthesizer | 60°-180° (neutral) |
| +1 (PLUS) | Generator/Executor | 0°-60°, 300°-360° (warm) |

## Babashka Implementation

```clojure
(ns skill-loader
  (:require [babashka.fs :as fs]
            [clojure.edn :as edn]
            [clojure.string :as str]))

(def skills-dir (str (System/getProperty "user.home") "/.claude/skills"))

(defn list-skills []
  (->> (fs/list-dir skills-dir)
       (filter fs/directory?)
       (map fs/file-name)
       (filter #(fs/exists? (fs/path skills-dir % "skill.md")))
       sort))

(defn parse-frontmatter [content]
  (when-let [[_ yaml] (re-find #"(?s)^---\n(.*?)\n---" content)]
    (reduce (fn [m line]
              (if-let [[_ k v] (re-find #"^(\w+):\s*(.+)$" line)]
                (assoc m (keyword k) v)
                m))
            {} (str/split-lines yaml))))

(defn load-skill [skill-name]
  (let [path (fs/path skills-dir skill-name "skill.md")]
    (when (fs/exists? path)
      (let [content (slurp (str path))
            meta (parse-frontmatter content)]
        {:name skill-name
         :meta meta
         :content content
         :loaded-at (System/currentTimeMillis)}))))

(defn load-triad [s1 s2 s3]
  "Load three skills with GF(3) conservation"
  (let [skills [(assoc (load-skill s1) :trit -1)
                (assoc (load-skill s2) :trit 0)
                (assoc (load-skill s3) :trit +1)]]
    {:skills skills
     :sum (reduce + (map :trit skills))
     :conserved? (zero? (mod (reduce + (map :trit skills)) 3))}))
```

## Integration with Dynamic Categories

Following (Shapiro & Spivak 2022), skill loading forms a **dynamic monoidal category** where:
- Objects are skill interfaces
- Morphisms are arrangements
- State updates follow reverse derivative backpropagation

This enables gradient-based skill optimization analogous to neural network training.

## References

- Jarvis, S. (2024). "Building dynamic structures". Topos Institute Blog.
- Shapiro, B.T. & Spivak, D.I. (2022). "Dynamic Categories, Dynamic Operads: From Deep Learning to Prediction Markets."
- Cockett et al. (2020). "Reverse Derivative Categories." CSL 2020.
