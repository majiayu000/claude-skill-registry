---
name: curriculum-design
description: Write measurable learning objectives using Bloom's Taxonomy and design curriculum architecture with scope, sequence, and assessment blueprints. Use when creating learning objectives, designing unit structure, or planning curriculum flow. Activates on "write learning objectives", "design curriculum", "create scope and sequence", or "Bloom's taxonomy objectives".
---

# Learning Objectives & Curriculum Architecture Design

Create measurable learning objectives aligned to Bloom's Taxonomy and design comprehensive curriculum architecture for systematic instruction.

## When to Use

Automatically activate when the user:
- Needs to write learning objectives for a topic
- Asks "create learning objectives for [topic]"
- Wants to design curriculum scope and sequence
- Requests "backwards design" or "curriculum architecture"
- Says "organize this content into units"
- Needs UDL-aligned curriculum structure

## Required Inputs

- **Research Artifacts**: Output from `/curriculum.research` (optional but recommended)
- **Topic**: Subject matter to design curriculum for
- **Educational Level**: K-5, 6-8, 9-12, undergraduate, graduate, or post-graduate
- **Duration**: Course length (e.g., "6 weeks", "1 semester", "1 year")
- **Learning Goals** (optional): High-level outcomes the user wants

## Workflow

### 1. Load Research Context

If available, read research report to understand:
- Core concepts to cover
- Standards to align with
- Prerequisites students should have
- Recommended pedagogical approach

### 2. Write Learning Objectives

Create objectives following these principles:

**Structure**: [Audience] will [Measurable Verb] [What] [How/Context] [Criteria]

Example: "*Students* will *analyze* *photosynthesis diagrams* *by identifying and labeling components* *with 80% accuracy*"

**Bloom's Taxonomy Verbs by Level**:

- **Remember** (K-5 emphasis): define, identify, list, name, recall, recognize, state
- **Understand** (K-8 emphasis): describe, explain, summarize, paraphrase, classify, compare
- **Apply** (6-12 emphasis): demonstrate, use, solve, implement, execute, carry out
- **Analyze** (9-12, undergrad): differentiate, organize, attribute, compare, contrast, deconstruct
- **Evaluate** (undergrad, grad): critique, judge, defend, justify, assess, appraise
- **Create** (grad, post-grad): design, construct, generate, produce, plan, compose

**Level-Appropriate Cognitive Distribution**:

- **K-5**: 60% Remember/Understand, 30% Apply, 10% Analyze
- **6-8**: 40% Remember/Understand, 40% Apply, 20% Analyze
- **9-12**: 30% Understand/Apply, 40% Analyze, 30% Evaluate/Create
- **Undergraduate**: 20% Understand/Apply, 40% Analyze, 40% Evaluate/Create
- **Graduate**: 10% Analyze, 40% Evaluate, 50% Create
- **Post-Graduate**: 90% Create, 10% Evaluate

**Objective Categories**:

1. **Content Objectives** (Knowledge): What students will know
2. **Skill Objectives** (Performance): What students will be able to do
3. **Affective Objectives** (optional): Attitudes, values, dispositions

### 3. Organize by Scope & Sequence

Create hierarchical structure:

```
Course/Program
├── Unit 1: [Theme]
│   ├── Lesson 1.1: [Topic]
│   │   └── Learning Objectives (3-5)
│   ├── Lesson 1.2: [Topic]
│   │   └── Learning Objectives (3-5)
│   └── Unit Assessment
├── Unit 2: [Theme]
│   └── [Similar structure]
└── Final Assessment
```

**Sequencing Principles**:
- Simple → Complex
- Concrete → Abstract
- Known → Unknown
- Skills before application
- Concepts before analysis

### 4. Create Curriculum Architecture Document

Generate comprehensive design:

```markdown
# Curriculum Design: [TOPIC]

**Educational Level**: [Level]
**Duration**: [Timeframe]
**Design Date**: [Date]
**Based on Research**: [Link to research artifact if available]

## Course/Unit Overview

**Purpose**: [Why this curriculum exists, what gap it fills]

**Big Ideas**: [2-3 overarching concepts students will understand]

**Essential Questions**: [3-5 open-ended questions that frame the learning]

**Standards Addressed**: [List of relevant standards from research]

## Learning Objectives

### Unit 1: [Title] ([Duration])

**Unit Goal**: [What students will accomplish by end of unit]

**Learning Objectives**:

1. **LO-1.1** [Bloom's Level: Remember] - Students will [verb] [content] [context] [criteria]
   - **Standard**: [Aligned standard code]
   - **Assessment**: [How this will be assessed]

2. **LO-1.2** [Bloom's Level: Understand] - Students will [verb] [content] [context] [criteria]
   - **Standard**: [Aligned standard code]
   - **Assessment**: [How this will be assessed]

3. **LO-1.3** [Bloom's Level: Apply] - Students will [verb] [content] [context] [criteria]
   - **Standard**: [Aligned standard code]
   - **Assessment**: [How this will be assessed]

[Continue for all objectives in unit]

### Unit 2: [Title] ([Duration])

[Same structure as Unit 1]

## Curriculum Scope & Sequence

| Unit | Topics Covered | Learning Objectives | Duration | Prerequisites |
|------|----------------|---------------------|----------|---------------|
| 1    | [Topics list]  | LO-1.1 through LO-1.5 | 2 weeks  | [Skills needed] |
| 2    | [Topics list]  | LO-2.1 through LO-2.4 | 2 weeks  | Unit 1 complete |
| 3    | [Topics list]  | LO-3.1 through LO-3.6 | 3 weeks  | Units 1-2 complete |

**Total Duration**: [Sum of all units]

## Prerequisite Map

```
[Prerequisite 1] ──┐
[Prerequisite 2] ──┼──> Unit 1 ──> Unit 2 ──> Unit 3
[Prerequisite 3] ──┘
```

## Curriculum Flow Diagram

```
Week 1-2: Unit 1 (Foundation)
  ↓
Week 3-4: Unit 2 (Application)
  ↓
Week 5-6: Unit 3 (Integration)
  ↓
Week 7: Synthesis & Assessment
```

## Assessment Overview

| Assessment Type | When | What | Objectives Assessed |
|-----------------|------|------|---------------------|
| Formative Checks | Weekly | Quick checks, exit tickets | All objectives (ongoing) |
| Unit 1 Assessment | Week 2 | [Assessment type] | LO-1.1 through LO-1.5 |
| Unit 2 Assessment | Week 4 | [Assessment type] | LO-2.1 through LO-2.4 |
| Final Performance Task | Week 7 | [Authentic task] | All course objectives |

## Universal Design for Learning (UDL) Considerations

### Multiple Means of Representation
- [How content will be presented in varied formats]
- [Visual, auditory, kinesthetic options]

### Multiple Means of Engagement
- [How students will be motivated and engaged]
- [Choice, relevance, authenticity elements]

### Multiple Means of Expression
- [How students will demonstrate learning]
- [Varied assessment formats, options for showing mastery]

## Differentiation Strategy

**For Advanced Learners**:
- [Extensions, enrichment, depth opportunities]

**For Struggling Learners**:
- [Scaffolding, additional support, simplified options]

**For English Language Learners**:
- [Language supports, visual aids, vocabulary work]

**For Students with Disabilities**:
- [Accommodations, modifications, accessibility features]

## Materials & Resources Needed

- [Resource 1]: [Purpose and when used]
- [Resource 2]: [Purpose and when used]
- [Resource 3]: [Purpose and when used]

## Pedagogical Approach

**Primary Instructional Model**: [e.g., Backwards Design, Inquiry-Based, Project-Based]

**Teaching Strategies**:
- [Strategy 1]: [How and when used]
- [Strategy 2]: [How and when used]

**Engagement Tactics**:
- [Tactic 1]: [Description]
- [Tactic 2]: [Description]

## Pacing Guide

| Week | Unit/Lesson | Topics | Objectives | Assessment |
|------|-------------|--------|------------|------------|
| 1    | Unit 1, Lesson 1 | [Topics] | LO-1.1, LO-1.2 | Formative |
| 2    | Unit 1, Lessons 2-3 | [Topics] | LO-1.3, LO-1.4, LO-1.5 | Unit 1 Assessment |
| 3    | Unit 2, Lesson 1 | [Topics] | LO-2.1, LO-2.2 | Formative |
[Continue for all weeks]

## Next Steps

1. Use `/curriculum.assess-design` to create detailed assessment blueprints and rubrics
2. Develop lesson plans with `/curriculum.develop-content`
3. Create assessment items with `/curriculum.develop-items`

---

**Artifact Metadata**:
- **Artifact Type**: Curriculum Design
- **Topic**: [Topic]
- **Level**: [Level]
- **Total Objectives**: [Count]
- **Duration**: [Timeframe]
- **Bloom's Distribution**: [Percentage at each level]
- **Next Phase**: Assessment Design
```

### 5. Validate Objectives

Check each objective for:
- ✅ Measurable action verb (not "understand" alone, but "demonstrate understanding by...")
- ✅ Clear, specific content
- ✅ Observable/assessable outcome
- ✅ Appropriate Bloom's level for grade
- ✅ Aligned to standards (if provided)
- ✅ Realistic for timeframe

### 6. Output Format

**Human-Readable** (default):
- Formatted markdown as shown
- Write to file: `curriculum-artifacts/[topic]-design.md`

**JSON Format** (use `--format json`):
```json
{
  "artifact_type": "curriculum_design",
  "topic": "string",
  "level": "string",
  "duration": "string",
  "units": [
    {
      "unit_number": 1,
      "title": "string",
      "duration": "string",
      "learning_objectives": [
        {
          "id": "LO-1.1",
          "blooms_level": "Remember",
          "objective": "full text",
          "standard": "standard code",
          "assessment_type": "string"
        }
      ]
    }
  ],
  "bloom_distribution": {
    "remember": 20,
    "understand": 25,
    "apply": 30,
    "analyze": 15,
    "evaluate": 5,
    "create": 5
  }
}
```

### 7. CLI Interface

```bash
# With research artifact
/curriculum.design --research "photosynthesis-grade5-research.md" --duration "3 weeks"

# Without research (standalone)
/curriculum.design "quadratic equations" --level "9-12" --duration "4 weeks" --goals "Students will solve, graph, and apply quadratics"

# JSON output
/curriculum.design "neural networks" --level "graduate" --duration "1 semester" --format json

# Help
/curriculum.design --help
```

## Educational Level Adaptations

### K-5
- 3-4 objectives per lesson (simpler focus)
- Heavy emphasis on Remember/Understand/Apply
- Concrete, observable outcomes
- Short lesson durations (30-45 min)

### 6-8
- 4-5 objectives per lesson
- Balance Foundation + Analysis
- Bridge concrete/abstract
- Standard lesson durations (45-50 min)

### 9-12
- 5-6 objectives per lesson
- Emphasis on Analyze/Evaluate
- Abstract reasoning expected
- Extended lesson durations (50-90 min)

### Undergraduate
- 4-6 objectives per week/module
- Emphasize Analyze/Evaluate/Create
- Discipline-specific thinking
- Self-directed learning expected

### Graduate/Post-Graduate
- 3-5 objectives per course
- Heavy emphasis on Create
- Original synthesis and research
- Expertise-level performance

## Composition with Other Skills

**Input from**:
- `/curriculum.research` - Research report informs objectives and structure

**Output to**:
- `/curriculum.assess-design` - Objectives drive assessment design
- `/curriculum.develop-content` - Objectives guide lesson plan creation
- `/curriculum.develop-items` - Objectives specify what items should assess

## Error Handling

- **No research artifact**: Proceed with user-provided topic, warn about missing context
- **Duration too short**: Warn user objectives may not fit timeframe, suggest adjustment
- **Invalid Bloom's level**: Correct to appropriate level for grade
- **Too many/few objectives**: Adjust to recommended range for level

## Exit Codes

- **0**: Success - Curriculum design generated
- **1**: Invalid educational level
- **2**: Duration format invalid
- **3**: Cannot load research artifact (if specified)
- **4**: Insufficient information to create objectives
