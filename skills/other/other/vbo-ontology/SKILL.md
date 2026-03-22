---
name: vbo-ontology
description: Access the Vertebrate Breed Ontology (VBO) for standardized breed nomenclature across 49 species with 19,500+ breed concepts. Use for breed identification, cross-referencing, and taxonomic standardization.
---

# Vertebrate Breed Ontology (VBO)

## Overview

The Vertebrate Breed Ontology (VBO) is a standardized, structured taxonomy of animal breeds and varieties across 49 domesticated and semi-domesticated species. Developed and maintained by the VBO consortium (veterinary geneticists, bioinformaticians, breed club representatives), VBO enables consistent breed naming, automated breed-predisposition reasoning, and integration with genetic disease databases (OMIA, VetClaw). With 19,500+ breed concepts and hierarchical classification, VBO powers precision veterinary medicine.

## When to Use

- User identifies patient breed and needs standardized breed nomenclature for records/research
- User queries breed-specific health predispositions (MDR1 in herding breeds)
- User resolves breed name ambiguities (e.g., "English Springer Spaniel" vs. "Springer Spaniel" variant)
- User performs cross-species breed classification (dog breed groups, horse registry standards)
- User links breed-specific genetic test recommendations to patient phenotype
- Keywords: VBO, breed ontology, breed identification, breed predisposition, standardized nomenclature, FCI

## What is VBO?

**Definition:** Formal ontology structured as directed acyclic graph (DAG) where:
- Nodes = breed concepts (unique IDs)
- Edges = hierarchical relationships (is-a, part-of)
- Metadata = breed names (preferred + synonyms), species, FCI classification (for dogs/cats), breed clubs

**Coverage (by Species):**
- **Companion Animals:** Canis familiaris (dog) - 900+ breeds; Felis catus (cat) - 250+ breeds; Rabbit (200+), Guinea pig (50+)
- **Livestock:** Cattle (300+), Horse (350+), Sheep (500+), Goat (200+), Swine (100+), Poultry (200+)
- **Exotic Species:** Fish (200+), Rodents, Amphibians, Reptiles

**Total:** 19,500+ breed concepts across 49 species

## VBO Hierarchical Structure

**Dog (Canis familiaris) Example:**

```
VBO_DOG_ROOT (Dog - all breeds)
├── VBO_GROUP_1 (FCI Group 1: Sheepdogs & Cattle Dogs)
│   ├── VBO_COLLIE (Rough Collie)
│   ├── VBO_COLLIE_SMOOTH (Smooth Collie)
│   ├── VBO_AUSTRALIAN_SHEPHERD (Australian Shepherd)
│   ├── VBO_GERMAN_SHEPHERD (German Shepherd Dog)
│   └── ... (50+ herding breeds)
├── VBO_GROUP_2 (FCI Group 2: Pinschers, Schnauzers, Molossians)
│   ├── VBO_BOXER (Boxer)
│   ├── VBO_DOBERMAN (Doberman Pinscher)
│   └── ... (20+ molossoid breeds)
├── VBO_GROUP_3 (FCI Group 3: Terriers)
│   ├── VBO_SMOOTH_FOX_TERRIER (Smooth Fox Terrier)
│   └── ... (30+ terrier breeds)
├── VBO_GROUP_8 (FCI Group 8: Retrievers, Flushing Dogs)
│   ├── VBO_LABRADOR (Labrador Retriever)
│   ├── VBO_GOLDEN (Golden Retriever)
│   └── ... (30+ gun dogs)
└── ... (8 total FCI groups + miscellaneous/non-FCI breeds)
```

**Cattle (Bos taurus) Example:**

```
VBO_CATTLE_ROOT
├── VBO_DAIRY (Dairy Breeds)
│   ├── VBO_HOLSTEIN (Holstein-Friesian)
│   ├── VBO_JERSEY (Jersey)
│   ├── VBO_GUERNSEY (Guernsey)
│   └── VBO_BROWN_SWISS (Brown Swiss)
├── VBO_BEEF (Beef Breeds)
│   ├── VBO_ANGUS (Angus)
│   ├── VBO_HEREFORD (Hereford)
│   ├── VBO_CHAROLAIS (Charolais)
│   └── ...
└── VBO_DUAL_PURPOSE (Dairy/Beef Breeds)
    ├── VBO_SIMMENTAL (Simmental)
    └── ...
```

## VBO Breed ID Format

**Standard Format:** `VBO_XXXXXX` (6-character code or full name reference)

**Examples:**
- VBO_0000147 = Labrador Retriever (canine)
- VBO_0000456 = Collie (canine)
- VBO_0000123 = Siamese (feline)
- VBO_0001000 = Holstein (bovine)
- VBO_0002156 = Thoroughbred (equine)

**Nomenclature Standards:**
- Preferred name = FCI standard (for FCI-recognized breeds)
- Synonyms = regional variants, historical names, abbreviated forms
- Example: "Rough Collie" (preferred) ≈ "Lassie type" (historical) ≈ "Collie long-coat" (variant)

## Accessing VBO

**Web Interface (OBO Foundry/BioPortal):**
https://www.ebi.ac.uk/ols/ontologies/vbo (EMBL-EBI OLS - Ontology Lookup Service)

**Search Functions:**
1. **Breed by Name:** Enter "Labrador" → Returns VBO_0000147 + linked data
2. **Breed by FCI Code:** Enter "8.1" (FCI retriever code) → Lists all retrievers
3. **By Species:** Select "Canis familiaris" → Browse all dog breeds
4. **By Predisposition:** (Advanced) Query "MDR1 mutation" → Returns all affected breeds

**Download Formats:**
- OWL (Web Ontology Language): Full semantic structure, machine-readable
- OBO Format: Text-based, human-readable
- JSON: Programmatic access
- CSV: Breed list spreadsheets

**File Location:** https://github.com/vbreeds/vbo (open-source repository)

## VBO-OMIA Integration

**Power of Linking:**
VBO enables automated health predisposition reasoning by linking breed ID to inherited disease databases (OMIA).

**Example Query:**
```
Breed: VBO_0000456 (Collie)
→ Link to OMIA records for Collie predispositions
→ Results:
  - MDR1 mutation: 50-70% carriers
  - Collie Eye Anomaly: 15-25% carriers
  - Progressive Retinal Atrophy: Breed-specific loci
  - Microphthalmia: Rare
→ Veterinarian alert: "Collie breed: avoid ivermectin (MDR1); screen eyes (CERF)"
```

**Breeding Program Integration:**
```
1. Breeder registers breeding dogs: VBO ID + genetic test results (OMIA-linked)
2. System identifies mating risks:
   - Both parents carriers of PRA → 25% affected puppies
   - One parent MDR1 homozygous, other carrier → all puppies carriers
3. Recommendation: Avoid mating; counsel on genetic implications
```

## VBO Hierarchical Relationships

**Parent-Child Relationships:**
```
FCI Group 8 (Retrievers)
  ├── Labrador Retriever (VBO_0000147)
  │   ├── Black Labrador (phenotypic variant)
  │   ├── Yellow Labrador (phenotypic variant)
  │   └── Chocolate Labrador (phenotypic variant)
  └── Golden Retriever (VBO_0000234)
```

**Breed Variants (Size/Coat):**
Some breeds have recognized size/coat variants (not separate breed in FCI, but distinct lines):
- **Standard Poodle** vs. **Miniature Poodle** vs. **Toy Poodle**
  - VBO distinguishes size variants with separate IDs
  - Different health predispositions (patella luxation more common in toy sizes)
- **Rough Collie** vs. **Smooth Collie**
  - Both VBO IDs, same genetic predispositions (MDR1)
  - Phenotypic difference (coat length) only

## Breed Predisposition Reasoning

**Automated Workflow (VetClaw AI):**
```
1. Patient Information Input:
   - Species: Canis familiaris
   - Breed: "Rough Collie"
   - Age: 8 months
   - Gender: Female

2. VBO Lookup:
   - Resolves "Rough Collie" → VBO_0000456
   - Identifies parent FCI group: Group 1 (Herding Dogs)

3. OMIA Predisposition Query:
   - Search OMIA: "VBO_0000456" + inherited diseases
   - Returns: MDR1, Collie Eye Anomaly, PRA, etc.

4. Genetic Test Recommendations:
   - MDR1: Recommended (drug interaction implications)
   - Eye exam: CERF certification (Collie Eye Anomaly screening)
   - PRA testing: Candidate gene panel

5. Clinical Alert Generation:
   - "Breed predisposition: Avoid ivermectin + analogs"
   - "Recommend ophthalmology exam before breeding"

6. Treatment Plan Modification:
   - Alternative antiparasitic: Spinosad (not MDR1-substrate)
   - Genetic counseling: If breeding planned
```

## Cross-Species Breed Standardization

**Problem:** Same breed name across species with different meanings
- "Angora": Could be Angora rabbit, Angora goat, or Angora cat
- VBO resolves with species prefix: VBO_ANGORA_RABBIT vs. VBO_ANGORA_GOAT

**International Breed Name Variation:**
- "English Springer Spaniel" (FCI) vs. "English Springer Spaniel" (AKC) vs. "Springer Spaniel" (colloquial)
- VBO preferred: FCI standard; synonyms capture variants

**Horse Registry Integration:**
- Thoroughbred (Equestrian registry: Jockey Club)
- Quarter Horse (AQHA registration)
- VBO links both to equine taxonomy, but maintains registry distinctions

## VBO Querying Examples

**Example 1: Find All Large-Breed Dogs (Hip Dysplasia Risk)**
```
SPARQL Query:
SELECT ?breed ?breedLabel
WHERE {
  ?breed rdfs:subClassOf vbo:GROUP_8 .  # Retrievers, gun dogs
  ?breed rdfs:label ?breedLabel .
}
Returns: Labrador, Golden Retriever, etc. (all large breeds)
Filter by predisposition: High hip dysplasia prevalence
```

**Example 2: Identify All Cat Breeds with PKD1 Risk**
```
Query: "Felis catus" + "PKD1" + inheritance:autosomal_dominant
Returns: Persian, Maine Coon, Bengal, British Shorthair, etc.
Link to OMIA: PKD1 prevalence per breed
Breeding recommendation: Screen parents (ultrasound kidney assessment)
```

**Example 3: Breed Equivalence Across Registries**
```
Query: VBO_LABRADOR (FCI) + AKC equivalent
Returns: Labrador Retriever (AKC) = Labrador (FCI) = same breed
Use for breed-predisposition research (align datasets from different registries)
```

## VBO-Based Breed Identification Workflow

**Ambiguous Case: User Says "Spaniel"**

```
1. VBO Query: "Spaniel" (search for partial name match)
2. Returns multiple breeds:
   - English Springer Spaniel (VBO_0000XXX)
   - Cocker Spaniel (VBO_0000YYY)
   - Cavalier King Charles Spaniel (VBO_0000ZZZ)
   - American Spaniel Variety (multiple lines)

3. Veterinarian Clarifies:
   - "Which spaniel breed exactly?"
   - Obtain FCI classification or show pedigree

4. Once Breed Confirmed:
   - VBO ID assigned (e.g., VBO_0000XXX = English Springer Spaniel)
   - Health predispositions retrieved
   - Genetic testing recommendations automated

5. Medical Record:
   - Store VBO ID (standardized across clinics/research)
   - Enable data sharing, breeding program tracking
```

## Limitations

- **Non-FCI Breeds:** Many regional/emerging breeds lack VBO classification
- **Mixed-Breed Animals:** VBO applies to purebreds; hybrids/mongrels not classified
- **Breed Validity:** FCI recognition varies; some "breeds" are phenotypic variants, not genetically distinct
- **Phenotypic vs. Genetic:** VBO emphasizes FCI breed standards (phenotype) rather than genetic similarity (genotype)
  - Example: English Springer Spaniel vs. Cocker Spaniel are distinct FCI breeds but genetically closely related
- **Updating Lag:** New breeds recognized by breed clubs; VBO updates lag (6-12 months typical)
- **Species Bias:** Dog, cat, horse breeds well-represented; exotic species sparse

## Sources

- **VBO GitHub:** https://github.com/vbreeds/vbo
- **OBO Foundry:** https://www.obofoundry.org/ontology/vbo
- **EMBL-EBI OLS:** https://www.ebi.ac.uk/ols/ontologies/vbo
- **FCI (Fédération Cynologique Internationale):** https://www.fci.be (dog breed standards)
- **TICA (The International Cat Association):** https://www.tica.org (cat breed standards)
- **Equine Breed Registries:** Various (Jockey Club, AQHA, etc.)
- **OMIA (Cross-Reference):** https://www.omia.org

## Advanced Integration

VetClaw SDK provides VBO breed lookups and OMIA predisposition queries integrated into clinical decision support. See `/sessions/charming-practical-mayer/mnt/OpenVet/vetclaw/vetclaw/sdk/` for Python/TypeScript breed ontology client examples.
