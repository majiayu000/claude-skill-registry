---
name: standards-crosswalk-mapper
description: Create crosswalks between different standards frameworks, map equivalent standards across systems, show alignment between multiple frameworks simultaneously. Use when comparing or mapping standards. Activates on "crosswalk", "standards mapping", or "framework comparison".
---

# Standards: Crosswalk Mapper

Create crosswalks between different educational standards frameworks showing equivalencies and relationships.

## When to Use

- Multi-state curriculum development
- Standards migration (old → new version)
- International/national alignment
- Integrated curriculum design
- Understanding standards relationships

## Crosswalk Types

### 1. State-to-State

**Example**: Texas TEKS ↔ California Standards ↔ New York Standards

**Use Cases**:
- Textbook publishers serving multiple states
- Online curriculum providers
- Relocating students/teachers

### 2. State-to-National

**Example**: State Standards ↔ Common Core ↔ NGSS

**Use Cases**:
- Understanding national framework adoption
- Supplementing state standards
- Assessment alignment

### 3. Old-to-New Version

**Example**: NGSS Draft ↔ NGSS Final
**Example**: Common Core 2010 ↔ State-adapted versions

**Use Cases**:
- Standards revisions
- Curriculum updates
- Legacy content mapping

### 4. Subject Integration

**Example**: NGSS ↔ CCSS Math ↔ CCSS ELA

**Use Cases**:
- Integrated STEM units
- Cross-curricular projects
- Literacy across content areas

### 5. International Alignment

**Example**: US Common Core ↔ UK National Curriculum ↔ IB MYP

**Use Cases**:
- International schools
- Student transfers
- Comparative education

## Crosswalk Structure

### Three Relationship Types

**1. Exact Match** (≈):
- Standards address same content/skill
- Same cognitive level
- Fully equivalent

**2. Partial Match** (⊃ or ⊂):
- One standard broader/narrower than other
- Overlapping content
- Different emphasis

**3. Related** (∼):
- Connected concepts
- Different approaches to similar ideas
- Complementary rather than equivalent

### Crosswalk Matrix

| Framework A | Relationship | Framework B | Relationship | Framework C |
|-------------|--------------|-------------|--------------|-------------|
| TEKS 7.3A | ≈ | CCSS.7.NS.A.1 | ⊃ | NY-7.NS.1a, NY-7.NS.1b |
| TEKS 7.3B | ∼ | CCSS.7.NS.A.2 | ≈ | NY-7.NS.2 |

## Mapping Methodology

### 1. Granularity Matching

**Challenge**: Standards at different grain sizes

**Solution**:
- Break broad standards into components
- Group fine-grained standards
- Note one-to-many relationships

### 2. Cognitive Level Analysis

**DOK/Bloom's Alignment**:
- Ensure equivalent cognitive demand
- Note when one framework expects higher-level thinking

### 3. Content Coverage

**Scope Analysis**:
- Identify unique content in each framework
- Note gaps and additions
- Highlight prerequisites

### 4. Assessment Emphasis

**Testing Focus**:
- Which standards heavily tested
- Assessment format differences
- Practical vs. theoretical emphasis

## Common Crosswalks

### Math: State ↔ Common Core

**Patterns**:
- Most states have Common Core-aligned or similar standards
- State variations in order of topics
- Some states added standards (financial literacy, coding)

### Science: State Standards ↔ NGSS

**Patterns**:
- NGSS three-dimensional vs. traditional standards
- Performance Expectations vs. content standards
- Engineering added in NGSS

### ELA: State ↔ Common Core

**Patterns**:
- Reading literature vs. informational text balance
- Writing genres emphasis
- Speaking/listening integration

## CLI Interface

```bash
# Two-way crosswalk
/standards.crosswalk-mapper --framework-a "Texas-TEKS-Math-7" --framework-b "Common-Core-Math-7"

# Multi-way crosswalk (3+ frameworks)
/standards.crosswalk-mapper --frameworks "TX-TEKS,CA-Standards,NY-Standards,FL-BEST" --subject "math" --grade "7"

# Subject integration
/standards.crosswalk-mapper --integrate --frameworks "NGSS-MS,CCSS-Math-6-8,CCSS-ELA-6-8"

# Version migration
/standards.crosswalk-mapper --old "State-Standards-2010" --new "State-Standards-2024" --migration-guide

# International
/standards.crosswalk-mapper --frameworks "US-CCSS-Math-7,UK-NC-Year-8,IB-MYP-Year-3" --international
```

## Output

- Crosswalk matrix/table
- Relationship codes (exact, partial, related, none)
- Unique standards in each framework
- Coverage gaps
- Migration/adoption guide
- Visual crosswalk diagram

## Composition

**Input from**: `/standards.us-state-mapper`, `/standards.subject-standards`, `/standards.international-curriculum`
**Works with**: All other standards skills
**Output to**: Integrated curriculum, multi-framework documentation

## Exit Codes

- **0**: Crosswalk created
- **1**: Framework not found
- **2**: Incompatible frameworks
- **3**: Insufficient granularity for mapping
