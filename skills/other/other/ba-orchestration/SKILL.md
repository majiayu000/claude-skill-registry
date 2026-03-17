---
name: ba-orchestration
description: Multi-technique business analysis orchestration using BABOK. Coordinates 14 techniques across strategic analysis, problem solving, planning, and design into comprehensive analysis packages.
allowed-tools: Read, Glob, Grep, Skill
---

# Business Analysis Orchestration

Coordinate multiple business analysis techniques into comprehensive analysis packages. Based on BABOK v3 methodology for combining techniques effectively.

## Overview

Business analysis rarely uses a single technique in isolation. Complex initiatives require orchestrated combinations of techniques, sequenced appropriately, with findings synthesized into actionable recommendations.

## Available Techniques (14 Skills)

### Strategic Analysis

| Skill | Purpose |
|-------|---------|
| `swot-pestle-analysis` | SWOT, PESTLE, Porter's Five Forces |
| `business-model-canvas` | BMC, Lean Canvas, 9-block analysis |
| `benchmarking` | Competitive analysis, industry comparison |

### Problem Solving

| Skill | Purpose |
|-------|---------|
| `root-cause-analysis` | Fishbone/Ishikawa, 5 Whys |
| `decision-analysis` | Decision tables, weighted scoring, decision trees |
| `risk-analysis` | Risk registers, probability/impact matrices |

### Planning & Estimation

| Skill | Purpose |
|-------|---------|
| `prioritization` | MoSCoW, Kano model, weighted scoring |
| `estimation` | Analogous, parametric, PERT, story points |
| `capability-mapping` | Business capabilities, maturity models |
| `stakeholder-analysis` | Power/interest, RACI, communication plans |

### Process & Data Design

| Skill | Purpose |
|-------|---------|
| `value-stream-mapping` | Current/future state, Lean analysis |
| `journey-mapping` | Customer experience, touchpoints |
| `process-modeling` | BPMN notation, workflows |
| `data-modeling` | ERDs, data dictionaries |

## Technique Selection Guide

| Goal | Primary Technique | Supporting Techniques |
|------|-------------------|----------------------|
| Strategic planning | SWOT/PESTLE | Capability Mapping, Benchmarking |
| Business model design | Business Model Canvas | Stakeholder Analysis, Value Stream |
| Process improvement | Value Stream Mapping | Root Cause Analysis, Process Modeling |
| Customer experience | Journey Mapping | Stakeholder Analysis, Prioritization |
| Problem investigation | Root Cause Analysis | Risk Analysis, Decision Analysis |
| Technology decision | Decision Analysis | Benchmarking, Risk Analysis |
| Project estimation | Estimation | Prioritization, Risk Analysis |
| Backlog prioritization | Prioritization | Stakeholder Analysis, Estimation |
| Database design | Data Modeling | Process Modeling, Capability Mapping |
| Risk management | Risk Analysis | Prioritization, Stakeholder Analysis |
| Transformation planning | Capability + VSM | SWOT, Stakeholder Analysis |
| New initiative | Full analysis | Multi-technique package |
| M&A due diligence | Capability + Benchmarking | Stakeholder Analysis, Risk |
| Competitive positioning | Benchmarking | SWOT, Business Model Canvas |

## Standard Workflows

### Workflow 1: Strategic Planning

```text
1. Stakeholder Analysis - Identify key stakeholders
2. Capability Mapping - Create capability model
3. Benchmarking - Compare against industry
4. SWOT/PESTLE Analysis - Environmental scan
5. Prioritization - Investment decisions
```

### Workflow 2: Customer Experience Improvement

```text
1. Stakeholder Analysis - Identify user segments
2. Journey Mapping - Map current experience
3. Value Stream Mapping - Identify operational waste
4. Capability Mapping - Link to capabilities
5. Prioritization - Impact vs effort matrix
```

### Workflow 3: Process Optimization

```text
1. Process Modeling - Capture current process (BPMN)
2. Value Stream Mapping - Identify waste and bottlenecks
3. Journey Mapping - User experience perspective
4. Root Cause Analysis - Identify improvement areas
5. Estimation - Plan improvement effort
```

### Workflow 4: Full Analysis Package

```text
1. Stakeholder Analysis - Who is involved?
2. Process Modeling - What happens today?
3. Capability Mapping - What do we do?
4. Value Stream Mapping - How efficiently?
5. Journey Mapping - What's the experience?
6. Synthesis - Integrated findings
```

### Workflow 5: Strategic Assessment

```text
1. SWOT/PESTLE Analysis - Environmental scan
2. Benchmarking - Competitive position
3. Business Model Canvas - Current model
4. Capability Mapping - Internal strengths
5. Gap Analysis - Strategic gaps
6. Prioritization - Strategic initiatives
```

### Workflow 6: Problem Investigation

```text
1. Stakeholder Analysis - Who's affected?
2. Root Cause Analysis - What's causing it?
3. Risk Analysis - What's at risk?
4. Decision Analysis - What are options?
5. Prioritization - Which solution?
6. Estimation - Implementation effort
```

### Workflow 7: New Project Planning

```text
1. Stakeholder Analysis - Who's involved?
2. Risk Analysis - Project risks
3. Estimation - Effort and duration
4. Prioritization - Backlog ordering
5. Process Modeling - Key workflows
6. Data Modeling - Data structures
```

### Workflow 8: Database/System Design

```text
1. Process Modeling - Business workflows
2. Data Modeling - Entity relationships
3. Stakeholder Analysis - Data owners
4. Risk Analysis - Data risks
5. Capability Mapping - System capabilities
```

## Orchestration Process

### Step 1: Understand the Goal

Ask clarifying questions:

- What decision needs to be made?
- Who are the key stakeholders?
- What's the time frame?
- What data/access is available?

### Step 2: Select Workflow

Based on the goal, select the appropriate workflow from above or design a custom sequence.

### Step 3: Execute Techniques

For each technique in the workflow:

1. Load the appropriate skill
2. Gather required inputs
3. Execute the technique
4. Capture outputs

### Step 4: Synthesize Findings

Combine outputs into integrated analysis:

1. **Cross-reference stakeholders** to capability owners
2. **Link pain points** to capabilities and processes
3. **Align improvements** across all techniques
4. **Prioritize recommendations** by impact and feasibility
5. **Create unified roadmap**

## Parallel vs Sequential Execution

### When to Parallelize

Execute techniques in parallel when:

- No data dependencies between them
- Different stakeholders/SMEs provide input
- Time constraints require faster completion

### When to Sequence

Execute techniques sequentially when:

- Output of one feeds into another
- Same stakeholders for both (avoids fatigue)
- Earlier technique shapes scope of later one

### Example Parallel Plan

**Phase 1 (Parallel):**

- Stakeholder Analysis
- Capability Mapping (discovery)

**Phase 2 (Parallel, after Phase 1):**

- Value Stream Mapping (uses stakeholder context)
- Journey Mapping (uses persona from stakeholder analysis)

**Phase 3 (Sequential):**

- Synthesis and Integration

## Output Package Structure

### Integrated Analysis Package

```markdown
## Integrated Business Analysis: [Initiative]

### Executive Summary
[Key findings and recommendations]

### Stakeholder Landscape
[From stakeholder-analysis skill]

### Capability Model
[From capability-mapping skill]

### Value Stream Analysis
[From value-stream-mapping skill]

### Customer Experience
[From journey-mapping skill]

### Integrated Findings
[Cross-cutting insights]

### Prioritized Roadmap
[Unified recommendations]

### Appendix: Detailed Outputs
[Full outputs from each technique]
```

## Quality Checklist

Orchestrated packages must include:

- [ ] Clear problem/goal statement
- [ ] Technique selection rationale
- [ ] Outputs from each technique
- [ ] Cross-referenced findings
- [ ] Integrated recommendations
- [ ] Prioritized roadmap
- [ ] Traceability between deliverables

## Related Skills

- `stakeholder-analysis` - Stakeholder identification and engagement
- `capability-mapping` - Business capability modeling
- `value-stream-mapping` - Lean value stream analysis
- `journey-mapping` - Customer/user experience mapping
- `process-modeling` - BPMN process documentation
- `data-modeling` - Entity-relationship design
- `root-cause-analysis` - Problem investigation
- `swot-pestle-analysis` - Strategic environmental scan
- `business-model-canvas` - Business model design
- `prioritization` - MoSCoW, Kano, weighted scoring
- `risk-analysis` - Risk identification and mitigation
- `decision-analysis` - Decision support techniques
- `estimation` - Effort and duration estimation
- `benchmarking` - Competitive analysis

## Version History

- **v1.0.0** (2026-01-10): Initial release - extracted from ba-orchestrator agent
