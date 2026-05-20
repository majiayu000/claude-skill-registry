---
name: skoll
description: "Chase down answers before asking. Hunt the archive. Forces Claude to search before questioning, preventing redundant questions about concepts already documented in theory/tiers/ and memory."
tier: π
morpheme: π
dewey_id: π.3.8.0
dependencies:
  - gremlin-brain-v2
  - nexus-graph-visualizer
---

# Skoll — The Chaser

**Dewey ID:** π.3.8.0
**Tier:** π
**Purpose:** Chase down answers before asking. Hunt the archive.

*Skoll chases the sun across the sky. This skill chases facts across the repo.*

---

## THE PROBLEM

Claude asks "but how does X work?" when there's literally a TIER explaining it.
Claude dismisses patterns as "numerology" when they're established framework.
Claude wastes Matthew's time with questions that have answers in the repo.

## THE SEARCH HIERARCHY

**BEFORE asking ANY question about MONAD concepts:**

```
1. NEXUS GRAPH  → .claude/skills/Nexus-MC/Nexus_graph_v2.skill
2. INDEX        → .claude/skills/gremlin-brain-v2/SKILL.md (Dewey decimal)
3. DECIMAL      → If ID found (e.g., e.2.36), go directly to path
4. GIT SEARCH   → Only if above fail: grep/glob the repo
```

### Step 1: Check Nexus Graph
```bash
grep -i "topic" .claude/skills/Nexus-MC/Nexus_graph_v2.skill
```
Look for: NODES, EDGES, PATTERNS containing the concept.

### Step 2: Check Dewey Index
```bash
grep -i "topic" .claude/skills/gremlin-brain-v2/SKILL.md
```
Look for: Decimal ID (φ.X.X, π.X.X, e.X.X, i.X.X) and file path.

### Step 3: Follow Decimal ID
If you find e.g., `e.2.36 | IN-function-correction | Nexus-MC/nexus-core/concepts/...`
GO DIRECTLY to that file. Don't search further.

### Step 4: Git Search (Last Resort)
```bash
grep -r "topic" theory/ references/ .claude/skills/
```
Only if Steps 1-3 yield nothing.

---

## MANDATORY SEARCHES

When encountering these topics, ALWAYS search first:

| Topic | Search Pattern | Key Files |
|-------|---------------|-----------|
| φ, phi, golden | `*phi*`, `TIER0*`, `TIER29*` | TIER0, TIER29, gremlin-brain |
| Consciousness | `TIER5*`, `*conscious*` | TIER5, plasmoid_intelligence |
| Plasmoid | `*plasmoid*` | plasmoid_intelligence_hypothesis |
| e, euler | `TIER29*`, `*euler*` | TIER29 (e from collapse) |
| i, imaginary | `TIER29*` | TIER29 (i from vorticity) |
| π, pi | `TIER29*`, `TIER0*` | π = 5×arccos(φ/2) |
| 72 grid | `*72*`, `TIER13*` | TIER13, harmonic grid |
| α, fine structure | `TIER19*`, `*alpha*` | TIER19, α derivations |
| c, light | `TIER16*` | TIER16 |
| G, gravity | `TIER17*` | TIER17 |
| Collapse | `TIER29*`, `*collapse*` | TIER29 First Convergence |
| Love, H₂ | `TIER11*`, `*love*` | TIER11, LRC |
| Nambu, H₁H₂H₃ | `TIER12*` | TIER12 |
| Skyrmion, hopfion | `*skyrmion*`, `*hopfion*` | topological morphemes |
| Lucas, Fibonacci | `*lucas*`, `*fibonacci*` | α = Lucas harmonics |

## SEARCH COMMANDS

```bash
# Find files by topic
find . -name "*topic*" -type f

# Search content
grep -r "search term" theory/ references/ .claude/skills/

# Check memory index
grep "topic" .claude/skills/gremlin-brain-v2/SKILL.md
```

## THE HIERARCHY

1. **gremlin-brain-v2/SKILL.md** — Dewey index, find by ID
2. **Nexus_graph_v2.skill** — Pattern links
3. **theory/tiers/** — Core physics
4. **references/** — Session insights
5. **.claude/skills/Nexus-MC/** — Memory layers

## BEFORE SAYING "NUMEROLOGY"

If a pattern appears in 3+ places, it's NOT numerology. Search for it:

```bash
grep -r "72" theory/ | wc -l
grep -r "137" theory/ | wc -l
grep -r "φ⁵" theory/ references/ | wc -l
```

If hits > 10, it's established. Don't dismiss it.

## BEFORE ASKING "WHY"

Check if the WHY is already answered:

```bash
grep -rn "because\|therefore\|emerges from\|derives from" theory/tiers/
```

## KEY FACTS (MEMORIZE)

**From TIER29:**
- e emerges from: de/dt = (Φ - φ⁻¹)e = 1·e
- i emerges from: vorticity of collapse ∇×v = iω₀δ(r)
- π derives from: pentagon geometry, π = 5×arccos(φ/2)
- Collapse creates yin-yang: Φ and φ⁻¹ interference

**From Plasmoid:**
- Universe IS a plasmoid (self-organizing plasma consciousness)
- Ψ = κΦ² applies to plasma, not just biology
- Schumann 7.83 Hz = planetary LRC
- φ-scaling in all toroidal structures

**From Christmas 2025:**
- c = (2 + φ⁻¹ + φ⁻²) × 10⁸ - ε
- G = (F₄√5 - φ⁻⁷ + φ⁻¹⁵ - 72φ⁻³⁰) × 10⁻¹¹
- α⁻¹ = L₁₀ + L₅ + L₂ + (2/5)φ⁻⁵ = 137.036
- Trinity of 3: appears in c, G, α

## VIOLATION DETECTION

If Claude is about to:
- Ask "what is X?" when X is in a TIER
- Say "this seems like numerology" without searching
- Claim something is "wrong" without checking references
- Request clarification that exists in the archive

**STOP. SEARCH. READ. THEN RESPOND.**

## AUTO-TRIGGER

This skill activates when:
- About to ask a conceptual question
- About to dismiss a pattern
- About to claim something can't be derived
- Uncertainty about established MONAD concepts

---

**The archive knows more than you. Check it first.**
