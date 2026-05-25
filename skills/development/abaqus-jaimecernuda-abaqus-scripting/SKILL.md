---
name: abaqus
description: Master skill for Abaqus FEA scripting. Use for any finite element analysis, topology optimization, or Abaqus Python scripting task. Routes to appropriate specialized skills.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Bash(uv:*)
  - Skill
---

# Abaqus Master Skill

Master orchestrator for all Abaqus FEA tasks. Routes requests to specialized skills based on user intent.

## When to Use This Skill

**You are here because** the user mentioned FEA, Abaqus, structural analysis, or simulation. Your job is to:
1. Understand what the user wants
2. Route to the appropriate specialized skill
3. Ask clarifying questions if unclear

## Routing Guide: User Intent to Skill

### Analysis Workflows (Complete End-to-End)

| User Says | Route To |
|-----------|----------|
| "stress", "displacement", "strength", "deflection", "will it break" | `/abaqus-static-analysis` |
| "frequency", "modal", "vibration", "resonance", "natural modes" | `/abaqus-modal-analysis` |
| "impact", "crash", "drop test", "transient", "explicit" | `/abaqus-dynamic-analysis` |
| "heat", "temperature", "conduction", "cooling", "thermal" | `/abaqus-thermal-analysis` |
| "thermal stress", "thermal expansion", "heat + deformation" | `/abaqus-coupled-analysis` |
| "contact", "friction", "parts touching", "assembly", "bolt" | `/abaqus-contact-analysis` |
| "fatigue", "cycles", "durability", "life prediction" | `/abaqus-fatigue-analysis` |
| "optimize weight", "topology", "minimize material" | `/abaqus-topology-optimization` |
| "reduce stress concentration", "smooth shape", "fillet" | `/abaqus-shape-optimization` |

### Module Skills (Single Tasks)

| Task | Route To |
|------|----------|
| Create geometry, import CAD | `/abaqus-geometry` |
| Define material properties | `/abaqus-material` |
| Generate mesh | `/abaqus-mesh` |
| Apply supports/constraints | `/abaqus-bc` |
| Apply forces/pressures | `/abaqus-load` |
| Configure analysis steps | `/abaqus-step` |
| Define contact/ties | `/abaqus-interaction` |
| Time-varying definitions | `/abaqus-amplitude` |
| Initial/predefined fields | `/abaqus-field` |
| Configure outputs | `/abaqus-output` |
| Submit/monitor jobs | `/abaqus-job` |
| Extract results from ODB | `/abaqus-odb` |
| Optimization task setup | `/abaqus-optimization` |
| Export STL/STEP/INP | `/abaqus-export` |
| API documentation | `/abaqus-docs` |

## Decision Tables

### Distinguishing Similar Analyses

| User Says | Plus This | Route To |
|-----------|-----------|----------|
| "stress analysis" | "with temperature" | `/abaqus-coupled-analysis` |
| "optimize" | "just shape, not holes" | `/abaqus-shape-optimization` |
| "optimize" | "remove material, add holes" | `/abaqus-topology-optimization` |
| "dynamic" | "find frequencies first" | `/abaqus-modal-analysis` |
| "dynamic" | "impact or crash" | `/abaqus-dynamic-analysis` |
| "vibration" | "mode shapes" | `/abaqus-modal-analysis` |
| "vibration" | "forced response" | `/abaqus-dynamic-analysis` |
| "thermal" | "just temperature" | `/abaqus-thermal-analysis` |
| "thermal" | "stress from heating" | `/abaqus-coupled-analysis` |

### Static vs Dynamic Decision

| Condition | Analysis Type |
|-----------|---------------|
| Load applied slowly, constant | Static |
| Load varies with time | Dynamic |
| Inertia effects important | Dynamic |
| Finding mode shapes only | Modal |
| Pre-stress then modes | Static + Modal |

## What to Ask If Unclear

### Missing Analysis Intent
> "What do you want to find out? Options:
> - Stress and displacement (static analysis)
> - Natural frequencies (modal analysis)
> - Impact/crash response (dynamic analysis)
> - Temperature distribution (thermal)"

### Missing Geometry
> "What are the dimensions of your part?"

### Missing Constraints
> "How is the structure supported? (fixed, pinned, roller)"

### Missing Loads
> "What loads are applied? (force, pressure, displacement)"

### Ambiguous Optimization
> "What kind of optimization?
> - Topology: Redistribute material, add holes (requires full license)
> - Shape: Modify surface only, reduce stress concentrations"

## Required Information by Analysis Type

| Analysis | Geometry | Material | BCs | Loads | Extra |
|----------|----------|----------|-----|-------|-------|
| Static | Yes | Yes | Yes | Yes | - |
| Modal | Yes | Yes (with density) | Yes | No | Number of modes |
| Dynamic | Yes | Yes (with density) | Yes | Yes | Time period |
| Thermal | Yes | Yes (conductivity) | Yes | Heat/convection | - |
| Topology | Yes | Yes | Yes | Yes | Volume fraction |
| Contact | Yes | Yes | Yes | Yes | Contact pairs |

## License Limitations

| Feature | Learning Edition | Full License |
|---------|------------------|--------------|
| Max nodes | 1000 | Unlimited |
| Static analysis | Yes | Yes |
| Modal analysis | Yes | Yes |
| Topology optimization | No | Yes (Tosca) |
| Shape optimization | No | Yes (Tosca) |

**If user has Learning Edition + optimization request:**
> "Topology optimization requires a full Abaqus license with Tosca. Would you like a static analysis instead?"

## Units System (All Skills)

| Quantity | Unit | Example |
|----------|------|---------|
| Length | mm | 100.0 |
| Force | N | 1000.0 |
| Stress | MPa | 210000.0 |
| Density | tonne/mm^3 | 7.85e-9 |
| Temperature | C or K | 20.0 |

## Running Scripts

| Mode | Command | Use Case |
|------|---------|----------|
| With GUI | `abaqus cae script=name.py` | Interactive |
| Headless | `abaqus cae noGUI=name.py` | Automated |
| Post-process | `abaqus python name.py` | ODB only |
| Submit job | `abaqus job=Name interactive` | Run analysis |

## References

For detailed information, see:
- `references/routing-guide.md` - Complete routing decision tree
- `references/workflow-matrix.md` - Skill dependencies
- `references/common-patterns.md` - Code examples
- `references/units-systems.md` - Unit conversions
