---
name: kp-specialized-domain
description: "Domain knowledge for 10 specialized subjects: philosophy, theology, physical education, nature studies, home economics, visual arts, music, trades, astronomy, learning to learn. Use when generating Specialized & Deepening tier pack content."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "specialized.*pack"
          - "(philosophy|theology|art|music).*pack"
          - "specialized.*tier"
        files:
          - "src/knowledge/packs/philo-101/**"
          - "src/knowledge/packs/theo-101/**"
          - "src/knowledge/packs/pe-101/**"
          - "src/knowledge/packs/nature-101/**"
          - "src/knowledge/packs/domestic-101/**"
          - "src/knowledge/packs/art-101/**"
          - "src/knowledge/packs/music-101/**"
          - "src/knowledge/packs/trade-101/**"
          - "src/knowledge/packs/astro-101/**"
          - "src/knowledge/packs/learn-101/**"
        contexts:
          - "specialized content"
          - "deepening subjects"
        threshold: 0.7
      token_budget: "1.0%"
      version: 1
      enabled: true
      plan_origin: "244-chipset-agent-definitions"
      phase_origin: "244"
---

# Specialized Domain

## Purpose

Provides domain expertise for the 10 Specialized & Deepening tier packs. These subjects enrich and deepen the educational experience beyond core academics and applied skills: philosophy, theology, physical education, nature studies, home economics, visual arts, music, trades, astronomy, and learning to learn. Each subject emphasizes personal growth, cultural awareness, and life skills.

## Capabilities

- Subject-specific learning outcome hierarchies for 10 specialized subjects
- Cross-subject prerequisite mapping to core and applied tiers where applicable
- Grade-level complexity scaling with emphasis on experiential learning at all levels
- Specialized activity types (philosophical debates, art projects, musical performance, nature observation, hands-on trades)
- Assessment methods emphasizing reflection, portfolio, and demonstration
- Resource curation with emphasis on primary sources, community resources, and hands-on materials

## Subject Coverage

| Subject | Pack ID | Key Domains |
|---------|---------|-------------|
| Philosophy | PHILO-101 | Ethics, metaphysics, epistemology, logic, aesthetics |
| Theology | THEO-101 | World religions, comparative study, ethics, history |
| Physical Education | PE-101 | Movement, fitness, sports, health, body awareness |
| Nature Studies | NATURE-101 | Observation, identification, ecology, seasonal cycles |
| Home Economics | DOMESTIC-101 | Cooking, budgeting, sewing, household management |
| Visual Arts | ART-101 | Drawing, painting, sculpture, art history, design |
| Music | MUSIC-101 | Theory, performance, composition, history, appreciation |
| Trades | TRADE-101 | Woodworking, electronics, plumbing, mechanical skills |
| Astronomy | ASTRO-101 | Solar system, stars, galaxies, cosmology, observation |
| Learning to Learn | LEARN-101 | Study strategies, metacognition, time management, memory |

Note: LEARN-101 is the meta-pack that cross-references study strategies applicable to all other 34 packs.

## Dependencies

- kp-content-authoring skill for file structure and templates
- Pack runtime schemas for validation
- Core academic packs as foundational prerequisites where applicable

## Token Budget Rationale

1.0% budget covers the domain knowledge reference for 10 subjects. The skill provides subject-specific guidance (not full content) -- the actual content is generated in context using the authoring templates.
