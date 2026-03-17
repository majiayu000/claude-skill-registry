---
name: systems-architect
version: 1.1
last_updated: 2026-01-29
description: Use when designing software architecture for bioinformatics pipelines, defining data structures, planning scalability, or making technical design decisions for complex systems.
success_criteria:
  - Architecture addresses all functional requirements
  - Scalability considerations documented and planned
  - Technology choices justified with trade-offs explained
  - Data structures appropriate for use case
  - APIs and interfaces clearly defined
  - Technical specification complete for implementation
  - Non-functional requirements addressed (performance, maintainability)
extended_thinking_budget: 8192-12288
metadata:
    skill-author: David Angeles Albores
    category: bioinformatics-workflow
    workflow: software-development
    integrates-with: [bioinformatician, biologist-commentator, software-developer]
    use_extended_thinking_for:
      - Complex architectural decisions with multiple trade-offs
      - Scalability planning for large-scale data processing
      - Technology stack selection with competing options
      - Design pattern selection for novel problem domains
allowed-tools: [Read, Write, Bash]
---

# Systems Architect Skill

## Purpose

Design robust, scalable architectures for bioinformatics software and pipelines.

## When to Use This Skill

Use this skill when you need to:
- Design software architecture for complex bioinformatics systems
- Choose appropriate data structures (pandas, anndata, HDF5, databases)
- Plan for scalability (memory, compute, storage)
- Define APIs and interfaces between components
- Design pipeline orchestration (Snakemake, Nextflow, custom)
- Make technology stack decisions

## Workflow Integration

**Pattern: Requirements → Architecture Design → Implementation Spec**
```
Biologist Commentator validates requirements
    ↓
Systems Architect designs architecture
    ↓
Produces technical specification
    ↓
Software Developer implements from spec
```

## Core Responsibilities

### 1. System Design
- Component architecture (modular, extensible)
- Data flow design
- Error handling strategy
- Scalability planning

### 2. Technology Selection
- Data structures (when to use what)
- Storage formats (CSV, HDF5, Parquet, databases)
- Execution environments (local, HPC, cloud)
- Pipeline orchestration tools

### 3. Performance Planning
- Memory requirements estimation
- Compute resource allocation
- I/O optimization strategies
- Parallelization approach

### 4. Integration Strategy
- How to wrap existing tools
- Container strategy (Docker/Singularity)
- Dependency management
- Version pinning

### 5. Architecture Context Document
- Maintain persistent context document describing module structure
- Track dependencies and modification order for safe incremental changes
- Document intended usage patterns for each major component
- Provide streaming/incremental change strategies

## Architecture Context Document

The Architecture Context Document (`.architecture/context.md`) is a **persistent, version-controlled reference** that captures architectural intent across sessions. Unlike ephemeral handoffs (deleted after workflow completion), this document survives to guide future development.

**Purpose**: Provide all agents with a bird's-eye view of the codebase structure, preventing scope creep and ensuring dependency-respecting changes.

**Lifecycle**:
- **Created**: During Phase 3 (Architecture Design) of programming-pm workflow
- **Updated**: When architectural changes occur (new modules, dependency changes, interface modifications)
- **Read**: By senior-developer and junior-developer before starting implementation (pre-flight step)

**Template and protocols**: See `references/architecture-context-template.md` for:
- Four-section template (Module Interconnections, Usage Patterns, Modification Order, Streaming Strategies)
- Generation protocol (Phase 3, Bootstrap Mode for existing codebases, SIMPLE mode abbreviation)
- Maintenance protocol (when to update, staleness detection, drift handling)
- Merge conflict resolution

### Bootstrap Mode

For **existing codebases without an Architecture Context Document**, systems-architect generates the document during Phase 3 using static analysis:
1. List modules/components from directory structure (`src/`, `modules/`)
2. Infer dependencies from import statements
3. Mark unknowns explicitly with `[TBD]`, `[UNKNOWN]`, or `[INFERRED]` tags
4. Document incomplete areas as "Known Gaps" at document end

Bootstrap Mode prioritizes **incomplete but honest** documentation over fabricated completeness. Developers are instructed to treat the code as ground truth and report discrepancies.

## Standard Architecture Template

Use `assets/architecture_template.md`:

```
# System Architecture: [Project Name]

## Overview
[1-2 sentence system description]

## Components
1. [Component Name]: [Purpose]
2. [Component Name]: [Purpose]

## Data Flow
[Input] → [Processing] → [Output]

## Technology Stack
- Language: Python 3.11
- Key Libraries: pandas, numpy, scikit-learn
- Storage: HDF5 for matrices, SQLite for metadata
- Execution: Snakemake on HPC cluster

## Scalability
- Dataset size: [Expected range]
- Memory: [Requirements]
- Compute: [CPU cores, time estimates]
- Storage: [Space requirements]

## Error Handling
[Strategy for failures, retries, logging]

## Deployment
[Installation, configuration, execution]
```

## Data Structure Selection Guide

See `references/data_structure_guide.md` for full details.

**Quick Reference**:

| Use Case | Structure | When |
|----------|-----------|------|
| Tabular data <1GB | pandas DataFrame | General analysis |
| Tabular data >1GB | Dask DataFrame | Out-of-core processing |
| Single-cell data | AnnData | scRNA-seq analysis |
| Large matrices | HDF5 | Persistent storage |
| Relational queries | SQLite/PostgreSQL | Complex joins |
| Genomic intervals | BED/GFF files | Standard interchange |
| Time series | pandas with DatetimeIndex | Temporal data |

## Scalability Considerations

### Memory Estimation
```
RNA-seq count matrix: genes × samples × 8 bytes
  20,000 genes × 1,000 samples × 8 = 160 MB (fits in RAM)
  20,000 genes × 100,000 cells × 8 = 16 GB (need sparse or chunking)
```

### Compute Planning
```
DESeq2 analysis: O(n_genes × n_samples²)
  100 samples: ~5 minutes
  1,000 samples: ~8 hours
  Strategy: Subset for testing, full run overnight
```

### Storage Planning
```
FASTQ (compressed): 50-100 MB per million reads
  50M reads = 5 GB
  100 samples × 50M reads = 500 GB
  Strategy: Delete FASTQ after alignment, keep BAM
```

## Integration Patterns

### Wrapping External Tools
```python
# Pattern 1: Subprocess call
import subprocess
result = subprocess.run(
    ['fastqc', input_file, '-o', output_dir],
    capture_output=True, check=True
)

# Pattern 2: Python binding (preferred if available)
import pysam
bam = pysam.AlignmentFile(bam_file, 'rb')
```

### Container Strategy
```yaml
# Dockerfile approach for reproducibility
FROM python:3.11-slim
RUN pip install numpy pandas scikit-learn
COPY pipeline.py /app/
ENTRYPOINT ["python", "/app/pipeline.py"]
```

## Output: Technical Specification

Deliverable to Software Developer includes:
1. **Architecture diagram** (components + data flow)
2. **Component specifications** (inputs, outputs, responsibilities)
3. **Technology stack** (exact versions)
4. **Data structures** (schemas, formats)
5. **Error handling** (what to do when steps fail)
6. **Performance requirements** (memory, time, storage)
7. **Testing strategy** (unit, integration, validation)
8. **Architecture Context Document** (`.architecture/context.md` - persistent context for incremental development)

## References

For detailed guidance:
- `references/architecture_patterns.md` - Common patterns with pros/cons
- `references/data_structure_guide.md` - When to use which data structure
- `references/scalability_considerations.md` - Memory, compute, storage planning
- `references/integration_patterns.md` - How to wrap tools, containers, dependencies
- `references/architecture-context-template.md` - Architecture Context Document template, generation, and maintenance protocols

## Example Architecture

**Project**: QC Pipeline for 1,000 RNA-seq Samples

```
## Architecture Specification

### Overview
Parallel QC pipeline processing 1,000 bulk RNA-seq FASTQ files with automated report generation.

### Components
1. Validator: Check FASTQ integrity, format
2. QC Runner: Execute FastQC in parallel
3. Aggregator: Combine metrics with MultiQC
4. Reporter: Generate summary statistics and plots

### Data Flow
FASTQ files → Validator → QC Runner (parallel) → Aggregator → HTML Report

### Technology Stack
- Execution: Snakemake (manages dependencies, parallelization)
- QC: FastQC 0.12.1
- Aggregation: MultiQC 1.14
- Custom code: Python 3.11, pandas, matplotlib
- Storage: FASTQ (gzip), QC metrics (JSON), report (HTML)

### Scalability
- Data: 1,000 samples × 50M reads × 100 bp = 500 GB FASTQ
- Compute: 100 parallel jobs on HPC cluster
- Time: 30 min per sample → 300 min total (5 hours)
- Memory: 4 GB per FastQC job = 400 GB total (distributed)

### Error Handling
- Retry failed jobs (3 attempts)
- Continue pipeline if individual samples fail
- Log all errors with sample ID
- Final report includes QC pass/fail status per sample

### Deployment
- Install: conda env from environment.yml
- Config: samples.csv (list of FASTQ paths)
- Execute: snakemake --cores 100 --cluster "sbatch -c 4 --mem=4GB"
- Output: results/multiqc_report.html
```

Hands to Software Developer for implementation.

## Success Criteria

Architecture is complete when:
- [ ] All components clearly defined
- [ ] Data flow unambiguous
- [ ] Technology choices justified
- [ ] Scalability analyzed (memory, compute, storage)
- [ ] Error handling planned
- [ ] Developer can implement without architecture questions
