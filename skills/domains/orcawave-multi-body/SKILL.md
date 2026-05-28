---
name: orcawave-multi-body
description: Multi-body hydrodynamic interaction specialist for OrcaWave. Handles
  coupled vessel analysis, side-by-side operations, FPSO-tanker interactions, gap
  resonance, and hydrodynamic shielding effects.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- multi-body hydrodynamics
- side-by-side operation
- coupled vessel analysis
- FPSO tanker interaction
- gap resonance
- hydrodynamic shielding
- STS transfer
- offloading operation
---

# OrcaWave Multi-Body Analysis Skill

Specialized expertise for multi-body hydrodynamic interaction analysis in OrcaWave, including side-by-side operations and coupled vessel dynamics.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  numpy: '>=1.24.0'
  scipy: '>=1.11.0'
orcawave_version: '>=11.0'
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
```

## When to Use

- Side-by-side (STS) ship-to-ship transfer operations
- FPSO and offloading tanker interaction
- Multiple floating bodies in close proximity
- Gap resonance phenomenon investigation
- Hydrodynamic shielding effects
- Coupled vessel response analysis
- Multi-body mooring system design

## Multi-Body Configurations

### Common Scenarios

| Configuration | Bodies | Application |
|---------------|--------|-------------|
| Side-by-Side | 2 | STS transfer, offloading |
| Tandem | 2 | Towing, CALM buoy |
| Spread | 3+ | Offshore construction |
| Nested | 2 | Dock/vessel, barge/cargo |

### Gap Resonance

Gap resonance occurs when waves resonate in the gap between closely spaced vessels:
- Critical for side-by-side operations
- Can cause extreme relative motions
- Gap width typically 2-10 meters
- Dominant in beam seas

## Python API

### Basic Multi-Body Setup

```python
from digitalmodel.modules.orcawave.multibody import MultiBodyAnalysis

# Initialize multi-body analysis
mb = MultiBodyAnalysis()

# Add primary vessel (FPSO)
mb.add_body(
    name="FPSO",
    mesh_file="geometry/fpso_panels.gdf",
    position=[0.0, 0.0, 0.0],  # Origin at FPSO
    mass=250000.0,  # tonnes
    cog=[150.0, 0.0, 12.0],
    radii_of_gyration=[25.0, 80.0, 82.0]
)

# Add secondary vessel (Shuttle Tanker)
mb.add_body(
    name="Shuttle_Tanker",
    mesh_file="geometry/tanker_panels.gdf",
    position=[280.0, 15.0, 0.0],  # Side-by-side, 15m gap
    mass=150000.0,
    cog=[130.0, 0.0, 10.0],
    radii_of_gyration=[20.0, 65.0, 67.0]
)

# Configure analysis
mb.configure(
    water_depth=1200.0,
    frequencies=np.linspace(0.02, 1.5, 40),
    headings=[0, 30, 60, 90, 120, 150, 180],
    include_coupling=True
)

# Run analysis
results = mb.run()

# Extract coupled response
coupled_raos = results.get_coupled_raos()
relative_motion = results.get_relative_motion("FPSO", "Shuttle_Tanker")
```

### Gap Resonance Analysis

```python
from digitalmodel.modules.orcawave.multibody import GapResonanceAnalyzer

# Initialize gap resonance analyzer
gap = GapResonanceAnalyzer()

# Configure gap geometry
gap.configure(
    vessel1="FPSO",
    vessel2="Shuttle_Tanker",
    gap_width=8.0,  # meters
    gap_length=200.0,  # overlap length
    draft1=22.0,
    draft2=18.0
)

# Identify resonance frequencies
resonances = gap.find_resonances(
    frequency_range=(0.1, 1.0),
    resolution=0.01
)

for mode, freq in resonances.items():
    print(f"Mode {mode}: {freq:.3f} rad/s (T = {2*np.pi/freq:.1f} s)")

# Analyze gap wave elevation
gap_waves = gap.compute_gap_elevation(
    frequencies=results.frequencies,
    headings=[90]  # Beam seas - worst case
)

# Plot gap resonance response
gap.plot_response(
    gap_waves,
    output_file="plots/gap_resonance.html"
)
```

### Side-by-Side Operations

```python
from digitalmodel.modules.orcawave.multibody import SideBySideAnalysis

# Initialize STS analysis
sts = SideBySideAnalysis()

# Configure vessels
sts.configure_fpso(
    mesh="geometry/fpso.gdf",
    loa=300.0,
    beam=50.0,
    draft=22.0
)

sts.configure_tanker(
    mesh="geometry/tanker.gdf",
    loa=250.0,
    beam=45.0,
    draft=18.0
)

# Set gap configuration
sts.set_gap_configuration(
    gap_width=8.0,
    longitudinal_offset=25.0,  # Tanker forward of FPSO midship
    fender_locations=[(50.0, 0.0), (150.0, 0.0), (250.0, 0.0)]
)

# Run STS analysis
results = sts.run(
    headings=[0, 30, 60, 90, 120, 150, 180],
    frequencies=np.linspace(0.05, 1.2, 35)
)

# Extract key results
relative_surge = results.get_relative_motion("surge")
relative_sway = results.get_relative_motion("sway")
relative_heave = results.get_relative_motion("heave")
relative_roll = results.get_relative_motion("roll")

# Check operability limits
operability = sts.check_operability(
    results,
    limits={
        "relative_surge": 2.0,  # m
        "relative_sway": 1.5,   # m
        "relative_heave": 1.0,  # m
        "relative_roll": 2.0    # degrees
    }
)

print(f"Operability: {operability['overall']:.1%}")
```

### Hydrodynamic Coupling Matrices

```python
from digitalmodel.modules.orcawave.multibody import CouplingMatrixExtractor

# Extract coupling matrices
extractor = CouplingMatrixExtractor()

# Load multi-body results
extractor.load_results("results/multibody.owr")

# Get coupled added mass (12x12 for 2 bodies)
coupled_added_mass = extractor.get_coupled_added_mass(frequency=0.1)
print(f"Coupled matrix shape: {coupled_added_mass.shape}")  # (12, 12)

# Decompose into blocks
A11, A12, A21, A22 = extractor.decompose_coupling(coupled_added_mass)
# A11: Body 1 self-influence (6x6)
# A12: Body 1 -> Body 2 influence (6x6)
# A21: Body 2 -> Body 1 influence (6x6)
# A22: Body 2 self-influence (6x6)

# Compare with isolated bodies
isolated_A1 = extractor.get_isolated_added_mass("FPSO", frequency=0.1)
coupling_effect = np.linalg.norm(A11 - isolated_A1) / np.linalg.norm(isolated_A1)
print(f"Coupling effect on FPSO added mass: {coupling_effect:.1%}")
```

### Shielding Effects

```python
from digitalmodel.modules.orcawave.multibody import ShieldingAnalyzer

# Analyze wave shielding
shielding = ShieldingAnalyzer()

# Configure
shielding.load_multibody_results("results/multibody.owr")

# Compare sheltered vs exposed
shielding_factor = shielding.compute_shielding_factor(
    target_body="Shuttle_Tanker",
    shielding_body="FPSO",
    headings=[0, 180],  # Head/stern seas
    frequency_range=(0.1, 0.8)
)

# Plot shielding effect
shielding.plot_shielding(
    shielding_factor,
    output_file="plots/shielding_effect.html"
)

# Key metrics
print(f"Average shielding (head seas): {shielding_factor['avg_head']:.1%}")
print(f"Average shielding (stern seas): {shielding_factor['avg_stern']:.1%}")
```

## Configuration Examples

### Multi-Body Analysis Configuration

```yaml
# configs/multibody_analysis.yml

multibody:
  name: "FPSO_STS_Operation"

  bodies:
    - name: "FPSO"
      mesh: "geometry/fpso_panels.gdf"
      position: [0.0, 0.0, 0.0]
      mass: 250000.0  # tonnes
      cog: [150.0, 0.0, 12.0]
      radii_of_gyration: [25.0, 80.0, 82.0]
      draft: 22.0

    - name: "Shuttle_Tanker"
      mesh: "geometry/tanker_panels.gdf"
      position: [280.0, 15.0, 0.0]  # Side-by-side
      mass: 150000.0
      cog: [130.0, 0.0, 10.0]
      radii_of_gyration: [20.0, 65.0, 67.0]
      draft: 18.0

  environment:
    water_depth: 1200.0
    water_density: 1025.0

  analysis:
    frequencies:
      min: 0.02
      max: 1.5
      count: 40
    headings: [0, 30, 60, 90, 120, 150, 180]

  coupling:
    include_hydrodynamic: true
    include_mechanical: false  # Handled in OrcaFlex

  gap_resonance:
    analyze: true
    gap_width: 8.0
    damping_factor: 0.02  # Viscous gap damping

  output:
    directory: "results/multibody/"
    individual_results: true
    coupled_results: true
    relative_motion: true
```

### STS Operability Configuration

```yaml
# configs/sts_operability.yml

sts_operability:
  vessels:
    fpso:
      mesh: "geometry/fpso.gdf"
      loa: 300.0
      beam: 50.0
      draft: 22.0
    tanker:
      mesh: "geometry/tanker.gdf"
      loa: 250.0
      beam: 45.0
      draft: 18.0

  gap:
    width: 8.0
    longitudinal_offset: 25.0

  limits:
    relative_surge: 2.0  # m
    relative_sway: 1.5   # m
    relative_heave: 1.0  # m
    relative_roll: 2.0   # degrees
    relative_yaw: 1.0    # degrees

  sea_states:
    - hs: 1.5
      tp: 8.0
    - hs: 2.0
      tp: 9.0
    - hs: 2.5
      tp: 10.0
    - hs: 3.0
      tp: 11.0

  headings: [0, 30, 60, 90, 120, 150, 180]

  output:
    operability_envelope: true
    limiting_parameter: true
    plots: true
```

## CLI Usage

```bash
# Run multi-body analysis
python -m digitalmodel.modules.orcawave.multibody run \
    --config configs/multibody_analysis.yml \
    --output results/multibody/

# Analyze gap resonance
python -m digitalmodel.modules.orcawave.multibody gap-resonance \
    --results results/multibody/coupled.owr \
    --gap-width 8.0 \
    --output plots/gap_resonance.html

# Compute shielding factors
python -m digitalmodel.modules.orcawave.multibody shielding \
    --results results/multibody/coupled.owr \
    --shielding-body FPSO \
    --target-body Shuttle_Tanker \
    --output reports/shielding.csv

# STS operability analysis
python -m digitalmodel.modules.orcawave.multibody operability \
    --config configs/sts_operability.yml \
    --output reports/sts_operability.html

# Extract coupling matrices
python -m digitalmodel.modules.orcawave.multibody coupling \
    --results results/multibody/coupled.owr \
    --frequency 0.1 \
    --output coupling_matrices.csv
```

## Multi-Body to OrcaFlex

### Export for Time-Domain

```python
from digitalmodel.modules.orcawave.multibody import MultiBodyOrcaFlexExporter

# Export multi-body results for OrcaFlex
exporter = MultiBodyOrcaFlexExporter()

# Load multi-body results
exporter.load_results("results/multibody/coupled.owr")

# Export individual vessel types
exporter.export_vessel_types(
    output_directory="orcaflex_models/",
    include_coupling=True
)

# Export coupling data (for OrcaFlex couplings if needed)
exporter.export_coupling_data(
    output_file="orcaflex_models/coupling_data.yml"
)

# Generate OrcaFlex model template
exporter.generate_orcaflex_template(
    output_file="orcaflex_models/sts_model_template.dat",
    include_vessels=True,
    include_connections=True
)
```

## Best Practices

1. **Mesh Separation**: Ensure no mesh overlap between bodies
2. **Gap Damping**: Add viscous damping for gap resonance
3. **Frequency Resolution**: Use finer resolution near gap resonance
4. **Heading Coverage**: Include beam seas for STS analysis
5. **Relative Motion**: Focus on relative motion for operations
6. **Shielding Check**: Verify shielding assumptions in beam seas
7. **OrcaFlex Validation**: Verify multi-body response in time-domain

## Error Handling

```python
# Handle multi-body analysis errors
try:
    mb = MultiBodyAnalysis()
    mb.add_body("FPSO", "fpso.gdf", [0, 0, 0])
    mb.add_body("Tanker", "tanker.gdf", [280, 15, 0])
    results = mb.run()

except MeshOverlapError as e:
    print(f"Bodies overlap: {e}")
    # Adjust body positions

except GapTooNarrowError as e:
    print(f"Gap too narrow for reliable results: {e}")
    # Minimum gap typically 2m

except CouplingConvergenceError as e:
    print(f"Coupling calculation did not converge: {e}")
    # Reduce frequency range or check mesh quality
```

## Related Skills

- [orcawave-analysis](../orcawave-analysis/SKILL.md) - Single body diffraction
- [orcawave-mesh-generation](../orcawave-mesh-generation/SKILL.md) - Panel mesh creation
- [orcawave-to-orcaflex](../orcawave-to-orcaflex/SKILL.md) - Export to OrcaFlex
- [mooring-design](../mooring-design/SKILL.md) - Mooring system design

## References

- Faltinsen, O.M.: Sea Loads on Ships and Offshore Structures
- Newman, J.N.: Wave Effects on Deformable Bodies
- Molin, B.: On the Piston and Sloshing Modes in Moonpools
- OrcaWave Multi-Body Documentation

---

**Version History**

- **1.0.0** (2026-01-17): Initial release with STS analysis, gap resonance, and coupling matrix extraction
