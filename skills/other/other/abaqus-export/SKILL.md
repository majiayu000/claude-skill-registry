---
name: abaqus-export
description: Export Abaqus geometry and results. Use when user mentions exporting to STL, STEP, CSV, or generating input files for external use.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Export Skill

Export geometry and results from Abaqus to external formats for 3D printing, CAD exchange, data analysis, or archival.

## When to Use This Skill

**Route here when user mentions:**
- "Export to STL" / "Convert to STL" / "3D printing"
- "Save as STEP" / "Export to CAD"
- "Generate input file" / "Write INP"
- "Export results to CSV" / "Export to Excel"
- "Save the mesh" / "Extract mesh data"
- "Export deformed shape" / "Export topology result"

**Route elsewhere:**
- Reading ODB results → `/abaqus-odb`
- Importing CAD files → `/abaqus-geometry`
- Running analysis → `/abaqus-job`

## Key Decisions

### What Format to Use?

| Need | Format | Requires |
|------|--------|----------|
| 3D printing | STL (double precision) | Meshed part |
| CAD exchange | STEP | Part geometry |
| Legacy CAD | IGES | Part geometry |
| Data analysis | CSV | ODB file |
| Archive/HPC | INP | Complete model |
| Reports/images | PNG/SVG | GUI session |

### What to Export?

| Source | Available Formats |
|--------|------------------|
| Part geometry | STL, STEP, IGES, SAT |
| Assembly | STL, SAT |
| Mesh data | CSV (nodes, elements) |
| Results (U, S, RF) | CSV |
| Time history | CSV |
| Model definition | INP |
| Topology result | STL (with density threshold) |

## What to Ask User

If unclear, ask:
1. **What format?** STL, STEP, CSV, INP?
2. **What to export?** Geometry, mesh, or results?
3. **Which parts/steps?** Specific part name, all parts, specific time step?
4. **For TO results:** What density threshold? (0.3-0.5 typical)

## Workflow

### Exporting Geometry (STL/STEP/IGES)

1. **Identify the part** - Get part name from model
2. **Check if meshed** - STL requires mesh; STEP works on geometry
3. **Call export method** - Use appropriate API call
4. **Verify output** - Check file was created

### Exporting Results to CSV

1. **Open the ODB** - Use `openOdb()` with `readOnly=True`
2. **Navigate to frame** - Find correct step and frame (typically last)
3. **Extract field output** - U (displacement), S (stress), etc.
4. **Write CSV** - Loop through values, write rows
5. **Close ODB** - Always close when done

### Generating Input File

1. **Create job object** - Job needs model name
2. **Call writeInput()** - Creates `JobName.inp`
3. **Verify INP created** - Check file exists

### Exporting TO Result

1. **Locate TO ODB** - Usually `Optimization/TOSCA_POST/Optimization.odb`
2. **Set density threshold** - 0.3-0.5 typical (lower = more material)
3. **Export STL** - Use session method or GUI

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "Cannot write STL - no mesh" | Part not meshed | Mesh part first |
| "STEP export failed" | Invalid geometry | Try IGES or SAT |
| Large STL file | Fine mesh | Coarsen mesh for viz |
| Permission denied | File open elsewhere | Close file first |
| Image export fails | noGUI mode | Run with GUI |

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
