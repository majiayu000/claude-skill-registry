---
name: data-pipeline-manager
version: 1.0
last_updated: 2026-01-29
description: Design and troubleshoot robust data pipelines with comprehensive quality validation, error handling, and monitoring capabilities for bioinformatics and data processing workflows
success_criteria:
  - Pipeline runs end-to-end without errors
  - Quality validation implemented at each stage
  - Error handling comprehensive and informative
  - Data format mismatches caught and reported
  - Monitoring and logging in place for troubleshooting
  - Pipeline failure modes documented with recovery strategies
  - Performance acceptable for expected data volumes
category: bioinformatics-workflow
integrates-with:
  - bioinformatician
  - systems-architect
---

# Data Pipeline Manager

## Purpose

The Data Pipeline Manager skill provides comprehensive guidance for designing, implementing, and troubleshooting data processing pipelines with emphasis on quality validation, error handling, and reliability. Data pipelines are a critical component of modern bioinformatics and data science workflows, yet they are a prevalent source of failures in automated systems. Poor data quality, format mismatches, missing files, and transient errors can cascade through pipelines, causing failures that are difficult to diagnose and fix.

This skill addresses these challenges by providing structured approaches to pipeline design, validation strategies at each stage, robust error handling patterns, and monitoring techniques. Whether you're building a new RNA-seq analysis pipeline, debugging a failed ETL job, or ensuring data quality across complex multi-stage workflows, this skill provides the frameworks and best practices needed for success.

The skill integrates closely with the bioinformatician skill (which implements specific bioinformatics pipelines) and the systems-architect skill (which designs the overall system architecture), providing the critical middle layer of pipeline orchestration, validation, and reliability.

## When to Use This Skill

Use the Data Pipeline Manager skill when you need to:

### Pipeline Design and Implementation

- Design new data processing pipelines from scratch
- Set up RNA-seq, ChIP-seq, or other genomics processing pipelines
- Build ETL (Extract, Transform, Load) workflows for data integration
- Create data transformation pipelines for machine learning preprocessing
- Implement batch processing systems for high-throughput data
- Design real-time streaming data pipelines

### Debugging and Troubleshooting

- Debug failed pipeline runs and identify root causes
- Investigate data quality issues causing downstream failures
- Trace errors through multi-stage pipeline workflows
- Identify bottlenecks and performance issues
- Diagnose format mismatches between pipeline stages
- Resolve dependency and ordering issues in complex workflows

### Quality Assurance

- Implement validation checks at each pipeline stage
- Ensure data quality and completeness throughout processing
- Verify format consistency between stages
- Validate output correctness and expected ranges
- Implement data integrity checks and checksums
- Monitor data quality metrics over time

### Error Recovery and Reliability

- Implement retry logic for transient failures
- Design checkpoint and resume capabilities
- Handle partial failures in parallel processing
- Implement rollback mechanisms for failed stages
- Design idempotent pipeline operations
- Create robust error logging and alerting systems

### Pipeline Optimization

- Optimize pipeline performance and resource usage
- Parallelize independent pipeline stages
- Reduce data transfer between stages
- Implement caching strategies for expensive operations
- Balance throughput and latency requirements
- Scale pipelines to handle increasing data volumes

## Core Workflow

The Data Pipeline Manager follows a structured six-stage workflow that ensures robust, reliable pipeline operation:

### 1. Design Phase

**Define Pipeline Architecture**

Begin by clearly defining the pipeline's purpose, inputs, outputs, and transformations. Use a structured approach:

- **Inputs**: Specify all input data sources, formats, schemas, and expected volume
- **Transformations**: Document each processing stage, its purpose, and dependencies
- **Outputs**: Define output formats, destinations, and success criteria
- **Dependencies**: Map dependencies between stages to identify sequential vs. parallel operations
- **Resources**: Estimate compute, memory, and storage requirements for each stage
- **Constraints**: Identify time, cost, and resource constraints

**Choose Pipeline Pattern**

Select the appropriate pipeline pattern based on your requirements:

- **Sequential**: Each stage depends on the previous stage's output
- **Parallel**: Multiple independent branches process different data or stages
- **Conditional**: Branching logic based on data content or intermediate results
- **Hybrid**: Combination of patterns for complex workflows

**Design for Observability**

Build in observability from the start:

- Define metrics to track at each stage (records processed, time taken, errors)
- Plan logging strategy (what to log, where, at what level)
- Design monitoring dashboards and alerting thresholds
- Implement tracing for distributed pipeline components

### 2. Input Validation

**Pre-Flight Checks**

Before processing begins, validate all inputs thoroughly:

- **Existence**: Verify all input files and data sources exist and are accessible
- **Format**: Check file formats match expected specifications (FASTQ, BAM, CSV, JSON)
- **Completeness**: Ensure files are complete and not corrupted (checksums, file size)
- **Schema**: Validate data schema matches expected structure (columns, data types)
- **Non-Empty**: Verify files contain actual data, not just headers or empty content
- **Encoding**: Check text encoding is correct (UTF-8, ASCII)
- **Permissions**: Verify read/write permissions for all required paths

**Content Validation**

Beyond basic format checks, validate data content:

- **Value Ranges**: Check numeric values fall within expected ranges
- **Required Fields**: Ensure all mandatory fields are present and non-null
- **Referential Integrity**: Verify foreign key relationships and identifiers
- **Consistency**: Check related fields are consistent (e.g., start < end coordinates)
- **Quality Metrics**: For bioinformatics data, check quality scores, read lengths
- **Sample Metadata**: Verify sample identifiers match expected manifest

**Early Failure Strategy**

Fail fast on input validation errors rather than processing invalid data:

- Report all validation errors clearly with specific file, line, and field information
- Provide actionable error messages explaining what's wrong and how to fix it
- Stop processing before consuming expensive resources
- Log validation errors for tracking and trend analysis

### 3. Transform Phase

**Stage-by-Stage Processing**

Execute each transformation stage with careful attention to reliability:

- **Isolation**: Process each stage independently with clear input/output contracts
- **Error Handling**: Wrap transformations in try-catch blocks with specific error handling
- **Progress Tracking**: Log progress at regular intervals (every N records or time period)
- **Resource Monitoring**: Track memory, CPU, and disk usage to detect resource issues
- **Intermediate Validation**: Validate data between stages to catch errors early
- **Checkpointing**: Save intermediate results for resumability after failures

**Transformation Best Practices**

Follow these practices for robust transformations:

- **Idempotency**: Design operations that can be safely retried without side effects
- **Atomic Operations**: Make changes atomically where possible (write to temp, then rename)
- **Batch Processing**: Process data in appropriately sized batches for memory efficiency
- **Error Context**: Capture rich error context (input data, parameters, environment)
- **Graceful Degradation**: Continue processing other data when individual records fail
- **Type Safety**: Use strong typing and validation to prevent type errors

**Handling Large Data**

For large-scale data processing:

- Stream data rather than loading entire datasets into memory
- Use chunking or windowing for processing large files
- Implement backpressure mechanisms to prevent overwhelming downstream stages
- Use efficient file formats (Parquet, Arrow) for intermediate data
- Consider distributed processing frameworks (Spark, Dask) for very large datasets

### 4. Output Validation

**Structure Validation**

Verify output structure meets specifications:

- **Format**: Confirm output files are in the correct format
- **Schema**: Validate output schema matches expected structure
- **Shape**: For tabular or array data, check dimensions are as expected
- **Completeness**: Ensure all expected output files are generated
- **Size**: Check output file sizes are reasonable (not empty, not suspiciously large)

**Content Validation**

Validate output data quality and correctness:

- **Value Ranges**: Check numeric outputs fall within biologically/logically plausible ranges
- **Missing Data**: Check for unexpected NaN, Inf, or null values
- **Distribution**: Verify output distributions are reasonable (not all zeros, reasonable variance)
- **Relationships**: Check relationships between output fields are logical
- **Sanity Checks**: Apply domain-specific sanity checks (e.g., gene counts are positive)
- **Regression Checks**: Compare key metrics against baseline or previous runs

**Quality Metrics**

Calculate and report quality metrics:

- Record counts (inputs vs. outputs, filtered, passed)
- Success rates and error rates by stage
- Data quality scores and flags
- Processing time and resource usage
- Coverage and completeness metrics
- Domain-specific quality metrics (alignment rates, duplication rates)

### 5. Error Handling

**Error Classification**

Classify errors to determine appropriate handling:

- **Transient Errors**: Network timeouts, temporary resource unavailability, rate limits
- **Permanent Errors**: Format errors, missing required data, logic errors
- **Configuration Errors**: Wrong parameters, missing credentials, invalid paths
- **Resource Errors**: Out of memory, disk full, quota exceeded
- **Data Errors**: Invalid values, corrupted files, schema mismatches

**Retry Logic**

Implement intelligent retry strategies:

- **Transient Failures**: Retry with exponential backoff (e.g., 1s, 2s, 4s, 8s)
- **Max Retries**: Set reasonable retry limits (3-5 retries typically)
- **Backoff Strategy**: Use exponential backoff with jitter to avoid thundering herd
- **Circuit Breaker**: Stop retrying if error rate exceeds threshold
- **Idempotency**: Ensure retried operations don't cause duplicate processing
- **Timeout**: Set appropriate timeouts for each operation

**Logging and Diagnostics**

Create comprehensive error logs:

- **Structured Logging**: Use structured formats (JSON) for easy parsing
- **Context**: Include input data, parameters, environment, stack traces
- **Severity Levels**: Use appropriate log levels (ERROR, WARN, INFO, DEBUG)
- **Correlation IDs**: Track related log entries across distributed systems
- **Error Patterns**: Log patterns that enable error aggregation and analysis
- **Sensitive Data**: Avoid logging sensitive data (credentials, PII)

**Checkpointing for Resumability**

Enable pipeline resumption after failures:

- Save pipeline state at strategic points (after expensive operations)
- Record completed stages and their outputs
- Store metadata about what remains to be processed
- Enable resume from last successful checkpoint
- Clean up checkpoints after successful completion
- Handle concurrent checkpoint access in distributed systems

### 6. Monitoring and Alerting

**Real-Time Monitoring**

Track pipeline health in real-time:

- **Stage Progress**: Monitor progress through each pipeline stage
- **Processing Rate**: Track records/bytes processed per second
- **Queue Depth**: Monitor input queues and backlogs
- **Error Rate**: Track errors per stage and overall
- **Resource Usage**: Monitor CPU, memory, disk, network usage
- **Latency**: Track end-to-end and per-stage latency

**Alerting Strategy**

Set up intelligent alerts:

- **Failure Alerts**: Immediate alerts for pipeline failures
- **Degradation Alerts**: Alerts when performance degrades below thresholds
- **Data Quality Alerts**: Alerts when quality metrics fall outside expected ranges
- **Resource Alerts**: Alerts approaching resource limits
- **SLA Alerts**: Alerts when SLAs are at risk
- **Alert Fatigue**: Avoid over-alerting; aggregate and prioritize

**Dashboard Design**

Create effective monitoring dashboards:

- Overall pipeline status and health indicators
- Stage-by-stage progress visualization
- Error rates and types over time
- Resource utilization trends
- Data quality metrics over time
- Historical performance comparisons

## Pipeline Patterns

### Sequential Pipeline

**Description**: Each stage depends on the previous stage's output. Data flows linearly through the pipeline.

**Use Cases**:
- RNA-seq analysis: FASTQ → QC → Alignment → Count Matrix → Differential Expression
- Data ETL: Extract → Transform → Load
- Image processing: Load → Preprocess → Model Inference → Post-process

**Advantages**:
- Simple to understand and implement
- Easy to reason about data flow
- Natural checkpointing at each stage
- Clear dependency management

**Disadvantages**:
- Limited parallelism
- Slowest stage becomes bottleneck
- Failure at any stage stops entire pipeline

**Implementation Considerations**:
- Implement clear stage interfaces with defined inputs/outputs
- Validate data between each stage
- Save intermediate outputs for debugging and resume
- Use pipeline orchestration tools (Snakemake, Nextflow, Airflow)

### Parallel Pipeline

**Description**: Multiple independent branches process data simultaneously without dependencies.

**Use Cases**:
- Processing multiple samples independently
- Running multiple tools on same input data
- Processing different data partitions
- Fan-out pattern for distributing work

**Advantages**:
- High throughput through parallelism
- Failures in one branch don't affect others
- Good resource utilization
- Natural scaling with more workers

**Disadvantages**:
- Requires careful resource management
- More complex error handling
- Need to aggregate results from branches
- Potential for resource contention

**Implementation Considerations**:
- Partition data appropriately for parallel processing
- Implement worker pools or parallel execution frameworks
- Handle partial failures gracefully
- Aggregate results correctly from all branches
- Balance load across workers to avoid stragglers

### Conditional Pipeline

**Description**: Pipeline branches based on data content or intermediate results.

**Use Cases**:
- Different processing based on data type or quality
- Skip expensive steps when not needed
- Route samples to different analysis paths
- Quality-based filtering and routing

**Advantages**:
- Efficient resource usage (skip unnecessary work)
- Flexible workflow adapts to data
- Can optimize processing path based on characteristics
- Handles heterogeneous data naturally

**Disadvantages**:
- More complex logic and testing
- Harder to predict resource requirements
- Debugging is more challenging
- Need to handle all possible paths

**Implementation Considerations**:
- Make branching logic explicit and well-documented
- Validate that all paths are tested
- Log which path was taken for each item
- Ensure consistent output format across paths
- Handle edge cases at branch points

### Hybrid Pipeline

**Description**: Combination of sequential, parallel, and conditional patterns for complex workflows.

**Use Cases**:
- Multi-omics integration pipelines
- Complex bioinformatics workflows
- Enterprise ETL with multiple data sources
- Machine learning pipelines with feature engineering

**Advantages**:
- Maximum flexibility for complex requirements
- Optimized throughput and resource usage
- Can model real-world workflows accurately
- Best performance for complex dependencies

**Disadvantages**:
- Most complex to design and maintain
- Difficult to debug and troubleshoot
- Requires sophisticated orchestration
- Testing is challenging

**Implementation Considerations**:
- Use workflow management systems (Nextflow, Snakemake, Airflow)
- Document pipeline DAG (Directed Acyclic Graph) clearly
- Implement comprehensive testing for all paths
- Use visualization tools for pipeline understanding
- Modularize pipeline components for reusability

## Quality Validation Strategies

### Input Validation

**File Existence and Accessibility**

```python
# Check file exists and is readable
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Input file not found: {input_file}")
if not os.access(input_file, os.R_OK):
    raise PermissionError(f"Cannot read input file: {input_file}")
```

**Format Validation**

```python
# Validate FASTQ format
def validate_fastq(file_path):
    with open(file_path) as f:
        line_count = 0
        for line in f:
            line_count += 1
            if line_count % 4 == 1 and not line.startswith('@'):
                raise ValueError(f"Invalid FASTQ format at line {line_count}")
            if line_count % 4 == 3 and not line.startswith('+'):
                raise ValueError(f"Invalid FASTQ format at line {line_count}")
```

**Non-Empty Validation**

```python
# Check file is not empty
file_size = os.path.getsize(input_file)
if file_size == 0:
    raise ValueError(f"Input file is empty: {input_file}")
if file_size < expected_min_size:
    raise ValueError(f"Input file is too small: {file_size} bytes")
```

**Schema Validation**

```python
# Validate CSV schema
required_columns = ['sample_id', 'condition', 'batch']
df = pd.read_csv(metadata_file)
missing_cols = set(required_columns) - set(df.columns)
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")
```

### Intermediate Validation

**Dimension Checking**

```python
# Validate array dimensions
if counts_matrix.shape[0] != n_genes:
    raise ValueError(f"Expected {n_genes} genes, got {counts_matrix.shape[0]}")
if counts_matrix.shape[1] != n_samples:
    raise ValueError(f"Expected {n_samples} samples, got {counts_matrix.shape[1]}")
```

**Missing Data Detection**

```python
# Check for NaN and Inf values
if np.isnan(data).any():
    nan_count = np.isnan(data).sum()
    raise ValueError(f"Data contains {nan_count} NaN values")
if np.isinf(data).any():
    inf_count = np.isinf(data).sum()
    raise ValueError(f"Data contains {inf_count} Inf values")
```

**Range Validation**

```python
# Validate numeric ranges
if (data < 0).any():
    raise ValueError("Data contains negative values (expected non-negative)")
if data.max() > expected_max:
    raise ValueError(f"Data contains values above {expected_max}")
```

### Output Validation

**Completeness Checking**

```python
# Verify all expected outputs exist
expected_outputs = ['counts.csv', 'qc_metrics.json', 'results.html']
for output_file in expected_outputs:
    if not os.path.exists(output_file):
        raise ValueError(f"Missing expected output: {output_file}")
```

**Distribution Validation**

```python
# Check output distributions are reasonable
mean_count = counts_matrix.mean()
if mean_count < 100:
    warnings.warn(f"Low mean count: {mean_count} (expected > 100)")
if counts_matrix.std() / mean_count > 10:
    warnings.warn(f"High coefficient of variation: {counts_matrix.std() / mean_count}")
```

**Sanity Checks**

```python
# Domain-specific sanity checks
if alignment_rate < 0.5:
    warnings.warn(f"Low alignment rate: {alignment_rate:.1%} (expected > 50%)")
if duplication_rate > 0.3:
    warnings.warn(f"High duplication rate: {duplication_rate:.1%} (expected < 30%)")
```

## Error Handling Strategies

### Transient Error Retry

**Exponential Backoff**

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except TransientError as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
            return None
        return wrapper
    return decorator
```

### Checkpoint Implementation

**Basic Checkpointing**

```python
def process_with_checkpoint(items, checkpoint_file, process_func):
    # Load checkpoint if exists
    completed = set()
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file) as f:
            completed = set(json.load(f))

    # Process items, skipping completed ones
    for item in items:
        if item in completed:
            continue

        process_func(item)
        completed.add(item)

        # Save checkpoint
        with open(checkpoint_file, 'w') as f:
            json.dump(list(completed), f)
```

### Comprehensive Error Logging

**Structured Error Context**

```python
import logging
import json

def log_pipeline_error(stage, error, context):
    error_data = {
        'timestamp': datetime.now().isoformat(),
        'stage': stage,
        'error_type': type(error).__name__,
        'error_message': str(error),
        'context': context,
        'traceback': traceback.format_exc()
    }
    logging.error(json.dumps(error_data))
```

## Bioinformatics-Specific Considerations

### FASTQ to Count Matrix Pipeline

**Standard Workflow**:
1. **Quality Control**: FastQC on raw FASTQ files
2. **Preprocessing**: Trimming adapters and low-quality bases (Trimmomatic, cutadapt)
3. **Alignment**: Align to reference genome (STAR, HISAT2, BWA)
4. **Quality Control**: Check alignment metrics (samtools, picard)
5. **Quantification**: Count reads per gene (featureCounts, HTSeq, RSEM)
6. **Count Matrix**: Assemble counts into matrix for downstream analysis

**Critical Validation Points**:
- Raw read quality scores (median Q30+)
- Adapter contamination levels
- Alignment rate (>70% for RNA-seq)
- Duplicate rate (<30%)
- Gene detection rate (>10,000 genes for human)
- Count distribution (not zero-inflated)

### Genome Build Consistency

**Problem**: Mixing genome builds (hg19 vs hg38, mm9 vs mm10) causes misalignments and incorrect results.

**Solution**:
- Document genome build in metadata and file headers
- Validate genome build consistency across all samples
- Check reference FASTA matches annotation GTF
- Verify chromosome naming conventions (chr1 vs 1)
- Use genome build as pipeline parameter
- Include genome build in output file names

### Sample Metadata Tracking

**Essential Metadata**:
- Sample identifier (unique across study)
- Biological condition/phenotype
- Technical batch information
- Sequencing run information
- Library preparation protocol
- Genome build and annotation version
- Processing date and pipeline version

**Validation**:
- Check sample IDs match between FASTQ files and metadata
- Verify no duplicate sample IDs
- Ensure required metadata fields are present
- Validate controlled vocabulary terms
- Check metadata-data consistency (e.g., species matches reference)

### Reference Data Management

**Best Practices**:
- Version control reference genomes and annotations
- Use consistent naming conventions
- Store checksums for reference files
- Document reference source and version
- Maintain separate references per genome build
- Validate reference integrity before each run

## Integration with Other Skills

### Integration with Bioinformatician Skill

The Data Pipeline Manager provides the framework and infrastructure for pipelines that the bioinformatician skill implements:

- **Design Phase**: Data Pipeline Manager designs pipeline architecture; bioinformatician selects specific tools
- **Implementation**: Bioinformatician implements analysis steps; Data Pipeline Manager adds validation and error handling
- **Debugging**: Data Pipeline Manager identifies pipeline failures; bioinformatician debugs analysis-specific issues
- **Optimization**: Data Pipeline Manager optimizes pipeline orchestration; bioinformatician optimizes algorithm performance

### Integration with Systems Architect Skill

The Data Pipeline Manager implements pipelines within infrastructure designed by systems-architect:

- **Architecture**: Systems architect designs overall system; Data Pipeline Manager designs pipeline components
- **Scalability**: Systems architect provides infrastructure scaling; Data Pipeline Manager implements pipeline parallelization
- **Reliability**: Systems architect ensures infrastructure reliability; Data Pipeline Manager implements pipeline reliability
- **Monitoring**: Systems architect provides monitoring infrastructure; Data Pipeline Manager implements pipeline-specific monitoring

## Summary

The Data Pipeline Manager skill provides comprehensive guidance for building robust, reliable data processing pipelines. By following the structured workflow of design, input validation, transformation, output validation, error handling, and monitoring, you can create pipelines that handle errors gracefully, validate data quality at every stage, and provide clear diagnostics when issues occur.

Key principles:
- Validate early and often at every pipeline stage
- Fail fast with clear, actionable error messages
- Implement intelligent retry logic for transient errors
- Use checkpointing for resumability after failures
- Monitor pipeline health and data quality continuously
- Design for observability from the start
- Integrate with complementary skills for complete solutions

Whether you're building new pipelines or troubleshooting existing ones, this skill provides the patterns, strategies, and best practices needed for success in bioinformatics and data processing workflows.
