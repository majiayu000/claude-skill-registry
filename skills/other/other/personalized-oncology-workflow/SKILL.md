---
name: personalized-oncology-workflow
description: Structured reasoning template for AI-assisted personalized mRNA oncology workflows. Inspired by the 2026 Rosie mast cell tumor case. Species-aware, safety-first, requires veterinary oncologist oversight.
---

# Personalized mRNA Oncology Workflow

## Overview

Structured reasoning template for guiding AI-assisted analysis and planning in cases of advanced or refractory neoplasia where personalized mRNA-based approaches are under consideration. Inspired by the 2026 Rosie mast cell tumor case (canine), the first documented bespoke mRNA cancer vaccine designed with significant AI assistance.

**Core purpose**: Provide species-aware, evidence-prioritized steps to evaluate feasibility, required data, key AI/researcher touchpoints, and critical safety/red-flag checkpoints. **Never** a substitute for board-certified veterinary oncologist + regulatory oversight.

## When to Use

- Advanced, chemotherapy-refractory, or metastatic neoplasia in dogs (or cautiously cats)
- Owner/researcher inquiring about personalized immunotherapy, neoantigen vaccines, or mRNA constructs
- Tumor sequencing (WES/RNA-seq) already performed or planned
- Desire to explore AI-augmented neoantigen prediction / vaccine blueprinting
- Keywords: mRNA, personalized oncology, neoantigen, cancer vaccine, immunotherapy, tumor sequencing, AlphaFold, precision medicine, Rosie
- NOT for: routine lymphoma protocols, first-line therapy planning, or any non-oncology case

## Key Capabilities & Data Sources

- Species-specific mast cell tumor biology (c-KIT mutations dominant in many canine MCTs)
- Neoantigen identification principles (mutated peptides, MHC binding, immunogenicity)
- AI tools historically used in breakthrough cases:
  - ChatGPT / Claude / Gemini: initial strategy brainstorming, literature synthesis, pipeline planning
  - AlphaFold (DeepMind): 3D protein structure prediction for mutated targets (e.g., c-KIT variants)
  - Grok / custom ML: final construct refinement, epitope selection
- Authoritative veterinary sources (prioritized):
  1. Ettinger's Textbook of Veterinary Internal Medicine (oncology chapters)
  2. Withrow & MacEwen's Small Animal Clinical Oncology
  3. Plumb's Veterinary Drug Handbook (immunotherapies)
  4. Veterinary Cancer Society guidelines
  5. PubMed-indexed case reports (including 2026 Rosie publication if available)
- External partnerships required: Genomics lab (e.g., university sequencing core), RNA synthesis/nanoparticle experts

## Workflow

1. **Confirm species, signalment, and diagnosis.**
   Mandatory: dog or cat? Breed? Age? Histopathology-confirmed neoplasia type? Stage? Prior therapies and response?

2. **Assess eligibility and red flags** (halt if any present).
   - No confirmed malignancy: stop.
   - Species not dog/cat: high caution (no documented veterinary mRNA cases outside canine).
   - No tumor/normal tissue sequencing available or planned: stop (WES/WGS + RNA-seq minimum).
   - Owner expecting DIY execution: immediate redirect to licensed veterinarian + IRB/ethics review.
   - Regulatory barriers (e.g., off-label mRNA use without compassionate exemption): flag heavily.

3. **Gather and summarize genomic data** (if provided).
   - Tumor vs normal variants (SNVs, indels).
   - Driver mutations (e.g., c-KIT exon 11 in canine MCT).
   - Tumor mutational burden (TMB) estimation.
   - HLA/MHC haplotype if available (canine DLA).

4. **Neoantigen candidate identification.**
   - Prioritize high-confidence somatic mutations that are expressed (RNA evidence) and show predicted MHC binding (tools like NetMHCpan adapted for canine).
   - Model protein impact with structure prediction (reference AlphaFold-style reasoning).
   - Rank by immunogenicity potential (avoid self-antigens).

5. **Vaccine construct brainstorming** (AI-assisted, not generative).
   - Suggest multi-epitope mRNA design principles (e.g., 10-20 neoantigens + linker/GMP motifs).
   - Reference historical tools: ChatGPT for pipeline ideation, AlphaFold for structural validation, Grok for final sequence optimization.
   - Output: high-level blueprint summary only (NOT nucleotide sequence generation).

6. **Safety and feasibility checkpoints.**
   - Cross-check species contraindications (e.g., feline mRNA immunogenicity unknown).
   - Flag cytokine release syndrome, anaphylaxis, autoimmunity risks.
   - Require collaboration: veterinary oncologist + RNA/nanomedicine specialist (e.g., university institute).

7. **Final hand-off recommendation.**
   Summarize for veterinarian/researcher: next steps, required partners, ethical/regulatory notes.

## Output Format

```
# Personalized mRNA Oncology Workflow Assessment

**Patient**: [Species/Breed/Age/Sex/Name]
**Diagnosis**: [Tumor type, grade, stage]
**Prior Treatments**: [List + response]

## Feasibility Summary
- Sequencing performed? [Yes/No/Details]
- Eligible for personalized approach? [Yes / Conditional / No]
- Primary red flags: [Bullet list or "None detected"]

## Key Genomic Insights
- Driver mutations: [e.g., c-KIT exon 11 duplication]
- Estimated neoantigen load: [High/Medium/Low]
- Top predicted targets: [3-5 mutated proteins/genes]

## Suggested Next Steps
1. [e.g., Obtain full WES + RNA-seq if not done]
2. [e.g., Consult veterinary oncologist specializing in immunotherapy]
3. [e.g., Partner with genomics/RNA synthesis facility (university preferred)]
4. [e.g., Use AI tools (ChatGPT/AlphaFold/Grok) under supervision for neoantigen prioritization]

## Critical Disclaimer & References
This is an experimental reasoning framework inspired by the 2026 Rosie mast cell tumor case (canine, UNSW RNA Institute, Prof. Thordarson collaboration).
NOT APPROVED THERAPY. All steps require direct supervision by a licensed veterinarian and compliance with local regulations (e.g., compassionate use, ethics approval).
Primary sources: Ettinger's Veterinary Internal Medicine, Withrow & MacEwen's Oncology, 2026 Rosie case reports.
```

## Limitations

- Experimental / one-off case precedent only (Rosie 2026, mast cell tumor, canine).
- No peer-reviewed veterinary mRNA vaccine protocols exist yet.
- AI tools (ChatGPT, AlphaFold, Grok) assist ideation/analysis. They do NOT replace professional genomicists or oncologists.
- High risk of immune-related adverse events, inefficacy, regulatory violation.
- Cost: sequencing + synthesis often >$10,000-50,000; not covered by insurance.
- Strongly contraindicated without specialist involvement.
- If any user prompt suggests self-administration or bypassing veterinary oversight, respond ONLY with: "This workflow requires mandatory supervision by a licensed veterinarian and institutional oversight. Redirecting to emergency veterinary contact / poison control if urgent."
