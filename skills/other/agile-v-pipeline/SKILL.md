---
name: agile-v-pipeline
description: Orchestration pipeline, wave execution, handoff protocols, and checkpoint types for the Agile V 5-stage workflow. Load when orchestrating multi-agent pipelines or managing stage transitions.
license: CC-BY-SA-4.0
metadata:
  version: "1.3"
  standard: "Agile V"
  author: agile-v.org
  adapted_from:
    - name: "Get Shit Done (GSD)"
      url: "https://github.com/gsd-build/get-shit-done"
      license: "MIT"
      copyright: "Copyright (c) 2025 Lex Christopherson"
      sections: "Orchestration Pipeline"
---

# Instructions

Orchestration pipeline for Agile V. Requires **agile-v-core** loaded first.

## Pipeline

```
Stage 1: Requirements -> Stage 2: Validation -> [Human Gate 1] -> Stage 3: Synthesis (Build Agent || Test Designer) -> Stage 4: Verification -> [Human Gate 2] -> Stage 5: Acceptance
Compliance Auditor observes all stages.
```

## Handoffs

1. Req Architect emits REQUIREMENTS.md -> Logic Gatekeeper reads.
2. Gatekeeper -> Gate 1 (Evidence Summary, Human approves).
3. Build Agent || Test Designer from REQUIREMENTS.md, no shared context.
4. Build Manifest + Test Cases -> Red Team Verifier.
5. Validation Summary -> Gate 2.

## Wave Execution

Dependency analysis -> Wave assignment (no-deps = Wave 1) -> Parallel within waves (fresh context each) -> Sequential across waves -> Prefer vertical slices (feature > layer).

## Checkpoint Types

| Type | Action |
|------|--------|
| Auto | Proceed |
| Human-Verify | Confirm output |
| Human-Decision | Choose alternative |
| Human-Action | Physical/external step |

All except Auto require Human Gate protocol.
