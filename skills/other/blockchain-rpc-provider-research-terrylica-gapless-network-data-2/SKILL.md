---
name: blockchain-rpc-provider-research
description: Systematic workflow for researching and validating blockchain RPC providers. Use when evaluating RPC providers for historical data collection, rate limits, archive access, compute unit costs, or timeline estimation for large-scale blockchain data backfills.
---

# Blockchain RPC Provider Research

## Overview

This skill provides a systematic, empirically-validated workflow for researching blockchain RPC providers before committing to large-scale data collection projects. Use when selecting an RPC provider for historical blockchain data backfill, evaluating rate limits, comparing free tier options, or estimating collection timelines.

**Key principle**: Never trust documented rate limits—always validate empirically with POC testing.

## Investigation Workflow

This skill follows a 5-step workflow. Each step builds on the previous:

1. **Research Official Documentation** - Survey provider docs, pricing, archive access
2. **Calculate Theoretical Timeline** - Compute expected collection time from documented limits
3. **Empirical Validation with POC Testing** - Test actual rate limits (CRITICAL STEP)
4. **Create Comparison Matrix** - Build side-by-side provider comparison
5. **Document Findings and Make Recommendation** - Write comprehensive analysis report

**Detailed workflow**: See `references/workflow-steps.md` for complete step-by-step guide with code examples, questions to answer, and success criteria.

**Quick start**: For immediate testing, jump to Step 3 (Empirical Validation) using `scripts/test_rpc_rate_limits.py`.

## Rate Limiting Best Practices

When implementing the selected provider, use conservative targeting (80-90% of empirically validated rate) with monitoring and fallback strategy.

**Full guide**: See `references/rate-limiting-guide.md` for detailed monitoring requirements, fallback strategies, and safety margins.

## Common Pitfalls

**Critical mistakes to avoid**: Trusting documented burst limits (always validate empirically), testing with <50 blocks, parallel fetching on free tiers, ignoring compute unit costs, and forgetting archive access restrictions.

**Full guide**: See `references/common-pitfalls.md` for detailed anti-patterns with real-world examples (e.g., LlamaRPC 50 RPS → 1.37 RPS case).

## Scripts

- `calculate_timeline.py` - Calculate collection timeline from rate limits (RPS or compute units)
- `test_rpc_rate_limits.py` - Empirical rate limit testing template

**Usage guide**: See `scripts/README.md` for detailed usage examples, configuration options, and success criteria.

## References

### Workflow Documentation

- `references/workflow-steps.md` - Complete 5-step workflow with detailed guidance for each step
- `references/rate-limiting-guide.md` - Best practices for conservative rate targeting and monitoring
- `references/common-pitfalls.md` - Anti-patterns to avoid with real-world examples
- `references/example-workflow.md` - Complete case study: 13M Ethereum blocks RPC selection

### Data References

- `references/validated-providers.md` - Alchemy vs LlamaRPC vs Infura vs QuickNode empirical comparison
- `references/rpc-comparison-template.md` - Template for creating provider comparison matrices

### Scripts

- `scripts/README.md` - Complete usage guide for all scripts
- `scripts/calculate_timeline.py` - Timeline calculator (RPS and compute unit modes)
- `scripts/test_rpc_rate_limits.py` - Empirical rate limit testing template

## Example Workflow

**Case study**: Selecting RPC provider for 13M Ethereum blocks → Alchemy chosen at 5.79 RPS (26 days timeline, 4.2x faster than LlamaRPC).

**Full walkthrough**: See `references/example-workflow.md` for complete step-by-step case study showing research, calculation, validation, comparison, and final recommendation.

## When to Use This Skill

Invoke this skill when:

- Evaluating blockchain RPC providers for a new project
- Planning historical data backfill timelines
- Comparing free tier vs paid provider options
- Investigating rate limiting issues with current provider
- Estimating collection timelines for multi-million block datasets
- Validating archive node access for historical queries
- Researching compute unit or API credit costs
- Building POC before production implementation

## Related Patterns

This skill pairs well with:
- `blockchain-data-collection-validation` - For validating the complete data pipeline after provider selection
- Project scratch investigations in `scratch/ethereum-collector-poc/` and `scratch/rpc-provider-comparison/`
