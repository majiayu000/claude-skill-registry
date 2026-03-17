---
name: gene-lookup
description: >
  Look up gene or protein information from biological database IDs and accessions.
  Use when working with gene IDs, protein accessions, or identifiers from UniProt,
  Ensembl, FlyBase, WormBase, NCBI/RefSeq, or similar databases. Covers: identifying
  what database an ID comes from, converting IDs to gene symbols or names, retrieving
  protein function or annotation, batch querying APIs, and cross-referencing between
  databases. Use whenever someone asks "what gene is this", "look up this protein",
  "get info on these accessions", or needs to map between identifier systems. Also
  use for phylogenetic tree tip label gene name resolution.
user-invocable: false
---

# Gene / Protein ID Lookup

Resolve accessions to gene symbols across biological databases. Add new databases
as we encounter them.

---

## When to Use

- Tree tip labels contain accessions instead of gene symbols (e.g., `tr|Q9R1A3|...`)
- Need gene names for model species in a phylogenetic tree
- Building an `accession_gene_map.tsv` for the tree-formatting skill
- Any analysis where you have protein/gene IDs and need readable gene symbols

---

## Quick ID Detection

Identify the database from the accession pattern:

| Pattern | Database | Example |
|---------|----------|---------|
| `sp\|ACC\|GENE_SPECIES` | UniProt Swiss-Prot | `sp\|O95631\|NET1_HUMAN` |
| `tr\|ACC\|ACC_SPECIES` | UniProt TrEMBL | `tr\|Q23158\|Q23158_CAEEL` |
| 6-10 alphanum (e.g., `Q9R1A3`) | UniProt accession | `A0A8C1NMY5` |
| `ENS[species]G\d{11}` | Ensembl gene | `ENSG00000139618`, `ENSMUSG00000017146` |
| `ENS[species]P\d{11}` | Ensembl protein | `ENSP00000369497`, `ENSDARP00000012345` |
| `ENS[species]T\d{11}` | Ensembl transcript | `ENST00000380152` |
| `FBgn\d{7}` | FlyBase gene | `FBgn0000490` |
| `FBpp\d{7}` | FlyBase polypeptide | `FBpp0082828` |
| `FBtr\d{7}` | FlyBase transcript | `FBtr0083387` |
| `WBGene\d{8}` | WormBase gene | `WBGene00006763` |
| `CE\d+` | WormBase protein | `CE28580` |
| `XP_\d+\.\d+` | NCBI RefSeq predicted protein | `XP_032238380.2` |
| `NP_\d+\.\d+` | NCBI RefSeq curated protein | `NP_000537.3` |
| `XM_\d+\.\d+` / `NM_\d+\.\d+` | NCBI RefSeq mRNA | `NM_000546.6` |

---

## General Workflow

1. **Identify which accession types are present** — inspect labels, match patterns above
2. **Swiss-Prot entries (sp|) already have gene names embedded** — parse directly
   from the label: `sp|O95631|NET1_HUMAN` → gene = `NET1`
3. **Other entries need API lookup** — batch-query the appropriate database (see below)
4. **Save results to TSV** — `accession_gene_map.tsv` with columns:
   `accession`, `gene_name` (and optionally `database`, `species`)
5. **Load TSV in downstream scripts** — tree-formatting templates read this file

---

## Database: UniProt

### ID patterns
- `sp|ACC|GENE_SPECIES` or `tr|ACC|ACC_SPECIES` in tip labels
- Bare accessions: 6-10 alphanumeric (e.g., `Q9R1A3`, `A0A8C1NMY5`)

### Lookup
- `sp|` entries: gene name embedded in label — parse directly, no API needed
- `tr|` entries and bare accessions: REST API batch query

```r
# Batch up to ~200 accessions per request
query_str <- paste0("(", paste0("accession:", accessions, collapse = " OR "), ")")
url <- paste0(
  "https://rest.uniprot.org/uniprotkb/search?",
  "query=", URLencode(query_str, reserved = TRUE),
  "&fields=accession,gene_primary&format=tsv&size=500"
)
result <- read.delim(url(url), stringsAsFactors = FALSE)
# Columns: "Entry" (accession), "Gene.Names..primary." (gene symbol)
```

### UniProt ID Mapping Service
For cross-database conversions (e.g., FBgn → UniProt, WBGene → UniProt):
- POST to `https://rest.uniprot.org/idmapping/run` with `from`, `to`, `ids`
- Poll `https://rest.uniprot.org/idmapping/status/{jobId}`
- Supports `from=FlyBase`, `from=WormBase`, `to=UniProtKB`
- Up to 100,000 IDs per job

### Notes
- Rate limit: ~100 requests/minute
- For >500 accessions, paginate or split into multiple queries

---

## Database: Ensembl

### ID patterns
`ENS` + optional species code + feature type letter + 11 digits.

| Species | Gene | Protein |
|---------|------|---------|
| Human | `ENSG00000000000` | `ENSP00000000000` |
| Mouse | `ENSMUSG00000000000` | `ENSMUSP00000000000` |
| Zebrafish | `ENSDARG00000000000` | `ENSDARP00000000000` |
| Chicken | `ENSGALG00000000000` | `ENSGALP00000000000` |
| Ciona | `ENSCING00000000000` | `ENSCINP00000000000` |

Ensembl Metazoa species (Amphimedon, Nematostella, etc.) use the same REST API.

### Lookup
**Base URL:** `https://rest.ensembl.org`

**Gene IDs → symbol (1 batch call):**
- POST `/lookup/id` with `{"ids": ["ENSG...", ...]}` (max 1000 per request)
- Gene symbol is in `display_name` field

**Protein IDs → symbol (2 batch calls):**
Protein (Translation) objects have NO `display_name`. Must chain through parents:
1. POST protein IDs → get `Parent` transcript IDs
2. POST transcript IDs → get `display_name` (format: `GENE-NNN`, e.g., `BRCA2-201`)
3. Strip isoform suffix: `sub("-\\d+$", "", display_name)`

```r
# Batch POST (up to 1000 IDs)
resp <- httr2::request("https://rest.ensembl.org") |>
  httr2::req_url_path("lookup", "id") |>
  httr2::req_headers("Content-Type" = "application/json",
                     "Accept" = "application/json") |>
  httr2::req_body_json(list(ids = id_vector)) |>
  httr2::req_perform()
results <- httr2::resp_body_json(resp)
```

### Gotchas
- **Protein IDs return no gene symbol** — must chain through Parent transcript
- **`expand=1` fails on protein IDs** — returns `null`
- **Batch returns `null` for unknown IDs** — handle gracefully
- **Rate limit: 55,000 requests/hour** (no API key needed)
- Both versioned (`ENSG...19`) and unversioned IDs accepted

---

## Database: FlyBase

### ID patterns
`FBgn`, `FBpp`, `FBtr` + 7-digit zero-padded number (e.g., `FBgn0000490`).

### Lookup
**Best approach: FlyBase precomputed bulk file** (not the API — it lacks ID-to-symbol
endpoints and is unreliable).

**For FBgn only** — lightweight file:
```
https://s3ftp.flybase.org/releases/current/precomputed_files/genes/fbgn_annotation_ID_fb_YYYY_NN.tsv.gz
```
Columns: `gene_symbol`, `organism_abbreviation`, `primary_FBgn#`, ...

**For FBgn, FBtr, AND FBpp** — expanded file (needed for polypeptide IDs):
```
https://s3ftp.flybase.org/releases/current/precomputed_files/genes/fbgn_fbtr_fbpp_expanded_fb_YYYY_NN.tsv.gz
```
Columns: `gene_ID`, `gene_symbol`, `transcript_ID`, `polypeptide_ID`, ...
~36K rows. Download once, cache locally.

**R/Bioconductor alternative** (FBgn only):
```r
library(org.Dm.eg.db)
symbols <- AnnotationDbi::mapIds(org.Dm.eg.db,
  keys = fbgn_ids, column = "SYMBOL", keytype = "FLYBASE")
```
Use `keytype = "FLYBASE"` (not `"ENSEMBL"`) for FBgn IDs.

**UniProt ID mapping** also works for FBgn → gene symbol (via `from=FlyBase`,
`to=UniProtKB`), but does NOT work for FBpp or FBtr.

### Gotchas
- **FlyBase REST API has no ID-to-symbol endpoint** — use bulk files instead
- **`Dmel\` prefix**: FlyBase uses species prefixes for non-melanogaster genes
  (e.g., `Dvir\Dfd`). In UniProt, Drosophila gene names sometimes carry
  `Dmel\` prefix — strip with `sub("^Dmel\\\\", "", gene)`
- **Case conventions**: lowercase initial = recessive phenotype (e.g., `dpp`),
  uppercase initial = dominant or molecular function (e.g., `Abd-B`)
- **Bulk files update ~6x/year** — `current` URL alias always points to latest

---

## Database: WormBase

### ID patterns
- Gene: `WBGene` + 8-digit zero-padded number (e.g., `WBGene00006763`)
- Protein: `CE` + digits (e.g., `CE28580`)
- Sequence names (cosmid-based): e.g., `JC8.10`, `C15F1.7`

### Lookup
**Best approach: WormBase ParaSite REST API** (has batch support, works for all
nematode species).

```
POST https://parasite.wormbase.org/rest-19/lookup/id
Content-Type: application/json
Accept: application/json

{"ids": ["WBGene00006763", "WBGene00004930"]}
```

- Max 1000 IDs per request
- Gene symbol is in `display_name` field (e.g., `unc-26`, `sod-1`)
- Use versioned URL (`rest-19`) or follow 307 redirect from `/rest/`

**For richer per-gene data** (aliases, descriptions), use the WormBase REST API:
```
GET https://rest.wormbase.org/rest/field/gene/WBGene00006763/name
```
Returns `data.label` = gene symbol. No batch support — single-gene queries only.

### Gotchas
- **C. elegans naming**: 3-4 lowercase letters + hyphen + number (e.g., `unc-26`,
  `spc-1`). Letter prefix is the "gene class" from mutant phenotype
- **Genes without standard names** use cosmid/sequence names (e.g., `JC8.10`)
- **UniProt ID mapping** (`from=WormBase`) works for WBGene IDs but is a multi-step
  process — ParaSite is simpler
- `from=WBParaSite` does NOT work with WBGene IDs in UniProt ID mapping

---

## Database: NCBI / RefSeq

### ID patterns
`PREFIX_DIGITS.VERSION`:

| Prefix | Type | Example |
|--------|------|---------|
| `XP_` | Predicted protein | `XP_032238380.2` |
| `NP_` | Curated protein | `NP_000537.3` |
| `XM_` | Predicted mRNA | `XM_032382489.2` |
| `NM_` | Curated mRNA | `NM_000546.6` |

Both versioned and unversioned forms accepted by NCBI APIs.

### Lookup
**Best approach: NCBI Datasets API** (single GET, clean JSON — much simpler than
E-utilities).

```
GET https://api.ncbi.nlm.nih.gov/datasets/v2/gene/accession/{comma_separated_accessions}
```

- Gene symbol in `reports[].gene.symbol`
- Also returns `gene_id`, `description`, `taxname`
- Batch: comma-separate accessions in URL (~400 per request due to URL length)
- Accepts XP_, NP_, XM_, NM_ directly

```r
url <- paste0(
  "https://api.ncbi.nlm.nih.gov/datasets/v2/gene/accession/",
  paste(accessions, collapse = ",")
)
resp <- httr2::request(url) |>
  httr2::req_headers(Accept = "application/json") |>
  httr2::req_perform()
body <- httr2::resp_body_json(resp)
# body$reports[[i]]$gene$symbol
```

### Gotchas
- **Use Datasets API, not E-utilities** — E-utilities requires multiple steps
  (ESearch → ELink → ESummary) and XML parsing
- **Rate limits**: 5 req/sec without API key, 10 req/sec with key
- **API key**: register at `https://account.ncbi.nlm.nih.gov/settings/`, pass via
  `?api_key=KEY` parameter
- **Non-model organisms** may return `LOC` + number as gene symbol (e.g.,
  `LOC5512993` for Nematostella) — this means no official symbol assigned

---

## Output Format

All lookups should produce a TSV file (`accession_gene_map.tsv`) with at minimum:

```
accession	gene_name
Q9R1A3	Sptbn1
Q23158	unc-70
Q9VZU3	betaSpec
XP_032238380.2	LOC5512993
```

Optional extra columns: `database`, `species`, `gene_id`.

The tree-formatting templates load this file automatically:
```r
gene_map <- read.delim(file.path(out_dir, "accession_gene_map.tsv"))
acc_to_gene <- setNames(gene_map$gene_name, gene_map$accession)
```

---

## Related Skills

- **tree-formatting:** Consumes gene_map TSV for tip labeling
- **protein-phylogeny:** May produce trees with mixed accession formats
