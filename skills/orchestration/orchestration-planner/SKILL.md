---
name: Orchestration Planner
description: Plan multi-step workflows using capability graph and Codex-powered goal decomposition with HTN-style hierarchical task planning.
version: 1.0.0
category: ai-native
tags:
  - codex
  - planning
  - orchestration
  - htn
---

# Orchestration Planner

**Plan multi-step workflows using capability graph and Codex-powered goal decomposition**

## Purpose

Takes high-level goals and decomposes them into executable workflows using the capability graph. Uses Codex to understand goal semantics, find matching capabilities, validate preconditions, and generate Hierarchical Task Network (HTN) plans with alternatives and scoring.

## When to Use

- Converting user goals into executable plans (e.g., "build RAG system")
- Finding optimal capability sequences for complex tasks
- Validating that project state supports a capability
- Generating alternatives when primary path is blocked
- Explaining why certain capabilities are recommended

## Key Capabilities

- **Goal Decomposition**: Uses Codex to break goals into required effects
- **Capability Matching**: Finds capabilities that produce desired effects
- **Precondition Validation**: Checks if current project state satisfies requirements
- **HTN Planning**: Builds hierarchical task networks with subtasks
- **Scoring & Ranking**: Evaluates paths by cost, latency, risk, diversity
- **Alternative Generation**: Provides fallback options when primary path fails
- **Decision Logging**: Captures rationale for capability selection

## Inputs

```yaml
inputs:
  goal: string # User goal (e.g., "implement RAG")
  project_state: object # Current project state (files, dependencies, env vars)
  capability_graph: string # Path to capability-graph.json
  preferences: object # User preferences (cost_weight, risk_tolerance, etc.)
  context: array # Recently used capabilities (for cooldown)
```

## Process

### Step 1: Goal Analysis with Codex

```bash
# Use Codex to understand goal and extract required effects
codex exec "
Analyze this goal and determine what effects are needed:

GOAL: ${USER_GOAL}

Examples of effects:
- creates_vector_index
- adds_auth_middleware
- configures_database
- implements_api_endpoint
- adds_tests

Task: Extract the effects needed to achieve this goal.

Output JSON:
{
  \"goal\": \"original goal\",
  \"required_effects\": [\"effect1\", \"effect2\"],
  \"optional_effects\": [\"effect3\"],
  \"domains\": [\"rag\", \"api\"],
  \"reasoning\": \"explanation\"
}
" > /tmp/goal-analysis.json
```

### Step 2: Find Candidate Capabilities

```bash
# Query capability graph for matching capabilities
python3 <<EOF
import json

# Load goal analysis
with open('/tmp/goal-analysis.json') as f:
    goal_analysis = json.load(f)

# Load capability graph
with open('META/capability-graph.json') as f:
    graph_data = json.load(f)
    graph = graph_data['graph']

# Find capabilities by effect
candidates = []
for effect in goal_analysis['required_effects']:
    if effect in graph['effects']:
        for capability in graph['effects'][effect]:
            # Get full capability data
            node = next((n for n in graph['nodes'] if n['id'] == capability), None)
            if node:
                candidates.append({
                    'capability': capability,
                    'effect': effect,
                    'required': True,
                    'node': node
                })

# Find optional capabilities
for effect in goal_analysis.get('optional_effects', []):
    if effect in graph['effects']:
        for capability in graph['effects'][effect]:
            node = next((n for n in graph['nodes'] if n['id'] == capability), None)
            if node and capability not in [c['capability'] for c in candidates]:
                candidates.append({
                    'capability': capability,
                    'effect': effect,
                    'required': False,
                    'node': node
                })

# Write candidates
with open('/tmp/candidates.json', 'w') as f:
    json.dump(candidates, f, indent=2)
EOF
```

### Step 3: Validate Preconditions

```bash
# For each candidate, check if preconditions are satisfied
python3 <<EOF
import json
import os
import subprocess

# Load candidates
with open('/tmp/candidates.json') as f:
    candidates = json.load(f)

# Load project state
with open('/tmp/project-state.json') as f:
    project_state = json.load(f)

def evaluate_precondition(check, project_state):
    """Evaluate a precondition check against project state"""
    # Handle file_exists('path')
    if check.startswith('file_exists('):
        path = check[12:-2]  # Extract path from function call
        return os.path.exists(path)

    # Handle not file_exists('path')
    if check.startswith('not file_exists('):
        path = check[16:-2]
        return not os.path.exists(path)

    # Handle has_dependency('package')
    if check.startswith('has_dependency('):
        package = check[15:-2]
        return package in project_state.get('dependencies', {})

    # Handle env_var_set('VAR')
    if check.startswith('env_var_set('):
        var = check[12:-2]
        return var in project_state.get('env_vars', {})

    # Handle OR conditions
    if ' or ' in check:
        parts = check.split(' or ')
        return any(evaluate_precondition(p.strip(), project_state) for p in parts)

    # Handle AND conditions
    if ' and ' in check:
        parts = check.split(' and ')
        return all(evaluate_precondition(p.strip(), project_state) for p in parts)

    # Unknown check type
    return False

# Validate each candidate
for candidate in candidates:
    node = candidate['node']
    preconditions = node.get('preconditions', [])

    satisfied = []
    unsatisfied = []

    for precond in preconditions:
        check = precond['check']
        required = precond.get('required', True)
        result = evaluate_precondition(check, project_state)

        if result:
            satisfied.append(precond)
        else:
            unsatisfied.append(precond)
            if required:
                candidate['blocked'] = True
                candidate['missing_precondition'] = precond

    candidate['satisfied_preconditions'] = satisfied
    candidate['unsatisfied_preconditions'] = unsatisfied

# Write validated candidates
with open('/tmp/candidates-validated.json', 'w') as f:
    json.dump(candidates, f, indent=2)
EOF
```

### Step 4: Build HTN Plan with Codex

```bash
# Use Codex to build hierarchical task network
CANDIDATES=$(cat /tmp/candidates-validated.json)
GRAPH=$(cat META/capability-graph.json)

codex exec "
Build a hierarchical task network (HTN) plan to achieve this goal.

GOAL:
$(cat /tmp/goal-analysis.json)

AVAILABLE CAPABILITIES:
$CANDIDATES

CAPABILITY GRAPH:
$GRAPH

Task: Create an HTN plan with ordered steps, alternatives, and dependencies.

HTN Structure:
{
  \"goal\": \"original goal\",
  \"plan\": [
    {
      \"step\": 1,
      \"capability\": \"capability-name\",
      \"effect\": \"what this achieves\",
      \"required\": true,
      \"blocked\": false,
      \"alternatives\": [\"alt-capability-1\", \"alt-capability-2\"],
      \"dependencies\": [\"step-0\"],
      \"reasoning\": \"why this capability\"
    }
  ],
  \"total_cost\": \"medium\",
  \"total_latency\": \"slow\",
  \"max_risk\": \"low\",
  \"parallel_steps\": [[1, 2], [3, 4]]
}

Instructions:
1. Order capabilities by dependencies (requires/enables)
2. For each capability, list alternatives with similar effects
3. Mark parallel-executable steps
4. Validate each step's preconditions
5. Calculate aggregate cost/latency/risk
6. Explain reasoning for each choice

Output ONLY valid JSON.
" > /tmp/htn-plan.json
```

### Step 5: Score and Rank Plans

```bash
# Score plan using utility function
python3 <<EOF
import json

with open('/tmp/htn-plan.json') as f:
    plan = json.load(f)

# Scoring weights (configurable by user preferences)
COST_WEIGHT = 0.3
LATENCY_WEIGHT = 0.2
RISK_WEIGHT = 0.3
DIVERSITY_WEIGHT = 0.2

# Map qualitative values to scores
cost_scores = {'free': 1.0, 'low': 0.8, 'medium': 0.5, 'high': 0.2}
latency_scores = {'instant': 1.0, 'fast': 0.7, 'slow': 0.3}
risk_scores = {'safe': 1.0, 'low': 0.8, 'medium': 0.5, 'high': 0.2, 'critical': 0.0}

# Calculate scores
cost_score = cost_scores.get(plan['total_cost'], 0.5)
latency_score = latency_scores.get(plan['total_latency'], 0.5)
risk_score = risk_scores.get(plan['max_risk'], 0.5)

# Diversity bonus (using different domains/kinds)
capabilities = [step['capability'] for step in plan['plan']]
unique_domains = len(set([cap.split('-')[0] for cap in capabilities]))
diversity_score = min(unique_domains / 5.0, 1.0)

# Total utility
utility = (
    cost_score * COST_WEIGHT +
    latency_score * LATENCY_WEIGHT +
    risk_score * RISK_WEIGHT +
    diversity_score * DIVERSITY_WEIGHT
)

plan['scores'] = {
    'utility': utility,
    'cost_score': cost_score,
    'latency_score': latency_score,
    'risk_score': risk_score,
    'diversity_score': diversity_score
}

# Write scored plan
with open('/tmp/plan-scored.json', 'w') as f:
    json.dump(plan, f, indent=2)

print(f"Plan utility score: {utility:.2f}")
EOF
```

### Step 6: Generate Decision Log

```bash
# Create explainable decision log
cat > /tmp/decision-log.json <<EOF
{
  "goal": "$(jq -r .goal /tmp/goal-analysis.json)",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "selected_plan": $(cat /tmp/plan-scored.json),
  "alternatives_considered": [
    {
      "capability": "alternative-1",
      "reason_rejected": "Higher cost",
      "score": 0.65
    }
  ],
  "precondition_checks": $(cat /tmp/candidates-validated.json),
  "reasoning": "Selected capabilities optimizing for low risk and moderate cost"
}
EOF
```

## Scoring Function

```javascript
function scoreCapability(capability, context) {
  // Base scores from manifest
  const costScores = { free: 1.0, low: 0.8, medium: 0.5, high: 0.2 }
  const latencyScores = { instant: 1.0, fast: 0.7, slow: 0.3 }
  const riskScores = { safe: 1.0, low: 0.8, medium: 0.5, high: 0.2, critical: 0.0 }

  let score = 0
  score += costScores[capability.cost] * context.costWeight
  score += latencyScores[capability.latency] * context.latencyWeight
  score += riskScores[capability.risk_level] * context.riskWeight

  // Diversity bonus: prefer capabilities from underrepresented domains
  const domainCount = context.usedDomains[capability.domains[0]] || 0
  const diversityBonus = 1.0 / (1 + domainCount)
  score += diversityBonus * context.diversityWeight

  // Cooldown penalty: reduce score for recently used capabilities
  const lastUsed = context.recentlyUsed[capability.name]
  if (lastUsed) {
    const stepsSince = context.currentStep - lastUsed
    if (stepsSince < 3) {
      score *= 0.7 // 30% penalty
    }
  }

  // Novelty bonus: prefer capabilities not yet used in this plan
  if (!context.usedCapabilities.has(capability.name)) {
    score *= 1.2 // 20% bonus
  }

  return score
}
```

## Example Output

```json
{
  "goal": "Build RAG system for documentation search",
  "plan": [
    {
      "step": 1,
      "capability": "openai-integration",
      "effect": "enables_embedding_generation",
      "required": true,
      "blocked": false,
      "alternatives": ["anthropic-integration", "local-embeddings"],
      "dependencies": [],
      "reasoning": "Provides embeddings API for vector generation",
      "preconditions_met": true
    },
    {
      "step": 2,
      "capability": "pinecone-mcp",
      "effect": "creates_vector_index",
      "required": true,
      "blocked": false,
      "alternatives": ["weaviate-mcp", "qdrant-mcp"],
      "dependencies": [1],
      "reasoning": "Managed vector database with low latency",
      "preconditions_met": true
    },
    {
      "step": 3,
      "capability": "rag-implementer",
      "effect": "configures_retrieval_pipeline",
      "required": true,
      "blocked": false,
      "alternatives": [],
      "dependencies": [1, 2],
      "reasoning": "Orchestrates embedding + retrieval workflow",
      "preconditions_met": true
    }
  ],
  "total_cost": "medium",
  "total_latency": "slow",
  "max_risk": "low",
  "parallel_steps": [[1, 2]],
  "scores": {
    "utility": 0.78,
    "cost_score": 0.65,
    "latency_score": 0.7,
    "risk_score": 0.8,
    "diversity_score": 0.8
  }
}
```

## Integration

### With capability-graph-builder

Queries the capability graph to find matching capabilities and relationships.

### With manifest-generator

Uses manifest metadata (preconditions, effects, cost, latency, risk) for planning.

### With Repository Brain

Will integrate into `scripts/brain/plan` command for interactive planning.

## Success Metrics

- ✅ Plans correctly decompose 90%+ of test goals
- ✅ Precondition validation catches incompatible capabilities
- ✅ Alternative generation provides 2+ options per step
- ✅ Decision logs are explainable and traceable
- ✅ Scoring function produces reasonable rankings

## Related Skills

- capability-graph-builder: Provides queryable graph
- manifest-generator: Provides capability metadata
- system-diagnostician: Uses planner for recommendations
