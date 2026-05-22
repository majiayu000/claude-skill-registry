---
name: protein-phylogeny
description: >
  Protein (gene) phylogeny inference pipeline: generates a .qmd analysis script that performs
  alignment, optional trimming, and tree building. Use when building phylogenetic trees from
  protein sequences, aligning protein families, running IQ-TREE or MAFFT for phylogenetics,
  or when the user says "gene tree" or "protein tree." Covers single domains, whole proteins,
  and multi-domain proteins across deep evolutionary distances (sponges, animals, eukaryotes).
  Do NOT load for nucleotide-only phylogenies, species trees from concatenated matrices,
  or tree visualization (use tree-formatting skill for that).
user-invocable: false
---

# Protein Phylogeny Inference

Pipeline for building protein phylogenies across deep evolutionary distances. Designed for
single domains, whole single-domain proteins, and multi-domain proteins, from ~10 to
several thousand sequences, spanning sponges to all eukaryotes.

**If the user says "gene tree" they may mean protein sequences.** Confirm if ambiguous,
or inspect the input sequences (amino acid alphabet vs nucleotide).

---

## Overview: Two-Phase Workflow

This skill generates a **reproducible .qmd analysis script** (Python) rather than running
commands directly. The workflow is:

1. **Discuss** — Resolve all pipeline decisions with the user (input sequences, algorithm,
   model tier, trimming, etc.)
2. **Generate** — Write a complete `.qmd` script encoding all decisions as configuration
   variables, following quarto-docs and script-organization skill conventions
3. **Render** — User renders with `quarto render` (or Claude renders it), producing all
   outputs in `outs/<subdirectory>/XX_script_name/`

One script per major deliverable (one protein family or domain tree). All pipeline steps
go in one `.qmd` unless there is a strong reason to split.

---

## Phase 1: Discussion

Resolve these questions with the user **before generating the script**. Use the
recommendation logic below to guide the conversation.

### 1. Input validation

- Input: protein FASTA file
- If sequences look like nucleotides (only A/T/G/C/N), confirm with user
- Report basic stats: number of sequences, median length, min/max length

### 2. Minimum length cutoff

- Calculate median sequence length
- Flag sequences shorter than 50% of median: "You have N sequences shorter than 50% of
  the median length (X aa). Short fragments can degrade alignment quality. Want to remove
  them, use a different cutoff, or keep all?"

### 3. CD-HIT redundancy reduction (optional, off by default)

- If requested: 99% identity threshold
- Report how many sequences would be removed

### 4. MAFFT algorithm selection

| Condition | Algorithm | MAFFT flags |
|-----------|-----------|-------------|
| Single domain or whole protein, <= 2000 seq | **L-INS-i** (default) | `--localpair --maxiterate 1000 --reorder` |
| Multi-domain protein with variable linkers | **E-INS-i** | `--genafpair --maxiterate 1000 --reorder` |
| > 2000 sequences | **auto** (MAFFT decides) | `--auto --reorder` |

Recommendation: "You have N sequences, median length X aa. This looks like a
[single-domain / multi-domain / whole-protein] dataset. I'd recommend MAFFT
[L-INS-i / E-INS-i / auto]. Does that sound right?"

### 5. Trimming (optional, off by default)

Do not trim unless the user requests it. For deep divergences, aggressive trimming can
remove phylogenetically informative sites. Good models (site-heterogeneous) handle noisy
columns.

| Tool | Mode | Best for |
|------|------|----------|
| **ClipKIT** | `kpic-gappy` | General purpose |
| **BMGE** | BLOSUM30 | Very deep divergences with compositional heterogeneity |

- Deep datasets (cross-animal, cross-eukaryote): recommend BMGE
- Otherwise: recommend ClipKIT

### 6. IQ-TREE tier selection

| Tier | Model | When to use | Approximate time (166 seq) |
|------|-------|-------------|---------------------------|
| **1** | MFP (ModelFinder) | Quick exploration, screening | ~15-30 min |
| **2** | ELM+C60+G PMSF (default) | Deep eukaryotic phylogenies | ~3-8 hours |
| **2 alt** | LG+C60+F+R PMSF | Non-eukaryotic or for comparison | ~3-8 hours |
| **3** | PhyloBayes CAT+GTR | Maximum rigor, < 200 seq | Hours to days |

- **ELM** (Eukaryotic Linked Mixture): better than LG with profile mixtures for
  eukaryotic data (Banos et al. 2024, MBE)
- C60: 60-class amino acid profile mixture
- PMSF: posterior mean site frequency profiles (ML approximation of Bayesian CAT)

### 7. Branch support

- **Default:** UFBoot2 (1000) + SH-aLRT (1000), simultaneous with `-B 1000 -alrt 1000`
- **Optional:** Non-parametric bootstrap (`-b 1000`) for publication-quality final trees
- Note: UFBoot >= 95 ~ traditional bootstrap >= 70

### 8. No automated outlier removal

The user inspects the tree after inference and decides if anything looks wrong. Do not
use TreeShrink or similar tools automatically.

---

## Phase 2: Script Generation

Once all decisions are resolved, generate a `.qmd` script following these conventions.

### Naming and placement

Follow the script-organization skill:
- Script: `scripts/<subdirectory>/XX_name.qmd` (next available number)
- Outputs: `outs/<subdirectory>/XX_name/`
- Register in project CLAUDE.md script table

### .qmd structure

Generate a Python `.qmd` with these sections in order:

1. YAML frontmatter (standard quarto-docs Python template)
2. Setup chunk (PROJECT_ROOT, out_dir, git_hash, imports)
3. **Configuration chunk** — all user decisions as named variables
4. Inputs chunk (FASTA path, clearly labeled)
5. Input validation chunk (sequence stats, length filtering)
6. [Optional] CD-HIT chunk (controlled by config flag)
7. Alignment chunk (MAFFT via subprocess)
8. [Optional] Trimming chunk (controlled by config flag)
9. Tree inference chunk (IQ-TREE, tier from config)
10. Summary chunk (alignment stats, model, support values)
11. Build info chunk (standard BUILD_INFO.txt)

### Key patterns

**Configuration chunk** — all decisions as named variables at the top:

```python
#| label: config

# ---- Pipeline Configuration ----
# Resolved during discussion; change here to re-run with different options.

INPUT_FASTA = PROJECT_ROOT / "data/phylogenetics/sequences.fasta"
MIN_LENGTH_FRACTION = 0.5        # Remove sequences shorter than this fraction of median

RUN_CDHIT = False                # Redundancy reduction
CDHIT_THRESHOLD = 0.99

MAFFT_ALGORITHM = "linsi"        # "linsi" | "einsi" | "auto"
MAFFT_THREADS = 8                # Parallel threads for MAFFT alignment

RUN_TRIMMING = False
TRIMMING_TOOL = "clipkit"        # "clipkit" | "bmge"

IQTREE_TIER = 2                  # 1 = quick MFP, 2 = ELM+C60+G PMSF, 3 = PhyloBayes
IQTREE_MATRIX = "ELM"           # "ELM" | "LG" (Tier 2 only)
IQTREE_THREADS = 8              # Fixed thread count (AUTO crashes with PMSF in v3.0.1)
BOOTSTRAP_REPS = 1000
```

**Caching pattern** — skip expensive steps if output exists:

```python
aligned_fasta = out_dir / "aligned.fasta"

if not aligned_fasta.exists():
    print("Running MAFFT alignment...")
    # ... subprocess call ...
    print(f"  Alignment: {n_seqs} sequences x {n_cols} columns")
else:
    print(f"Alignment cached at {aligned_fasta.name}, skipping MAFFT")
```

**Subprocess pattern** — consistent error handling:

```python
result = subprocess.run(
    cmd, capture_output=True, text=True
)
if result.returncode != 0:
    print(f"STDERR: {result.stderr[:500]}")
    raise RuntimeError("MAFFT failed")
```

### MAFFT algorithm mapping

```python
MAFFT_FLAGS = {
    "linsi": ["--localpair", "--maxiterate", "1000", "--reorder", "--thread", str(MAFFT_THREADS)],
    "einsi": ["--genafpair", "--maxiterate", "1000", "--reorder", "--thread", str(MAFFT_THREADS)],
    "auto":  ["--auto", "--reorder", "--thread", str(MAFFT_THREADS)],
}
```

### IQ-TREE commands by tier

**Tier 1 — Quick baseline:**
```python
cmd = [
    "iqtree3", "-s", str(input_aln),
    "-m", "MFP",
    "-B", str(BOOTSTRAP_REPS), "-alrt", str(BOOTSTRAP_REPS),
    "-nstop", "50", "-T", "AUTO",
    "-pre", str(out_dir / "tree")
]
```

**Tier 2 — Two-pass PMSF (default for deep eukaryotic phylogenies):**

```python
model = f"{IQTREE_MATRIX}+C60+G" if IQTREE_MATRIX == "ELM" else f"{IQTREE_MATRIX}+C60+F+R"

# Pass 1: guide tree
guide_tree = out_dir / "guide.treefile"
if not guide_tree.exists():
    cmd_pass1 = [
        "iqtree3", "-s", str(input_aln),
        "-m", model,
        "-nstop", "50", "-T", str(IQTREE_THREADS),
        "-pre", str(out_dir / "guide")
    ]
    subprocess.run(cmd_pass1, check=True)

# Pass 2: PMSF tree with bootstrap
final_tree = out_dir / "pmsf.treefile"
if not final_tree.exists():
    cmd_pass2 = [
        "iqtree3", "-s", str(input_aln),
        "-m", model,
        "-ft", str(guide_tree),
        "-B", str(BOOTSTRAP_REPS), "-alrt", str(BOOTSTRAP_REPS),
        "-nstop", "50", "-T", str(IQTREE_THREADS),
        "-pre", str(out_dir / "pmsf")
    ]
    subprocess.run(cmd_pass2, check=True)
```

> **Bug workaround (IQ-TREE 3.0.1):** `-T AUTO` crashes with an assertion error
> during PMSF site frequency computation (`computePartialParsimonyFast`). Use a
> fixed thread count (e.g., `-T 8`) instead. Re-test with future IQ-TREE releases.

**Tier 3 — PhyloBayes (special case):**

PhyloBayes runs for hours to days and does not fit the "render once" model. The `.qmd`
should launch chains and note that convergence must be checked separately:

```python
print("PhyloBayes requires long-running chains.")
print("Launch manually:")
print(f"  pb_mpi -d {input_phy} -cat -gtr -x 1 10000 chain1")
print(f"  pb_mpi -d {input_phy} -cat -gtr -x 1 10000 chain2")
print("Check convergence with bpcomp -x 2500 chain1 chain2")
```

- CAT+GTR: infinite mixture model, gold standard for deep phylogenetics
- Very slow; not practical for > ~200 sequences

### Summary chunk

Parse IQ-TREE output and report:

```python
# Read support values from treefile
import re
tree_text = (out_dir / "pmsf.treefile").read_text()
supports = re.findall(r'\)([\d.]+)/([\d.]+):', tree_text)
ufboot = [float(s[1]) for s in supports]
shalrt = [float(s[0]) for s in supports]

total = len(ufboot)
print(f"=== Tree Inference Summary ===")
print(f"Sequences: {n_seqs}")
print(f"Alignment: {n_cols} columns")
print(f"Model: {model} (Tier {IQTREE_TIER})")
print(f"UFBoot >= 95: {sum(1 for v in ufboot if v >= 95)}/{total}")
print(f"UFBoot >= 70: {sum(1 for v in ufboot if v >= 70)}/{total}")
print(f"SH-aLRT >= 80: {sum(1 for v in shalrt if v >= 80)}/{total}")
print(f"\nTree file: {final_tree}")
print(f"\nNext: use tree-formatting skill for visualization")
```

---

## Phase 3: After Rendering

### Output files

The rendered script produces these files in `outs/<subdirectory>/XX_name/`:

| File | Description |
|------|-------------|
| `pmsf.treefile` | ML tree with UFBoot/SH-aLRT support (Tier 2) |
| `pmsf.contree` | Bootstrap consensus tree |
| `pmsf.iqtree` | Full IQ-TREE report |
| `pmsf.sitefreq` | PMSF site frequency profiles |
| `guide.treefile` | Pass 1 guide tree (Tier 2) |
| `aligned.fasta` | MAFFT alignment |
| `BUILD_INFO.txt` | Script provenance |

### How to render

```bash
source ~/miniconda3/etc/profile.d/conda.sh && conda activate <env>
quarto render scripts/<subdirectory>/XX_name.qmd --output-dir outs/<subdirectory>/XX_name/
```

For long-running Tier 2 analyses, consider rendering in a screen/tmux session.

### Next steps

- "Tree is ready. Want to visualize it? The tree-formatting skill handles layout,
  coloring, and clade collapsing."
- "Want to re-run with trimming / different model / PhyloBayes?"

---

## Optional Sensitivity Analyses

These are not part of the standard pipeline but can be added as additional chunks:

- **Dayhoff6 recoding:** Reduces 20 amino acids to 6 physicochemical groups. Tests
  whether topology is driven by compositional convergence. Run IQ-TREE with `-m GTR+R`
  on the recoded alignment.
- **AU topology test:** If competing hypotheses exist for specific nodes. Run IQ-TREE
  with `-zb 10000 -au`.

---

## Required Tools

| Tool | Purpose | Install |
|------|---------|---------|
| MAFFT | Alignment | `conda install -c bioconda mafft` |
| IQ-TREE 3 | Tree inference | `conda install -c bioconda iqtree` (ensure v3+) |
| BioPython | FASTA I/O, sequence handling | `pip install biopython` |
| CD-HIT | Redundancy reduction (optional) | `conda install -c bioconda cd-hit` |
| ClipKIT | Trimming (optional) | `pip install clipkit` |
| BMGE | Trimming (optional) | `conda install -c bioconda bmge` |
| PhyloBayes-MPI | Bayesian inference (optional) | `conda install -c bioconda phylobayes-mpi` |

---

## Key References

- Katoh & Standley (2013) MAFFT v7. Mol Biol Evol 30:772-780.
- Banos et al. (2024) GTRpmix: A linked GTR model for profile mixture models. Mol Biol Evol 41:msae174.
- Steenwyk et al. (2020) ClipKIT: a multiple sequence alignment trimming software. PLoS Biol 18:e3001007.
- Criscuolo & Gribaldo (2010) BMGE. BMC Evol Biol 10:210.
- Wang et al. (2017) PMSF model. Syst Biol 67:216-235.
- Lartillot et al. (2013) PhyloBayes-MPI. Syst Biol 62:611-615.
