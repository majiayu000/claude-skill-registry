---
name: bmad-commands
description: Atomic command primitives for BMAD operations. Provides type-safe, testable wrappers around file operations and test execution with structured JSON I/O and built-in telemetry. This skill should be used when BMAD workflows need deterministic, reliable primitive operations with observability.
allowed-tools: Bash, Read
acceptance:
  - commands_executed: "All requested commands executed successfully"
  - json_io_valid: "All inputs parsed and outputs generated as valid JSON"
  - telemetry_emitted: "Telemetry data emitted for all command executions"
  - errors_handled: "All errors caught and reported in structured format"
  - deterministic_behavior: "Same inputs produce same outputs (idempotent where applicable)"
inputs:
  command:
    type: enum
    values: ["read_file", "run_tests", "generate_architecture_diagram", "analyze_tech_stack", "extract_adrs", "validate_patterns"]
    required: true
    description: "Command name to execute"
  command_args:
    type: object
    required: true
    description: "Command-specific arguments (varies by command)"
    examples:
      read_file: {"path": "workspace/tasks/task-001.md"}
      run_tests: {"path": ".", "framework": "jest", "timeout": 120}
      generate_architecture_diagram: {"architecture": "docs/architecture.md", "type": "c4-context", "output": "docs/diagrams"}
outputs:
  success:
    type: boolean
    description: "Whether command executed successfully"
  outputs:
    type: object
    description: "Command-specific outputs (varies by command)"
  telemetry:
    type: object
    description: "Telemetry data with command, duration_ms, timestamp"
    required_fields: ["command", "duration_ms", "timestamp"]
  errors:
    type: array
    description: "Array of error objects (empty if success=true)"
    item_schema:
      error_code: "string"
      message: "string"
      details: "object (optional)"
telemetry:
  emit: "skill.bmad-commands.command-executed"
  track:
    - command
    - duration_ms
    - success
    - error_count
    - timestamp
  aggregations:
    - command_usage_frequency
    - average_duration_by_command
    - error_rate_by_command
---

# BMAD Commands

## Overview

BMAD Commands provide atomic, testable command primitives that BMAD skills compose into workflows. Each command follows a strict contract with typed inputs/outputs, structured error handling, and built-in telemetry.

**Design Principles:**
- **Deterministic**: Same inputs always produce same outputs
- **Testable**: Pure functions with JSON I/O
- **Observable**: All commands emit telemetry data
- **Composable**: Commands are building blocks for skills

## Available Commands

### read_file

Read file contents with metadata.

**Usage:**
```bash
python scripts/read_file.py --path <file-path> --output json
```

**Inputs:**
- `path` (required): Path to file to read

**Outputs:**
- `content`: File contents as text
- `line_count`: Number of lines
- `size_bytes`: File size in bytes
- `path`: Absolute path to file

**Example:**
```bash
python .claude/skills/bmad-commands/scripts/read_file.py \
  --path workspace/tasks/task-001.md \
  --output json
```

**Returns:**
```json
{
  "success": true,
  "outputs": {
    "content": "# Task Specification\n...",
    "line_count": 45,
    "size_bytes": 1024,
    "path": "/absolute/path/to/task-001.md"
  },
  "telemetry": {
    "command": "read_file",
    "duration_ms": 12,
    "timestamp": "2025-01-15T10:30:00Z",
    "path": "workspace/tasks/task-001.md",
    "line_count": 45
  },
  "errors": []
}
```

---

### run_tests

Execute tests with specified framework and return structured results.

**Usage:**
```bash
python scripts/run_tests.py --path <test-path> --framework <jest|pytest> --timeout <seconds> --output json
```

**Inputs:**
- `path` (required): Directory containing tests
- `framework` (optional): Test framework (default: jest)
- `timeout` (optional): Timeout in seconds (default: 120)

**Outputs:**
- `passed`: Whether all tests passed (boolean)
- `summary`: Human-readable summary
- `total_tests`: Total number of tests
- `passed_tests`: Number passed
- `failed_tests`: Number failed
- `coverage_percent`: Coverage percentage (0-100)
- `junit_path`: Path to JUnit report

**Example:**
```bash
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --timeout 120 \
  --output json
```

**Returns:**
```json
{
  "success": true,
  "outputs": {
    "passed": true,
    "summary": "10/10 tests passed",
    "total_tests": 10,
    "passed_tests": 10,
    "failed_tests": 0,
    "coverage_percent": 87,
    "junit_path": "./junit.xml"
  },
  "telemetry": {
    "command": "run_tests",
    "framework": "jest",
    "duration_ms": 4523,
    "timestamp": "2025-01-15T10:30:00Z",
    "total_tests": 10,
    "passed_tests": 10,
    "failed_tests": 0
  },
  "errors": []
}
```

---

### generate_architecture_diagram

Generate architecture diagrams from architecture documents (C4 model, deployment, sequence diagrams).

**Usage:**
```bash
python scripts/generate_architecture_diagram.py --architecture <file-path> --type <diagram-type> --output <output-dir>
```

**Inputs:**
- `architecture` (required): Path to architecture document
- `type` (required): Diagram type (c4-context, c4-container, c4-component, deployment, sequence)
- `output` (optional): Output directory (default: docs/diagrams)

**Outputs:**
- `diagram_path`: Path to generated diagram file
- `diagram_type`: Type of diagram generated
- `diagram_format`: Format (svg, png)
- `architecture_source`: Source architecture document

**Example:**
```bash
python .claude/skills/bmad-commands/scripts/generate_architecture_diagram.py \
  --architecture docs/architecture.md \
  --type c4-context \
  --output docs/diagrams
```

**Returns:**
```json
{
  "success": true,
  "outputs": {
    "diagram_path": "/path/to/docs/diagrams/c4-context-20250131.svg",
    "diagram_type": "c4-context",
    "diagram_format": "svg",
    "architecture_source": "docs/architecture.md"
  },
  "telemetry": {
    "command": "generate_architecture_diagram",
    "diagram_type": "c4-context",
    "duration_ms": 450,
    "timestamp": "2025-01-31T10:30:00Z"
  },
  "errors": []
}
```

---

### analyze_tech_stack

Analyze technology stack from architecture document, validate compatibility, identify risks.

**Usage:**
```bash
python scripts/analyze_tech_stack.py --architecture <file-path> --output <json|summary>
```

**Inputs:**
- `architecture` (required): Path to architecture document
- `output` (optional): Output format (default: json)

**Outputs:**
- `technologies`: List of detected technologies with categories
- `tech_count`: Number of technologies detected
- `categories`: Technology categories (frontend, backend, database, etc.)
- `compatibility`: Compatibility analysis and warnings
- `architecture_source`: Source architecture document

**Example:**
```bash
python .claude/skills/bmad-commands/scripts/analyze_tech_stack.py \
  --architecture docs/architecture.md \
  --output json
```

**Returns:**
```json
{
  "success": true,
  "outputs": {
    "technologies": [
      {"name": "React", "category": "frontend", "version": "18+"},
      {"name": "Node.js", "category": "backend", "version": "20+"},
      {"name": "PostgreSQL", "category": "database", "version": "15+"}
    ],
    "tech_count": 3,
    "categories": ["frontend", "backend", "database"],
    "compatibility": {
      "issues": [],
      "warnings": [],
      "recommendations": ["Verify versions are compatible"]
    },
    "architecture_source": "docs/architecture.md"
  },
  "telemetry": {
    "command": "analyze_tech_stack",
    "tech_count": 3,
    "duration_ms": 180,
    "timestamp": "2025-01-31T10:30:00Z"
  },
  "errors": []
}
```

---

### extract_adrs

Extract Architecture Decision Records (ADRs) from architecture document into separate files.

**Usage:**
```bash
python scripts/extract_adrs.py --architecture <file-path> --output <output-dir>
```

**Inputs:**
- `architecture` (required): Path to architecture document
- `output` (optional): Output directory for ADR files (default: docs/adrs)

**Outputs:**
- `adrs_extracted`: Number of ADRs extracted
- `adrs`: List of ADRs with number, title, and file path
- `output_directory`: Directory where ADRs were saved
- `architecture_source`: Source architecture document

**Example:**
```bash
python .claude/skills/bmad-commands/scripts/extract_adrs.py \
  --architecture docs/architecture.md \
  --output docs/adrs
```

**Returns:**
```json
{
  "success": true,
  "outputs": {
    "adrs_extracted": 5,
    "adrs": [
      {
        "number": "001",
        "title": "Technology Stack Selection",
        "file": "/path/to/docs/adrs/ADR-001-technology-stack-selection.md"
      },
      {
        "number": "002",
        "title": "Database Choice",
        "file": "/path/to/docs/adrs/ADR-002-database-choice.md"
      }
    ],
    "output_directory": "/path/to/docs/adrs",
    "architecture_source": "docs/architecture.md"
  },
  "telemetry": {
    "command": "extract_adrs",
    "adrs_count": 5,
    "duration_ms": 120,
    "timestamp": "2025-01-31T10:30:00Z"
  },
  "errors": []
}
```

---

### validate_patterns

Validate architectural patterns against best practices, check appropriateness for requirements.

**Usage:**
```bash
python scripts/validate_patterns.py --architecture <file-path> [--requirements <file-path>] --output <json|summary>
```

**Inputs:**
- `architecture` (required): Path to architecture document
- `requirements` (optional): Path to requirements document
- `output` (optional): Output format (default: json)

**Outputs:**
- `detected_patterns`: List of architectural patterns found
- `validation`: Validation results including warnings and recommendations
- `architecture_source`: Source architecture document
- `requirements_source`: Source requirements document (if provided)

**Example:**
```bash
python .claude/skills/bmad-commands/scripts/validate_patterns.py \
  --architecture docs/architecture.md \
  --requirements docs/prd.md \
  --output json
```

**Returns:**
```json
{
  "success": true,
  "outputs": {
    "detected_patterns": [
      {
        "name": "Microservices",
        "category": "architectural",
        "validated": true,
        "warnings": []
      },
      {
        "name": "Repository Pattern",
        "category": "architectural",
        "validated": true,
        "warnings": []
      }
    ],
    "validation": {
      "patterns_validated": 2,
      "patterns_appropriate": 2,
      "anti_patterns_detected": 0,
      "warnings": [],
      "recommendations": [
        "Validate pattern complexity matches team expertise",
        "Ensure pattern choice aligns with scale requirements"
      ]
    },
    "architecture_source": "docs/architecture.md",
    "requirements_source": "docs/prd.md"
  },
  "telemetry": {
    "command": "validate_patterns",
    "patterns_count": 2,
    "anti_patterns_count": 0,
    "duration_ms": 210,
    "timestamp": "2025-01-31T10:30:00Z"
  },
  "errors": []
}
```

---

## Response Format

All commands return JSON with this structure:

```json
{
  "success": boolean,
  "outputs": {
    // Command-specific outputs
  },
  "telemetry": {
    "command": string,
    "duration_ms": number,
    "timestamp": string,
    // Command-specific telemetry
  },
  "errors": [
    // Array of error strings (empty if success=true)
  ]
}
```

**Exit Codes:**
- `0`: Command succeeded (`success: true`)
- `1`: Command failed (`success: false`)

---

## Using Commands from Skills

To use commands from other skills, execute the script and parse the JSON output.

**Example in a skill's SKILL.md:**

```markdown
### Step 1: Read Task Specification

Execute the read_file command:

python .claude/skills/bmad-commands/scripts/read_file.py \
  --path workspace/tasks/{task_id}.md \
  --output json

Parse the JSON response and extract `outputs.content` for the task specification.

### Step 2: Run Tests

Execute the run_tests command:

python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json

Parse the JSON response and check `outputs.passed` to verify tests passed.
```

---

## Error Handling

All commands handle errors gracefully and return structured error information:

```json
{
  "success": false,
  "outputs": {},
  "telemetry": {
    "command": "read_file",
    "duration_ms": 5,
    "timestamp": "2025-01-15T10:30:00Z"
  },
  "errors": ["file_not_found"]
}
```

**Common Errors:**
- `file_not_found`: File doesn't exist
- `path_is_not_file`: Path is a directory
- `permission_denied`: Insufficient permissions
- `timeout`: Operation exceeded timeout
- `invalid_path`: Path validation failed
- `unexpected_error`: Unexpected error occurred

---

## Telemetry

All commands emit telemetry data for observability:

- `command`: Command name
- `duration_ms`: Execution time in milliseconds
- `timestamp`: ISO 8601 timestamp
- Command-specific metrics (e.g., line_count, test_count)

This telemetry enables:
- Performance monitoring
- Usage analytics
- Debugging workflows
- Production observability

---

## Command Contracts

Full command contracts (inputs, outputs, errors, telemetry) are documented in:
`references/command-contracts.yaml`

Reference this file when:
- Creating new commands
- Updating existing commands
- Integrating commands into skills
- Understanding command behavior

---

## Testing Commands

Test commands independently before using in workflows:

```bash
# Test read_file
python .claude/skills/bmad-commands/scripts/read_file.py \
  --path README.md \
  --output json

# Test run_tests (if you have a test suite)
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

Verify:
- JSON output is valid
- Exit code is 0 for success, 1 for failure
- Telemetry data is present
- Errors are structured

---

## Extending Commands

To add new commands:

1. Create `scripts/<command_name>.py`
2. Follow the standard response format
3. Add command contract to `references/command-contracts.yaml`
4. Update this SKILL.md with usage documentation
5. Make script executable: `chmod +x scripts/<command_name>.py`
6. Test independently before integrating

---

## Philosophy

Commands are the **foundation layer** of BMAD's 3-layer architecture:

1. **Commands** (this skill): Atomic, testable primitives
2. **Skills**: Compose commands into workflows
3. **Subagents**: Orchestrate skills with routing and guardrails

By keeping commands deterministic and testable, we enable:
- Unit testing of the framework itself
- Reliable skill composition
- Observable workflows
- Production-ready operations

---

## Utility Scripts

In addition to command primitives, this skill includes utility scripts for UX and system management:

### bmad-wizard.py

Interactive command wizard to help users find the right command for their task.

**Usage:**
```bash
python .claude/skills/bmad-commands/scripts/bmad-wizard.py
python .claude/skills/bmad-commands/scripts/bmad-wizard.py --list-all
python .claude/skills/bmad-commands/scripts/bmad-wizard.py --subagent alex
```

**Features:**
- Goal-based recommendations
- Interactive command selection
- Browse all commands
- Filter by subagent

**Documentation:** See `docs/UX-IMPROVEMENTS-GUIDE.md`

---

### error-handler.py

Professional error handling system with structured errors and remediation guidance.

**Usage:**
```bash
python .claude/skills/bmad-commands/scripts/error-handler.py
```

**Features:**
- 10 predefined error templates
- Structured error format
- Remediation steps
- Color-coded severity levels
- JSON output support

**Documentation:** See `docs/UX-IMPROVEMENTS-GUIDE.md`

---

### progress-visualizer.py

Real-time progress tracking for workflows with multiple visualization styles.

**Usage:**
```bash
python .claude/skills/bmad-commands/scripts/progress-visualizer.py
```

**Features:**
- 7-step workflow tracking
- 4 visualization styles (bar, spinner, dots, minimal)
- ETA calculation
- Elapsed time tracking
- Real-time updates

**Documentation:** See `docs/UX-IMPROVEMENTS-GUIDE.md`

---

### monitor-skills.py

Skill validation and monitoring tool for ensuring all skills are properly loaded.

**Usage:**
```bash
python .claude/skills/bmad-commands/scripts/monitor-skills.py
python .claude/skills/bmad-commands/scripts/monitor-skills.py --validate-only
python .claude/skills/bmad-commands/scripts/monitor-skills.py --category planning
python .claude/skills/bmad-commands/scripts/monitor-skills.py --skill implement-feature
python .claude/skills/bmad-commands/scripts/monitor-skills.py --json output.json
```

**Features:**
- Discover and validate all skills
- Check YAML frontmatter
- Verify workflow steps
- Export to JSON
- Category filtering

**Documentation:** See `docs/SKILL-LOADING-MONITORING.md`

---

### health-check.sh

Quick health check to validate system configuration and skill loading.

**Usage:**
```bash
./.claude/skills/bmad-commands/scripts/health-check.sh
```

**Features:**
- Check project structure
- Validate skills by category
- Check Python environment
- Validate required packages
- Check configuration
- Disk space check

**Documentation:** See `docs/SKILL-LOADING-MONITORING.md`

---

### deploy-to-project.sh

Smart deployment script for deploying BMAD Enhanced to other projects.

**Usage:**
```bash
./.claude/skills/bmad-commands/scripts/deploy-to-project.sh <target-directory>
./.claude/skills/bmad-commands/scripts/deploy-to-project.sh --full <target-directory>
./.claude/skills/bmad-commands/scripts/deploy-to-project.sh --dry-run <target-directory>
```

**Features:**
- Minimal or full deployment modes
- Dry-run mode
- Force overwrite option
- Symlink support for full mode
- Post-deployment instructions

**Documentation:** See `docs/DEPLOYMENT-TO-PROJECTS.md`

---
