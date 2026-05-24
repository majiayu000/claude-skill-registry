---
name: omia-database
description: Query OMIA (Online Mendelian Inheritance in Animals) for inherited disorders and traits cataloged across species. The veterinary equivalent of OMIM. Use for genetic disease research and breed predisposition data.
---

# OMIA Database

## Overview

OMIA (Online Mendelian Inheritance in Animals) is a veterinary genetic disease database maintained by the University of Sydney. It catalogs inherited disorders, morphological traits, and genetic variants across 300+ animal species, with extensive data on companion animals (dogs, cats), livestock (cattle, horses, sheep), and model organisms. OMIA is the animal medicine equivalent of OMIM (Online Mendelian Inheritance in Man).

## When to Use

- User searches for inherited diseases in a specific breed or species (e.g., hip dysplasia in Golden Retrievers)
- User identifies genetic basis for clinical phenotype (mutation + gene + inheritance pattern)
- User researches breed predispositions for preventive medicine or breeding programs
- User maps veterinary genetic variants to human orthologous diseases (translational oncology)
- User looks up Mendelian inheritance patterns, carrier frequencies, diagnostic tests
- Keywords: OMIA, inherited disease, genetic, Mendelian, breed predisposition, mutation, gene, carrier, MDR1

## What is OMIA?

**Database Contents:**
- 6,000+ inherited disorders and traits across 300+ species
- 15,000+ genetic loci/genes documented
- Emphasis on companion animals (dogs, cats, rabbits) and livestock
- Cross-referenced with OMIM, GenBank, UniProt for translational research

**Regulatory Scope:**
- Non-profit, university-maintained (University of Sydney)
- Peer-reviewed disease/trait entries (veterinarians, geneticists)
- Continuously updated as new genetic discoveries published
- Free public access: https://www.omia.org

**Typical Entry Includes:**
- Disease/trait name and synonyms
- Affected species, breeds, ethnic groups
- Gene(s) involved and chromosomal location
- Mutation(s) identified
- Inheritance pattern (autosomal dominant/recessive, X-linked, multifactorial)
- Phenotype description
- Diagnostic test availability
- References (peer-reviewed publications)
- Frequency/prevalence in breed(s)

## Key Veterinary Conditions in OMIA

**Genetic Disease Examples (Canine):**

| Disease | Gene | Pattern | Breeds Affected | Notes |
|---------|------|---------|-----------------|-------|
| Multidrug Resistance 1 | MDR1 | Autosomal recessive | Collie, Sheltie, Aussie, etc. | Ivermectin sensitivity/neurotoxicity |
| von Willebrand Disease (Type I) | VWF | Autosomal dominant | Doberman Pinscher, many breeds | Bleeding disorder; carriers asymptomatic |
| Progressive Retinal Atrophy | PRA (multi-gene) | Autosomal recessive | Labrador, Irish Setter, Poodle | Blindness by age 1-5 |
| Hip Dysplasia | FN gene (complex) | Multifactorial | Golden Retriever, German Shepherd | Environmental + genetic factors |
| Polycystic Kidney Disease | PKD1 | Autosomal dominant | Persians, Burmese cats | Chronic renal failure |
| Hemophilia B | F9 | X-linked recessive | Various breeds | Clotting factor deficiency |
| Progressive Myoclonic Epilepsy | EPM2A | Autosomal recessive | Ungulate, some dogs | Seizures + progressive neurologic decline |
| Cerebellar Hypoplasia | (multiple genes) | Varies | Collies, Irish Setters | Ataxia from birth |

**Genetic Disease Examples (Feline):**

| Disease | Gene | Pattern | Breeds Affected | Notes |
|---------|------|---------|-----------------|-------|
| Polycystic Kidney Disease | PKD1 | Autosomal dominant | Persians, Maine Coons, others | Most common inherited feline disease |
| Hypertrophic Cardiomyopathy | MYBPC3, MRPL3 | Autosomal dominant | Maine Coons, Bengals, others | Sudden cardiac death |
| Glycogen Storage Disease IV | GBE1 | Autosomal recessive | Norwegian Forest Cats | Lethal liver disease in kittens |
| Spinal Muscular Atrophy | SMN1 | Autosomal recessive | Maine Coons | Neuromuscular degeneration |

**Livestock Examples:**

| Disease | Gene | Species | Pattern | Notes |
|---------|------|---------|---------|-------|
| Bovine Leukocyte Adhesion Deficiency | ITGB2 | Cattle | Autosomal recessive | Immunodeficiency; affects several breeds |
| Polled/Horned | POLL/HORNED | Cattle | Autosomal dominant | Breeding selection |
| Lavender Foal Syndrome | MFSD11 | Horse | Autosomal recessive | Neurologic disease; often lethal |
| Ovine Fetal Encephalomyopathy | PFKM | Sheep | Autosomal recessive | Stillbirths/congenital neurologic |

## Accessing OMIA

**Web Interface:**
https://www.omia.org

**Search Functions:**

1. **By Disease Name:**
   - Enter "hip dysplasia" → Returns all species with HipDys, filter by breed
   - Enter "von Willebrand" → Returns type 1, 2, 3 (multiple loci)

2. **By Breed:**
   - Select "Labrador Retriever" → Lists all documented inherited disorders in breed
   - Shows genetic basis, carrier testing availability, prevalence

3. **By Gene:**
   - Enter "MDR1" → Shows all species/breeds affected by MDR1 variants
   - Returns all conditions linked to that gene (drug sensitivities, etc.)

4. **By Chromosome Location:**
   - Search "canine chromosome 5" → Lists all genes/disorders mapped to that chromosome

5. **By Species:**
   - Select "Felis catus" → Display all inherited diseases in cats
   - Comprehensive list with prevalence in common breeds

## OMIA Entry Structure

**Typical OMIA Record Includes:**

```
Title: Hip Dysplasia, Canine
Synonym: Canine Hip Dysplasia (CHD), Hip Dysplasia in Dogs

Affected Species: Canis familiaris

Genes:
  FN (Fibronectin): Complex/multifactorial
  Evidence: GWAS studies, candidate gene association

Inheritance: Multifactorial (polygenic + environmental)
  - Autosomal inheritance
  - Influenced by body size, growth rate, exercise
  - Penetrance variable

Phenotype:
  - Clinical: Hind limb lameness, pain, degenerative joint disease
  - Radiographic: Femoral head subluxation, shallow acetabulum
  - Age of onset: 6 months to 5+ years

Breed Predispositions:
  - Higher risk: German Shepherd, Golden Retriever, Labrador
  - Lower risk: Greyhound, Dachshund, small toy breeds
  - Prevalence: 5-10% in high-risk breeds (radiographic screening)

Diagnostic Tests:
  - Radiographic assessment (PennHIP, Orthopaedic Foundation for Animals)
  - Genetic testing: Not available (complex trait)
  - Parentage verification: Recommended for breeding programs

Prevention:
  - Selective breeding (screen parents radiographically)
  - Weight management
  - Exercise moderation in juvenile period
  - Environmental factors

References:
  - 15-30 peer-reviewed publications
  - Links to PubMed, GenBank accessions
```

## Inheritance Pattern Descriptions

**Autosomal Dominant:**
- One mutant allele sufficient for phenotype
- Affected individual has ≥50% affected offspring (if heterozygous)
- Example: von Willebrand Disease type 1 (variability in expression)
- Carriers: Usually symptomatic (unless variably penetrant)

**Autosomal Recessive:**
- Two mutant alleles required for phenotype
- Affected individual: homozygous (aa)
- Carriers: heterozygous (Aa) - unaffected but can transmit
- Affected offspring from two carriers: 25% (a/a), 50% carriers (A/a), 25% normal (A/A)
- Example: MDR1 mutation in collies; colorblindness

**X-Linked Recessive:**
- Mutation on X chromosome
- Males (XaY) affected; females (XAXa) carriers usually unaffected
- Female carriers can have 50% affected male offspring
- Example: Hemophilia B (F9 gene)

**Multifactorial (Complex Trait):**
- Multiple genes + environmental factors
- No simple Mendelian inheritance
- Siblings of affected animal have increased but not predictable risk
- Example: Hip dysplasia, elbow dysplasia, most cancer predispositions
- Polygenic risk scores being developed

**Mitochondrial:**
- Rare; inheritance through maternal cytoplasm
- All offspring of affected mother likely affected
- Father never transmits
- Example: Some neurologic conditions

## Breed Predisposition Analysis

**OMIA Approach:**
1. Select breed (e.g., Collie)
2. OMIA lists all documented genetic diseases
3. Prevalence/carrier frequency provided if known
4. Genetic basis explained

**Collie Breed Example (Partial List):**
- MDR1 mutation: ~50-70% carriers; 5-10% homozygous affected (varies by region)
- Collie Eye Anomaly: Autosomal recessive; ~15-25% carriers
- Microphthalmia: Rare; autosomal recessive
- Smooth/Rough coat: Autosomal dominant (phenotypic, not disease)

**Breeding Program Integration:**
- Veterinarians counsel clients on inherited disease risks
- Recommend genetic testing before breeding
- OMIA provides test recommendations (OFA, Orthopedic Foundation for Animals)
- Breeding decisions: avoid mating two carriers of recessive disease

## Diagnostic Test Information

**OMIA Lists:**
- Where testing is available (genetic testing labs, universities, breed clubs)
- Test method (DNA sequencing, SNP panel, enzyme assay)
- Cost range (typically $50-300)
- Turnaround time (7-14 days typical)
- Interpretation (affected, carrier, clear)

**Example: MDR1 Testing**
- Gene: MDR1 (P-glycoprotein)
- Test Method: DNA PCR, mutation-specific assay
- Labs: VetGen, UC Davis, Mars Petcare
- Cost: ~$75-150
- Result: Wild-type/normal, heterozygous/carrier, homozygous/affected
- Clinical Use: Guide ivermectin/avermectin dosing or avoidance

## Cross-Reference with OMIM (Human Diseases)

**Translational Value:**
OMIA links veterinary genetic diseases to human orthologous conditions via OMIM IDs.

**Example: Canine Hemophilia B → Human Hemophilia B**
- Canine: F9 gene mutation, X-linked; bleeding disorder
- Human: Same F9 gene mutation; hemophilia B/Christmas disease
- Translational Research: Dogs with naturally occurring F9 mutations used in gene therapy trials for human hemophilia
- Phenotype Monitoring: Similar coagulation cascade, bone/joint hemorrhage complications

**Oncology Example: Canine Osteosarcoma**
- Canine genetic predispositions (SV40, TP53, BRCA1/BRCA2)
- Homologous to human osteosarcoma (same mutations associated)
- Translational: Canine tumors provide model for human pediatric osteosarcoma therapy

**Advantage:** Veterinary research informs human genomic medicine; human discoveries guide animal breeding/treatment.

## OMIA-Based Clinical Workflows

**Workflow 1: Preventive Genetic Screening**
```
1. Patient: 8-month-old Labrador Retriever
2. Breed enters OMIA → retrieve predispositions
3. High-risk conditions identified:
   - Hip dysplasia (multifactorial)
   - Elbow dysplasia (multifactorial)
   - Exercise-Induced Collapse (EIC, autosomal recessive)
   - Progressive Retinal Atrophy (PRA, multiple loci)
4. Veterinarian recommends:
   - Radiographic screening (hips/elbows at 2 years)
   - Genetic testing for EIC, PRA (DNA test $50-100 each)
   - Weight management + controlled exercise until skeletal maturity
5. Client counseling: If breeding planned, genetic tests required before mating
```

**Workflow 2: Unexplained Clinical Sign**
```
1. Patient: 3-year-old male Collie, seizures + progressive neurologic decline
2. Differential: Search OMIA for "Collie + neurologic"
3. OMIA findings:
   - Collie Eye Anomaly (autosomal recessive) → not neurologic
   - Ceroid Lipofuscinosis (NCL, autosomal recessive) → matches (neurologic, progressive)
   - Other: Epilepsy (genetic + idiopathic)
4. Diagnostic approach: Genetic test for NCL mutation (DNA test)
5. If positive: Genetic counseling, management strategy, breeding advice
```

**Workflow 3: Breed Club Genetic Health Program**
```
1. Breed club curator: Compile genetic disease prevalence in breed
2. Use OMIA to identify priority conditions (high prevalence, severity)
3. Establish testing recommendations (mandatory for breeding):
   - Eye examination (CERF - Canine Eye Registration Foundation)
   - Hip/elbow radiographs (OFA)
   - Genetic tests for recessive conditions (DNA labs)
4. Breeding registry: Track genetic test results, accumulate data
5. Long-term: Monitor frequency trends, inform breeding practices
```

## Limitations

- **Ascertainment Bias:** Documented disorders are often those affecting popular breeds; rare breed diseases underrepresented
- **Incomplete Penetrance:** Some dominant conditions show variable expression (carriers may be asymptomatic)
- **Variable Prevalence:** Frequency data may be outdated or based on limited studies
- **Multifactorial Diseases:** Hip dysplasia, cancer predispositions are difficult to model genetically; simple Mendelian predictions fail
- **Species Variation:** Small animal (dog/cat) data extensive; exotic/wildlife sparse
- **International Variation:** Prevalence data often US-centric; European breeding practices may differ

## Sources

- **OMIA Database:** https://www.omia.org
- **OMIA Advanced Search:** https://www.omia.org/search
- **OMIM (Human Diseases):** https://www.omim.org (cross-reference)
- **OFA (Orthopedic Foundation for Animals):** https://www.ofa.org (screening databases)
- **Canine Inherited Disorders Database:** https://www.cidc.iastate.edu/ (Iowa State)
- **Feline Genetics Laboratory:** UC Davis School of Veterinary Medicine
- **PubMed:** Cross-referenced from OMIA entries

## Advanced Integration

VetClaw SDK may provide OMIA query wrappers for automated breed risk stratification. Consult `/sessions/charming-practical-mayer/mnt/OpenVet/vetclaw/vetclaw/sdk/` for Python/TypeScript client examples integrating OMIA breed predisposition data.
