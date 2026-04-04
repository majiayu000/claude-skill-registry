# Research Skill

research
OVERVIEW
actor: {{actor}} | mandate: Conduct systematic investigation and analysis | bounds: Research and analysis only

ORIENTATION
Confirm .spec/constitution.md for current architecture and delivery guardrails.
Review .spec/glossary.md entries relevant to research to keep terminology aligned.
Load the {{actor}} persona brief from .spec/agents/{{actor}}.agent.md for format expectations.

LIFECYCLE TRANSITION
from: ANY ➜ to: SAME
ACCEPTS_FROM: []
tag: [research] (append to story ## Lifecycle Log)

WHEN TO RUN
Research investigations needed for decision making
Hypotheses need validation with quantitative/qualitative data
{{research_domain}} patterns and constraints require analysis
{{research_domain}} research or competitive analysis needed
Best practices investigation required for implementation

REQUIRED INPUTS
story_id
research_type ({{research_types}} - includes product-discovery)
research_questions (specific questions to answer)
research_context (decision requirements or problems)
{{research_domain_inputs}}
MCP tooling: [WebSearch, WebFetch, Read]

CONTEXT PACK
<<story.current_state>>
<<personas.active_assignments>>
<<recent_transition_log>>
<<<GLOSSARY(term=research)>>>

EXECUTION ALGORITHM
Validate prerequisites (research_type, research_questions, research_context). If anything missing → BLOCKED format below.
Collect evidence based on research type:
{{research_mode_evidence}}
Execute analysis methodology appropriate to research type:
{{research_mode_analysis}}
Generate insights and recommendations based on findings.
Document research methodology and evidence sources.
Provide actionable recommendations for decision-making.
Draft gate artifact using the structure in ARTIFACT OUTPUT.
Append the TRANSITION LOG entry to the story's ## Lifecycle Log, matching persona tone.
Update glossary/constitution if new terminology or workflows were introduced.

ARTIFACT OUTPUT
=== Research Summary ===
summary:<concise summary of research findings and recommendations>
inputs:research_type=<type> research_questions=<ref> research_context=<ref>
evidence:<analysis_type>|result=<validated/supported/identified>|ref=<path_to_research>
risks:[ ]<risk_description>|owner=<persona>|mitigation=<action>
next_steps:<follow-up needed or n/a>
=== END Research Summary ===

TRANSITION LOG TEMPLATE
[TRANSITION|research] by {{actor}}
MODE: tolerant
FROM_STATE: <current_state>
TO_STATE: SAME
WHY:
- Research investigation required for informed decision making
- {{research_type}} analysis needed to answer critical questions
OUTPUT:
=== Research Summary ===
summary:Conducted {{research_type}} research and provided evidence-based recommendations.
inputs:research_type={{research_type}} research_questions=docs/questions.md research_context=decision-context.pdf
evidence:{{research_evidence_type}}|result=hypothesis_supported|ref=research/{{research_type}}-report-{{date}}.pdf
risks:[ ]{{research_risk}}|owner={{actor}}|mitigation={{research_mitigation}}
next_steps:Proceed with implementation using validated research findings.
=== END Research Summary ===
FOLLOW-UP:
- Apply research findings - owner={{actor}} - due={{date}}

BLOCKED FORMAT
BLOCKED(missing_inputs=[research_questions, research_context], unblock_steps=[define_questions, clarify_context])

GUARDRAILS
Keep entries <=120 chars per line for CLI readability.
All findings must be supported by evidence and appropriate citations.
Research methodology must be clearly documented and reproducible.
Limitations and assumptions must be explicitly stated.
{{research_domain_guardrails}}
Conflicting information must be acknowledged and resolved.
Update .spec/glossary.md if you introduce new terms, channels, or artifacts.

---

# Research Templates

## Template Selection Mechanism

Agents can specify research type in two ways:
1. **Skill Specification**: Use `research` skill with `research_type` parameter
2. **Intent Interpretation**: System determines research type from context and questions

### Usage Examples
```bash
# Direct template specification
exec story=PROJECT-001 skill=research research_type=analytics

# System interpretation based on questions and context
exec story=PROJECT-001 skill=research  # Analyzes research_questions to determine type
```

## Template Definitions

### 1. Analytics Research Template
**Intended for**: Any agent with data-driven questions
**When to use**: Hypothesis validation, metrics analysis, quantitative insights
**Parameters**:
- research_type: analytics
- actor: {{actor}} (flexible based on context)
- research_types: analytics/technical/market/competitive
- research_domain_inputs: data_sources (available data and analytics)
- research_mode_evidence: |
  Analytics: data sources, analytics reports, metrics
- research_mode_analysis: |
  Analytics: Statistical analysis, hypothesis testing, data validation
- research_evidence_type: customer_analysis
- research_risk: Data quality limitations
- research_mitigation: additional_data_collection
- research_domain_guardrails: Data sources must be clearly identified and validated.

**Additional Required Inputs**:
- data_sources: Available data and analytics
- analysis_requirements: Specific analysis methods and metrics

**Evidence Type**: data_analysis with statistical validation
**Output Focus**: Quantitative insights, metrics validation, hypothesis testing

### 2. Technical Research Template
**Intended for**: architect, tech-lead agents
**When to use**: Technology evaluation, feasibility studies, best practices
**Parameters**:
- research_type: technical
- actor: {{actor}} (typically architect or tech-lead)
- research_domain_inputs: research_topics (specific areas to investigate)
- research_mode_evidence: |
  Technical: documentation, specifications, case studies
- research_mode_analysis: |
  Technical: Pattern analysis, constraint evaluation, feasibility assessment
- research_evidence_type: technical_findings
- research_risk: Technical feasibility uncertainty
- research_mitigation: prototype_development
- research_domain_guardrails: Technical assumptions must be validated through proof of concepts.

**Additional Required Inputs**:
- research_topics: Specific technical areas to investigate
- technical_constraints: Known technical limitations and requirements

**Evidence Type**: findings with technical documentation
**Output Focus**: Technical patterns, constraints, feasibility assessment

### 3. Market Research Template
**Intended for**: product-ops agent
**When to use**: Market analysis, opportunity sizing, trend identification
**Parameters**:
- research_type: market
- actor: {{actor}} (typically product-ops)
- research_domain_inputs: market_scope (target market segments)
- research_mode_evidence: |
  Market: market reports, competitive analysis, trends
- research_mode_analysis: |
  Market: Trend analysis, opportunity sizing, gap identification
- research_evidence_type: market_analysis
- research_risk: Market data availability limitations
- research_mitigation: expand_research_sources
- research_domain_guardrails: Market assumptions must be validated with multiple sources.

**Additional Required Inputs**:
- market_scope: Target market segments and geography
- competitive_landscape: Known competitors and market dynamics

**Evidence Type**: market_analysis with trend identification
**Output Focus**: Market insights, opportunity sizing, trend analysis

### 4. Competitive Research Template
**Intended for**: product-ops, architect agents
**When to use**: Competitive analysis, positioning, differentiation
**Parameters**:
- research_type: competitive
- actor: {{actor}} (typically product-ops or architect)
- research_domain_inputs: competitor_list (known competitors to analyze)
- research_mode_evidence: |
  Competitive: competitor products, positioning, analysis
- research_mode_analysis: |
  Competitive: Feature comparison, positioning analysis, SWOT assessment
- research_evidence_type: competitive_analysis
- research_risk: Incomplete competitive landscape
- research_mitigation: broaden_competitor_search
- research_domain_guardrails: Competitive data must be current and from reliable sources.

**Additional Required Inputs**:
- competitor_list: Specific competitors to analyze
- analysis_criteria: Comparison framework and evaluation metrics

**Evidence Type**: competitive_analysis with feature comparison
**Output Focus**: Competitive insights, positioning, differentiation opportunities

### 5. Product Discovery Template
**Intended for**: product-ops agent
**When to use**: Problem validation, market need confirmation, customer pain point analysis
**Parameters**:
- research_type: product-discovery
- actor: {{actor}} (typically product-ops)
- research_domain_inputs: customer_interviews (customer interview notes, recordings)
- research_mode_evidence: |
  Product Discovery: customer interviews, market research, competitive analysis
- research_mode_analysis: |
  Product Discovery: Problem validation, market sizing, customer pain quantification
- research_evidence_type: validation_survey
- research_risk: Market size validation uncertainty
- research_mitigation: expand_research_segments
- research_domain_guardrails: Problem statement must be validated with at least 3 different customer sources.

**Additional Required Inputs**:
- customer_interviews: Customer interview notes, recordings, transcripts
- market_analysis: Competitive landscape, market sizing data
- stakeholder_requirements: Initial stakeholder inputs and requirements

**Evidence Type**: validation_survey with quantitative evidence
**Output Focus**: Problem validation findings, market need confirmation, customer pain quantification

**Special State Transition**:
- from_state: DRAFT
- to_state: PRD_READY
- tag: product.discovery

## Template Selection Logic

### Automatic Intent Interpretation
When `research_type` is not specified, the system determines the appropriate template based on:

1. **Question Analysis**: Keywords in research_questions suggest research type
   - "validate", "measure", "quantify", "metrics" → analytics
   - "feasibility", "implementation", "technical", "architecture" → technical
   - "market", "customers", "opportunity", "sizing" → market
   - "competitors", "comparison", "positioning", "differentiation" → competitive
   - "problem", "pain points", "need", "validation", "discovery" → product-discovery

2. **Agent Role**: Each agent has default research preferences
   - product-ops → market, competitive, or product-discovery research
   - architect → technical research
   - tech-lead → technical research
   - qa → analytics or technical research

3. **Available Inputs**: Context and additional inputs indicate type
   - data_sources available → analytics
   - research_topics specified → technical
   - market_scope defined → market
   - competitor_list provided → competitive
   - customer_interviews available → product-discovery

4. **Context Clues**: Task domain and current gate suggest appropriate research
   - Discovery phase → product-discovery, market, or competitive research
   - Architecture phase → technical research
   - Implementation phase → technical or analytics research
   - Testing phase → analytics research

### Parameter Override
Agents can explicitly specify research parameters:
```bash
exec story=PROJECT-001 skill=research research_type=competitive actor=product-ops
```

### Multi-Mode Research
Complex research can span multiple modes:
```bash
exec story=PROJECT-001 skill=research research_type="market+competitive"
```

The system will execute multiple research modes and consolidate findings.

---

*Unified Research skill supporting multiple research methodologies with template-driven execution and intent interpretation.*