---
name: user-needs-map
description: "Map user needs independently of solutions using Allen's User Needs Mapping methodology. Identifies underserved needs that feed into the Opportunity Solution Tree."
---

# User Needs Mapping

Map what users need independently of any particular solution. Discover needs through research, not assumption. Source: Rich Allen (User Needs Mapping), connected to Wardley Mapping and Team Topologies.

## When to Use
- During L2 Opportunity discovery
- When building initial understanding of user landscape
- When validating whether team/service boundaries align with user needs
- When the OST needs a stronger needs foundation

## Workflow

### 1. Identify User Types
Who interacts with or is affected by this product/service?
- Direct users (hands-on)
- Indirect users (affected by outcomes)
- Internal users (staff, support, ops)

### 2. Extract Needs from Research
From interviews, observations, support tickets, and behavioral data, extract discrete need statements:

**Format**: "As a [user type], I need to [action/capability], so that [outcome/benefit]"

**Three dimensions** (from Christensen JTBD, applied to Allen's framework):
- **Functional**: What they need to accomplish practically
- **Emotional**: How they need to feel during and after
- **Social**: How it affects their relationships, status, perception

**Rules**:
- Needs come from RESEARCH, not brainstorming or stakeholder wishes
- Each need must cite at least one evidence source
- Separate needs from solutions: "I need to know my order status" not "I need email notifications"

### 3. Score Needs (Importance vs Satisfaction)
For each need:
- **Importance** (1-10): How critical is this to the user?
- **Current satisfaction** (1-10): How well do existing solutions meet this need?
- **Underserved score**: importance - current_satisfaction (higher = bigger opportunity)

### 4. Classify Need States
- **Met**: Current solutions adequately address this (satisfaction >= 7)
- **Underserved**: Need exists, current solutions are poor (importance high, satisfaction low)
- **Overserved**: Too much effort on needs users don't care about (importance low, satisfaction high)
- **Unrecognized**: Users have this need but don't articulate it (discovered through observation, not interviews)

### 5. Identify Opportunity Areas
Cluster underserved, high-importance needs into opportunity areas. These become the foundation for the OST.

### 6. Map to Value Chain (Allen's connection to Wardley)
User needs sit at the TOP of the Wardley Map (most visible to users). Each need implies a dependency chain of components needed to serve it. This is where User Needs Mapping connects to strategic landscape mapping.

### 7. Inform Team Boundaries (Allen's connection to Team Topologies)
User needs can inform team boundaries: each stream-aligned team should own a coherent cluster of user needs, not a technical component. If team boundaries don't align with need clusters, Conway's Law will create fragmented user experiences.

## Canvas Output
**Always update** `canvas/user-needs.yml` with discovered needs, scores, and states.
Also update:
- `canvas/opportunities.yml` with opportunity areas derived from underserved needs
- `canvas/landscape.yml` if needs mapping reveals new value chain components
- `canvas/team-shape.yml` if need clusters suggest different team boundaries

## Bias Warning
Before mapping needs, run `/bias-check`. Key biases:
- **Functional fixation**: Only mapping functional needs, missing emotional/social
- **Availability heuristic**: Overweighting needs from recent/loud users
- **Projection bias**: Assuming users need what YOU would need

## Theory Citations
- Allen: User Needs Mapping (methodology, connection to Wardley and Team Topologies)
- Christensen: Jobs to be Done (functional/emotional/social dimensions)
- Wardley: Value chain mapping (needs as anchor points)
- Skelton: Team Topologies (needs informing team boundaries)
