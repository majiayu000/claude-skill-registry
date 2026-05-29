---
name: abaqus-odb
description: Read analysis results. Use when user asks about maximum stress, extracting displacements, reaction forces, or exporting results. Post-processes ODB files.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Bash(python:*)
---

# Abaqus ODB Skill

This skill reads and extracts analysis results from Abaqus ODB files.

## When to Use This Skill

**Route here when user mentions:**
- "What is the maximum stress?", "extract displacement"
- "Get reaction forces", "post-process the ODB"
- "Export results to CSV", "what are the eigenfrequencies?"

**Route elsewhere:**
- Running the analysis → `/abaqus-job`
- Configuring what output to save → `/abaqus-output`
- Exporting geometry (STL, STEP) → `/abaqus-export`

## Key Decisions

### 1. What Result is Needed?

| Need | Field | Notes |
|------|-------|-------|
| Displacement | `U` | Use `.magnitude` for total |
| Stress | `S` | Use `.mises` for von Mises |
| Reaction force | `RF` | Sum components for total |
| Strain | `E` | Similar structure to stress |
| Temperature | `NT` | Thermal analysis results |
| Eigenfrequency | Frame description | Parse from frame metadata |

### 2. Which Step/Frame?

| Scenario | Frame Selection |
|----------|-----------------|
| Final results | `step.frames[-1]` |
| All time history | Loop all frames |
| Specific time | Find by `frameValue` |
| Modal analysis | Each frame = mode |

### 3. Location: Global Max or Specific?

| Need | Approach |
|------|----------|
| Overall maximum | Loop all values, find max |
| Specific node | Filter by `nodeLabel` |
| Subset/region | Use `getSubset(region=...)` |

### 4. Export Format?

| Format | Use Case |
|--------|----------|
| Print to console | Quick check |
| CSV file | Spreadsheet analysis |
| Text report | Documentation |

## What to Ask User

If unclear, ask:
1. **What result?** Stress, displacement, reaction force, frequency?
2. **Which step/frame?** Final, specific time, or all?
3. **Location?** Maximum anywhere, or specific node/region?
4. **Output format?** Print, CSV, or report?

## Workflow

1. **Open ODB** - Use `readOnly=True` for extraction
2. **Navigate to step/frame** - List steps with `odb.steps.keys()`
3. **Get field output** - Access via `frame.fieldOutputs['U']`
4. **Extract values** - Loop `field.values`, use `.magnitude`, `.mises`
5. **Close ODB** - Always close when done

## Common Tasks

| Task | Approach |
|------|----------|
| Max displacement | Loop U values, find max magnitude |
| Max von Mises stress | Loop S values, find max mises |
| Total reaction force | Sum RF components across all nodes |
| Displacement at node | Filter by nodeLabel |
| Results in region | Use getSubset with node/element set |
| Eigenfrequencies | Parse frame.description in frequency step |
| Time history | Use historyRegions and historyOutputs |
| Export to CSV | Write values with csv module |

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "ODB locked" | Another process has it | Delete `.lck` file |
| "Key not found" | Wrong variable name | List available keys first |
| "No values" | Output not requested | Check FieldOutputRequest in model |
| "AttributeError: mises" | Element has no mises | Check element formulation |

## Code Patterns

For API syntax and code examples, see:
- [ODB Extraction Patterns](references/extraction-patterns.md)
- [Common Queries](references/common-queries.md)
- [Export Templates](references/export-templates.md)
