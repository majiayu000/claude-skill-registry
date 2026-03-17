---
name: yaml-workflow-executor
description: Execute configuration-driven analysis workflows from YAML files. Use for running analysis pipelines, data processing tasks, and automation workflows defined in YAML configuration.
version: 1.1.0
category: development
related_skills:
  - data-pipeline-processor
  - engineering-report-generator
  - parallel-file-processor
---

# YAML Workflow Executor

> Version: 1.1.0
> Category: Development
> Last Updated: 2026-01-02

Execute configuration-driven workflows where YAML files define the analysis parameters, data sources, and execution steps.

## Quick Start

```yaml
# config/workflows/analysis.yaml
task: analyze_data

input:
  data_path: data/raw/measurements.csv

output:
  results_path: data/results/analysis.json

parameters:
  filter_column: status
  filter_value: active
```

```python
from workflow_executor import execute_workflow

# Execute workflow
result = execute_workflow("config/workflows/analysis.yaml")
print(f"Status: {result['status']}")
```

```bash
# CLI execution
python -m workflow_executor config/workflows/analysis.yaml --verbose
```

## When to Use

- Running analysis defined in YAML configuration files
- Executing data processing pipelines from config
- Automating repetitive tasks with parameterized configs
- Building reproducible workflows
- Processing multiple scenarios from config variations

## Core Pattern

```
YAML Config -> Load -> Validate -> Route to Handler -> Execute -> Output
```

## Implementation

### Configuration Loader

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class WorkflowConfig:
    """Configuration container for workflow execution."""
    task: str
    input: Dict[str, Any] = field(default_factory=dict)
    output: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
    options: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'WorkflowConfig':
        """Load configuration from YAML file."""
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {yaml_path}")

        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        return cls(
            task=data.get('task', 'default'),
            input=data.get('input', {}),
            output=data.get('output', {}),
            parameters=data.get('parameters', {}),
            options=data.get('options', {})
        )

    def validate(self) -> bool:
        """Validate configuration has required fields."""
        if not self.task:
            raise ValueError("Configuration must specify 'task'")
        return True
```

### Workflow Router

```python
class WorkflowRouter:
    """Route tasks to appropriate handlers based on configuration."""

    def __init__(self):
        self.handlers = {}

    def register(self, task_name: str, handler_func):
        """Register a handler for a task type."""
        self.handlers[task_name] = handler_func

    def route(self, config: WorkflowConfig) -> Any:
        """Route configuration to appropriate handler."""
        task = config.task

        if task not in self.handlers:
            available = ', '.join(self.handlers.keys())
            raise ValueError(f"Unknown task: {task}. Available: {available}")

        handler = self.handlers[task]
        logger.info(f"Routing to handler: {task}")

        return handler(config)

# Global router instance
router = WorkflowRouter()
```

### Handler Registration Pattern

```python
def register_handlers(router: WorkflowRouter):
    """Register all available task handlers."""

    @router.register('analyze_data')
    def analyze_data(config: WorkflowConfig):
        """Handler for data analysis tasks."""
        import pandas as pd

        # Load input
        df = pd.read_csv(config.input['data_path'])

        # Apply parameters
        if config.parameters.get('filter_column'):
            col = config.parameters['filter_column']
            val = config.parameters['filter_value']
            df = df[df[col] == val]

        # Process
        results = {
            'row_count': len(df),
            'columns': list(df.columns),
            'statistics': df.describe().to_dict()
        }

        # Save output
        if config.output.get('results_path'):
            import json
            with open(config.output['results_path'], 'w') as f:
                json.dump(results, f, indent=2)

        return results

    @router.register('generate_report')
    def generate_report(config: WorkflowConfig):
        """Handler for report generation tasks."""
        # Import report generator
        from .report_generator import generate_report

        return generate_report(
            data_path=config.input['data_path'],
            output_path=config.output['report_path'],
            title=config.parameters.get('title', 'Analysis Report'),
            sections=config.parameters.get('sections', {})
        )

    @router.register('transform_data')
    def transform_data(config: WorkflowConfig):
        """Handler for data transformation tasks."""
        import pandas as pd

        df = pd.read_csv(config.input['data_path'])

        # Apply transformations from config
        transforms = config.parameters.get('transforms', [])
        for transform in transforms:
            op = transform['operation']
            if op == 'rename':
                df = df.rename(columns=transform['mapping'])
            elif op == 'filter':
                df = df.query(transform['expression'])
            elif op == 'aggregate':
                df = df.groupby(transform['by']).agg(transform['agg'])
            elif op == 'sort':
                df = df.sort_values(transform['by'], ascending=transform.get('ascending', True))

        # Save output
        df.to_csv(config.output['data_path'], index=False)
        return {'rows': len(df), 'columns': len(df.columns)}
```

### Main Executor

```python
def execute_workflow(yaml_path: str, overrides: Dict[str, Any] = None) -> Any:
    """
    Execute workflow from YAML configuration.

    Args:
        yaml_path: Path to YAML config file
        overrides: Optional parameter overrides

    Returns:
        Workflow execution results
    """
    # Load config
    config = WorkflowConfig.from_yaml(yaml_path)

    # Apply overrides
    if overrides:
        config.parameters.update(overrides)

    # Validate
    config.validate()

    # Log execution
    logger.info(f"Executing workflow: {config.task}")
    logger.info(f"Input: {config.input}")
    logger.info(f"Output: {config.output}")

    # Register handlers and route
    register_handlers(router)
    result = router.route(config)

    logger.info(f"Workflow completed: {config.task}")
    return result
```

## YAML Configuration Format

### Basic Structure

```yaml
# config/workflows/analysis.yaml

task: analyze_data

input:
  data_path: data/raw/measurements.csv
  schema_path: config/schemas/measurements.json  # optional

output:
  results_path: data/results/analysis.json
  report_path: reports/analysis.html

parameters:
  filter_column: status
  filter_value: active
  date_range:
    start: "2024-01-01"
    end: "2024-12-31"

options:
  verbose: true
  parallel: false
  cache: true
```

### Data Transformation Config

```yaml
task: transform_data

input:
  data_path: data/raw/source.csv

output:
  data_path: data/processed/transformed.csv

parameters:
  transforms:
    - operation: rename
      mapping:
        old_name: new_name
        date_col: timestamp

    - operation: filter
      expression: "value > 0 and status == 'valid'"

    - operation: aggregate
      by: [category, month]
      agg:
        value: [sum, mean, count]
        quantity: sum

    - operation: sort
      by: timestamp
      ascending: true
```

### Report Generation Config

```yaml
task: generate_report

input:
  data_path: data/processed/results.csv

output:
  report_path: reports/monthly_analysis.html

parameters:
  title: "Monthly Production Analysis"
  project: "Field Development Project"
  sections:
    summary: |
      <p>Analysis of production data for the reporting period.</p>
    methodology: |
      <p>Data processed using standard statistical methods.</p>
  charts:
    - type: line
      x: date
      y: production
      title: "Daily Production Trend"

    - type: bar
      x: well_id
      y: cumulative
      color: status
      title: "Well Performance Comparison"
```

### Multi-Step Workflow

```yaml
task: pipeline

steps:
  - name: extract
    task: transform_data
    input:
      data_path: data/raw/source.csv
    output:
      data_path: data/staging/extracted.csv

  - name: transform
    task: transform_data
    input:
      data_path: data/staging/extracted.csv
    output:
      data_path: data/processed/transformed.csv
    depends_on: extract

  - name: analyze
    task: analyze_data
    input:
      data_path: data/processed/transformed.csv
    output:
      results_path: data/results/analysis.json
    depends_on: transform

  - name: report
    task: generate_report
    input:
      data_path: data/processed/transformed.csv
    output:
      report_path: reports/final_report.html
    depends_on: analyze
```

## CLI Integration

### Command-Line Interface

```python
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Execute YAML-defined workflows'
    )
    parser.add_argument(
        'config',
        help='Path to YAML configuration file'
    )
    parser.add_argument(
        '--override', '-o',
        action='append',
        help='Parameter override (key=value)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate config without executing'
    )

    args = parser.parse_args()

    # Parse overrides
    overrides = {}
    if args.override:
        for item in args.override:
            key, value = item.split('=', 1)
            overrides[key] = value

    # Configure logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')

    try:
        if args.dry_run:
            config = WorkflowConfig.from_yaml(args.config)
            config.validate()
            print(f"Configuration valid: {args.config}")
            print(f"Task: {config.task}")
            return 0

        result = execute_workflow(args.config, overrides)
        print(f"Workflow completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

### Bash Wrapper

```bash
#!/bin/bash
# scripts/run_workflow.sh

CONFIG_FILE="${1:?Usage: $0 <config.yaml> [--override key=value]}"
shift

# Activate environment if needed
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Run workflow
python -m workflow_executor "$CONFIG_FILE" "$@"
```

## Usage Examples

### Example 1: Run Analysis

```bash
# Direct execution
python -m workflow_executor config/workflows/analysis.yaml

# With overrides
python -m workflow_executor config/workflows/analysis.yaml \
    --override filter_value=completed \
    --override date_range.start=2024-06-01

# Via bash script
./scripts/run_workflow.sh config/workflows/analysis.yaml -v
```

### Example 2: Batch Processing

```python
from pathlib import Path

# Process multiple configs
config_dir = Path('config/workflows/')
for config_file in config_dir.glob('*.yaml'):
    print(f"Processing: {config_file}")
    result = execute_workflow(str(config_file))
    print(f"Result: {result}")
```

### Example 3: Programmatic Use

```python
# Load and modify config programmatically
config = WorkflowConfig.from_yaml('config/base.yaml')
config.parameters['custom_param'] = 'value'
config.input['data_path'] = 'data/custom_input.csv'

result = router.route(config)
```

### Example 4: Dynamic Workflow Generation

```python
import yaml

def generate_workflow_config(data_files: list, output_dir: str) -> str:
    """Generate workflow config for multiple data files."""
    config = {
        'task': 'pipeline',
        'steps': []
    }

    for i, data_file in enumerate(data_files):
        config['steps'].append({
            'name': f'process_{i}',
            'task': 'analyze_data',
            'input': {'data_path': data_file},
            'output': {'results_path': f'{output_dir}/result_{i}.json'}
        })

    config_path = 'config/generated_workflow.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(config, f)

    return config_path
```

## Best Practices

### Do

1. Keep configs in `config/workflows/` directory
2. Use descriptive filenames: `<domain>_<task>_<variant>.yaml`
3. Version control all configurations
4. Use comments to document parameters
5. Validate configs before execution with `--dry-run`
6. Log sufficient context for debugging

### Don't

1. Hardcode absolute paths
2. Skip input validation
3. Mix configuration with implementation
4. Create overly complex nested configs
5. Ignore error handling

### Configuration Design
- Keep configs in `config/workflows/` directory
- Use descriptive filenames: `<domain>_<task>_<variant>.yaml`
- Version control all configurations
- Use comments to document parameters

### Handler Development
- One handler per task type
- Validate inputs at handler start
- Log progress for long-running tasks
- Return structured results

### File Organization
```
project/
    config/
        workflows/           # Workflow configs
            analysis.yaml
            transform.yaml
        schemas/             # Validation schemas
    src/
        workflow_executor/   # Executor code
    scripts/
        run_workflow.sh      # CLI wrapper
    data/
        raw/
        processed/
        results/
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError` | Config file missing | Verify config path |
| `ValueError: Unknown task` | Handler not registered | Check task name spelling |
| `KeyError` | Missing required config field | Add missing field to YAML |
| `yaml.YAMLError` | Invalid YAML syntax | Validate YAML format |

### Error Template

```python
def safe_execute_workflow(yaml_path: str) -> dict:
    """Execute workflow with comprehensive error handling."""
    try:
        # Validate config exists
        if not Path(yaml_path).exists():
            return {'status': 'error', 'message': f'Config not found: {yaml_path}'}

        # Load and validate
        config = WorkflowConfig.from_yaml(yaml_path)
        config.validate()

        # Execute
        result = execute_workflow(yaml_path)
        return {'status': 'success', 'result': result}

    except yaml.YAMLError as e:
        return {'status': 'error', 'message': f'Invalid YAML: {e}'}
    except ValueError as e:
        return {'status': 'error', 'message': f'Validation error: {e}'}
    except Exception as e:
        return {'status': 'error', 'message': f'Execution error: {e}'}
```

## Execution Checklist

- [ ] YAML config file exists and is valid
- [ ] All required fields present (task, input, output)
- [ ] Input data files exist
- [ ] Output directories exist or can be created
- [ ] Handler registered for specified task
- [ ] Parameters are correctly typed
- [ ] Dry-run validation passes
- [ ] Logging configured for debugging
- [ ] Error handling covers all failure modes

## Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Config Load Time | <100ms | YAML parsing speed |
| Validation Time | <50ms | Config validation duration |
| Handler Dispatch | <10ms | Routing overhead |
| Total Execution | Varies | Depends on task complexity |

## Related Skills

- [data-pipeline-processor](../data-pipeline-processor/SKILL.md) - Data transformation
- [engineering-report-generator](../engineering-report-generator/SKILL.md) - Report generation
- [parallel-file-processor](../parallel-file-processor/SKILL.md) - Batch file processing

---

## Version History

- **1.1.0** (2026-01-02): Upgraded to SKILL_TEMPLATE_v2 format with Quick Start, Error Handling, Metrics, Execution Checklist, additional examples
- **1.0.0** (2024-10-15): Initial release with WorkflowConfig, WorkflowRouter, CLI integration
