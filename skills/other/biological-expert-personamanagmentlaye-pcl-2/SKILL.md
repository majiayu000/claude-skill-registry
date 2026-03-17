---
name: biological-expert
version: 1.0.0
description: Expert-level biology, biotechnology, genetics, bioinformatics, and computational biology
category: scientific
tags: [biology, biotechnology, genetics, bioinformatics, genomics]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(python:*)
---

# Biological Sciences Expert

Expert guidance for biology, biotechnology, genetics, bioinformatics, and computational biology applications.

## Core Concepts

### Molecular Biology
- DNA, RNA, and protein structure
- Central dogma (transcription, translation)
- Gene expression and regulation
- Genetic mutations and variations
- CRISPR and gene editing
- Protein folding and structure

### Genomics & Bioinformatics
- DNA sequencing (Sanger, NGS, long-read)
- Genome assembly and annotation
- Sequence alignment (BLAST, BLAT)
- Variant calling and analysis
- RNA-seq analysis
- Phylogenetic analysis

### Systems Biology
- Metabolic pathways
- Protein-protein interactions
- Gene regulatory networks
- Mathematical modeling
- Pathway analysis
- Network biology

## DNA Sequence Analysis

```python
from Bio import SeqIO, Seq
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction, molecular_weight
from typing import Dict, List

class DNAAnalyzer:
    """Analyze DNA sequences"""

    def __init__(self, sequence: str):
        self.sequence = Seq(sequence.upper())

    def basic_stats(self) -> Dict:
        """Calculate basic sequence statistics"""
        return {
            "length": len(self.sequence),
            "gc_content": gc_fraction(self.sequence) * 100,
            "molecular_weight": molecular_weight(self.sequence, "DNA"),
            "nucleotide_counts": self._count_nucleotides()
        }

    def _count_nucleotides(self) -> Dict[str, int]:
        """Count each nucleotide"""
        return {
            'A': self.sequence.count('A'),
            'T': self.sequence.count('T'),
            'G': self.sequence.count('G'),
            'C': self.sequence.count('C')
        }

    def transcribe(self) -> str:
        """Transcribe DNA to RNA"""
        return str(self.sequence.transcribe())

    def translate(self, table: int = 1) -> str:
        """Translate DNA to protein"""
        return str(self.sequence.translate(table=table))

    def reverse_complement(self) -> str:
        """Get reverse complement"""
        return str(self.sequence.reverse_complement())

    def find_orfs(self, min_length: int = 100) -> List[Dict]:
        """Find Open Reading Frames"""
        orfs = []

        for strand, seq in [(+1, self.sequence), (-1, self.sequence.reverse_complement())]:
            for frame in range(3):
                trans = seq[frame:].translate(to_stop=False)

                for i, aa in enumerate(trans):
                    if aa == 'M':  # Start codon
                        for j in range(i + 1, len(trans)):
                            if trans[j] == '*':  # Stop codon
                                orf_len = (j - i) * 3

                                if orf_len >= min_length:
                                    orfs.append({
                                        "strand": strand,
                                        "frame": frame,
                                        "start": i * 3 + frame,
                                        "end": j * 3 + frame,
                                        "length": orf_len,
                                        "protein": str(trans[i:j])
                                    })
                                break

        return orfs

    def find_motif(self, motif: str) -> List[int]:
        """Find motif positions in sequence"""
        positions = []
        motif = motif.upper()

        for i in range(len(self.sequence) - len(motif) + 1):
            if str(self.sequence[i:i+len(motif)]) == motif:
                positions.append(i)

        return positions
```

## Sequence Alignment

```python
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import numpy as np

class SequenceAligner:
    """Perform sequence alignments"""

    @staticmethod
    def global_alignment(seq1: str, seq2: str,
                        match: float = 2,
                        mismatch: float = -1,
                        gap_open: float = -0.5,
                        gap_extend: float = -0.1):
        """Perform global alignment (Needleman-Wunsch)"""
        alignments = pairwise2.align.globalms(
            seq1, seq2,
            match, mismatch,
            gap_open, gap_extend
        )

        best = alignments[0]

        return {
            "aligned_seq1": best.seqA,
            "aligned_seq2": best.seqB,
            "score": best.score,
            "identity": SequenceAligner._calculate_identity(best.seqA, best.seqB)
        }

    @staticmethod
    def local_alignment(seq1: str, seq2: str,
                       match: float = 2,
                       mismatch: float = -1,
                       gap_open: float = -0.5,
                       gap_extend: float = -0.1):
        """Perform local alignment (Smith-Waterman)"""
        alignments = pairwise2.align.localms(
            seq1, seq2,
            match, mismatch,
            gap_open, gap_extend
        )

        best = alignments[0]

        return {
            "aligned_seq1": best.seqA,
            "aligned_seq2": best.seqB,
            "score": best.score,
            "identity": SequenceAligner._calculate_identity(best.seqA, best.seqB)
        }

    @staticmethod
    def _calculate_identity(seq1: str, seq2: str) -> float:
        """Calculate sequence identity percentage"""
        matches = sum(1 for a, b in zip(seq1, seq2) if a == b and a != '-')
        return (matches / min(len(seq1), len(seq2))) * 100
```

## Genomic Variant Analysis

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Variant:
    chromosome: str
    position: int
    reference: str
    alternate: str
    quality: float
    genotype: str
    depth: int
    allele_frequency: Optional[float] = None

class VariantAnnotator:
    """Annotate genetic variants"""

    def __init__(self):
        self.gene_annotations = {}

    def annotate_variant(self, variant: Variant) -> Dict:
        """Annotate variant with functional consequences"""
        annotation = {
            "variant": f"{variant.chromosome}:{variant.position}{variant.reference}>{variant.alternate}",
            "type": self._classify_variant_type(variant),
            "effect": self._predict_effect(variant),
            "quality": variant.quality,
            "depth": variant.depth
        }

        if variant.allele_frequency:
            annotation["allele_frequency"] = variant.allele_frequency
            annotation["rarity"] = self._classify_rarity(variant.allele_frequency)

        return annotation

    def _classify_variant_type(self, variant: Variant) -> str:
        """Classify variant type"""
        ref_len = len(variant.reference)
        alt_len = len(variant.alternate)

        if ref_len == 1 and alt_len == 1:
            return "SNV"  # Single Nucleotide Variant
        elif ref_len < alt_len:
            return "INSERTION"
        elif ref_len > alt_len:
            return "DELETION"
        else:
            return "INDEL"

    def _predict_effect(self, variant: Variant) -> str:
        """Predict variant effect on protein"""
        # Simplified effect prediction
        if self._classify_variant_type(variant) == "SNV":
            # Would check if it's in coding region, causes stop codon, etc.
            return "MISSENSE"
        return "UNKNOWN"

    def _classify_rarity(self, af: float) -> str:
        """Classify variant rarity"""
        if af > 0.05:
            return "COMMON"
        elif af > 0.01:
            return "LOW_FREQUENCY"
        else:
            return "RARE"
```

## RNA-seq Analysis

```python
import pandas as pd
import numpy as np
from scipy import stats

class RNASeqAnalyzer:
    """Analyze RNA-seq expression data"""

    def __init__(self, counts_matrix: pd.DataFrame):
        """
        counts_matrix: genes x samples matrix of raw counts
        """
        self.counts = counts_matrix
        self.normalized = None

    def normalize_counts(self, method: str = "tpm"):
        """Normalize count data"""
        if method == "tpm":
            # Transcripts Per Million
            self.normalized = (self.counts / self.counts.sum(axis=0)) * 1e6
        elif method == "log2":
            # Log2 transformation
            self.normalized = np.log2(self.counts + 1)

        return self.normalized

    def differential_expression(self, condition1: List[str],
                                condition2: List[str],
                                method: str = "ttest") -> pd.DataFrame:
        """Perform differential expression analysis"""
        results = []

        for gene in self.counts.index:
            expr1 = self.counts.loc[gene, condition1]
            expr2 = self.counts.loc[gene, condition2]

            if method == "ttest":
                statistic, pvalue = stats.ttest_ind(expr1, expr2)

            fc = expr2.mean() / (expr1.mean() + 1)
            log2fc = np.log2(fc)

            results.append({
                "gene": gene,
                "mean_condition1": expr1.mean(),
                "mean_condition2": expr2.mean(),
                "fold_change": fc,
                "log2_fold_change": log2fc,
                "p_value": pvalue,
                "significant": pvalue < 0.05 and abs(log2fc) > 1
            })

        return pd.DataFrame(results)

    def identify_marker_genes(self, threshold_fc: float = 2,
                             threshold_pval: float = 0.05) -> List[str]:
        """Identify significantly differentially expressed genes"""
        # This would use the differential_expression results
        pass
```

## Best Practices

### Data Analysis
- Use appropriate statistical tests
- Account for multiple testing correction
- Validate results with independent methods
- Document data preprocessing steps
- Use version control for analysis scripts
- Maintain reproducible workflows

### Sequence Analysis
- Quality control of sequencing data
- Use appropriate reference genomes
- Validate variant calls
- Consider batch effects
- Use established bioinformatics tools
- Benchmark against known datasets

### Computational Biology
- Use efficient data structures for large datasets
- Parallelize computationally intensive tasks
- Validate biological interpretations
- Consult domain experts
- Document assumptions clearly
- Use standardized file formats (FASTA, VCF, BAM)

## Anti-Patterns

❌ No quality control of input data
❌ Ignoring batch effects
❌ No multiple testing correction
❌ Over-interpreting correlations
❌ Inadequate sample sizes
❌ Not validating computational predictions
❌ Ignoring biological context

## Resources

- Biopython: https://biopython.org/
- NCBI Resources: https://www.ncbi.nlm.nih.gov/
- Ensembl: https://www.ensembl.org/
- Galaxy Project: https://galaxyproject.org/
- Bioconductor: https://www.bioconductor.org/
