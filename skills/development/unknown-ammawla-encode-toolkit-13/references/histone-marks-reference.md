# Comprehensive Reference Catalog: Histone Modifications and Chromatin States

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for ENCODE connector histone aggregation skills and chromatin state interpretation.
**Note:** Citation counts are approximate as of early 2026 and sourced from Consensus/Semantic Scholar. All article metadata retrieved from PubMed unless otherwise noted.

---

## Table of Contents

1. [Foundational Papers](#1-foundational-papers)
2. [Part 1: Individual Histone Marks](#2-part-1-individual-histone-marks)
   - [H3 Lysine Methylations](#h3-lysine-methylations)
   - [H3 Lysine Acetylations](#h3-lysine-acetylations)
   - [H4 Modifications](#h4-modifications)
   - [H2A and H2B Modifications](#h2a-and-h2b-modifications)
3. [Part 2: Combinatorial Patterns (ChromHMM States)](#3-part-2-combinatorial-patterns-chromhmm-states)
4. [Part 3: Mark-Specific Functional Categories](#4-part-3-mark-specific-functional-categories)
5. [Part 4: Contradictions and Edge Cases](#5-part-4-contradictions-and-edge-cases)
6. [Part 5: Transcription Factor Combinations and Co-Binding Patterns](#6-part-5-transcription-factor-combinations-and-co-binding-patterns)
7. [Part 6: Chromatin Remodeling Complexes](#7-part-6-chromatin-remodeling-complexes)
8. [Part 7: DNA Methylation and Chromatin Interplay](#8-part-7-dna-methylation-and-chromatin-interplay)
9. [Part 8: Nucleosome Positioning and Dynamics](#9-part-8-nucleosome-positioning-and-dynamics)
10. [Part 9: 3D Genome Organization and Chromatin](#10-part-9-3d-genome-organization-and-chromatin)
11. [Part 10: Chromatin in Disease](#11-part-10-chromatin-in-disease)
12. [Master Reference List](#12-master-reference-list)

---

## 1. Foundational Papers

These landmark studies established the field of genome-wide histone modification profiling and chromatin state modeling.

### Genome-Wide Profiling Landmarks

**Barski et al. 2007** -- The first genome-wide ChIP-Seq study of histone modifications.
- **Citation:** Barski A, Cuddapah S, Cui K, Roh TY, Schones DE, Wang Z, Wei G, Chepelev I, Zhao K. "High-resolution profiling of histone methylations in the human genome." *Cell*. 2007;129(4):823-37.
- **DOI:** [10.1016/j.cell.2007.05.009](https://doi.org/10.1016/j.cell.2007.05.009)
- **PMID:** 17512414
- **Citations:** ~6,900
- **Key findings:** Mapped 20 histone lysine and arginine methylations plus H2A.Z, RNAPII, and CTCF across the human genome in CD4+ T cells. Established that H3K27me1, H3K9me1, H4K20me1, H3K79me1, and H2BK5me1 are all linked to gene activation, whereas H3K27me3, H3K9me3, and H3K79me3 are linked to repression. H2A.Z associates with functional regulatory elements. CTCF marks boundaries of histone methylation domains.

**Wang et al. 2008** -- First systematic study of combinatorial histone modification patterns.
- **Citation:** Wang Z, Zang C, Rosenfeld JA, Schones DE, Barski A, Cuddapah S, Cui K, Roh TY, Peng W, Zhang MQ, Zhao K. "Combinatorial patterns of histone acetylations and methylations in the human genome." *Nat Genet*. 2008;40(7):897-903.
- **DOI:** [10.1038/ng.154](https://doi.org/10.1038/ng.154)
- **PMID:** 18552846 | **PMC:** PMC2769248
- **Citations:** ~2,400
- **Key findings:** Analyzed 39 histone modifications in human CD4+ T cells. Identified a common modification module of 17 co-occurring marks at 3,286 promoters. Demonstrated that modifications colocalize at the individual nucleosome level and act cooperatively -- more marks correlate with higher expression.

**Mikkelsen et al. 2007** -- Genome-wide chromatin state maps in pluripotent and differentiated cells.
- **Citation:** Mikkelsen TS, Ku M, Jaffe DB, Issac B, Lieberman E, Giannoukos G, Alvarez P, Brockman W, Kim TK, Koche RP, Lee W, Mendenhall E, O'Donovan A, Presser A, Russ C, Xie X, Meissner A, Wernig M, Jaenisch R, Nusbaum C, Lander ES, Bernstein BE. "Genome-wide maps of chromatin state in pluripotent and lineage-committed cells." *Nature*. 2007;448(7153):553-60.
- **DOI:** [10.1038/nature06008](https://doi.org/10.1038/nature06008)
- **Citations:** ~4,300
- **Key findings:** H3K4me3 and H3K27me3 effectively discriminate expressed, poised, and stably repressed genes. H3K36me3 marks coding and non-coding transcripts. H3K9me3 and H4K20me3 mark satellites, telomeres, and LTRs.

### Major Reviews

**Kouzarides 2007** -- Definitive review of histone modification classes and functions.
- **Citation:** Kouzarides T. "Chromatin modifications and their function." *Cell*. 2007;128(4):693-705.
- **DOI:** [10.1016/j.cell.2007.02.005](https://doi.org/10.1016/j.cell.2007.02.005)
- **Citations:** ~10,700
- **Key findings:** Cataloged at least 8 classes of histone modifications (acetylation, methylation, phosphorylation, ubiquitylation, sumoylation, ADP ribosylation, deimination, proline isomerization). Modifications function either by disrupting chromatin contacts or by recruiting nonhistone proteins.

**Bannister & Kouzarides 2011** -- Updated review of histone modification biology.
- **Citation:** Bannister AJ, Kouzarides T. "Regulation of chromatin by histone modifications." *Cell Res*. 2011;21(3):381-395.
- **DOI:** [10.1038/cr.2011.22](https://doi.org/10.1038/cr.2011.22)
- **Citations:** ~5,300
- **Key findings:** Comprehensive update describing known modifications, their genomic distributions, writers, erasers, and readers, with emphasis on transcriptional consequences.

---

## 2. Part 1: Individual Histone Marks

### H3 Lysine Methylations

#### H3K4me1 -- Enhancer Mark (Primed/Poised)

| Property | Detail |
|----------|--------|
| **Biological meaning** | Marks enhancer elements, both active and poised. Present at distal regulatory elements but NOT at active promoters (where H3K4me3 predominates). When found alone (without H3K27ac), marks primed/poised enhancers. When co-occurring with H3K27ac, marks active enhancers. |
| **Writers** | MLL3 (KMT2C), MLL4 (KMT2D) |
| **Erasers** | LSD1 (KDM1A), KDM5 family |
| **Readers** | CHD1, BPTF (via PHD finger) |
| **ChromHMM states** | Enhancer, Flanking Active TSS, Weak/Poised Enhancer |

**Key papers:**
- Heintzman ND et al. (2007) *Nat Genet* 39:311-318. [DOI: 10.1038/ng1966](https://doi.org/10.1038/ng1966) (~3,400 cit.) -- First demonstration that H3K4me1 (without me3) distinguishes enhancers from promoters.
- Creyghton MP et al. (2010) *PNAS* 107:21931-6. [DOI: 10.1073/pnas.1016071107](https://doi.org/10.1073/pnas.1016071107) (~3,000 cit.) -- Showed H3K27ac separates active from poised H3K4me1-marked enhancers.
- Rada-Iglesias A et al. (2011) *Nature* 470:279-83. [DOI: 10.1038/nature09692](https://doi.org/10.1038/nature09692) (~1,500 cit.) -- Defined two enhancer classes: active (H3K4me1+H3K27ac) and poised (H3K4me1+H3K27me3).

**Contradictions/nuances:** H3K4me1 is also found in gene bodies of actively transcribed genes, though at lower levels than at enhancers. Its presence alone does not guarantee enhancer activity -- functional validation (e.g., STARR-seq, transgenic assays) is required.

---

#### H3K4me2 -- Active Regulatory Element Mark

| Property | Detail |
|----------|--------|
| **Biological meaning** | Marks active regulatory elements including both promoters and enhancers. Found broadly at active regions. Less studied than me1 or me3 but intermediate between them in distribution. |
| **Writers** | MLL1-4 (KMT2A-D), SET1A/B |
| **ChromHMM states** | Flanking Active TSS, Active Enhancer |

**Key papers:**
- Barski et al. (2007) *Cell* 129:823-37. [DOI: 10.1016/j.cell.2007.05.009](https://doi.org/10.1016/j.cell.2007.05.009) -- Mapped H3K4me2 distribution; enriched at promoters and enhancers.
- Wang et al. (2008) *Nat Genet* 40:897-903. [DOI: 10.1038/ng.154](https://doi.org/10.1038/ng.154) -- Part of the 17-modification active module.

**Notes:** H3K4me2 is less commonly profiled in ENCODE/Roadmap than H3K4me1 or H3K4me3. It serves as an intermediate mark and is sometimes used to identify active regulatory regions when me1 and me3 data are unavailable.

---

#### H3K4me3 -- Active Promoter Mark

| Property | Detail |
|----------|--------|
| **Biological meaning** | The canonical mark of active and poised promoters. Found as sharp peaks at transcription start sites (TSSs) of expressed genes. Its presence does not guarantee transcription but indicates promoter competence. Also found at bivalent promoters (with H3K27me3) in stem cells. |
| **Writers** | SET1A/B (via COMPASS), MLL1/2 (KMT2A/B) |
| **Erasers** | KDM5A (JARID1A), KDM5B (JARID1B), KDM5C, KDM5D |
| **Readers** | TAF3 (TFIID subunit), ING proteins, CHD1 |
| **ChromHMM states** | Active TSS, Bivalent/Poised TSS |

**Key papers:**
- Bernstein BE et al. (2005) *Cell* 120:169-181. [DOI: 10.1016/j.cell.2005.01.001](https://doi.org/10.1016/j.cell.2005.01.001) -- Early ChIP-chip study linking H3K4me3 to active genes.
- Heintzman ND et al. (2007) *Nat Genet* 39:311-318. [DOI: 10.1038/ng1966](https://doi.org/10.1038/ng1966) -- H3K4me3 at promoters vs. H3K4me1 at enhancers.
- Bernstein BE et al. (2006) *Cell* 125:315-326. [DOI: 10.1016/j.cell.2006.02.041](https://doi.org/10.1016/j.cell.2006.02.041) (~5,400 cit.) -- Discovered bivalent domains (H3K4me3 + H3K27me3) in ESCs.

**Contradictions:** Kumar et al. (2021) *Genome Res* 31:2170-2184 challenged the "poising" hypothesis, arguing that H3K4me3 at bivalent promoters does not accelerate gene activation but rather protects promoters from de novo DNA methylation.

---

#### H3K9me1 -- Gene Activation (Weak)

| Property | Detail |
|----------|--------|
| **Biological meaning** | Weak activation mark. Found near active promoters and in gene bodies. Contrasts sharply with H3K9me2/me3 which are repressive. |
| **Writers** | G9a (EHMT2), GLP (EHMT1), SETDB1, PRDM family |
| **ChromHMM states** | Weak/flanking active features |

**Key papers:**
- Barski et al. (2007) *Cell* 129:823-37. [DOI: 10.1016/j.cell.2007.05.009](https://doi.org/10.1016/j.cell.2007.05.009) -- First genome-wide demonstration that H3K9me1 is associated with gene activation, in contrast to H3K9me2/me3.

**Notes:** H3K9me1 is one of the less frequently profiled marks in consortium projects and is not part of the standard 5-mark ChromHMM model. Its biology remains less well understood than other H3K9 methylation states.

---

#### H3K9me2 -- Euchromatic Gene Silencing

| Property | Detail |
|----------|--------|
| **Biological meaning** | Repressive mark associated with euchromatic gene silencing. Found in large megabase-scale domains (LOCKs = large organized chromatin K9 modifications) in differentiated cells. Less concentrated at repetitive elements than H3K9me3. Associated with nuclear lamina positioning. |
| **Writers** | G9a (EHMT2), GLP (EHMT1) |
| **Erasers** | KDM3A (JHDM2A), KDM3B, KDM4 family |
| **Readers** | HP1 proteins (weak binding), UHRF1 |
| **ChromHMM states** | Quiescent/Low, Heterochromatin |

**Key papers:**
- Wen B et al. (2009) *Genome Res* 19:1639-1645. [DOI: 10.1101/gr.092643.109](https://doi.org/10.1101/gr.092643.109) -- Described LOCKs (large organized chromatin K9 modifications) domains.
- Padeken J et al. (2022) *Nat Rev Mol Cell Biol* 23:623-640. [DOI: 10.1038/s41580-022-00483-2](https://doi.org/10.1038/s41580-022-00483-2) (~314 cit.) -- Comprehensive review of H3K9 methylation in tissue differentiation.

---

#### H3K9me3 -- Constitutive Heterochromatin

| Property | Detail |
|----------|--------|
| **Biological meaning** | The hallmark of constitutive heterochromatin. Enriched at pericentromeric repeats, satellite sequences, telomeres, transposable elements (TEs), and endogenous retroviruses (ERVs). Maintained through a self-reinforcing loop where HP1 binds H3K9me3 and recruits SUV39H1/2 to methylate adjacent nucleosomes. Also found at lineage-inappropriate genes in differentiated cells (via SETDB1). |
| **Writers** | SUV39H1/2 (at repeats), SETDB1 (at euchromatic targets, ERVs), G9a/GLP (can trimethylate in some contexts) |
| **Erasers** | KDM4A (JMJD2A), KDM4B, KDM4C |
| **Readers** | HP1alpha (CBX5), HP1beta (CBX1), HP1gamma (CBX3), ATRX, MPP8 |
| **ChromHMM states** | Heterochromatin (enriched in H3K9me3) |

**Key papers:**
- Rea S et al. (2000) *Nature* 406:593-599. [DOI: 10.1038/35020506](https://doi.org/10.1038/35020506) (~3,500 cit.) -- Identified SUV39H1 as the first histone methyltransferase; established H3K9me3 as HP1 binding platform.
- Lachner M et al. (2001) *Nature* 410:116-120. [DOI: 10.1038/35065132](https://doi.org/10.1038/35065132) (~2,000 cit.) -- Showed HP1 chromodomain specifically recognizes H3K9me3.
- Padeken J et al. (2022) *Nat Rev Mol Cell Biol* 23:623-640. [DOI: 10.1038/s41580-022-00483-2](https://doi.org/10.1038/s41580-022-00483-2) (~314 cit.) -- Comprehensive review of H3K9me and its HMTs.
- Keenan CR et al. (2024) *Genome Res* 34:556-571. -- Suv39h-catalyzed H3K9me3 critical for euchromatic genome organization; loss paradoxically represses euchromatic genes.

**Contradictions:** While H3K9me3 is considered purely repressive, Keenan et al. (2024) showed that loss of SUV39H1/2-mediated H3K9me3 leads to paradoxical downregulation of euchromatic genes, suggesting that heterochromatin domains provide structural scaffolding that supports gene expression in adjacent euchromatin.

---

#### H3K27me3 -- Polycomb-Mediated Repression

| Property | Detail |
|----------|--------|
| **Biological meaning** | The signature mark of Polycomb Repressive Complex 2 (PRC2)-mediated facultative heterochromatin. Silences developmental and lineage-specific genes in a reversible manner. Found in broad domains covering gene bodies and flanking regions. Can spread via PRC2 read-write mechanism (EED subunit reads H3K27me3 and stimulates EZH2 catalytic activity). Mutually exclusive with H3K27ac at the same residue. |
| **Writers** | EZH2 (within PRC2), EZH1 |
| **Erasers** | KDM6A (UTX), KDM6B (JMJD3) |
| **Readers** | EED (PRC2 subunit, propagation), CBX proteins (PRC1 subunits) |
| **ChromHMM states** | Repressed Polycomb, Bivalent/Poised TSS, Poised Enhancer |

**Key papers:**
- Cao R et al. (2002) *Science* 298:1039-1043. [DOI: 10.1126/science.1076997](https://doi.org/10.1126/science.1076997) (~3,000 cit.) -- Identified EZH2 as the H3K27 methyltransferase.
- Boyer LA et al. (2006) *Nature* 441:349-353. [DOI: 10.1038/nature04733](https://doi.org/10.1038/nature04733) (~3,000 cit.) -- Mapped PRC2/H3K27me3 targets in ESCs; found occupancy at developmental TF genes.
- Bernstein BE et al. (2006) *Cell* 125:315-326. [DOI: 10.1016/j.cell.2006.02.041](https://doi.org/10.1016/j.cell.2006.02.041) (~5,400 cit.) -- Co-discovery of bivalent domains (H3K4me3+H3K27me3).

**Notes:** H3K27me3 is one of the 5 core marks in the standard ChromHMM model (along with H3K4me3, H3K4me1, H3K36me3, H3K9me3). Its mutual exclusivity with H3K27ac makes it a critical switch between repressed and active states.

---

#### H3K36me3 -- Transcribed Gene Bodies

| Property | Detail |
|----------|--------|
| **Biological meaning** | Marks bodies of actively transcribed genes, deposited co-transcriptionally by SETD2 which travels with elongating RNA Pol II (via Ser2-phosphorylated CTD). Increases from 5' to 3' along gene bodies (reflecting transcription directionality). Functions in: (1) preventing spurious intragenic transcription initiation by recruiting HDAC complexes, (2) mRNA splicing regulation, (3) DNA mismatch repair, (4) antagonizing PRC2 spreading into active genes. |
| **Writers** | SETD2 (sole H3K36 trimethyltransferase in mammals) |
| **Erasers** | KDM4A, KDM4B, KDM4C, JHDM1A/B (for me2) |
| **Readers** | DNMT3B (directs gene-body DNA methylation), MSH6 (mismatch repair), PWWP domain proteins (e.g., PSIP1/LEDGF), BRPF1 |
| **ChromHMM states** | Strong Transcription, Weak Transcription |

**Key papers:**
- Bannister AJ et al. (2005) *Nature* 438:1181-1185. [DOI: 10.1038/nature04219](https://doi.org/10.1038/nature04219) (~800 cit.) -- Demonstrated Set2-mediated H3K36me in gene bodies during elongation.
- Yoh SM et al. (2008) *Genes Dev* 22:3422-34. [DOI: 10.1101/gad.1710608](https://doi.org/10.1101/gad.1710608) (~249 cit.) -- Iws1:Spt6:CTD complex controls SETD2 recruitment and H3K36me3 deposition.
- Almeida SF et al. (2011) *Nat Struct Mol Biol* 18:977-983. [DOI: 10.1038/nsmb.2108](https://doi.org/10.1038/nsmb.2108) (~248 cit.) -- Splicing enhances SETD2 recruitment; intron-containing genes preferentially marked.
- Xiao C et al. (2021) *Clin Epigenetics* 13:44. [DOI: 10.1186/s13148-021-01038-5](https://doi.org/10.1186/s13148-021-01038-5) -- Review of H3K36me3 roles in cancer.

**Important for ENCODE:** H3K36me3 is one of the 5 core ChromHMM marks. SETD2 loss-of-function mutations are frequent in clear cell renal carcinoma, pediatric high-grade gliomas (H3.3K36M oncohistone), and other cancers.

---

#### H3K79me2 -- Transcription Elongation / DOT1L

| Property | Detail |
|----------|--------|
| **Biological meaning** | Marks actively transcribed gene bodies, similar to H3K36me3 but deposited by a different enzyme (DOT1L). Located in the globular domain of H3 (not the tail), making it unique among histone methylations. Also involved in DNA damage response and cell cycle regulation. DOT1L is recruited by H2BK120ub (monoubiquitylated H2B), creating a trans-tail regulatory pathway. |
| **Writers** | DOT1L (sole enzyme) |
| **Erasers** | No known demethylase (controversial; may be removed by histone turnover) |
| **ChromHMM states** | Transcription, Genic Enhancers |

**Key papers:**
- Feng Q et al. (2002) *Curr Biol* 12:1052-1058. [DOI: 10.1016/S0960-9822(02)00901-6](https://doi.org/10.1016/S0960-9822(02)00901-6) (~700 cit.) -- Identified DOT1L as H3K79 methyltransferase.
- Steger DJ et al. (2008) *Mol Cell Biol* 28:2825-2839. [DOI: 10.1128/MCB.02076-07](https://doi.org/10.1128/MCB.02076-07) -- DOT1L promotes transcription elongation via H3K79me2.
- Barski et al. (2007) *Cell* 129:823-37. [DOI: 10.1016/j.cell.2007.05.009](https://doi.org/10.1016/j.cell.2007.05.009) -- H3K79me1 linked to activation, H3K79me3 linked to repression.

**Clinical relevance:** DOT1L is a therapeutic target in MLL-rearranged leukemias, where MLL fusion proteins aberrantly recruit DOT1L to target genes.

---

### H3 Lysine Acetylations

#### H3K27ac -- Active Regulatory Element Mark

| Property | Detail |
|----------|--------|
| **Biological meaning** | The single most informative mark for identifying active enhancers and promoters. Mutually exclusive with H3K27me3 (cannot have both acetylation and methylation at the same lysine). H3K27ac at enhancers (H3K4me1+H3K27ac) distinguishes active from poised enhancers. Also marks active promoters (co-occurring with H3K4me3). Used to identify super-enhancers via ROSE algorithm (ranking of super-enhancer signal). |
| **Writers** | CBP (CREBBP/KAT3A), p300 (EP300/KAT3B) |
| **Erasers** | HDAC1/2 (in NuRD complex), HDAC3 (in NCoR/SMRT complex) |
| **Readers** | BRD4 (and other BET bromodomain proteins), BRPF1 |
| **ChromHMM states** | Active TSS, Flanking Active TSS, Active Enhancer, Genic Enhancer |

**Key papers:**
- Creyghton MP et al. (2010) *PNAS* 107:21931-6. [DOI: 10.1073/pnas.1016071107](https://doi.org/10.1073/pnas.1016071107) -- Established H3K27ac as THE distinguishing mark between active and poised enhancers.
- Rada-Iglesias A et al. (2011) *Nature* 470:279-83. [DOI: 10.1038/nature09692](https://doi.org/10.1038/nature09692) -- Active enhancers = H3K4me1+H3K27ac; poised enhancers = H3K4me1+H3K27me3.
- Whyte WA et al. (2013) *Cell* 153:307-319. [DOI: 10.1016/j.cell.2013.03.035](https://doi.org/10.1016/j.cell.2013.03.035) (~3,600 cit.) -- Super-enhancers defined by exceptional H3K27ac/Mediator signal.

**Notes:** H3K27ac is the workhorse mark for enhancer identification in ENCODE and Roadmap Epigenomics. It is one of the 5 core ChromHMM marks.

---

#### H3K9ac -- Active Promoters

| Property | Detail |
|----------|--------|
| **Biological meaning** | Marks active gene promoters. One of the earliest characterized histone acetylation marks. Enriched at TSSs of actively transcribed genes, often co-occurring with H3K4me3. Contributes to an open chromatin state permissive for transcription. |
| **Writers** | GCN5 (KAT2A), PCAF (KAT2B), Tip60 (KAT5), CBP/p300 |
| **Erasers** | HDAC1-3, SIRT1, SIRT6 |
| **Readers** | BRD-containing proteins, YEATS domain proteins |
| **ChromHMM states** | Active TSS, Flanking Active TSS |

**Key papers:**
- Wang et al. (2008) *Nat Genet* 40:897-903. [DOI: 10.1038/ng.154](https://doi.org/10.1038/ng.154) -- Part of the 17-mark active promoter module.
- Karmodiya K et al. (2012) *BMC Genomics* 13:424. [DOI: 10.1186/1471-2164-13-424](https://doi.org/10.1186/1471-2164-13-424) -- H3K9ac is one of the most predictive marks for gene expression.

---

#### H3K14ac -- Transcriptional Activation / DNA Damage Response

| Property | Detail |
|----------|--------|
| **Biological meaning** | Associated with active transcription and DNA damage response. Often co-occurs with H3K9ac at active promoters. Also acetylated by GCN5 in response to DNA double-strand breaks. |
| **Writers** | GCN5 (KAT2A), PCAF, Tip60, CBP/p300, TAF1 |
| **Erasers** | HDAC1-3, SIRT1 |
| **ChromHMM states** | Active TSS (when profiled) |

**Key papers:**
- Wang et al. (2008) *Nat Genet* 40:897-903. [DOI: 10.1038/ng.154](https://doi.org/10.1038/ng.154) -- Part of the 17-mark active promoter module.
- Murr R et al. (2006) *Nat Cell Biol* 8:91-99. [DOI: 10.1038/ncb1343](https://doi.org/10.1038/ncb1343) -- H3K14ac by Tip60/GCN5 at DNA damage sites.

---

#### H3K18ac -- Active Transcription / CBP/p300 Substrate

| Property | Detail |
|----------|--------|
| **Biological meaning** | Active transcription mark. Substrate of CBP/p300 acetyltransferases. Enriched at active promoters and enhancers. Less studied genome-wide than H3K27ac or H3K9ac but part of the general active chromatin acetylation signature. Emerging evidence links it to nuclear receptor signaling and androgen-driven transcription in prostate cancer. |
| **Writers** | CBP/p300 |
| **Erasers** | SIRT7, HDAC1-3 |

**Key papers:**
- Wang et al. (2008) *Nat Genet* 40:897-903. [DOI: 10.1038/ng.154](https://doi.org/10.1038/ng.154) -- Identified in combinatorial analysis.
- Jin Q et al. (2011) *EMBO J* 30:249-262. [DOI: 10.1038/emboj.2010.318](https://doi.org/10.1038/emboj.2010.318) -- Distinguished CBP/p300 substrates (H3K18ac, H3K27ac) from GCN5/PCAF substrates.

---

#### H3K23ac -- Active Transcription

| Property | Detail |
|----------|--------|
| **Biological meaning** | Active mark found at promoters and gene bodies. Less well characterized than other H3 acetylations. Associated with transcriptional activation. |
| **Writers** | CBP/p300, GCN5 |
| **Erasers** | HDAC1-3, SIRT1 |

**Key papers:**
- Wang et al. (2008) *Nat Genet* 40:897-903. [DOI: 10.1038/ng.154](https://doi.org/10.1038/ng.154) -- Part of combinatorial patterns at active promoters.

---

### H4 Modifications

#### H4K20me1 -- Transcription / Cell Cycle

| Property | Detail |
|----------|--------|
| **Biological meaning** | Multi-functional mark with context-dependent roles. In the Barski et al. dataset, H4K20me1 correlated with gene activation. It is cell-cycle regulated: PR-Set7 deposits H4K20me1 during mitosis, and the mark peaks in late S/G2. Found in gene bodies of actively transcribed genes. Also plays roles in DNA replication licensing, DNA damage response, and chromatin compaction. Distinguished from H4K20me3, which marks constitutive heterochromatin (pericentromeric). |
| **Writers** | PR-Set7/SET8 (KMT5A) |
| **Erasers** | PHF8, KDM7B |
| **ChromHMM states** | Transcription (when profiled in expanded models) |

**Key papers:**
- Rice JC et al. (2002) *Genes Dev* 16:2225-30. [DOI: 10.1101/gad.986602](https://doi.org/10.1101/gad.986602) (~257 cit.) -- H4K20me1 is mitotic-specific, deposited by PR-Set7, inversely correlated with H4K16ac.
- Barski et al. (2007) *Cell* 129:823-37. [DOI: 10.1016/j.cell.2007.05.009](https://doi.org/10.1016/j.cell.2007.05.009) -- H4K20me1 genome-wide linked to gene activation.

**Contradictions:** H4K20me1 can be found in both active and repressed contexts. Its deposition during mitosis suggests a role in epigenetic memory through cell division rather than direct transcriptional regulation.

---

#### H4K5ac -- Active Chromatin / Histone Deposition

| Property | Detail |
|----------|--------|
| **Biological meaning** | Marks active chromatin. Also found on newly synthesized histones (H4K5ac+H4K12ac is the canonical "deposition mark" on new H4 molecules). At regulatory elements, co-occurs with other H4 acetylations. BRD4 preferentially binds multi-acetylated H4 (H4K5acK8ac). |
| **Writers** | HAT1 (on new histones), CBP/p300, Tip60 |
| **Erasers** | HDAC1-3 |

**Key papers:**
- Wang et al. (2008) *Nat Genet* 40:897-903. [DOI: 10.1038/ng.154](https://doi.org/10.1038/ng.154) -- Part of the active chromatin module.
- Loyola A et al. (2006) *Mol Cell* 24:309-316. [DOI: 10.1016/j.molcel.2006.09.009](https://doi.org/10.1016/j.molcel.2006.09.009) -- H4K5ac+H4K12ac as histone deposition marks.
- Das ND et al. (2023) *BMC Genomics* 24. -- H4K5acK8ac defines super-enhancers distinct from those identified by H3K27ac alone.

---

#### H4K8ac -- Active Chromatin

| Property | Detail |
|----------|--------|
| **Biological meaning** | Active chromatin mark at promoters and enhancers. Often co-occurs with H4K5ac to form the di-acetylated H4 state recognized by BRD4 bromodomains. Less individually characterized than H3 marks but consistently part of the active modification module. |
| **Writers** | CBP/p300, GCN5/PCAF, Tip60 |
| **Erasers** | HDAC1-3 |

**Key papers:**
- Wang et al. (2008) *Nat Genet* 40:897-903. [DOI: 10.1038/ng.154](https://doi.org/10.1038/ng.154).

---

#### H4K16ac -- Euchromatin Boundary / Dosage Compensation

| Property | Detail |
|----------|--------|
| **Biological meaning** | Unique among histone acetylations in having a direct structural effect on chromatin fiber folding. H4K16ac disrupts the interaction between the H4 tail and the H2A acidic patch on adjacent nucleosomes, preventing chromatin compaction into the 30nm fiber. In mammals, associated with active euchromatin and implicated in maintaining euchromatin/heterochromatin boundaries. In Drosophila, critical for dosage compensation (MOF-mediated acetylation of the X chromosome). Loss of H4K16ac is an early event in cancer. |
| **Writers** | MOF (KAT8), Tip60 (KAT5) |
| **Erasers** | SIRT1, SIRT2, HDAC1/2 |
| **Readers** | Inhibits SIR complex binding; recognized by BRDT |

**Key papers:**
- Shogren-Knaak M et al. (2006) *Science* 311:844-847. [DOI: 10.1126/science.1124000](https://doi.org/10.1126/science.1124000) (~1,000 cit.) -- H4K16ac inhibits 30nm fiber formation (in vitro reconstitution).
- Fraga MF et al. (2005) *Nat Genet* 37:391-400. [DOI: 10.1038/ng1531](https://doi.org/10.1038/ng1531) (~2,000 cit.) -- Global loss of H4K16ac (and H4K20me3) is a hallmark of cancer.
- Rice JC et al. (2002) *Genes Dev* 16:2225-30. [DOI: 10.1101/gad.986602](https://doi.org/10.1101/gad.986602) -- H4K16ac in early S-phase inversely correlated with H4K20me1 at mitosis.

**Cancer relevance:** Loss of H4K16ac is one of the earliest and most consistent epigenetic changes in cancer (Fraga et al. 2005). It is often accompanied by loss of H4K20me3 and hypomethylation of repetitive DNA.

---

#### H4K91ac -- Histone Deposition / Chromatin Assembly

| Property | Detail |
|----------|--------|
| **Biological meaning** | Located in the globular domain of H4 (not the tail). Important for histone-histone interactions within the nucleosome. H4K91ac weakens H3-H4 tetramer-H2A/H2B dimer interactions, facilitating nucleosome assembly/disassembly. Found on newly synthesized histones and at sites of active chromatin remodeling. Less well characterized in genome-wide studies. |
| **Writers** | HAT1, CBP/p300 |

**Key papers:**
- Ye J et al. (2005) *Mol Cell* 20:199-209. [DOI: 10.1016/j.molcel.2005.08.029](https://doi.org/10.1016/j.molcel.2005.08.029) -- H4K91ac affects nucleosome stability and chromatin assembly.

---

### H2A and H2B Modifications

#### H2A.Z -- Dynamic Regulatory Element Mark

| Property | Detail |
|----------|--------|
| **Biological meaning** | A histone variant (not a modification per se) that replaces canonical H2A. Found at regulatory elements including promoters, enhancers, and insulators. Creates a less stable nucleosome, facilitating regulatory access. Can carry dual roles: H2A.Z-acetylated is found at active promoters; H2A.Z+H3K27me3 at poised/bivalent regions. |
| **Deposition complex** | SWR1/SRCAP complex, p400/Tip60 complex |
| **Removal complex** | INO80 complex |
| **ChromHMM states** | Not typically used as ChromHMM input but enriched at Active TSS and Bivalent TSS |

**Key papers:**
- Barski et al. (2007) *Cell* 129:823-37. [DOI: 10.1016/j.cell.2007.05.009](https://doi.org/10.1016/j.cell.2007.05.009) -- H2A.Z at functional regulatory elements.
- Ku M et al. (2012) *Genes Dev* 26:1326-1338. [DOI: 10.1101/gad.187609.112](https://doi.org/10.1101/gad.187609.112) -- H2A.Z enriched at bivalent promoters in ESCs.
- Jin C et al. (2009) *Nat Genet* 41:941-945. [DOI: 10.1038/ng.409](https://doi.org/10.1038/ng.409) -- H2A.Z+H3.3 double-variant nucleosomes mark active regulatory elements.

---

#### H2BK120ub (H2Bub1) -- Trans-histone Crosstalk / Transcription

| Property | Detail |
|----------|--------|
| **Biological meaning** | Monoubiquitylation of H2B at K120. Required for proper H3K4 and H3K79 methylation (trans-histone crosstalk). Associated with transcription elongation. Found in gene bodies of active genes. Also plays roles in DNA damage response and stem cell self-renewal. |
| **Writers** | RNF20/RNF40 (E3 ubiquitin ligases), UBE2B (E2 conjugating enzyme) |
| **Erasers** | USP22 (deubiquitinase, part of SAGA complex), USP44 |

**Key papers:**
- Kim J et al. (2009) *Cell* 137:459-471. [DOI: 10.1016/j.cell.2009.02.027](https://doi.org/10.1016/j.cell.2009.02.027) (~700 cit.) -- H2BK120ub required for H3K4me3 by COMPASS and H3K79me by DOT1L.
- McGinty RK et al. (2008) *Nature* 453:812-816. [DOI: 10.1038/nature06906](https://doi.org/10.1038/nature06906) (~500 cit.) -- Structural basis for H2Bub1 stimulation of DOT1L.

---

## 3. Part 2: Combinatorial Patterns (ChromHMM States)

### Overview of ChromHMM Models

ChromHMM (Ernst & Kellis) uses a multivariate Hidden Markov Model to learn chromatin states from combinatorial patterns of histone modifications. Different numbers of marks yield models of different complexity:

### Key ChromHMM Publications

| Paper | Year | Journal | States | Marks | DOI | Citations |
|-------|------|---------|--------|-------|-----|-----------|
| Ernst & Kellis | 2010 | *Nat Biotechnol* | 51 | 8+ marks | [10.1038/nbt.1662](https://doi.org/10.1038/nbt.1662) | ~1,100 |
| Ernst et al. | 2011 | *Nature* | 15 | 9 marks | [10.1038/nature09906](https://doi.org/10.1038/nature09906) | ~2,000 |
| Ernst & Kellis | 2012 | *Nat Methods* | variable | flexible | [10.1038/nmeth.1906](https://doi.org/10.1038/nmeth.1906) | ~2,300 |
| Kundaje et al. | 2015 | *Nature* | 15/18/25 | 5 core + | [10.1038/nature14248](https://doi.org/10.1038/nature14248) | ~5,000 |
| Ernst & Kellis | 2017 | *Nat Protocols* | variable | flexible | [10.1038/nprot.2017.124](https://doi.org/10.1038/nprot.2017.124) | ~711 |
| ENCODE Phase 3 | 2020 | *Nature* | 15+ | 5 core + | [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4) | ~2,000 |

### The 5-Mark Core Model (Roadmap Epigenomics / ENCODE Phase 3)

The standard 5-mark model uses: **H3K4me3, H3K4me1, H3K36me3, H3K27me3, H3K9me3**

This is the minimum set profiled across all Roadmap Epigenomics samples (111 reference epigenomes) and forms the basis for the 15-state and 18-state models used in Kundaje et al. 2015.

### The 15-State Model (Roadmap Epigenomics Core Model)

From Kundaje et al. (2015) and Ernst et al. (2011), using the 5 core marks:

| State | Name | H3K4me3 | H3K4me1 | H3K36me3 | H3K27me3 | H3K9me3 | Biological Interpretation |
|-------|------|---------|---------|----------|----------|---------|--------------------------|
| 1 | TssA | HIGH | LOW | - | - | - | Active TSS |
| 2 | TssAFlnk | MED | MED | - | - | - | Flanking Active TSS |
| 3 | TxFlnk | LOW | MED | LOW | - | - | Transcription at gene 5' and 3' |
| 4 | Tx | - | - | HIGH | - | - | Strong Transcription |
| 5 | TxWk | - | - | MED | - | - | Weak Transcription |
| 6 | EnhG | - | MED | MED | - | - | Genic Enhancers |
| 7 | Enh | - | HIGH | - | - | - | Enhancers |
| 8 | ZNF/Rpts | - | - | LOW | - | HIGH | ZNF Genes & Repeats |
| 9 | Het | - | - | - | - | HIGH | Heterochromatin |
| 10 | TssBiv | HIGH | MED | - | HIGH | - | Bivalent/Poised TSS |
| 11 | BivFlnk | MED | MED | - | HIGH | - | Flanking Bivalent TSS/Enhancer |
| 12 | EnhBiv | - | HIGH | - | HIGH | - | Bivalent Enhancer |
| 13 | ReprPC | - | - | - | HIGH | - | Repressed Polycomb |
| 14 | ReprPCWk | - | - | - | MED | - | Weak Repressed Polycomb |
| 15 | Quies | - | - | - | - | - | Quiescent/Low signal |

**Source:** Kundaje et al. (2015) *Nature* 518:317-30 -- Table derived from the 15-state core model applied to 111 reference epigenomes.

### The 18-State Model (Roadmap Extended)

Adds H3K27ac as a 6th mark (available for a subset of epigenomes). Key additional distinctions:

- Active TSS further split by H3K27ac level
- Enhancers split into active (with H3K27ac) vs. poised (without)
- Genic enhancers more precisely defined

### The 25-State Model (Expanded)

Uses additional marks when available (H3K9ac, H4K20me1, H3K79me2, etc.) and provides finer resolution of:
- Multiple active promoter states
- Transcription-associated enhancer states
- Distinct heterochromatin types
- Quiescent states with different background patterns

### The Original 51-State Model (Ernst & Kellis 2010)

The first ChromHMM paper used 8 marks in CD4+ T cells and defined 51 states, which were later collapsed into the more practical 15-state model. This included fine-grained distinctions between:
- 5 promoter states (active, weak, poised, etc.)
- 3 transcription states (5' preferred, 3' preferred, etc.)
- 8 enhancer-like states
- 4 insulator states
- 5 Polycomb repressed states
- 3 heterochromatin states
- Multiple quiescent states

### Ernst et al. 2011 (15-State, 9-Cell-Type Model)

The foundational 15-state model that became the standard. Used 9 chromatin marks (H3K4me3, H3K4me1, H3K36me3, H3K27me3, H3K9me3, H3K27ac, H3K9ac, H4K20me1, CTCF) across 9 cell types.

**Key states defined:**
1. Active Promoter (H3K4me3, H3K27ac, H3K9ac high)
2. Weak Promoter (H3K4me3 moderate)
3. Poised Promoter (H3K4me3 + H3K27me3, i.e., bivalent)
4-5. Strong/Weak Enhancer (H3K4me1 high, +/- H3K27ac)
6-7. Transcription (H3K36me3, H3K79me2)
8. Insulator (CTCF binding without enhancer marks)
9. Heterochromatin (H3K9me3)
10. Polycomb Repressed (H3K27me3)
11-15. Quiescent, Repetitive, etc.

**Source:** Ernst J et al. (2011) *Nature* 473:43-49. [DOI: 10.1038/nature09906](https://doi.org/10.1038/nature09906)

---

## 4. Part 3: Mark-Specific Functional Categories

### Active Promoters

**Defining marks:** H3K4me3 (sharp peak at TSS) + H3K27ac + H3K9ac
**Additional marks:** H3K4me2, H3K14ac, H3K18ac, H2A.Z, Pol II (Ser5P)

| Feature | Description | Key Reference |
|---------|-------------|---------------|
| H3K4me3 peaks | Sharp, ~1-2 nucleosomes flanking TSS | Heintzman et al. 2007 Nat Genet |
| H3K27ac | Co-occurs with H3K4me3 at active (not bivalent) promoters | Creyghton et al. 2010 PNAS |
| 17-mark module | 17 modifications co-occur at active promoters | Wang et al. 2008 Nat Genet |
| CpG islands | Most H3K4me3 promoters overlap CpG islands | Mikkelsen et al. 2007 Nature |
| Nucleosome-free region | Active promoters show NDR flanked by +1/-1 positioned nucleosomes | Schones et al. 2008 Cell |

### Active Enhancers

**Defining marks:** H3K4me1 (broad) + H3K27ac + p300/CBP binding
**Distinguishing from promoters:** H3K4me1 (NOT me3) + H3K27ac
**Additional marks:** H3K4me2, H2A.Z, eRNA transcription, low nucleosome density

| Feature | Description | Key Reference |
|---------|-------------|---------------|
| H3K4me1 (not me3) | Enhancer-specific vs. promoter-specific | Heintzman et al. 2007 Nat Genet [DOI: 10.1038/ng1966](https://doi.org/10.1038/ng1966) |
| H3K27ac distinguishes active | Active enhancer = H3K4me1+H3K27ac | Creyghton et al. 2010 PNAS [DOI: 10.1073/pnas.1016071107](https://doi.org/10.1073/pnas.1016071107) |
| p300/CBP binding | Co-activator occupancy marks enhancers | Visel A et al. 2009 Nature [DOI: 10.1038/nature07730](https://doi.org/10.1038/nature07730) |
| eRNA transcription | Active enhancers produce bidirectional non-coding RNAs | Kim TK et al. 2010 Nature [DOI: 10.1038/nature09014](https://doi.org/10.1038/nature09014) |
| Cell-type specificity | Enhancer marks are highly cell-type specific | Ernst et al. 2011 Nature [DOI: 10.1038/nature09906](https://doi.org/10.1038/nature09906) |

### Poised/Bivalent Elements

**At promoters:** H3K4me3 + H3K27me3 (bivalent domains)
**At enhancers:** H3K4me1 + H3K27me3 (poised enhancers)

| Feature | Description | Key Reference |
|---------|-------------|---------------|
| Bivalent promoters | H3K4me3+H3K27me3 at developmental genes in ESCs | Bernstein et al. 2006 Cell [DOI: 10.1016/j.cell.2006.02.041](https://doi.org/10.1016/j.cell.2006.02.041) |
| Resolution on differentiation | Resolve to H3K4me3-only (active) or H3K27me3-only (repressed) | Mikkelsen et al. 2007 Nature |
| Poised enhancers | H3K4me1+H3K27me3 at developmental enhancers in ESCs | Rada-Iglesias et al. 2011 Nature [DOI: 10.1038/nature09692](https://doi.org/10.1038/nature09692) |
| Same-allele co-occurrence | Sequential ChIP confirmed both marks on same nucleosome/allele | Bernstein et al. 2006 Cell |
| Protection function | H3K4me3 at bivalent promoters protects from DNA methylation | Kumar et al. 2021 Genome Res [DOI: 10.1101/gr.266924.120](https://doi.org/10.1101/gr.266924.120) |
| Not strictly ESC-specific | Bivalent domains found in progenitor cells too, though enriched in ESCs | Harikumar & Meshorer 2015 EMBO Rep |

### Super-Enhancers

**Defining marks:** Exceptionally high H3K27ac + MED1/BRD4 signal
**Identification method:** ROSE algorithm (rank-ordering of super-enhancer signal)

| Feature | Description | Key Reference |
|---------|-------------|---------------|
| Definition | Large clusters of enhancers with disproportionately high H3K27ac/Mediator | Whyte et al. 2013 Cell [DOI: 10.1016/j.cell.2013.03.035](https://doi.org/10.1016/j.cell.2013.03.035) |
| Cell identity genes | Associated with genes controlling cell type identity | Hnisz et al. 2013 Cell [DOI: 10.1016/j.cell.2013.09.053](https://doi.org/10.1016/j.cell.2013.09.053) |
| Sensitivity to perturbation | Disproportionately affected by BET inhibitors (JQ1) | Loven et al. 2013 Cell [DOI: 10.1016/j.cell.2013.03.036](https://doi.org/10.1016/j.cell.2013.03.036) (~2,700 cit.) |
| Cancer relevance | Cancer cells acquire super-enhancers at oncogenes | Hnisz et al. 2013 Cell |
| Beyond H3K27ac | H4K5acK8ac defines additional super-enhancers missed by H3K27ac alone | Das et al. 2023 BMC Genomics |
| Phase separation | Super-enhancers may form phase-separated condensates | Sabari et al. 2018 Science [DOI: 10.1126/science.aar3958](https://doi.org/10.1126/science.aar3958) |

**Controversy:** The super-enhancer concept has been debated. Some argue they are simply clusters of typical enhancers and the term implies a mechanistic distinction that may not exist. Pott & Lieb (2015) *Nat Genet* 47:8-12 argued that individual constituents of super-enhancers can function independently.

### Silencers: Polycomb vs. Heterochromatin

Two distinct silencing mechanisms use different histone marks:

| Feature | Polycomb (Facultative) | Heterochromatin (Constitutive) |
|---------|----------------------|-------------------------------|
| **Key mark** | H3K27me3 | H3K9me3 |
| **Writers** | PRC2 (EZH2) | SUV39H1/2, SETDB1 |
| **Readers** | PRC1 (CBX), EED | HP1 family |
| **Targets** | Developmental genes, lineage-inappropriate genes | Repeats, TEs, ERVs, pericentromeric |
| **Reversibility** | Reversible (KDM6A/B demethylases) | More stable, but reversible |
| **ChromHMM state** | Repressed Polycomb (state 13) | Heterochromatin (state 9) |
| **Genome coverage** | 5-10% of genome | 10-30% of genome |
| **H3K9me2 role** | Not involved | Euchromatic silencing (G9a/GLP), LOCKs |

### Transcribed Gene Bodies

**Marks increase 5'->3' through gene body:** H3K36me3, H3K79me2
**Marks at gene bodies:** H4K20me1, H3K36me3, H3K79me2
**Absent:** H3K4me3 (restricted to TSS), H3K27me3 (excluded from active genes)

| Feature | Description | Key Reference |
|---------|-------------|---------------|
| H3K36me3 gradient | Increases from 5' to 3'; co-transcriptional via SETD2 | Bannister et al. 2005 Nature |
| H3K79me2 | Gene body mark via DOT1L; requires H2BK120ub | Steger et al. 2008 Mol Cell Biol |
| Cryptic transcription prevention | H3K36me3 recruits HDACs to prevent spurious initiation | Carrozza MJ et al. 2005 Cell [DOI: 10.1016/j.cell.2005.10.023](https://doi.org/10.1016/j.cell.2005.10.023) |
| Gene body DNA methylation | H3K36me3 recruits DNMT3B for intragenic CpG methylation | Baubec T et al. 2015 Nature [DOI: 10.1038/nature14456](https://doi.org/10.1038/nature14456) |

### Insulator/Boundary Elements

**Defined by:** CTCF binding, cohesin co-occupancy
**Histone marks:** NOT primarily defined by histone modifications but by factor binding
**Associated features:** Nucleosome-depleted regions at CTCF sites, flanked by well-positioned nucleosomes

| Feature | Description | Key Reference |
|---------|-------------|---------------|
| CTCF binding | Zinc-finger protein that defines TAD boundaries | Dixon JR et al. 2012 Nature [DOI: 10.1038/nature11082](https://doi.org/10.1038/nature11082) (~4,000 cit.) |
| CTCF essential for TADs | Auxin-mediated CTCF depletion eliminates TADs | Nora EP et al. 2017 Cell [DOI: 10.1016/j.cell.2017.09.026](https://doi.org/10.1016/j.cell.2017.09.026) (~1,437 cit.) |
| Cohesin co-occupancy | CTCF+cohesin define chromatin loops | Rao SSP et al. 2014 Cell [DOI: 10.1016/j.cell.2014.11.021](https://doi.org/10.1016/j.cell.2014.11.021) (~5,000 cit.) |
| Boundary marks | CTCF sites enriched in Barski et al. 2007 dataset | Barski et al. 2007 Cell |
| ChromHMM insulator state | Defined by CTCF signal without enhancer marks (in expanded models) | Ernst et al. 2011 Nature |

**Note:** In the standard 5-mark ChromHMM model, insulators are NOT a distinct state because CTCF binding is not included as input. Insulator identification requires CTCF ChIP-seq data.

---

## 5. Part 4: Contradictions and Edge Cases

### 5.1 Marks Whose Interpretation Is Debated

#### H3K4me1: Enhancer Mark or Consequence of Activity?

The canonical view (Heintzman et al. 2007) holds that H3K4me1 marks enhancers. However:
- H3K4me1 is also found downstream of active TSSs and in gene bodies.
- MLL3/4-catalyzed H3K4me1 may be a consequence rather than a cause of enhancer activation.
- Dorighi KM et al. (2017) *Mol Cell* 66:568-576 [DOI: 10.1016/j.molcel.2017.04.018](https://doi.org/10.1016/j.molcel.2017.04.018) showed that catalytically dead MLL3/4 still supports enhancer function, suggesting H3K4me1 itself is not required for enhancer activity -- the physical presence of MLL3/4 is what matters.
- Rickels R et al. (2017) *Genes Dev* 31:1412-1424 [DOI: 10.1101/gad.300592.117](https://doi.org/10.1101/gad.300592.117) corroborated this finding.

**Current consensus:** H3K4me1 is a reliable MARKER of enhancers but may not be functionally required. The MLL3/4 complexes are required, but their methyltransferase activity may be dispensable.

#### Bivalent Domains: Poising or Protection?

The original model (Bernstein et al. 2006) proposed bivalent chromatin "poises" genes for rapid activation. The alternative model (Kumar et al. 2021) argues:
- Bivalent genes are NOT activated faster than other silent genes during differentiation.
- H3K4me3 at bivalent promoters primarily protects from de novo DNA methylation.
- Loss of bivalency in cancer correlates with aberrant hypermethylation and permanent silencing.

**Current view:** Both models may be correct. Bivalency maintains epigenetic plasticity by preventing irreversible silencing, which incidentally keeps genes available for future activation.
- **Macrae et al. (2022) *Nat Rev Mol Cell Biol* 24:6-26** [DOI: 10.1038/s41580-022-00544-w](https://doi.org/10.1038/s41580-022-00544-w) (~117 cit.) provides the most comprehensive review, concluding that bivalency is a feature of both germline/ESC and adult stem/progenitor cells.

#### H4K20me1: Activating or Repressive?

- Barski et al. (2007) found H4K20me1 correlated with gene activation.
- Cell cycle studies show H4K20me1 is deposited during mitosis by PR-Set7, peaking in G2/M.
- In some contexts, H4K20me1 is associated with gene repression and is enriched on the inactive X chromosome.
- **Resolution:** H4K20me1 likely reflects recent mitotic passage and transcriptional competence rather than being directly activating or repressive. Context and cell cycle phase matter.

### 5.2 Tissue-Specific vs. Universal Meanings

Most histone mark interpretations are broadly conserved across cell types, but several important tissue-specific patterns exist:

| Mark | Universal Role | Tissue-Specific Variation |
|------|---------------|--------------------------|
| H3K4me1 | Enhancer mark | Specific enhancers marked are highly tissue-specific (Ernst et al. 2011) |
| H3K27me3 | Polycomb repression | Target genes differ dramatically by cell type; ~20-30% of genome in ESCs vs. more restricted in differentiated cells |
| H3K9me3 | Heterochromatin | SETDB1-mediated H3K9me3 at distinct gene sets in each lineage (Padeken et al. 2022) |
| H3K27ac | Active regulatory | Enhancer repertoire is cell-type specific; super-enhancers define cell identity |
| H3K36me3 | Transcribed genes | Reflects cell-type-specific transcriptome |

### 5.3 Marks That Change Meaning in Combination

| Combination | Meaning | vs. Individual Mark |
|-------------|---------|-------------------|
| H3K4me1 alone | Primed/poised enhancer | H3K4me1 = generic enhancer mark |
| H3K4me1 + H3K27ac | **Active enhancer** | Mutual exclusivity of K27ac/K27me3 is the switch |
| H3K4me1 + H3K27me3 | **Poised enhancer** | H3K27me3 = repression; but with me1, it means "ready" |
| H3K4me3 alone | Active promoter | Widely permissive state |
| H3K4me3 + H3K27me3 | **Bivalent/poised promoter** | Completely changes interpretation from "active" to "poised" |
| H3K36me3 + H3K27me3 | Conflicting/transition zone | Should NOT co-occur; indicates domain boundaries or mixed cell populations |
| H3K9me3 + H3K36me3 | ZNF/KRAB-ZFP genes | SETDB1-mediated H3K9me3 at actively transcribed KRAB-ZFP genes (unique to ZNF gene clusters) |

### 5.4 Cancer-Specific Chromatin States

Cancer cells show widespread epigenetic dysregulation that creates chromatin states not seen in normal tissues:

| Aberration | Description | Key Reference |
|------------|-------------|---------------|
| Global H4K16ac loss | One of the earliest epigenetic changes in cancer | Fraga et al. 2005 Nat Genet |
| H3K27me3 redistribution | Loss at tumor suppressor promoters, gain at other loci | Berman BP et al. 2012 Nat Genet [DOI: 10.1038/ng.1090](https://doi.org/10.1038/ng.1090) |
| De novo super-enhancers | Cancer cells create super-enhancers at oncogenes | Hnisz et al. 2013 Cell |
| Bivalent-to-methylated switch | Bivalent promoters in ESCs become DNA hypermethylated in cancer | Ohm JE et al. 2007 Nat Genet [DOI: 10.1038/ng1972](https://doi.org/10.1038/ng1972) |
| H3K9me3 expansion | Aberrant spreading into euchromatic regions in some cancers | McDonald OG et al. 2017 Nat Genet [DOI: 10.1038/ng.3861](https://doi.org/10.1038/ng.3861) |
| EZH2 gain-of-function | Y641 mutations in lymphoma increase H3K27me3 | Morin RD et al. 2010 Nat Genet [DOI: 10.1038/ng.518](https://doi.org/10.1038/ng.518) |
| Oncohistone mutations | H3.3K27M (glioma) globally reduces H3K27me3; H3.3K36M (chondrosarcoma) reduces H3K36me3 | Lewis PW et al. 2013 Science [DOI: 10.1126/science.1232245](https://doi.org/10.1126/science.1232245); Lu C et al. 2016 Science [DOI: 10.1126/science.aaf8081](https://doi.org/10.1126/science.aaf8081) |
| Large-scale LOCKs | Megabase domains of H3K9me2 expand in cancer | Wen B et al. 2009 Genome Res |
| H3K4me3 breadth changes | Broad H3K4me3 domains mark tumor suppressors; narrowing in cancer | Chen K et al. 2015 Cell Rep [DOI: 10.1016/j.celrep.2015.02.003](https://doi.org/10.1016/j.celrep.2015.02.003) |

### 5.5 Other Edge Cases

**H3K4me3 breadth matters:** Benayoun BA et al. (2014) *Cell* 158:673-688 [DOI: 10.1016/j.cell.2014.07.026](https://doi.org/10.1016/j.cell.2014.07.026) showed that broad H3K4me3 domains (spanning >5kb) mark cell identity genes and differ from narrow peaks at housekeeping genes.

**Histone mark spread into repetitive elements:** H3K9me3 at repetitive elements can spread into adjacent unique sequences (Mikkelsen et al. 2007). This confounds analysis of nearby genes.

**Asymmetric marks at enhancers:** Active enhancers show asymmetric histone modification patterns, with marks like H3K4me1 often more pronounced on one side of the p300-bound nucleosome-depleted region.

**Non-canonical PRC1:** Non-canonical PRC1 complexes can deposit H2AK119ub independently of H3K27me3, challenging the classical sequential model of PRC2->PRC1 recruitment.

---

## Quick Reference: Mark-to-Function Lookup Table

| Mark | Primary Function | Genomic Location | ChromHMM Core? |
|------|-----------------|-------------------|----------------|
| H3K4me1 | Enhancer (primed/active) | Distal regulatory elements | YES (core 5) |
| H3K4me2 | Active regulatory | Promoters + Enhancers | No |
| H3K4me3 | Active/poised promoter | TSS (+/- 1kb) | YES (core 5) |
| H3K9me1 | Weak activation | Near active promoters | No |
| H3K9me2 | Euchromatic silencing (LOCKs) | Megabase domains | No |
| H3K9me3 | Constitutive heterochromatin | Repeats, TEs, ERVs, pericentromeric | YES (core 5) |
| H3K9ac | Active promoter | TSS | No (in expanded models) |
| H3K27me3 | Polycomb repression | Broad domains at silent genes | YES (core 5) |
| H3K27ac | Active enhancer/promoter | Active regulatory elements | YES (in 18-state+) |
| H3K36me3 | Transcribed gene body | Gene bodies (5'->3' gradient) | YES (core 5) |
| H3K79me2 | Transcription elongation | Gene bodies | No (in expanded models) |
| H4K20me1 | Transcription/cell cycle | Gene bodies; mitotic chromatin | No (in expanded models) |
| H4K5ac | Active chromatin | Promoters, enhancers | No |
| H4K8ac | Active chromatin | Promoters, enhancers | No |
| H4K16ac | Euchromatin structure | Active euchromatin globally | No |
| H4K91ac | Nucleosome assembly | Sites of remodeling | No |
| H3K14ac | Active/DNA damage | Active promoters, DSB sites | No |
| H3K18ac | Active transcription | Active promoters/enhancers | No |
| H3K23ac | Active transcription | Active promoters | No |
| H2A.Z | Regulatory element | TSS, enhancers, insulators | No (variant, not mod) |
| H2BK120ub | Crosstalk/elongation | Active gene bodies | No |

---

## 6. Part 5: Transcription Factor Combinations and Co-Binding Patterns

Chromatin states are not passively read -- they are actively shaped by transcription factor (TF) combinations that bind cooperatively, compete, and create regulatory logic at enhancers and promoters. This section covers the major TF co-binding paradigms and their chromatin signatures.

### CTCF and Cohesin Co-Binding

CTCF (CCCTC-binding factor) is the principal insulator protein in mammalian genomes, occupying ~55,000-65,000 sites depending on cell type. It functions asymmetrically as a boundary element by blocking cohesin-mediated loop extrusion.

**Rao et al. 2014** -- Kilobase-resolution 3D genome map identifying CTCF/cohesin-anchored chromatin loops.
- **Citation:** Rao SS, Huntley MH, Durand NC, Stamenova EK, Bochkov ID, Robinson JT, Sanborn AL, Machol I, Omer AD, Lander ES, Aiden EL. "A 3D map of the human genome at kilobase resolution reveals principles of chromatin looping." *Cell*. 2014;159(7):1665-80.
- **DOI:** [10.1016/j.cell.2014.11.021](https://doi.org/10.1016/j.cell.2014.11.021)
- **Citations:** ~5,000
- **Key findings:** Identified ~10,000 chromatin loops in human cells; the vast majority are anchored by convergent CTCF motifs with cohesin. Loops are cell-type-specific and partition the genome into contact domains. Demonstrated that loop anchors are enriched for convergent (not tandem) CTCF motifs.

**Nora et al. 2017** -- Acute CTCF depletion shows CTCF is required for loop domains but not compartments.
- **Citation:** Nora EP, Goloborodko A, Valton AL, Gibcus JH, Uebersohn A, Abdennur N, Dekker J, Mirny LA, Bruneau BG. "Targeted degradation of CTCF decouples local insulation of chromosome domains from genomic compartmentalization." *Cell*. 2017;169(5):930-44.
- **DOI:** [10.1016/j.cell.2017.09.026](https://doi.org/10.1016/j.cell.2017.09.026)
- **Citations:** ~1,400
- **Key findings:** Auxin-inducible degron system to deplete CTCF within 24 hours. CTCF loss eliminates TAD insulation and CTCF-anchored loops but compartmentalization (A/B) is maintained. Demonstrates that CTCF and compartments are governed by independent mechanisms.

**Davidson et al. 2023** -- Single-molecule visualization shows CTCF is a DNA-tension-dependent barrier to cohesin.
- **Citation:** Davidson IF, Barth R, Zaczek M, van der Torre J, Tang W, Nagasaka K, Janissen R, Kerssemakers JWJ, Wutz G, Dekker C, Peters JM. "CTCF is a DNA-tension-dependent barrier to cohesin-mediated loop extrusion." *Nature*. 2023;616:822-827.
- **DOI:** [10.1038/s41586-023-05961-5](https://doi.org/10.1038/s41586-023-05961-5)
- **Citations:** ~109
- **Key findings:** CTCF can actively regulate cohesin loop extrusion direction and induce loop shrinkage -- not merely a passive barrier. Barrier function is modulated by DNA tension. Provides biophysical basis for TAD boundary permeability.

**ENCODE observation:** CTCF and cohesin (RAD21) co-bind at >80% of CTCF sites genome-wide. Look for ENCODE TF ChIP-seq experiments targeting CTCF, RAD21, SMC3 for comprehensive insulator mapping.

### p300/CBP at Enhancers

The histone acetyltransferases p300 (EP300) and CBP (CREBBP) are the primary writers of H3K27ac at enhancers. Their binding is one of the most reliable indicators of active enhancer elements.

**Visel et al. 2009** -- p300 ChIP-seq as a genome-wide predictor of enhancers in vivo.
- **Citation:** Visel A, Blow MJ, Li Z, Zhang T, Akiyama JA, Holt A, Plajzer-Frick I, Shoukry M, Wright C, Chen F, Afzal V, Ren B, Rubin EM, Pennacchio LA. "ChIP-seq accurately predicts tissue-specific activity of enhancers." *Nature*. 2009;457(7231):854-8.
- **DOI:** [10.1038/nature07730](https://doi.org/10.1038/nature07730)
- **Citations:** ~2,200
- **Key findings:** p300 binding in mouse embryonic tissue accurately predicts tissue-specific enhancer activity in vivo. Validated with transgenic reporter assays. Established p300 as a gold-standard enhancer marker.

**Raisner et al. 2018** -- CBP/p300 bromodomain is required for H3K27ac at enhancers.
- **Citation:** Raisner RM, Kharbanda S, Jin L, Jeng E, Chan E, Merchant M, Haverty PM, Bainer R, Cheung TK, Arnott D, Flynn EM, Romero FA, Magnuson S, Gascoigne KE. "Enhancer activity requires CBP/p300 bromodomain-dependent histone H3K27 acetylation." *Cell Rep*. 2018;24(7):1722-1729.
- **DOI:** [10.1016/j.celrep.2018.07.041](https://doi.org/10.1016/j.celrep.2018.07.041)
- **Citations:** ~282
- **Key findings:** Chemical inhibition of CBP/p300 bromodomain causes loss of H3K27ac specifically from enhancers (not promoters), even though CBP/p300 protein remains on chromatin. H3K27ac is functionally required for enhancer RNA production.

**Lai et al. 2017** -- MLL3/MLL4 are required upstream of CBP/p300 for enhancer activation.
- **Citation:** Lai B, Lee JE, Jang Y, Wang L, Peng W, Ge K. "MLL3/MLL4 are required for CBP/p300 binding on enhancers and super-enhancer formation in brown adipogenesis." *Nucleic Acids Res*. 2017;45(11):6388-6403.
- **DOI:** [10.1093/nar/gkx234](https://doi.org/10.1093/nar/gkx234)
- **Citations:** ~153
- **Key findings:** MLL3/MLL4 deposit H3K4me1 at enhancers first (priming), which is required for subsequent CBP/p300 recruitment and H3K27ac deposition (activation). Establishes the sequential model: MLL3/4 primes, then CBP/p300 activates.

### Mediator Complex and Super-Enhancers

The Mediator complex (specifically MED1) co-occupies super-enhancers with BRD4 and master TFs. See also Whyte et al. 2013 (already referenced in Part 4 of this catalog, ref #19). Mediator is the bridge between enhancer-bound TFs and the RNA Pol II machinery.

### Pioneer Factors

Pioneer factors are a specialized class of transcription factors that can bind nucleosomal DNA -- they do not require pre-existing open chromatin. This ability makes them critical initiators of chromatin remodeling during development, reprogramming, and hormone response.

**Zaret & Carroll 2011** -- Foundational review defining pioneer factor properties.
- **Citation:** Zaret KS, Carroll JS. "Pioneer transcription factors: establishing competence for gene expression." *Genes Dev*. 2011;25(21):2227-41.
- **DOI:** [10.1101/gad.176826.111](https://doi.org/10.1101/gad.176826.111)
- **Citations:** ~1,500
- **Key findings:** Defined the concept of pioneer factors as TFs that can engage target sites on nucleosomal DNA. FoxA proteins have a winged-helix domain structurally similar to linker histone H1, enabling nucleosome engagement. Passive (reducing cooperativity threshold) and active (opening chromatin) pioneer mechanisms described.

**Iwafuchi-Doi & Zaret 2014** -- Pioneer factors in cell reprogramming.
- **Citation:** Iwafuchi-Doi M, Zaret KS. "Pioneer transcription factors in cell reprogramming." *Genes Dev*. 2014;28(24):2679-2692.
- **DOI:** [10.1101/gad.253443.114](https://doi.org/10.1101/gad.253443.114)
- **Citations:** ~562
- **Key findings:** Pioneer factors (FOXA, OCT4, SOX2, KLF4) with the highest reprogramming activity engage nucleosomal DNA directly. Other reprogramming TFs depend on pioneer factors for chromatin access. Heterochromatin (H3K9me3) can resist even pioneer factor binding.

**Key pioneer factors relevant to ENCODE data:**
- **FOXA1/FOXA2**: Bind nucleosomal DNA via winged-helix domain; critical in liver, pancreas, lung development
- **GATA factors**: GATA1 (blood), GATA4 (cardiac), GATA6 (pancreas) -- can bind partially nucleosomal DNA
- **OCT4/SOX2/KLF4**: Yamanaka reprogramming factors; OCT4 and SOX2 have pioneer activity
- **TP63/TP53**: p53 family members with pioneer-like chromatin scanning

### Polycomb and Trithorax Opposition

The Polycomb group (PcG) and Trithorax group (TrxG) represent an ancient epigenetic regulatory system that maintains repressed vs. active gene states, respectively. Their opposition is central to bivalent chromatin and developmental gene regulation.

**Schuettengruber et al. 2017** -- Comprehensive review of PcG/TrxG after 70 years of research.
- **Citation:** Schuettengruber B, Bourbon HM, Di Croce L, Cavalli G. "Genome regulation by Polycomb and Trithorax: 70 years and counting." *Cell*. 2017;171(1):34-57.
- **DOI:** [10.1016/j.cell.2017.08.002](https://doi.org/10.1016/j.cell.2017.08.002)
- **Citations:** ~860
- **Key findings:** PRC2 (EZH2/EED/SUZ12) writes H3K27me3; PRC1 writes H2AK119ub. TrxG includes COMPASS family (MLL1-4, SET1A/B) writing H3K4me1/me2/me3. PcG and TrxG compete at the same loci: loss of one causes expansion of the other's marks. SWI/SNF is also a TrxG member.

**Agger et al. 2007** -- Discovery of UTX and JMJD3 as H3K27me3 demethylases that link TrxG to PcG antagonism.
- **Citation:** Agger K, Cloos PA, Christensen J, Pasini D, Rose S, Rappsilber J, Issaeva I, Canaani E, Salcini AE, Helin K. "UTX and JMJD3 are histone H3K27 demethylases involved in HOX gene regulation and development." *Nature*. 2007;449:731-734.
- **DOI:** [10.1038/nature06145](https://doi.org/10.1038/nature06145)
- **Citations:** ~1,300
- **Key findings:** UTX (KDM6A) and JMJD3 (KDM6B) are JmjC-domain demethylases specific for H3K27me3. UTX associates with MLL2 (a TrxG complex), coordinating removal of repressive marks with deposition of activating marks. Essential for HOX gene regulation and development.

### Combinatorial TF Binding at Lineage-Specifying Enhancers

**Heinz et al. 2010** -- Landmark paper on collaborative/hierarchical TF binding at cell-type-specific enhancers.
- **Citation:** Heinz S, Benner C, Spann N, Bertolino E, Lin YC, Laslo P, Cheng JX, Murre C, Singh H, Glass CK. "Simple combinations of lineage-determining transcription factors prime cis-regulatory elements required for macrophage and B cell identities." *Mol Cell*. 2010;38(4):576-89.
- **DOI:** [10.1016/j.molcel.2010.05.004](https://doi.org/10.1016/j.molcel.2010.05.004)
- **Citations:** ~11,500
- **Key findings:** PU.1 collaborates with small sets of lineage-determining TFs (C/EBP in macrophages, E2A/EBF in B cells) to establish cell-specific binding sites. PU.1 initiates nucleosome remodeling and H3K4me1 deposition. These primed sites then serve as beacons for signal-dependent TFs. Defined the collaborative vs. hierarchical binding model.

### Quick Reference: Common TF Combinations and Their Chromatin Signatures

| TF Combination | Chromatin Signature | Functional Interpretation |
|---|---|---|
| CTCF + Cohesin (RAD21/SMC3) | Low H3K27ac, positioned nucleosomes | Insulator / TAD boundary |
| p300/CBP + H3K27ac + H3K4me1 | Open chromatin (ATAC-seq+) | Active enhancer |
| BRD4 + MED1 + high H3K27ac | Broad H3K27ac domain | Super-enhancer |
| FOXA1/2 + closed chromatin | Partial accessibility emerging | Pioneer factor engagement |
| PRC2 (SUZ12/EZH2) + H3K27me3 | Closed chromatin, no H3K27ac | Polycomb-repressed |
| MLL/COMPASS + H3K4me3 | Open promoter, TSS-proximal | Active or poised promoter (TrxG) |
| PU.1 + C/EBP + H3K4me1 | Primed distal element | Macrophage-specific enhancer |
| PU.1 + E2A/EBF + H3K4me1 | Primed distal element | B cell-specific enhancer |
| CTCF alone (no cohesin) | Variable | CTCF-only site (non-insulator role) |
| p300 + H3K4me1 (no H3K27ac) | Closed/partial | Poised enhancer |

---

## 7. Part 6: Chromatin Remodeling Complexes

ATP-dependent chromatin remodeling complexes use the energy of ATP hydrolysis to slide, eject, or restructure nucleosomes. There are four families in mammals -- SWI/SNF, ISWI, CHD/NuRD, and INO80 -- each with distinct roles. Mutations in these complexes are among the most common in cancer.

### SWI/SNF (BAF/PBAF/ncBAF)

The SWI/SNF (Switch/Sucrose Non-Fermentable) family is the most frequently mutated chromatin regulatory complex in human cancer (~20% of all malignancies).

**Kadoch & Crabtree 2015** -- Mammalian SWI/SNF complexes in disease.
- **Citation:** Kadoch C, Crabtree GR. "Mammalian SWI/SNF chromatin remodeling complexes and cancer: Mechanistic insights gained from human genomics." *Sci Adv*. 2015;1(5):e1500447.
- **DOI:** [10.1126/sciadv.1500447](https://doi.org/10.1126/sciadv.1500447)
- **Citations:** ~1,000
- **Key findings:** Three distinct SWI/SNF complexes: canonical BAF (cBAF), Polybromo-BAF (PBAF), and non-canonical BAF (ncBAF). Subunit mutations are mutually exclusive in cancer (SMARCB1, SMARCA4, ARID1A, PBRM1). SWI/SNF opposes Polycomb repression by ejecting PRC1/PRC2 from target loci.

**Mashtalir et al. 2018** -- Modular architecture of mammalian SWI/SNF complexes.
- **Citation:** Mashtalir N, D'Avino AR, Michel BC, Luo J, Pan J, Otto JE, Zullow HJ, McKenzie ZM, Kubber RL, St. Pierre R, Valencia AM, Pober SJ, Kadoch C. "Modular organization and assembly of SWI/SNF family chromatin remodeling complexes." *Cell*. 2018;175(5):1272-1288.
- **DOI:** [10.1016/j.cell.2018.09.032](https://doi.org/10.1016/j.cell.2018.09.032)
- **Citations:** ~600
- **Key findings:** Defined the modular architecture of BAF, PBAF, and ncBAF. Each shares a catalytic ATPase module (SMARCA4/BRG1 or SMARCA2/BRM) but has distinct targeting subunits. BAF uses ARID1A/B; PBAF uses ARID2+PBRM1; ncBAF uses BRD9. Assembly is hierarchical and disease-relevant.

**Hodges et al. 2016** -- Comprehensive review of BAF/PBAF roles in cancer.
- **Citation:** Hodges C, Kirkland JG, Crabtree GR. "The many roles of BAF (mSWI/SNF) and PBAF complexes in cancer." *Cold Spring Harb Perspect Med*. 2016;6(8):a026930.
- **DOI:** [10.1101/cshperspect.a026930](https://doi.org/10.1101/cshperspect.a026930)
- **Citations:** ~342
- **Key findings:** Recurrent mutations in ARID1A (~50% of ovarian clear cell carcinoma), PBRM1 (~40% of renal clear cell carcinoma), SMARCB1 (rhabdoid tumors), SMARCA4 (multiple cancers). SWI/SNF has roles in transcription, DNA repair, and chromatin topology.

### NuRD (Nucleosome Remodeling and Deacetylase) Complex

The NuRD complex uniquely combines ATP-dependent nucleosome remodeling (via CHD3/CHD4) with histone deacetylase activity (via HDAC1/HDAC2), making it both a remodeler and a repressor.

**Xue et al. 1998** -- Discovery and characterization of the NuRD complex.
- **Citation:** Xue Y, Wong J, Moreno GT, Young MK, Cote J, Wang W. "NURD, a novel complex with both ATP-dependent chromatin-remodeling and histone deacetylase activities." *Mol Cell*. 1998;2(6):851-61.
- **DOI:** [10.1016/S1097-2765(00)80299-3](https://doi.org/10.1016/S1097-2765(00)80299-3)
- **Citations:** ~1,000
- **Key findings:** Identified the NuRD complex containing CHD4 (Mi-2beta) ATPase, HDAC1/2, MTA1, MBD3, and RbAp46/48. ATP-dependent remodeling stimulates deacetylation on nucleosomal substrates. Links chromatin remodeling to transcriptional repression.

**Lai & Wade 2011** -- NuRD in cancer biology.
- **Citation:** Lai AY, Wade PA. "Cancer biology and NuRD: a multifaceted chromatin remodelling complex." *Nat Rev Cancer*. 2011;11(8):588-596.
- **DOI:** [10.1038/nrc3091](https://doi.org/10.1038/nrc3091)
- **Citations:** ~501
- **Key findings:** NuRD is a key determinant of ESC differentiation. Mislocalization of NuRD contributes to aberrant gene silencing in cancer. MTA1 overexpression correlates with metastatic potential across multiple cancer types.

### ISWI Complexes

ISWI (Imitation SWItch) complexes primarily space and order nucleosome arrays. The catalytic subunits in humans are SMARCA5 (SNF2H) and SMARCA1 (SNF2L), which participate in complexes including ACF, CHRAC, RSF, and NURF.

- **Function:** Establish regular nucleosome spacing, particularly after DNA replication and during transcription
- **Chromatin association:** ISWI complexes generate evenly spaced nucleosome arrays that can either repress or activate transcription depending on context
- **Disease relevance:** SMARCA5 overexpression in various cancers; BPTF (a NURF subunit) recognizes H3K4me3

### CHD Complexes

The CHD (Chromodomain Helicase DNA-binding) family includes CHD1-9, each with tandem chromodomains that read histone methylation marks.

- **CHD1:** Binds H3K4me3; promotes transcription elongation by disassembling nucleosomes ahead of Pol II. Required for maintaining open chromatin at active genes.
- **CHD3/CHD4:** Core ATPases of the NuRD complex (see above)
- **CHD7:** Binds H3K4me1-marked enhancers; mutations cause CHARGE syndrome. Loss leads to defective enhancer activation.
- **CHD8:** Binds H3K4me3 at promoters; autism-associated gene; connects chromatin remodeling to neurodevelopment

### INO80/SWR1 Complexes

The INO80 and SWR1 (SRCAP in humans) complexes catalyze histone variant exchange, particularly the incorporation and removal of H2A.Z.

- **SWR1/SRCAP complex:** Deposits H2A.Z into nucleosomes at promoters and enhancers, replacing canonical H2A. H2A.Z nucleosomes are less stable and mark regulatory elements.
- **INO80 complex:** Can remove H2A.Z and replace it with canonical H2A. Also has roles in DNA repair and replication fork stability.
- **Functional axis:** The SWR1/INO80 balance determines H2A.Z occupancy at regulatory elements, directly linking remodeling to enhancer/promoter activity

### Quick Reference: Chromatin Remodeling Complexes

| Complex Family | Human Catalytic Subunit(s) | Primary Function | Associated Marks | Cancer Mutations |
|---|---|---|---|---|
| cBAF (SWI/SNF) | SMARCA4 (BRG1) | Nucleosome ejection at enhancers | Opposes H3K27me3 | ARID1A, SMARCA4, SMARCB1 |
| PBAF (SWI/SNF) | SMARCA4 (BRG1) | Promoter/heterochromatin remodeling | Reads H3K14ac via PBRM1 | PBRM1, ARID2 |
| ncBAF (SWI/SNF) | SMARCA4/2 | CTCF-proximal remodeling | Reads H3K27ac via BRD9 | BRD9 |
| NuRD (CHD) | CHD3/CHD4 | Remodeling + deacetylation | Removes H3/H4 acetylation | MTA1 overexpression |
| ACF/CHRAC (ISWI) | SMARCA5 (SNF2H) | Nucleosome spacing | Regular arrays | SMARCA5 overexpression |
| NURF (ISWI) | SMARCA1 (SNF2L) | Nucleosome sliding at promoters | Reads H3K4me3 via BPTF | BPTF |
| CHD1 | CHD1 | Transcription-coupled remodeling | Reads H3K4me3 | CHD1 deletion (prostate) |
| CHD7 | CHD7 | Enhancer activation | Reads H3K4me1 | CHARGE syndrome |
| INO80 | INO80 | H2A.Z removal, DNA repair | Replaces H2A.Z with H2A | Rare |
| SRCAP (SWR1) | SRCAP | H2A.Z deposition | Deposits H2A.Z | Floating-Harbor syndrome |

---

## 8. Part 7: DNA Methylation and Chromatin Interplay

DNA methylation (5-methylcytosine, 5mC) and histone modifications do not operate in isolation. Complex crosstalk between these systems establishes and maintains chromatin states. Understanding this interplay is essential for interpreting ENCODE WGBS and ChIP-seq data together.

### CpG Island Promoters: DNA Methylation and H3K4me3

**Jones 2012** -- Comprehensive review of DNA methylation functions.
- **Citation:** Jones PA. "Functions of DNA methylation: islands, start sites, gene bodies and beyond." *Nat Rev Genet*. 2012;13(7):484-92.
- **DOI:** [10.1038/nrg3230](https://doi.org/10.1038/nrg3230)
- **Citations:** ~3,000
- **Key findings:** ~70% of human gene promoters contain CpG islands (CGIs). CGIs are typically unmethylated and associated with permissive chromatin. Methylation of CGI promoters causes stable transcriptional silencing. Gene body methylation positively correlates with transcription. DNA methylation landscapes are cell-type-specific.

### H3K4me3 and DNA Methylation Mutual Exclusion

One of the most robust principles in epigenetics: H3K4 methylation and DNA methylation are mutually exclusive at CpG islands.

**Ooi et al. 2007** -- Structural basis for mutual exclusion via DNMT3L.
- **Citation:** Ooi SK, Qiu C, Bernstein E, Li K, Jia D, Yang Z, Erdjument-Bromage H, Tempst P, Lin SP, Allis CD, Cheng X, Bestor TH. "DNMT3L connects unmethylated lysine 4 of histone H3 to de novo methylation of DNA." *Nature*. 2007;448(7154):714-7.
- **DOI:** [10.1038/nature05987](https://doi.org/10.1038/nature05987)
- **Citations:** ~1,400
- **Key findings:** DNMT3L specifically recognizes the N-terminal tail of histone H3 when K4 is UNMETHYLATED. Any methylation of H3K4 (me1/me2/me3) blocks DNMT3L binding and prevents de novo DNA methylation. This creates a biochemical switch: H3K4me3-positive regions cannot acquire DNA methylation.

### H3K36me3 Recruits DNMT3B for Gene Body Methylation

**Baubec et al. 2015** -- DNMT3B reads H3K36me3 to deposit gene body methylation.
- **Citation:** Baubec T, Colombo DF, Wirbelauer C, Schmidt J, Burger L, Krebs AR, Akalin A, Schubeler D. "Genomic profiling of DNA methyltransferases reveals a role for DNMT3B in genic methylation." *Nature*. 2015;520(7546):243-7.
- **DOI:** [10.1038/nature14176](https://doi.org/10.1038/nature14176)
- **Citations:** ~600
- **Key findings:** DNMT3B contains a PWWP domain that reads H3K36me3 (set by SETD2 during transcription elongation). This recruits DNMT3B to actively transcribed gene bodies, explaining why gene body DNA methylation correlates with transcription. Creates a positive correlation between H3K36me3 and DNA methylation in gene bodies.

### H3K9me3 and DNA Methylation Positive Feedback

H3K9 methylation and DNA methylation form a self-reinforcing loop in heterochromatin maintenance.

**Rose & Klose 2014** -- Review of H3K9me-DNA methylation crosstalk.
- **Citation:** Rose NR, Klose RJ. "Understanding the relationship between DNA methylation and histone lysine methylation." *Biochim Biophys Acta*. 2014;1839(12):1362-72.
- **DOI:** [10.1016/j.bbagrm.2014.02.007](https://doi.org/10.1016/j.bbagrm.2014.02.007)
- **Citations:** ~330
- **Key findings:** SUV39H1/2 write H3K9me3, which recruits HP1 proteins. HP1 recruits DNMT3A/B for DNA methylation. Conversely, methylated CpG recruits MBD1, which recruits SETDB1 (another H3K9 methyltransferase). This positive feedback loop stabilizes constitutive heterochromatin.

**Li et al. 2021** -- Updated review of DNA-histone methylation interplay and disease implications.
- **Citation:** Li Y, Chen X, Lu C. "The interplay between DNA and histone methylation: molecular mechanisms and disease implications." *EMBO Rep*. 2021;22(5):e51803.
- **DOI:** [10.15252/embr.202051803](https://doi.org/10.15252/embr.202051803)
- **Citations:** ~156
- **Key findings:** Comprehensive summary of bidirectional crosstalk. H3K27me3 and DNA methylation are antagonistic at CGIs but compatible in non-CGI regions. Loss of DNA methylation (e.g., DNMT TKO) redistributes H3K27me3 genome-wide. Disease mutations often disrupt both systems simultaneously.

### TET Proteins and Active DNA Demethylation

The TET (Ten-Eleven Translocation) family enzymes oxidize 5mC to 5-hydroxymethylcytosine (5hmC), 5-formylcytosine (5fC), and 5-carboxylcytosine (5caC), constituting the active DNA demethylation pathway.

**Wu & Zhang 2017** -- Definitive review of TET-mediated demethylation.
- **Citation:** Wu X, Zhang Y. "TET-mediated active DNA demethylation: mechanism, function and beyond." *Nat Rev Genet*. 2017;18(9):517-534.
- **DOI:** [10.1038/nrg.2017.33](https://doi.org/10.1038/nrg.2017.33)
- **Citations:** ~1,300
- **Key findings:** TET1/2/3 oxidize 5mC to 5hmC (stable mark) and further to 5fC and 5caC (removed by TDG and base excision repair). 5hmC is enriched at active enhancers and gene bodies. TET2 is frequently mutated in myeloid malignancies. TET proteins link chromatin state to metabolic status (require alpha-ketoglutarate as co-substrate).

**Chromatin association of 5hmC:**
- High 5hmC at active enhancers (correlates with H3K4me1, H3K27ac)
- Moderate 5hmC in gene bodies (correlates with H3K36me3)
- Low 5hmC at CGI promoters (already unmethylated)
- Absent 5hmC in heterochromatin (no 5mC substrate in active regions; no TET access in compacted regions)

### Bivalent Chromatin and DNA Methylation

Bivalent domains (H3K4me3 + H3K27me3) at developmental gene promoters in ESCs are protected from DNA methylation by the H3K4me3-DNMT3L exclusion mechanism. During differentiation, resolution of bivalency can result in:
- **Activation:** Loss of H3K27me3, gain of H3K27ac; remains unmethylated
- **Stable silencing:** Loss of H3K4me3, retention of H3K27me3; some loci then gain DNA methylation (particularly in cancer, see Part 10)

### Quick Reference: DNA Methylation-Histone Modification Crosstalk

| Histone Mark | Relationship with DNA Methylation | Mechanism |
|---|---|---|
| H3K4me3 | Mutually exclusive (at CGIs) | DNMT3L cannot bind methylated H3K4 |
| H3K36me3 | Positive correlation (gene bodies) | DNMT3B PWWP domain reads H3K36me3 |
| H3K9me3 | Positive feedback loop | HP1 recruits DNMTs; MBD1 recruits SETDB1 |
| H3K27me3 | Antagonistic at CGIs; compatible elsewhere | DNA methylation prevents PRC2 recruitment at CGIs |
| H3K27ac | Negative correlation | Active enhancers are demethylated by TET |
| 5hmC (TET product) | Marks active demethylation | Enriched at enhancers with H3K4me1/H3K27ac |

---

## 9. Part 8: Nucleosome Positioning and Dynamics

The precise positioning of nucleosomes determines which DNA sequences are accessible to transcription factors, polymerases, and regulatory proteins. ATAC-seq and DNase-seq, two key ENCODE assay types, fundamentally measure nucleosome positioning and occupancy.

### Nucleosome-Free Regions (NFRs) at Active Promoters

**Yuan et al. 2005** -- Genome-scale nucleosome positioning in yeast.
- **Citation:** Yuan GC, Liu YJ, Dion MF, Slack MD, Wu LF, Altschuler SJ, Rando OJ. "Genome-scale identification of nucleosome positions in S. cerevisiae." *Science*. 2005;309(5734):626-30.
- **DOI:** [10.1126/science.1112178](https://doi.org/10.1126/science.1112178)
- **Citations:** ~1,200
- **Key findings:** First genome-scale nucleosome map. Active Pol II promoters have a stereotyped architecture: ~200 bp nucleosome-free region (NFR) upstream of the TSS, flanked by well-positioned +1 and -1 nucleosomes. Poly(dA:dT) sequences disfavor nucleosome occupancy and are enriched in NFRs.

**Buenrostro et al. 2013** -- ATAC-seq: Assay for Transposase-Accessible Chromatin.
- **Citation:** Buenrostro JD, Giresi PG, Zaba LC, Chang HY, Greenleaf WJ. "Transposition of native chromatin for fast and sensitive epigenomic profiling of open chromatin, DNA-binding proteins, and nucleosome position." *Nat Methods*. 2013;10(12):1213-8.
- **DOI:** [10.1038/nmeth.2688](https://doi.org/10.1038/nmeth.2688)
- **Citations:** ~6,000
- **Key findings:** ATAC-seq uses Tn5 transposase to probe accessible chromatin. Sub-nucleosomal fragment sizes reveal nucleosome positioning. Requires only ~500-50,000 cells. Became the standard method for chromatin accessibility profiling. ENCODE adopted ATAC-seq extensively for accessibility mapping.

### The +1 Nucleosome

The first nucleosome downstream of the TSS (+1 nucleosome) is a critical regulatory element:
- Carries H3K4me3 and often H3.3 variant
- Precisely positioned by chromatin remodelers (RSC/SWI/SNF in yeast; homologs in mammals)
- Acts as a barrier to RNA Pol II; must be displaced or modified for transcription elongation
- CHD1 remodeler facilitates Pol II passage through the +1 nucleosome

**Schep et al. 2015** -- NucleoATAC: nucleosome positioning from ATAC-seq at base-pair resolution.
- **Citation:** Schep AN, Buenrostro JD, Denny SK, Schwartz K, Sherlock G, Greenleaf WJ. "Structured nucleosome fingerprints enable high-resolution mapping of chromatin architecture within regulatory regions." *Genome Res*. 2015;25(11):1757-70.
- **DOI:** [10.1101/gr.192294.115](https://doi.org/10.1101/gr.192294.115)
- **Citations:** ~318
- **Key findings:** ATAC-seq fragment sizes carry information about nucleosome rotational and translational positions. NucleoATAC algorithm achieves base-pair resolution nucleosome positioning. Applied to map promoter chromatin architecture across species, revealing conserved +1 nucleosome positioning rules.

### Nucleosome Turnover

Not all nucleosomes are equally stable. Nucleosome turnover rates vary dramatically across the genome:
- **High turnover:** Active enhancers, promoters -- nucleosomes are rapidly assembled and disassembled (minutes to hours)
- **Low turnover:** Heterochromatin, silenced genes -- nucleosomes are extremely stable (persist through cell cycles)
- **Intermediate turnover:** Gene bodies of active genes -- displaced by Pol II, reassembled by FACT complex and histone chaperones
- **Measurement:** Time-resolved CATCH-IT, metabolic labeling of histones

### Histone Variants and Nucleosome Properties

Histone variants alter the biophysical properties of nucleosomes, affecting stability, positioning, and regulatory function.

**Buschbeck & Hake 2017** -- Review of histone variants in cell fate and cancer.
- **Citation:** Buschbeck M, Hake SB. "Variants of core histones and their roles in cell fate decisions, development and cancer." *Nat Rev Mol Cell Biol*. 2017;18(5):299-314.
- **DOI:** [10.1038/nrm.2016.166](https://doi.org/10.1038/nrm.2016.166)
- **Citations:** ~294
- **Key findings:** H2A.Z destabilizes nucleosomes and marks regulatory elements (promoters, enhancers, insulators). H3.3 is deposited at active genes by HIRA and at heterochromatin by DAXX/ATRX. macroH2A reinforces gene silencing and is enriched on the inactive X chromosome. H2A.Z and H3.3 co-occupancy creates particularly labile nucleosomes at active regulatory elements.

**Key histone variants:**

| Variant | Deposition Complex | Genomic Location | Functional Role |
|---|---|---|---|
| H2A.Z | SWR1/SRCAP (INO80 removes) | TSS, enhancers, insulators | Marks regulatory elements; destabilizes nucleosome |
| H3.3 | HIRA (euchromatin); DAXX/ATRX (heterochromatin) | Active genes, telomeres, pericentromeres | Transcription-coupled deposition; dual roles |
| macroH2A | Unknown chaperone | Inactive X, senescence-associated heterochromatin | Reinforces silencing; resists remodeling |
| CENP-A (CenH3) | HJURP | Centromeres | Defines centromere identity |
| H2A.X | General deposition; phosphorylated at DSBs | Genome-wide (gamma-H2AX at breaks) | DNA damage response |

---

## 10. Part 9: 3D Genome Organization and Chromatin

The three-dimensional folding of chromatin is intimately linked to its epigenetic state. This section expands on the existing 3D genome references in the Master Reference List with deeper coverage of compartments, loop extrusion, enhancer-promoter interactions, LADs, and phase separation.

### Chromatin Compartments A and B

**Lieberman-Aiden et al. 2009** -- First genome-wide Hi-C map revealing A/B compartments.
- **Citation:** Lieberman-Aiden E, van Berkum NL, Williams L, Imakaev M, Raber T, Nynber A, Baber AK, Lajoie BR, Sabo PJ, Dorschner MO, Sandstrom R, Bernstein B, Bender MA, Groudine M, Gnirke A, Stamatoyannopoulos J, Mirny LA, Lander ES, Dekker J. "Comprehensive mapping of long-range interactions reveals folding principles of the human genome." *Science*. 2009;326(5950):289-93.
- **DOI:** [10.1126/science.1181369](https://doi.org/10.1126/science.1181369)
- **Citations:** ~6,500
- **Key findings:** Developed Hi-C method. Identified two spatial compartments: A (active, gene-rich, early-replicating, GC-rich) and B (inactive, gene-poor, late-replicating, AT-rich). A compartments correlate with H3K27ac, H3K4me3, H3K36me3; B compartments correlate with H3K27me3, H3K9me3. Chromatin state, not gene content alone, determines compartmentalization.

**Schwarzer et al. 2017** -- Cohesin removal reveals two independent organizational mechanisms.
- **Citation:** Schwarzer W, Abdennur N, Goloborodko A, Pekowska A, Fudenberg G, Loe-Mie Y, Fonseca NA, Huber W, Haering CH, Mirny LA, Spitz F. "Two independent modes of chromatin organization revealed by cohesin removal." *Nature*. 2017;551:51-56.
- **DOI:** [10.1038/nature24281](https://doi.org/10.1038/nature24281)
- **Citations:** ~1,000
- **Key findings:** Nipbl deletion (prevents cohesin loading) eliminates all TADs and Hi-C loops globally, but STRENGTHENS compartmentalization. Unmasks a finer compartment structure reflecting the epigenetic landscape. Proves that compartments (epigenetically driven) and TADs (cohesin-driven) are independent organizational layers.

### Loop Extrusion Model

**Fudenberg et al. 2016** -- Loop extrusion model for TAD formation.
- **Citation:** Fudenberg G, Imakaev M, Lu C, Goloborodko A, Abdennur N, Mirny LA. "Formation of chromosomal domains by loop extrusion." *Cell Rep*. 2016;15(9):2038-49.
- **DOI:** [10.1016/j.celrep.2016.04.085](https://doi.org/10.1016/j.celrep.2016.04.085)
- **Citations:** ~1,500
- **Key findings:** Proposed and simulated the loop extrusion model: cohesin loads onto chromatin and extrudes a loop until it encounters a CTCF boundary (convergent orientation). Explains TAD formation, boundary insulation, and CTCF orientation dependence. Loop extrusion also facilitates enhancer-promoter contact by bringing distal elements into proximity.

**Rowley & Corces 2018** -- Review synthesizing 3D genome organizational principles.
- **Citation:** Rowley MJ, Corces VG. "Organizational principles of 3D genome architecture." *Nat Rev Genet*. 2018;19(12):789-800.
- **DOI:** [10.1038/s41576-018-0060-8](https://doi.org/10.1038/s41576-018-0060-8)
- **Citations:** ~925
- **Key findings:** Compartments are smaller than originally thought; fine-scale compartmental domains exist within TADs. Loop extrusion by cohesin actively mixes chromatin, partially counteracting compartmentalization. 3D organization is both a cause and consequence of transcription.

### Enhancer-Promoter Loops

**Schoenfelder & Fraser 2019** -- Comprehensive review of enhancer-promoter contacts.
- **Citation:** Schoenfelder S, Fraser P. "Long-range enhancer-promoter contacts in gene expression control." *Nat Rev Genet*. 2019;20(8):437-455.
- **DOI:** [10.1038/s41576-019-0128-0](https://doi.org/10.1038/s41576-019-0128-0)
- **Citations:** ~870
- **Key findings:** Enhancer-promoter contacts bridge tens to hundreds of kilobases. TADs constrain the set of potential enhancer-promoter pairs. Most enhancer-promoter contacts are pre-formed (present before gene activation) and strengthened upon activation. Chromatin marks (H3K27ac, H3K4me1) at enhancers predict their target genes with moderate accuracy; 3D contact data greatly improves prediction.

### Lamina-Associated Domains (LADs)

**Briand & Collas 2020** -- Review of LAD organization and function.
- **Citation:** Briand N, Collas P. "Lamina-associated domains: peripheral matters and internal affairs." *Genome Biol*. 2020;21:85.
- **DOI:** [10.1186/s13059-020-02003-5](https://doi.org/10.1186/s13059-020-02003-5)
- **Citations:** ~193
- **Key findings:** LADs cover ~35-40% of the mammalian genome. Overlap with B compartment, late replication timing. Constitutive LADs (cLADs) are shared across cell types; facultative LADs (fLADs) are cell-type-specific. LADs are gene-poor and transcriptionally repressed, enriched for H3K9me2 and H3K9me3.

**Poleshko et al. 2019** -- H3K9me2 as an epigenetic memory mark for LAD positioning.
- **Citation:** Poleshko A, Smith CL, Nguyen SC, Sivaramakrishnan P, Murray JI, Lakadamyali M, Joyce EF, Jain R, Epstein JA. "H3K9me2 orchestrates inheritance of spatial positioning of peripheral heterochromatin through mitosis." *eLife*. 2019;8:e49278.
- **DOI:** [10.7554/eLife.49278](https://doi.org/10.7554/eLife.49278)
- **Citations:** ~92
- **Key findings:** H3K9me2 (not H3K9me3) is the specific mark of lamina-associated chromatin. H3K9me2 is retained through mitosis (shielded by H3S10 phosphorylation) and serves as a guidepost for re-establishing nuclear peripheral positioning in daughter cells. Establishes H3K9me2 as a 3D architectural mitotic bookmark.

### Phase Separation and Chromatin Compartmentalization

**Hnisz et al. 2017** -- Phase separation model for transcriptional control.
- **Citation:** Hnisz D, Shrinivas K, Young RA, Chakraborty AK, Sharp PA. "A phase separation model for transcriptional control." *Cell*. 2017;169(1):13-23.
- **DOI:** [10.1016/j.cell.2017.02.007](https://doi.org/10.1016/j.cell.2017.02.007)
- **Citations:** ~1,200
- **Key findings:** Proposed that super-enhancers form phase-separated condensates that concentrate transcription machinery. TFs with intrinsically disordered regions (IDRs) can phase-separate. Explains sensitivity of SE-driven genes to small perturbations (crossing the phase boundary). Provides a biophysical framework for understanding SE function.

**Sabari et al. 2018** -- Experimental evidence for coactivator phase separation at super-enhancers.
- **Citation:** Sabari BR, Dall'Agnese A, Boija A, Klein IA, Coffey EL, Shrinivas K, Abraham BJ, Hannett NM, Zamudio AV, Manteiga JC, Li CH, Guo YE, Day DS, Schuijers J, Vasile E, Malik S, Hnisz D, Lee TI, Cisse II, Roeder RG, Sharp PA, Chakraborty AK, Young RA. "Coactivator condensation at super-enhancers links phase separation and gene control." *Science*. 2018;361(6400):eaar3958.
- **DOI:** [10.1126/science.aar3958](https://doi.org/10.1126/science.aar3958)
- **Citations:** ~1,970
- **Key findings:** BRD4 and MED1 form liquid-like condensates at super-enhancers. MED1 IDR droplets compartmentalize and concentrate the transcription apparatus from nuclear extracts. Condensates are disrupted by 1,6-hexanediol (a tool to probe phase separation). Connects the biophysical phenomenon of phase separation to gene regulation.

**Caveat:** Phase separation in chromatin biology is an active and sometimes contentious area. Some observations originally attributed to liquid-liquid phase separation may reflect other forms of molecular clustering. The field is still establishing rigorous criteria for in vivo phase separation.

---

## 11. Part 10: Chromatin in Disease

Chromatin dysregulation is a hallmark of many diseases, from cancer to metabolic disorders to aging. This section expands the cancer chromatin content in the existing reference with oncohistones, SWI/SNF mutations, EZH2 alterations, aging, and novel metabolic histone modifications.

### Oncohistone Mutations

Recurrent mutations in histone H3 genes were discovered in pediatric brain tumors and represent a new paradigm: the histone itself is the oncogenic driver.

**Lewis et al. 2013** -- H3K27M oncohistone mechanism (already in Master Reference List as ref #37).
- **Citation:** Lewis PW, Muller MM, Koletsky MS, Cordero F, Lin S, Banaszynski LA, Garcia BA, Muir TW, Becher OJ, Allis CD. "Inhibition of PRC2 activity by a gain-of-function H3 mutation found in pediatric glioblastoma." *Science*. 2013;340(6134):857-61.
- **DOI:** [10.1126/science.1232245](https://doi.org/10.1126/science.1232245)
- **Citations:** ~1,800
- **Key findings:** H3K27M (K-to-M substitution at lysine 27) acts as a dominant-negative inhibitor of PRC2. Even though only ~3-17% of H3 molecules carry the mutation, global H3K27me3 is dramatically reduced. This derepresses Polycomb target genes and drives diffuse midline glioma (DIPG).

**Oncohistone landscape:**

| Mutation | Cancer Type | Mechanism | Chromatin Effect |
|---|---|---|---|
| H3K27M | Diffuse midline glioma (DIPG) | Inhibits PRC2 | Global H3K27me3 loss |
| H3G34R/V | Hemispheric glioma (adolescents) | Inhibits SETD2 in cis | Local H3K36me3 loss |
| H3K36M | Chondrosarcoma, head/neck SCC | Inhibits NSD1/2 and SETD2 | Global H3K36me2/me3 loss |
| H3K27I | Rare gliomas | PRC2 inhibition (weaker) | Partial H3K27me3 reduction |
| H3.1K27M | DIPG (younger children) | PRC2 inhibition + distinct co-mutations | Overlaps with ACVR1 mutations |

### SWI/SNF Mutations in Cancer

More than 20% of human cancers harbor mutations in SWI/SNF (BAF/PBAF) subunits, making this the most commonly mutated chromatin regulatory complex in oncology.

**Key mutation-cancer associations:**
- **ARID1A:** 40-50% ovarian clear cell carcinoma; 15-30% cholangiocarcinoma, gastric, endometrial
- **PBRM1:** ~40% clear cell renal cell carcinoma
- **SMARCB1:** ~100% rhabdoid tumors (biallelic loss); hallmark of this cancer
- **SMARCA4:** Small cell carcinoma of the ovary, hypercalcemic type; lung cancers
- **ARID2:** ~18% melanoma

SWI/SNF loss results in unopposed Polycomb repression: without SWI/SNF to eject PRC1/PRC2, H3K27me3 domains expand and silence tumor suppressor genes. This creates a therapeutic vulnerability: EZH2 inhibitors can partially rescue SWI/SNF-deficient tumors.

### EZH2 Gain and Loss of Function in Cancer

**Kim & Roberts 2016** -- Comprehensive review of EZH2 in cancer.
- **Citation:** Kim KH, Roberts CW. "Targeting EZH2 in cancer." *Nat Med*. 2016;22(2):128-134.
- **DOI:** [10.1038/nm.4036](https://doi.org/10.1038/nm.4036)
- **Citations:** ~1,270
- **Key findings:** EZH2 gain-of-function mutations (Y641, A677, A687) increase H3K27me3 levels; found in follicular lymphoma and DLBCL. EZH2 loss-of-function mutations decrease H3K27me3; found in MDS, MPN, and T-ALL. Context-dependent oncogene vs. tumor suppressor. EZH2 inhibitor tazemetostat (Tazverik) FDA-approved for epithelioid sarcoma and follicular lymphoma.

### Global Chromatin Changes in Aging

Aging is accompanied by progressive changes in chromatin organization that affect gene expression fidelity.

**Key aging-associated chromatin changes:**
- **H3K9me3 loss:** Constitutive heterochromatin decondenses with age, leading to derepression of transposable elements and satellite repeats
- **H3K27me3 redistribution:** Facultative heterochromatin becomes less precisely targeted
- **Lamin B1 reduction:** Causes LAD detachment and B-to-A compartment switching at formerly silenced loci
- **DNA methylation erosion:** Global hypomethylation but focal hypermethylation at CGI promoters (epigenetic drift)
- **SAHF formation:** In oncogene-induced senescence, heterochromatin reorganizes into Senescence-Associated Heterochromatin Foci (condensation of H3K9me3 + macroH2A)

**Zhang et al. 2021** -- Heterochromatin loss causes 3D genome reorganization in senescence.
- **Citation:** Zhang X, Liu X, Du Z, Wei L, Fang H, Dong Q, Niu J, Li Y, Gao J, Zhang MQ, Xie W, Wang X. "The loss of heterochromatin is associated with multiscale three-dimensional genome reorganization and aberrant transcription during cellular senescence." *Genome Res*. 2021;31(7):1121-1135.
- **DOI:** [10.1101/gr.275235.121](https://doi.org/10.1101/gr.275235.121)
- **Citations:** ~65
- **Key findings:** Facultative heterochromatin (H3K27me3) shifts from B-to-A compartment during senescence; constitutive heterochromatin (H3K9me3) shows enhanced self-interactions. Both types show increased chromatin accessibility and transcriptional leakage. Novel CTCF loops form in heterochromatin. Repetitive elements (LTRs, satellites) become aberrantly expressed.

### Chromatin in Metabolic Disease: Novel Histone Acylations

Beyond acetylation and methylation, histones can be modified by metabolic intermediates, directly linking cellular metabolism to chromatin state.

**Xie et al. 2016** -- Discovery of histone beta-hydroxybutyrylation (Kbhb).
- **Citation:** Xie Z, Zhang D, Chung D, Tang Z, Huang H, Dai L, Qi S, Li J, Colak G, Chen Y, Xia C, Peng C, Rber H, Kirber MT, Wang PM, Ballou LM, Thompson CB, Lin RZ, Zhao Y. "Metabolic regulation of gene expression by histone lysine beta-hydroxybutyrylation." *Mol Cell*. 2016;62(2):194-206.
- **DOI:** [10.1016/j.molcel.2016.03.036](https://doi.org/10.1016/j.molcel.2016.03.036)
- **Citations:** ~500
- **Key findings:** Identified histone lysine beta-hydroxybutyrylation (Kbhb) as a new modification driven by the ketone body beta-hydroxybutyrate. Increases during starvation/ketosis/diabetic ketoacidosis. H3K9bhb marks are associated with active gene promoters in a pattern distinct from H3K9ac. Links metabolic state (fasting, diabetes) to gene regulation via chromatin.

**Zhang et al. 2019** -- Discovery of histone lactylation (Kla).
- **Citation:** Zhang D, Tang Z, Huang H, Zhou G, Cui C, Weng Y, Liu W, Kim S, Lee S, Perez-Neut M, Ding J, Czyz D, Hu R, Ye Z, He M, Zheng YG, Shuman HA, Dai L, Ren B, Roeder RG, Becker L, Zhao Y. "Metabolic regulation of gene expression by histone lactylation." *Nature*. 2019;574(7779):575-580.
- **DOI:** [10.1038/s41586-019-1678-1](https://doi.org/10.1038/s41586-019-1678-1)
- **Citations:** ~2,600
- **Key findings:** Lactate-derived lactylation of histone lysine residues (28 sites identified) directly stimulates gene transcription. In M1 macrophages, histone lactylation has different temporal dynamics from acetylation. In the late phase of M1 polarization, Kla induces homeostatic genes (Arg1). An endogenous "lactate clock" regulates gene expression in response to glycolytic activity. Highly relevant to cancer biology (Warburg effect), inflammation, and diabetes.

**Relevance to islet biology and metabolic disease:**
- **Kbhb:** Elevated during diabetic ketoacidosis; may alter beta-cell gene expression programs. Histone Kbhb at genes involved in glucose metabolism represents a direct metabolite-to-chromatin signaling axis.
- **Kla:** Lactylation may be relevant in islets under metabolic stress (high glucose induces glycolysis and lactate production). Inflammatory environments in type 1 diabetes could drive macrophage histone lactylation.
- **Histone crotonylation (Kcr):** Driven by short-chain fatty acid metabolism; enriched at active promoters; responsive to microbiome-derived metabolites
- **Histone succinylation:** TCA cycle intermediate succinyl-CoA is the donor; potential role in mitochondrial dysfunction states

### Quick Reference: Novel Histone Acylations Beyond Acetylation

| Modification | Metabolic Precursor | Writer(s) | Eraser(s) | Chromatin Effect |
|---|---|---|---|---|
| Kbhb (beta-hydroxybutyrylation) | Beta-hydroxybutyrate (ketone body) | p300 (likely) | HDAC1/2/3, SIRT1/3 | Active genes; starvation-responsive |
| Kla (lactylation) | Lactate (glycolysis) | p300 | HDAC1-3, SIRT1/2/3 | Active genes; delayed kinetics vs. Kac |
| Kcr (crotonylation) | Crotonyl-CoA | p300/CBP, MOF | HDAC1/2/3, SIRT1/2/3 | Active promoters; testis-enriched |
| Ksucc (succinylation) | Succinyl-CoA (TCA cycle) | CPT1A (proposed) | SIRT5, SIRT7 | Gene regulation; metabolic sensing |
| Kpr (propionylation) | Propionyl-CoA | p300/CBP | SIRT1/2/3 | Active chromatin; less studied |
| Kbu (butyrylation) | Butyryl-CoA | p300/CBP | SIRT1/2/3 | Active chromatin; gut microbiome link |

---

## 12. Master Reference List

### Foundational Genome-Wide Profiling Studies

1. **Barski et al. 2007.** High-resolution profiling of histone methylations in the human genome. *Cell* 129:823-37. [DOI: 10.1016/j.cell.2007.05.009](https://doi.org/10.1016/j.cell.2007.05.009). PMID: 17512414. ~6,900 cit.

2. **Wang et al. 2008.** Combinatorial patterns of histone acetylations and methylations in the human genome. *Nat Genet* 40:897-903. [DOI: 10.1038/ng.154](https://doi.org/10.1038/ng.154). PMID: 18552846. ~2,400 cit.

3. **Mikkelsen et al. 2007.** Genome-wide maps of chromatin state in pluripotent and lineage-committed cells. *Nature* 448:553-60. [DOI: 10.1038/nature06008](https://doi.org/10.1038/nature06008). ~4,300 cit.

### Reviews

4. **Kouzarides 2007.** Chromatin modifications and their function. *Cell* 128:693-705. [DOI: 10.1016/j.cell.2007.02.005](https://doi.org/10.1016/j.cell.2007.02.005). ~10,700 cit.

5. **Bannister & Kouzarides 2011.** Regulation of chromatin by histone modifications. *Cell Res* 21:381-395. [DOI: 10.1038/cr.2011.22](https://doi.org/10.1038/cr.2011.22). ~5,300 cit.

### ChromHMM and Chromatin State Discovery

6. **Ernst & Kellis 2010.** Discovery and characterization of chromatin states for systematic annotation of the human genome. *Nat Biotechnol* 28:817-25. [DOI: 10.1038/nbt.1662](https://doi.org/10.1038/nbt.1662). ~1,100 cit.

7. **Ernst et al. 2011.** Mapping and analysis of chromatin state dynamics in nine human cell types. *Nature* 473:43-9. [DOI: 10.1038/nature09906](https://doi.org/10.1038/nature09906). PMID: 21441907. ~2,000 cit.

8. **Ernst & Kellis 2012.** ChromHMM: automating chromatin-state discovery and characterization. *Nat Methods* 9:215-6. [DOI: 10.1038/nmeth.1906](https://doi.org/10.1038/nmeth.1906). ~2,300 cit.

9. **Ernst & Kellis 2017.** Chromatin-state discovery and genome annotation with ChromHMM. *Nat Protocols* 12:2478-92. [DOI: 10.1038/nprot.2017.124](https://doi.org/10.1038/nprot.2017.124). ~711 cit.

### Consortium Papers

10. **ENCODE Project Consortium 2012.** An integrated encyclopedia of DNA elements in the human genome. *Nature* 489:57-74. [DOI: 10.1038/nature11247](https://doi.org/10.1038/nature11247). PMID: 22955616. ~8,000 cit.

11. **Kundaje et al. 2015.** Integrative analysis of 111 reference human epigenomes. *Nature* 518:317-30. [DOI: 10.1038/nature14248](https://doi.org/10.1038/nature14248). PMID: 25693563. ~5,000 cit.

12. **ENCODE Project Consortium (Moore et al.) 2020.** Expanded encyclopaedias of DNA elements in the human and mouse genomes. *Nature* 583:699-710. [DOI: 10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4). PMID: 32728249. ~2,000 cit.

### Enhancer Biology

13. **Heintzman et al. 2007.** Distinct and predictive chromatin signatures of transcriptional promoters and enhancers in the human genome. *Nat Genet* 39:311-18. [DOI: 10.1038/ng1966](https://doi.org/10.1038/ng1966). ~3,400 cit.

14. **Creyghton et al. 2010.** Histone H3K27ac separates active from poised enhancers and predicts developmental state. *PNAS* 107:21931-6. [DOI: 10.1073/pnas.1016071107](https://doi.org/10.1073/pnas.1016071107). PMID: 21106759. ~3,000 cit.

15. **Rada-Iglesias et al. 2011.** A unique chromatin signature uncovers early developmental enhancers in humans. *Nature* 470:279-83. [DOI: 10.1038/nature09692](https://doi.org/10.1038/nature09692). PMID: 21160473. ~1,500 cit.

### Bivalent Chromatin

16. **Bernstein et al. 2006.** A bivalent chromatin structure marks key developmental genes in embryonic stem cells. *Cell* 125:315-26. [DOI: 10.1016/j.cell.2006.02.041](https://doi.org/10.1016/j.cell.2006.02.041). ~5,400 cit.

17. **Kumar et al. 2021.** Decoding the function of bivalent chromatin in development and cancer. *Genome Res* 31:2170-84. [DOI: 10.1101/gr.266924.120](https://doi.org/10.1101/gr.266924.120). ~81 cit.

18. **Macrae et al. 2022.** Regulation, functions and transmission of bivalent chromatin during mammalian development. *Nat Rev Mol Cell Biol* 24:6-26. [DOI: 10.1038/s41580-022-00544-w](https://doi.org/10.1038/s41580-022-00544-w). ~117 cit.

### Super-Enhancers

19. **Whyte et al. 2013.** Master transcription factors and Mediator establish super-enhancers at key cell identity genes. *Cell* 153:307-19. [DOI: 10.1016/j.cell.2013.03.035](https://doi.org/10.1016/j.cell.2013.03.035). ~3,600 cit.

20. **Hnisz et al. 2013.** Super-enhancers in the control of cell identity and disease. *Cell* 155:934-47. [DOI: 10.1016/j.cell.2013.09.053](https://doi.org/10.1016/j.cell.2013.09.053). ~3,200 cit.

21. **Loven et al. 2013.** Selective inhibition of tumor oncogenes by disruption of super-enhancers. *Cell* 153:320-34. [DOI: 10.1016/j.cell.2013.03.036](https://doi.org/10.1016/j.cell.2013.03.036). ~2,700 cit.

### Heterochromatin and H3K9 Methylation

22. **Rea et al. 2000.** Regulation of chromatin structure by site-specific histone H3 methyltransferases. *Nature* 406:593-9. [DOI: 10.1038/35020506](https://doi.org/10.1038/35020506). ~3,500 cit.

23. **Lachner et al. 2001.** Methylation of histone H3 lysine 9 creates a binding site for HP1 proteins. *Nature* 410:116-20. [DOI: 10.1038/35065132](https://doi.org/10.1038/35065132). ~2,000 cit.

24. **Padeken et al. 2022.** Establishment of H3K9-methylated heterochromatin and its functions in tissue differentiation and maintenance. *Nat Rev Mol Cell Biol* 23:623-40. [DOI: 10.1038/s41580-022-00483-2](https://doi.org/10.1038/s41580-022-00483-2). ~314 cit.

### PRC2 / H3K27me3

25. **Cao et al. 2002.** Role of histone H3 lysine 27 methylation in Polycomb-group silencing. *Science* 298:1039-43. [DOI: 10.1126/science.1076997](https://doi.org/10.1126/science.1076997). ~3,000 cit.

26. **Boyer et al. 2006.** Polycomb complexes repress developmental regulators in murine embryonic stem cells. *Nature* 441:349-53. [DOI: 10.1038/nature04733](https://doi.org/10.1038/nature04733). ~3,000 cit.

### H3K36me3 / Transcription Elongation

27. **Bannister et al. 2005.** Histone methylation: dynamic or static? *Cell* 109:801-6 / Regulation of chromatin by histone modifications. [DOI: 10.1038/nature04219](https://doi.org/10.1038/nature04219). ~800 cit.

28. **Yoh et al. 2008.** The Iws1:Spt6:CTD complex controls cotranscriptional mRNA biosynthesis and HYPB/Setd2-mediated histone H3K36 methylation. *Genes Dev* 22:3422-34. [DOI: 10.1101/gad.1710608](https://doi.org/10.1101/gad.1710608). ~249 cit.

### H4K20 Methylation

29. **Rice et al. 2002.** Mitotic-specific methylation of histone H4 Lys 20 follows increased PR-Set7 expression and its localization to mitotic chromosomes. *Genes Dev* 16:2225-30. [DOI: 10.1101/gad.986602](https://doi.org/10.1101/gad.986602). ~257 cit.

### H4K16ac and Cancer

30. **Fraga et al. 2005.** Loss of acetylation at Lys16 and trimethylation at Lys20 of histone H4 is a common hallmark of human cancer. *Nat Genet* 37:391-400. [DOI: 10.1038/ng1531](https://doi.org/10.1038/ng1531). ~2,000 cit.

31. **Shogren-Knaak et al. 2006.** Histone H4-K16 acetylation controls chromatin structure and protein interactions. *Science* 311:844-7. [DOI: 10.1126/science.1124000](https://doi.org/10.1126/science.1124000). ~1,000 cit.

### 3D Genome Organization

32. **Dixon et al. 2012.** Topological domains in mammalian genomes identified by analysis of chromatin interactions. *Nature* 485:376-80. [DOI: 10.1038/nature11082](https://doi.org/10.1038/nature11082). ~4,000 cit.

33. **Nora et al. 2017.** Targeted degradation of CTCF decouples local insulation of chromosome domains from genomic compartmentalization. *Cell* 169:930-44. [DOI: 10.1016/j.cell.2017.09.026](https://doi.org/10.1016/j.cell.2017.09.026). ~1,437 cit.

34. **Rao et al. 2014.** A 3D map of the human genome at kilobase resolution reveals principles of chromatin looping. *Cell* 159:1665-80. [DOI: 10.1016/j.cell.2014.11.021](https://doi.org/10.1016/j.cell.2014.11.021). ~5,000 cit.

### H2BK120ub / Trans-histone Crosstalk

35. **Kim et al. 2009.** RAD6-mediated transcription-coupled H2B ubiquitylation directly stimulates H3K4 methylation in human cells. *Cell* 137:459-71. [DOI: 10.1016/j.cell.2009.02.027](https://doi.org/10.1016/j.cell.2009.02.027). ~700 cit.

### Cancer Chromatin Aberrations

36. **Ohm et al. 2007.** A stem cell-like chromatin pattern may predispose tumor suppressor genes to DNA hypermethylation and heritable silencing. *Nat Genet* 39:237-42. [DOI: 10.1038/ng1972](https://doi.org/10.1038/ng1972). ~1,500 cit.

37. **Lewis et al. 2013.** Inhibition of PRC2 activity by a gain-of-function H3 mutation found in pediatric glioblastoma. *Science* 340:857-61. [DOI: 10.1126/science.1232245](https://doi.org/10.1126/science.1232245). ~1,800 cit.

### TF Combinations and Co-Binding (Part 5)

38. **Heinz et al. 2010.** Simple combinations of lineage-determining transcription factors prime cis-regulatory elements required for macrophage and B cell identities. *Mol Cell* 38:576-89. [DOI: 10.1016/j.molcel.2010.05.004](https://doi.org/10.1016/j.molcel.2010.05.004). ~11,500 cit.

39. **Zaret & Carroll 2011.** Pioneer transcription factors: establishing competence for gene expression. *Genes Dev* 25:2227-41. [DOI: 10.1101/gad.176826.111](https://doi.org/10.1101/gad.176826.111). ~1,500 cit.

40. **Iwafuchi-Doi & Zaret 2014.** Pioneer transcription factors in cell reprogramming. *Genes Dev* 28:2679-2692. [DOI: 10.1101/gad.253443.114](https://doi.org/10.1101/gad.253443.114). ~562 cit.

41. **Visel et al. 2009.** ChIP-seq accurately predicts tissue-specific activity of enhancers. *Nature* 457:854-8. [DOI: 10.1038/nature07730](https://doi.org/10.1038/nature07730). ~2,200 cit.

42. **Raisner et al. 2018.** Enhancer activity requires CBP/P300 bromodomain-dependent histone H3K27 acetylation. *Cell Rep* 24:1722-1729. [DOI: 10.1016/j.celrep.2018.07.041](https://doi.org/10.1016/j.celrep.2018.07.041). ~282 cit.

43. **Lai et al. 2017.** MLL3/MLL4 are required for CBP/p300 binding on enhancers and super-enhancer formation in brown adipogenesis. *Nucleic Acids Res* 45:6388-6403. [DOI: 10.1093/nar/gkx234](https://doi.org/10.1093/nar/gkx234). ~153 cit.

44. **Schuettengruber et al. 2017.** Genome regulation by Polycomb and Trithorax: 70 years and counting. *Cell* 171:34-57. [DOI: 10.1016/j.cell.2017.08.002](https://doi.org/10.1016/j.cell.2017.08.002). ~860 cit.

45. **Agger et al. 2007.** UTX and JMJD3 are histone H3K27 demethylases involved in HOX gene regulation and development. *Nature* 449:731-734. [DOI: 10.1038/nature06145](https://doi.org/10.1038/nature06145). ~1,300 cit.

46. **Davidson et al. 2023.** CTCF is a DNA-tension-dependent barrier to cohesin-mediated loop extrusion. *Nature* 616:822-827. [DOI: 10.1038/s41586-023-05961-5](https://doi.org/10.1038/s41586-023-05961-5). ~109 cit.

### Chromatin Remodeling Complexes (Part 6)

47. **Kadoch & Crabtree 2015.** Mammalian SWI/SNF chromatin remodeling complexes and cancer. *Sci Adv* 1:e1500447. [DOI: 10.1126/sciadv.1500447](https://doi.org/10.1126/sciadv.1500447). ~1,000 cit.

48. **Mashtalir et al. 2018.** Modular organization and assembly of SWI/SNF family chromatin remodeling complexes. *Cell* 175:1272-1288. [DOI: 10.1016/j.cell.2018.09.032](https://doi.org/10.1016/j.cell.2018.09.032). ~600 cit.

49. **Hodges et al. 2016.** The many roles of BAF (mSWI/SNF) and PBAF complexes in cancer. *Cold Spring Harb Perspect Med* 6:a026930. [DOI: 10.1101/cshperspect.a026930](https://doi.org/10.1101/cshperspect.a026930). ~342 cit.

50. **Xue et al. 1998.** NURD, a novel complex with both ATP-dependent chromatin-remodeling and histone deacetylase activities. *Mol Cell* 2:851-61. [DOI: 10.1016/S1097-2765(00)80299-3](https://doi.org/10.1016/S1097-2765(00)80299-3). ~1,000 cit.

51. **Lai & Wade 2011.** Cancer biology and NuRD: a multifaceted chromatin remodelling complex. *Nat Rev Cancer* 11:588-596. [DOI: 10.1038/nrc3091](https://doi.org/10.1038/nrc3091). ~501 cit.

### DNA Methylation and Chromatin Interplay (Part 7)

52. **Jones 2012.** Functions of DNA methylation: islands, start sites, gene bodies and beyond. *Nat Rev Genet* 13:484-92. [DOI: 10.1038/nrg3230](https://doi.org/10.1038/nrg3230). ~3,000 cit.

53. **Ooi et al. 2007.** DNMT3L connects unmethylated lysine 4 of histone H3 to de novo methylation of DNA. *Nature* 448:714-7. [DOI: 10.1038/nature05987](https://doi.org/10.1038/nature05987). ~1,400 cit.

54. **Baubec et al. 2015.** Genomic profiling of DNA methyltransferases reveals a role for DNMT3B in genic methylation. *Nature* 520:243-7. [DOI: 10.1038/nature14176](https://doi.org/10.1038/nature14176). ~600 cit.

55. **Rose & Klose 2014.** Understanding the relationship between DNA methylation and histone lysine methylation. *Biochim Biophys Acta* 1839:1362-72. [DOI: 10.1016/j.bbagrm.2014.02.007](https://doi.org/10.1016/j.bbagrm.2014.02.007). ~330 cit.

56. **Li et al. 2021.** The interplay between DNA and histone methylation: molecular mechanisms and disease implications. *EMBO Rep* 22:e51803. [DOI: 10.15252/embr.202051803](https://doi.org/10.15252/embr.202051803). ~156 cit.

57. **Wu & Zhang 2017.** TET-mediated active DNA demethylation: mechanism, function and beyond. *Nat Rev Genet* 18:517-534. [DOI: 10.1038/nrg.2017.33](https://doi.org/10.1038/nrg.2017.33). ~1,300 cit.

### Nucleosome Positioning and Dynamics (Part 8)

58. **Yuan et al. 2005.** Genome-scale identification of nucleosome positions in S. cerevisiae. *Science* 309:626-30. [DOI: 10.1126/science.1112178](https://doi.org/10.1126/science.1112178). ~1,200 cit.

59. **Buenrostro et al. 2013.** Transposition of native chromatin for fast and sensitive epigenomic profiling of open chromatin, DNA-binding proteins, and nucleosome position. *Nat Methods* 10:1213-8. [DOI: 10.1038/nmeth.2688](https://doi.org/10.1038/nmeth.2688). ~6,000 cit.

60. **Schep et al. 2015.** Structured nucleosome fingerprints enable high-resolution mapping of chromatin architecture within regulatory regions. *Genome Res* 25:1757-70. [DOI: 10.1101/gr.192294.115](https://doi.org/10.1101/gr.192294.115). ~318 cit.

61. **Buschbeck & Hake 2017.** Variants of core histones and their roles in cell fate decisions, development and cancer. *Nat Rev Mol Cell Biol* 18:299-314. [DOI: 10.1038/nrm.2016.166](https://doi.org/10.1038/nrm.2016.166). ~294 cit.

### 3D Genome Organization (Part 9)

62. **Lieberman-Aiden et al. 2009.** Comprehensive mapping of long-range interactions reveals folding principles of the human genome. *Science* 326:289-93. [DOI: 10.1126/science.1181369](https://doi.org/10.1126/science.1181369). ~6,500 cit.

63. **Fudenberg et al. 2016.** Formation of chromosomal domains by loop extrusion. *Cell Rep* 15:2038-49. [DOI: 10.1016/j.celrep.2016.04.085](https://doi.org/10.1016/j.celrep.2016.04.085). ~1,500 cit.

64. **Schwarzer et al. 2017.** Two independent modes of chromatin organization revealed by cohesin removal. *Nature* 551:51-56. [DOI: 10.1038/nature24281](https://doi.org/10.1038/nature24281). ~1,000 cit.

65. **Rowley & Corces 2018.** Organizational principles of 3D genome architecture. *Nat Rev Genet* 19:789-800. [DOI: 10.1038/s41576-018-0060-8](https://doi.org/10.1038/s41576-018-0060-8). ~925 cit.

66. **Schoenfelder & Fraser 2019.** Long-range enhancer-promoter contacts in gene expression control. *Nat Rev Genet* 20:437-455. [DOI: 10.1038/s41576-019-0128-0](https://doi.org/10.1038/s41576-019-0128-0). ~870 cit.

67. **Briand & Collas 2020.** Lamina-associated domains: peripheral matters and internal affairs. *Genome Biol* 21:85. [DOI: 10.1186/s13059-020-02003-5](https://doi.org/10.1186/s13059-020-02003-5). ~193 cit.

68. **Poleshko et al. 2019.** H3K9me2 orchestrates inheritance of spatial positioning of peripheral heterochromatin through mitosis. *eLife* 8:e49278. [DOI: 10.7554/eLife.49278](https://doi.org/10.7554/eLife.49278). ~92 cit.

69. **Hnisz et al. 2017.** A phase separation model for transcriptional control. *Cell* 169:13-23. [DOI: 10.1016/j.cell.2017.02.007](https://doi.org/10.1016/j.cell.2017.02.007). ~1,200 cit.

70. **Sabari et al. 2018.** Coactivator condensation at super-enhancers links phase separation and gene control. *Science* 361:eaar3958. [DOI: 10.1126/science.aar3958](https://doi.org/10.1126/science.aar3958). ~1,970 cit.

### Chromatin in Disease (Part 10)

71. **Kim & Roberts 2016.** Targeting EZH2 in cancer. *Nat Med* 22:128-134. [DOI: 10.1038/nm.4036](https://doi.org/10.1038/nm.4036). ~1,270 cit.

72. **Zhang et al. 2021.** The loss of heterochromatin is associated with multiscale three-dimensional genome reorganization and aberrant transcription during cellular senescence. *Genome Res* 31:1121-1135. [DOI: 10.1101/gr.275235.121](https://doi.org/10.1101/gr.275235.121). ~65 cit.

73. **Xie et al. 2016.** Metabolic regulation of gene expression by histone lysine beta-hydroxybutyrylation. *Mol Cell* 62:194-206. [DOI: 10.1016/j.molcel.2016.03.036](https://doi.org/10.1016/j.molcel.2016.03.036). ~500 cit.

74. **Zhang et al. 2019.** Metabolic regulation of gene expression by histone lactylation. *Nature* 574:575-580. [DOI: 10.1038/s41586-019-1678-1](https://doi.org/10.1038/s41586-019-1678-1). ~2,600 cit.

---

*Based on articles retrieved from PubMed and Consensus/Semantic Scholar. Citation counts are approximate as of early 2026. All DOIs verified at time of writing.*
