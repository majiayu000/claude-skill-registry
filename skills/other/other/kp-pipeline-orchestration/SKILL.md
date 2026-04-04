---
name: kp-pipeline-orchestration
description: "Orchestrates knowledge pack content generation pipeline: batch scheduling, completion tracking, cross-pack dependency ordering, and validation triggering. Use when coordinating pack generation across phases 245-251."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "knowledge.*pipeline"
          - "pack.*batch"
          - "pack.*schedule"
          - "pack.*orchestrat"
        files:
          - "infra/packs/knowledge/chipset.yaml"
          - "infra/packs/knowledge/teams/kp-content-pipeline.yaml"
        contexts:
          - "knowledge pack pipeline"
          - "pack batch scheduling"
        threshold: 0.7
      token_budget: "1.0%"
      version: 1
      enabled: true
      plan_origin: "244-chipset-agent-definitions"
      phase_origin: "244"
---

# Pipeline Orchestration

## Purpose

Coordinates the 35-pack content generation pipeline using a map-reduce pattern. Manages batch scheduling (7 phases x 5 packs), tracks completion state across phases, resolves cross-pack dependency ordering to prevent forward references, and triggers validation/review after each batch completes.

## Capabilities

- 7-phase batch scheduling: phases 245-251 with 5 packs per batch
- Cross-pack dependency ordering within batches (e.g., MATH-101 before PHYS-101)
- Completion state tracking per pack per phase
- Validation gate triggering after batch generation
- Review assignment after validation passes
- Progress reporting across all 35 packs
- Retry coordination for packs that fail validation

## Key Modules

| Module | Purpose |
|--------|---------|
| `infra/packs/knowledge/chipset.yaml` | Master agent/skill/team/pack definitions |
| `infra/packs/knowledge/teams/kp-content-pipeline.yaml` | Pipeline team topology and stages |
| `src/knowledge/registry.ts` | Pack registry for completion verification |
| `src/knowledge/content-validator.ts` | Content validator for batch validation gates |

## Usage Examples

**Batch scheduling:**
```
Phase 245: MATH-101, SCI-101, TECH-101, ENGR-101, PHYS-101 (Core Academic batch 1)
Phase 246: CHEM-101, READ-101, CRIT-101, PROB-101, COMM-101 (Core Academic batch 2)
Phase 247: HIST-101, GEO-101, MFAB-101, BUS-101, STAT-101 (Core Academic batch 3)
Phase 248: CODE-101, DATA-101, LANG-101, PSYCH-101, ENVR-101 (Applied batch 1)
Phase 249: NUTR-101, ECON-101, WRIT-101, LOG-101, DIGLIT-101 (Applied batch 2)
Phase 250: PHILO-101, THEO-101, PE-101, NATURE-101, DOMESTIC-101 (Specialized batch 1)
Phase 251: ART-101, MUSIC-101, TRADE-101, ASTRO-101, LEARN-101 (Specialized batch 2)

After each batch: kp-validator runs schema checks, kp-reviewer runs quality review.
```

## Dependencies

- Pack runtime API (src/knowledge/) for registry and validation
- Chipset YAML for pack-to-agent and pack-to-phase mapping
- Pipeline team YAML for coordination topology

## Token Budget Rationale

1.0% budget reflects the orchestration metadata (chipset, pipeline team, batch schedule). The coordinator reads definitions but does not hold pack content in context.
