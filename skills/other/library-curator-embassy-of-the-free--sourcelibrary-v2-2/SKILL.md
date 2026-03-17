---
name: library-curator
description: Autonomous curator for Source Library - discover, evaluate, and import historical texts in alchemy, Hermetica, Kabbalah, Rosicrucianism, and early modern knowledge. Use when asked to curate books, find new sources, expand the collection, or build thematic batches.
---

# Library Curator

Autonomous book acquisition agent for Source Library, focused on Western esoteric tradition and early modern knowledge.

## When to Use

- "Find books about alchemy"
- "Curate a batch of Rosicrucian texts"
- "Add more works by Paracelsus"
- "Expand the Hermetica collection"
- "What should we acquire next?"

## Role & Mission

**Affiliation**: Embassy of the Free Mind (Bibliotheca Philosophica Hermetica, Amsterdam)
**Mission**: Build a comprehensive digital library of Western esoteric tradition and early modern knowledge

## Thematic Focus

### Primary Collections (Priority 1)
- **Hermetica** - Corpus Hermeticum, Ficino translations, Trismegistus tradition
- **Alchemy** - Paracelsus, iatrochemistry, transmutation, Theatrum Chemicum
- **Kabbalah** - Christian Kabbalah, Pico, Reuchlin, Knorr von Rosenroth
- **Rosicrucianism** - Manifestos, Andreae, Fludd, early responses
- **Theosophy** - Boehme, Gichtel, Pordage, German mysticism
- **Natural Magic** - Agrippa, Della Porta, Bruno, Renaissance magia

### Secondary Collections (Priority 2)
- **Early Science** - Copernicus, Kepler, Newton, mathematical arts
- **Neoplatonism** - Plotinus, Proclus, Florentine Academy
- **Emblemata** - Alciato, emblem books, symbolic imagery
- **Architecture** - Vitruvius, Palladio, sacred geometry
- **Art Theory** - Dürer, Leonardo, proportion and perspective

### Language Priority
1. Latin (primary scholarly language)
2. German (Boehme, Paracelsus, Reformation mysticism)
3. English (17th century translations, Cambridge Platonists)
4. Italian (Renaissance sources)
5. French (18th century editions)
6. Dutch (Amsterdam printing tradition)

## Selection Rules (CRITICAL)

### ACQUIRE
- Original historical editions (pre-1800 primary sources)
- Early printed books in original language
- First editions and important early printings
- Contemporary translations (e.g., 17th-century English translations of Latin works)
- Critical scholarly editions with original text (e.g., Flasch's Bruno, Tocco's Bruno)

### REJECT
- Modern translations (20th-21st century) without original text
- Secondary literature and commentaries (unless exceptional)
- Facsimile reprints when original scans exist
- Anthologies that excerpt rather than present complete works
- Books already in collection (check before importing)

## Scoring Criteria (1-10 scale)

| Criterion | Weight | Notes |
|-----------|--------|-------|
| Thematic fit | 3x | Core esoteric tradition |
| Edition quality | 2x | First editions, important printings |
| Rarity | 2x | Not widely available digitally |
| Historical authenticity | 2x | Original vs modern editions |
| Completeness | 1x | Full text vs fragments |
| Image quality | 1x | Readable scans |
| Research value | 1x | Citations, scholarly interest |

## Import APIs

### Internet Archive
```bash
curl -X POST "https://sourcelibrary.org/api/import/ia" \
  -H "Content-Type: application/json" \
  -d '{
    "ia_identifier": "bookid123",
    "title": "Book Title",
    "author": "Author Name",
    "year": 1617,
    "original_language": "Latin"
  }'
```

### Gallica (BnF)
```bash
curl -X POST "https://sourcelibrary.org/api/import/gallica" \
  -H "Content-Type: application/json" \
  -d '{
    "ark": "bpt6k61073880",
    "title": "Book Title",
    "author": "Author Name",
    "year": 1617,
    "original_language": "Latin"
  }'
```

### MDZ (Bavarian State Library)
```bash
curl -X POST "https://sourcelibrary.org/api/import/mdz" \
  -H "Content-Type: application/json" \
  -d '{
    "bsb_id": "bsb00029099",
    "title": "Book Title",
    "author": "Author Name",
    "year": 1473,
    "original_language": "Latin"
  }'
```

## Check Existing Collection

Before importing, always check if the book is already in the collection:

```bash
# Search by title
curl -s "https://sourcelibrary.org/api/search?q=TITLE"

# Get all books
curl -s "https://sourcelibrary.org/api/books" | jq '.[] | {id, title, author, year}'

# Search by author
curl -s "https://sourcelibrary.org/api/books" | jq '.[] | select(.author | contains("AUTHOR_NAME"))'
```

## Workflow

1. **Identify Theme** - Choose a thematic focus or gap to fill
2. **Search Sources** - Use catalog CSVs or archive searches to find candidates
3. **Evaluate Books** - Score each book using criteria above
4. **Check Collection** - Verify books aren't already imported
5. **Import Batch** - Import 5-20 books with thematic coherence
6. **Generate Report** - Document batch with rationale and notes
7. **Update Logs** - Add to successes log in agentcurator.md

## Catalog Sources

### Primary Catalogs
- **BPH Catalog**: `data/bph_catalog.csv` (28,814 entries)
  - Bibliotheca Philosophica Hermetica holdings
  - Strong in Hermetica, alchemy, Rosicrucianism

- **IA Catalog**: `data/ia_catalog.csv` (9,000 entries)
  - Internet Archive / McGill early printed books
  - Strong in incunabula, 15th-16th century

### Discovery Methods
- Archive.org searches by theme/author
- Cross-references from acquired texts
- Scholarly bibliographies (Thorndike, Yates, etc.)
- BnF Gallica catalog searches
- MDZ/BSB Munich digitization searches

## Report Format

### Per-Book Report
```
## [Title] ([Year])
**Author**: [Name]
**Language**: [Lang] | **Pages**: [N] | **Source**: [Archive ID]
**Theme**: [Primary collection]
**Score**: [N]/10
**Notes**: [1-2 sentences on significance]
**Status**: [acquired/skipped/pending]
```

### Batch Report
```
# Acquisition Batch [DATE] - [THEME]

## Summary
- Books acquired: N
- Total pages: N
- Languages: X, Y, Z
- Date range: YYYY-YYYY

## Thematic Rationale
[Why this batch, how it connects]

## Books
[Individual reports]

## Gaps Identified for Future Batches
[What to acquire next]
```

## Quality Management

### Spot Checks (10% of acquisitions)
- OCR accuracy on random page
- Image/text alignment
- Metadata accuracy vs source
- Page completeness (no missing pages)

### Issue Flags
- `FLAG:OCR` - OCR quality problems
- `FLAG:ALIGN` - Image/text misalignment
- `FLAG:META` - Metadata errors
- `FLAG:INCOMPLETE` - Missing pages
- `FLAG:DUPLICATE` - Already in collection

## Current Gaps (Priority Acquisitions)

### URGENT - Missing Key Authors
| Author | What We Need | Priority |
|--------|--------------|----------|
| Thomas Vaughan | Lumen de Lumine, Aula Lucis, Anima Magica Abscondita | HIGH |
| Gichtel | Theosophia Practica | HIGH |
| Jane Lead | English Philadelphian Society | MEDIUM |
| Cudworth | True Intellectual System | MEDIUM |

### Have Some, Need More
| Author/Text | Have | Need |
|-------------|------|------|
| Boehme | 3 works | More German originals (Aurora, Signatura Rerum) |
| Fludd | 3 works | Complete Utriusque Cosmi (5+ volumes) |
| Dee | 1 work | True Relation, Monas hieroglyphica |
| Paracelsus | Several | Individual treatises in German |

## Batch Size & Pacing
- **Target**: 5-20 books per acquisition session
- **Pace**: Quality over quantity
- **Grouping**: Thematic coherence within batches
- **Documentation**: All acquisitions logged to `agentcurator.md`

## Metadata Attention
- Accurate author attribution (including pseudonyms)
- Precise dating (not just century)
- Printer/publisher (important for provenance)
- Edition details (first, revised, translation)
- Physical description (folio, quarto, illustrated)
- Shelf marks and catalog references

## Reports Storage
- Session reports append to `agentcurator.md`
- Quality audit reports go to `curatorreports.md`
- Maintain successes log with all imported books
- Track rejects with rationale
