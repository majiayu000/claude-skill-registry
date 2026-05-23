---
name: running-examples
description: Runs Breakdown CLI examples for user-perspective verification. Use when testing Breakdown as a real user would, verifying use cases work correctly, checking environment-related issues, running example scripts (03-22), setting up examples environment, or cleaning up after examples. Keywords: examples, run examples, user test, use case test, setup examples, clean examples, verify breakdown.
allowed-tools: Bash, Read
---

# Running Breakdown Examples

Breakdown の examples/ を実行し、ユーザー視点での動作確認を行う。

## When to Use

- ユーザー視点での動作確認（ユニットテストではなく実際の利用方法）
- 環境起因の問題確認
- ユースケース網羅確認
- リリース前のユーザー体験検証

## Key Principle

examples/ はテストではない。ユーザーと同じ方法で Breakdown を実行し、実際の動作を確認するもの。

## Quick Commands

### Setup (Required First)

```bash
cd /Users/tettuan/github/breakdown/examples
bash 03_setup_environment.sh
```

### Basic Verification (05-08)

```bash
bash 05_basic_usage.sh      # to, summary, defect
bash 06_stdin_example.sh    # STDIN input
bash 07_summary_issue.sh    # summary issue
bash 08_defect_patterns.sh  # defect patterns
```

### Config Tests (09-15)

```bash
bash 09_config_basic.sh
bash 10_config_destination_prefix.sh
bash 11_config_environments.sh
bash 12_config_team.sh
bash 13_config_production.sh
bash 14_config_production_example.sh
bash 15_config_production_custom.sh
```

### Parameter Tests (16-18)

```bash
bash 16_input_parameter.sh       # --edition/-e=
bash 17_adaptation_parameter.sh  # --adaptation/-a=
bash 18_custom_variables.sh      # --uv-*
```

### Advanced (19-21)

```bash
bash 19_pipeline_processing.sh
bash 20_batch_processing.sh
bash 21_error_handling.sh
```

### Cleanup (Required Last)

```bash
bash 22_clean.sh
```

## Full Sequence

```bash
cd /Users/tettuan/github/breakdown/examples

# Setup
bash 03_setup_environment.sh

# Basic (05-08)
for i in 05 06 07 08; do bash ${i}_*.sh; done

# Config (09-15)
for i in 09 10 11 12 13 14 15; do bash ${i}_*.sh; done

# Params (16-18)
for i in 16 17 18; do bash ${i}_*.sh; done

# Advanced (19-21)
for i in 19 20 21; do bash ${i}_*.sh; done

# Cleanup
bash 22_clean.sh
```

## Script Summary

| Range | Purpose                                     |
| ----- | ------------------------------------------- |
| 01-02 | Guidance, install info                      |
| 03-04 | Environment setup                           |
| 05-08 | Basic commands (to, summary, defect, stdin) |
| 09-15 | Configuration variations                    |
| 16-18 | Parameter options                           |
| 19-21 | Advanced patterns                           |
| 22    | Cleanup                                     |

## Error Recovery

```bash
bash 22_clean.sh              # Clean first
bash 03_setup_environment.sh  # Re-setup
# Then retry failed script
```

## Output Verification

If these directories exist at project root (not in examples/), something is wrong: `prompts`,
`prompt`, `output`, `schema`, `schemas`, `configs`

## References

- `examples/README.md` - Full documentation
- `examples/CLAUDE.md` - Purpose and rules
