---
name: run-job-data
description: Run generate_job_data to execute a study definition
allowed-tools: Bash
argument-hint: "[--asan] <definition.json> [--start DATE] [--end DATE] [--cash AMOUNT] [--name NAME]"
---

# Run Job Data

Execute a study definition using `generate_job_data`.

## Usage

```bash
# Research study (no trading)
/run-job-data "job_data/definitions/test_runner/my_research.json" --start 2023-01-01 --end 2023-12-31

# Trading campaign (with cash)
/run-job-data "job_data/definitions/test_runner/my_strategy.json" --cash 100000 --start 2023-01-01 --end 2023-12-31

# Debug with AddressSanitizer
/run-job-data --asan "job_data/definitions/test_runner/my_strategy.json" --cash 100000
```

## Options

| Option | Description |
|--------|-------------|
| `--asan` | Use debug build with AddressSanitizer (must be first arg) |
| `--start DATE` | Start date (default: 2023-01-01) |
| `--end DATE` | End date (default: 2023-12-31) |
| `--cash AMOUNT` | Initial cash - creates trading campaign if set |
| `--name NAME` | Output name (default: definition filename) |

## Run

```bash
/home/adesola/EpochDev/ClaudeCodeResearch/cpp_tools/run_generate_job_data.sh $ARGUMENTS
```

## Notes

- **Research study**: Omit `--cash` - outputs to `research_studies/`
- **Trading campaign**: Include `--cash` - outputs to `campaigns/`
- Build first with `/build-job-data` if binary is missing
