# Hi-C Loop Caller Comparison

Reference guide covering concordance between Hi-C loop callers, based on Wolff et al. 2022 benchmarking and individual tool characteristics.

## The Concordance Problem

Wolff et al. (2022, GigaScience) performed the most comprehensive benchmark of Hi-C loop callers to date. The critical finding:

> Loop callers **intersect by approximately 50% at most**. Different algorithms applied to the same Hi-C data produce substantially different loop sets, even when tuned to similar sensitivity levels.

This discordance is the primary motivation for the union approach in Hi-C aggregation. Any single caller misses loops that another caller recovers.

## Major Loop Callers

### HiCCUPS (Rao et al. 2014)

- **Developer**: Aiden Lab (Baylor College of Medicine)
- **Method**: Identifies enriched pixels in the contact matrix relative to local background using a donut-shaped kernel
- **Resolution**: Works best at 5kb and 10kb
- **Strengths**: Gold standard for point-source loop detection; GPU-accelerated
- **Weaknesses**: Conservative (high specificity, lower sensitivity); requires deep sequencing (>1B contacts for 5kb resolution); misses weaker loops
- **ENCODE usage**: Primary loop caller in ENCODE Hi-C pipeline

### Mustache (Roayaei Ardakany et al. 2020, 165 citations)

- **Developer**: Ay Lab (La Jolla Institute)
- **Method**: Scale-space theory with blob detection across multiple resolutions
- **Resolution**: Multi-scale (5kb to 100kb simultaneously)
- **Strengths**: Recovers more validated loops than HiCCUPS; works at multiple resolutions simultaneously; no GPU required; works with both Hi-C and Micro-C
- **Weaknesses**: More liberal calling (higher sensitivity, more potential false positives)
- **Key advantage**: Multi-scale approach avoids resolution-specific artifacts

### Fit-Hi-C / FitHiC2 (Ay et al. 2014; Kaul et al. 2020)

- **Developer**: Ay Lab
- **Method**: Statistical model of contact frequency as function of genomic distance; identifies outlier contacts
- **Resolution**: Flexible (1kb to 1Mb)
- **Strengths**: Principled statistical framework; handles distance decay properly; provides p-values and q-values
- **Weaknesses**: Calls many short-range interactions that may not be structural loops; less specific for point interactions

### HiCExplorer (Wolff et al. 2020)

- **Developer**: Manke Lab (Max Planck Institute)
- **Method**: Z-score based enrichment relative to expected contact frequency
- **Resolution**: Configurable, typically 10-50kb
- **Strengths**: Full Hi-C analysis suite; integrates with other HiCExplorer tools
- **Weaknesses**: Z-score approach sensitive to normalization method

### Chromosight (Matthey-Doret et al. 2020)

- **Developer**: Koszul Lab (Institut Pasteur)
- **Method**: Template matching using convolution with loop kernel
- **Resolution**: Flexible
- **Strengths**: Fast; pattern-based approach detects loops, borders, and stripes
- **Weaknesses**: Less commonly used in ENCODE context

## Wolff et al. 2022 Benchmark Results

### Pairwise Overlap Between Callers

| Caller A | Caller B | Overlap (A in B) | Overlap (B in A) |
|----------|----------|-----------------|-----------------|
| HiCCUPS | Mustache | ~45% | ~40% |
| HiCCUPS | FitHiC2 | ~50% | ~30% |
| HiCCUPS | HiCExplorer | ~40% | ~35% |
| Mustache | FitHiC2 | ~45% | ~35% |

Note: Exact percentages vary by dataset and parameters. The consistent finding is that **no two callers agree on more than half their loops**.

### Factors Affecting Concordance

1. **Sequencing depth**: Deeper datasets show better concordance (more power to detect weak loops)
2. **Resolution**: 10kb resolution shows better concordance than 5kb (larger bins reduce stochastic variation)
3. **Cell type**: Cell types with strong compartmentalization (e.g., GM12878) show better concordance than those with weaker structure
4. **Normalization**: KR vs ICE vs VC normalization affects each caller differently

## Implications for Union Aggregation

### Why Union Is Appropriate

1. **Different callers have different strengths**: HiCCUPS excels at strong point interactions; Mustache finds weaker but validated loops; FitHiC2 provides robust statistics
2. **False negatives are the bigger problem**: For a catalog of "what loops exist," missing real loops is worse than including a few false positives
3. **Loop Catalog precedent**: Reyna et al. (2025) created a union catalog of 4.19M loops across 1,089 datasets using this rationale

### Handling Mixed Caller Output

When merging loops from different experiments that may have used different callers:

```bash
# All loops go into the same union, regardless of which caller produced them
# The sample/experiment ID tracks provenance, not the caller
# Resolution harmonization is the critical step, not caller harmonization
```

### Confidence Annotation Accounts for Caller Variation

The confidence system (HIGH / SUPPORTED / SINGLETON) naturally handles caller discordance:
- A loop detected by multiple callers in the same experiment counts once per experiment
- A loop detected across multiple experiments (regardless of caller) gets higher confidence
- Caller-specific loops that do not replicate across experiments remain singletons

## Resolution Effects on Loop Detection

| Resolution | Loops Detected | Concordance | Best For |
|-----------|---------------|-------------|---------|
| 1 kb | Most (finest scale) | Lowest | Micro-C data, promoter-enhancer |
| 5 kb | Many | Moderate | Standard analysis, ENCODE |
| 10 kb | Moderate | Highest | Cross-study comparison |
| 25 kb | Fewest | High | Large-scale domain contacts |

**Recommendation**: When merging loops across studies, harmonize to 10kb resolution for maximum concordance, unless all datasets support 5kb resolution.

## Practical Recommendations

1. **Accept that callers disagree** -- this is a feature of loop detection, not a bug
2. **Use union approach** for catalogs ("where are loops?")
3. **Use intersection** only for high-confidence subsets needed for specific analyses
4. **Record the caller** in provenance metadata for each experiment
5. **Prefer Mustache** if re-calling loops from contact matrices (more validated loops)
6. **Prefer HiCCUPS** if using ENCODE pre-called loops (already the pipeline standard)

## References

- Wolff et al. 2022, GigaScience -- comprehensive loop caller benchmark (~50% concordance finding)
- Roayaei Ardakany et al. 2020, Genome Biology -- Mustache multi-scale loop caller (165 citations)
- Rao et al. 2014, Cell -- HiCCUPS algorithm and original loop catalog (4,900+ citations)
- Kaul et al. 2020, Nature Methods -- FitHiC2 with improved statistical model
- Reyna et al. 2025, Nucleic Acids Research -- Loop Catalog with 4.19M union loops
- Matthey-Doret et al. 2020, Nature Communications -- Chromosight pattern-based detection
