---
name: obo-foundry-ontologies
description: Access OBO Foundry biomedical ontologies relevant to veterinary medicine including VBO (breeds), UBERON (anatomy), HP/MP (phenotypes), ChEBI (chemicals), and NCBITaxon (species taxonomy).
---

# OBO Foundry Ontologies

## Overview

OBO (Open Biomedical Ontologies) Foundry is a collaborative effort to develop standardized, shared biomedical ontologies that enable structured reasoning across species, phenotypes, anatomical features, and chemicals. For veterinary AI, OBO ontologies provide formal semantic frameworks for breed classification, anatomical mapping, inherited disease phenotypes, and cross-species gene annotation.

## When to Use

- User structures veterinary data with standardized ontology terms (breed IDs, phenotype codes, anatomical structures)
- User needs to perform SPARQL queries across linked veterinary datasets
- User maps canine genetic variants to human orthologous genes
- User enables cross-species disease reasoning (canine cancer → human cancer translational mapping)
- Keywords: OBO Foundry, ontology, VBO, UBERON, HP/MP, ChEBI, NCBITaxon, semantic reasoning, SPARQL

## Key Veterinary Ontologies

**Vertebrate Breed Ontology (VBO):**
- **Coverage:** 49 species, 19,500+ breed concepts
- **Structure:** Species → Breed Group (FCI classification) → Individual Breed
- **Example IDs:** VBO_0000147 = "Labrador Retriever" (canine), VBO_0000456 = "Holstein" (bovine)
- **Use Case:** Link breed-specific health predispositions (MDR1 mutation in collies) to phenotype databases
- **File Format:** OWL/RDF; queryable via OBO ontology repositories

**UBERON (Uber-Anatomy Ontology):**
- **Coverage:** Multi-species anatomy (vertebrate + invertebrate structures)
- **Example IDs:** UBERON_0000080 = "bone", UBERON_0001068 = "heart", UBERON_0001555 = "kidney"
- **Alignment:** Cross-species anatomical homologies (dog kidney ≈ human kidney = UBERON_0001555)
- **Use Case:** Standardize surgical/pathology reports across species; enable cross-species organ toxicity mapping
- **Benefit:** Same anatomy code for veterinary + human medicine (precision medicine drug trials)

**HP/MP (Human/Mammalian Phenotype Ontologies):**
- **HP (Human Phenotype):** Standardized terms for human disease manifestations
  - Example: HP_0007565 = "Hepatomegaly" (liver enlargement)
- **MP (Mammalian Phenotype):** Veterinary/model organism phenotypes
  - Example: MP_0001559 = "abnormal kidney development" (applicable to mice, dogs, cats)
- **Alignment:** HP and MP are cross-mapped; same phenotype in human and animal has consistent code
- **Use Case:** Link veterinary clinical signs to inherited disease databases (OMIA/OMIM)

**ChEBI (Chemical Entities of Biological Interest):**
- **Coverage:** Small-molecule drugs, metabolites, ions, organic compounds
- **Example IDs:** CHEBI_2676 = "amoxicillin", CHEBI_31532 = "omeprazole"
- **Alignment:** Veterinary pharmacology integrated with human pharmacology (same drug = same CHEBI ID)
- **Use Case:** Standardize drug representations in adverse event databases, pharmacogenomics annotations

**NCBITaxon (NCBI Taxonomy Ontology):**
- **Coverage:** All living organisms (bacteria, fungi, plants, animals)
- **Example IDs:** NCBITaxon_9615 = "dog", NCBITaxon_9685 = "cat", NCBITaxon_9796 = "horse"
- **Alignment:** Links species taxonomy to genomic databases (GenBank, RefSeq) and phenotype databases
- **Use Case:** Resolve species synonyms (Canis lupus familiaris = dog = NCBITaxon_9615); enable genomic data retrieval

## Ontology Structure & Semantic Relationships

**Hierarchical Relationships:**
```
VBO hierarchy example:
VBO_0000001 (Dog)
  ├── VBO_0000048 (Herding Group)
  │   ├── VBO_0000147 (Labrador Retriever)
  │   ├── VBO_0000456 (Collie)
  │   └── VBO_0000789 (German Shepherd)
  └── VBO_0000049 (Sporting Group)
      ├── VBO_0000234 (Golden Retriever)
      └── ...

UBERON hierarchy example:
UBERON_0011005 (Organ)
  ├── UBERON_0001068 (Heart)
  │   ├── UBERON_0001076 (Left Ventricle)
  │   └── UBERON_0001078 (Right Atrium)
  └── UBERON_0001555 (Kidney)
      ├── UBERON_0001557 (Renal Cortex)
      └── UBERON_0001558 (Renal Medulla)
```

**Semantic Relationships (Beyond is-a):**
- `part_of`: "Left ventricle" part_of "Heart"
- `has_part`: "Heart" has_part "Left ventricle"
- `located_in`: "Kidney" located_in "Abdomen"
- `develops_from`: "Adult kidney" develops_from "Ureteric bud"
- `orthologous_to`: "Dog liver" orthologous_to "Human liver" (same UBERON term)

## SPARQL Querying for Veterinary Data

**SPARQL Basics:** Structured query language for linked semantic data (RDF graphs).

**Example 1: Find All Herding Dog Breeds**
```sparql
PREFIX vbo: <http://purl.obolibrary.org/obo/VBO_>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?breed ?breedLabel
WHERE {
  ?breed rdfs:subClassOf vbo:0000048 .  # 0000048 = Herding Group
  ?breed rdfs:label ?breedLabel .
}
```
Returns: VBO codes for Collie, Sheltie, Australian Shepherd, German Shepherd, etc.

**Example 2: Cross-Species Organ Mapping (Kidney Toxicity)**
```sparql
PREFIX uberon: <http://purl.obolibrary.org/obo/UBERON_>

SELECT ?species ?organ
WHERE {
  ?organ rdfs:subClassOf uberon:0001555 .  # 0001555 = Kidney
  ?organ rdfs:label ?organLabel .
}
```
Returns: Dog kidney = Human kidney = Cat kidney (all UBERON_0001555, enabling cross-species toxicity lookup)

**Example 3: Link Breed to Genetic Disorder (MDR1 + Collies)**
```sparql
PREFIX vbo: <http://purl.obolibrary.org/obo/VBO_>
PREFIX omia: <http://omia.org/>

SELECT ?breed ?disorder
WHERE {
  ?breed rdfs:subClassOf vbo:0000048 .  # Herding Group
  ?breed <http://predisposes_to> ?disorder .
  ?disorder rdfs:label "Multidrug Resistance 1" .
}
```
Returns: Collie, Sheltie, Australian Shepherd + MDR1 mutation link

## Veterinary Use Cases

**1. Precision Medicine Drug Trials:**
- Use UBERON to standardize organ toxicity endpoints across canine/feline/human studies
- Link anatomical lesions (hepatic necrosis = UBERON lesion) to severity grading
- Example: "Liver toxicity (UBERON_0002107 lesion) observed in canine trial; cross-map to human hepatotoxicity (HP_0008279) for translational relevance"

**2. Breed Predisposition Reasoning:**
- Query VBO to identify herding breeds (Collies, Aussies, Shelties)
- Cross-reference with OMIA database for MDR1 mutation prevalence
- Automated alert: "Ivermectin contraindicated in patient breed due to MDR1 risk"

**3. Cross-Species Genomics:**
- Use NCBITaxon to link canine/feline/equine species to GenBank orthologous genes
- Map canine gene (dog BRCA2 = feline BRCA2 = NCBITaxon alignment)
- Enable translational studies: "BRCA2 mutations in dogs → predict human breast cancer risk"

**4. Anatomical Standardization in EHR:**
- Use UBERON codes for surgical/histopathology reports
- Example: Spay report uses UBERON_0003714 (uterus) instead of free text
- Benefits: Automated adverse event detection, standardized coding across practices

**5. Phenotype-to-Disease Mapping:**
- Veterinarian notes: "Hepatomegaly, jaundice, weight loss" in a 5-year-old Shih Tzu
- Query MP/HP ontologies: MP_0001559 (abnormal liver development) → search OMIA for inherited liver diseases in Shih Tzus
- Automated differential: Polycystic kidney disease, amyloidosis, etc.

## Accessing OBO Ontologies

**Public Repositories:**
- **OBO Foundry:** https://www.obofoundry.org/ (download OWL/OBO files)
- **EMBL-EBI OLS (Ontology Lookup Service):** https://www.ebi.ac.uk/ols (interactive browser)
- **BioPortal:** https://bioportal.bioontology.org (multi-ontology search)

**File Formats:**
- **OWL (Web Ontology Language):** XML-based; semantically rich; widely used
- **RDF/Turtle:** Human-readable linked data format
- **OBO Format:** Legacy text-based format; still supported

**Python Integration:**
```python
# Using pronto library to load OBO ontologies
import pronto

# Load VBO
vbo = pronto.Ontology("http://purl.obolibrary.org/obo/vbo.owl")

# Query breed by ID
collie = vbo["VBO:0000456"]
print(f"Breed: {collie.name}")

# Find parent classes (breed group)
for parent in collie.superclasses():
    print(f"Group: {parent.name}")

# Load UBERON
uberon = pronto.Ontology("http://purl.obolibrary.org/obo/uberon.owl")
kidney = uberon["UBERON:0001555"]
print(f"Anatomy: {kidney.name}, Definition: {kidney.definition}")
```

## Ontology Standards & Governance

- **Coordination:** OBO Foundry editorial board ensures consistency across ontologies
- **Licensing:** Mostly CC-BY 4.0 or similar permissive licenses
- **Version Control:** Regular updates (quarterly to annually); version tracking
- **Cross-Mapping:** OBO ontologies are intentionally aligned (HP-MP, VBO-NCBITaxon) to enable cross-dataset queries
- **Community Contribution:** Open curation; veterinary community can propose additions

## Limitations

- **Completeness:** Not all veterinary breeds, anatomical variants, or rare diseases are comprehensively coded
- **Veterinary Specificity:** VBO is rich; others (HP/MP) are more human-biased; veterinary phenotypes may need custom extensions
- **Adoption:** Veterinary EHRs often use free-text or proprietary codes; full ontology integration requires software implementation
- **Curation Burden:** Maintaining ontologies requires ongoing community effort; emerging diseases may lack codes initially
- **Interoperability:** Integration with legacy veterinary systems (non-RDF) requires data mapping layers

## Sources

- **OBO Foundry:** https://www.obofoundry.org
- **VBO (Vertebrate Breed Ontology):** https://github.com/vbreeds/vbo
- **UBERON:** https://uberon.github.io
- **HP/MP:** https://hpo.jax.org (Human Phenotype Ontology includes MP alignment)
- **ChEBI:** https://www.ebi.ac.uk/chebi
- **NCBITaxon:** https://www.ncbi.nlm.nih.gov/taxonomy
- **EMBL-EBI OLS:** https://www.ebi.ac.uk/ols
- **Pronto (Python library):** https://github.com/althonos/pronto

## Advanced Integration

VetClaw SDK may provide convenience wrappers around SPARQL queries and ontology traversal. Consult `/sessions/charming-practical-mayer/mnt/OpenVet/vetclaw/vetclaw/sdk/` for Python/TypeScript ontology client examples.
