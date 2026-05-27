---
name: blockchain-data-collection-validation
description: Empirical validation workflow for blockchain data collection pipelines before production implementation. Use when validating data sources, testing DuckDB integration, building POC collectors, or verifying complete fetch-to-storage pipelines for blockchain data.
---

# Blockchain Data Collection Validation

## Overview

This skill provides a systematic, test-driven workflow for validating blockchain data collection pipelines before production implementation. Use when building POC collectors, validating new data sources, testing DuckDB integration, or verifying complete fetch-to-storage workflows.

**Key principle**: Validate every component empirically before implementation—connectivity, schema, rate limits, storage, and complete pipeline.

## Validation Workflow

This skill follows a 5-step empirical validation workflow:

| Step                | Purpose                      | Output                          | Success Criteria                      |
| ------------------- | ---------------------------- | ------------------------------- | ------------------------------------- |
| **1. Connectivity** | Test basic RPC access        | Block fetch confirmed           | Response <500ms, no errors            |
| **2. Schema**       | Validate all required fields | Field validation report         | All fields present, types correct     |
| **3. Rate Limits**  | Find sustainable RPS         | Empirical rate (e.g., 5.79 RPS) | 100% success over 50+ blocks          |
| **4. Pipeline**     | Test fetch→DuckDB flow       | Complete pipeline working       | Data persisted, constraints pass      |
| **5. Decision**     | Document findings            | Go/No-Go recommendation         | All steps passed, timeline calculated |

**Detailed workflow**: See `references/validation-workflow.md` for complete step-by-step guide with code templates, testing patterns, and success criteria for each step.

**Quick start**: Create `01_single_block_fetch.py` using template in `scripts/`, then iterate through steps 2-5.

## DuckDB Integration Patterns

**Critical patterns for data integrity**:

- CHECKPOINT requirement (crash-tested, prevents data loss)
- Batch INSERT from DataFrame (124K blocks/sec performance)
- CHECK constraints for schema validation
- Storage estimates (76-100 bytes/block empirically validated)

**Full guide**: See `references/duckdb-patterns.md` for complete DuckDB integration guide with code examples, crash test results, and performance benchmarks.

## Common Pitfalls

**Critical mistakes to avoid**: Skipping empirical rate validation, testing <50 blocks, forgetting DuckDB CHECKPOINT (data loss), ignoring CHECK constraints, and parallel fetching on free tiers.

**Real-world examples**: LlamaRPC 50 RPS documented → 1.37 RPS sustainable (2.7% of max), parallel fetch worked for 20 blocks → failed at 50.

**Full guide**: See `references/common-pitfalls.md` for detailed anti-patterns with problem/reality/solution format and code examples.

## Scripts

POC template scripts for empirical validation:

- `poc_single_block.py` - Connectivity and schema validation (Steps 1-2)
- `poc_batch_parallel_fetch.py` - Parallel fetch testing (Step 3, expect failures)
- `poc_rate_limited_fetch.py` - Rate-limited sequential fetch (Step 3, find sustainable rate)
- `poc_complete_pipeline.py` - Complete fetch→DuckDB pipeline (Step 4)

**Templates and usage**: See `scripts/README.md` for complete code templates, usage examples, and testing progression guide.

## References

### Workflow Documentation

- `references/validation-workflow.md` - Complete 5-step workflow with detailed guidance, code examples, and success criteria
- `references/common-pitfalls.md` - Anti-patterns to avoid with problem/reality/solution format
- `references/example-workflow.md` - Complete case study: Validating Alchemy for Ethereum collection

### Technical Patterns

- `references/duckdb-patterns.md` - DuckDB integration patterns (CHECKPOINT, batch INSERT, constraints, performance)
- `references/ethereum-collector-poc-findings.md` - Ethereum collector POC case study with rate limit discovery

### Scripts

- `scripts/README.md` - Complete script templates and testing progression guide
- `scripts/poc_single_block.py` - Connectivity and schema validation template
- `scripts/poc_batch_parallel_fetch.py` - Parallel fetch testing template
- `scripts/poc_rate_limited_fetch.py` - Rate-limited fetch template
- `scripts/poc_complete_pipeline.py` - Complete pipeline template

## Example Workflow

**Case study**: Validating Alchemy for Ethereum collection → ✅ GO at 5.79 RPS sustained (26 days for 13M blocks, HIGH confidence).

**Full walkthrough**: See `references/example-workflow.md` for complete step-by-step case study showing all 5 validation steps with actual test results and final decision.

## When to Use This Skill

Invoke this skill when:

- Validating a new blockchain RPC provider before implementation
- Testing DuckDB integration for blockchain data
- Building POC collector for new blockchain
- Verifying complete fetch-to-storage pipeline
- Investigating data quality issues
- Planning production collector implementation
- Need empirical validation before committing to architecture

## Related Patterns

This skill pairs well with:

- `blockchain-rpc-provider-research` - For comparing multiple providers before validation
- Project scratch investigations in `scratch/ethereum-collector-poc/` and `scratch/duckdb-batch-validation/`
