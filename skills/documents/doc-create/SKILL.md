---
name: doc-create
description: Create new documentation from templates
user-invocable: true
allowed-tools: Skill, Read, Write, Glob
---

# Documentation Create Skill

Create new AsciiDoc documents from predefined templates.

## Parameters

- **type** (required): standard|readme|guide
- **name** (required): Document name
- **path** (optional): Output path (default: inferred from type)

## Workflow

### Step 1: Validate Parameters

```
If type not provided OR type not in [standard, readme, guide]:
  Show usage and exit

If name not provided:
  Show usage and exit
```

**Usage:**
```
/doc-create type=<type> name=<name> [path=<path>]

Parameters:
  type - Required: standard|readme|guide
  name - Required: Document name (used in title and filename)
  path - Optional: Output path (default: inferred from type)

Default paths by type:
  standard → standards/{name}.adoc
  readme   → README.adoc (or {name}/README.adoc if name != project)
  guide    → docs/{name}.adoc

Examples:
  /doc-create type=standard name=java-logging
  /doc-create type=readme name=MyProject
  /doc-create type=guide name=setup-guide
  /doc-create type=standard name=testing path=docs/standards/
```

### Step 2: Determine Output Path

```
If path specified:
  output_path = {path}/{name}.adoc

Else:
  If type = standard:
    output_path = standards/{name}.adoc
  If type = readme:
    output_path = README.adoc (or {name}/README.adoc)
  If type = guide:
    output_path = docs/{name}.adoc
```

### Step 3: Check for Existing File

```
If file exists at output_path:
  Ask user: "File exists. Overwrite? (y/n)"
  If no: Exit
```

### Step 4: Load Documentation Skill

```
Skill: pm-documents:ref-documentation
```

### Step 5: Execute Creation Workflow

```
Execute workflow: create-from-template
Parameters:
  type: {type}
  name: {name}
  path: {output_path}
```

### Step 6: Generate Report

```
═══════════════════════════════════════════════
Document Created
═══════════════════════════════════════════════

File: {output_path}
Type: {type}
Status: Created and validated

Next steps:
1. Open {output_path} in your editor
2. Fill in the template sections
3. Run /doc-doctor target={output_path} to validate
```

## Architecture

**Pattern**: Thin Orchestrator (~80 lines)
- Validates parameters
- Delegates creation to ref-documentation skill
- No business logic in skill

**Skill Dependency**: pm-documents:ref-documentation
- Provides: create-from-template workflow
- Templates: templates/standard-template.adoc, readme-template.adoc, guide-template.adoc

## Related

- `/doc-doctor` - Diagnose documentation issues
- `/doc-maintain` - Maintain existing documentation
- `ref-documentation` skill - Provides creation workflow and templates
