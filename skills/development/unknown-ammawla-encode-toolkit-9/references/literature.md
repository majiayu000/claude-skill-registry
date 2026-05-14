# DNase-seq Pipeline — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the pipeline-dnaseseq skill — papers defining ENCODE DNase-seq processing standards, DHS calling with Hotspot2, transcription factor footprinting, and quality assessment for DNase I hypersensitivity assays.

---

## DNase-seq Method & Standards

---

### Thurman et al. 2012 — The accessible chromatin landscape of the human genome

- **Citation:** Thurman RE, Rynes E, Humbert R, Vierstra J, Maurano MT, Haugen E, Sheffield NC, Stergachis AB, Wang H, Vernot B, Garg K, John S, Sandstrom R, Bates D, Boatman L, Canfield TK, Diegel M, Dunn D, Ebersol AK, Frum T, Giste E, Johnson AK, Johnson EM, Kutyavin T, Laber B, Lee K, Lotakis D, Neph S, Neri F, Nguyen ED, Qu H, Reynolds AP, Roach V, Safi A, Sanchez ME, Sanyal A, Shafer A, Simon JM, Song L, Vong S, Weaver M, Yan Y, Zhang Z, Zhang Z, Lenhard B, Tewari M, Dorschner MO, Hansen RS, Navas PA, Stamatoyannopoulos G, Iyer VR, Lieb JD, Sunyaev SR, Akey JM, Sabo PJ, Kaul R, Furey TS, Dekker J, Crawford GE, Stamatoyannopoulos JA. The accessible chromatin landscape of the human genome. Nature, 489(7414):75-82, 2012.
- **DOI:** [10.1038/nature11232](https://doi.org/10.1038/nature11232)
- **PMID:** 22955617 | **PMC:** PMC3721348
- **Citations:** ~3,000
- **Key findings:** Generated the most comprehensive map of DNase I hypersensitive sites (DHSs) across 125 diverse human cell and tissue types as part of ENCODE Phase 2. Identified ~2.9 million unique DHSs covering ~40% of the genome, with individual cell types having 100,000-200,000 DHSs. Demonstrated that distal DHSs (enhancers) are highly cell-type-specific while promoter DHSs are more shared. Established that DHSs mark virtually all classes of cis-regulatory elements and that 95% of the genome lies within 10 kb of a DHS in at least one cell type. This paper validated DNase-seq as a primary assay for the ENCODE encyclopedia.

---

### John et al. 2011 — Hotspot2: chromatin accessibility peak calling

- **Citation:** John S, Sabo PJ, Thurman RE, Sung MH, Biddie SC, Johnson TA, Hager GL, Stamatoyannopoulos JA. Chromatin accessibility pre-determines glucocorticoid receptor binding patterns. Nature Genetics, 43(3):264-268, 2011.
- **DOI:** [10.1038/ng.759](https://doi.org/10.1038/ng.759)
- **PMID:** 21258342 | **PMC:** PMC3049959
- **Citations:** ~600
- **Key findings:** Introduced the Hotspot algorithm (predecessor to Hotspot2) for identifying statistically significant regions of chromatin accessibility from DNase-seq data. The algorithm uses a local background model that accounts for mappability variation across the genome — critical because DNase I cuts accessible chromatin regardless of whether fragments map uniquely. Hotspot2 (the current version used in ENCODE) extends this with improved FDR control and peak refinement. Unlike MACS2 (designed for ChIP-seq), Hotspot2 is specifically calibrated for the diffuse signal pattern of DNase-seq data and is the ENCODE standard for DNase-seq peak calling.

---

### Vierstra et al. 2020 — Global reference mapping of TF footprints

- **Citation:** Vierstra J, Lazar J, Sandstrom R, Halow J, Lee K, Bates D, Diegel M, Dunn D, Neri F, Haugen E, Rynes E, Reynolds A, Nelson J, Johnson A, Frerker M, Buckley M, Kaul R, Meuleman W, Stamatoyannopoulos JA. Global reference mapping of human transcription factor footprints. Nature, 583(7818):729-736, 2020.
- **DOI:** [10.1038/s41586-020-2528-x](https://doi.org/10.1038/s41586-020-2528-x)
- **PMID:** 32728250 | **PMC:** PMC7410830
- **Citations:** ~600
- **Key findings:** Created a global reference map of TF footprints from 243 human cell types using deep DNase-seq (>200M reads per sample). Identified >4.5 million unique TF footprints genome-wide, demonstrating that ~2% of the genome is occupied by TFs at any given time. Established the analytical framework for digital genomic footprinting: bias-corrected DNase cleavage profiles around TF motifs, with bound sites showing a characteristic protection pattern (footprint) flanked by elevated cleavage. Published as part of ENCODE Phase 3, providing the reference standard for interpreting TF footprints from DNase-seq data.

---

### ENCODE Project Consortium 2020 — Expanded encyclopaedias of DNA elements

- **Citation:** ENCODE Project Consortium et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature, 583(7818):699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,500
- **Key findings:** ENCODE Phase 3 paper establishing DNase-seq as a primary accessibility assay alongside ATAC-seq for identifying candidate cis-Regulatory Elements (cCREs). DNase-seq DHSs are a core input for the cCRE classification system, with DHS signal strength and overlap with histone marks determining element type (promoter-like, enhancer-like, CTCF-only, K4m3). Established uniform processing standards: BWA-MEM alignment, Hotspot2 peak calling, SPOT score as the primary QC metric (>0.4 for acceptable quality), and GRCh38/mm10 as reference assemblies.

---

### Hitz et al. 2023 — The ENCODE Uniform Analysis Pipelines

- **Citation:** Hitz BC, Lee JW, Jolanki O, et al. The ENCODE Uniform Analysis Pipelines. Research Square (preprint), 2023.
- **DOI:** [10.21203/rs.3.rs-311127/v1](https://doi.org/10.21203/rs.3.rs-311127/v1)
- **Citations:** ~84
- **Key findings:** Documents the official ENCODE DNase-seq pipeline specification: BWA-MEM alignment, Picard MarkDuplicates, Hotspot2 for DHS calling with FDR control, and SPOT score computation. Specifies that DNase-seq uses Hotspot2 (not MACS2) because Hotspot2's mappability-aware background model is critical for the DNase-seq signal profile. Pipeline infrastructure uses Docker containers and WDL for reproducible execution.

---

## TF Footprinting

---

### Li et al. 2019 — HINT-ATAC: TF footprinting from chromatin accessibility

- **Citation:** Li Z, Schulz MH, Look T, Begus M, Zenke M, Costa IG. Identification of transcription factor binding sites using ATAC-seq. Genome Research, 29(11):1850-1858, 2019.
- **DOI:** [10.1186/s13059-019-1642-2](https://doi.org/10.1186/s13059-019-1642-2)
- **PMID:** 31649060
- **Citations:** ~300
- **Key findings:** Introduced HINT-ATAC, a computational framework for TF footprinting from chromatin accessibility data (ATAC-seq and DNase-seq). HINT-ATAC models the enzymatic cleavage bias of both DNase I and Tn5 transposase, providing bias-corrected footprint scores that improve over raw cleavage signal. Supports both DNase-seq and ATAC-seq data with enzyme-specific bias correction models. Used in this pipeline's optional footprinting analysis step, producing per-motif footprint scores that can be compared against the Vierstra et al. 2020 reference atlas.

---

### Neph et al. 2012 — An expansive human regulatory lexicon encoded in TF footprints

- **Citation:** Neph S, Vierstra J, Stergachis AB, Reynolds AP, Haugen E, Vernot B, Thurman RE, John S, Sandstrom R, Johnson AK, Maurano MT, Humbert R, Rynes E, Wang H, Vong S, Lee K, Bates D, Diegel M, Roach V, Dunn D, Neri J, Schafer A, Hansen RS, Kutyavin T, Giste E, Weaver M, Canfield T, Sabo P, Zhang M, Balasundaram G, Byron R, MacCoss MJ, Akey JM, Bender MA, Groudine M, Kaul R, Stamatoyannopoulos JA. An expansive human regulatory lexicon encoded in transcription factor footprints. Nature, 489(7414):83-90, 2012.
- **DOI:** [10.1038/nature11212](https://doi.org/10.1038/nature11212)
- **PMID:** 22955618 | **PMC:** PMC3736026
- **Citations:** ~1,200
- **Key findings:** First genome-wide census of TF footprints from DNase-seq data across 41 diverse human cell types. Identified ~8.4 million distinct TF occupancy events involving 475 sequence motifs. Demonstrated that digital genomic footprinting from deep DNase-seq can detect individual TF binding events with nucleotide precision. Revealed regulatory motif co-occurrence patterns and cell-type-specific regulatory lexicons. Established the computational methodology for DNase-seq footprinting that forms the basis for this pipeline's footprinting analysis.

---

## Supplementary Tools (Non-DNase-Specific)

See pipeline-chipseq/references/literature.md for detailed descriptions of shared tools.

---

### Li & Durbin 2009 — BWA

- **DOI:** [10.1093/bioinformatics/btp324](https://doi.org/10.1093/bioinformatics/btp324) | **PMID:** 19451168 | **Citations:** ~25,000
- **DNase-seq role:** Read alignment with BWA-MEM. Same alignment approach as ChIP-seq. MAPQ filtering removes multi-mapped reads that could create false DHS calls.

---

### Li et al. 2009 — SAMtools

- **DOI:** [10.1093/bioinformatics/btp352](https://doi.org/10.1093/bioinformatics/btp352) | **PMID:** 19505943 | **Citations:** ~53,700
- **DNase-seq role:** BAM sorting, filtering, and indexing. Used for MAPQ filtering, coordinate sorting, and computing alignment statistics.

---

### Broad Institute — Picard MarkDuplicates

- **URL:** [https://broadinstitute.github.io/picard/](https://broadinstitute.github.io/picard/)
- **DNase-seq role:** PCR duplicate marking and library complexity estimation. NRF, PBC1, PBC2 metrics computed from Picard output. DNase-seq libraries can have moderate duplication rates due to the enzymatic digestion step.

---

### Quinlan & Hall 2010 — BEDTools

- **DOI:** [10.1093/bioinformatics/btq033](https://doi.org/10.1093/bioinformatics/btq033) | **PMID:** 20110278 | **Citations:** ~12,000
- **DNase-seq role:** Used for blacklist region filtering, SPOT score calculation (reads in hotspots), and peak annotation with gene models.

---

### Amemiya et al. 2019 — ENCODE Blacklist

- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | **PMID:** 31249361 | **Citations:** ~1,372
- **DNase-seq role:** Blacklist v2 filtering is essential for DNase-seq because DNase I can preferentially cut accessible regions in blacklisted repetitive elements, creating artifact peaks.

---

### Ewels et al. 2016 — MultiQC

- **DOI:** [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354) | **PMID:** 27312411 | **Citations:** ~6,800
- **DNase-seq role:** Aggregates QC metrics from FastQC, BWA alignment, Picard deduplication, and Hotspot2 into a unified HTML report for batch-level quality assessment.

---

### Andrews 2010 — FastQC

- **URL:** [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- **DNase-seq role:** Raw read quality assessment. DNase-seq libraries typically show characteristic fragment size distributions with a peak at sub-nucleosomal sizes (50-100 bp).

---

### Martin 2011 — Cutadapt (basis for Trim Galore)

- **DOI:** [10.14806/ej.17.1.200](https://doi.org/10.14806/ej.17.1.200) | **Citations:** ~13,000
- **DNase-seq role:** Adapter trimming with Trim Galore. Important for DNase-seq because short sub-nucleosomal fragments frequently read through into adapters, similar to ATAC-seq.
