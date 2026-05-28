---
name: nl-router
description: Route natural language requests to appropriate skills and workflows. Use when relevant to the task.
---

# nl-router

Route natural language requests to appropriate skills and workflows.

## Triggers

This skill is the meta-router - it processes natural language and routes to other skills. It should be consulted when no explicit skill trigger is matched.

## Purpose

This skill interprets natural language requests and routes them to the appropriate skills or workflows by:
- Parsing user intent from natural language
- Matching to available skills and commands
- Handling ambiguous requests with clarification
- Suggesting relevant actions
- Learning from routing patterns

## Behavior

When triggered, this skill:

1. **Parses user intent**:
   - Extract action verbs
   - Identify objects/targets
   - Detect qualifiers and constraints
   - Recognize context from conversation

2. **Matches to skills**:
   - Search skill trigger patterns
   - Score match confidence
   - Consider context relevance

3. **Routes request**:
   - High confidence: Route directly
   - Medium confidence: Confirm with user
   - Low confidence: Offer options
   - No match: Suggest alternatives

4. **Handles follow-ups**:
   - Track routing context
   - Enable corrections
   - Learn from feedback

## Routing Patterns

### SDLC Workflows

```yaml
sdlc_patterns:
  phase_transitions:
    patterns:
      - "transition to {phase}"
      - "move to {phase}"
      - "start {phase}"
      - "begin {phase}"
      - "ready for {phase}"
    routes_to: flow-{from}-to-{to}
    extract: [from_phase, to_phase]

  gate_checks:
    patterns:
      - "check gate"
      - "can we transition"
      - "ready for {phase}"
      - "validate {gate}"
      - "gate check"
    routes_to: gate-evaluation
    extract: [gate_name, phase]

  project_status:
    patterns:
      - "where are we"
      - "what's next"
      - "project status"
      - "current phase"
      - "status update"
    routes_to: project-awareness
    action: status_report

  risk_management:
    patterns:
      - "update risks"
      - "risk review"
      - "new risk"
      - "mitigate {risk}"
    routes_to: risk-cycle
    extract: [risk_id, action]

  security_review:
    patterns:
      - "security review"
      - "run security"
      - "threat model"
      - "security scan"
    routes_to: security-assessment
    extract: [scope]
```

### Artifact Operations

```yaml
artifact_patterns:
  create:
    patterns:
      - "create {artifact}"
      - "generate {artifact}"
      - "new {artifact}"
      - "draft {artifact}"
    routes_to: artifact-orchestration
    extract: [artifact_type]

  review:
    patterns:
      - "review {artifact}"
      - "check {artifact}"
      - "validate {artifact}"
    routes_to: artifact_type_specific_review
    extract: [artifact_type]

  trace:
    patterns:
      - "trace {requirement}"
      - "what implements {id}"
      - "coverage for {id}"
    routes_to: traceability-check
    extract: [requirement_id]
```

### Marketing Workflows

```yaml
marketing_patterns:
  brand_review:
    patterns:
      - "brand review"
      - "check brand compliance"
      - "is this on-brand"
      - "brand audit"
    routes_to: brand-compliance
    extract: [asset_path]

  approval:
    patterns:
      - "submit for approval"
      - "approval workflow"
      - "get sign-off"
      - "approval status"
    routes_to: approval-workflow
    extract: [asset_id]

  performance:
    patterns:
      - "how are we doing"
      - "marketing report"
      - "performance summary"
      - "campaign results"
    routes_to: performance-digest
    extract: [period, channel]

  competitive:
    patterns:
      - "competitor analysis"
      - "what are competitors doing"
      - "competitive landscape"
    routes_to: competitive-intel
    extract: [competitor_name]
```

### Utility Operations

```yaml
utility_patterns:
  decision:
    patterns:
      - "help me decide"
      - "compare options"
      - "trade-off analysis"
      - "which should I choose"
    routes_to: decision-support
    extract: [decision_topic]

  test_coverage:
    patterns:
      - "test coverage"
      - "what's not tested"
      - "coverage report"
    routes_to: test-coverage
    extract: [scope]

  incident:
    patterns:
      - "production issue"
      - "system down"
      - "incident"
      - "P0"
      - "SEV1"
    routes_to: incident-triage
    priority: urgent

  config:
    patterns:
      - "validate config"
      - "check setup"
      - "config issues"
    routes_to: config-validator
```

## Intent Classification

### Action Verbs

```yaml
action_verbs:
  create:
    words: [create, generate, new, draft, make, build, write]
    intent: creation

  review:
    words: [review, check, validate, verify, audit, assess]
    intent: validation

  update:
    words: [update, change, modify, edit, revise]
    intent: modification

  delete:
    words: [delete, remove, deprecate, archive]
    intent: removal

  analyze:
    words: [analyze, understand, explain, investigate, explore]
    intent: analysis

  transition:
    words: [transition, move, progress, advance, start, begin]
    intent: workflow_progression

  compare:
    words: [compare, contrast, versus, vs, trade-off]
    intent: comparison
```

### Object Mappings

```yaml
object_mappings:
  artifacts:
    sad: software-architecture-document
    adr: architecture-decision-record
    test_plan: test-plan
    requirements: software-requirements-spec
    threat_model: threat-model

  phases:
    inception: inception
    elaboration: elaboration
    construction: construction
    transition: transition
    production: production

  gates:
    lom: lifecycle-objective-milestone
    abm: architecture-baseline-milestone
    ioc: initial-operational-capability
    prm: product-release-milestone
```

## Confidence Scoring

```yaml
confidence_levels:
  high:
    threshold: 0.85
    action: route_directly
    example: "create SAD" → artifact-orchestration (SAD)

  medium:
    threshold: 0.60
    action: confirm_before_routing
    example: "review this" → "Did you mean brand review or code review?"

  low:
    threshold: 0.40
    action: offer_options
    example: "help" → "Here are things I can help with..."

  none:
    threshold: 0.0
    action: clarify
    example: "do the thing" → "I'm not sure what you'd like to do. Can you clarify?"
```

## Routing Response Format

### Direct Route (High Confidence)

```yaml
routing_response:
  confidence: high
  matched_skill: artifact-orchestration
  extracted_params:
    artifact_type: sad
  message: "Creating Software Architecture Document..."
  next_action: invoke_skill
```

### Confirmation Route (Medium Confidence)

```yaml
routing_response:
  confidence: medium
  candidates:
    - skill: brand-compliance
      confidence: 0.72
      reason: "brand" keyword matched
    - skill: code-reviewer
      confidence: 0.65
      reason: "review" action detected
  message: "I found multiple possible actions. Did you mean..."
  next_action: await_clarification
```

### Options Route (Low Confidence)

```yaml
routing_response:
  confidence: low
  suggestions:
    - category: Documentation
      actions: [create SAD, generate ADR, draft requirements]
    - category: Review
      actions: [brand review, code review, security review]
    - category: Status
      actions: [project status, coverage report, risk review]
  message: "I'm not sure what you'd like to do. Here are some options..."
  next_action: await_selection
```

## Usage Examples

### Clear Intent

```
User: "Generate the architecture document"

Skill routes:
- Intent: create
- Object: architecture document → SAD
- Confidence: 0.95 (high)

Output:
"Routing to artifact-orchestration to generate Software Architecture Document.

Starting SAD generation..."

[Invokes artifact-orchestration with artifact_type=sad]
```

### Ambiguous Intent

```
User: "Review the landing page"

Skill analyzes:
- Intent: review
- Object: landing page
- Possible skills: brand-compliance, qa-protocol, code-reviewer
- Confidence: 0.65 (medium)

Output:
"I found a few review options for 'landing page':

1. **Brand Review** - Check brand compliance
2. **QA Review** - Check quality and specs
3. **Content Review** - Check copy and messaging

Which would you like?"
```

### Unclear Intent

```
User: "Help with the project"

Skill analyzes:
- Intent: unclear
- Object: project (generic)
- Confidence: 0.30 (low)

Output:
"I can help with many things! Here are some common actions:

**Project Status**
- Where are we? → Project status
- What's next? → Phase recommendations

**Documentation**
- Create SAD → Architecture document
- Generate ADR → Decision record

**Reviews**
- Security review → Threat assessment
- Brand review → Compliance check

What would you like to do?"
```

### Contextual Routing

```
User: (After discussing a bug) "Create a ticket for this"

Skill analyzes:
- Context: Bug discussion
- Intent: create
- Object: ticket
- Inference: incident or defect ticket
- Confidence: 0.80 (high with context)

Output:
"Based on our discussion, I'll create an incident ticket for the authentication issue.

Routing to incident-triage..."
```

## Integration

This skill is the central router and integrates with all other skills:
- All SDLC skills
- All MMK skills
- All utility skills
- All workflow commands

## Configuration

### Custom Patterns

Add custom routing patterns in `.aiwg/config/routing.yaml`:

```yaml
custom_patterns:
  - trigger: "standup update"
    routes_to: project-awareness
    action: standup_summary

  - trigger: "weekly report"
    routes_to: performance-digest
    params:
      period: weekly
```

### Priority Overrides

```yaml
priority_overrides:
  # Urgent patterns always match first
  urgent:
    - "production down"
    - "SEV1"
    - "security breach"

  # Exact matches before fuzzy
  exact_first: true

  # Prefer skill in current context
  context_boost: 0.15
```

## Output Locations

- Routing logs: `.aiwg/logs/routing/`
- Pattern analytics: `.aiwg/analytics/routing-patterns.json`

## References

- Skill catalog: Available skills from all frameworks
- Command catalog: Available workflow commands
- Translation table: docs/simple-language-translations.md
