---
name: scad-load
description: |
  Loads OpenSCAD files with full dependency context by parsing use/include statements,
  resolving library paths, and extracting API surface (modules, functions, parameters).
  Use when working with OpenSCAD files, debugging rendering issues, understanding module
  dependencies, or before refactoring. Triggers on "load scad", "scad-load [file]",
  "load openscad context", "show scad dependencies", or when investigating .scad files.
  Works with .scad files, BOSL2, woodworkers-lib, NopSCADlib, and project-specific libraries.

---

# scad-load

## Quick Start

Load an OpenSCAD file with all its dependencies:

```bash
# Load main file with dependency tree
/scad-load workshop/workbenches/mini-workbench.scad

# Output includes:
# - Dependency tree visualization
# - Available modules and functions
# - Customizer parameters
# - Configuration variables
# - File locations (project lib/, system libraries/)
```

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Instructions
   3.1. Load OpenSCAD File
   3.2. Parse Dependencies
   3.3. Extract API Surface
   3.4. Present Context Summary
4. Supporting Files
5. Expected Outcomes
6. Requirements
7. Red Flags to Avoid

## When to Use This Skill

### Explicit Triggers
- User says: "load scad [file]"
- User says: "/scad-load [file]"
- User says: "load openscad context for [file]"
- User says: "show dependencies for [file]"

### Implicit Triggers
- Before modifying OpenSCAD files (understand context first)
- Debugging rendering errors (check dependency chain)
- Understanding module availability (what can be called)
- Investigating missing function errors
- Planning refactoring work

### Debugging Scenarios
- "Module X is undefined" errors → check dependency tree
- "Variable Y is undef" → verify include vs use
- Circular dependency suspected → detect loops
- Library path issues → resolve library locations

## What This Skill Does

This skill provides systematic OpenSCAD file context loading:

1. **Read target file** - Load specified .scad file
2. **Parse dependencies** - Extract use/include statements recursively
3. **Resolve paths** - Find files in project lib/, system libraries/, relative paths
4. **Extract API** - Identify modules, functions, customizer parameters, variables
5. **Detect issues** - Circular dependencies, missing files, path resolution failures
6. **Present summary** - Structured overview with dependency tree and API surface

## Instructions

### 3.1. Load OpenSCAD File

**Read the specified file:**

```bash
# User provides path (absolute or relative to project root)
file_path = "workshop/workbenches/mini-workbench.scad"

# Read file
Read file_path
```

**Extract metadata:**
- File path (absolute)
- File size
- Module name (from filename)
- First-level use/include statements

### 3.2. Parse Dependencies

**Extract include/use statements:**

Use Grep to find dependency statements:

```bash
# Find all use/include statements
grep -E '^\s*(use|include)\s*<' file_path

# Example matches:
# use <BOSL2/std.scad>
# include <../../lib/assembly-framework.scad>
# use <woodworkers-lib/std.scad>
```

**Resolve paths:**

Apply OpenSCAD path resolution rules:

1. **Angle brackets `<lib/file.scad>`:**
   - Check project `lib/` directory first
   - Check `~/Documents/OpenSCAD/libraries/` (macOS)
   - Check `~/.local/share/OpenSCAD/libraries/` (Linux)

2. **Relative paths `../../lib/file.scad`:**
   - Resolve relative to current file's directory
   - Convert to absolute path

3. **Library references `<BOSL2/std.scad>`:**
   - Check `~/Documents/OpenSCAD/libraries/BOSL2/std.scad` (macOS)
   - Check `~/.local/share/OpenSCAD/libraries/BOSL2/std.scad` (Linux)

**Recursive loading:**

For each dependency found:
- Check if already visited (circular dependency detection)
- Add to visited set
- Read dependency file
- Extract its use/include statements
- Recurse (up to max depth, default 5)

**Circular dependency detection:**

```
visited = set()
stack = []

function load_dependencies(file, depth=0, max_depth=5):
    if depth > max_depth:
        return "Max depth reached"

    if file in stack:
        return "CIRCULAR DEPENDENCY: " + " -> ".join(stack + [file])

    stack.append(file)
    visited.add(file)

    # Parse use/include statements
    # Recursively load each dependency

    stack.pop()
```

### 3.3. Extract API Surface

**Parse module definitions:**

```bash
# Find module definitions
grep -E '^\s*module\s+\w+\s*\(' file_path

# Example matches:
# module drawer_stack(width, x_start, drawer_start=0) {
# module ww_cabinet_shell() {
# module _helper_function() {  # (private, prefixed with _)
```

**Parse function definitions:**

```bash
# Find function definitions
grep -E '^\s*function\s+\w+\s*\(' file_path

# Example matches:
# function asmfw_section_internal_width(section_id) = ...
# function calc_dimensions(w, h) = [w, h, w+h];
```

**Extract customizer parameters:**

```bash
# Find customizer section comments
grep -E '/\*\s*\[.*\]\s*\*/' file_path

# Example matches:
# /* [Dimensions] */
# /* [Display Options] */

# Parameters follow section comments:
# wall_thickness = 18;  // Wall panel thickness
# show_drawers = true;  // Show drawer boxes
```

**Extract configuration variables:**

```bash
# Find top-level variable assignments
grep -E '^\s*\w+\s*=' file_path | head -20

# Distinguish from parameters by context (before/after customizer sections)
```

**Categorize API:**

- **Public modules:** No underscore prefix, documented
- **Private modules:** Underscore prefix (`_helper()`)
- **Public functions:** No underscore prefix
- **Private functions:** Underscore prefix
- **Customizer params:** In `/* [Section] */` blocks
- **Config variables:** Top-level assignments

### 3.4. Present Context Summary

**Format output:**

```
========================================
OpenSCAD File Context: mini-workbench.scad
========================================

File: /Users/.../workshop/workbenches/mini-workbench.scad
Size: 15.2 KB
Lines: 450

Dependency Tree:
----------------
mini-workbench.scad
├── lib/assembly-framework.scad (project lib)
│   ├── lib/materials.scad (project lib)
│   └── woodworkers-lib/std.scad (system library)
│       ├── woodworkers-lib/planes.scad
│       └── woodworkers-lib/cutlist.scad
├── BOSL2/std.scad (system library)
│   ├── BOSL2/transforms.scad
│   ├── BOSL2/attachments.scad
│   └── BOSL2/shapes3d.scad
└── lib/labels.scad (project lib)

Dependencies Loaded: 11 files
Max Depth Reached: 3 levels

Available Modules (Public):
----------------------------
- mini_workbench() - Main assembly module
- drawer_stack(width, x_start, drawer_start=0) - Creates vertical drawer stack
- dividers() - Renders all vertical dividers
- cabinet_shell() - Outer cabinet box

Available Functions (Public):
------------------------------
- None (uses framework functions)

Customizer Parameters:
----------------------
/* [Display Options] */
show_cabinet = true;         // Show cabinet shell
show_drawers = true;         // Show drawer boxes
show_faceplates = true;      // Show drawer faces
show_runners = true;         // Show drawer runners
show_dividers = true;        // Show vertical dividers

/* [Dimensions] */
total_width = 1650;          // Assembly total width
assembly_height = 500;       // Internal height
assembly_depth = 580;        // Front-to-back depth

Configuration Variables:
------------------------
ASMFW_SECTION_IDS = ["A", "B", "C", "D", "E"]
ASMFW_SECTION_WIDTHS = [253, 562, 562, 153, 120]
ASMFW_TOTAL_WIDTH = 1650
ASMFW_ASSEMBLY_HEIGHT = 500
ASMFW_ASSEMBLY_DEPTH = 580

Framework Functions Available:
-------------------------------
(from lib/assembly-framework.scad)
- asmfw_section_internal_width(section_id)
- asmfw_section_x_start(section_id)
- asmfw_section_x_end(section_id)
- asmfw_drawer_box_width(section_id)
- asmfw_faceplate_width(section_id)
- asmfw_runner_x_positions(section_id)

Key Insights:
-------------
✓ Uses assembly framework for automatic positioning
✓ 5-section cabinet (A, B, C, D, E)
✓ Drawer stacks in sections B and C
✓ Side-access tray in section D
✓ Tall drawer in section A
✓ All dimensions driven by framework configuration

Next Steps:
-----------
- Modify customizer parameters to change display
- Adjust ASMFW_SECTION_WIDTHS to resize sections
- Add new modules using framework functions
- Update drawer stack configurations in sections
========================================
```

## Supporting Files

### scripts/
- `parse_scad.py` - OpenSCAD parser for extracting modules/functions/variables
- `resolve_paths.py` - Library path resolution utility
- `dependency_graph.py` - Builds and visualizes dependency tree

### references/
- `openscad-path-resolution.md` - Detailed path resolution rules
- `api-extraction-patterns.md` - Regex patterns for parsing OpenSCAD syntax
- `library-locations.md` - Standard library installation paths by OS

### examples/
- `example-output-simple.md` - Output for simple single-file .scad
- `example-output-complex.md` - Output for multi-dependency project file
- `example-circular-dependency.md` - Handling circular dependency detection

## Expected Outcomes

### Success Case

```
✅ Loaded: workshop/workbenches/mini-workbench.scad
✅ Dependencies: 11 files resolved
✅ Modules: 4 public, 2 private
✅ Functions: 0 public (uses framework)
✅ Customizer params: 9 parameters in 2 sections
✅ No circular dependencies detected
✅ All library paths resolved

Ready to work with this file.
```

### Failure Case

```
❌ Failed to load: workshop/cabinets/broken.scad

Issues Found:
1. Missing dependency: lib/missing-framework.scad
   - Referenced at line 5: include <lib/missing-framework.scad>
   - File not found in project lib/ or system libraries/

2. Circular dependency detected:
   - a.scad -> b.scad -> c.scad -> a.scad

3. Unresolved library: CustomLib/helper.scad
   - Not found in ~/Documents/OpenSCAD/libraries/
   - Not found in ~/.local/share/OpenSCAD/libraries/

Recommendations:
- Install missing library: CustomLib
- Fix circular dependency in a.scad/b.scad/c.scad
- Create missing file: lib/missing-framework.scad
```

## Requirements

**Tools:**
- Read (load .scad files)
- Grep (extract use/include statements, parse syntax)
- Bash (check file existence, resolve paths)

**Knowledge:**
- OpenSCAD syntax (use vs include semantics)
- Library path resolution (angle brackets vs relative)
- Customizer format (`/* [Section] */` comments)
- Module/function definition patterns

**Environment:**
- Access to project directory
- Access to system library directories (~/Documents/OpenSCAD/libraries/)

## Red Flags to Avoid

- [ ] **Don't load files without checking existence** - Verify file exists before attempting to read
- [ ] **Don't assume library locations** - Check both macOS and Linux paths
- [ ] **Don't skip circular dependency detection** - Always track visited files in stack
- [ ] **Don't parse OpenSCAD with complex regex** - Use simple patterns for module/function extraction
- [ ] **Don't load entire library files** - Stop at max depth to avoid loading massive libraries
- [ ] **Don't ignore use vs include semantics** - Include loads variables, use doesn't
- [ ] **Don't miss relative path resolution** - Resolve paths relative to current file's directory
- [ ] **Don't overload context** - Summarize library contents instead of loading full text
- [ ] **Don't skip customizer sections** - These are critical for understanding configurable parameters
- [ ] **Don't assume underscore convention** - Not all projects use `_private()` naming

## Notes

**Path Resolution Priority:**

1. Angle brackets `<file.scad>`:
   - Project `lib/` directory (highest priority)
   - System libraries (macOS: `~/Documents/OpenSCAD/libraries/`)
   - System libraries (Linux: `~/.local/share/OpenSCAD/libraries/`)

2. Relative paths `../lib/file.scad`:
   - Relative to current file's directory
   - Convert to absolute for consistency

**Use vs Include:**

- `use <file.scad>` - Imports modules/functions ONLY (no variables, no top-level code)
- `include <file.scad>` - Imports everything (modules, functions, variables, executes top-level code)

**Max Depth Rationale:**

Default max depth of 5 prevents loading entire library trees (e.g., BOSL2 has 50+ files).
Focus on direct dependencies and first-level library interfaces.

**Performance:**

For large projects with many dependencies:
- Cache resolved paths
- Skip re-parsing already visited files
- Summarize large libraries instead of extracting full API
