---
name: inquire
description: Request clarification when input is ambiguous. Use when user request has missing parameters, conflicting interpretations, or insufficient constraints for reliable execution.
argument-hint: "[ambiguous_input] [context] [max_questions=3]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
---

## Intent

Generate targeted clarifying questions when a user request is ambiguous or underspecified, enabling the agent to gather missing information before committing to an action.

**Success criteria:**
- Questions target specific missing parameters or ambiguous interpretations
- Each question provides bounded answer options when applicable
- Confidence score reflects actual ambiguity level
- Evidence anchors reference the specific ambiguous elements

**Compatible schemas:**
- `schemas/output_schema.yaml`
- `reference/capability_ontology.yaml#/inquire`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `ambiguous_input` | Yes | string\|object | The underspecified request or goal to clarify |
| `context` | No | object | Previous conversation or domain context for better question generation |
| `max_questions` | No | integer | Maximum clarifying questions to generate (default: 3) |

## Procedure

1) **Analyze the input**: Examine the ambiguous_input for completeness
   - Identify required parameters for the likely intended action
   - Check for conflicting interpretations
   - Note any implicit assumptions that need validation

2) **Categorize ambiguity types**: Classify what's unclear
   - **Missing parameters**: Required information not provided
   - **Conflicting interpretations**: Multiple valid ways to interpret the request
   - **Constraint gaps**: Boundaries or limits not specified
   - **Domain uncertainty**: Unclear which domain or scope applies

3) **Generate clarifying questions**: For each ambiguity, formulate a question
   - Target specific missing information
   - Provide bounded options when possible (2-4 choices)
   - Frame questions to elicit actionable answers
   - Prioritize questions by impact on execution

4) **Ground claims**: Attach evidence anchors to the ambiguity analysis
   - Reference specific phrases or words that are ambiguous
   - Link to context that informed the interpretation
   - Format: `input:phrase`, `context:field`, or `inference:reason`

5) **Format output**: Structure results according to the output contract

6) **Assess confidence**: Rate how confident you are that clarification is needed
   - High confidence (0.8-1.0): Clear missing required parameters
   - Medium confidence (0.5-0.8): Ambiguous but could proceed with assumptions
   - Low confidence (0.0-0.5): Probably clear enough, clarification optional

## Output Contract

Return a structured object:

```yaml
questions:
  - question: "Which database should this operation target?"
    parameter: "target_database"
    options: ["production", "staging", "development"]
  - question: "Should this include archived records?"
    parameter: "include_archived"
    options: ["yes", "no"]
ambiguity_analysis:
  missing_parameters: ["target_database", "date_range"]
  conflicting_interpretations:
    - interpretation: "Query all users"
      confidence: 0.6
    - interpretation: "Query only active users"
      confidence: 0.4
  confidence_without_clarification: 0.3
confidence: 0.85  # How confident we are that clarification is needed
evidence_anchors: ["input:users", "context:previous_query_was_active_only"]
assumptions: []  # No assumptions made - we're asking for clarification
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `questions` | array | Clarifying questions with optional bounded answers |
| `questions[].question` | string | The clarifying question text |
| `questions[].parameter` | string | What parameter this question resolves |
| `questions[].options` | array | Suggested answers if the question has bounded options |
| `ambiguity_analysis` | object | Analysis of what makes the input ambiguous |
| `ambiguity_analysis.missing_parameters` | array | Parameters required but not provided |
| `ambiguity_analysis.conflicting_interpretations` | array | Different valid interpretations |
| `ambiguity_analysis.confidence_without_clarification` | number | How confident we could be if we just guessed |
| `confidence` | number | 0.0-1.0 confidence that clarification is needed |
| `evidence_anchors` | array | References to ambiguous elements |
| `assumptions` | array | Assumptions made (typically empty for inquire) |

## Examples

### Example 1: Ambiguous API Request

**Input:**
```yaml
ambiguous_input: "Update the user's email"
context:
  recent_topic: "user management"
  available_users: 150
max_questions: 3
```

**Output:**
```yaml
questions:
  - question: "Which user's email should be updated?"
    parameter: "user_id"
    options: []  # Open-ended - too many users to list
  - question: "What should the new email address be?"
    parameter: "new_email"
    options: []
  - question: "Should this send a verification email to the new address?"
    parameter: "send_verification"
    options: ["yes", "no", "only if production"]
ambiguity_analysis:
  missing_parameters: ["user_id", "new_email"]
  conflicting_interpretations: []
  confidence_without_clarification: 0.1
confidence: 0.95
evidence_anchors: ["input:the user's", "input:email"]
assumptions: []
```

**Evidence pattern:** The phrase "the user's" indicates a specific user is intended but not identified. "email" is ambiguous - could mean view, update, or verify.

---

### Example 2: Multiple Valid Interpretations

**Input:**
```yaml
ambiguous_input: "Show me the report"
context:
  available_reports: ["sales", "inventory", "user_activity"]
  last_viewed_report: "sales"
max_questions: 2
```

**Output:**
```yaml
questions:
  - question: "Which report would you like to see?"
    parameter: "report_type"
    options: ["sales", "inventory", "user_activity"]
  - question: "For what time period?"
    parameter: "date_range"
    options: ["today", "this week", "this month", "custom range"]
ambiguity_analysis:
  missing_parameters: ["report_type", "date_range"]
  conflicting_interpretations:
    - interpretation: "Show sales report (last viewed)"
      confidence: 0.5
    - interpretation: "Show most recently generated report"
      confidence: 0.3
    - interpretation: "Show all available reports"
      confidence: 0.2
  confidence_without_clarification: 0.5
confidence: 0.7
evidence_anchors: ["input:the report", "context:available_reports:3", "context:last_viewed:sales"]
assumptions: []
```

**Evidence pattern:** "the report" implies a specific report but context shows 3 options. Recent history (sales) provides a weak signal.

## Verification

- [ ] Output contains at least one question when confidence > 0.5
- [ ] Each question has a non-empty `parameter` field
- [ ] Options array is provided for bounded-choice questions
- [ ] Evidence anchors reference specific input elements
- [ ] Confidence is justified by ambiguity analysis

**Verification tools:** None beyond allowed tools

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Do not make assumptions - the purpose is to ask, not to guess
- Limit questions to max_questions to avoid overwhelming users
- If confidence < 0.3, consider returning empty questions (input may be clear enough)
- Never include sensitive data in question options

## Composition Patterns

**Commonly follows:**
- `critique` - After identifying issues with a request, inquire resolves them
- `receive` - After receiving a new request that needs clarification

**Commonly precedes:**
- `receive` - After inquiring, wait for user's clarification response
- `integrate` - Merge clarification into the original request
- `plan` - Once clarified, proceed to planning

**Anti-patterns:**
- Never use `inquire` after `execute` - clarify BEFORE acting
- Avoid chaining multiple `inquire` calls - combine questions into one request
- Don't use with `mutate` in the same step - inquire is read-only

**Workflow references:**
- See `reference/workflow_catalog.yaml#clarify_intent` for the complete clarification workflow
