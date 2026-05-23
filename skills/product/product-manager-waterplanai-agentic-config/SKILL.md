---
name: product-manager
description: "Decomposes large features into concrete development phases with DAG dependencies. Each phase produces fully functional code. Outputs YAML manifest. Triggers on keywords: decompose feature, phase planning, roadmap breakdown, feature phases, PM decomposition, split feature"
project-agnostic: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Product Manager - Phase Decomposition

Decomposes large features/bugs/chores into concrete, self-contained development phases.

## Core Principles

1. **Self-Contained Phases**: Each phase produces fully functional code (even if partial to overall goal)
2. **Incremental Value**: Every phase delivers testable, deployable value
3. **Clear Boundaries**: Phases have explicit inputs, outputs, and acceptance criteria
4. **DAG Dependencies**: Phases form a directed acyclic graph - parallel where possible

## Input Analysis

When given a feature/prompt/spec:

1. **Read input thoroughly** - Understand full scope
2. **Identify atomic units** - Find smallest deployable pieces
3. **Map dependencies** - What must exist before what
4. **Group logically** - Combine related atoms into phases
5. **Validate DAG** - Ensure no circular dependencies

## Phase Decomposition Rules

### Phase Sizing
- **Too small**: Single file change, trivial addition
- **Just right**: 1-3 related components, clear acceptance criteria, testable
- **Too large**: Multiple unrelated concerns, can't be tested independently

### Feature Complexity Assessment

Assess overall feature complexity to guide phase count and mux-ospec modifier selection:

| Feature Complexity | Typical Phases | Default Phase Modifier |
|-------------------|----------------|------------------------|
| Simple            | 1-2            | lean or leanest        |
| Medium            | 2-4            | lean or normal         |
| Complex           | 4-8            | normal or full         |
| Very Complex      | 8+             | full (critical phases) |

### Phase Independence
Each phase MUST:
- Have clear entry point (what exists before)
- Produce working code (no broken intermediate states)
- Be testable in isolation
- Have explicit acceptance criteria

### Dependency Types
- `hard`: Phase cannot start until dependency completes
- `soft`: Phase benefits from dependency but can proceed with stubs

## Output Format

### Complexity to mux-ospec Mapping

When generating `o_spec_config` for each phase, use this mapping:

| estimated_complexity | o_spec_config.modifier | o_spec_config.skip |
|---------------------|------------------------|-------------------|
| trivial             | leanest                | ["TEST", "DOCUMENT"] |
| low                 | leanest                | [] |
| medium              | lean                   | [] |
| high                | normal                 | [] |
| critical            | full                   | [] |

The `o_spec_config.model` field is optional; leave null unless specific model override is needed for the phase.

### Phase Bundling Rules

Bundling reduces orchestration overhead by combining related phases into single `/mux-ospec` cycles.

#### Complexity Scores (for bundle size limits)

| estimated_complexity | score | bundleable |
|---------------------|-------|------------|
| trivial             | 1     | yes        |
| low                 | 2     | yes        |
| medium              | 3     | yes        |
| high                | N/A   | no (standalone) |
| critical            | N/A   | no (standalone) |

#### Bundling Criteria

Phases CAN be bundled when ALL conditions are met:
1. **Complexity ceiling**: Only trivial, low, medium phases (high/critical stay standalone)
2. **DAG alignment**: Same `execution_order` batch (no cross-dependency bundling)
3. **Size limits**: Max 5 phases AND cumulative score <= 10 per bundle
4. **Semantic cohesion**: Related functionality (shared concern/component)

#### Semantic Similarity Heuristics

Cluster bundleable phases by:
- **Title prefix**: Common prefix indicates shared concern (e.g., "Auth: models", "Auth: endpoints")
- **Scope overlap**: Shared file paths or component names
- **Description keywords**: API, database, UI, models as group markers

#### Bundle Configuration Aggregation

For bundled phases, compute aggregate `bundle_config`:
- `modifier`: MAX(phase modifiers) - leanest < lean < normal < full
- `skip`: INTERSECTION(phase skips) - if any phase needs a stage, bundle runs it
- `model`: First non-null model, or null

#### Bundling Algorithm

```
FOR each batch in execution_order:
  1. Separate high/critical phases as standalone
  2. FOR remaining trivial/low/medium phases:
     a. Cluster by semantic similarity (title prefix, scope overlap)
     b. FOR each cluster:
        - While cumulative_score <= 10 AND phase_count <= 5: add phase
        - Assign bundle_id to grouped phases
  3. Generate bundle entries with aggregated config
```

Generate manifest at: `outputs/phases/{timestamp}-{feature-slug}/manifest.yml`

```yaml
# Phase Manifest
# Generated by product-manager skill

meta:
  feature: "Feature title"
  description: "Brief description of overall goal"
  created_at: "ISO timestamp"
  total_phases: N
  estimated_complexity: "low|medium|high|very_high"

phases:
  - id: "phase-1"
    title: "Short descriptive title"
    description: |
      What this phase accomplishes.
      Why it's a logical unit.
    scope:
      - "Specific deliverable 1"
      - "Specific deliverable 2"
    acceptance_criteria:
      - "Testable criterion 1"
      - "Testable criterion 2"
    dependencies: []  # or ["phase-id"]
    dependency_type: null  # or "hard"|"soft"
    spec_prompt: |
      Inline prompt for /mux-ospec to execute this phase.
      Include specific technical requirements.
    o_spec_config:
      modifier: "lean"      # full | normal | lean | leanest (derived from estimated_complexity)
      model: null           # opus | sonnet | haiku (optional override)
      skip: []              # list of stages to skip, e.g., ["TEST", "DOCUMENT"]
    estimated_complexity: "trivial|low|medium|high|critical"
    bundle_id: null         # Set by bundling algorithm; null = standalone execution

  - id: "phase-2"
    title: "..."
    dependencies: ["phase-1"]
    dependency_type: "hard"
    # ... rest of fields

execution_order:
  # Computed from DAG - phases that can run in parallel grouped together
  - parallel: ["phase-1", "phase-3"]  # No dependencies, run together
  - sequential: ["phase-2"]            # Depends on phase-1
  - parallel: ["phase-4", "phase-5"]   # Both depend on phase-2

validation:
  dag_valid: true
  no_circular_deps: true
  all_phases_reachable: true

bundles:
  # Generated by bundling algorithm - groups trivial/low/medium phases
  - bundle_id: "bundle-batch1-group1"
    phases: ["phase-1", "phase-2"]
    bundle_config:
      modifier: "lean"        # MAX of bundled phase modifiers
      model: null
      skip: []                # INTERSECTION of bundled phase skips
    spec_title: "Auth models and basic utilities"
    spec_path: "specs/2025/12/feat/oauth/bundle-001-auth-models.md"
    cumulative_score: 4       # Sum of phase complexity scores

  - bundle_id: "bundle-batch2-group1"
    phases: ["phase-4", "phase-5"]
    bundle_config:
      modifier: "lean"
      model: null
      skip: []
    spec_title: "Session and RBAC utilities"
    spec_path: "specs/2025/12/feat/oauth/bundle-002-session-rbac.md"
    cumulative_score: 5
```

## Decomposition Process

### Step 1: Scope Analysis
```
Read input -> Extract requirements -> Identify components -> List concerns
```

### Step 2: Atomic Breakdown
For each concern:
- What's the minimum viable piece?
- What can be tested independently?
- What has clear boundaries?

### Step 3: Dependency Mapping
```
For each atomic unit:
  - What must exist before this works?
  - What does this enable?
  - Can this run in parallel with anything?
```

### Step 4: Phase Grouping
Combine atoms into phases when:
- They share the same concern
- They must change together (coupling)
- Separate execution would be wasteful

### Step 5: DAG Validation
```python
# Pseudocode for validation
def validate_dag(phases):
    visited = set()
    in_progress = set()

    def has_cycle(phase_id):
        if phase_id in in_progress:
            return True  # Cycle detected
        if phase_id in visited:
            return False

        in_progress.add(phase_id)
        for dep in phases[phase_id].dependencies:
            if has_cycle(dep):
                return True
        in_progress.remove(phase_id)
        visited.add(phase_id)
        return False

    for phase_id in phases:
        if has_cycle(phase_id):
            raise ValueError(f"Circular dependency detected: {phase_id}")
```

### Step 6: Bundle Computation

After DAG validation, compute phase bundles:

```python
# Pseudocode for bundle computation
COMPLEXITY_SCORES = {"trivial": 1, "low": 2, "medium": 3}
MAX_BUNDLE_SCORE = 10
MAX_BUNDLE_SIZE = 5

def compute_bundles(phases, execution_order):
    bundles = []
    for batch in execution_order:
        batch_phases = [p for p in phases if p.id in batch.phases]
        # Separate standalone (high/critical) from bundleable
        standalone = [p for p in batch_phases if p.estimated_complexity in ("high", "critical")]
        bundleable = [p for p in batch_phases if p.estimated_complexity not in ("high", "critical")]

        # Cluster bundleable by semantic similarity (title prefix, scope overlap)
        clusters = cluster_by_similarity(bundleable)

        for cluster in clusters:
            # Create bundles respecting size limits
            bundle = create_bundle_from_cluster(cluster, MAX_BUNDLE_SCORE, MAX_BUNDLE_SIZE)
            bundles.append(bundle)

    return bundles
```

### Step 7: Execution Order
Compute topological sort with parallelization:
1. Find all phases with no unmet dependencies
2. Group them as parallel batch
3. Mark as "scheduled"
4. Repeat until all scheduled

## Example Decomposition

**Input**: "Add user authentication with OAuth2, session management, and role-based access control"

**Output Phases**:

1. **phase-auth-models** (no deps)
   - User model, session model, role model
   - Database migrations
   - Acceptance: Models exist, migrations run

2. **phase-oauth-provider** (no deps, parallel with 1)
   - OAuth2 provider configuration
   - Token handling utilities
   - Acceptance: Can obtain tokens from provider

3. **phase-auth-flow** (deps: phase-auth-models, phase-oauth-provider)
   - Login/logout endpoints
   - Session creation/validation
   - Acceptance: User can authenticate

4. **phase-rbac** (deps: phase-auth-models)
   - Role assignment logic
   - Permission checking middleware
   - Acceptance: Roles restrict access

5. **phase-integration** (deps: phase-auth-flow, phase-rbac)
   - Wire authentication into existing routes
   - Add role requirements to protected endpoints
   - Acceptance: Full auth flow works E2E

## Usage

Invoke when:
- Feature requires multiple `/mux-ospec` cycles
- Scope is unclear and needs breakdown
- Dependencies between parts are complex
- Parallel development is desired

Output is consumed by `/mux-ospec` command for orchestrated execution.
