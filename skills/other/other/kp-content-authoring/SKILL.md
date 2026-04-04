---
name: kp-content-authoring
description: "Generates knowledge pack content suites: vision documents, modules YAML, activities JSON, assessment frameworks, resource catalogs, and .skillmeta files. Shared by all 3 tier-specific author agents. Use when creating or updating pack content files."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "pack.*create|create.*pack"
          - "pack.*content"
          - "vision.*doc"
          - "module.*yaml"
          - "activit.*json"
          - "assessment.*framework"
        files:
          - "src/knowledge/packs/**/vision.md"
          - "src/knowledge/packs/**/modules.yaml"
          - "src/knowledge/packs/**/activities.json"
          - "src/knowledge/packs/**/assessment.md"
          - "src/knowledge/packs/**/resources.md"
          - "src/knowledge/packs/**/.skillmeta"
        contexts:
          - "knowledge pack authoring"
          - "educational content creation"
        threshold: 0.7
      token_budget: "2.0%"
      version: 1
      enabled: true
      plan_origin: "244-chipset-agent-definitions"
      phase_origin: "244"
---

# Content Authoring

## Purpose

Provides the content generation methodology for all 35 knowledge packs. This is the shared authoring skill loaded by KP-02 (core), KP-03 (applied), and KP-04 (specialized). It defines the pack file structure, content templates, quality standards, and parallel instruction patterns that enable token caching across packs.

## Capabilities

- Vision document generation following PACK-TEMPLATE.md structure (~40 pages per pack)
- Modules YAML with learning outcomes, topics, grade levels, time estimates, and prerequisite chains
- Activities JSON with grade-appropriate hands-on activities per module
- Assessment framework with rubric levels (Beginning, Developing, Proficient, Advanced)
- Resource catalog with categorized links by audience and grade level
- .skillmeta YAML generation with full KnowledgePackSchema compliance
- Grade level spanning: PreK through College+ with appropriate content differentiation
- Learning pathway support: Maker, Academic, Curiosity, Social, Parent-Guided

## Parallel Instruction Patterns (NFR-06)

The following instruction sections are identical across all 35 packs and should be cached:

1. **Pack file structure template** -- the 6-file directory layout is the same for every pack
2. **Vision document skeleton** -- section headings (Vision, Problem Statement, Core Concepts, Skill Tree, Modules, Assessment Framework, Parent Guidance, Resources) are reused
3. **Modules YAML schema** -- PackModuleSchema structure with time_estimates, prerequisite_modules, activities sub-objects
4. **Activities JSON schema** -- PackActivitySchema with grade_range, duration_minutes, materials, learning_objectives
5. **Assessment rubric template** -- 4-level rubric (Beginning, Developing, Proficient, Advanced) with formative/summative sections
6. **Resource catalog template** -- categorized sections (Young Learners, Older Learners, Parents, Deeper Study)
7. **.skillmeta boilerplate** -- common fields (version, status, copyright, gsd_integration, accessibility stubs, translation stubs)
8. **Grade level bands** -- Foundation (PreK-K), Elementary (1-5), Middle School (6-8), High School (9-12), College (13-16)

These 8 patterns are loaded once and reused across all pack generation sessions, reducing per-pack token overhead by ~60%.

## Key Modules

| Module | Purpose |
|--------|---------|
| `src/knowledge/types.ts` | Zod schemas defining pack data structures |
| `src/knowledge/skillmeta-parser.ts` | Validates generated .skillmeta against KnowledgePackSchema |
| `src/knowledge/vision-parser.ts` | Validates generated vision documents |
| `src/knowledge/activity-loader.ts` | Validates generated activities JSON |
| `src/knowledge/assessment-loader.ts` | Validates generated assessment markdown |
| `src/knowledge/resource-loader.ts` | Validates generated resource catalogs |

## Usage Examples

**Generate a pack content suite:**
```
For each pack (e.g., MATH-101):
1. Create src/knowledge/packs/math-101/ directory
2. Write vision.md using pack-specific content + shared template sections
3. Write modules.yaml matching ModulesFileSchema
4. Write activities.json as PackActivity[] array
5. Write assessment.md with 4-level rubric
6. Write resources.md with categorized links
7. Write .skillmeta matching KnowledgePackSchema
```

**Apply parallel instruction patterns:**
```
Before generating any pack, load:
- Pack file structure template (shared)
- Vision document skeleton (shared)
- Modules YAML schema (shared)
- Activities JSON schema (shared)
- Assessment rubric template (shared)
- Resource catalog template (shared)
- .skillmeta boilerplate (shared)
- Grade level bands (shared)
Then inject pack-specific: subject content, domain activities, subject-specific resources
```

## Dependencies

- Pack runtime API (src/knowledge/) for schema validation
- Domain-specific skill (core, applied, or specialized) for subject matter knowledge
- Pack template structure from delivery package

## Token Budget Rationale

2.0% budget reflects the comprehensive authoring methodology covering 6 file types, 8 parallel instruction patterns, and the pack generation workflow. This is the largest knowledge pack skill because it provides the reusable templates that reduce per-pack generation cost. Shared across 3 agents but loaded once per session.
