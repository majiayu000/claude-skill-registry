---
name: create-playground
description: Create and maintain the interactive Streamlit playground for learning VRP-Toolkit through hands-on exploration. Use this skill when adding playground features, integrating new algorithms, or enhancing the learning experience.
version: 1.0.0
tags: [project, playground, streamlit, learning, visualization]
---

# Create Playground Skill

Create and maintain an interactive Streamlit playground that enables "learn by playing" instead of "learn by reading code."

## Goal

Build and evolve a web-based playground where users can:
1. **Explore** VRP problems interactively (select, generate, visualize instances)
2. **Experiment** with algorithms (configure parameters, run solvers, compare results)
3. **Learn** through interaction (understand interfaces, pipelines, mechanisms)
4. **Reproduce** experiments (save configs, replay runs, export results)

## Core Philosophy

Following the vision in `playground/VISION.md`:
- **Three-layer learning:** Interface → Pipeline → Mechanism
- **Minimal cognitive load:** Only expose what's needed for current task
- **Contract-based trust:** Playground behavior matches actual code (verified by tests)
- **Just-in-time learning:** Dive deeper only when hitting limitations

## Workflow

### Step 1: Analyze User Request

**Understand what the user wants to learn or build:**

Questions to ask:
- What feature/algorithm do you want to explore?
- Which parameters are most important?
- What level of detail (beginner/intermediate/advanced)?
- What kind of visualization helps understanding?

**Common requests:**
- "Add support for CVRP problems"
- "Show how temperature affects ALNS search"
- "Visualize operator impact step-by-step"
- "Compare two algorithm configurations"

### Step 2: Design UI/UX

**Choose appropriate Streamlit components:**

Reference: `references/ui_components.md` for patterns

**Component selection guide:**
- **Parameters:** `st.slider`, `st.number_input`, `st.selectbox`
- **Problem definition:** `st.file_uploader`, `st.radio`, `st.multiselect`
- **Visualization:** `st.pyplot`, `st.plotly_chart`, `st.map`
- **Results:** `st.dataframe`, `st.metric`, `st.json`
- **Layout:** `st.columns`, `st.tabs`, `st.expander`

**Progressive disclosure:**
- Start with 5-10 key parameters
- Hide advanced parameters in `st.expander("Advanced")`
- Use defaults for 80% use cases

### Step 3: Integrate VRP-Toolkit Modules

**Map playground interactions to toolkit APIs:**

Reference: `references/integration_patterns.md` for examples

**Integration checklist:**
- [ ] Import correct modules (`from vrp_toolkit.problems import ...`)
- [ ] Convert UI inputs to API format (e.g., sliders → config dict)
- [ ] Handle errors gracefully (try-except with user-friendly messages)
- [ ] Extract outputs for display (solution → routes, cost, metrics)

**Key integration points:**
1. **Problem layer:** `PDPTWInstance`, `VRPProblem`, etc.
2. **Algorithm layer:** `ALNSSolver`, `ALNSConfig`, etc.
3. **Data layer:** `OrderGenerator`, `DemandGenerator`, `RealMap`
4. **Visualization layer:** `PDPTWVisualizer`, route plotting

### Step 4: Implement Visualization

**Make algorithm behavior visible:**

**Visualization types:**
- **Route maps:** Show vehicle routes on 2D map with nodes/edges
- **Convergence plots:** Cost vs. iteration (line chart)
- **Operator impact:** Before/after comparison (side-by-side)
- **Metrics dashboard:** Cost breakdown, constraint violations, runtime

**Best practices:**
- Use existing `vrp_toolkit.visualization` modules when possible
- Add interactive elements (hover for details, zoom, pan)
- Color-code for clarity (feasible=green, infeasible=red)
- Include legends and axis labels

### Step 5: Add Contract Tests

**Ensure playground behavior matches actual code:**

Reference: Create tests in `contracts/` directory

**Critical contracts to test:**
1. **Reproducibility:** Same seed + same config → same result
   ```python
   def test_reproducibility():
       config = {...}
       result1 = run_with_seed(config, seed=42)
       result2 = run_with_seed(config, seed=42)
       assert result1 == result2
   ```

2. **Feasibility:** Playground claims "feasible" → solution actually feasible
   ```python
   def test_feasibility_contract():
       solution = playground_run(...)
       if playground_says_feasible(solution):
           assert actually_feasible(solution)
   ```

3. **Evaluation consistency:** Playground displays correct objective value
   ```python
   def test_objective_value_contract():
       solution = playground_run(...)
       displayed_cost = playground_display_cost(solution)
       actual_cost = solution.objective_value
       assert displayed_cost == actual_cost
   ```

4. **Parameter validation:** Invalid inputs rejected with clear messages
   ```python
   def test_parameter_validation():
       with pytest.raises(ValueError, match="num_vehicles must be positive"):
           playground_run(num_vehicles=-1)
   ```

### Step 6: Update Documentation

**Keep documentation synchronized with playground features:**

**Files to update:**

1. **playground/README.md** - User-facing usage guide
   - Installation instructions
   - How to launch playground
   - Quick start guide
   - Feature overview

2. **playground/FEATURES.md** - Feature tracking
   - Current features (with status: ✅ Stable, 🚧 Beta, 🔮 Planned)
   - Recent additions
   - Known limitations
   - Roadmap

3. **playground/ARCHITECTURE.md** - Technical documentation
   - File structure (app.py, pages/, components/, utils/)
   - Component responsibilities
   - State management (session_state usage)
   - Extension guide (how to add new features)

4. **CHANGELOG_LEARNINGS.md** (if bugs fixed)
   - Root cause analysis
   - Fix description
   - Impact on playground features
   - New contract tests added

## Component Structure

Organize playground code for maintainability:

```
playground/
├── app.py                    # Main entry point (home page)
├── pages/                    # Multi-page app sections
│   ├── 1_Problem_Definition.py
│   ├── 2_Algorithm_Config.py
│   └── 3_Experiments.py
├── components/               # Reusable UI components
│   ├── instance_viewer.py   # Display instance details
│   ├── route_visualizer.py  # Plot routes on map
│   ├── convergence_plot.py  # Show cost over iterations
│   └── metrics_dashboard.py # Display KPIs
├── utils/                    # Helper functions
│   ├── state_manager.py     # Session state management
│   ├── export_utils.py      # Save/load experiments
│   └── validation.py        # Input validation
├── README.md                 # Usage guide
├── FEATURES.md               # Feature tracking
├── ARCHITECTURE.md           # Technical docs
└── requirements.txt          # Streamlit + dependencies
```

## Development Stages

### Stage 1: MVP (Minimal Viable Playground)
**Timeline:** 1-2 evenings
**Goal:** Get something playable

**Features:**
- Single-page app with basic workflow
- Instance selection (upload CSV or generate synthetic)
- Algorithm config (5-10 key parameters)
- Run button → display results
- Route visualization + cost metric

**Deliverables:**
- playground/app.py (~200 lines)
- playground/README.md (installation + quick start)
- 1-2 contract tests (reproducibility, feasibility)

### Stage 2: Explainability & Quality
**Timeline:** 2-3 evenings
**Goal:** Make learning actionable

**Features:**
- Multi-page app (Problem | Algorithm | Experiments)
- Seed control for reproducibility
- Convergence plot (cost vs. iteration)
- Experiment saving (runs/ directory)
- Contract test suite (5+ tests)

**Deliverables:**
- playground/pages/ (3 pages)
- contracts/ (5+ tests)
- runs/ directory structure
- playground/FEATURES.md

### Stage 3: Gamified Learning
**Timeline:** Future iterations
**Goal:** Self-driven learning

**Features:**
- Learning missions ("Get feasible solution in 30s")
- Step-by-step operator visualization
- Parameter impact hints
- Achievement tracking

## Common Patterns

### Pattern 1: Parameter Configuration UI

```python
import streamlit as st

def render_algorithm_config():
    """Render ALNS parameter configuration UI."""
    st.subheader("ALNS Configuration")

    # Core parameters (always visible)
    max_iterations = st.slider("Max Iterations", 100, 10000, 1000, step=100)
    start_temp = st.number_input("Start Temperature", 0.1, 100.0, 10.0)

    # Advanced parameters (in expander)
    with st.expander("Advanced Parameters"):
        cooling_rate = st.slider("Cooling Rate", 0.90, 0.99, 0.95)
        segment_length = st.number_input("Segment Length", 10, 200, 100)

    # Create config object
    from vrp_toolkit.algorithms.alns import ALNSConfig
    config = ALNSConfig(
        max_iterations=max_iterations,
        start_temp=start_temp,
        cooling_rate=cooling_rate,
        segment_length=segment_length
    )

    return config
```

### Pattern 2: Experiment Saving/Loading

```python
import json
from datetime import datetime
from pathlib import Path

def save_experiment(config, solution, metrics):
    """Save experiment to runs/ directory."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = Path(f"runs/{timestamp}")
    run_dir.mkdir(parents=True, exist_ok=True)

    # Save config
    with open(run_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Save solution
    with open(run_dir / "solution.json", "w") as f:
        json.dump(solution.to_dict(), f, indent=2)

    # Save metrics
    with open(run_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    st.success(f"Experiment saved to {run_dir}")
    return run_dir
```

### Pattern 3: Error Handling

```python
def run_algorithm_with_feedback():
    """Run algorithm with user-friendly error handling."""
    try:
        solution = solver.solve(instance)
        st.success("✅ Algorithm completed successfully")
        return solution
    except ValueError as e:
        st.error(f"❌ Invalid input: {e}")
        st.info("💡 Hint: Check that all parameters are positive")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        st.warning("🐛 This might be a bug. Please report it.")
        return None
```

## Quality Checklist

Before marking a playground feature as "complete":

- [ ] **Functionality:** Feature works as designed
- [ ] **UI/UX:** Interface is intuitive (5-second rule: can user figure it out in 5s?)
- [ ] **Integration:** Correctly calls vrp-toolkit APIs
- [ ] **Visualization:** Results are clearly visible
- [ ] **Error handling:** Invalid inputs show helpful messages
- [ ] **Contract tests:** At least 1 test verifies feature behavior
- [ ] **Documentation:** README.md and FEATURES.md updated
- [ ] **Reproducibility:** Same inputs → same outputs (when using fixed seed)

## Integration with Other Skills

**Works with:**
- **maintain-architecture-map:** Reference ARCHITECTURE_MAP.md to understand module structure
- **maintain-data-structures:** Reference data structure docs when integrating APIs
- **create-tutorial:** Playground features can inspire tutorial topics
- **track-learnings:** When bugs found, use track-learnings to document fixes

**Maintains:**
- playground/README.md
- playground/FEATURES.md
- playground/ARCHITECTURE.md
- contracts/ tests

## References

- `references/streamlit_guide.md` - Streamlit basics and best practices
- `references/ui_components.md` - Common UI component patterns
- `references/integration_patterns.md` - How to integrate vrp-toolkit modules
- `playground/VISION.md` - Design philosophy and principles

---

**Remember:** The goal is learning through interaction, not building a production app. Prioritize clarity and educational value over performance optimization.
