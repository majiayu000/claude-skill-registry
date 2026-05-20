---
name: maintain-architecture-map
description: Maintain system architecture documentation (ARCHITECTURE_MAP.md) showing module structure, data flows, and entry points. Use this skill when architecture changes, modules are added, or system overview needs updating.
version: 1.0.0
tags: [project, architecture, documentation, system-design]
---

# Maintain Architecture Map Skill

Maintain a living architecture document that shows the system's big picture: modules, data flows, entry points, and dependencies.

## Goal

Keep **ARCHITECTURE_MAP.md** and related architecture docs synchronized with the actual codebase, providing:
1. **Module Overview:** What modules exist and what they do
2. **Data Flows:** How data moves through the system (Instance → Solver → Solution → Visualizer)
3. **Entry Points:** Where to start when using the toolkit
4. **Dependencies:** How modules depend on each other

## Relationship to Other Skills

**Complementary to maintain-data-structures:**
- **maintain-data-structures:** Focuses on **what** (data structure definitions, attributes, methods, formats)
- **maintain-architecture-map:** Focuses on **how** (module structure, data flows, system pipelines)

**Example:**
- `maintain-data-structures` documents: `PDPTWInstance` has attributes `n`, `order_table`, `distance_matrix`
- `maintain-architecture-map` documents: `PDPTWInstance` is created in Data layer, consumed by Algorithm layer, visualized by Visualization layer

## When to Use This Skill

Trigger this skill when:
- [ ] New module added (e.g., new problem type, new algorithm)
- [ ] Module structure changes (files moved, packages reorganized)
- [ ] New entry point created (new public API)
- [ ] Data flow changes (new pipeline stage added)
- [ ] Major refactoring completed (architecture evolution)
- [ ] Preparing for playground development (need system overview)
- [ ] User asks "how does the system work?"

## Workflow

### Step 1: Scan Project Structure

**Identify current module organization:**

Reference: `references/scanning_scripts.md` for automation ideas

**Key directories to scan:**
```
vrp_toolkit/
├── problems/          # Problem definitions (PDPTW, VRP, etc.)
├── algorithms/        # Solving algorithms (ALNS, GA, etc.)
├── data/             # Data generation and loading
├── visualization/    # Plotting and visualization
└── utils/            # Common utilities
```

**For each module, extract:**
- Module purpose (from `__init__.py` docstring or README)
- Public classes (classes exported in `__init__.py`)
- Public functions (functions exported in `__init__.py`)
- Dependencies (imports from other modules)

### Step 2: Identify Entry Points

**Entry points are where users start using the toolkit:**

**Common entry point types:**
1. **Problem creation:**
   - `PDPTWInstance(order_table)` - Create problem from data
   - `generate_pdptw_instance(...)` - Generate synthetic problem

2. **Algorithm execution:**
   - `ALNSSolver.solve(problem)` - Solve using ALNS
   - `greedy_insertion_initial_solution(...)` - Generate initial solution

3. **Data generation:**
   - `OrderGenerator.generate()` - Generate order data
   - `RealMap(...)` - Create synthetic map

4. **Visualization:**
   - `PDPTWVisualizer.visualize(solution)` - Plot routes

**Document in ARCHITECTURE_MAP.md with:**
- Function signature
- One-sentence purpose
- Example usage (1-2 lines)

### Step 3: Map Data Flows

**Trace how data moves through the system:**

**Primary data flow (Problem → Solution):**
```
1. Data Layer:      Generate/load data
                    ↓
2. Problem Layer:   Create Instance (PDPTWInstance)
                    ↓
3. Algorithm Layer: Solve Instance → Solution (ALNSSolver.solve())
                    ↓
4. Visualization:   Visualize Solution (PDPTWVisualizer.visualize())
```

**Secondary data flows:**
- **Configuration:** User params → ALNSConfig → ALNSSolver
- **Evaluation:** Solution → Objective function → Cost metric
- **Validation:** Solution → Feasibility checker → Constraint violations

Reference: Create `.claude/docs/data_flows.md` for detailed flow diagrams

### Step 4: Document Module Dependencies

**Map which modules depend on which:**

**Dependency rules (VRP-Toolkit architecture):**
- ✅ **Algorithm** can depend on **Problem** (solvers need instances)
- ✅ **Visualization** can depend on **Problem** and **Algorithm** (visualizers need instances and solutions)
- ✅ **Data** can depend on **Problem** (generators create instances)
- ❌ **Problem** should NOT depend on **Algorithm** (instances are algorithm-agnostic)

**Create dependency graph:**
```
Data ────────┐
             ↓
Problem ←────┘
   ↓
Algorithm
   ↓
Visualization
```

Reference: Create `.claude/docs/module_dependencies.md` for full dependency map

### Step 5: Update ARCHITECTURE_MAP.md

**Use the template from `references/architecture_template.md`:**

**Required sections:**
1. **System Overview** - 2-3 paragraph summary
2. **Three-Layer Architecture** - Problem/Algorithm/Data layer descriptions
3. **Module Guide** - One subsection per module with purpose and key exports
4. **Entry Points** - How to start using the toolkit
5. **Data Flows** - Visual diagram + text description
6. **Key Abstractions** - VRPProblem, VRPSolution, Solver interfaces
7. **Extension Guide** - How to add new problems/algorithms
8. **Quick Reference** - Cheat sheet of common operations

**Formatting guidelines:**
- Keep it concise (aim for <500 lines total)
- Use diagrams (ASCII art or mermaid)
- Include code examples (1-3 lines each)
- Link to detailed docs (maintain-data-structures references)

### Step 6: Update Supporting Docs

**Create/update `.claude/docs/` as needed:**

**data_flows.md** - Detailed data flow diagrams
- Problem creation flow
- Algorithm execution flow
- Visualization flow
- Configuration flow

**module_dependencies.md** - Dependency graph
- Import graph (module → imported modules)
- Circular dependency checks
- Layer violations (if any)

**extension_guide.md** - How to extend the system
- Adding a new problem type
- Adding a new algorithm
- Adding a new operator
- Adding a new visualization

## Architecture Template

### Minimal ARCHITECTURE_MAP.md Structure

```markdown
# VRP-Toolkit Architecture Map

**Last Updated:** YYYY-MM-DD
**Version:** 0.1.0

## System Overview

[2-3 paragraphs describing the toolkit]

## Three-Layer Architecture

### 1. Problem Layer (vrp_toolkit/problems/)
[Description + key classes]

### 2. Algorithm Layer (vrp_toolkit/algorithms/)
[Description + key classes]

### 3. Data Layer (vrp_toolkit/data/)
[Description + key classes]

### 4. Visualization Layer (vrp_toolkit/visualization/)
[Description + key classes]

## Module Guide

### problems/
**Purpose:** [One sentence]
**Key Exports:**
- `PDPTWInstance` - [Purpose]
- `VRPProblem` - [Purpose]

[Repeat for each module]

## Entry Points

### 1. Create a Problem
```python
from vrp_toolkit.problems.pdptw import PDPTWInstance
instance = PDPTWInstance(order_table=df)
```

### 2. Solve the Problem
```python
from vrp_toolkit.algorithms.alns import ALNSSolver
solver = ALNSSolver(config)
solution = solver.solve(instance)
```

[Continue for main workflows]

## Data Flows

[ASCII diagram or mermaid]

## Key Abstractions

[Describe VRPProblem, VRPSolution, Solver interfaces]

## Extension Guide

[How to add new problems/algorithms]

## Quick Reference

[Cheat sheet table]
```

Full template: `references/architecture_template.md`

## Automation Helpers

### Script: Scan Module Structure

```python
# scripts/scan_modules.py
from pathlib import Path
import importlib

def scan_module(module_path):
    """Scan a module and extract public API."""
    init_file = module_path / "__init__.py"

    if not init_file.exists():
        return None

    # Read __init__.py
    content = init_file.read_text()

    # Extract __all__ if present
    if "__all__" in content:
        # Parse __all__ list
        pass

    # Extract docstring
    # Extract classes/functions

    return {
        'name': module_path.name,
        'docstring': '...',
        'exports': [...]
    }

def scan_all_modules():
    """Scan all vrp_toolkit modules."""
    toolkit_path = Path("vrp-toolkit/vrp_toolkit")
    modules = []

    for module_dir in toolkit_path.iterdir():
        if module_dir.is_dir() and not module_dir.name.startswith('_'):
            info = scan_module(module_dir)
            if info:
                modules.append(info)

    return modules
```

Reference: See `references/scanning_scripts.md` for full scripts

## Quality Checklist

Before marking ARCHITECTURE_MAP.md as up-to-date:

- [ ] **Accuracy:** All listed modules/classes exist in codebase
- [ ] **Completeness:** All major modules documented
- [ ] **Entry points:** At least 3-5 entry points with examples
- [ ] **Data flows:** At least 1 visual diagram
- [ ] **Dependencies:** Dependency graph present
- [ ] **Layer compliance:** No violations of three-layer architecture
- [ ] **Links:** Cross-references to maintain-data-structures docs work
- [ ] **Freshness:** "Last Updated" date is current
- [ ] **Brevity:** Total length < 500 lines (main file)

## Integration with Other Skills

**Works with:**
- **maintain-data-structures:** Link to data structure references for details
- **create-playground:** Playground references ARCHITECTURE_MAP for integration patterns
- **migrate-module:** After migration, update architecture docs
- **build-session-context:** Reads ARCHITECTURE_MAP for project overview

**Maintains:**
- `.claude/ARCHITECTURE_MAP.md` - Main architecture document
- `.claude/docs/data_flows.md` - Data flow diagrams
- `.claude/docs/module_dependencies.md` - Dependency graph

## Common Patterns

### Pattern 1: Document a New Module

When adding a new module (e.g., `vrp_toolkit/algorithms/genetic/`):

1. Add entry to "Module Guide" section:
   ```markdown
   ### algorithms/genetic/
   **Purpose:** Genetic algorithm solver for VRP problems
   **Key Exports:**
   - `GeneticSolver` - Main GA solver implementing Solver interface
   - `GAConfig` - Configuration for genetic parameters
   ```

2. Update "Entry Points" if new public API:
   ```markdown
   ### 3. Solve with Genetic Algorithm
   ```python
   from vrp_toolkit.algorithms.genetic import GeneticSolver
   solver = GeneticSolver(config)
   solution = solver.solve(instance)
   ```
   ```

3. Update dependency graph if needed

### Pattern 2: Document Data Flow

When documenting a new data flow (e.g., "How does configuration work?"):

1. Create ASCII diagram:
   ```
   User Input
      ↓
   UI Widgets (Streamlit)
      ↓
   ALNSConfig (dataclass)
      ↓
   ALNSSolver.__init__(config)
      ↓
   ALNS.run() uses config params
   ```

2. Add text explanation

3. Link from ARCHITECTURE_MAP.md to detailed docs

### Pattern 3: Update After Refactoring

When architecture changes (e.g., "Split ALNS into solver.py and operators.py"):

1. Update module structure in "Module Guide"
2. Update imports in code examples
3. Update dependency graph
4. Verify no broken cross-references

## References

- `references/architecture_template.md` - Full ARCHITECTURE_MAP.md template
- `references/scanning_scripts.md` - Automation scripts for module scanning
- `maintain-data-structures/` skill - For detailed data structure docs

---

**Remember:** ARCHITECTURE_MAP.md is for the big picture. For detailed class/function documentation, use maintain-data-structures skill.
