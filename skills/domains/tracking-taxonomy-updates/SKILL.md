---
name: tracking-taxonomy-updates
description: Tracks and reconciles bacterial, archaeal, viral, and eukaryotic taxonomy changes across NCBI Taxonomy, GTDB, ICTV, and community eukaryote frameworks. Use when you need the most current proposals/ratifications/releases, or when you must assign taxonomy to sequences with explicit ranks, stable identifiers (NCBI taxids), provenance, and conflict flags.
---

# Tracking taxonomy updates

## When to use
Use this Skill when the user asks for any of:
- “latest / most recent” taxonomy proposals, ratifications, or consensus statements
- differences between **NCBI Taxonomy** and **GTDB**
- **ICTV** virus taxonomy standards (realms → species; MSL updates; binomial species naming)
- how to use **NCBI taxids**, lineages, and **TaxonKit**
- sequence→taxonomy assignment using **QuickClade**, **GTDB-Tk**, **EukCC**, **vConTACT3**

## Navigation
Read only what you need (progressive disclosure):
- **Authoritative sources to check (by domain)** → [reference/sources.md](reference/sources.md)
- **Ranks + identifiers (NCBI taxids, “no rank”, virus realms)** → [reference/ranks-and-identifiers.md](reference/ranks-and-identifiers.md)
- **Tool cheat sheets (QuickClade, GTDB-Tk, EukCC, vConTACT3, TaxonKit)** → [reference/tools.md](reference/tools.md)
- **Environment setup (Pixi; containers)** → [env/README.md](env/README.md)
- **Reporting templates** → [reference/report-template.md](reference/report-template.md)
- **QA checklist** → [reference/qa-checklist.md](reference/qa-checklist.md)
- **Last-verified examples (time-stamped; may be outdated)** → [reference/last-verified-snapshots.md](reference/last-verified-snapshots.md)

## Non-negotiables
- For every “most recent” claim: include **date** + **release/proposal identifier** + **authority** (NCBI/GTDB/ICTV/etc.).
- Never rely on names as join keys. Prefer **stable IDs** (NCBI taxid; GTDB genome identifiers; ICTV MSL IDs if present).
- Always capture **provenance** (tool version + database release + run date + command/settings).
- Preserve **no-rank clades** (don’t coerce into ranks).
- When sources disagree, **report both** and flag conflicts explicitly.

---

# Workflow A: Taxonomy update scan (proposals + consensus + releases)

Copy/paste this checklist and check items off in your response:

```
Taxonomy Update Scan
- [ ] A1. Define scope (domains + timeframe + output format)
- [ ] A2. Pull authoritative updates (NCBI/GTDB/ICTV/euk frameworks)
- [ ] A3. Extract versioned changes (what changed + date + identifier)
- [ ] A4. Identify pipeline impacts (ranks, names, IDs, joins)
- [ ] A5. Deliver a versioned summary table + action items
```

## A1. Define scope
Default scope if user is vague:
- Domains: Bacteria, Archaea, Viruses, Eukaryota
- Timeframe: last 12 months
- Output: 1-page summary + “what breaks/changes” for pipelines

## A2. Pull authoritative updates
Use [reference/sources.md](reference/sources.md). Prefer:
- committee ratifications (ICTV)
- database release notes / announcements (NCBI Taxonomy, GTDB)
- consensus framework papers (eukaryotes)

## A3. Extract “what changed” (versioned)
For each domain, capture:
- Authority/source (NCBI Taxonomy / GTDB / ICTV / UniEuk / etc.)
- Release / proposal / ratification identifier
- Release/ratification date (UTC date if available)
- Summary of changes (new ranks, renamed clades, reorganized lineages, binomialization)
- Known impacts (taxid merges/deletions, renamed high-level nodes, schema changes)

## A4. Pipeline impacts to always flag
- **Rank schema changes** (e.g., domain vs superkingdom; viral realm usage).
- **Name changes** that don’t change the underlying taxon (synonyms/aliases).
- **ID changes**: taxid merges/deletions (breaks downstream joins).
- **Virus species naming shifts** (binomialization) that break string matching.

## A5. Output format
Produce:
1) Short narrative (what changed + why it matters)
2) One table: domain × source × version/date × key changes × action items
3) Compatibility guidance (if requested): how to store both old/new labels and IDs

---

# Workflow B: Taxonomy assignment (sequence → taxonomy)

Copy/paste this checklist and check items off:

```
Taxonomy Assignment
- [ ] B1. Identify target domain (bac/arch/euk/virus/mixed)
- [ ] B2. Choose tool(s): QuickClade / GTDB-Tk / EukCC / vConTACT3
- [ ] B3. Run tools and capture raw outputs + tool/db versions
- [ ] B4. Normalize & enrich with NCBI taxids (TaxonKit) where applicable
- [ ] B5. Validate (cross-check sources, flag conflicts, record uncertainty)
- [ ] B6. Deliver a standardized results table + provenance
```

## B1. Identify target domain
Use evidence from:
- marker genes, known sample context, assembly stats
- a fast first-pass classifier (QuickClade), then confirm with domain-appropriate tools

## B2. Tool selection (rules of thumb)
- **Bacteria/Archaea genomes (MAGs/SAGs/isolate genomes)**: **GTDB-Tk** for genome-based taxonomy
- **Eukaryotic MAGs/genomes**: **EukCC** for QC + taxonomic context
- **Viruses**: **vConTACT3** to cluster and support taxonomic inference; interpret with ICTV standards
- **Fast screening for bins/contigs**: **QuickClade** (k-mer based)

See [reference/tools.md](reference/tools.md).

## B3. Environment guidance (preferred)
- **QuickClade**: run in the official BBTools container `bryce911/bbtools:39.65` (Docker or Apptainer).
- **GTDB-Tk / EukCC / vConTACT3 / TaxonKit**: manage dependencies with **Pixi** using [env/pixi.toml](env/pixi.toml).

See [env/README.md](env/README.md).

## B4. Normalize with NCBI taxids (when applicable)
Include:
- `ncbi_taxid`
- `scientific_name`
- `rank`
- `lineage_names` (semicolon-delimited)
- `lineage_taxids` (semicolon-delimited)

Use TaxonKit; treat merged/deleted taxid warnings as data-quality events.

See [reference/ranks-and-identifiers.md](reference/ranks-and-identifiers.md).

## B5. Validate and flag uncertainty
Flag **needs-review** when:
- GTDB and NCBI disagree at high ranks
- k-mer screening disagrees with marker-gene phylogeny
- viral contigs cluster ambiguously or lack hallmark genes
- taxids are merged/deleted or names are synonyms causing joins to fail

## B6. Standard output schema
Use the template in [reference/report-template.md](reference/report-template.md).

---

## References and templates
- Sources: [reference/sources.md](reference/sources.md)
- Tools: [reference/tools.md](reference/tools.md)
- IDs/ranks: [reference/ranks-and-identifiers.md](reference/ranks-and-identifiers.md)
- Environment: [env/README.md](env/README.md)
- QA: [reference/qa-checklist.md](reference/qa-checklist.md)
