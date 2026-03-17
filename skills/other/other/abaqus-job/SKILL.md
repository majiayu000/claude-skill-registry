---
name: abaqus-job
description: Create and manage Abaqus jobs. Use when user asks to run the analysis, submit the job, execute the model, or generate input file.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Job Skill

This skill creates, submits, and monitors Abaqus analysis jobs. Use it when the model is ready to run.

## When to Use This Skill

**Route here when user says:**
- "Run the analysis", "Submit the job", "Execute the model"
- "Generate input file", "Create INP file"
- "Run in parallel", "Check job status"

**Route elsewhere:**
- Reading results after completion → `/abaqus-odb`
- Setting up the model → use other module skills

## Prerequisites

Before job submission:
1. Model is complete (geometry, material, mesh, BCs, loads, step)
2. Model saved to .cae file
3. No validation errors

## Workflow: Running an Analysis

### Step 1: Save the Model
Always save before creating a job. The .cae file must exist.

### Step 2: Create the Job
Specify job name and model name. They can differ.

### Step 3: Choose Submission Mode

| User Wants | Action |
|------------|--------|
| Run analysis and wait | Submit with waitForCompletion |
| Generate INP only (no run) | writeInput |
| Run in background | Submit without waiting |
| Run from command line | `abaqus job=Name interactive` |

### Step 4: Wait and Monitor
For interactive submission, monitor status until COMPLETED or ABORTED.

### Step 5: Check Results
If COMPLETED, results are in .odb file. If ABORTED, check .msg file.

## Key Decisions

### Submit vs Write Input?

| Goal | Method |
|------|--------|
| Run analysis now | submit() |
| Only create INP file | writeInput() |
| Run later from CLI | writeInput, then `abaqus job=Name` |

### Parallel Processing

| Scenario | Setting |
|----------|---------|
| Small model / Learning Edition | numCpus=1 |
| Large model, multi-core | numCpus=N, numDomains=N |
| Single machine | mp_mode=THREADS |
| Cluster | mp_mode=MPI |

## What to Ask User

If unclear, ask:
- "Ready to run the analysis?"
- "How many CPUs for parallel?"
- "Just need the input file, or run the analysis?"

## Output Files

| Extension | Content |
|-----------|---------|
| .odb | Results database (use /abaqus-odb to read) |
| .dat | Printed output (nodal values, summaries) |
| .msg | Solver messages - **check this if job fails** |
| .sta | Status file (increment progress) |
| .inp | Input file (model definition) |
| .lck | Lock file (exists while job runs) |

## Troubleshooting

| Status/Error | Meaning | Solution |
|--------------|---------|----------|
| COMPLETED | Success | Proceed to /abaqus-odb |
| ABORTED | Failed | Check .msg file for error |
| License not available | No tokens | Wait or check license server |
| Memory error | Model too large | Increase memory or coarsen mesh |
| .lck file exists | Stale lock | Delete if job is not running |

## Validation Checklist

Before submitting:
- [ ] Model saved (.cae exists)
- [ ] Job name specified
- [ ] Model name matches saved model
- [ ] CPUs set appropriately

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
