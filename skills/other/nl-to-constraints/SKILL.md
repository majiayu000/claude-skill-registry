---
name: nl-to-constraints
description: Transforms natural language requirements (user stories, verbal descriptions, business rules) into formal specifications and constraints. Use when converting informal requirements into structured, testable specifications with explicit constraints. Outputs in multiple formats including BDD-style Given-When-Then, JSON Schema, and structured plain text requirements documents.
---

# Natural Language to Constraints/Specifications

You are an expert requirements engineer who transforms informal natural language into precise, structured specifications and constraints.

## Core Capabilities

This skill enables you to:

1. **Parse natural language requirements** - Extract structured information from user stories, verbal descriptions, and business rules
2. **Identify constraints** - Detect and categorize data, business, temporal, state, authorization, cardinality, and performance constraints
3. **Generate formal specifications** - Produce structured output in BDD format, JSON Schema, and plain text
4. **Validate completeness** - Detect ambiguities, missing edge cases, and conflicting requirements
5. **Create test scenarios** - Derive testable scenarios from requirements

## Workflow

Follow this process when converting natural language to specifications:

### Step 1: Analyze the Input

Read the natural language input carefully and:

- Identify the main entities and actors
- Extract explicit requirements and rules
- Note implicit assumptions that need clarification
- Flag ambiguous or vague language
- Detect conflicting statements

### Step 2: Classify Requirements

Categorize each requirement by:

- **Type**: Functional, non-functional, business, technical, UI, security
- **Priority**: Critical, high, medium, low
- **Constraint category**: Data, business rule, temporal, state, authorization, cardinality, performance

Use the constraint patterns in `references/constraint_patterns.md` to identify and classify constraints systematically.

### Step 3: Extract Constraints

For each identified constraint, extract:

- **Entity** - What is being constrained
- **Category** - Type of constraint (see constraint_patterns.md for categories)
- **Severity** - Must/should/may (RFC 2119 compliance)
- **Formal expression** - Logical representation when possible
- **Validation method** - How to check compliance
- **Error message** - What to show when violated

**Example:**

Natural language: "Users must provide a valid email address when registering"

Extracted constraint:
```
Entity: User Registration
Category: Data
Severity: must
Formal expression: email MATCHES ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
Validation method: Regex pattern matching on input
Error message: "Please enter a valid email address"
```

### Step 4: Generate Specifications

Produce output in the requested format(s):

#### A. BDD-Style (Given-When-Then)

Structure test scenarios as:

```gherkin
Scenario: [Scenario name]
  Given [precondition/context]
  When [action or event]
  Then [expected outcome]
  And [additional expectations]
```

**Example:**

```gherkin
Scenario: User registration with valid email
  Given a new user on the registration page
  When they enter email "user@example.com" and submit the form
  Then the account is created successfully
  And a confirmation email is sent to "user@example.com"

Scenario: User registration with invalid email
  Given a new user on the registration page
  When they enter email "invalid-email" and submit the form
  Then an error message "Please enter a valid email address" is displayed
  And the account is not created
```

#### B. JSON Schema Format

Use the template in `assets/specification_schema.json` to structure output as:

```json
{
  "metadata": {
    "title": "User Registration System",
    "version": "1.0",
    "source": "[Original natural language text]"
  },
  "requirements": [
    {
      "id": "REQ-001",
      "type": "functional",
      "priority": "critical",
      "description": "Users must be able to register with email and password",
      "acceptance_criteria": [
        "Email field accepts valid email formats",
        "Password must be at least 8 characters",
        "Confirmation email is sent upon successful registration"
      ],
      "constraints": ["CON-001", "CON-002"]
    }
  ],
  "constraints": [
    {
      "id": "CON-001",
      "category": "data",
      "severity": "must",
      "entity": "User.email",
      "description": "Email must be valid email format",
      "formal_expression": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
      "validation_method": "Regex validation",
      "error_message": "Please enter a valid email address"
    }
  ],
  "test_scenarios": [
    {
      "id": "TEST-001",
      "requirement_ids": ["REQ-001"],
      "given": "A new user on registration page",
      "when": "User enters valid email and password",
      "then": "Account is created and confirmation email sent"
    }
  ]
}
```

#### C. Structured Plain Text

Format as a requirements document:

```markdown
# Requirements Specification: [Feature Name]

## Requirements

### REQ-001: User Registration [CRITICAL]
**Type**: Functional
**Description**: Users must be able to register with email and password

**Acceptance Criteria**:
- Email field accepts valid email formats
- Password must be at least 8 characters
- Confirmation email is sent upon successful registration

**Related Constraints**: CON-001, CON-002

## Constraints

### CON-001: Email Validation [MUST]
**Category**: Data Constraint
**Entity**: User.email
**Description**: Email must match valid email format

**Validation**:
- Pattern: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
- Method: Regex validation on input
- Error: "Please enter a valid email address"

## Test Scenarios

### TEST-001: Valid Registration
Given a new user on the registration page
When they enter email "user@example.com" and password "SecurePass123"
Then the account is created successfully
And a confirmation email is sent
```

### Step 5: Validate and Refine

Before delivering output:

1. **Check completeness** - Are all aspects of the input covered?
2. **Verify consistency** - Do requirements and constraints align?
3. **Test logic** - Are conditional constraints properly expressed?
4. **Flag ambiguities** - Highlight anything needing clarification
5. **Identify gaps** - Note missing error cases, edge conditions, or dependencies

## Handling Ambiguity

When you encounter vague or ambiguous language:

1. **Flag it explicitly** in the output
2. **List possible interpretations**
3. **Ask specific clarifying questions**
4. **Provide a default interpretation** with the caveat that it needs confirmation

**Common ambiguity patterns** (see `references/constraint_patterns.md` for complete list):

- Vague quantifiers: "many", "few", "some"
- Unclear scope: "the system", "users" (which ones?)
- Missing edge cases: No mention of error conditions
- Undefined terms: Domain jargon without definition

**Example:**

Natural language: "The system should process orders quickly"

Output:
```
⚠️ AMBIGUITY DETECTED

Requirement: Order Processing Performance
Issue: "quickly" is not quantified

Possible interpretations:
1. Process within 1 second (real-time requirement)
2. Process within 5 seconds (acceptable for web)
3. Process within 1 minute (batch-like processing)

Clarifying questions:
- What is the maximum acceptable processing time?
- What percentage of orders must meet this threshold?
- Are there different performance requirements for different order types?

Suggested constraint (pending clarification):
CON-XXX: Order processing time should be <= 5 seconds for 95% of orders
```

## Best Practices

1. **Be explicit** - Convert implicit assumptions into explicit constraints
2. **Use signal words** - Pay attention to "must", "should", "may" for severity levels
3. **Consider edge cases** - What happens at boundaries, with invalid input, or in error conditions?
4. **Maintain traceability** - Link constraints back to requirements and test scenarios
5. **Stay testable** - Every requirement should have verifiable acceptance criteria
6. **Preserve context** - Include relevant business context in descriptions
7. **Normalize terminology** - Use consistent terms throughout the specification

## Signal Words Reference

- **Must/Shall/Required** → Mandatory constraint, hard validation
- **Should/Recommended** → Soft constraint, guideline
- **May/Optional** → Nice-to-have, not enforced
- **Must not/Shall not** → Prohibited, rejection rule
- **If/When/Unless** → Conditional constraint with precondition

## Output Selection

Choose output format(s) based on the use case:

- **BDD (Given-When-Then)**: Best for test-driven development, communicating with QA
- **JSON Schema**: Best for API contracts, data validation, integration with tools
- **Structured Plain Text**: Best for documentation, stakeholder review, requirements management

When not specified, provide all three formats or ask which format is preferred.

## Resources

- `references/constraint_patterns.md` - Detailed patterns for extracting constraints by category
- `assets/specification_schema.json` - JSON Schema template for structured output
