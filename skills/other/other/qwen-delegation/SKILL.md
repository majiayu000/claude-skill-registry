---
name: qwen-delegation
description: Qwen CLI delegation workflow implementing delegation-core for Alibaba's
version: 1.9.0
alwaysApply: false
  Qwen models. Use when delegation-core selected Qwen, need Qwen's large context capabilities,
  batch processing required. Do not use when deciding which model to use (use delegation-core
  first), qwen CLI not installed.
category: delegation-implementation
tags:
- qwen
- cli
- delegation
- alibaba
- large-context
dependencies:
- delegation-core
tools:
- qwen-cli
- delegation-executor
usage_patterns:
- qwen-cli-integration
- large-context-analysis
- bulk-processing
complexity: intermediate
model_hint: standard
estimated_tokens: 600
progressive_loading: true
modules:
- modules/qwen-specifics.md
references:
- delegation-core/shared-shell-execution.md
---
## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Smart Delegation](#smart-delegation)
- [Qwen-Specific Details](#qwen-specific-details)


# Qwen CLI Delegation

## Overview

This skill implements `conjure:delegation-core` for the Qwen CLI.
It provides Qwen-specific authentication, quota management,
and command construction.

For shared delegation patterns, see `Skill(conjure:delegation-core)`.

## When To Use

- After `Skill(conjure:delegation-core)` determines Qwen is suitable
- When you need Qwen's large context window (100K+ tokens)
- For batch processing, summarization, or multi-file analysis
- If the `qwen` CLI is installed and configured

## Prerequisites

**Installation:**
```bash
# Install Qwen CLI
pip install qwen-cli

# Verify installation
qwen --version

# Check authentication
qwen auth status

# Login if needed
qwen auth login

# Or set API key
export QWEN_API_KEY="your-key"
```
**Verification:** Run `python --version` to verify Python environment.

## Quick Start

### Using Shared Delegation Executor
```bash
# Basic file analysis
python ~/conjure/tools/delegation_executor.py qwen "Analyze this code" --files src/main.py

# With specific model
python ~/conjure/tools/delegation_executor.py qwen "Summarize" --files src/**/*.py --model qwen-max

# With output format
python ~/conjure/tools/delegation_executor.py qwen "Extract functions" --files src/main.py --format json
```

### Direct CLI Usage
```bash
# Basic command
qwen -p "@path/to/file Analyze this code"

# Multiple files
qwen -p "@src/**/*.py Summarize these files"

# Specific model
qwen --model qwen-max -p "..."
```

### Save Output
```bash
qwen -p "..." > delegations/qwen/$(date +%Y%m%d_%H%M%S).md
```

## Smart Delegation

The shared delegation executor can auto-select the best service:
```bash
# Auto-select based on requirements
python ~/conjure/tools/delegation_executor.py auto "Analyze large codebase" \
  --files src/**/* --requirement large_context
```

## Qwen-Specific Details

For Qwen-specific models, CLI options, cost reference,
and troubleshooting, see `modules/qwen-specifics.md`.
