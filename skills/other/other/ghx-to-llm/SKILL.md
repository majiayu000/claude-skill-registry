---
name: ghx-to-llm
description: Convert GHX files to LLM-readable format and generate RAG summaries. Use when users mention GHX, Grasshopper definition, .ghx files, convert for LLM, document Grasshopper, or RAG context for parametric workflows.
trigger: manual
---

# GHX to LLM Converter

Convert Grasshopper `.ghx` files into two complementary outputs for LLM understanding and RAG retrieval.

## How to Use This Skill

1. User provides path to `.ghx` file
2. Run Python converter script → creates `{name}_ghx-to-llm.md`
3. Analyze conversion output → create `{name}_ghx-summary.md`
4. Both files saved to same folder as input

## When to Use This Skill

- User invokes `/ghx-to-llm [path]`
- User asks to convert/document a Grasshopper file
- Creating RAG context for GH definitions
- Preparing GH workflows for LLM analysis

## CLI Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/ghx_to_llm.py` | Convert .ghx to LLM-readable markdown | `python scripts/ghx_to_llm.py input.ghx [-o output.md]` |

**Script options:**
- `input` - Path to .ghx file (required)
- `-o, --output` - Custom output path (default: `{input}_ghx-to-llm.md`)
- `--stdout` - Print to console instead of file

## Output Files

| Input | Output 1 (Phase 1) | Output 2 (Phase 2) |
|-------|--------------------|--------------------|
| `Task_01.ghx` | `Task_01_ghx-to-llm.md` | `Task_01_ghx-summary.md` |

## Example Workflow

```bash
# Phase 1: Convert (from skill folder)
python .claude/skills/ghx-to-llm/scripts/ghx_to_llm.py "path/to/Definition.ghx"
# Output: path/to/Definition_ghx-to-llm.md

# Phase 2: Summarize (LLM reads conversion, writes summary)
# Read the _ghx-to-llm.md file
# Create: path/to/Definition_ghx-summary.md
```

## Critical Requirements

- **Input format**: Must be `.ghx` (XML-based), not binary `.gh`
- **Python**: 3.8+ with standard library only (no external dependencies)
- **Better output**: Groups in Grasshopper improve output structure significantly
- **Cluster internals** (optional): Requires .NET 8+ SDK and Rhino 8 installed (for `GH_IO.dll`). Without these, clusters still appear as labeled components with I/O, but the `## CLUSTERS` section showing internal components is skipped

## Quick Decision Tree

```
Have a .ghx file to document?
├── Want raw component data? → Phase 1 only (run script)
└── Want semantic summary? → Full workflow (both phases)

Have a .gh (binary) file?
└── Save as .ghx in Grasshopper first (File → Save As)
```

## Phase 1: Conversion Output Format

The converter produces structured markdown with:
- Component groups as `## GROUP` sections
- Wire connections between components
- Parameter values (sliders, toggles, panels)
- Data flow references (e.g., `5.1` = component 5, output 1)
- Modifiers: F=Flatten, G=Graft, S=Simplify, R=Reverse
- Clusters labeled as `Cluster"Name"[I/O]` with descriptions
- `## CLUSTERS` section showing internal components of each cluster (requires .NET + Rhino 8)

## Phase 2: Summary Structure Template

After reading the `_ghx-to-llm.md` file, create a semantic summary:

```markdown
# {Filename} - Grasshopper Definition Summary

## Purpose
[What this definition calculates or produces - 1-2 sentences]

## Required Setup
- **Rhino Layers:** [List layers with expected geometry types]
- **Plugins:** [List required Grasshopper plugins]

## Workflow Logic
[Plain language description of how data flows through the definition]

1. **[Stage Name]**: [What happens and why]
2. **[Stage Name]**: [What happens and why]
...

## Key Parameters
| Parameter | Default | Effect |
|-----------|---------|--------|
| [Name] | [Value] | [What changing it does] |

## Key Calculations
[Any important formulas or operations, explained in context]

## Output
[What the definition produces and how to interpret results]
```

## Analysis Guidelines

When creating the Phase 2 summary:

1. **Extract Purpose** - Look at output groups and final calculations
2. **Trace Data Flow** - Follow group sequence and connections
3. **Identify Parameters** - Find all Number Sliders, Boolean Toggles, editable Panels
4. **Explain Calculations** - Translate mathematical component chains into formulas
5. **Note Dependencies** - Identify required Rhino geometry and GH plugins

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| "File not found" | Wrong path | Use absolute path or verify relative path |
| Empty output | No components in file | Verify .ghx has content in Grasshopper |
| Missing connections | Unnamed groups | Add descriptive group names in Grasshopper |
| XML parse error | Corrupted or binary file | Re-save as .ghx from Grasshopper |
| Plugin components show as unknown | Third-party plugins | Component type name still captured; note plugin in summary |
| Encoding errors on Windows | Console encoding | Script handles this automatically |

## Boundaries

This skill should NOT:
- Modify the original `.ghx` file
- Generate Grasshopper component code
- Skip either output phase (both files are required for complete documentation)
- Include excessive technical detail in the summary (focus on intent and usage)
