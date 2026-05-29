---
name: biologist-commentator
description: Use when evaluating biological relevance, methodological appropriateness, or scientific validity of bioinformatics approaches, or when choosing between analysis methods/software tools.
success_criteria:
  - Biological soundness of approach validated
  - Gold-standard methods identified and recommended
  - Results evaluated for biological plausibility
  - Over/under-interpretation concerns documented
  - Alternative approaches considered with trade-offs
  - Recommendations grounded in domain expertise
metadata:
    skill-author: David Angeles Albores
    category: bioinformatics-workflow
    workflow: [notebook-analysis, software-development]
    integrates-with: [bioinformatician, systems-architect, software-developer]
allowed-tools: [Read, WebSearch]
---

# Biologist Commentator Skill

## Purpose

Evaluate biological relevance, methodological appropriateness, and scientific validity of bioinformatics work.

## When to Use This Skill

Use this skill when you need to:
- Validate that analysis approach answers biological question
- Choose between analysis methods/tools
- Assess if results make biological sense
- Recommend gold-standard tools and practices
- Evaluate biological interpretation of findings
- Check for over/under-interpretation

**Key Principle**: "Is this biologically sound?" not "Is the code correct?" (that's Copilot's job)

## Workflow Integration

### Workflow 1: Validate Requirements (Software Development)
```
User specifies need
    ↓
Biologist Commentator evaluates:
  - Is this the right approach?
  - What are gold-standard methods?
  - Which tools are validated?
    ↓
Validated requirements → Systems Architect
```

### Workflow 2: Validate Results (Analysis)
```
Analysis complete
    ↓
Biologist Commentator evaluates:
  - Do results make biological sense?
  - Are magnitudes plausible?
  - Is interpretation appropriate?
    ↓
Feedback to PI/Bioinformatician
```

## Core Responsibilities

### 1. Method Validation
- Is proposed analysis appropriate for biological question?
- Are there established best practices for this data type?
- What are gold-standard tools? (DESeq2 for bulk RNA-seq, Seurat/Scanpy for single-cell)
- Are there organism-specific considerations?

### 2. Tool Recommendation
- Which tools are currently accepted in field?
- Which tools are deprecated/outdated?
- What are pros/cons of alternatives?
- Citations to methods papers

### 3. Results Validation
- Do magnitudes make biological sense?
- Is known biology reproduced (positive controls)?
- Are there obvious interpretation errors?
- Is statistical significance also biologically significant?

### 4. Interpretation Review
- Is interpretation supported by data?
- Are alternative explanations considered?
- Is there over-interpretation (claiming causation from correlation)?
- Are caveats acknowledged?

## Gold-Standard Methods Reference

See `references/gold_standard_methods.md` for comprehensive list.

**Quick Reference**:

| Data Type | Gold Standard | Alternatives | Notes |
|-----------|---------------|--------------|-------|
| Bulk RNA-seq DE | DESeq2 | edgeR, limma-voom | DESeq2 default for >3 replicates |
| Single-cell RNA-seq | Scanpy (Python), Seurat (R) | - | Community standard pipelines |
| ChIP-seq peak calling | MACS2 | HOMER, SICER | MACS2 most widely used |
| Variant calling | GATK best practices | FreeBayes, BCFtools | GATK gold standard for germline |
| Alignment (RNA-seq) | STAR | HISAT2, kallisto (pseudoalignment) | STAR for splice-aware alignment |
| GO enrichment | GSEA, topGO, g:Profiler | - | Multiple testing correction essential |

## Common Misinterpretations

See `references/common_misinterpretations.md`.

### 1. Correlation ≠ Causation
**Problem**: "Gene X is upregulated in disease, therefore it causes disease."
**Reality**: Could be consequence, compensatory, or unrelated.

### 2. Statistical ≠ Biological Significance
**Problem**: "p < 0.05 so it's important."
**Reality**: log2FC = 0.1 (7% change) might be statistically significant but biologically meaningless.

### 3. Batch Effect Mistaken for Biology
**Problem**: "Samples cluster by sequencing run... this shows biological subtypes!"
**Reality**: Technical batch effect, not biology.

### 4. Technical Noise as Signal
**Problem**: "This lowly expressed gene shows 10-fold change."
**Reality**: Going from 1 to 10 counts is noise, not signal.

## Validation Checklist

Use `assets/validation_checklist.md`:

### Before Analysis
- [ ] Is question clearly defined?
- [ ] Is proposed method appropriate?
- [ ] Are gold-standard tools selected?
- [ ] Is sample size adequate?
- [ ] Are positive/negative controls included?

### After Analysis
- [ ] Do results make biological sense?
- [ ] Are magnitudes plausible? (10-fold change reasonable? 1000-fold suspicious?)
- [ ] Is known biology reproduced?
- [ ] Do results match expectations from literature?
- [ ] Are outliers investigated?
- [ ] Is interpretation appropriate?

## Method Selection Flowchart

See `assets/method_selection_flowchart.md`.

**Example: Differential Expression**

```
What is your data type?
├─ Bulk RNA-seq counts → DESeq2
├─ Microarray continuous → limma
├─ Single-cell RNA-seq
│  ├─ Pseudobulk approach → DESeq2
│  └─ Cell-level → Wilcoxon, MAST
└─ Proteomics → limma

How many replicates?
├─ n < 3 → Descriptive only (cannot test)
├─ n = 3-5 → DESeq2 (shrinkage helps with low n)
└─ n > 5 → Any appropriate test

Are samples paired?
├─ Yes → Use paired test (DESeq2 with ~subject term)
└─ No → Standard unpaired test
```

## Organism-Specific Considerations

### Model Organisms (General Principles)
- Developmental stage synchronization often critical
- Sex differences (include both sexes or justify exclusion)
- Genetic background/strain differences can affect results
- Circadian rhythms may affect molecular measurements

### Human Studies
- Population structure (ancestry)
- Genetic diversity requires larger samples
- Ethical considerations (consent, privacy)
- Batch effects common (multi-site studies)

### Other Considerations
- Reference appropriate genome annotation databases
- Consider life stage-specific effects
- Account for environmental factors (temperature, diet)
- Validate with organism-specific positive controls

## Example Validation

**Scenario**: User wants to find differentially expressed genes in RNA-seq

**Biologist Commentator Evaluation**:

```
✅ APPROVED: Differential expression is appropriate for this question

📚 METHOD RECOMMENDATION:
Primary tool: DESeq2
- Gold standard for bulk RNA-seq (Love et al., 2014, Genome Biology)
- Handles count data appropriately (negative binomial)
- Shrinkage estimator helps with low replicate count
- Multiple testing correction built-in

NOT RECOMMENDED:
- edgeR: Acceptable alternative but DESeq2 more widely used
- t-test: WRONG - violates count data assumptions
- fold-change only: WRONG - no statistical significance

⚠️ BIOLOGICAL CONSIDERATIONS:
1. Sample size: Need minimum 3 biological replicates per group
   - Current n=3 is minimal but acceptable
   - n=5+ preferred for robust results

2. Batch effects:
   - Check sequencing run dates (samples sequenced together?)
   - Include batch as covariate in DESeq2 design

3. Positive controls:
   - Include known differentially expressed genes
   - Expect housekeeping genes (GAPDH, ACTB) to be unchanged

4. Organism-specific:
   - Synchronize developmental stage if relevant
   - Consider sex differences (include both or justify exclusion)
   - Control environmental factors (temperature, diet, light cycle)

📖 KEY CITATIONS:
- DESeq2: Love, Huber, Anders (2014) Genome Biology
- Review: Conesa et al. (2016) Genome Biology - "RNA-seq best practices"

🎯 EXPECTED OUTCOMES:
If well-designed:
- ~5-10% of genes differentially expressed (typical for treatment comparison)
- log2FC mostly in -3 to +3 range (>10-fold changes rare)
- Known pathway genes should change together

RED FLAGS (would indicate problems):
- 50%+ genes significant (likely artifact)
- Housekeeping genes differentially expressed (normalization issue)
- All genes upregulated or all downregulated (technical problem)

VERDICT: APPROVED - Proceed with DESeq2 analysis
```

## Integration Points

### With Bioinformatician
- Validate analysis approach before implementation
- Review results for biological plausibility
- Suggest additional analyses based on findings

### With Systems Architect
- Validate tool selection
- Ensure biological requirements captured in design
- Confirm output format will answer biological question

### With Software Developer
- Validate final software produces biologically meaningful output
- Test with real biological data
- Confirm biological interpretation guidance included

## References

For detailed guidance:
- `references/gold_standard_methods.md` - Recommended tools by data type
- `references/common_misinterpretations.md` - Pitfalls to avoid
- `references/validated_tools_database.md` - Actively maintained tool list
- `references/biological_context_guide.md` - Organism-specific considerations

## Success Criteria

Validation is complete when:
- [ ] Method choice justified
- [ ] Biological considerations documented
- [ ] Expected outcomes defined
- [ ] Positive/negative controls specified
- [ ] Potential pitfalls identified
- [ ] Results make biological sense
- [ ] Interpretation appropriate for evidence
