---
name: rivet-scan
description: Initialize Rivet by scanning codebase structure. Use when SessionStart hook reports no .rivet/systems.yaml, when user says "install rivet" or "set up rivet", or to refresh system definitions after major codebase changes.
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Write, AskUserQuestion
---

# Rivet Scan - Codebase Auto-Discovery

Analyze the codebase structure and propose systems for .rivet/systems.yaml.

## Purpose

This skill runs during plugin installation to bootstrap .rivet/systems.yaml. It gathers structural data from the codebase and uses that to propose systems that form the project's architecture.

## What Makes a Good System

A system is a cohesive bundle of code that forms a single mental model:

- Has clear boundaries (you can point to where it starts and ends)
- Forms a coherent abstraction (the pieces "fit together" conceptually)
- Substantial size (~5% of codebase, or significant enough to cause confusion)
- Has a name worth tracking (you'd mention it when explaining architecture)

A system is something you'd draw as a box in an architecture diagram. NOT individual functions, utility helpers, or single implementation files.

## Scan Process

### Step 1: Gather Package Boundaries

Look for package manifest files that indicate module boundaries:

```bash
# Find all package manifests
fd -t f -e json -e toml -e mod -e yaml '(package|Cargo|go|pyproject|pom)' .
```

Check for:
- `package.json` (Node.js)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- `pyproject.toml` / `setup.py` (Python)
- `pom.xml` / `build.gradle` (Java)

### Step 2: Analyze Directory Structure

```bash
# Get top-level directories with clear purpose
ls -la
# Look for common patterns: src/, lib/, pkg/, cmd/, internal/, etc.
```

Identify directories that represent distinct systems:
- `src/commands/` - Command implementations
- `src/services/` - Service layer
- `src/api/` - API endpoints
- `lib/` - Shared libraries
- `pkg/` - Public packages

### Step 3: Find Major Entry Points

```bash
# Find main entry points
fd -t f '(main|index|app|server)\.(ts|js|py|go|rs)$'

# Find exports/public interfaces
grep -r "export" --include="*.ts" --include="*.js" | head -50
```

### Step 4: Map Import Relationships (Optional)

For dependency hints between systems:

```bash
# TypeScript/JavaScript imports
grep -rh "^import.*from" --include="*.ts" --include="*.js" | sort | uniq -c | sort -rn

# Python imports
grep -rh "^from.*import\|^import" --include="*.py" | sort | uniq -c | sort -rn
```

### Step 5: Check for Existing .rivet/systems.yaml

```bash
ls .rivet/systems.yaml 2>/dev/null
```

If .rivet/systems.yaml exists, prompt the user:
- "We detected these systems in your codebase: [list]. Your .rivet/systems.yaml has: [list]. What would you like to do?"
- Options: Update existing / Start fresh / Skip scan

### Step 6: Propose Systems

Based on gathered data, create .rivet/systems.yaml with:

```yaml
project:
  name: <from package.json or directory name>
  purpose: <inferred or left blank>

systems:
  <SystemName>:
    description: <what this system does>
    paths:
      - <directory paths>
```

## Output Format

Create the .rivet/ folder and write systems.yaml with proposed systems. Each system should have:

- A clear, concise name (PascalCase)
- A one-line description of what it does
- Associated paths in the codebase
- Optional: depends_on hints from import analysis

## Example Output

```yaml
project:
  name: my-app
  purpose: ""

systems:
  API:
    description: HTTP endpoints and request handlers
    paths:
      - src/api/
      - src/routes/

  Database:
    description: Data persistence and query layer
    paths:
      - src/db/
      - src/models/

  CLI:
    description: Command-line interface and argument parsing
    paths:
      - bin/
      - src/commands/
```
