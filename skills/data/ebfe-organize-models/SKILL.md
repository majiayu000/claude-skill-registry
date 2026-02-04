---
name: ebfe_organize_models
model: sonnet
description: |
  Organize downloaded FEMA eBFE/BLE model files into standardized 4-folder structure.

  Use when working with eBFE downloads that need organization into:
  - HMS Model/ (HEC-HMS hydrologic models)
  - RAS Model/ (HEC-RAS hydraulic models)
  - Spatial Data/ (GIS, terrain, geodatabases)
  - Documentation/ (reports, PDFs, metadata)

  Handles variable archive structures, nested zips, and mixed content through
  intelligent file analysis and recursive extraction.
---

# Organizing eBFE Models

## Purpose

Organize downloaded FEMA eBFE/BLE study area files into a standardized 4-folder structure, regardless of the original archive organization patterns.

## Standardized Output Structure

Every organized eBFE study area should have this structure:

```
{StudyAreaName}_{HUC8}/
├── HMS Model/              # HEC-HMS hydrologic models
│   ├── {ProjectName}.hms
│   ├── {ProjectName}.basin
│   ├── *.dss
│   └── ... (all HMS-related files)
├── RAS Model/              # HEC-RAS hydraulic models
│   ├── {Model1}/
│   │   ├── {Model1}.prj
│   │   ├── {Model1}.g##
│   │   ├── {Model1}.p##
│   │   └── ... (all RAS project files)
│   └── {Model2}/...
├── Spatial Data/           # GIS, terrain, geodatabases
│   ├── Terrain/
│   ├── *.tif, *.hdf
│   ├── *.gdb/
│   └── ... (all spatial data)
└── Documentation/          # Reports, metadata, inventories
    ├── *.pdf
    ├── *.xlsx (inventories)
    ├── *_metadata.xml
    └── ... (all documentation)
```

## Input Patterns

The skill must handle these downloaded archive patterns:

**Pattern 1**: Multiple 1D models in variable wrapper folders (80-200 MB)
**Pattern 2**: ModelURLs.txt links file (1 KB)
**Pattern 3**: Single 2D model in nested zip (5-15 GB)
**Pattern 4**: Compound HMS + RAS in nested zips (8+ GB)

See `feature_dev_notes/eBFE_Integration/RESEARCH_FINDINGS.md` for complete pattern documentation.

## File Classification Rules

### HMS Model/ Folder

Include files with these extensions or patterns:
- `.hms` - HEC-HMS project
- `.basin` - Basin model file
- `.met` - Meteorology file
- `.control` - Control specifications
- `.run` - Run configuration
- `.results` - HMS results
- `.dss` in `Hydrology/` path
- `.log`, `.out` in HMS folders

**Path indicators**: `Hydrology/`, `HMS/`

### RAS Model/ Folder

Include files with these extensions or patterns:
- `.prj` - HEC-RAS project (validate: contains "Proj Title=", "Geom File=")
- `.g##` - Geometry file
- `.p##` - Plan file
- `.f##` - Flow file
- `.u##` - Unsteady flow file
- `.c##` - Sediment file
- `.b##` - Bridge/culvert file
- `.bco##` - Boundary condition override
- `.IC.O##` - Initial conditions override
- `.x##` - Cross section index
- `.rasmap` - RAS Mapper project
- `.dsc` - DSS catalog (if in RAS folder)
- `.dss` (if in RAS folder, not HMS folder)

**Exclude**: `.prj` files in `Features/`, `Shp/`, `gis/` (shapefiles, not HEC-RAS)

**Organization within RAS Model/**:
- If single model: Place files directly in RAS Model/
- If multiple models: Create subfolder per model (use .prj stem as folder name)

### Spatial Data/ Folder

Include files with these extensions or patterns:
- `.tif` - GeoTIFF raster
- `.hdf` - Terrain HDF (if NOT .g##.hdf or .p##.hdf)
- `.vrt` - Virtual raster
- `.gdb/` - File geodatabase
- `.shp`, `.shx`, `.dbf`, `.prj` - Shapefiles (in Features/, Shp/, gis/ folders)
- Folder named `Terrain/` (entire folder)
- Folder named `Spatial/`, `GIS/`, `Shp/`, `Features/`

**Exception**: `.g##.hdf` (geometry preprocessor) and `.p##.hdf` (results) stay with RAS Model/

### Documentation/ Folder

Include files with these extensions or patterns:
- `.pdf` - Reports, guides
- `.xlsx`, `.xls` - Inventories, metadata spreadsheets
- `.xml` - Metadata
- Files with "Inventory" in name
- Files with "metadata" in name
- Files with "Report" in name
- `README*` files

## Agent Deliverables

**REQUIRED for Every Organization**:

1. ✅ Organized model in 4-folder structure
2. ✅ `agent/model_log.md` - Agent work log
3. ✅ `MANIFEST.md` - Organization manifest
4. ✅ **NEW**: Generated `organize_{modelname}()` function in `feature_dev_notes/eBFE_Integration/generated_functions/`
5. ✅ **NEW**: DSS validation results (if DSS files present)
6. ✅ **NEW**: Suggested compute test command for user
7. ✅ **NEW**: Haiku subagent results check (if compute test run)

## Workflow

### Step 1: Analyze Archive Structure

```python
# Inspect the downloaded archive
# - List all files
# - Identify nested zips
# - Detect pattern (1-4)
# - Count .prj files (RAS) and .hms files (HMS)
```

### Step 2: Extract Recursively

```python
# Extract Models.zip
# Find nested .zip files (_Final.zip, RAS_Submittal.zip, etc.)
# Extract nested zips in place
# Preserve directory structure during extraction
```

### Step 3: Classify and Organize

```python
# Recursively walk extracted content
# For each file:
#   - Determine classification (HMS/RAS/Spatial/Docs)
#   - Move to appropriate standardized folder
#   - For RAS models with multiple projects:
#       - Group files by .prj stem
#       - Create subfolder per model

# CRITICAL INTEGRATIONS (to create runnable HEC-RAS models):

# 1. Move Output/ folder INTO HEC-RAS project folder
#    eBFE separates Output/ (pre-run HDF files) from Input/ (project)
#    HEC-RAS expects HDF files in project folder
for model_folder in ras_model.glob('**/Input'):
    output_folder = model_folder.parent / 'Output'
    if output_folder.exists():
        # Move all Output/*.hdf and other files INTO Input/
        for output_file in output_folder.rglob('*'):
            if output_file.is_file():
                shutil.copy2(output_file, model_folder / output_file.name)

# 2. Move Terrain/ INTO HEC-RAS project folder
#    eBFE places Terrain/ as sibling to Input/ (breaks .rasmap references)
#    HEC-RAS expects Terrain/ in project folder
for model_folder in ras_model.glob('**/Input'):
    terrain_folder = model_folder.parent / 'Terrain'
    if terrain_folder.exists():
        # Move Terrain/ INTO Input/Terrain/
        shutil.copytree(terrain_folder, model_folder / 'Terrain', dirs_exist_ok=True)
```

### Step 4: Validate Organization

```python
# Verify each folder:
#   - HMS Model/: Check for .hms files
#   - RAS Model/: Verify .prj files are valid HEC-RAS projects
#   - Spatial Data/: Check for terrain files
#   - Documentation/: Ensure reports are present
#
# Report summary:
#   - X HMS projects found
#   - Y RAS projects found
#   - Z terrain files found
#   - N documents organized
```

### Step 4: Correct DSS File Paths (CRITICAL - VALIDATE EXISTENCE)

```python
# CRITICAL: Fix DSS file path references in HEC-RAS files AND verify files exist
# eBFE models have:
#   - Absolute paths from original system: C:\eBFE\... (doesn't exist on user system)
#   - Wrong relative paths: DSS\Input\file.dss (file is actually in same folder)
# These cause "DSS path needs correction" GUI popups that break automation

import re

# Step 1: Find all DSS files that ACTUALLY EXIST in organized structure
dss_files = list(ras_model_folder.glob('**/*.dss'))
dss_lookup = {dss.name: dss for dss in dss_files}  # Lookup by filename

print(f"Found {len(dss_files)} DSS file(s):")
for dss in dss_files:
    print(f"  - {dss.relative_to(ras_model_folder)}")

# Step 2: Find HEC-RAS files that reference DSS (.u##, .prj, .p##)
hecras_files = []
hecras_files.extend(ras_model_folder.glob('**/*.u[0-9]*'))   # Unsteady flow files
hecras_files.extend(ras_model_folder.glob('**/*.p[0-9][0-9]'))  # Plan files
hecras_files.extend(ras_model_folder.glob('**/*.prj'))  # Project files

# Step 3: For each HEC-RAS file, validate and correct DSS references
for hecras_file in hecras_files:
    content = hecras_file.read_text(encoding='utf-8', errors='ignore')
    modified = False

    # Find all "DSS File=" lines
    dss_file_pattern = re.compile(r'DSS File=(.+?)(?:\n|$)', re.IGNORECASE)

    for match in dss_file_pattern.finditer(content):
        old_path = match.group(1).strip()
        dss_filename = Path(old_path).name  # Extract just the filename

        # Check if this DSS file exists in our organized structure
        if dss_filename in dss_lookup:
            actual_dss_path = dss_lookup[dss_filename]

            # CRITICAL: Verify the DSS file actually exists
            if actual_dss_path.exists():
                # Calculate correct relative path from HEC-RAS file to actual DSS location
                rel_path = actual_dss_path.relative_to(hecras_file.parent)
                rel_path_str = str(rel_path).replace('\\', '/')

                # Only replace if current path is wrong
                if old_path != rel_path_str:
                    old_full = f"DSS File={old_path}"
                    new_full = f"DSS File={rel_path_str}"
                    content = content.replace(old_full, new_full)
                    modified = True
                    print(f"  Corrected in {hecras_file.name}:")
                    print(f"    Old: {old_path}")
                    print(f"    New: {rel_path_str} (✓ verified exists)")
            else:
                print(f"  ⚠️ WARNING: DSS not found: {dss_filename}")
        else:
            print(f"  ⚠️ WARNING: DSS not in organized structure: {dss_filename}")

    if modified:
        hecras_file.write_text(content, encoding='utf-8')

# Result: Model opens without GUI popups, all DSS paths verified
# Handles cases like:
#   DSS\Input\UPG_precip.dss → UPG_precip.dss (if file is in same folder)
#   C:\eBFE\...\file.dss → ../DSS/file.dss (if file is in subdirectory)
```

### Step 5: Validate DSS Files (If Present)

```python
# Validate DSS pathname contents (not just file paths)
from ras_commander.dss import RasDss

# Find all .dss files in RAS Model/
dss_files = list(ras_model_folder.glob('**/*.dss'))

for dss_file in dss_files:
    # Get catalog
    catalog = RasDss.get_catalog(dss_file)

    # Check each pathname
    for pathname in catalog['pathname']:
        result = RasDss.check_pathname(dss_file, pathname)
        if not result.is_valid:
            # Document invalid pathnames in model_log.md
            pass
```

### Step 6: Suggest Compute Test (If RAS Model Present)

```python
# If RAS model organized, suggest optional compute test to user
# This validates terrain, land use, and DSS files are correct

print("=" * 80)
print("OPTIONAL VALIDATION: Compute Test")
print("=" * 80)
print("To verify terrain, land use, and DSS files are correct,")
print("run at least one plan:")
print()
print("  from ras_commander import init_ras_project, RasCmdr")
print(f"  init_ras_project(r'{ras_model_folder}', '{version}')")
print("  RasCmdr.compute_plan('01', num_cores=2)")
print()
print("If the plan executes successfully, terrain/DSS files are valid.")
print("=" * 80)
```

### Step 7: Check Results with Haiku Subagent (If Compute Test Run)

```python
# After compute test completes (if user runs it), check results for errors
from ras_commander.hdf import HdfResultsPlan

# Launch haiku subagent to check results
Task(
    subagent_type="notebook-output-auditor",
    model="haiku",
    description="Check HEC-RAS results for errors",
    prompt=f"""
    Check HEC-RAS results for errors in: {hdf_file}

    Extract compute messages and check for:
    - Error messages
    - Warning messages
    - Convergence issues
    - Numerical instabilities
    - Missing data

    Write findings to: {agent_folder}/compute_test_results.md
    """
)
```

### Step 8: Generate Deterministic Function

**REQUIRED**: After organizing each model, generate a Python function for future use.

```python
# Generate organize_{modelname}() function
# Write to: feature_dev_notes/eBFE_Integration/generated_functions/{studyarea}_{huc8}.py

def organize_{clean_name}(
    downloaded_folder: Path,
    output_folder: Optional[Path] = None
) -> Path:
    """
    Organize {StudyArea} ({HUC8}) eBFE model.

    Pattern {X}: {Pattern description}

    Generated by ebfe_organize_models agent on {date}.
    """
    # Specific organization steps discovered by agent
    # Include pattern detection, extraction, classification
    # Use lessons learned from this organization
    pass
```

**Deliverable**: Write generated function to `feature_dev_notes/eBFE_Integration/generated_functions/organize_{studyarea}_{huc8}.py`

### Step 9: Generate Manifest and Model Log

```python
# Create organization manifest: MANIFEST.md (in project root)
# Document:
#   - Original archive pattern detected
#   - Files organized by category
#   - RAS project inventory (model names, types, sizes)
#   - HMS project inventory (if any)
#   - Terrain files inventory
#   - Document inventory
#   - DSS validation results
#   - Suggested compute test command

# Create agent work log: agent/model_log.md (in project root)
# **REQUIRED**: Every organized model MUST have agent/model_log.md
# Document:
#   - Agent actions taken
#   - Files classified and moved
#   - Decisions made during organization
#   - Issues encountered and resolutions
#   - DSS validation results
#   - Generated function location
#   - Timestamps for all operations
```

## Output Format

### REQUIRED: agent/model_log.md

**CRITICAL**: Every organized eBFE model MUST have `agent/model_log.md` documenting agent work.

**Location**: `{StudyAreaName}_{HUC8}/agent/model_log.md`

**Template**:
```markdown
# Agent Work Log - {StudyAreaName}

**Agent**: ebfe_organize_models
**Date**: {YYYY-MM-DD HH:MM:SS}
**Study Area**: {Name} ({HUC8})
**Pattern**: {Pattern 1/2/3/4}

## Actions Taken

### Archive Extraction
- Extracted: {source_archive}
- Nested zips: {list any nested zips extracted}
- Total files extracted: {count}

### File Classification
{For each file category, list files moved}

#### HMS Model (X files, Y MB)
- {list key files}

#### RAS Model (X files, Y GB)
- {list models and key files}

#### Spatial Data (X files, Y MB)
- {list terrain, shapefiles, etc.}

#### Documentation (X files, Y MB)
- {list reports, inventories}

### Decisions Made
- {Document any classification decisions}
- {Document handling of ambiguous files}
- {Document terrain handling approach}

### Issues Encountered
- {List any problems}
- {Document resolutions}

### Validation Checks
- [x] All files classified
- [x] RAS .prj files validated (not shapefiles)
- [x] Terrain location documented
- [x] Manifest created

## Next Steps for User
{Provide clear next steps, e.g., testing with ras-commander}
```

### MANIFEST.md Template

```markdown
# eBFE Model Organization Manifest

**Study Area**: {Name}
**HUC8**: {HUC8}
**Original Pattern**: {Pattern 1/2/3/4}
**Organized Date**: {YYYY-MM-DD}

## HMS Model

{X} HEC-HMS projects found:
- {ProjectName}.hms - {StormFrequencies}

## RAS Model

{Y} HEC-RAS projects found:

### {ModelName1}
- Type: {1D/2D}
- Plans: {#}
- Size: {MB/GB}
- Terrain: {Self-contained/External/Not needed}

### {ModelName2}
...

## Spatial Data

{Z} terrain/spatial files:
- {TerrainFile1} - {Size}
- Geodatabase: {.gdb folders}
- Shapefiles: {count}

## Documentation

{N} documents:
- {Report1}.pdf - {Size}
- {Inventory}.xlsx
- {Metadata}.xml

## Notes

{Any special observations or issues encountered}
```

## Example Usage

```python
# Organize a downloaded study area
from pathlib import Path

# Input: Raw downloaded and extracted files
source = Path("D:/eBFE/raw_downloads/12040102_Spring_Models_extracted/")

# Output: Organized into 4 folders
target = Path("D:/eBFE/organized/SpringCreek_12040102/")

# Agent organizes the files
# Result: target/ now has HMS Model/, RAS Model/, Spatial Data/, Documentation/
```

## Special Handling Notes

### Nested Zips
- Recursively extract _Final.zip, RAS_Submittal.zip, etc.
- Delete intermediate zips after extraction (optional)
- Preserve meaningful folder names

### Shapefile .prj vs HEC-RAS .prj
- Shapefiles: `.prj` in Features/, Shp/, gis/ → Spatial Data/
- HEC-RAS: `.prj` with "Proj Title=" content → RAS Model/

### Self-Contained vs External Terrain
- If Terrain/ folder in model directory → stays with RAS Model/, copy to Spatial Data/
- If .rasmap references external terrain → document in manifest

### Multiple RAS Projects
- Create subfolder per .prj file using stem name
- Group related files (.g##, .p##, .f##) with matching basename
- Keep directory hierarchy for watershed organization if meaningful

## Generated Function Template

Every organization must generate an `organize_{modelname}()` function:

**File Location**: `feature_dev_notes/eBFE_Integration/generated_functions/organize_{studyarea}_{huc8}.py`

**Template**:
```python
"""
Generated organization function for {StudyArea} ({HUC8})

Generated by: ebfe_organize_models agent
Date: {YYYY-MM-DD}
Pattern: {Pattern X}
"""

from pathlib import Path
from typing import Optional
import shutil
import zipfile
from ras_commander.dss import RasDss


def organize_{clean_name}(
    downloaded_folder: Path,
    output_folder: Optional[Path] = None,
    validate_dss: bool = True
) -> Path:
    """
    Organize {StudyArea} ({HUC8}) eBFE model.

    Pattern {X}: {Pattern description discovered by agent}

    Args:
        downloaded_folder: Path to extracted {HUC8}_Models folder
        output_folder: Output location (default: ./ebfe_organized/{StudyArea}_{HUC8}/)
        validate_dss: Run DSS validation checks

    Returns:
        Path to organized model with 4-folder structure + agent/model_log.md

    Generated: {date} by ebfe_organize_models agent
    """
    # [Agent-discovered organization steps]
    # 1. Extract nested zips (if pattern requires)
    # 2. Find .prj files recursively
    # 3. Classify files to HMS/RAS/Spatial/Docs
    # 4. Create 4-folder structure
    # 5. Move files to organized locations
    # 6. Validate DSS files if present
    # 7. Create agent/model_log.md
    # 8. Generate MANIFEST.md

    if validate_dss:
        # DSS validation code
        pass

    return output_folder


# Example usage in notebook
if __name__ == '__main__':
    """
    Example usage for {StudyArea}:

    >>> from pathlib import Path
    >>> organized = organize_{clean_name}(
    ...     Path(r"D:/downloads/{HUC8}_Models_extracted")
    ... )
    >>> from ras_commander import init_ras_project
    >>> init_ras_project(organized / "RAS Model", "{version}")
    """
```

## DSS Validation Example

```python
# After organizing RAS Model, validate DSS files
from ras_commander.dss import RasDss
from pathlib import Path

ras_model_folder = Path(r"D:/Organized/Model/RAS Model")
dss_files = list(ras_model_folder.glob('**/*.dss'))

dss_validation_results = []

for dss_file in dss_files:
    print(f"\nValidating: {dss_file.name}")

    # Get catalog
    try:
        catalog = RasDss.get_catalog(dss_file)
        print(f"  Found {len(catalog)} pathnames")

        # Validate each pathname
        for pathname in catalog['pathname']:
            result = RasDss.check_pathname(dss_file, pathname)

            if not result.is_valid:
                dss_validation_results.append({
                    'file': dss_file.name,
                    'pathname': pathname,
                    'issues': result.message
                })
                print(f"  ✗ INVALID: {pathname}")
                print(f"    Issue: {result.message}")
            else:
                print(f"  ✓ Valid: {pathname}")

    except Exception as e:
        print(f"  ✗ Error reading DSS: {e}")
        dss_validation_results.append({
            'file': dss_file.name,
            'pathname': 'N/A',
            'issues': f"Failed to read: {e}"
        })

# Document results in agent/model_log.md
if dss_validation_results:
    print(f"\n⚠️ Found {len(dss_validation_results)} DSS validation issues")
    print("  See agent/model_log.md for details")
else:
    print(f"\n✓ All DSS files valid")
```

## Compute Test Validation Workflow

```python
# After organization, suggest optional compute test
print("\n" + "=" * 80)
print("OPTIONAL: Compute Test Validation")
print("=" * 80)
print("\nTo verify terrain, land use, and DSS files are correct:")
print()
print("```python")
print(f"from ras_commander import init_ras_project, RasCmdr")
print(f"from pathlib import Path")
print()
print(f"project = Path(r'{organized_folder / 'RAS Model'}')")
print(f"init_ras_project(project, '{version}')")
print(f"RasCmdr.compute_plan('01', num_cores=2)")
print("```")
print()
print("If plan executes successfully → terrain/DSS files are valid")
print("If plan fails → check compute messages for specific errors")
print("=" * 80)

# After user runs compute test, check results with haiku
# (See Step 7 in workflow above)
```

## See Also

- **Research**: `feature_dev_notes/eBFE_Integration/RESEARCH_FINDINGS.md` - 5 patterns documented
- **Implementation**: `feature_dev_notes/eBFE_Integration/IMPLEMENTATION_SUMMARY.md` - Design guidance
- **Discovery API**: `feature_dev_notes/eBFE_Integration/prototype_discovery.py` - Download helpers
- **Generated Functions**: `feature_dev_notes/eBFE_Integration/generated_functions/` - Agent-generated deterministic functions
- **DSS Validation**: `.claude/rules/hec-ras/dss-files.md` - DSS validation patterns
- **Results Checking**: `.claude/agents/notebook-output-auditor.md` - Haiku results checker
