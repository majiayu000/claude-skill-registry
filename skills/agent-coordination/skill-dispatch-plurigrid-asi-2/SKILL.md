---
name: skill-dispatch
description: ' GF(3) Triadic Task Routing for Subagent Orchestration'
---

# skill-dispatch

> GF(3) Triadic Task Routing for Subagent Orchestration

**Version**: 1.0.0  
**Trit**: 0 (Ergodic - coordinates routing)  
**Bundle**: core  

## Overview

Skill-dispatch routes tasks to appropriate skills based on GF(3) triadic conservation. Each task is assigned to a triad of skills (MINUS/ERGODIC/PLUS) that sum to 0 mod 3, ensuring balanced execution.

## Core Concept

```
Task → Infer Bundle → Select Triad → Dispatch to Subagents

Each triad: (-1) ⊗ (0) ⊗ (+1) = 0 mod 3
```

## Skill Registry

```ruby
SKILLS = {
  # MINUS (-1): Validators
  'sheaf-cohomology'    => { trit: -1, bundle: :cohomological, action: :verify },
  'three-match'         => { trit: -1, bundle: :core, action: :reduce },
  'clj-kondo-3color'    => { trit: -1, bundle: :database, action: :lint },
  'influence-propagation' => { trit: -1, bundle: :network, action: :validate },
  
  # ERGODIC (0): Coordinators
  'unworld'             => { trit: 0, bundle: :core, action: :derive },
  'acsets'              => { trit: 0, bundle: :database, action: :query },
  'cognitive-surrogate' => { trit: 0, bundle: :learning, action: :predict },
  'entropy-sequencer'   => { trit: 0, bundle: :core, action: :arrange },
  
  # PLUS (+1): Generators
  'gay-mcp'             => { trit: 1, bundle: :core, action: :color },
  'agent-o-rama'        => { trit: 1, bundle: :learning, action: :train },
  'atproto-ingest'      => { trit: 1, bundle: :acquisition, action: :fetch },
  'triad-interleave'    => { trit: 1, bundle: :core, action: :interleave }
}
```

## Canonical Triads

```ruby
TRIADS = {
  core:        %w[three-match unworld gay-mcp],
  database:    %w[clj-kondo-3color acsets rama-gay-clojure],
  learning:    %w[self-validation-loop cognitive-surrogate agent-o-rama],
  network:     %w[influence-propagation bisimulation-game atproto-ingest],
  repl:        %w[slime-lisp borkdude cider-clojure]
}
```

## Capabilities

### 1. dispatch

Route a task to the appropriate triad.

```python
from skill_dispatch import Dispatcher

dispatcher = Dispatcher(seed=0xf061ebbc2ca74d78)

assignment = dispatcher.dispatch(
    task="analyze interaction patterns",
    bundle="learning"  # optional, inferred if not provided
)

# Returns:
# {
#   task: "analyze interaction patterns",
#   bundle: "learning",
#   triad: ["self-validation-loop", "cognitive-surrogate", "agent-o-rama"],
#   assignments: [
#     {skill: "self-validation-loop", trit: -1, role: "validator"},
#     {skill: "cognitive-surrogate", trit: 0, role: "coordinator"},
#     {skill: "agent-o-rama", trit: 1, role: "generator"}
#   ],
#   gf3_sum: 0,
#   conserved: true
# }
```

### 2. execute-triad

Execute a full triad pipeline: MINUS → ERGODIC → PLUS.

```python
result = dispatcher.execute_triad(
    bundle="core",
    input_data=raw_interactions,
    executor=lambda skill, data, info: skill.run(data)
)

# Pipeline: three-match → unworld → gay-mcp
# Each step's output feeds into the next
```

### 3. cross-compose

Compose skills across different bundles while maintaining GF(3).

```python
hybrid = dispatcher.cross_compose(
    minus_bundle="database",    # clj-kondo-3color
    ergodic_bundle="learning",  # cognitive-surrogate
    plus_bundle="core"          # gay-mcp
)

# Still conserves: (-1) + (0) + (+1) = 0
```

### 4. infer-bundle

Automatically determine bundle from task description.

```python
bundle = dispatcher.infer_bundle("lint the clojure code")
# Returns: "database" (matches kondo pattern)

bundle = dispatcher.infer_bundle("train a predictor")
# Returns: "learning"
```

## Subagent Roles

```python
ROLES = {
    -1: {
        "name": "validator",
        "color": "#2626D8",  # Blue
        "verbs": ["verify", "constrain", "reduce", "filter", "lint"]
    },
    0: {
        "name": "coordinator", 
        "color": "#26D826",  # Green
        "verbs": ["transport", "derive", "navigate", "bridge", "arrange"]
    },
    1: {
        "name": "generator",
        "color": "#D82626",  # Red
        "verbs": ["create", "compose", "generate", "expand", "train"]
    }
}
```

## DuckDB Integration

```sql
CREATE TABLE dispatch_log (
    dispatch_id VARCHAR PRIMARY KEY,
    task VARCHAR,
    bundle VARCHAR,
    triad VARCHAR[],
    gf3_sum INT,
    conserved BOOLEAN,
    seed BIGINT,
    dispatched_at TIMESTAMP
);

-- Verify all dispatches conserve GF(3)
SELECT COUNT(*) as violations
FROM dispatch_log
WHERE NOT conserved;
-- Should always be 0
```

## Configuration

```yaml
# skill-dispatch.yaml
dispatcher:
  seed: 0xf061ebbc2ca74d78
  default_bundle: core
  strict_conservation: true

bundles:
  core: [three-match, unworld, gay-mcp]
  learning: [self-validation-loop, cognitive-surrogate, agent-o-rama]
  network: [influence-propagation, bisimulation-game, atproto-ingest]

inference:
  patterns:
    - pattern: "lint|kondo|clojure"
      bundle: database
    - pattern: "train|learn|predict"
      bundle: learning
    - pattern: "network|influence|propagat"
      bundle: network
```

## Justfile Recipes

```makefile
# Dispatch a task
dispatch task="analyze" bundle="core":
    ruby lib/skill_dispatch.rb dispatch "{{task}}" "{{bundle}}"

# Execute full triad
execute-triad bundle="learning" input="data.json":
    ruby lib/skill_dispatch.rb execute "{{bundle}}" "{{input}}"

# Verify all triads conserve GF(3)
verify-triads:
    ruby lib/skill_dispatch.rb verify
```

## Example Workflow

```bash
# 1. Dispatch a learning task
just dispatch "train cognitive model" learning

# 2. Execute the triad
just execute-triad learning interactions.json

# 3. Verify conservation
just verify-triads
# Output:
# core: three-match ⊗ unworld ⊗ gay-mcp = 0 ✓
# learning: self-validation-loop ⊗ cognitive-surrogate ⊗ agent-o-rama = 0 ✓
# network: influence-propagation ⊗ bisimulation-game ⊗ atproto-ingest = 0 ✓
```

## Related Skills

- `gay-mcp` - Provides deterministic seeding
- `triad-interleave` - Interleaves dispatched tasks
- `tripartite_dispatcher.rb` - Reference implementation
