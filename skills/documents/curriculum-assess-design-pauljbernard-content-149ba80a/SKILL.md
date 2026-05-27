---
name: curriculum-assess-design
description: Design assessment blueprints mapping learning objectives to valid assessment types and create detailed rubrics with performance criteria. Use when planning assessments, creating rubrics, or ensuring constructive alignment. Activates on "create assessment blueprint", "design rubric", "assessment alignment", or "backwards design assessment".
---

# Assessment Blueprint & Rubric Design

Design valid assessments aligned to learning objectives and create rubrics with clear performance criteria following backwards design principles.

## When to Use

Automatically activate when the user:
- Needs to design assessments for learning objectives
- Asks "create assessment blueprint"
- Wants rubrics for assignments or projects
- Requests "align assessments to objectives"
- Says "how should I assess [learning objective]"
- Needs formative or summative assessment planning

## Required Inputs

- **Learning Objectives**: From `/curriculum.design` or user-provided
- **Educational Level**: K-5, 6-8, 9-12, undergraduate, graduate, or post-graduate
- **Assessment Purpose**: Formative, summative, diagnostic, or authentic
- **Constraints** (optional): Time limits, format requirements, accessibility needs

## Workflow

### 1. Load Learning Objectives

Read curriculum design artifact to get:
- All learning objectives with IDs (e.g., LO-1.1, LO-1.2)
- Bloom's taxonomy levels for each
- Standards alignments
- Performance expectations

### 2. Map Objectives to Assessment Types

For each objective, determine appropriate assessment method based on Bloom's level:

**Remember/Understand**:
- Multiple choice
- Matching
- Short answer
- Fill-in-the-blank
- Labeling diagrams

**Apply**:
- Problem sets
- Demonstrations
- Simulations
- Lab activities
- Case applications

**Analyze**:
- Compare/contrast essays
- Diagramming relationships
- Categorization tasks
- Error analysis
- Data interpretation

**Evaluate**:
- Critiques
- Judgments with justification
- Recommendation reports
- Peer review
- Editorial analysis

**Create**:
- Projects
- Designs
- Research papers
- Portfolios
- Original artifacts

### 3. Create Assessment Blueprint

Document the complete assessment strategy:

```markdown
# Assessment Blueprint: [TOPIC]

**Educational Level**: [Level]
**Based on**: [Link to curriculum design]
**Blueprint Date**: [Date]

## Assessment Philosophy

**Approach**: [Formative-heavy, summative-focused, mastery-based, etc.]

**Balance**:
- Formative Assessment: [Percentage]%
- Summative Assessment: [Percentage]%
- Authentic/Performance: [Percentage]%

**Alignment Principle**: Every learning objective has at least one directly aligned assessment item

## Assessment Map

### Unit 1 Assessments

| Objective ID | Objective | Bloom's Level | Assessment Type | When | Weight |
|--------------|-----------|---------------|-----------------|------|--------|
| LO-1.1 | [Full objective text] | Remember | Multiple choice (10 items) | Week 1 | 5% |
| LO-1.2 | [Full objective text] | Understand | Short answer (3 questions) | Week 2 | 10% |
| LO-1.3 | [Full objective text] | Apply | Problem set (5 problems) | Week 2 | 15% |
| LO-1.4 | [Full objective text] | Analyze | Case analysis essay | Week 2 | 20% |

**Unit 1 Total Weight**: 50%

### Unit 2 Assessments

[Same structure]

### Final/Cumulative Assessments

| Assessment | Objectives Assessed | Type | When | Weight |
|------------|-------------------|------|------|--------|
| Final Performance Task | All course objectives | Authentic project | Week 7 | 30% |
| Final Exam | LO-1.1, LO-2.2, LO-3.1, LO-3.4 | Mixed format | Week 8 | 20% |

## Assessment Schedule

| Week | Assessment | Type | Objectives | Rubric Needed |
|------|------------|------|------------|---------------|
| 1    | Formative Check #1 | Quick quiz | LO-1.1, LO-1.2 | No |
| 2    | Unit 1 Assessment | Mixed | LO-1.1-1.4 | Yes |
| 3    | Formative Check #2 | Exit ticket | LO-2.1 | No |
| 4    | Unit 2 Assessment | Performance | LO-2.1-2.3 | Yes |
[Continue for all weeks]

## Rubrics Required

1. **Unit 1 Case Analysis Essay Rubric** (for LO-1.4)
2. **Unit 2 Performance Task Rubric** (for LO-2.3)
3. **Final Project Rubric** (for all objectives)

[Each rubric detailed below]

---

## Rubric 1: [Assessment Name]

**Assessment Type**: [Essay, project, performance task, etc.]
**Objectives Assessed**: [LO-X.X, LO-Y.Y]
**Total Points**: [Point value]
**Rubric Type**: [Analytic or Holistic]

### Analytic Rubric

| Criterion | Exemplary (4) | Proficient (3) | Developing (2) | Beginning (1) | Points |
|-----------|---------------|----------------|----------------|---------------|--------|
| **[Criterion 1]** | [Detailed descriptor of exemplary performance] | [Detailed descriptor of proficient performance] | [Detailed descriptor of developing performance] | [Detailed descriptor of beginning performance] | /4 |
| **[Criterion 2]** | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | /4 |
| **[Criterion 3]** | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | /4 |
| **[Criterion 4]** | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | /4 |

**Total**: /16 points

### Performance Level Conversion

- **Exemplary (A)**: 14-16 points (87.5-100%)
- **Proficient (B)**: 12-13 points (75-87%)
- **Developing (C)**: 10-11 points (62.5-75%)
- **Beginning (D/F)**: < 10 points (< 62.5%)

### Criterion Descriptions

**Criterion 1: [Name]** - [What this criterion assesses and why it's important]

**Exemplary (4)**:
- [Specific indicator 1]
- [Specific indicator 2]
- [Specific indicator 3]

**Proficient (3)**:
- [Specific indicator 1]
- [Specific indicator 2]
- [Minor gap compared to exemplary]

**Developing (2)**:
- [Specific indicator 1]
- [Noticeable gaps]

**Beginning (1)**:
- [Minimal evidence]
- [Significant gaps]

[Repeat for each criterion]

---

## Assessment Validity & Alignment

### Constructive Alignment Check

✅ **Objectives → Assessments**: Every objective has aligned assessment
✅ **Bloom's Match**: Assessment types match cognitive levels
✅ **Content Validity**: Assessments measure intended learning
✅ **Authenticity**: Real-world application where appropriate

### Alignment Matrix

|  | LO-1.1 | LO-1.2 | LO-1.3 | LO-2.1 | LO-2.2 |
|--|--------|--------|--------|--------|--------|
| **Quiz #1** | ✓ | ✓ |  |  |  |
| **Unit 1 Exam** | ✓ | ✓ | ✓ |  |  |
| **Lab Report** |  |  | ✓ | ✓ |  |
| **Final Project** | ✓ | ✓ | ✓ | ✓ | ✓ |

## Accessibility & UDL Considerations

### Universal Design for Assessment

**Multiple Means of Expression**:
- [Option 1]: [Description]
- [Option 2]: [Description]
- [Option 3]: [Description]

**Accommodations Available**:
- Extended time
- Read-aloud
- Scribe
- Simplified language
- Visual supports
- Alternative formats

### Bias Review

**Potential Barriers Identified**:
- [Barrier 1]: [Mitigation strategy]
- [Barrier 2]: [Mitigation strategy]

## Assessment Item Specifications

### Item Type 1: Multiple Choice

**Objective**: [LO-X.X]
**Quantity**: [Number of items]
**Bloom's Level**: [Level]

**Stem Format**: [Question style]
**Options**: [Number of distractors]
**Time per Item**: [Estimated minutes]

**Sample Item**:
[Example question demonstrating format and difficulty]

### Item Type 2: [Type]

[Same structure for each assessment type]

## Grading Workflow

1. **Formative Assessments**: Quick feedback, no formal grade or completion only
2. **Summative Assessments**: Apply rubrics, provide criterion-level feedback
3. **Authentic Tasks**: Use analytic rubrics, conference with students
4. **Final Grades**: Weighted average per assessment schedule

## Next Steps

1. Use `/curriculum.develop-items` to create actual assessment items based on this blueprint
2. Use `/curriculum.develop-content` to create lesson plans aligned to assessments
3. Use `/curriculum.review-pedagogy` to verify alignment after development

---

**Artifact Metadata**:
- **Artifact Type**: Assessment Blueprint
- **Topic**: [Topic]
- **Level**: [Level]
- **Total Assessments**: [Count]
- **Rubrics Created**: [Count]
- **Alignment Verified**: [Yes/No]
- **Next Phase**: Item Development or Content Development
```

### 4. Rubric Quality Standards

Ensure each rubric includes:

✅ **Clear Criteria**: Specific, important aspects of performance
✅ **Distinct Levels**: 3-5 performance levels (4 is standard)
✅ **Descriptive Language**: Observable indicators, not vague terms
✅ **Positive Framing**: Describe what IS present, not just what's missing
✅ **Student-Friendly**: Language students can understand and use for self-assessment
✅ **Actionable Feedback**: Students know how to improve

### 5. Assessment Type Selection Guide

Use this logic to recommend assessment types:

```python
if blooms_level in ["Remember", "Understand"]:
    if level in ["K-5", "6-8"]:
        recommend "Selected response (MC, matching) + some short answer"
    else:
        recommend "Mixed format with emphasis on application"

elif blooms_level == "Apply":
    if level in ["K-5"]:
        recommend "Demonstrations, hands-on tasks, simple problems"
    else:
        recommend "Problem sets, case applications, simulations"

elif blooms_level == "Analyze":
    recommend "Essays, diagrams, comparative analysis, data interpretation"

elif blooms_level == "Evaluate":
    recommend "Critiques, justified judgments, recommendation reports"

elif blooms_level == "Create":
    recommend "Projects, designs, research papers, portfolios, original artifacts"
```

### 6. Output Format

**Human-Readable** (default):
- Formatted markdown with tables
- Write to: `curriculum-artifacts/[topic]-assessment-blueprint.md`

**JSON Format** (use `--format json`):
```json
{
  "artifact_type": "assessment_blueprint",
  "topic": "string",
  "level": "string",
  "assessments": [
    {
      "name": "string",
      "type": "formative|summative|authentic",
      "objectives": ["LO-1.1", "LO-1.2"],
      "blooms_levels": ["Remember", "Apply"],
      "weight": 15,
      "rubric": {
        "type": "analytic|holistic",
        "criteria": [
          {
            "name": "string",
            "exemplary": "descriptor",
            "proficient": "descriptor",
            "developing": "descriptor",
            "beginning": "descriptor",
            "points": 4
          }
        ]
      }
    }
  ]
}
```

### 7. CLI Interface

```bash
# With curriculum design artifact
/curriculum.assess-design --design "photosynthesis-grade5-design.md"

# Specify assessment focus
/curriculum.assess-design --design "quadratics-hs-design.md" --emphasis "authentic"

# Create single rubric
/curriculum.assess-design --rubric-only --objective "LO-3.4" --type "essay"

# JSON output
/curriculum.assess-design --design "neural-networks-design.md" --format json

# Help
/curriculum.assess-design --help
```

## Educational Level Adaptations

### K-5
- Simple rubrics (3 levels: Great, Good, Needs Work)
- Heavy formative emphasis (frequent quick checks)
- Hands-on performance tasks
- Visual rubrics with icons/colors

### 6-8
- Standard rubrics (4 levels)
- Balance formative/summative
- Mix of formats
- Student-involved rubric creation

### 9-12
- Detailed analytic rubrics
- Authentic performance tasks
- Self and peer assessment
- Standards-aligned scoring

### Undergraduate/Graduate
- Professional-quality rubrics
- Emphasis on authentic assessment
- Research and creation tasks
- Discipline-specific criteria

## Composition with Other Skills

**Input from**:
- `/curriculum.design` - Learning objectives drive assessment design

**Output to**:
- `/curriculum.develop-items` - Blueprint specifies items to create
- `/curriculum.develop-content` - Assessments inform instruction
- `/curriculum.review-pedagogy` - Alignment verification
- `/curriculum.grade-assist` - Rubrics used for grading

## Error Handling

- **No learning objectives**: Cannot create blueprint without objectives
- **Missing Bloom's levels**: Infer from objective wording
- **Invalid assessment type**: Suggest appropriate type for cognitive level
- **Rubric criteria unclear**: Use best practices for common task types

## Exit Codes

- **0**: Success - Assessment blueprint and rubrics created
- **1**: Invalid educational level
- **2**: Cannot load learning objectives
- **3**: Assessment type not appropriate for Bloom's level
- **4**: Insufficient information to create rubrics
