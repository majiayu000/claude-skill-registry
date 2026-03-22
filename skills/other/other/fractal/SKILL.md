---
name: fractal
description: "Fractal decomposition — recursively split a complex task into orthogonal sub-specs, solve each leaf independently via subagents, then reunify results bottom-up. Use when a task is too large for a single agent pass, when you need to decompose a problem into independently-solvable pieces, or when the user invokes /fractal decompose <task-or-spec-path>."
---

# Fractal Decomposition Skill

> **Governance:** This skill implements the Harness governance protocol.
> See [HARNESS.md](../../HARNESS.md) for the evaluation model, checkpoint protocol,
> and feedback taxonomy. Fractal's checkpoint map:
> - Step 2.5 DECOMPOSE GATE → Layer 1
> - Step 3.5 SOLVE GATE → Layer 1 (or Layer 2 via solve_mode: factory)
> - Step 4.5 REUNIFY REWORK → Layer 2
> - Step 5 Escalate (on rework exhaustion) → Layer 3

Recursively decompose a complex task into a tree of sub-specs on disk, solve each leaf via independent subagents, then reunify results bottom-up into a single coherent output.

## Why specs as intermediate medium

Claude Code subagents cannot spawn their own subagents (no nesting). True fractal decomposition requires recursive depth. The solution: **materialize the decomposition tree as spec files on disk**. Each level of the tree is a directory of sub-specs. The orchestrator (this skill) walks the tree level by level, spawning subagents for each node. The filesystem IS the recursion stack.

```
.fractal/{work-id}/
├── manifest.json              # Tree state + metrics
├── root.md                    # Original task spec
├── tree/
│   ├── 1-auth/
│   │   ├── spec.md            # Sub-spec: "design auth system"
│   │   ├── result.md          # Filled in after solve
│   │   ├── 1-oauth/
│   │   │   ├── spec.md        # Leaf spec: "OAuth flow"
│   │   │   └── result.md
│   │   └── 2-sessions/
│   │       ├── spec.md        # Leaf spec: "session management"
│   │       └── result.md
│   ├── 2-data/
│   │   ├── spec.md
│   │   ├── result.md
│   │   └── ...
│   └── 3-api/
│       ├── spec.md            # Leaf (no further split needed)
│       └── result.md
└── output.md                  # Final reunified result
```

## Usage

```
/fractal decompose <task-description-or-spec-path>
```

Examples:
```
/fractal decompose specs/045-some-feature/README.md
/fractal decompose "Design a microservices platform with auth, data layer, and API gateway"
```

## Configuration

Defaults can be overridden by placing a `.fractal.yaml` in the repo root:

```yaml
fractal:
  max_depth: 3                    # Maximum tree depth (default: 3)
  max_children: 5                 # Max sub-specs per node (default: 5)
  max_total_nodes: 20             # Hard cap on total tree nodes (default: 20)
  split_strategy: orthogonal      # orthogonal | aspect-based | temporal
  reunification: lossless-merge   # lossless-merge | best-child | summary-merge
  min_complexity: medium          # Minimum complexity before splitting is allowed
  solve_mode: parallel            # parallel | sequential
  output_mode: code               # code | design | analysis
```

## Design Principle: Algorithmic Spine

> **AI for semantics, algorithms for structure.**
>
> If the operation can be expressed as a function over syntax trees, diffs,
> dependency graphs, or set operations — it's an algorithm, not a subagent call.

The orchestration protocol uses **classical algorithms** for all structurally-decidable
operations, reserving AI subagents exclusively for semantic input→output transformation:

| Operation | Method | Algorithm |
|-----------|--------|-----------|
| Leaf detection (pre-filter) | Deterministic | Weighted feature scoring (decision tree criterion) |
| Orthogonality check | Deterministic | TF-IDF cosine similarity + Jaccard pre-filter |
| Cycle detection | Deterministic | Kahn's topological sort |
| Solve scheduling | Deterministic | DAG BFS layer decomposition (MapReduce shuffle) |
| Budget allocation | Deterministic | Proportional distribution by complexity score |
| Code reunification | Deterministic | 3-way merge (git merge-tree) |
| Conflict detection | Deterministic | Set intersection on file paths + symbol exports |
| Redundancy pruning | Deterministic | Greedy set cover + diff subset analysis |
| Decompose (semantic) | AI subagent | Understands task meaning → produces sub-specs |
| Solve (semantic) | AI subagent | Understands sub-spec → writes code/design |
| Conflict resolution (semantic) | AI subagent | Resolves ambiguous interface mismatches |

The algorithmic spine is implemented in Rust as `synodic fractal` subcommands:
- `synodic fractal gate` — TF-IDF orthogonality (via `rust-tfidf`), cycle detection, complexity scoring, budget allocation
- `synodic fractal schedule` — DAG-based critical path scheduling into parallel waves
- `synodic fractal reunify` — git merge-tree reunification + structural conflict detection
- `synodic fractal prune` — set cover redundancy analysis
- `synodic fractal complexity` — standalone complexity scoring

All accept JSON from stdin (or `--input <file>`) and output JSON to stdout.

## Orchestration Protocol

When invoked, execute the following steps **exactly**:

### Step 1 — Initialize

1. Parse the input: if a file path, read the spec. If a string, treat it as the task description.
2. Generate a work ID: `fractal-{unix-timestamp}` (e.g., `fractal-1710600000`).
3. Create `.fractal/{work-id}/` directory.
4. Write `root.md` with the original task.
5. Initialize `manifest.json`:
   ```json
   {
     "id": "{work-id}",
     "status": "decomposing",
     "config": {
       "max_depth": 3,
       "max_children": 5,
       "max_total_nodes": 20,
       "split_strategy": "orthogonal",
       "reunification": "lossless-merge"
     },
     "tree": {},
     "metrics": {}
   }
   ```
6. Read `.fractal.yaml` from the repo root if it exists and override defaults.

### Step 1.5 — Complexity Pre-Filter (algorithmic)

Before invoking AI for decomposition, compute a **complexity score** deterministically:

```
echo '<spec text>' | synodic fractal complexity
```

Or as part of the full gate:
```
echo '{"parent_spec": "<spec text>", "children": [], "current_depth": 0, "max_depth": 3, "total_nodes": 0, "max_total_nodes": 20}' | synodic fractal gate
```

The script returns a `complexity_score` (0.0–1.0) based on weighted feature scoring:
- **line_count** (0.15) — longer specs describe more complex tasks
- **term_diversity** (0.25) — more unique concepts = more complex
- **cross_cutting** (0.35) — architectural terms (auth, caching, validation) predict decomposition need
- **enumeration** (0.25) — bullet points / numbered items suggest multiple parts

**If `complexity_score` < `min_complexity` threshold:** auto-LEAF. Skip AI decompose entirely.
**If above threshold:** proceed to Step 2, passing the score as context to the AI.

This is the same principle as a **decision tree split criterion** — a deterministic feature-weighted score decides whether to recurse.

### Step 2 — Decompose (top-down, level by level)

This is the core phase. It runs iteratively (not recursively) to work around the no-nested-subagents constraint.

**For each level, starting from the root:**

Spawn a **general-purpose subagent** for each node that needs decomposition:

```
Agent(
  subagent_type: "general-purpose",
  prompt: <DECOMPOSE_PROMPT below>
)
```

**DECOMPOSE_PROMPT:**

> You are the DECOMPOSE station of a fractal decomposition pipeline.
>
> ## Task
> {content of the node's spec.md}
>
> ## Parent context
> {content of parent spec.md, or "This is the root task." if root}
>
> ## Constraints
> - Split strategy: {split_strategy}
> - Maximum children: {max_children}
> - Current depth: {current_depth} / {max_depth}
> - Remaining node budget: {remaining_nodes}
> - Complexity score: {complexity_score} (algorithmic pre-assessment)
> - Budget allocation: {per-child budget from algorithmic allocation}
>
> ## Instructions
>
> Analyze this task and determine whether it should be split into sub-problems.
>
> **Do NOT split if:**
> - The task is simple enough for one agent to complete in a single pass
> - The task has no natural orthogonal decomposition
> - Current depth equals max depth
> - Splitting would produce trivial sub-problems
>
> **If splitting, for each sub-problem produce:**
> 1. A short slug name (e.g., `auth`, `data-layer`, `api-gateway`)
> 2. A scope description: what this sub-problem covers
> 3. Explicit boundaries: what it does NOT cover
> 4. Input dependencies: what it needs from sibling sub-problems (if any)
> 5. Output contract: what it produces
>
> ## Output format
>
> If this task should NOT be split:
> ```
> === DECOMPOSE VERDICT ===
> VERDICT: LEAF
> REASON: {why splitting is unnecessary}
> === END DECOMPOSE VERDICT ===
> ```
>
> If this task SHOULD be split:
> ```
> === DECOMPOSE VERDICT ===
> VERDICT: SPLIT
> CHILDREN:
> - slug: {slug}
>   scope: {what this child handles}
>   boundaries: {what it does NOT handle}
>   inputs: {dependencies from siblings, or "none"}
>   outputs: {what it produces}
> - slug: {slug}
>   ...
> === END DECOMPOSE VERDICT ===
> ```

After each decompose subagent returns:
- Parse the DECOMPOSE VERDICT.
- If LEAF: mark this node as a leaf in the manifest. No further action.
- If SPLIT: create child directories under `tree/{node-path}/` and write each child's `spec.md` from the scope/boundaries/outputs.
- Update `manifest.json` with the tree structure.
- Decrement the remaining node budget.

**Repeat** for the next level of the tree until all nodes are either leaves or at max depth.

**Budget enforcement:** If `max_total_nodes` would be exceeded, mark the current node as a leaf regardless of the decompose verdict.

### Step 2.5 — DECOMPOSE GATE (algorithmic)

After parsing a SPLIT verdict, **before** writing child spec files, validate the decomposition structurally. This does NOT require a subagent — it's a deterministic check.

1. **Run the gate.** Pipe the decomposition data to the Rust CLI:
   ```
   echo '{"parent_spec": "<parent spec text>", "children": [{"slug": "...", "scope": "...", "inputs": "...", "outputs": "..."}], "current_depth": N, "max_depth": N, "total_nodes": N, "max_total_nodes": N}' | synodic fractal gate
   ```
   The script returns JSON with:
   - `flags` — advisory warnings (array of `{category, description}`)
   - `complexity_score` — parent complexity (0.0–1.0)
   - `budget_allocation` — per-child node budget (proportional to complexity)
   - `dependency_order` — solve waves (parallel groups from topological sort)

2. **Flag categories:**
   - `[orthogonality]` — scope overlap between children (>30% TF-IDF cosine similarity, Jaccard pre-filter)
   - `[coverage]` — parent requirements not covered by any child (>20% parent terms missing)
   - `[cycle]` — circular dependencies between children (detected by Kahn's topological sort)
   - `[budget]` — node budget under pressure (>80% used with depth remaining)

3. **If any flags raised:**
   - Do NOT auto-reject. Append the flags to the DECOMPOSE subagent's output and re-prompt **once** with:

     > The following structural concerns were detected with your decomposition:
     > {flags}
     > Please revise your SPLIT verdict to address these concerns,
     > or change to LEAF if splitting is not appropriate.

   - Parse the revised verdict. Accept it regardless (one retry only).
   - Record **both** the original and revised verdicts in the manifest.

4. **If no flags:** proceed normally.

5. **Store algorithmic outputs** in the manifest for downstream steps:
   - `budget_allocation` → used in child decomposition (Step 2 recursion)
   - `dependency_order` → used in solve scheduling (Step 3)

This gate is fast and deterministic — no LLM cost. It catches common decomposition failures (overlapping scopes, missing coverage, circular dependencies, budget exhaustion) before they propagate down the tree.

### Step 3 — Solve (leaves, dependency-ordered waves)

Schedule leaf nodes for solving using the **DAG-based solve scheduler**:

```
cat .fractal/{work-id}/manifest.json | synodic fractal schedule
```

The scheduler returns:
- `waves` — groups of leaves that can run concurrently (topological sort layers)
- `critical_path` — the longest dependency chain (determines minimum sequential waves)
- `max_parallelism` — peak concurrent leaves in any wave

**Execute waves sequentially, leaves within each wave concurrently.** This replaces the binary parallel/sequential choice with dependency-aware scheduling:
- All independent leaves → single wave (= fully parallel)
- All dependent leaves → one per wave (= fully sequential)
- Mixed → multiple waves with maximal parallelism per wave

For each leaf node, spawn a **general-purpose subagent**:

```
Agent(
  subagent_type: "general-purpose",
  isolation: "worktree",   # Only if output_mode is "code"
  prompt: <SOLVE_PROMPT below>
)
```

**SOLVE_PROMPT:**

> You are the SOLVE station of a fractal decomposition pipeline.
> You are solving ONE specific sub-problem in isolation.
>
> ## Your sub-problem
> {content of this leaf's spec.md}
>
> ## Scope boundaries
> You are ONLY responsible for: {scope}
> You are NOT responsible for: {boundaries}
>
> ## Sibling context (read-only)
> These are the other sub-problems being solved in parallel. You may read
> their specs for interface alignment, but do NOT implement their functionality.
> {list of sibling spec.md contents}
>
> ## Output contract
> Your solution must produce: {outputs from decompose step}
>
> ## Instructions
>
> 1. Read the sub-problem spec carefully.
> 2. Implement a self-contained solution within your declared scope.
> 3. If output_mode is "code": write files, run tests, commit with prefix `fractal({slug}):`.
> 4. If output_mode is "design" or "analysis": produce a structured document.
> 5. Respect your boundaries — do not reach into sibling scopes.
>
> ## Output format
>
> ```
> === SOLVE REPORT ===
> SLUG: {slug}
> STATUS: COMPLETE | PARTIAL | FAILED
> FILES: {comma-separated list of files changed, or "N/A" for non-code}
> SUMMARY: {one-paragraph summary of what was produced}
> INTERFACES: {any interfaces/contracts this solution exposes for siblings}
> === END SOLVE REPORT ===
> ```

After each solve subagent returns:
- Parse the SOLVE REPORT.
- Write `result.md` in the leaf's directory with the full subagent output.
- Update the manifest with solve status.
- Proceed to the SOLVE GATE (Step 3.5).

### Step 3.5 — SOLVE GATE

After each leaf's SOLVE subagent returns, apply a quality gate. The gate tier depends on `solve_mode`:

**If `solve_mode` is `parallel` or `sequential` (lightweight gate):**

1. Run static checks on changed files (same checks as Factory's STATIC GATE):
   - **Rust** (`.rs` files): `cargo check` and `cargo clippy -- -D warnings`
   - **TypeScript/JavaScript** (`.ts`, `.tsx`, `.js`, `.jsx`): `tsc --noEmit` and `eslint`
   - **Python** (`.py` files): `pyright` and `ruff check`
   - Only run checkers for languages that appear in the leaf's changed files.

2. If `.harness/rules/` exists, run each executable rule script against the leaf's changes.

3. **If static failures:** re-solve **once** with failures as feedback.
   - Track as `static_rework_count` per leaf in the manifest.
   - Cap at 1 retry per leaf (trees have many leaves — keep cost bounded).

4. **If pass:** proceed to reunify.

**If `solve_mode` is `factory` (full governance gate):**

Delegate to `/factory run` for each leaf spec. Factory's own BUILD → STATIC GATE → INSPECT pipeline provides the quality gate — no additional gate needed here. Record the Factory manifest reference (work ID) in the Fractal manifest under the leaf node.

This creates two tiers of governance for SOLVE:
- **Lightweight** (default): static checks only, fast, no AI cost
- **Full** (`solve_mode: factory`): Factory's complete pipeline per leaf

### Step 4 — Reunify (bottom-up, algorithm-first)

Once all leaves at a level are solved, reunify them into their parent. Walk the tree bottom-up.

**For `output_mode: code` — algorithmic reunification first:**

Run `synodic fractal reunify` to attempt deterministic merging via git:

```
echo '{"base_ref": "main", "children": [...], "dependency_order": [...], "node_slug": "root"}' | synodic fractal reunify
```

The script performs:
1. **Structural conflict detection** (deterministic, no AI):
   - `[boundary]` — child modified files outside its declared scope (set intersection on file paths)
   - `[redundancy]` — multiple children modified the same file (file owner map)
   - `[gap]` — child declares inputs not produced by any sibling (set difference on contracts)

2. **Git 3-way merge** for each child branch in dependency order:
   - `git merge-tree --write-tree <base> <ours> <theirs>`
   - Clean merges proceed automatically
   - Textual conflicts classified: rename, modify/delete, content

3. **Auto-resolution** for mechanical conflicts (rename, additive changes)

4. **Output**: `{status, auto_resolved, conflicts, merge_order, needs_ai}`

**If `needs_ai` is false:** reunification is complete. Write `result.md`, mark MERGED, continue bottom-up. No AI subagent needed.

**If `needs_ai` is true:** spawn AI subagent ONLY for the specific unresolved conflicts:

```
Agent(
  subagent_type: "general-purpose",
  isolation: "worktree",   # Only if output_mode is "code"
  prompt: <REUNIFY_PROMPT below>
)
```

**For `output_mode: design` or `analysis` — AI reunification:**

Spawn a **general-purpose subagent** (no algorithmic shortcut for prose merging):

**REUNIFY_PROMPT:**

> You are the REUNIFY station of a fractal decomposition pipeline.
> Your job is to merge child solutions into a coherent whole for this level.
>
> ## This node's scope
> {content of this node's spec.md}
>
> ## Reunification strategy: {reunification}
>
> ## Structural analysis (from algorithmic pre-check)
> {conflicts detected by reunify_merge.py, if any}
> {auto-resolved items, if any}
>
> ## Child solutions
> {for each child: slug, spec.md content, result.md content}
>
> ## Instructions
>
> **lossless-merge** (default): Integrate ALL child outputs. Resolve interface
> mismatches. The merged result must be strictly more complete than any child alone.
>
> **best-child**: Select the single child whose solution best addresses the parent
> scope. Justify the selection.
>
> **summary-merge**: Produce a synthesis from child summaries without including
> full implementations (use when context would be too large).
>
> Steps:
> 1. Review each child's solution against its declared scope and output contract.
> 2. Focus on the **unresolved conflicts** identified by the structural analysis.
> 3. Resolve conflicts — prefer the solution that better matches the parent scope.
> 4. Produce the merged result.
> 5. If output_mode is "code": integrate code, resolve import conflicts, run tests.
>
> ## Output format
>
> ```
> === REUNIFY REPORT ===
> STATUS: MERGED | CONFLICT | PARTIAL
> CONFLICTS: {list of conflicts found, or "none"}
> RESOLUTION: {how conflicts were resolved, or "N/A"}
> SUMMARY: {one-paragraph summary of the merged result}
> === END REUNIFY REPORT ===
> ```
>
> Each conflict MUST be prefixed with a category tag:
>
> - [interface] — mismatched types, signatures, or contracts between children
> - [boundary] — a child implemented something outside its declared scope
> - [redundancy] — multiple children solved the same thing differently
> - [gap] — something needed for integration was not produced by any child

After reunification (algorithmic or AI):
- Write `result.md` in the node's directory.
- Update the manifest.
- If STATUS is MERGED: continue bottom-up. No additional action.
- If STATUS is CONFLICT or PARTIAL: proceed to Step 4.5 (REUNIFY REWORK).

### Step 4.5 — REUNIFY REWORK

When reunification returns CONFLICT or PARTIAL status, attempt bounded rework:

1. Parse the CONFLICTS list from the reunification output.
2. Identify which child solutions are in conflict.
3. Re-spawn SOLVE subagents for **only** the conflicting children, with:
   - The original spec
   - The conflict description as additional context
   - The non-conflicting sibling results as fixed constraints
4. After re-solve, run Step 3.5 (SOLVE GATE) on the re-solved leaves.
5. Retry reunification (algorithmic first, then AI if needed) once with the updated child solutions.
6. If still CONFLICT after one retry: mark this node as PARTIAL in the manifest and continue bottom-up. The parent reunification will see a PARTIAL child and can attempt resolution at its level.

Track `reunify_rework_count` per node in the manifest. Maximum 1 rework per reunify node — trees compound, so keep it bounded.

After rework (or if no rework needed), continue bottom-up until the root is reunified.

### Step 5 — Prune & Finalize (algorithmic)

1. **Run the prune gate** to detect redundancy algorithmically:
   ```
   echo '{"tree": <manifest tree>}' | synodic fractal prune
   ```
   The script performs:
   - **Subset detection**: is a node's output files a strict subset of a sibling's?
   - **Identical output detection**: did multiple nodes change the same file set?
   - **Greedy set cover**: find the minimal set of nodes that covers all output files

   Returns: `{prunable, reasons, kept, minimal_covering_set}`

2. Mark prunable nodes in the manifest. No AI needed — this is a deterministic set operation.
3. Write `output.md` in the work directory with the final reunified result.
3. Update `manifest.json` with final metrics:
   ```json
   {
     "status": "complete",
     "metrics": {
       "cycle_time_seconds": 0,
       "tree_depth": 0,
       "total_nodes": 0,
       "leaf_nodes": 0,
       "solve_parallelism": 0,
       "pruned_nodes": 0
     }
   }
   ```
4. Report results to the user.

### Step 5b — Persist to GovernanceLog

After finalizing the manifest, append a summary record to `.harness/fractal.governance.jsonl`. This file is **not** gitignored — it accumulates across runs and is committed to version control.

Each line is a JSON object:

```json
{
  "work_id": "fractal-...",
  "source": "fractal",
  "timestamp": "<ISO 8601>",
  "status": "complete|partial|failed",
  "config": { "max_depth": 3, "split_strategy": "orthogonal", "..." : "..." },
  "tree_metrics": {
    "depth": 0,
    "total_nodes": 0,
    "leaf_nodes": 0,
    "pruned_nodes": 0
  },
  "decompose_flags": [
    {"node": "1-auth", "category": "orthogonality", "description": "..."}
  ],
  "solve_failures": [
    {"leaf": "1-auth/2-sessions", "static_failures": ["type_error"], "rework_count": 1}
  ],
  "reunify_conflicts": [
    {"node": "1-auth", "category": "interface", "description": "..."}
  ],
  "cycle_time_seconds": 0
}
```

Fields:
- `decompose_flags`: all flags raised by Step 2.5 across all nodes in this run.
- `solve_failures`: all static gate failures from Step 3.5, grouped by leaf.
- `reunify_conflicts`: all conflicts from Step 4/4.5, with category tags.
- `tree_metrics`: final tree shape metrics from the manifest.

After appending, commit the updated `governance.jsonl` as part of the fractal run.

## Parsing Rules

- DECOMPOSE VERDICT is between `=== DECOMPOSE VERDICT ===` and `=== END DECOMPOSE VERDICT ===`.
- SOLVE REPORT is between `=== SOLVE REPORT ===` and `=== END SOLVE REPORT ===`.
- REUNIFY REPORT is between `=== REUNIFY REPORT ===` and `=== END REUNIFY REPORT ===`.
- If a subagent response doesn't contain the expected block, log the raw response in the manifest and treat the node as FAILED.

## Important Notes

- **No nested subagents.** The orchestrator (you) walks the tree level by level, spawning flat subagents at each step. The spec files on disk ARE the recursion.
- **Algorithmic spine.** Most orchestration logic is deterministic — AI is only invoked for semantic operations (decompose, solve, conflict resolution). The `synodic fractal` subcommands implement classical algorithms in Rust: TF-IDF similarity (via `rust-tfidf` crate), topological sort, 3-way merge, set cover.
- `.fractal/` directory is gitignored (per-run manifests are local artifacts). Governance infrastructure lives in `.harness/` (rules, scripts, governance logs) and is committed to version control.
- SOLVE subagents with `output_mode: code` run in `isolation: worktree` to avoid conflicts.
- SOLVE subagents receive sibling specs as read-only context for interface alignment.
- The decompose phase is inherently sequential (each level depends on the previous). The solve phase uses **DAG-based wave scheduling** — neither purely parallel nor sequential, but dependency-aware.
- Each fractal run is independent — concurrent runs use different work IDs.
- Budget enforcement is strict: if `max_total_nodes` is hit, remaining nodes become forced leaves. Budget is **allocated proportionally** to children by complexity score (not first-come-first-served).
- **COMPLEXITY PRE-FILTER** (Step 1.5) uses weighted feature scoring to auto-LEAF trivial tasks without invoking AI. Same principle as decision tree split criteria.
- **DECOMPOSE GATE** (Step 2.5) runs `synodic fractal gate` with TF-IDF cosine similarity (via `rust-tfidf`), dependency cycle detection via Kahn's algorithm, and per-child budget allocation. Deterministic and fast — no LLM cost.
- **SOLVE SCHEDULER** (Step 3) runs `synodic fractal schedule` to compute parallel execution waves via topological sort. Critical path analysis determines minimum sequential depth.
- **REUNIFY MERGE** (Step 4) runs `synodic fractal reunify` to attempt deterministic git merge-tree reunification. AI subagents are only spawned for semantic conflicts that algorithms can't resolve.
- **PRUNE GATE** (Step 5) runs `synodic fractal prune` for algorithmic redundancy detection via set cover and diff subset analysis. No AI needed.
- **SOLVE GATE** (Step 3.5) applies static checks to leaf solutions. Two tiers: lightweight (static checks only) for default mode, full Factory pipeline for `solve_mode: factory`.
- **REUNIFY REWORK** (Step 4.5) re-solves conflicting children once when reunification fails. Bounded to 1 retry per node to prevent exponential cost in deep trees.
- **GovernanceLog** (`.harness/fractal.governance.jsonl`) accumulates a summary record from every fractal run, enabling cross-run pattern analysis. Shared static rules with Factory via `.harness/rules/`.
- All governance checkpoints are **bounded**: 1 retry at DECOMPOSE, 1 retry per leaf at SOLVE, 1 retry per node at REUNIFY. This is intentional — trees compound, and unbounded rework would be catastrophic for cost.

## Comparison with Factory Skill

| Aspect | Factory | Fractal |
|--------|---------|---------|
| Shape | Linear pipeline (BUILD → INSPECT) | Recursive tree (DECOMPOSE → SOLVE → REUNIFY) |
| Parallelism | Sequential stations | Parallel leaf solving |
| Rework | INSPECT → BUILD loop (max 3) | Bounded: 1 retry at DECOMPOSE, SOLVE, REUNIFY |
| Governance | STATIC GATE + adversarial INSPECT | DECOMPOSE GATE + SOLVE GATE + REUNIFY REWORK |
| Learning | .harness/factory.governance.jsonl | .harness/fractal.governance.jsonl (shared rules) |
| Output | PR from single implementation | Unified result from merged sub-solutions |
| When to use | Single spec, needs review | Complex task, needs decomposition |

## Composability

The fractal skill composes with the factory skill:

- **Fractal → Factory**: Each leaf sub-spec is implemented via `/factory run` instead of a bare SOLVE subagent. This adds adversarial review to each leaf. To enable, set `solve_mode: factory` in `.fractal.yaml`.
- **Factory → Fractal**: A factory BUILD station can invoke `/fractal decompose` if it determines the spec is too complex for a single pass.

## Future: Cross-Topology Crystallization

Both Factory and Fractal write to governance logs (`.harness/factory.governance.jsonl`
and `.harness/fractal.governance.jsonl`). A future crystallization process can aggregate
across BOTH logs to identify patterns that transcend execution topology:

- Recurring decompose flags → improve DECOMPOSE_PROMPT heuristics or add
  static decomposition templates for known problem shapes
- Recurring solve static failures → feed into `.harness/rules/` (shared with Factory)
- Recurring reunify conflicts → generate interface contract templates
  in `.fractal/templates/` that future decompositions can reference

The static rules in `.harness/rules/` are shared between Factory and Fractal
because SOLVE (Fractal) and BUILD (Factory) face the same class of structural errors.
Crystallizing once benefits both topologies.
