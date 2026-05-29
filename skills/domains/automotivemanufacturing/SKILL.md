---
name: AutomotiveManufacturing
description: |
  Expert guidance for writing automotive manufacturing business processes, work instructions, and standard operating procedures.
  Follows IATF 16949, ISO 9001, and APQP/PPAP standards. Covers assembly, machining, quality/inspection, and material handling.
  USE WHEN user says 'write work instruction', 'create business process', 'automotive SOP', 'manufacturing procedure',
  'APQP documentation', 'process flow', or 'quality procedure'.

  Integrates with A3CriticalThinking for problem solving and SupplyChain for supplier requirements.
---

# Automotive Manufacturing Documentation

## When to Activate This Skill
- "Write a work instruction for [process]"
- "Create a business process for [operation]"
- "Document manufacturing procedure"
- "Build SOP for [automotive process]"
- "Create APQP documentation"
- "Write quality inspection procedure"
- "Document assembly/machining/material handling process"

## Core Document Types

### 1. Work Instructions (WI)
**Purpose**: Detailed step-by-step operator guidance
**Key Elements**:
- Clear title and document ID
- Scope and applicability
- Required materials, tools, equipment
- Safety warnings and PPE requirements
- Numbered sequential steps with visual aids
- Quality checkpoints and acceptance criteria
- References to specifications/standards

### 2. Standard Operating Procedures (SOP)
**Purpose**: Standardized process methodology
**Key Elements**:
- Purpose and scope
- Responsibilities and authorities
- Process flowchart
- Detailed procedure steps
- Forms and records
- Related documents
- Revision history

### 3. Business Process Documents
**Purpose**: High-level process definition and control
**Key Elements**:
- Process ownership
- Inputs and outputs
- Key performance indicators (KPIs)
- Process flow diagram
- Interaction with other processes
- Risks and controls
- Continuous improvement tracking

## Standards Compliance

### IATF 16949 Requirements
- Process approach methodology
- Risk-based thinking
- Turtle diagrams for process definition
- FMEA linkage
- Control plan alignment
- Layered process audits consideration

### ISO 9001 Structure
- Context of organization
- Leadership and planning
- Support and operation
- Performance evaluation
- Improvement focus

### APQP/PPAP Integration
- Process flow diagrams
- PFMEA considerations
- Control plans
- Work instructions as PPAP deliverables
- Measurement system analysis references

## Writing Framework

### Document Structure Template
```
1. HEADER
   - Document Title
   - Document Number
   - Revision/Date
   - Approvals (Prepared/Reviewed/Approved)

2. PURPOSE & SCOPE
   - Why this document exists
   - What processes/operations it covers
   - What it doesn't cover

3. RESPONSIBILITIES
   - Who performs the work
   - Who supervises
   - Who approves/validates

4. SAFETY & PPE
   - Hazards and risks
   - Required personal protective equipment
   - Emergency procedures

5. MATERIALS & EQUIPMENT
   - Parts/components list
   - Tools required
   - Equipment specifications
   - Gages and measuring devices

6. PROCEDURE/STEPS
   - Sequential numbered steps
   - Action-oriented language (verb-first)
   - Visual aids (photos, diagrams)
   - Quality checks embedded

7. QUALITY REQUIREMENTS
   - Specifications and tolerances
   - Inspection frequency
   - Acceptance/rejection criteria
   - Rework procedures

8. RECORDS & DOCUMENTATION
   - What gets recorded
   - Where records stored
   - Retention requirements

9. REFERENCES
   - Related documents
   - Engineering drawings
   - Specifications
   - Standards

10. REVISION HISTORY
    - Date, revision, changes made
```

## Process Type Guidelines

### Assembly Operations
- **Focus**: Sequence, torque specs, orientation
- **Include**: Part numbers, installation direction, fastener specifications
- **Visuals**: Assembly diagrams, before/after photos, exploded views
- **Checks**: Fit, alignment, function tests

### Machining Operations
- **Focus**: Setup, program, tooling, parameters
- **Include**: Machine settings, feed/speed, tool specifications, fixtures
- **Visuals**: Setup photos, tool paths, measurement points
- **Checks**: Dimensional verification, surface finish, first-piece inspection

### Quality/Inspection
- **Focus**: What to inspect, how to measure, accept/reject criteria
- **Include**: Gage R&R references, sampling plans, measurement methods
- **Visuals**: Measurement locations, gage usage, defect examples
- **Checks**: Calibration verification, data recording

### Material Handling
- **Focus**: Movement, storage, protection, traceability
- **Include**: Handling methods, storage conditions, labeling, FIFO
- **Visuals**: Packaging methods, storage layouts, label formats
- **Checks**: Condition verification, count accuracy, traceability

## Best Practices

### Writing Style
- **Active voice**: "Insert the bolt" not "The bolt is inserted"
- **Present tense**: "Check the torque" not "The torque should be checked"
- **Imperative mood**: Direct commands to operator
- **Concise**: One action per step
- **Specific**: Exact values, not ranges when possible

### Visual Elements
- Photos of actual parts/processes (preferred)
- Diagrams for complex assemblies
- Flowcharts for decision points
- Callouts for critical features
- Color coding for emphasis (warnings in red/yellow)

### Quality Integration
- Embed quality checks within process steps
- Reference control plans
- Link to FMEA high-priority items
- Include mistake-proofing (poka-yoke) features
- Document inspection frequency

### Revision Control
- Clear document numbering system
- Revision history table
- Change bars for modified sections
- Effective date tracking
- Training requirements for changes

## Common Mistakes to Avoid
- Assuming operator knowledge
- Missing safety information
- Vague quantities or specifications
- No visual aids for complex operations
- Incomplete tool/equipment lists
- Missing quality acceptance criteria
- No revision history
- Passive voice or unclear instructions

## Quick Reference: Document Selection

| Need | Document Type | Complexity |
|------|--------------|------------|
| Operator guidance | Work Instruction | Low-Medium |
| Department procedure | SOP | Medium |
| Process definition | Business Process | Medium-High |
| Quality procedure | Quality SOP | Medium |
| Inspection method | Inspection WI | Low-Medium |

## Output Format

When creating documents, structure output as:

```markdown
# [DOCUMENT TITLE]
**Document Number**: [AUTO-XXX-####]
**Revision**: [X] | **Date**: [YYYY-MM-DD]
**Prepared**: _____ | **Reviewed**: _____ | **Approved**: _____

## 1. Purpose & Scope
[Content]

## 2. Responsibilities
[Content]

[Continue with standard sections...]
```

## Supplementary Resources

For comprehensive methodologies and advanced topics:
`read ~/.claude/skills/AutomotiveManufacturing/CLAUDE.md`

For document templates:
`ls ~/.claude/skills/AutomotiveManufacturing/templates/`

## Integration with Related Skills

### A3CriticalThinking
When manufacturing issues arise, use A3 problem-solving methodology:
- Quality defects → Root cause analysis (5 Whys, Fishbone)
- Process failures → Structured countermeasure development
- Decision making → Apply priority hierarchy (Safety → Customer → Cost)

**Load A3 skill:** `read ~/.claude/skills/A3CriticalThinking/SKILL.md`

### SupplyChain
For supplier-related documentation and requirements:
- Supplier quality requirements in work instructions
- PPAP documentation for purchased components
- Incoming inspection procedures

**Load SupplyChain skill:** `read ~/.claude/skills/SupplyChain/SKILL.md`

### HoshinKanri
For strategic alignment of manufacturing objectives:
- Cascade targets to shop floor metrics
- Link work instructions to quality objectives
- Bowling chart for manufacturing KPIs

**Load HoshinKanri skill:** `read ~/.claude/skills/HoshinKanri/SKILL.md`

---

## Key Principles

**Priority Hierarchy (from A3CriticalThinking):**
```
1. SAFETY FIRST     → Never compromise for cost or delivery
2. CUSTOMER VALUE   → Quality that meets/exceeds requirements
3. SHAREHOLDER VALUE → Optimize after 1 & 2 are secured
```

1. **Safety First**: Always lead with safety considerations - this is non-negotiable
2. **Clarity Over Brevity**: Be clear, even if it takes more words
3. **Visual Communication**: A picture is worth 1000 words
4. **Measurable Requirements**: Specific, measurable acceptance criteria
5. **Traceability**: Link to higher-level documents and standards
6. **Living Documents**: Build in revision and improvement processes
7. **Problem Solving**: Use A3 methodology for issues and improvements
