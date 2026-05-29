---
name: kp-content-validation
description: "Validates knowledge pack content against runtime schemas: .skillmeta against KnowledgePackSchema, modules against ModulesFileSchema, activities against PackActivitySchema. Checks cross-pack references, learning outcome uniqueness, and file completeness. Use when validating pack content after generation."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "pack.*validat"
          - "schema.*check"
          - "pack.*verify"
          - "cross.*pack.*ref"
        files:
          - "src/knowledge/content-validator.ts"
          - "src/knowledge/__tests__/content-validator.test.ts"
        contexts:
          - "pack content validation"
          - "schema verification"
        threshold: 0.7
      token_budget: "1.0%"
      version: 1
      enabled: true
      plan_origin: "244-chipset-agent-definitions"
      phase_origin: "244"
---

# Content Validation

## Purpose

Validates all generated pack content against the runtime schemas defined in src/knowledge/types.ts. This is the quality gate skill used by the KP-05 validator agent after each batch of packs is generated. It catches schema violations, missing files, broken cross-pack references, and duplicate learning outcome codes before content reaches the review stage.

## Capabilities

- .skillmeta YAML validation against KnowledgePackSchema via parseSkillmeta
- Modules YAML validation against ModulesFileSchema
- Activities JSON validation against PackActivitySchema (per-entry)
- Vision document structure validation (required sections present)
- Assessment framework structure validation (rubric levels present)
- Resource catalog validation (links resolve, categories present)
- Cross-pack dependency reference validation (pack_id exists in registry)
- Learning outcome code uniqueness across all registered packs
- File completeness check (all 6 required files per pack directory)
- Batch validation: run all checks across 5 packs in a single pass

## Key Modules

| Module | Purpose |
|--------|---------|
| `src/knowledge/content-validator.ts` | Pack content validation engine |
| `src/knowledge/skillmeta-parser.ts` | .skillmeta YAML parsing with Zod validation |
| `src/knowledge/registry.ts` | Pack registry for cross-reference checking |
| `src/knowledge/dependency-resolver.ts` | Prerequisite chain validation with cycle detection |
| `src/knowledge/prerequisite-validator.ts` | Entry requirement checking |

## Usage Examples

**Validate a single pack:**
```typescript
import { validatePack } from './content-validator.js';

const result = await validatePack('src/knowledge/packs/math-101');
// result.valid: boolean
// result.errors: string[] (empty if valid)
// result.warnings: string[] (non-blocking issues)
```

**Validate a batch:**
```
After Phase 245 completes, run validation across all 5 generated packs:
- MATH-101, SCI-101, TECH-101, ENGR-101, PHYS-101
Check cross-pack references resolve within the batch and against previously registered packs.
```

## Dependencies

- Pack runtime API (src/knowledge/) -- all parsers and validators
- Registry with previously registered packs for cross-reference resolution

## Token Budget Rationale

1.0% budget reflects the validation module references and schema knowledge needed for comprehensive checking. The validator operates on the runtime API, not on raw content, keeping context requirements moderate.
