---
name: wardley-map
description: "Create or update a Wardley Map of the value chain. Maps user needs, components, evolution stages, and strategic gameplay."
---

# Wardley Mapping

Visualize your value chain and make strategic decisions. Source: Simon Wardley.

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
Update canvas/landscape.yml with components, evolution stages, movements, and gameplay options.

## Connection to Other Frameworks
- Evolution stage maps to Cynefin domain (use `/cynefin-classify`)
- User needs at top map to OST outcomes (use `/ost-builder`)
- Strategic gameplay informs GIST goals (use `/gist-plan`)
