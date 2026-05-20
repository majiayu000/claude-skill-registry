---
name: kp-applied-domain
description: "Domain knowledge for 10 applied subjects: computer science, data science, world languages, psychology, environmental science, nutrition, economics, creative writing, logic, digital literacy. Use when generating Applied & Practical tier pack content."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "applied.*pack"
          - "(coding|data|language|psychology).*pack"
          - "applied.*tier"
        files:
          - "src/knowledge/packs/code-101/**"
          - "src/knowledge/packs/data-101/**"
          - "src/knowledge/packs/lang-101/**"
          - "src/knowledge/packs/psych-101/**"
          - "src/knowledge/packs/envr-101/**"
          - "src/knowledge/packs/nutr-101/**"
          - "src/knowledge/packs/econ-101/**"
          - "src/knowledge/packs/writ-101/**"
          - "src/knowledge/packs/log-101/**"
          - "src/knowledge/packs/diglit-101/**"
        contexts:
          - "applied skills content"
          - "practical subjects"
        threshold: 0.7
      token_budget: "1.0%"
      version: 1
      enabled: true
      plan_origin: "244-chipset-agent-definitions"
      phase_origin: "244"
---

# Applied Domain

## Purpose

Provides domain expertise for the 10 Applied & Practical tier packs. These are practical skills that build on core academic foundations: computer science, data science, world languages, psychology, environmental science, nutrition, economics, creative writing, logic, and digital literacy. Each subject emphasizes hands-on application and real-world relevance.

## Capabilities

- Subject-specific learning outcome hierarchies for 10 applied subjects
- Cross-subject prerequisite mapping to core tier (e.g., CODE-101 depends on MATH-101, PROB-101)
- Grade-level complexity scaling with emphasis on middle school through college
- Applied activity types (coding projects, data analysis labs, language immersion exercises, field studies)
- Assessment methods emphasizing portfolio and project-based evaluation
- Resource curation with emphasis on interactive tools and practice environments

## Subject Coverage

| Subject | Pack ID | Key Domains |
|---------|---------|-------------|
| Computer Science | CODE-101 | Programming, algorithms, data structures, software engineering |
| Data Science | DATA-101 | Data wrangling, visualization, ML basics, statistical modeling |
| World Languages | LANG-101 | Language acquisition, grammar, culture, communication |
| Psychology | PSYCH-101 | Development, cognition, behavior, mental health |
| Environmental Science | ENVR-101 | Ecology, climate, conservation, sustainability |
| Nutrition | NUTR-101 | Macronutrients, meal planning, food science, health |
| Economics | ECON-101 | Supply/demand, markets, personal finance, macro/micro |
| Creative Writing | WRIT-101 | Literature analysis, creative writing, rhetoric, genre |
| Logic | LOG-101 | Propositional logic, predicate logic, proofs, paradoxes |
| Digital Literacy | DIGLIT-101 | Information evaluation, digital citizenship, online safety |

## Dependencies

- kp-content-authoring skill for file structure and templates
- Pack runtime schemas for validation
- Core academic packs as prerequisites (MATH-101, READ-101, PROB-101, COMM-101)

## Token Budget Rationale

1.0% budget covers the domain knowledge reference for 10 subjects. The skill provides subject-specific guidance (not full content) -- the actual content is generated in context using the authoring templates.
