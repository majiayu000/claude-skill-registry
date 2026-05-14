# UCSC Genome Browser — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the ucsc-browser skill — papers describing the UCSC Genome Browser infrastructure, data retrieval tools, file formats, and coordinate systems used for genome visualization and data access.

---

### Kent et al. 2002 — The UCSC Genome Browser

- **Citation:** Kent WJ, Sugnet CW, Furey TS, Roskin KM, Pringle TH, Zahler AM, Haussler D. The human genome browser at UCSC. *Genome Research*, 12(6), 996-1006, 2002.
- **DOI:** [10.1101/gr.229102](https://doi.org/10.1101/gr.229102)
- **PMID:** 12045153 | **PMC:** PMC186604
- **Citations:** ~5,000
- **Key findings:** Introduced the UCSC Genome Browser as a web-based tool for visualizing genome annotations at any scale. The browser displays assembly contigs, mRNA alignments, gene predictions, cross-species homologies, SNPs, and repeats as coregistered tracks. This is the foundational paper for the genome browser infrastructure that ENCODE data is visualized on, and it remains the primary citation for any workflow involving UCSC Browser data access.

---

### Karolchik et al. 2004 — The UCSC Table Browser

- **Citation:** Karolchik D, Hinrichs AS, Furey TS, Roskin KM, Sugnet CW, Haussler D, Kent WJ. The UCSC Table Browser data retrieval tool. *Nucleic Acids Research*, 32(Database issue), D493-D496, 2004.
- **DOI:** [10.1093/nar/gkh103](https://doi.org/10.1093/nar/gkh103)
- **PMID:** 14681465 | **PMC:** PMC308837
- **Citations:** ~3,000
- **Key findings:** Described the Table Browser, a text-based data retrieval interface for the UCSC Genome Browser Database. It supports field-value restrictions, free-form SQL queries, and combined queries on multiple tables, with output in formats that can be uploaded as custom tracks. This tool is essential for programmatic extraction of ENCODE annotations, intersection of genomic features, and bulk data retrieval from the UCSC database.

---

### Hinrichs et al. 2006 — UCSC chain/net alignments and coordinate liftover

- **Citation:** Hinrichs AS, Karolchik D, Baertsch R, Barber GP, Bejerano G, Clawson H, Diekhans M, Furey TS, Harte RA, Hsu F, Hillman-Jackson J, Kuhn RM, Pedersen JS, Pohl A, Raney BJ, Rosenbloom KR, Siepel A, Smith KE, Sugnet CW, Sultan-Qurraie A, Thomas DJ, Trumbower H, Weber RJ, Weirauch M, Zweig AS, Haussler D, Kent WJ. The UCSC Genome Browser Database: update 2006. *Nucleic Acids Research*, 34(Database issue), D590-D598, 2006.
- **DOI:** [10.1093/nar/gkj144](https://doi.org/10.1093/nar/gkj144)
- **PMID:** 16381938 | **PMC:** PMC1347506
- **Citations:** ~1,200
- **Key findings:** Detailed the chain/net alignment framework used for cross-species genome comparisons and coordinate liftover between assemblies. The chain format represents pairwise alignments that allow gaps in both sequences, while nets capture the best reciprocal alignments. This system underlies the liftOver tool critical for converting ENCODE annotations between genome assemblies (e.g., hg19 to GRCh38), a common requirement in integrative genomic analysis.

---

### Kent et al. 2010 — BigWig and BigBed file formats

- **Citation:** Kent WJ, Zweig AS, Barber G, Hinrichs AS, Karolchik D. BigWig and BigBed: enabling browsing of large distributed datasets. *Bioinformatics*, 26(17), 2204-2207, 2010.
- **DOI:** [10.1093/bioinformatics/btq351](https://doi.org/10.1093/bioinformatics/btq351)
- **PMID:** 20639541 | **PMC:** PMC2922891
- **Citations:** ~1,500
- **Key findings:** Introduced the BigWig and BigBed compressed binary indexed file formats that enable efficient display of large genomic datasets. These formats use R-trees and multi-resolution data storage so that only data needed for the current view is transmitted. BigWig is the standard format for ENCODE signal tracks (fold change, p-value), and BigBed is used for peak calls and other interval annotations, making this paper essential for understanding ENCODE file formats.

---

### Raney et al. 2014 — Track Data Hubs for custom data visualization

- **Citation:** Raney BJ, Dreszer TR, Barber GP, Clawson H, Fujita PA, Wang T, Nguyen N, Paten B, Zweig AS, Karolchik D, Kent WJ. Track data hubs enable visualization of user-defined genome-wide annotations on the UCSC Genome Browser. *Bioinformatics*, 30(7), 1003-1005, 2014.
- **DOI:** [10.1093/bioinformatics/btt637](https://doi.org/10.1093/bioinformatics/btt637)
- **PMID:** 24227676 | **PMC:** PMC3967101
- **Citations:** ~600
- **Key findings:** Described Track Data Hubs, a mechanism for displaying remotely hosted custom annotation data on the UCSC Genome Browser without uploading data to UCSC servers. Hubs enable integration of large datasets like ENCODE by hosting BigWig and BigBed files on external servers while maintaining the full browser visualization experience. This is the standard method for sharing and visualizing custom ENCODE analysis results.

---

### Haeussler et al. 2019 — UCSC Genome Browser 2019 update

- **Citation:** Haeussler M, Zweig AS, Tyner C, Speir ML, Rosenbloom KR, Raney BJ, Lee CM, Lee BT, Hinrichs AS, Gonzalez JN, Gibson D, Diekhans M, Clawson H, Casper J, Barber GP, Haussler D, Kuhn RM, Kent WJ. The UCSC Genome Browser database: 2019 update. *Nucleic Acids Research*, 47(D1), D853-D858, 2019.
- **DOI:** [10.1093/nar/gky1095](https://doi.org/10.1093/nar/gky1095)
- **PMID:** 30407534 | **PMC:** PMC6323953
- **Citations:** ~1,500
- **Key findings:** Documented major updates including the addition of gnomAD, TCGA expression, GTEx eQTLs, CRISPR guides, and a 30-way primate alignment. Introduced new tools for interactive arrangement of graphing tracks, new formats for chromosome interactions, and ChIP-Seq peak display for track hubs. These features directly support visualization of ENCODE regulatory element annotations alongside population genetics and expression data.

---

### Navarro Gonzalez et al. 2021 — UCSC 2021 update with ENCODE integration

- **Citation:** Navarro Gonzalez J, Zweig AS, Speir ML, Schmelter D, Rosenbloom KR, Raney BJ, Powell CC, Nassar LR, Maulding ND, Lee CM, Lee BT, Hinrichs AS, Fyfe AC, Fernandes JD, Diekhans M, Clawson H, Casper J, Benet-Pages A, Barber GP, Haussler D, Kuhn RM, Haeussler M, Kent WJ. The UCSC Genome Browser database: 2021 update. *Nucleic Acids Research*, 49(D1), D1046-D1057, 2021.
- **DOI:** [10.1093/nar/gkaa1070](https://doi.org/10.1093/nar/gkaa1070)
- **PMID:** 33221922 | **PMC:** PMC7779060
- **Citations:** ~400
- **Key findings:** Reported the integration of the ENCODE registry of candidate cis-regulatory elements (cCREs) as a native browser track, alongside Hi-C heatmap display and phased VCF visualization. The addition of ENCODE cCREs directly into the browser interface enables researchers to overlay their data with the definitive catalog of regulatory elements, making this update particularly relevant for any workflow that connects ENCODE annotations with custom experimental data.

---
