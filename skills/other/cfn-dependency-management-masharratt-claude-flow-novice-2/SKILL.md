---
name: cfn-dependency-management
description: "Task dependency extraction and context ingestion. Use when you need to parse task criteria, identify dependencies, generate execution order, or inject context for complex multi-step tasks."
version: 1.1.0
tags: [mega-skill, dependencies, extraction, ingestion, orchestration]
status: production
---

# Dependency Management Skill (Mega-Skill)

**Version:** 1.1.0
**Purpose:** Task dependency extraction and context ingestion
**Status:** Production
**Consolidates:** cfn-dependency-extractor, cfn-dependency-ingestion
**Confidence:** 9.5/10 (with orchestration layer)

---

## Overview

This mega-skill provides complete dependency handling:
- **Extractor** - Parse task criteria, identify dependencies, generate execution order
- **Ingestion** - Consume manifests, inject context, coordinate dependencies
- **Orchestration** - Unified interface coordinating extraction and ingestion

---

## Directory Structure

```
dependency-management/
├── SKILL.md
├── execute.sh                    # Main orchestration script
├── cfn-dependency-management.sh  # Skill wrapper entry point
└── lib/
    ├── extractor/                # From cfn-dependency-extractor
    └── ingestion/                # From cfn-dependency-ingestion
```

---

## Usage

### Main Entry Point

```bash
# Basic usage
./cfn-dependency-management.sh --task-description "Implement OAuth2 auth"

# Save to file
./cfn-dependency-management.sh --task-description "Build admin dashboard" --output-file deps.txt

# Mode-specific execution
./cfn-dependency-management.sh --task-description "Add user profiles" --mode mvp
./cfn-dependency-management.sh --task-description "Full system audit" --mode enterprise --verbose
```

### Modes

- **MVP**: Only P0 critical dependencies (fastest)
- **Standard**: P0 and P1 dependencies (balanced)
- **Enterprise**: All dependencies including deprecated (comprehensive)

---

## Pipeline Flow

1. **Extraction** - Analyze task description → produce dependency graph
2. **Mode Configuration** - Apply mode-specific filters (P0, P1, P2)
3. **Ingestion** - Consume dependency graph → inject context for execution
4. **Summary** - Generate execution report with critical path and parallel opportunities

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-dependency-extractor/ | dependency-management/lib/extractor/ |
| cfn-dependency-ingestion/ | dependency-management/lib/ingestion/ |

---

## Version History

### 1.1.0 (2025-12-08)
- Added execute.sh orchestration script
- Added cfn-dependency-management.sh wrapper entry point
- Implemented mode-based execution (mvp/standard/enterprise)
- Added comprehensive help and error handling
- Fixed coordination between extraction and ingestion

### 1.0.0 (2025-12-02)
- Consolidated extractor + ingestion into unified dependency pipeline

---

## Pipeline Flow

1. Extractor analyzes task → produces dependency graph
2. Ingestion consumes graph → injects context for execution

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-dependency-extractor/ | dependency-management/lib/extractor/ |
| cfn-dependency-ingestion/ | dependency-management/lib/ingestion/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated extractor + ingestion into unified dependency pipeline

