---
name: Ancient Near East Research
description: >
  Academic research skill for Biblical Hebrew, Semitic linguistics, cuneiform studies,
  and comparative Ancient Near Eastern research. Provides Sefaria API for Hebrew Bible,
  CDLI/ORACC for cuneiform databases, and web discovery via Omnisearch, Exa, Firecrawl,
  and Obscura for finding scholarly sources across JSTOR, Perseus, Persée, Google Scholar,
  and academia.edu. Triggers on Hebrew quotes, cuneiform, Sefaria, ANE research, Minoan,
  search for scholarship, find papers, literature review, scholarly search, academic search,
  Genesis/Tehom, Ugaritic, Talmudic sources, extract from PDF, OCR academic.
---

## Additional Triggers

This skill should also be activated for:
- **Gnostic/Orphic**: "Nag Hammadi", "Sethian", "Gnostic", "Orphic", "On the Origin of the World", "demiurge"
- **Etymology**: "purple etymology", "tip'eret", "p-r root", "Membliaros", "Kadmos", "Europa"
- **Minoan parallels**: "Moses-Minos", "Bezalel-Daedalus", "Kaphtor", "Caphtor", "Linear A"
- **OCR/tools**: "extract from PDF", "OCR academic", "compile quotations", "theme categorization"
- **Paper research**: "Thera eruption", "Tempest Stela", "primordial waters", "Gaza as Minoa", "Manat"
- **JSTOR**: "search JSTOR", "JSTOR article", "download from JSTOR", "saved articles", "academic database"
- **Web Discovery**: "find papers about", "search for scholarship", "literature search", "Google Scholar", "academic search", "find sources", "discover research", "omnisearch", "Exa search"
- **Source Extraction**: "extract from URL", "scrape academic page", "stealth fetch", "parse PDF URL", "get abstract from JSTOR"

# Ancient Near East Research

Academic research assistant for Biblical Hebrew, Semitic linguistics, and comparative Ancient Near Eastern studies.

## Core Capabilities

1. **Sefaria API** - Fetch Hebrew Bible passages with vocalization, translations, and commentaries
2. **Hebrew Text Handling** - Proper display of Hebrew with cantillation marks (טעמים)
3. **Cross-referencing** - Link Biblical texts to Talmud, Midrash, and commentaries
4. **Citation Formatting** - Academic citation styles for primary sources
5. **Cuneiform Databases** - Access CDLI and ORACC for Akkadian/Sumerian primary sources

## Sefaria API Usage

### Fetching Texts

To retrieve a passage, use the Sefaria API endpoint:

```
https://www.sefaria.org/api/v3/texts/{reference}
```

**Reference Format:**
- Book names: `Genesis`, `Exodus`, `Isaiah`, `Psalms`, etc.
- Chapters/verses: Use periods as separators: `Genesis.1.1-3`
- Ranges: `Genesis.1.1-2.4` (chapter 1 verse 1 through chapter 2 verse 4)

**Examples:**
- `Genesis.1.1-3` - Genesis 1:1-3
- `Exodus.20.1-17` - The Ten Commandments
- `Isaiah.45.7` - Isaiah 45:7
- `Psalms.104` - Full chapter

### Running the Fetch Script

For formatted output with Hebrew text and translation:

```bash
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_sefaria.py "Genesis 1:1-3"
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_sefaria.py "Exodus 20:2" --hebrew-only
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_sefaria.py "Isaiah 45:7" --with-rashi
```

### Direct API Calls

```bash
# Basic verse fetch
curl -s "https://www.sefaria.org/api/v3/texts/Genesis.1.2"

# Search for Hebrew term
curl -s "https://www.sefaria.org/api/search-wrapper?query=תהום&type=text&filters=Tanakh"
```

### Key Passages for ANE Comparative Research

See `references/hebrew-passages.md` for detailed passage tables and commentaries.

**Core passages:** Genesis 1:2 (Tehom), Isaiah 27:1 (Leviathan), 1 Kings 18:19 (Asherah), Amos 9:7 (Caphtor)

## Cuneiform Database Resources

See `references/cuneiform-databases.md` for CDLI/ORACC API details and script commands.

**Quick access:**
- CDLI: `https://cdli.earth/artifacts/{P-number}.json`
- ORACC: `https://oracc.museum.upenn.edu/{project}/corpusjson/{P-number}.json`
- Key P-number: P480701 = Enuma Elish composite

## Web Discovery & Source Extraction

### Source Escalation Ladder

| Tier | Tool | When | ANE Examples |
|------|------|------|--------------|
| 0 | Sefaria / CDLI / ORACC | Known reference, free structured data | Genesis 1:2, P480701, deity lookup |
| 1 | Omnisearch `--academic` | Broad discovery, unknown sources | "Minoan Semitic connections Bronze Age" |
| 2 | Exa `--category "research paper"` | Domain-filtered neural search | `--domains jstor.org,persee.fr` |
| 3 | Firecrawl `scrape` / `parse` | Page extraction, PDF-to-markdown | Known URL, remote PDF |
| 4 | Obscura `ane_stealth_fetch.sh` | Bot-protected sites | JSTOR, Scholar, Persée |
| 5 | Scrapling | Cloudflare Turnstile | Last resort |

### Tier 1: Omnisearch (Broad Discovery)

When the omnisearch skill is available, use it as the entry point for finding new scholarship. The `--academic` flag routes to Exa's research paper index.

```bash
# Broad ANE topic discovery
python3 ~/.claude/skills/omnisearch/scripts/omnisearch.py "Minoan Semitic linguistic connections" --academic

# Parallel multi-provider search for corroboration
python3 ~/.claude/skills/omnisearch/scripts/omnisearch.py "Thera eruption Tempest Stela" --parallel --no-text

# News about recent archaeological finds
python3 ~/.claude/skills/omnisearch/scripts/omnisearch.py "Knossos excavation 2025" --news
```

### Tier 2: Exa Neural Search (Domain-Filtered)

Direct Exa search with ANE-specific domain lists and the `research paper` category. Use when omnisearch is unavailable or when more control over domains and filtering is needed.

```bash
python3 ~/.claude/skills/exa-search/scripts/exa_search.py "Asherah cult Ugarit" \
  --category "research paper" \
  --domains jstor.org persee.fr perseus.tufts.edu academia.edu \
  -n 20 --no-text
```

**ANE Domain List:**

| Domain | Content |
|--------|---------|
| jstor.org | Journals: BASOR, JBL, JNES, JAOS, VT, IEJ |
| persee.fr | French academic: BCH, Syria, RHR |
| academia.edu | Pre-prints and working papers |
| perseus.tufts.edu | Classical texts (Greek, Latin primary sources) |
| sefaria.org | Hebrew Bible and rabbinic literature |
| cdli.earth | Cuneiform Digital Library |
| oracc.museum.upenn.edu | Open Richly Annotated Cuneiform Corpus |
| etana.org | Electronic Tools and ANE Archives |
| asor.org | American Schools of Oriental Research |

**Pre-Built ANE Search Queries:**

| Theme | Query |
|-------|-------|
| Thera | `"Thera eruption" OR "Santorini eruption" Bronze Age` |
| Knossos | `"Knossos palace" OR "Minoan archaeology" ritual` |
| Minos | `"Moses Minos" OR "Daedalus Bezalel" OR "Minoan law"` |
| Palestine | `"Asherah Ugarit" OR "Athirat" OR "Tehom Tiamat"` |
| Linguistics | `"Semitic etymology" OR "Hellenosemitica" OR "begadkephat"` |

**Similar Page Discovery:**

```bash
python3 ~/.claude/skills/exa-search/scripts/exa_similar.py \
  "https://www.jstor.org/stable/528927" \
  --category "research paper" -n 15
```

### Tier 3: Firecrawl (Page Extraction & PDF Parsing)

For extracting content from known URLs and parsing remote PDFs.

```bash
# Scrape an academic page
firecrawl scrape "https://www.persee.fr/doc/..." --only-main-content

# Parse a remote PDF (Fire-PDF v2.9)
python3 ~/.claude/skills/firecrawl/scripts/firecrawl_api.py scrape \
  "https://example.com/paper.pdf" --pdf-mode auto

# Search + scrape in one operation
firecrawl search "Cyrus Gordon Minoan Semitic" --scrape --limit 10
```

### Tier 4: Obscura Stealth Extraction (Bot-Protected Sites)

For JSTOR, Google Scholar, Persée, Perseus, and Academia.edu. Extracts publicly visible metadata and abstracts — not for bypassing paywalls.

```bash
# Auto-detect site type from URL
bash ~/.claude/skills/ancient-near-east-research/scripts/ane_stealth_fetch.sh URL

# Google Scholar search
bash ~/.claude/skills/ancient-near-east-research/scripts/ane_stealth_fetch.sh \
  "https://scholar.google.com/scholar?q=minoan+semitic+etymology" scholar
```

Supported site types: `scholar`, `pubmed`, `jstor`, `persee`, `perseus`, `academia`, `cdli`, `oracc`, `sefaria`, `general`

See `references/obscura-ane-patterns.md` for site-specific extraction patterns and gotchas.

### Complete Research Pipeline

```
Topic Question
    ↓
Tier 0: Check Sefaria / CDLI / ORACC (known references)
    ↓
Tier 1: Omnisearch --academic (broad discovery, titles only)
    ↓
Tier 2: Exa --category "research paper" --domains [ANE list] (focused search)
    ↓
Pick URLs → Tier 3: Firecrawl scrape / parse (extract content)
    ↓
Bot-blocked? → Tier 4: Obscura ane_stealth_fetch.sh (stealth extraction)
    ↓
PDF downloaded → Mistral OCR → Quotations DB → Themed Compilation
```

## Akkadian Terms and Enuma Elish

See `references/akkadian-terms.md` for comprehensive Akkadian terminology, Enuma Elish passages, and Hebrew-Akkadian cognate pairs.

**Key cognate:** תְּהוֹם (Tehom) ↔ Ti'āmat

## Research Context

This skill supports comparative research across:

- **Minoan-Aegean**: Palace culture, goddess worship, Thera eruption
- **Ugaritic-Canaanite**: Athirat/Asherah, Yamm/Sea mythology, Ba'al cycle
- **Babylonian**: Tiamat/Enuma Elish, primordial waters cosmology
- **Biblical Hebrew**: Genesis creation, Tehom/Tiamat cognate, Leviathan
- **Semitic Etymology**: Astour (Kadmos, Europa, Membliaros), Gordon (Moses-Minos, Daedalus-Bezalel)

See `references/gordon-papers/gordon-findings.md` for Gordon's Minoan-Semitic connections.

## Translation Philosophy

**Always be literal.** Preserve Hebrew terms rather than translating to generic English equivalents. This maintains etymological connections crucial for comparative ANE research.

| Hebrew | Literal | NOT Generic |
|--------|---------|-------------|
| אֱלֹהִים | Elohim | God |
| יהוה | YHWH | the LORD |
| תְּהוֹם | Tehom | the deep |
| תְּהֹמוֹת | Tehomot | the depths |
| תַּנִּינִים | Tanninim | sea monsters |
| לִוְיָתָן | Leviathan | — |
| רוּחַ אֱלֹהִים | Ruach Elohim / Spirit of Elohim | Spirit of God |

This approach preserves the cognate relationships (Tehom ↔ Tiamat, Tanninim ↔ Ugaritic tnn) that are obscured by conventional translations.

## Classical Phoenician/Ugaritic Pronunciation

For etymological analysis, use pre-begadkephat pronunciation (פ as /p/ not /f/):

| Hebrew | Modern | Classical | Significance |
|--------|--------|-----------|--------------|
| תִּפְאֶרֶת | tif'eret | *tip'art* | Connects to πορφύρα via p-r root |
| כַּפְתּוֹר | Kaftor | *Kaptaru* | = Caphtor = Crete |
| פָּרוֹכֶת | parokhet | *parukatt* | Temple veil, cognate analysis |

This preserves etymological connections obscured by later pronunciation shifts (e.g., tip'eret → purpura).

## Output Formatting

When presenting Hebrew text in research:

```
בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ
"In the beginning Elohim created the heavens and the earth" (Genesis 1:1)
```

For academic citations:
- Hebrew Bible: Book Chapter:Verse (e.g., Gen 1:2)
- With Hebrew: Include original + transliteration when relevant
- Commentaries: Rashi on Genesis 1:2, s.v. "תהום"

## Integration with Research Workflow

This skill connects to the quotations compilation system at:
`~/Desktop/Athirat, Knossos, & Minos/`

Generated quotations can be added to the themed compilation by:
1. Saving output as markdown in the `Snippets/` directory
2. Adding `**Category: [Theme]**` header (Thera, Knossos, Minos, Palestine, Linguistics)
3. Running `python3 compile_themed_quotations.py`

## Resources

### Scripts

- `scripts/fetch_sefaria.py` - Fetch Hebrew Bible passages with translations and commentaries
- `scripts/fetch_cuneiform.py` - Access CDLI and ORACC cuneiform databases
- `scripts/fetch_jstor.py` - JSTOR browser automation (search, saved articles, PDF download)
- `scripts/compile_quotations.py` - Compile themed quotation documents (5-theme categorization)
- `scripts/ane_stealth_fetch.sh` - Stealth fetch wrapper for 10 academic site types (Scholar, JSTOR, Persée, Perseus, CDLI, ORACC, Sefaria, PubMed, Academia, general)
- `scripts/ocr_academic_pdf.py` - Extract text from academic PDFs using Marker OCR
- `scripts/mistral_ocr_pdf.py` - High-accuracy OCR using Mistral Pixtral-Large (94.89% accuracy on scanned docs)

### Mistral OCR Usage

Convert PDFs to Markdown using Mistral's Pixtral vision model:

```bash
# Basic usage (requires MISTRAL_API_KEY env var)
python3 ~/.claude/skills/ancient-near-east-research/scripts/mistral_ocr_pdf.py document.pdf

# Specify output file
python3 ~/.claude/skills/ancient-near-east-research/scripts/mistral_ocr_pdf.py document.pdf -o output.md

# OCR specific pages
python3 ~/.claude/skills/ancient-near-east-research/scripts/mistral_ocr_pdf.py document.pdf --pages 1-50

# Process large PDFs in chunks (requires PyMuPDF)
python3 ~/.claude/skills/ancient-near-east-research/scripts/mistral_ocr_pdf.py large.pdf --chunked --chunk-size 20
```

**Requirements:** `uv pip install mistralai --system` (and `PyMuPDF` for chunked mode)

### References

- `references/sefaria_api.md` - Complete Sefaria API documentation
- `references/source-directories.md` - Filesystem locations for source materials and tools
- `references/categorization-keywords.md` - Theme keywords for quotation auto-categorization
- `references/obscura-ane-patterns.md` - Site-specific Obscura extraction patterns for ANE academic sites
- `references/gordon-papers/` - Cyrus H. Gordon's Minoan-Semitic research
  - `gordon-findings.md` - Summary of key findings (Moses-Minos, Daedalus-Bezalel, Ida footstool)
  - `Ugarit-and-Caphtor.pdf`, `Gordon-Minoica-1962.pdf`, `Gordon-DeciphermentMinoanEteocretan-1975.pdf`
- `references/drafts/` - Working paper drafts (gnostic-reception-genesis.md, gordon-findings.md)

## Active Paper Project

This skill supports a 3-part academic paper series: **"Thera, Knossos, and Minos: Minoan-Semitic Connections in the Ancient Mediterranean"**

**Part I: Thera** (in progress): Thera eruption → Greek sources → Astour's etymologies → Tehom-Tiamat → Athirat of the Sea → Thera the Goddess → purple etymology (tip'eret)
**Part II: Knossos/Knossot** (planned): Palace culture, Linear A, Daedalus-Bezalel, kaftôrîm, priestess traditions
**Part III: Minos/Manna/Moses** (planned): Moses-Minos parallels, law-giver traditions, Gaza as Minoa, Manat the Goddess

Active repo: `~/Desktop/Thera-Knossos-Minos-Paper/`

## Cuneiform Script Usage

See `references/cuneiform-databases.md` for full script commands and ORACC project reference.

**Quick commands:**
```bash
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_cuneiform.py cdli P480701
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_cuneiform.py deity tiamat
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_cuneiform.py oracc-projects
```

## JSTOR Browser Automation

> **Prefer Obscura stealth fetch (Tier 4) or Exa search (Tier 2) for JSTOR metadata and abstracts.** This script is retained for cases requiring authenticated full-text download.

Access JSTOR scholarly database using browser automation via `agent-browser`. Requires a JSTOR account with download privileges.

See `references/jstor-research.md` for URL patterns and search strategies.

### First-Time Setup

Authenticate with JSTOR (opens browser for manual login):

```bash
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_jstor.py login
```

Auth state is saved to `~/.jstor-auth.json` and reused for subsequent commands.

### JSTOR Commands

```bash
# Check authentication status
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_jstor.py status

# Search for articles
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_jstor.py search "minoan semitic etymology" -n 20

# List saved articles (My Library)
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_jstor.py saved

# List recently read articles
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_jstor.py recent

# Get article metadata
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_jstor.py article https://jstor.org/stable/12345

# Download PDF to specified directory
python3 ~/.claude/skills/ancient-near-east-research/scripts/fetch_jstor.py download https://jstor.org/stable/12345 -o ~/sources/
```

### Research Pipeline

JSTOR integrates with the existing OCR and quotations workflow:

```
JSTOR Search → Download PDFs → Mistral OCR → Quotations DB → RAG Dossiers
```

**Example workflow:**
```bash
# 1. Search JSTOR
python3 fetch_jstor.py search "Cyrus Gordon minoan" --json > results.json

# 2. Download interesting article
python3 fetch_jstor.py download https://jstor.org/stable/528927 -o ~/sources/gordon/

# 3. OCR the PDF
python3 mistral_ocr_pdf.py ~/sources/gordon/jstor-528927.pdf -o ~/sources/gordon/article.md

# 4. Extract quotations and add to database
```
