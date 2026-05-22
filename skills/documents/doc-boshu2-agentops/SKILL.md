---
name: doc
description: 'This skill should be used when the user asks to "generate documentation", "validate docs", "check doc coverage", "find missing docs", "create code-map", "sync documentation", "update docs", or needs guidance on documentation generation and validation for any repository type. Triggers: doc, documentation, code-map, doc coverage, validate docs.'
---

# Doc Skill

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Generate and validate documentation for any project.

## Execution Steps

Given `/doc [command] [target]`:

### Step 1: Detect Project Type

```bash
# Check for indicators
ls package.json pyproject.toml go.mod Cargo.toml 2>/dev/null

# Check for existing docs
ls -d docs/ doc/ documentation/ 2>/dev/null
```

Classify as:
- **CODING**: Has source code, needs API docs
- **INFORMATIONAL**: Primarily documentation (wiki, knowledge base)
- **OPS**: Infrastructure, deployment, runbooks

### Step 2: Execute Command

**discover** - Find undocumented features:
```bash
# Find public functions without docstrings (Python)
grep -r "^def " --include="*.py" | grep -v '"""' | head -20

# Find exported functions without comments (Go)
grep -r "^func [A-Z]" --include="*.go" | head -20
```

**coverage** - Check documentation coverage:
```bash
# Count documented vs undocumented
TOTAL=$(grep -r "^def \|^func \|^class " --include="*.py" --include="*.go" | wc -l)
DOCUMENTED=$(grep -r '"""' --include="*.py" | wc -l)
echo "Coverage: $DOCUMENTED / $TOTAL"
```

**gen [feature]** - Generate documentation:
1. Read the code for the feature
2. Understand what it does
3. Generate appropriate documentation
4. Write to docs/ directory

**all** - Update all documentation:
1. Run discover to find gaps
2. Generate docs for each undocumented feature
3. Validate existing docs are current

### Step 3: Generate Documentation

When generating docs, include:

**For Functions/Methods:**
```markdown
## function_name

**Purpose:** What it does

**Parameters:**
- `param1` (type): Description
- `param2` (type): Description

**Returns:** What it returns

**Example:**
```python
result = function_name(arg1, arg2)
```

**Notes:** Any important caveats
```

**For Classes:**
```markdown
## ClassName

**Purpose:** What this class represents

**Attributes:**
- `attr1`: Description
- `attr2`: Description

**Methods:**
- `method1()`: What it does
- `method2()`: What it does

**Usage:**
```python
obj = ClassName()
obj.method1()
```
```

### Step 4: Create Code-Map (if requested)

**Write to:** `docs/code-map/`

```markdown
# Code Map: <Project>

## Overview
<High-level architecture>

## Directory Structure
```
src/
├── module1/     # Purpose
├── module2/     # Purpose
└── utils/       # Shared utilities
```

## Key Components

### Module 1
- **Purpose:** What it does
- **Entry point:** `main.py`
- **Key files:** `handler.py`, `models.py`

### Module 2
...

## Data Flow
<How data moves through the system>

## Dependencies
<External dependencies and why>
```

### Step 5: Validate Documentation

Check for:
- Out-of-date docs (code changed, docs didn't)
- Missing sections (no examples, no parameters)
- Broken links
- Inconsistent formatting

### Step 6: Write Report

**Write to:** `.agents/doc/YYYY-MM-DD-<target>.md`

```markdown
# Documentation Report: <Target>

**Date:** YYYY-MM-DD
**Project Type:** <CODING/INFORMATIONAL/OPS>

## Coverage
- Total documentable items: <count>
- Documented: <count>
- Coverage: <percentage>%

## Generated
- <list of docs generated>

## Gaps Found
- <undocumented item 1>
- <undocumented item 2>

## Validation Issues
- <issue 1>
- <issue 2>

## Next Steps
- [ ] Document remaining gaps
- [ ] Fix validation issues
```

### Step 7: Report to User

Tell the user:
1. Documentation coverage percentage
2. Docs generated/updated
3. Gaps remaining
4. Location of report

## Key Rules

- **Detect project type first** - approach varies
- **Generate meaningful docs** - not just stubs
- **Include examples** - always show usage
- **Validate existing** - docs can go stale
- **Write the report** - track coverage over time

## Commands Summary

| Command | Action |
|---------|--------|
| `discover` | Find undocumented features |
| `coverage` | Check documentation coverage |
| `gen [feature]` | Generate docs for specific feature |
| `all` | Update all documentation |
| `validate` | Check docs match code |
