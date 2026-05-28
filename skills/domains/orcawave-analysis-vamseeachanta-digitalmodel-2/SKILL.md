---
name: orcawave-analysis
description: Expert agent for OrcaWave diffraction/radiation analysis with deep expertise
  in marine hydrodynamics and panel method computations. Use for wave-structure interaction,
  added mass/damping calculations, QTF computation, and OrcaFlex hydrodynamic database
  generation.
version: 1.0.0
updated: 2025-01-02
category: offshore-engineering
triggers:
- OrcaWave analysis
- diffraction analysis
- radiation damping
- added mass calculation
- multi-body interaction
- QTF computation
- panel mesh generation
- hydrodynamic database
- wave-structure interaction
- frequency domain analysis
---
# OrcaWave Analysis Skill

Specialized expertise for OrcaWave diffraction/radiation analysis with panel method computations and OrcaFlex integration.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  hydrodynamics: '>=1.0.0,<2.0.0'
orcaflex_version: '>=11.0'
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
  - Linux
  - macOS
```

## Changelog

### [1.0.0] - 2026-01-07

**Added:**
- Initial version metadata and dependency management
- Semantic versioning support
- Compatibility information for Python 3.10-3.13

**Changed:**
- Enhanced skill documentation structure


## When to Use

- Diffraction analysis for wave-structure interaction
- Radiation analysis for added mass and damping
- Multi-body hydrodynamic interactions
- QTF (Quadratic Transfer Function) second-order calculations
- Panel mesh generation and optimization
- Batch processing of multiple configurations
- OrcaFlex hydrodynamic database generation
- Frequency domain marine analysis

## Agent Capabilities

This skill integrates agent capabilities from `/agents/orcawave/`:

### Core Capabilities
- **Diffraction Analysis**: Wave-structure interaction modeling
- **Radiation Damping**: Energy dissipation calculations
- **Added Mass Calculation**: Frequency-dependent inertia
- **Multi-body Interaction**: Coupled body dynamics
- **QTF Computation**: Second-order wave force calculations
- **Mesh Generation**: Panel mesh optimization and convergence
- **Batch Processing**: Parallel execution of multiple analyses
- **OrcaFlex Integration**: Hydrodynamic database generation

### Required Tools
- OrcaWave
- Python 3.8+
- COM Interface
- NumPy
- Pandas

### Expertise Areas
- Marine hydrodynamics
- Panel method theory
- Wave-structure interaction
- Frequency domain analysis
- Offshore engineering

## Performance Targets

| Metric | Target |
|--------|--------|
| Analysis Time | 10-60 seconds per configuration |
| Daily Throughput | 50-100 configurations |
| Accuracy | 5% tolerance vs benchmarks |
| Success Rate | 99%+ |

## Prerequisites

- OrcaWave license (COM API access)
- Python environment with `digitalmodel` package
- Panel mesh geometry files

## Python API

### Basic Analysis

```python
from digitalmodel.orcawave.orcawave_analysis import OrcaWaveAnalysis

# Initialize analysis
orcawave = OrcaWaveAnalysis()

# Configure analysis
config = {
    "vessel_mesh": "geometry/hull_panels.dat",
    "water_depth": 1000.0,
    "frequencies": [0.05, 0.1, 0.15, 0.2, 0.3, 0.5],
    "wave_directions": [0, 45, 90, 135, 180]
}

# Run diffraction/radiation analysis
results = orcawave.run(config)

# Extract added mass at specific frequency
added_mass = results.get_added_mass(frequency=0.1)

# Extract damping
damping = results.get_damping(frequency=0.1)

# Get RAOs
raos = results.get_raos()
```

### Batch Processing

```python
from digitalmodel.orcawave.batch import OrcaWaveBatch

# Initialize batch processor
batch = OrcaWaveBatch(parallel=True, max_workers=4)

# Define configurations
configs = [
    {"name": "draft_full", "draft": 20.0},
    {"name": "draft_ballast", "draft": 12.0},
    {"name": "draft_transit", "draft": 8.0}
]

# Run batch analysis
results = batch.run_batch(
    base_config="configs/base_analysis.yml",
    variations=configs,
    output_directory="results/draft_study/"
)

# Generate summary report
batch.generate_report(results, "results/batch_summary.html")
```

### OrcaFlex Integration

```python
from digitalmodel.orcawave.orcaflex_export import OrcaFlexExporter

# Initialize exporter
exporter = OrcaFlexExporter()

# Load OrcaWave results
exporter.load_results("orcawave_results/vessel.dat")

# Export to OrcaFlex hydrodynamic database
exporter.create_hydrodynamic_database(
    output_file="orcaflex_models/vessel_hydro.yml",
    include_qtf=True,
    viscous_damping={
        "roll": 0.05,  # 5% critical
        "pitch": 0.03,
        "heave": 0.02
    }
)
```

### Mesh Convergence Study

```python
from digitalmodel.orcawave.mesh_study import MeshConvergenceStudy

# Initialize study
study = MeshConvergenceStudy()

# Define mesh sizes to test
mesh_sizes = [2.0, 1.5, 1.0, 0.75, 0.5]

# Run convergence study
convergence = study.run(
    geometry="geometry/hull.step",
    mesh_sizes=mesh_sizes,
    target_frequency=0.1,
    output_directory="results/mesh_study/"
)

# Plot convergence
study.plot_convergence(
    convergence,
    output_file="results/mesh_convergence.html"
)

# Get recommended mesh size
recommended = study.get_recommended_size(convergence, tolerance=0.02)
print(f"Recommended mesh size: {recommended}m")
```

## Configuration Examples

### Standard Analysis

```yaml
# configs/orcawave_analysis.yml

orcawave:
  vessel:
    name: "FPSO"
    mesh_file: "geometry/hull_panels.dat"
    mass: 250000.0  # tonnes
    cog: [150.0, 0.0, 15.0]  # m
    radii_of_gyration: [25.0, 80.0, 82.0]  # m

  environment:
    water_depth: 1000.0  # m
    water_density: 1025.0  # kg/m3

  analysis:
    frequencies:
      min: 0.02
      max: 2.0
      count: 50
    wave_directions: [0, 30, 60, 90, 120, 150, 180]

  options:
    compute_qtf: true
    compute_drift: true
    irregular_frequencies: "lid_method"

  output:
    format: ["csv", "orcaflex"]
    directory: "results/"
```

### Multi-Body Analysis

```yaml
orcawave:
  multi_body:
    enabled: true
    bodies:
      - name: "FPSO"
        mesh_file: "geometry/fpso_panels.dat"
        position: [0, 0, 0]
      - name: "Offloading_Tanker"
        mesh_file: "geometry/tanker_panels.dat"
        position: [300, 50, 0]  # Side-by-side

  coupling:
    hydrodynamic: true
    mechanical: false  # Handle in OrcaFlex

  output:
    individual_results: true
    coupled_results: true
```

## Integration Targets

| Target | Purpose |
|--------|---------|
| OrcaFlex | Hydrodynamic database export, vessel creation |
| AQWA | Benchmark validation, result comparison |
| Excel | Automated reporting, visualization |
| CAD Systems | Mesh import, geometry handling |

## Workflow Support

- **Parallel Processing**: Multi-core execution for batch analyses
- **Batch Execution**: Run multiple configurations automatically
- **Error Recovery**: Automatic retry with license management
- **License Management**: Check and queue for available licenses

## MCP Tool Integration

### Swarm Coordination
```javascript
// Initialize panel method analysis swarm
mcp__claude-flow__swarm_init { topology: "star", maxAgents: 3 }

// Spawn specialized agents
mcp__claude-flow__agent_spawn { type: "analyst", name: "orcawave-processor" }
mcp__claude-flow__agent_spawn { type: "code-analyzer", name: "mesh-validator" }
```

### Memory Coordination
```javascript
// Store analysis configuration
mcp__claude-flow__memory_usage {
  action: "store",
  key: "orcawave/analysis/config",
  namespace: "hydrodynamics",
  value: JSON.stringify({
    vessel: "FPSO",
    mesh_panels: 5000,
    frequencies: 50,
    timestamp: Date.now()
  })
}

// Track batch progress
mcp__claude-flow__memory_usage {
  action: "store",
  key: "orcawave/batch/progress",
  namespace: "hydrodynamics",
  value: JSON.stringify({
    total: 100,
    completed: 45,
    failed: 2,
    running: 4
  })
}
```

### Benchmark Validation vs AQWA

Compare OrcaWave results with AQWA for validation at peak/significant values.

```python
from digitalmodel.diffraction.comparison_framework import PeakRAOComparator
from digitalmodel.diffraction.aqwa_converter import AQWAConverter
from digitalmodel.diffraction.orcawave_converter import OrcaWaveConverter

# Extract both datasets
aqwa_results = AQWAConverter(...).convert_to_unified_schema(...)
orcawave_results = OrcaWaveConverter(vessel).convert()

# Peak-focused comparison
comparator = PeakRAOComparator(
    aqwa_results=aqwa_results,
    orcawave_results=orcawave_results,
    peak_threshold=0.10,  # ≥10% of peak
    tolerance=0.05  # 5% tolerance
)

# Run comparison
results = comparator.compare_peaks()

# Generate report
comparator.generate_peak_report_html(
    results,
    output_file="benchmark/comparison_report.html"
)
```

**Validation Criteria:**
- 5% tolerance on peak values
- 90% of significant points within 5%
- Significant = RAO ≥ 10% of peak magnitude
- Focus on resonance regions

**Benchmark Location:**
`docs/modules/orcawave/L01_aqwa_benchmark/`

**Automated Scripts:**
- `run_comparison.py` - Full comparison with all data points
- `run_comparison_peaks.py` - Peak-focused validation (recommended)

## Best Practices

1. **Mesh Quality**: Ensure panel mesh convergence before production runs
2. **Frequency Range**: Cover wave spectrum frequencies of interest
3. **Direction Resolution**: Use finer resolution for asymmetric vessels
4. **QTF Computation**: Include second-order effects for deep-draft vessels
5. **Validation**: Cross-check peak values with AQWA (5% tolerance on significant values)
6. **License Management**: Queue analyses during peak license usage
7. **Benchmark Testing**: Run AQWA comparison before production use

## Error Handling

### License Issues
```python
# Check license before batch
from digitalmodel.orcawave.license import check_orcawave_license

if not check_orcawave_license():
    print("Waiting for license...")
    wait_for_license(timeout=3600)  # Wait up to 1 hour
```

### Mesh Issues
```python
# Validate mesh before analysis
from digitalmodel.orcawave.mesh import validate_panel_mesh

validation = validate_panel_mesh("geometry/hull_panels.dat")
if validation["issues"]:
    for issue in validation["issues"]:
        print(f"Mesh issue: {issue}")
```

## Related Skills

- [diffraction-analysis](../diffraction-analysis/SKILL.md) - **Master skill** for all diffraction workflows
- [bemrosetta](../bemrosetta/SKILL.md) - AQWA → OrcaFlex conversion with QTF and mesh support
- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Apply hydrodynamic database in OrcaFlex
- [aqwa-analysis](../aqwa-analysis/SKILL.md) - AQWA validation and comparison
- [gmsh-meshing](../gmsh-meshing/SKILL.md) - Panel mesh generation
- [hydrodynamics](../hydrodynamics/SKILL.md) - Coefficient management

## References

- Orcina OrcaWave Documentation
- Newman, J.N.: Marine Hydrodynamics
- Faltinsen, O.M.: Sea Loads on Ships and Offshore Structures
- Agent Configuration: `agents/orcawave/agent_config.json`

---

## Version History

- **1.1.0** (2026-01-05): Added AQWA benchmark comparison, peak-focused validation framework, 5% tolerance criteria for significant values
- **1.0.0** (2025-01-02): Initial release from agents/orcawave/ configuration

---

## OrcaWave API Properties Reference

These properties return the same data as shown on the validation page in the OrcaWave GUI:

**Frequency/Period Data:**
- `headings` - Wave heading angles (degrees)
- `frequencies` - Wave frequencies (rad/s)
- `angularFrequencies` - Angular frequencies
- `periods` - Wave periods (seconds)
- `periodsOrFrequencies` - Display format

**Hydrostatic and Frequency-Dependent:**
- `hydrostaticResults` - Hydrostatic stiffness matrix
- `addedMass` - Frequency-dependent added mass
- `infiniteFrequencyAddedMass` - Infinite frequency added mass
- `damping` - Radiation damping coefficients

**RAO Data:**
- `loadRAOsHaskind` - Force/moment RAOs (Haskind method) - N/m, N·m/m
- `loadRAOsDiffraction` - Force/moment RAOs (diffraction) - N/m, N·m/m
- `displacementRAOs` - **Motion/displacement RAOs** (m/m, rad/m) - **Use for AQWA comparison**

**QTF Data:**
- `meanDriftHeadingPairs` - Mean drift force heading combinations
- `QTFHeadingPairs` - QTF heading pairs
- `QTFFrequencies`, `QTFAngularFrequencies`, `QTFPeriods`, `QTFPeriodsOrFrequencies`

**Mean Drift and Pressure:**
- `meanDriftLoadPressureIntegration` - Mean drift from pressure
- `meanDriftLoadControlSurface` - Mean drift from control surface
- `meanDriftLoadMomentumConservation` - Mean drift from momentum

**Field Points:**
- `fieldPointPressure` - Pressure at field points
- `fieldPointRAO` - RAO at field points
- `fieldPointVelocity` - Velocity at field points
- `fieldPointRAOGradient` - RAO gradients

**Panel Data:**
- `panelGeometry` - Panel mesh geometry
- `panelPressure` - Panel pressure (total)
- `panelPressureDiffraction` - Panel pressure (diffraction component)
- `panelPressureRadiation` - Panel pressure (radiation component)
- `panelVelocity` - Panel velocities
- `panelVelocityDiffraction` - Panel velocity (diffraction)
- `panelVelocityRadiation` - Panel velocity (radiation)
- `panelPotentialInfiniteFrequencyRadiation` - Infinite frequency potential

**Quadratic Loads:**
- `quadraticLoadFromPressureIntegration` - Quadratic loads from pressure
- `quadraticLoadFromControlSurface` - Quadratic loads from control surface
- `directPotentialLoad` - Direct potential loads
- `indirectPotentialLoad` - Indirect potential loads

**Roll Damping:**
- `extraRollDamping` - Additional roll damping
- `rollDampingPercentCritical` - Roll damping as % of critical
