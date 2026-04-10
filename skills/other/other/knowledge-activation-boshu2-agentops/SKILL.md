---
name: knowledge-activation
description: 'Operationalize a mature .agents corpus into usable information. Consolidates packet layers, promotes a belief book, generates playbook candidates, compiles runtime briefings, and surfaces flywheel gaps. Triggers: "operationalize .agents", "turn dot agents into usable information", "knowledge activation", "knowledge flywheel outer loop", "activate knowledge corpus".'
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [TASK]
  intel_scope: topic
metadata:
  tier: knowledge
  dependencies:
    - compile
    - harvest
    - flywheel
output_contract: ".agents/beliefs.md, .agents/playbooks/*.md, .agents/briefings/*.md"
---

# Knowledge Activation

Turn a mature `.agents` corpus into operator-ready knowledge surfaces.

## What This Skill Does

Use this skill when the problem is no longer "capture more knowledge," but:

- promote the strongest recurring claims into a belief system
- turn healthy topics into reusable playbooks
- compile a small goal-time briefing for future work
- surface thin topics and promotion gaps before they silently calcify

`$compile` remains the hygiene loop. `knowledge-activation` owns corpus operationalization.

## Preconditions

This skill assumes the current workspace already has:

- a `.agents/` directory
- packet refresh builders under `.agents/scripts/` when `ao knowledge activate` needs to rebuild source manifests, topics, promoted packets, and chunk bundles
- packet, topic, playbook, and briefing surfaces that can be refreshed mechanically

Read [references/script-contracts.md](references/script-contracts.md) for the required builder inventory and command ownership.

## Command Contract

The stable product surface is the `ao knowledge` command family:

```bash
ao knowledge activate --goal "turn agents into usable information"
ao knowledge beliefs
ao knowledge playbooks
ao knowledge brief --goal "fix auth startup"
ao knowledge gaps
```

The skill owns routing, sequencing, interpretation, and next-step recommendations. `ao` owns the belief/playbook/brief/gap product surfaces directly.

`ao context assemble` and `ao codex start` consume these outputs as operator context. Matched knowledge briefings are the preferred dynamic startup surface, while selected beliefs and healthy playbooks provide bounded supporting guidance.

## Execution Steps

### Step 1: Preflight

Verify that `.agents/` exists. When you plan to run `ao knowledge activate`, also verify that the packet refresh builders are present.

- packet builders: `source_manifest_build.py`, `topic_packet_build.py`, `corpus_packet_promote.py`, `knowledge_chunk_build.py`
- native operator surfaces: `ao knowledge beliefs`, `ao knowledge playbooks`, `ao knowledge brief`, `ao knowledge gaps`

### Step 2: Consolidate Evidence

Run the packet layers in order:

1. source manifests
2. topic packets
3. promoted packets
4. historical chunk bundles

Read [references/dag.md](references/dag.md) for the full DAG and its trust gates.

### Step 3: Distill Operator Surfaces

Refresh the promoted operator layers:

```bash
ao knowledge beliefs
ao knowledge playbooks
```

These should materialize the consumer surfaces under `.agents/knowledge/` and `.agents/playbooks/`.

### Step 4: Compile A Goal-Time Briefing

When there is an active objective, compile a bounded startup aid:

```bash
ao knowledge brief --goal "your goal here"
```

The briefing should stay small, cite its source surfaces, and include warnings when a selected topic is thin.

### Step 5: Surface Gaps

Run:

```bash
ao knowledge gaps
```

This reports thin topics, missing promotions, weak claims needing review, and the next recommended mining work.

### Step 6: Full Outer Loop

If you want the complete pass in one step, run:

```bash
ao knowledge activate --goal "your goal here"
```

That command sequences evidence consolidation, belief/playbook refresh, optional briefing compilation, and a gap summary.

## Trust Rules

- packetization is substrate, not the product
- beliefs, playbooks, and briefings are the real operator surfaces
- thin topics stay discovery-only until evidence improves
- every generated surface should name its consumer
- repeated unchanged runs should stay structurally deterministic

Read [references/output-surfaces.md](references/output-surfaces.md) for the canonical output surfaces and trust boundaries.

## Output Surfaces

The consumer-facing outputs are:

- `.agents/knowledge/book-of-beliefs.md`
- `.agents/playbooks/index.md`
- `.agents/playbooks/<topic>.md`
- `.agents/briefings/YYYY-MM-DD-<goal>.md`
- `.agents/retro/`

The substrate surfaces remain:

- `.agents/packets/`
- `.agents/topics/`
- `.agents/packets/chunks/catalog.jsonl`

## Examples

**Activate the full outer loop for an active goal**

```bash
/knowledge-activation
ao knowledge activate --goal "productize knowledge activation"
```

**Refresh only the belief and playbook promotion layers**

```bash
ao knowledge beliefs
ao knowledge playbooks
```

**Check whether the corpus is safe to promote**

```bash
ao knowledge gaps
```

## References

- [references/dag.md](references/dag.md)
- [references/script-contracts.md](references/script-contracts.md)
- [references/output-surfaces.md](references/output-surfaces.md)
