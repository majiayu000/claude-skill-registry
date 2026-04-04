---
name: kp-core-academic-domain
description: "Domain knowledge for 15 core academic subjects: math, science, technology, engineering, physics, chemistry, reading, critical thinking, problem solving, communication, history, geography, materials, business, statistics. Use when generating Core Academic tier pack content."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "core.*academic"
          - "(math|science|physics|chemistry|engineering).*pack"
          - "(reading|history|geography).*pack"
          - "core.*tier"
        files:
          - "src/knowledge/packs/math-101/**"
          - "src/knowledge/packs/sci-101/**"
          - "src/knowledge/packs/tech-101/**"
          - "src/knowledge/packs/engr-101/**"
          - "src/knowledge/packs/phys-101/**"
          - "src/knowledge/packs/chem-101/**"
          - "src/knowledge/packs/read-101/**"
          - "src/knowledge/packs/crit-101/**"
          - "src/knowledge/packs/prob-101/**"
          - "src/knowledge/packs/comm-101/**"
          - "src/knowledge/packs/hist-101/**"
          - "src/knowledge/packs/geo-101/**"
          - "src/knowledge/packs/mfab-101/**"
          - "src/knowledge/packs/bus-101/**"
          - "src/knowledge/packs/stat-101/**"
        contexts:
          - "core academic content"
          - "foundational subjects"
        threshold: 0.7
      token_budget: "1.0%"
      version: 1
      enabled: true
      plan_origin: "244-chipset-agent-definitions"
      phase_origin: "244"
---

# Core Academic Domain

## Purpose

Provides domain expertise for the 15 Core Academic tier packs. Contains subject-specific knowledge for generating educationally accurate content: learning outcome frameworks, prerequisite relationships within and across subjects, grade-appropriate complexity scaling, and standards alignment references (Common Core, NCTM, NGSS where applicable).

## Capabilities

- Subject-specific learning outcome hierarchies for 15 core subjects
- Cross-subject prerequisite mapping (e.g., MATH-101 as prerequisite for PHYS-101, STAT-101)
- Grade-level complexity scaling from PreK through College+
- Standards alignment references: Common Core (math, reading), NCTM (math), NGSS (science, engineering)
- Subject-specific activity types (lab experiments for science, proof exercises for math, debates for communication)
- Assessment method selection per subject domain
- Resource curation guidance per subject (textbooks, interactive tools, online courses)

## Subject Coverage

| Subject | Pack ID | Key Domains |
|---------|---------|-------------|
| Mathematics | MATH-101 | Number sense, algebra, geometry, calculus, statistics |
| Science Method | SCI-101 | Scientific method, observation, hypothesis, experimentation |
| Technology | TECH-101 | Digital tools, computational thinking, tech literacy |
| Engineering | ENGR-101 | Design process, constraints, prototyping, testing |
| Physics | PHYS-101 | Mechanics, thermodynamics, waves, electromagnetism |
| Chemistry | CHEM-101 | Atomic structure, reactions, stoichiometry, organic |
| Reading | READ-101 | Phonics, comprehension, analysis, critical reading |
| Critical Thinking | CRIT-101 | Logic, argument analysis, bias detection, evaluation |
| Problem Solving | PROB-101 | Strategies, decomposition, pattern recognition |
| Communication | COMM-101 | Speaking, listening, persuasion, media literacy |
| History | HIST-101 | Chronology, causation, primary sources, historiography |
| Geography | GEO-101 | Physical geography, human geography, mapping, GIS |
| Materials | MFAB-101 | Material properties, manufacturing, sustainability |
| Business | BUS-101 | Entrepreneurship, management, ethics, law basics |
| Statistics | STAT-101 | Data collection, probability, inference, visualization |

## Dependencies

- kp-content-authoring skill for file structure and templates
- Pack runtime schemas for validation

## Token Budget Rationale

1.0% budget covers the domain knowledge reference for 15 subjects. The skill provides subject-specific guidance (not full content) -- the actual content is generated in context using the authoring templates.
