---
name: orcaflex-modeling
description: Setup, configure, and run OrcaFlex hydrodynamic simulations using the
  universal runner. Use for marine/offshore analysis including static analysis, dynamic
  simulations, mooring analysis, and batch processing of OrcaFlex models.
version: 2.0.0
updated: 2025-01-02
category: offshore-engineering
triggers:
- OrcaFlex model setup
- hydrodynamic simulation
- mooring analysis
- riser analysis
- installation analysis
- batch OrcaFlex processing
- .yml model files
- .dat model files
- .sim simulation files
---
# OrcaFlex Modeling Skill

Create, configure, and execute OrcaFlex hydrodynamic simulations for offshore engineering analysis.

## Version Metadata

```yaml
version: 2.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-file-conversion: '>=1.0.0,<2.0.0'
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

## Changelog

### [2.0.0] - 2026-01-07

**Added:**
- Initial version metadata and dependency management
- Semantic versioning support
- Compatibility information for Python 3.10-3.13

**Changed:**
- Enhanced skill documentation structure


## When to Use

- Setting up OrcaFlex analysis projects with standardized folder structure
- Running static or dynamic hydrodynamic simulations
- Batch processing multiple OrcaFlex models (.yml, .dat files)
- Configuring mooring analysis or iterative simulations
- Using the universal runner for pattern-based batch execution
- Preprocessing vessel data and checking model configurations
- Hydrodynamic analysis and mooring system design
- Riser analysis and installation sequence planning
- Fatigue assessment of offshore structures

## Agent Capabilities

This skill integrates agent capabilities from `/agents/orcaflex/`:

### Domain Expertise
- **Tools**: OrcaFlex, OrcaWave
- **Analysis Types**:
  - Hydrodynamic analysis
  - Mooring system design
  - Riser analysis
  - Installation analysis
  - Fatigue assessment

### Industry Standards
- DNV-ST-F201 (Dynamic Risers)
- API RP 2SK (Stationkeeping)
- ISO 19901-7 (Mooring Systems)

### Critical Production Rules

**NEVER** create mock .sim files or replace production .sim files with test data.

Protected paths (DO NOT MODIFY):
- `*/runtime_test/*.sim`
- `*/production/*.sim`
- Production .sim files are large binary OrcaFlex model files (often GB in size)

### Workflow Automation
- Enhanced specs with auto-update and learning
- Analysis automation with batch processing
- Result extraction and summary generation

## Prerequisites

- OrcaFlex license (checked via `OrcFxAPI`)
- Python environment with `digitalmodel` package installed
- YAML configuration files for analysis parameters

## Standardized Folder Structure

All OrcaFlex analyses MUST use this directory structure:

```
<analysis_directory>/
├── .dat/                    # OrcaFlex data files
│   ├── original/           # Original unmodified files
│   ├── modified/           # Modified during iteration
│   └── archive/            # Timestamped archives
├── .sim/                    # OrcaFlex simulation files
├── configs/                 # Configuration files
│   └── analysis_config.yml
├── results/                 # Analysis outputs
│   ├── summary/
│   ├── time_series/
│   └── reports/
├── logs/                    # Execution logs
└── scripts/                 # Helper scripts
```

## Configuration Pattern

### Basic Analysis Configuration

```yaml
# configs/analysis_config.yml

basename: project_name

default:
  analysis:
    file_type: yml
    file_path_pattern: null  # Optional glob pattern

orcaflex:
  # Preprocessing options
  preprocess:
    VesselType_Loading:
      flag: false
    check_yml_file:
      flag: false

  # Analysis options
  analysis:
    static: false           # Run static analysis only
    simulation: true        # Run full dynamic simulation
    iterate:
      flag: false           # Iterative analysis
    mooring:
      flag: false           # Mooring-specific analysis

  # Output options
  postprocess:
    summary:
      flag: true
```

### Universal Runner Configuration

```yaml
# For batch processing with universal runner

default:
  analysis:
    file_type: yml
    file_path_pattern: "*.yml"  # Process all YAML files

orcaflex:
  universal_runner:
    flag: true
    input_directory: "."
    output_directory: "results/"
    parallel: true
    max_workers: 4
    mock_mode: false         # Dry run without OrcaFlex
```

## Universal Runner Usage

### Command Line Interface

```bash
# Process all YAML files in current directory
python -m digitalmodel.modules.orcaflex.universal pattern="*.yml"

# Specify input/output directories
python -m digitalmodel.modules.orcaflex.universal \
    pattern="mooring_*.yml" \
    input_directory="configs/" \
    output_directory="results/"

# Mock mode (dry run without OrcaFlex license)
python -m digitalmodel.modules.orcaflex.universal \
    pattern="*.yml" \
    mock_mode=true

# Parallel processing with limited workers
python -m digitalmodel.modules.orcaflex.universal \
    pattern="*.yml" \
    parallel=true \
    max_workers=8
```

### Python API

```python
from digitalmodel.modules.orcaflex.universal import UniversalOrcaFlexRunner

# Initialize runner
runner = UniversalOrcaFlexRunner(
    input_directory="configs/",
    output_directory="results/",
    mock_mode=False
)

# Run single model
result = runner.run_single("model.yml")

# Run batch with pattern
results = runner.run_batch(
    pattern="*.yml",
    parallel=True,
    max_workers=4
)

# Check results
for file_name, status in results.items():
    print(f"{file_name}: {status['success']}")
```

## Model Runner for .sim Generation

### Batch Processing

```python
from digitalmodel.modules.orcaflex.run_to_sim import OrcaFlexModelRunner

# Initialize runner
runner = OrcaFlexModelRunner()

# Run single model → .sim file
runner.run_single_model(
    model_file="model.yml",
    output_dir="results/.sim/"
)

# Batch processing with parallel execution
model_files = ["model1.yml", "model2.yml", "model3.yml"]
runner.run_batch(
    model_list=model_files,
    output_dir="results/.sim/",
    max_workers=30
)
```

## Analysis Types

### Static Analysis

Quick structural equilibrium check without time-domain simulation.

```yaml
orcaflex:
  analysis:
    static: true
    simulation: false
```

### Dynamic Simulation

Full time-domain hydrodynamic simulation.

```yaml
orcaflex:
  analysis:
    static: false
    simulation: true
```

### Iterative Analysis

Run multiple iterations with parameter variations.

```yaml
orcaflex:
  analysis:
    iterate:
      flag: true
      parameters:
        - name: wave_height
          values: [2.0, 4.0, 6.0, 8.0]
        - name: wave_period
          values: [8, 10, 12]
```

### Mooring Analysis

Specialized mooring system analysis.

```yaml
orcaflex:
  analysis:
    mooring:
      flag: true
      line_types: ["chain", "wire", "polyester"]
      pretension_range: [100, 200, 300]  # kN
```

## Preprocessing Options

### Vessel Loading

Load vessel data from external sources.

```yaml
orcaflex:
  preprocess:
    VesselType_Loading:
      flag: true
      source: "vessel_database.csv"
      vessel_name: "FPSO_Alpha"
```

### YAML Validation

Check model configuration before running.

```yaml
orcaflex:
  preprocess:
    check_yml_file:
      flag: true
      strict: true
      report_path: "logs/validation_report.txt"
```

## Utilities

### License Check

```python
from digitalmodel.modules.orcaflex.orcaflex_utilities import OrcaflexUtilities

utils = OrcaflexUtilities()
if utils.is_orcaflex_available():
    print("OrcaFlex license available")
else:
    print("Running in mock mode")
```

### Model Loading

```python
# Load simulation with metadata
model, metadata = utils.get_model_and_metadata("simulation.sim")
print(f"Simulation period: {metadata['period']} seconds")
print(f"Time step: {metadata['timestep']} seconds")
```

### Wave Calculations

```python
# Calculate theoretical maximum wave height
Hmax = utils.get_theoretical_hmax({
    "Hs": 6.0,          # Significant wave height (m)
    "Tp": 12.0,         # Peak period (s)
    "duration": 3600,   # Storm duration (s)
    "gamma": 3.3        # JONSWAP peakedness
})
print(f"Theoretical Hmax: {Hmax:.2f} m")

# Calculate associated period
Tassociated = utils.get_tassociated(Hmax, Tp=12.0)
print(f"Associated period: {Tassociated:.2f} s")
```

## Error Handling

### Common Issues

1. **License Not Available**
   ```python
   # Use mock mode for development/testing
   runner = UniversalOrcaFlexRunner(mock_mode=True)
   ```

2. **Model Convergence Failure**
   - Check initial conditions
   - Reduce time step
   - Verify boundary conditions

3. **Memory Issues with Large Batches**
   - Limit `max_workers` parameter
   - Process in smaller batches
   - Use sequential processing for very large models

## Best Practices

### Project Setup

1. Always use the standardized folder structure
2. Keep original .dat files in `.dat/original/`
3. Use descriptive YAML configuration names
4. Version control configuration files, not .sim files

### Batch Processing

1. Start with mock mode to validate configuration
2. Use pattern matching for related analyses
3. Monitor logs for failures
4. Archive results with timestamps

### Performance

1. Use parallel processing for independent runs
2. Limit workers based on available licenses
3. Run compute-intensive jobs overnight
4. Clean up intermediate files after processing

## MCP Tool Integration

### Swarm Coordination
```javascript
// Initialize offshore analysis swarm
mcp__claude-flow__swarm_init { topology: "hierarchical", maxAgents: 5 }

// Spawn specialized agents
mcp__claude-flow__agent_spawn { type: "code-analyzer", name: "orcaflex-validator" }
mcp__claude-flow__agent_spawn { type: "tester", name: "simulation-verifier" }
```

### Memory Coordination
```javascript
// Store model configuration
mcp__claude-flow__memory_usage {
  action: "store",
  key: "orcaflex/model/config",
  namespace: "offshore",
  value: JSON.stringify({
    model: "mooring_analysis",
    status: "configured",
    timestamp: Date.now()
  })
}

// Track analysis progress
mcp__claude-flow__memory_usage {
  action: "store",
  key: "orcaflex/analysis/progress",
  namespace: "offshore",
  value: JSON.stringify({
    phase: "simulation",
    completion: 0.75,
    files_processed: 15
  })
}
```

## External Documentation

Automatically refreshed from:
- https://www.orcina.com/webhelp/OrcaFlex/
- https://www.orcina.com/resources/examples/
- https://www.dnv.com/rules-standards/

Refresh schedule:
- Official docs: Weekly
- Standards: Monthly
- Examples: Bi-weekly

## Related Skills

- [orcaflex-post-processing](../orcaflex-post-processing/SKILL.md) - Post-process simulation results
- [orcawave-analysis](../orcawave-analysis/SKILL.md) - Diffraction/radiation analysis
- [mooring-design](../mooring-design/SKILL.md) - Mooring system design
- [structural-analysis](../structural-analysis/SKILL.md) - Structural verification
- [aqwa-analysis](../aqwa-analysis/SKILL.md) - AQWA benchmark validation

## References

- OrcaFlex Documentation: [Orcina OrcaFlex](https://www.orcina.com/orcaflex/)
- OrcFxAPI Python Guide
- Universal Runner: `src/digitalmodel/modules/orcaflex/universal/README.md`
- Agent Configuration: `agents/orcaflex/agent.yaml`

---

## Version History

- **2.0.0** (2025-01-02): Merged agent capabilities from agents/orcaflex/, added MCP integration, critical production rules, external documentation refresh
- **1.0.0** (2024-12-01): Initial release with universal runner and batch processing
