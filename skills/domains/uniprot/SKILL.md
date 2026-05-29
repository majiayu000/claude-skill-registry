---
name: uniprot
description: >
  Access UniProt for protein sequence and annotation retrieval.
  Use this skill when: (1) Looking up protein sequences by accession,
  (2) Finding functional annotations,
  (3) Getting domain boundaries,
  (4) Finding homologs and variants,
  (5) Cross-referencing to PDB structures.

  For structure retrieval, use pdb.
  For sequence design, use proteinmpnn.
license: MIT
category: utilities
tags: [database, sequence, annotation]
---

# UniProt Database Access

**Note**: This skill uses the UniProt REST API directly. No Modal deployment needed - all operations run locally via HTTP requests.

## Fetching Sequences

### By Accession
```bash
# FASTA format
curl "https://rest.uniprot.org/uniprotkb/P00533.fasta"

# JSON format with annotations
curl "https://rest.uniprot.org/uniprotkb/P00533.json"
```

### Using Python
```python
import requests

def get_uniprot_sequence(accession):
    """Fetch sequence from UniProt."""
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.fasta"
    response = requests.get(url)
    if response.ok:
        lines = response.text.strip().split('\n')
        header = lines[0]
        sequence = ''.join(lines[1:])
        return header, sequence
    return None, None
```

## Getting Annotations

### Full Entry
```python
def get_uniprot_entry(accession):
    """Fetch full UniProt entry as JSON."""
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.json"
    response = requests.get(url)
    return response.json() if response.ok else None

entry = get_uniprot_entry("P00533")
print(f"Protein: {entry['proteinDescription']['recommendedName']['fullName']['value']}")
```

### Domain Boundaries
```python
def get_domains(accession):
    """Extract domain annotations."""
    entry = get_uniprot_entry(accession)
    domains = []

    for feature in entry.get('features', []):
        if feature['type'] == 'Domain':
            domains.append({
                'name': feature.get('description', ''),
                'start': feature['location']['start']['value'],
                'end': feature['location']['end']['value']
            })

    return domains

# Example: EGFR domains
domains = get_domains("P00533")
# [{'name': 'Kinase', 'start': 712, 'end': 979}, ...]
```

## Searching UniProt

### By Gene Name
```python
def search_uniprot(query, organism=None, limit=10):
    """Search UniProt by query."""
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": query,
        "format": "json",
        "size": limit
    }
    if organism:
        params["query"] += f" AND organism_id:{organism}"

    response = requests.get(url, params=params)
    return response.json()['results']

# Search for human EGFR
results = search_uniprot("EGFR", organism=9606)
```

### By Sequence Similarity (BLAST)
```python
# Use UniProt BLAST
# https://www.uniprot.org/blast
```

## Cross-References

### Get PDB Structures
```python
def get_pdb_references(accession):
    """Get PDB structures for UniProt entry."""
    entry = get_uniprot_entry(accession)
    pdbs = []

    for xref in entry.get('uniProtKBCrossReferences', []):
        if xref['database'] == 'PDB':
            pdbs.append({
                'pdb_id': xref['id'],
                'method': xref.get('properties', [{}])[0].get('value', ''),
                'chains': xref.get('properties', [{}])[1].get('value', '')
            })

    return pdbs

# Example: PDB structures for EGFR
pdbs = get_pdb_references("P00533")
```

## Common Use Cases

### Target Selection
```python
# 1. Find protein by name
results = search_uniprot("insulin receptor", organism=9606)

# 2. Get accession
accession = results[0]['primaryAccession']  # e.g., P06213

# 3. Get domains
domains = get_domains(accession)

# 4. Find PDB structure
pdbs = get_pdb_references(accession)

# 5. Download best structure for design
```

### Sequence Alignment Info
```python
def get_sequence_variants(accession):
    """Get natural variants from UniProt."""
    entry = get_uniprot_entry(accession)
    variants = []

    for feature in entry.get('features', []):
        if feature['type'] == 'Natural variant':
            variants.append({
                'position': feature['location']['start']['value'],
                'original': feature.get('alternativeSequence', {}).get('originalSequence', ''),
                'variant': feature.get('alternativeSequence', {}).get('alternativeSequences', [''])[0],
                'description': feature.get('description', '')
            })

    return variants
```

## API Reference

| Endpoint | Description |
|----------|-------------|
| `/uniprotkb/{id}.fasta` | FASTA sequence |
| `/uniprotkb/{id}.json` | Full entry JSON |
| `/uniprotkb/search` | Search entries |
| `/uniprotkb/stream` | Batch download |

## Troubleshooting

**Entry not found**: Check accession format (e.g., P00533)
**Rate limits**: Add delay between requests
**Large downloads**: Use stream endpoint with pagination

---

**Next**: Use sequence with `esm` for embeddings or `colabfold` for structure.
