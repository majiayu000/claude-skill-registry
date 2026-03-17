---
name: build-job-data
description: Build generate_job_data binary (release or ASAN debug mode)
allowed-tools: Bash
argument-hint: "[--asan]"
---

# Build Job Data

Build the `generate_job_data` binary with file locking to prevent concurrent builds.

## Usage

```bash
# Release build (default)
/build-job-data

# Debug build with AddressSanitizer
/build-job-data --asan
```

## Run

```bash
/home/adesola/EpochDev/ClaudeCodeResearch/cpp_tools/build_generate_job_data.sh $ARGUMENTS
```

## Notes

- Uses `flock` to ensure only one build runs at a time
- Release builds use `/home/adesola/EpochDev/EpochBackend/build`
- ASAN builds use `/home/adesola/EpochDev/EpochBackend/build-asan`
