---
name: patent-reviewer
description: Expert system for reviewing utility patent applications against USPTO MPEP guidelines.
---

# Patent Creator Skill

Comprehensive patent creation system with USPTO MPEP, prior art databases, and USPTO API for complete patent application analysis.

## When to Use

Review patent applications for USPTO compliance, analyze claims/specifications/formalities, integrate prior art, get USPTO guidance, assist with patent drafting.

## Quick Review Commands

```bash
/full-review              # Complete parallel review
/review-claims            # 35 USC 112b compliance
/review-specification     # 35 USC 112a compliance
/review-formalities       # MPEP 608 compliance
/create-patent            # New patent application
```

## Available MCP Tools

### MPEP & Regulations

- `search_mpep` - Search MPEP, 35 USC, 37 CFR
- `get_mpep_section` - Get complete MPEP section by number

### Patent Search

- `search_patents_bigquery` - Search 76M+ patents
- `get_patent_bigquery` - Get full patent details
- `search_patents_by_cpc_bigquery` - Search by CPC classification

### Patent Analysis

- `review_patent_claims` - Analyze claims for 35 USC 112(b)
- `review_specification` - Check specification support (112a)
- `check_formalities` - Verify MPEP 608 compliance

### Diagram Generation

- `render_diagram` - Create diagrams from DOT code
- `create_flowchart` - Generate patent-style flowcharts
- `create_block_diagram` - Create system block diagrams
- `add_diagram_references` - Add reference numbers

## Review Workflows

### Complete Patent Creation Review (/full-review)

Runs all analyzers in **parallel** for comprehensive analysis:

**Output:**
- All compliance issues across components
- Severity ratings (critical/important/minor)
- Specific MPEP citations
- Actionable fix recommendations
- Prioritized remediation plan

### Claims-Only Review (/review-claims)

**35 USC 112(b) Compliance:**
- Antecedent basis
- Definiteness
- Claim structure
- Subjective terms
- Means-plus-function compliance

### Specification Review (/review-specification)

**35 USC 112(a) Requirements:**
- Written description
- Enablement
- Best mode
- Claim support

### Formalities Check (/review-formalities)

**MPEP 608 Compliance:**
- Abstract (50-150 words)
- Title (<=500 characters)
- Drawing references
- Required sections

## Patent Creation Workflow (/create-patent)

Complete 6-phase patent drafting (55-80 minutes):

1. **Discovery (10-15 min)** - Gather invention details
2. **Technology Analysis (5 min)** - Assess patentability (101, 102, 103)
3. **Specification Drafting (15-20 min)** - Background, summary, detailed description
4. **Claims Drafting (10-15 min)** - Independent + dependent claims
5. **Diagrams & Abstract (10-15 min)** - Block diagrams, flowcharts, abstract
6. **Automatic Validation (5-10 min)** - Runs /full-review, provides fixes

**Output:** USPTO-ready filing package with diagrams

## MPEP Research

```python
# General search
search_mpep("claim definiteness 112(b)", top_k=5)

# Filtered by source
search_mpep("enablement", source_filter="35_USC")
search_mpep("abstract", source_filter="MPEP")

# Get specific section
get_mpep_section("2173")  # Claim definiteness
```

### Common MPEP Sections

| Section | Topic |
|---------|-------|
| 608 | Formalities (abstract, title, drawings) |
| 2100 | Patentability requirements |
| 2163 | Guidelines for 35 USC 112(a) |
| 2173 | Claim definiteness (35 USC 112(b)) |

## Prior Art Integration

```python
# BigQuery search (76M+ patents)
search_patents_bigquery(
    query="neural network training",
    country="US",
    start_year=2020,
    limit=20
)

# CPC classification search
search_patents_by_cpc_bigquery(cpc_code="G06N3", limit=50)
```

**Integrate findings:**
1. Cite in Background section
2. Emphasize distinctions in Summary
3. Explain advantages in Detailed Description
4. Draft claims to avoid/distinguish
5. List in IDS

## Best Practices

**Before Review:**
- Prepare complete application
- Run /full-review
- Address critical issues first

**During Review:**
- Focus on critical issues (antecedent basis, claim support, definiteness)
- Use MPEP citations
- Iterate until compliant

**After Review:**
- Document compliance
- Final /full-review validation
- Prepare filing package

## Common Review Findings

**Critical (Must Fix):**
- Missing antecedent basis
- Claim elements unsupported
- Abstract exceeds 150 words
- Indefinite language

**Important (Should Fix):**
- Subjective terms without criteria
- Weak enablement
- Inconsistent terminology

**Minor (Optional):**
- Add example embodiments
- Strengthen best mode
- Improve claim scope

## Quick Reference

### Key Compliance Checks

| Requirement | Citation | Tool |
|-------------|----------|------|
| Antecedent basis | 35 USC 112(b) | review_patent_claims |
| Written description | 35 USC 112(a) | review_specification |
| Enablement | 35 USC 112(a) | review_specification |
| Abstract length | MPEP 608.01(b) | check_formalities |
| Title format | MPEP 606 | check_formalities |
