---
name: qwen-delegation
description: Qwen CLI delegation workflow implementing delegation-core for Alibaba's Qwen models.
triggers: qwen cli, qwen delegation, alibaba qwen, qwen batch, multi-file analysis, 100K context
use_when: delegation-core selected Qwen, need Qwen's large context capabilities, batch processing required
do_not_use_when: deciding which model to use (use delegation-core first), qwen CLI not installed
category: delegation-implementation
tags: [qwen, cli, delegation, alibaba, large-context]
dependencies: [delegation-core]
tools: [qwen-cli, delegation-executor]
usage_patterns:
  - qwen-cli-integration
  - large-context-analysis
  - bulk-processing
complexity: intermediate
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
- [Delegation Flow](#delegation-flow)
- [Quick Start](#quick-start)
- [Using Shared Delegation Executor](#using-shared-delegation-executor)
- [Direct CLI Usage](#direct-cli-usage)
- [Save Output](#save-output)
- [Smart Delegation](#smart-delegation)
- [Shared Patterns](#shared-patterns)
- [Qwen-Specific Details](#qwen-specific-details)
- [Exit Criteria](#exit-criteria)


# Qwen CLI Delegation

## Overview

This skill implements `conjure:delegation-core` for the Qwen CLI using shared delegation patterns. It provides Qwen-specific authentication, quota management, and command construction.

## When to Use
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

## Delegation Flow

Implements standard delegation-core flow with Qwen specifics:

1. `qwen-delegation:auth-verified` - Verify Qwen authentication
2. `qwen-delegation:quota-checked` - Check Qwen API quota
3. `qwen-delegation:command-executed` - Execute via Qwen CLI
4. `qwen-delegation:usage-logged` - Log Qwen API usage

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
**Verification:** Run `python --version` to verify Python environment.

### Direct CLI Usage
```bash
# Basic command
qwen -p "@path/to/file Analyze this code"

# Multiple files
qwen -p "@src/**/*.py Summarize these files"

# Specific model
qwen --model qwen-max -p "..."
```
**Verification:** Run the command with `--help` flag to verify availability.

### Save Output
```bash
qwen -p "..." > delegations/qwen/$(date +%Y%m%d_%H%M%S).md
```
**Verification:** Run the command with `--help` flag to verify availability.

## Smart Delegation

The shared delegation executor can auto-select the best service:
```bash
# Auto-select based on requirements
python ~/conjure/tools/delegation_executor.py auto "Analyze large codebase" \
  --files src/**/* --requirement large_context
```
**Verification:** Run `python --version` to verify Python environment.

## Shared Patterns

This skill uses shared infrastructure from delegation-core:
- **Shell Execution**: See `delegation-core/shared-shell-execution.md`
- **Authentication**: Standard CLI authentication patterns
- **Quota Management**: Unified quota tracking
- **Usage Logging**: Centralized usage analytics

## Qwen-Specific Details

For Qwen-specific models, CLI options, cost reference, and troubleshooting, see `modules/qwen-specifics.md`.

## Exit Criteria
- Authentication confirmed working
- Quota checked and sufficient
- Command executed successfully using shared infrastructure
- Usage logged for tracking with unified analytics
