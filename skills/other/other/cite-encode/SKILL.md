---
name: cite-encode
description: Generate proper ENCODE citations for publications, grants, and presentations. Use when the user needs to cite ENCODE data, create bibliography entries, write acknowledgment sections, or ensure compliance with ENCODE data use policy.
---

# Cite ENCODE Data Properly

## When to Use

- User wants to generate proper citations for ENCODE data, tools, and consortium papers
- User asks about "citing ENCODE", "BibTeX", "references", "bibliography", or "data citation"
- User needs to create a Key Resources Table (STAR Methods) for Cell-family journals
- User wants to export citations in BibTeX, RIS, or other reference manager formats
- Example queries: "cite the ENCODE experiments I used", "generate BibTeX for my tracked experiments", "how do I cite ENCODE in my paper?"

Help the user generate correct citations for ENCODE data following official guidelines. This is the definitive guide to citing ENCODE data in manuscripts, grants, presentations, and supplementary materials.

## ENCODE Citation Requirements

ENCODE data use policy requires citing data in publications. Data is freely available with **no embargo** -- unrestricted use upon release. However, proper attribution is both a scientific obligation and a practical necessity: reviewers will check that you have cited data sources correctly, and incomplete citations are a common reason for revision requests.

## Step 0: Assess Publication Trust Before Citing

Before citing any study, check its scientific integrity using the **publication-trust** skill. This step catches:
- Formally retracted papers still in circulation
- Key findings contradicted by independent groups
- Expressions of concern from journal editors
- Authors with patterns of problematic publications

If a study scores Trust Level 1 (Compromised) or 2 (Reliability concerns), flag it prominently in the citation list and note the issue. A compromised citation undermines the entire analysis built on it.

```
# For each paper you plan to cite:
# 1. Get metadata: get_article_metadata(pmids=["PMID"])
# 2. Check retractions: search_articles(query="PMID[PMID] AND Retracted Publication[pt]")
# 3. Check contradictions: search for citing articles with refutation language
# See publication-trust skill for full workflow
```

## Step 1: Identify What to Cite

Determine what the user needs to cite:

### Individual Experiments
For specific experiments used in analysis:
1. Track the experiment: `encode_track_experiment(accession="ENCSR...")`
2. Get associated publications: `encode_get_citations(accession="ENCSR...")`
3. The experiment's own publications should be cited

### The ENCODE Project Itself
When referencing ENCODE as a data source, cite the consortium papers:

**ENCODE Phase 3 (2020)**:
- ENCODE Project Consortium et al. "Expanded encyclopaedias of DNA elements in the human and mouse genomes." Nature 583, 699-710 (2020). PMID: 32728249. DOI: 10.1038/s41586-020-2493-4

**ENCODE Phase 2 (2012)**:
- ENCODE Project Consortium. "An integrated encyclopedia of DNA elements in the human genome." Nature 489, 57-74 (2012). PMID: 22955616. DOI: 10.1038/nature11247

**Original ENCODE (2007)**:
- ENCODE Project Consortium. "Identification and analysis of functional elements in 1% of the human genome by the ENCODE pilot project." Nature 447, 799-816 (2007). PMID: 17571346. DOI: 10.1038/nature05874

### Specific Data Standards
When your methods rely on ENCODE standards:
- ChIP-seq guidelines: Landt et al. "ChIP-seq guidelines and practices of the ENCODE and modENCODE consortia." Genome Res 22, 1813-1831 (2012). PMID: 22955991. DOI: 10.1101/gr.136184.111
- ENCODE uniform pipelines: Hitz et al. "The ENCODE Uniform Analysis Pipelines." Nucleic Acids Res 51, D1014-D1024 (2023). DOI: 10.1093/nar/gkac1067
- ENCODE Blacklist: Amemiya et al. "The ENCODE Blacklist: Identification of Problematic Regions of the Genome." Sci Rep 9, 9354 (2019). DOI: 10.1038/s41598-019-45839-z

## Step 2: Export Citations

Use `encode_get_citations` with appropriate format:
- `export_format="bibtex"` -- For LaTeX, Overleaf, BibDesk
- `export_format="ris"` -- For Endnote, Zotero, Mendeley, Papers
- `export_format="json"` -- For programmatic use

For all tracked experiments:
```
encode_get_citations(export_format="bibtex")
```

For a specific experiment:
```
encode_get_citations(accession="ENCSR133RZO", export_format="bibtex")
```

## Step 3: Generate Data Availability Statement

For the Data Availability section of a publication:

Template:
> "[Assay type] data for [biosample] were obtained from the ENCODE Project (https://www.encodeproject.org). Experiment accessions: [list ENCSR accessions]. All ENCODE data are freely available under unrestricted use policy."

Use `encode_export_data(format="csv")` to generate a supplementary table listing all experiments used, with columns for accession, assay, biosample, target, lab, and date released.

## Step 4: Write Acknowledgments

Template:
> "This work used data generated by the ENCODE Consortium (encodeproject.org). The ENCODE Project is funded by the National Human Genome Research Institute (NHGRI)."

If using data from specific labs, consider acknowledging them:
> "We thank [Lab Name] for generating the [assay type] data used in this study (ENCODE accession [ENCSR...])."

## Step 5: Cross-Reference with Literature

Use `encode_get_references` to find all linked PMIDs and DOIs for tracked experiments. These can be:
- Passed to PubMed tools for full metadata
- Used to find related articles
- Included in the bibliography

## Step 6: Supplementary Materials

For reproducibility, include in supplements:
1. Full experiment accession list: `encode_export_data(format="tsv")`
2. File accessions used: list specific ENCFF accessions
3. Pipeline versions and parameters
4. Quality metrics for each experiment used
5. Any derived files with provenance: `encode_get_provenance`

---

## Walkthrough: End-to-End From Analysis to Submitted Manuscript

This walkthrough covers generating ALL citation content needed for a manuscript that uses ENCODE data. Follow each phase in order.

### Phase 1: Gather All Experiments Used

```
encode_list_tracked()
```

Review the output. A typical multi-omic study might track 12 experiments: 5 Histone ChIP-seq, 3 ATAC-seq, 2 RNA-seq, 2 WGBS. Verify every experiment has publications fetched (the publications column should show a count greater than zero). If any show zero publications, run `encode_get_citations(accession="ENCSR...")` for those experiments individually to trigger a fresh lookup.

Check that every experiment you actually used in the analysis is tracked. A common oversight is forgetting to track experiments that were used only for quality comparison or as controls. If you generated a figure or statistic from an experiment, it must be tracked and cited.

### Phase 2: Generate Methods Section Citations

Every bioinformatics tool used in your analysis pipeline must be cited. Reviewers routinely check for these. Common tools and their canonical citations:

| Tool | Citation | DOI |
|------|----------|-----|
| MACS2 v2.2.7.1 | Zhang et al. Genome Biol 2008 | 10.1186/gb-2008-9-9-r137 |
| STAR v2.7.10b | Dobin et al. Bioinformatics 2013 | 10.1093/bioinformatics/bts635 |
| DESeq2 v1.38 | Love et al. Genome Biol 2014 | 10.1186/s13059-014-0550-8 |
| deepTools v3.5.4 | Ramirez et al. Nucleic Acids Res 2016 | 10.1093/nar/gkw257 |
| bedtools v2.31.0 | Quinlan & Hall. Bioinformatics 2010 | 10.1093/bioinformatics/btq033 |
| samtools v1.17 | Danecek et al. GigaScience 2021 | 10.1093/gigascience/giab008 |
| Bowtie2 v2.5.1 | Langmead & Salzberg. Nat Methods 2012 | 10.1038/nmeth.1923 |
| featureCounts (Subread) | Liao et al. Bioinformatics 2014 | 10.1093/bioinformatics/btt656 |
| Bismark | Krueger & Andrews. Bioinformatics 2011 | 10.1093/bioinformatics/btr167 |
| HOMER | Heinz et al. Mol Cell 2010 | 10.1016/j.molcel.2010.05.004 |
| IGV | Robinson et al. Nat Biotechnol 2011 | 10.1038/nbt.2754 |
| Picard | Broad Institute (URL-only citation) | https://broadinstitute.github.io/picard/ |
| BWA-MEM | Li. arXiv 2013 | arXiv:1303.3997 |

See the `bioinformatics-installer` and `scientific-writing` skills for the complete citation list covering 134+ tools.

Always include tool versions. "We called peaks using MACS2" is insufficient. Write: "We called peaks using MACS2 v2.2.7.1 (Zhang et al. 2008) with parameters --nomodel --shift -100 --extsize 200 --broad."

### Phase 3: Generate ENCODE Consortium Citations

Every manuscript using ENCODE data must include at minimum:

1. **ENCODE Phase 3**: Nature 583, 699-710 (2020) -- PMID: 32728249
   - Cite this whenever you use ENCODE data from any source.

2. **ENCODE Standards** (conditional): Landt et al. Genome Res 2012 -- PMID: 22955991
   - Cite this if you reference ENCODE quality metrics (FRiP, NSC, RSC, NRF) or use ENCODE QC thresholds to filter your own data.

3. **ENCODE Portal** (conditional): Hitz et al. Nucleic Acids Res 2023 -- DOI: 10.1093/nar/gkac1067
   - Cite this if you accessed data through the ENCODE portal website or used the ENCODE uniform analysis pipeline outputs.

4. **ENCODE Blacklist** (conditional): Amemiya et al. Sci Rep 2019 -- DOI: 10.1038/s41598-019-45839-z
   - Cite this if you applied the ENCODE Blacklist v2 to filter problematic genomic regions (you should always do this).

### Phase 4: Generate Experiment-Specific Citations

```
encode_get_citations(export_format="bibtex")
```

This returns BibTeX entries for all publications associated with tracked experiments. Merge these with your consortium papers and tool citations into a single .bib file. Check for duplicate entries -- the same publication may be associated with multiple experiments from the same lab.

If a tracked experiment has no associated publication (some ENCODE data is released without an accompanying paper), cite the ENCODE consortium paper and list the experiment accession in your Data Availability statement and Supplementary Table.

### Phase 5: Generate Data Availability Statement

Adapt this template to your specific study:

> "Histone ChIP-seq (H3K27ac, H3K4me1, H3K4me3, H3K27me3, H3K36me3), ATAC-seq, RNA-seq, and whole-genome bisulfite sequencing data were obtained from the ENCODE Project (https://www.encodeproject.org). Experiment accessions are listed in Supplementary Table S1. All ENCODE data are freely available without restriction."

If you combined ENCODE data with your own generated data, clearly separate them:

> "Published ChIP-seq and ATAC-seq data were obtained from ENCODE (accessions in Supplementary Table S1). RNA-seq data were generated in this study and deposited in GEO under accession GSE######."

### Phase 6: Generate Acknowledgments

Template:

> "This study used data generated by the ENCODE Consortium (encodeproject.org), funded by the National Human Genome Research Institute (NHGRI). We thank [Lab PI names from tracked experiments] for generating the [assay types] data used in this work."

To fill in the PI names, check the `lab` field from `encode_list_tracked()`. For example: "We thank the Bernstein, Stamatoyannopoulos, and Snyder laboratories for generating the histone ChIP-seq, chromatin accessibility, and transcription factor binding data, respectively."

### Phase 7: Generate Supplementary Table S1

```
encode_export_data(format="tsv")
```

This creates a table with the columns needed for reproducibility:

| Accession | Assay | Target | Biosample | Assembly | Lab | Date Released | Publication PMID |
|-----------|-------|--------|-----------|----------|-----|---------------|-----------------|
| ENCSR123ABC | Histone ChIP-seq | H3K27ac | pancreatic islet | GRCh38 | Bernstein | 2020-03-15 | 32728249 |
| ENCSR456DEF | ATAC-seq | -- | pancreatic islet | GRCh38 | Stamatoyannopoulos | 2020-06-01 | 32728249 |

This table goes in Supplementary Materials. Some journals (Nature, Cell) require it. All journals benefit from having it.

---

## BibTeX Citation Format Examples

Use these BibTeX entries for the most commonly cited ENCODE papers. Export additional entries with `encode_get_citations(export_format="bibtex")`.

```bibtex
@article{encode2020expanded,
  title={Expanded encyclopaedias of {DNA} elements in the human and mouse genomes},
  author={{ENCODE Project Consortium} and Moore, Jill E and Purcaro, Michael J and others},
  journal={Nature},
  volume={583},
  number={7818},
  pages={699--710},
  year={2020},
  publisher={Nature Publishing Group},
  doi={10.1038/s41586-020-2493-4}
}

@article{landt2012chipseq,
  title={{ChIP}-seq guidelines and practices of the {ENCODE} and mod{ENCODE} consortia},
  author={Landt, Stephen G and Marinov, Georgi K and Kundaje, Anshul and others},
  journal={Genome Research},
  volume={22},
  number={9},
  pages={1813--1831},
  year={2012},
  publisher={Cold Spring Harbor Laboratory Press},
  doi={10.1101/gr.136184.111}
}

@article{hitz2023encode,
  title={The {ENCODE} Uniform Analysis Pipelines},
  author={Hitz, Benjamin C and Lee, Jin-Wook and Jolanki, Otto and others},
  journal={Nucleic Acids Research},
  volume={51},
  number={D1},
  pages={D1014--D1024},
  year={2023},
  publisher={Oxford University Press},
  doi={10.1093/nar/gkac1067}
}

@article{encode2012integrated,
  title={An integrated encyclopedia of {DNA} elements in the human genome},
  author={{ENCODE Project Consortium}},
  journal={Nature},
  volume={489},
  number={7414},
  pages={57--74},
  year={2012},
  publisher={Nature Publishing Group},
  doi={10.1038/nature11247}
}

@article{amemiya2019blacklist,
  title={The {ENCODE} Blacklist: Identification of Problematic Regions of the Genome},
  author={Amemiya, Haley M and Kundaje, Anshul and Boyle, Alan P},
  journal={Scientific Reports},
  volume={9},
  pages={9354},
  year={2019},
  publisher={Nature Publishing Group},
  doi={10.1038/s41598-019-45839-z}
}
```

## RIS Citation Format Examples

Use RIS format for import into Zotero, Mendeley, Endnote, and most other reference managers. Export with `encode_get_citations(export_format="ris")`.

```
TY  - JOUR
AU  - ENCODE Project Consortium
AU  - Moore, Jill E
AU  - Purcaro, Michael J
TI  - Expanded encyclopaedias of DNA elements in the human and mouse genomes
JO  - Nature
VL  - 583
IS  - 7818
SP  - 699
EP  - 710
PY  - 2020
DO  - 10.1038/s41586-020-2493-4
ER  -

TY  - JOUR
AU  - Landt, Stephen G
AU  - Marinov, Georgi K
AU  - Kundaje, Anshul
TI  - ChIP-seq guidelines and practices of the ENCODE and modENCODE consortia
JO  - Genome Research
VL  - 22
IS  - 9
SP  - 1813
EP  - 1831
PY  - 2012
DO  - 10.1101/gr.136184.111
ER  -

TY  - JOUR
AU  - Hitz, Benjamin C
AU  - Lee, Jin-Wook
AU  - Jolanki, Otto
TI  - The ENCODE Uniform Analysis Pipelines
JO  - Nucleic Acids Research
VL  - 51
IS  - D1
SP  - D1014
EP  - D1024
PY  - 2023
DO  - 10.1093/nar/gkac1067
ER  -
```

---

## Citation Management by Reference Manager

### Zotero

1. Export citations: `encode_get_citations(export_format="ris")`
2. Save the output to a file with the `.ris` extension (e.g., `encode_citations.ris`)
3. In Zotero: File > Import > select the .ris file
4. Citations appear in your library with full metadata including DOIs
5. Use the Zotero Word plugin or Zotero Connector for Google Docs to insert citations inline
6. Zotero auto-resolves DOIs to fetch abstracts and PDFs when available

Tip: Create a dedicated Zotero collection named "ENCODE Data Sources" to keep data citations separate from your literature references. This makes it easy to identify which references are data sources vs. analytical method citations.

### Mendeley

1. Export citations: `encode_get_citations(export_format="ris")`
2. Save to a `.ris` file
3. In Mendeley: File > Import > RIS format
4. Check that DOIs resolved correctly -- Mendeley auto-fetches PDFs for open access articles
5. Use Mendeley Cite plugin for Word or Google Docs

Tip: Tag imported ENCODE citations with "ENCODE" so you can filter them later when building your bibliography.

### Endnote

1. Export citations: `encode_get_citations(export_format="ris")`
2. Save to a `.ris` file
3. In Endnote: File > Import > select "Reference Manager (RIS)" as the import filter
4. Map to your desired output style (e.g., Nature, Cell, Genome Research, PNAS)
5. Endnote handles journal abbreviation formatting automatically based on the selected style

### LaTeX / Overleaf

1. Export citations: `encode_get_citations(export_format="bibtex")`
2. Save as `encode_refs.bib`
3. Add to your LaTeX project: `\bibliography{encode_refs}` (or `\addbibresource{encode_refs.bib}` for biblatex)
4. Cite in text: `\cite{encode2020expanded}`, `\cite{landt2012chipseq}`
5. In Overleaf: upload the .bib file to your project files panel
6. Run BibTeX/Biber to compile references

Tip: Use `\nocite{*}` during drafting to render all entries, then remove it before submission so only cited entries appear in the bibliography.

### Google Docs

1. Export citations: `encode_get_citations(export_format="ris")`
2. Import into Zotero or Mendeley (see above)
3. Install the Zotero Connector or Mendeley Cite browser extension
4. In Google Docs: use the Zotero/Mendeley toolbar to insert citations
5. Generate the bibliography at the end of the document using the plugin

---

## Journal-Specific Citation Requirements

Different journals have different requirements for citing public datasets like ENCODE. Consult the target journal's author guidelines, but use these as a starting reference.

### Nature / Nature Genetics / Nature Methods

- **Data Availability**: Required. Must list specific ENCSR accessions and the ENCODE portal URL.
- **Code Availability**: Required if custom analysis code was used. Host on GitHub or Zenodo.
- **Supplementary Table**: Required with all accessions and metadata used. Include assembly version.
- **Max references**: Approximately 50 in the main text; unlimited in supplementary materials.
- **Citation format**: Author(s). Title. Journal Volume, Pages (Year).
- **Note**: Nature journals require a "Reporting Summary" that includes questions about data availability.

### Cell / Cell Reports / Cell Systems

- **STAR Methods**: Required. Include all ENCODE accessions in the STAR Methods "Key Resources Table" (see template below).
- **Citation format**: Author(s) (Year). Title. Journal Volume, Pages.
- **Key Resources Table**: Must list every dataset as a separate row. Include the accession as the IDENTIFIER and "ENCODE" as the SOURCE.
- **Data and Code Availability**: A dedicated subsection within STAR Methods listing all accessions, URLs, and software.

### Genome Research

- **Data access**: Strongly supports ENCODE-style open data citation. Extended data access policy awareness.
- **Citation format**: Standard author-year with full DOI.
- **Methods detail**: Expects comprehensive pipeline descriptions with all parameters and versions.

### Nucleic Acids Research

- **Database papers**: If citing the ENCODE portal itself, cite Hitz et al. 2023.
- **Citation format**: Author(s) (Year) Title. Journal, Volume, Pages.
- **Web server / database issues**: NAR has dedicated database issues; ENCODE portal papers appear here.

### PLOS Journals (PLOS ONE, PLOS Genetics, PLOS Comp Bio)

- **Open data policy**: All accessions must be listed in a Data Availability statement. This is mandatory.
- **Citation format**: Author(s). Title. Journal. Year;Volume(Issue):Pages.
- **Data Availability**: Appears before the references section, not in Methods. Must include URLs.

### Genome Biology

- **Availability of data and materials**: Required section. Must list all ENCODE accessions with URLs.
- **Citation format**: Author(s). Title. Journal. Year;Volume:Pages.
- **Open access**: All articles are open access, which aligns with ENCODE's open data policy.

---

## Key Resources Table Template (Cell-family Journals)

For manuscripts submitted to Cell, Cell Reports, Cell Systems, Molecular Cell, or other Cell Press journals, a STAR Methods Key Resources Table is required. Use this template:

```
| REAGENT or RESOURCE | SOURCE | IDENTIFIER |
|---|---|---|
| **Deposited Data** | | |
| H3K27ac ChIP-seq, human pancreatic islets | ENCODE | ENCSR123ABC |
| H3K4me1 ChIP-seq, human pancreatic islets | ENCODE | ENCSR456DEF |
| H3K4me3 ChIP-seq, human pancreatic islets | ENCODE | ENCSR789GHI |
| H3K27me3 ChIP-seq, human pancreatic islets | ENCODE | ENCSR012JKL |
| ATAC-seq, human pancreatic islets | ENCODE | ENCSR345MNO |
| RNA-seq, human pancreatic islets | ENCODE | ENCSR678PQR |
| GRCh38 reference genome | UCSC | https://hgdownload.soe.ucsc.edu/goldenPath/hg38/ |
| GENCODE v41 gene annotation | GENCODE | https://www.gencodegenes.org/human/release_41.html |
| ENCODE Blacklist v2 | Amemiya et al., 2019 | https://github.com/Boyle-Lab/Blacklist/ |
| **Software and Algorithms** | | |
| MACS2 v2.2.7.1 | Zhang et al., 2008 | https://github.com/macs3-project/MACS |
| STAR v2.7.10b | Dobin et al., 2013 | https://github.com/alexdobin/STAR |
| DESeq2 v1.38 | Love et al., 2014 | https://bioconductor.org/packages/DESeq2 |
| bedtools v2.31.0 | Quinlan & Hall, 2010 | https://github.com/arq5x/bedtools2 |
| deepTools v3.5.4 | Ramirez et al., 2016 | https://github.com/deeptools/deepTools |
| samtools v1.17 | Danecek et al., 2021 | https://github.com/samtools/samtools |
| Custom analysis scripts | This study | https://github.com/[your-repo] |
```

Populate this table by running `encode_list_tracked()` to get all experiment accessions, then pair each with its assay type and biosample term.

---

## Pitfalls: Common Citation Mistakes

### 1. "ENCODE data" without accessions
Always list specific ENCSR accessions. "We used ENCODE ChIP-seq data" is NOT sufficient for reproducibility. A reviewer has no way to identify which of the thousands of ENCODE ChIP-seq experiments you used. Write: "We used H3K27ac ChIP-seq data from human pancreatic islets (ENCODE accession ENCSR123ABC)."

### 2. Citing only the consortium paper
The ENCODE Phase 3 consortium paper (Nature 2020) covers the project as a whole. You must ALSO cite the specific laboratory publication associated with each experiment you used. Run `encode_get_citations(accession="ENCSR...")` for each experiment to find the lab paper.

### 3. Forgetting tool citations
Every bioinformatics tool used in your pipeline must be cited. Reviewers routinely check for MACS2, STAR, DESeq2, samtools, and bedtools citations. Missing tool citations are one of the most common reasons for revision requests. See the `bioinformatics-installer` skill for complete DOI lists.

### 4. Missing assembly version
When citing ENCODE data, always specify the genome assembly: "GRCh38 (hg38)" for human or "mm10 (GRCm38)" for mouse. Assembly version determines coordinate systems, and mixing assemblies silently corrupts integrative analyses. If you performed liftOver between assemblies, cite the liftOver tool and state both source and target assemblies.

### 5. Not distinguishing reanalyzed data
If you reprocessed raw ENCODE data (FASTQ) with your own pipeline, state this clearly: "We reprocessed raw sequencing data from ENCODE (accession ENCSR...) using [your pipeline]." Do not cite ENCODE processed files (ENCFF) if you did not use them. Conversely, if you used ENCODE-processed files directly, say so: "We used IDR-thresholded peaks (ENCFF...) from the ENCODE uniform analysis pipeline."

### 6. Citing retracted or corrected papers
Always verify publication status before submitting your manuscript. Use the `publication-trust` skill to check for retractions, corrections, and expressions of concern. A single retracted citation can undermine reviewer confidence in your entire study.

### 7. Preprint vs. published version
If an ENCODE experiment's publication was originally a preprint (bioRxiv) but has since been published in a peer-reviewed journal, always cite the journal version. Use `convert_article_ids` or check PubMed for the latest version. Citing a preprint when a peer-reviewed version exists signals to reviewers that you are not current with the literature.

### 8. Consortium vs. lab attribution
The ENCODE consortium paper should be cited when referencing the project broadly. Individual lab papers should be cited when using specific experiments. Do both when appropriate -- they are complementary, not redundant.

### 9. Stale DOIs
DOI links can break if a publisher migrates. Always verify DOIs resolve correctly before submitting a manuscript. Use https://doi.org/[DOI] to check.

### 10. Year ambiguity
Some ENCODE papers have online-first dates different from print dates. Use the year that appears on the journal's official article page. For BibTeX, use the year field that matches the volume/issue assignment.

---

## Grant Writing: Citing ENCODE in NIH/NSF Applications

ENCODE data is a powerful resource to reference in grant applications. Proper citation strengthens your proposal by demonstrating you are leveraging existing public data rather than requesting funds for data generation that already exists.

### Background and Significance

Cite the ENCODE Phase 3 paper to establish the resource and its scope:

> "The ENCODE Project has generated comprehensive maps of functional genomic elements across hundreds of human and mouse biosamples, including [relevant tissue/cell type] (ENCODE Consortium, Nature 2020). These data provide the foundation for [your research question]."

If relevant, cite the scale of available data:

> "ENCODE has released over 15,000 experiments covering histone modifications, transcription factor binding, chromatin accessibility, DNA methylation, and gene expression across diverse tissues and cell types."

### Preliminary Data

If you have already analyzed ENCODE data, cite the specific experiments:

> "In preliminary analyses, we integrated H3K27ac ChIP-seq and ATAC-seq data from ENCODE (accessions ENCSR123ABC, ENCSR456DEF) with our RNA-seq data to identify [N] candidate regulatory elements in [tissue]."

This demonstrates feasibility and shows reviewers that the public data you plan to use actually exists and is compatible with your approach.

### Approach / Research Strategy

Reference ENCODE quality standards as the basis for your quality control pipeline:

> "We will apply ENCODE quality standards (Landt et al. 2012) to all ChIP-seq data, requiring FRiP >= 1%, NSC > 1.05, RSC > 0.8, and at least two concordant biological replicates. All analyses will exclude ENCODE Blacklist regions (Amemiya et al. 2019)."

For computational proposals, reference the ENCODE uniform pipelines:

> "Raw sequencing data will be processed using the ENCODE uniform analysis pipeline (Hitz et al. 2023) to ensure reproducibility and comparability with existing ENCODE processed data."

### Data Management Plan

ENCODE's open data model is a useful precedent to reference:

> "Following the ENCODE Project's model of immediate, unrestricted data release, all processed data and analysis code will be deposited in [GEO/Zenodo/GitHub] upon publication."

### Budget Justification

When using ENCODE data reduces the need for new data generation, state this:

> "The availability of comprehensive ENCODE datasets for [tissue/cell type] eliminates the need for de novo [assay type] data generation, reducing project costs by approximately $[amount]."

---

## Key Literature

### ENCODE Consortium Papers

| Paper | Year | Journal | PMID | DOI |
|-------|------|---------|------|-----|
| ENCODE Phase 3 | 2020 | Nature 583, 699-710 | 32728249 | 10.1038/s41586-020-2493-4 |
| ENCODE Phase 2 | 2012 | Nature 489, 57-74 | 22955616 | 10.1038/nature11247 |
| ENCODE Pilot | 2007 | Nature 447, 799-816 | 17571346 | 10.1038/nature05874 |
| ChIP-seq guidelines | 2012 | Genome Res 22, 1813-1831 | 22955991 | 10.1101/gr.136184.111 |
| ENCODE Pipelines | 2023 | Nucleic Acids Res 51, D1014-D1024 | -- | 10.1093/nar/gkac1067 |
| ENCODE Blacklist | 2019 | Sci Rep 9, 9354 | 31249361 | 10.1038/s41598-019-45839-z |

### Data Citation Principles

| Paper | Year | Journal | DOI |
|-------|------|---------|-----|
| FAIR Principles | 2016 | Scientific Data 3, 160018 | 10.1038/sdata.2016.18 |
| Data Citation Principles | 2015 | PeerJ Computer Science 1, e1 | 10.7717/peerj-cs.1 |
| Force11 Data Citation Roadmap | 2014 | -- | 10.25490/a97f-egyk |

The FAIR principles (Findable, Accessible, Interoperable, Reusable; Wilkinson et al. 2016) provide the conceptual framework for why proper data citation matters. ENCODE data is FAIR by design: each experiment has a persistent accession (Findable), data is freely downloadable (Accessible), uses standard formats like BED/BAM/bigWig (Interoperable), and includes full metadata and provenance (Reusable). Citing ENCODE data correctly is how you uphold the Reusable principle by crediting the data generators.

The Joint Declaration of Data Citation Principles (Starr et al. 2015) established that data citations should be treated as first-class scholarly objects, equivalent to literature citations. When you cite ENCODE experiments, you are following this standard.

---

## Code Examples

### 1. Get citations for an experiment
```
encode_get_citations(accession="ENCSR000AKA")
```

Expected output:
```json
{
  "citations": [
    {"pmid": "29126249", "title": "ENCODE encyclopedia", "year": 2012}
  ]
}
```

### 2. Link a reference to an experiment
```
encode_link_reference(accession="ENCSR000AKA", reference_type="pubmed", reference_id="29126249", notes="ENCODE consortium paper")
```

Expected output:
```json
{"status": "linked", "accession": "ENCSR000AKA", "reference_type": "pubmed", "reference_id": "29126249"}
```

### 3. List all tracked experiments for citation
```
encode_list_tracked()
```

Expected output:
```json
{
  "experiments": [
    {"accession": "ENCSR000AKA", "assay": "Histone ChIP-seq", "notes": "GM12878 H3K27ac"},
    {"accession": "ENCSR637ENO", "assay": "ATAC-seq", "notes": "GM12878 accessibility"}
  ]
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Citation lists | **scientific-writing** | Publication-ready reference lists |
| Linked PubMed IDs | **cross-reference** | Bidirectional experiment-publication links |
| Data availability statements | **data-provenance** | Complete data access documentation |
| Experiment citation metadata | **track-experiments** | Annotate tracked experiments with publications |
| ENCODE consortium citations | **publication-trust** | Verify citation accuracy |
| Reference collections | **disease-research** | Cite all data sources in disease studies |

## Related Skills

| Skill | When to Use Instead/Additionally |
|-------|--------------------------------|
| `publication-trust` | Assess scientific integrity of cited studies before including them |
| `track-experiments` | Track experiments locally to manage citation collections |
| `cross-reference` | Link experiments to PubMed, DOI, GEO, and other identifiers |
| `data-provenance` | Log the full analysis chain for methods sections |
| `geo-connector` | Find GEO accessions for ENCODE experiments to include in citations |
| `bioinformatics-installer` | Get canonical citations and DOIs for 134+ bioinformatics tools |
| `scientific-writing` | Generate publication-ready methods, figures, and tables sections |
| `quality-assessment` | Get QC metrics to report in your methods section |

## Presenting Results

- Present citations in the requested format (BibTeX/RIS/text). Show total publications found and any missing DOIs.
- For manuscript walkthroughs, present each phase sequentially and confirm the user has the data for each section before proceeding.
- When generating BibTeX, check for duplicate citation keys and resolve them.
- Suggest: "Would you like to export all citations for your reference manager?"
- For grant applications, offer to draft the specific paragraph with citations inline.

## For the request: "$ARGUMENTS"
