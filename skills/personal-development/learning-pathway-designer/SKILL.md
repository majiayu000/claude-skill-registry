---
name: learning-pathway-designer
description: Create personalized, adaptive learning pathways with branching logic, prerequisite tracking, competency-based progression, and mastery-based advancement. Use when designing adaptive curricula or personalized learning experiences. Activates on "learning path", "adaptive curriculum", "personalization", or "custom pathway".
---

# Learning Pathway Designer

Design adaptive learning pathways that personalize content based on learner performance, preferences, and goals.

## When to Use
- Personalized learning programs
- Competency-based education
- Adaptive curricula
- Self-paced learning
- Remediation/acceleration paths

## Pathway Components

### 1. Prerequisite Mapping
- Define knowledge dependencies
- Create prerequisite trees
- Gate content by mastery
- Detect readiness

### 2. Branching Logic
```
IF mastery < 70% THEN remediation_path
ELSE IF mastery >= 90% THEN acceleration_path
ELSE standard_path
```

### 3. Competency-Based Progression
- Define competencies
- Map content to competencies
- Track mastery per competency
- Advance when ready

### 4. Personalization Rules
- Learning style preferences
- Pacing options
- Content format choices
- Interest-based examples

### 5. Mastery Criteria
- Performance thresholds
- Multiple evidence points
- Time-based vs. mastery-based
- Retry/reassessment policies

## CLI Interface
```bash
/learning.pathway-designer --objectives "LO-1.1,LO-1.2,LO-1.3" --adaptive --prerequisites "path-to-prereqs.json"
/learning.pathway-designer --competency-based --competencies "competencies.json"
/learning.pathway-designer --visualize --pathway "data-science-pathway.json"
```

## Output
- Pathway flowchart/diagram
- Branching rules specification
- Prerequisite graph
- Personalization logic
- JSON pathway definition

## Composition
**Input from**: `/curriculum.design`, `/learning.needs-analysis`, `/learning.diagnostic-assessment`
**Output to**: LMS configuration, adaptive system setup

## Exit Codes
- **0**: Pathway created
- **1**: Invalid prerequisite structure
- **2**: Circular dependencies detected
- **3**: Missing competency definitions
