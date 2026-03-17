---
name: book-biography
description: Bibliographic research agent for analyzing books and manuscripts. Builds comprehensive "book biographies" showing production context, textual transmission, related editions, and scholarly networks. Use when asked to research a book's history, find related editions, analyze manuscript transmission, or build bibliographic context.
---

# Book Biography

Bibliographic research agent that analyzes books and manuscripts in Source Library, situating them within their networks of production, transmission, and reception.

## When to Use

- "Research this book's history"
- "Find other editions of this text"
- "Where does this manuscript fit in the tradition?"
- "Build a book biography for..."
- "What other versions of this text exist?"
- "Analyze the transmission of..."
- "Find related works to import"

## Invocation

```
/book-biography                           # Start interactive session
/book-biography [book_id]                 # Research specific book
/book-biography "Title or Author"         # Research by name
/book-biography import [book_id]          # Research and import related editions
```

## Core Disciplines

This skill applies methods from:

| Field | Focus | Application |
|-------|-------|-------------|
| **Bibliography** | Books as physical objects | Format, binding, typography |
| **Codicology** | Manuscripts as objects | Scribes, materials, construction |
| **Paleography** | Historical scripts | Dating, localization |
| **Stemmatology** | Textual transmission | Manuscript families, variants |
| **Provenance** | Ownership history | Stamps, ex libris, annotations |
| **Reception History** | How texts were read | Annotations, citations, influence |
| **Book History** | Social/cultural context | Patrons, printers, readers |

## Research Workflow

### Phase 1: Identification

1. **Get book from Source Library**
```bash
curl -s "https://sourcelibrary.org/api/books/BOOK_ID" | jq '{
  title, author, year, place, publisher,
  original_language, pages: .pages_count,
  image_source
}'
```

2. **Check source institution** (Gallica, IA, MDZ)
```bash
# For Gallica
curl -s "https://gallica.bnf.fr/ark:/12148/ARK_ID"

# For Internet Archive
curl -s "https://archive.org/metadata/IA_ID" | jq '.metadata'

# For MDZ
curl -s "https://api.digitale-sammlungen.de/iiif/presentation/v2/BSB_ID/manifest"
```

3. **Extract physical description**
   - Shelfmark
   - Date and origin
   - Dimensions and format
   - Scribe/printer
   - Binding
   - Provenance marks

### Phase 2: Production Context

1. **Research the maker** (scribe, printer, publisher)
   - Web search for biographical info
   - Other works by same maker
   - Workshop/network connections

2. **Research the patron/owner**
   - Commissioning context
   - Collection history
   - Contemporary documentation

3. **Research the place/institution**
   - Printing center history
   - Scriptoria traditions
   - Library/collection context

### Phase 3: Textual Transmission

1. **Identify the text(s)**
   - Author attribution (real vs pseudonymous)
   - Original composition date
   - Genre and tradition

2. **Map the stemma (manuscript families)**
   - Key witnesses (MSS and early prints)
   - Siglum designations (A, B, C...)
   - Critical editions and their apparatus

3. **Position this witness**
   - What exemplar was it copied from?
   - What derives from it?
   - Unique readings or variants?

### Phase 4: Related Works in Source Library

```bash
# Search by author
curl -s "https://sourcelibrary.org/api/search?q=AUTHOR&limit=20" | jq '.results[] | {id, title, author}'

# Search by title/text
curl -s "https://sourcelibrary.org/api/search?q=TEXT_NAME&limit=20" | jq '.results[] | {id, title, author}'

# Search by theme
curl -s "https://sourcelibrary.org/api/search?q=THEME&limit=20" | jq '.results[] | {id, title, author}'
```

### Phase 5: Find External Editions

**Archive.org**
```bash
curl -s "https://archive.org/advancedsearch.php?q=creator:(AUTHOR)+OR+title:(TITLE)&fl[]=identifier&fl[]=title&fl[]=date&fl[]=creator&sort[]=date+asc&rows=30&output=json" | jq '.response.docs'
```

**Gallica**
- Search: https://gallica.bnf.fr/
- Check for IIIF manifests

**MDZ (Bavarian State Library)**
- Search: https://www.digitale-sammlungen.de/
- BSB identifiers for import

**USTC (pre-1601 books)**
- https://www.ustc.ac.uk/
- Authoritative bibliographic data

**WorldCat**
- https://www.worldcat.org/
- Edition counts and library holdings

### Phase 6: Import Related Editions

```bash
# Internet Archive
curl -X POST "https://sourcelibrary.org/api/import/ia" \
  -H "Content-Type: application/json" \
  -d '{
    "ia_identifier": "IDENTIFIER",
    "title": "Title (Editor/Translator Year)",
    "author": "Author; Editor (ed.)",
    "year": YYYY,
    "original_language": "Language"
  }'

# Gallica
curl -X POST "https://sourcelibrary.org/api/import/gallica" \
  -H "Content-Type: application/json" \
  -d '{
    "ark": "ARK_ID",
    "title": "Title",
    "author": "Author",
    "year": YYYY,
    "original_language": "Language"
  }'

# MDZ
curl -X POST "https://sourcelibrary.org/api/import/mdz" \
  -H "Content-Type: application/json" \
  -d '{
    "bsb_id": "BSB_ID",
    "title": "Title",
    "author": "Author",
    "year": YYYY,
    "original_language": "Language"
  }'
```

## Book Biography Template

```markdown
# Book Biography: [Shelfmark]

## Physical Description

| Field | Value |
|-------|-------|
| **Shelfmark** | [Institution, Collection, Number] |
| **Date** | [YYYY or range] |
| **Origin** | [Place] |
| **Format** | [Folio/Quarto/Octavo/MS] |
| **Dimensions** | [H × W mm] |
| **Foliation** | [Structure] |
| **Binding** | [Description] |
| **Scribe/Printer** | [Name] |
| **Patron/Owner** | [Name] |

---

## Contents

| No. | Text | Author | Folios |
|-----|------|--------|--------|
| 1 | [Title] | [Author] | ff. X-Y |
| 2 | [Title] | [Author] | ff. Y-Z |

---

## Production Context

### The Maker
[Biography and significance of scribe/printer]

### The Patron
[Who commissioned/owned, why]

### Historical Context
[What was happening when this was made]

---

## Textual Transmission

### The Text(s)
- **Original composition**: [Date, place, circumstances]
- **Author**: [Real name, dates, attribution issues]
- **Genre**: [Type of text]

### Stemma
```
[ASCII diagram of manuscript relationships]
```

### Key Witnesses
| Siglum | Manuscript | Date | Notes |
|--------|-----------|------|-------|
| A | [Shelfmark] | [Date] | [Significance] |
| B | [Shelfmark] | [Date] | [Significance] |

### This Witness
- **Exemplar**: [What it was copied from]
- **Descendants**: [What was copied from it]
- **Unique features**: [Variants, errors, additions]

---

## Related Works in Source Library

| ID | Title | Relationship |
|----|-------|--------------|
| `[id]` | [Title] | [How related] |

---

## Editions Available

### Manuscripts
| Location | Shelfmark | Date | Notes |
|----------|-----------|------|-------|
| [City] | [Shelfmark] | [Date] | [Significance] |

### Printed Editions (Chronological)
| Year | Place | Editor/Translator | Significance |
|------|-------|-------------------|--------------|
| YYYY | [City] | [Name] | [First edition/Critical/etc.] |

### On Archive.org
| ID | Title | Year | Pages |
|----|-------|------|-------|
| `[ia_id]` | [Title] | YYYY | N |

---

## Research Questions

1. [Open question about this witness]
2. [Open question about transmission]
3. [Open question about reception]

---

## Bibliography

- [Scholarly works on this text/manuscript]
- [Critical editions]
- [Catalog entries]
```

## Network Visualization

When mapping relationships, use ASCII diagrams:

```
ANTIQUITY                BYZANTIUM              RENAISSANCE            PRINT

[Original]  ──────────►  [MS Family A]  ────►  [Humanist copy]  ────►  [Editio princeps]
                              │                       │                      │
                         [MS Family B]  ────►  [YOUR BOOK]  ◄────────────────┘
                              │                       │
                         [MS Family C]  ────►  [Later editions]
```

## Scoring Editions for Import

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Historical priority** | 3x | Earlier = better (editio princeps, early MSS) |
| **Critical apparatus** | 2x | Scholarly editions with variants |
| **Textual coverage** | 2x | Complete vs excerpts |
| **Language** | 1x | Original language > translations |
| **Availability** | 1x | Not already in collection |
| **Image quality** | 1x | Readable scans |

## Example Session

```
User: /book-biography 695230c6ab34727b1f044784

Agent: Researching BnF grec 2518...

## Physical Description
- **Shelfmark**: Paris, BnF, grec 2518
- **Date**: 1530-1539
- **Origin**: Venice
- **Scribe**: Ange Vergèce (royal scribe)
- **Patron**: Francis I of France

## Contents
1. Hero of Alexandria, Pneumatica
2. Corpus Hermeticum
3. Ocellus Lucanus, De universi natura

## Key Finding
This manuscript predates all printed editions of its texts:
- Ocellus first printed: 1539
- Hero Pneumatica first printed: 1575
- Corpus Hermeticum (Greek): 1554

## Related Works in Source Library
[Lists 15+ related Hermetic and Ficino texts]

## Available Editions on Archive.org
[Lists 17 editions of Hero and Ocellus]

Would you like me to import these related editions?
```

## Reports Storage

- Session reports append to `bookbiography.md`
- Import logs tracked with book IDs and page counts
- Network diagrams preserved for reference

## Key Resources

### Digital Libraries
- [Archive.org](https://archive.org) - Largest free collection
- [Gallica](https://gallica.bnf.fr) - BnF digitizations
- [MDZ](https://www.digitale-sammlungen.de) - Bavarian State Library
- [e-rara](https://www.e-rara.ch) - Swiss rare books
- [Google Books](https://books.google.com) - Pre-1928 works

### Catalogs
- [USTC](https://www.ustc.ac.uk) - Universal Short Title Catalogue (pre-1601)
- [ISTC](https://data.cerl.org/istc) - Incunabula Short Title Catalogue (pre-1501)
- [WorldCat](https://www.worldcat.org) - Global library holdings
- [Biblissima](https://portail.biblissima.fr) - Medieval MSS portal

### Scholarship
- **Textual Criticism**: West, Reynolds & Wilson
- **Codicology**: Lemaire, Derolez
- **Book History**: Johns, Chartier, Febvre & Martin
- **Paleography**: Bischoff, Brown

## Rules

### DO
- Always get book details from Source Library first
- Check what's already in the collection before importing
- Research production context (who, when, where, why)
- Map textual transmission (stemma)
- Search multiple digital libraries
- Present findings with clear citations
- Offer to import related editions
- Generate network visualizations

### DO NOT
- Import without checking for duplicates
- Skip the physical description
- Ignore production context
- Present speculation as fact
- Import modern copyrighted editions
- Forget to document imports
