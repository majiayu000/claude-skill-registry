---
name: digital-archive
description: Digital archiving workflows with AI enrichment, entity extraction, and knowledge graph construction. Use when building content archives, implementing AI-powered categorization, extracting entities and relationships, or integrating multiple data sources. Covers patterns from the Jay Rosen Digital Archive project.
---

# Digital archive methodology

Patterns for building production-quality digital archives with AI-powered analysis and knowledge graph construction.

## Archive architecture

### Multi-source integration pattern
```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────┐
│  OCR Pipeline   │    │  Web Scraping    │    │  Social Media  │
│  (newspapers)   │    │  (articles)      │    │  (transcripts) │
└────────┬────────┘    └────────┬─────────┘    └───────┬────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │  Unified Schema       │
                    │  (35+ fields)         │
                    └───────────┬───────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
┌────────▼────────┐  ┌──────────▼──────────┐  ┌───────▼───────┐
│  AI Enrichment  │  │  Entity Extraction  │  │  PDF Archive  │
│  (Gemini)       │  │  (Knowledge Graph)  │  │  (WCAG 2.1)   │
└────────┬────────┘  └──────────┬──────────┘  └───────┬───────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │  Google Sheets        │
                    │  (primary database)   │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │  Frontend Export      │
                    │  (JSON/CSV)           │
                    └───────────────────────┘
```

### Unified schema design

```python
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from enum import Enum

class ContentType(Enum):
    ARTICLE = 'Article'
    VIDEO = 'Video'
    AUDIO = 'Audio'
    SOCIAL = 'Social Post'
    NEWSPAPER = 'Newspaper Article'

class ThematicCategory(Enum):
    PRESS_CRITICISM = 'Press & Media Criticism'
    JOURNALISM_THEORY = 'Journalism Theory'
    POLITICS = 'Politics & Democracy'
    TECHNOLOGY = 'Technology & Digital Media'
    EDUCATION = 'Journalism Education'
    AUDIENCE = 'Audience & Public Engagement'

class HistoricalEra(Enum):
    ERA_1990s = '1990-1999'
    ERA_2000_04 = '2000-2004'
    ERA_2005_09 = '2005-2009'
    ERA_2010_15 = '2010-2015'
    ERA_2016_20 = '2016-2020'
    ERA_2021_PRESENT = '2021-present'

@dataclass
class ArchiveRecord:
    # Core identifiers
    id: str                              # Format: SOURCE-00001
    url: str
    title: str

    # Content
    author: Optional[str] = None
    publication_date: Optional[date] = None
    publication: Optional[str] = None
    content_type: ContentType = ContentType.ARTICLE
    text: str = ''

    # AI-enriched fields
    summary: Optional[str] = None
    pull_quote: Optional[str] = None
    categories: list[ThematicCategory] = field(default_factory=list)
    key_concepts: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    era: Optional[HistoricalEra] = None
    scope: Optional[str] = None  # Theoretical, Commentary, Case Study, etc.

    # Entity references
    entities_mentioned: list[str] = field(default_factory=list)
    related_to: list[str] = field(default_factory=list)
    responds_to: list[str] = field(default_factory=list)

    # Archive metadata
    pdf_url: Optional[str] = None
    transcript_url: Optional[str] = None
    verified: bool = False
    processing_status: str = 'pending'
    last_updated: Optional[date] = None

def generate_record_id(source: str, sequence: int) -> str:
    """Generate unique ID with source prefix."""
    prefixes = {
        'nytimes': 'NYT',
        'columbia journalism review': 'CJR',
        'pressthink': 'PT',
        'twitter': 'TW',
        'youtube': 'YT',
        'newspaper': 'NEWS',
    }
    prefix = prefixes.get(source.lower(), 'MISC')
    return f"{prefix}-{sequence:05d}"
```

## AI-powered categorization

### Taxonomy-based classification

```python
import google.generativeai as genai
import json
from typing import Optional

TAXONOMY = {
    "thematic_categories": [
        "Press & Media Criticism",
        "Journalism Theory",
        "Politics & Democracy",
        "Technology & Digital Media",
        "Journalism Education",
        "Audience & Public Engagement"
    ],
    "key_concepts": [
        "The View from Nowhere",
        "Verification vs. Assertion",
        "Citizens vs. Consumers",
        "Public Journalism",
        "The Rosen Test",
        "Savvy vs. Naive",
        "Professional vs. Amateur",
        "Production vs. Distribution",
        "Trust vs. Transparency",
        "Horse Race Coverage",
        "Both Sides Journalism",
        "Audience Atomization",
        "The Church of the Savvy"
    ],
    "scope_types": [
        "Theoretical",
        "Commentary",
        "Historical",
        "Case Study",
        "Pedagogical",
        "Personal Reflection"
    ]
}

class ArchiveCategorizer:
    def __init__(self, model: str = 'gemini-2.0-flash'):
        self.model = genai.GenerativeModel(model)

    def categorize(self, record: ArchiveRecord) -> dict:
        prompt = f"""Analyze this archival content and categorize it according to the taxonomy.

CONTENT:
Title: {record.title}
Author: {record.author or 'Unknown'}
Date: {record.publication_date or 'Unknown'}
Text (first 8000 chars):
{record.text[:8000]}

TAXONOMY:
{json.dumps(TAXONOMY, indent=2)}

Respond with JSON containing:
{{
  "categories": ["category1", "category2"],  // 1-3 from thematic_categories
  "key_concepts": ["concept1", "concept2"],  // 0-5 from key_concepts list
  "scope": "scope_type",                     // one from scope_types
  "era": "YYYY-YYYY",                        // decade range
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],  // 5 contextual keywords
  "summary": "2-3 sentence summary",
  "pull_quote": "Most impactful quote from the text"
}}

IMPORTANT:
- Only use categories/concepts from the taxonomy
- Tags should be lowercase, hyphenated keywords
- Summary should capture the main argument
- Pull quote must be an exact excerpt from the text
"""

        response = self.model.generate_content(prompt)
        result = self._parse_response(response.text)

        # Validate against taxonomy
        result['categories'] = [c for c in result.get('categories', [])
                               if c in TAXONOMY['thematic_categories']]
        result['key_concepts'] = [c for c in result.get('key_concepts', [])
                                  if c in TAXONOMY['key_concepts']]

        return result

    def _parse_response(self, text: str) -> dict:
        """Extract JSON from response, handling markdown code blocks."""
        # Remove markdown code blocks if present
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0]
        elif '```' in text:
            text = text.split('```')[1].split('```')[0]

        return json.loads(text.strip())

    def validate_response(self, result: dict, text: str) -> bool:
        """Detect AI hallucination patterns."""
        # Check for uniform response signature (all same values)
        if len(set(result.get('tags', []))) < 3:
            return False

        # Check pull quote exists in text
        pull_quote = result.get('pull_quote', '')
        if pull_quote and pull_quote.lower() not in text.lower():
            return False

        # Check summary isn't generic
        generic_phrases = ['this article discusses', 'the author explores', 'this piece examines']
        summary = result.get('summary', '').lower()
        if any(phrase in summary for phrase in generic_phrases):
            return False

        return True
```

## Entity extraction and knowledge graph

### Entity types and relationships

```python
from dataclasses import dataclass
from typing import Literal

EntityType = Literal['Person', 'Organization', 'Work', 'Concept', 'Event', 'Location']
RelationshipType = Literal[
    'Mentions', 'Criticizes', 'Cites', 'Discusses', 'Expands On', 'Supports',
    'Founded By', 'Pioneered', 'Inspired By',
    'Affiliated With', 'Published In', 'Originated By', 'Occurred At',
    'Owns', 'Owned By'
]

@dataclass
class Entity:
    id: str                    # P-001, O-001, W-001, etc.
    name: str
    type: EntityType
    aliases: list[str]         # Alternative names/spellings
    prominence: float          # 0-10 based on discussion depth
    mention_count: int = 0
    first_mentioned_in: str = ''  # Record ID

@dataclass
class Relationship:
    source_entity_id: str
    target_entity_id: str
    relationship_type: RelationshipType
    source_record_id: str      # Which record established this relationship
    confidence: float = 1.0

class EntityRegistry:
    """Deduplication and normalization for entities."""

    NORMALIZATIONS = {
        'nyt': 'The New York Times',
        'new york times': 'The New York Times',
        'ny times': 'The New York Times',
        'washington post': 'The Washington Post',
        'wapo': 'The Washington Post',
        'cnn': 'CNN',
        'fox': 'Fox News',
        'fox news channel': 'Fox News',
    }

    def __init__(self):
        self.entities: dict[str, Entity] = {}
        self.name_to_id: dict[str, str] = {}

    def normalize_name(self, name: str) -> str:
        """Normalize entity name to canonical form."""
        name_lower = name.lower().strip()
        return self.NORMALIZATIONS.get(name_lower, name.strip())

    def find_or_create(self, name: str, entity_type: EntityType) -> Entity:
        """Find existing entity or create new one."""
        normalized = self.normalize_name(name)

        # Check if already exists
        if normalized.lower() in self.name_to_id:
            entity_id = self.name_to_id[normalized.lower()]
            entity = self.entities[entity_id]
            entity.mention_count += 1
            return entity

        # Create new entity
        type_prefix = entity_type[0].upper()  # P, O, W, C, E, L
        count = sum(1 for e in self.entities.values() if e.type == entity_type)
        entity_id = f"{type_prefix}-{count + 1:04d}"

        entity = Entity(
            id=entity_id,
            name=normalized,
            type=entity_type,
            aliases=[name] if name != normalized else [],
            prominence=0.0,
            mention_count=1
        )

        self.entities[entity_id] = entity
        self.name_to_id[normalized.lower()] = entity_id

        return entity
```

### AI-powered entity extraction

```python
class EntityExtractor:
    def __init__(self, registry: EntityRegistry):
        self.registry = registry
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def extract(self, record: ArchiveRecord) -> tuple[list[Entity], list[Relationship]]:
        prompt = f"""Extract named entities and relationships from this archival content.

CONTENT:
Title: {record.title}
Text: {record.text[:10000]}

ENTITY TYPES:
- Person: journalists, politicians, academics, media figures
- Organization: news outlets, media companies, academic institutions
- Work: articles, books, blog posts, studies, reports
- Concept: journalism theories, media criticism frameworks
- Event: conferences, elections, media crises
- Location: geographic locations relevant to media context

RELATIONSHIP TYPES:
- Mentions, Criticizes, Cites, Discusses, Expands On, Supports
- Founded By, Pioneered, Inspired By
- Affiliated With, Published In, Originated By, Occurred At
- Owns, Owned By

Respond with JSON:
{{
  "entities": [
    {{"name": "Entity Name", "type": "Person|Organization|...", "prominence": 1-10}}
  ],
  "relationships": [
    {{"source": "Entity Name", "target": "Entity Name", "type": "Relationship Type"}}
  ]
}}

IMPORTANT:
- Prominence: 1-3 = mentioned briefly, 4-6 = discussed, 7-10 = central focus
- Only extract entities actually discussed, not just mentioned in passing
- Relationships must connect entities that appear in the same text
"""

        response = self.model.generate_content(prompt)
        data = json.loads(response.text)

        entities = []
        entity_name_to_obj = {}

        # Process entities
        for e in data.get('entities', []):
            entity = self.registry.find_or_create(e['name'], e['type'])
            entity.prominence = max(entity.prominence, e.get('prominence', 5))
            entities.append(entity)
            entity_name_to_obj[e['name'].lower()] = entity

        # Process relationships
        relationships = []
        for r in data.get('relationships', []):
            source = entity_name_to_obj.get(r['source'].lower())
            target = entity_name_to_obj.get(r['target'].lower())

            if source and target:
                relationships.append(Relationship(
                    source_entity_id=source.id,
                    target_entity_id=target.id,
                    relationship_type=r['type'],
                    source_record_id=record.id
                ))

        return entities, relationships
```

## PDF archival generation

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from pathlib import Path

class ArchivePDFGenerator:
    """Generate accessible PDFs for archival preservation."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.styles = getSampleStyleSheet()

        # Custom styles
        self.styles.add(ParagraphStyle(
            'ArchiveTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12
        ))
        self.styles.add(ParagraphStyle(
            'ArchiveMeta',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor='#666666',
            spaceAfter=6
        ))

    def generate(self, record: ArchiveRecord) -> Path:
        output_path = self.output_dir / f"{record.id}.pdf"

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            title=record.title,
            author=record.author or 'Unknown',
            subject=f"Archive record {record.id}"
        )

        story = []

        # Title
        story.append(Paragraph(record.title, self.styles['ArchiveTitle']))

        # Metadata block
        meta_lines = [
            f"<b>Author:</b> {record.author or 'Unknown'}",
            f"<b>Date:</b> {record.publication_date or 'Unknown'}",
            f"<b>Source:</b> {record.publication or 'Unknown'}",
            f"<b>URL:</b> {record.url}",
            f"<b>Archive ID:</b> {record.id}",
        ]
        for line in meta_lines:
            story.append(Paragraph(line, self.styles['ArchiveMeta']))

        story.append(Spacer(1, 0.25 * inch))

        # Summary (if available)
        if record.summary:
            story.append(Paragraph("<b>Summary:</b>", self.styles['Heading2']))
            story.append(Paragraph(record.summary, self.styles['Normal']))
            story.append(Spacer(1, 0.25 * inch))

        # Main content
        story.append(Paragraph("<b>Full Text:</b>", self.styles['Heading2']))

        # Split into paragraphs and add
        paragraphs = record.text.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), self.styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))

        # Build PDF
        doc.build(story)

        return output_path
```

## Data quality and validation

```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class ValidationResult:
    field: str
    valid: bool
    message: str
    severity: Literal['error', 'warning', 'info']

class ArchiveValidator:
    """Validate archive records for completeness and consistency."""

    REQUIRED_FIELDS = ['id', 'url', 'title', 'text']
    CRITICAL_FIELDS = ['publication_date', 'author', 'summary']
    OPTIONAL_FIELDS = ['categories', 'tags', 'pull_quote']

    def validate(self, record: ArchiveRecord) -> list[ValidationResult]:
        results = []

        # Required fields
        for field in self.REQUIRED_FIELDS:
            value = getattr(record, field, None)
            if not value:
                results.append(ValidationResult(
                    field=field,
                    valid=False,
                    message=f"Required field '{field}' is missing",
                    severity='error'
                ))

        # Critical fields (should have but not blocking)
        for field in self.CRITICAL_FIELDS:
            value = getattr(record, field, None)
            if not value:
                results.append(ValidationResult(
                    field=field,
                    valid=False,
                    message=f"Critical field '{field}' is missing",
                    severity='warning'
                ))

        # Content length check
        if record.text and len(record.text) < 100:
            results.append(ValidationResult(
                field='text',
                valid=False,
                message=f"Text unusually short ({len(record.text)} chars)",
                severity='warning'
            ))

        # Date format validation
        if record.publication_date:
            try:
                # Ensure date is valid
                _ = record.publication_date.isoformat()
            except (AttributeError, ValueError):
                results.append(ValidationResult(
                    field='publication_date',
                    valid=False,
                    message="Invalid date format",
                    severity='error'
                ))

        # Category validation
        for cat in record.categories:
            if cat not in ThematicCategory:
                results.append(ValidationResult(
                    field='categories',
                    valid=False,
                    message=f"Unknown category: {cat}",
                    severity='warning'
                ))

        return results

    def is_complete(self, record: ArchiveRecord) -> bool:
        """Check if record has all critical fields populated."""
        results = self.validate(record)
        errors = [r for r in results if r.severity == 'error']
        return len(errors) == 0
```

## Integration workflow

```python
class ArchiveWorkflow:
    """Orchestrate the complete archive processing pipeline."""

    def __init__(self, config: Config):
        self.scraper = ScrapingCascade()
        self.categorizer = ArchiveCategorizer()
        self.entity_registry = EntityRegistry()
        self.entity_extractor = EntityExtractor(self.entity_registry)
        self.pdf_generator = ArchivePDFGenerator(config.PDF_DIR)
        self.sheets_service = SheetsService(config.CREDENTIALS_PATH)
        self.validator = ArchiveValidator()
        self.progress = ProgressTracker(config.PROGRESS_FILE)

    def process_url(self, url: str, record_id: str) -> ArchiveRecord:
        """Process a single URL through the complete pipeline."""

        # 1. Scrape content
        result = self.scraper.fetch(url)
        if not result:
            raise ValueError(f"Failed to scrape: {url}")

        # 2. Create initial record
        record = ArchiveRecord(
            id=record_id,
            url=url,
            title=result.title,
            text=result.content
        )

        # 3. AI categorization
        categories = self.categorizer.categorize(record)
        record.summary = categories.get('summary')
        record.pull_quote = categories.get('pull_quote')
        record.categories = categories.get('categories', [])
        record.key_concepts = categories.get('key_concepts', [])
        record.tags = categories.get('tags', [])
        record.era = categories.get('era')
        record.scope = categories.get('scope')

        # 4. Entity extraction
        entities, relationships = self.entity_extractor.extract(record)
        record.entities_mentioned = [e.id for e in entities]

        # 5. Generate PDF
        pdf_path = self.pdf_generator.generate(record)
        record.pdf_url = str(pdf_path)

        # 6. Validate
        validation = self.validator.validate(record)
        record.verified = self.validator.is_complete(record)
        record.processing_status = 'completed'

        return record

    def run_batch(self, input_csv: Path):
        """Process all URLs from input CSV."""
        for row in read_input(input_csv):
            if self.progress.is_processed(row.id):
                continue

            try:
                record = self.process_url(row.url, row.id)
                self.sheets_service.append_row(self.worksheet, record_to_row(record))
                self.progress.mark_processed(row.id)
            except Exception as e:
                self.progress.log_error(row.id, str(e))
```

## Export for frontend consumption

```python
import json
from pathlib import Path

def export_for_frontend(records: list[ArchiveRecord], output_dir: Path):
    """Export archive data in frontend-friendly formats."""

    # Main archive JSON
    archive_data = {
        'metadata': {
            'total_records': len(records),
            'last_updated': datetime.now().isoformat(),
            'schema_version': '2.0'
        },
        'records': [asdict(r) for r in records]
    }

    (output_dir / 'archive-data.json').write_text(
        json.dumps(archive_data, indent=2, default=str)
    )

    # Entity export
    entities_data = [asdict(e) for e in entity_registry.entities.values()]
    (output_dir / 'entities.json').write_text(
        json.dumps(entities_data, indent=2)
    )

    # Relationships export
    relationships_data = [asdict(r) for r in all_relationships]
    (output_dir / 'relationships.json').write_text(
        json.dumps(relationships_data, indent=2)
    )

    # CSV exports for spreadsheet compatibility
    records_df = pd.DataFrame([asdict(r) for r in records])
    records_df.to_csv(output_dir / 'archive_records.csv', index=False)
```
