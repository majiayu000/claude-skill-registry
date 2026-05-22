---
name: software-engineering-standards
description: Reference and apply IEEE, ISO/IEC, and other software engineering standards for development, quality assurance, and project management. Use when selecting standards for specific activities, formatting standard references, establishing project frameworks, or creating documentation templates.
---

# Software Engineering Standards

## When to Use This Skill
- Selecting standards for a software project
- Formatting references to IEEE/ISO standards in documentation
- Establishing project lifecycle frameworks
- Creating quality assurance plans
- Developing project management documentation
- Determining which standards apply to specific development activities

## Standard Naming Convention

### Format
```
[Organization] Std [Number]-[Year], [Name]
```

### Components
- **Organization**: Standard body (IEEE, ISO, IEC, EIA, or combinations)
- **Std**: Literal text "Std"
- **Number**: Unique standard identifier
- **Year**: Adoption year
- **Name**: Descriptive title of the standard

### Examples
- `IEEE Std 830-1998, Recommended Practice for Software Requirements Specifications`
- `IEEE/EIA Std 12207-1997, Information Technology—Software Life Cycle Processes`
- `ISO/IEC Std 12207, Information Technology—Software Life Cycle Processes`

### Joint Standards
When multiple organizations adopt a standard, list all organizations:
- `IEEE/EIA Std 12207-1997` (joint IEEE and EIA adoption)

## Top-Level Framework Standard

### ISO/IEC 12207 - Software Life Cycle Processes

**Purpose**: Defines the international standard framework for software development and management project lifecycles.

**US Adoption**: Adopted as `IEEE/EIA Std 12207`

**Role**: Serves as the foundational standard that provides the basis for all other software engineering standards.

**When to reference**:
- Establishing overall project lifecycle framework
- Defining process architecture
- Creating process improvement plans

## Selecting Standards by Activity

### Software Development Activities
Use when creating requirements, design, configuration, or user documentation.

**See**: `references/development-standards.md`

### Quality Assurance Activities
Use when planning reviews, testing, or quality metrics.

**See**: `references/qa-standards.md`

### Project Management Activities
Use when creating project plans, managing risk, or measuring productivity.

**See**: `references/management-standards.md`

## Application Workflow

```
1. Identify activity type
   ↓
2. Check if top-level framework needed (ISO/IEC 12207)
   ↓
3. Select specific standard for activity
   ↓
4. Format reference correctly
   ↓
5. Apply standard requirements to deliverables
```

## Best Practices

- **Start with framework**: Begin with ISO/IEC 12207 for overall structure
- **Be specific**: Use the most specific standard for each activity
- **Stay current**: Use the latest year version unless project requirements specify otherwise
- **Document references**: Include standard citations in project documentation
- **Train team**: Ensure team understands applicable standards

## Common Use Cases

### Creating a Requirements Document
1. Reference: `IEEE Std 830-1998`
2. Follow structure defined in standard
3. Include standard citation in document header

### Establishing QA Process
1. Reference: `IEEE Std 730-2002` for overall QA plan
2. Reference: `IEEE Std 1028-1997` for review procedures
3. Reference: `IEEE Std 829-1998` for test documentation

### Project Planning
1. Reference: `IEEE Std 1058-1998` for project management plan
2. Reference: `IEEE Std 1074-1997` for lifecycle process definition
3. Reference: `IEEE Std 1540-2001` for risk management