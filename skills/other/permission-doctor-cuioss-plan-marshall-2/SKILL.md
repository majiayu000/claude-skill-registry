---
name: permission-doctor
description: Diagnose permission issues across settings files (read-only analysis)
user-invocable: true
allowed-tools: Read, Grep, Bash
---

# Permission Doctor Skill

Read-only permission analysis for Claude Code settings. Detects redundant permissions, security anti-patterns, and validates permission syntax without making changes.

## What This Skill Provides

### Permission Validation Standards
- Syntax validation patterns for all permission types
- Path format validation rules
- Duplicate detection algorithms
- Permission categorization logic

### Architecture Patterns
- Global vs Local permission separation
- Universal git access patterns
- Project-specific permission patterns
- Skill and tool permission organization

### Security Anti-Patterns
- Suspicious permission detection patterns
- Critical system directory checks
- Dangerous command patterns
- Overly broad wildcard detection

## When to Activate This Skill

Activate when:
- Validating permission syntax
- Detecting security anti-patterns
- Understanding global/local architecture
- Analyzing permission issues without making changes

## Operations

### Operation: detect-redundant

Detect permissions in local settings that duplicate global settings.

**Script**: `permission-doctor.py detect-redundant`

**Input**:
```bash
python3 .plan/execute-script.py plan-marshall:permission-doctor:permission-doctor detect-redundant \
  --global-settings {global_path} \
  --local-settings {local_path}
```

**Output JSON**:
```json
{
  "redundant": [
    {"permission": "Bash(git:*)", "reason": "Exact duplicate", "type": "exact_duplicate"}
  ],
  "marketplace_in_local": [
    {"permission": "Skill(pm-dev-builder:*)", "reason": "Should be in global", "type": "marketplace_permission"}
  ],
  "summary": {
    "redundant_count": 1,
    "marketplace_in_local_count": 1
  }
}
```

**Usage**: Call before fixing to identify redundancies between global and local settings.

---

### Operation: detect-suspicious

Detect permissions matching anti-patterns (security risks).

**Script**: `permission-doctor.py detect-suspicious`

**Input**:
```bash
python3 .plan/execute-script.py plan-marshall:permission-doctor:permission-doctor detect-suspicious \
  --settings {settings_path} \
  [--approved-file {run_config_path}]
```

**Output JSON**:
```json
{
  "suspicious": [
    {"permission": "Write(/tmp/**)", "reason": "System temp access", "severity": "medium"}
  ],
  "already_approved": ["Bash(sudo:*)"],
  "summary": {
    "total_suspicious": 1,
    "by_severity": {"high": 0, "medium": 1, "low": 0}
  }
}
```

**Usage**: Call to identify security anti-patterns. User-approved permissions are excluded.

---

### Operation: analyze-settings

High-level analysis of settings files for permission issues.

**Workflow**: Runs detect-redundant and detect-suspicious operations and consolidates results.

**Input**:
```
global_settings: ~/.claude/settings.json
local_settings: .claude/settings.json
```

**Output JSON**:
```json
{
  "redundant_issues": {...},
  "suspicious_issues": {...},
  "total_issues": 5,
  "recommendations": [
    "Remove 3 redundant permissions from local settings",
    "Review 2 suspicious permissions in global settings"
  ]
}
```

**Usage**: Entry point for permission analysis. Consolidates multiple detection results.

## Scripts

| Script | Subcommand | Purpose |
|--------|------------|---------|
| `permission-doctor.py` | `detect-redundant` | Detects redundant permissions between global/local |
| `permission-doctor.py` | `detect-suspicious` | Detects security anti-patterns in permissions |

## Standards Organization

- `standards/permission-validation-standards.md` - Validation patterns, syntax rules, categorization
- `standards/permission-architecture.md` - Global/Local separation, universal access patterns
- `standards/permission-anti-patterns.md` - Security patterns, suspicious permission detection

## Non-Prompting Requirements

This skill is designed to run without user prompts. Required permissions:

**Script Execution:**
- `Bash(python3 .plan/execute-script.py *)` - Script execution via executor

**File Operations:**
- `Read(~/.claude/settings.json)` - Read global settings
- `Read(.claude/settings.json)` - Read project settings

**Ensuring Non-Prompting:**
- All operations are read-only analysis
- No file modifications performed
- Script invocation uses executor pattern

## Critical Rules

**Read-Only:**
- This skill NEVER modifies files
- All operations are analysis and reporting only
- Use `permission-fix` skill for write operations

**Anti-Pattern Detection:**
- Uses 24 suspicious patterns from standards
- Severity scoring: high, medium, low
- User-approved permissions are excluded from reports

Part of: plan-marshall-core bundle
