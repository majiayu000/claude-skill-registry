---
name: publication-trust
description: Assess the scientific integrity and trustworthiness of publications before relying on their findings. Use this skill whenever evaluating a paper for a workflow, citing a study, building an analysis on published methods, or when a user asks about the reliability of a study. Checks for formal retractions, corrections, expressions of concern, and — critically — informal contradictions where subsequent studies failed to reproduce key findings. Integrates with PubMed, bioRxiv, and Consensus to provide a trust assessment. Use this skill for ANY publication evaluation, retraction checking, author reliability assessment, or when a user says "can I trust this paper", "is this study reliable", "has this been refuted", or "check this publication".
---

# Publication Trust Assessment

Evaluate the scientific integrity and reliability of publications before building analyses on their findings.

## When to Use

- User wants to evaluate the reliability and reproducibility of a genomics publication
- User asks about "publication quality", "reproducibility", "trust assessment", or "paper evaluation"
- User needs to check if a paper follows ENCODE data standards and best practices
- User wants to verify that cited datasets, tools, and methods meet community standards
- Example queries: "is this paper's ChIP-seq analysis trustworthy?", "evaluate the methods in this genomics paper", "check if this study follows ENCODE standards"

## Why This Matters

Not all published findings are reliable. Problems range from formal retractions (data fabrication, image manipulation) to informal contradictions where independent groups fail to reproduce key claims. In genomics and computational biology, building pipelines or analyses on unreliable findings wastes resources and propagates errors.

**The problem is not always obvious.** Formal retractions are rare compared to the number of problematic papers. More commonly:
- A subsequent study contradicts the key finding without triggering a retraction
- An erratum quietly corrects a critical result
- The original authors publish a "correction" that substantially changes conclusions
- Independent groups fail to replicate and publish their negative results

This skill provides a systematic approach to detecting these issues.

## Trust Assessment Framework

### Trust Levels

| Level | Label | Meaning |
|-------|-------|---------|
| 5 | **High confidence** | No issues found; replicated by independent groups |
| 4 | **Standard** | No issues found; not yet independently replicated |
| 3 | **Caution advised** | Minor corrections, errata, or partial contradictions exist |
| 2 | **Reliability concerns** | Key findings contradicted by independent study, or expression of concern issued |
| 1 | **Compromised** | Retracted, or key findings refuted with evidence of methodological problems |

**Default trust level is 4** (standard) — absence of evidence is not evidence of absence. A paper starts at "standard" and moves up with independent replication or down with identified issues.

## Step 1: Gather Publication Metadata

For any publication being assessed, retrieve full metadata:

```
get_article_metadata(pmids=["PMID"])
```

Record:
- **article_types**: Check for "Retracted Publication", "Published Erratum", "Expression of Concern"
- **authors**: Note corresponding author and senior author (last position)
- **journal**: Impact factor context (high-profile journals ≠ automatic reliability)
- **publication_date**: Older papers have had more time for replication/refutation

If starting from a DOI:
```
convert_article_ids(ids=["DOI"], id_type="doi")
```

## Step 2: Check Formal Integrity Markers

### 2a. Retraction Status

Search PubMed for retraction notices linked to this paper:

```
search_articles(query="PMID[PMID] AND (Retracted Publication[pt] OR Retraction of Publication[pt])")
```

Also check the `article_types` field from Step 1 — if it contains "Retracted Publication", the paper has been formally retracted.

**If retracted → Trust Level 1 (Compromised)**

### 2b. Errata and Corrections

Search for corrections:

```
search_articles(query="PMID[PMID] AND (Published Erratum[pt] OR Correction[pt])")
```

Errata can be minor (typo in a table) or major (recalculated results that change conclusions). Read the erratum to distinguish:
- **Minor**: Trust level unchanged
- **Major** (changes key results or conclusions): Trust Level 3 (Caution advised)

### 2c. Expression of Concern

```
search_articles(query="PMID[PMID] AND Expression of Concern[pt]")
```

An Expression of Concern from a journal editor indicates an active investigation. **Trust Level 2 (Reliability concerns)** until resolved.

## Step 3: Check for Contradicting Publications

This is the most important and most nuanced step. Many problematic findings are never formally retracted — they are contradicted by subsequent independent work.

### 3a. Find Citing Articles

```
find_related_articles(pmids=["PMID"], link_type="pubmed_pubmed", max_results=50)
```

This returns computationally similar articles. From these, search for contradiction signals.

### 3b. Search for Contradiction Signals

Search PubMed for articles that cite the original AND contain contradiction language:

```
search_articles(query="\"[key claim from title]\" AND (\"fail to replicate\" OR \"unable to reproduce\" OR \"does not\" OR \"do not support\" OR \"contradicts\" OR \"challenges\" OR \"reanalysis\" OR \"re-analysis\" OR \"not reproducible\" OR \"could not confirm\")")
```

Also search with the first author's last name + key topic terms:

```
search_articles(query="[FirstAuthor] [KeyTopic] AND (Comment[pt] OR Letter[pt] OR \"fail\" OR \"does not\")")
```

### 3c. Search Academic Databases

Use Consensus to find contradicting evidence:

```
consensus_search(query="does [key claim from paper] replicate? contradiction evidence")
```

### 3d. Check bioRxiv for Preprints

Contradictions sometimes appear first as preprints:

```
search_preprints(category="[relevant category]", date_from="[pub date]", date_to="[today]")
```

### 3e. Evaluate Contradictions

Not every disagreement is a refutation. Assess:

| Factor | Strengthens contradiction | Weakens contradiction |
|--------|--------------------------|----------------------|
| Independent lab | Yes — different group, different reagents | Same group correcting themselves (may be honest science) |
| Sample size | Larger sample in contradicting study | Smaller sample or different model system |
| Methodology | Direct replication attempt | Different methodology that may explain discrepancy |
| Specificity | Contradicts the specific key claim | Disagrees on secondary finding |
| Mechanism | Provides alternative explanation with evidence | Simply fails to replicate without explanation |

**If key finding is contradicted by independent group with stronger methodology → Trust Level 2**

## Step 4: Author and Group Assessment

### 4a. Check Author Track Record

If a contradiction or retraction is found, check whether the authors have other problematic publications:

```
search_articles(query="[SeniorAuthor][Author] AND Retracted Publication[pt]")
```

**A pattern of retractions from the same group is a stronger signal than a single incident.**

### 4b. Contextual Notes

When flagging author concerns, use measured language:
- "Publications from this group have been subject to independent contradiction"
- "A previous study from this corresponding author was contradicted by [citation]"
- "This group's findings in [area] have not been independently replicated"

**Never use**: fabrication, fraud, doctored, liar, shady, dishonest — unless a formal investigation has published findings using those terms. Stick to what the published record shows.

## Step 5: Generate Trust Report

Present findings in a structured format:

```
## Publication Trust Assessment

**Paper**: [Title] ([Journal], [Year])
**PMID**: [PMID] | **DOI**: [DOI]
**Authors**: [First Author] ... [Senior Author]

### Trust Level: [X/5] — [Label]

### Formal Markers
- Retraction: None / Yes (date, reason)
- Corrections: None / [count] ([minor/major])
- Expression of Concern: None / Yes (date)

### Contradicting Evidence
- [Citation of contradicting paper] — [brief description of contradiction]
- Independent replication: Yes/No/Unknown

### Author Context
- [Any relevant notes about author track record]

### Recommendation
- [Clear guidance on whether to rely on this paper's findings]
```

## Step 6: Integration with Other Skills

When this skill identifies a trust issue, the finding should propagate:

- **cite-encode**: Flag compromised papers in citation lists
- **quality-assessment**: Downweight methods from compromised sources
- **variant-annotation**: Note if variant-gene associations rely on compromised evidence
- **disease-research**: Flag if disease mechanisms depend on contradicted findings
- **regulatory-elements**: Note if regulatory element classifications cite problematic work
- **data-provenance**: Record trust assessment in provenance chain

## Examples

### Example 1: Informal Contradiction (Islet Biology)

**Original**: Li et al. 2016, Cell — "Artemisinins Target GABA Receptor Signaling and Impair Alpha Cell Identity" (Kubicek lab)
- Claimed artemisinins convert alpha cells to beta cells via GABA receptor signaling
- High-profile publication in Cell

**Contradicting**: van der Meulen et al. 2017, Cell Metabolism — "Artemether Does Not Turn Alpha Cells into Beta Cells" (Huising lab)
- Direct replication attempt by independent group
- Found no evidence of alpha-to-beta transdifferentiation
- Showed artemether actually suppresses Ins2 expression 100-fold and impairs beta cell function
- Concluded artemisinins cause general dedifferentiation, not directed transdifferentiation

**Trust Level: 2 (Reliability concerns)** — Key finding directly contradicted by independent group using primary cells (vs. cell lines in original).

**Author context**: When encountering other publications from this group, note that a previous high-profile finding was independently contradicted.

### Example 2: Formal Retraction

**Any paper with** `article_types` **containing** "Retracted Publication":
- **Trust Level: 1 (Compromised)** — No further analysis needed
- Note retraction reason if available
- Check for other retractions from same group

### Example 3: Statistical Reanalysis Leading to Retraction

**Original**: Potti et al. 2006, Nature Medicine — Genomic signatures predicting individual patient chemotherapy response. Used microarray data to build classifiers for drug sensitivity.

**Contradicting**: Baggerly & Coombes 2009, Annals of Applied Statistics — Independent reanalysis found simple off-by-one indexing errors, mislabeled cell lines, and reversed sensitive/resistant labels. The genomic signatures were artifacts of data handling mistakes, not biology.

**Outcome**: Clinical trials based on the signatures were halted. The paper was retracted in 2011. Senior author had multiple subsequent retractions.

**Trust Level: 1 (Compromised)** — Statistical reanalysis using the original data conclusively demonstrated methodological errors. This case illustrates why reanalysis (using the same data to reach different conclusions) is the strongest form of contradiction — it eliminates methodology differences as an explanation.

## User Override

If the user reviews a flagged paper and determines the contradiction doesn't apply (e.g., different model system, different question), they can override:

- "Actually, that paper doesn't refute this finding because [reason]"
- Update trust level accordingly and note the user's reasoning in the assessment

Trust assessments are living documents — they should be updated as new evidence emerges.

## Walkthrough: Verifying Literature Claims Before ENCODE Analysis

**Goal**: Validate key literature claims that inform your ENCODE analysis pipeline — ensuring you're building on solid scientific ground before investing analysis effort.
**Context**: Genomics analysis choices (peak callers, normalization methods, quality thresholds) are often justified by citing papers. This skill verifies those citations are accurate and current.

### Step 1: Identify claims to verify

Before running a ChIP-seq analysis, you might rely on these claims:
1. "MACS2 is the gold standard peak caller for ChIP-seq" — is this still true?
2. "FRiP >= 1% indicates acceptable ChIP-seq quality" — where did this threshold come from?
3. "IDR < 0.05 ensures reproducible peaks" — what's the original source?

### Step 2: Verify claim 1 — MACS2 as gold standard

Search PubMed for the original MACS2 publication and recent benchmarks:
```
search_articles(query="MACS2 peak calling benchmark ChIP-seq", max_results=5, sort="relevance")
```

Key findings:
- Zhang et al. 2008 (PMID: 18798982) — original MACS paper, 12,000+ citations
- Recent benchmarks (2023-2024) confirm MACS2 remains competitive but note SEACR performs better for CUT&RUN data
- **Verdict**: Claim is VALID for ChIP-seq but NOT for CUT&RUN/CUT&Tag

### Step 3: Verify claim 2 — FRiP threshold

```
search_articles(query="Landt 2012 ChIP-seq quality guidelines ENCODE", max_results=3)
```

Key findings:
- Landt et al. 2012 (PMID: 22955991) — ENCODE ChIP-seq guidelines
- FRiP >= 1% is indeed the ENCODE standard
- **Verdict**: Claim is VALID. Source: Landt et al. 2012, Genome Research

### Step 4: Track verified experiments with literature provenance

```
encode_track_experiment(accession="ENCSR000AKA", notes="H3K27ac ChIP-seq - QC thresholds verified per Landt 2012 (PMID:22955991)")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR000AKA",
  "notes": "H3K27ac ChIP-seq - QC thresholds verified per Landt 2012 (PMID:22955991)"
}
```

### Step 5: Document verification results

Record which claims were verified, sources found, and any caveats:
- Verified: MACS2 for ChIP-seq, FRiP >= 1%, IDR < 0.05
- Caveats: MACS2 not recommended for CUT&RUN (use SEACR instead)
- This verification log feeds into → **data-provenance** and → **scientific-writing**

### Integration with downstream skills
- Verified QC thresholds inform → **quality-assessment** criteria
- Literature validation supports → **scientific-writing** methods sections
- Citation accuracy feeds into → **cite-encode** for proper attribution
- Verified pipeline choices guide → **pipeline-guide** recommendations

## Code Examples

### 1. Verify an experiment's publication and quality

```
encode_get_experiment(accession="ENCSR123ABC")
```

Expected output:
```json
{
  "accession": "ENCSR123ABC",
  "assay_title": "Histone ChIP-seq",
  "target": "H3K27ac-human",
  "status": "released",
  "audit": {"WARNING": 1, "NOT_COMPLIANT": 0, "ERROR": 0},
  "replicates": 2,
  "lab": "Bernstein, Broad",
  "date_released": "2020-03-15"
}
```

**Trust check**: 0 errors, 2 replicates, released status — meets ENCODE standards.

### 2. Check citations for a tracked experiment

```
encode_get_citations(accession="ENCSR123ABC")
```

Expected output:
```json
{
  "accession": "ENCSR123ABC",
  "citations": {
    "consortium": "ENCODE Project Consortium. Nature 2020;583:699-710",
    "lab_publication": "Roadmap Epigenomics. Nature 2015;518:317-330",
    "data_citation": "ENCODE Project. https://www.encodeproject.org/experiments/ENCSR123ABC/"
  }
}
```

### 3. Compare two experiments for consistency

```
encode_compare_experiments(
  accession1="ENCSR123ABC",
  accession2="ENCSR456DEF"
)
```

Expected output:
```json
{
  "compatible": true,
  "shared": {"organism": "Homo sapiens", "assembly": "GRCh38"},
  "differences": {"lab": ["Bernstein, Broad", "Snyder, Stanford"]},
  "warnings": ["Different labs — check for batch effects"]
}
```

## Pitfalls & Edge Cases

- **High citation count ≠ high quality**: Highly cited papers can contain errors that propagate through the field. Always evaluate methods independently of citation count or journal prestige.
- **"Standard pipeline" is vague**: Papers claiming to use "standard" or "established" pipelines without naming specific tools and versions cannot be reproduced. Require exact tool + version + parameters.
- **Missing replicate information**: Papers that do not report the number of biological replicates, or confuse biological with technical replicates, cannot support differential claims. Minimum: 2 biological replicates.
- **Genome build ambiguity**: Papers that report coordinates without specifying the genome assembly (hg19 vs hg38) are a major reproducibility hazard. Coordinates can shift by megabases between builds.
- **Incomplete data availability**: Papers that claim "data available upon request" instead of depositing in public repositories (GEO, ENCODE) effectively prevent reproduction. FAIR principles require public deposition.
- **Overinterpretation of motif analysis**: Finding a motif in peaks does not prove direct binding. Background motif frequency, peak-to-motif distance, and orthogonal ChIP validation are all required.

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Verified QC thresholds | **quality-assessment** | Use validated thresholds for ENCODE data QC |
| Citation verification reports | **cite-encode** | Ensure cited methods papers are accurate |
| Validated pipeline recommendations | **pipeline-guide** | Select pipelines backed by verified benchmarks |
| Literature provenance records | **data-provenance** | Document which papers justified analysis choices |
| Verified methods claims | **scientific-writing** | Write methods sections with verified citations |
| Updated tool recommendations | **bioinformatics-installer** | Install tools backed by current benchmarks |
| Verified regulatory annotations | **regulatory-elements** | Confirm annotation sources are authoritative |
| Literature search results | **cross-reference** | Link ENCODE experiments to verified publications |

## Related Skills

- `cite-encode` — Citation management with trust integration
- `quality-assessment` — ENCODE experiment quality (complementary to publication quality)
- `data-provenance` — Track trust assessments in provenance chains
- `disease-research` — Disease research workflows that depend on publication reliability

## Presenting Results

- Present literature assessment as: claim | supporting_paper | citation_count | journal | year. Flag papers with <50 citations as lower confidence. Suggest: "Would you like to find the full text via PubMed?"

## For the request: "$ARGUMENTS"
