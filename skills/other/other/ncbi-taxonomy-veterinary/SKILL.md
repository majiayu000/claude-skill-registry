---
name: ncbi-taxonomy-veterinary
description: Query NCBI Taxonomy for veterinary species identification, taxonomic classification, and cross-referencing species names. Covers domestic, exotic, and wildlife species relevant to veterinary medicine.
---

# NCBI Taxonomy - Veterinary

## Overview

NCBI (National Center for Biotechnology Information) Taxonomy is a comprehensive database of organism classification and names. For veterinary medicine, NCBI Taxonomy provides standardized species identifiers (TaxIDs), hierarchical taxonomic relationships, and links to genomic databases (GenBank, RefSeq, SRA). This skill covers species lookup, TaxID resolution, and programmatic access via Entrez API.

## When to Use

- User looks up species classification, binomial name, or synonyms (e.g., "dog" → Canis lupus familiaris → TaxID 9615)
- User retrieves genomic data for a species (GenBank sequences, reference genomes)
- User performs phylogenetic analysis requiring standardized species nomenclature
- User links veterinary data to genomic research databases
- Keywords: NCBI, taxonomy, TaxID, binomial name, species classification, Entrez, GenBank, RefSeq, SRA

## Key Veterinary Species TaxIDs

| Common Name | Binomial Name | TaxID | Notes |
|------------|---------------|-------|-------|
| Dog | Canis lupus familiaris | 9615 | Primary veterinary species; ~30K+ genes sequenced |
| Cat | Felis catus | 9685 | Key veterinary species; complete reference genome |
| Horse | Equus caballus | 9796 | Equine medicine; draft/sport breeds |
| Cattle | Bos taurus | 9913 | Dairy/beef; major food animal |
| Sheep | Ovis aries | 9940 | Wool/meat; important research model |
| Swine | Sus scrofa domesticus | 9825 | Pork production; disease model |
| Chicken | Gallus gallus | 9031 | Poultry; avian medicine |
| Turkey | Meleagris gallopavo | 9103 | Poultry production |
| Rabbit | Oryctolagus cuniculus | 9986 | Research + pet; pharmaceuticals tested in rabbits |
| Guinea Pig | Cavia porcellus | 10141 | Research model; common exotic pet |
| Mouse | Mus musculus | 10090 | Reference mammalian genome; translational models |
| Rat | Rattus norvegicus | 10116 | Research toxicology model |
| Rhesus Macaque | Macaca mulatta | 9544 | Non-human primate; drug efficacy translational |
| Zebrafish | Danio rerio | 7955 | Aquaculture; vertebrate developmental model |
| Ferret | Mustela putorius furo | 9646 | Exotic pet; respiratory disease model |
| Hedgehog (African) | Atelerix albiventris | 9365 | Exotic pet medicine |

## NCBI Taxonomy Structure

**Hierarchical Classification:**
```
Kingdom: Animalia
  Phylum: Chordata
    Class: Mammalia
      Order: Carnivora
        Family: Canidae
          Genus: Canis
            Species: C. lupus
              Subspecies: C. l. familiaris (domestic dog)
                TaxID: 9615
```

**Taxonomic Ranks (from broadest to specific):**
- Superkingdom (Eukaryota, Bacteria, Archaea)
- Kingdom (Animalia, Plantae, Fungi)
- Phylum (Chordata, Arthropoda, Mollusca)
- Class (Mammalia, Aves, Reptilia, Amphibia)
- Order (Carnivora, Primates, Rodentia)
- Family (Canidae, Felidae, Equidae)
- Genus (Canis, Felis, Equus)
- Species (lupus, catus, caballus)
- Subspecies (familiaris for domestic dog)

## Querying NCBI Taxonomy

**Web Interface:**
https://www.ncbi.nlm.nih.gov/taxonomy

**Search Examples:**
1. Enter "dog" → Returns Canis lupus familiaris (TaxID 9615) + alternate names
2. Enter "9615" → Returns full taxonomy for domestic dog
3. Enter "feline" → Returns Felis catus, Felis silvestris, etc. (all feline species)
4. Enter "equine" → Returns horses, zebras, donkeys (family Equidae)

**Web Results Include:**
- Taxonomy browser (full hierarchy)
- Alternate names and synonyms
- Cross-references (GenBank accessions, RefSeq, SRA)
- Number of sequences available in GenBank
- Associated publications

## Entrez API Programmatic Access

**Entrez Query Syntax:**
Query NCBI databases including Taxonomy via REST/XML API.

**Base URL:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

**Example 1: Search for Species by Name**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?
  db=taxonomy&term="Canis lupus familiaris"&rettype=json

Response:
{
  "result": {
    "uid": ["9615"],
    "count": "1"
  }
}
```

**Example 2: Fetch Full Taxonomy Record for TaxID**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?
  db=taxonomy&id=9615&rettype=xml

Response: (XML with full taxonomy, rank, lineage, alternate names)
```

**Example 3: Search for All Dog Breeds (Canis lupus variants)**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?
  db=taxonomy&term="Canis lupus[orgn]"&retmax=100&rettype=json

Response: Returns TaxIDs for dog, wolf, dingo, and domestic dog variants
```

**Python SDK (Biopython):**
```python
from Bio import Entrez

# Set email (NCBI requires it)
Entrez.email = "veterinarian@clinic.com"

# Search for species
handle = Entrez.esearch(db="taxonomy", term="Canis lupus familiaris")
record = Entrez.read(handle)
taxid = record["IdList"][0]
print(f"TaxID for dog: {taxid}")

# Fetch full taxonomy record
handle = Entrez.efetch(db="taxonomy", id=taxid, rettype="xml")
taxonomy = Entrez.read(handle)
print(f"Lineage: {taxonomy[0]['Lineage']}")
print(f"Rank: {taxonomy[0]['Rank']}")

# Get all names/synonyms
names = taxonomy[0]["OrgName"]["OrgMod"] if "OrgMod" in taxonomy[0]["OrgName"] else []
for name_info in names:
    print(f"Synonym: {name_info['Subname']}")
```

## Linking Taxonomy to Genomic Data

**Genomic Database Cross-References:**

**GenBank:** DNA sequences submitted by researchers
- Link: Search GenBank with species TaxID
- Example: Filter by "Canis lupus familiaris [organism]" to retrieve all dog sequences
- Use Case: Find canine tumor suppressor sequences, drug targets

**RefSeq:** Reference sequence database (non-redundant, curated genomes)
- Link: "Genome" tab in NCBI Taxonomy page
- Current Dog Genome: CanFam3.1 (dog TaxID 9615)
- Example: Download dog reference genome FASTA, align patient tumor WGS to reference

**SRA (Sequence Read Archive):** Raw sequencing data (fastq, bam files)
- Link: Search by species + disease context
- Example: "Canis lupus familiaris [organism] AND osteosarcoma [disease]"
- Use Case: Download canine osteosarcoma raw RNA-seq data for analysis

**Entrez Gene:** Gene nomenclature and annotations
- Link: Cross-indexed from taxonomy records
- Example: Query gene symbol "TP53" [organism: Canis lupus familiaris]
- Returns: Dog TP53 gene ID, genomic location (chromosome 5), homology to human/mouse

**Workflow Example: Analyze Canine Cancer Gene Expression**
```
1. Start: Patient dog with melanoma
2. Query NCBI Taxonomy: TaxID 9615 (Canis lupus familiaris)
3. Link to RefSeq: Download CanFam3.1 reference genome
4. Find target gene: Query Entrez Gene for "BRAF" [organism: dog]
5. Retrieve sequences: GenBank FASTA for canine BRAF orthologs
6. Download expression data: SRA search "dog melanoma" → retrieve RNA-seq fastq
7. Align & analyze: Map dog tumor RNAseq to reference, quantify BRAF expression
8. Compare to human: Map dog BRAF to human BRAF (NCBI HomoloGene)
9. Translational insight: High BRAF expression in dog → informs human melanoma mechanism
```

## Species Synonyms & Nomenclature Issues

**Common Challenges:**
- "Dog" ≠ "Canis familiaris" (outdated subspecies classification)
- Modern classification: Canis lupus familiaris (dog is subspecies of gray wolf)
- NCBI Taxonomy lists all names: "domestic dog", "pet dog", "Canis familiaris" (synonym)
- Query flexibility: NCBI accepts any recognized name; returns standardized TaxID 9615

**Example: Resolving Nomenclature**
```
Query: "ferret" → NCBI returns multiple:
- Mustela putorius furo (domestic ferret) - TaxID 9646
- Mustela putorius (European polecat, wild ancestor)
- Mustela erminea (stoat, different species)

Veterinarian must verify: Are we discussing domesticated ferret (9646) or wild species?
```

**Taxonomy Updates:**
- NCBI Taxonomy is updated regularly as phylogenetic understanding evolves
- Old names may be deprecated; NCBI redirects to current classification
- Example: Some snake species reclassified; old names still searchable with notes

## Programmatic Integration for Veterinary AI

**Use Case 1: Standardize Patient Species in EHR**
```python
def standardize_species(species_name):
    """Convert user input to NCBI TaxID."""
    handle = Entrez.esearch(db="taxonomy", term=species_name)
    record = Entrez.read(handle)
    if record["IdList"]:
        return record["IdList"][0]  # Return TaxID
    else:
        return None  # Not found

# Clinical example:
patient_species = standardize_species("cat")  # Returns 9685
# Store TaxID in database for downstream analysis
```

**Use Case 2: Retrieve Species-Specific Genes for Precision Medicine**
```python
def get_orthologous_gene(gene_symbol, target_species_taxid):
    """Find orthologous gene in target species."""
    # Search for gene in target species
    handle = Entrez.esearch(
        db="gene",
        term=f'{gene_symbol} [GENE] AND {target_species_taxid} [ORGN]'
    )
    result = Entrez.read(handle)
    return result["IdList"]

# Example: Find dog BRCA2 to inform hereditary breast cancer screening
dog_brca2 = get_orthologous_gene("BRCA2", 9615)
# Returns list of dog BRCA2 gene IDs for annotation
```

**Use Case 3: Cross-Species Disease Modeling**
```python
# Map canine tumor to human disease model
canine_species = 9615  # Dog
human_species = 9606   # Human
mouse_species = 10090  # Mouse

# Download canine osteosarcoma gene signatures (SRA + RNA-seq)
# Align to human osteosarcoma expression data
# Identify conserved oncogenic pathways across species
```

## Rate Limits & Best Practices

**Entrez API Limits:**
- Without API key: 3 requests per second per IP
- With API key (free registration): 10 requests per second
- Register: https://www.ncbi.nlm.nih.gov/account/

**Best Practices:**
- Cache results locally; avoid redundant queries
- Use `retmax=10000` to batch searches (vs. multiple small queries)
- Implement backoff retry (if rate-limited, wait 1-2 seconds)
- Always provide `Entrez.email` in scripts (NCBI monitors abuse)
- Batch Entrez calls: query multiple species in single request if possible

## Limitations

- **Incomplete Metadata:** Some organisms lack complete genomic annotation (rare exotic species)
- **Taxonomy Instability:** Species nomenclature evolves; old publication names may not match current NCBI
- **Limited Exotic Data:** Well-characterized species (dog, cat, horse) have extensive data; rare species have sparse genomic resources
- **Data Quality:** Not all GenBank submissions are curated; sequence annotations may contain errors
- **This is Reference Only:** Taxonomy lookup does not provide clinical guidance; veterinary judgment required for translational decisions

## Sources

- **NCBI Taxonomy:** https://www.ncbi.nlm.nih.gov/taxonomy
- **NCBI Entrez:** https://www.ncbi.nlm.nih.gov/books/NBK25499/ (E-utilities documentation)
- **Biopython Entrez:** https://biopython.org/wiki/Documentation (Python API)
- **GenBank:** https://www.ncbi.nlm.nih.gov/genbank
- **RefSeq:** https://www.ncbi.nlm.nih.gov/refseq
- **SRA:** https://www.ncbi.nlm.nih.gov/sra
- **Entrez Gene:** https://www.ncbi.nlm.nih.gov/gene

## Advanced Integration

VetClaw SDK provides convenience wrappers around Entrez API for species lookup and genomic data retrieval. See `/sessions/charming-practical-mayer/mnt/OpenVet/vetclaw/vetclaw/sdk/` for Python/TypeScript NCBI Taxonomy client examples.
