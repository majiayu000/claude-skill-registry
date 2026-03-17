---
name: gay-fokker-planck-staging
description: Two Fokker-Plancks per staging gate, conditioned on (rama OR goblins)
  with accessible counterfactual worlds for each skill load.
license: MIT
metadata:
  trit: 0
  gf3_triad: fokker-planck-analyzer (-1) ⊗ gay-fokker-planck-staging (0) ⊗ agent-o-rama (+1)
  condition: "(rama OR goblins)"
  status: NOT_IN_PLURIGRID_ASI
---

# Gay Fokker-Planck Staging

> *"Each staging gate requires two independent convergence checks"*

**Trit**: 0 (ERGODIC - coordinator)
**Color**: #26D826 (Green)
**Condition**: `(rama OR goblins)` - distributed capability requirement

---

## Overview

Every skill activation MUST:
1. Pass through **two Fokker-Planck equilibrium checks**
2. Provide **accessible counterfactual worlds** (rama-path, goblins-path, both-path)
3. Satisfy triangle inequality for world accessibility
4. Conserve GF(3) across staging gates

## Staging Gate Protocol

```clojure
(defn staging-gate [skill seed]
  (let [;; Two independent Fokker-Planck checks
        fp1 (fokker-planck-check skill :temperature 0.01)
        fp2 (fokker-planck-check skill :temperature 0.001)

        ;; Condition: rama OR goblins available
        rama-accessible? (check-capability :rama)
        goblins-accessible? (check-capability :goblins)
        condition-met? (or rama-accessible? goblins-accessible?)]

    {:skill skill
     :fp1-converged (:converged fp1)
     :fp2-converged (:converged fp2)
     :staging-pass (and (:converged fp1)
                        (:converged fp2)
                        condition-met?)
     :condition {:rama rama-accessible?
                 :goblins goblins-accessible?}}))
```

## Counterfactual Worlds (Mandatory)

Each skill MUST declare accessible counterfactual worlds:

```ruby
class SkillWithWorlds
  attr_reader :actual_world, :counterfactuals

  def initialize(skill_name, seed)
    @actual_world = PossibleWorld.new(seed: seed, skill: skill_name)

    # MANDATORY: Three counterfactual paths
    @counterfactuals = [
      rama_world(seed),      # W₁: rama-only execution
      goblins_world(seed),   # W₂: goblins-only execution
      both_world(seed)       # W₃: rama + goblins
    ]
  end

  def rama_world(seed)
    PossibleWorld.new(
      seed: derive(seed, :rama),
      variant: :rama,
      accessible: true,
      distance_from_actual: 1.0
    )
  end

  def goblins_world(seed)
    PossibleWorld.new(
      seed: derive(seed, :goblins),
      variant: :goblins,
      accessible: true,
      distance_from_actual: 1.0
    )
  end

  def both_world(seed)
    PossibleWorld.new(
      seed: derive(derive(seed, :rama), :goblins),
      variant: :both,
      accessible: true,
      distance_from_actual: 1.414  # √2, composed path
    )
  end
end
```

## Triangle Inequality Verification

```
        actual
         /\
    1.0 /  \ 1.0
       /    \
   rama ---- goblins
        1.0

Triangle: d(actual, goblins) ≤ d(actual, rama) + d(rama, goblins)
          1.0 ≤ 1.0 + 1.0 = 2.0 ✓
```

## Two Fokker-Plancks Per Staging

### Why Two?

1. **Temperature sensitivity**: Different T reveals different equilibria
2. **Mixing time validation**: Second check confirms first wasn't premature
3. **Gibbs distribution verification**: Two independent samples

### Implementation

```python
def dual_fokker_planck_gate(skill_trajectory):
    # FP1: Higher temperature (exploration)
    fp1 = fokker_planck_check(
        trajectory=skill_trajectory,
        temperature=0.01,
        mixing_threshold=100
    )

    # FP2: Lower temperature (exploitation)
    fp2 = fokker_planck_check(
        trajectory=skill_trajectory,
        temperature=0.001,
        mixing_threshold=500
    )

    # Both must converge
    return fp1.converged and fp2.converged
```

## Random Walk Agent Protocol

Three agents walk skills, each with counterfactual worlds:

```clojure
(def agent-seeds [0xDEAD01 0xBEEF02 0xCAFE03])

(defn agent-walk [seed]
  {:agent-trit (- (mod seed 3) 1)
   :skills (for [step (range 3)]
             (let [skill (walk-step seed step)
                   worlds (counterfactual-worlds skill seed)]
               {:skill skill
                :trit (- (mod step 3) 1)
                :worlds worlds
                :staging (dual-fokker-planck-gate skill)}))})
```

## GF(3) Conservation

Each staging gate maintains:

```
Σ(skill trits) ≡ 0 (mod 3)

Agent 1: covariant-modification(-1) + cybernetic-immune(0) + X(+1) = 0 ✓
Agent 2: mdm-cobordism(-1) + tailscale-file-transfer(0) + Y(+1) = 0 ✓
Agent 3: discohy-streams(-1) + code-review(0) + Z(+1) = 0 ✓
```

## Commands

```bash
# Run staging gate
just gay-staging skill_name

# Check dual Fokker-Planck
just fp-dual-check trajectory.json

# List counterfactual worlds
just worlds-list skill_name

# Verify triangle inequality
just triangle-check skill_name
```

## PR Template

When committing to plurigrid/asi:

```markdown
## Summary
- Add gay-fokker-planck-staging skill
- Two FP equilibrium checks per staging gate
- Mandatory counterfactual worlds (rama/goblins/both)

## Test plan
- [ ] Dual Fokker-Planck convergence
- [ ] Counterfactual world accessibility
- [ ] Triangle inequality verification
- [ ] GF(3) conservation across agents

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

**Skill Name**: gay-fokker-planck-staging
**Type**: Staging Gate Coordinator
**Trit**: 0 (ERGODIC)
**Condition**: (rama OR goblins)
**FP Gates**: 2 per staging
**Counterfactual Worlds**: 3 per skill (rama, goblins, both)
