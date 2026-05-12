---
name: wardley-map
description: "Create or update a Wardley Map of the value chain. Maps user needs, components, evolution stages, and strategic gameplay."
instruction_budget: 10
---

# Wardley Mapping

Visualize your value chain and make strategic decisions. Source: Simon Wardley.

## Preflight: Read target canvas file(s) before any Write/Edit

**Hard rule.** Before issuing `Write` or `Edit` against any `.claude/canvas/*.yml`, use the **Read tool** on that file in this session. Claude Code's Read-before-Write check requires the `Read` tool specifically — `cat`/`head`/`grep` via Bash do NOT satisfy it. Reaching for `Write` first produces a tool error and forces a remedial Read, which costs ~14k tokens of pure ceremony at typical canvas sizes (anti-pattern #7 instance #5, 2026-05-09).

If this skill writes to multiple canvas files, Read each one first. If unsure whether a write is needed, Read first anyway — Read is cheap, the recovery loop is not.

See `CLAUDE.md` *Canvas writes — Read before Write* for the canonical rule.

## Mapping Process

### 1. Identify the User
Who is the map for? What scope?

### 2. Identify User Needs
What does the user need? Place at the top of the map (most visible).

### 3. Map the Value Chain
What components are needed to serve those needs? Draw dependency lines top-down.

### 4. Assess Evolution Stage
For each component:
| Stage | Characteristics | Strategy |
|-------|----------------|----------|
| **Genesis** | Novel, uncertain, high failure rate | Explore, experiment, small teams |
| **Custom** | Better understood, bespoke builds | Build or partner, reduce uncertainty |
| **Product** | Standardized, feature competition | Buy or build competitively |
| **Commodity** | Utility, cost competition | Consume as service, don't differentiate here |

### 5. Add Movement
Mark components that are evolving (arrow pointing right). All components evolve over time.

### 6. Identify Patterns
- Components in Genesis = Complex domain (Cynefin) -> probe
- Components in Commodity = Clear domain -> best practice
- Evolution mismatch = waste (building custom what you should buy as commodity)

### 7. Apply Gameplay
Strategic options based on the map:
- Open source: Accelerate commoditization
- ILC: Innovate -> Leverage -> Commoditize
- Ecosystem: Build platform, commoditize lower layers
- Tower and moat: Invest in defensibility

## Output
Update .claude/canvas/landscape.yml with components, evolution stages, movements, and gameplay options.

## Decision Log (MANDATORY per G-P4)
**APPEND** a `### Wardley Map Assessment` entry to `.claude/harness/decision-log.md` with: components mapped, evolution stages, strategic gameplay identified, recommendations.

## Connection to Other Frameworks
- Evolution stage maps to Cynefin domain (use `/mycelium:cynefin-classify`)
- User needs at top map to OST outcomes (use `/mycelium:ost-builder`)
- Strategic gameplay informs GIST goals (use `/mycelium:gist-plan`)
