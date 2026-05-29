---
name: using-simulation-foundations
description: Router for simulation math - ODEs, state-space, stability, control, numerics, chaos, stochastic
---

# Using Simulation-Foundations (Meta-Skill Router)

**Your entry point to mathematical simulation foundations.** This skill routes you to the right combination of mathematical skills for your game simulation challenge.

## Purpose

This is a **meta-skill** that:
1. ✅ **Routes** you to the correct mathematical skills
2. ✅ **Combines** multiple skills for complex simulations
3. ✅ **Provides** workflows for common simulation types
4. ✅ **Explains** when to use theory vs empirical tuning

**You should use this skill:** When building any simulation system that needs mathematical rigor.

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-simulation-foundations/SKILL.md`

Reference sheets like `differential-equations-for-games.md` are at:
  `skills/using-simulation-foundations/differential-equations-for-games.md`

NOT at:
  `skills/differential-equations-for-games.md` ← WRONG PATH

When you see a link like `[differential-equations-for-games.md](differential-equations-for-games.md)`, read the file from the same directory as this SKILL.md.

---

## Core Philosophy: Theory Enables Design

### The Central Idea

**Empirical Tuning**: Trial-and-error adjustment of magic numbers
- Slow iteration (run simulation, observe, tweak, repeat)
- Unpredictable behavior (systems drift to extremes)
- No guarantees (stability, convergence, performance)
- Difficult debugging (why did it break?)

**Mathematical Foundation**: Formulate systems using theory
- Fast iteration (predict behavior analytically)
- Predictable behavior (stability analysis)
- Guarantees (equilibrium, convergence, bounds)
- Systematic debugging (root cause analysis)

### When This Pack Applies

**✅ Use simulation-foundations when:**
- Building physics, AI, or economic simulation systems
- Need stability guarantees (ecosystems, economies)
- Performance matters (60 FPS real-time constraints)
- Multiplayer determinism required (lockstep networking)
- Long-term behavior unpredictable (100+ hour campaigns)

**❌ Don't use simulation-foundations when:**
- Simple systems with no continuous dynamics
- Pure authored content (no simulation)
- Empirical tuning sufficient (static balance tables)
- Math overhead not justified (tiny indie game)

---

## Pack Overview: 8 Core Skills

### Wave 1: Foundational Mathematics

#### 1. differential-equations-for-games
**When to use:** ANY continuous dynamics (population, physics, resources)
**Teaches:** Formulating and solving ODEs for game systems
**Examples:** Lotka-Volterra ecosystems, spring-damper camera, resource regeneration
**Time:** 2.5-3.5 hours
**Key insight:** Systems with rates of change need ODEs

#### 2. state-space-modeling
**When to use:** Complex systems with many interacting variables
**Teaches:** Representing game state mathematically, reachability analysis
**Examples:** Fighting game frame data, RTS tech trees, puzzle solvability
**Time:** 2.5-3.5 hours
**Key insight:** Explicit state representation enables analysis

#### 3. stability-analysis
**When to use:** Need to prevent crashes, explosions, extinctions
**Teaches:** Equilibrium points, eigenvalue analysis, Lyapunov functions
**Examples:** Ecosystem balance, economy stability, physics robustness
**Time:** 3-4 hours
**Key insight:** Analyze stability BEFORE shipping

### Wave 2: Control and Integration

#### 4. feedback-control-theory
**When to use:** Smooth tracking, adaptive systems, disturbance rejection
**Teaches:** PID controllers for game systems
**Examples:** Camera smoothing, AI pursuit, dynamic difficulty
**Time:** 2-3 hours
**Key insight:** PID replaces magic numbers with physics

#### 5. numerical-methods
**When to use:** Implementing continuous systems in discrete timesteps
**Teaches:** Euler, Runge-Kutta, symplectic integrators
**Examples:** Physics engines, cloth, orbital mechanics
**Time:** 2.5-3.5 hours
**Key insight:** Integration method affects stability

#### 6. continuous-vs-discrete
**When to use:** Choosing model type (continuous ODEs vs discrete events)
**Teaches:** When to use continuous, discrete, or hybrid
**Examples:** Turn-based vs real-time, cellular automata, quantized resources
**Time:** 2-2.5 hours
**Key insight:** Wrong choice costs 10× performance OR 100× accuracy

### Wave 3: Advanced Topics

#### 7. chaos-and-sensitivity
**When to use:** Multiplayer desyncs, determinism requirements, sensitivity analysis
**Teaches:** Butterfly effect, Lyapunov exponents, deterministic chaos
**Examples:** Weather systems, multiplayer lockstep, proc-gen stability
**Time:** 2-3 hours
**Key insight:** Deterministic ≠ predictable

#### 8. stochastic-simulation
**When to use:** Random processes, loot systems, AI uncertainty
**Teaches:** Probability distributions, Monte Carlo, stochastic differential equations
**Examples:** Loot drops, crit systems, procedural generation
**Time:** 2-3 hours
**Key insight:** Naive randomness creates exploits

---

## Routing Logic: Which Skills Do I Need?

### Decision Tree

```
START: What are you building?

├─ ECOSYSTEM / POPULATION SIMULATION
│  ├─ Formulate dynamics → differential-equations-for-games
│  ├─ Prevent extinction/explosion → stability-analysis
│  ├─ Implement simulation → numerical-methods
│  └─ Random events? → stochastic-simulation
│
├─ PHYSICS SIMULATION
│  ├─ Formulate forces → differential-equations-for-games
│  ├─ Choose integrator → numerical-methods
│  ├─ Prevent explosions → stability-analysis
│  ├─ Multiplayer determinism? → chaos-and-sensitivity
│  └─ Real-time vs turn-based? → continuous-vs-discrete
│
├─ ECONOMY / RESOURCE SYSTEM
│  ├─ Formulate flows → differential-equations-for-games
│  ├─ Prevent inflation/deflation → stability-analysis
│  ├─ Discrete vs continuous? → continuous-vs-discrete
│  └─ Market randomness? → stochastic-simulation
│
├─ AI / CONTROL SYSTEM
│  ├─ Smooth behavior → feedback-control-theory
│  ├─ State machine analysis → state-space-modeling
│  ├─ Decision uncertainty → stochastic-simulation
│  └─ Prevent oscillation → stability-analysis
│
├─ MULTIPLAYER / DETERMINISM
│  ├─ Understand desync sources → chaos-and-sensitivity
│  ├─ Choose precision → numerical-methods
│  ├─ Discrete events? → continuous-vs-discrete
│  └─ State validation → state-space-modeling
│
└─ LOOT / RANDOMNESS SYSTEM
   ├─ Choose distributions → stochastic-simulation
   ├─ Prevent exploits → stochastic-simulation (anti-patterns)
   ├─ Pity systems → feedback-control-theory (setpoint tracking)
   └─ Long-term balance → stability-analysis
```

---

## 15+ Scenarios: Which Skills Apply?

### Scenario 1: "Rimworld-style ecosystem (wolves/deer/grass)"
**Primary:** differential-equations-for-games (Lotka-Volterra)
**Secondary:** stability-analysis (prevent extinction), numerical-methods (RK4 integration)
**Optional:** stochastic-simulation (random migration events)
**Time:** 6-10 hours

### Scenario 2: "Unity physics engine with springs/dampers"
**Primary:** differential-equations-for-games (spring-mass-damper)
**Secondary:** numerical-methods (semi-implicit Euler), stability-analysis (prevent explosion)
**Optional:** chaos-and-sensitivity (multiplayer physics)
**Time:** 5-8 hours

### Scenario 3: "EVE Online-style economy (inflation prevention)"
**Primary:** differential-equations-for-games (resource flows)
**Secondary:** stability-analysis (equilibrium analysis), continuous-vs-discrete (discrete items)
**Optional:** stochastic-simulation (market fluctuations)
**Time:** 6-9 hours

### Scenario 4: "Smooth camera follow (Uncharted-style)"
**Primary:** feedback-control-theory (PID camera)
**Secondary:** differential-equations-for-games (spring-damper alternative)
**Optional:** None (focused problem)
**Time:** 2-4 hours

### Scenario 5: "Left 4 Dead AI Director (adaptive difficulty)"
**Primary:** feedback-control-theory (intensity tracking)
**Secondary:** differential-equations-for-games (smooth intensity changes)
**Optional:** stochastic-simulation (spawn randomness)
**Time:** 4-6 hours

### Scenario 6: "Fighting game frame data analysis"
**Primary:** state-space-modeling (state transitions)
**Secondary:** None (discrete system)
**Optional:** chaos-and-sensitivity (combo sensitivity to timing)
**Time:** 3-5 hours

### Scenario 7: "RTS lockstep multiplayer (prevent desyncs)"
**Primary:** chaos-and-sensitivity (understand floating-point sensitivity)
**Secondary:** numerical-methods (fixed-point arithmetic), continuous-vs-discrete (deterministic events)
**Optional:** state-space-modeling (state validation)
**Time:** 5-8 hours

### Scenario 8: "Kerbal Space Program orbital mechanics"
**Primary:** numerical-methods (symplectic integrators for energy conservation)
**Secondary:** differential-equations-for-games (Newton's gravity), chaos-and-sensitivity (three-body problem)
**Optional:** None (focused on accuracy)
**Time:** 6-10 hours

### Scenario 9: "Diablo-style loot drops (fair randomness)"
**Primary:** stochastic-simulation (probability distributions, pity systems)
**Secondary:** None (focused problem)
**Optional:** feedback-control-theory (pity timer as PID)
**Time:** 3-5 hours

### Scenario 10: "Cloth simulation (Unity/Unreal)"
**Primary:** numerical-methods (Verlet integration, constraints)
**Secondary:** differential-equations-for-games (spring forces), stability-analysis (prevent blow-up)
**Optional:** None (standard cloth physics)
**Time:** 5-8 hours

### Scenario 11: "Turn-based tactical RPG"
**Primary:** continuous-vs-discrete (choose discrete model)
**Secondary:** state-space-modeling (action resolution), stochastic-simulation (hit/crit rolls)
**Optional:** None (discrete system)
**Time:** 4-6 hours

### Scenario 12: "Procedural weather system (dynamic)"
**Primary:** differential-equations-for-games (smooth weather transitions)
**Secondary:** stochastic-simulation (random weather events), chaos-and-sensitivity (Lorenz attractor)
**Optional:** numerical-methods (weather integration)
**Time:** 5-8 hours

### Scenario 13: "Path of Exile economy balance"
**Primary:** stability-analysis (currency sink/faucet equilibrium)
**Secondary:** differential-equations-for-games (flow equations), stochastic-simulation (drop rates)
**Optional:** continuous-vs-discrete (discrete items, continuous flows)
**Time:** 6-9 hours

### Scenario 14: "Racing game suspension (realistic feel)"
**Primary:** differential-equations-for-games (spring-damper suspension)
**Secondary:** feedback-control-theory (PID for stability), numerical-methods (fast integration)
**Optional:** stability-analysis (prevent oscillation)
**Time:** 5-8 hours

### Scenario 15: "Puzzle game solvability checker"
**Primary:** state-space-modeling (reachability analysis)
**Secondary:** None (graph search problem)
**Optional:** chaos-and-sensitivity (sensitivity to initial state)
**Time:** 3-5 hours

---

## Multi-Skill Workflows

### Workflow 1: Ecosystem Simulation (Rimworld, Dwarf Fortress)
**Skills in sequence:**
1. **differential-equations-for-games** (2.5-3.5h) - Formulate Lotka-Volterra
2. **stability-analysis** (3-4h) - Find equilibrium, prevent extinction
3. **numerical-methods** (2.5-3.5h) - Implement RK4 integration
4. **stochastic-simulation** (2-3h) - Add random migration/disease

**Total time:** 10-14 hours
**Result:** Stable ecosystem with predictable long-term behavior

### Workflow 2: Physics Engine (Unity, Unreal, custom)
**Skills in sequence:**
1. **differential-equations-for-games** (2.5-3.5h) - Newton's laws, spring-damper
2. **numerical-methods** (2.5-3.5h) - Semi-implicit Euler, Verlet
3. **stability-analysis** (3-4h) - Prevent ragdoll explosion
4. **chaos-and-sensitivity** (2-3h) - Multiplayer determinism (if needed)

**Total time:** 10-14 hours (12-17 with multiplayer)
**Result:** Stable, deterministic physics at 60 FPS

### Workflow 3: Economy System (EVE, Path of Exile)
**Skills in sequence:**
1. **differential-equations-for-games** (2.5-3.5h) - Resource flow equations
2. **stability-analysis** (3-4h) - Equilibrium analysis, inflation prevention
3. **continuous-vs-discrete** (2-2.5h) - Discrete items, continuous flows
4. **stochastic-simulation** (2-3h) - Market fluctuations, drop rates

**Total time:** 10-13 hours
**Result:** Self-regulating economy with predictable equilibrium

### Workflow 4: AI Control System (Camera, Difficulty, NPC)
**Skills in sequence:**
1. **feedback-control-theory** (2-3h) - PID controller design
2. **differential-equations-for-games** (1-2h) - Alternative spring-damper (optional)
3. **stability-analysis** (1-2h) - Prevent oscillation (optional)

**Total time:** 2-7 hours (depending on complexity)
**Result:** Smooth, adaptive AI behavior

### Workflow 5: Multiplayer Determinism (RTS, Fighting Games)
**Skills in sequence:**
1. **chaos-and-sensitivity** (2-3h) - Understand desync sources
2. **numerical-methods** (2.5-3.5h) - Fixed-point arithmetic
3. **state-space-modeling** (2.5-3.5h) - State validation
4. **continuous-vs-discrete** (2-2.5h) - Deterministic event ordering

**Total time:** 9-12.5 hours
**Result:** Zero desyncs in multiplayer

---

## Integration with Other Skillpacks

### Primary Integration: bravos/simulation-tactics

**simulation-tactics = HOW to implement**
**simulation-foundations = WHY it works mathematically**

Cross-references TO simulation-foundations:
- physics-simulation-patterns → differential-equations + numerical-methods (math behind fixed timestep)
- ecosystem-simulation → stability-analysis (Lotka-Volterra mathematics)
- debugging-simulation-chaos → chaos-and-sensitivity (determinism theory)
- performance-optimization → numerical-methods (integration accuracy vs cost)

Cross-references FROM simulation-foundations:
- differential-equations → simulation-tactics for implementation patterns
- stability-analysis → ecosystem-simulation for practical code
- numerical-methods → physics-simulation for engine integration

### Secondary Integration: bravos/systems-as-experience

Cross-references:
- state-space-modeling → strategic-depth-from-systems (build space mathematics)
- stochastic-simulation → player-driven-narratives (procedural event probabilities)

---

## Quick Start Guides

### Quick Start 1: Stable Ecosystem (4 hours)
**Goal:** Predator-prey system that doesn't crash

**Steps:**
1. Read differential-equations Quick Start (1h)
2. Formulate Lotka-Volterra equations (0.5h)
3. Read stability-analysis Quick Start (1h)
4. Find equilibrium, check eigenvalues (1h)
5. Implement with semi-implicit Euler (0.5h)

**Result:** Ecosystem oscillates stably, no extinction

### Quick Start 2: Smooth Camera (2 hours)
**Goal:** Uncharted-style camera follow

**Steps:**
1. Read feedback-control Quick Start (0.5h)
2. Implement PID controller (1h)
3. Tune using Ziegler-Nichols (0.5h)

**Result:** Smooth camera with no overshoot

### Quick Start 3: Fair Loot System (3 hours)
**Goal:** Diablo-style loot with pity timer

**Steps:**
1. Read stochastic-simulation Quick Start (1h)
2. Choose distribution (Bernoulli + pity) (0.5h)
3. Implement and test fairness (1.5h)

**Result:** Loot system with guaranteed legendary every 90 pulls

---

## Common Pitfalls

### Pitfall 1: Skipping Stability Analysis
**Problem:** Shipping systems without analyzing equilibrium

**Symptom:** Game works fine for 10 hours, crashes at hour 100 (population explosion)

**Fix:** ALWAYS use stability-analysis for systems with feedback loops

### Pitfall 2: Wrong Integrator Choice
**Problem:** Using explicit Euler for stiff systems

**Symptom:** Physics explodes at high framerates or with strong springs

**Fix:** Use numerical-methods decision framework (semi-implicit for physics)

### Pitfall 3: Assuming Determinism
**Problem:** Identical code on two machines, assuming identical results

**Symptom:** Multiplayer desyncs after 5+ minutes

**Fix:** Read chaos-and-sensitivity, understand floating-point divergence

### Pitfall 4: Naive Randomness
**Problem:** Using uniform random for everything

**Symptom:** Players exploit patterns, loot feels unfair

**Fix:** Use stochastic-simulation to choose proper distributions

### Pitfall 5: Continuous for Discrete Problems
**Problem:** Using ODEs for turn-based combat

**Symptom:** 100× CPU overhead for no benefit

**Fix:** Read continuous-vs-discrete, use difference equations

---

## Success Criteria

### Your simulation uses foundations successfully when:

**Predictability:**
- [ ] Can predict long-term behavior analytically
- [ ] Equilibrium points known before shipping
- [ ] Stability verified mathematically

**Performance:**
- [ ] Integration method chosen deliberately (not default Euler)
- [ ] Real-time constraints met (60 FPS)
- [ ] Appropriate model type (continuous/discrete)

**Robustness:**
- [ ] No catastrophic failures (extinctions, explosions)
- [ ] Handles edge cases (zero populations, high framerates)
- [ ] Multiplayer determinism verified (if needed)

**Maintainability:**
- [ ] Parameters have physical meaning (not magic numbers)
- [ ] Behavior understood mathematically
- [ ] Debugging systematic (not trial-and-error)

---

## Conclusion

**The Golden Rule:**
> "Formulate first, tune second. Math predicts, empiricism confirms."

### When You're Done with This Pack

You should be able to: formulate systems as differential equations, analyze stability before shipping, choose correct numerical integrators, design PID controllers, understand deterministic chaos, apply proper probability distributions, prevent catastrophic failures, and debug simulations systematically.

### Next Steps

1. **Identify your simulation type** (use routing logic above)
2. **Read foundational skill** (usually differential-equations-for-games)
3. **Apply skills in sequence** (use workflows above)
4. **Validate mathematically** (stability analysis, testing)
5. **Integrate with simulation-tactics** (implementation patterns)

---

## Simulation Foundations Specialist Skills Catalog

After routing, load the appropriate specialist skill for detailed guidance:

1. [differential-equations-for-games.md](differential-equations-for-games.md) - ODEs for continuous dynamics, Lotka-Volterra ecosystems, spring-damper systems, resource flows, Newton's laws
2. [state-space-modeling.md](state-space-modeling.md) - State representation, reachability analysis, fighting game frame data, RTS tech trees, puzzle solvability
3. [stability-analysis.md](stability-analysis.md) - Equilibrium points, eigenvalue analysis, Lyapunov functions, preventing extinction/explosion/inflation
4. [feedback-control-theory.md](feedback-control-theory.md) - PID controllers, camera smoothing, AI pursuit, dynamic difficulty, disturbance rejection
5. [numerical-methods.md](numerical-methods.md) - Euler, Runge-Kutta, symplectic integrators, fixed-point arithmetic, integration stability
6. [continuous-vs-discrete.md](continuous-vs-discrete.md) - Choosing model type, continuous ODEs vs discrete events, turn-based vs real-time
7. [chaos-and-sensitivity.md](chaos-and-sensitivity.md) - Butterfly effect, Lyapunov exponents, deterministic chaos, multiplayer desyncs, floating-point sensitivity
8. [stochastic-simulation.md](stochastic-simulation.md) - Probability distributions, Monte Carlo, stochastic differential equations, loot systems, randomness patterns

---

**Go build simulations with mathematical rigor.**
