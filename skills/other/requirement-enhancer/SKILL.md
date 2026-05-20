---
name: requirement-enhancer
description: "Iteratively enhance user requirements into clear, complete, actionable specifications through analysis and clarification. Use when: (1) Users provide initial requirements that need refinement, (2) Requirements are vague, incomplete, or ambiguous, (3) Creating formal specifications from informal descriptions, (4) Identifying missing constraints, edge cases, or acceptance criteria, (5) Clarifying assumptions and implicit dependencies, or (6) Preparing requirements for design, implementation, or verification. Operates interactively: analyze → ask clarifying questions → refine based on responses."
---

# Requirement Enhancer

Transform initial requirements into clear, complete, actionable specifications through iterative analysis and refinement.

## Core Principles

### Preserve Intent
- Maintain the user's original goals and vision
- Do not change fundamental requirements without confirmation
- Clarify rather than assume

### Iterative Refinement
- Analyze → Ask → Refine → Repeat
- Ask targeted questions to fill gaps
- Incorporate user responses progressively

### Explicit Over Implicit
- Make assumptions visible with [ASSUMED] or [INFERRED] labels
- Distinguish confirmed facts from educated guesses
- Highlight areas needing clarification

### Avoid Over-Specification
- Do not add unnecessary details without user input
- Focus on essential requirements first
- Mark nice-to-have vs. must-have clearly

## Enhancement Workflow

### 1. Initial Analysis

Analyze the requirement across multiple dimensions:

**Clarity**: Identify vague terms, ambiguous language, undefined metrics
**Completeness**: Find missing functional/non-functional requirements, edge cases
**Consistency**: Detect conflicts, contradictions, terminology issues
**Feasibility**: Note technical concerns, resource constraints
**Testability**: Check for measurable acceptance criteria

### 2. Identify Issues

Categorize issues by severity:

🔴 **Critical**: Core functionality undefined, conflicting requirements
🟡 **Important**: Missing constraints, unclear scope, vague metrics
🟢 **Minor**: Terminology inconsistencies, formatting issues

### 3. Formulate Questions

Ask targeted clarification questions:

**For ambiguity**: "What exactly does [vague term] mean in measurable terms?"
**For incompleteness**: "What should happen when [edge case]?"
**For conflicts**: "How do requirements X and Y work together?"
**For missing details**: "What are the [performance/security/usability] requirements?"

Use the AskUserQuestion tool to present questions clearly.

### 4. Incorporate Responses

Based on user answers:
- Update requirements with confirmed information
- Add [CONFIRMED] labels to user-provided details
- Keep [ASSUMED] labels for inferences
- Note [INFERRED] for logical deductions

### 5. Enrich with Domain Knowledge

Add standard practices when applicable:

**For authentication**: Password requirements, session management, rate limiting
**For APIs**: Error codes, versioning, rate limits, documentation
**For data processing**: Validation, error handling, performance bounds
**For web apps**: Browser compatibility, accessibility, security (OWASP)

Label enrichments as [STANDARD PRACTICE] or [BEST PRACTICE].

### 6. Structure Output

Organize enhanced requirement in clear sections:

```markdown
## [Requirement Name]

### Overview
[Brief description preserving original intent]

### Functional Requirements
[Detailed functional requirements with IDs]

### Non-Functional Requirements
[Performance, security, usability, etc.]

### Acceptance Criteria
[Testable criteria in Given/When/Then format]

### Assumptions
[Explicit list of assumptions with labels]

### Edge Cases
[Identified edge cases and expected behavior]

### Constraints
[Technical, business, regulatory constraints]

### Out of Scope
[Explicitly excluded items]
```

## Analysis Framework

For detailed analysis dimensions and patterns, see [analysis_framework.md](references/analysis_framework.md).

Key areas to analyze:
- Clarity and precision
- Completeness
- Consistency
- Feasibility
- Testability

## Common Ambiguity Patterns

### Quantifier Ambiguity
**Vague**: "The system should be fast"
**Enhanced**: "The system MUST respond within 200ms for 95% of requests"

### Modal Ambiguity
**Vague**: "The system should support users"
**Enhanced**: "The system MUST support at least 10,000 concurrent users"

### Scope Ambiguity
**Vague**: "Users can edit documents"
**Enhanced**: "Authenticated users with 'Editor' role can modify content of documents they own"

### Temporal Ambiguity
**Vague**: "Backup data regularly"
**Enhanced**: "Perform incremental backups every 6 hours, full backups daily at 2 AM UTC"

### Conditional Ambiguity
**Vague**: "If user is inactive, log them out"
**Enhanced**: "After 30 min inactivity, warn user. After 35 min total, save work and log out"

## Requirement Categories

### Functional Requirements (FR)
What the system must do:
- User actions and system responses
- Data processing and transformations
- Business logic and rules
- Integration points

### Non-Functional Requirements (NFR)
How the system must perform:
- **Performance**: Response time, throughput, latency
- **Security**: Authentication, authorization, encryption
- **Usability**: User experience, accessibility
- **Reliability**: Uptime, error rates, recovery
- **Scalability**: Load handling, growth capacity
- **Maintainability**: Code quality, documentation

### Acceptance Criteria (AC)
Testable conditions for requirement satisfaction:
- Given [precondition]
- When [action]
- Then [expected result]

## Labeling Conventions

### Confirmation Status
- `[CONFIRMED]`: User explicitly confirmed
- `[ASSUMED]`: Reasonable assumption, needs confirmation
- `[INFERRED]`: Logical deduction from confirmed facts
- `[STANDARD PRACTICE]`: Industry-standard approach
- `[BEST PRACTICE]`: Recommended approach

### Priority Levels (RFC 2119)
- `MUST`: Mandatory, non-negotiable
- `SHOULD`: Highly desired, may be deferred
- `MAY`: Optional, nice-to-have
- `MUST NOT`: Explicitly forbidden

### Risk Indicators
- 🔴 Critical issue requiring immediate attention
- 🟡 Important issue to address
- 🟢 Minor issue or improvement

## Output Format

Structure enhanced requirements as Markdown:

```markdown
# [Feature/System Name]

## Overview
[Brief description, 2-3 sentences]

## Functional Requirements

### FR-[ID]-001: [Requirement Name]
- **Priority**: MUST/SHOULD/MAY
- **Description**: [Detailed description]
- **Acceptance Criteria**:
  - Given [precondition]
  - When [action]
  - Then [expected result]

## Non-Functional Requirements

### NFR-[ID]-001: [Category]
- **Priority**: MUST/SHOULD/MAY
- **Description**: [Specific requirement with metrics]
- **Measurement**: [How to verify]

## Assumptions
- [CONFIRMED] [User-confirmed assumption]
- [ASSUMED] [Reasonable assumption needing confirmation]
- [INFERRED] [Logical deduction]

## Edge Cases
- **[Scenario]**: [Expected behavior]

## Constraints
- [Technical/business/regulatory constraints]

## Out of Scope
- [Explicitly excluded features or functionality]
```

## Interactive Loop

### Round 1: Initial Analysis
1. Receive initial requirement
2. Analyze for issues
3. Ask 3-5 most critical clarification questions
4. Wait for user responses

### Round 2: Refinement
1. Incorporate user responses
2. Generate enhanced requirement draft
3. Identify remaining ambiguities
4. Ask follow-up questions if needed
5. Wait for user responses

### Round 3: Finalization
1. Incorporate final responses
2. Add domain-specific best practices
3. Complete all sections
4. Present final enhanced requirement
5. Confirm with user

## Quality Checks

Before finalizing, verify:

✓ All critical ambiguities resolved
✓ Functional and non-functional requirements specified
✓ Acceptance criteria are testable
✓ Assumptions explicitly labeled
✓ Edge cases identified
✓ Constraints documented
✓ Priority levels assigned
✓ Original intent preserved

## Examples

For complete before/after examples including:
- User authentication enhancement
- Data export feature enhancement
- Search functionality enhancement

See [examples.md](references/examples.md).

## Tips

- **Start broad**: Ask high-level questions first, then drill down
- **Be specific**: Ask for concrete examples and metrics
- **Avoid leading questions**: Don't suggest answers
- **One topic at a time**: Don't overwhelm with too many questions
- **Confirm understanding**: Paraphrase user responses to verify
- **Preserve intent**: Always check if enhancements align with user goals
- **Label everything**: Make confirmation status explicit
- **Iterate**: Multiple rounds are normal and expected
- **Know when to stop**: Don't over-specify without user input
