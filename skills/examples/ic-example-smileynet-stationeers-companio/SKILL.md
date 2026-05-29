---
name: ic-example
description: Find example IC10 code for common patterns. Use when user asks for examples, templates, or sample code for Stationeers automation like airlocks, pressure control, solar tracking, or furnace management.
---

# IC10 Example Finder

Find example IC10 code from local library or external sources.

## Workflow

### 1. Local Search Phase

Use Task tool to spawn:
- `pattern-finder` - Search local examples/ directory

### 2. External Search Phase (If Local Empty)

If local search returns no good matches:
- `resource-curator` - Search external sources

### 3. Adaptation Phase (If Nothing Found Anywhere)

If neither local nor external found:
- `code-generator` - Create example based on closest patterns

## Decision Flow

```
User Request
    |
    v
pattern-finder (local examples/)
    |
    +-- FOUND --> Present local example(s)
    |             with full code
    |
    +-- NOT FOUND
            |
            v
    resource-curator (external)
            |
            +-- FOUND --> Create guide
            |             Present top results with links
            |
            +-- NOT FOUND
                    |
                    v
            Offer to generate new example
            using code-generator
```

## Available Categories (Local)

### Atmosphere
- Pressure regulation
- Temperature control
- Gas mixing
- Filtration systems

### Power
- Solar tracking
- Battery monitoring
- Generator control
- Power distribution

### Airlocks
- Simple cycling
- Pressure-based cycling
- Multi-door sequences
- Emergency protocols

### Patterns
- PID controller
- Hysteresis (bang-bang)
- State machines
- Proportional control

## Instructions

When the user asks for example code:

1. **Search locally first**:
   - Launch `pattern-finder` with category/pattern name
   - Check `examples/` directory

2. **If found locally**:
   - Present the example with full code
   - Explain what it does
   - Note device requirements
   - Highlight customization points
   - Done

3. **If NOT found locally**:
   - Launch `resource-curator` with the topic
   - Wait for external search results

4. **If found externally**:
   - Present top resources with links
   - Note guide location: `guides/[topic]-resources.md`
   - Explain these are external resources (not local examples)
   - Done

5. **If nothing found anywhere**:
   - Inform user no existing examples found
   - Offer to generate a new example
   - If user agrees, launch `code-generator`

## Example Triggers

- "Show me an example of..."
- "How do I control pressure?"
- "Give me a template for..."
- "What's a good pattern for...?"
- "Do you have example code for...?"
- "I need a sample script for..."

## Example Response (Local Found)

```
## Local Example: Pressure Control

Found in `examples/atmosphere/pressure-control.ic10`:

```ic10
# Pressure regulation for a room
# d0 = Pressure sensor
# d1 = Active vent (inward)
...
```

**Devices required**: Pressure sensor, Active vent
**Customization**: Change TARGET_PRESSURE constant (line 5)
```

## Example Response (External Found)

```
## External Resources for "trading automation"

No local examples found, but I searched external sources.

**Found 4 resources:**

1. **jhillacre/trading-controller.ic10**
   https://github.com/jhillacre/stationeers-scripts/...
   Full auto-trading with satellite dish control

2. **Wiki: Satellite Dish**
   https://stationeers-wiki.com/Satellite_Dish
   Manual control and signal detection

Full guide saved to: `guides/trading-resources.md`
```

## Example Response (Nothing Found)

```
## No Examples Found

I searched both local examples and external sources but didn't find existing code for "[topic]".

Would you like me to generate a new example? I can create one based on the closest related patterns.
```
