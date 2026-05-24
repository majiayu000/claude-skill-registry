---
name: curriculum-research
description: Research subject matter, align to educational standards, map prerequisites, and recommend learning theories for curriculum design. Use when starting curriculum development, exploring new topics, or needing standards alignment. Activates on "research this topic", "what standards apply", "curriculum research", or "prerequisite analysis".
---

# Curriculum Research & Standards Alignment

Research subject matter and provide comprehensive analysis for curriculum design including standards alignment, prerequisite mapping, and pedagogical recommendations.

## When to Use

Automatically activate when the user:
- Starts curriculum development for a new topic
- Asks "research [topic] for [grade level]"
- Needs educational standards alignment (Common Core, NGSS, etc.)
- Requests prerequisite skill analysis
- Says "what learning theory should I use for [topic]"
- Needs interdisciplinary connections identified

## Required Inputs

- **Topic**: Subject matter to research (e.g., "photosynthesis", "quadratic equations", "Renaissance history")
- **Educational Level**: K-5, 6-8, 9-12, undergraduate, graduate, or post-graduate
- **Standards Framework** (optional): Specific standards to align with (e.g., "Common Core Math", "NGSS", "AP Biology")

## Workflow

### 1. Gather Topic and Level

```bash
# User provides topic and level
Topic: [user specified]
Level: [K-5 | 6-8 | 9-12 | undergraduate | graduate | post-graduate]
Standards: [optional: Common Core, NGSS, state standards, discipline framework]
```

### 2. Conduct Subject Matter Research

Use WebSearch to gather:
- **Core Concepts**: Foundational ideas, terminology, definitions
- **Scope & Boundaries**: What's included/excluded at this level
- **Common Misconceptions**: Student difficulties, conceptual barriers
- **Real-World Applications**: Relevance, career connections, authentic contexts
- **Interdisciplinary Connections**: Links to other subjects

### 3. Align to Educational Standards

Use WebSearch to identify:
- **Relevant Standards**: Specific standards codes and descriptions
  - K-12: Common Core (Math/ELA), NGSS (Science), state standards, C3 Framework (Social Studies)
  - Undergraduate: Discipline-specific accreditation standards (ABET, APA, etc.)
  - Graduate: Professional competency frameworks, research methodologies
- **Performance Expectations**: What students should know and be able to do
- **Cognitive Levels**: Bloom's taxonomy levels expected at this grade/level
- **Assessment Boundaries**: What's assessable vs. out of scope

### 4. Map Prerequisites

Analyze and document:
- **Required Prior Knowledge**: Concepts students must already understand
- **Skill Dependencies**: Procedural skills needed before this topic
- **Cognitive Readiness**: Developmental appropriateness
- **Prerequisite Sequence**: Order in which foundational topics should be taught
- **Gap Identification**: Common missing prerequisites to address

### 5. Recommend Learning Theories & Approaches

Based on topic and level, recommend:
- **Primary Learning Theory**: Constructivism, cognitivism, connectivism, behaviorism, etc.
- **Instructional Approaches**: Direct instruction, inquiry-based, problem-based, project-based, etc.
- **Pedagogical Strategies**: Scaffolding, modeling, think-alouds, collaborative learning, etc.
- **Engagement Tactics**: Hooks, real-world connections, student choice, authentic tasks
- **Assessment Philosophy**: Formative vs summative emphasis, authentic assessment, mastery-based, etc.

### 6. Generate Research Report

Create a structured document with:

```markdown
# Curriculum Research Report: [TOPIC]

**Educational Level**: [Level]
**Standards Framework**: [Framework(s)]
**Research Date**: [Date]

## Executive Summary

[2-3 paragraph overview of topic scope, key concepts, and pedagogical recommendations]

## Core Concepts & Scope

### Foundational Ideas
- [Concept 1]: [Definition and importance]
- [Concept 2]: [Definition and importance]
- [Concept 3]: [Definition and importance]

### Topic Boundaries
**Included**: [What this curriculum will cover]
**Excluded**: [What's out of scope or saved for later]

### Common Misconceptions
1. [Misconception 1]: [Why students think this and how to address]
2. [Misconception 2]: [Why students think this and how to address]

## Educational Standards Alignment

### Relevant Standards

**[Standard Code]**: [Full standard description]
- **Performance Expectation**: [What students will demonstrate]
- **Cognitive Level**: [Bloom's level]
- **Assessment Boundary**: [What to assess/what not to assess]

[Repeat for each relevant standard]

### Cross-Curricular Connections

- **[Subject Area]**: [How this topic connects]
- **[Subject Area]**: [How this topic connects]

## Prerequisite Analysis

### Required Prior Knowledge

| Prerequisite | Description | Typical Grade Taught | Why Needed |
|--------------|-------------|---------------------|------------|
| [Concept/Skill] | [What it is] | [Grade level] | [Connection to current topic] |

### Recommended Prerequisite Sequence

1. [First prerequisite topic]
2. [Second prerequisite topic]
3. [Third prerequisite topic]
   → Then ready for [Current topic]

### Common Gaps & Remediation

- **Gap**: [Missing knowledge students often have]
  - **Remediation**: [How to address in current curriculum]

## Pedagogical Recommendations

### Recommended Learning Theory

**[Theory Name]** (e.g., Constructivism, Cognitivism)

**Rationale**: [Why this theory fits the topic and level]

**Implications for Instruction**:
- [How this theory shapes teaching approach]
- [Specific strategies that align with this theory]

### Instructional Approach

**Primary Approach**: [e.g., Inquiry-based learning, Direct instruction, Project-based learning]

**Supporting Strategies**:
- [Strategy 1]: [How to implement]
- [Strategy 2]: [How to implement]
- [Strategy 3]: [How to implement]

### Engagement Considerations

- **Hook Ideas**: [Compelling ways to introduce topic]
- **Real-World Connections**: [Authentic applications]
- **Student Choice Opportunities**: [Where students can make decisions]
- **Differentiation Needs**: [How to support diverse learners]

### Assessment Philosophy

- **Formative Assessment**: [Recommended frequency and types]
- **Summative Assessment**: [Recommended culminating assessments]
- **Authentic Assessment**: [Real-world performance tasks]

## Real-World Applications

- [Application 1]: [Description and relevance]
- [Application 2]: [Description and relevance]
- [Application 3]: [Description and relevance]

## Resources for Further Development

- [Resource type]: [Specific recommendations]
- [Resource type]: [Specific recommendations]

## Next Steps

1. Use `/curriculum.design` to create learning objectives based on this research
2. Identify assessment types in `/curriculum.assess-design`
3. Develop instructional content with `/curriculum.develop-content`

---

**Artifact Metadata** (for traceability):
- **Artifact Type**: Research Report
- **Topic**: [Topic]
- **Level**: [Level]
- **Standards**: [Frameworks used]
- **Next Phase**: Design (Learning Objectives)
```

### 7. Output Format

Support both human-readable and machine-readable formats:

**Human-Readable** (default):
- Formatted markdown as shown above
- Write to file: `curriculum-artifacts/[topic]-research.md`

**JSON Format** (use `--format json`):
```json
{
  "artifact_type": "research_report",
  "topic": "string",
  "level": "string",
  "standards": ["array of standard codes"],
  "core_concepts": [
    {"name": "string", "description": "string"}
  ],
  "prerequisites": [
    {"concept": "string", "grade": "string", "rationale": "string"}
  ],
  "learning_theory": "string",
  "instructional_approach": "string",
  "real_world_applications": ["array of strings"],
  "next_steps": ["array of skill calls"]
}
```

### 8. CLI Interface

```bash
# Basic usage
/curriculum.research "photosynthesis" --level "6-8" --standards "NGSS"

# With output format
/curriculum.research "quadratic equations" --level "9-12" --standards "Common Core Math" --format json

# Graduate level (discipline-specific)
/curriculum.research "neural networks" --level "graduate" --standards "ACM Computing Curricula"

# Help
/curriculum.research --help
```

## Educational Level Adaptations

### K-5
- Focus on concrete, observable phenomena
- Emphasize hands-on exploration
- Use age-appropriate vocabulary
- Prioritize foundational skills
- Heavy scaffolding needs

### 6-8
- Bridge concrete to abstract thinking
- Introduce symbolic representations
- Build on elementary foundations
- Support identity formation (relevance crucial)
- Moderate scaffolding

### 9-12
- Abstract reasoning expected
- Discipline-specific thinking
- College/career preparation focus
- Greater cognitive complexity
- Reduced scaffolding

### Undergraduate
- Disciplinary frameworks & epistemology
- Research introduction
- Professional practice preparation
- High cognitive demand (Analyze, Evaluate, Create)

### Graduate
- Original research & scholarship
- Cutting-edge knowledge
- Thought leadership development
- Expertise-level performance

### Post-Graduate
- Specialization & innovation
- Field contributions
- Advanced professional practice
- Research dissemination

## Composition with Other Skills

This skill outputs research artifacts that feed into:
- `/curriculum.design` - Uses research to inform learning objectives
- `/curriculum.assess-design` - Uses standards for assessment alignment
- `/curriculum.develop-content` - Uses concepts, misconceptions, and pedagogical recommendations

## Error Handling

- **No search results**: Broaden search, try related terms, inform user if topic is too obscure
- **Standards not found**: Suggest closest framework, document assumption
- **Level mismatch**: Warn if topic typically taught at different level, provide guidance
- **Ambiguous topic**: Ask user for clarification on scope

## Output Example

User: "Research photosynthesis for grade 5"

Output: Complete research report with:
- Core concepts (light energy, chloroplasts, glucose production, oxygen release)
- NGSS standards (5-PS3-1, 5-LS1-1, 5-LS2-1)
- Prerequisites (plant structure, energy basics, cycles in nature)
- Recommended approach (Inquiry-based with hands-on investigation)
- Common misconceptions (plants eat soil, only leaves do photosynthesis)
- Real-world connections (food production, climate, oxygen generation)

File saved to: `curriculum-artifacts/photosynthesis-grade5-research.md`

## Exit Codes

- **0**: Success - Research report generated
- **1**: Invalid educational level specified
- **2**: Topic too vague - needs clarification
- **3**: Standards framework not found
- **4**: WebSearch unavailable - cannot complete research
