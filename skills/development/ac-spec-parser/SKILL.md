---
name: ac-spec-parser
description: Parse and validate project specifications. Use when loading YAML/JSON specs, validating spec structure, extracting requirements, or converting between spec formats.
---

# AC Spec Parser

Parse and validate project specifications for autonomous coding.

## Purpose

Parses YAML/JSON/Markdown specifications into structured data for feature generation and planning.

## Quick Start

```python
from scripts.spec_parser import SpecParser

parser = SpecParser(project_dir)
spec = await parser.parse("spec.yaml")
print(spec.project_name)
print(spec.requirements)
```

## Supported Formats

- **YAML**: `.yaml`, `.yml` - Structured specifications
- **JSON**: `.json` - Machine-readable specs
- **Markdown**: `.md` - Human-readable specs with sections

## Specification Schema

```yaml
project:
  name: "Project Name"
  description: "What the project does"
  type: "web-app|api|cli|library"

requirements:
  functional:
    - id: "REQ-001"
      description: "User can login"
      priority: "high|medium|low"
      acceptance_criteria:
        - "Valid credentials grant access"
        - "Invalid credentials show error"

  non_functional:
    - id: "NFR-001"
      description: "Response under 200ms"
      category: "performance|security|usability"

technology:
  language: "python|typescript|go"
  framework: "fastapi|nextjs|gin"
  database: "postgresql|mongodb"

constraints:
  - "Must run on AWS"
  - "Budget under $100/month"
```

## Workflow

1. **Load**: Read spec file from disk
2. **Parse**: Convert to structured data
3. **Validate**: Check required fields and schema
4. **Normalize**: Standardize format for downstream use
5. **Export**: Output to feature analyzer

## Validation Rules

- Project name required
- At least one functional requirement
- All requirements have unique IDs
- Priority values are valid
- Technology stack is coherent

## Integration

Used by:
- `ac-spec-generator`: Generates feature list from parsed spec
- `ac-feature-analyzer`: Analyzes requirements
- `ac-complexity-assessor`: Estimates complexity

## API Reference

See `scripts/spec_parser.py` for full implementation.
