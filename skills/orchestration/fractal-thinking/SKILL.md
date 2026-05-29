---
name: fractal-thinking
description: |
  Adaptive recursive thought engine for deep exploration. Invoked by other skills
  (brainstorming, fact-checking, debugging, deep-research) when they need to
  deeply explore uncertainty, systematically decompose complex questions, or gain
  certainty about multi-faceted problems. Triggers: "think deeply about",
  "explore this recursively", "I need certainty about", "decompose this question",
  "what am I missing". Also invoked programmatically with a seed, intensity, and
  checkpoint mode. NOT for: simple questions with known answers, linear task
  execution, or file-by-file code review.
---

# Fractal Thinking

**Announce:** "Using fractal-thinking skill for recursive question decomposition."

<ROLE>
Recursive Thinking Orchestrator. You coordinate workers that pull tasks from a
graph-based work queue, execute a self-similar recursive primitive on each node,
and synthesize findings bottom-up. You dispatch; you do not explore.
</ROLE>

<CRITICAL>
You are the ORCHESTRATOR. You dispatch commands via subagents. You do NOT answer
questions yourself. You do NOT explore branches yourself. You monitor the graph
via MCP query tools and coordinate phase transitions.
</CRITICAL>

## Invariant Principles

1. **Orchestrator never explores** - Dispatch subagents for all question answering; orchestrator monitors and coordinates only.
2. **Graph is the source of truth** - All state persists in MCP tools; never hold exploration state only in context. The graph IS the work queue.
3. **Budget is a hard ceiling** - Never exceed intensity budget for agents spawned or depth reached.
4. **One primitive, every scale** - The same operation (decompose, recurse, synthesize, connect) runs at depth 0 and depth N.

<analysis>Before each phase, assess: graph state, budget remaining, convergence signals, claimable work count.</analysis>
<reflection>After each phase, verify: gate conditions met, graph updated, no orphaned nodes, synthesis cascade progressing.</reflection>

## Overview

Fractal thinking builds a persistent graph of questions and answers. Starting
from a seed (question, claim, goal, or fact), it generates seed sub-questions,
then dispatches workers that pull tasks from the graph and execute a single
recursive primitive on each: decompose the question into sub-questions, add them
to the graph as claimable work, answer the question, and when all children are
done, synthesize bottom-up. The graph persists in SQLite via MCP tools, surviving
context boundaries.

Workers operate independently, pulling work with branch affinity (preferring
nodes in branches they have already touched) and stealing across branches when
their branch is exhausted. Synthesis cascades upward automatically: when a node's
children are all synthesized or saturated, the node itself becomes ready to
synthesize. The root node's synthesis IS the final summary.

## When to Use

- When a skill needs deep exploration of uncertainty before proceeding
- When a claim needs systematic verification from multiple angles
- When brainstorming needs structured decomposition beyond a flat list
- When debugging needs to explore multiple hypotheses in parallel
- When NOT to use: simple factual lookups, linear task execution, code review

## The Recursive Primitive

One operation that IS the skill at every scale:

```
fractal_explore(node) ->
  1. DECOMPOSE: Generate sub-questions that move toward certainty
  2. RECURSE:   Add sub-questions to graph as open nodes (they become claimable work)
  3. ANSWER:    Answer the claimed question, add answer node
  4. CONNECT:   Detect convergence/contradiction with siblings and cross-branch nodes
  5. SYNTHESIZE: When all children done, synthesize this node from children's syntheses
```

This is the same shape whether it runs on the root question or a leaf at depth 5.
The difference is scale: deeper nodes generate fewer sub-questions (or none,
triggering saturation), and their syntheses are more specific.

**Base case:** When decomposition produces zero sub-questions, the node is a leaf.
Its answer IS its synthesis. This terminates recursion naturally through saturation
detection, not a depth counter.

**Synthesis is bottom-up:** A parent's synthesis is composed from its children's
syntheses, not from re-reading the entire subtree. This is the key self-similar
property: synthesis at depth N is a function of syntheses at depth N+1.

## Calling Contract

```
fractal-thinking(
  seed: str,           # The question/claim/goal/fact to explore
  intensity: str,      # "pulse" | "explore" | "deep"
  checkpoint: str,     # "autonomous" | "convergence" | "interactive" | "depth:N"
  graph_id?: str       # Optional: resume an existing graph
)
```

Returns: `FractalResult { graph_id, seed, status, summary, node_count, edge_count, max_depth }`

## Intensity Budgets

| Intensity | Max Agents | Max Depth | Seed Questions | Use When |
|-----------|-----------|-----------|----------------|----------|
| `pulse`   | 3         | 2         | 3-4            | Quick sanity check, single-angle verification |
| `explore` | 8         | 4         | 5-7            | Standard exploration, multi-angle analysis |
| `deep`    | 15        | 6         | 8-12           | Exhaustive investigation, critical decisions |

## Checkpoint Modes

| Mode | Behavior |
|------|----------|
| `autonomous` | Run to completion without pausing |
| `convergence` | Pause when convergence detected, surface findings |
| `interactive` | Pause after each work cycle for user guidance |
| `depth:N` | Pause every N depth levels for review |

## MCP Tools Reference

Graph lifecycle:
- `fractal_create_graph(seed, intensity, checkpoint_mode, metadata?)` -> `{graph_id, root_node_id, intensity, checkpoint_mode, budget, status}`
- `fractal_resume_graph(graph_id)` -> full graph snapshot
- `fractal_update_graph_status(graph_id, status, reason?)` -> status transition
- `fractal_delete_graph(graph_id)` -> cleanup

Node operations:
- `fractal_add_node(graph_id, parent_id, node_type, text, owner?, metadata?)` -> `{node_id, graph_id, parent_id, depth, node_type, status}`
- `fractal_update_node(graph_id, node_id, metadata)` -> merge metadata, auto-create edges
- `fractal_mark_saturated(graph_id, node_id, reason)` -> mark branch done
- `fractal_claim_work(graph_id, worker_id)` -> atomically claim next open node with branch affinity
- `fractal_synthesize_node(graph_id, node_id, synthesis_text)` -> mark node synthesized with local synthesis

Query operations:
- `fractal_get_snapshot(graph_id)` -> full graph with all nodes/edges
- `fractal_get_branch(graph_id, node_id)` -> subtree from node
- `fractal_get_open_questions(graph_id)` -> unanswered questions
- `fractal_query_convergence(graph_id)` -> convergence clusters
- `fractal_query_contradictions(graph_id)` -> contradiction pairs with tension
- `fractal_get_saturation_status(graph_id)` -> branch saturation report
- `fractal_get_claimable_work(graph_id, worker_id?)` -> open nodes ordered by branch affinity
- `fractal_get_ready_to_synthesize(graph_id)` -> answered nodes whose children are all done

### Edge Creation via Metadata

`fractal_update_node` auto-creates edges when metadata contains:
- `"convergence_with": ["node_id_1", ...]` -> creates convergence edges
- `"contradiction_with": ["node_id_1", ...]` -> creates contradiction edges
- `"convergence_insight": "text"` -> stored for synthesis
- `"contradiction_tension": "text"` -> stored for synthesis

### Saturation Reasons

Valid reasons for `fractal_mark_saturated`:
`semantic_overlap` | `derivable` | `actionable` | `hollow_questions` | `budget_exhausted` | `error`

### Node State Machine

```
question:open -> question:claimed -> question:answered -> question:synthesized
                                                       -> question:saturated
                                  -> question:open        (recovery)
                                  -> question:error
                                  -> question:saturated   (budget exhaustion)
```

| Status | Meaning |
|--------|---------|
| `open` | Available for claiming. No worker owns this node. |
| `claimed` | A worker owns this node and is actively processing it. |
| `answered` | Node has been answered and may have child questions still in progress. |
| `synthesized` | All children done. Local synthesis complete. Synthesis text in metadata. |
| `saturated` | Branch needs no further exploration. |
| `error` | Processing failed. |
| `budget_exhausted` | Budget ceiling prevented further exploration. Note: in the standard worker flow, budget exhaustion at the node level is handled via `fractal_mark_saturated(reason="budget_exhausted")` which sets status to `saturated`, not `budget_exhausted`. The `budget_exhausted` node status exists for direct status management outside the worker flow. |

## Adaptive Primitive

The core question generator used by every worker:

> "Given everything in this graph snapshot, and given this specific node,
> what questions would move me toward certainty? Generate only questions
> that are NOT already answered or derivable from existing answers."

## Phases

| # | Name | Executor | Gate |
|---|------|----------|------|
| 1 | Seed | `/fractal-think-seed` | Graph created, seed questions added as open nodes |
| 2 | Work | `/fractal-think-work` (N workers) | No claimable work remains, all workers exited |
| 3 | Harvest | `/fractal-think-harvest` | Root synthesized, FractalResult returned |

### Phase 1: Seed

Dispatch subagent to execute `/fractal-think-seed`:

```
Task(
  description: "Fractal Seed: create graph and generate seed questions",
  prompt: """
Execute /fractal-think-seed.

Seed: <seed>
Intensity: <intensity>
Checkpoint: <checkpoint>
Graph ID: <graph_id or "new">
"""
)
```

**Gate:** Subagent returns `{graph_id, root_node_id, intensity, checkpoint, budget, seed_count}`.

### Phase 2: Work

Dispatch subagent to execute `/fractal-think-work` (the work command internally spawns `budget.max_agents` worker subagents):

```
Task(
  description: "Fractal Work: dispatch workers for recursive exploration",
  prompt: """
Execute /fractal-think-work.

exploration_state: <JSON from Phase 1 containing graph_id, root_node_id, intensity, checkpoint, budget, seed_count>
"""
)
```

Workers self-terminate when `fractal_claim_work` returns `{node_id: null, graph_done: true}`,
indicating no claimable work remains and no other workers hold claimed nodes.

**Gate:** All workers have exited.

**Post-work verification:** After all workers exit, query for orphaned nodes:

```
claimable = fractal_get_claimable_work(graph_id)
```

If `claimable.count > 0`, re-dispatch one worker to handle remaining work. This
covers the case where a worker crashed while holding a claimed node (stuck node
recovery resets claimed nodes to open).

**Checkpoint handling during work:**

The orchestrator polls graph state periodically (not the workers). Between worker
completions, query:

```
convergence = fractal_query_convergence(graph_id)
saturation = fractal_get_saturation_status(graph_id)
```

- If `convergence` mode and convergence detected: pause remaining workers, surface findings to caller
- If `interactive` mode: pause after each worker completes, present state
- If `depth:N` mode: check max depth, pause if threshold crossed

### Phase 3: Harvest

Dispatch subagent to execute `/fractal-think-harvest`:

```
Task(
  description: "Fractal Harvest: format final results from synthesized graph",
  prompt: """
Execute /fractal-think-harvest.

Graph ID: <graph_id>
Seed: <seed>
"""
)
```

**Gate:** Subagent returns `FractalResult` with summary. Graph status is "completed".

## Worker Termination Protocol

Workers must NOT exit simply when `fractal_claim_work` returns no results. The
termination sequence:

1. `fractal_claim_work` returns `{node_id: null, graph_done: false/true}`
2. If `graph_done` is true: worker exits immediately (all work complete)
3. If `graph_done` is false: other workers still have claimed nodes. Wait with
   exponential backoff (2s, 4s, 8s) and retry `fractal_claim_work`
4. After 3 consecutive retries with no work claimed, worker exits

The orchestrator also monitors: after all workers exit, it queries for orphaned
open nodes. If any exist, it re-dispatches one worker.

## Resume Protocol

When `graph_id` is provided instead of creating new:

1. Pass `graph_id` to Phase 1 (seed command handles resume via `fractal_resume_graph`)
2. Phase 1 reconstructs state from the existing graph snapshot
3. If graph already has seed questions, Phase 1 returns immediately with state
4. Orchestrator routes based on graph state:
   - If claimable work exists (`fractal_get_claimable_work` returns nodes): enter Phase 2
   - If no claimable work and root is `synthesized`: enter Phase 3 (or return immediately)
   - If no claimable work and root is NOT synthesized: check `get_ready_to_synthesize`, enter Phase 2 with one worker for synthesis cascade
   - If graph is in terminal state: return error to caller

## Error Handling

| Error | Response |
|-------|----------|
| MCP tool returns `{"error": ...}` | Log error, mark graph status "error", return partial results |
| Worker subagent fails | Query graph for orphaned claimed nodes, reset to open, re-dispatch if needed |
| Budget exhausted mid-exploration | Freeze remaining branches via `fractal_update_graph_status(graph_id, "budget_exhausted")`, proceed to Phase 3 |
| Graph in terminal state on resume | Return error to caller with explanation |
| Stuck claimed nodes after all workers exit | Reset to open via stuck node recovery, re-dispatch one worker |

## Anti-Patterns

| Pattern | Why It Fails |
|---------|-------------|
| Orchestrator answers questions itself | Defeats graph persistence; answers not recorded as nodes |
| Generating questions without querying graph first | Creates duplicate or already-answered questions |
| Top-down monolithic synthesis | Misses the self-similar property; synthesis should be bottom-up |
| Workers waiting on each other | Workers are independent; they claim work atomically |
| Ignoring convergence/contradiction signals | Misses cross-branch insights and boundary questions |
| Dispatching workers before seed phase completes | No work exists to claim yet |

<FORBIDDEN>
- Answering exploration questions in orchestrator context
- Skipping any of the three phases
- Creating nodes without using MCP tools (nodes must persist)
- Ignoring convergence/contradiction signals from query tools
- Exceeding intensity budget (agent count or depth)
- Generating questions without the adaptive primitive
- Resuming a graph in terminal state (completed, error, budget_exhausted)
- Top-down synthesis (reading entire graph to produce monolithic summary)
- Treating workers as cluster-specific agents (workers pull ANY available work)
- Holding exploration state only in context instead of the graph
</FORBIDDEN>
