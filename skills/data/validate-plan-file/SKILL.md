---
name: validate-plan-file
description: Validate that orchestrator plan files conform to expected JSON schema. Use before workers read plan files or after orchestrators create them to ensure proper structure and required fields.
allowed-tools: Read
---

# Validate Plan File

Validate orchestrator plan files to ensure they conform to the expected schema before workers process them.

## When to Use

- Before workers read plan files
- After orchestrators create plan files
- When debugging plan file issues
- In quality gates validation

## Instructions

### Step 1: Read Plan File

Use Read tool to load the plan file.

**Expected Input**:

- `file_path`: Path to plan file (e.g., `.bug-detection-plan.json`, `.security-scan-plan.json`)

**Tools Used**: Read

### Step 2: Determine Schema

Map file name pattern to appropriate JSON schema.

**Schema Mapping**:

- `.bug-*-plan.json` → `.claude/schemas/bug-plan.schema.json`
- `.security-*-plan.json` → `.claude/schemas/security-plan.schema.json`
- `.dead-code-*-plan.json` → `.claude/schemas/dead-code-plan.schema.json`
- `.dependency-*-plan.json` → `.claude/schemas/dependency-plan.schema.json`
- `.version-*-plan.json` → base schema (version update workflow)

**New Naming Convention** (standardized):

- Bug workflow: `.bug-detection-plan.json`, `.bug-fixing-plan.json`, `.bug-verification-plan.json`
- Security workflow: `.security-scan-plan.json`, `.security-remediation-plan.json`, `.security-verification-plan.json`
- Dead code workflow: `.dead-code-detection-plan.json`, `.dead-code-cleanup-plan.json`, `.dead-code-verification-plan.json`
- Dependency workflow: `.dependency-audit-plan.json`, `.dependency-update-plan.json`, `.dependency-verification-plan.json`

### Step 3: Load and Parse JSON Schema

Use Read tool to load the appropriate schema file from `.claude/schemas/`.

**Tools Used**: Read

### Step 4: Validate JSON Against Schema

Validate the plan file content against the loaded JSON schema.

**Base Schema Validation** (all plan files):

- `workflow`: String (required, e.g., "bug-management", "security-audit")
- `phase`: String (required, e.g., "detection", "fixing", "verification")
- `phaseNumber`: Integer (optional, for sequencing)
- `config`: Object (required, domain-specific configuration)
- `validation`: Object (required, with `required` array of validation criteria)
- `nextAgent`: String (optional, agent to invoke next)
- `timestamp`: String (optional, ISO-8601 format)
- `metadata`: Object (optional, with `createdBy`, `iteration`, `maxIterations`)

**Domain-Specific Validation**:

**Bug Plans**:

- `config.priority`: "critical"|"high"|"medium"|"low"|"all" (required)
- `config.categories`: Array of bug types (optional)
- `config.maxBugsPerRun`: Integer (optional, default 50)
- `config.verifyOnly`: Boolean (optional, default false)

**Security Plans**:

- `config.severity`: "critical"|"high"|"medium"|"low"|"all" (required)
- `config.categories`: Array of vulnerability types (optional)
- `config.maxVulnsPerRun`: Integer (optional, default 25)
- `config.skipSupabaseRLS`: Boolean (optional, default false)

**Dead Code Plans**:

- `config.type`: "critical"|"high"|"medium"|"low"|"all" (required)
- `config.categories`: Array of dead code types (optional)
- `config.maxItemsPerRun`: Integer (optional, default 100)
- `config.safeMode`: Boolean (optional, default true)

**Dependency Plans**:

- `config.category`: "security"|"unused"|"outdated"|"all" (required)
- `config.severity`: "critical"|"high"|"medium"|"low"|"all" (optional)
- `config.maxUpdatesPerRun`: Integer (optional, default 10)
- `config.updateStrategy`: "one-at-a-time"|"batch-compatible"|"all" (optional)

### Step 5: Return Validation Result

Return detailed validation result with errors/warnings.

**Expected Output**:

```json
{
  "valid": true,
  "file": ".bug-detection-plan.json",
  "errors": [],
  "warnings": [],
  "schema": "bug-plan",
  "schemaPath": ".claude/schemas/bug-plan.schema.json"
}
```

## Error Handling

- **File Not Found**: Return error with file path
- **Invalid JSON**: Return parsing error with line number if possible
- **Schema File Not Found**: Return error if schema file missing
- **Missing Required Fields**: List all missing fields from JSON schema validation
- **Invalid Field Types**: Describe type mismatches (e.g., expected string, got number)
- **Invalid Enum Values**: Report when value not in allowed enum list
- **Schema Mismatch**: Warn if file doesn't match expected schema pattern
- **Validation Array Errors**: Report missing or invalid validation criteria

## Examples

### Example 1: Valid Bug Detection Plan

**Input**:

```
file_path: .bug-detection-plan.json
```

**Content**:

```json
{
  "workflow": "bug-management",
  "phase": "detection",
  "phaseNumber": 1,
  "config": {
    "priority": "all",
    "categories": ["type-errors", "runtime-errors"],
    "maxBugsPerRun": 50
  },
  "validation": {
    "required": ["report-exists", "type-check"],
    "optional": ["tests"]
  },
  "nextAgent": "bug-hunter",
  "timestamp": "2025-10-18T14:00:00Z",
  "metadata": {
    "createdBy": "bug-orchestrator",
    "iteration": 1,
    "maxIterations": 3
  }
}
```

**Output**:

```json
{
  "valid": true,
  "file": ".bug-detection-plan.json",
  "errors": [],
  "warnings": [],
  "schema": "bug-plan",
  "schemaPath": ".claude/schemas/bug-plan.schema.json"
}
```

### Example 2: Missing Required Field

**Input**:

```
file_path: .security-scan-plan.json
```

**Content**:

```json
{
  "workflow": "security-audit",
  "phase": "scan",
  "config": {
    "categories": ["sql-injection"]
  },
  "validation": {
    "required": ["report-exists"]
  }
}
```

**Output**:

```json
{
  "valid": false,
  "file": ".security-scan-plan.json",
  "errors": [
    "Missing required property: config.severity",
    "Schema validation failed at /config/severity: required property missing"
  ],
  "warnings": [],
  "schema": "security-plan",
  "schemaPath": ".claude/schemas/security-plan.schema.json"
}
```

### Example 3: Invalid Enum Value

**Input**:

```
file_path: .dependency-audit-plan.json
```

**Content**:

```json
{
  "workflow": "dependency-management",
  "phase": "audit",
  "config": {
    "category": "deprecated",
    "severity": "critical"
  },
  "validation": {
    "required": ["report-exists", "lockfile-valid"]
  },
  "nextAgent": "dependency-auditor"
}
```

**Output**:

```json
{
  "valid": false,
  "file": ".dependency-audit-plan.json",
  "errors": [
    "Invalid enum value at /config/category: 'deprecated' not in allowed values ['security', 'unused', 'outdated', 'all']"
  ],
  "warnings": [],
  "schema": "dependency-plan",
  "schemaPath": ".claude/schemas/dependency-plan.schema.json"
}
```

### Example 4: Workflow/Phase Mismatch

**Input**:

```
file_path: .bug-fixing-plan.json
```

**Content**:

```json
{
  "workflow": "security-audit",
  "phase": "fixing",
  "config": {
    "priority": "critical"
  },
  "validation": {
    "required": ["type-check"]
  }
}
```

**Output**:

```json
{
  "valid": false,
  "file": ".bug-fixing-plan.json",
  "errors": [
    "Schema mismatch: file pattern suggests 'bug-plan' schema but workflow field is 'security-audit'",
    "Invalid enum value at /phase: 'fixing' not in allowed values ['detection', 'fixing', 'verification'] for bug-plan"
  ],
  "warnings": ["Consider renaming file to match workflow: .security-remediation-plan.json"],
  "schema": "bug-plan",
  "schemaPath": ".claude/schemas/bug-plan.schema.json"
}
```

## Validation

- [ ] Validates all required fields present
- [ ] Checks field types correctly (string, number, boolean, array, object)
- [ ] Validates enum values against allowed lists
- [ ] Identifies schema based on file name pattern
- [ ] Returns clear error messages with JSON paths
- [ ] Handles malformed JSON gracefully
- [ ] Validates domain-specific fields (priority, severity, category)
- [ ] Checks workflow/phase consistency
- [ ] Validates validation criteria arrays (required/optional)
- [ ] Handles schema file loading errors

## Supporting Files

Located in `.claude/schemas/`:

- `base-plan.schema.json`: Base schema for all plan files
- `bug-plan.schema.json`: Bug management workflow schema
- `security-plan.schema.json`: Security audit workflow schema
- `dead-code-plan.schema.json`: Dead code cleanup workflow schema
- `dependency-plan.schema.json`: Dependency management workflow schema

## Integration with Orchestrators

All orchestrators should use this Skill after creating plan files:

```markdown
## Step 3: Create Plan File

1. Write plan to `.{domain}-{phase}-plan.json`
2. Use validate-plan-file Skill to verify:
   - Input: file_path = ".{domain}-{phase}-plan.json"
   - Check result.valid === true
   - If errors exist, fix plan file and retry
3. Only signal readiness after validation passes
```

## Notes

**JSON Schema Validation**: This Skill performs full JSON Schema Draft-07 validation including:

- Type checking (string, number, boolean, array, object)
- Required properties
- Enum constraints
- Pattern matching
- Nested object validation (allOf, $ref)
- Array item validation

**File Naming Convention**: Plan files must follow pattern `.{domain}-{phase}-plan.json` where:

- `{domain}`: bug|security|dead-code|dependency
- `{phase}`: detection|fixing|verification (bugs), scan|remediation|verification (security), etc.

**Schema References**: Uses JSON Schema `$ref` for base schema inheritance. All domain schemas extend `base-plan.schema.json`.
