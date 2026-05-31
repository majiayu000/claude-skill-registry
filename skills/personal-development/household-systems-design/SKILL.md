---
name: household-systems-design
description: Designing the household as an operating system. Covers room-function mapping, work-triangle analysis, storage topology, utility flow, and the Richards/Beecher lineage that treats the home as an engineered environment rather than a stage set. Use when planning a new kitchen, reorganizing a room, diagnosing friction in a daily routine, or teaching a learner to see the house as a system with inputs, flows, and outputs.
type: skill
category: home-economics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/home-economics/household-systems-design/SKILL.md
superseded_by: null
---
# Household Systems Design

The household is an operating system. It has inputs (food, water, energy, materials, time, attention), state (inventory, cleanliness, maintenance status), flows (cooking, cleaning, laundry, repair), and outputs (meals, clean clothes, care, rest). Treating it that way — rather than as a collection of decor choices — is the foundational move of home economics as Ellen Swallow Richards and Catharine Beecher understood it. This skill catalogs the analytic tools for designing and diagnosing household systems: room-function mapping, work triangles, storage topology, utility flow, and the habitability criteria that Richards inherited from sanitary engineering.

**Agent affinity:** richards (systems framing and sanitary engineering), beecher (pedagogy of the engineered home), gilbreth (motion-efficient layout)

**Concept IDs:** home-room-function, home-work-triangle, home-storage-topology

## 1. The House as an Operating System

A functioning household has five subsystems that Richards named in her 1910 book *Euthenics*: nourishment, cleanliness, shelter, clothing, and care. Each subsystem has a work process, a storage requirement, a utility draw, and a failure mode. A household is "designed" when the five subsystems do not collide, do not starve each other, and produce their outputs with minimum wasted motion.

| Subsystem | Work process | Primary storage | Utility draw | Failure mode |
|---|---|---|---|---|
| Nourishment | Shopping, prep, cook, serve, clean | Pantry, fridge, freezer, dry goods | Water, gas/electric, ventilation | Food waste, contamination, skipped meals |
| Cleanliness | Sweep, wash, dispose, sanitize | Cleaning closet, laundry | Water, soap, electricity | Soil accumulation, cross-contamination |
| Shelter | Repair, maintain, weatherize, inspect | Tool area, supply shelf | Power, heat, air | Leaks, rot, cold, pest entry |
| Clothing | Launder, mend, store, retire | Closet, dresser, hamper | Water, electricity, dry air | Wear-out without replacement, lost items |
| Care | Rest, recovery, socialize, medicate | Bedroom, bath, medicine cabinet | Quiet, light, heat | Sleep debt, unmanaged illness |

Most household dysfunction is a subsystem collision: the laundry hamper is in the bath so the care subsystem blocks the clothing subsystem, or the pantry is in the living area so the nourishment subsystem leaks into the care subsystem. Diagnosing a room starts by asking which subsystems it serves and which ones are incompatible.

## 2. Room-Function Mapping

Every room has a primary function and a set of secondary functions. A room is well-designed when its primary function's work process is unobstructed and the secondary functions do not compromise it. The diagnostic procedure is:

1. **Name the primary function** of the room in one sentence. "This is the room where meals are cooked."
2. **List the secondary functions** the room actually serves today (homework, mail sorting, charging station, cat feeding).
3. **Measure obstruction**: for the primary function, how many secondary objects are in the work path? If the countertop is the work surface for cooking and it holds mail, a charger, and a fruit bowl, it has three obstructions.
4. **Relocate secondary functions** to rooms where they are themselves primary, or designate explicit zones that do not overlap the primary work path.

The goal is not minimalism. A home serves many functions. The goal is that the primary function of each room has priority over the secondary functions that accumulate there by default.

## 3. The Kitchen Work Triangle

The kitchen work triangle, formalized by Lillian Gilbreth in the 1920s and codified by the Cornell School of Home Economics in the 1940s, is the classic example of systems design applied to a room. The three work stations are the **refrigerator** (cold storage), the **sink** (water and waste), and the **stove** (heat). Cooking consists of short trips among these three stations plus longer excursions to the pantry.

**Geometric rule.** The three legs of the triangle should each be 4 to 9 feet, and the total perimeter should be 13 to 26 feet. Shorter than 13 feet crowds the cook; longer than 26 feet wastes motion on every meal.

**Obstruction rule.** No traffic path, no tall cabinet, and no permanent obstacle should cross any leg of the triangle.

**Zones.** Around each vertex, designate a small zone for the tools that serve that vertex: knives and cutting boards near the sink; pots, lids, and cooking oils near the stove; leftover containers and fresh produce near the refrigerator. Tools migrate to their vertex over time; enforce the migration periodically.

**Worked example.** A kitchen has refrigerator on the left wall, sink on the back wall, stove on the right wall. Triangle legs: 6 feet, 5 feet, 7 feet. Perimeter 18 feet. The triangle is inside the recommended envelope. The cook checks that the trash can is between sink and stove (not between sink and fridge, where it would block produce retrieval), that the spice rack is within arm's reach of the stove, and that the cutting board lives to the right of the sink where the wet-to-dry flow naturally goes.

## 4. Storage Topology

Storage is the household's memory. Badly arranged storage forces the user to search, which wastes time on every retrieval and produces duplicate purchases of items the user could not find. Well-arranged storage respects three principles.

**Principle 1 — Co-locate by workflow, not by category.** Items used together live together. A can of tomatoes, a can of tomato paste, and a jar of oregano used in the same weekly recipe are co-located even though one is a canned good and one is a spice. The workflow is the primary index; the category index is secondary.

**Principle 2 — Frequency determines height.** Items used daily go at chest-to-eye level, the zone that requires no bending or reaching. Items used weekly go at waist level or overhead. Items used monthly go at knee or highest-shelf level. Items used yearly go in the archive (basement, attic, garage bin). Demote items that have not been touched in six months; a half-year is a reliable indicator that the item no longer belongs in the active-use zone.

**Principle 3 — First-in-first-out is enforced by geometry.** Pantry shelves should be narrow enough that new items cannot be placed in front of old items — the geometry forces the cook to use older items first. Deep shelves defeat FIFO because old items get pushed to the back and forgotten.

## 5. Utility Flow

Every household subsystem draws utilities: water, gas, electricity, ventilation, bandwidth. A common failure mode is utility starvation: the cook cannot run the dishwasher while the laundry is running because the hot water heater is undersized, or the breakfast routine cannot use the kettle and toaster simultaneously because the circuit breaker trips.

The diagnostic is a utility-flow diagram. Draw each major appliance as a node. Draw the utility feeds as edges. Label each edge with its capacity (gallons per minute, amps, BTUs). For each daily routine, list which edges are simultaneously active. If the sum of active loads exceeds the capacity of any upstream edge, the routine will fail during peak.

**Fix patterns.** Reschedule (run the dishwasher overnight), rewire (dedicated circuit for the kitchen), resize (larger water heater), or reduce (smaller appliance load). The cheapest fix is usually rescheduling. Rewiring and resizing are expensive and should be reserved for persistent daily failures.

## 6. Richards's Habitability Criteria

Ellen Richards's sanitary engineering background gave home economics a non-negotiable set of habitability criteria. A dwelling is habitable when it meets all of these, and any diagnostic must check them first before turning to aesthetic or efficiency questions.

| Criterion | Test | Failure signal |
|---|---|---|
| Air | CO2 below 1000 ppm at occupied hours; no visible mold; no combustion byproducts indoors | Stuffiness, headache on waking, visible soot, musty smell |
| Water | Potable at the tap; hot water available; drainage works | Discoloration, taste, slow drains, sewer smell |
| Light | 300+ lux at task surfaces; daylight access for at least one major room | Eye strain, depression, inability to do fine work |
| Temperature | 18-24 C indoors; humidity 30-60% | Condensation on windows, cold floors, dry skin |
| Quiet | Below 45 dB at sleep hours | Sleep disruption, chronic fatigue |
| Cleanliness | No pest ingress; no cross-contamination between food and waste paths | Droppings, insects, garbage odor at food surfaces |

Habitability precedes efficiency. A motion-perfect kitchen in a house with mold is a worse design than an awkward kitchen in a dry, clean, well-ventilated house.

## 7. Diagnostic Protocol

A household-systems diagnosis follows this sequence:

1. **Habitability audit** (Section 6). Fail-fast: if any habitability criterion fails, stop and report that before any other work.
2. **Subsystem inventory** (Section 1). Name the five subsystems and where in the home each one lives.
3. **Collision check.** For each pair of subsystems, identify any shared room where they conflict.
4. **Room-function mapping** (Section 2) for the rooms that serve more than one subsystem.
5. **Work-triangle analysis** (Section 3) for kitchens and, by analogy, work-station analysis for any room with a primary production task (sewing, homework, laundry).
6. **Storage topology check** (Section 4) for pantry, closet, and tool area.
7. **Utility flow check** (Section 5) for daily peak routines.
8. **Prioritized recommendations**, organized by effort-to-benefit ratio: no-cost moves (rearranging) first, small purchases second, appliance replacements third, structural changes last.

## 8. Common Failure Patterns

| Pattern | Cause | Fix |
|---|---|---|
| "I can never find anything" | Storage not co-located by workflow | Re-sort by the recipes, routines, or tasks that use items together |
| "We keep buying things we already have" | Deep shelves defeat visibility | Narrow shelves, clear bins, front-load FIFO |
| "Cooking takes forever" | Work triangle broken by obstacles, or tools dispersed | Relocate traffic, consolidate tools at their vertex |
| "The laundry is always behind" | No dedicated zone, or zone collides with another subsystem | Relocate hamper, sort baskets, and folding surface out of the bath |
| "The house is always cold" | Envelope failure, not thermostat setting | Inspect windows, doors, insulation; habitability criterion fails before efficiency |
| "We fight about cleaning" | Shared work with no visible assignment | Make the assignment explicit on a routine chart |

## 9. Cross-References

- **richards agent** — Sanitary engineering framing, habitability audit, connection to public health and environmental hazard analysis
- **beecher agent** — Historical foundation of the engineered American home, pedagogical framing for teaching the skill
- **gilbreth agent** — Motion study applied to the work triangle and storage topology
- **nutrition-and-meal-planning skill** — Depends on a working kitchen; cannot be practiced in a kitchen whose triangle is broken
- **time-and-motion-in-the-home skill** — Gilbreth's method applied to daily routines
- **household-economics-and-budgeting skill** — Financial envelope that constrains appliance and structural fixes

## 10. References

- Richards, E. S. (1910). *Euthenics: The Science of Controllable Environment*. Whitcomb & Barrows.
- Beecher, C. E., & Stowe, H. B. (1869). *The American Woman's Home*. J. B. Ford & Co.
- Gilbreth, L. M. (1927). *The Home-Maker and Her Job*. D. Appleton.
- Cornell University School of Home Economics. (1949). *Kitchen Planning Standards*. Cornell Bulletin 677.
- Susanka, S. (1998). *The Not So Big House*. Taunton Press. (Modern complement.)
- Small Planet Institute. (2019). *Kitchen Work Triangle Revisited*. Design review paper.
