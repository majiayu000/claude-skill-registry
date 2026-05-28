---
name: standards-us-state-mapper
description: Map curriculum to any US state standards framework, support all 50 states' unique standards, crosswalk between state standards, and generate state-specific alignment reports. Use when aligning to state education standards. Activates on "state standards", "TEKS", "state curriculum", or "standards alignment".
---

# Standards: US State Mapper

Map educational content to any US state's educational standards and generate compliance reports.

## When to Use

- Aligning curriculum to state standards
- Multi-state textbook or course development
- State assessment preparation
- Standards reporting for administrators
- Curriculum adoption processes

## Supported State Standards

### All 50 States + Territories

**Major State Frameworks**:
- **Texas**: TEKS (Texas Essential Knowledge and Skills)
- **California**: California Content Standards
- **New York**: New York State Learning Standards (NYSLS)
- **Florida**: NGSSS/B.E.S.T. Standards
- **Illinois**: Illinois Learning Standards
- **Pennsylvania**: PA Core Standards
- **Ohio**: Ohio Learning Standards
- **Virginia**: Virginia Standards of Learning (SOL)
- [All other states...]

**Territories**:
- Puerto Rico
- US Virgin Islands
- Guam
- American Samoa
- Northern Mariana Islands

### Subject Areas Covered

- English Language Arts (ELA)/Reading
- Mathematics
- Science
- Social Studies/History
- Arts
- Physical Education
- Health
- World Languages
- Career and Technical Education (CTE)

## Standards Formats

### Standard Coding Systems

**Examples by State**:
- **Texas**: TEKS §110.11(b)(1)(A)
- **California**: CA.CCSS.ELA-LITERACY.RL.7.1
- **New York**: NY-7.RL.1
- **Common Core (adopted states)**: CCSS.MATH.CONTENT.7.G.A.1

### Standard Components

**Typical Structure**:
- Subject area
- Grade level
- Domain/strand
- Standard number
- Sub-standard (if applicable)

## Alignment Process

### 1. Content Analysis

**Identify**:
- Learning objectives
- Skills taught
- Content covered
- Assessment items

### 2. Standards Matching

**Match to**:
- Specific state standard codes
- Depth of Knowledge (DOK) levels
- Cognitive complexity
- Assessment emphasis

### 3. Coverage Mapping

**Create**:
- Lesson-to-standard maps
- Unit-to-standard maps
- Course-to-standard maps
- Assessment-to-standard maps

### 4. Gap Identification

**Analyze**:
- Which standards covered
- Which standards missing
- Depth of coverage
- Balance across domains

## Multi-State Alignment

### Crosswalk Creation

**Common Scenarios**:
- Textbook publisher (need 5-10 state alignments)
- Online course provider (serve multiple states)
- Curriculum company (national market)

**Approach**:
- Identify common core standards
- Map state-specific variations
- Note unique state requirements
- Create master alignment matrix

## CLI Interface

```bash
# Single state alignment
/standards.us-state-mapper --content "7th-grade-math-unit/" --state "Texas" --subject "mathematics"

# Multiple states
/standards.us-state-mapper --content "science-course/" --states "CA,TX,NY,FL" --subject "science" --grade "7"

# Generate report
/standards.us-state-mapper --curriculum "full-year-ela/" --state "Virginia" --report "school-board"

# Crosswalk multiple states
/standards.us-state-mapper --crosswalk --states "TX,CA,NY,FL,IL" --subject "math" --grade "8"

# Gap analysis
/standards.us-state-mapper --content "existing-curriculum/" --state "Ohio" --gap-analysis
```

## Output

- State standards alignment map (by lesson, unit, course)
- Standard codes with descriptions
- Coverage percentages
- Gap analysis report
- Multi-state crosswalk matrix
- Curriculum correlation documents

## Composition

**Input from**: `/curriculum.design`, `/curriculum.develop-content`, `/curriculum.assess-design`
**Works with**: `/standards.crosswalk-mapper`, `/standards.gap-analysis`, `/standards.coverage-validator`
**Output to**: Standards-aligned curriculum, compliance documentation

## Exit Codes

- **0**: Standards mapping complete
- **1**: State not recognized
- **2**: Subject/grade combination invalid
- **3**: Insufficient content for mapping
