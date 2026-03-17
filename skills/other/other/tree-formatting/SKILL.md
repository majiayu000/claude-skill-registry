---
name: tree-formatting
description: >
  Phylogenetic tree visualization and formatting with ggtree (R) or iTOL (web).
  Use when rendering a phylogenetic tree as a figure, choosing tree layout,
  coloring branches or labels by taxonomy, collapsing clades, displaying
  support values, or adding overlays to a tree. Do NOT load for tree inference
  (use protein-phylogeny skill) or domain annotation (future separate skill).
user-invocable: false
---

# Tree Formatting & Visualization

Conventions for rendering phylogenetic trees using **ggtree** (R/Bioconductor)
or **iTOL** (Interactive Tree of Life, web-based).

---

## Step 0: Choose Rendering Backend

Ask the user which backend to use based on their needs:

| Backend | Best for | Output | Language |
|---------|----------|--------|----------|
| **ggtree** | Publication figures, full programmatic control, offline use | PDF/PNG/SVG | R (.qmd script) |
| **iTOL** | Interactive exploration, quick iteration, web sharing, UI tweaking | Web + PDF/SVG/PNG exports | R (.qmd annotations) + Python (.qmd upload) |

### Backend comparison

| Feature | ggtree | iTOL |
|---------|--------|------|
| Interactive exploration | No | Yes (web UI) |
| Label alignment control | Full (programmatic) | Limited (UI toggle only, not via API) |
| Collapse triangle labels | Manual `geom_text()` | Built-in LABELS for internal nodes |
| Circular label positioning | Complex (manual angle computation) | Automatic |
| Branch length display | Yes (phylogram/cladogram toggle) | Yes (via UI) |
| Offline/reproducible | Fully offline | Requires iTOL API + internet |
| Two-script workflow | No (single .qmd) | Yes (R .qmd annotations + Python .qmd upload) |

---

## Step 1: Choose the Tree Type

Help the user select the right visualization. Ask about **purpose** and **tree size**,
then recommend from the options below.

### Tree type options

| Type | Best for | Tips | Key features |
|------|----------|------|-------------|
| **Collapsed rectangular phylogram** | Large family trees; showing branch-length variation and gene family structure | 250-2000+ | Collapsed pure clades, branch lengths, selective labels |
| **Collapsed rectangular cladogram** | Large family trees; topology focus, cleaner labels | 250-2000+ | Same as phylogram but no branch lengths, narrower page |
| **Collapsed circular** | Large trees; compact overview showing overall structure | 250-2000+ | Circular layout, collapsed clades, optional selective labels |
| **Simple rectangular phylogram** | Small-medium trees where all tips are readable | < 250 | All tips labeled, no collapsing needed |
| **Unrooted** | Networks, showing relationships without root assumption | Any | No directionality implied |

### Decision flow

1. **How many tips?**
   - < 250: Simple rectangular (all tips labeled)
   - 250+: Collapsed rectangular or circular — ask user preference
2. **Branch lengths meaningful?**
   - Yes -> phylogram option available
   - No / topology-only -> cladogram
3. **Layout**: Rectangular or circular? Often useful to produce both.
4. **Both phylogram and cladogram?** Often useful to produce both for rectangular trees.
5. **Which species to highlight?** -> Focal species list (see Step 2)

---

## Step 2: User Prompts (Ask Before Building)

Gather these decisions before writing any code:

1. **Rendering backend**: ggtree or iTOL? (see Step 0)
2. **Tree type**: Offer the relevant options from the table above based on tip count
3. **Collapsing strategy**: "Should pure clades be collapsed?
   (Recommended for trees with >100 tips.)"
   - **Which groups to collapse?** The `collapse_groups` parameter controls which
     taxonomic groups are eligible. Common choices:
     - `c("Bilateria")` — only collapse bilaterians (keeps sponges/cnidarians expanded)
     - `c("Bilateria", "Protostomia", "Deuterostomia")` — collapse specific groups
     - `NULL` — all groups eligible for collapsing
   - **Purity threshold**: 100% pure (strict) or 90%+ (relaxed)?
   - **Model species on triangles**: Collapsed triangles automatically list gene
     names of model species (human, mouse, fly, worm) inside them, e.g.,
     `"Bilateria (36 tips: LAMA1, LAMA2, LAMB1)"`. This ensures key gene family
     members remain visible even when the clade is collapsed.
   - **Never collapse by gene family** — unless eggNOG orthogroup data is available
4. **Labeling level**: "What level of tip labeling do you want?"
   - **No labels** — branch colors only (good for overview figures)
   - **All tips labeled** — every visible tip gets a label (good for small trees)
   - **Selective** — model species + focal species only (recommended for large trees)
5. **Focal species list** (if selective labeling): "Which non-model species should be
   individually labeled? Typically sponges + species with single-cell data
   (e.g., Hydra, Nematostella). Provide full species names."
6. **Rooting strategy**: "Midpoint root, or specify an outgroup?"
7. **Gene name resolution**: "Do tips include model species from non-Swiss-Prot
   sources (e.g., tr| entries, Ensembl, FlyBase, WormBase)? If so, we need to look
   up gene symbols." -> See **gene-lookup** skill for database-specific workflows.
8. **iTOL project** (if iTOL backend): "Which iTOL project should the tree go in?
   Name an existing project, or create a new one in the iTOL web UI
   (My Trees > New Project) and tell me the name." Set as `ITOL_PROJECT` env var
   or hardcode in the upload script.

---

## Step 3a: Build with ggtree

**All ggtree templates are Quarto `.qmd` documents** following the project's data
science conventions (YAML frontmatter with status field, git hash, BUILD_INFO.txt).

### Collapsed rectangular (phylogram / cladogram)

**Reference template**: `~/.claude/skills/tree-formatting/templates/ggtree/collapsed_rectangular.qmd`

This template is a complete, runnable `.qmd` with all tuned style parameters. Copy it
into the project's `scripts/` directory and adapt the sections marked PROJECT-SPECIFIC:
- File paths
- Tip label parsing functions (must match actual label formats in the tree)
- Taxonomy mapping (species -> group)
- Model and focal species lists
- `collapse_groups` parameter (which taxonomic groups to collapse)

The template handles: tree loading, midpoint rooting, pure-clade collapsing by
taxonomic group, branch coloring by taxonomy, all visible tips labeled, model species
gene names on collapsed triangle labels, formula-based page sizing, and PDF output.

**Key features:**
- **No branch capping** — branch lengths are never manipulated (this is a hard rule)
- **Formula-based page sizing** — `INCHES_PER_TIP = 0.12`, height = `max(8, n_visible * INCHES_PER_TIP)`
- **`collapse_groups` parameter** — controls which taxonomic groups are eligible for
  collapsing (e.g., `c("Bilateria")` to only collapse bilaterians, or `NULL` for all)
- **Model species gene names on triangles** — collapsed labels show
  `"Group (N tips: GENE1, GENE2, ...)"` so key gene family members remain visible
- **Collapse label positioning** — labels at `max(pre_data$x[tip_ids])` (triangle tip),
  not at internal node x (triangle base)

### Collapsed circular (overview and/or labeled)

**Reference template**: `~/.claude/skills/tree-formatting/templates/ggtree/collapsed_circular.qmd`

Same structure as rectangular — adapt PROJECT-SPECIFIC sections. Produces:
- **Circular overview** (no labels): 20" square page, branch colors only
- **Circular labeled** (selective labels): 28" square page, manually positioned labels

**Critical circular gotcha**: Labels must be positioned BEFORE `collapse()` is called.
The template handles this by computing angles from y-position (`y / max_y * 360`),
flipping text on the left half of the circle, and using `geom_text()` with explicit
angle/hjust values instead of `geom_tiplab2()`.

### Other tree types

For simple rectangular or unrooted trees, no template exists yet. Build from ggtree
basics:

```r
# Simple rectangular (all tips labeled)
p <- ggtree(tree) + geom_tiplab(size = 2)

# Unrooted
p <- ggtree(tree, layout = "unrooted")
```

**All style parameters are defined as named constants at the top of each template**
(e.g., `BRANCH_LINE_WIDTH`, `LABEL_SIZE`, `INCHES_PER_TIP`). Do not scatter
magic numbers through the code.

---

## Step 3b: Build with iTOL

### Two-script workflow

iTOL requires separate R and Python steps (do not mix in one `.qmd`):

1. **R script** — generates annotation files + relabeled Newick tree
2. **Python script** — uploads tree + annotations to iTOL, exports rendered images

### Annotation generation (R)

**Reference template**: `~/.claude/skills/tree-formatting/templates/itol/annotations.R`

Copy into project and adapt PROJECT-SPECIFIC sections. Generates these files:
- `GENE.tree` — relabeled Newick (short display labels, no `|` characters)
- `GENE_branch_colors.txt` — TREE_COLORS with clade + branch entries
- `GENE_label_colors.txt` — TREE_COLORS label color entries
- `GENE_collapse.txt` — COLLAPSE entries for pure clades
- `GENE_collapse_labels.txt` — LABELS for collapsed clade internal nodes

### Upload and export (Python)

**Reference template**: `~/.claude/skills/tree-formatting/templates/itol/upload_export.py`

Uploads two versions:
1. **Uncollapsed** — tree + branch colors + label colors (all tips visible)
2. **Collapsed** — tree + all annotations including collapse files

Exports multiple layout/format combinations (circular PDF/SVG/PNG, rectangular
PDF/SVG, unrooted PDF).

### iTOL API setup

- **API key**: iTOL > My Account > API access -> set as `ITOL_API_KEY` env var
- **Project**: set `ITOL_PROJECT` env var (default: "misc"). The project must
  already exist — **the iTOL API cannot create projects**, only the web UI can
  (My Trees > New Project). Prompt the user to create it if needed.
- **Paid subscription** required for full batch export API access

### After upload: always report links

After rendering the upload script, **always read the BUILD_INFO.txt** and report the
iTOL URLs back to the user in chat. These clickable links are essential for quick
iteration. Format:

```
**Uncollapsed:** http://itol.embl.de/external.cgi?tree=TREE_ID&restore_saved=1
**Collapsed:** http://itol.embl.de/external.cgi?tree=TREE_ID&restore_saved=1
```

---

## Tip Label Parsing (General Guidance)

Tip label formats vary substantially depending on data source. **Do not assume a
fixed format.** Inspect the actual tip labels first, then write parsing functions
tailored to what's present.

### Common formats

| Source | Example | Species part | ID part |
|--------|---------|-------------|---------|
| UniProt (sp) | `sp\|O95631\|NET1_HUMAN` | Suffix: `HUMAN` | Gene: `NET1` |
| UniProt (tr) | `tr\|Q23158\|Q23158_CAEEL` | Suffix: `CAEEL` | Accession: `Q23158` |
| Species\|taxid.acc | `Mus_musculus\|10090.Q9R1A3` | Before `\|` | After `taxid.` |
| Species\|acc | `Nematostella\|XP_032238380.2` | Before `\|` | After `\|` |
| BLAST-annotated | `Hydra\|8692.t25743aep_EHBP1_HUMAN_...` | Before `\|` | Transcript ID only |

### Key rules

- **Model species** (human, mouse, fly, worm): resolve to gene names via sp| labels
  or the **gene-lookup** skill for other databases
- **Non-model species**: use actual protein/transcript IDs only — **never** infer
  gene names from BLAST annotations
- **Display format**: `G._species_GENE_OR_ID` (e.g., `H._sapiens_SPTB1`,
  `E._muelleri_Em0014g869a`)

---

## Taxonomic Color Scheme

| Taxonomic Group | Hex |
|-----------------|-----|
| Demosponges | `#2ca02c` |
| Calcarea + Homoscleromorpha | `#98df8a` |
| Ctenophora | `#9467bd` |
| Cnidaria + Placozoa | `#ff7f0e` |
| Deuterostomia | `#d62728` |
| Protostomia | `#1f77b4` |
| Non-metazoan eukaryotes | `#555555` |
| Mixed (internal nodes) | `#999999` |

Species that are commonly misclassified:

| Species | Correct group | Notes |
|---------|---------------|-------|
| Thelohanellus_kitauei | Cnidaria + Placozoa | Myxozoan = cnidarian |
| Meara_stichopi, Waminoa | Deuterostomia | Xenacoelomorpha |
| Spadella_cephaloptera | Protostomia | Chaetognath |
| Monosiga, Salpingoeca | Non-metazoan | Choanoflagellates |

---

## Key ggtree Gotchas

These are hard-won lessons — do not skip:

1. **Pre-compute label positions BEFORE `collapse()`** — collapse modifies `p$data`
   coordinates. Extract x/y from `p$data` first. This applies to BOTH rectangular
   and circular layouts.

2. **Match on node column, not row index** — `p$data` rows may not be ordered by
   node ID. Always use `match(tip_node_ids, pre_data$node)`.

3. **Collapse label x-position: use `max(pre_data$x[tip_ids])`, NOT node x** —
   The internal node sits at the base of the collapsed triangle, but the label
   should appear at the triangle tip (where descendant tips extend to). Using the
   node x places labels at the triangle base, which looks wrong.

4. **Never cap branch lengths** — Branch lengths represent real evolutionary
   distances. Capping or truncating them is data manipulation. If long branches
   compress internal structure, offer a cladogram as the honest alternative.

5. **Circular labels: use `geom_text()` with manual angles, NOT `geom_tiplab2()`** —
   compute angles as `y / max_y * 360`, flip text on left half (`angles > 90 & < 270`),
   and pass angle/hjust outside `aes()`.

6. **`show.legend = FALSE` on `geom_text`** — prevents "a" character artifacts
   appearing in the color legend.

7. **`branch.length = "none"` for cladogram** — cannot pass `NULL`. Must use
   if/else to conditionally include this argument.

8. **`coord_cartesian(clip = "off")`** — required for rectangular labels that extend
   beyond the plot area. Pair with wide right margin. Not needed for circular.

9. **Daylight layout** — produces unusable output for large trees (branches crossing,
   triangles overlapping). Avoid it.

10. **Page sizing formula** — Use `INCHES_PER_TIP = 0.12` with
    `PAGE_HEIGHT = max(8, n_visible * INCHES_PER_TIP)` where `n_visible` counts
    non-collapsed tips plus collapsed triangles. This formula keeps labels readable
    without excess whitespace. Hardcoded page sizes invariably need adjustment.

11. **Never collapse by gene family** — Unless eggNOG orthogroup data is available
    to intelligently define ortholog groups, only collapse by taxonomic group.
    Gene families within a tree are the object of study, not noise to be hidden.

---

## Key iTOL Gotchas

Hard-won lessons from iTOL annotation file development:

1. **Tip labels must NOT contain `|` characters** — iTOL uses `|` as the MRCA
   separator in TREE_COLORS clade entries (`tipA|tipB clade ...`), COLLAPSE entries,
   and LABELS internal node entries. If tip labels contain `|`, all clade/collapse
   specifications silently break (wrong MRCA selected, or entries ignored entirely).
   **Solution**: relabel tips to short display names before writing the Newick tree.

2. **`ape::write.tree()` converts spaces to underscores** — display labels must use
   underscores from the start (`H._sapiens_SPTN2` not `H. sapiens SPTN2`), or
   annotation file IDs will not match the tree.

3. **`itol.toolkit` R package is incompatible with `|` in tip labels** — the toolkit
   also uses `|` internally and cannot escape it. Write annotation files manually
   (plain text with TAB separator) instead of using `itol.toolkit`.

4. **MRCA pair selection**: to specify an internal node, provide one tip from each
   child subtree (`tipA|tipB`). Using `tips[1]` and `tips[N]` (first/last by array
   index) can give two tips from the same child, which specifies a different MRCA.

5. **Label alignment is NOT controllable via batch export API** — the "Align tip
   labels" toggle is UI-only. The `label_display` export parameter controls
   visibility (0=hide, 1=show) but not alignment. Users must toggle alignment
   manually in the iTOL web interface.

6. **Collapsed triangle labels** — use LABELS annotation type with MRCA specification
   (`tipA|tipB\tLabel text`). These render as the displayed name on collapsed
   triangles.

7. **Two uploads for collapsed vs uncollapsed** — upload annotation files are baked
   into the tree on upload. To have both an uncollapsed and collapsed version,
   upload twice: once without collapse files, once with all files.

---

## Related Skills

- **protein-phylogeny:** Inference pipeline that produces the tree
- **gene-lookup:** Resolve accessions to gene symbols across databases (UniProt,
  Ensembl, FlyBase, WormBase, etc.)
- **Pfam domain annotation (future):** Domain annotations for overlay
