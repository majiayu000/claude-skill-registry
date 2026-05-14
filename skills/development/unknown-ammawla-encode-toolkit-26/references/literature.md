# JASPAR Motifs — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the jaspar-motifs skill — key papers informing transcription factor binding profile databases, motif quality curation, and experimental methods for determining DNA-binding specificities.

---

## JASPAR Database Releases

---

### Castro-Mondragon et al. 2022 — JASPAR 2022: the 9th release

- **Citation:** Castro-Mondragon JA, Riudavets-Puig R, Rauluseviciute I, Lemma
  RB, Turber L, Blanc-Mathieu R, Lucas J, Boddie P, Khan A, Manosalva Perez N,
  et al. JASPAR 2022: the 9th release of the open-access database of
  transcription factor binding profiles. Nucleic Acids Research,
  50(D1):D165-D173, 2022.
- **DOI:** [10.1093/nar/gkab1113](https://doi.org/10.1093/nar/gkab1113)
- **PMID:** 34850907 | **PMC:** PMC8728201
- **Citations:** ~1,400
- **Key findings:** JASPAR 2022 expanded to 1,956 curated TF binding profiles
  (a 20% increase over JASPAR 2020) across 7 taxonomic groups: vertebrates
  (879 profiles), plants (635), insects (158), nematodes (49), fungi (175),
  urochordata (23), and a new unvalidated collection for computationally
  predicted profiles. Profiles are derived from ChIP-seq, DAP-seq, SELEX, and
  protein binding microarray experiments, each assigned a quality score based
  on the level of experimental validation and independent confirmation. The
  RESTful API (jaspar.elixir.no/api/v1/) supports programmatic retrieval of
  position frequency matrices (PFMs), position weight matrices (PWMs), and TF
  metadata including structural classification, UniProt accession, and source
  publication. JASPAR's defining feature is manual curation — every profile is
  reviewed by domain experts and cross-validated against independent data,
  distinguishing it from automated databases that trade accuracy for breadth.

---

### Sandelin et al. 2004 — JASPAR: the original open-access TF binding database

- **Citation:** Sandelin A, Alkema W, Engstrom P, Wasserman WW, Lenhard B.
  JASPAR: an open-access database for eukaryotic transcription factor binding
  profiles. Nucleic Acids Research, 32(Database issue):D91-D94, 2004.
- **DOI:** [10.1093/nar/gkh012](https://doi.org/10.1093/nar/gkh012)
- **PMID:** 14681366 | **PMC:** PMC308747
- **Citations:** ~2,500
- **Key findings:** Launched JASPAR as the first fully open-access alternative
  to the TRANSFAC database, which required costly commercial licensing that
  limited its use in academic research. The founding collection contained 111
  non-redundant, experimentally verified TF binding profiles represented as
  position frequency matrices (PFMs) — the raw count format from which PWMs,
  information content logos, and scanning thresholds are derived. Established
  the curation principles that still govern JASPAR two decades later: each
  profile must derive from direct experimental binding evidence (SELEX, DNase
  I footprinting, gel shift, ChIP), profiles are non-redundant (one canonical
  profile per TF per species per experimental method), and quality annotations
  distinguish high-confidence profiles from lower-confidence entries. The
  open-access model was revolutionary for the field, enabling unrestricted
  motif analysis in academic settings and establishing the PFM/PWM standard
  format adopted by HOMER, MEME Suite, and virtually all motif analysis tools.

---

### Mathelier et al. 2016 — JASPAR 2016: major expansion with ChIP-seq profiles

- **Citation:** Mathelier A, Fornes O, Arenillas DJ, Chen CY, Denber G, Lee J,
  Shi W, Shyr C, Tan G, Worsley-Hunt R, et al. JASPAR 2016: a major expansion
  and update of the open-access database of transcription factor binding
  profiles. Nucleic Acids Research, 44(D1):D110-D115, 2016.
- **DOI:** [10.1093/nar/gkv1176](https://doi.org/10.1093/nar/gkv1176)
- **PMID:** 26531826 | **PMC:** PMC4702842
- **Citations:** ~1,000
- **Key findings:** JASPAR 2016 represented a paradigm shift by incorporating
  ChIP-seq-derived binding profiles alongside traditional in vitro methods,
  growing the vertebrate core collection from 205 to 519 profiles (a 153%
  increase). Introduced pre-computed TFBS genome tracks providing genome-wide
  binding site predictions for all profiles in GRCh37 and mm9, eliminating the
  need for users to run their own FIMO/MOODS scans. Added structural
  classification of TFs based on DNA-binding domain architecture (C2H2 zinc
  finger, basic helix-loop-helix, homeodomain, basic leucine zipper, nuclear
  receptor, etc.), enabling family-level motif comparisons that reveal shared
  binding preferences within structural classes. The profile clustering tool
  groups TFs with similar binding specificities — critical for identifying
  when multiple motifs represent the same recognition sequence and for
  selecting non-redundant representative profiles for enrichment analysis.

---

### Khan et al. 2018 — JASPAR 2018: TF flexible models and expanded API

- **Citation:** Khan A, Fornes O, Stigliani A, Gheorghe M, Castro-Mondragon
  JA, van der Lee R, Besber A, Cheneby J, Kulkarni SR, Tan G, et al. JASPAR
  2018: update of the open-access database of transcription factor binding
  profiles and its web framework. Nucleic Acids Research, 46(D1):D260-D266,
  2018.
- **DOI:** [10.1093/nar/gkx1126](https://doi.org/10.1093/nar/gkx1126)
- **PMID:** 29140473 | **PMC:** PMC5753243
- **Citations:** ~900
- **Key findings:** JASPAR 2018 introduced TF flexible models (TFFMs) as a
  complement to traditional position weight matrices, using first-order hidden
  Markov models to capture dinucleotide positional dependencies that PWMs
  cannot represent due to their assumption of inter-position independence.
  TFFMs improve binding site prediction accuracy by 10-20% for TFs with strong
  positional dependencies, particularly C2H2 zinc finger proteins where
  adjacent finger-DNA contacts create correlated base preferences. The update
  expanded the vertebrate collection to 579 profiles with improved metadata
  linking to UniProt protein identifiers and Ensembl gene IDs for cross-
  database integration. Enhanced the interactive web interface with ChIP-seq
  peak enrichment data as a quality metric, allowing users to assess how well
  each profile predicts binding in independent ChIP-seq experiments. Added BED
  track downloads for direct genome browser visualization of predicted binding
  sites.

---

### Fornes et al. 2020 — JASPAR 2020: community curation and expanded coverage

- **Citation:** Fornes O, Castro-Mondragon JA, Khan A, van der Lee R, Zhang X,
  Richmond PA, Modi BP, Correard S, Gheorghe M, Baranasic D, et al. JASPAR
  2020: update of the open-access database of transcription factor binding
  profiles. Nucleic Acids Research, 48(D1):D87-D92, 2020.
- **DOI:** [10.1093/nar/gkz1001](https://doi.org/10.1093/nar/gkz1001)
- **PMID:** 31701148 | **PMC:** PMC7145627
- **Citations:** ~1,500
- **Key findings:** JASPAR 2020 reached 1,636 TF binding profiles with a 26%
  increase in the vertebrate core collection, incorporating profiles from
  ChIP-seq, ChIP-exo, DAP-seq (DNA affinity purification sequencing), and
  SMiLE-seq (selective microfluidics-based ligand enrichment sequencing)
  experiments. Introduced community-driven curation enabling researchers to
  submit profiles through a standardized web interface, accelerating database
  growth beyond the core curation team's capacity while maintaining quality
  standards. Added 315 non-validated profiles in a separate collection for TFs
  with computational predictions but lacking independent experimental
  confirmation — clearly separated from the curated core to maintain trust.
  Integrated CpG methylation sensitivity annotations for TFs whose binding
  affinity is modulated by cytosine methylation status, directly relevant for
  interpreting TF binding in the context of WGBS methylation data from ENCODE
  experiments.

---

## Binding Specificity Data

---

### Weirauch et al. 2014 — CIS-BP: comprehensive catalog of TF binding specificities

- **Citation:** Weirauch MT, Yang A, Albu M, Cote AG, Montenegro-Montero A,
  Drewe P, Najafabadi HS, Lambert SA, Mann I, Cook K, et al. Determination and
  inference of eukaryotic transcription factor sequence specificity. Cell,
  158(6):1431-1443, 2014.
- **DOI:** [10.1016/j.cell.2014.08.009](https://doi.org/10.1016/j.cell.2014.08.009)
- **PMID:** 25215497 | **PMC:** PMC4163041
- **Citations:** ~1,800
- **Key findings:** Created the CIS-BP (Catalog of Inferred Sequence Binding
  Preferences) database combining direct experimental binding data with
  homology-based inference: if two TFs share >80% amino acid identity in their
  DNA-binding domains, their binding motifs are predicted to be
  interchangeable with ~90% accuracy. This inference principle enabled motif
  prediction for thousands of TFs lacking direct experimental
  characterization, covering >1,000 species and dramatically expanding the
  universe of TFs with known or predicted motifs. CIS-BP serves as a
  complementary resource to JASPAR — CIS-BP prioritizes breadth through
  computational inference while JASPAR prioritizes depth through experimental
  validation and manual curation. A key biological finding was that the ~1,400
  human TFs converge on far fewer distinct binding specificities than the TF
  count suggests — many TF families share essentially identical core motifs,
  achieving regulatory specificity through cooperative binding, chromatin
  context, protein-protein interactions, and post-translational modifications
  rather than DNA sequence alone.

---

### Jolma et al. 2013 — DNA-binding specificities of human TFs by HT-SELEX

- **Citation:** Jolma A, Yan J, Whitington T, Toivonen J, Nitta KR, Rastas P,
  Morgunova E, Enge M, Taipale M, Wei G, et al. DNA-binding specificities of
  human transcription factors. Cell, 152(1-2):327-339, 2013.
- **DOI:** [10.1016/j.cell.2012.12.009](https://doi.org/10.1016/j.cell.2012.12.009)
- **PMID:** 23332764
- **Citations:** ~2,500
- **Key findings:** Determined DNA-binding specificities for 830 human TF DNA-
  binding domains spanning 239 structural classes using high-throughput SELEX
  (HT-SELEX) with 5 rounds of selection and deep sequencing. Revealed that
  most TFs recognize substantially longer sequences than captured by
  traditional 6-10 bp motif models, with secondary binding preferences and
  flanking nucleotide contexts that quantitatively modulate binding affinity
  by 2-10 fold — implying that standard PWM scanning with short motifs
  systematically underestimates the sequence information used for in vivo
  binding site selection. Discovered that many TF family members previously
  assumed to share identical binding preferences have distinct specificities
  driven by subtle amino acid differences at DNA-contact positions — for
  example, different bHLH heterodimers (MYC/MAX vs. TWIST/E12) prefer
  distinct E-box variants despite recognizing the same CANNTG core. The HT-
  SELEX dataset became a primary data source for JASPAR profiles and
  demonstrated strong correlation between in vitro binding specificities and
  in vivo ChIP-seq occupancy when chromatin accessibility and TF cooperativity
  are taken into account, validating the use of in vitro-derived motifs for
  interpreting ENCODE ChIP-seq peak sequences.

---
