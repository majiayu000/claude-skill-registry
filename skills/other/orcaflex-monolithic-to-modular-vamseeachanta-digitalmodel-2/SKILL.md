---
name: orcaflex-monolithic-to-modular
description: Convert monolithic OrcaFlex YAML files to modular include format for maintainability, reusability, and parametric analysis.
version: 1.0.0
updated: 2026-01-21
category: offshore-engineering
triggers:
- convert monolithic to modular
- split OrcaFlex YAML
- modularize OrcaFlex model
- create OrcaFlex includes
- reverse engineer OrcaFlex YAML
- prepare modular model
---
# OrcaFlex Monolithic to Modular Converter Skill

Convert large monolithic OrcaFlex YAML files into organized modular structures with reusable includes and parameterized inputs.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
orcaflex_version: '>=11.0'
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

- Converting large single-file YAML models to maintainable modular format
- Extracting reusable components (line types, buoy types, environments)
- Preparing models for parametric analysis
- Creating template libraries from existing models
- Standardizing model organization across projects

## Directory Structure Convention

### Target Structure

```
<example_folder>/
├── monolithic.yml           # Original single-file (preserved)
└── modular/
    ├── master.yml           # Entry point with includes
    ├── includes/            # Component definitions
    │   ├── 01_general.yml
    │   ├── 02_var_data.yml
    │   ├── 03_environment.yml
    │   ├── 05_line_types.yml
    │   ├── 07_lines.yml
    │   ├── 08_buoys.yml
    │   ├── 09_shapes.yml
    │   ├── 10_groups.yml
    │   ├── 13_supports.yml
    │   └── 14_morison.yml
    └── inputs/
        └── parameters.yml   # Extracted parameters
```

### Naming Conventions

| Convention | Example | Rationale |
|------------|---------|-----------|
| Folder name | `30in_pipeline/` | Descriptive, filesystem-safe |
| Original file | `monolithic.yml` | Clear purpose identification |
| Entry point | `master.yml` | Standard modular entry |
| Include prefix | `01_`, `02_` | Dependency ordering |

## Include File Ordering

**Critical**: Include order matters due to OrcaFlex dependencies.

```yaml
# master.yml - Correct dependency order
- includefile: includes/01_general.yml      # Global settings first
- includefile: includes/02_var_data.yml     # Variable data
- includefile: includes/03_environment.yml  # Environment before objects
- includefile: includes/05_line_types.yml   # Types before instances
- includefile: includes/13_supports.yml     # Supports before lines
- includefile: includes/14_morison.yml      # Morison elements
- includefile: includes/09_shapes.yml       # Shapes before buoys
- includefile: includes/08_buoys.yml        # Buoys before lines connect
- includefile: includes/07_lines.yml        # Lines reference types/buoys
- includefile: includes/10_groups.yml       # Groups reference objects
```

### Dependency Rules

1. **Types before instances** - LineTypes before Lines
2. **Connections before dependents** - Buoys before Lines that connect to them
3. **Global before specific** - General/Environment before objects
4. **References resolved** - Define before reference

## Component Mapping

| Section | Include File | Contents |
|---------|-------------|----------|
| General | `01_general.yml` | Units, simulation settings |
| Variable Data | `02_var_data.yml` | Tags, variables |
| Environment | `03_environment.yml` | Water depth, waves, current, wind |
| Line Types | `05_line_types.yml` | Cable/chain/riser properties |
| Lines | `07_lines.yml` | Line instances, connections |
| Buoys | `08_buoys.yml` | 3D/6D buoy definitions |
| Shapes | `09_shapes.yml` | Drawing shapes |
| Groups | `10_groups.yml` | Object groupings |
| Supports | `13_supports.yml` | Support definitions |
| Morison | `14_morison.yml` | Morison elements |

## Parameter Extraction

Extract key parameters to `inputs/parameters.yml` for parametric studies:

```yaml
# inputs/parameters.yml
parameters:
  environment:
    water_depth: 8
    current_speed: 1
    current_direction: 270
    wind_speed: 8.87
    water_density: 1.03

  waves:
    hs: 0
    tp: 8
    wave_direction: 180

  simulation:
    stage_durations: [8, 16]
    time_step: 0.1
```

## Conversion Process

### Step 1: Analyze Monolithic File

```python
import yaml
from pathlib import Path

def analyze_monolithic(yml_path: Path) -> dict:
    """Identify sections in monolithic YAML."""
    with open(yml_path) as f:
        content = yaml.safe_load(f)

    sections = {
        'General': content.get('General', {}),
        'Environment': content.get('Environment', {}),
        'LineTypes': content.get('LineTypes', []),
        'Lines': content.get('Lines', []),
        'Buoys': content.get('Buoys', []),
        # ... etc
    }
    return sections
```

### Step 2: Create Modular Structure

```python
def create_modular_structure(base_dir: Path):
    """Create standard directory structure."""
    (base_dir / 'modular' / 'includes').mkdir(parents=True, exist_ok=True)
    (base_dir / 'modular' / 'inputs').mkdir(parents=True, exist_ok=True)
```

### Step 3: Split Sections

```python
def split_to_includes(sections: dict, includes_dir: Path):
    """Write each section to separate include file."""

    section_mapping = {
        'General': '01_general.yml',
        'Environment': '03_environment.yml',
        'LineTypes': '05_line_types.yml',
        'Lines': '07_lines.yml',
        'Buoys': '08_buoys.yml',
    }

    for section, filename in section_mapping.items():
        if section in sections and sections[section]:
            output_path = includes_dir / filename
            with open(output_path, 'w') as f:
                yaml.dump({section: sections[section]}, f,
                         default_flow_style=False)
```

### Step 4: Generate Master File

```python
def generate_master(modular_dir: Path, original_meta: dict):
    """Generate master.yml with includes."""

    includes = sorted((modular_dir / 'includes').glob('*.yml'))

    master_content = [
        '%YAML 1.1',
        '# Type: Model',
        f'# Converted from: {original_meta["source"]}',
        f'# Created: {original_meta["timestamp"]}',
        '---',
    ]

    # Add includes in dependency order
    for inc in includes:
        master_content.append(f'- includefile: includes/{inc.name}')

    with open(modular_dir / 'master.yml', 'w') as f:
        f.write('\n'.join(master_content))
```

## Lessons Learned

### From Production Usage (2026-01-21)

1. **Use descriptive folder names**: `30in_pipeline` is clearer than `5_tug_env_6D_buoys`

2. **Separate monolithic from modular**: Keep original as `monolithic.yml` alongside `modular/` directory

3. **Extract parameters early**: Identify parameters for parametric studies before splitting

4. **Preserve metadata**: Keep original file header (Program version, creation date, user)

5. **Test after conversion**: Load `master.yml` in OrcaFlex to verify integrity

6. **Document include order**: Include order is critical - document dependencies in master.yml

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Lines fail to load | Check LineTypes included before Lines |
| Buoy connections missing | Include Buoys before Lines that connect |
| Groups reference missing objects | Groups must be last |
| Parameters hardcoded | Extract to inputs/parameters.yml |

## Validation

### Quick Validation

```bash
# Load modular model in OrcaFlex
python -c "import OrcFxAPI; m = OrcFxAPI.Model('modular/master.yml'); print('OK')"
```

### Full Validation

```python
def validate_modular(master_path: Path, monolithic_path: Path) -> bool:
    """Compare modular vs monolithic models."""
    import OrcFxAPI

    model_mono = OrcFxAPI.Model(str(monolithic_path))
    model_mod = OrcFxAPI.Model(str(master_path))

    # Compare object counts
    mono_objects = len(list(model_mono.objects))
    mod_objects = len(list(model_mod.objects))

    if mono_objects != mod_objects:
        print(f"Object count mismatch: {mono_objects} vs {mod_objects}")
        return False

    print(f"Validation passed: {mod_objects} objects")
    return True
```

## Example Usage

### Convert Existing Model

```bash
# 1. Create example folder
mkdir -p docs/modules/orcaflex/pipeline/installation/floating/30in_pipeline

# 2. Copy original as monolithic.yml
cp "original model.yml" 30in_pipeline/monolithic.yml

# 3. Run conversion (manual or scripted)
python -m digitalmodel.tools.orcaflex_modularize 30in_pipeline/monolithic.yml

# 4. Verify
ls -la 30in_pipeline/modular/
```

### Parametric Study Setup

```python
import yaml
from pathlib import Path

# Load parameters
params_path = Path('30in_pipeline/modular/inputs/parameters.yml')
with open(params_path) as f:
    params = yaml.safe_load(f)

# Modify for study
for hs in [2, 4, 6, 8]:
    params['parameters']['waves']['hs'] = hs
    case_dir = Path(f'cases/hs_{hs}')
    case_dir.mkdir(parents=True, exist_ok=True)

    # Save modified parameters
    with open(case_dir / 'parameters.yml', 'w') as f:
        yaml.dump(params, f)
```

## Related Skills

- [orcaflex-file-conversion](../orcaflex-file-conversion/SKILL.md) - Format conversion (.dat/.yml/.sim)
- [orcaflex-model-generator](../orcaflex-model-generator/SKILL.md) - Template-based model generation
- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations

## References

- Example: `docs/modules/orcaflex/pipeline/installation/floating/30in_pipeline/`
- Spec: `specs/modules/orcaflex/monolithic-to-modular-converter/`
- OrcaFlex YAML Include Documentation

---

## Version History

- **1.0.0** (2026-01-21): Initial release with directory conventions, include ordering, and lessons learned from production usage
