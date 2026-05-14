# Broad vs Narrow Histone Marks

Reference guide for selecting the correct peak format and merge parameters during histone ChIP-seq aggregation.

## Classification

### Narrow (Focal) Marks

These marks create sharp, well-defined peaks suitable for **narrowPeak** format (10 columns). They localize to specific regulatory elements and typically span 1-5kb.

| Mark | Function | Typical Peak Width | Genomic Context |
|------|----------|-------------------|-----------------|
| **H3K4me3** | Active promoters | 2-4 kb | TSS +/- 1-2kb |
| **H3K27ac** | Active enhancers and promoters | 2-5 kb | Enhancers, TSS |
| **H3K4me1** | Enhancers (poised or active) | 2-5 kb | Distal regulatory |
| **H3K9ac** | Active chromatin | 1-3 kb | Promoters, enhancers |

### Broad (Diffuse) Marks

These marks spread across large genomic domains requiring **broadPeak** format (9 columns). They reflect chromatin states spanning entire gene bodies, repressed loci, or heterochromatin.

| Mark | Function | Typical Domain Width | Genomic Context |
|------|----------|---------------------|-----------------|
| **H3K27me3** | Polycomb repression | 10-100+ kb | Developmental gene silencing |
| **H3K36me3** | Active transcription (gene body) | 10-100 kb | Transcribed gene bodies |
| **H3K9me3** | Constitutive heterochromatin | 50-500+ kb | Pericentromeric, repetitive DNA |
| **H3K4me1** (broad mode) | Broad enhancer domains | Variable | Sometimes called as broad |

### Context-Dependent Marks

Some marks can be called in either mode depending on the peak caller configuration:

- **H3K4me1**: Usually narrow at enhancers; occasionally broad at primed/poised domains
- **H3K36me3**: Clearly broad across gene bodies; narrow caller misses most signal
- **H3K27me3**: Always broad; narrow caller captures only focal Polycomb peaks at promoters

## MACS2 Parameters by Mark Type

| Parameter | Narrow Marks | Broad Marks |
|-----------|-------------|-------------|
| `--broad` | No | **Yes** |
| `--broad-cutoff` | N/A | 0.1 (default) |
| `--nomodel --extsize` | 147 (nucleosome) | 147 |
| `-q` / `--qvalue` | 0.05 | 0.05 |
| `--keep-dup` | 1 (default) | 1 (default) |
| Gap parameters | N/A | `--max-gap 500` typical |

ENCODE pipeline default: MACS2 with `--broad` for H3K27me3, H3K9me3, H3K36me3; standard narrow mode for all others.

## Peak Merging Considerations

### Narrow Marks

```bash
# Default overlap-only merge (no gap tolerance)
bedtools merge -i sorted_peaks.bed -c 4 -o count_distinct
```

- Merge distance (`-d`): **0** (overlap only, default)
- Peaks >10kb are suspicious for narrow marks
- Summit positions (column 10) are lost after merge

### Broad Marks

```bash
# Gap-tolerant merge for domain marks
bedtools merge -i sorted_peaks.bed -d 1000 -c 4 -o count_distinct
```

- Merge distance (`-d`): **1000-5000 bp** depending on domain size
- H3K27me3: use `-d 5000` (domains can be fragmented)
- H3K36me3: use `-d 1000` (gene body coverage)
- H3K9me3: use `-d 5000` (large heterochromatin blocks)

### Critical Rules

1. **Never merge narrow and broad formats together.** They represent different biological features at different scales.
2. **broadPeak has 9 columns** (no summit column). narrowPeak has 10 columns (summit in column 10).
3. **Check ENCODE output_type**: broad marks use `output_type="replicated peaks"` with `file_type="bed broadPeak"`, while narrow marks use `output_type="IDR thresholded peaks"`.

## How to Identify the Correct Format

When downloading from ENCODE, check the file metadata:

```
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    assembly="GRCh38"
)
```

Look at the `file_type` field in the response:
- `bed narrowPeak` = narrow format (10 columns)
- `bed broadPeak` = broad format (9 columns)

If the mark is called as both narrow and broad in different experiments, prefer the biologically appropriate format from the table above.

## References

- Landt et al. 2012, Genome Research (ENCODE ChIP-seq guidelines) -- established narrow vs broad calling conventions
- ENCODE Phase 3, Gorkin et al. 2020, Nature -- mark classification and peak calling parameters across 1,128 experiments
- MACS2 documentation (Zhang et al. 2008) -- `--broad` flag implementation and gap parameters
- Roadmap Epigenomics Consortium 2015, Nature -- chromatin state classification using narrow and broad marks
