---
name: life-sciences-connector
description: Query PubMed and scientific databases for protocols, analyze biological data with Biopython, handle HIPAA-compliant data. Use for biology research, protocol searches, sequence analysis, or scientific data handling. Cross-validates sources for high accuracy. Triggers on "PubMed", "biology", "scientific data", "sequences", "protocols", "life sciences", "HIPAA".
---

# Life Sciences Connector

## Purpose

Connect to scientific databases (PubMed, Benchling) for protocol queries and biological data analysis with Biopython integration.

## When to Use

- Biology research tasks
- Protocol searches
- Scientific data handling
- Sequence analysis
- Lab data integration
- HIPAA-compliant workflows

## Core Instructions

### PubMed Query

```python
from Bio import Entrez
Entrez.email = "your.email@example.com"

def search_pubmed(term, retmax=5):
    """Search PubMed for articles"""
    handle = Entrez.esearch(db="pubmed", term=term, retmax=retmax)
    record = Entrez.read(handle)
    return record['IdList']

def fetch_article(pmid):
    """Fetch article details"""
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml")
    return Entrez.read(handle)

# Usage
results = search_pubmed("CRISPR protocol")
for pmid in results:
    article = fetch_article(pmid)
    print(article['Title'])
```

### Sequence Analysis

```python
from Bio import SeqIO
from Bio.Align import PairwiseAligner

# Parse FASTA
sequences = list(SeqIO.parse("sequences.fasta", "fasta"))

# Align sequences
aligner = PairwiseAligner()
alignments = aligner.align(sequences[0].seq, sequences[1].seq)
print(f"Alignment score: {alignments[0].score}")
```

### HIPAA Compliance

```python
def anonymize_patient_data(data):
    """
    Anonymize patient information (HIPAA)
    """
    # Remove PHI (Protected Health Information)
    phi_fields = [
        'name', 'address', 'phone', 'email',
        'ssn', 'medical_record_number'
    ]

    anonymized = data.copy()
    for field in phi_fields:
        if field in anonymized:
            anonymized[field] = hash_or_remove(field, data[field])

    return anonymized
```

## Guidelines

- **Accuracy**: Cross-validate sources
- **Privacy**: Anonymize patient data (HIPAA)
- **Citations**: Always cite sources
- **Verification**: Cross-check protocols

## Dependencies

- Python 3.8+
- biopython
- requests
- PubMed Entrez API access

## Version

v1.0.0 (2025-10-23)

