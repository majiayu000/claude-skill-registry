---
name: diagram-review
context: fork
description: Analyse architecture diagrams and flowcharts
model: opus
---

# /diagram-review

Perform comprehensive analysis of architecture diagrams, flowcharts, and technical drawings using Sonnet sub-agents.

## Usage

```
/diagram-review <image-path>
/diagram-review Attachments/architecture-diagram.png
/diagram-review Attachments/data-flow.png --type "C4"
/diagram-review Attachments/process-flow.png --project "Integration Project"
```

## Instructions

This skill uses **Sonnet model sub-agents** for thorough diagram analysis with vision capabilities.

### Phase 1: Diagram Loading

1. Verify the image exists at the specified path
2. Identify diagram type if specified or detect automatically
3. Load project context if provided

### Phase 2: Comprehensive Analysis (Sonnet Sub-Agents)

Launch these sub-agents using `model: "sonnet"`:

**Agent 1: Component Extraction** (Sonnet)
```
Task: Extract all components and elements from the diagram
- Read the image file using the Read tool
- Identify all boxes, shapes, and containers
- Extract all labels and text
- Note icons, symbols, and visual indicators
- Capture any legend or key information
Return: Complete component inventory with labels
```

**Agent 2: Relationship Mapping** (Sonnet)
```
Task: Map all connections and relationships
- Read the image file
- Identify all lines, arrows, and connectors
- Determine direction of data/process flow
- Note relationship types (dependency, data flow, API call, etc.)
- Identify any protocols or technologies on connections
- Map parent-child or containment relationships
Return: Relationship matrix with flow directions
```

**Agent 3: Architecture Pattern Analysis** (Sonnet)
```
Task: Analyse architectural patterns and quality
- Read the image file
- Identify the diagram type (C4, UML, flowchart, network, etc.)
- Recognise architectural patterns (microservices, layered, event-driven)
- Assess separation of concerns
- Identify potential single points of failure
- Note security boundaries if visible
- Evaluate completeness and clarity
- **Readability assessment:**
  - Count edge crossings (target: <5 for complex, 0 for simple)
  - Check visual hierarchy (is the system boundary the most prominent element?)
  - Verify consistent flow direction (L→R or T→B, not mixed)
  - Assess Gestalt proximity compliance (are related elements grouped together?)
  - Check single abstraction level (no database tables on container diagrams)
Return: Pattern analysis with architectural assessment and readability score
```

**Agent 4: Technology & Integration Analysis** (Sonnet)
```
Task: Identify technologies and integrations
- Read the image file
- Recognise technology logos and icons
- Identify cloud services (AWS, Azure, GCP)
- Note databases, queues, APIs
- Map external system integrations
- Identify known enterprise systems (ERP, MRO, data platforms, etc.)
Return: Technology inventory with integration points
```

### Phase 3: Compile Report

```markdown
# Diagram Analysis

**Image**: {{filename}}
**Analysed**: {{DATE}}
**Diagram Type**: {{C4/UML/Flowchart/Network/ERD/Other}}
**Project**: {{if specified}}

## Summary

{{3-4 sentence overview of what the diagram represents}}

## Component Inventory

### Systems/Services
| Component | Type | Description | Technology |
|-----------|------|-------------|------------|
{{component table}}

### Data Stores
| Store | Type | Purpose |
|-------|------|---------|
{{data stores}}

### External Systems
{{external dependencies}}

## Relationships

### Data Flows
```
{{ASCII representation of key flows}}
```

| Source | Target | Type | Protocol/Method |
|--------|--------|------|-----------------|
{{relationship table}}

### Dependencies
{{dependency analysis}}

## Architecture Assessment

### Patterns Identified
{{architectural patterns}}

### Strengths
{{positive aspects of the design}}

### Concerns
{{potential issues or risks}}

### Recommendations
{{suggested improvements}}

## Readability Assessment

| Criterion                     | Result            | Target                           |
|-------------------------------|-------------------|----------------------------------|
| **Edge crossings**            | {{count}}         | <5 for complex, 0 for simple     |
| **Visual hierarchy**          | {{pass/fail}}     | System boundary most prominent   |
| **Flow direction**            | {{L→R / T→B / mixed}} | Consistent single direction  |
| **Grouping effectiveness**    | {{pass/fail}}     | Related elements close together  |
| **Relationship traceability** | {{pass/fail}}     | Can follow each line clearly     |
| **Abstraction level**         | {{pass/fail}}     | One level per diagram            |

### Declaration Order Recommendation
{{If Mermaid/PlantUML source is available, suggest optimal declaration order based on data flow. Otherwise note "Source not available for declaration order analysis."}}

## Technology Stack

### Cloud Services
{{cloud platforms and services}}

### Databases
{{database technologies}}

### Integration Technologies
{{APIs, messaging, ETL tools}}

## Related Notes

### Matching Projects
{{links to related project notes}}

### Related ADRs
{{links to architecture decisions}}

### Related Systems
{{links to organisation or system notes}}

## Suggested Follow-ups

- [ ] {{action item based on analysis}}
- [ ] {{documentation suggestion}}
```

### Notes

- Optimised for C4 diagrams, UML, flowcharts, and network diagrams
- Can recognise organisation-specific systems and technologies
- Useful for architecture reviews and documentation
