---
name: pseudocode-to-specification
description: Analyzes pseudocode, algorithms, or code snippets to extract and document functional requirements and business specifications. Produces functional specifications, business logic documentation, data requirements, and workflow specifications focused exclusively on WHAT the system does, not HOW it's implemented. Use when analyzing pseudocode for business logic, extracting functional requirements from algorithms, documenting business behavior from code, reverse engineering functional specifications, or when users mention "pseudocode to spec", "extract requirements", "business logic documentation", "functional specification from code", or "requirements from pseudocode".
---

# Pseudocode to Specification

Extract functional requirements and business specifications from pseudocode, algorithms, or code snippets.

## Core Workflow

## 1. Analyze Pseudocode

Parse structure, control flow, and identify:

- Inputs, outputs, and data transformations
- Variables, constants, and data structures
- Algorithms and logic patterns
- Assumptions and implicit requirements

Ask for clarification on:

- Ambiguous variable names or operations
- Missing context about data sources/destinations
- Unclear business rules or constraints
- Undefined error handling or edge cases

### 2. Extract Functional Requirements

Document core business functionality as requirements:

```
FR-001: [Function Name]
Business Purpose: [Why this function exists]
Description: System shall [action] when [condition]
Inputs: [business data, parameters, context]
Processing Logic: [business rules and decision steps]
Outputs: [business results, side effects]
Business Rules: [constraints, validations, calculations]
Preconditions: [required business state]
Postconditions: [resulting business state]
```

For detailed requirement patterns: [requirements-patterns.md](references/requirements-patterns.md)

### 3. Extract Business Data Requirements

Identify business entities and their requirements:

- Business entities and their meaning
- Business attributes and their purpose
- Business constraints and validation rules
- Business relationships between entities
- Data lifecycle and state transitions

Document as:

```
Business Entity: [EntityName]
Business Meaning: [What this represents]
Attributes:
  - name: [Business meaning, constraints]
  - field: [Business purpose, validation rules]
Relationships:
  - [Business relationship] with [OtherEntity]
  - Cardinality: [min..max]
Business Rules:
  - [Business constraint or invariant]
Lifecycle States:
  - [State] → [State] when [condition]
```

### 4. Document Business Workflow and Logic

Analyze business process flow:

- Sequential business operations
- Business decision points and conditions
- Iterative business processes
- Business exception paths
- Business event triggers

Generate business workflow specification:

```
Business Process: [ProcessName]
Purpose: [Business goal]

Step 1: [Business Action]
  - Business Condition: [when/if from business perspective]
  - Action: [what happens in business terms]
  - Business Rules Applied: [relevant rules]
  - Next: [step or branch]

Step 2: [Business Decision]
  Branches:
    - If [business condition]: Go to Step 3
    - Else: Go to Step 5
  - Decision Criteria: [business factors]

Business Error Conditions:
  - [ErrorCondition]: [Business impact and recovery]
```

For complex business logic, use decision tables. See [mermaid-diagrams.md](references/mermaid-diagrams.md) for business flow notation.

### 5. Generate Service Function Specifications

Document service functions in business terms:

```
Function: [functionName]
Business Purpose: [What business problem this solves]
Business Context: [When/why this is needed]
Inputs:
  - param1: [Business meaning, constraints]
  - param2: [Business meaning, required/optional]
Processing Logic:
  1. [Business rule or validation]
  2. [Business calculation or transformation]
  3. [Business decision point]
Outputs: [Business result description]
Business Rules:
  - [Rule 1: condition → action]
  - [Rule 2: validation or constraint]
Error Conditions:
  - [Business error]: [Condition and meaning]
Example Business Scenarios:
  Scenario: [situation]
  Input: [business context]
  Output: [expected business result]
```

### 6. Identify Integration Points

Document functional dependencies on external systems:

```
Integration: [SystemName]
Business Purpose: [Why this dependency exists]
Data Exchanged: [Business data sent/received]
Business Rules:
  - [When interaction occurs]
  - [What triggers communication]
Failure Impact:
  - Business consequence: [Impact on business process]
  - Mitigation: [Business workaround or fallback]
```

### 7. Document Assumptions and Constraints

**Business Assumptions:**

- Expected data volumes and patterns
- User behavior expectations
- Business process frequency
- External system availability

**Business Constraints:**

- Regulatory requirements
- Business policy limitations
- Data retention requirements
- Compliance requirements

### 8. Identify Business Acceptance Criteria

Define how to verify functional correctness:

- Normal business scenarios
- Business edge cases and boundary conditions
- Business error conditions
- Business rules validation

Format:

```
Acceptance Criterion: AC-001
For: [FR-XXX]
Given: [business context]
When: [business action]
Then: [expected business outcome]

Business Scenarios:
  Scenario 1: Normal case
    - Context: [typical business situation]
    - Action: [user/system action]
    - Expected: [business result]
  
  Scenario 2: Edge case
    - Context: [boundary condition]
    - Action: [user/system action]
    - Expected: [business result]
```

## Output Formats

Generate functional specification based on context. Standard format:

**Functional Specification Document:**

```markdown
# [System/Component] Functional Specification

## 1. Overview
[Business purpose, scope, and objectives]

## 2. Functional Requirements
[FR-001, FR-002, etc. - business functionality]

## 3. Business Data Requirements
[Business entities, attributes, relationships, constraints]

## 4. Business Workflow and Logic
[Business process flows, decision logic, business rules]

## 5. Service Function Specifications
[Business functions, inputs/outputs, processing logic]

## 6. Integration Points
[External system dependencies at functional level]

## 7. Business Rules and Constraints
[Complete business logic, validation rules, calculations]

## 8. Business Acceptance Criteria
[How to verify functional correctness]

## 9. Assumptions and Dependencies
[Business assumptions and constraints]

## 10. Appendices
[Business flow diagrams, glossary, references]
```

**User Stories (Agile Format):**

```
Epic: [High-level business capability]

Story 1: As a [role], I want [capability] so that [business benefit]

Acceptance Criteria:
  - Given [business context], when [user action], then [business outcome]
  - Given [business context], when [user action], then [business outcome]

Business Rules:
  - [Rule 1: condition → action]
  - [Rule 2: constraint or validation]

Story 2: [Next story following same pattern]
```

For additional specification formats: [specification-templates.md](references/specification-templates.md)

## Key Principles

**Focus Strictly on Functional Requirements:**

- Extract WHAT the system does, not HOW it's built
- Describe business behavior, not technical implementation
- Specify business rules, not design patterns
- Document business logic, not architecture
- Exclude performance, security, scalability (non-functional)

**Maintain Business Traceability:**

- Link requirements to business logic in pseudocode
- Use identifiers: FR (functional), BR (business rule), AC (acceptance criteria)
- Reference pseudocode sections showing business logic

**Clarify Business Intent:**

- Extract WHY (business purpose) and WHAT (business capability)
- Describe business value and outcomes
- Separate business requirements from technical choices
- Mark inferred business rules vs stated logic

**Validate Functional Completeness:**

- Ensure all business logic paths documented
- Verify all business inputs/outputs specified
- Check all business error conditions covered
- Confirm all business rules extracted

## Common Business Patterns

Recognize and document business patterns:

**CRUD Operations:** Create/read/update/delete → Business entity management spec with business rules
**State Machines:** State transitions → Business lifecycle spec with state meanings and transition conditions
**Business Process:** Sequential steps → Business workflow spec with decision points
**Data Transformation:** Input → process → output → Business function spec with transformation rules
**Event-Driven:** Trigger → react → Business event spec with business triggers and actions

## Functional Specification Quality Checklist

Before finalizing, verify:

- ✓ All business logic from pseudocode extracted
- ✓ Requirements describe WHAT (functionality), not HOW (design/implementation)
- ✓ Business rules complete and clear
- ✓ Business entities and relationships defined
- ✓ Business workflows cover all decision paths
- ✓ Business error conditions documented
- ✓ Business assumptions stated
- ✓ Integration dependencies at functional level (data exchanged, not technical protocols)
- ✓ Acceptance criteria defined (functional verification, not test cases)
- ✓ No design decisions (architecture, patterns, technology choices)
- ✓ No implementation details (algorithms, data structures, code)
- ✓ No testing strategies (test plans, test cases, coverage)
- ✓ No deployment considerations (infrastructure, environments, scaling)
- ✓ Focus maintained exclusively on business functionality and requirements

## Examples

**Simple Algorithm:**

Input pseudocode:

```
function calculateShippingCost(weight, distance, priority):
    if weight <= 0 or distance <= 0:
        throw error "Invalid input"
    baseCost = weight * 0.5 + distance * 0.1
    if priority == "express":
        baseCost = baseCost * 1.5
    return round(baseCost, 2)
```

Generated functional specification excerpt:

```
FR-001: Shipping Cost Calculation

Business Purpose:
  Calculate shipping cost based on package characteristics and service level

Business Inputs:
  - weight: Package weight in kg (must be positive)
  - distance: Shipping distance in km (must be positive)
  - priority: Service level (express or standard)

Business Logic:
  1. Validate business constraints:
     - Weight must represent a real package (> 0)
     - Distance must be a valid route (> 0)
  2. Calculate base cost using business formula:
     - Weight component: weight × $0.50 per kg
     - Distance component: distance × $0.10 per km
  3. Apply service level multiplier:
     - Express service: 1.5× base cost
     - Standard service: 1.0× base cost (no change)
  4. Round to currency precision (2 decimal places)

Business Rules:
  - BR-001: Weight and distance must be positive values
  - BR-002: Express service costs 50% more than standard
  - BR-003: Cost calculated in USD currency

Business Output:
  - Shipping cost in USD

Business Error Conditions:
  - Invalid package weight: Cannot calculate for non-physical package
  - Invalid distance: Cannot calculate for invalid route
  - Unknown service level: Must specify express or standard service

Acceptance Criteria:
  - Given valid weight and distance, when calculating standard shipping,
    then cost equals (weight × 0.5 + distance × 0.1) rounded to 2 decimals
  - Given valid inputs with express priority, when calculating,
    then cost is 1.5× the standard calculation
```

**Complex Workflow:**

For detailed workflow examples with branching logic and integration points, see [specification-templates.md](references/specification-templates.md).

## Additional Resources

Load as needed:

- [specification-templates.md](references/specification-templates.md) - Industry-standard spec formats
- [requirements-patterns.md](references/requirements-patterns.md) - Common requirement structures
- [mermaid-diagrams.md](references/mermaid-diagrams.md) - Mermaid diagram notation and examples
