---
name: netgraph-dsl
description: >
  NetGraph scenario DSL for defining network topologies, traffic demands, failure policies,
  and analysis workflows in YAML. Use when: creating or editing .yaml/.yml network scenarios,
  defining nodes/links/groups, writing link rules with patterns, configuring selectors or blueprints,
  setting up traffic demands or failure policies, running scenarios and interpreting results,
  debugging DSL syntax or validation errors, or asking about NetGraph scenario structure.
---

# NetGraph DSL

Define network simulation scenarios in YAML format.

> **Quick Start**: See [Minimal Example](#minimal-example) below.
> **Complete Reference**: See [references/REFERENCE.md](references/REFERENCE.md) for full documentation.

## Instructions

When working with NetGraph scenarios:

1. **Creating new scenarios**: Start with the [Minimal Example](#minimal-example), then add sections as needed
2. **Editing existing scenarios**: Identify the relevant section (network, demands, failures, etc.)
3. **Understanding selection**: Review [Selection Models](#selection-models) to understand path-based vs condition-based selection
4. **Debugging issues**: Check [Common Pitfalls](#common-pitfalls) and [Validation Checklist](#validation-checklist)
5. **Complex topologies**: Use [Blueprints](#blueprints) for reusable patterns
6. **Failure simulation**: Define [Risk Groups](#risk-groups) before creating failure policies

Refer to specific sections below for detailed syntax and examples.

## Quick Reference

| Section | Purpose |
|---------|---------|
| `network` | Topology: nodes, links (required) |
| `blueprints` | Reusable topology templates |
| `components` | Hardware library for cost/power modeling |
| `risk_groups` | Failure correlation groups |
| `vars` | YAML anchors for value reuse |
| `demands` | Traffic demand definitions |
| `failures` | Failure simulation rules |
| `workflow` | Analysis execution steps |
| `seed` | Master seed for reproducibility |

## Minimal Example

```yaml
network:
  nodes:
    A: {}
    B: {}
  links:
    - source: A
      target: B
      capacity: 100
      cost: 1
```

## Core Patterns

### Selection Models

The DSL implements two distinct selection patterns:

**1. Path-based Node Selection** (link rules, traffic demands, workflow steps)

- Uses regex patterns on hierarchical node names
- Supports capture group-based grouping
- Supports attribute-based grouping (`group_by`)
- Supports attribute filtering (`match` conditions)
- Supports `active_only` filtering

**2. Condition-based Entity Selection** (failure rules, membership rules, risk group generation)

- Works on nodes/links; failure + membership can also target risk_groups
- Optional regex `path` filter on entity names/IDs (no capture grouping)
- Attribute filtering via `match.conditions` (`match.logic` defaults vary by context)

These patterns share common primitives (condition evaluation, match specification) but serve different purposes and should not be confused.

> **For comprehensive details** on entity creation flows, processing steps, and comparison tables, see the [Entity Creation Architecture](references/REFERENCE.md#entity-creation-architecture) section in the full reference.

### Nodes and Links

```yaml
network:
  nodes:
    Seattle:
      attrs:           # Custom attributes go here
        role: core
      risk_groups: ["RG1"]
      disabled: false
    Portland:
      attrs:
        role: edge

  links:
    - source: Seattle
      target: Portland
      capacity: 100    # Direct properties (no wrapper)
      cost: 10
      attrs:
        distance_km: 280
      count: 2         # Parallel links
```

### Node Groups

```yaml
network:
  nodes:
    leaf:
      count: 4
      template: "leaf-{n}"
      attrs:
        role: leaf
```

Creates: `leaf/leaf-1`, `leaf/leaf-2`, `leaf/leaf-3`, `leaf/leaf-4`

### Template Syntaxes

| Syntax | Example | Context |
|--------|---------|---------|
| `[1-3]` | `dc[1-3]/rack` | Group names, risk groups |
| `$var`/`${var}` | `pod${p}/leaf` | Links, rules, demands |
| `{n}` | `srv-{n}` | `template` field |

These are NOT interchangeable. See [REFERENCE.md](references/REFERENCE.md) for details.

### Bracket Expansion

```yaml
network:
  nodes:
    dc[1-3]/rack[a,b]:    # Cartesian product
      count: 4
      template: "srv-{n}"
```

Creates: `dc1/racka`, `dc1/rackb`, `dc2/racka`, `dc2/rackb`, `dc3/racka`, `dc3/rackb`

**Scope**: Bracket expansion works in group names, risk group definitions (including children), and risk group membership arrays. Component names and other fields treat brackets as literal characters.

### Link Patterns

```yaml
network:
  links:
    - source: /leaf
      target: /spine
      pattern: mesh        # Every source to every target
      capacity: 100

    - source: /group_a     # 4 nodes
      target: /group_b     # 2 nodes
      pattern: one_to_one  # Pairwise with modulo wrap (sizes must have multiple factor)
```

### Selectors with Conditions

```yaml
network:
  links:
    - source:
        path: "/datacenter"
        match:
          logic: and         # "and" or "or"; defaults vary by context (see below)
          conditions:
            - attr: role
              op: "=="
              value: leaf
      target: /spine
      pattern: mesh
```

**Operators**: `==`, `!=`, `<`, `<=`, `>`, `>=`, `contains`, `not_contains`, `in`, `not_in`, `exists`, `not_exists`

**Logic defaults by context (for `match.logic`)**:

| Context | Default `logic` | Rationale |
|---------|-----------------|-----------|
| Link `match` | `"or"` | Inclusive: match any condition |
| Demand `match` | `"or"` | Inclusive: match any condition |
| Membership rules | `"and"` | Precise: must match all conditions |
| Failure rules | `"or"` | Inclusive: match any condition |

### Capturing Groups for Grouping

```yaml
# Single capture group creates groups by captured value
source: "^(dc[1-3])/.*"     # Groups: dc1, dc2, dc3

# Multiple capture groups join with |
source: "^(dc\\d+)/(spine|leaf)/.*"  # Groups: dc1|spine, dc1|leaf, etc.
```

### Variable Expansion

```yaml
links:
  - source: "plane${p}/rack"
    target: "spine${s}"
    expand:
      vars:
        p: [1, 2]
        s: [1, 2, 3]
      mode: cartesian  # or "zip" (equal-length lists required)
    pattern: mesh
```

**Expansion limit**: Maximum 10,000 expansions per template. Exceeding this raises an error.

### Blueprints

```yaml
blueprints:
  clos_pod:
    nodes:
      leaf:
        count: 4
        template: "leaf-{n}"
      spine:
        count: 2
        template: "spine-{n}"
    links:
      - source: /leaf
        target: /spine
        pattern: mesh
        capacity: 100

network:
  nodes:
    pod[1-2]:
      blueprint: clos_pod
      params:
        leaf.count: 6  # Override defaults
```

**Alternative: Inline nested nodes** (no blueprint needed):

```yaml
network:
  nodes:
    datacenter:
      nodes:              # Inline hierarchy
        rack1:
          count: 2
          template: "srv-{n}"
```

### Node and Link Rules

Modify entities after creation with optional attribute filtering:

```yaml
network:
  node_rules:
    - path: "^pod1/.*"
      match:                      # Optional: filter by attributes
        conditions:
          - {attr: role, op: "==", value: compute}
      disabled: true

  link_rules:
    - source: "^pod1/.*"
      target: "^pod2/.*"
      link_match:                 # Optional: filter by link attributes
        conditions:
          - {attr: capacity, op: ">=", value: 400}
      cost: 99
```

Rules also support `expand` for variable-based application.

### Traffic Demands

```yaml
demands:
  production:
    - source: "^dc1/.*"
      target: "^dc2/.*"
      volume: 1000
      mode: pairwise       # or "combine"
      flow_policy: SHORTEST_PATHS_ECMP
```

**Flow policies**: `SHORTEST_PATHS_ECMP`, `SHORTEST_PATHS_WCMP`, `TE_WCMP_UNLIM`, `TE_ECMP_16_LSP`, `TE_ECMP_UP_TO_256_LSP`

### Failure Policies

```yaml
failures:
  single_link:
    expand_groups: false         # Expand to shared-risk entities
    modes:                       # Weighted modes (one selected per iteration)
      - weight: 1.0
        rules:
          - scope: link          # Required: node, link, or risk_group
            mode: choice         # all, choice, or random
            count: 1
            # Optional: weight_by: capacity  # Weighted sampling by attribute
```

**Rule modes**: `all` (select all matches), `choice` (sample `count`), `random` (each with `probability`)

### Risk Groups

Risk groups model failure correlation (shared infrastructure, geographic regions, vendor dependencies, or any custom domain). Three methods:

**Direct definition:**

```yaml
risk_groups:
  - name: "RG1"              # Full form
  - "RG2"                    # String shorthand (equivalent to {name: "RG2"})
```

**Membership rules** (assign entities by attribute matching; optional `path` filter):

```yaml
risk_groups:
  - name: HighCapacityLinks
    membership:
      scope: link            # Required: node, link, or risk_group
      match:
        logic: and           # "and" or "or" (default: "and" for membership)
        conditions:
          - attr: capacity
            op: ">="
            value: 1000
```

**Generate blocks** (create groups from unique attribute values; optional `path` filter):

```yaml
risk_groups:
  - generate:
      scope: node            # Required: node or link only
      path: "^prod_.*"       # Optional: narrow entities before grouping
      group_by: region       # Any attribute to group by
      name: "Region_${value}"
```

**Validation:** Risk group references are validated at load time (undefined references and circular hierarchies detected).

See [REFERENCE.md](references/REFERENCE.md) for complete details.

### Workflow

```yaml
workflow:
  - type: NetworkStats
    name: stats
  - type: MaximumSupportedDemand
    name: msd
    demand_set: production
    alpha_start: 1.0
    resolution: 0.05
  - type: TrafficMatrixPlacement
    name: placement
    demand_set: production
    failure_policy: single_link
    iterations: 1000
    alpha_from_step: msd          # Reference MSD result
    alpha_from_field: data.alpha_star
  - type: MaxFlow
    source: "^(dc[1-3])$"
    target: "^(dc[1-3])$"
    mode: pairwise
    failure_policy: single_link
    iterations: 1000
    seed: 42                      # Optional: for reproducibility
```

**Step types**: `BuildGraph`, `NetworkStats`, `MaxFlow`, `TrafficMatrixPlacement`, `MaximumSupportedDemand`, `CostPower`

## Common Pitfalls

### 1. Custom fields must go in `attrs`

```yaml
# WRONG
nodes:
  A:
    my_field: value    # Error!

# CORRECT
nodes:
  A:
    attrs:
      my_field: value
```

### 2. Link properties are flattened (no wrapper)

```yaml
# WRONG
links:
  - source: A
    target: B
    link_params:       # Error! No wrapper
      capacity: 100

# CORRECT
links:
  - source: A
    target: B
    capacity: 100      # Direct property
```

### 3. `one_to_one` requires compatible sizes

Sizes must have a multiple factor (4-to-2 OK, 3-to-2 ERROR).

### 4. Path patterns are anchored at start

```yaml
path: "leaf"       # Only matches names STARTING with "leaf"
path: ".*leaf.*"   # Matches "leaf" anywhere
```

**Note**: Leading `/` is stripped and has no effect. `/leaf` and `leaf` are equivalent. All paths are relative to the current scope (blueprint instantiation path or network root).

### 5. Variable syntax uses `$` prefix

```yaml
# WRONG (conflicts with regex {m,n})
source: "{dc}/leaf"

# CORRECT
source: "${dc}/leaf"
```

### 6. `zip` requires equal-length lists

```yaml
# WRONG
expand:
  vars:
    a: [1, 2]
    b: [x, y, z]     # Length mismatch!
  mode: zip
```

### 7. Processing order matters

1. Groups and direct nodes created
2. Node rules applied
3. Blueprint links expanded
4. Top-level links expanded (including direct links)
5. Link rules applied

Rules only affect entities that exist at their processing stage.

## Validation Checklist

- [ ] Custom fields inside `attrs`
- [ ] Link properties directly on link (no wrapper)
- [ ] Referenced blueprints exist
- [ ] Node names in direct links exist
- [ ] `one_to_one` sizes have multiple factor
- [ ] `zip` lists have equal length
- [ ] Selectors have at least one of: `path`, `group_by`, `match`

## More Information

- [Full DSL Reference](references/REFERENCE.md) - Complete field documentation, all operators, workflow steps
- [Working Examples](references/EXAMPLES.md) - 22 complete scenarios from simple to advanced

## Running Scenarios

**Always validate before running:**

```bash
./venv/bin/ngraph inspect scenario.yaml && ./venv/bin/ngraph run scenario.yaml
```

### CLI Commands

| Command | Purpose |
|---------|---------|
| `ngraph inspect <file>` | Validate and summarize scenario |
| `ngraph inspect -d <file>` | Detailed view with node/link tables |
| `ngraph run <file>` | Execute and write `<file>.results.json` |
| `ngraph run <file> --stdout` | Execute and print results to stdout |
| `ngraph run <file> --profile` | Execute with CPU profiling |

### Success Indicators

**inspect success:**
```
✓ YAML file loaded successfully
✓ Scenario structure is valid
```

**run success:**
```
✅ Scenario execution completed
✅ Results written to: scenario.results.json
```
Exit code 0, results JSON created.

### Failure Indicators

**Schema validation error:**
```
❌ ERROR: Failed to inspect scenario
  ValidationError: Additional properties are not allowed ('bad_field' was unexpected)
On instance['network']['nodes']['A']:
    {'bad_field': 'x'}
```
Fix: Move custom fields inside `attrs: {}`.

**Missing node reference:**
```
ValueError: Source node 'X' not found in network
```
Fix: Check node name spelling or pattern matching.

**Empty selector match:**
```
WARNING: No nodes matched selector
```
Fix: Verify regex pattern matches actual node names.

### Interpreting Results

Results JSON structure:
```json
{
  "steps": {
    "<step_name>": {
      "metadata": { "duration_sec": 0.5 },
      "data": { ... }
    }
  }
}
```

**Key metrics by step type:**

| Step | Key Field | Good Value | Problem |
|------|-----------|------------|---------|
| MaximumSupportedDemand | `alpha_star` | >= 1.0 | < 1.0 means network undersized |
| TrafficMatrixPlacement | `flow_results[].summary.total_dropped` | 0 | > 0 means congestion |
| MaxFlow | `flow_results[].summary.total_placed` | = total_demand | < demand means bottleneck |

**Quick validation after run:**

```bash
# Check alpha_star (should be >= 1.0)
grep -o '"alpha_star": [0-9.]*' scenario.results.json

# Check for dropped traffic (should be 0)
grep -o '"total_dropped": [0-9.]*' scenario.results.json | head -5
```

### Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Additional properties are not allowed` | Custom field outside `attrs` | Move to `attrs: {field: value}` |
| `Source node 'X' not found` | Link references non-existent node | Fix node name or create the node |
| `one_to_one pattern requires sizes with multiple factor` | Mismatched group sizes | Use sizes like 4-to-2, not 3-to-2 |
| `Variable '$x' not found in expand.vars` | Missing variable definition | Add to `expand: {vars: {x: [...]}}` |
| `zip expansion requires equal-length lists` | Lists have different lengths | Make lists same length or use `cartesian` |

### Profiling Scenarios

When performance matters:

```bash
./venv/bin/ngraph run scenario.yaml --profile --profile-memory
```

Output shows:
- **Step timing**: Time per workflow step
- **Bottlenecks**: Steps taking >10% of total time
- **Memory**: Peak memory per step (with `--profile-memory`)
- **Recommendations**: Optimization suggestions

### Iteration Pattern

1. Write scenario YAML
2. `./venv/bin/ngraph inspect scenario.yaml` - fix any errors
3. `./venv/bin/ngraph run scenario.yaml`
4. Check results: `alpha_star`, `total_dropped`
5. If results bad -> adjust topology/demands -> repeat
