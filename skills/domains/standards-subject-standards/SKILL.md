---
name: standards-subject-standards
description: Align to subject-specific national standards including NGSS, Common Core, C3, NCTM, ACTFL, SHAPE, ISTE, and arts standards. Generate detailed standards alignment with codes. Use for national standards alignment. Activates on "NGSS", "Common Core", "national standards", or "NCTM".
---

# Standards: Subject-Specific Standards

Align curriculum to subject-specific national standards frameworks.

## When to Use

- Developing subject-specific curriculum
- Aligning to national frameworks
- Creating standards-based assessments
- Documenting pedagogical rigor
- Grant applications requiring standards alignment

## Supported Standards Frameworks

### English Language Arts

**Common Core State Standards (CCSS-ELA)**:
- Reading: Literature (RL), Informational Text (RI)
- Writing (W)
- Speaking & Listening (SL)
- Language (L)
- Grades K-12

**Example Standard**: CCSS.ELA-LITERACY.RL.7.2 - "Determine a theme or central idea of a text"

### Mathematics

**Common Core State Standards for Mathematics (CCSS-M)**:
- Counting & Cardinality (K)
- Operations & Algebraic Thinking
- Number & Operations
- Measurement & Data
- Geometry
- Statistics & Probability
- High School: Algebra, Functions, Modeling, Geometry, Statistics

**NCTM (National Council of Teachers of Mathematics)**:
- Process Standards: Problem Solving, Reasoning, Communication, Connections, Representation
- Content Standards by grade band

**Example**: CCSS.MATH.CONTENT.7.G.A.2 - "Draw geometric shapes with given conditions"

### Science

**NGSS (Next Generation Science Standards)**:
- **Structure**: Performance Expectations (PEs)
- **Three Dimensions**:
  - Science & Engineering Practices (SEPs)
  - Disciplinary Core Ideas (DCIs)
  - Crosscutting Concepts (CCCs)
- **Grade Bands**: K-2, 3-5, MS (6-8), HS (9-12)

**Example**: MS-LS1-6 - "Construct a scientific explanation based on evidence for the role of photosynthesis"

### Social Studies

**C3 Framework (College, Career, and Civic Life)**:
- Dimension 1: Developing Questions and Planning Inquiries
- Dimension 2: Applying Disciplinary Concepts
- Dimension 3: Evaluating Sources and Using Evidence
- Dimension 4: Communicating Conclusions and Taking Informed Action

**NCSS (National Council for the Social Studies)**:
- 10 Thematic Strands
- Grades K-12

### World Languages

**ACTFL (American Council on the Teaching of Foreign Languages)**:
- 5 C's: Communication, Cultures, Connections, Comparisons, Communities
- Proficiency Levels: Novice, Intermediate, Advanced, Superior, Distinguished
- Performance Descriptors

### Arts

**National Core Arts Standards**:
- Creating
- Performing/Presenting/Producing
- Responding
- Connecting
- Covers: Dance, Media Arts, Music, Theatre, Visual Arts

### Physical Education

**SHAPE America Standards**:
- Standard 1: Motor Skills & Movement Patterns
- Standard 2: Movement Concepts & Strategies
- Standard 3: Physical Activity
- Standard 4: Fitness
- Standard 5: Personal & Social Responsibility

### Technology

**ISTE Standards (International Society for Technology in Education)**:
- **For Students**: Empowered Learner, Digital Citizen, Knowledge Constructor, etc.
- **For Educators**: Learner, Leader, Citizen, Collaborator, Designer, Facilitator, Analyst
- **For Education Leaders**
- **For Coaches**

## Alignment Methodology

### Three-Dimensional Alignment (for NGSS)

**Map to All Dimensions**:
1. **SEP**: Which science practice? (Asking Questions, Developing Models, Analyzing Data, etc.)
2. **DCI**: Which core idea? (LS1.A Structure and Function, PS1.B Chemical Reactions, etc.)
3. **CCC**: Which crosscutting concept? (Patterns, Cause & Effect, Systems, etc.)

### Common Core ELA/Math

**Identify**:
- Specific standard code
- Depth of Knowledge (DOK) level
- Cognitive demand
- Standard clusters/groups

### Subject-Specific Nuances

**ACTFL (Languages)**:
- Mode: Interpretive, Interpersonal, Presentational
- Proficiency level alignment
- Cultural contexts

**Arts**:
- Artistic process
- Anchor standard
- Performance standard by grade

## CLI Interface

```bash
# NGSS alignment
/standards.subject-standards --content "photosynthesis-unit/" --framework "NGSS" --grade "MS" --subject "life-science"

# Common Core Math
/standards.subject-standards --content "fractions-unit/" --framework "CCSS-Math" --grade "5"

# Common Core ELA
/standards.subject-standards --content "argument-writing/" --framework "CCSS-ELA" --grade "9-10" --strand "writing"

# C3 Framework
/standards.subject-standards --content "civics-unit/" --framework "C3" --grade "8"

# ACTFL
/standards.subject-standards --content "spanish-course/" --framework "ACTFL" --level "Intermediate-Mid"

# Multiple frameworks
/standards.subject-standards --content "integrated-unit/" --frameworks "NGSS,CCSS-Math,CCSS-ELA" --grade "7"
```

## Output

- Detailed standards alignment map
- Standard codes with full descriptions
- Three-dimensional NGSS analysis (if applicable)
- DOK/cognitive complexity levels
- Coverage analysis by strand/domain
- Alignment documentation

## Composition

**Input from**: `/curriculum.research`, `/curriculum.design`, `/curriculum.develop-content`
**Works with**: `/standards.us-state-mapper`, `/standards.international-curriculum`, `/standards.crosswalk-mapper`
**Output to**: Nationally-aligned curriculum

## Exit Codes

- **0**: Standards alignment complete
- **1**: Framework not supported
- **2**: Grade level incompatible
- **3**: Insufficient content for alignment
