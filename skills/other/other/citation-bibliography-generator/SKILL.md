---
name: citation-bibliography-generator
description: Format citations in APA, MLA, Chicago, IEEE, Harvard styles from structured data, DOI/ISBN lookup, or manual entry. Generate bibliographies with auto-sort.
---

# Citation & Bibliography Generator

Generate properly formatted citations and bibliographies in multiple academic and professional styles. Supports manual entry, structured data import, and automatic metadata lookup via DOI/ISBN.

## Quick Start

```python
from scripts.citation_generator import CitationGenerator

# Create generator with desired style
gen = CitationGenerator(style='apa')

# Cite a book
citation = gen.cite_book(
    authors=["Smith, John", "Doe, Jane"],
    title="Research Methods in Social Science",
    year=2020,
    publisher="Academic Press",
    city="New York"
)
print(citation)
# Output: Smith, J., & Doe, J. (2020). Research methods in social science. Academic Press.

# Build bibliography
gen.add_to_bibliography(citation)
bibliography = gen.generate_bibliography()
print(bibliography)
```

## Supported Citation Styles

- **APA** (American Psychological Association) - 7th Edition
- **MLA** (Modern Language Association) - 9th Edition
- **Chicago** (Chicago Manual of Style) - 17th Edition
- **IEEE** (Institute of Electrical and Electronics Engineers)
- **Harvard** (Harvard referencing style)

## Features

### 1. Manual Citation Creation

Format citations by source type:
- **Books** - Monographs, edited volumes, editions
- **Journal Articles** - Peer-reviewed articles with DOI
- **Websites** - Online sources with access dates
- **Conference Papers** - Proceedings and presentations

### 2. Automatic Metadata Lookup

- **DOI Lookup** - Fetch article metadata from CrossRef API
- **ISBN Lookup** - Retrieve book information (when available)
- Auto-detect source type and format accordingly

### 3. Bibliography Management

- Add multiple citations
- Auto-sort by author, year, or title
- Duplicate detection and removal
- Export to plain text or BibTeX

### 4. In-Text Citations

Generate parenthetical or narrative in-text citations:
- Parenthetical: `(Smith, 2020, p. 45)`
- Narrative: `Smith (2020) argues that...`
- Multiple authors with et al. handling

### 5. Batch Processing

Import citations from CSV files with structured data and generate complete bibliographies.

## API Reference

### CitationGenerator

**Initialization**:
```python
gen = CitationGenerator(style='apa')
```

**Parameters**:
- `style` (str): Citation style - 'apa', 'mla', 'chicago', 'ieee', or 'harvard'

### Citation Methods

#### cite_book()
```python
citation = gen.cite_book(
    authors=["Last, First", "Last, First"],
    title="Book Title",
    year=2020,
    publisher="Publisher Name",
    city="City",           # Optional
    edition="3rd ed.",     # Optional
    isbn="978-0-123456-78-9"  # Optional
)
```

**Returns**: Formatted citation string

#### cite_article()
```python
citation = gen.cite_article(
    authors=["Last, First"],
    title="Article Title",
    journal="Journal Name",
    year=2020,
    volume=10,          # Optional
    issue=2,            # Optional
    pages="45-67",      # Optional
    doi="10.1234/example"  # Optional
)
```

**Returns**: Formatted citation string

#### cite_website()
```python
citation = gen.cite_website(
    authors=["Last, First"],  # Can be empty list
    title="Page Title",
    url="https://example.com",
    access_date="2024-01-15",
    publish_date="2023-12-01"  # Optional
)
```

**Returns**: Formatted citation string

#### cite_from_doi()
```python
citation = gen.cite_from_doi(doi="10.1234/example")
```

Looks up article metadata from CrossRef API and generates formatted citation.

**Returns**: Formatted citation string

### Bibliography Management

#### add_to_bibliography()
```python
gen.add_to_bibliography(citation)
```

Add a citation to the bibliography list.

#### generate_bibliography()
```python
bibliography = gen.generate_bibliography(
    sort_by='author',      # 'author', 'year', or 'title'
    deduplicate=True       # Remove duplicate entries
)
```

**Returns**: Formatted bibliography string with hanging indent

#### export_bibtex()
```python
gen.export_bibtex(output_path='references.bib')
```

Export bibliography as BibTeX format for LaTeX documents.

### In-Text Citations

#### in_text_citation()
```python
citation = gen.in_text_citation(
    authors=["Smith, J."],
    year=2020,
    page="45",          # Optional
    narrative=False     # True for narrative style
)
```

**Returns**:
- Parenthetical: `(Smith, 2020, p. 45)`
- Narrative: `Smith (2020)`

### Batch Processing

#### import_from_csv()
```python
citations = gen.import_from_csv(csv_path='citations.csv')
```

Import multiple citations from CSV file.

**CSV Format**:
```csv
type,authors,title,year,journal,publisher,doi,isbn,url,access_date
article,"Smith, J.|Doe, A.",Research Methods,2020,Journal of Science,,10.1234/example,,,
book,"Johnson, M.",Data Analysis,2019,,Academic Press,,978-0-123456-78-9,,
website,,"Web Page Title",2024,,,,,https://example.com,2024-01-15
```

**Note**: Separate multiple authors with `|` pipe character

**Returns**: List of formatted citation strings

## CLI Usage

### Single Citation

**Book**:
```bash
python scripts/citation_generator.py book \
    --authors "Smith, J." "Doe, A." \
    --title "Research Methods" \
    --year 2020 \
    --publisher "Academic Press" \
    --city "New York" \
    --style apa
```

**Article**:
```bash
python scripts/citation_generator.py article \
    --authors "Smith, J." \
    --title "Study Title" \
    --journal "Journal Name" \
    --year 2020 \
    --volume 10 \
    --issue 2 \
    --pages "45-67" \
    --doi "10.1234/example" \
    --style mla
```

**Website**:
```bash
python scripts/citation_generator.py website \
    --title "Page Title" \
    --url "https://example.com" \
    --access-date "2024-01-15" \
    --style chicago
```

### DOI Lookup

```bash
python scripts/citation_generator.py doi \
    --doi "10.1234/example" \
    --style apa
```

### Batch Processing

```bash
python scripts/citation_generator.py batch \
    --input citations.csv \
    --style harvard \
    --output bibliography.txt \
    --sort author
```

### BibTeX Export

```bash
python scripts/citation_generator.py batch \
    --input citations.csv \
    --format bibtex \
    --output references.bib
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--style`, `-s` | Citation style (apa/mla/chicago/ieee/harvard) | apa |
| `--authors`, `-a` | Author names (multiple allowed) | - |
| `--title`, `-t` | Title of work | - |
| `--year`, `-y` | Publication year | - |
| `--input`, `-i` | Input CSV file (batch mode) | - |
| `--output`, `-o` | Output file path | stdout |
| `--format`, `-f` | Output format (text/bibtex) | text |
| `--sort` | Sort bibliography by (author/year/title) | author |

## Examples

### Example 1: APA Book Citation

```python
gen = CitationGenerator(style='apa')
citation = gen.cite_book(
    authors=["Doe, Jane", "Smith, John"],
    title="The Art of Research",
    year=2021,
    publisher="University Press",
    edition="2nd ed."
)
print(citation)
# Doe, J., & Smith, J. (2021). The art of research (2nd ed.). University Press.
```

### Example 2: MLA Article Citation

```python
gen = CitationGenerator(style='mla')
citation = gen.cite_article(
    authors=["Johnson, Mary"],
    title="Digital Humanities in the 21st Century",
    journal="Modern Research Quarterly",
    year=2022,
    volume=15,
    issue=3,
    pages="112-145",
    doi="10.5678/mrq.2022.15.3"
)
print(citation)
# Johnson, Mary. "Digital Humanities in the 21st Century." Modern Research Quarterly, vol. 15, no. 3, 2022, pp. 112-145. DOI: 10.5678/mrq.2022.15.3.
```

### Example 3: Chicago Website Citation

```python
gen = CitationGenerator(style='chicago')
citation = gen.cite_website(
    authors=["Brown, Robert"],
    title="Understanding Machine Learning",
    url="https://ml-guide.example.com",
    access_date="2024-01-20",
    publish_date="2023-11-15"
)
print(citation)
# Brown, Robert. "Understanding Machine Learning." Last modified November 15, 2023. Accessed January 20, 2024. https://ml-guide.example.com.
```

### Example 4: Building a Bibliography

```python
gen = CitationGenerator(style='apa')

# Add multiple citations
gen.add_to_bibliography(gen.cite_book(
    authors=["Smith, A."],
    title="First Book",
    year=2020,
    publisher="Press A"
))

gen.add_to_bibliography(gen.cite_article(
    authors=["Jones, B."],
    title="Research Article",
    journal="Journal X",
    year=2021
))

# Generate formatted bibliography
bibliography = gen.generate_bibliography(sort_by='author')
print(bibliography)
```

### Example 5: DOI Lookup

```python
gen = CitationGenerator(style='ieee')
citation = gen.cite_from_doi(doi="10.1109/ACCESS.2019.2947014")
print(citation)
# Auto-fetches metadata and formats in IEEE style
```

### Example 6: Batch Processing from CSV

```python
gen = CitationGenerator(style='harvard')
citations = gen.import_from_csv('my_references.csv')

# Add all to bibliography
for citation in citations:
    gen.add_to_bibliography(citation)

# Generate and export
gen.export_bibtex('references.bib')
```

## Dependencies

```
pandas>=2.0.0
requests>=2.31.0
```

Install dependencies:
```bash
pip install -r scripts/requirements.txt
```

## Limitations

- **API Availability**: DOI/ISBN lookups require internet connection and depend on third-party APIs (CrossRef)
- **API Rate Limits**: CrossRef API has rate limits; implement delays for batch lookups
- **Style Variations**: Some citation styles have discipline-specific variations not fully covered
- **Special Characters**: Unicode support for accents and special characters may vary by output format
- **Edition Numbers**: Different styles format editions differently (ordinal vs text)
- **Author Name Formats**: Input should be "Last, First" format; parsing other formats may be inconsistent
- **Multiple Authors**: Et al. rules vary by style (APA: 3+, MLA: 3+, Chicago: 4+)
- **Online-First Articles**: Articles published online before print may have partial metadata
- **Non-English Sources**: Some citation styles have specific rules for non-English sources that may not be fully implemented

## Citation Style Guidelines

### APA (American Psychological Association)
- Author-date system
- Ampersand (&) before last author
- Title case for book titles, sentence case for article titles
- DOI as URL: https://doi.org/10.xxxx

### MLA (Modern Language Association)
- Author-page system
- "And" before last author
- Title case for all titles
- Container concept (journal is container for article)

### Chicago (Chicago Manual of Style)
- Notes and bibliography system
- "And" before last author
- Title case for titles
- Access dates for websites

### IEEE (Institute of Electrical and Electronics Engineers)
- Numbered references [1], [2], etc.
- Initials before last name
- Quotation marks for article titles
- Abbreviated journal names

### Harvard
- Author-date system
- "And" before last author
- Italic for book/journal titles
- Available at: for URLs
