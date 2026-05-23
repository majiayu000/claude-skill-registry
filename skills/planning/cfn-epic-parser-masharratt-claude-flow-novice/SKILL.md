---
name: cfn-epic-parser
description: "Converts natural language epic documents from markdown into structured JSON configurations for MDAP or CFN Loop execution. Use when you need to parse epic documents, validate epic structure, or generate execution configurations from planning documents."
version: 1.0.0
tags: [epic, parser, mdap, cfn-loop, planning]
status: production
---

# CFN Epic Parser

## Overview

The cfn-epic-parser skill converts natural language epic documents written in markdown format into structured JSON configurations suitable for execution in either MDAP or CFN Loop modes.

## Usage

### Basic Usage

```bash
# Parse with auto-detected mode
./.claude/skills/cfn-epic-parser/parse.sh planning/my-epic.md

# Force MDAP mode
./.claude/skills/cfn-epic-parser/parse.sh planning/my-epic.md --mode mdap

# Force CFN Loop mode with output file
./.claude/skills/cfn-epic-parser/parse.sh planning/my-epic.md --mode cfn-loop --output epic-config.json

# Validate epic structure without generating output
./.claude/skills/cfn-epic-parser/parse.sh planning/my-epic.md --validate

# Enable verbose logging
./.claude/skills/cfn-epic-parser/parse.sh planning/my-epic.md --verbose
```

### Command Line Options

- `<input.md>`: Path to the epic markdown file to parse (required)
- `-o, --output <file>`: Output JSON file path (default: stdout)
- `-m, --mode <mode>`: Execution mode: `mdap`, `cfn-loop`, or `auto` (default: auto)
- `-v, --validate`: Validate epic structure without generating output
- `-V, --verbose`: Enable verbose logging
- `-h, --help`: Show help message

### Mode Descriptions

- **auto**: Automatically detect mode based on epic content
  - Detects CFN Loop mode if multiple phases are defined
  - Defaults to MDAP mode for single-phase epics
- **mdap**: Generate MDAP-compatible configuration for atomic task execution
  - Creates task-based structure with maxTaskSize of 50 lines
  - Atomic execution with pre-loaded context injection
- **cfn-loop**: Generate CFN Loop configuration for phased execution
  - Creates phase-based structure with dependencies
  - Configures consensus and gate thresholds for validation

## Epic Document Format

The parser expects markdown files with the following structure:

### Required Sections

```markdown
# Epic Title

**Epic ID**: `unique-epic-identifier`
**Status**: [Not Started | In Progress | Completed]
**Estimated Duration**: [X weeks]
**Owner**: [Team or individual]
**Priority**: [Low | Medium | High]

## Epic Description

Detailed description of the epic goals and scope.

## Strategic Goals

1. Goal one description
2. Goal two description
3. ...

## Phases (for CFN Loop)

### Phase 1: Phase Name
**Status**: Not Started
**Duration**: X weeks
**Dependencies**: [None | Phase X, Phase Y]

Description of phase goals.

### Phase 2: Phase Name
...
```

### Optional Fields

- **Agents**: Number of agents involved (e.g., `Agents: 50`)
- **File**: Reference to phase file (e.g., `File: planning/phase-1.md`)
- **Deliverables**: List of expected deliverables
- **Acceptance Criteria**: Checklist of completion criteria

## Output Format

### MDAP Mode Output

```json
{
  "executionMode": "mdap",
  "metadata": {
    "epicId": "unique-identifier",
    "name": "Epic Title",
    "description": "Epic description",
    "status": "not_started",
    "priority": "high",
    "estimatedDuration": "10 weeks",
    "owner": "Team Name"
  },
  "goals": ["Goal 1", "Goal 2", "Goal 3"],
  "tasks": [],
  "configuration": {
    "maxTaskSize": 50,
    "atomicExecution": true,
    "contextInjection": "pre-loaded"
  }
}
```

### CFN Loop Mode Output

```json
{
  "executionMode": "cfn-loop",
  "metadata": { ... },
  "phases": [
    {
      "phaseId": "phase-1",
      "name": "Phase Name",
      "description": "Phase description",
      "status": "not_started",
      "estimatedDuration": "5 weeks",
      "dependencies": []
    },
    ...
  ],
  "goals": ["Goal 1", "Goal 2", "Goal 3"],
  "configuration": {
    "loopMode": "standard",
    "consensusThreshold": 0.90,
    "gateThreshold": 0.95
  }
}
```

## Testing

Run the test suite to verify parser functionality:

```bash
./.claude/skills/cfn-epic-parser/test-parser.sh
```

The test suite validates:
- Help output and error handling
- Metadata extraction (ID, status, priority, etc.)
- Phase parsing and dependency tracking
- Goal extraction from Strategic Goals section
- Mode auto-detection based on content
- Validation of epic structure
- File output generation

## Dependencies

- `jq`: Required for JSON processing
  - Ubuntu/Debian: `sudo apt-get install jq`
  - macOS: `brew install jq`

## Examples

### Parse Marketing Epic

```bash
./.claude/skills/cfn-epic-parser/parse.sh \
  planning/global/marketing/EPIC_OVERVIEW.md \
  --mode cfn-loop \
  --output marketing-epic-config.json
```

### Validate Epic Structure

```bash
./.claude/skills/cfn-epic-parser/parse.sh \
  planning/my-new-epic.md \
  --validate --verbose
```

### Generate MDAP Configuration

```bash
./.claude/skills/cfn-epic-parser/parse.sh \
  planning/simple-feature-epic.md \
  --mode mdap \
  --output simple-feature-config.json
```

## Error Handling

The parser provides clear error messages for:
- Missing input files
- Invalid execution modes
- Malformed epic structure
- Missing required fields
- JSON validation failures

## Integration with CFN Workflows

The generated JSON configurations can be used by:
- CFN Loop orchestrator for phased execution
- MDAP decomposer for atomic task generation
- Epic management tools for tracking progress
- Validation agents for structure compliance

## Best Practices

1. **Consistent Epic IDs**: Use lowercase with hyphens (e.g., `user-authentication-v2`)
2. **Clear Phase Dependencies**: Explicitly list dependencies in each phase
3. **Specific Goals**: Use numbered lists for strategic goals
4. **Descriptive Phases**: Include duration and clear deliverables
5. **Status Tracking**: Keep status updated for accurate reporting