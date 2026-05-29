---
name: epub-creator
description: Create production-quality EPUB 3 ebooks from markdown and images with automated QA, formatting fixes, and validation. Use when creating ebooks, converting markdown to EPUB, or compiling chapters into a publishable book. Handles markdown quirks, generates TOC, adds covers, and validates output automatically.
allowed-tools: Bash, Read, Write
---

# EPUB Creator (Production Grade)

Create validated, publication-ready EPUB 3 ebooks from markdown files and images.

## Prerequisites

**Python Version**: Requires Python 3.8 or higher

```bash
# Install all required packages
uv pip install ebooklib markdown Pillow beautifulsoup4 lxml PyYAML

# Or with pip
pip install ebooklib markdown Pillow beautifulsoup4 lxml PyYAML
```

**Optional** (for EPUB validation):
```bash
# macOS
brew install epubcheck

# Linux (Debian/Ubuntu)
apt install epubcheck

# Via Python wrapper
uv pip install epubcheck
```

## Production Workflow

Follow this 5-step workflow to create high-quality EPUBs:

```
1. PRE-PROCESS → 2. CONVERT → 3. ASSEMBLE → 4. VALIDATE → 5. DELIVER
```

---

## Step 1: Pre-Processing (Input Validation & Fixes)

Before conversion, validate and fix all inputs.

### 1.1 Gather Inputs

```python
from pathlib import Path
import re

def gather_inputs(source_dir: str):
    """Collect and validate all input files."""
    source = Path(source_dir)

    inputs = {
        'markdown_files': sorted(source.glob('**/*.md')),
        'images': list(source.glob('**/*.{jpg,jpeg,png,gif,svg}')),
        'cover': None,
        'metadata': {}
    }

    # Find cover image
    for pattern in ['cover.*', 'Cover.*', '*cover*.*']:
        covers = list(source.glob(pattern))
        if covers:
            inputs['cover'] = covers[0]
            break

    # Look for metadata file
    meta_file = source / 'metadata.yaml'
    if meta_file.exists():
        import yaml
        with open(meta_file) as f:
            inputs['metadata'] = yaml.safe_load(f)

    return inputs
```

### 1.2 Fix Markdown Quirks

```python
def fix_markdown_quirks(content: str) -> str:
    """Fix common markdown issues."""

    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    # Fix inconsistent heading levels (ensure starts with #)
    lines = content.split('\n')
    fixed_lines = []
    found_first_heading = False

    for line in lines:
        # Detect heading
        if line.startswith('#'):
            if not found_first_heading:
                # Ensure first heading is h1
                heading_match = re.match(r'^(#+)\s*(.+)$', line)
                if heading_match:
                    level = len(heading_match.group(1))
                    if level > 1:
                        line = f'# {heading_match.group(2)}'
                found_first_heading = True
        fixed_lines.append(line)

    content = '\n'.join(fixed_lines)

    # Fix unclosed emphasis
    # Count asterisks and underscores, close if odd
    for char in ['*', '_']:
        count = content.count(char)
        if count % 2 == 1:
            content += char

    # Ensure blank line before headings
    content = re.sub(r'([^\n])\n(#{1,6}\s)', r'\1\n\n\2', content)

    # Fix broken links - remove if target missing
    content = re.sub(r'\[([^\]]+)\]\(\s*\)', r'\1', content)

    # Normalize whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip() + '\n'
```

### 1.3 Validate Images

```python
from PIL import Image
import os

def validate_and_fix_images(image_paths: list, max_size_mb: float = 2.0):
    """Validate images and optimize if needed."""
    validated = []
    issues = []

    for img_path in image_paths:
        path = Path(img_path)

        try:
            with Image.open(path) as img:
                # Check format
                if img.format not in ['JPEG', 'PNG', 'GIF']:
                    issues.append(f"Converting {path.name} to PNG")
                    new_path = path.with_suffix('.png')
                    img.save(new_path, 'PNG')
                    path = new_path

                # Check size
                size_mb = os.path.getsize(path) / (1024 * 1024)
                if size_mb > max_size_mb:
                    issues.append(f"Optimizing {path.name} ({size_mb:.1f}MB)")
                    # Resize large images
                    if max(img.size) > 2000:
                        ratio = 2000 / max(img.size)
                        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                        img = img.resize(new_size, Image.Resampling.LANCZOS)
                    img.save(path, optimize=True, quality=85)

                validated.append({
                    'path': path,
                    'size': img.size,
                    'format': img.format
                })

        except Exception as e:
            issues.append(f"ERROR: Cannot read {path.name}: {e}")

    return validated, issues
```

### 1.4 Validate Cover Image

```python
def validate_cover(cover_path: str) -> tuple:
    """Ensure cover meets EPUB requirements."""
    RECOMMENDED_SIZE = (1600, 2400)
    MIN_SIZE = (1400, 2100)

    issues = []

    with Image.open(cover_path) as img:
        width, height = img.size

        # Check minimum size
        if width < MIN_SIZE[0] or height < MIN_SIZE[1]:
            issues.append(f"Cover too small ({width}x{height}), minimum {MIN_SIZE[0]}x{MIN_SIZE[1]}")

        # Check aspect ratio (should be ~1:1.5)
        ratio = height / width
        if ratio < 1.3 or ratio > 1.7:
            issues.append(f"Cover aspect ratio {ratio:.2f} not ideal (should be ~1.5)")

        # Convert to RGB if needed (remove alpha)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            cover_path = Path(cover_path).with_suffix('.jpg')
            img.save(cover_path, 'JPEG', quality=95)
            issues.append(f"Converted cover to JPEG")

    return cover_path, issues
```

### 1.5 Pre-Validate All Sources

Run comprehensive validation before processing:

```python
def validate_sources(source_dir: str) -> dict:
    """Pre-validate all source files before processing."""
    report = {
        'valid': True,
        'markdown_files': [],
        'images': [],
        'errors': [],
        'warnings': []
    }

    source = Path(source_dir)

    # Check directory exists
    if not source.exists():
        report['valid'] = False
        report['errors'].append(f"Source directory not found: {source_dir}")
        return report

    # Find markdown files
    md_files = sorted(source.glob('*.md'))
    if not md_files:
        md_files = sorted(source.glob('**/*.md'))

    if not md_files:
        report['valid'] = False
        report['errors'].append("No markdown files found")
        return report

    print(f"📋 Pre-validating {len(md_files)} markdown files...")

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            report['markdown_files'].append({
                'path': str(md_file),
                'size': md_file.stat().st_size,
                'word_count': len(content.split())
            })

            # Check for broken image references
            img_refs = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
            for alt, img_path in img_refs:
                full_path = (md_file.parent / img_path).resolve()
                if not full_path.exists():
                    report['warnings'].append(f"Missing image: {img_path} in {md_file.name}")
                else:
                    report['images'].append(str(full_path))

        except Exception as e:
            report['errors'].append(f"Cannot read {md_file.name}: {e}")

    # Check for cover
    cover_patterns = ['cover.jpg', 'cover.png', 'Cover.jpg', 'Cover.png']
    cover_found = any((source / p).exists() for p in cover_patterns)
    if not cover_found:
        report['warnings'].append("No cover image found (optional but recommended)")

    report['valid'] = len(report['errors']) == 0

    # Print summary
    print(f"   ✓ {len(report['markdown_files'])} markdown files")
    print(f"   ✓ {len(report['images'])} images referenced")
    if report['warnings']:
        for w in report['warnings']:
            print(f"   ⚠ {w}")
    if report['errors']:
        for e in report['errors']:
            print(f"   ✗ {e}")

    return report
```

---

## Step 2: Content Conversion

### 2.1 Extract Metadata from Frontmatter

```python
import yaml
import re

def extract_frontmatter(content: str) -> tuple:
    """Extract YAML frontmatter and content."""
    frontmatter = {}

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            content = content[match.end():]
        except yaml.YAMLError:
            pass

    return frontmatter, content
```

### 2.2 Smart Title Extraction

```python
def extract_title(content: str, filename: str, frontmatter: dict) -> str:
    """Extract chapter title with fallback chain."""

    # 1. Check frontmatter
    if frontmatter.get('title'):
        return frontmatter['title']

    # 2. Find first heading
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # 3. Fallback to filename
    name = Path(filename).stem
    # Remove leading numbers and dashes
    name = re.sub(r'^[\d\-_]+', '', name)
    return name.replace('-', ' ').replace('_', ' ').title()
```

### 2.3 Convert Markdown to XHTML

```python
import markdown
from bs4 import BeautifulSoup

def markdown_to_xhtml(content: str, title: str) -> str:
    """Convert markdown to valid EPUB XHTML."""

    # Use robust markdown extensions
    html = markdown.markdown(
        content,
        extensions=[
            'tables',
            'fenced_code',
            'toc',
            'smarty',       # Smart quotes and dashes
            'sane_lists',   # Better list handling
            'attr_list',    # HTML attributes
            'md_in_html',   # Markdown inside HTML blocks
        ],
        output_format='xhtml'
    )

    # Parse and clean with BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')

    # Ensure all images have alt text
    for img in soup.find_all('img'):
        if not img.get('alt'):
            img['alt'] = 'Image'

    # Add classes to first paragraphs after headings (no indent)
    for heading in soup.find_all(['h1', 'h2', 'h3']):
        next_p = heading.find_next_sibling('p')
        if next_p:
            next_p['class'] = next_p.get('class', []) + ['first']

    # Wrap in proper XHTML structure
    xhtml = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="../styles/main.css"/>
</head>
<body>
{soup.decode_contents()}
</body>
</html>'''

    return xhtml
```

### 2.4 Extract Nested ToC Structure

Generate hierarchical table of contents with section anchors:

```python
from slugify import slugify  # pip install python-slugify

def extract_toc_structure(content: str, chapter_file: str, toc_depth: int = 2) -> list:
    """Extract hierarchical TOC entries from chapter content.

    Args:
        content: HTML content of the chapter
        chapter_file: Filename for href links
        toc_depth: 1=H1 only, 2=H1+H2, 3=H1+H2+H3

    Returns:
        List of TOC entries with nested children
    """
    entries = []
    soup = BeautifulSoup(content, 'lxml')

    # Get H1 (chapter title)
    h1 = soup.find('h1')
    if h1:
        chapter_entry = {
            'title': h1.get_text().strip(),
            'href': chapter_file,
            'children': []
        }

        # Get H2 entries if toc_depth >= 2
        if toc_depth >= 2:
            for h2 in soup.find_all('h2'):
                h2_id = slugify(h2.get_text())
                h2['id'] = h2_id  # Add anchor to HTML
                h2_entry = {
                    'title': h2.get_text().strip(),
                    'href': f"{chapter_file}#{h2_id}",
                    'children': []
                }

                # Get H3 entries if toc_depth >= 3
                if toc_depth >= 3:
                    # Find H3s that follow this H2 (until next H2)
                    next_elem = h2.find_next_sibling()
                    while next_elem and next_elem.name != 'h2':
                        if next_elem.name == 'h3':
                            h3_id = slugify(next_elem.get_text())
                            next_elem['id'] = h3_id
                            h2_entry['children'].append({
                                'title': next_elem.get_text().strip(),
                                'href': f"{chapter_file}#{h3_id}"
                            })
                        next_elem = next_elem.find_next_sibling()

                chapter_entry['children'].append(h2_entry)

        entries.append(chapter_entry)

    return entries, str(soup)  # Return modified HTML with IDs


def build_nested_toc(toc_entries: list) -> tuple:
    """Build ebooklib TOC structure from nested entries."""
    toc = []

    for entry in toc_entries:
        if entry.get('children'):
            # Create section with children
            children = []
            for child in entry['children']:
                if child.get('children'):
                    # H2 with H3 children
                    grandchildren = [
                        epub.Link(gc['href'], gc['title'], gc['title'])
                        for gc in child['children']
                    ]
                    children.append((
                        epub.Link(child['href'], child['title'], child['title']),
                        grandchildren
                    ))
                else:
                    children.append(epub.Link(child['href'], child['title'], child['title']))

            toc.append((
                epub.Link(entry['href'], entry['title'], entry['title']),
                children
            ))
        else:
            toc.append(epub.Link(entry['href'], entry['title'], entry['title']))

    return toc
```

---

## Step 3: EPUB Assembly

### 3.1 Professional CSS Stylesheet

```python
EPUB_CSS = '''
/* Professional EPUB Stylesheet */
@charset "UTF-8";

/* Base Typography */
body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1em;
    line-height: 1.6;
    margin: 1em;
    text-align: justify;
    hyphens: auto;
    -webkit-hyphens: auto;
}

/* Headings */
h1 {
    font-size: 1.8em;
    font-weight: bold;
    margin: 2em 0 1em;
    text-align: center;
    page-break-before: always;
    page-break-after: avoid;
}

h2 {
    font-size: 1.4em;
    font-weight: bold;
    margin: 1.5em 0 0.5em;
    page-break-after: avoid;
}

h3 {
    font-size: 1.2em;
    font-weight: bold;
    margin: 1em 0 0.5em;
}

/* Paragraphs */
p {
    margin: 0.5em 0;
    text-indent: 1.5em;
}

p.first,
h1 + p,
h2 + p,
h3 + p,
blockquote + p {
    text-indent: 0;
}

/* Block Elements */
blockquote {
    margin: 1em 2em;
    font-style: italic;
    border-left: 3px solid #ccc;
    padding-left: 1em;
}

/* Code */
code {
    font-family: "Courier New", Courier, monospace;
    font-size: 0.9em;
    background-color: #f5f5f5;
    padding: 0.1em 0.3em;
    border-radius: 3px;
}

pre {
    font-family: "Courier New", Courier, monospace;
    font-size: 0.85em;
    background-color: #f5f5f5;
    padding: 1em;
    margin: 1em 0;
    overflow-x: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
    border-radius: 5px;
}

pre code {
    background: none;
    padding: 0;
}

/* Lists */
ul, ol {
    margin: 0.5em 0 0.5em 2em;
    padding: 0;
}

li {
    margin: 0.3em 0;
}

/* Images */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}

figure {
    margin: 1em 0;
    text-align: center;
}

figcaption {
    font-size: 0.9em;
    font-style: italic;
    color: #666;
    margin-top: 0.5em;
}

/* Tables */
table {
    border-collapse: collapse;
    margin: 1em auto;
    font-size: 0.9em;
}

th, td {
    border: 1px solid #ccc;
    padding: 0.5em;
    text-align: left;
}

th {
    background-color: #f5f5f5;
    font-weight: bold;
}

/* Links */
a {
    color: #0066cc;
    text-decoration: none;
}

/* Horizontal Rule */
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 2em 0;
}
'''
```

### 3.2 Complete EPUB Builder

```python
from ebooklib import epub
from pathlib import Path
import uuid
from datetime import datetime

def create_production_epub(
    source_dir: str,
    output_path: str,
    title: str,
    author: str,
    language: str = 'en',
    cover_path: str = None,
    publisher: str = None,
    description: str = None,
    # Configurable parameters
    max_image_size_mb: float = 2.0,
    max_image_dimension: int = 2000,
    image_quality: int = 85,
    cover_min_width: int = 1400,
    cover_min_height: int = 2100,
    toc_depth: int = 2,  # 1=chapters only, 2=include H2, 3=include H3
    custom_css: str = None,
) -> dict:
    """Create a production-quality EPUB with full QA.

    Args:
        source_dir: Directory containing markdown files
        output_path: Output EPUB file path
        title: Book title
        author: Author name
        language: Language code (default: 'en')
        cover_path: Path to cover image (optional)
        publisher: Publisher name (optional)
        description: Book description (optional)
        max_image_size_mb: Maximum image file size before optimization
        max_image_dimension: Maximum image dimension in pixels
        image_quality: JPEG quality for optimized images (1-100)
        cover_min_width: Minimum cover width in pixels
        cover_min_height: Minimum cover height in pixels
        toc_depth: Table of contents depth (1-3)
        custom_css: Custom CSS to append to stylesheet

    Returns:
        dict: Creation report with status, chapters, fixes, and errors
    """

    print(f"📖 Starting EPUB creation: {title}")
    print(f"   Source: {source_dir}")
    print(f"   Output: {output_path}")

    report = {
        'status': 'success',
        'fixes_applied': [],
        'warnings': [],
        'errors': [],
        'chapters': [],
        'images': []
    }

    # Initialize book
    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language(language)
    book.add_author(author)

    if publisher:
        book.add_metadata('DC', 'publisher', publisher)
    if description:
        book.add_metadata('DC', 'description', description)

    book.add_metadata('DC', 'date', datetime.now().strftime('%Y-%m-%d'))

    # Add CSS
    css = epub.EpubItem(
        uid='main_css',
        file_name='styles/main.css',
        media_type='text/css',
        content=EPUB_CSS
    )
    book.add_item(css)

    # Process cover
    if cover_path and Path(cover_path).exists():
        cover_path, cover_issues = validate_cover(cover_path)
        report['fixes_applied'].extend(cover_issues)

        with open(cover_path, 'rb') as f:
            book.set_cover('images/cover.jpg', f.read())

    # Gather and process markdown files
    source = Path(source_dir)
    md_files = sorted(source.glob('**/*.md'))

    if not md_files:
        report['errors'].append('No markdown files found')
        report['status'] = 'failed'
        return report

    chapters = []
    toc = []
    image_items = {}

    print(f"   📝 Processing {len(md_files)} chapters...")

    for i, md_file in enumerate(md_files, 1):
        print(f"      [{i}/{len(md_files)}] {md_file.name}")

        # Read and fix content
        with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
            raw_content = f.read()

        # Extract frontmatter
        frontmatter, content = extract_frontmatter(raw_content)

        # Fix quirks
        original_content = content
        content = fix_markdown_quirks(content)
        if content != original_content:
            report['fixes_applied'].append(f'Fixed markdown quirks in {md_file.name}')

        # Extract title
        chapter_title = extract_title(content, md_file.name, frontmatter)

        # Find and process images referenced in this chapter
        img_refs = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        for alt, img_path in img_refs:
            img_full_path = (md_file.parent / img_path).resolve()
            if img_full_path.exists() and str(img_full_path) not in image_items:
                with open(img_full_path, 'rb') as f:
                    img_content = f.read()

                img_name = f'images/{img_full_path.name}'
                img_item = epub.EpubImage()
                img_item.file_name = img_name
                img_item.content = img_content
                book.add_item(img_item)
                image_items[str(img_full_path)] = img_name
                report['images'].append(img_full_path.name)

            # Update path in content
            if str(img_full_path) in image_items:
                content = content.replace(f']({img_path})', f'](../{image_items[str(img_full_path)]})')

        # Convert to XHTML
        xhtml = markdown_to_xhtml(content, chapter_title)

        # Create chapter
        chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=f'chapters/chapter_{i:02d}.xhtml',
            lang=language
        )
        chapter.content = xhtml
        chapter.add_item(css)

        book.add_item(chapter)
        chapters.append(chapter)
        toc.append(epub.Link(f'chapters/chapter_{i:02d}.xhtml', chapter_title, f'ch{i}'))

        report['chapters'].append({
            'file': md_file.name,
            'title': chapter_title,
            'word_count': len(content.split())
        })

    # Build TOC and spine
    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapters

    # Write EPUB
    print(f"   📦 Assembling EPUB...")
    epub.write_epub(output_path, book, {})

    print(f"   ✓ Created: {output_path}")
    report['output'] = output_path
    report['total_chapters'] = len(chapters)
    report['total_images'] = len(image_items)

    return report
```

---

## Step 4: Validation & QA

### 4.1 EPUB Validation

```python
import subprocess
import zipfile

def validate_epub(epub_path: str) -> dict:
    """Validate EPUB with epubcheck."""
    result = {
        'valid': False,
        'errors': [],
        'warnings': []
    }

    try:
        # Try Python epubcheck wrapper
        output = subprocess.run(
            ['python', '-m', 'epubcheck', epub_path],
            capture_output=True,
            text=True
        )

        if output.returncode == 0:
            result['valid'] = True
        else:
            # Parse errors from output
            for line in output.stderr.split('\n'):
                if 'ERROR' in line:
                    result['errors'].append(line)
                elif 'WARNING' in line:
                    result['warnings'].append(line)

    except FileNotFoundError:
        # Fallback: basic structure validation
        result['warnings'].append('epubcheck not installed, using basic validation')

        with zipfile.ZipFile(epub_path, 'r') as zf:
            files = zf.namelist()

            # Check required files
            required = ['mimetype', 'META-INF/container.xml']
            for req in required:
                if req not in files:
                    result['errors'].append(f'Missing required file: {req}')

            # Check mimetype content
            mimetype = zf.read('mimetype').decode('utf-8')
            if mimetype != 'application/epub+zip':
                result['errors'].append('Invalid mimetype')

            if not result['errors']:
                result['valid'] = True

    return result
```

### 4.2 Comprehensive Post-Validation

Run thorough checks on the generated EPUB:

```python
import zipfile
import subprocess

def post_validate_epub(epub_path: str) -> dict:
    """Comprehensive post-creation validation."""
    report = {
        'valid': True,
        'checks': [],
        'errors': [],
        'warnings': []
    }

    path = Path(epub_path)

    print(f"\n🔍 Post-validating: {path.name}")

    # 1. File exists and readable
    if not path.exists():
        report['valid'] = False
        report['errors'].append("EPUB file not created")
        return report
    report['checks'].append("✓ File exists")

    # 2. File size check
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > 50:
        report['warnings'].append(f"Large file: {size_mb:.1f}MB (may cause reader issues)")
    elif size_mb < 0.001:
        report['valid'] = False
        report['errors'].append("File too small - likely empty or corrupted")
    report['checks'].append(f"✓ File size: {size_mb:.2f}MB")

    # 3. Valid ZIP structure
    try:
        with zipfile.ZipFile(path, 'r') as zf:
            names = zf.namelist()

            # Check mimetype
            if 'mimetype' not in names:
                report['errors'].append("Missing mimetype file")
                report['valid'] = False
            else:
                mime = zf.read('mimetype').decode('utf-8')
                if mime.strip() != 'application/epub+zip':
                    report['errors'].append(f"Invalid mimetype: {mime}")
                    report['valid'] = False
                else:
                    report['checks'].append("✓ Valid mimetype")

            # Check container.xml
            if 'META-INF/container.xml' not in names:
                report['errors'].append("Missing container.xml")
                report['valid'] = False
            else:
                report['checks'].append("✓ Container.xml present")

            # Check for content
            xhtml_files = [n for n in names if n.endswith('.xhtml')]
            if not xhtml_files:
                report['errors'].append("No XHTML content files")
                report['valid'] = False
            else:
                report['checks'].append(f"✓ {len(xhtml_files)} content files")

            # Check for styles
            css_files = [n for n in names if n.endswith('.css')]
            if css_files:
                report['checks'].append(f"✓ {len(css_files)} stylesheet(s)")

            # Check for images
            img_files = [n for n in names if any(n.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif'])]
            if img_files:
                report['checks'].append(f"✓ {len(img_files)} image(s)")

    except zipfile.BadZipFile:
        report['valid'] = False
        report['errors'].append("Invalid ZIP/EPUB structure")

    # 4. Try epubcheck if available
    try:
        result = subprocess.run(
            ['epubcheck', str(path)],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            report['checks'].append("✓ epubcheck validation passed")
        else:
            # Parse epubcheck output for specific issues
            for line in result.stderr.split('\n'):
                if 'ERROR' in line:
                    report['errors'].append(line.strip())
                elif 'WARNING' in line:
                    report['warnings'].append(line.strip())
    except FileNotFoundError:
        report['checks'].append("○ epubcheck not installed (optional)")
    except subprocess.TimeoutExpired:
        report['warnings'].append("epubcheck timed out - file may be too large")

    # Print summary
    for check in report['checks']:
        print(f"   {check}")
    for warning in report['warnings']:
        print(f"   ⚠ {warning}")
    for error in report['errors']:
        print(f"   ✗ {error}")

    return report
```

### 4.3 Content QA Checklist

```python
def qa_checklist(epub_path: str, report: dict) -> dict:
    """Run QA checklist on generated EPUB."""
    qa = {
        'passed': [],
        'failed': [],
        'warnings': []
    }

    # 1. Check file exists and size
    path = Path(epub_path)
    if path.exists():
        qa['passed'].append(f'EPUB created: {path.name}')
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > 50:
            qa['warnings'].append(f'Large file size: {size_mb:.1f}MB')
    else:
        qa['failed'].append('EPUB file not created')
        return qa

    # 2. Check chapter count
    if report.get('total_chapters', 0) > 0:
        qa['passed'].append(f'Chapters: {report["total_chapters"]}')
    else:
        qa['failed'].append('No chapters in EPUB')

    # 3. Check for fixes applied
    if report.get('fixes_applied'):
        qa['warnings'].append(f'Fixes applied: {len(report["fixes_applied"])}')

    # 4. Validate structure
    validation = validate_epub(epub_path)
    if validation['valid']:
        qa['passed'].append('EPUB validation: PASSED')
    else:
        qa['failed'].append('EPUB validation: FAILED')
        qa['failed'].extend(validation['errors'])

    qa['warnings'].extend(validation.get('warnings', []))

    # 5. Overall status
    qa['status'] = 'PASSED' if not qa['failed'] else 'FAILED'

    return qa
```

---

## Step 5: Complete Production Script

```python
#!/usr/bin/env python3
"""
Production EPUB Creator
Creates validated, publication-ready EPUB files from markdown.
"""

from pathlib import Path
import json
from datetime import datetime

def create_epub_production(
    source_dir: str,
    output_dir: str = None,
    title: str = None,
    author: str = 'Unknown Author',
    **kwargs
) -> str:
    """
    Create a production-quality EPUB with full QA.

    Args:
        source_dir: Directory containing markdown files and images
        output_dir: Output directory (default: source_dir)
        title: Book title (default: derived from directory name)
        author: Author name
        **kwargs: Additional metadata (language, publisher, description)

    Returns:
        Path to created EPUB file
    """
    source = Path(source_dir)
    output_dir = Path(output_dir or source_dir)

    # Default title from directory name
    if not title:
        title = source.name.replace('-', ' ').replace('_', ' ').title()

    # Create output filename
    safe_title = "".join(c if c.isalnum() or c in ' -_' else '' for c in title)
    output_path = output_dir / f'{safe_title.replace(" ", "_")}.epub'

    print(f"Creating EPUB: {title}")
    print(f"Source: {source}")
    print(f"Output: {output_path}")
    print("-" * 50)

    # Find cover
    cover_path = None
    for pattern in ['cover.jpg', 'cover.png', 'Cover.*', '*cover*.*']:
        covers = list(source.glob(pattern))
        if covers:
            cover_path = str(covers[0])
            break

    # Create EPUB
    report = create_production_epub(
        source_dir=str(source),
        output_path=str(output_path),
        title=title,
        author=author,
        cover_path=cover_path,
        **kwargs
    )

    # Run QA
    qa = qa_checklist(str(output_path), report)

    # Print report
    print("\n📚 EPUB Creation Report")
    print("=" * 50)
    print(f"Title: {title}")
    print(f"Author: {author}")
    print(f"Chapters: {report.get('total_chapters', 0)}")
    print(f"Images: {report.get('total_images', 0)}")

    if report.get('fixes_applied'):
        print(f"\n🔧 Fixes Applied ({len(report['fixes_applied'])}):")
        for fix in report['fixes_applied']:
            print(f"  - {fix}")

    print(f"\n✅ QA Status: {qa['status']}")
    for item in qa['passed']:
        print(f"  ✓ {item}")
    for item in qa['failed']:
        print(f"  ✗ {item}")
    for item in qa['warnings']:
        print(f"  ⚠ {item}")

    # Save report
    report_path = output_path.with_suffix('.report.json')
    with open(report_path, 'w') as f:
        json.dump({
            'creation_report': report,
            'qa_report': qa,
            'timestamp': datetime.now().isoformat()
        }, f, indent=2, default=str)

    print(f"\n📄 Report saved: {report_path}")
    print(f"📖 EPUB created: {output_path}")

    return str(output_path)


# Usage
if __name__ == '__main__':
    create_epub_production(
        source_dir='./my-book',
        title='My Amazing Book',
        author='John Doe',
        language='en',
        publisher='Self Published',
        description='A wonderful book about...'
    )
```

---

## Usage Examples

### Basic Usage
```
"Create an EPUB from the markdown files in ./chapters"
```
Claude will:
1. Scan for markdown files
2. Fix any formatting issues
3. Generate TOC from headings
4. Create styled EPUB
5. Validate and report

### With Cover Image
```
"Create an EPUB called 'My Novel' from ./book with cover.jpg as the cover"
```

### Full Metadata
```
"Create an EPUB from ./manuscript:
- Title: The Great Adventure
- Author: Jane Smith
- Language: English
- Publisher: Indie Press"
```

### QA Mode
```
"Create an EPUB from ./draft and show me all the issues found"
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No markdown files found" | Ensure `.md` files exist in source directory |
| "Cover too small" | Use image at least 1400x2100 pixels |
| "Validation failed" | Check report for specific errors |
| "Broken images" | Verify image paths are relative to markdown files |
| "Encoding errors" | Files will be auto-converted to UTF-8 |

---

## Tips for Best Results

1. **Organize chapters** with numbered prefixes: `01-intro.md`, `02-chapter1.md`
2. **Use consistent heading levels**: Start each chapter with `# Title`
3. **Place images** in same directory as markdown or `images/` subfolder
4. **Add YAML frontmatter** for chapter metadata:
   ```yaml
   ---
   title: Chapter One
   ---
   ```
5. **Validate before publishing** with `epubcheck`
