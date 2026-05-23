---
name: ensembl-annotation
description: Query the Ensembl REST API for regulatory feature annotations, variant effect prediction (VEP), coordinate liftover, gene lookups, and cross-references. Use when the user needs to annotate variants with VEP (consequence, CADD, REVEL, SpliceAI), check Ensembl Regulatory Build overlap for ENCODE regions, convert coordinates between GRCh37 and GRCh38, resolve gene IDs (Ensembl ↔ symbol ↔ RefSeq), look up gene phenotype associations, or cross-reference ENCODE targets with Ensembl annotations. Also use when the user mentions Ensembl, VEP, variant effect predictor, liftover, assembly conversion, regulatory build, gene lookup, or cross-references between databases.
---

# Query the Ensembl REST API

## When to Use

- User wants to annotate variants with Ensembl VEP (Variant Effect Predictor) consequences
- User asks about "VEP", "Ensembl", "variant annotation", "regulatory build", or "gene annotation"
- User needs to convert coordinates between assemblies using Ensembl's liftover API
- User wants to check the Ensembl Regulatory Build for overlap with ENCODE elements
- Example queries: "run VEP on my variant list", "annotate SNPs with regulatory consequences", "check Ensembl regulatory build for my peaks"

Annotate variants, look up regulatory features, convert coordinates, and resolve gene identifiers using the Ensembl REST API.

## Scientific Rationale

**The question**: "What does the Ensembl Regulatory Build say about this region, and what is the predicted effect of this variant?"

The Ensembl Regulatory Build integrates ENCODE, Roadmap Epigenomics, and Blueprint data into a unified annotation of regulatory features across human cell types. The Variant Effect Predictor (VEP) is the standard tool for variant consequence prediction, integrating 50+ annotation sources including CADD, REVEL, SpliceAI, and AlphaMissense.

### Ensembl ↔ ENCODE Feedback Loop

Ensembl's Regulatory Build incorporates ENCODE ChIP-seq, DNase-seq, and CTCF data to define regulatory features. Querying Ensembl after an ENCODE analysis provides an independent, aggregated view of regulatory annotations — often including data from non-ENCODE sources (Blueprint, Roadmap) that may cover biosamples not in ENCODE.

### Literature Support

- **Cunningham et al. 2022** (Nucleic Acids Research): Ensembl 2022 update. [DOI](https://doi.org/10.1093/nar/gkab1049)
- **McLaren et al. 2016** (Genome Biology, ~4,500 citations): The Ensembl Variant Effect Predictor. [DOI](https://doi.org/10.1186/s13059-016-0974-4)
- **Zerbino et al. 2015** (Genome Biology): The Ensembl Regulatory Build. [DOI](https://doi.org/10.1186/s13059-015-0621-5)

## API Reference

**Base URL**: `https://rest.ensembl.org`
**Authentication**: None required
**Rate limit**: Reasonable use expected; max 5Mb region queries
**Formats**: JSON (default), XML, GFF3, BED
**Current version**: Ensembl 114

Add `content-type: application/json` header to all requests.

## Step 1: Regulatory Feature Overlap

Query what regulatory features the Ensembl Regulatory Build assigns to a region:

```bash
# Get regulatory features in a region
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/overlap/region/human/7:140424943-140624564?feature=regulatory"

# Also get TF binding motifs
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/overlap/region/human/7:140424943-140624564?feature=regulatory;feature=motif"
```

### Regulatory Feature Types

| Type | Description | ENCODE Equivalent |
|------|-------------|-------------------|
| Promoter | Active promoter region | cCRE PLS |
| Enhancer | Active enhancer region | cCRE pELS/dELS |
| Open chromatin | Accessible region without H3K27ac | DNase-only sites |
| CTCF binding site | CTCF-occupied region | cCRE CTCF-only |
| TF binding site | Other TF binding | TF ChIP-seq peaks |
| Promoter flanking | Region flanking a promoter | cCRE TssAFlnk |

## Step 2: Variant Effect Prediction (VEP)

VEP provides consequence predictions for variants:

### Single Variant (by region notation)

```bash
# VEP annotation for a variant
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/vep/human/region/9:22125503-22125502:1/C"

# By rs ID
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/vep/human/id/rs699"
```

### Batch VEP (POST, up to 200 variants)

```bash
curl -X POST -H "Content-type: application/json" \
  "https://rest.ensembl.org/vep/human/region" \
  -d '{"variants": ["1 230710048 . A G . . .", "2 241533886 . T C . . ."]}'
```

### Key VEP Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `CADD=1` | Include CADD scores | Off |
| `Enformer=1` | Include Enformer predictions | Off |
| `AlphaMissense=1` | Include AlphaMissense pathogenicity | Off |
| `REVEL=1` | Include REVEL scores | Off |
| `SpliceAI=1` | Include SpliceAI splicing predictions | Off |
| `regulatory=1` | Include regulatory feature overlap | Off |
| `cell_type=` | Cell type for regulatory annotations | All |

### VEP Consequence Hierarchy (most to least severe)

| Consequence | Impact | Description |
|-------------|--------|-------------|
| `transcript_ablation` | HIGH | Deletion of entire transcript |
| `splice_donor_variant` | HIGH | Essential splice donor site |
| `stop_gained` | HIGH | Premature stop codon |
| `frameshift_variant` | HIGH | Reading frame change |
| `missense_variant` | MODERATE | Amino acid change |
| `splice_region_variant` | LOW | Near splice site |
| `synonymous_variant` | LOW | No amino acid change |
| `regulatory_region_variant` | MODIFIER | In regulatory element |
| `intergenic_variant` | MODIFIER | Between genes |

**For ENCODE regulatory variants**: Most will be classified as `regulatory_region_variant` (MODIFIER impact). The VEP consequence alone does not capture regulatory impact — combine with ENCODE cCRE class, tissue activity, and TF disruption data.

## Step 3: Coordinate Conversion (LiftOver)

Convert between GRCh37 (hg19) and GRCh38 (hg38):

```bash
# GRCh37 → GRCh38
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/map/human/GRCh37/17:1000000..1000100:1/GRCh38"

# GRCh38 → GRCh37
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/map/human/GRCh38/17:1000000..1000100:1/GRCh37"
```

**When needed**: Older GWAS studies report variants on GRCh37. ENCODE data uses GRCh38. Always liftOver before intersecting.

## Step 4: Gene Lookup and Cross-References

### Gene Information

```bash
# By Ensembl ID
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/lookup/id/ENSG00000157764?expand=1"

# By symbol
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/lookup/symbol/homo_sapiens/BRAF"
```

### Cross-References (Ensembl ↔ External DBs)

```bash
# Get all external references for a gene
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/xrefs/id/ENSG00000157764"

# Filter by external DB
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/xrefs/id/ENSG00000157764?external_db=HGNC"
```

**ENCODE integration**: ENCODE target names are typically HGNC symbols or Ensembl IDs. Use this endpoint to resolve between identifier systems.

## Step 5: Phenotype/Disease Associations

```bash
# Get phenotype associations for a gene
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/phenotype/gene/homo_sapiens/BRCA2"

# Get phenotype associations for a region
curl -H "Content-type: application/json" \
  "https://rest.ensembl.org/phenotype/region/homo_sapiens/9:22125500-22136000"
```

## Integrated ENCODE + Ensembl Workflow

```
1. Find ENCODE regulatory variants:
   → Intersect GWAS variants with ENCODE cCREs

2. Annotate with VEP:
   curl "https://rest.ensembl.org/vep/human/id/rs699?CADD=1;regulatory=1;REVEL=1"
   → Get consequence, CADD score, regulatory overlap

3. Check Ensembl Regulatory Build for independent confirmation:
   curl "https://rest.ensembl.org/overlap/region/human/CHR:START-END?feature=regulatory"
   → Compare with ENCODE cCRE classification

4. If working with GRCh37 data, liftOver:
   curl "https://rest.ensembl.org/map/human/GRCh37/CHR:POS..POS:1/GRCh38"

5. Resolve gene identifiers for ENCODE targets:
   curl "https://rest.ensembl.org/lookup/symbol/homo_sapiens/GENE_SYMBOL"

6. Check disease associations:
   curl "https://rest.ensembl.org/phenotype/gene/homo_sapiens/GENE"
```

## Pitfalls and Caveats

1. **Ensembl Regulatory Build ≠ ENCODE cCREs**: The Regulatory Build incorporates ENCODE data but uses different classification criteria. Annotations may not perfectly overlap with ENCODE cCRE calls.
2. **VEP MODIFIER impact for regulatory variants**: Non-coding regulatory variants are classified as MODIFIER impact by default. This does NOT mean low importance — it means VEP cannot assess regulatory consequence from sequence alone. Combine with ENCODE data.
3. **Region size limits**: Overlap queries limited to ~5Mb regions. For genome-wide analysis, download Ensembl GFF files or use the Perl VEP tool locally.
4. **Batch VEP limit**: REST API accepts max 200 variants per POST request. For larger sets, use the standalone VEP tool.
5. **GRCh38/GRCh37 consistency**: Always match assembly between ENCODE data and Ensembl queries. Use the liftOver endpoint when needed.
6. **Version updates**: Ensembl releases quarterly. Regulatory Build annotations may change between versions. Note the Ensembl version in your analysis.

## Walkthrough: Variant Effect Prediction for ENCODE Regulatory Variants

**Goal**: Use Ensembl VEP to predict functional consequences of variants located within ENCODE-defined regulatory elements, combining variant annotation with regulatory context.
**Context**: Ensembl provides the gold-standard Variant Effect Predictor (VEP) and Regulatory Build. Combined with ENCODE peaks, this enables comprehensive variant interpretation.

### Step 1: Find ENCODE experiments for the tissue of interest

```
encode_search_experiments(assay_title="ATAC-seq", organ="brain", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 32,
  "results": [
    {"accession": "ENCSR800BRN", "assay_title": "ATAC-seq", "biosample_summary": "brain", "status": "released"},
    {"accession": "ENCSR801CTX", "assay_title": "ATAC-seq", "biosample_summary": "cerebral cortex", "status": "released"}
  ]
}
```

### Step 2: Download peaks and extract variants

```
encode_download_files(accessions=["ENCFF900ATK"], download_dir="/data/brain_atac")
```

### Step 3: Run VEP on regulatory variants

Using Ensembl REST API (via skill guidance):
```
POST https://rest.ensembl.org/vep/human/region
Content-Type: application/json
{"variants": ["1 230710048 . A G", "7 87160618 . T C"]}
```

Expected VEP output:
```json
[
  {
    "input": "1 230710048 . A G",
    "most_severe_consequence": "regulatory_region_variant",
    "regulatory_feature_consequences": [
      {
        "regulatory_feature_id": "ENSR00000123456",
        "biotype": "promoter",
        "consequence_terms": ["regulatory_region_variant"]
      }
    ]
  }
]
```

**Interpretation**: VEP classifies this as a regulatory_region_variant in an Ensembl Regulatory Build promoter. Cross-referencing with the ENCODE ATAC-seq peak confirms the variant is in open chromatin in brain tissue.

### Step 4: Liftover if needed

If ENCODE peaks are in GRCh38 but variants are in hg19:
- Use → **liftover-coordinates** to convert variant positions before intersection
- Or use Ensembl REST API liftover endpoint

### Step 5: Integrate Ensembl Regulatory Build with ENCODE peaks

```
GET https://rest.ensembl.org/regulatory/species/homo_sapiens/id/ENSR00000123456
```

**Interpretation**: Compare Ensembl Regulatory Build activity with ENCODE experimental data. If the Regulatory Build calls a region a "promoter" and ENCODE H3K4me3 ChIP-seq confirms this, the annotation is high confidence.

### Integration with downstream skills
- ENCODE peaks define regions to annotate via → VEP regulatory consequence prediction
- VEP results feed into → **variant-annotation** for multi-source annotation
- Regulatory Build comparisons inform → **regulatory-elements** cCRE classification
- Gene consequence predictions connect to → **gtex-expression** for expression validation
- Coordinate conversions handled by → **liftover-coordinates** for cross-assembly work

## Code Examples

### 1. Find ENCODE data for an Ensembl-annotated gene

```
# Step 1: Identify the gene's regulatory neighborhood
# (via Ensembl REST API — see skill instructions)

# Step 2: Search ENCODE for ChIP-seq at the gene locus
encode_search_experiments(
  assay_title="Histone ChIP-seq",
  organ="liver",
  target="H3K27ac"
)
```

Expected output:
```json
{
  "total": 8,
  "experiments": [
    {
      "accession": "ENCSR123ABC",
      "assay_title": "Histone ChIP-seq",
      "target": "H3K27ac-human",
      "biosample_summary": "liver tissue male adult (54 years)"
    }
  ]
}
```

### 2. Track and cross-reference an annotated experiment

```
encode_track_experiment(
  accession="ENCSR123ABC",
  notes="Liver H3K27ac for VEP-annotated enhancer variants"
)
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR123ABC",
  "publications": 1,
  "files": 12
}
```

## Integration

| This skill produces... | Feed into... | Using tool/skill |
|---|---|---|
| VEP-annotated variant list | Regulatory variant filtering | variant-annotation skill |
| Gene annotations with coordinates | Peak-to-gene assignment | peak-annotation skill |
| Lifted-over coordinates (GRCh37→38) | ENCODE data integration | liftover-coordinates skill |
| Regulatory Build overlap results | Enhancer/promoter classification | regulatory-elements skill |
| Gene constraint scores | Target prioritization | cross-reference → Open Targets |

## Related Skills

| Skill | When to Use Instead/Additionally |
|-------|--------------------------------|
| `variant-annotation` | Full ENCODE-based post-GWAS workflow |
| `gnomad-variants` | Population frequency and constraint data for variants |
| `regulatory-elements` | ENCODE cCRE classification and chromatin state analysis |
| `ucsc-browser` | UCSC-hosted ENCODE tracks and sequence retrieval |
| `disease-research` | Connecting variants to disease mechanisms |
| `cross-reference` | General external database cross-referencing |
| `publication-trust` | Verify literature claims backing analytical decisions |

## Presenting Results

- Present gene annotations as: gene | ensembl_id | biotype | chr:start-end | strand. Include transcript count. Suggest: "Would you like to check expression in GTEx for these genes?"

## For the request: "$ARGUMENTS"
