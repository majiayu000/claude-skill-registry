# Planning Skill

planning
OVERVIEW
actor: {{actor}} | mandate: {{mandate}} | bounds: {{bounds}}

ORIENTATION
Confirm .spec/constitution.md for current architecture and delivery guardrails.
Review .spec/glossary.md entries relevant to planning to keep terminology aligned.
Load the {{actor}} persona brief from .spec/agents/{{actor}}.agent.md for format expectations.

LIFECYCLE TRANSITION
from: {{from_state}} ➜ to: {{to_state}}
ACCEPTS_FROM: [{{accepts_from}}]
tag: [{{planning_type}}.planning] (append to story ## Lifecycle Log)

WHEN TO RUN
{{trigger_scenario_1}}
{{trigger_scenario_2}}
{{trigger_scenario_3}}
{{trigger_scenario_4}}

REQUIRED INPUTS
story_id
{{planning_context}} (context and requirements for planning)
{{planning_resources}} (available resources and constraints)
{{planning_dependencies}} (dependencies and considerations)
MCP tooling: [{{mcp_tools}}]

CONTEXT PACK
<<story.current_state>>
<<personas.active_assignments>>
<<recent_transition_log>>
<<<GLOSSARY(term={{planning_type}}_planning)>>>

EXECUTION ALGORITHM
Validate prerequisites ({{planning_context}}, {{planning_resources}}). If anything missing → BLOCKED format below.
Collect evidence: resource assessments, dependency analysis, stakeholder inputs.
{{planning_analysis_steps}}
Document planning decisions with rationale and trade-offs.
Identify and document all planning risks and mitigation approaches.
Draft gate artifact using the structure in ARTIFACT OUTPUT.
Append the TRANSITION LOG entry to the story's ## Lifecycle Log, matching persona tone.
Update glossary/constitution if new terminology or workflows were introduced.

ARTIFACT OUTPUT
=== {{Planning_Type}} Plan ===
summary:<concise summary of planning decisions and outcomes>
inputs:{{planning_context}}=<ref> {{planning_resources}}=<ref> {{planning_dependencies}}=<ref>
evidence:{{planning_validation}}|result=<validated/pending>|ref=<path_to_plan>
risks:[ ]<risk_description>|owner=<persona>|mitigation=<action>
next_steps:<follow-up needed or n/a>
=== END {{Planning_Type}} Plan ===

TRANSITION LOG TEMPLATE
[TRANSITION|{{planning_type}}.planning] by {{actor}}
MODE: strict|tolerant|branch
FROM_STATE: {{from_state}}
TO_STATE: {{to_state}}
WHY:
- {{planning_reason_1}}
- {{planning_reason_2}}
OUTPUT:
=== {{Planning_Type}} Plan ===
summary:{{planning_summary}}
inputs:{{planning_context}}=refs=planning/context.md {{planning_resources}}=docs/resources.csv
evidence:{{planning_validation}}|result=validated|ref=plans/{{planning_type}}-plan-{{date}}.md
risks:[ ]{{planning_risk}}|owner={{actor}}|mitigation={{planning_mitigation}}
next_steps:{{planning_next_steps}}
=== END {{Planning_Type}} Plan ===
FOLLOW-UP:
- {{planning_followup_action}} - owner={{actor}} - due={{date}}

BLOCKED FORMAT
BLOCKED(missing_inputs=[{{planning_context}}, {{planning_resources}}], unblock_steps=[{{unblock_step_1}}, {{unblock_step_2}}])

GUARDRAILS
Keep entries <=120 chars per line for CLI readability.
{{planning_guardrail_1}}
{{planning_guardrail_2}}
{{planning_guardrail_3}}
Update .spec/glossary.md if you introduce new terms, channels, or artifacts.

---

# Planning Templates

## Template Selection Mechanism

Agents can specify planning type in two ways:
1. **Skill Specification**: Use `planning` skill with `planning_type` parameter
2. **Intent Interpretation**: System determines planning type from context and agent role

### Usage Examples
```bash
# Direct template specification
exec story=PROJECT-001 skill=planning planning_type=agile

# System interpretation based on agent and context
exec story=PROJECT-001 skill=planning  # architect agent → architect-planning template
```

## Template Definitions

### 1. Agile Planning Template
**Intended for**: product-ops agent
**When to use**: Backlog sequencing, capacity allocation, sprint planning
**Parameters**:
- planning_type: agile
- actor: product-ops
- mandate: Sequence backlog and allocate capacity
- bounds: No technical implementation decisions
- from_state: PRD_READY
- to_state: PLANNED
- accepts_from: [product-prd]
- planning_context: requirements (from product-prd)
- planning_resources: team_capacity (available resources and skills)
- planning_dependencies: dependencies (technical and business dependencies)
- mcp_tools: [Read, Write]
- planning_analysis_steps: |
  Sequence backlog items based on business value and dependencies.
  Allocate capacity across team members with skill matching.
  Define sprint/iteration boundaries with realistic timelines.
  Identify and document all blocking dependencies.
- planning_validation: capacity_plan
- planning_guardrail_1: Timeline estimates must include buffer for unexpected delays.
- planning_guardrail_2: All dependencies must have identified owners and resolution timelines.
- planning_guardrail_3: Resource allocation must match team skill sets and availability.

### 2. Architect Planning Template
**Intended for**: architect agent
**When to use**: System architecture, technical decisions, NFR definition
**Parameters**:
- planning_type: architect
- actor: architect
- mandate: Define system architecture and technical approach
- bounds: No code implementation
- from_state: ANY
- to_state: PLANNED
- accepts_from: []
- planning_context: requirements (business and technical requirements)
- planning_resources: constraints (technical, business, compliance constraints)
- planning_dependencies: quality_targets (performance, security, scalability NFRs)
- mcp_tools: [Read, Write, WebSearch]
- planning_analysis_steps: |
  Define system architecture with clear component boundaries.
  Specify technology choices with rationale and trade-offs.
  Define measurable NFR targets with validation criteria.
  Identify architectural risks with mitigation strategies.
- planning_validation: design_review
- planning_guardrail_1: All NFR targets must be measurable with specific validation methods.
- planning_guardrail_2: Technology choices must include clear rationale and trade-off analysis.
- planning_guardrail_3: Architecture decisions must consider scalability and maintenance.

### 3. Testing Planning Template
**Intended for**: qa agent
**When to use**: Test strategy, environment setup, quality planning
**Parameters**:
- planning_type: testing
- actor: qa
- mandate: Design comprehensive testing strategy and quality plan
- bounds: No test execution
- from_state: REVIEWED
- to_state: READY
- accepts_from: [code-review]
- planning_context: test_requirements (testing scope and criteria)
- planning_resources: environment_specifications (test environment needs)
- planning_dependencies: reviewed_code (from code-review)
- mcp_tools: [Read, Write, Bash]
- planning_analysis_steps: |
  Design comprehensive test strategy for all quality dimensions.
  Plan test environment setup and configuration requirements.
  Define test data management and fixture requirements.
  Establish quality gates and acceptance criteria.
- planning_validation: test_strategy
- planning_guardrail_1: Test environment must be isolated from production systems.
- planning_guardrail_2: All test fixtures must be version controlled and documented.
- planning_guardrail_3: Quality gates must be measurable and verifiable.

### 4. Implementation Planning Template
**Intended for**: tech-lead agent
**When to use**: Technical implementation, task breakdown, resource coordination
**Parameters**:
- planning_type: implementation
- actor: tech-lead
- mandate: Coordinate technical implementation and resource planning
- bounds: No code changes
- from_state: PLANNED
- to_state: BUILT
- accepts_from: [agile-planning, architect-plan]
- planning_context: architecture_plan (from architect-plan)
- planning_resources: development_resources (team allocation and skills)
- planning_dependencies: implementation_requirements (from agile-planning)
- mcp_tools: [Read, Write, Bash]
- planning_analysis_steps: |
  Break down architecture plan into implementable tasks.
  Allocate development resources based on skills and availability.
  Define integration points and technical dependencies.
  Establish implementation milestones and validation criteria.
- planning_validation: implementation_plan
- planning_guardrail_1: Implementation tasks must be atomic and testable.
- planning_guardrail_2: Resource allocation must consider skill dependencies.
- planning_guardrail_3: Integration points must be clearly defined and validated.

## Template Selection Logic

### Automatic Intent Interpretation
When `planning_type` is not specified, the system determines the appropriate template based on:

1. **Agent Role**: Each agent has a default planning template
   - product-ops → agile-planning
   - architect → architect-planning
   - qa → testing-planning
   - tech-lead → implementation-planning

2. **Current State**: The task state suggests appropriate planning type
   - PRD_READY → agile-planning (product-ops)
   - DRAFT/ANY → architect-planning (architect)
   - REVIEWED → testing-planning (qa)
   - PLANNED → implementation-planning (tech-lead)

3. **Context Analysis**: Available inputs and required outputs
   - requirements + team_capacity → agile-planning
   - requirements + constraints → architect-planning
   - test_requirements + environment_specs → testing-planning
   - architecture_plan + development_resources → implementation-planning

### Parameter Override
Agents can explicitly specify planning parameters:
```bash
exec story=PROJECT-001 skill=planning planning_type=testing actor=qa
```

This allows cross-agent planning when needed, maintaining flexibility while providing sensible defaults.

---

*Unified Planning skill supporting multiple planning domains with template-driven execution and intent interpretation.*