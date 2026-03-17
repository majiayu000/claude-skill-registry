---
name: unstructured
description: Python library for preprocessing unstructured documents (PDFs, HTML, Word, PowerPoint, images, etc.) into structured formats for downstream ML/NLP tasks
version: 0.21.5
ecosystem: python
license: Apache-2.0
generated_with: gpt-4.1
---

# unstructured

## Imports

```python
# Auto-detection and partitioning
from unstructured.partition.auto import partition

# Specialized partitioners
from unstructured.partition.html import partition_html
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.md import partition_md

# Chunking
from unstructured.chunking.dispatch import add_chunking_strategy
from unstructured.chunking.base import CHUNK_MAX_CHARS_DEFAULT

# Serialization
from unstructured.staging.base import (
    elements_to_json,
    elements_from_json
)

# Element types
from unstructured.documents.elements import (
    Element,
    Title,
    NarrativeText,
    ListItem,
    Table,
    Image,
    Header,
    Footer,
    ElementMetadata
)

# Metrics and evaluation
from unstructured.metrics.element_type import (
    get_element_type_frequency,
    calculate_element_type_percent_match
)
from unstructured.metrics.table.table_eval import (
    calculate_table_detection_metrics
)
from unstructured.metrics.evaluate import (
    TextExtractionMetricsCalculator,
    ElementTypeMetricsCalculator,
    TableStructureMetricsCalculator,
    get_mean_grouping,
    filter_metrics
)

# Utilities
from unstructured.utils import (
    save_as_jsonl,
    read_from_jsonl,
    first,
    only,
    requires_dependencies,
    catch_overlapping_and_nested_bboxes
)

# Error handling
from unstructured.partition.common import UnsupportedFileFormatError
```

## Installation

```bash
# Base package (text, HTML, XML, JSON, emails only)
pip install unstructured

# All document types
pip install "unstructured[all-docs]"

# Specific document types
pip install "unstructured[docx,pptx]"
pip install "unstructured[pdf]"
```

**⚠️ Python 3.11+ Required**: As of v0.20.0, minimum Python version is 3.11. Supports Python 3.11, 3.12, and 3.13.

## Quick Start

```python
from unstructured.partition.auto import partition

# Auto-detect file type and extract elements
elements = partition(filename="document.pdf")

# Each element has text, type, and metadata
for element in elements:
    print(f"{element.category}: {element.text[:100]}")
    print(f"Page: {element.metadata.page_number}")
```

## Core Concepts

### Elements
All partitioners return a list of `Element` objects. Common element types:
- `Title` - Document titles and section headings
- `NarrativeText` - Paragraphs and prose
- `ListItem` - Bulleted or numbered list items
- `Table` - Tabular data
- `Image` - Image elements
- `Footer` / `Header` - Page headers and footers

### Partitioning
The `partition()` function auto-detects file types and routes to specialized partitioners:

```python
from unstructured.partition.auto import partition

# From file path
elements = partition(filename="document.pdf")

# From file object
with open("document.pdf", "rb") as f:
    elements = partition(file=f)

# From raw bytes
with open("document.pdf", "rb") as f:
    elements = partition(file=f, content_type="application/pdf")
```

### Chunking
Split elements into chunks for vector databases or LLM contexts:

```python
from unstructured.partition.auto import partition
from unstructured.chunking.dispatch import add_chunking_strategy

elements = partition(filename="document.pdf")

# Apply chunking strategy
chunks = add_chunking_strategy(
    elements,
    chunking_strategy="by_title",
    max_characters=1000,
    combine_text_under_n_chars=100
)
```

### Serialization
Convert elements to JSON or other formats:

```python
from unstructured.staging.base import elements_to_json, elements_from_json

# To JSON string
json_string = elements_to_json(elements)

# From JSON string
elements = elements_from_json(json_string)
```

## Core Patterns

### Pattern 1: Basic Document Partitioning

```python
from unstructured.partition.auto import partition

# Partition a document
elements = partition(filename="report.pdf")

# Filter by element type
titles = [el for el in elements if el.category == "Title"]
text = [el for el in elements if el.category == "NarrativeText"]

# Access metadata
for element in elements:
    print(f"Text: {element.text}")
    print(f"Type: {element.category}")
    if element.metadata.page_number:
        print(f"Page: {element.metadata.page_number}")
```

### Pattern 2: HTML Partitioning

```python
from unstructured.partition.html import partition_html

# From file
elements = partition_html(filename="page.html")

# From URL
elements = partition_html(url="https://example.com/page.html")

# From string
html_string = "<html><body><h1>Title</h1><p>Text</p></body></html>"
elements = partition_html(text=html_string)
```

### Pattern 3: Chunking with Strategy

```python
from unstructured.partition.auto import partition
from unstructured.chunking.dispatch import add_chunking_strategy
from unstructured.chunking.base import CHUNK_MAX_CHARS_DEFAULT

elements = partition(filename="long_document.pdf")

# Chunk by title sections
chunks = add_chunking_strategy(
    elements,
    chunking_strategy="by_title",
    max_characters=CHUNK_MAX_CHARS_DEFAULT,  # Default: 500
    combine_text_under_n_chars=100,
    new_after_n_chars=400
)

# Each chunk is an element with combined text
for chunk in chunks:
    print(f"Chunk ({len(chunk.text)} chars): {chunk.text[:100]}...")
```

### Pattern 4: Language Detection

```python
from unstructured.partition.auto import partition

# Default language detection
elements = partition(filename="multilingual.pdf")

# Detect language per element
elements = partition(
    filename="document.pdf",
    detect_language_per_element=True
)

# Custom fallback for short text
def my_language_fallback(text: str):
    """Custom logic for short ASCII text."""
    if len(text) < 10 and text.isascii():
        return ["spa"]  # ISO 639-3 code for Spanish
    return None

elements = partition(
    filename="document.pdf",
    language_fallback=my_language_fallback
)

# Access detected language
for element in elements:
    if hasattr(element.metadata, 'languages'):
        print(f"Languages: {element.metadata.languages}")
```

### Pattern 5: Serialization and Storage

```python
from unstructured.partition.auto import partition
from unstructured.staging.base import elements_to_json, elements_from_json
from unstructured.utils import save_as_jsonl, read_from_jsonl

elements = partition(filename="document.pdf")

# To JSON string
json_str = elements_to_json(elements)

# From JSON string
restored = elements_from_json(json_str)

# Save as JSONL file
data = [{"text": el.text, "type": el.category} for el in elements]
save_as_jsonl(data, "output.jsonl")

# Read from JSONL file
data = read_from_jsonl("output.jsonl")
```

### Pattern 6: Table Extraction and Evaluation

```python
from unstructured.partition.auto import partition
from unstructured.metrics.table.table_eval import calculate_table_detection_metrics

# Extract tables from document
elements = partition(filename="tables.pdf")
tables = [el for el in elements if el.category == "Table"]

# Evaluate table detection (for testing/validation)
matched_indices = [0, 1, 2]  # Indices of matched tables
ground_truth_count = 3

recall, precision, f1 = calculate_table_detection_metrics(
    matched_indices=matched_indices,
    ground_truth_tables_number=ground_truth_count
)
print(f"Table Detection - Recall: {recall}, Precision: {precision}, F1: {f1}")
```

### Pattern 7: Document Element Type Metrics

```python
from unstructured.partition.auto import partition
from unstructured.staging.base import elements_to_json
from unstructured.metrics.element_type import (
    get_element_type_frequency,
    calculate_element_type_percent_match
)

# Get element type distribution
elements = partition(filename="document.pdf")
json_output = elements_to_json(elements)
frequency = get_element_type_frequency(json_output)

# Format: {('ElementType', depth): count}
# Example: {('Title', None): 5, ('NarrativeText', None): 20, ('ListItem', 1): 10}
print(frequency)

# Compare against expected distribution
expected_frequency = {
    ('Title', None): 5,
    ('NarrativeText', None): 18,
    ('ListItem', 1): 12
}

match_percent = calculate_element_type_percent_match(
    frequency,
    expected_frequency,
    threshold=0.8  # Weight threshold for comparison
)
print(f"Element type match: {match_percent:.2%}")
```

### Pattern 8: Bulk Document Evaluation

```python
from unstructured.metrics.evaluate import (
    TextExtractionMetricsCalculator,
    ElementTypeMetricsCalculator,
    TableStructureMetricsCalculator
)

# Text extraction metrics (CCT accuracy)
calculator = TextExtractionMetricsCalculator(
    documents_dir="output_docs/",
    ground_truths_dir="ground_truth_docs/"
)
df = calculator.calculate(
    export_dir="metrics_output/",
    visualize_progress=True,
    display_agg_df=True
)

# Element type classification metrics
element_calculator = ElementTypeMetricsCalculator(
    documents_dir="output_docs/",
    ground_truths_dir="ground_truth_docs/"
)
df = element_calculator.calculate(export_dir="metrics_output/")

# Table structure metrics
table_calculator = TableStructureMetricsCalculator(
    documents_dir="output_docs/",
    ground_truths_dir="ground_truth_docs/"
)
df = table_calculator.calculate(export_dir="metrics_output/")
```

### Pattern 9: Dependency Checking Decorator

```python
from unstructured.utils import requires_dependencies

@requires_dependencies("pdfplumber")
def process_pdf_with_pdfplumber(filename):
    """This function requires pdfplumber to be installed."""
    import pdfplumber
    # Process PDF
    pass

# Will raise ImportError with helpful message if pdfplumber not installed
process_pdf_with_pdfplumber("document.pdf")
```

### Pattern 10: Bounding Box Validation

```python
from unstructured.partition.auto import partition
from unstructured.utils import catch_overlapping_and_nested_bboxes

elements = partition(filename="document.pdf")

# Detect overlapping or nested bounding boxes
has_issues, issue_list = catch_overlapping_and_nested_bboxes(
    elements,
    nested_error_tolerance_px=5,
    sm_overlap_threshold=10.0
)

if has_issues:
    print(f"Found {len(issue_list)} bounding box issues")
    for issue in issue_list:
        print(f"Issue: {issue}")
```

## API Reference

### Core Functions

#### partition
```python
from unstructured.partition.auto import partition

elements = partition(
    filename: str = None,
    file: IO[bytes] = None,
    content_type: str = None,
    languages: List[str] = None,
    detect_language_per_element: bool = False,
    language_fallback: Callable[[str], Optional[List[str]]] = None,
    **kwargs
) -> List[Element]
```
Auto-detects file type and extracts structured elements. Main entry point for document processing.

#### partition_html
```python
from unstructured.partition.html import partition_html

elements = partition_html(
    filename: Optional[str] = None,
    file: Optional[IO[bytes]] = None,
    text: Optional[str] = None,
    url: Optional[str] = None,
    **kwargs
) -> List[Element]
```
Partition HTML documents from file, string, or URL.

#### add_chunking_strategy
```python
from unstructured.chunking.dispatch import add_chunking_strategy

chunks = add_chunking_strategy(
    elements: List[Element],
    chunking_strategy: str = "by_title",  # or "basic"
    max_characters: int = 500,
    combine_text_under_n_chars: int = 0,
    new_after_n_chars: Optional[int] = None,
    **kwargs
) -> List[Element]
```
Apply chunking strategy to elements for downstream processing.

#### elements_to_json / elements_from_json
```python
from unstructured.staging.base import elements_to_json, elements_from_json

# Serialize to JSON
json_string = elements_to_json(elements: List[Element], **kwargs) -> str

# Deserialize from JSON
elements = elements_from_json(text: str, **kwargs) -> List[Element]
```

### Element Classes

#### Element (Base Class)
```python
from unstructured.documents.elements import Element

element = Element(
    text: str,
    element_id: str = None,
    metadata: ElementMetadata = None,
    **kwargs
)

# Properties
element.text          # Element text content
element.category      # Element type (e.g., "Title", "NarrativeText")
element.metadata      # ElementMetadata object
element.id            # Unique identifier
```

#### Specialized Elements
```python
from unstructured.documents.elements import (
    Title,
    NarrativeText,
    ListItem,
    Table,
    Image,
    Header,
    Footer
)

# All follow same constructor pattern
title = Title(text="Document Title", **kwargs)
paragraph = NarrativeText(text="Paragraph content", **kwargs)
```

#### ElementMetadata
```python
from unstructured.documents.elements import ElementMetadata

metadata = ElementMetadata(
    page_number: Optional[int] = None,
    filename: Optional[str] = None,
    languages: Optional[List[str]] = None,
    **kwargs
)
```

### Metrics and Evaluation

#### Element Type Metrics
```python
from unstructured.metrics.element_type import (
    get_element_type_frequency,
    calculate_element_type_percent_match
)

# Get frequency distribution
frequency = get_element_type_frequency(
    elements_json: str
) -> Dict[Tuple[str, Optional[int]], int]

# Compare distributions
match_percent = calculate_element_type_percent_match(
    frequency1: Dict,
    frequency2: Dict,
    threshold: float = 0.0
) -> float
```

#### Table Metrics
```python
from unstructured.metrics.table.table_eval import calculate_table_detection_metrics

recall, precision, f1 = calculate_table_detection_metrics(
    matched_indices: List[int],
    ground_truth_tables_number: int
) -> Tuple[float, float, float]
```

#### Bulk Evaluation
```python
from unstructured.metrics.evaluate import (
    TextExtractionMetricsCalculator,
    ElementTypeMetricsCalculator,
    TableStructureMetricsCalculator,
    get_mean_grouping,
    filter_metrics
)

# Initialize calculator
calculator = TextExtractionMetricsCalculator(
    documents_dir: str,
    ground_truths_dir: str,
    document_type: str = "json",  # or "txt"
    group_by: Optional[str] = None  # e.g., "doctype", "connector"
)

# Calculate metrics
df = calculator.calculate(
    export_dir: str,
    visualize_progress: bool = True,
    display_agg_df: bool = True
) -> pd.DataFrame

# Aggregate by grouping
agg_df = get_mean_grouping(
    group_by: str,  # e.g., "doctype"
    data_input: Union[pd.DataFrame, str],  # DataFrame or TSV file path
    export_dir: str,
    eval_name: str  # "text_extraction", "element_type", or "table_structure"
) -> pd.DataFrame

# Filter metrics
filtered_df = filter_metrics(
    data_input: Union[pd.DataFrame, str],
    filter_list: str,  # Path to file with filter values
    filter_by: str,  # Column name to filter by
    export_filename: str,
    export_dir: str,
    return_type: str = "file"  # or "df"
) -> Optional[pd.DataFrame]
```

### Utility Functions

#### JSONL Operations
```python
from unstructured.utils import save_as_jsonl, read_from_jsonl

# Save list of dicts to JSONL
save_as_jsonl(
    data: List[Dict[str, Any]],
    filepath: str
) -> None

# Read JSONL file
data = read_from_jsonl(filepath: str) -> List[Dict[str, Any]]
```

#### Iterator Utilities
```python
from unstructured.utils import first, only

# Get first element (raises ValueError if empty)
first_item = first(iterator: Iterable[T]) -> T

# Get only element (raises ValueError if not exactly one)
only_item = only(iterator: Iterable[T]) -> T
```

#### Dependency Checking
```python
from unstructured.utils import requires_dependencies

@requires_dependencies("package_name")
def my_function():
    # Function requires package_name
    pass

# Can specify multiple dependencies
@requires_dependencies(["package1", "package2"])
def another_function():
    pass
```

### ⚠️ Deprecated APIs

The following embedding encoders are deprecated as of v0.21.5. Functionality has moved to the separate `unstructured-ingest` project. They still work but are no longer recommended for new code:

```python
# ⚠️ Deprecated - Use unstructured-ingest project instead
from unstructured.embed.openai import OpenAIEmbeddingEncoder
from unstructured.embed.huggingface import HuggingFaceEmbeddingEncoder
from unstructured.embed.bedrock import BedrockEmbeddingEncoder
from unstructured.embed.vertexai import VertexAIEmbeddingEncoder
from unstructured.embed.voyageai import VoyageAIEmbeddingEncoder
from unstructured.embed.mixedbreadai import MixedbreadAIEmbeddingEncoder
from unstructured.embed.octoai import OctoAIEmbeddingEncoder
```

**Migration**: Install and use the `unstructured-ingest` project for embedding functionality.

## Error Handling

```python
from unstructured.partition.auto import partition
from unstructured.partition.common import UnsupportedFileFormatError

try:
    elements = partition(filename="document.xyz")
except UnsupportedFileFormatError as e:
    print(f"File format not supported: {e}")
except Exception as e:
    print(f"Error processing document: {e}")
```

## Configuration and Environment

### Analytics Opt-Out
```bash
export DO_NOT_TRACK=true
```

### PDF Character Deduplication
```bash
# Configure threshold for bold text deduplication (default: 2.0 pixels)
export PDF_CHAR_DUPLICATE_THRESHOLD=2.0

# Disable deduplication
export PDF_CHAR_DUPLICATE_THRESHOLD=0
```

## Development Setup

```bash
# Clone repository
git clone https://github.com/Unstructured-IO/unstructured.git
cd unstructured

# Install dependencies (requires uv)
make install

# Run tests
make test

# Check linting/formatting
make check

# Apply formatting
make tidy

# Update lockfile after pyproject.toml changes
make lock

# Start development Docker environment
make docker-start-dev
```

## Migration Guide

### Upgrading to v0.21.x

#### From v0.20.x to v0.21.0 (Security Update)
**NLTK Removed** (CVE-2025-14009 - CVSS 10.0 RCE vulnerability):
- Language detection now uses spaCy instead of NLTK
- spaCy model `en-core-web-sm` auto-installs at runtime with SHA256 verification
- **No code changes required** for most users
- If you imported NLTK directly, update to use spaCy

#### From v0.19.x to v0.20.0 (Python Version)
**Python 3.11+ Required**:
```python
# Before (Python 3.8+)
pip install unstructured

# After (Python 3.11+ required)
pip install unstructured  # Requires Python 3.11, 3.12, or 3.13
```

**Action Items**:
1. Upgrade to Python 3.11 or later
2. Update `unstructured-ingest` to `>=1.4.0`
3. Remove Python 3.8/3.9/3.10-specific workarounds

#### v0.21.3: Language Detection Enhancements
**New Parameters**:
```python
from unstructured.partition.auto import partition
from unstructured.partition.md import partition_md

# Custom fallback for short ASCII text
def my_fallback(text: str):
    if len(text) < 10 and text.isascii():
        return ["fra"]  # French
    return None

elements = partition(
    filename="document.pdf",
    language_fallback=my_fallback
)

# Disable language detection in Markdown
elements = partition_md(
    filename="document.md",
    languages=[""]  # Empty string disables detection
)
```

#### v0.20.6: Security - Decompression Limits
Elements JSON decompression now has automatic size limits to prevent resource exhaustion. No code changes required.

#### v0.20.5: Chunking Error Handling
Invalid `text_as_html` in elements no longer crashes chunking:
```python
# Before: Would raise lxml.etree.ParserError
chunks = add_chunking_strategy(elements_with_bad_html)

# After: Logs WARNING and continues with plain-text fallback
chunks = add_chunking_strategy(elements_with_bad_html)
```

#### v0.20.3: PDF Bold Text Fix
Automatic deduplication of fake-bold characters (where bold is rendered by drawing twice):
```python
# Configure threshold (default: 2.0 pixels)
import os
os.environ["PDF_CHAR_DUPLICATE_THRESHOLD"] = "2.0"

# Disable deduplication
os.environ["PDF_CHAR_DUPLICATE_THRESHOLD"] = "0"
```

### Dependency Management
```bash
# Use --locked instead of --frozen (fails fast on stale lockfiles)
uv sync --locked

# Prevent implicit re-syncing
uv run --no-sync pytest
uv build --no-sync

# Update lockfile after changes
make lock
```

## Pitfalls

### ❌ Installing base package for all document types
```python
pip install unstructured
# Only supports text, HTML, XML, JSON, emails
```

### ✅ Install with extras
```python
pip install "unstructured[all-docs]"  # All document types
# OR
pip install "unstructured[pdf,docx]"  # Specific types
```

### ❌ Using frozen lockfile sync
```bash
uv sync --frozen  # Doesn't fail fast on stale lockfiles
```

### ✅ Use locked sync
```bash
uv sync --locked  # Fails immediately if lockfile is stale
```

---

### ❌ Assuming all PDFs are readable
```python
elements = partition(filename="scanned_image.pdf")
# May return empty or minimal text for image-based PDFs
```

### ✅ Use OCR strategy for image-based PDFs
```python
# Requires unstructured[pdf] with OCR dependencies
elements = partition(
    filename="scanned_image.pdf",
    strategy="ocr_only"  # or "hi_res" for mixed content
)
```

## Resources

- Official Documentation: https://docs.unstructured.io/
- GitHub Repository: https://github.com/Unstructured-IO/unstructured
- Changelog: View project changelog on GitHub
- unstructured-ingest: https://github.com/Unstructured-IO/unstructured-ingest

## References

- [Homepage](https://github.com/Unstructured-IO/unstructured)
