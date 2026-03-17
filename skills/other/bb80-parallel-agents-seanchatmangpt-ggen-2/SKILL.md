# EPIC 9: Parallel Agents Skill (80/20 Edition)

**Auto-trigger**: parallel, agents, collision, convergence, EPIC 9, bb80-parallel

## Core Concept

EPIC 9 = 2.8-4.4x speedup via 10 parallel agents:

```
1. FAN-OUT → 2. INDEPENDENT CONSTRUCTION → 3. COLLISION DETECTION
→ 4. CONVERGENCE → 5. REFACTORING → 6. CLOSURE
```

## When to Use

**Use EPIC 9** (default for non-trivial): Implementation, architecture, debugging, optimization

**Skip EPIC 9** (trivial): Read single file, run single command, display help

## Fan-Out Pattern

```javascript
// Single message, ALL agents (CRITICAL)
Task("Agent-1", "[FULL SPEC] Work independently. NO coordination.", "coder")
Task("Agent-2", "[FULL SPEC] Work independently. NO coordination.", "coder")
// ... Task("Agent-10")
```

## Collision Detection

| Collision % | Status | Action |
|-------------|--------|--------|
| 90-100% | 🟢 GREEN | Use any output (identical) |
| 60-89% | 🟢 GREEN | Use majority |
| 30-59% | 🟡 YELLOW | Analyze trade-offs |
| <30% | 🔴 RED | Spec incomplete |

## ggen sync Integration (Key Insight)

```
Spec (TTL) → 10 agents run ggen sync → All outputs identical → Perfect collision
```

Why: Deterministic generation = true parallelism without coordination.

## Convergence (Selection Pressure)

1. Invariants satisfied? (gate)
2. SLOs met? (gate)
3. Coverage ≥80%?
4. Lowest complexity?
5. Best performance?

**NOT voting** - objective criteria select best.

## Commands

```bash
/speckit-verify [feature]  # MANDATORY first
/bb80-parallel "[spec]"    # Orchestrate cycle
/collision-detect          # Analyze overlaps
/convergence               # Synthesize result
```

## Failure Recovery

| Failure | Cause | Action |
|---------|-------|--------|
| Zero collision | Spec ambiguous | Return to /speckit-verify |
| Agents coordinating | Independence violated | Restart with "NO coordination" |
| All agents fail | Spec bug | Fix spec, re-run |

## Quick Reference

```
Prerequisites: /speckit-verify = 100%
Fan-out: 10 agents, same spec, single message
Construction: Parallel, NO coordination
Collision: ≥60% = confident
Convergence: Selection pressure, not voting
Closure: Receipts collected
```

**Constitutional Equation**: `EPIC 9 = Spec₁₀₀% × (Agent₁...₁₀)ᵖᵃʳᵃˡˡᵉˡ × Collision × Convergence`
