---
name: mooco-mirror
description: "Parallel introspection for MOOCO sessions and cross-orchestrator comparison"
license: MIT
tier: 0
allowed-tools: []
protocol: MOOCO-MIRROR
tags: [moollm, introspection, orchestration, traceability]
related: [mooco, cursor-mirror, session-log, event-logging, yaml-jazz, thoughtful-commitment, skill-snitch]
---

# MOOCO Mirror

> *"Watch two orchestration realities at once."*

MOOCO‑mirror is a reflection skill for MOOCO sessions. It is built to compare orchestration decisions, context assembly, and tool execution between MOOCO and Cursor environments. It also runs in production without a Cursor sidecar.

## Core Capabilities

- **Session introspection**: read MOOCO event logs and context bundles
- **Cross‑mirror**: line up a MOOCO run with a Cursor run
- **Divergence analysis**: highlight where context, tools, or outputs differ
- **Trace provenance**: show which steps are deterministic vs LLM‑driven
- **Optimization**: find bottlenecks and reduce orchestration friction
- **Debugging**: isolate drift, regressions, and tool misuse
- **Exploration**: probe alternative orchestration strategies safely
- **Play‑Learn‑Lift**: capture learnings and uplift them into skills
- **Context analysis**: inspect what was loaded and why
- **Reverse engineering**: infer Cursor and MOOCO orchestration patterns

## Cross‑Mirror Pattern

1. Capture a MOOCO session event stream.
2. Capture the parallel Cursor session via cursor‑mirror.
3. Align by task goal or timestamp.
4. Compare context, tools, and emitted events.

## Use Cases

- Validate MOOCO orchestration choices
- Debug unexpected tool selection
- Diagnose context drift across orchestrators
- Improve skill portability by exposing hidden assumptions
- Support thoughtful-commitment by exporting prompts, thoughts, context assembly, and cause/effect into commit and PR messages
- Run skill-snitch style scans to detect suspicious patterns in mirrored traces
