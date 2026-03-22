---
name: neoantigen-vaccine-design
description: Guide the computational pipeline for designing personalized neoantigen cancer vaccines for veterinary patients. Covers tumor/normal sequencing, somatic variant calling, DLA/MHC typing, neoantigen prediction, and candidate selection. Use when exploring personalized immunotherapy for animal cancer patients.
---

# Personalized Neoantigen Vaccine Design for Veterinary Cancer

## Overview

Guide the end-to-end computational pipeline for designing personalized neoantigen cancer vaccines for veterinary patients. This is the same approach used in human precision oncology (Moderna/Merck Phase III trials), adapted for veterinary species. In March 2026, the first personalized mRNA cancer vaccine for a dog was successfully designed using this pipeline, reportedly resulting in significant tumor shrinkage (~50-75% reported in press) in a canine mast cell cancer case (Conyngham/UNSW, 2025-2026; not yet peer-reviewed).

This skill walks through each step: from tumor biopsy to sequencing, through computational neoantigen prediction, to candidate selection for vaccine design. The key veterinary-specific challenge is that dogs use DLA (Dog Leukocyte Antigen) instead of HLA, requiring adapted MHC binding prediction tools.

**Important:** This skill provides a computational research framework. Vaccine synthesis and administration require laboratory infrastructure, institutional ethics approval, and veterinary oncologist oversight. This is not a DIY protocol.

## When to Use

- User asks about personalized cancer treatment options for a veterinary patient
- User asks about neoantigen vaccines, mRNA vaccines, or immunotherapy for animals
- User asks about tumor sequencing or cancer genomics in dogs, cats, or horses
- User asks about the "Rosie" case or AI-designed veterinary cancer vaccines
- User wants to understand the computational pipeline for personalized veterinary cancer immunotherapy
- Keywords: neoantigen, mRNA vaccine, cancer vaccine, personalized, immunotherapy, tumor sequencing, DLA, MHC, WES, somatic mutation, AlphaFold
- **Related skill:** For the broader precision medicine framework (pharmacogenomics, targeted therapy, companion diagnostics), see `precision-medicine-mrna-design`. This skill focuses specifically on the 8-step neoantigen vaccine bioinformatics pipeline.

## The Pipeline: Step by Step

### Step 1: Tumor Biopsy and Sample Collection

**What happens:** Fresh tumor tissue is collected alongside a normal tissue sample (typically blood or buccal swab) from the same patient.

**Requirements:**
- Fresh or flash-frozen tumor tissue (FFPE is possible but yields lower quality DNA/RNA)
- Matched normal tissue (peripheral blood is standard)
- Sufficient tumor cellularity (ideally >60% tumor content)

**Veterinary considerations:**
- Tumor biopsy is a routine surgical procedure in veterinary oncology
- Sample handling and shipping to a genomics center must maintain cold chain
- Cost for this step: typically $200-500 for sample preparation

### Step 2: Whole Exome Sequencing (WES) + RNA Sequencing

**What happens:** Both the tumor and normal samples undergo next-generation sequencing. WES captures all protein-coding regions (~2% of the genome). RNA-seq measures which genes are actively expressed in the tumor.

**Specifications:**
- Tumor WES: target 300X coverage depth
- Normal WES: target 150X coverage depth
- Tumor RNA-seq: target 100M reads (fresh tissue, poly-A capture) or 300M reads (FFPE, Ribo-Zero)
- Reference genome: CanFam3.1/CanFam4 (dog), felCat9 (cat), EquCab3.0 (horse)

**Key tools:**
- Alignment: BWA-MEM2 or HISAT2 (DNA), STAR (RNA-seq)
- Quality control: FastQC, Picard MarkDuplicates, GATK BQSR

**Veterinary considerations:**
- Canine reference genome (CanFam3.1/CanFam4) is well-assembled and annotated
- Feline and equine genomes are available but with less annotation depth
- Sequencing cost: approximately $1,000-3,000 for WES + RNA-seq (commercial pricing as of 2026)
- Services like UNSW Ramaciotti Centre for Genomics or commercial labs (Novogene, BGI, Illumina) can process veterinary samples

### Step 3: Somatic Variant Calling

**What happens:** Compare tumor sequencing data against the matched normal to identify mutations unique to the cancer (somatic mutations). These are the mutations that create potential neoantigens.

**Key tools (standard pipeline):**
- Strelka2 (SNVs and indels)
- Mutect2 (GATK, SNVs and indels)
- VarScan2 (SNVs and indels)
- Pindel (structural variants, large indels)
- Best practice: use at least 2 callers and take the intersection or union with filtering

**Filtering criteria:**
- Tumor variant allele frequency (VAF) >= 5%
- Normal VAF = 0% (or < 1% to account for noise)
- Coverage depth >= 30X at variant site in both tumor and normal
- Non-synonymous mutations only (these change the protein sequence)

**Output:** VCF (Variant Call Format) file containing somatic mutations with annotations.

**Veterinary considerations:**
- The same tools used for human somatic variant calling work on canine/feline data with the appropriate reference genome
- Canine tumors typically harbor 1-5 somatic mutations per megabase (similar to many human cancers)
- Common canine cancer mutations: TP53, BRAF V595E (analogous to human V600E), KIT, NRAS, KRAS

### Step 4: DLA/MHC Typing (Species-Specific)

**What happens:** Determine the patient's MHC alleles. In dogs, this is DLA (Dog Leukocyte Antigen). The MHC determines which mutant peptides can be presented to the immune system.

**This is the critical veterinary-specific step.** Human pipelines use well-characterized HLA typing tools (OptiType, HLA-HD, xHLA). Canine MHC typing is less mature but rapidly advancing.

**Canine DLA system:**
- DLA-88 is the primary classical MHC class I gene in dogs (analogous to HLA-A/B/C)
- ~150 known DLA-88 alleles (vs. 12,000+ HLA alleles in humans)
- DLA-12 and DLA-64 are additional MHC-I loci with unclear classical status
- DLA-DRB1, DLA-DQA1, DLA-DQB1 are MHC class II genes

**Key tools for DLA typing:**
- KPR assembler (de novo assembly from RNA-seq data, validated for DLA-88)
- seq2HLA (can be adapted for canine with DLA reference sequences)
- PCR-based Sanger sequencing (gold standard but slower)
- Pseudo-alignment of RNA-seq reads against known DLA sequences

**Known DLA-88 binding motifs:**
- DLA-88*50101: binding motif characterized, similar to human HLA-A*02:01 (Barth et al., 2016, PLOS ONE)
- DLA-88*034:01: motif known, dominant in Boxer breed
- DLA-88*002:01: used in canine melanoma neoantigen prediction studies

**Veterinary considerations:**
- DLA typing is less standardized than HLA typing. Fewer known alleles means higher chance of encountering novel alleles.
- Breed-specific DLA distributions exist (some breeds have limited MHC diversity)
- For cats: FLA (Feline Leukocyte Antigen) system is even less characterized than DLA
- For horses: ELA (Equine Leukocyte Antigen) has reasonable characterization

### Step 5: Neoantigen Prediction

**What happens:** Combine somatic mutations with MHC typing to predict which mutant peptides will bind to the patient's MHC molecules and potentially be recognized by T cells.

**Key tools:**
- **pVACtools** (https://pvactools.readthedocs.io): The most comprehensive neoantigen prediction suite. Supports multiple binding prediction algorithms. Has been used in canine neoantigen studies.
- **NetMHCpan 4.1**: Neural network-based MHC binding prediction. Trained primarily on human data but can accept custom MHC sequences. The most widely used binding predictor.
- **MHCflurry**: Open-source MHC class I binding prediction.
- **AlphaFold**: Protein structure prediction for modeling mutant protein 3D structure and confirming neoantigen surface accessibility.

**Prediction workflow:**
1. Generate all possible mutant peptides (8-11 amino acids for MHC-I) from each somatic mutation
2. Predict binding affinity of each mutant peptide to each of the patient's DLA alleles
3. Also predict binding of the corresponding wild-type (normal) peptide
4. Calculate "differential agretopicity index" (DAI): how much better does the mutant bind vs. wild-type?
5. Filter for strong binders: IC50 < 500 nM (or percentile rank < 2%)

**Veterinary-specific adaptation:**
- NetMHCpan can accept DLA protein sequences directly if the allele is not in its training set
- pVACtools has been validated for canine neoantigen prediction against DLA-88*002:01
- When DLA binding data is limited, the similarity between DLA-88*50101 and HLA-A*02:01 can be leveraged cautiously

### Step 6: Neoantigen Prioritization and Selection

**What happens:** From potentially hundreds of predicted binders, select the 10-20 best candidates for vaccine inclusion.

**Prioritization criteria (ranked):**
1. **Binding affinity:** Strong binders (IC50 < 50 nM) over moderate binders
2. **Differential agretopicity:** High DAI (mutant binds much better than wild-type)
3. **Expression level:** Mutation must be expressed in the tumor (confirmed by RNA-seq, TPM > 1)
4. **Clonality:** Mutations present in all tumor cells (high VAF) over subclonal mutations
5. **AlphaFold confidence:** High pLDDT score for the mutant protein structure, confirming the neoantigen is in a well-folded, surface-accessible region
6. **Binding to multiple alleles:** Neoantigens binding multiple DLA alleles are preferred
7. **Foreignness:** How different is the mutant peptide from any self-peptide in the proteome?
8. **Peptide stability:** Predicted half-life of the pMHC complex

**Output:** A ranked list of 10-20 neoantigen peptide sequences for vaccine design.

### Step 7: Vaccine Construct Design

**What happens:** The selected neoantigen sequences are encoded into a delivery format.

**Delivery options:**
- **mRNA vaccine** (as used in the Rosie case): mRNA encoding the selected neoantigens, formulated in lipid nanoparticles (LNPs). Same technology as COVID-19 mRNA vaccines.
- **Synthetic long peptide (SLP) vaccine:** Peptides synthesized chemically, combined with adjuvant.
- **Dendritic cell vaccine:** Patient's dendritic cells pulsed with neoantigen peptides ex vivo.

**mRNA construct design:**
- Concatenate selected neoantigen sequences (typically 25-mer context around each mutation)
- Add linker sequences between neoantigens
- Optimize codon usage for the target species
- Add 5' cap, UTRs, and poly-A tail for stability
- Formulate in LNPs for delivery

**This step requires laboratory infrastructure.** The mRNA must be synthesized, purified, quality-controlled, and formulated by a qualified RNA laboratory or contract manufacturer.

### Step 8: Administration and Monitoring

**Vaccine administration:**
- Subcutaneous or intramuscular injection
- Prime-boost schedule (typically 2-3 doses, 2-4 weeks apart)
- Often combined with immune checkpoint inhibitors (anti-PD-1/PD-L1) to enhance response
- Requires veterinary oncologist oversight and institutional ethics approval for experimental treatments

**Response monitoring:**
- Tumor measurement (calipers, ultrasound, CT) at defined intervals
- Immune monitoring: ELISPOT or flow cytometry for neoantigen-specific T cell responses
- Blood chemistry and CBC for safety monitoring
- Imaging for metastatic disease assessment

## Practical Guide: How to Get Started

### Who Is This For?

This pipeline is relevant for three audiences with different entry points:

| Audience | Starting Point | What They Need |
| --- | --- | --- |
| **Pet owner with a cancer diagnosis** | "My dog has advanced cancer, chemo isn't working" | Start at "Talking to Your Vet" below |
| **Veterinary oncologist** | "I want to explore personalized immunotherapy for a patient" | Start at Step 1, coordinate with a genomics lab |
| **Researcher / bioinformatician** | "I have sequencing data and want to run the neoantigen pipeline" | Start at Step 3, you already have the VCF |

### Talking to Your Veterinarian (For Pet Owners)

Most veterinarians have not yet encountered personalized neoantigen vaccines. If you want to explore this option, here is how to frame the conversation:

1. **Ask for a referral to a veterinary oncologist.** General practice vets typically do not manage experimental immunotherapy. You need a board-certified veterinary oncologist (DACVIM-Oncology or DECVIM-CA).
2. **Frame it as "compassionate use" or "experimental therapy."** The language matters. Vets understand compassionate use protocols for cases where standard therapy has failed or is not an option.
3. **Key questions to ask your oncologist:**
   - "Is my pet's cancer type a good candidate for immunotherapy?" (High mutational burden tumors like mast cell tumors, melanoma, and hemangiosarcoma are better candidates than lymphoma.)
   - "Can you collect and ship a fresh-frozen tumor sample and matched blood sample to a genomics lab?"
   - "Are you willing to collaborate with a research group for an experimental treatment?"
   - "What institutional or ethics requirements apply in our jurisdiction?"
4. **Be realistic about cost.** This is currently a $7,000-56,000+ experimental process with no guarantee of success. See the cost table below.
5. **Be realistic about timeline.** From biopsy to vaccine administration is typically 2-4 months. Rapidly progressing cancers may not allow enough time.

### Where to Get Sequencing Done (Veterinary-Friendly Labs)

Most genomics labs process human samples but will accept veterinary samples with advance coordination. Key considerations: specify the species and reference genome, confirm they can return raw FASTQ or BAM files (not just a clinical report), and request both WES and RNA-seq.

| Lab / Service | Location | Notes |
| --- | --- | --- |
| UNSW Ramaciotti Centre for Genomics | Sydney, Australia | Processed the Rosie case. Research pricing available. |
| Novogene | Global (US, EU, Asia hubs) | Commercial sequencing, accepts veterinary samples, competitive pricing |
| BGI Genomics | Global (Shenzhen HQ) | Large-scale sequencing, veterinary-compatible |
| Azenta (formerly Genewiz) | US, EU, Asia | WES + RNA-seq services, will process non-human samples |
| Veterinary Genetics Laboratory (UC Davis) | California, USA | Specializes in veterinary genomics |
| Integrated Canine Data Commons (ICDC) | NIH / NCI | Free access to existing canine cancer genomic datasets for research |

**What to request from the lab:**
- Whole Exome Sequencing (WES): tumor + matched normal, 300X / 150X depth
- RNA-seq: tumor only, 100M reads minimum, poly-A capture
- Deliverables: raw FASTQ files, aligned BAM files, and basic QC report
- Reference genome: specify CanFam3.1 or CanFam4 (dog), felCat9 (cat), EquCab3.0 (horse)

### Running the Bioinformatics Pipeline (For Researchers)

If you have sequencing data and want to run the computational analysis yourself, there are two approaches:

**Option A: Use the OpenVax pipeline (recommended for beginners)**

The OpenVax neoantigen vaccine pipeline (https://github.com/openvax/neoantigen-vaccine-pipeline) is a Dockerized, Snakemake-based workflow that chains variant calling through neoantigen prediction. It was built for human samples but can be adapted for veterinary use by substituting the reference genome.

Requirements: Docker, 32GB+ RAM, 8+ CPU cores, 500GB+ storage for reference genomes and intermediate files.

**Option B: Run individual tools manually**

For more control, run each step separately:

1. Align reads: `bwa mem -t 8 CanFam3.1.fa tumor_R1.fq.gz tumor_R2.fq.gz | samtools sort -o tumor.bam`
2. Call variants: Run both Strelka2 and Mutect2, intersect results
3. Annotate: VEP (Variant Effect Predictor) with the Ensembl canine database
4. Predict neoantigens: `pvacseq run input.vcf SAMPLE_NAME "DLA-88*50101" NetMHCpan output_dir -e1 8,9,10,11`
5. Prioritize: Filter by IC50 < 500nM, expression > 1 TPM, DAI score

**Compute options:**
- Local workstation: Feasible for a single case with 32GB RAM
- Cloud: AWS/GCP with spot instances, approximately $20-50 per case for compute
- University HPC: Most research universities provide free compute for affiliated researchers

### Where to Get mRNA Synthesized (The Wet Lab Step)

This is the most expensive and least accessible step. mRNA synthesis and LNP formulation require specialized laboratory equipment (clean room, HPLC, lipid mixing).

| Partner Type | Examples | Approximate Cost | Notes |
| --- | --- | --- | --- |
| University RNA lab | UNSW RNA Institute, MIT Koch Institute, UPenn Gene Therapy | $5,000-15,000 | Research pricing, requires collaboration agreement |
| Contract RNA manufacturer | TriLink BioTechnologies, APExBIO, Integrated DNA Technologies | $10,000-50,000+ | Commercial pricing, faster turnaround |
| Peptide synthesis (SLP alternative) | GenScript, Peptide 2.0, CPC Scientific | $2,000-8,000 | Cheaper than mRNA, no LNP needed, but may be less effective |

**Important:** Most synthesis partners will require institutional affiliation or a collaboration with a licensed veterinarian. They will not synthesize a vaccine for an individual without institutional oversight.

### Decision Tree: Is This Right for My Patient?

**Start here:**

1. Is the cancer confirmed by histopathology? If NO: stop, get a definitive diagnosis first.
2. Has the cancer failed or is it expected to fail standard therapy (surgery, chemo, radiation)? If NO: pursue standard therapy first. Personalized vaccines are experimental and should not replace proven treatments.
3. Is the expected survival time long enough for the pipeline (2-4 months minimum from biopsy to first dose)? If NO: this approach may not be feasible. Consider palliative care.
4. Is the cancer type likely to have high mutational burden? Good candidates: mast cell tumor, melanoma, hemangiosarcoma, osteosarcoma, transitional cell carcinoma. Poor candidates: lymphoma (lower TMB), round cell tumors.
5. Can the owner commit $7,000-56,000+ with no guarantee of response? If NO: this is not currently an accessible option. Discuss with oncologist.
6. Is there a veterinary oncologist willing to oversee the case? If NO: do not proceed without specialist involvement.

If all answers are favorable: proceed to Step 1 (tumor biopsy and sample collection).

## Available Resources and Databases

| Resource | URL | Purpose |
| --- | --- | --- |
| CanFam3.1/4 reference genome | NCBI/Ensembl | Canine reference genome for alignment |
| IPD-MHC Database | https://www.ebi.ac.uk/ipd/mhc/ | Known DLA allele sequences |
| pVACtools | https://pvactools.readthedocs.io | Neoantigen prediction pipeline |
| NetMHCpan 4.1 | https://services.healthtech.dtu.dk | MHC binding prediction |
| AlphaFold | https://alphafold.ebi.ac.uk | Protein structure prediction |
| openvax pipeline | https://github.com/openvax/neoantigen-vaccine-pipeline | Open-source vaccine pipeline (human, adaptable) |
| COSMIC | https://cancer.sanger.ac.uk/cosmic | Cancer mutation database (cross-species reference) |
| IEDB | https://www.iedb.org | Immune epitope database and prediction tools |

## Cost Estimate (2026, approximate)

| Step | Estimated Cost |
| --- | --- |
| Tumor biopsy and sample prep | $200-500 |
| WES + RNA-seq (tumor + normal) | $1,000-3,000 |
| Bioinformatics analysis | $500-2,000 (or free with open-source tools + compute) |
| mRNA synthesis and LNP formulation | $5,000-50,000+ (research lab vs. GMP) |
| Veterinary oncologist consultation | $200-500 per visit |
| **Total (research/experimental)** | **$7,000-56,000+** |

Note: The Rosie case was performed at research cost through university collaboration. Commercial personalized veterinary cancer vaccines do not yet exist as a product.

## Current State of the Field

- **Proof of concept:** The Rosie case (2025-2026) reported successful pipeline application in a canine patient with mast cell cancer. Not yet peer-reviewed.
- **Active research:** Canine melanoma neoantigen vaccines are being studied at multiple institutions (NC State, Colorado State, UPenn).
- **DLA characterization is advancing:** New DLA-88 alleles are being discovered through NGS-based typing, expanding the reference database.
- **Comparative oncology value:** Dogs develop cancers similar to humans (melanoma, osteosarcoma, lymphoma, bladder cancer), making canine neoantigen vaccines valuable for both veterinary treatment and translational human medicine.
- **Regulatory landscape:** Veterinary experimental treatments face lighter regulatory scrutiny than human medicine, enabling faster iteration. No FDA CVM approval pathway currently exists for personalized veterinary cancer vaccines.

## Limitations

- **This is experimental.** Personalized neoantigen vaccines are at the frontier of veterinary oncology. The Rosie case is a single anecdotal case, not a clinical trial.
- **DLA typing is immature.** Only ~150 DLA-88 alleles are known vs. 12,000+ HLA alleles. Novel alleles are frequently discovered. Binding prediction accuracy for DLA is lower than for well-characterized HLA alleles.
- **Laboratory infrastructure required.** mRNA synthesis and LNP formulation require specialized equipment and expertise. This cannot be done at home.
- **Cost is prohibitive for most pet owners.** Until commercial pipelines exist, this approach costs thousands to tens of thousands of dollars.
- **No guarantee of efficacy.** Neoantigen prediction has a high false-positive rate (~95% of predicted neoantigens do not elicit T cell responses). Even in human trials, only a subset of patients respond.
- **Species-specific immunology gaps.** Canine T cell biology, checkpoint pathways, and tumor microenvironment are less characterized than human equivalents.
- **Not applicable to all cancers.** Tumors with low mutational burden (few somatic mutations) may not generate sufficient neoantigen candidates.
- **Ethics and oversight required.** Experimental treatments require institutional ethics approval and veterinary oncologist supervision.

## References

Key publications supporting this pipeline:

1. Barth et al. (2016). "Characterization of the Canine MHC Class I DLA-88*50101 Peptide Binding Motif." PLOS ONE. 11(11): e0167017.
2. Hundal et al. (2020). "pVACtools: A Computational Toolkit to Identify and Visualize Cancer Neoantigens." Cancer Immunology Research. 8(3): 409-420.
3. Pyo et al. (2022). "Genotyping of canine MHC gene DLA-88 by next-generation sequencing." HLA. 101(1): 30-44.
4. Conyngham/Thordarson/UNSW (2025-2026). First personalized mRNA cancer vaccine for a dog (Rosie case). UNSW RNA Institute / University of Queensland.
5. Ott et al. (2017). "An immunogenic personal neoantigen vaccine for patients with melanoma." Nature. 547: 217-221.
6. Genome Medicine (2019). "Best practices for bioinformatic characterization of neoantigens for clinical utility."
