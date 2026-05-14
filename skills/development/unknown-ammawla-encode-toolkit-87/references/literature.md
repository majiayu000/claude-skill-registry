# Liftover Coordinates — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the liftover-coordinates skill — papers on genome assembly conversion tools, chain file generation, and the practical considerations for coordinate liftover between reference assemblies.

---

## Assembly Conversion Tools

---

### Kent et al. 2002 — UCSC Genome Browser and liftOver

- **Citation:** Kent WJ, Sugnet CW, Furey TS, Roskin KM, Pringle TH, Zahler AM, Haussler D. The human genome browser at UCSC. Genome Research, 12(6):996-1006, 2002.
- **DOI:** [10.1101/gr.229102](https://doi.org/10.1101/gr.229102)
- **PMID:** 12045153 | **PMC:** PMC186604
- **Citations:** ~8,000
- **Key findings:** Introduced the UCSC Genome Browser infrastructure including the liftOver tool for converting genomic coordinates between assembly versions. liftOver uses chain files that encode the pairwise alignment between two assemblies and maps coordinates through these alignments. The tool handles insertions, deletions, and rearrangements between assemblies by splitting features that span breakpoints and reporting unmapped regions. liftOver is the ENCODE-recommended tool for BED, narrowPeak, and other interval-based formats. Supports -minMatch parameter (default 0.95) to control the fraction of bases that must remap.

---

### Zhao et al. 2014 — CrossMap: coordinate conversion for multi-format genomic data

- **Citation:** Zhao H, Sun Z, Wang J, Huang H, Kocher JP, Wang L. CrossMap: a versatile tool for coordinate conversion between genome assemblies. Bioinformatics, 30(7):1006-1007, 2014.
- **DOI:** [10.1093/bioinformatics/btt730](https://doi.org/10.1093/bioinformatics/btt730)
- **PMID:** 24351709 | **PMC:** PMC3967108
- **Citations:** ~500
- **Key findings:** Introduced CrossMap, a versatile coordinate conversion tool that handles formats beyond BED: VCF (variant calls), BAM/SAM (alignments), bigWig (signal tracks), GFF/GTF (gene annotations), and Wiggle files. CrossMap properly handles VCF files by updating not just coordinates but also reference/alternate alleles when strand changes occur during liftover. The ENCODE liftover-coordinates skill recommends CrossMap for VCF and bigWig files (where UCSC liftOver has limited support) and UCSC liftOver for BED-based formats.

---

### Hinrichs et al. 2006 — UCSC Genome Browser database

- **Citation:** Hinrichs AS, Karolchik D, Baertsch R, Barber GP, Bejerano G, Clawson H, Diekhans M, Furey TS, Harte RA, Hsu F, Hillman-Jackson J, Kuhn RM, Pedersen JS, Pohl A, Raney BJ, Rosenbloom KR, Siepel A, Smith KE, Sugnet CW, Sultan-Qurraie A, Thomas DJ, Trumbower H, Weber RJ, Weirauch M, Zweig AS, Haussler D, Kent WJ. The UCSC Genome Browser Database: update 2006. Nucleic Acids Research, 34(Database issue):D590-D598, 2006.
- **DOI:** [10.1093/nar/gkj144](https://doi.org/10.1093/nar/gkj144)
- **PMID:** 16381938 | **PMC:** PMC1347506
- **Citations:** ~1,200
- **Key findings:** Documents the UCSC Genome Browser database including the chain file infrastructure used for coordinate liftover. Chain files are generated from whole-genome alignments between two assemblies and encode the correspondence between coordinate systems. The UCSC downloads site provides pre-computed chain files for all major assembly pairs (hg19↔hg38, hg38↔mm10, mm9↔mm10, etc.). Chain files are the critical reference input for both liftOver and CrossMap.

---

## Assembly Standards

---

### Schneider et al. 2017 — GRCh38: Genome Reference Consortium human build 38

- **Citation:** Schneider VA, Graves-Lindsay T, Howe K, Bouk N, Chen HC, Kitts PA, Murphy TD, Pruitt KD, Tello-Ruiz MK, Erber J, Phan L, Robbertse B, Schoch CL, Vnencak-Jones CL, Renfree MB, Havlak P, Seidl CJ, Church DM. Evaluation of GRCh38 and de novo haploid genome assemblies demonstrates the enduring quality of the reference assembly. Genome Research, 27(5):849-864, 2017.
- **DOI:** [10.1101/gr.213611.116](https://doi.org/10.1101/gr.213611.116)
- **PMID:** 28396521 | **PMC:** PMC5411779
- **Citations:** ~200
- **Key findings:** Describes the GRCh38 human reference assembly, the ENCODE standard for human data. Key differences from GRCh37/hg19: addition of alternate loci, centromere representation, improved sequence accuracy in segmental duplications, and ~400 sequence patches. These structural differences mean that liftover between hg19 and GRCh38 involves not just coordinate shifts but genuine sequence differences, with expected loss rates of 1-5% of regions (higher in complex loci like HLA, segmental duplications, and centromeric regions).

---

### ENCODE Project Consortium 2020 — Assembly standards

- **Citation:** ENCODE Project Consortium et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature, 583(7818):699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,500
- **Key findings:** ENCODE Phase 3 established GRCh38 as the standard human assembly and mm10 (GRCm38) as the standard mouse assembly. All ENCODE processed data files use these assemblies. Liftover is required when integrating ENCODE data with older datasets processed on hg19/hg18 or mm9. The ENCODE portal provides assembly-specific file versions, reducing but not eliminating the need for liftover in multi-source analyses.

---

## Practical Considerations

---

### Castel et al. 2015 — Tools for resolving reference bias in allele-specific analysis

- **Citation:** Castel SE, Levy-Moonshine A, Mohammadi P, Banks E, Lappalainen T. Tools and best practices for data processing in allelic expression analysis. Genome Biology, 16:195, 2015.
- **DOI:** [10.1186/s13059-015-0762-6](https://doi.org/10.1186/s13059-015-0762-6)
- **PMID:** 26381377 | **PMC:** PMC4573554
- **Citations:** ~300
- **Key findings:** While focused on allele-specific analysis, this paper documents practical challenges of coordinate conversion including: reference allele changes between assemblies affecting variant interpretation, multi-mapping regions where coordinates are ambiguous, and the critical requirement to re-validate functional annotations after liftover. Relevant to the liftover-coordinates skill because it establishes that liftover is not just a coordinate transformation — downstream interpretation may change when the reference sequence itself differs between assemblies.
