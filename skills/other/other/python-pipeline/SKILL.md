---
name: python-pipeline
description: Python data processing pipelines with modular architecture. Use when building content processing workflows, implementing dispatcher patterns, integrating Google Sheets/Drive APIs, or creating batch processing systems. Covers patterns from rosen-scraper, image-analyzer, and social-scraper projects.
---

# Python data pipeline development

Patterns for building production-quality data processing pipelines with Python.

## Architecture patterns

### Modular processor architecture
```
src/
├── workflow.py              # Main orchestrator
├── dispatcher.py            # Content-type router
├── processors/
│   ├── __init__.py
│   ├── base.py             # Abstract base class
│   ├── article_processor.py
│   ├── video_processor.py
│   └── audio_processor.py
├── services/
│   ├── sheets_service.py   # Google Sheets integration
│   ├── drive_service.py    # Google Drive integration
│   └── ai_service.py       # Gemini API wrapper
├── utils/
│   ├── logger.py
│   └── rate_limiter.py
└── config.py               # Environment configuration
```

### Dispatcher pattern

```python
from typing import Protocol
from urllib.parse import urlparse

class Processor(Protocol):
    def can_process(self, url: str) -> bool: ...
    def process(self, url: str, metadata: dict) -> dict: ...

class Dispatcher:
    def __init__(self):
        self.processors: list[Processor] = [
            ArticleProcessor(),
            VideoProcessor(),
            AudioProcessor(),
            SocialProcessor(),
        ]

    def dispatch(self, url: str, metadata: dict) -> dict:
        for processor in self.processors:
            if processor.can_process(url):
                return processor.process(url, metadata)
        raise ValueError(f"No processor found for URL: {url}")

# Pattern-based routing
class ArticleProcessor:
    DOMAINS = ['nytimes.com', 'washingtonpost.com', 'medium.com']

    def can_process(self, url: str) -> bool:
        domain = urlparse(url).netloc.replace('www.', '')
        return any(d in domain for d in self.DOMAINS)
```

### CSV-based pipeline workflow

```python
import csv
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Iterator

@dataclass
class Record:
    id: str
    url: str
    title: str | None = None
    content: str | None = None
    status: str = 'pending'

def read_input(path: Path) -> Iterator[Record]:
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield Record(**{k: v for k, v in row.items() if k in Record.__annotations__})

def write_output(records: list[Record], path: Path):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(Record.__annotations__.keys()))
        writer.writeheader()
        writer.writerows(asdict(r) for r in records)

def process_batch(input_path: Path, output_path: Path):
    dispatcher = Dispatcher()
    results = []

    for record in read_input(input_path):
        try:
            processed = dispatcher.dispatch(record.url, asdict(record))
            record.status = 'completed'
            record.title = processed.get('title')
            record.content = processed.get('content')
        except Exception as e:
            record.status = f'failed: {e}'
        results.append(record)

    write_output(results, output_path)
```

## Google Sheets integration

```python
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

class SheetsService:
    def __init__(self, credentials_path: str):
        creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        self.client = gspread.authorize(creds)

    def get_worksheet(self, spreadsheet_id: str, sheet_name: str):
        spreadsheet = self.client.open_by_key(spreadsheet_id)
        return spreadsheet.worksheet(sheet_name)

    def read_all(self, worksheet) -> list[dict]:
        return worksheet.get_all_records()

    def append_row(self, worksheet, row: list):
        worksheet.append_row(row, value_input_option='USER_ENTERED')

    def batch_update(self, worksheet, updates: list[dict]):
        """Update multiple cells efficiently."""
        # Format: [{'range': 'A1', 'values': [[value]]}]
        worksheet.batch_update(updates, value_input_option='USER_ENTERED')

    def find_row_by_id(self, worksheet, id_value: str, id_column: int = 1) -> int | None:
        """Find row number by ID value."""
        try:
            cell = worksheet.find(id_value, in_column=id_column)
            return cell.row
        except gspread.CellNotFound:
            return None
```

## Rate limiting

```python
import time
from functools import wraps
from ratelimit import limits, sleep_and_retry

# Simple rate limiter
@sleep_and_retry
@limits(calls=10, period=60)  # 10 calls per minute
def rate_limited_api_call(url: str):
    return requests.get(url)

# Custom rate limiter with backoff
class RateLimiter:
    def __init__(self, calls_per_minute: int = 10):
        self.delay = 60 / calls_per_minute
        self.last_call = 0

    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_call = time.time()

# Usage
limiter = RateLimiter(calls_per_minute=10)

def fetch_with_rate_limit(url: str):
    limiter.wait()
    return requests.get(url)
```

## Progress tracking with resume capability

```python
import json
from pathlib import Path

class ProgressTracker:
    def __init__(self, progress_file: Path):
        self.progress_file = progress_file
        self.state = self._load()

    def _load(self) -> dict:
        if self.progress_file.exists():
            return json.loads(self.progress_file.read_text())
        return {'processed_ids': [], 'last_row': 0, 'errors': []}

    def save(self):
        self.progress_file.write_text(json.dumps(self.state, indent=2))

    def mark_processed(self, record_id: str):
        self.state['processed_ids'].append(record_id)
        self.save()

    def is_processed(self, record_id: str) -> bool:
        return record_id in self.state['processed_ids']

    def log_error(self, record_id: str, error: str):
        self.state['errors'].append({'id': record_id, 'error': error})
        self.save()

# Usage in workflow
tracker = ProgressTracker(Path('progress.json'))

for record in records:
    if tracker.is_processed(record.id):
        continue  # Skip already processed

    try:
        process(record)
        tracker.mark_processed(record.id)
    except Exception as e:
        tracker.log_error(record.id, str(e))
```

## Gemini AI integration

```python
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

class AIService:
    def __init__(self, model: str = 'gemini-2.0-flash'):
        self.model = genai.GenerativeModel(model)

    def categorize(self, text: str, taxonomy: dict) -> dict:
        prompt = f"""Analyze this content and categorize it.

Content:
{text[:10000]}  # Truncate to avoid token limits

Taxonomy:
{json.dumps(taxonomy, indent=2)}

Respond with JSON containing:
- category: one of the taxonomy categories
- tags: list of relevant tags
- summary: 2-3 sentence summary
"""
        response = self.model.generate_content(prompt)
        return json.loads(response.text)

    def extract_entities(self, text: str) -> list[dict]:
        prompt = f"""Extract named entities from this text.

Text:
{text[:10000]}

For each entity, provide:
- name: entity name
- type: Person, Organization, Location, Event, Work, or Concept
- prominence: 1-10 score based on importance in text

Respond with JSON array of entities.
"""
        response = self.model.generate_content(prompt)
        return json.loads(response.text)

# Batch processing with cost tracking
class BatchAIProcessor:
    def __init__(self, ai_service: AIService):
        self.ai = ai_service
        self.total_tokens = 0
        self.cost_per_1k_tokens = 0.00025  # Adjust for your model

    def process_batch(self, items: list[str]) -> list[dict]:
        results = []
        for item in items:
            result = self.ai.categorize(item, TAXONOMY)
            self.total_tokens += len(item) // 4  # Rough estimate
            results.append(result)
        return results

    @property
    def estimated_cost(self) -> float:
        return (self.total_tokens / 1000) * self.cost_per_1k_tokens
```

## Image classification with Gemini Vision

```python
import google.generativeai as genai
from PIL import Image
from pathlib import Path

def classify_image(image_path: Path, categories: list[str]) -> dict:
    model = genai.GenerativeModel('gemini-2.0-flash')
    image = Image.open(image_path)

    prompt = f"""Analyze this image and classify it.

Available categories: {', '.join(categories)}

Respond with JSON:
{{
  "category": "category name",
  "description": "brief description",
  "suggested_filename": "descriptive-filename-with-dashes",
  "tags": ["tag1", "tag2", "tag3"]
}}
"""
    response = model.generate_content([prompt, image])
    return json.loads(response.text)

def organize_images(source_dir: Path, output_dir: Path):
    categories = ['Nature', 'People', 'Architecture', 'Art', 'Technology', 'Other']

    for image_path in source_dir.glob('*.{jpg,png,webp}'):
        try:
            result = classify_image(image_path, categories)
            category_dir = output_dir / result['category']
            category_dir.mkdir(exist_ok=True)

            new_name = f"{result['suggested_filename']}{image_path.suffix}"
            image_path.rename(category_dir / new_name)
        except Exception as e:
            (output_dir / 'failures').mkdir(exist_ok=True)
            image_path.rename(output_dir / 'failures' / image_path.name)
```

## Environment configuration

```python
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
    GOOGLE_SHEET_ID = os.environ['GOOGLE_SHEET_ID']

    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / 'data'
    OUTPUT_DIR = PROJECT_ROOT / 'output'
    CREDENTIALS_PATH = PROJECT_ROOT / 'google_credentials.json'

    # Rate limits
    API_CALLS_PER_MINUTE = 10
    BATCH_SIZE = 50

    @classmethod
    def ensure_dirs(cls):
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
```

## Logging setup

```python
import logging
from pathlib import Path
from datetime import datetime

def setup_logging(log_dir: Path, name: str = 'pipeline') -> logging.Logger:
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console handler (INFO+)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    # File handler (DEBUG+)
    log_file = log_dir / f"{name}_{datetime.now():%Y%m%d_%H%M%S}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger
```

## Common pitfalls

**Google Sheets cell limits:**
```python
MAX_CELL_LENGTH = 50000

def truncate_for_sheets(text: str) -> str:
    if len(text) > MAX_CELL_LENGTH:
        return text[:MAX_CELL_LENGTH - 20] + '... [truncated]'
    return text
```

**CSV encoding issues:**
```python
# Always specify encoding
with open(path, 'r', encoding='utf-8-sig') as f:  # BOM handling
    reader = csv.reader(f)
```

**API quota management:**
```python
# Cache API responses
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_api_call(url: str) -> dict:
    return api_client.fetch(url)
```
