---
name: leela-ai
description: "Manufacturing Intelligence — Leela AI develops MOOLLM for practical use and industrial exploration"
license: MIT
tier: 0
allowed-tools: [read_file, list_dir]
protocol: LEELA-AI
related: [moollm, manufacturing-intelligence, society-of-mind, k-lines, schema-mechanism, constructionism, simulator-effect, speed-of-light, representation-ethics, yaml-jazz]
tags: [moollm, meta, company, manufacturing, industrial, neural-symbolic, drescher]
---

# Leela AI Skill

> *Manufacturing Intelligence -- from theory to industrial application.*

## Overview

This skill describes Leela AI's relationship to MOOLLM. Leela develops MOOLLM with an eye toward manufacturing intelligence, using it daily for practical devops, edgebox management, coding, debugging, and design work. The team is exploring how the theoretical foundations of Minsky, Papert, and Drescher might eventually deploy on factory floors.

## Leela and Gary Drescher

Leela's foundations lie in Gary Drescher's work at MIT under Marvin Minsky and Seymour Papert. Drescher brought Jean Piaget's developmental psychology into computing: infants learn through sensorimotor experience and build *schemas* (context → action → result). Henry Minsky was exposed to this as a student; years later he reimplemented Drescher's algorithms and, with Cyrus Shaoul and Milan Minsky, founded Leela AI. The name *Leela* is Sanskrit for divine play — the play of creation, destruction, and re-creation.

Key points:

- **Schema mechanism**: Leela builds models of the world using schemas that reason about which actions are possible and what changes when an action is performed. Goals are achieved by chaining schemas (planner finds actions whose results match the goal).
- **Self-supervised learning**: Leela learns from exploratory actions without labeled examples or explicit reward; it forms and tests hypotheses. In multi-goal grid-world experiments (Kommrusch et al., IWSSL 2020), Leela reached training targets in ~160N² steps vs DQN ~360N^2.7, and does not suffer catastrophic forgetting.
- **Neurosymbolic extension**: Later work (Symbolic Guidance for Constructivist Learning, Neurosymbolic Learning on Video Data, Society of LLMs) combines the symbolic schema system with neural perception (object/pose detection, cortical columns, multi-LLM instances). *Society of LLMs* (Kommrusch & Minsky, IWSSL 2024) maps Drescher's schema mechanism onto multi-agent LLMs: curiosity-driven goals, multiple plans, training samples when plans differ and one succeeds, contextual sub-activation (one agent "thinking subconsciously"), and incremental LoRA updates; evaluation target ARC-AGI. Leela Core uses the hybrid for manufacturing video intelligence — causal reasoning and explainability on top of ConvNets.

See: [schema-mechanism/](../schema-mechanism/), [reference/drescher-lineage.yml](reference/drescher-lineage.yml), [reference/publications.yml](reference/publications.yml), [reference/society-of-llms.yml](reference/society-of-llms.yml).

## Core Technology

### Neural-Symbolic Vision

Traditional computer vision is pattern matching. Leela's neural-symbolic system is *causal reasoning*.

```yaml
neural_symbolic:
  layer_1: neural
    - object detection (what is there?)
    - pose estimation (how is it positioned?)
    - motion tracking (where is it going?)
    
  layer_2: symbolic
    - context inference (what situation is this?)
    - causal reasoning (why is this happening?)
    - SQL queries over temporal event database
    - prediction (what will happen next?)
    - explanation (human-readable "why")
    
  layer_3: pda  # LLM interface layer
    - generate: natural language → SQL
    - perform: execute queries
    - interpret: results → meaning
    - explain: causation in plain language
    - visualize: charts, timelines, maps
    - remember: query history, preferences
```

The neural layer provides perception. The symbolic layer provides reasoning. The PDA layer provides natural language interface -- neural at the surface, symbolic in the protocol.

### Schema Mechanism (Drescher)

Every inference follows Drescher's schema pattern:

```yaml
schema:
  context: [observable conditions]
  action: [event that occurred]
  result: [observed outcome]
  
  learning:
    marginal_attribution: 
      - which context features predict result?
    synthetic_items:
      - inferred entities not directly observed
    generalization:
      - when does this schema apply elsewhere?
```

### Edge Computing Architecture

Intelligence at the edge, not in the cloud:

```yaml
edge_architecture:
  edgebox:
    location: factory floor
    latency: <50ms
    capabilities: [inference, alerting, logging]
    
  cloud:
    purpose: training, aggregation, analytics
    latency: acceptable for non-real-time
    
  principle: |
    Real-time decisions happen at the edge.
    Learning and optimization happen in the cloud.
    Data sovereignty stays with the customer.
```

## Applications

### 1. Safety Monitoring

```yaml
safety_monitoring:
  purpose: Prevent accidents through predictive awareness
  
  examples:
    - pedestrian_in_vehicle_zone
    - ppe_compliance (hard hats, vests, glasses)
    - ergonomic_risk (repetitive motion, lifting posture)
    - near_miss_detection (close calls before accidents)
    
  output:
    alert: real-time notification
    explanation: why this is a safety concern
    recommendation: suggested action
    audit: logged for compliance
```

### 2. Process Optimization

```yaml
process_optimization:
  purpose: Improve efficiency through observation and inference
  
  examples:
    - cycle_time_analysis
    - bottleneck_detection
    - idle_time_measurement
    - workflow_optimization
    
  output:
    insight: what is happening
    causation: why it is happening
    recommendation: how to improve
    simulation: what-if scenarios
```

### 3. Predictive Maintenance

```yaml
predictive_maintenance:
  purpose: Fix equipment before it fails
  
  signals:
    visual: vibration patterns, wear indicators, alignment
    thermal: heat signatures indicating friction or failure
    acoustic: sound patterns indicating mechanical issues
    
  schema:
    context: [equipment state, operational history]
    action: [detected anomaly]
    result: [predicted failure mode]
    
  output:
    prediction: what will fail, when
    explanation: why we predict this
    recommendation: maintenance action
    confidence: certainty level
```

### 4. DevOps Automation

```yaml
devops:
  purpose: Apply MOOLLM patterns to infrastructure
  
  patterns:
    files_as_state:
      - infrastructure as code
      - git as audit trail
      - YAML as configuration
      
    coherence_engine:
      - detect configuration drift
      - propose remediation
      - explain changes
      
    speed_of_light:
      - batch operations
      - parallel deployment
      - minimal round-trips
```

## MOOLLM Integration

### Rooms as Zones

```yaml
# Factory zone as MOOLLM room
zone:
  id: assembly_line_3
  type: [production, monitored, indoor]
  
  contains:
    - equipment: [robot_arm_1, conveyor_2, station_7]
    - personnel: [operator_badge_1234]
    - cameras: [cam_3a, cam_3b, cam_3c]
    
  exits:
    - to: staging_area
    - to: quality_check
    
  atmosphere:
    safety_status: green
    production_status: active
    alert_level: none
```

### Characters as Entities

```yaml
# Forklift as MOOLLM character
entity:
  id: forklift_07
  type: [vehicle, autonomous, tracked]
  
  location: loading_dock_2
  state: stationary
  
  current_task: awaiting_clearance
  
  relationships:
    operator: badge_5678
    cargo: pallet_1234
    
  needs:
    fuel: 0.73
    maintenance: 0.15  # due soon
```

### Skills as Inference Rules

```yaml
# Safety protocol as MOOLLM skill
skill:
  id: pedestrian-safety
  
  activation:
    context: pedestrian detected in vehicle zone
    
  action:
    - alert vehicle operators
    - log safety event
    - track pedestrian until zone-clear
    
  advertisement:
    provides: pedestrian-zone-monitoring
    satisfies: [safety, compliance, awareness]
```

## The Team

| Team Member | Role | Background |
|-------------|------|------------|
| **Henry Minsky** | CTO | MIT AI Lab, NTT DoCoMo, Google Nest. Marvin Minsky's son. |
| **Dr. Cyrus Shaoul** | Chief Evangelist | Computational neuroscientist, Digital Garage co-founder/CTO |
| **Dr. Milan Singh Minsky** | VP Product | Venture-backed startups, RayVio co-founder |
| **Sheung Li** | VP Applications | Machine vision in manufacturing |
| **Dr. Steve Kommrusch** | Senior AI Research Scientist | Deep learning, AMD/HP/National Semiconductor |
| **Don Hopkins** | AI Architect | The Sims, NeWS, pie menus, MOOLLM |

The theory meets the practice. Minsky's ideas, refined through Hopkins's implementation experience and Kommrusch's deep learning expertise, deployed on factory floors.

## Ethical Framework

### Transparency

```yaml
transparency:
  principle: Every inference is explainable
  
  implementation:
    - causal_chains: visible in audit log
    - confidence_levels: always reported
    - uncertainty: acknowledged, not hidden
    - limitations: documented
```

### Privacy

```yaml
privacy:
  principle: Data sovereignty and minimal collection
  
  implementation:
    - edge_processing: data stays local when possible
    - anonymization: faces pixelated by default
    - retention: minimal, configurable
    - consent: clear signage, worker awareness
```

### Human Agency

```yaml
human_agency:
  principle: AI advises, humans decide
  
  implementation:
    - critical_decisions: require human approval
    - recommendations: clearly labeled as suggestions
    - override: always possible
    - accountability: human remains responsible
```

## Integration Points

| System | Integration |
|--------|-------------|
| **SCADA** | Sensor data ingestion |
| **MES** | Production event correlation |
| **ERP** | Business context enrichment |
| **CMMS** | Maintenance recommendation routing |
| **Safety Systems** | Alert escalation |

## Deployment Model

```yaml
deployment:
  edge:
    edgeboxes: industrial compute at the source
    latency: <50ms for real-time inference
    resilience: operates offline if cloud disconnected
    
  cloud:
    platform: customer choice (AWS, GCP, Azure, on-prem)
    purpose: training, aggregation, dashboard
    sovereignty: customer owns their data
    
  hybrid:
    edge_to_cloud: telemetry, events, learning data
    cloud_to_edge: model updates, configuration
```

## References

- Drescher, G. (1991). *Made-Up Minds.* MIT Press.
- Minsky, M. (1985). *Society of Mind.* Simon & Schuster.
- Kommrusch et al. (2020). Self-Supervised Learning for Multi-Goal Grid World: Comparing Leela and Deep Q Network. IWSSL, PMLR 131.
- [MOOLLM Skills](../README.md)
- [Schema Mechanism](../schema-mechanism/)
- [reference/publications.yml](reference/publications.yml) — papers and case study
- [leela.ai](https://leela.ai)
