---
name: using-simulation-tactics
description: Router skill - analyze requirements and direct to appropriate tactics
---

# Using Simulation Tactics: The Router Meta-Skill

## Description

This is the PRIMARY ROUTER META-SKILL for the simulation-tactics skillpack. It teaches you how to:

1. **Analyze simulation requirements** - Understand what the user actually needs
2. **Route to appropriate skills** - Determine which of the 10 core skills apply
3. **Apply skills in correct order** - Use the optimal workflow for the situation
4. **Combine multiple skills** - Handle complex scenarios requiring several simulation types

This skill does NOT teach simulation implementation details. It teaches DECISION MAKING: which skill to use, when, and why.

## When to Use This Meta-Skill

Use this meta-skill when:
- Starting ANY simulation-related game development task
- User asks about simulation but unclear which type
- Facing complex scenarios requiring multiple simulation types
- Need to determine implementation order for multi-system games
- Debugging simulation issues and unclear where to start
- Planning architecture for simulation-heavy games

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-simulation-tactics/SKILL.md`

Reference sheets like `physics-simulation-patterns.md` are at:
  `skills/using-simulation-tactics/physics-simulation-patterns.md`

NOT at:
  `skills/physics-simulation-patterns.md` ← WRONG PATH

---

## The 10 Core Skills

Before routing, understand what each skill provides:

### 1. simulation-vs-faking (FOUNDATIONAL)
**What it teaches**: The fundamental trade-off between full simulation and approximation/faking
**When to route**: ALWAYS FIRST - determines if you even need simulation
**Key question**: "Do I simulate this, fake it, or use a hybrid approach?"

### 2. physics-simulation-patterns
**What it teaches**: Rigid bodies, vehicles, cloth, fluids, integration methods
**When to route**: Need realistic physics for vehicles, ragdolls, destructibles, or fluid dynamics
**Key question**: "Does this need real-time physics simulation?"

### 3. ai-and-agent-simulation
**What it teaches**: FSM, behavior trees, utility AI, GOAP, agent behaviors
**When to route**: Need intelligent agent behavior (enemies, NPCs, units)
**Key question**: "Do agents need to make decisions and act autonomously?"

### 4. traffic-and-pathfinding
**What it teaches**: A*, navmesh, flow fields, traffic simulation, congestion
**When to route**: Need agents to navigate environments or simulate traffic
**Key question**: "Do entities need to find paths or simulate traffic flow?"

### 5. economic-simulation-patterns
**What it teaches**: Supply/demand, markets, trade networks, price discovery
**When to route**: Need economic systems (trading, markets, resources)
**Key question**: "Does the game involve trade, economy, or resource markets?"

### 6. ecosystem-simulation
**What it teaches**: Predator-prey dynamics, food chains, population control
**When to route**: Need living ecosystems with wildlife populations
**Key question**: "Do I need animals/plants that breed, eat, and die naturally?"

### 7. crowd-simulation
**What it teaches**: Boids, formations, social forces, LOD for crowds
**When to route**: Need large groups moving together (crowds, flocks, armies)
**Key question**: "Do I need many entities moving as a coordinated group?"

### 8. weather-and-time
**What it teaches**: Day/night cycles, weather systems, seasonal effects
**When to route**: Need atmospheric effects or time-based gameplay
**Key question**: "Does the game need time progression or weather?"

### 9. performance-optimization-for-sims
**What it teaches**: Profiling, spatial partitioning, LOD, time-slicing, caching
**When to route**: Performance problems with existing simulation
**Key question**: "Is my simulation too slow?"

### 10. debugging-simulation-chaos
**What it teaches**: Systematic debugging, desync detection, determinism, chaos prevention
**When to route**: Simulation behaves incorrectly, chaotically, or unpredictably
**Key question**: "Is my simulation broken, desyncing, or chaotic?"

---

## CORE ROUTING FRAMEWORK

### The Decision Tree

Follow this decision tree for ALL simulation tasks:

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: ALWAYS START HERE                                   │
│ ═══════════════════════════════════════════════════════════ │
│ Route to: simulation-vs-faking                              │
│                                                              │
│ Questions to ask:                                            │
│ • Do I need to simulate this at all?                        │
│ • What level of detail is required?                         │
│ • What can I fake or approximate?                           │
│ • Where is the player's attention focused?                  │
│                                                              │
│ This prevents the #1 mistake: over-engineering systems     │
│ that could be faked.                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: ROUTE TO SPECIFIC SIMULATION TYPE(S)                │
│ ═══════════════════════════════════════════════════════════ │
│ Identify which simulation domains apply:                    │
│                                                              │
│ Physics domain → physics-simulation-patterns                │
│ AI domain → ai-and-agent-simulation                         │
│ Pathfinding domain → traffic-and-pathfinding                │
│ Economy domain → economic-simulation-patterns               │
│ Ecosystem domain → ecosystem-simulation                     │
│ Crowds domain → crowd-simulation                            │
│ Atmosphere domain → weather-and-time                        │
│                                                              │
│ Multiple domains? Route to ALL applicable skills.           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: IF PERFORMANCE ISSUES ARISE                         │
│ ═══════════════════════════════════════════════════════════ │
│ Route to: performance-optimization-for-sims                 │
│                                                              │
│ Triggers:                                                    │
│ • Frame rate drops below 60 FPS                             │
│ • Profiler shows simulation bottleneck                      │
│ • Agent count causes slowdown                               │
│ • Simulation gets expensive at scale                        │
│                                                              │
│ WARNING: Don't route here prematurely!                      │
│ Premature optimization wastes time.                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: IF BUGS/CHAOS OCCUR                                 │
│ ═══════════════════════════════════════════════════════════ │
│ Route to: debugging-simulation-chaos                        │
│                                                              │
│ Triggers:                                                    │
│ • Simulation behaves chaotically/unpredictably              │
│ • Multiplayer desyncs                                       │
│ • Physics explosions or NaN values                          │
│ • Agents stuck or behaving erratically                      │
│ • Systems producing nonsensical results                     │
│                                                              │
│ This is a REACTIVE skill - only use when broken.            │
└─────────────────────────────────────────────────────────────┘
```

### Key Routing Principles

**Principle 1: simulation-vs-faking is ALWAYS step 1**
- Even if you "know" you need simulation, validate this assumption
- Prevents 90% of over-engineering disasters
- Takes 5 minutes, saves hours of wasted work

**Principle 2: Multiple domains are common**
- Most games need 2-4 simulation types
- Route to ALL applicable skills
- Order matters (see [multi-skill-workflows.md](multi-skill-workflows.md))

**Principle 3: Optimization comes AFTER implementation**
- Don't route to performance-optimization-for-sims until you have a working simulation
- Profile first, optimize later
- Premature optimization is the root of all evil

**Principle 4: Debugging is reactive, not proactive**
- Only route to debugging-simulation-chaos when something is broken
- Don't use it as a preventative measure
- Fix the bug, THEN refactor to prevent recurrence

---

## QUICK REFERENCE TABLE

| User Need | Primary Skill | Secondary Skills | Also Consider |
|-----------|---------------|------------------|---------------|
| **Vehicle physics** | physics-simulation-patterns | - | performance-optimization (if many vehicles) |
| **City traffic** | traffic-and-pathfinding | simulation-vs-faking | performance-optimization (scale to 10k) |
| **NPC AI** | ai-and-agent-simulation | simulation-vs-faking | traffic-and-pathfinding (if NPCs move) |
| **RTS units** | ai-and-agent-simulation, traffic-and-pathfinding | crowd-simulation (formations) | performance-optimization (1000+ units) |
| **Trading system** | economic-simulation-patterns | simulation-vs-faking | ai-and-agent-simulation (NPC traders) |
| **Wildlife/hunting** | ecosystem-simulation | ai-and-agent-simulation | simulation-vs-faking (detail level) |
| **Crowds** | crowd-simulation | simulation-vs-faking | performance-optimization (scale) |
| **Day/night** | weather-and-time | simulation-vs-faking | - |
| **Weather effects** | weather-and-time | physics-simulation-patterns (wind) | - |
| **Pathfinding** | traffic-and-pathfinding | simulation-vs-faking | performance-optimization (many agents) |
| **Flocking birds** | crowd-simulation | simulation-vs-faking | performance-optimization (LOD) |
| **Ragdolls** | physics-simulation-patterns | - | debugging-simulation-chaos (stability) |
| **Performance issue** | performance-optimization-for-sims | (original implementation skill) | debugging-simulation-chaos (if bug) |
| **Physics explodes** | debugging-simulation-chaos | physics-simulation-patterns | - |
| **Ecosystem collapse** | debugging-simulation-chaos | ecosystem-simulation | - |
| **Multiplayer desync** | debugging-simulation-chaos | (any affected skills) | - |

---

## DECISION FLOWCHART

Use this flowchart for quick routing decisions:

```
START: User describes simulation need
    ↓
[Is this DEFINITELY about simulation?]
    ├─ No → Don't use simulation-tactics at all
    └─ Yes → Continue
        ↓
[Route to: simulation-vs-faking]
    "Do I simulate, fake, or hybrid?"
        ↓
[Identify domain(s)]
    ├─ Physics? → physics-simulation-patterns
    ├─ AI/Agents? → ai-and-agent-simulation
    ├─ Pathfinding? → traffic-and-pathfinding
    ├─ Economy? → economic-simulation-patterns
    ├─ Ecosystem? → ecosystem-simulation
    ├─ Crowds? → crowd-simulation
    └─ Weather/Time? → weather-and-time
        ↓
[Is simulation ALREADY implemented?]
    ├─ No → Use identified skill(s) to implement
    └─ Yes → Continue
        ↓
[Is there a PERFORMANCE problem?]
    ├─ Yes → performance-optimization-for-sims
    └─ No → Continue
        ↓
[Is there a BUG/CHAOS problem?]
    ├─ Yes → debugging-simulation-chaos
    └─ No → Implementation complete!
```

---

## COMMON ROUTING MISTAKES

These are the mistakes that waste the most time. Learn to recognize them.

### Mistake 1: Skipping simulation-vs-faking

**Symptom**: Over-engineered simulation that could have been faked

**Example**:
- Building full ecosystem for background birds that are never scrutinized
- Simulating NPC hunger/sleep when player never notices
- Full traffic simulation for distant cars player can't interact with

**Fix**: ALWAYS route to simulation-vs-faking first. Ask "Will player notice if I fake this?"

**Cost of mistake**: Weeks of wasted work, ongoing performance burden

### Mistake 2: Premature optimization

**Symptom**: Routing to performance-optimization-for-sims before implementation is complete

**Example**:
- Implementing LOD systems before having working simulation
- Using spatial partitioning before knowing if it's needed
- Caching pathfinding before pathfinding exists

**Fix**: Profile first, optimize later. Only route to performance-optimization-for-sims when:
- You have working simulation
- You have measured performance problem
- Profiler shows bottleneck

**Cost of mistake**: Wasted time optimizing code that might change, or optimizing the wrong thing

### Mistake 3: Not debugging systematically

**Symptom**: Trying to fix bugs by changing random things, routing to implementation skills instead of debugging-simulation-chaos

**Example**:
- "Physics explodes, let me try different integration method" (should debug first)
- "Ecosystem collapses, let me add more food" (should debug why it collapses)
- "Pathfinding breaks, let me rewrite the algorithm" (should debug the existing code)

**Fix**: When simulation is broken, ALWAYS route to debugging-simulation-chaos first. Identify root cause before attempting fixes.

**Cost of mistake**: Bug persists, or you "fix" symptom without addressing cause

### Mistake 4: Wrong skill for the domain

**Symptom**: Using ai-and-agent-simulation when you need traffic-and-pathfinding, etc.

**Example**:
- Using ai-and-agent-simulation for pathfinding (use traffic-and-pathfinding instead)
- Using physics-simulation-patterns for kinematic movement (use ai-and-agent-simulation)
- Using crowd-simulation for trading (use economic-simulation-patterns)

**Fix**: Understand what each skill covers. Pathfinding is NOT AI. Physics is NOT movement. Crowds are NOT flocking AI.

**Cost of mistake**: Learning wrong techniques for your problem

### Mistake 5: Implementing in wrong order

**Symptom**: Building dependent system before foundation

**Example**:
- Implementing AI behaviors before pathfinding exists (AI can't move)
- Building economy before resource sources exist (nothing to trade)
- Adding weather effects before day/night cycle (no time progression)

**Fix**: Follow the dependency order in multi-skill workflows. Foundation first, then dependent systems.

**Cost of mistake**: Rework when foundation changes breaks dependent systems

### Mistake 6: Ignoring multiplayer determinism

**Symptom**: Building single-player simulation without considering multiplayer needs

**Example**:
- Using floating-point physics for multiplayer game (desyncs)
- Random number generation without shared seed (desyncs)
- Iterating unordered collections (desyncs)

**Fix**: If multiplayer is planned, route to debugging-simulation-chaos early to learn determinism requirements.

**Cost of mistake**: Complete rewrite to fix desyncs

### Mistake 7: Over-combining skills

**Symptom**: Trying to use every skill when only 1-2 are needed

**Example**:
- Simple puzzle game doesn't need ecosystem-simulation
- Turn-based game doesn't need performance-optimization-for-sims
- Static world doesn't need weather-and-time

**Fix**: Route to ONLY the skills you actually need. More skills = more complexity.

**Cost of mistake**: Wasted time learning and implementing unnecessary systems

---

## Additional Guidance

For detailed examples and workflows, see:

- [routing-scenarios.md](routing-scenarios.md) - 20 concrete routing examples
- [multi-skill-workflows.md](multi-skill-workflows.md) - 8 game genre workflows (RTS, Survival, City Builder, etc.)
- [expert-routing-guide.md](expert-routing-guide.md) - Tips, checklists, self-checks, edge cases

---

## Simulation Tactics Specialist Skills Catalog

After routing, load the appropriate specialist skill for detailed guidance:

1. [simulation-vs-faking.md](simulation-vs-faking.md) - FOUNDATIONAL: Trade-off between full simulation and approximation/faking
2. [physics-simulation-patterns.md](physics-simulation-patterns.md) - Rigid bodies, vehicles, cloth, fluids, integration methods
3. [ai-and-agent-simulation.md](ai-and-agent-simulation.md) - FSM, behavior trees, utility AI, GOAP, agent behaviors
4. [traffic-and-pathfinding.md](traffic-and-pathfinding.md) - A*, navmesh, flow fields, traffic simulation, congestion
5. [economic-simulation-patterns.md](economic-simulation-patterns.md) - Supply/demand, markets, trade networks, price discovery
6. [ecosystem-simulation.md](ecosystem-simulation.md) - Predator-prey dynamics, food chains, population control
7. [crowd-simulation.md](crowd-simulation.md) - Boids, formations, social forces, LOD for crowds
8. [weather-and-time.md](weather-and-time.md) - Day/night cycles, weather systems, seasonal effects
9. [performance-optimization-for-sims.md](performance-optimization-for-sims.md) - Profiling, spatial partitioning, LOD, time-slicing
10. [debugging-simulation-chaos.md](debugging-simulation-chaos.md) - Systematic debugging, desync detection, determinism

Now route confidently to the specific skills you need!
