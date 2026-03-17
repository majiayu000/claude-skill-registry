---
name: patent-application-creator
description: Complete end-to-end patent application creation from invention disclosure to USPTO-ready filing - prior art search, claims drafting, specification writing, diagrams, compliance checking
tools: Bash, Read, Write
model: sonnet
---

# Patent Application Creator Skill

Complete end-to-end patent application creation from invention disclosure to USPTO-ready filing.

## When to Use

Invoke this skill when users ask to:
- Create a complete patent application
- Draft a provisional patent application
- Prepare a utility patent application
- Write patent claims and specification
- Generate a full patent filing package

## What This Skill Does

Orchestrates the complete patent creation workflow:

1. **Prior Art Search** → Identify existing patents
2. **Claims Drafting** → Write independent and dependent claims
3. **Specification Writing** → Create detailed description
4. **Diagram Generation** → Produce technical figures
5. **Abstract Creation** → Write concise summary
6. **Compliance Checking** → Validate USPTO requirements
7. **IDS Preparation** → List prior art for disclosure

## Complete Workflow

### Phase 1: Discovery & Research (15-30 min)

1. **Invention Interview**:
   - Get detailed invention description from user
   - Extract key features and novel aspects
   - Identify problem being solved
   - List all components/steps

2. **Prior Art Search**:
   - Use **Prior Art Search** skill (7-step methodology)
   - Find 10-20 most relevant patents
   - Document key differences
   - Assess patentability

3. **Technology Landscape**:
   - Identify CPC classifications
   - Review competing approaches
   - Find terminology used in field

**Output**: Research summary with prior art analysis

---

### Phase 2: Claims Drafting (20-40 min)

1. **Claim Strategy**:
   - Define claim scope based on prior art
   - Identify distinguishing features
   - Plan independent/dependent structure
   - Choose claim types (system, method, etc.)

2. **Independent Claims**:
   - Draft 1-3 broad independent claims
   - Use preamble-transition-body structure
   - Include all essential elements
   - Distinguish from prior art

3. **Dependent Claims**:
   - Add 10-20 dependent claims
   - Cover specific implementations
   - Add fall-back positions
   - Include preferred embodiments

4. **Claim Review**:
   - Use **Patent Claims Analyzer** skill
   - Check antecedent basis
   - Fix definiteness issues
   - Validate dependencies

**Output**: Complete claims section (20-25 claims)

---

### Phase 3: Specification Writing (40-90 min)

1. **Title**:
   - Clear, descriptive (< 500 characters)
   - Matches invention scope
   - Includes key technology terms

2. **Field of the Invention**:
   - 1-2 paragraphs
   - Describe technical field
   - Reference relevant classifications

3. **Background**:
   - Problem statement (2-3 paragraphs)
   - Limitations of existing solutions
   - Need for invention
   - Cite prior art from search

4. **Summary**:
   - High-level description (3-5 paragraphs)
   - Main features and advantages
   - How it solves the problem
   - Independent claims in prose

5. **Brief Description of Drawings**:
   - List each figure
   - One sentence per figure
   - Reference numbers introduced

6. **Detailed Description**:
   - Complete description of all embodiments
   - Multiple embodiments (preferred + variations)
   - Step-by-step for methods
   - Component-by-component for systems
   - Reference numbers throughout
   - Support ALL claim elements (35 USC 112(a))

7. **Examples/Embodiments**:
   - Specific implementations
   - Working examples
   - Alternative designs

8. **Advantages/Benefits**:
   - List key advantages
   - Explain improvements over prior art

9. **Specification Review**:
   - Use **Patent Claims Analyzer** skill (specification mode)
   - Verify all claims are supported
   - Check enablement
   - Validate completeness

**Output**: Complete specification (20-50 pages)

---

### Phase 4: Diagrams & Figures (15-30 min)

1. **Identify Figures Needed**:
   - System block diagrams
   - Method flowcharts
   - Component details
   - Alternative embodiments

2. **Generate Diagrams**:
   - Use **Patent Diagram Generator** skill
   - Create all required figures
   - Add reference numbers (10, 20, 30...)
   - Ensure clarity

3. **Figure Descriptions**:
   - Write detailed figure descriptions
   - Explain all reference numbers
   - Describe relationships between components

**Output**: 3-10 patent figures (SVG/PNG/PDF)

---

### Phase 5: Abstract & Front Matter (10-15 min)

1. **Abstract**:
   - 50-150 words (USPTO requirement)
   - Single paragraph
   - No claim limitations
   - Broad technical description

2. **Title Page Info**:
   - Inventors
   - Assignee
   - Correspondence address
   - Prior applications (if any)

3. **Cross-References**:
   - Related applications
   - Priority claims
   - Provisional references

**Output**: Complete front matter

---

### Phase 6: Compliance & Validation (15-20 min)

1. **Formalities Check**:
   - Use **Patent Claims Analyzer** skill (formalities mode)
   - Abstract length: 50-150 words
   - Title length: < 500 characters
   - Required sections present
   - Drawing references valid

2. **Claims Compliance**:
   - 35 USC 112(b) definiteness
   - Antecedent basis correct
   - No indefinite terms
   - Proper dependencies

3. **Specification Compliance**:
   - 35 USC 112(a) written description
   - Enablement complete
   - Best mode disclosed
   - All claims supported

4. **MPEP Guidance**:
   - Use **MPEP Search** skill
   - Verify format requirements
   - Check section 608 compliance
   - Review any special requirements

**Output**: Compliance report with fixes

---

### Phase 7: Final Assembly (10-15 min)

1. **Document Assembly**:
   - Title page
   - Abstract
   - Drawings (brief description)
   - Specification
   - Claims
   - Abstract (at end)

2. **IDS Preparation**:
   - List all prior art from search
   - Include publication numbers
   - Add filing/grant dates
   - Note relevance

3. **Filing Package**:
   - Specification document
   - Claims document
   - Figures (separate files)
   - IDS form data
   - Assignment (if applicable)

**Output**: USPTO-ready filing package

---

## Document Templates

### Specification Structure

```markdown
[TITLE]

FIELD OF THE INVENTION

[Technical field description]

BACKGROUND

[Problem statement and prior art]

SUMMARY

[High-level invention description]

BRIEF DESCRIPTION OF THE DRAWINGS

FIG. 1 illustrates...
FIG. 2 shows...
FIG. 3 depicts...

DETAILED DESCRIPTION

[Comprehensive description with reference numbers]

First Embodiment

[Detailed description of main embodiment]

Second Embodiment

[Alternative embodiment]

Examples

[Working examples]

ADVANTAGES

[Key benefits and improvements]

CONCLUSION

[Broad scope statement]

CLAIMS

[Claims section]
```

### Claims Structure

```
What is claimed is:

1. A [system/method/apparatus] for [purpose], comprising:
    a [first element];
    a [second element]; and
    wherein [novel relationship/function].

2. The [system/method/apparatus] of claim 1, wherein [additional limitation].

3. The [system/method/apparatus] of claim 1, wherein [alternative limitation].

...

[Continue through all claims]
```

## Quality Checklist

Before finalizing, verify:

- [ ] Prior art search completed (Top 10 documented)
- [ ] Claims drafted (1-3 independent, 10-20 dependent)
- [ ] Specification written (20+ pages)
- [ ] All claim elements supported in specification
- [ ] Diagrams created (3+ figures with reference numbers)
- [ ] Abstract written (50-150 words)
- [ ] Title created (< 500 characters)
- [ ] Antecedent basis checked (no critical issues)
- [ ] Definiteness verified (no indefinite terms)
- [ ] Enablement complete (sufficient detail)
- [ ] Formalities compliant (MPEP 608)
- [ ] IDS list prepared (all prior art included)
- [ ] Figures match description
- [ ] Reference numbers consistent
- [ ] USPTO format requirements met

## File Organization

```
patent-application/
├── 01-research/
│   ├── prior-art-search.md
│   ├── top-10-patents.md
│   └── patentability-assessment.md
├── 02-claims/
│   ├── claims-draft-v1.md
│   ├── claims-final.md
│   └── claims-analysis-report.md
├── 03-specification/
│   ├── specification-outline.md
│   ├── specification-full.md
│   └── specification-review.md
├── 04-diagrams/
│   ├── fig1-system-diagram.svg
│   ├── fig2-method-flowchart.svg
│   ├── fig3-component-detail.svg
│   └── figures-list.md
├── 05-front-matter/
│   ├── abstract.md
│   ├── title.md
│   └── bibliographic-data.md
├── 06-compliance/
│   ├── formalities-check.md
│   ├── claims-compliance.md
│   └── spec-compliance.md
└── 07-filing-package/
    ├── complete-specification.pdf
    ├── claims.pdf
    ├── drawings.pdf
    └── ids-list.md
```

## Integration with Other Skills

This workflow orchestrates:
- **Prior Art Search** skill (Phase 1)
- **Patent Claims Analyzer** skill (Phase 2, 6)
- **Patent Diagram Generator** skill (Phase 4)
- **MPEP Search** skill (Phase 6)
- **BigQuery Patent Search** skill (Phase 1)

## Estimated Timeline

**Provisional Application** (Lighter requirements):
- Research: 15 min
- Claims: 20 min
- Specification: 40 min
- Diagrams: 15 min
- **Total: ~90 minutes**

**Utility Application** (Full formal requirements):
- Research: 30 min
- Claims: 40 min
- Specification: 90 min
- Diagrams: 30 min
- Compliance: 20 min
- **Total: ~3.5 hours**

## User Interaction Points

Throughout the workflow, pause to:

1. **After Research**: Present patentability assessment, ask if should proceed
2. **After Claims**: Show draft claims, get feedback on scope
3. **After Specification Outline**: Review structure before full writing
4. **After Diagrams**: Confirm figures match invention description
5. **After Compliance**: Show any issues found, make fixes
6. **Before Final**: Present complete package for review

## Tools Available

- **Bash**: Run Python tools for search, analysis
- **Write**: Save all documents and sections
- **Read**: Load user invention descriptions, prior art
- **Grep**: Search through generated content
