---
$id: https://schema.org.ai/Skill
$type: http://www.w3.org/2000/01/rdf-schema#Class
$context: http://schema.org.ai/context/agents
label: Skill
comment: A specific capability or skill that an agent can perform
subClassOf:
  - http://schema.org/Thing
properties:
  name: string
  description: string
  category: string
  proficiencyLevel: number
  prerequisites: array
  examples: array
---

# Skill

A **Skill** represents a specific capability or ability that an AI agent possesses. Skills can be innate (from training) or acquired (through fine-tuning or tool access).

## Properties

- **name**: Name of the skill
- **description**: What the skill enables
- **category**: Domain or category (analysis, generation, transformation, execution)
- **proficiencyLevel**: Skill level (0.0-1.0)
- **prerequisites**: Other skills required to use this skill
- **examples**: Example demonstrations of the skill

## Examples

```yaml
$type: Skill
name: code-review
description: Analyze code for quality, bugs, and best practices
category: analysis
proficiencyLevel: 0.9
prerequisites:
  - programming-knowledge
  - pattern-recognition
```
