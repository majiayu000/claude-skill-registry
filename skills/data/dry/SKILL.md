---
name: dry
description: Detect duplicate code and suggest DRY refactors using jscpd
allowed-tools: [Bash, Read, Write, Glob, Grep]
---

# DRY Check

Detect duplicate code across your codebase using jscpd.

## Subcommands

| Command | Description |
|---------|-------------|
| `dry` or `dry scan` | Run duplication scan |
| `dry report` | Show last scan results |
| `dry config` | Show current jscpd configuration |
| `dry init` | Create project-specific jscpd.json |

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--threshold N` | Minimum token count for duplicate detection (higher = fewer matches) | jscpd default |
| `--path <dir>` | Directory to scan for duplicates | Current directory |

## Examples

```bash
# Scan with higher threshold (find only large duplicates)
/bluera-base:dry scan --threshold 100

# Scan specific directory
/bluera-base:dry scan --path src/

# Combine both
/bluera-base:dry scan --threshold 75 --path lib/
```

## Workflow

**Phases:** Check jscpd → Scan codebase → Report duplicates → Suggest refactors

### 1. Check jscpd Installation

```bash
command -v jscpd || npx jscpd --version
```

If not installed, suggest: `npm install -g jscpd`

### 2. Run Scan

```bash
jscpd --reporters json --output .bluera/bluera-base/state/ .
```

### 3. Parse Results

Results are stored in `.bluera/bluera-base/state/jscpd-report.json`

### 4. Refactoring Guidance

See skills/dry-refactor/SKILL.md for language-specific refactoring patterns.
