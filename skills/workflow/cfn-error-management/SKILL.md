---
name: cfn-error-management
description: "Unified error handling, batching, and logging for CFN Loop. Use when you need to capture agent errors, batch multiple errors for processing, log structured error data, or categorize and recover from agent failures."
version: 1.0.0
tags: [mega-skill, errors, logging, batch-processing]
status: production
---

# Error Management Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Unified error handling, batching, and logging
**Status:** Production
**Consolidates:** cfn-standardized-error-handling, cfn-error-batching-strategy, cfn-error-logging

---

## Overview

This mega-skill provides complete error management:
- **Capture** - Standardized error capture and categorization
- **Batching** - Error grouping for batch agent processing
- **Logging** - Error log storage and retrieval

---

## Directory Structure

```
error-management/
├── SKILL.md                          # This file
├── lib/
│   ├── capture/                      # Error capture (from cfn-standardized-error-handling)
│   │   ├── capture-agent-error.sh    # Capture agent errors
│   │   └── README.md                 # Capture documentation
│   ├── batching/                     # Error batching (from cfn-error-batching-strategy)
│   │   ├── cli.sh                    # Batching CLI
│   │   ├── analyze-errors.sh         # Error analysis
│   │   ├── calculate-waves.sh        # Wave calculation
│   │   ├── cluster-files.sh          # File clustering
│   │   ├── create-batches.sh         # Batch creation
│   │   ├── templates/                # Batch templates
│   │   └── README.md                 # Batching documentation
│   └── logging/                      # Error logging (from cfn-error-logging)
│       ├── invoke-error-logging.sh   # Log errors
│       ├── cleanup-error-logs.sh     # Log cleanup
│       ├── src/                      # TypeScript implementation
│       └── README.md                 # Logging documentation
└── cli/                              # CLI wrappers
    ├── capture-error.sh              # → lib/capture/capture-agent-error.sh
    ├── batch-errors.sh               # → lib/batching/cli.sh
    └── log-error.sh                  # → lib/logging/invoke-error-logging.sh
```

---

## Quick Start

### 1. Capture an Error

```bash
./cli/capture-error.sh \
  --agent-id "agent-123" \
  --error-type "TIMEOUT" \
  --message "Agent timed out after 900s" \
  --context "Loop 3 implementation"
```

### 2. Batch Errors for Processing

```bash
./cli/batch-errors.sh \
  --input errors.json \
  --max-batch-size 5 \
  --output batches.json
```

### 3. Log an Error

```bash
./cli/log-error.sh \
  --task-id "task-123" \
  --agent-id "agent-123" \
  --error-type "VALIDATION" \
  --message "Output validation failed"
```

---

## Module Details

### Capture Module (lib/capture/)

**Purpose:** Standardized error capture and categorization

**Error Types:**
- TIMEOUT - Agent execution timeout
- CRASH - Agent process crash
- VALIDATION - Output validation failure
- COORDINATION - Redis coordination failure
- UNKNOWN - Uncategorized errors

**Features:**
- Standardized error format
- Category-based recovery strategies
- Context preservation

### Batching Module (lib/batching/)

**Purpose:** Group errors for batch agent processing

**Features:**
- Error clustering by file
- Wave calculation for parallel processing
- Tier-based batching (small/medium/large)
- Template-based batch configuration

### Logging Module (lib/logging/)

**Purpose:** Error log storage and management

**Features:**
- Structured error logging
- Log cleanup and rotation
- Integration with CLI and Docker modes
- TypeScript implementation

---

## Integration with CFN Loop

```bash
# 1. Capture error when agent fails
./cli/capture-error.sh \
  --agent-id "$AGENT_ID" \
  --error-type "TIMEOUT" \
  --message "$ERROR_MESSAGE"

# 2. Log the error
./cli/log-error.sh \
  --task-id "$TASK_ID" \
  --agent-id "$AGENT_ID" \
  --error-type "TIMEOUT"

# 3. Batch multiple errors for batch processing
./cli/batch-errors.sh --input collected-errors.json
```

---

## Migration from Individual Skills

### Old Paths → New Paths

| Old Path | New Path |
|----------|----------|
| `.claude/skills/cfn-standardized-error-handling/capture-agent-error.sh` | `.claude/skills/error-management/lib/capture/capture-agent-error.sh` |
| `.claude/skills/cfn-error-batching-strategy/cli.sh` | `.claude/skills/error-management/lib/batching/cli.sh` |
| `.claude/skills/cfn-error-logging/invoke-error-logging.sh` | `.claude/skills/error-management/lib/logging/invoke-error-logging.sh` |

---

## Version History

### 1.0.0 (2025-12-02) - Mega-Skill Creation
- Merged: cfn-standardized-error-handling, cfn-error-batching-strategy, cfn-error-logging
- Added: CLI wrappers
- Added: Unified documentation

---

## Dependencies

- **Bash:** 4.0+
- **jq:** JSON processing
- **Node.js:** TypeScript logging (optional)
