---
name: development-workflow-orchestrator
version: "1.0.0"
category: coordination
description: "Development Workflow Orchestrator"
---

# Development Workflow Orchestrator

> **Version:** 1.0.0
> **Created:** 2026-01-05
> **Category:** workspace-hub
> **Related Skills:** sparc-workflow, knowledge-base-system, ai-questioning-pattern

## Overview

Orchestrates the complete development workflow: `user_prompt.md` → YAML configuration → pseudocode → TDD → implementation → execution. This skill automates the systematic approach to feature development defined in DEVELOPMENT_WORKFLOW.md, ensuring consistency and quality across all 26+ repositories.

## Purpose

**Automate and enforce the 6-phase development workflow:**
1. **User Requirements** (user_prompt.md - user-controlled)
2. **YAML Configuration** (AI-generated, structured input)
3. **Pseudocode Review** (AI-generated, user-approved)
4. **TDD Implementation** (tests first, then code)
5. **Code Implementation** (following pseudocode exactly)
6. **Bash Execution** (YAML-driven, direct execution)

## When to Use

**Trigger this skill for:**
- Any new feature implementation
- Any significant code changes
- Data analysis pipelines
- API development
- Workflow automation
- Module creation

**Examples:**
- "Implement CSV data analysis with interactive HTML reports"
- "Create API endpoint for user authentication"
- "Add bulk data processing pipeline"
- "Build monitoring dashboard"

## Workflow Phases

### Phase 1: User Requirements (READ ONLY)

**File:** `user_prompt.md`

**AI Actions:**
✅ **DO:**
- READ the file thoroughly
- ASK clarifying questions (MANDATORY)
- WAIT for user approval
- UNDERSTAND all requirements completely

❌ **DON'T:**
- Edit user_prompt.md (only user edits)
- Make assumptions about requirements
- Skip the questioning phase
- Proceed without explicit approval

**Question Template:**
```
I've reviewed your requirements in user_prompt.md. Before proceeding,
I need clarification on:

1. **Scope:** [Specific question about what's included/excluded]
2. **Technical approach:** [Question about implementation choices]
3. **Edge cases:** [How to handle specific scenarios]
4. **Performance:** [Any specific requirements or constraints]

Please provide guidance before I generate the YAML configuration.
```

**Example Interaction:**
```
USER: user_prompt.md created with "Analyze CSV data and generate report"

AI: Thank you for the requirements. Before generating YAML config:

1. **Data validation:** Should we validate CSV structure before processing?
   What columns are required?

2. **Statistics:** You mentioned "summary statistics" - which ones exactly?
   - Mean, median, mode, standard deviation?
   - Percentiles (25th, 50th, 75th)?
   - All of the above?

3. **Output format:** For the HTML report:
   - Should it be standalone or require external assets?
   - Dark mode support needed?
   - Any specific visualization preferences?

4. **Error handling:** If CSV is malformed:
   - Skip problematic rows and continue?
   - Fail immediately with error?
   - Attempt auto-fix?
```

### Phase 2: YAML Configuration Generation

**Output:** `config/input/feature-name-YYYYMMDD.yaml`
**Template:** `templates/input_config.yaml`

**AI generates structured configuration:**

```yaml
metadata:
  feature: "csv-data-analysis"
  created: "2026-01-05"
  status: "draft"
  author: "user"

requirements:
  input:
    - type: "csv"
    - path_type: "relative"
    - max_size_mb: 100
    - required_columns: ["id", "timestamp", "value"]

  processing:
    - calculate_statistics: true
    - statistics_types:
        - "mean"
        - "median"
        - "std"
        - "quantiles"
    - validation:
        - check_missing_values: true
        - check_data_types: true

  output:
    - format: "html"
    - visualization: "plotly"  # MANDATORY: interactive only
    - interactive: true
    - export_json: true
    - standalone: true

  constraints:
    - max_response_time_sec: 5
    - memory_limit_mb: 512

modules:
  - data_loader
  - statistics_calculator
  - validation
  - visualization_generator
  - report_builder

tests:
  - test_csv_loading
  - test_statistics_calculation
  - test_validation
  - test_report_generation
  - test_performance_constraint

execution:
  entry_point: "src/pipelines/csv_analysis_pipeline.py"
  bash_command: "python src/pipelines/csv_analysis_pipeline.py --config config/input/csv-data-analysis-20260105.yaml"
```

**Validation Checklist:**
- [ ] All parameters explicitly defined
- [ ] No hardcoded paths (use relative)
- [ ] Validation rules specified
- [ ] Test coverage defined
- [ ] Execution command provided
- [ ] Follows HTML_REPORTING_STANDARDS (interactive plots only)

### Phase 3: Pseudocode Review

**Output:** `docs/pseudocode/feature-name.md`
**Template:** `templates/pseudocode.md`

**AI generates implementation plan:**

```markdown
# Pseudocode: CSV Data Analysis Pipeline

## Module: DataLoader

```
FUNCTION load_csv(file_path, config):
  VALIDATE file_path is relative
  CHECK file_size <= config.max_size_mb
  READ csv_data FROM file_path

  IF validation_enabled:
    VALIDATE required_columns exist
    VALIDATE data_types are correct

  IF validation_fails:
    RAISE ValidationError with details

  RETURN csv_data
```

## Module: StatisticsCalculator

```
FUNCTION calculate_statistics(data, config):
  statistics = empty_dictionary

  FOR EACH statistic_type IN config.statistics_types:
    CASE statistic_type:
      WHEN "mean":
        statistics["mean"] = CALCULATE_MEAN(data)
      WHEN "median":
        statistics["median"] = CALCULATE_MEDIAN(data)
      WHEN "std":
        statistics["std"] = CALCULATE_STD(data)
      WHEN "quantiles":
        statistics["quantiles"] = CALCULATE_QUANTILES(data, [0.25, 0.5, 0.75])

  RETURN statistics
```

## Module: VisualizationGenerator

```
FUNCTION generate_interactive_plot(data, statistics, config):
  # MANDATORY: Use Plotly for interactive visualization
  # NO static matplotlib exports allowed

  plot = CREATE_PLOTLY_FIGURE()

  ADD_SCATTER(plot, data.x, data.y)
  ADD_HOVER_TOOLTIPS(plot, data)
  ADD_STATISTICS_ANNOTATIONS(plot, statistics)

  CONFIGURE_LAYOUT(plot, responsive=true)

  RETURN plot
```

## Integration Flow

```
MAIN FUNCTION run_pipeline(config_file):
  1. config = LOAD_YAML_CONFIG(config_file)
  2. data = DataLoader.load_csv(config.input.path, config)
  3. stats = StatisticsCalculator.calculate_statistics(data, config)
  4. plot = VisualizationGenerator.generate_interactive_plot(data, stats, config)
  5. report = ReportBuilder.generate_html(data, stats, plot, config)

  IF config.output.export_json:
    EXPORT_JSON(stats, output_path)

  RETURN report_path
```

## Error Handling

```
- FileNotFoundError → Raise with clear message
- FileSizeError → Raise if exceeds limit
- ValidationError → Raise with details of failures
- TimeoutError → Raise if exceeds time constraint
```

## Performance Optimization

```
- Use pandas for efficient CSV reading
- Lazy loading for large files
- Caching intermediate results
- Parallel processing where applicable
```
```

**User Review Required:**
```
AI: I've generated pseudocode in docs/pseudocode/csv-data-analysis.md.

Please review:
1. Algorithm logic - is it correct?
2. Edge cases - are they handled properly?
3. Performance - meets your needs?
4. Error handling - comprehensive enough?

Approve before I proceed to TDD implementation? (yes/no)
```

### Phase 4: TDD Implementation

**Test-Driven Development Cycle:**

```
1. RED   → Write failing test
2. GREEN → Write minimal code to pass
3. REFACTOR → Improve code quality
4. REPEAT
```

**Test Structure:**
```
tests/
├── unit/
│   ├── test_data_loader.py
│   ├── test_statistics_calculator.py
│   ├── test_validation.py
│   └── test_visualization_generator.py
├── integration/
│   └── test_csv_analysis_pipeline.py
├── performance/
│   └── test_performance_constraints.py
└── run_tests.sh
```

**Example Test (Red Phase):**
```python
# tests/unit/test_data_loader.py
import pytest
from src.modules.data_loader import CSVLoader

def test_load_csv_with_valid_file():
    """Test loading valid CSV file."""
    loader = CSVLoader(max_size_mb=10)
    data = loader.load("../data/test_sample.csv")

    assert data is not None
    assert len(data) > 0
    assert "required_column" in data.columns

def test_load_csv_rejects_oversized_file():
    """Test rejection of files exceeding size limit."""
    loader = CSVLoader(max_size_mb=1)

    with pytest.raises(FileSizeError):
        loader.load("../data/large_file.csv")

def test_load_csv_validates_required_columns():
    """Test validation of required columns."""
    loader = CSVLoader(required_columns=["id", "value"])

    with pytest.raises(ValidationError) as exc:
        loader.load("../data/missing_columns.csv")

    assert "missing required columns" in str(exc.value)
```

**Run Tests (Should Fail):**
```bash
$ pytest tests/unit/test_data_loader.py
# All tests FAIL - this is expected (RED phase)
```

**Implementation (Green Phase):**
```python
# src/modules/data_loader/csv_loader.py
import pandas as pd
from pathlib import Path

class CSVLoader:
    """Load and validate CSV files."""

    def __init__(self, max_size_mb=100, required_columns=None):
        self.max_size_mb = max_size_mb
        self.required_columns = required_columns or []

    def load(self, file_path):
        """Load CSV with validation."""
        path = Path(file_path)

        # Size validation
        if path.stat().st_size > self.max_size_mb * 1024 * 1024:
            raise FileSizeError(f"File exceeds {self.max_size_mb}MB limit")

        # Load data
        data = pd.read_csv(path)

        # Column validation
        missing = set(self.required_columns) - set(data.columns)
        if missing:
            raise ValidationError(f"Missing required columns: {missing}")

        return data
```

**Run Tests (Should Pass):**
```bash
$ pytest tests/unit/test_data_loader.py
# All tests PASS - this is expected (GREEN phase)
```

**Refactor Phase:**
- Improve code quality
- Add docstrings
- Optimize performance
- Keep tests passing

### Phase 5: Code Implementation

**Module Structure:**
```
src/
├── modules/
│   ├── data_loader/
│   │   ├── __init__.py
│   │   ├── csv_loader.py
│   │   └── validators.py
│   ├── statistics/
│   │   ├── __init__.py
│   │   └── calculator.py
│   └── visualization/
│       ├── __init__.py
│       └── plotly_generator.py
├── pipelines/
│   └── csv_analysis_pipeline.py
└── utils/
    ├── config_loader.py
    └── error_handlers.py
```

**Pipeline Integration:**
```python
# src/pipelines/csv_analysis_pipeline.py
"""
ABOUTME: CSV data analysis pipeline with interactive reporting
ABOUTME: Implements user_prompt requirements through YAML-driven workflow
"""

import argparse
import yaml
from pathlib import Path

from modules.data_loader import CSVLoader
from modules.statistics import StatisticsCalculator
from modules.visualization import PlotlyGenerator
from modules.reporting import HTMLReportBuilder

def run_pipeline(config_path):
    """Execute CSV analysis pipeline."""
    # Load configuration
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Load data (following pseudocode)
    loader = CSVLoader(
        max_size_mb=config['requirements']['input']['max_size_mb'],
        required_columns=config['requirements']['input']['required_columns']
    )
    data = loader.load(config['requirements']['input']['path'])

    # Calculate statistics (following pseudocode)
    calculator = StatisticsCalculator()
    stats = calculator.calculate(
        data,
        stat_types=config['requirements']['processing']['statistics_types']
    )

    # Generate interactive visualization (MANDATORY: Plotly)
    viz = PlotlyGenerator()
    plot = viz.create_interactive_plot(data, stats)

    # Build HTML report
    report_builder = HTMLReportBuilder()
    report_path = report_builder.generate(
        data=data,
        statistics=stats,
        plot=plot,
        config=config
    )

    print(f"✓ Report generated: {report_path}")
    return report_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV Analysis Pipeline")
    parser.add_argument("--config", required=True, help="Path to YAML config")
    args = parser.parse_args()

    run_pipeline(args.config)
```

### Phase 6: Bash Execution

**Direct Execution Script:**
```bash
#!/bin/bash
# scripts/run_csv_analysis.sh

set -e

CONFIG_FILE="$1"
OUTPUT_DIR="${2:-./reports}"

if [ -z "$CONFIG_FILE" ]; then
    echo "Usage: ./scripts/run_csv_analysis.sh <config.yaml> [output_dir]"
    exit 1
fi

echo "Running CSV analysis pipeline..."
echo "Config: $CONFIG_FILE"
echo "Output: $OUTPUT_DIR"

# Direct execution - shortest route
python src/pipelines/csv_analysis_pipeline.py \
    --config "$CONFIG_FILE" \
    --output "$OUTPUT_DIR" \
    --verbose

echo "✓ Pipeline completed successfully!"
echo "Report: $OUTPUT_DIR/report.html"
```

**Usage:**
```bash
# Single command execution
./scripts/run_csv_analysis.sh config/input/csv-data-analysis-20260105.yaml

# With custom output
./scripts/run_csv_analysis.sh config/input/csv-data-analysis-20260105.yaml ./custom_output
```

## Automation Workflow

### Complete Automation Script

```bash
#!/bin/bash
# scripts/workflow_orchestrator.sh

set -e

FEATURE_NAME="$1"

if [ -z "$FEATURE_NAME" ]; then
    echo "Usage: ./scripts/workflow_orchestrator.sh <feature-name>"
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Development Workflow: $FEATURE_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Phase 1: Read user_prompt.md
echo ""
echo "Phase 1: Reading user requirements..."
if [ ! -f "user_prompt.md" ]; then
    echo "✗ user_prompt.md not found"
    exit 1
fi
echo "✓ Requirements loaded"

# Phase 2: Generate YAML configuration
echo ""
echo "Phase 2: Generating YAML configuration..."
claude-flow workflow generate-yaml \
    --input user_prompt.md \
    --output "config/input/$FEATURE_NAME-$(date +%Y%m%d).yaml"
echo "✓ YAML configuration created"

# Phase 3: Generate pseudocode
echo ""
echo "Phase 3: Generating pseudocode..."
claude-flow workflow generate-pseudocode \
    --config "config/input/$FEATURE_NAME-$(date +%Y%m%d).yaml" \
    --output "docs/pseudocode/$FEATURE_NAME.md"
echo "✓ Pseudocode generated"
echo ""
echo "Please review: docs/pseudocode/$FEATURE_NAME.md"
echo "Press ENTER when approved, or Ctrl+C to abort..."
read

# Phase 4-5: TDD Implementation
echo ""
echo "Phase 4-5: TDD Implementation"
echo "1. Write tests in tests/unit/"
echo "2. Implement in src/modules/"
echo "3. Run: pytest tests/"
echo ""
echo "Continue when tests pass. Press ENTER..."
read

# Phase 6: Execution
echo ""
echo "Phase 6: Ready for execution"
echo "Run: ./scripts/run_$FEATURE_NAME.sh config/input/$FEATURE_NAME-$(date +%Y%m%d).yaml"
echo ""
echo "✓ Workflow setup complete!"
```

## Validation and Quality Gates

### Pre-Implementation Checklist

Before proceeding to each phase:

**Phase 1 → 2:**
- [ ] All clarifying questions asked and answered
- [ ] User requirements fully understood
- [ ] Edge cases identified
- [ ] Performance constraints clear

**Phase 2 → 3:**
- [ ] YAML configuration complete
- [ ] All parameters explicitly defined
- [ ] No hardcoded values
- [ ] Validation rules specified
- [ ] Test coverage defined

**Phase 3 → 4:**
- [ ] Pseudocode reviewed and approved
- [ ] Algorithm logic correct
- [ ] Error handling comprehensive
- [ ] Performance considerations addressed

**Phase 4 → 5:**
- [ ] All tests written (RED phase)
- [ ] Tests failing as expected
- [ ] Test coverage meets requirements (80%+)

**Phase 5 → 6:**
- [ ] All tests passing (GREEN phase)
- [ ] Code follows pseudocode exactly
- [ ] Refactoring complete
- [ ] Documentation updated

**Phase 6 → Deployment:**
- [ ] Bash execution tested
- [ ] Output verified
- [ ] Performance within constraints
- [ ] Error handling tested

## Standards Compliance

### Automatic Validation

**HTML Reporting:**
```python
def validate_reporting_standards(config):
    """Ensure HTML reporting standards compliance."""
    if config['output']['visualization'] not in ['plotly', 'bokeh', 'altair', 'd3']:
        raise StandardsViolation(
            "HTML_REPORTING_STANDARDS.md violation: "
            "Must use interactive plots (Plotly, Bokeh, Altair, D3.js). "
            "Static matplotlib exports NOT ALLOWED."
        )

    if not config['output']['interactive']:
        raise StandardsViolation(
            "Interactive mode must be enabled for all visualizations"
        )
```

**File Organization:**
```python
def validate_file_organization(module_path):
    """Ensure file organization standards compliance."""
    # Check module structure
    required_files = ['__init__.py', 'core.py']
    for file in required_files:
        if not (module_path / file).exists():
            raise StandardsViolation(
                f"FILE_ORGANIZATION_STANDARDS.md violation: "
                f"Missing required file: {file}"
            )

    # Check depth limit (max 5 levels)
    depth = len(module_path.parts)
    if depth > 5:
        raise StandardsViolation(
            "FILE_ORGANIZATION_STANDARDS.md violation: "
            f"Maximum folder depth exceeded ({depth} > 5)"
        )
```

**Testing Standards:**
```python
def validate_testing_standards(coverage_report):
    """Ensure testing framework standards compliance."""
    if coverage_report.line_coverage < 80:
        raise StandardsViolation(
            f"TESTING_FRAMEWORK_STANDARDS.md violation: "
            f"Line coverage {coverage_report.line_coverage}% < 80% minimum"
        )

    if coverage_report.branch_coverage < 75:
        raise StandardsViolation(
            f"Branch coverage {coverage_report.branch_coverage}% < 75% minimum"
        )
```

## Integration with Other Skills

**With knowledge-base-system:**
```python
# Load patterns and examples
kb = KnowledgeBase()
patterns = kb.search(query="YAML configuration", category="workflow")
examples = kb.examples.find(task="CSV analysis")

# Use KB templates
yaml_template = kb.templates.get("input_config.yaml")
pseudocode_template = kb.templates.get("pseudocode.md")
```

**With ai-questioning-pattern:**
```python
# Use questioning skill before YAML generation
questions = AIQuestioningPattern().generate_questions(user_prompt)
answers = await ask_user(questions)
yaml_config = generate_yaml(user_prompt, answers)
```

**With sparc-workflow:**
```python
# Integrate with SPARC phases
sparc = SPARCWorkflow()
sparc.specification(user_prompt)    # Phase 1-2
sparc.pseudocode(yaml_config)       # Phase 3
sparc.architecture(pseudocode)      # Design
sparc.refinement(tests, code)       # Phase 4-5
sparc.completion(execution)         # Phase 6
```

## Metrics and Success Criteria

**Workflow Efficiency:**
- Time from user_prompt to working code
- Number of rework cycles
- Standards violations caught early
- Test coverage achieved

**Quality Metrics:**
- First-try success rate
- Bug count in production
- Performance within constraints
- User satisfaction

**Compliance Metrics:**
- Standards violations (should be 0)
- Documentation completeness
- Test coverage (target: 80%+)
- Code review approval time

## Troubleshooting

**Problem: User requirements unclear**
```
Solution: Use AI Questioning Pattern skill
- Ask specific questions about ambiguities
- Provide options with trade-offs
- Wait for explicit approval
```

**Problem: YAML generation failing**
```
Solution: Use templates from knowledge base
- Load yaml_config.yaml template
- Fill in from user_prompt systematically
- Validate against schema
```

**Problem: Pseudocode not approved**
```
Solution: Iterate based on feedback
- Address specific concerns
- Provide alternatives
- Re-generate and re-submit
```

**Problem: Tests not passing**
```
Solution: Follow TDD cycle properly
- Verify tests are correct first
- Implement minimal code to pass
- Don't proceed until all tests pass
```

## Best Practices

1. **Always ask before implementing** - MANDATORY per AI_AGENT_GUIDELINES.md
2. **Follow the 6 phases strictly** - Don't skip or combine phases
3. **Use templates from knowledge base** - Ensure consistency
4. **Validate standards at each phase** - Catch violations early
5. **Document as you go** - Keep documentation in sync
6. **Test before implementing** - TDD is non-negotiable
7. **Execute via bash** - Direct, simple, efficient

---

## Version History

- **1.0.0** (2026-01-05): Initial development workflow orchestrator skill

---

**This skill ensures consistent, high-quality feature development across all repositories!** 🚀
