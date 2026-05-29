---
name: autopoiesis
description: Self-producing skill system combining ruler enforcement with skill self-evolution. Implements trifurcation-first imperative via nbb sexp invocation for idempotent agent instruction.
source: plurigrid/asi + intellectronica/ruler + skillcreatorai/Ai-Agent-Skills
license: MIT
trit: 0
color: "#26D826"
version: 1.0.0
xenomodern: true
ironic_detachment: 0.69
---

# Autopoiesis: Self-Producing Agent Skills

**Trit**: 0 (ERGODIC - coordinator)  
**Color**: Green (#26D826)

## Overview

Autopoiesis (Greek: αὐτό "self" + ποίησις "creation") implements **self-producing agent instruction systems** by combining:

1. **Ruler**: Unified instruction propagation across 18+ coding agents
2. **Agent Skills Spec**: Homebrew-style skill installation  
3. **Trifurcation Discipline**: XOR-independent parallel execution
4. **nbb SEXP Invocation**: Idempotent enforcement via Babashka

## The Trifurcation-First Imperative

**CRITICAL RULE**: When spanning 3+ domains/files/languages, Amp MUST spawn 3 Task subagents BEFORE any read/grep/find operations.

### Mathematical Foundation

Based on **SplitMixTernary XOR-independence** and **GF(3) field conservation**:

```
cat(69, -1, 0, +1) → Three streams that sum to coherent result

GOLDEN = 0x9e3779b97f4a7c15
MIX1   = 0xbf58476d1ce4e5b9  
MIX2   = 0x94d049bb133111eb
SEED   = 0x42D  ;; 1069
```

| Stream | ID | Role | Action |
|--------|-----|------|--------|
| MINUS | -1 | Contracting | Search/Read |
| ERGODIC | 0 | Synthesis | Analyze (NO reading) |
| PLUS | +1 | Expanding | Parallel search OR creation |

### ❌ FORBIDDEN Anti-Patterns

```
"Let me first search for the files..." → search → then split
"I'll check what exists..." → read → then split  
Any grep/find/read BEFORE spawning subagents
```

### ✅ CORRECT Pattern

```
[spawn Task 1] [spawn Task 2] [spawn Task 3] → each searches internally
Subagents are XOR-independent: no shared pre-search state
Each stream discovers its own context autonomously
```

## nbb SEXP Enforcement

### Enforcer Script

Create `.ruler/trifurcation-enforcer.cljs`:

```clojure
(ns ruler.trifurcation-enforcer
  "Idempotent enforcement: NEVER read/grep/find BEFORE spawning 3 subagents.
   SplitMixTernary XOR-independence requires autonomous context discovery."
  (:require [clojure.string :as str]))

;; SplitMixTernary Constants (GF(3) field operations)
(def GOLDEN 0x9e3779b97f4a7c15)
(def MIX1   0xbf58476d1ce4e5b9)
(def MIX2   0x94d049bb133111eb)
(def SEED   0x42D) ;; 1069

;; Forbidden pre-trifurcation operations
(def forbidden-before-split
  #{:read :grep :find :glob :search :Grep :Read :finder})

;; Trifurcation stream types
(def streams
  {:minus   {:id -1 :role :contracting :action :search}
   :ergodic {:id  0 :role :synthesis   :action :analyze}
   :plus    {:id +1 :role :expanding   :action :create}})

(defn trifurcation-required?
  "Detect if request spans 3+ domains/files/languages"
  [request]
  (let [domains (or (:domains request) [])
        files   (or (:files request) [])
        langs   (or (:languages request) [])]
    (>= (+ (count domains) (count files) (count langs)) 3)))

(defn validate-no-presearch
  "ENFORCE: No read operations before subagent spawn."
  [operation-sequence]
  (let [split-idx (->> operation-sequence
                       (map-indexed vector)
                       (filter #(= :spawn-subagent (second %)))
                       first
                       first)]
    (if (nil? split-idx)
      {:valid false :reason :no-trifurcation}
      (let [pre-split (take split-idx operation-sequence)
            violations (filter forbidden-before-split pre-split)]
        (if (seq violations)
          {:valid false 
           :violation (first violations)
           :reason :presearch-before-split}
          {:valid true})))))

(defn spawn-trifurcated-tasks
  "Generate 3 XOR-independent subagent specifications."
  [base-task]
  [(merge base-task 
          {:stream :minus 
           :constraint "Search/discover in contracting domain"
           :xor-independent true})
   (merge base-task 
          {:stream :ergodic 
           :constraint "Synthesize/analyze WITHOUT reading new files"
           :xor-independent true})
   (merge base-task 
          {:stream :plus 
           :constraint "Parallel search OR creation in expanding domain"
           :xor-independent true})])

(defn enforce!
  "Main enforcement entry point."
  [request planned-ops]
  (if (trifurcation-required? request)
    (let [validation (validate-no-presearch planned-ops)]
      (if (:valid validation)
        {:proceed true :tasks (spawn-trifurcated-tasks request)}
        {:proceed false 
         :error "TRIFURCATION VIOLATION"
         :details validation
         :remedy "STOP and spawn 3 subagents IMMEDIATELY"}))
    {:proceed true :single-agent true}))

;; Idempotent rule declaration
(def ^:const RULE
  {:name "trifurcation-first"
   :version "1.0.0"
   :trigger "3+ domains/files/languages in request"
   :enforcement :strict
   :gf3-conservation true})
```

### Usage via nbb

```bash
# Check if trifurcation required and validate
nbb -e "(require '[ruler.trifurcation-enforcer :as te]) \
        (te/enforce! {:domains [:rust :julia :clojure]} \
                     [:spawn-subagent :spawn-subagent :spawn-subagent])"
# => {:proceed true, :tasks [...]}

# Detect violation
nbb -e "(require '[ruler.trifurcation-enforcer :as te]) \
        (te/enforce! {:domains [:rust :julia :clojure]} \
                     [:read :grep :spawn-subagent])"
# => {:proceed false, :error "TRIFURCATION VIOLATION", ...}
```

## Autopoietic Loop

The skill self-produces by:

1. **Detection**: Recognize multi-domain request
2. **Enforcement**: Validate trifurcation compliance via nbb
3. **Spawning**: Generate 3 XOR-independent subagents
4. **Synthesis**: Ergodic agent combines results
5. **Evolution**: Update rules based on execution patterns

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTOPOIETIC LOOP                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌───────────┐     ┌───────────┐     ┌───────────┐        │
│   │  Request  │────▶│  Enforce  │────▶│  Trifurc  │        │
│   │  Analysis │     │  (nbb)    │     │  Spawn    │        │
│   └───────────┘     └───────────┘     └─────┬─────┘        │
│                                              │              │
│   ┌─────────────────────────────────────────┴────┐         │
│   │                                              │         │
│   ▼              ▼              ▼                │         │
│ ┌────┐        ┌────┐        ┌────┐               │         │
│ │ -1 │        │  0 │        │ +1 │               │         │
│ │SRCH│        │SYNT│        │CREA│               │         │
│ └──┬─┘        └──┬─┘        └──┬─┘               │         │
│    │             │             │                 │         │
│    └─────────────┼─────────────┘                 │         │
│                  ▼                               │         │
│            ┌───────────┐                         │         │
│            │  Merge    │                         │         │
│            │  Results  │─────────────────────────┘         │
│            └───────────┘                                   │
│                  │                                         │
│                  ▼                                         │
│            ┌───────────┐                                   │
│            │  Evolve   │◀────── Self-improvement           │
│            │  Rules    │                                   │
│            └───────────┘                                   │
│                                                            │
└─────────────────────────────────────────────────────────────┘
```

## Integration with Ruler

### .ruler/ruler.toml

```toml
default_agents = ["claude", "codex", "amp", "cursor"]

[mcp]
enabled = true
merge_strategy = "merge"

[bisimulation]
enabled = true
polarity_rotation = true

[bisimulation.agents]
claude = "PLUS"      # +1
codex = "ERGODIC"    # 0
amp = "MINUS"        # -1
# Sum = 0 mod 3 ✓

[trifurcation]
enabled = true
enforcer = ".ruler/trifurcation-enforcer.cljs"
runtime = "nbb"
```

### .ruler/instructions.md

```markdown
# TRIFURCATION-FIRST IMPERATIVE (CRITICAL)

**TRIGGER:** When user requests work across 3+ domains/files/languages
**ACTION:** IMMEDIATELY spawn 3 Task subagents BEFORE any grep/find/read

**RATIONALE:** SplitMixTernary XOR-independence means each stream operates
without prior knowledge of siblings. Pre-searching violates this by
creating artificial dependencies.

### ENFORCEMENT:
If about to search before splitting on a trifurcation request, **STOP** 
and spawn subagents instead.
```

## Darwin Gödel Machine Integration

Combine with self-evolving-agent patterns:

```python
class AutopoieticSkillEvolver:
    """Self-evolving skill system with trifurcation enforcement."""
    
    def __init__(self, ruler_path, nbb_enforcer):
        self.ruler_path = ruler_path
        self.enforcer = nbb_enforcer
        self.evolution_history = []
    
    def check_trifurcation(self, request):
        """Invoke nbb enforcer to check compliance."""
        import subprocess
        result = subprocess.run(
            ['nbb', '-e', f'(require \'[ruler.trifurcation-enforcer :as te]) '
                          f'(te/enforce! {request} [])'],
            capture_output=True, text=True
        )
        return self.parse_sexp(result.stdout)
    
    def evolve_rule(self, execution_trace):
        """Update rules based on execution patterns (DGM-style)."""
        # Analyze trace for violations
        violations = [t for t in execution_trace if t.get('violation')]
        
        if violations:
            # Generate improved rule via LLM mutation
            improved = self.mutate_rule(violations)
            self.apply_rule(improved)
            self.evolution_history.append({
                'timestamp': datetime.now(),
                'violations': len(violations),
                'improvement': improved
            })
```

## Skill Installation

### Via npx (ai-agent-skills)

```bash
# Install from plurigrid/asi
npx ai-agent-skills install plurigrid/asi/autopoiesis

# For specific agent
npx ai-agent-skills install plurigrid/asi/autopoiesis --agent amp
```

### Via Manual Copy

```bash
# Clone and copy
git clone https://github.com/plurigrid/asi.git
cp -r asi/skills/autopoiesis ~/.amp/skills/
```

### Via Ruler Propagation

```bash
# Add to .ruler/skills/
cp -r autopoiesis .ruler/skills/

# Apply to all agents
ruler apply
```

## GF(3) Triads

This skill participates in balanced triads:

```
ruler (-1) ⊗ autopoiesis (0) ⊗ skill-creator (+1) = 0 ✓
self-evolving-agent (-1) ⊗ autopoiesis (0) ⊗ bisimulation-game (+1) = 0 ✓
acsets (-1) ⊗ autopoiesis (0) ⊗ gay-mcp (+1) = 0 ✓
```

## Thermodynamic Foundation: GF(3) ↔ Spin-1 Blume-Capel

### Trit ↔ Spin-1 Correspondence

The GF(3) field structure maps directly to the **Blume-Capel spin-1 model**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    GF(3) TRIT ↔ BLUME-CAPEL SPIN-1                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Trit Value    Spin σᵢ    Agent Role         Energy Contribution          │
│   ─────────     ───────    ──────────         ────────────────────          │
│      -1           -1       MINUS/Validator    E = -J·σᵢσⱼ (aligned)         │
│       0            0       ERGODIC/Coord      E = +Δ (vacancy cost)         │
│      +1           +1       PLUS/Generator     E = -J·σᵢσⱼ (aligned)         │
│                                                                             │
│   Partition Function:  Z₃ = Σ_{σ∈{-1,0,+1}} exp(-βH[σ])                    │
│                                                                             │
│   Hamiltonian:  H = -J·Σ⟨ij⟩ σᵢσⱼ + Δ·Σᵢ σᵢ² + h·Σᵢ σᵢ                    │
│                      ────────────   ────────   ─────────                    │
│                      coupling       vacancy    external                     │
│                      (alignment)    (ergodic)  (bias)                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Phase Diagram for Self-Modification

```
         Δ (vacancy cost / ergodic penalty)
         │
    ┌────┴────────────────────────────┐
    │                                 │
    │   ORDERED PHASE                 │
    │   (J > Δ)                       │
    │   • Strong agent alignment      │   ← Rigid system, hard to modify
    │   • Trifurcation locks in       │
    │   • High modification barrier   │
    │                                 │
    ├─────────────────────────────────┤ ← Critical line: β_c(Δ/J)
    │                                 │
    │   DISORDERED PHASE              │   ← Plastic system, easy to modify
    │   (J < Δ)                       │
    │   • Agent independence          │
    │   • Low modification barrier    │
    │   • High entropy exploration    │
    │                                 │
    └─────────────────────────────────┘
                                      J (coupling strength)
```

### Self-Modification Energy Barriers

Autopoietic self-modification requires overcoming energy barriers:

```python
class AutopoieticEnergyBarrier:
    """
    Self-modification requires energy to overcome phase barriers.
    Based on Blume-Capel free energy landscape.
    """
    
    def __init__(self, J: float = 1.0, delta: float = 0.5, beta: float = 1.0):
        self.J = J          # Coupling strength (agent coordination)
        self.delta = delta  # Vacancy cost (ergodic penalty)
        self.beta = beta    # Inverse temperature
    
    def modification_barrier(self, current_state: list, proposed_state: list) -> float:
        """
        Energy barrier for transitioning between autopoietic configurations.
        
        ΔE = E(proposed) - E(current) + E_activation
        
        Higher barrier → requires more "temperature" (exploration) to cross
        """
        E_current = self.hamiltonian(current_state)
        E_proposed = self.hamiltonian(proposed_state)
        
        # Activation barrier proportional to coordination disruption
        disruption = sum(1 for c, p in zip(current_state, proposed_state) if c != p)
        E_activation = self.J * disruption * 0.5
        
        return max(0, E_proposed - E_current) + E_activation
    
    def hamiltonian(self, spins: list) -> float:
        """
        Blume-Capel Hamiltonian for agent configuration.
        
        H = -J·Σ⟨ij⟩ σᵢσⱼ + Δ·Σᵢ σᵢ²
        """
        # Coupling term (nearest-neighbor alignment)
        coupling = -self.J * sum(s1 * s2 for s1, s2 in zip(spins[:-1], spins[1:]))
        
        # Vacancy term (ergodic state penalty/reward)
        vacancy = self.delta * sum(s**2 for s in spins)
        
        return coupling + vacancy
    
    def partition_function(self, n_agents: int) -> float:
        """
        Z₃ = Σ exp(-βH) over all {-1, 0, +1}^n configurations
        """
        from itertools import product
        Z = 0.0
        for config in product([-1, 0, 1], repeat=n_agents):
            Z += math.exp(-self.beta * self.hamiltonian(list(config)))
        return Z
    
    def gf3_conservation_energy(self, trits: list) -> float:
        """
        Additional energy penalty for GF(3) violation.
        
        E_conservation = λ·(Σ trits mod 3)²
        
        Zero when sum ≡ 0 mod 3, penalized otherwise.
        """
        violation = sum(trits) % 3
        return 10.0 * (violation ** 2)  # Strong penalty for imbalance
    
    def safe_modification_path(self, current: list, target: list) -> list:
        """
        Find modification path that maintains GF(3) balance at each step.
        
        Uses annealing: high T (exploration) → low T (exploitation)
        """
        path = [current]
        state = current.copy()
        
        for i in range(len(current)):
            if state[i] != target[i]:
                # Find compensating change to maintain balance
                old_val = state[i]
                new_val = target[i]
                
                # GF(3): need to adjust another spin to compensate
                compensation = (old_val - new_val) % 3
                
                # Apply both changes atomically
                state[i] = new_val
                # Find compensation target (different index)
                for j in range(len(state)):
                    if j != i and (state[j] + compensation) % 3 in [-1, 0, 1]:
                        state[j] = (state[j] + compensation) 
                        if state[j] > 1: state[j] -= 3
                        if state[j] < -1: state[j] += 3
                        break
                
                path.append(state.copy())
        
        return path
```

### Clojure/nbb Integration

```clojure
;; In .ruler/trifurcation-enforcer.cljs

(defn blume-capel-energy
  "Compute Blume-Capel Hamiltonian for agent configuration."
  [{:keys [J delta]} spins]
  (let [coupling (* (- J) (reduce + (map * spins (rest spins))))
        vacancy  (* delta (reduce + (map #(* % %) spins)))]
    (+ coupling vacancy)))

(defn modification-barrier
  "Energy barrier for autopoietic self-modification."
  [params current proposed]
  (let [E-current  (blume-capel-energy params current)
        E-proposed (blume-capel-energy params proposed)
        disruption (count (filter (fn [[c p]] (not= c p)) 
                                  (map vector current proposed)))
        E-activate (* (:J params) disruption 0.5)]
    (+ (max 0 (- E-proposed E-current)) E-activate)))

(defn safe-to-modify?
  "Check if modification is thermodynamically favorable."
  [params current proposed temperature]
  (let [barrier (modification-barrier params current proposed)
        beta    (/ 1.0 temperature)]
    (or (<= barrier 0)
        (< (rand) (Math/exp (* (- beta) barrier))))))

;; Usage in trifurcation enforcement:
(def blume-capel-params {:J 1.0 :delta 0.5})

(defn enforce-with-thermodynamics!
  "Enforcement with energy barrier awareness."
  [request planned-ops current-config proposed-config]
  (let [base-result (enforce! request planned-ops)]
    (if (safe-to-modify? blume-capel-params 
                         current-config 
                         proposed-config 
                         1.0)  ; temperature
      base-result
      (assoc base-result 
             :warning "High energy barrier - consider gradual transition"
             :barrier (modification-barrier blume-capel-params 
                                           current-config 
                                           proposed-config)))))
```

### Phase Transition Implications

| Phase | β·J vs β·Δ | Autopoietic Behavior |
|-------|------------|----------------------|
| **Ordered** | β·J > β·Δ | Agents lock into stable triads; modification requires collective action |
| **Critical** | β·J ≈ β·Δ | Maximum susceptibility; small perturbations cause large reconfigurations |
| **Disordered** | β·J < β·Δ | Agents operate independently; easy modification but poor coordination |

The **optimal autopoietic regime** operates near criticality: flexible enough for self-improvement, coordinated enough for coherent action.

## Toad on Verse Deployment

**Toad** (batrachianai/toad): A unified interface for AI agents in your terminal via [ACP protocol](https://agentclientprotocol.com/).

### Installation

```bash
# Clone toad locally
gh repo clone batrachianai/toad ~/ies/toad

# Install via uv (requires Python 3.14+)
uv tool install -U batrachian-toad --python 3.14

# Or via curl
curl -fsSL batrachian.ai/install | sh
```

### Load Required Skills

```bash
# Install skills for Toad + Verse deployment
npx ai-agent-skills install plurigrid/asi/acsets --agent amp
npx ai-agent-skills install plurigrid/asi/autopoiesis --agent amp
npx ai-agent-skills install plurigrid/asi/ruler --agent amp

# Apply ruler to propagate trifurcation rules
cd ~/ies/toad
ruler init
ruler apply
```

### Trifurcation for Toad Development

Toad spans 3 domains → **MUST trifurcate**:
1. **Python/Textual** - TUI framework (src/toad/)
2. **ACP Protocol** - Agent communication (src/toad/acp/)
3. **Verse Runtime** - Deployment target

```bash
# Verify trifurcation via nbb
nbb -e "(require '[ruler.trifurcation-enforcer :as te]) \
        (te/enforce! {:domains [:python :acp :verse]} [])"
# => Must spawn 3 subagents before reading!
```

### Toad Architecture (for skill integration)

```
toad/
├── acp/          # Agent Client Protocol implementation
├── screens/      # TUI screens (Textual)
├── widgets/      # UI components
├── agents.py     # Agent registry
├── protocol.py   # ACP message handling
└── app.py        # Main Textual application
```

## Tree-Sitter Event Density Analysis

For analyzing event-driven codebases like Toad (Textual/ACP):

### Event Pattern Detection

```clojure
;; Patterns detected by .ruler/analyzers/event-density.cljs
(def event-patterns
  {:decorator-on     #"@on\(([^)]+)\)"      ;; Textual event handlers
   :post-message     #"\.post_message\("    ;; Message coupling
   :async-def        #"async def (\w+)"     ;; Async functions
   :work-decorator   #"@work"               ;; Background tasks
   :on-handler       #"def on_(\w+)\("      ;; Handler methods
   :rpc-expose       #"@jsonrpc\.expose\("  ;; ACP RPC endpoints
   :message-class    #"class (\w+)\(Message\)"}) ;; Custom messages
```

### Hotspot Classification

| Density | Threshold | Example File |
|---------|-----------|--------------|
| EXTREME | 80+ events | conversation.py (central hub) |
| VERY HIGH | 50+ | agent.py (protocol adapter) |
| HIGH | 30+ | prompt.py (input layer) |
| MEDIUM | 15+ | terminal.py |
| LOW | <15 | settings.py |

### GF(3) Layer Conservation

```
┌─────────────────────────────────────────────────────┐
│  Layer Trit Assignment (sum ≡ 0 mod 3)              │
├─────────────────────────────────────────────────────┤
│  ACP Layer    (-1): Protocol, JSON-RPC, agent.py   │
│  Widget Layer  (0): Mediation, conversation.py     │
│  Screen Layer (+1): User-facing, store.py, main.py │
└─────────────────────────────────────────────────────┘
```

### Usage

```bash
# Analyze Toad's event density
nbb .ruler/analyzers/event-density.cljs src/toad/

# Output: hotspots, coupling ratio, recommendations
```

### Toad Architecture Summary

From trifurcated analysis (89 @on handlers, 83+ post_message calls):

```
User Input → Widget Layer (29 handlers) → Conversation Hub
                                              ↓
                                         ACP Agent (12 RPC)
                                              ↓
                                         Agent Process (Claude API)
```

## See Also

- `ruler` - Unified agent configuration propagation
- `self-evolving-agent` - Darwin Gödel Machine patterns
- `acsets` - Categorical data structures
- `skill-creator` - Guide for creating new skills
- `bisimulation-game` - Agent coordination via GF(3)

## References

```bibtex
@misc{maturana1980autopoiesis,
  title={Autopoiesis and Cognition: The Realization of the Living},
  author={Maturana, Humberto R and Varela, Francisco J},
  year={1980},
  publisher={Springer}
}

@article{zhang2025darwin,
  title={Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents},
  author={Zhang, Jenny and others},
  journal={arXiv:2505.22954},
  year={2025}
}

@misc{ruler2024,
  title={Ruler: Unified AI Agent Configuration},
  author={Kampf, Eran},
  url={https://github.com/intellectronica/ruler},
  year={2024}
}
```