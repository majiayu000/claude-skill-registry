---
name: orcawave-mesh-generation
description: Panel mesh generation and optimization specialist for OrcaWave diffraction analysis.
  Handles CAD-to-panel mesh conversion, mesh quality validation, convergence studies,
  and GDF file generation for hydrodynamic computations.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- panel mesh generation
- OrcaWave mesh
- GDF file creation
- mesh convergence study
- waterline refinement
- mesh quality validation
- CAD to panel mesh
- STL to GDF conversion
- mesh aspect ratio
- watertight mesh
---

# OrcaWave Mesh Generation Skill

Specialized expertise for generating and optimizing panel meshes for OrcaWave diffraction/radiation analysis.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  gmsh: '>=4.11.0'
  numpy: '>=1.24.0'
  trimesh: '>=3.20.0'
orcawave_version: '>=11.0'
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

## When to Use

- Converting CAD geometry (STL, OBJ, STEP) to OrcaWave panel mesh
- Generating GDF (Geometry Definition File) for OrcaWave
- Running mesh convergence studies
- Validating mesh quality (watertight, normals, aspect ratio)
- Optimizing waterline panel refinement
- Checking symmetry and enforcing port/starboard symmetry
- Preparing multi-body meshes with proper separation

## Core Capabilities

### Geometry Import
- **STL Import**: Triangulated surface meshes
- **OBJ Import**: Wavefront object files
- **STEP/IGES Import**: CAD solid models (via FreeCAD/gmsh)
- **GDF Import/Export**: OrcaWave native format

### Mesh Generation
- **Panel Discretization**: Quadrilateral and triangular panels
- **Waterline Refinement**: Finer mesh near free surface
- **Symmetry Handling**: Port/starboard symmetry detection and enforcement
- **Multi-body Meshing**: Separate meshes for coupled analysis

### Quality Validation
- **Watertight Check**: Closed surface validation
- **Normal Orientation**: Outward-pointing normals
- **Aspect Ratio**: Panel shape quality (target < 3:1)
- **Skewness**: Panel distortion metrics
- **Panel Count**: Optimal range 1000-5000 panels

## Python API

### Basic Mesh Generation

```python
from digitalmodel.modules.orcawave.mesh import OrcaWaveMeshGenerator

# Initialize generator
generator = OrcaWaveMeshGenerator()

# Load CAD geometry
generator.load_geometry("geometry/hull.stl")

# Generate panel mesh
mesh = generator.generate_mesh(
    target_panels=3000,
    waterline_refinement=1.5,  # Refinement factor at waterline
    symmetry="port-starboard",
    max_aspect_ratio=3.0
)

# Validate mesh quality
validation = generator.validate_mesh(mesh)
print(f"Quality score: {validation['quality_score']:.2f}")
print(f"Panel count: {validation['panel_count']}")
print(f"Watertight: {validation['is_watertight']}")

# Export to GDF
generator.export_gdf(mesh, "output/hull_panels.gdf")
```

### Mesh Convergence Study

```python
from digitalmodel.modules.orcawave.mesh_study import MeshConvergenceStudy

# Initialize study
study = MeshConvergenceStudy()

# Define mesh sizes to test
mesh_configs = [
    {"target_panels": 500, "label": "coarse"},
    {"target_panels": 1000, "label": "medium"},
    {"target_panels": 2000, "label": "fine"},
    {"target_panels": 4000, "label": "very_fine"},
]

# Run convergence study
results = study.run(
    geometry="geometry/hull.stl",
    mesh_configs=mesh_configs,
    reference_frequency=0.1,  # rad/s
    output_directory="results/mesh_convergence/"
)

# Analyze convergence
convergence = study.analyze_convergence(results)
print(f"Recommended panels: {convergence['recommended_panels']}")
print(f"Convergence achieved: {convergence['is_converged']}")

# Generate HTML report
study.generate_report(
    results,
    output_file="results/mesh_convergence_report.html"
)
```

### STL to GDF Conversion

```python
from digitalmodel.modules.orcawave.converters import STLtoGDFConverter

# Initialize converter
converter = STLtoGDFConverter()

# Convert with options
converter.convert(
    input_file="geometry/hull.stl",
    output_file="geometry/hull.gdf",
    options={
        "scale_factor": 1.0,  # mm to m if needed
        "translate_to_origin": True,
        "enforce_symmetry": True,
        "flip_normals": False,
        "target_panels": 3000
    }
)

# Validate output
validation = converter.validate_gdf("geometry/hull.gdf")
```

### Waterline Refinement

```python
from digitalmodel.modules.orcawave.mesh import WaterlineRefiner

# Initialize refiner
refiner = WaterlineRefiner()

# Load existing mesh
refiner.load_mesh("geometry/hull_coarse.gdf")

# Apply waterline refinement
refined_mesh = refiner.refine(
    waterline_z=0.0,  # Waterline elevation
    refinement_band=2.0,  # meters above/below waterline
    refinement_factor=2.0,  # 2x finer at waterline
    preserve_symmetry=True
)

# Export refined mesh
refiner.export_gdf(refined_mesh, "geometry/hull_refined.gdf")
```

## Configuration Examples

### Standard Mesh Generation

```yaml
# configs/mesh_generation.yml

mesh_generation:
  input:
    file: "geometry/fpso_hull.stl"
    format: "stl"
    units: "meters"

  parameters:
    target_panels: 3000
    max_panels: 5000
    min_panels: 1000

  waterline:
    elevation: 0.0
    refinement_band: 3.0  # meters
    refinement_factor: 1.5

  quality:
    max_aspect_ratio: 3.0
    max_skewness: 0.5
    enforce_watertight: true

  symmetry:
    type: "port-starboard"
    tolerance: 0.01  # meters

  output:
    format: "gdf"
    directory: "output/meshes/"
    filename: "fpso_panels.gdf"
```

### Convergence Study Configuration

```yaml
# configs/convergence_study.yml

convergence_study:
  geometry: "geometry/vessel.stl"

  mesh_levels:
    - panels: 500
      label: "Level 1 (Coarse)"
    - panels: 1000
      label: "Level 2"
    - panels: 2000
      label: "Level 3"
    - panels: 4000
      label: "Level 4 (Fine)"
    - panels: 8000
      label: "Level 5 (Very Fine)"

  analysis:
    frequencies: [0.05, 0.1, 0.2, 0.5]
    directions: [0, 90, 180]

  convergence_criteria:
    tolerance: 0.02  # 2% change between levels
    metric: "heave_rao_peak"

  output:
    directory: "results/convergence/"
    generate_plots: true
    generate_report: true
```

## Quality Metrics

### Panel Quality Thresholds

| Metric | Excellent | Good | Acceptable | Poor |
|--------|-----------|------|------------|------|
| Aspect Ratio | < 2.0 | < 3.0 | < 5.0 | >= 5.0 |
| Skewness | < 0.3 | < 0.5 | < 0.7 | >= 0.7 |
| Panel Count | 2000-4000 | 1000-5000 | 500-8000 | < 500 or > 10000 |
| Quality Score | > 0.9 | > 0.7 | > 0.5 | <= 0.5 |

### Validation Checks

```python
from digitalmodel.modules.diffraction.geometry_quality import GeometryQualityChecker

# Initialize checker
checker = GeometryQualityChecker()

# Run all quality checks
results = checker.validate(
    mesh_file="geometry/hull.gdf",
    checks=[
        "watertight",
        "normal_orientation",
        "aspect_ratio",
        "skewness",
        "panel_count",
        "symmetry",
        "waterline_intersection"
    ]
)

# Check results
for check, result in results.items():
    status = "PASS" if result["passed"] else "FAIL"
    print(f"{check}: {status} - {result['message']}")
```

## CLI Usage

```bash
# Generate mesh from STL
python -m digitalmodel.modules.orcawave.mesh generate \
    --input geometry/hull.stl \
    --output geometry/hull.gdf \
    --panels 3000 \
    --symmetry port-starboard

# Validate existing mesh
python -m digitalmodel.modules.orcawave.mesh validate \
    --input geometry/hull.gdf \
    --report validation_report.html

# Run convergence study
python -m digitalmodel.modules.orcawave.mesh convergence \
    --geometry geometry/hull.stl \
    --levels 500,1000,2000,4000 \
    --output results/convergence/

# Convert STL to GDF
python -m digitalmodel.modules.orcawave.converters stl-to-gdf \
    --input geometry/hull.stl \
    --output geometry/hull.gdf \
    --scale 0.001  # mm to m
```

## Integration with gmsh-meshing Skill

For advanced meshing requirements, combine with the gmsh-meshing skill:

```python
from digitalmodel.modules.gmsh.mesh_generator import GmshMeshGenerator
from digitalmodel.modules.orcawave.converters import GmshToGDFConverter

# Generate high-quality mesh with gmsh
gmsh_gen = GmshMeshGenerator()
gmsh_mesh = gmsh_gen.generate(
    geometry="geometry/hull.step",
    element_size=0.5,
    refinement_fields=["waterline", "bilge_keel"]
)

# Convert to OrcaWave GDF format
converter = GmshToGDFConverter()
converter.convert(gmsh_mesh, "geometry/hull.gdf")
```

## Best Practices

1. **Start Coarse**: Begin with 500-1000 panels for initial testing
2. **Convergence First**: Always run convergence study before production
3. **Waterline Focus**: Finer mesh near waterline improves accuracy
4. **Symmetry**: Use symmetry when applicable to reduce computation
5. **Quality Check**: Validate mesh quality before running analysis
6. **Panel Count**: Optimal range is 2000-4000 for most vessels
7. **Aspect Ratio**: Keep below 3:1 for accurate results

## Error Handling

### Common Issues

```python
# Handle non-watertight geometry
try:
    mesh = generator.generate_mesh("geometry/hull.stl")
except MeshNotWatertightError as e:
    print(f"Geometry not watertight: {e}")
    # Attempt auto-heal
    mesh = generator.generate_mesh(
        "geometry/hull.stl",
        auto_heal=True,
        heal_tolerance=0.01
    )

# Handle symmetry issues
try:
    mesh = generator.generate_mesh(
        "geometry/hull.stl",
        symmetry="port-starboard"
    )
except SymmetryViolationError as e:
    print(f"Symmetry violation: {e}")
    # Generate without symmetry enforcement
    mesh = generator.generate_mesh(
        "geometry/hull.stl",
        symmetry=None
    )
```

## Related Skills

- [orcawave-analysis](../orcawave-analysis/SKILL.md) - Main diffraction analysis
- [gmsh-meshing](../gmsh-meshing/SKILL.md) - Advanced mesh generation
- [freecad-automation](../freecad-automation/SKILL.md) - CAD geometry preparation
- [cad-engineering](../cad-engineering/SKILL.md) - CAD file format handling

## References

- OrcaWave GDF File Format Specification
- Orcina Panel Method Documentation
- WAMIT Manual (GDF format compatibility)
- Lee, C.H.: WAMIT Theory Manual

---

**Version History**

- **1.0.0** (2026-01-17): Initial release with mesh generation, validation, and convergence study capabilities
