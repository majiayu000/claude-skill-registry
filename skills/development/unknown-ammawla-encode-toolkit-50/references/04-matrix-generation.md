# Contact Matrix Generation with Juicer and Cooler

Generate multi-resolution contact matrices in .hic (Juicer) and .mcool
(cooler) formats from deduplicated .pairs files.

## Juicer Tools: Generate .hic File

The .hic format is the ENCODE standard for Hi-C contact matrices.

### Convert pairs to Juicer medium format

```bash
# pairtools output -> Juicer medium format
# Format: strand1 chr1 pos1 frag1 strand2 chr2 pos2 frag2
pairtools select \
    '(pair_type == "UU")' \
    sample_dedup.pairs.gz \
    | awk 'BEGIN{OFS="\t"} !/^#/ {
        s1 = ($6 == "+") ? 0 : 16;
        s2 = ($7 == "+") ? 0 : 16;
        print s1, $2, $3, 0, s2, $4, $5, 1
    }' > sample_juicer_medium.txt
```

### Build .hic file

```bash
java -Xmx64g -jar juicer_tools.jar pre \
    --threads 4 \
    -r 1000,5000,10000,25000,50000,100000,250000,500000,1000000 \
    -k KR,VC,VC_SQRT \
    sample_juicer_medium.txt \
    sample.hic \
    hg38.chrom.sizes
```

### Key Parameters

| Parameter | Value | Reason |
|-----------|-------|--------|
| `-Xmx64g` | 64 GB heap | Large matrices need significant memory |
| `-r` | Multiple resolutions | Enables multi-scale analysis |
| `-k` | KR,VC,VC_SQRT | Generate multiple normalization vectors |

### Normalization Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| KR | Knight-Ruiz balancing | Default, most common |
| VC | Vanilla Coverage | Simple, transparent |
| VC_SQRT | Square root VC | Reduces extreme values |

ENCODE standard: KR normalization for primary analysis.

## Cooler: Generate .mcool File

The .mcool format is preferred by Python/R analysis tools.

### Load pairs into cooler

```bash
# Create single-resolution .cool files, then zoom
cooler cload pairs \
    --chrom1 2 --pos1 3 --chrom2 4 --pos2 5 \
    --assembly hg38 \
    hg38.chrom.sizes:1000 \
    sample_valid.pairs.gz \
    sample_1kb.cool

# Generate multi-resolution mcool
cooler zoomify \
    --balance \
    --resolutions 1000,5000,10000,25000,50000,100000,250000,500000,1000000 \
    --nproc 4 \
    sample_1kb.cool \
    -o sample.mcool
```

### ICE Balancing

cooler uses ICE (Iterative Correction and Eigenvector decomposition) by
default via the `--balance` flag. This is equivalent to the `cooler balance`
command:

```bash
cooler balance --nproc 4 sample_1kb.cool
```

## Matrix Quality Assessment

### Contact Count per Resolution

```bash
# Check contacts at each resolution
for res in 1000 5000 10000 25000; do
    cooler info sample.mcool::resolutions/${res} | \
        python3 -c "import json,sys; d=json.load(sys.stdin); print(f'${res}bp: {d[\"sum\"]:,} contacts')"
done
```

### Distance Decay Curve

The contact frequency vs distance curve is a fundamental QC metric:

```bash
# Using cooltools
cooltools expected-cis \
    --nproc 4 \
    sample.mcool::resolutions/10000 \
    -o sample_expected_cis.tsv
```

The slope should be approximately -1 on a log-log plot (power law decay).
Deviations indicate:
- Steeper slope: Over-digestion or poor ligation
- Shallower slope: Incomplete digestion

### Compartment Calling (A/B)

At 100 kb resolution, call A/B compartments using eigenvector decomposition:

```bash
cooltools eigs-cis \
    --n-eigs 3 \
    --phasing-track /ref/gene_density.bedGraph \
    sample.mcool::resolutions/100000 \
    -o sample_compartments
```

The first eigenvector (E1) separates active (A) from inactive (B) compartments.
Use gene density as phasing track to orient E1 correctly (positive = A compartment).

## Visualization

### Juicebox (for .hic files)
```bash
# Launch Juicebox desktop application
java -jar Juicebox.jar sample.hic
```

### HiGlass (for .mcool files)
```bash
# Ingest into HiGlass server
higlass-manage ingest sample.mcool --assembly hg38
```
