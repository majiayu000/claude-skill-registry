---
name: PlantCapability
description: |
  MNMUK machine shop capability checker. Answers "can we make this?" queries against the plant list.
  Recommends optimal machine selection based on part requirements.
  USE WHEN user asks 'can we make', 'which machine', 'capability check', 'feasibility',
  'what can we hold', 'tolerance capability', or describes a part to quote.
---

# PlantCapability - MNMUK Machine Shop

**Purpose:** Instant feasibility checks and machine selection for quoting and planning.

## When to Activate
- "Can we make this part?"
- "Which machine should we use for...?"
- "What's our tolerance capability on...?"
- "Can we turn/mill a part that is..."
- "Do we have capacity for..."
- Part feasibility questions during quoting

---

## MNMUK Plant List

### 5-AXIS MACHINING CENTRES

| Machine | Envelope (X,Y,Z) | Tolerance | Features |
|---------|------------------|-----------|----------|
| DMG MORI NMV3000 | 470 x 350 x 510mm | ±0.010mm | 114 pallet automation |
| DMG MORI DMU50 | 650 x 650 x 550mm | ±0.010mm | 10 pallet automation |
| DMG MORI NHX500 | 650 x 650 x 750mm | ±0.010mm | Twin pallet, 4-axis |

**Best for:** Complex geometries, multi-face machining, aerospace/medical components, batch production with pallet systems.

### 4-AXIS MACHINING CENTRES

| Machine | Envelope (X,Y,Z) | Tolerance | Features |
|---------|------------------|-----------|----------|
| Vertical 4-Axis VMC | 700 x 500 x 450mm | ±0.010mm | Rotary table |

**Best for:** Parts requiring indexing, larger prismatic components.

### TURNING CENTRES

| Machine | Max Diameter | Bar Capacity | Z-Travel | Tolerance | Features |
|---------|--------------|--------------|----------|-----------|----------|
| DMG MORI NLX2500 Twin | Ø200mm | Ø95mm | 250mm | ±0.010mm | Twin spindle, live tooling |
| DMG MORI NLX2500 Single | Ø200mm | Ø80mm | 700mm | ±0.010mm | Single spindle, live tooling, long parts |
| DMG MORI ALX2000 | Ø150mm | Ø50.8mm | 375mm | ±0.005mm | Higher precision |
| HARDINGE Twin | Ø270mm | Ø50.8mm | 350mm | ±0.003mm | Best turning tolerance |

**Best for:** Rotational parts, shaft work, parts with milled features (live tooling).

### SWISS-TYPE MACHINES

| Machine | Max Diameter | Bar Capacity | Z-Travel | Tolerance | Features |
|---------|--------------|--------------|----------|-----------|----------|
| CITIZEN Sliding Head (Laser) | Ø50mm | Ø38.1mm | 300mm | ±0.003mm | Laser head, twin spindle, live tooling |
| CITIZEN Sliding Head LFV | Ø50mm | Ø38.1mm | 300mm | ±0.003mm | LFV chip breaking, twin spindle |

**Best for:** Small precision parts, medical components, high-volume turned parts, difficult chip-breaking materials.

### EDM MACHINES

| Machine | Envelope (X,Y,Z) | Tolerance | Type |
|---------|------------------|-----------|------|
| MITSUBISHI Wire EDM | 350 x 350 x 350mm | ±0.004mm | Wire erosion |
| MITSUBISHI Spark EDM | 350 x 350 x 350mm | ±0.050mm | Sinker/spark erosion |

**Best for:** Hardened materials, complex internal profiles, sharp internal corners, die/mold work.

### FAST RESPONSE CELL

| Machine | Envelope/Capacity | Tolerance | Features |
|---------|-------------------|-----------|----------|
| Haas Mini Mill | 250 x 250 x 250mm | ±0.050mm | Quick setup |
| Haas Tool Room Lathe | Ø180mm x 200mm | ±0.050mm | Prototypes, one-offs |

**Best for:** Prototypes, urgent one-offs, simple parts, proving out before production.

---

## Capability Decision Logic

### Tolerance Selection Guide

| Required Tolerance | Recommended Route |
|--------------------|-------------------|
| ±0.003mm or tighter | HARDINGE turning, CITIZEN Swiss, Wire EDM |
| ±0.005mm | DMG MORI ALX2000, Swiss machines |
| ±0.010mm | Standard DMG MORI turning/milling |
| ±0.050mm | Haas fast response cell |
| Looser | Any machine, optimize for cycle time |

### Part Type Routing

**Turned Parts (rotational):**
```
IF diameter > 200mm → CANNOT MAKE (max Ø270mm on Hardinge)
IF diameter > 150mm AND tolerance < ±0.005mm → HARDINGE only
IF diameter ≤ 50mm AND high volume → CITIZEN Swiss
IF length > 700mm → CANNOT MAKE (max Z700mm on NLX2500 Single)
IF tolerance ≤ ±0.003mm → HARDINGE or CITIZEN
ELSE → DMG MORI NLX2500 (twin for short parts, single for long)
```

**Milled Parts (prismatic):**
```
IF any dimension > 700mm → CANNOT MAKE
IF 5-axis required AND part ≤ 470x350x510mm → NMV3000 (best automation)
IF 5-axis required AND part ≤ 650x650x550mm → DMU50
IF 4-axis sufficient AND part ≤ 700x500x450mm → Vertical VMC
IF simple prototype → Haas Mini Mill
```

**Complex Geometries:**
```
IF hardened material (>50 HRC) → EDM route
IF sharp internal corners required → Wire EDM
IF through-profile cuts → Wire EDM
IF cavity/pocket in hardened steel → Spark EDM
```

### Material Considerations

| Material Type | Notes |
|---------------|-------|
| Aluminium | All machines, optimize speeds |
| Stainless (303/304/316) | Consider CITIZEN LFV for chip breaking |
| Titanium | 5-axis mills, reduce speeds, rigid setups |
| Inconel/Hastelloy | Reduced feeds, consider EDM for features |
| Hardened steel (>50 HRC) | EDM only for machining, or machine before hardening |
| Plastics/Delrin | Swiss machines excellent, watch for heat |
| Brass/Bronze | All machines, free-machining |

---

## Capacity Limits Summary

| Capability | Maximum | Machine |
|------------|---------|---------|
| Largest turned diameter | Ø270mm | HARDINGE |
| Longest turned part | Z700mm | NLX2500 Single |
| Best turning tolerance | ±0.003mm | HARDINGE, CITIZEN |
| Largest milled part | 700 x 500 x 450mm | 4-axis VMC |
| Best milling tolerance | ±0.010mm | All DMG MORI mills |
| Smallest precision parts | Ø50mm max | CITIZEN Swiss |
| Hardened material machining | Via EDM | MITSUBISHI |

---

## Example Queries and Responses

**Query:** "Can we turn a Ø150mm x 400mm shaft in 316SS to ±0.008mm?"
**Response:** YES - Use DMG MORI NLX2500 Single Spindle
- Diameter OK: Ø150mm < Ø200mm capacity
- Length OK: 400mm < 700mm Z-travel
- Tolerance OK: ±0.008mm achievable (machine capable of ±0.010mm)
- Material: 316SS fine, consider live tooling for any milled features

**Query:** "Can we make a 5-axis aerospace bracket 500x400x300mm in Ti-6Al-4V?"
**Response:** YES - Use DMG MORI DMU50
- Envelope OK: 500x400x300 fits in 650x650x550mm
- 5-axis capability: Yes
- Material: Titanium requires reduced parameters, rigid fixturing
- Note: NMV3000 too small (470x350x510mm)

**Query:** "Small precision medical pin Ø3mm x 25mm, ±0.002mm tolerance, 10,000 qty?"
**Response:** MARGINAL - CITIZEN Swiss closest but tolerance challenging
- Size OK: Well within Ø50mm capacity
- Volume: Swiss machines ideal for high volume
- Tolerance: ±0.002mm tighter than ±0.003mm capability
- Recommendation: Discuss with engineering - may need post-process grinding or accept ±0.003mm

---

## Response Format

When answering capability queries, use this structure:

```
## Feasibility: [YES / NO / MARGINAL]

**Recommended Machine:** [Machine name]

**Analysis:**
- Envelope: [OK/Issue] - [details]
- Tolerance: [OK/Issue] - [details]
- Material: [OK/Issue] - [details]
- Features: [OK/Issue] - [details]

**Alternatives:** [If applicable]

**Risks/Notes:** [Any concerns or special considerations]
```

---

## Quick Reference Card

```
TURNING:
  Max Ø270mm (Hardinge) | Max Z700mm (NLX2500 Single)
  Best tol: ±0.003mm (Hardinge/Citizen)

MILLING:
  Max 700x500x450mm (4-axis VMC)
  5-axis max: 650x650x750mm (NHX500)
  Best tol: ±0.010mm

SWISS:
  Max Ø50mm | ±0.003mm | High volume

EDM:
  350x350x350mm | ±0.004mm wire | Hardened materials

FAST RESPONSE:
  Prototypes | ±0.050mm | Quick turnaround
```
