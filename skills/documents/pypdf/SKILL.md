---
name: pypdf
description: Manipulate PDF documents programmatically. Merge, split, rotate, and watermark PDFs. Extract text and metadata. Handle form filling and encryption/decryption.
version: 1.0.0
category: office-docs
type: skill
capabilities:
  - pdf_merging
  - pdf_splitting
  - page_rotation
  - watermarking
  - text_extraction
  - metadata_handling
  - form_filling
  - encryption_decryption
tools:
  - python
  - pypdf
  - reportlab
tags: [pdf, document-manipulation, merge, split, watermark, encryption, office-automation]
platforms: [windows, macos, linux]
related_skills:
  - python-docx
  - reportlab
  - pillow
---

# PyPDF PDF Manipulation Skill

## Overview

PyPDF is a pure-Python library for working with PDF files. This skill covers comprehensive patterns for PDF manipulation including:

- **PDF merging** - Combine multiple PDFs into one document
- **PDF splitting** - Extract specific pages or split into multiple files
- **Page rotation** - Rotate pages by 90, 180, or 270 degrees
- **Watermarking** - Add text or image watermarks to pages
- **Text extraction** - Extract text content from PDF pages
- **Metadata handling** - Read and modify PDF metadata
- **Form filling** - Fill PDF form fields programmatically
- **Encryption/Decryption** - Secure PDFs with passwords

## When to Use This Skill

### USE when:
- Merging multiple PDF files into a single document
- Splitting large PDFs into smaller files
- Extracting specific pages from PDFs
- Adding watermarks or stamps to documents
- Extracting text content for analysis
- Reading or modifying PDF metadata
- Filling PDF forms programmatically
- Encrypting or decrypting PDF files
- Adding page numbers or headers/footers
- Rotating or reordering pages
- Automating PDF workflows in pipelines

### DON'T USE when:
- Creating PDFs from scratch (use reportlab or weasyprint)
- Need advanced text layout control (use reportlab)
- Converting other formats to PDF (use dedicated converters)
- Need OCR for scanned documents (use pytesseract + pdf2image)
- Working with complex form creation (use reportlab)
- Need to edit existing text content (limited support)

## Prerequisites

### Installation

```bash
# Basic installation
pip install pypdf

# Using uv (recommended)
uv pip install pypdf

# With crypto support for encryption
pip install pypdf[crypto]

# For creating PDFs (watermarks, overlays)
pip install pypdf reportlab

# Full installation
pip install pypdf[crypto] reportlab Pillow
```

### Verify Installation

```python
from pypdf import PdfReader, PdfWriter, PdfMerger
from pypdf.errors import PdfReadError

print("pypdf installed successfully!")
print(f"Version: {pypdf.__version__}")
```

## Core Capabilities

### 1. PDF Merging

```python
"""
Merge multiple PDF files into a single document.
"""
from pypdf import PdfMerger, PdfReader, PdfWriter
from pathlib import Path
from typing import List, Optional

def merge_pdfs(
    pdf_paths: List[str],
    output_path: str,
    bookmarks: bool = True
) -> None:
    """Merge multiple PDFs into one file."""
    merger = PdfMerger()

    for pdf_path in pdf_paths:
        path = Path(pdf_path)
        if path.exists():
            # Add with bookmark (outline entry)
            merger.append(
                str(pdf_path),
                outline_item=path.stem if bookmarks else None
            )
            print(f"Added: {path.name}")
        else:
            print(f"Warning: File not found - {pdf_path}")

    merger.write(output_path)
    merger.close()

    print(f"Merged PDF saved to: {output_path}")


def merge_with_page_selection(
    pdf_configs: List[dict],
    output_path: str
) -> None:
    """Merge specific pages from multiple PDFs.

    Args:
        pdf_configs: List of dicts with 'path', 'pages' (optional) keys
                    pages can be tuple (start, end) or list of page numbers
        output_path: Output file path
    """
    merger = PdfMerger()

    for config in pdf_configs:
        pdf_path = config['path']
        pages = config.get('pages')

        if pages is None:
            # Add all pages
            merger.append(pdf_path)
        elif isinstance(pages, tuple):
            # Add page range (start, end)
            merger.append(pdf_path, pages=pages)
        elif isinstance(pages, list):
            # Add specific pages
            reader = PdfReader(pdf_path)
            for page_num in pages:
                if 0 <= page_num < len(reader.pages):
                    merger.append(pdf_path, pages=(page_num, page_num + 1))

        print(f"Added: {pdf_path} - Pages: {pages or 'all'}")

    merger.write(output_path)
    merger.close()

    print(f"Merged PDF saved to: {output_path}")


def merge_directory(
    directory: str,
    output_path: str,
    pattern: str = "*.pdf",
    sort_key: Optional[str] = "name"
) -> int:
    """Merge all PDFs in a directory."""
    dir_path = Path(directory)
    pdf_files = list(dir_path.glob(pattern))

    if not pdf_files:
        print(f"No PDF files found in {directory}")
        return 0

    # Sort files
    if sort_key == "name":
        pdf_files.sort(key=lambda x: x.name.lower())
    elif sort_key == "date":
        pdf_files.sort(key=lambda x: x.stat().st_mtime)
    elif sort_key == "size":
        pdf_files.sort(key=lambda x: x.stat().st_size)

    merge_pdfs([str(f) for f in pdf_files], output_path)

    return len(pdf_files)


# Example usage
# merge_pdfs(['report1.pdf', 'report2.pdf', 'appendix.pdf'], 'complete_report.pdf')
#
# merge_with_page_selection([
#     {'path': 'doc1.pdf', 'pages': (0, 5)},  # First 5 pages
#     {'path': 'doc2.pdf', 'pages': [0, 2, 4]},  # Pages 1, 3, 5
#     {'path': 'doc3.pdf'}  # All pages
# ], 'combined.pdf')
```

### 2. PDF Splitting

```python
"""
Split PDF files into separate documents.
"""
from pypdf import PdfReader, PdfWriter
from pathlib import Path
from typing import List, Tuple, Optional

def split_pdf_by_pages(
    input_path: str,
    output_dir: str,
    pages_per_file: int = 1
) -> List[str]:
    """Split PDF into multiple files with specified pages per file."""
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    input_name = Path(input_path).stem
    created_files = []

    for start in range(0, total_pages, pages_per_file):
        writer = PdfWriter()
        end = min(start + pages_per_file, total_pages)

        for page_num in range(start, end):
            writer.add_page(reader.pages[page_num])

        # Generate output filename
        if pages_per_file == 1:
            output_file = output_path / f"{input_name}_page_{start + 1}.pdf"
        else:
            output_file = output_path / f"{input_name}_pages_{start + 1}-{end}.pdf"

        writer.write(str(output_file))
        created_files.append(str(output_file))

        print(f"Created: {output_file.name}")

    print(f"Split into {len(created_files)} files")
    return created_files


def extract_pages(
    input_path: str,
    output_path: str,
    page_numbers: List[int]
) -> None:
    """Extract specific pages from a PDF.

    Args:
        input_path: Source PDF file
        output_path: Destination file
        page_numbers: List of page numbers (0-indexed)
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_num in page_numbers:
        if 0 <= page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])
            print(f"Extracted page {page_num + 1}")
        else:
            print(f"Warning: Page {page_num + 1} out of range")

    writer.write(output_path)
    print(f"Extracted pages saved to: {output_path}")


def split_by_ranges(
    input_path: str,
    output_dir: str,
    ranges: List[Tuple[int, int, str]]
) -> List[str]:
    """Split PDF by specified page ranges.

    Args:
        input_path: Source PDF file
        output_dir: Output directory
        ranges: List of (start, end, name) tuples
                start and end are 0-indexed
    """
    reader = PdfReader(input_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    created_files = []

    for start, end, name in ranges:
        writer = PdfWriter()

        for page_num in range(start, min(end, len(reader.pages))):
            writer.add_page(reader.pages[page_num])

        output_file = output_path / f"{name}.pdf"
        writer.write(str(output_file))
        created_files.append(str(output_file))

        print(f"Created: {output_file.name} (pages {start + 1}-{end})")

    return created_files


def split_by_bookmarks(
    input_path: str,
    output_dir: str
) -> List[str]:
    """Split PDF by bookmark (outline) entries."""
    reader = PdfReader(input_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not reader.outline:
        print("No bookmarks found in PDF")
        return []

    created_files = []

    # Get bookmark page numbers
    bookmarks = []
    for item in reader.outline:
        if isinstance(item, list):
            continue  # Skip nested bookmarks
        try:
            page_num = reader.get_destination_page_number(item)
            title = item.title
            bookmarks.append((page_num, title))
        except:
            continue

    # Sort by page number
    bookmarks.sort(key=lambda x: x[0])

    # Add end marker
    bookmarks.append((len(reader.pages), "END"))

    # Create PDFs for each section
    for i in range(len(bookmarks) - 1):
        start_page, title = bookmarks[i]
        end_page = bookmarks[i + 1][0]

        if start_page >= end_page:
            continue

        writer = PdfWriter()
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        # Clean filename
        safe_title = "".join(c if c.isalnum() or c in ' -_' else '_' for c in title)
        output_file = output_path / f"{i + 1:02d}_{safe_title}.pdf"

        writer.write(str(output_file))
        created_files.append(str(output_file))

        print(f"Created: {output_file.name}")

    return created_files


# Example usage
# split_pdf_by_pages('large_document.pdf', 'split_output/', pages_per_file=10)
# extract_pages('document.pdf', 'selected_pages.pdf', [0, 4, 9])  # Pages 1, 5, 10
# split_by_ranges('manual.pdf', 'chapters/', [
#     (0, 10, 'chapter_1'),
#     (10, 25, 'chapter_2'),
#     (25, 40, 'chapter_3')
# ])
```

### 3. Page Rotation and Transformation

```python
"""
Rotate, crop, and transform PDF pages.
"""
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject
from pathlib import Path
from typing import List, Optional

def rotate_pages(
    input_path: str,
    output_path: str,
    rotation: int,
    pages: Optional[List[int]] = None
) -> None:
    """Rotate PDF pages by specified degrees.

    Args:
        input_path: Source PDF file
        output_path: Destination file
        rotation: Rotation in degrees (90, 180, or 270)
        pages: List of page numbers to rotate (0-indexed), None for all
    """
    if rotation not in [90, 180, 270]:
        raise ValueError("Rotation must be 90, 180, or 270 degrees")

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if pages is None or i in pages:
            page.rotate(rotation)
        writer.add_page(page)

    writer.write(output_path)
    print(f"Rotated PDF saved to: {output_path}")


def rotate_landscape_pages(
    input_path: str,
    output_path: str
) -> int:
    """Automatically rotate landscape pages to portrait."""
    reader = PdfReader(input_path)
    writer = PdfWriter()

    rotated_count = 0

    for page in reader.pages:
        # Get page dimensions
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        # Rotate if landscape
        if width > height:
            page.rotate(90)
            rotated_count += 1

        writer.add_page(page)

    writer.write(output_path)
    print(f"Rotated {rotated_count} landscape pages")
    return rotated_count


def crop_pages(
    input_path: str,
    output_path: str,
    crop_box: tuple,
    pages: Optional[List[int]] = None
) -> None:
    """Crop PDF pages to specified dimensions.

    Args:
        input_path: Source PDF file
        output_path: Destination file
        crop_box: (left, bottom, right, top) in points (72 points = 1 inch)
        pages: List of page numbers to crop (0-indexed), None for all
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    left, bottom, right, top = crop_box

    for i, page in enumerate(reader.pages):
        if pages is None or i in pages:
            page.mediabox = RectangleObject([left, bottom, right, top])
            page.cropbox = RectangleObject([left, bottom, right, top])

        writer.add_page(page)

    writer.write(output_path)
    print(f"Cropped PDF saved to: {output_path}")


def scale_pages(
    input_path: str,
    output_path: str,
    scale_x: float = 1.0,
    scale_y: float = 1.0
) -> None:
    """Scale PDF pages by specified factors."""
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        # Apply transformation
        op = Transformation().scale(sx=scale_x, sy=scale_y)
        page.add_transformation(op)

        # Update media box
        page.mediabox.lower_left = (
            float(page.mediabox.lower_left[0]) * scale_x,
            float(page.mediabox.lower_left[1]) * scale_y
        )
        page.mediabox.upper_right = (
            float(page.mediabox.upper_right[0]) * scale_x,
            float(page.mediabox.upper_right[1]) * scale_y
        )

        writer.add_page(page)

    writer.write(output_path)
    print(f"Scaled PDF saved to: {output_path}")


def reorder_pages(
    input_path: str,
    output_path: str,
    new_order: List[int]
) -> None:
    """Reorder PDF pages according to specified order.

    Args:
        input_path: Source PDF file
        output_path: Destination file
        new_order: List of page indices in desired order (0-indexed)
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_num in new_order:
        if 0 <= page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])

    writer.write(output_path)
    print(f"Reordered PDF saved to: {output_path}")


# Example usage
# rotate_pages('document.pdf', 'rotated.pdf', 90)
# rotate_pages('document.pdf', 'rotated.pdf', 90, pages=[0, 2, 4])
# crop_pages('document.pdf', 'cropped.pdf', (72, 72, 540, 720))  # 1 inch margins
# reorder_pages('document.pdf', 'reordered.pdf', [2, 0, 1, 4, 3])
```

### 4. Watermarking and Stamping

```python
"""
Add watermarks, stamps, and overlays to PDF pages.
"""
from pypdf import PdfReader, PdfWriter
from pathlib import Path
from typing import Optional, Tuple
from io import BytesIO

# For creating watermarks
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import Color
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def create_text_watermark(
    text: str,
    output_path: str,
    font_size: int = 60,
    opacity: float = 0.3,
    rotation: int = 45,
    color: Tuple[float, float, float] = (0.5, 0.5, 0.5)
) -> str:
    """Create a watermark PDF with specified text."""
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab is required for creating watermarks")

    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    width, height = letter

    # Set transparency
    c.setFillColor(Color(*color, alpha=opacity))

    # Save state, rotate, draw text
    c.saveState()
    c.translate(width / 2, height / 2)
    c.rotate(rotation)
    c.setFont("Helvetica-Bold", font_size)

    # Draw text centered
    text_width = c.stringWidth(text, "Helvetica-Bold", font_size)
    c.drawString(-text_width / 2, 0, text)

    c.restoreState()
    c.save()

    # Write to file
    packet.seek(0)
    with open(output_path, 'wb') as f:
        f.write(packet.getvalue())

    return output_path


def add_watermark(
    input_path: str,
    watermark_path: str,
    output_path: str,
    pages: Optional[list] = None
) -> None:
    """Add watermark to PDF pages.

    Args:
        input_path: Source PDF file
        watermark_path: Watermark PDF file
        output_path: Destination file
        pages: List of page numbers to watermark (0-indexed), None for all
    """
    reader = PdfReader(input_path)
    watermark_reader = PdfReader(watermark_path)
    watermark_page = watermark_reader.pages[0]

    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if pages is None or i in pages:
            page.merge_page(watermark_page)
        writer.add_page(page)

    writer.write(output_path)
    print(f"Watermarked PDF saved to: {output_path}")


def add_page_numbers(
    input_path: str,
    output_path: str,
    position: str = "bottom-center",
    start_number: int = 1,
    prefix: str = "Page ",
    font_size: int = 10
) -> None:
    """Add page numbers to PDF.

    Args:
        input_path: Source PDF file
        output_path: Destination file
        position: Position of page number (bottom-center, bottom-right, etc.)
        start_number: Starting page number
        prefix: Text before page number
        font_size: Font size for page numbers
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab is required for adding page numbers")

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        # Get page dimensions
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        # Create page number overlay
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=(width, height))

        # Calculate position
        page_num_text = f"{prefix}{start_number + i}"

        if position == "bottom-center":
            x = width / 2
            y = 30
        elif position == "bottom-right":
            x = width - 50
            y = 30
        elif position == "top-center":
            x = width / 2
            y = height - 30
        elif position == "top-right":
            x = width - 50
            y = height - 30
        else:
            x = width / 2
            y = 30

        c.setFont("Helvetica", font_size)
        text_width = c.stringWidth(page_num_text, "Helvetica", font_size)

        if "center" in position:
            x -= text_width / 2

        c.drawString(x, y, page_num_text)
        c.save()

        # Merge with page
        packet.seek(0)
        overlay = PdfReader(packet)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

    writer.write(output_path)
    print(f"Page numbers added to: {output_path}")


def add_header_footer(
    input_path: str,
    output_path: str,
    header: Optional[str] = None,
    footer: Optional[str] = None,
    font_size: int = 10
) -> None:
    """Add header and/or footer to all pages."""
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab is required for adding headers/footers")

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        # Create overlay
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=(width, height))
        c.setFont("Helvetica", font_size)

        if header:
            text_width = c.stringWidth(header, "Helvetica", font_size)
            c.drawString((width - text_width) / 2, height - 30, header)

        if footer:
            text_width = c.stringWidth(footer, "Helvetica", font_size)
            c.drawString((width - text_width) / 2, 20, footer)

        c.save()

        # Merge
        packet.seek(0)
        overlay = PdfReader(packet)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

    writer.write(output_path)
    print(f"Header/footer added to: {output_path}")


# Example usage
# create_text_watermark("CONFIDENTIAL", "watermark.pdf")
# add_watermark("document.pdf", "watermark.pdf", "watermarked_document.pdf")
# add_page_numbers("document.pdf", "numbered.pdf", position="bottom-center")
# add_header_footer("document.pdf", "with_header.pdf",
#                   header="Company Name - Confidential",
#                   footer="Do not distribute")
```

### 5. Text Extraction and Metadata

```python
"""
Extract text and manage PDF metadata.
"""
from pypdf import PdfReader, PdfWriter
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

def extract_text(
    input_path: str,
    pages: Optional[List[int]] = None,
    preserve_layout: bool = False
) -> str:
    """Extract text from PDF.

    Args:
        input_path: Source PDF file
        pages: List of page numbers to extract (0-indexed), None for all
        preserve_layout: Try to preserve text layout

    Returns:
        Extracted text as string
    """
    reader = PdfReader(input_path)
    text_parts = []

    target_pages = pages if pages else range(len(reader.pages))

    for page_num in target_pages:
        if 0 <= page_num < len(reader.pages):
            page = reader.pages[page_num]

            if preserve_layout:
                page_text = page.extract_text(extraction_mode="layout")
            else:
                page_text = page.extract_text()

            if page_text:
                text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")

    return "\n\n".join(text_parts)


def extract_text_to_file(
    input_path: str,
    output_path: str,
    pages: Optional[List[int]] = None
) -> int:
    """Extract text from PDF and save to file."""
    text = extract_text(input_path, pages)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    word_count = len(text.split())
    print(f"Extracted {word_count} words to: {output_path}")
    return word_count


def get_pdf_info(input_path: str) -> Dict:
    """Get PDF document information and metadata."""
    reader = PdfReader(input_path)

    info = {
        'file_path': input_path,
        'num_pages': len(reader.pages),
        'is_encrypted': reader.is_encrypted,
        'metadata': {}
    }

    # Get metadata
    if reader.metadata:
        metadata = reader.metadata
        info['metadata'] = {
            'title': metadata.get('/Title', ''),
            'author': metadata.get('/Author', ''),
            'subject': metadata.get('/Subject', ''),
            'creator': metadata.get('/Creator', ''),
            'producer': metadata.get('/Producer', ''),
            'creation_date': str(metadata.get('/CreationDate', '')),
            'modification_date': str(metadata.get('/ModDate', ''))
        }

    # Get page dimensions of first page
    if reader.pages:
        first_page = reader.pages[0]
        info['page_width'] = float(first_page.mediabox.width)
        info['page_height'] = float(first_page.mediabox.height)
        info['page_size_inches'] = (
            info['page_width'] / 72,
            info['page_height'] / 72
        )

    return info


def set_pdf_metadata(
    input_path: str,
    output_path: str,
    metadata: Dict[str, str]
) -> None:
    """Set PDF metadata.

    Args:
        input_path: Source PDF file
        output_path: Destination file
        metadata: Dictionary with keys: title, author, subject, keywords, creator
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Copy pages
    for page in reader.pages:
        writer.add_page(page)

    # Set metadata
    writer.add_metadata({
        '/Title': metadata.get('title', ''),
        '/Author': metadata.get('author', ''),
        '/Subject': metadata.get('subject', ''),
        '/Keywords': metadata.get('keywords', ''),
        '/Creator': metadata.get('creator', 'pypdf'),
        '/Producer': 'pypdf',
        '/ModDate': datetime.now().strftime("D:%Y%m%d%H%M%S")
    })

    writer.write(output_path)
    print(f"Metadata updated: {output_path}")


def search_pdf(
    input_path: str,
    search_term: str,
    case_sensitive: bool = False
) -> List[Dict]:
    """Search for text in PDF and return page numbers and context."""
    reader = PdfReader(input_path)
    results = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue

        search_text = text if case_sensitive else text.lower()
        term = search_term if case_sensitive else search_term.lower()

        if term in search_text:
            # Find context around match
            idx = search_text.find(term)
            start = max(0, idx - 50)
            end = min(len(text), idx + len(term) + 50)
            context = text[start:end].replace('\n', ' ')

            results.append({
                'page': i + 1,
                'context': f"...{context}..."
            })

    return results


# Example usage
# text = extract_text('document.pdf')
# info = get_pdf_info('document.pdf')
# set_pdf_metadata('document.pdf', 'with_metadata.pdf', {
#     'title': 'My Document',
#     'author': 'John Doe',
#     'subject': 'Report'
# })
# results = search_pdf('document.pdf', 'important')
```

### 6. Encryption and Form Filling

```python
"""
PDF encryption, decryption, and form handling.
"""
from pypdf import PdfReader, PdfWriter
from pathlib import Path
from typing import Dict, Optional, List

def encrypt_pdf(
    input_path: str,
    output_path: str,
    user_password: str,
    owner_password: Optional[str] = None,
    permissions: Optional[Dict[str, bool]] = None
) -> None:
    """Encrypt PDF with password protection.

    Args:
        input_path: Source PDF file
        output_path: Destination file
        user_password: Password to open the document
        owner_password: Password for full access (defaults to user_password)
        permissions: Dict of permission flags (print, modify, copy, etc.)
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Copy metadata if exists
    if reader.metadata:
        writer.add_metadata(reader.metadata)

    # Default permissions (restrictive)
    default_permissions = {
        'print': True,
        'modify': False,
        'copy': False,
        'annotations': True,
        'forms': True,
        'extract': False,
        'assemble': False,
        'print_high_quality': True
    }

    if permissions:
        default_permissions.update(permissions)

    # Encrypt
    owner_pwd = owner_password or user_password
    writer.encrypt(
        user_password=user_password,
        owner_password=owner_pwd,
        permissions_flag=-1  # All permissions by default
    )

    writer.write(output_path)
    print(f"Encrypted PDF saved to: {output_path}")


def decrypt_pdf(
    input_path: str,
    output_path: str,
    password: str
) -> bool:
    """Decrypt a password-protected PDF.

    Args:
        input_path: Encrypted PDF file
        output_path: Destination file (unencrypted)
        password: Password to decrypt

    Returns:
        True if successful, False otherwise
    """
    try:
        reader = PdfReader(input_path)

        if reader.is_encrypted:
            if not reader.decrypt(password):
                print("Incorrect password")
                return False

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        if reader.metadata:
            writer.add_metadata(reader.metadata)

        writer.write(output_path)
        print(f"Decrypted PDF saved to: {output_path}")
        return True

    except Exception as e:
        print(f"Decryption failed: {e}")
        return False


def get_form_fields(input_path: str) -> Dict[str, Dict]:
    """Get all form fields from a PDF."""
    reader = PdfReader(input_path)
    fields = {}

    if reader.get_fields():
        for name, field in reader.get_fields().items():
            field_type = field.get('/FT', '')
            value = field.get('/V', '')

            fields[name] = {
                'type': str(field_type),
                'value': str(value) if value else '',
                'field': field
            }

    return fields


def fill_pdf_form(
    input_path: str,
    output_path: str,
    field_values: Dict[str, str],
    flatten: bool = False
) -> None:
    """Fill PDF form fields with values.

    Args:
        input_path: Source PDF with form fields
        output_path: Destination file
        field_values: Dictionary of field names and values
        flatten: If True, make form fields uneditable
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Add pages
    for page in reader.pages:
        writer.add_page(page)

    # Update form fields
    writer.update_page_form_field_values(
        writer.pages[0] if writer.pages else None,
        field_values
    )

    if flatten:
        # Note: Full flatten support may require additional processing
        for page in writer.pages:
            if '/Annots' in page:
                del page['/Annots']

    writer.write(output_path)
    print(f"Form filled and saved to: {output_path}")


def list_form_fields_report(input_path: str) -> str:
    """Generate a report of all form fields in a PDF."""
    fields = get_form_fields(input_path)

    if not fields:
        return "No form fields found in this PDF."

    report = ["PDF Form Fields Report", "=" * 40, ""]

    for name, info in fields.items():
        report.append(f"Field: {name}")
        report.append(f"  Type: {info['type']}")
        report.append(f"  Current Value: {info['value'] or '(empty)'}")
        report.append("")

    report.append(f"Total fields: {len(fields)}")

    return "\n".join(report)


# Example usage
# encrypt_pdf('document.pdf', 'encrypted.pdf', 'mypassword')
# decrypt_pdf('encrypted.pdf', 'decrypted.pdf', 'mypassword')
#
# fields = get_form_fields('form.pdf')
# fill_pdf_form('form.pdf', 'filled_form.pdf', {
#     'name': 'John Doe',
#     'date': '2026-01-17',
#     'signature': 'John Doe'
# })
```

## Integration Examples

### Batch PDF Processing Pipeline

```python
"""
Batch process PDFs with configurable operations.
"""
from pypdf import PdfReader, PdfWriter, PdfMerger
from pathlib import Path
from typing import List, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Batch PDF processing with configurable operations."""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_batch(
        self,
        pdf_files: List[str],
        operations: List[Dict[str, Any]],
        parallel: bool = False
    ) -> List[Dict]:
        """Process multiple PDFs with specified operations.

        Args:
            pdf_files: List of PDF file paths
            operations: List of operation configs
            parallel: Run in parallel if True
        """
        results = []

        if parallel:
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {
                    executor.submit(self._process_single, f, operations): f
                    for f in pdf_files
                }
                for future in as_completed(futures):
                    results.append(future.result())
        else:
            for pdf_file in pdf_files:
                results.append(self._process_single(pdf_file, operations))

        return results

    def _process_single(
        self,
        pdf_path: str,
        operations: List[Dict[str, Any]]
    ) -> Dict:
        """Process single PDF with operations."""
        result = {'file': pdf_path, 'success': True, 'operations': []}

        try:
            current_path = pdf_path

            for op in operations:
                op_name = op['name']
                op_params = op.get('params', {})

                output_path = str(
                    self.output_dir / f"{Path(current_path).stem}_{op_name}.pdf"
                )

                if op_name == 'rotate':
                    self._rotate(current_path, output_path, **op_params)
                elif op_name == 'watermark':
                    self._watermark(current_path, output_path, **op_params)
                elif op_name == 'extract_pages':
                    self._extract_pages(current_path, output_path, **op_params)
                elif op_name == 'encrypt':
                    self._encrypt(current_path, output_path, **op_params)

                result['operations'].append({
                    'name': op_name,
                    'output': output_path
                })
                current_path = output_path

            result['final_output'] = current_path

        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            logger.exception(f"Failed to process {pdf_path}")

        return result

    def _rotate(self, input_path, output_path, rotation=90, pages=None):
        reader = PdfReader(input_path)
        writer = PdfWriter()
        for i, page in enumerate(reader.pages):
            if pages is None or i in pages:
                page.rotate(rotation)
            writer.add_page(page)
        writer.write(output_path)

    def _watermark(self, input_path, output_path, watermark_path):
        reader = PdfReader(input_path)
        watermark = PdfReader(watermark_path).pages[0]
        writer = PdfWriter()
        for page in reader.pages:
            page.merge_page(watermark)
            writer.add_page(page)
        writer.write(output_path)

    def _extract_pages(self, input_path, output_path, pages):
        reader = PdfReader(input_path)
        writer = PdfWriter()
        for p in pages:
            if 0 <= p < len(reader.pages):
                writer.add_page(reader.pages[p])
        writer.write(output_path)

    def _encrypt(self, input_path, output_path, password):
        reader = PdfReader(input_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
        writer.write(output_path)


# Example usage
# processor = PDFProcessor('processed_output/')
# results = processor.process_batch(
#     ['doc1.pdf', 'doc2.pdf', 'doc3.pdf'],
#     [
#         {'name': 'rotate', 'params': {'rotation': 90}},
#         {'name': 'watermark', 'params': {'watermark_path': 'watermark.pdf'}},
#         {'name': 'encrypt', 'params': {'password': 'secure123'}}
#     ],
#     parallel=True
# )
```

## Best Practices

### 1. Memory Management

```python
"""Best practices for handling large PDFs."""

# DO: Process pages one at a time for large files
def process_large_pdf(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        # Process page
        writer.add_page(page)
        # Writer streams to file, not memory

    writer.write(output_path)

# DO: Use context managers when available
with open('document.pdf', 'rb') as f:
    reader = PdfReader(f)
    # Process...
```

### 2. Error Handling

```python
"""Robust error handling for PDF operations."""
from pypdf.errors import PdfReadError, PdfReadWarning

def safe_read_pdf(pdf_path):
    """Safely read PDF with error handling."""
    try:
        reader = PdfReader(pdf_path)
        return reader, None
    except PdfReadError as e:
        return None, f"Invalid PDF: {e}"
    except FileNotFoundError:
        return None, f"File not found: {pdf_path}"
    except PermissionError:
        return None, f"Permission denied: {pdf_path}"
    except Exception as e:
        return None, f"Unexpected error: {e}"
```

### 3. Validation

```python
"""Validate PDF files before processing."""

def validate_pdf(pdf_path):
    """Validate PDF file."""
    path = Path(pdf_path)

    if not path.exists():
        return False, "File does not exist"

    if path.suffix.lower() != '.pdf':
        return False, "Not a PDF file"

    try:
        reader = PdfReader(pdf_path)
        _ = len(reader.pages)  # Try to access pages
        return True, "Valid PDF"
    except Exception as e:
        return False, f"Invalid PDF: {e}"
```

## Troubleshooting

### Common Issues

#### 1. Encrypted PDF Error

```python
# Problem: Cannot read encrypted PDF
# Solution: Decrypt first

reader = PdfReader("encrypted.pdf")
if reader.is_encrypted:
    reader.decrypt("password")  # Provide password
```

#### 2. Text Extraction Returns Empty

```python
# Problem: extract_text() returns empty string
# Solution: PDF may be image-based (scanned)

# For scanned PDFs, use OCR:
# pip install pdf2image pytesseract
# Then use pytesseract to OCR the images
```

#### 3. Memory Error with Large PDFs

```python
# Problem: Memory error with large files
# Solution: Process incrementally

def split_large_pdf(input_path, output_dir, max_pages=100):
    reader = PdfReader(input_path)
    total = len(reader.pages)

    for start in range(0, total, max_pages):
        writer = PdfWriter()
        end = min(start + max_pages, total)

        for i in range(start, end):
            writer.add_page(reader.pages[i])

        writer.write(f"{output_dir}/part_{start//max_pages + 1}.pdf")
```

## Version History

### 1.0.0 (2026-01-17)
- Initial skill creation
- Core capabilities documentation
- 6 complete code examples
- Batch processing patterns
- Encryption and form handling

## Resources

- **Official Documentation**: https://pypdf.readthedocs.io/
- **GitHub Repository**: https://github.com/py-pdf/pypdf
- **PyPI Package**: https://pypi.org/project/pypdf/
- **Migration from PyPDF2**: https://pypdf.readthedocs.io/en/latest/migration.html

## Related Skills

- **reportlab** - PDF creation from scratch
- **python-docx** - Word document handling
- **pillow** - Image processing for PDF images
- **pdf2image** - Convert PDF pages to images

---

*This skill provides comprehensive patterns for PDF manipulation refined from production document processing systems.*
