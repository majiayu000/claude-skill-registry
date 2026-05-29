---
name: running-openstudio-models
description: Use this skill when working with OpenStudio 3.10 .osm models to adjust HVAC systems, equipment, thermal zones, schedules, or constructions, then run simulations to validate changes. Handles applying existing measures, running CLI simulations, and saving versioned model files. Delegates to diagnosing-energy-models for simulation failures and writing-openstudio-model-measures for custom measure creation. Includes BCL measure search and download.
---

# Running OpenStudio Models

This skill helps you work with OpenStudio 3.10 `.osm` models to modify building systems, apply measures, and run simulations. It focuses on practical model adjustments and validation runs using the OpenStudio CLI.

# Core Approach

1. **Model Versioning**: Always save new versions before making changes (format: `projectname_YYYY-MM-DD_vX.osm`)
2. **Incremental Changes**: Modify HVAC, zones, schedules, or constructions systematically
3. **Apply Measures**: Use existing measures from BCL or local libraries
4. **Run & Validate**: Execute simulations and verify successful completion
5. **Delegate Issues**: Hand off failures to `diagnosing-energy-models` skill
6. **Delegate Custom Measures**: Hand off measure creation to `writing-openstudio-model-measures` skill

# OpenStudio CLI Basics

**Installation Path**: `C:\openstudio-3.10.0\bin\openstudio.exe`

**Core Commands**:
- `openstudio.exe run --workflow workflow.osw` - Run complete simulation
- `openstudio.exe run --measures_only --workflow workflow.osw` - Apply measures without simulation
- `openstudio.exe measure --update /path/to/measure/` - Update measure metadata

**File Conventions**:
- No whitespace in paths: use `underscored_path/my_model.osm` not `whitespace path/my model.osm`
- Use forward slashes in OSW files even on Windows

# Step-by-Step Workflow

## 1. Version the Current Model

Before any changes, create a versioned copy:

```bash
# Get current date for filename
node -e "console.log(new Date().toISOString().split('T')[0])"

# Copy model with versioning (example for project Example-RecCenter)
cp existing_model.osm Example-RecCenter_2025-12-03_v1.osm
```

**Naming Convention**: `{projectname}_{YYYY-MM-DD}_v{X}.osm`
- `projectname`: Project identifier (e.g., Example-RecCenter, Example-Office)
- `YYYY-MM-DD`: Today's date
- `vX`: Version number for that day (v1, v2, v3, etc.)

## 2. Check for Weather File

Before running simulations, verify weather file exists:

```bash
# Check if .epw file exists in current directory
cmd /c "dir *.epw /b"
```

If no weather file found:
- **Prompt user**: "No weather file found. Please provide the `.epw` file for this project."
- **Ask for location**: User should place `.epw` in the project folder or provide path

## 3. Create or Modify OpenStudio Workflow (OSW)

Create a JSON workflow file to define the simulation:

**Basic OSW Template** (`workflow.osw`):
```json
{
  "seed_file": "Example-RecCenter_2025-12-03_v1.osm",
  "weather_file": "USA_CO_Fort_Collins.epw",
  "steps": []
}
```

**OSW with Measures**:
```json
{
  "seed_file": "Example-RecCenter_2025-12-03_v1.osm",
  "weather_file": "USA_CO_Fort_Collins.epw",
  "steps": [
    {
      "measure_dir_name": "AddMeter",
      "arguments": {
        "meter_name": "Electricity:Facility"
      }
    }
  ]
}
```

Use Node.js to generate OSW files programmatically:

```javascript
#!/usr/bin/env node
import { writeFile } from 'fs/promises';

const workflow = {
  seed_file: "Example-RecCenter_2025-12-03_v1.osm",
  weather_file: "USA_CO_Fort_Collins.epw",
  steps: []
};

await writeFile('workflow.osw', JSON.stringify(workflow, null, 2));
console.log("Created workflow.osw");
```

## 4. Search and Download Measures from BCL

The Building Component Library (BCL) hosts community measures.

**Search for measures**:
- Visit: https://bcl.nrel.gov/
- Search by keyword (e.g., "HVAC", "schedule", "envelope")
- Note the measure name and download URL

**Download measures manually**:
1. Download `.tar.gz` or `.zip` from BCL
2. Extract to `measures/` directory in project folder
3. Update measure metadata:

```bash
C:\openstudio-3.10.0\bin\openstudio.exe measure --update measures/measure_name/
```

**Organize measures**:
```bash
# Create measures directory
mkdir measures

# After downloading and extracting BCL measure
C:\openstudio-3.10.0\bin\openstudio.exe measure --update_all measures/
```

## 5. Apply Measures to Model

**Option A: Using OSW Workflow** (Recommended)

Add measures to the `steps` array in your OSW file:

```json
{
  "seed_file": "Example-RecCenter_2025-12-03_v1.osm",
  "weather_file": "USA_CO_Fort_Collins.epw",
  "steps": [
    {
      "measure_dir_name": "SetThermostatSchedules",
      "arguments": {
        "heating_setpoint": 20,
        "cooling_setpoint": 24
      }
    }
  ]
}
```

Run with measures only (no simulation):

```bash
C:\openstudio-3.10.0\bin\openstudio.exe run --measures_only --workflow workflow.osw
```

**Option B: Compute Measure Arguments**

If you need to see what arguments a measure accepts:

```bash
C:\openstudio-3.10.0\bin\openstudio.exe measure --compute_arguments Example-RecCenter_2025-12-03_v1.osm measures/SetThermostatSchedules/
```

## 6. Run Simulation

Execute the full simulation workflow:

```bash
C:\openstudio-3.10.0\bin\openstudio.exe run --workflow workflow.osw
```

**With debugging** (if issues expected):

```bash
C:\openstudio-3.10.0\bin\openstudio.exe --verbose run --debug --workflow workflow.osw
```

**Output Files**:
- `run/` directory created with simulation results
- `run/eplusout.err` - EnergyPlus error file
- `run/eplusout.sql` - Simulation results database
- `out.osw` - Workflow output with execution log

## 7. Check Simulation Success

**Quick Check**:
```bash
# Check if error file exists and is small (successful runs have minimal errors)
cmd /c "dir run\eplusout.err"

# View last 20 lines of error file
cmd /c "type run\eplusout.err | more +20"
```

**Success Indicators**:
- `out.osw` contains `"completed_status": "Success"`
- `eplusout.err` has no severe errors
- `eplusout.sql` file exists and has data

**Failure Indicators**:
- `out.osw` shows `"completed_status": "Fail"`
- `eplusout.err` contains `** Severe **` errors
- Missing output files

## 8. Handle Simulation Failures

If simulation fails, **delegate to `diagnosing-energy-models` skill**:

**Gather context**:
```bash
# Read error file
type run\eplusout.err

# Check out.osw for step_errors
type out.osw | findstr "step_errors"

# Get model summary
C:\openstudio-3.10.0\bin\openstudio.exe --verbose run --measures_only --workflow workflow.osw
```

**Hand off to diagnostic skill**:
- Provide path to `.err` file
- Include `out.osw` step_errors
- Describe what changes were made
- Share OSW file contents

Example delegation:
> "Simulation failed with severe errors. Delegating to `diagnosing-energy-models` skill to analyze `run/eplusout.err` and diagnose the issue. Changes made: [describe HVAC/zone/schedule modifications]."

# Model Modification Patterns

## Modifying HVAC Systems

OpenStudio models use object-oriented HVAC components. Common modifications:

**Access HVAC loops programmatically** (requires Ruby or Python bindings):
- Air loops: `model.getAirLoopHVACs`
- Plant loops: `model.getPlantLoops`
- Thermal zones: `model.getThermalZones`

**Recommended approach**: Use existing measures from BCL
- "Add HVAC System" measure family
- "Replace HVAC" measures
- "Modify HVAC" measures

If custom HVAC logic needed, **delegate to `writing-openstudio-model-measures` skill**.

## Modifying Thermal Zones

**Via Measures**:
- "Set Thermal Zone Properties"
- "Assign Spaces to Thermal Zones"
- "Merge Thermal Zones"

**Manual edits**: Not recommended via CLI (use OpenStudio Application GUI or custom measure)

## Modifying Schedules

**Via Measures**:
- "Set Thermostat Schedules"
- "Modify Occupancy Schedules"
- "Add Typical Schedules"

**Arguments example**:
```json
{
  "measure_dir_name": "SetThermostatSchedules",
  "arguments": {
    "heating_setpoint_schedule": "HtgSetp 20C",
    "cooling_setpoint_schedule": "ClgSetp 24C"
  }
}
```

## Modifying Constructions

**Via Measures**:
- "Set Construction Properties"
- "Increase Insulation R-Value"
- "Replace Constructions"

**Arguments example**:
```json
{
  "measure_dir_name": "IncreaseInsulationRValueForExteriorWalls",
  "arguments": {
    "r_value": 3.5
  }
}
```

# Validation Checklist

After running simulation, verify:
- [ ] New versioned `.osm` file created
- [ ] Simulation completed without severe errors
- [ ] `eplusout.sql` file generated
- [ ] `out.osw` shows `"completed_status": "Success"`
- [ ] Results make sense for changes made

If failures occur:
- [ ] Delegate to `diagnosing-energy-models` with error context
- [ ] Include `.err` file path and recent changes

# Common Issues & Quick Fixes

## Issue: Missing Weather File

**Symptoms**: Workflow fails immediately with "weather file not found"

**Solution**:
```bash
# Check for weather files
cmd /c "dir *.epw /b"

# If missing, prompt user for .epw file path
```

**Prompt**: "No weather file found. Please provide the `.epw` file path for this project."

## Issue: Measure Not Found

**Symptoms**: `out.osw` shows measure directory not found

**Investigation**:
```bash
# Check measures directory
cmd /c "dir measures /b"

# Update measure if it exists
C:\openstudio-3.10.0\bin\openstudio.exe measure --update measures/MeasureName/
```

**Solution**:
- Download measure from BCL
- Verify measure directory name matches OSW `measure_dir_name`
- Run `--update` to regenerate metadata

## Issue: Model Translation Failure

**Symptoms**: Fails when translating OSM to IDF

**Delegate to**: `diagnosing-energy-models` skill
- Likely geometry issues (intersecting surfaces, non-planar surfaces)
- Could be orphaned objects

## Issue: EnergyPlus Simulation Severe Errors

**Symptoms**: Simulation runs but produces severe errors in `eplusout.err`

**Delegate to**: `diagnosing-energy-models` skill with:
- Path to `run/eplusout.err`
- Description of model changes
- OSW file contents

# Skill Orchestration

## When to Stay in This Skill
- Running existing models
- Applying downloaded/existing measures
- Making straightforward HVAC, zone, schedule, or construction changes
- Versioning and managing model files

## When to Delegate to `diagnosing-energy-models`
- Simulation fails with severe errors
- Model translation fails (OSM → IDF)
- Geometry errors appear
- Complex diagnostic analysis needed
- Provide: `.err` file path, `out.osw` errors, recent changes

## When to Delegate to `writing-openstudio-model-measures`
- Custom measure logic required
- Existing BCL measures don't fit use case
- Need to create reusable measure for repeated operations
- Provide: Desired functionality, model context, argument requirements

## Context Awareness

This skill integrates with work-command-center session tracking:

**Check Active Context:**

```bash
node .claude/skills/work-command-center/tools/session-state.js status
```

Returns: Project name, project number, duration, and deliverables context

**Log Activity Checkpoints:**

```bash
node .claude/skills/work-command-center/tools/session-state.js checkpoint \
  --activity "running-openstudio-models: Simulation completed successfully, annual EUI: 42.3 kBtu/sf"
```

**Signal Completion (called by WCC after skill returns):**

```bash
node .claude/skills/work-command-center/tools/session-state.js skill-complete \
  --skill-name "running-openstudio-models" \
  --summary "Simulation successful. EUI: 42.3 kBtu/sf. Model saved as v2.osm." \
  --outcome "success"
```

**Benefits:**

- WCC tracks time spent in this skill
- Session logs include skill work breakdown
- Context visible across skill transitions
- Deliverables auto-update from skill outcomes

# Reference Resources

## Official Documentation
- **OpenStudio CLI Reference**: https://nrel.github.io/OpenStudio-user-documentation/reference/command_line_interface/
- **OpenStudio SDK Docs**: https://nrel.github.io/OpenStudio-user-documentation/
- **Measure Writer's Guide**: https://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/

## Troubleshooting Resources
- **OpenStudio Coalition Troubleshooting**: https://openstudiocoalition.org/getting_started/troubleshooting/
- **Unmet Hours Forum**: https://unmethours.com/ (community Q&A)

## Measure Resources
- **Building Component Library (BCL)**: https://bcl.nrel.gov/
- **NREL GitHub**: https://github.com/NREL/ (official measures and tools)

See `./openstudio-cli-reference.md` for detailed CLI command syntax and examples.


## Saving Next Steps

When running-openstudio-models work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "running-openstudio-models" \
  --content "## Priority Tasks
1. Run simulation with updated HVAC measures
2. Validate results and check for severe errors
3. Extract EUI and utility costs from eplusout.sql"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`
