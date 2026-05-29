---
name: cad-engineering
description: Expert CAD Engineering Specialist with comprehensive knowledge of CAD
  systems, file formats, and conversion technologies. Use for CAD software guidance,
  file format conversions, technical drawings, 3D modeling, PDF to CAD conversions,
  and interoperability between open-source and proprietary CAD systems.
version: 1.0.0
updated: 2025-01-02
category: cad-engineering
triggers:
- CAD software
- file format conversion
- DWG DXF
- PDF to CAD
- FreeCAD
- LibreCAD
- OpenSCAD
- AutoCAD
- SolidWorks
- CATIA
- STEP IGES
- technical drawings
- 3D modeling
---
# CAD Engineering Skill

Expert guidance on Computer-Aided Design systems, file formats, conversion technologies, and interoperability between CAD platforms.

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

- CAD software selection and guidance
- File format conversions (DWG, DXF, STEP, IGES, etc.)
- PDF to CAD conversion strategies
- Technical drawing analysis
- 3D modeling approaches
- Open-source vs proprietary CAD decisions
- CAD automation and scripting
- Cross-platform interoperability

## Agent Capabilities

This skill integrates agent capabilities from `/agents/cad-engineering-specialist/`:

### Open-Source CAD Expertise

| Software | Capabilities |
|----------|-------------|
| **FreeCAD** | Parametric 3D modeling, Python scripting, workbench customization |
| **LibreCAD** | 2D drafting, DXF/DWG handling, command-line operations |
| **OpenSCAD** | Programmatic 3D modeling, CSG operations, parametric design |
| **QCAD** | Professional 2D CAD, scripting interface, batch processing |
| **BRL-CAD** | Solid modeling, ray-tracing, geometric analysis |
| **Blender** | CAD integration, mesh to solid conversion, technical visualization |
| **KiCAD** | PCB design, electrical schematics, 3D board visualization |

### Proprietary CAD Knowledge

| Software | Capabilities |
|----------|-------------|
| **AutoCAD** | Full command set, AutoLISP/VBA automation, custom tools |
| **SolidWorks** | Feature-based modeling, API programming, PDM integration |
| **CATIA** | V5/V6 platforms, complex surfaces, PLM workflows |
| **Inventor** | Parametric design, iLogic rules, Vault integration |
| **Fusion 360** | Cloud collaboration, generative design, CAM integration |
| **Creo/Pro-E** | Advanced assembly, mechanism design |
| **NX** | High-end manufacturing, synchronous technology |

### File Format Expertise

| Category | Formats |
|----------|---------|
| **Native** | DWG, DXF, DGN, IGES, STEP, STL, SAT, Parasolid |
| **Exchange** | IFC, COLLADA, OBJ, FBX, 3DS, VRML, X3D |
| **Documentation** | PDF, SVG, EPS, DWF, 3D PDF |

### Delegation Capability

This specialist agent delegates to software-specific agents:

```yaml
delegation:
  software_specific_agents:
    freecad:
      path: agents/freecad
      capabilities:
        - parametric_modeling
        - assembly_design
        - technical_drawings
    gmsh:
      path: agents/gmsh
      capabilities:
        - mesh_generation
        - finite_element_preprocessing
        - mesh_optimization
```

## PDF to CAD Conversion

### Conversion Strategy Selection

1. **Vector PDFs**: Direct vector extraction
2. **Scanned Drawings**: OCR and vectorization
3. **Mixed Content**: Hybrid approach
4. **Complex Cases**: Manual reconstruction

### Conversion Tools

| Category | Tools |
|----------|-------|
| **Commercial** | AutoDWG, AnyDWG, Print2CAD, Scan2CAD, pdf2cad |
| **Open-Source** | Inkscape+pstoedit, potrace, autotrace, pdf2dxf |
| **Libraries** | OpenCV, Tesseract OCR, CADLib, LibreDWG, TeighaFile |
| **Cloud Services** | Zamzar, CloudConvert, CAD Exchanger |
| **AI/ML Tools** | Deep learning drawing recognition, neural vectorization |

### PDF Analysis Workflow

```python
from digitalmodel.agents.cad import PDFAnalyzer

# Analyze PDF type
analyzer = PDFAnalyzer()
analysis = analyzer.analyze("drawing.pdf")

print(f"PDF Type: {analysis['type']}")  # vector/raster/hybrid
print(f"Creation Method: {analysis['creation_method']}")
print(f"Embedded Fonts: {analysis['fonts']}")
print(f"Layer Info: {analysis['layers']}")
print(f"Scale Detection: {analysis['detected_scale']}")

# Get conversion recommendation
recommendation = analyzer.recommend_conversion()
print(f"Recommended Tool: {recommendation['tool']}")
print(f"Expected Accuracy: {recommendation['accuracy']}")
print(f"Manual Cleanup: {recommendation['cleanup_required']}")
```

### Conversion Quality Optimization

```python
from digitalmodel.agents.cad import CADConverter

converter = CADConverter()

# Pre-processing for scanned PDFs
converter.preprocess(
    input_file="scanned_drawing.pdf",
    operations=[
        "denoise",
        "deskew",
        "contrast_enhance"
    ]
)

# Vectorization with tuned parameters
result = converter.convert(
    input_file="scanned_drawing.pdf",
    output_file="drawing.dxf",
    options={
        "line_tolerance": 0.5,
        "arc_detection": True,
        "text_recognition": True,
        "dimension_extraction": True
    }
)

# Post-processing cleanup
converter.postprocess(
    file="drawing.dxf",
    operations=[
        "remove_duplicates",
        "close_gaps",
        "standardize_layers"
    ]
)
```

## Format Conversion Examples

### STEP to DXF

```python
from digitalmodel.agents.cad import FormatConverter

converter = FormatConverter()

# Convert STEP to DXF with projection
result = converter.convert(
    input_file="model.step",
    output_file="drawing.dxf",
    projection="front",  # top, front, right, isometric
    scale=1.0,
    layer_mapping={
        "visible_edges": "0",
        "hidden_edges": "hidden",
        "dimensions": "dimensions"
    }
)
```

### DWG Version Conversion

```python
# Convert between DWG versions
result = converter.convert(
    input_file="drawing_2024.dwg",
    output_file="drawing_2010.dwg",
    target_version="2010"  # For compatibility
)
```

### Batch Format Conversion

```python
from digitalmodel.agents.cad import BatchConverter

batch = BatchConverter()

# Convert all STEP files to IGES
results = batch.convert_directory(
    input_directory="./step_files",
    output_directory="./iges_files",
    input_format="STEP",
    output_format="IGES",
    parallel=True,
    workers=4
)

# Generate conversion report
batch.generate_report(results, "conversion_report.html")
```

## Technical Drawing Analysis

```python
from digitalmodel.agents.cad import DrawingAnalyzer

analyzer = DrawingAnalyzer()

# Analyze technical drawing
analysis = analyzer.analyze("technical_drawing.dxf")

# Extract information
print(f"Drawing Scale: {analysis['scale']}")
print(f"Units: {analysis['units']}")
print(f"Layers: {analysis['layers']}")
print(f"Blocks: {analysis['blocks']}")
print(f"Dimensions: {len(analysis['dimensions'])}")
print(f"Text Annotations: {len(analysis['text'])}")

# Validate against standards
validation = analyzer.validate(
    standard="ISO",  # or "ANSI", "DIN", "JIS"
    checks=["layer_naming", "line_types", "dimensions"]
)
```

## MCP Tool Integration

### Swarm Coordination
```javascript
// Initialize CAD expertise swarm
mcp__claude-flow__swarm_init { topology: "hierarchical", maxAgents: 5 }

// Spawn specialized agents
mcp__claude-flow__agent_spawn { type: "analyst", name: "format-analyzer" }
mcp__claude-flow__agent_spawn { type: "coder", name: "converter" }
mcp__claude-flow__agent_spawn { type: "reviewer", name: "quality-checker" }
```

### Memory Coordination
```javascript
// Store conversion configuration
mcp__claude-flow__memory_usage {
  action: "store",
  key: "cad/conversion/config",
  namespace: "cad",
  value: JSON.stringify({
    source_format: "PDF",
    target_format: "DXF",
    method: "vectorization",
    accuracy_target: 0.95
  })
}
```

## Best Practices

### Format Selection
1. **STEP**: Best for 3D geometry exchange
2. **IGES**: Legacy support, use STEP when possible
3. **DXF**: Best for 2D CAD interoperability
4. **STL**: 3D printing and visualization only

### Conversion Quality
1. Always verify dimensional accuracy after conversion
2. Check for missing entities (arcs, splines, text)
3. Validate layer structure preservation
4. Test with small sample before batch processing

### Automation
1. Use Python scripting for repeatable tasks
2. Create conversion templates for standard workflows
3. Implement quality checks in CI/CD pipelines
4. Document conversion parameters for reproducibility

## Common Issues

### Lossy Conversions
```python
# Check for conversion losses
losses = converter.check_losses(
    original="model.step",
    converted="model.iges"
)

if losses["geometry_count_diff"] > 0:
    print(f"Lost {losses['geometry_count_diff']} entities")
if losses["accuracy_loss"] > 0.01:
    print(f"Accuracy loss: {losses['accuracy_loss']*100:.1f}%")
```

### Version Compatibility
```python
# Check format version before conversion
info = converter.get_format_info("drawing.dwg")
print(f"DWG Version: {info['version']}")
print(f"Created By: {info['application']}")
print(f"Compatible With: {info['compatible_versions']}")
```

## Related Skills

- [freecad-automation](../freecad-automation/SKILL.md) - FreeCAD operations
- [gmsh-meshing](../gmsh-meshing/SKILL.md) - Mesh generation from CAD
- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Marine analysis integration
- [structural-analysis](../structural-analysis/SKILL.md) - FEM preprocessing

## References

- DWG/DXF Specification: Open Design Alliance
- STEP Standard: ISO 10303
- IGES Standard: ASME Y14.26M
- Agent Configuration: `agents/cad-engineering-specialist/agent.yaml`

---

## Version History

- **1.0.0** (2025-01-02): Initial release from agents/cad-engineering-specialist/ configuration
