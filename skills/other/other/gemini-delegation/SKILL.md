---
name: gemini-delegation
description: Gemini CLI delegation workflow implementing delegation-core for Google's
version: 1.7.1
alwaysApply: false
  Gemini models. Use when delegation-core selected Gemini, need Gemini's 1M+ token
  context window, batch processing required. Do not use when deciding which model
  to use (use delegation-core first), gemini CLI not installed.
category: delegation-implementation
tags:
- gemini
- cli
- delegation
- google
- large-context
dependencies:
- delegation-core
tools:
- gemini-cli
usage_patterns:
- gemini-cli-integration
- large-context-analysis
- batch-processing
complexity: intermediate
model_hint: standard
estimated_tokens: 600
progressive_loading: true
modules:
- modules/gemini-specifics.md
references:
- delegation-core/../../leyline/skills/authentication-patterns/SKILL.md
- delegation-core/../../leyline/skills/quota-management/SKILL.md
- delegation-core/../../leyline/skills/usage-logging/SKILL.md
- delegation-core/../../leyline/skills/error-patterns/SKILL.md
---
## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Gemini-Specific Details](#gemini-specific-details)


# Gemini CLI Delegation

## Overview

This skill implements `conjure:delegation-core` for the Gemini CLI.
It provides Gemini-specific authentication, quota management,
and command construction.

For shared delegation patterns, see `Skill(conjure:delegation-core)`.

## When To Use

- After `Skill(conjure:delegation-core)` determines Gemini is suitable
- When you need Gemini's large context window (1M+ tokens)
- For batch processing, summarization, or pattern extraction tasks
- If the `gemini` CLI is installed and authenticated

## Prerequisites

**Installation:**
```bash
# Verify installation
gemini --version

# Check authentication
gemini auth status

# Login if needed
gemini auth login

# Or set API key
export GEMINI_API_KEY="your-key"
```
**Verification:** Run the command with `--help` flag to verify availability.

## Quick Start

### Basic Command
```bash
# File analysis
gemini -p "@path/to/file Analyze this code"

# Multiple files
gemini -p "@src/**/*.py Summarize these files"

# With specific model
gemini --model gemini-2.5-pro-exp -p "..."

# JSON output
gemini --output-format json -p "..."
```

### Save Output
```bash
gemini -p "..." > delegations/gemini/$(date +%Y%m%d_%H%M%S).md
```

## Gemini-Specific Details

For Gemini-specific models, CLI options, cost reference,
and troubleshooting, see `modules/gemini-specifics.md`.
