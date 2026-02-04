---
name: bio-prefect-dask-nextflow
description: Designs and scaffolds bioinformatics pipelines using Prefect (Python) with Dask for local/distributed task execution and Nextflow for HPC scheduler-native execution. Use when an agent must choose between Prefect+Dask vs Nextflow, generate runnable project skeletons, or adapt workflows for laptops, workstations, and HPC clusters (e.g., Slurm/PBS) with reproducibility, caching/resume, and resource-aware configuration.
---

# Bio Prefect + Dask + Nextflow

This skill helps an agent design, scaffold, and harden bioinformatics pipelines across:
- **Local workstation/laptop** (Prefect + Dask LocalCluster)
- **HPC clusters** (Nextflow executors; or Prefect → Slurm worker patterns)
- **Hybrid** patterns (Prefect orchestrates metadata/approvals/notifications; Nextflow runs heavy compute)

## Use this skill when
- The user mentions **Prefect**, **Dask**, **Nextflow**, **HPC**, **Slurm**, **PBS**, **nf-core**, or “bioinformatics pipeline”.
- The user needs **parallelism**, **distributed execution**, **retries**, **scheduling**, **reproducible runs**, or “local prototype then scale”.

## Outputs this skill should produce
When activated, the agent should return (and/or generate in a repo):
1. **Engine choice**: `prefect+dask`, `nextflow`, or `hybrid`, with rationale.
2. **Runnable scaffold** (files + commands) for the chosen engine.
3. **Resource plan** per step (cpus/mem/time) + I/O layout (scratch vs shared).
4. **Validation plan**: tiny test run + failure/retry + resume test.
5. **Pitfalls & mitigations**: what will likely break on HPC and why.

## 2-minute decision
Use the decision matrix for nuance: [decision-matrix.md](decision-matrix.md)

Default heuristics:
- Choose **Nextflow** if the pipeline is mainly **CLI tools over files**, must run on **HPC schedulers**, and reproducibility/caching are top priorities.
- Choose **Prefect + Dask** if the pipeline is mainly **Python functions**, needs **dynamic branching**, API/DB integration, or interactive development.
- Choose **Hybrid** if Prefect should own the “outer loop” (metadata, batching, approvals, notifications) while Nextflow owns “inner loop” compute.

## Standard workflow (agent playbook)
1. **Requirements intake**
   - Scheduler type (Slurm/PBS/LSF/etc), queue/partition rules, walltime limits, node topology.
   - Container policy (Docker vs Singularity/Apptainer vs no containers) and module/conda availability.
   - Data location and throughput constraints (shared FS vs scratch, object storage).
   - Parallelism shape (many independent samples? big distributed arrays? long single jobs?).
2. **Choose engine** using [decision-matrix.md](decision-matrix.md); state assumptions.
3. **Scaffold the project**
   - Prefect path → [prefect-dask.md](prefect-dask.md) and (if needed) [prefect-hpc-slurm.md](prefect-hpc-slurm.md)
   - Nextflow path → [nextflow-hpc.md](nextflow-hpc.md)
4. **Implement steps with replayable boundaries**
   - Each step idempotent; deterministic output paths.
   - Pass around *paths/URIs*, not giant in-memory objects.
5. **Add operational glue**
   - Logging, retries/timeouts, resource hints, output manifest.
6. **Validate locally**
   - Tiny dataset run + forced failure + resume/retry test.
7. **Scale to HPC**
   - Confirm filesystem layout, job submission permissions, and environment bootstrap.

## Response template
Use this template in your final answer to the user:

```markdown
# Pipeline plan: [name]

## Recommended engine
- Choice: [prefect+dask | nextflow | hybrid]
- Why: [3–6 bullet rationale]

## Project scaffold
- Files to create:
  - ...
- Commands to run:
  - ...

## Execution model
- Parallelism strategy:
- Resource plan (per step):
- Data layout (work/results/cache):

## Pitfalls & mitigations
- ...

## Validation checklist
- ...
```

## Deep references (read as needed)
- Engine comparison and “when to use what”: [decision-matrix.md](decision-matrix.md)
- Prefect + Dask local patterns: [prefect-dask.md](prefect-dask.md)
- Prefect on Slurm + Dask-on-HPC options: [prefect-hpc-slurm.md](prefect-hpc-slurm.md)
- Nextflow on HPC (executors, modules, resume/cache): [nextflow-hpc.md](nextflow-hpc.md)
- Examples (Prefect-only, Nextflow-only, Hybrid): [examples.md](examples.md)
- Validation loop + common failure modes: [validation-checklist.md](validation-checklist.md)

