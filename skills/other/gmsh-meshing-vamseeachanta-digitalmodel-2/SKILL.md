---
name: gmsh-meshing
description: Specialized AI agent for finite element mesh generation and manipulation
  using GMSH. Use for 1D/2D/3D mesh generation, geometry processing, quality assessment,
  optimization, and integration with OrcaFlex, ANSYS, and OpenFOAM.
version: 1.0.0
updated: 2025-01-02
category: cad-engineering
triggers:
- mesh generation
- finite element mesh
- GMSH
- panel mesh
- mesh quality
- mesh optimization
- STEP to mesh
- STL mesh
- mooring discretization
- structural mesh
---
# GMSH Meshing Skill

Specialized expertise for finite element mesh generation and manipulation using GMSH with quality assessment and engineering tool integration.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
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

- 1D/2D/3D mesh generation for analysis
- Geometry import and healing (STEP, IGES, STL)
- Mesh quality assessment and optimization
- Panel mesh generation for hydrodynamics
- Structural mesh for FEM analysis
- Mooring line discretization
- Batch mesh processing
- Integration with OrcaFlex, ANSYS, OpenFOAM

## Agent Capabilities

This skill integrates agent capabilities from `/agents/gmsh/`:

### Mesh Generation

| Dimension | Element Types |
|-----------|---------------|
| 1D | Beam, line, curve |
| 2D | Triangle, quadrilateral, mixed |
| 3D | Tetrahedron, hexahedron, prism, pyramid, mixed |

### Geometry Formats

| Import | Export |
|--------|--------|
| STEP, IGES, STL, BREP, GEO | MSH, VTK, CGNS, MED, INP, CDB, STL |

### Quality Metrics

| Metric | Description | Good Range | Critical |
|--------|-------------|------------|----------|
| Jacobian | Element distortion | > 0.3 | < 0.1 |
| Aspect Ratio | Element shape | < 5.0 | > 10.0 |
| Skewness | Element skew | < 0.7 | > 0.9 |
| Orthogonality | Angle quality | > 0.3 | < 0.1 |

### Optimization Methods
- Laplacian smoothing
- Adaptive refinement
- Remeshing
- Parallel optimization (up to 100 iterations)

## Prerequisites

- Python 3.10+
- GMSH Python bindings (`pip install gmsh`)
- NumPy, SciPy, PyVista

## Configuration

### Default Settings

```json
{
  "configuration": {
    "default_algorithm": "frontal-delaunay",
    "default_element_size": 1.0,
    "quality_thresholds": {
      "min_jacobian": 0.3,
      "max_aspect_ratio": 5.0,
      "max_skewness": 0.7
    },
    "performance": {
      "parallel_workers": 4,
      "chunk_size": 1000,
      "memory_limit_gb": 4
    }
  }
}
```

## Python API

### Basic Mesh Generation

```python
from digitalmodel.agents.gmsh import GMSHAgent

# Initialize agent
agent = GMSHAgent(config="agent_config.json")

# Generate mesh from geometry
mesh = agent.generate_mesh(
    geometry="platform.step",
    config={
        "algorithm": "frontal-delaunay",
        "element_size": 0.5,
        "element_type": "tetrahedron"
    }
)

# Save mesh
agent.save_mesh(mesh, "platform.msh")
```

### Quality Assessment

```python
# Assess mesh quality
quality = agent.assess_quality(mesh)

print(f"Elements: {quality['element_count']}")
print(f"Min Jacobian: {quality['min_jacobian']:.3f}")
print(f"Avg Aspect Ratio: {quality['avg_aspect_ratio']:.2f}")
print(f"Max Skewness: {quality['max_skewness']:.3f}")

# Check if optimization needed
if quality['min_jacobian'] < 0.3:
    print("Mesh requires optimization")
```

### Mesh Optimization

```python
# Optimize poor quality mesh
optimized = agent.optimize_mesh(
    mesh,
    method="laplacian_smoothing",
    iterations=10,
    quality_targets={
        "min_jacobian": 0.4,
        "max_aspect_ratio": 3.0
    }
)

# Verify improvement
quality_after = agent.assess_quality(optimized)
print(f"Jacobian improved: {quality['min_jacobian']:.3f} -> {quality_after['min_jacobian']:.3f}")
```

### Panel Mesh for Hydrodynamics

```python
# Generate panel mesh for OrcaFlex/OrcaWave
panel_mesh = agent.generate_panel_mesh(
    geometry="hull.step",
    panel_size=2.0,
    refinement_zones=["waterline", "appendages"]
)

# Export to OrcaFlex format
agent.export_to_orcaflex(panel_mesh, "hull_panels.dat")
```

### Structural Mesh for ANSYS

```python
# Generate structural mesh with boundary layers
struct_mesh = agent.generate_mesh(
    geometry="structure.step",
    element_type="hexahedron",
    boundary_layers={
        "walls": {"layers": 5, "growth_rate": 1.2}
    }
)

# Export to ANSYS with named selections
agent.export_to_ansys(
    struct_mesh,
    output="model.cdb",
    named_selections=["inlet", "outlet", "walls"]
)
```

### Batch Processing

```python
from digitalmodel.agents.gmsh.batch import GMSHBatch

# Initialize batch processor
batch = GMSHBatch(parallel=True, max_workers=4)

# Process multiple geometries
results = batch.process_directory(
    input_directory="./geometries",
    output_directory="./meshes",
    config={
        "algorithm": "frontal-delaunay",
        "element_size": {
            "min": 0.1,
            "max": 1.0
        },
        "quality_targets": {
            "min_jacobian": 0.4,
            "max_aspect_ratio": 4.0
        }
    }
)

# Generate quality report
batch.generate_report(results, "mesh_quality_report.html")
```

## Command Line Interface

```bash
# Generate mesh from geometry
python run_gmsh_agent.py generate \
    --input geometry.step \
    --output mesh.msh \
    --element-size 0.5

# Batch processing
python run_gmsh_agent.py batch \
    --input-directory ./geometries \
    --output-directory ./meshes \
    --config batch_config.yml \
    --parallel 4

# Quality assessment
python run_gmsh_agent.py assess \
    --mesh mesh.msh \
    --report quality_report.html

# Mesh optimization
python run_gmsh_agent.py optimize \
    --input mesh.msh \
    --output optimized.msh \
    --method laplacian \
    --iterations 10
```

## Integration Examples

### OrcaFlex Integration

```python
# Panel mesh for hydrodynamic analysis
panel_mesh = agent.generate_panel_mesh(
    geometry="hull.step",
    panel_size=2.0,
    refinement_zones=["waterline", "appendages"]
)

# Mooring line discretization
mooring_mesh = agent.discretize_mooring(
    length=800.0,
    segments=50,
    target_element_length=16.0
)

# Export to OrcaFlex
agent.export_to_orcaflex(panel_mesh, "hull_panels.dat")
```

### ANSYS Integration

```python
# Structural mesh with named selections
agent.export_to_ansys(
    mesh,
    output="model.cdb",
    format="CDB",
    boundary_conditions=True,
    named_selections=["fixed", "load", "contact"]
)

# Alternative INP format
agent.export_to_ansys(mesh, output="model.inp", format="INP")
```

## Templates

Pre-configured mesh templates:
- `offshore_platform.geo` - Platform mesh template
- `mooring_line.geo` - Mooring discretization
- `seabed_terrain.geo` - Seabed mesh

## MCP Tool Integration

### Swarm Coordination
```javascript
// Initialize meshing swarm
mcp__claude-flow__swarm_init { topology: "ring", maxAgents: 4 }

// Spawn specialized agents
mcp__claude-flow__agent_spawn { type: "code-analyzer", name: "mesh-generator" }
mcp__claude-flow__agent_spawn { type: "reviewer", name: "quality-checker" }
```

### Memory Coordination
```javascript
// Store mesh configuration
mcp__claude-flow__memory_usage {
  action: "store",
  key: "gmsh/mesh/config",
  namespace: "meshing",
  value: JSON.stringify({
    geometry: "hull.step",
    elements: 50000,
    quality: "verified"
  })
}

// Share mesh status with analysis agents
mcp__claude-flow__memory_usage {
  action: "store",
  key: "gmsh/mesh/ready",
  namespace: "shared",
  value: JSON.stringify({
    file: "hull_panels.dat",
    for_tool: "orcaflex",
    panels: 5000
  })
}
```

## Performance

| Operation | Metric |
|-----------|--------|
| Mesh Generation | >100K elements/second |
| Quality Assessment | <1 second for 1M elements |
| Optimization | ~10 seconds per iteration for 100K elements |
| Batch Processing | Linear scaling with CPU cores |

## Standard Workflows

### Standard Meshing Workflow
1. Import geometry
2. Heal geometry defects
3. Generate mesh
4. Assess quality
5. Optimize if needed
6. Export to desired format

### Batch Processing Workflow
1. Configure batch settings
2. Process files in parallel
3. Generate quality reports
4. Optimize poor meshes
5. Export all results

## Error Handling

### Memory Issues with Large Meshes
```python
# Use chunked processing
agent = GMSHAgent(config={
    "performance": {
        "chunk_size": 10000,
        "memory_limit_gb": 2
    }
})
```

### Poor Quality Meshes
```python
# Increase optimization iterations
optimized = agent.optimize_mesh(
    mesh,
    method="remeshing",
    iterations=20,
    quality_targets={
        "min_jacobian": 0.4,
        "max_aspect_ratio": 3.0
    }
)
```

## Related Skills

- [freecad-automation](../freecad-automation/SKILL.md) - CAD geometry creation
- [orcawave-analysis](../orcawave-analysis/SKILL.md) - Panel mesh application
- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Hydrodynamic analysis
- [structural-analysis](../structural-analysis/SKILL.md) - FEM application

## References

- GMSH Documentation: https://gmsh.info/doc/texinfo/gmsh.html
- Python API Reference: https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/api/gmsh.py
- Agent Configuration: `agents/gmsh/agent_config.json`

---

## Version History

- **1.0.0** (2025-01-02): Initial release from agents/gmsh/ configuration
