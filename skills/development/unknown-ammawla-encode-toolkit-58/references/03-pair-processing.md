# Pair Processing with pairtools

pairtools is the ENCODE-standard tool for Hi-C pair classification,
filtering, and deduplication. It processes aligned BAMs into sorted,
deduplicated .pairs files ready for matrix generation.

## Parse: Classify Read Pairs

Convert aligned BAM to .pairs format with pair type classification:

```bash
pairtools parse \
    --chroms-path chrom.sizes \
    --min-mapq 30 \
    --walks-policy mask \
    --max-inter-align-gap 30 \
    --nproc-in 4 \
    --nproc-out 4 \
    sample_paired.bam \
    | pairtools sort \
        --nproc 4 \
        --tmpdir /tmp/pairtools/ \
        -o sample_parsed_sorted.pairs.gz
```

### Parse Parameters

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--min-mapq 30` | MAPQ 30 | Filter low-confidence alignments |
| `--walks-policy mask` | Mask walks | Handle complex ligation events |
| `--max-inter-align-gap 30` | 30 bp | Maximum gap between split alignments |

### Pair Types Output

pairtools assigns each pair a two-letter code:

| Code | Meaning | Use |
|------|---------|-----|
| UU | Both uniquely mapped | Primary contacts |
| UR/RU | One unique, one rescued | Valid with caution |
| MU/UM | One multi-mapped | Ambiguous, usually excluded |
| MM | Both multi-mapped | Excluded |
| NM/MN | One unmapped | Excluded |
| NN | Both unmapped | Excluded |
| WW | Walk pair | Ligation artifact |
| DD | Duplicate | Removed in dedup step |

## Sort Pairs

Pairs must be sorted by genomic position for deduplication:

```bash
pairtools sort \
    --nproc 4 \
    --tmpdir /tmp/ \
    sample_parsed.pairs.gz \
    -o sample_sorted.pairs.gz
```

## Deduplicate

Remove PCR/optical duplicates based on alignment positions:

```bash
pairtools dedup \
    --nproc-in 4 \
    --nproc-out 4 \
    --mark-dups \
    --output-stats sample_dedup_stats.txt \
    -o sample_dedup.pairs.gz \
    sample_sorted.pairs.gz
```

### Dedup Statistics

The stats file reports:
- Total pairs processed
- Unique pairs retained
- PCR duplicate pairs removed
- Optical duplicate pairs removed
- Complexity estimate

Expected duplication rate: 10-40% depending on library complexity and depth.

## Filter for Valid Contacts

Select only UU pairs for contact matrix generation:

```bash
pairtools select \
    '(pair_type == "UU")' \
    sample_dedup.pairs.gz \
    -o sample_valid.pairs.gz
```

For higher sensitivity (at cost of some noise), include rescued pairs:

```bash
pairtools select \
    '(pair_type == "UU") or (pair_type == "UR") or (pair_type == "RU")' \
    sample_dedup.pairs.gz \
    -o sample_valid_rescued.pairs.gz
```

## Pair Statistics

Generate detailed contact statistics:

```bash
pairtools stats \
    sample_valid.pairs.gz \
    -o sample_pair_stats.txt
```

Key metrics from the stats output:
- **cis contacts**: Same chromosome (expect >60%)
- **trans contacts**: Different chromosomes
- **cis >20kb**: Long-range cis contacts (biologically meaningful)
- **cis <20kb**: Short-range, often ligation artifacts
- **Pair type distribution**: Should be dominated by UU

## Cis/Trans Ratio

The cis/trans ratio is a key QC metric:

```bash
awk '/cis/ {cis=$2} /trans/ {trans=$2} END {
    print "Cis:", cis;
    print "Trans:", trans;
    print "Cis/Trans ratio:", cis/trans
}' sample_pair_stats.txt
```

| Ratio | Quality |
|-------|---------|
| >2.0 | Good |
| 1.5-2.0 | Acceptable |
| 1.0-1.5 | Warning -- possible issues |
| <1.0 | Fail -- likely random ligation |
