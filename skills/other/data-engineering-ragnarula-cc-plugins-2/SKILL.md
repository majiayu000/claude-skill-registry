---
name: data-engineering
description: Use this skill when designing or reviewing data pipelines, ETL processes, data warehouses, streaming systems, or any system where data movement, transformation, and quality are primary concerns. Applies data engineering thinking to specifications, designs, and implementations.
version: 0.1.0
---

# Data Engineering

## When to Apply

Use this skill when the system involves:
- Data pipelines (batch or streaming)
- ETL/ELT processes
- Data warehouses or data lakes
- Schema design and evolution
- Data quality and validation
- Event streaming platforms (Kafka, Kinesis, etc.)

## Mindset

Data engineers think about data as a product with its own lifecycle, quality, and contracts.

**Questions to always ask:**
- What's the source of truth? Where does this data originate?
- What happens when upstream data is late, missing, or malformed?
- What's the schema? How will it evolve?
- How do we know the data is correct? What are the quality checks?
- What's the latency requirement? Batch or streaming?
- Who consumes this data? What's their contract?
- How do we replay or backfill if something goes wrong?

**Assumptions to challenge:**
- "The data is clean" - It's not. Validate everything.
- "Schema won't change" - It will. Design for evolution.
- "We process everything" - What about late data? Duplicates? Out-of-order?
- "It's just a simple transform" - Transforms accumulate. Document lineage.
- "We'll fix data quality later" - Garbage in, garbage out. Validate early.
- "Batch is good enough" - Is it? What's the actual latency requirement?

## Practices

### Schema Design
Design schemas for evolution. Use explicit versioning. Prefer additive changes (new fields) over breaking changes. Document every field. **Don't** make breaking changes without migration plans, use generic field names, or leave fields undocumented.

### Schema Evolution
Support backward and forward compatibility where possible. Use schema registries for enforcement. Plan migration paths for breaking changes. **Don't** break consumers without warning, skip validation against schema, or ignore compatibility rules.

### Data Quality
Validate data at ingestion. Define quality rules (completeness, uniqueness, ranges). Monitor quality metrics. Quarantine bad data; don't propagate it. **Don't** trust upstream data, skip validation for performance, or silently drop bad records.

### Idempotent Processing
Design pipelines to produce the same output when run multiple times. Use deterministic logic. Handle duplicates explicitly. **Don't** assume exactly-once delivery, use non-deterministic functions without care, or let duplicate processing cause incorrect results.

### Late & Out-of-Order Data
Define how late data is handled (accept with window, drop, or sidetrack). Use event time, not processing time. Design for out-of-order arrival. **Don't** assume data arrives in order, ignore late data silently, or use processing time for ordering.

### Lineage & Documentation
Track where data comes from and where it goes. Document transformations. Maintain data dictionaries. **Don't** lose track of data sources, have undocumented transformations, or let documentation drift from reality.

### Testing Pipelines
Test transformations with known inputs/outputs. Test edge cases (nulls, empty, malformed). Test schema compatibility. Test failure and recovery. **Don't** skip pipeline testing, test only happy path, or deploy without validating output schema.

### Backfill & Recovery
Design for reprocessing. Keep raw data immutable. Have clear backfill procedures. Test recovery before you need it. **Don't** mutate source data, lose ability to reprocess, or wait until disaster to test recovery.

## Vocabulary

Use precise terminology:

| Instead of | Say |
|------------|-----|
| "real-time" | "streaming with < 1s latency" / "micro-batch every 5 min" |
| "data quality" | "null rate < 1%" / "unique constraint on X" / "range [0, 100]" |
| "schema" | "Avro schema v2" / "backward compatible" |
| "pipeline" | "batch DAG" / "streaming topology" / "ELT job" |
| "source" | "source of truth" / "derived from X" / "CDC from Y" |
| "delay" | "event time lag" / "processing latency" / "watermark" |

## SDD Integration

**During Specification:**
- Define data sources and their reliability
- Specify latency requirements (batch windows, streaming SLAs)
- Establish data quality requirements
- Identify consumers and their contracts

**During Design:**
- Document schema with compatibility strategy
- Design validation rules per stage
- Specify handling for late/duplicate/malformed data
- Plan for backfill and disaster recovery
- Document data lineage

**During Review:**
- Verify schemas are documented and versioned
- Check quality validation is implemented at ingestion
- Confirm idempotent processing
- Validate late data handling is defined
- Ensure backfill procedures exist and are tested
