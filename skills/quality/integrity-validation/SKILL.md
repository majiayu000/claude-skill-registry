---
name: integrity-validation
description: Pre/post-operation validation to detect missing components and prevent future issues
version: 1.0.0
---

# Integrity Validation System

## Overview

The Integrity Validation System prevents future component loss by:
- Pre-operation inventory taking
- Post-operation verification
- Automatic detection of missing components
- Immediate alerts for discrepancies

## Core Components

### 1. Pre-Operation Validation
```python
# Before any major operation (restructuring, refactoring, migration)
pre_operation_inventory = {
    "agents": list_all_agents(),
    "commands": list_all_commands(),
    "skills": list_all_skills(),
    "patterns": list_all_patterns(),
    "critical_files": identify_critical_files()
}

# Store snapshot
store_validation_snapshot("pre_operation", pre_operation_inventory)
```

### 2. Post-Operation Validation
```python
# After operation completes
post_operation_inventory = {
    "agents": list_all_agents(),
    "commands": list_all_commands(),
    "skills": list_all_skills(),
    "patterns": list_all_patterns(),
    "critical_files": identify_critical_files()
}

# Compare and report discrepancies
differences = compare_inventories(pre_operation_inventory, post_operation_inventory)
if differences.missing_components:
    alert_missing_components(differences)
    suggest_recovery_options(differences)
```

### 3. Critical Components Registry

**Critical Components (must exist)**:
- All commands in categories (dev/, analyze/, validate/, debug/, learn/, workspace/, monitor/)
- Core agents (orchestrator, code-analyzer, quality-controller, test-engineer)
- Essential skills (pattern-learning, code-analysis, quality-standards)
- Plugin manifest (.claude-plugin/plugin.json)

**Warning Components (should exist)**:
- Documentation files (README.md, STRUCTURE.md)
- Configuration files
- Helper scripts (lib/ directory)

**Optional Components (nice to have)**:
- Example files
- Test files
- Development tools

## Validation Rules

### Pre-Operation Rules
1. **Mandatory Inventory**: Must capture all components before any major operation
2. **Critical Identification**: Mark components that cannot be lost
3. **Baseline Creation**: Establish known-good state
4. **Backup Trigger**: Auto-trigger backup for critical components

### Post-Operation Rules
1. **Immediate Validation**: Run within 5 seconds of operation completion
2. **Difference Detection**: Identify missing, added, or modified components
3. **Severity Assessment**: Classify issues (critical, warning, info)
4. **Auto-Recovery**: Offer automatic restoration for critical components

### Alert Classification
- **CRITICAL**: Core agents or commands missing (immediate action required)
- **HIGH**: Essential skills or patterns missing (action recommended)
- **MEDIUM**: Documentation or configuration missing (investigate)
- **LOW**: Optional components missing (note for next release)

## Integration Points

### Major Operations That Require Validation
- `/workspace:improve` - Plugin modifications
- `/dev:release` - Release preparation
- Command restructuring or categorization
- Agent or skill modifications
- File system reorganization

### Automatic Triggers
- File operations in commands/ directory
- Modifications to agents/ directory
- Changes to skills/ directory
- Plugin manifest updates

## Implementation Architecture

### Validation Flow
```python
async def validate_operation_integrity(operation_type):
    # 1. Pre-operation snapshot
    pre_snapshot = await create_inventory_snapshot()

    # 2. Execute operation
    await execute_operation(operation_type)

    # 3. Post-operation validation
    post_snapshot = await create_inventory_snapshot()

    # 4. Compare and analyze
    issues = compare_snapshots(pre_snapshot, post_snapshot)

    # 5. Handle issues
    if issues.critical:
        await handle_critical_issues(issues)
    elif issues.warnings:
        await suggest_improvements(issues)

    return issues
```

### Storage Format
```json
{
  "validation_snapshot": {
    "operation": "command_restructure",
    "timestamp": "2025-01-27T10:30:00Z",
    "pre_inventory": {
      "commands": {
        "count": 23,
        "files": ["commands/dev/auto.md", "commands/analyze/project.md", ...]
      },
      "agents": {
        "count": 19,
        "files": ["agents/orchestrator.md", "agents/code-analyzer.md", ...]
      }
    },
    "post_inventory": {
      "commands": {
        "count": 22,
        "files": ["commands/dev/auto.md", "commands/analyze/project.md", ...]
      },
      "agents": {
        "count": 19,
        "files": ["agents/orchestrator.md", "agents/code-analyzer.md", ...]
      }
    }
  }
}
```

## Success Metrics
- **Detection Rate**: 100% of missing components detected within 10 seconds
- **False Positive Rate**: <5% (accurate issue identification)
- **Recovery Success**: 95% of critical issues automatically resolvable
- **Performance Impact**: <2 seconds overhead for validation

## When to Apply

**Always Apply**:
- Before any file system restructuring
- After any command categorization changes
- During release preparation
- After any major refactoring

**Recommended**:
- After adding new agents or skills
- After modifying plugin manifest
- After any automated file operations
- Weekly integrity checks

## Failure Prevention

This system specifically prevents:
1. **Lost Commands**: Detects when commands are moved or deleted
2. **Missing Agents**: Identifies when agent files are removed
3. **Broken References**: Finds when cross-references are broken
4. **Configuration Drift**: Detects when configuration becomes inconsistent
5. **Documentation Gaps**: Identifies when documentation falls out of sync

## Recovery Process

1. **Immediate Detection**: Missing component identified within 5 seconds
2. **Alert Generation**: Clear, actionable alert with severity level
3. **Backup Search**: Search backups for missing component
4. **Auto-Restoration**: If found in recent backup, auto-restore
5. **Git Recovery**: If not in backup, check Git history
6. **Template Recreation**: If not found, create from template
7. **Manual Guidance**: Provide clear instructions for manual recovery