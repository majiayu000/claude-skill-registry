---
name: ontology-core
description: |
  Core Ontology Schema Validator for Ontology-Driven-Architecture (ODA) codebases.
  Validates ObjectType, LinkType, ActionType, and PropertyDefinition schemas.
  Generates scaffold templates and checks cross-type consistency.
user-invocable: true
model: opus
version: "3.0.0"
argument-hint: "validate <file> | validate-all <dir> | scaffold <type> <name> | check-links <dir>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Task
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/workload-files.sh"
      timeout: 5000
---

# /ontology-core - Core Ontology Schema Validator

> **Version:** 3.0.0 | **Model:** opus

---

## Overview

| Aspect | Description |
|--------|-------------|
| **Purpose** | Validate and scaffold ODA ontology type definitions |
| **Output** | L1: Pass/fail summary / L2: Per-file results / L3: Detailed fix suggestions |
| **Reference** | `.claude/rules/ontology.md` for naming conventions and rules |

---

## Cross-Skill Integration

| Skill | Relationship |
|-------|--------------|
| `/ontology-objecttype` | Calls this skill for validation after generation |
| `/ontology-why` | Provides design rationale for validation errors |
| `/ontology-linktype` | (Planned) LinkType definition assistant |

---

## Commands

| Command | Description |
|---------|-------------|
| `validate <file>` | Validate single ontology file |
| `validate-all <dir>` | Validate all files in directory |
| `scaffold <type> <name>` | Generate ObjectType/LinkType/ActionType template |
| `check-links <dir>` | Cross-validate LinkType source/target references |

---

## Supported Types

| Type | Key Validations |
|------|-----------------|
| **ObjectType** | Primary key, properties, backing dataset |
| **LinkType** | Cardinality, foreign key, cascade policy |
| **ActionType** | Parameters, affected types, edit specs |
| **PropertyDefinition** | Data type, constraints, visibility |

---

## Validation Rules

### ObjectType Rules

| Rule ID | Name | Severity |
|---------|------|----------|
| OT-001 | Primary Key Required | ERROR |
| OT-002 | Primary Key Property Exists | ERROR |
| OT-003 | Unique Property Names | ERROR |
| OT-004 | Valid Status | ERROR |
| OT-005 | Endorsed Requires Active | WARNING |
| OT-006 | Backing Dataset RID Format | ERROR |
| OT-007 | Property Data Type Valid | ERROR |

### LinkType Rules

| Rule ID | Name | Severity |
|---------|------|----------|
| LT-001 | Source ObjectType Required | ERROR |
| LT-002 | Target ObjectType Required | ERROR |
| LT-003 | Cardinality Required | ERROR |
| LT-004 | Foreign Key Implementation | ERROR |
| LT-005 | Backing Table for N:N | ERROR |
| LT-006 | No Endorsed Status | WARNING |
| LT-007 | Cascade Policy Consistency | WARNING |

### ActionType Rules

| Rule ID | Name | Severity |
|---------|------|----------|
| AT-001 | Unique Parameter Names | ERROR |
| AT-002 | Required Parameters First | WARNING |
| AT-003 | Affected ObjectType Exists | ERROR |
| AT-004 | Hazardous Flag | WARNING |
| AT-005 | Edit Spec Property Valid | ERROR |
| AT-006 | Implementation Required | ERROR |
| AT-007 | No Endorsed Status | WARNING |

### PropertyDefinition Rules

| Rule ID | Name | Severity |
|---------|------|----------|
| PD-001 | Valid Data Type | ERROR |
| PD-002 | Array Item Type | ERROR |
| PD-003 | Struct Reference | ERROR |
| PD-004 | Required Without Default | WARNING |
| PD-005 | Primary Key Constraints | ERROR |

---

## Output Format

### L1 - Summary (Default)

```
Validation Complete: 3 files, 21 rules passed, 1 warning, 0 errors
```

### L2 - Per-File Results

```
Validating: src/ontology/

src/ontology/employee.py
  ObjectType: Employee (7 passed, 1 warning)
    OT-005: Endorsed Requires Active

src/ontology/links.py
  LinkType: ProjectToEmployee (5 passed, 2 errors)
    LT-001: Source ObjectType 'Project' not found

Summary: 26 passed, 1 warning, 2 errors
```

### L3 - Detailed with Fix Suggestions

```
LT-001: Source ObjectType Required
   File: src/ontology/links.py:45
   LinkType: ProjectToEmployee
   Issue: source_object_type references 'Project' which doesn't exist

   Fix: Create Project ObjectType first, or change source to existing type

   Available ObjectTypes:
   - Employee (src/ontology/employee.py)
   - Department (src/ontology/department.py)
```

---

## Scaffold Templates

### ObjectType Template

```python
from ontology_definition.types import (
    ObjectType, PropertyDefinition, DataTypeSpec,
    PrimaryKeyDefinition, PropertyConstraints,
)
from ontology_definition.core.enums import DataType, ObjectStatus

{entity_name_lower}_type = ObjectType(
    api_name="{EntityName}",
    display_name="{Entity Name}",
    description="TODO: Add description",
    primary_key=PrimaryKeyDefinition(property_api_name="{entityName}Id"),
    properties=[
        PropertyDefinition(
            api_name="{entityName}Id",
            display_name="{Entity Name} ID",
            data_type=DataTypeSpec(type=DataType.STRING),
            constraints=PropertyConstraints(required=True, unique=True),
        ),
        # TODO(human): Add more properties
    ],
    status=ObjectStatus.ACTIVE,
)
```

### LinkType Template

```python
from ontology_definition.types import (
    LinkType, ObjectTypeReference, CardinalityConfig,
    LinkImplementation, ForeignKeyConfig,
)
from ontology_definition.core.enums import Cardinality, LinkImplementationType

{source_lower}_to_{target_lower} = LinkType(
    api_name="{Source}To{Target}",
    display_name="{Source} to {Target}",
    source_object_type=ObjectTypeReference(api_name="{Source}"),
    target_object_type=ObjectTypeReference(api_name="{Target}"),
    cardinality=CardinalityConfig(type=Cardinality.MANY_TO_ONE),
    implementation=LinkImplementation(
        type=LinkImplementationType.FOREIGN_KEY,
        foreign_key=ForeignKeyConfig(
            foreign_key_property="{target}Id",
            foreign_key_location=ForeignKeyLocation.SOURCE,
        ),
    ),
)
```

---

## Package Reference

```python
from ontology_definition.types import (
    ObjectType, LinkType, ActionType, PropertyDefinition,
)
from ontology_definition.core.enums import (
    DataType, ObjectStatus, Cardinality, LinkImplementationType,
)
```

**Package Location:** `/home/palantir/park-kyungchan/palantir/Ontology-Definition/`

---

## Error Handling

| Error | Recovery |
|-------|----------|
| File not found | Show available files |
| Parse error | Show line number and context |
| Unknown type | Suggest valid type names |
| Validation timeout | Save partial results |

---

## Version History

| Version | Change |
|---------|--------|
| 1.0.0 | Core ontology schema validator |
| 3.0.0 | Frontmatter normalization, MCP tool inclusion, duplicate removal |

**End of Skill Definition**
