# Xparcel Network Explainer Skill

---
name: xparcel-network-explainer
description: Visualize and explain Xparcel package journeys through FirstMile's National and Select networks using Google Maps MCP tools. Creates accurate facility maps, routing visualizations, and network education materials for sales and customer success.
triggers:
  - "network map"
  - "package journey"
  - "Xparcel routing"
  - "facility locations"
  - "zone skip"
  - "Select network"
  - "National network"
  - "transit visualization"
  - "hub locations"
  - "injection points"
---

## Purpose

Transform abstract shipping network concepts into concrete, visual explanations that help prospects and customers understand FirstMile's competitive advantage through:
1. **Accurate facility mapping** with real coordinates
2. **Package journey visualization** from origin to destination
3. **Zone-skip economics** showing cost/time savings
4. **Network comparison** (Select vs National routing)

## MCP Tools Required

| Tool | Server | Use Case |
|------|--------|----------|
| `search_places` | google-maps-grounding | Find facility addresses |
| `compute_routes` | google-maps-grounding | Calculate transit paths |
| `maps_geocode` | google-maps-community | Convert addresses to coordinates |
| `maps_directions` | google-maps-community | Step-by-step routing |
| `maps_distance_matrix` | google-maps-community | Multi-point zone analysis |

## Workflow

### 1. Gather Context
- Customer origin location (fulfillment center, warehouse)
- Primary destination regions (top states/zips from PLD)
- Service level requirements (Ground, Expedited, Priority)
- Current carrier for comparison baseline

### 2. Map the Journey
```
ORIGIN (Customer FC)
    ↓
FIRSTMILE INTAKE (Nearest hub)
    ↓
SELECT HUB (If applicable - metro injection)
    ↓
LAST MILE PARTNER (National network carrier)
    ↓
DESTINATION (End customer)
```

### 3. Generate Visualization Data
- Use `maps_geocode` for all facility coordinates
- Use `maps_directions` for actual routing paths
- Use `maps_distance_matrix` for zone analysis
- Calculate transit time windows per service level

### 4. Create Deliverables
- Network flow diagram with real locations
- Zone-skip savings calculation
- Transit time comparison table
- Facility proximity analysis

## Service Level SLAs (Reference)

| Service | Transit Window | Network | Use Case |
|---------|---------------|---------|----------|
| Xparcel Ground | 3-8 business days | National + Select | Economy shipping |
| Xparcel Expedited | 2-5 business days | Select preferred | Faster ground |
| Xparcel Priority | 1-3 business days | Select + Premium | Time-critical |

## Key Principle

**Never name specific last-mile carriers** (UPS, FedEx, USPS). Use:
- "National network" = nationwide coverage, all ZIPs
- "Select network" = metro injection hubs for zone-skipping

## Reference Documents

- `references/00-facility-locations.md` - Hub coordinates and details
- `references/01-network-routing-logic.md` - Package flow decision tree
- `references/02-visualization-rubrics.md` - Quality scoring for outputs

## Integration Points

| Pipeline Stage | Use Case |
|----------------|----------|
| **Discovery (Stage 3)** | Explain network during 38 Questions |
| **Rate Creation (Stage 4)** | Show zone-skip savings potential |
| **Proposal (Stage 5)** | Visual network comparison in deck |
| **Implementation (Stage 7)** | Facility mapping for integration |

## Example Prompts

```
"Map a package journey from Ontario, CA fulfillment center to Miami, FL customer using Xparcel Expedited"

"Show zone-skip savings for a Dallas-based shipper sending to Northeast"

"Create a facility proximity analysis for a prospect in Chicago"

"Visualize the Select network hub coverage map"
```

## Quality Gates

Before delivering any network visualization:
1. [ ] All coordinates verified via Google Maps MCP
2. [ ] Transit times match SLA windows
3. [ ] No carrier names mentioned (National/Select only)
4. [ ] Zone-skip logic accurately represented
5. [ ] Facility addresses current and accurate
