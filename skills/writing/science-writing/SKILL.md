---
name: science-writing
description: Write publication-quality scientific manuscripts with structured reference management, automated DOI validation via CrossRef API, and evidence-based writing principles. Always write in full paragraphs (never bullet points). Use for research papers, reviews, and journal submissions.
allowed-tools: [Read, Write, Edit, Bash, WebFetch]
---

# Science Writing

## Overview

Science writing is the craft of communicating research with precision, clarity, and impact. This skill provides comprehensive guidance for writing publication-quality scientific manuscripts using evidence-based principles from Nature, OSU Writing Center, and leading scientific communication experts.

**Core Principle**: Write in complete, flowing paragraphs. Never submit manuscripts with bullet points outside of Methods sections (inclusion/exclusion criteria only).

## When to Use This Skill

Use this skill when:
- Writing or revising manuscript sections (Abstract, Introduction, Methods, Results, Discussion)
- Structuring research papers using IMRAD or venue-specific formats
- Managing references with DOI validation and CrossRef API metadata retrieval
- Formatting citations in any style (APA, AMA, Vancouver, Chicago, IEEE, ACS, NLM)
- Creating publication-quality figures and tables
- Applying reporting guidelines (CONSORT, STROBE, PRISMA, STARD, ARRIVE, CARE)
- Adapting manuscripts for different target venues (Nature/Science, medical journals, ML conferences)
- Ensuring reproducibility and scientific rigor
- Addressing reviewer comments

## Key Features

### 1. Evidence-Based Writing Principles

Based on research from Nature Masterclasses, OSU Writing Guide, and scientific communication studies:

**Clarity Over Complexity**
- Use precise, unambiguous language
- Define technical terms at first use
- Maintain logical flow within and between paragraphs
- Active voice when it improves readability

**Conciseness Respects Time**
- Eliminate redundant phrases ("due to the fact that" → "because")
- Use strong verbs instead of noun+verb combinations ("analyze" not "perform an analysis")
- Remove unnecessary intensifiers and throat-clearing phrases
- Keep sentences 15-20 words average (field-dependent)

**Accuracy Builds Credibility**
- Report exact values with appropriate precision
- Use consistent terminology throughout
- Distinguish observations from interpretations
- Match precision to measurement capability

**Objectivity Maintains Integrity**
- Present results without bias
- Acknowledge conflicting evidence
- Avoid emotional or evaluative language
- Use appropriate hedging ("suggests" not "proves" for correlational data)

### 2. Structured Reference Management with CrossRef API

**Automated DOI Validation and Metadata Retrieval**

This skill includes `scripts/crossref_validator.py` for:
- Validating DOIs against CrossRef database
- Retrieving complete citation metadata (authors, title, journal, year, DOI)
- Checking title accuracy and completeness
- Formatting references in multiple citation styles
- Detecting missing or incorrect DOIs

**Usage:**
```bash
python scripts/crossref_validator.py --doi "10.1038/d41586-018-02404-4"
python scripts/crossref_validator.py --title "How to write a first-class paper"
python scripts/crossref_validator.py --validate-file references.bib
```

**Always Include DOIs**
- Required for all journal articles when available
- Use CrossRef API to verify and retrieve DOIs for papers missing them
- Format DOIs as URLs: `https://doi.org/10.xxxx/xxxxx`
- Check that DOI links resolve correctly

**Reference Quality Standards**
- Prefer peer-reviewed journal articles over preprints
- Cite primary sources (not secondary citations)
- Use recent sources (within 5-10 years for active fields, 2-3 years for ML)
- Maintain <20% self-citations
- Verify all citations against original sources

### 3. IMRAD Structure for Maximum Impact

**Introduction** (10-20% of manuscript)
- Establish broad context and importance
- Review relevant prior research
- Identify specific knowledge gap
- State clear research question or hypothesis

**Methods** (20-30% of manuscript)
- Provide sufficient detail for replication
- Describe study design, participants, procedures
- Specify statistical analysis with justification
- Include ethical approval statements

**Results** (25-35% of manuscript)
- Present findings objectively without interpretation
- Integrate with figures and tables
- Include statistical significance, effect sizes, and confidence intervals
- Report all tested hypotheses (not just significant results)

**Discussion** (25-40% of manuscript)
- Interpret findings in context of prior research
- Propose mechanisms or explanations
- Acknowledge limitations honestly and specifically
- Suggest future research directions
- State practical implications

**For details on IMRAD structure**: See `references/imrad_structure.md`

### 4. Venue-Specific Adaptation

Different venues have distinct expectations for style, structure, and emphasis:

| Venue Type | Word Count | Focus | Methods Detail | Writing Style |
|------------|-----------|-------|----------------|---------------|
| **Nature/Science** | 2,000-4,500 | Broad significance | Supplement | Engaging, accessible |
| **Medical (NEJM/Lancet)** | 2,700-3,500 | Clinical outcomes | Main text | Conservative, precise |
| **Field journals** | 3,000-6,000 | Technical depth | Main text | Formal, comprehensive |
| **ML conferences** | ~6,000 (8 pages) | Novel contribution | Concise main text | Direct, technical |

**Key Adaptations by Venue:**

**Nature/Science:**
- Lead with broad significance
- Accessible to non-specialists
- Story-driven organization
- Methods in supplement
- Strong visual presentation

**Medical Journals:**
- Clinical relevance prominent
- Strict IMRAD structure
- CONSORT/STROBE compliance
- Primary outcome first in Results
- Conservative interpretation

**ML Conferences (NeurIPS/ICML/ICLR):**
- Numbered contributions in Introduction
- Pseudocode and mathematical notation
- Extensive ablation studies
- Brief conclusion with limitations
- ArXiv preprints acceptable

**For complete venue adaptation guidance**: See `references/writing_principles.md` and `references/imrad_structure.md`

### 5. Two-Stage Writing Process

**Stage 1: Create Structured Outlines**
1. Gather literature and data
2. Create bullet-point outline with:
   - Main arguments or findings
   - Key studies to cite (with DOIs)
   - Data points and statistics
   - Logical flow and transitions
3. These bullets are scaffolding—NOT the final manuscript

**Stage 2: Convert to Flowing Prose**
1. Transform bullets into complete sentences
2. Add transitions between ideas (however, moreover, subsequently)
3. Integrate citations naturally within sentences
4. Expand with context and explanation
5. Ensure logical flow from sentence to sentence
6. Vary sentence structure for engagement

**Example Transformation:**

**Outline (Stage 1):**
```
- Background: AI in drug discovery gaining traction
  * Cite recent reviews (Smith 2023, Jones 2024)
  * Traditional methods are slow and expensive
- Gap: Limited application to rare diseases
  * Only 2 prior studies (Lee 2022, Chen 2023)
  * Small datasets remain a challenge
```

**Final Prose (Stage 2):**
```
Artificial intelligence approaches have gained significant traction in drug
discovery pipelines over the past decade (Smith, 2023; Jones, 2024). While these
computational methods show promise for accelerating the identification of therapeutic
candidates, traditional experimental approaches remain slow and resource-intensive,
often requiring years of laboratory work and substantial financial investment.
However, the application of AI to rare diseases has been limited, with only two
prior studies demonstrating proof-of-concept results (Lee, 2022; Chen, 2023).
The primary obstacle has been the scarcity of training data for conditions affecting
small patient populations.
```

### 6. Citation Styles and Formatting

Support for all major citation styles with automated formatting:

**Numbered Styles:**
- **AMA**: Superscript numbers (medical research)
- **Vancouver**: Brackets [1] (biomedical sciences)
- **IEEE**: Brackets [1] (engineering, computer science)
- **ACS**: Superscript or numbered (chemistry)

**Author-Date Styles:**
- **APA**: (Smith, 2023) - psychology, social sciences
- **Chicago**: (Smith 2023) - humanities, some sciences
- **Cell**: (Smith et al., 2023) - life sciences

**For complete citation formatting**: See `references/citation_styles.md`

### 7. Scientific Nomenclature Standards

**Microbial Nomenclature (International Committee on Systematics of Prokaryotes):**
- Genus capitalized, species lowercase, both italicized: *Escherichia coli*
- After first use, abbreviate genus: *E. coli*
- "sp." for single unnamed species; "spp." for multiple
- Infrasubspecific terms in roman text: *Staphylococcus aureus* subsp. *aureus*

**Genetic Nomenclature:**
- Gene names: Three italicized letters (*his*, *lac*, *gfp*)
- Phenotypes: Non-italicized with superscripts (His+, Lac-, GFP+)
- Genotypes: Italicized mutations (*hisA*, *lacZ*, *gfp*)
- Alleles: With numbers (*hisG251*)
- Deletions: Δ symbol (Δ*lacZ*)
- Insertions: :: notation (*lacZ::Tn10*)

**Viral Nomenclature (International Committee on Taxonomy of Viruses):**
- English common names (not Latinized binomials)
- Example: "severe acute respiratory syndrome coronavirus 2" (SARS-CoV-2)

**Chemical Nomenclature (IUPAC):**
- Systematic names for novel compounds
- Common names for well-known substances
- SMILES or InChI for database submissions

**For field-specific guidance**: See sections 9 (Field-Specific Language) in full skill documentation

### 8. Reporting Guidelines by Study Type

Ensure completeness and transparency:

| Study Type | Guideline | Key Requirements |
|-----------|-----------|------------------|
| Randomized controlled trials | CONSORT | Flow diagram, randomization, blinding |
| Observational studies | STROBE | Study design, participants, variables, bias |
| Systematic reviews | PRISMA | Search strategy, selection, quality assessment |
| Diagnostic accuracy | STARD | Patient selection, index test, reference standard |
| Prediction models | TRIPOD | Development/validation, model specification |
| Animal research | ARRIVE | Species, housing, experimental procedures |
| Case reports | CARE | Patient information, timeline, outcomes |

**For complete reporting guidelines**: See `references/reporting_guidelines.md`

### 9. Figures and Tables

**Design Principles:**
- Self-explanatory with complete captions
- Consistent formatting and terminology
- Label all axes, columns, rows with units
- Include sample sizes (n) and statistical annotations
- One figure/table per 1000 words guideline

**When to Use:**
- **Tables**: Precise numerical data, multiple variables requiring exact values
- **Figures**: Trends, patterns, relationships, comparisons best understood visually

**Common Figure Types:**
- Bar graphs: Comparing discrete categories
- Line graphs: Showing trends over time
- Scatterplots: Displaying correlations
- Box plots: Showing distributions and outliers
- Heatmaps: Visualizing matrices and patterns

**For detailed guidance**: See `references/figures_tables.md`

### 10. Common Pitfalls to Avoid

**Top Rejection Reasons:**
1. Inappropriate, incomplete, or insufficiently described statistics
2. Over-interpretation of results or unsupported conclusions
3. Poorly described methods affecting reproducibility
4. Small, biased, or inappropriate samples
5. Poor writing quality or difficult-to-follow text
6. Inadequate literature review or context
7. Unclear or poorly designed figures and tables
8. Failure to follow reporting guidelines

**Writing Quality Issues:**
- Mixing tenses inappropriately
- Excessive jargon or undefined acronyms
- Paragraph breaks disrupting logical flow
- Missing transitions between sections
- Inconsistent notation or terminology
- Bullet points in Results/Discussion (use paragraphs)

## Workflow for Manuscript Development

**Planning Phase**
1. Identify target journal and review author guidelines
2. Determine applicable reporting guideline
3. Outline manuscript structure (IMRAD or venue-specific)
4. Plan figures and tables as the data story backbone

**Drafting Phase** (Use two-stage process for each section)
1. Create figures and tables first (core data story)
2. For each section:
   - First: Create bullet-point outline with literature/data
   - Second: Convert bullets to flowing paragraphs with transitions
3. Draft in this order:
   - Methods (often easiest first)
   - Results (describing figures/tables objectively)
   - Discussion (interpreting findings)
   - Introduction (setting up research question)
   - Abstract (synthesizing complete story)
   - Title (concise and descriptive)

**Revision Phase**
1. Check logical flow and "red thread" throughout
2. Verify terminology and notation consistency
3. Ensure figures/tables are self-explanatory
4. Confirm adherence to reporting guidelines
5. Validate all citations with CrossRef API
6. Check word counts for each section
7. Proofread for grammar, spelling, and clarity

**Final Preparation**
1. Format according to journal requirements
2. Prepare supplementary materials
3. Write cover letter highlighting significance
4. Complete submission checklists
5. Gather required statements (funding, COI, data availability, ethics)

## Integration with CrossRef API for Reference Management

### Validating and Enriching References

The CrossRef API integration provides:

**DOI Validation:**
```bash
# Validate a single DOI
python scripts/crossref_validator.py --doi "10.1038/nature12373"

# Validate multiple DOIs from a file
python scripts/crossref_validator.py --validate-file my_references.txt
```

**Title Verification:**
```bash
# Look up complete metadata by title
python scripts/crossref_validator.py --title "CRISPR-Cas9 genome editing"

# Verify title matches DOI
python scripts/crossref_validator.py --doi "10.1126/science.1231143" --check-title
```

**Automated Reference Formatting:**
```bash
# Generate formatted references in multiple styles
python scripts/crossref_validator.py --doi "10.1038/nature12373" --style vancouver
python scripts/crossref_validator.py --doi "10.1038/nature12373" --style apa
```

**Batch Processing:**
```bash
# Process bibliography and report missing/incorrect DOIs
python scripts/crossref_validator.py --audit-bibliography references.bib --output report.txt
```

### Best Practices for Reference Management

1. **Always verify DOIs**: Use CrossRef API to validate before submission
2. **Check title accuracy**: Ensure titles are complete and correctly formatted
3. **Include all metadata**: Authors, year, journal, volume, pages, DOI
4. **Use persistent DOI URLs**: Format as `https://doi.org/10.xxxx/xxxxx`
5. **Verify link resolution**: Test that DOIs resolve to correct articles
6. **Update preprints**: Replace arXiv citations with published versions when available
7. **Maintain currency**: Check for retractions or corrections via CrossRef

## Verb Tense Guidelines

| Section | Tense | Usage |
|---------|-------|-------|
| Abstract - Background | Present/past | Present for facts, past for prior studies |
| Abstract - Methods | Past | "We recruited...", "Participants completed..." |
| Abstract - Results | Past | "The intervention reduced..." |
| Abstract - Conclusions | Present | "These findings suggest..." |
| Introduction - Background | Present | "Exercise improves health..." |
| Introduction - Prior work | Past | "Smith et al. found..." |
| Methods | Past | "We measured...", "Samples were collected..." |
| Results | Past | "Mean age was 45 years..." |
| Discussion - Your findings | Past | "We found that..." |
| Discussion - Interpretation | Present | "This suggests...", "These data indicate..." |

**For comprehensive tense guidance**: See `references/writing_principles.md`

## Resources and Supporting Files

This skill includes comprehensive reference files:

- `references/imrad_structure.md`: Detailed IMRAD format and venue-specific variations
- `references/citation_styles.md`: Complete citation style guides (APA, AMA, Vancouver, Chicago, IEEE, ACS, NLM)
- `references/figures_tables.md`: Best practices for data visualization
- `references/reporting_guidelines.md`: Study-specific reporting standards with checklists
- `references/writing_principles.md`: Core principles of scientific communication with venue-specific adaptations

- `scripts/crossref_validator.py`: CrossRef API integration for DOI validation and metadata retrieval
- `examples/`: Example manuscripts showing proper structure and style

Load these references as needed when working on specific aspects of scientific writing.

## Key Reminders

1. **Always write in complete paragraphs** - bullet points are for planning only
2. **Validate all DOIs with CrossRef API** - ensure completeness and accuracy
3. **Match writing style to target venue** - adapt tone, length, and emphasis
4. **Follow two-stage writing process** - outline first, then convert to prose
5. **Apply appropriate reporting guidelines** - ensure transparency and completeness
6. **Use consistent terminology throughout** - avoid synonym variation for key terms
7. **Distinguish observations from interpretations** - be clear about what data show vs. what you infer
8. **Acknowledge limitations specifically** - not generic statements like "larger sample needed"

---

**Evidence Base:**

This skill synthesizes guidance from:
- Nature Masterclasses: "How to write a first-class paper" (Gewin, 2018)
- Oregon State University Microbiology Writing Guide (scientific style standards)
- International Committee of Medical Journal Editors (ICMJE) recommendations
- EQUATOR Network reporting guidelines
- American Medical Association Manual of Style (11th ed.)
- Publication Manual of the American Psychological Association (7th ed.)
- Leading scientific communication research

**CrossRef API Documentation:**
- API endpoint: https://api.crossref.org/works/
- Rate limits: 50 requests/second for polite pool (with mailto in User-Agent)
- Full documentation: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
