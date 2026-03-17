---
name: freecad-automation
description: AI-powered automation agent for FreeCAD CAD operations including natural
  language processing, batch processing, parametric design, and marine engineering
  applications. Use for CAD automation, drawing generation, FEM preprocessing, and
  integration with offshore analysis tools.
version: 1.0.0
updated: 2025-01-02
category: cad-engineering
triggers:
- FreeCAD automation
- parametric modeling
- CAD batch processing
- technical drawings
- assembly management
- FEM preprocessing
- hull design
- marine CAD
- .FCStd files
- Python scripting CAD
---
# FreeCAD Automation Skill

AI-powered automation for FreeCAD CAD operations with natural language processing, batch processing, and marine engineering specialization.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  cad-engineering: '>=1.0.0,<2.0.0'
  gmsh-meshing: '>=1.0.0,<2.0.0'
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

- CAD automation and scripting
- Batch processing of FreeCAD files
- Parametric design and design tables
- Assembly management and constraint solving
- FEM preprocessing and mesh generation
- Drawing generation with automatic dimensioning
- Marine engineering hull design
- Natural language CAD commands
- Integration with OrcaFlex/AQWA workflows

## Agent Capabilities

This skill integrates agent capabilities from `/agents/freecad/`:

### Core Capabilities
- **CAD Automation**: Script-based FreeCAD operations
- **Batch Processing**: Parallel file processing with pattern matching
- **Parametric Design**: Design tables and parameter variations
- **Assembly Management**: Constraint solving and assembly creation
- **FEM Preprocessing**: Mesh generation and boundary conditions
- **Drawing Generation**: Automatic dimensioning and views
- **Natural Language Processing**: Convert commands to CAD operations
- **Script Generation**: Auto-generate Python scripts from prompts

### Marine Engineering Specialization
- Hull design automation
- Stability calculations
- Mooring system configuration
- Structural analysis preprocessing

### Integration Points
- **OrcaFlex**: Data exchange for hydrodynamic analysis
- **AQWA**: Diffraction analysis geometry
- **Signal Analysis**: Module connectivity
- **REST API**: External system integration

## Prerequisites

- Python 3.8+
- FreeCAD 1.0+ (November 2024 release)
- `digitalmodel` package installed

## Configuration

### Agent Settings

```json
{
  "settings": {
    "parallel_workers": 4,
    "max_workers": 8,
    "cache_enabled": true,
    "cache_size_mb": 500,
    "auto_save": true,
    "auto_save_interval": 300,
    "validation_level": "strict",
    "error_recovery": true,
    "retry_attempts": 3,
    "timeout_seconds": 600
  }
}
```

### Marine Engineering Settings

```json
{
  "marine_engineering": {
    "units": "metric",
    "standards": ["DNV", "ABS", "API"],
    "vessel_types": ["FPSO", "FSO", "FLNG", "Semi-sub", "TLP", "Spar"],
    "analysis_types": ["stability", "mooring", "structural", "hydrodynamic"]
  }
}
```

## Python API

### Basic Operations

```python
from digitalmodel.agents.freecad import FreeCADAgent

# Initialize agent
agent = FreeCADAgent()

# Natural language operation
result = agent.execute_prompt("Create a box 100x50x25mm with chamfered edges")

# Check result
print(f"Created: {result['object_name']}")
print(f"Volume: {result['properties']['volume']} mm3")
```

### Batch Processing

```python
# Batch processing with pattern matching
results = agent.batch_process(
    pattern="*.FCStd",
    input_directory="./models",
    operation="export_step",
    parallel_workers=4
)

# Process results
for file_name, result in results.items():
    if result["success"]:
        print(f"Exported: {file_name}")
    else:
        print(f"Failed: {file_name} - {result['error']}")
```

### Parametric Design

```python
# Generate parametric variations
agent.parametric_study(
    base_model="hull_template.FCStd",
    parameters={
        "length": [150, 175, 200, 225],
        "beam": [25, 30, 35],
        "draft": [10, 12, 15]
    },
    output_directory="hull_variations/",
    export_formats=["STEP", "STL"]
)
```

### Script Generation

```python
# Generate Python script from natural language
script = agent.generate_script(
    "Create parametric gear with 20 teeth, module 2mm,
     pressure angle 20 degrees, exportable to STEP"
)

# Save script
with open("gear_generator.py", "w") as f:
    f.write(script)

# Execute script
exec(script)
```

### Hull Design Automation

```python
from digitalmodel.agents.freecad.marine import HullDesigner

# Initialize hull designer
hull = HullDesigner()

# Create hull from parameters
hull_model = hull.create(
    length=280.0,
    beam=48.0,
    depth=26.0,
    draft=18.0,
    block_coefficient=0.85,
    hull_type="FPSO"
)

# Generate panel mesh for hydrodynamics
hull.generate_panel_mesh(
    model=hull_model,
    panel_size=2.0,
    output_file="hull_panels.dat"
)

# Export for OrcaFlex
hull.export_orcaflex(
    model=hull_model,
    output_file="orcaflex_models/fpso_hull.yml"
)
```

## Command Line Interface

```bash
# Show capabilities
python run_freecad_agent.py --show-capabilities

# Process single file
python run_freecad_agent.py --file model.FCStd --operation "add fillet radius 5mm"

# Batch processing
python run_freecad_agent.py \
    --pattern "*.FCStd" \
    --input-directory ./models \
    --output-directory ./exports \
    --parallel 4

# Natural language command
python run_freecad_agent.py \
    --prompt "Create a hull with 150m length and 25m beam"
```

## Batch Processing Patterns

| Pattern | Description |
|---------|-------------|
| `*.FCStd` | All FreeCAD files |
| `*_asm.FCStd` | Assembly files |
| `*_part.FCStd` | Part files |
| `*_drw.FCStd` | Drawing files |

## Output Formats

Supported export formats:
- **STEP** - Standard for CAD exchange
- **IGES** - Legacy CAD exchange
- **STL** - 3D printing, mesh applications
- **DXF** - 2D drawings
- **PDF** - Technical documentation

## MCP Tool Integration

### Swarm Coordination
```javascript
// Initialize CAD processing swarm
mcp__claude-flow__swarm_init { topology: "star", maxAgents: 4 }

// Spawn specialized agents
mcp__claude-flow__agent_spawn { type: "coder", name: "freecad-automator" }
mcp__claude-flow__agent_spawn { type: "reviewer", name: "geometry-validator" }
```

### Memory Coordination
```javascript
// Store CAD operation status
mcp__claude-flow__memory_usage {
  action: "store",
  key: "freecad/batch/status",
  namespace: "cad",
  value: JSON.stringify({
    operation: "batch_export",
    files_processed: 45,
    files_total: 100,
    format: "STEP"
  })
}

// Share geometry with analysis agents
mcp__claude-flow__memory_usage {
  action: "store",
  key: "freecad/geometry/hull",
  namespace: "shared",
  value: JSON.stringify({
    file: "hull_panels.dat",
    panels: 5000,
    ready_for_analysis: true
  })
}
```

## Performance Metrics

| Metric | Value |
|--------|-------|
| Batch Processing | Up to 5x faster than sequential |
| Memory Optimization | Efficient large assembly handling |
| Error Recovery | Automatic retry with exponential backoff |
| Caching | Intelligent operation caching |

## Error Handling

### FreeCAD Import Error
```python
# Add FreeCAD to Python path
import sys
sys.path.append('/path/to/FreeCAD/lib')
```

### Memory Issues
```python
# Reduce parallel workers for large files
agent = FreeCADAgent(config={
    "settings": {
        "parallel_workers": 2,
        "memory_limit_mb": 2048
    }
})
```

## Related Skills

- [gmsh-meshing](../gmsh-meshing/SKILL.md) - Advanced mesh generation
- [cad-engineering](../cad-engineering/SKILL.md) - General CAD expertise
- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Hydrodynamic analysis integration
- [aqwa-analysis](../aqwa-analysis/SKILL.md) - Panel mesh for diffraction

## References

- FreeCAD Documentation: https://wiki.freecadweb.org/
- FreeCAD Python API: https://wiki.freecadweb.org/Python_scripting_tutorial
- Agent Configuration: `agents/freecad/agent_config.json`

---

## Version History

- **1.0.0** (2025-01-02): Initial release from agents/freecad/ configuration
