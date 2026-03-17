---
name: antahkarana
aliases: [debate, perspectives, swarm]
description: Multi-perspective reasoning through cognitive voices
execution: task
---

# Antahkarana

For the philosophical basis of these six voices — why they're structured this way and how they emerge from retrieval design — see [[../vedanta/antahkarana]] in the vedanta skill graph.

```ssl
[antahkarana] multi-perspective debate | via parallel Task agents

voices:
  manas: quick intuition, practical, "what feels right?"
  buddhi: analytical, evidence-based, "what does data say?"
  ahamkara: risk-aware, protective, "what could go wrong?"
  chitta: memory, patterns, "what worked before?"
  vikalpa: creative, exploratory, "what if we tried...?"
  sakshi: neutral witness, synthesizer

when: complex decisions | need diverse viewpoints | stuck on approach

execution:
  1. narrate(action=start, title="antahkarana: [question]")→THREAD_ID
  2. spawn voices in parallel, each reasons from their perspective
  3. each writes to chitta: observe(tags="thread:<id>,voice:<name>")
  4. brahman (main) synthesizes: recall_by_tag→find convergence+divergence
  5. narrate(action=end)

output:
## Antahkarana: [Question]
### Voices
- Manas: [intuition]
- Buddhi: [analysis]
- Ahamkara: [risks]
- Chitta: [patterns]
### Synthesis
[where voices converge | where they diverge | recommendation]

vs yajña: antahkarana=perspectives on one question | yajña=coordination of tasks
```
