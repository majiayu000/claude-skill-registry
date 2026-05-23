---
name: world-model-workflow
description: Build a rigorous world model with state, dynamics, uncertainty, and provenance. Use when creating digital twins, constructing system representations, building simulation foundations, or establishing baseline world state.
argument-hint: "[goal] [scope] [constraints]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Bash, Edit, Git, Web
context: fork
agent: general-purpose
---

## Intent

Run the composed workflow **world-model-workflow** using atomic capability skills to construct a comprehensive, grounded representation of a system or domain.

A world model captures:
- **State**: Current entity states and attributes
- **Dynamics**: How the system evolves over time
- **Uncertainty**: Confidence bounds and unknowns
- **Provenance**: Source and lineage of all facts

**Success criteria:**
- Complete entity inventory with identity resolution
- State representation follows canonical schema
- Causal relationships and dynamics modeled
- Uncertainty quantified for all assertions
- Full provenance chain for every fact
- Simulation capability established

**Compatible schemas:**
- `reference/world_state_schema.yaml`
- `reference/event_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `goal` | Yes | string | The modeling objective (e.g., "model supply chain for disruption analysis") |
| `scope` | Yes | string\|array | Domain, system, or entities to model |
| `constraints` | No | object | Limits (e.g., time horizon, resolution, confidence threshold) |
| `sources` | No | array | Data sources for world state extraction |
| `prior_model` | No | object | Existing model to extend or refine |

## Procedure

0) **Create checkpoint marker** if mutation might occur:
   - Create `.claude/checkpoint.ok` after confirming rollback strategy

1) **Invoke `/retrieve`** and store output as `retrieve_out`
   - Gather raw data from configured sources

2) **Invoke `/inspect`** and store output as `inspect_out`
   - Examine retrieved data for structure and quality

3) **Invoke `/identity-resolution`** and store output as `identity-resolution_out`
   - Resolve entity references and establish canonical IDs

4) **Invoke `/world-state`** and store output as `world-state_out`
   - Construct canonical state representation

5) **Invoke `/state-transition`** and store output as `state-transition_out`
   - Define rules for state evolution

6) **Invoke `/causal-model`** and store output as `causal-model_out`
   - Map cause-effect relationships

7) **Invoke `/uncertainty-model`** and store output as `uncertainty-model_out`
   - Quantify confidence and unknowns

8) **Invoke `/provenance`** and store output as `provenance_out`
   - Document source and lineage of all facts

9) **Invoke `/grounding`** and store output as `grounding_out`
   - Attach evidence anchors to assertions

10) **Invoke `/simulation`** and store output as `simulation_out`
    - Validate model through simulation runs

11) **Invoke `/summarize`** and store output as `summarize_out`
    - Generate human-readable model summary

## Output Contract

Return a structured object:

```yaml
workflow_id: string  # Unique model construction ID
goal: string  # Modeling objective
status: completed | partial | failed
world_model:
  version: string
  created_at: string  # ISO timestamp
  schema_version: string
  entities:
    count: integer
    by_type: object  # type -> count
    sample: array[object]  # representative entities
  relationships:
    count: integer
    types: array[string]
    sample: array[object]
  evidence_anchors: array[string]
state:
  snapshot: object  # Canonical world state
  hash: string  # Integrity hash
  timestamp: string
  evidence_anchors: array[string]
dynamics:
  transition_rules: integer
  causal_links: integer
  temporal_scope: string  # e.g., "real-time", "daily", "event-driven"
  evidence_anchors: array[string]
uncertainty:
  overall_confidence: number  # 0.0-1.0
  high_uncertainty_areas: array[string]
  unknown_factors: array[string]
  evidence_anchors: array[string]
provenance:
  sources: array[string]
  lineage_depth: integer
  coverage: number  # 0.0-1.0 (% of facts with provenance)
  evidence_anchors: array[string]
simulation:
  validated: boolean
  scenarios_tested: integer
  anomalies_found: array[string]
  evidence_anchors: array[string]
summary:
  description: string
  key_insights: array[string]
  recommended_actions: array[string]
  evidence_anchors: array[string]
confidence: number  # 0.0-1.0
evidence_anchors: array[string]
assumptions: array[string]
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `workflow_id` | string | Unique identifier for this model construction |
| `world_model` | object | Metadata about entities and relationships |
| `state` | object | Canonical world state snapshot with integrity hash |
| `dynamics` | object | Transition rules and causal structure |
| `uncertainty` | object | Confidence levels and unknown factors |
| `provenance` | object | Source tracking and lineage |
| `simulation` | object | Model validation results |
| `summary` | object | Human-readable insights |
| `confidence` | number | 0.0-1.0 based on evidence completeness |
| `evidence_anchors` | array | All evidence references collected |
| `assumptions` | array | Explicit assumptions made during modeling |

## Examples

### Example 1: Build Supply Chain World Model

**Input:**
```yaml
goal: "Model electronics supply chain for disruption risk analysis"
scope:
  - "suppliers"
  - "manufacturers"
  - "logistics"
  - "inventory"
constraints:
  time_horizon: "6 months"
  geographic_scope: "Asia-Pacific"
  confidence_threshold: 0.7
sources:
  - type: database
    connection: "postgres://supply-chain-db"
  - type: api
    endpoint: "https://logistics.api/shipments"
```

**Output:**
```yaml
workflow_id: "world_20240115_100000_supplychain"
goal: "Model electronics supply chain for disruption risk analysis"
status: completed
world_model:
  version: "v1.0.0"
  created_at: "2024-01-15T10:00:00Z"
  schema_version: "world_state_schema_v2"
  entities:
    count: 1247
    by_type:
      supplier: 156
      manufacturer: 23
      warehouse: 45
      distribution_center: 12
      product: 892
      shipment: 119
    sample:
      - id: "supplier-taiwan-001"
        type: "supplier"
        name: "Taiwan Semiconductor Co"
        location: "Hsinchu, Taiwan"
        capacity: 50000
        lead_time_days: 45
      - id: "mfg-shenzhen-005"
        type: "manufacturer"
        name: "Shenzhen Electronics Assembly"
        location: "Shenzhen, China"
        capacity: 100000
  relationships:
    count: 3456
    types:
      - "supplies_to"
      - "located_in"
      - "transports_via"
      - "stores_at"
      - "depends_on"
    sample:
      - subject: "supplier-taiwan-001"
        predicate: "supplies_to"
        object: "mfg-shenzhen-005"
        attributes:
          volume: 25000
          frequency: "weekly"
  evidence_anchors:
    - "tool:database:supply-chain-db/entities"
    - "tool:api:logistics.api/shipments"
state:
  snapshot:
    timestamp: "2024-01-15T10:00:00Z"
    entities: "[1247 entities - see world_state.yaml]"
    relationships: "[3456 relationships - see world_state.yaml]"
  hash: "sha256:def456abc789..."
  timestamp: "2024-01-15T10:00:00Z"
  evidence_anchors:
    - "file:state/supply_chain_world.yaml"
dynamics:
  transition_rules: 34
  causal_links: 89
  temporal_scope: "daily"
  evidence_anchors:
    - "tool:state-transition:rule_extraction"
    - "tool:causal-model:dependency_graph"
uncertainty:
  overall_confidence: 0.82
  high_uncertainty_areas:
    - "Supplier capacity utilization (estimated from public data)"
    - "Shipping delays (historical average, not real-time)"
  unknown_factors:
    - "Competitor orders affecting supplier allocation"
    - "Regulatory changes in transit countries"
  evidence_anchors:
    - "tool:uncertainty-model:confidence_analysis"
provenance:
  sources:
    - "postgres://supply-chain-db (primary)"
    - "https://logistics.api (secondary)"
    - "public filings (supplementary)"
  lineage_depth: 3
  coverage: 0.94
  evidence_anchors:
    - "tool:provenance:lineage_trace"
simulation:
  validated: true
  scenarios_tested: 5
  anomalies_found:
    - "Taiwan supplier shutdown causes 67% production halt within 2 weeks"
    - "Shipping route disruption adds 12-day average delay"
  evidence_anchors:
    - "tool:simulation:scenario_results"
summary:
  description: "Electronics supply chain model covering 156 suppliers, 23 manufacturers, and supporting logistics infrastructure in Asia-Pacific region"
  key_insights:
    - "Single-source dependency on Taiwan for 45% of semiconductor supply"
    - "Shenzhen manufacturing hub handles 60% of assembly volume"
    - "Average supply chain depth of 3 tiers with limited visibility beyond tier 1"
  recommended_actions:
    - "Diversify semiconductor sourcing to reduce Taiwan concentration risk"
    - "Establish buffer inventory for critical components"
    - "Develop secondary logistics routes for key shipping lanes"
  evidence_anchors:
    - "tool:summarize:executive_summary"
confidence: 0.82
evidence_anchors:
  - "tool:database:supply-chain-db"
  - "tool:api:logistics.api"
  - "tool:simulation:scenario_results"
  - "file:state/supply_chain_world.yaml"
assumptions:
  - "Database reflects current operational state"
  - "API provides accurate shipment tracking"
  - "Public capacity data is within 20% of actual"
  - "Lead times based on historical 90-day average"
```

**Evidence pattern:** Multi-source data integration, entity resolution across databases, causal analysis from transaction patterns, uncertainty from data freshness and coverage.

## Verification

- [ ] **Entity Coverage**: All entities in scope identified with canonical IDs
- [ ] **Relationship Completeness**: Key relationships mapped with evidence
- [ ] **State Validity**: World state conforms to schema
- [ ] **Dynamics Defined**: Transition rules and causal links documented
- [ ] **Uncertainty Quantified**: Confidence scores for all major assertions
- [ ] **Provenance Complete**: Source documented for >90% of facts
- [ ] **Simulation Validated**: At least 1 scenario successfully executed

**Verification tools:** Read (for state files), Bash (for simulation), Web (for API validation)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: medium

**Capability-specific rules:**
- Do not modify source data during modeling
- Flag entities with confidence < threshold
- Document all assumptions explicitly
- Preserve raw data alongside derived state
- Validate schema conformance before completion
- Rate-limit API calls to respect source limits

## Composition Patterns

**Commonly follows:**
- `retrieve` - After gathering raw data
- `receive` - After ingesting real-time signals
- `inspect` - After initial data quality assessment

**Commonly precedes:**
- `digital-twin-sync-workflow` - World model is prerequisite for sync
- `simulate` - To run what-if scenarios
- `forecast-risk` - To predict future states
- `summarize` - To generate executive reports

**Anti-patterns:**
- Never skip identity resolution before state construction
- Never omit uncertainty modeling for production use
- Never finalize without provenance documentation
- Never deploy model without simulation validation

**Workflow references:**
- See `reference/workflow_catalog.yaml#world-model-workflow` for step definitions
- See `reference/world_state_schema.yaml` for canonical state format
