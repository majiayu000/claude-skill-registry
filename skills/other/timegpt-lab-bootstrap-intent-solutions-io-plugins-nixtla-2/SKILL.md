---
name: nixtla-timegpt-lab-bootstrap
description: Guides TimeGPT lab environment setup including Python dependencies, API key configuration, smoke testing, experiment workflows, and optional CI/CD integration. Inspects environment docs and scripts to provide step-by-step setup instructions, troubleshooting guidance, and onboarding for new developers. Use when setting up TimeGPT lab, troubleshooting environment issues, or running experiments.
allowed-tools: "Read,Glob,Grep"
version: "0.4.0"
license: "MIT"
---

# Nixtla TimeGPT Lab Bootstrap

Assists with setting up and validating the TimeGPT lab environment. Provides guidance on Python dependencies, API key configuration, environment validation, TimeGPT smoke testing, and config-driven experiment workflows. This skill is read-only and provides instructions without directly executing scripts or making API calls.

## Overview

This skill helps developers configure their local TimeGPT lab environment correctly. It inspects the lab's setup documentation, validation scripts, smoke test implementation, experiment harness, and configuration files to provide actionable setup instructions. It serves as the entry point for new developers joining the TimeGPT lab and as a troubleshooting aid for environment, API access, and experiment workflow issues.

Key capabilities:
- Inspects `docs/timegpt-env-setup.md` for canonical setup instructions
- Reviews `scripts/validate_env.py` to understand validation requirements
- Explains `scripts/timegpt_smoke_test.py` smoke test behavior and expected results
- Guides users through `scripts/run_experiment.py` experiment workflows
- Interprets experiment config (`experiments/timegpt_experiments.json`) and results
- Generates step-by-step setup guidance tailored to the user's context
- Identifies common configuration, API access, and experiment pitfalls with solutions
- Read-only skill: provides instructions but does NOT execute scripts or make API calls

## Prerequisites

**For this skill to be useful, the user needs**:
- Python 3.9+ installed on their local machine
- Access to install Python packages (`pip`)
- A valid Nixtla TimeGPT API key (obtainable from https://dashboard.nixtla.io/)
- Basic familiarity with command-line operations

**Required files**:
- `{baseDir}/docs/timegpt-env-setup.md` - Setup documentation (includes CI/CD integration section)
- `{baseDir}/scripts/validate_env.py` - Environment validation script
- `{baseDir}/scripts/timegpt_smoke_test.py` - TimeGPT API smoke test
- `{baseDir}/scripts/run_experiment.py` - Experiment harness
- `{baseDir}/experiments/timegpt_experiments.json` - Experiment configuration
- `{baseDir}/.env.example` - Example environment configuration
- `{baseDir}/data/timegpt_smoke_sample.csv` - Sample dataset for testing
- `{baseDir}/reports/timegpt_smoke_forecast.csv` - Forecast output (created after smoke test)
- `{baseDir}/reports/timegpt_experiments_results.csv` - Experiment metrics (created after experiments)
- `{baseDir}/reports/timegpt_experiments_summary.md` - Experiment summary (created after experiments)

**Optional CI/CD files** (Phase 09):
- `.github/workflows/timegpt-real-smoke.yml` - Weekly real-API smoke test workflow

## Instructions

When this skill is invoked, follow these steps:

### Step 1: Inspect Setup Documentation

Read the canonical setup guide:

```
{baseDir}/docs/timegpt-env-setup.md
```

Extract:
- Required Python version(s)
- Installation commands for dependencies
- Environment variable requirements (especially `NIXTLA_TIMEGPT_API_KEY`)
- Common troubleshooting scenarios

### Step 2: Review Validation Script

Read the environment validation script:

```
{baseDir}/scripts/validate_env.py
```

Understand what checks it performs:
- Python version validation
- Environment variable presence
- Package installation status

### Step 3: Generate Setup Guidance

Based on the user's request, provide tailored instructions:

**For first-time setup**:
1. Python environment creation and activation
2. Dependency installation (`pip install nixtla utilsforecast pandas`)
3. API key configuration (using `.env` file or shell export)
4. Running `validate_env.py` to confirm readiness
5. Running `timegpt_smoke_test.py` to test TimeGPT API access

**For troubleshooting**:
1. Identify the specific error from validation or smoke test output
2. Provide targeted fix (install package, set env var, upgrade Python, check API key)
3. Suggest re-running the appropriate script to confirm resolution

**For smoke test guidance**:
1. Explain what the smoke test does (ONE TimeGPT API call with sample data)
2. How to run it: `python scripts/timegpt_smoke_test.py`
3. What to expect (forecast saved to `reports/timegpt_smoke_forecast.csv`)
4. Cost considerations (single call, tiny dataset, minimal cost)

**For experiment guidance**:
1. Explain the experiment harness (`scripts/run_experiment.py`)
2. How experiments are configured (`experiments/timegpt_experiments.json`)
3. How to enable/disable experiments
4. How to run experiments: `python scripts/run_experiment.py`
5. How to interpret results (CSV metrics + Markdown summary)
6. Cost considerations (ONE API call per enabled experiment)

**For onboarding**:
1. Explain the purpose of the TimeGPT lab (API experimentation, workflow development)
2. Walkthrough of directory structure (`skills/`, `scripts/`, `experiments/`, `data/`, `reports/`, `docs/`)
3. Next steps after environment is validated, smoke test passes, and experiments run

### Step 4: Safety Guardrails

- **DO NOT** suggest committing `.env` files or API keys to git
- **DO NOT** claim the skill can execute scripts or make API calls directly (it's read-only)
- **DO NOT** provide placeholder or example API keys that could be confused with real keys
- **DO** remind users that `validate_env.py` is safe to run (no network calls)
- **DO** explain that `timegpt_smoke_test.py` makes ONE real API call (costs may apply)
- **DO** explain that `run_experiment.py` makes ONE API call per enabled experiment
- **DO** guide users to enable/disable experiments in config to control costs
- **DO** defer to official Nixtla documentation for advanced API usage patterns

## Output

The primary output of this skill is **guidance text** formatted as markdown or plain text:

- **Setup Instructions**: Step-by-step commands to configure the environment
- **Troubleshooting Advice**: Targeted solutions for specific validation failures
- **Environment Status Summary**: Interpretation of `validate_env.py` output
- **Next Steps**: Pointers to relevant documentation or scripts for further exploration

Example output format:

```markdown
## TimeGPT Lab Setup Instructions

### 1. Create Python Virtual Environment

cd 002-workspaces/timegpt-lab
python3 -m venv .venv-timegpt
source .venv-timegpt/bin/activate

### 2. Install Dependencies

pip install nixtla>=0.5.0 utilsforecast pandas

### 3. Configure API Key

cp .env.example .env
# Edit .env and set NIXTLA_TIMEGPT_API_KEY=your_actual_key_here

### 4. Validate Environment

python scripts/validate_env.py

Expected output: All checks should show ✓ (green checkmarks)

### 5. Run TimeGPT Smoke Test

python scripts/timegpt_smoke_test.py

Expected output: Forecast saved to reports/timegpt_smoke_forecast.csv

### 6. Next Steps

- Review forecast results in reports/
- Explore docs/timegpt-env-setup.md for detailed guidance
- Experiment with TimeGPT features using the lab environment
```

## Error Handling

### Missing Environment Variable

**Symptom**: `validate_env.py` shows `✗ NIXTLA_TIMEGPT_API_KEY environment variable NOT set`

**Solution**:

```bash
# Option 1: Export in current shell
export NIXTLA_TIMEGPT_API_KEY="your_key_here"

# Option 2: Use .env file (recommended)
cp .env.example .env
# Edit .env and add your key
```

### Import Errors

**Symptom**: `ImportError: No module named 'nixtla'`

**Solution**:

```bash
pip install nixtla utilsforecast pandas
```

### Python Version Too Old

**Symptom**: `validate_env.py` shows `✗ Python 3.8.x (unsupported)`

**Solution**:

```bash
# Upgrade Python to 3.9+ using your package manager
# Example (Ubuntu/Debian):
sudo apt update
sudo apt install python3.10

# Recreate virtual environment with new Python version
python3.10 -m venv .venv-timegpt
source .venv-timegpt/bin/activate
```

### File Not Found Errors

**Symptom**: Skill cannot locate `docs/timegpt-env-setup.md` or `scripts/validate_env.py`

**Solution**: Ensure Phase 3 was completed successfully. These files should have been created during TimeGPT lab bootstrap. If missing, re-run Phase 3 or contact the repository maintainer.

## Examples

### Example 1: First-Time Setup Request

**User Input**: "How do I set up the TimeGPT lab environment?"

**Skill Behavior**:
1. Read `docs/timegpt-env-setup.md`
2. Extract step-by-step setup instructions
3. Format as a clear, actionable guide
4. Include validation command at the end

**Output**: Step-by-step markdown guide (see "Output" section above)

### Example 2: Troubleshooting Validation Failure

**User Input**: "validate_env.py is failing with missing nixtla package"

**Skill Behavior**:
1. Identify the specific error (missing package)
2. Provide targeted fix: `pip install nixtla`
3. Suggest re-running validation to confirm

**Output**:

```markdown
## Troubleshooting: Missing nixtla Package

The error indicates the `nixtla` package is not installed in your current Python environment.

**Fix**:

pip install nixtla>=0.5.0 utilsforecast pandas

**Verify**:

python scripts/validate_env.py

All checks should now pass with ✓ symbols.
```

### Example 3: Testing TimeGPT API Access

**User Input**: "How do I test that TimeGPT is working?"

**Skill Behavior**:
1. Check that environment validation passed
2. Explain the smoke test script and its purpose
3. Provide instructions for running and interpreting results
4. Note cost considerations

**Output**:

```markdown
## Testing TimeGPT API Access

After validating your environment, run the TimeGPT smoke test:

**Run the Smoke Test**:

python scripts/timegpt_smoke_test.py

**What It Does**:
- Loads a small sample dataset (2 series, 90 days each)
- Makes ONE TimeGPT API forecast call (14-day horizon)
- Saves results to reports/timegpt_smoke_forecast.csv

**Expected Output (Success)**:

✓ TimeGPT Smoke Test: PASSED
Summary:
  Input series: 2
  Forecast horizon: 14 days
  Output: reports/timegpt_smoke_forecast.csv

**If It Fails**:
- Authentication error: Check your NIXTLA_TIMEGPT_API_KEY
- Dataset missing: Ensure you're in the correct directory
- Network error: Check internet connection

**Cost Note**:
This makes ONE real API call. Cost is minimal due to tiny dataset but varies by your TimeGPT plan. Don't run in a tight loop.

**Next Steps**:
- Review the forecast CSV in reports/
- Experiment with your own time series data
- Explore TimeGPT features and parameters
```

### Example 4: Running Experiments

**User Input**: "How do I run TimeGPT experiments and compare different forecast horizons?"

**Skill Behavior**:
1. Read `experiments/timegpt_experiments.json` to understand configured experiments
2. Explain the experiment harness workflow
3. Provide instructions for running and interpreting results
4. Note cost considerations

**Output**:

```markdown
## Running TimeGPT Experiments

The lab includes a config-driven experiment harness for systematic TimeGPT testing.

**Run Experiments**:

python scripts/run_experiment.py

**What It Does**:
- Loads experiment configs from experiments/timegpt_experiments.json
- Runs each enabled experiment (default: 2 enabled)
- Computes metrics (MAE, SMAPE) against holdout data
- Generates CSV + Markdown reports

**Default Experiments**:
- timegpt_baseline_14d: 14-day forecast (enabled)
- timegpt_baseline_28d: 28-day forecast (enabled)
- timegpt_short_7d: 7-day forecast (disabled)

**Expected Output**:

✓ Experiment Harness: COMPLETE
Experiments run: 2
Reports:
  - reports/timegpt_experiments_results.csv
  - reports/timegpt_experiments_summary.md

**Interpreting Results**:
- CSV: Per-series, per-experiment metrics for detailed analysis
- Markdown: Human-readable summary with comparative analysis
- Lower MAE/SMAPE indicates better forecast accuracy

**Cost Note**:
Each enabled experiment makes ONE API call. Default config = 2 API calls total.

**Modifying Experiments**:
- Edit experiments/timegpt_experiments.json
- Set "enabled": false to disable experiments
- Add new experiments by copying existing blocks
- Re-run to apply changes
```

### Example 5: Onboarding New Developer

**User Input**: "What is the TimeGPT lab and how do I get started?"

**Skill Behavior**:
1. Explain the purpose of the lab (API experimentation, workflow development)
2. Describe the directory structure
3. Provide setup instructions
4. Point to next steps

**Output**:

```markdown
## Welcome to TimeGPT Lab

The TimeGPT lab is a workspace for experimenting with Nixtla's TimeGPT API and developing forecasting workflows.

**Directory Structure**:
- skills/: Claude Skills for TimeGPT workflows
- scripts/: Python scripts for API experiments, validation, and smoke tests
- experiments/: Experiment configs (JSON)
- data/: Sample datasets (includes timegpt_smoke_sample.csv)
- reports/: Generated forecasts, metrics, and analysis
- docs/: Setup guides and best practices

**Getting Started**:
1. Follow setup instructions: docs/timegpt-env-setup.md
2. Run environment validation: python scripts/validate_env.py
3. Test TimeGPT access: python scripts/timegpt_smoke_test.py
4. Run experiments: python scripts/run_experiment.py
5. Review results in reports/

**Next Steps After Setup**:
- Review TimeGPT documentation: https://docs.nixtla.io/
- Experiment with custom datasets
- Design new experiments in experiments/timegpt_experiments.json
```

## Resources

**Internal References** (use `{baseDir}` for portability):
- Setup Guide: `{baseDir}/docs/timegpt-env-setup.md`
- Validation Script: `{baseDir}/scripts/validate_env.py`
- Smoke Test Script: `{baseDir}/scripts/timegpt_smoke_test.py`
- Experiment Harness: `{baseDir}/scripts/run_experiment.py`
- Experiment Config: `{baseDir}/experiments/timegpt_experiments.json`
- Sample Dataset: `{baseDir}/data/timegpt_smoke_sample.csv`
- Environment Example: `{baseDir}/.env.example`
- Workspace Standards: `{baseDir}/../.directory-standards.md` (in 002-workspaces root)

**External References**:
- Nixtla TimeGPT Documentation: https://docs.nixtla.io/
- Nixtla Dashboard (API keys): https://dashboard.nixtla.io/
- Nixtla SDK GitHub: https://github.com/Nixtla/nixtla

**Related Skills** (future):
- `nixtla-timegpt-forecaster`: Execute TimeGPT forecasts (Phase 4+)
- `nixtla-schema-mapper`: Transform data to Nixtla schema
- `nixtla-experiment-architect`: Design forecasting experiments

---

**Skill Version**: 0.4.0 (Bootstrap + Smoke Test + Experiments + CI/CD Integration)
**Phase**: 9 (TimeGPT Real-API CI Smoke)
**Status**: Lab-only skill, not yet promoted to 003-skills/
