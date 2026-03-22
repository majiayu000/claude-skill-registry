---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: layout-analyzer
description: ">"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: parsing
tags:
  - layout
  - analysis
  - structure
  - surya
department: All

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - analyze_document_structure

# Skill Capabilities
capabilities:
  - layout_detection
  - structure_analysis

# Language Support
languages:
  - en
  - zh
---

# Layout Analyzer Skill

## Overview

This skill enables document layout analysis using **surya** - an advanced document understanding system. Detect text blocks, tables, figures, headings, and determine reading order in complex documents.

## How to Use

1. Provide the document image or PDF
2. Specify what layout elements to detect
3. I'll analyze the structure and return detected regions

**Example prompts:**
- "Analyze the layout of this document page"
- "Detect all tables and text blocks in this image"
- "Determine the reading order for this PDF page"
- "Find headings and paragraphs in this document"

## Domain Knowledge

### surya Fundamentals

```python
from surya.detection import DetectionPredictor
from surya.layout import LayoutPredictor
from surya.reading_order import ReadingOrderPredictor
from PIL import Image

# Load image
image = Image.open("document.png")

# Detect layout elements
layout_predictor = LayoutPredictor()
layout_result = layout_predictor([image])
```

### Layout Element Types

| Element | Description |
|---------|-------------|
| Text | Regular paragraph text |
| Title | Document/section titles |
| Section-header | Section headings |
| List-item | Bulleted/numbered items |
| Table | Tabular data |
| Figure | Images/diagrams |
| Caption | Figure/table captions |
| Footnote | Footnotes |
| Formula | Mathematical equations |
| Page-header | Headers |
| Page-footer | Footers |

### Text Detection

```python
from surya.detection import DetectionPredictor
from PIL import Image

# Initialize detector
detector = DetectionPredictor()

# Load image
image = Image.open("document.png")

# Detect text regions
results = detector([image])

# Access results
for page_result in results:
    for bbox in page_result.bboxes:
        print(f"Text region: {bbox.bbox}")
        print(f"Confidence: {bbox.confidence}")
```

### Layout Analysis

```python
from surya.layout import LayoutPredictor
from PIL import Image

# Initialize layout predictor
layout_predictor = LayoutPredictor()

# Analyze layout
image = Image.open("document.png")
layout_results = layout_predictor([image])

# Process results
for page_result in layout_results:
    for element in page_result.bboxes:
        print(f"Type: {element.label}")
        print(f"Bbox: {element.bbox}")
        print(f"Confidence: {element.confidence}")
```

### Reading Order Detection

```python
from surya.reading_order import ReadingOrderPredictor
from surya.layout import LayoutPredictor
from PIL import Image

# Get layout first
layout_predictor = LayoutPredictor()
image = Image.open("document.png")
layout_results = layout_predictor([image])

# Determine reading order
reading_order_predictor = ReadingOrderPredictor()
order_results = reading_order_predictor([image], layout_results)

# Access ordered elements
for page_result in order_results:
    for i, element in enumerate(page_result.ordered_bboxes):
        print(f"{i+1}. {element.label}: {element.bbox}")
```

### OCR with Layout

```python
from surya.ocr import OCRPredictor
from surya.layout import LayoutPredictor
from PIL import Image

# Initialize predictors
ocr_predictor = OCRPredictor()
layout_predictor = LayoutPredictor()

# Load image
image = Image.open("document.png")

# Get layout
layout_results = layout_predictor([image])

# Run OCR
ocr_results = ocr_predictor([image])

# Combine results
for layout, ocr in zip(layout_results, ocr_results):
    for layout_elem in layout.bboxes:
        print(f"Element: {layout_elem.label}")
        
        # Find OCR text within this layout element
        for text_line in ocr.text_lines:
            if boxes_overlap(layout_elem.bbox, text_line.bbox):
                print(f"  Text: {text_line.text}")
```

### Processing PDFs

```python
from surya.layout import LayoutPredictor
from pdf2image import convert_from_path

def analyze_pdf_layout(pdf_path):
    """Analyze layout of all pages in PDF."""
    
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Initialize predictor
    layout_predictor = LayoutPredictor()
    
    # Analyze all pages
    results = layout_predictor(images)
    
    document_structure = []
    
    for page_num, page_result in enumerate(results):
        page_elements = []
        
        for element in page_result.bboxes:
            page_elements.append({
                'type': element.label,
                'bbox': element.bbox,
                'confidence': element.confidence
            })
        
        document_structure.append({
            'page': page_num + 1,
            'elements': page_elements
        })
    
    return document_structure

structure = analyze_pdf_layout("document.pdf")
```

### Visualization

```python
from surya.layout import LayoutPredictor
from PIL import Image, ImageDraw, ImageFont

def visualize_layout(image_path, output_path):
    """Visualize detected layout elements."""
    
    image = Image.open(image_path)
    layout_predictor = LayoutPredictor()
    results = layout_predictor([image])
    
    # Create drawing context
    draw = ImageDraw.Draw(image)
    
    # Color mapping for element types
    colors = {
        'Text': 'blue',
        'Title': 'red',
        'Table': 'green',
        'Figure': 'purple',
        'Section-header': 'orange',
        'List-item': 'cyan',
    }
    
    for element in results[0].bboxes:
        bbox = element.bbox
        color = colors.get(element.label, 'gray')
        
        # Draw rectangle
        draw.rectangle(bbox, outline=color, width=2)
        
        # Add label
        draw.text((bbox[0], bbox[1] - 15), 
                  f"{element.label} ({element.confidence:.2f})",
                  fill=color)
    
    image.save(output_path)
    return output_path
```

## Best Practices

1. **Use High-Quality Images**: 150+ DPI for best results
2. **Preprocess if Needed**: Deskew rotated documents
3. **Validate Results**: Check confidence scores
4. **Handle Multi-page**: Process pages individually
5. **Combine with OCR**: Get text within detected regions

## Common Patterns

### Document Structure Extraction
```python
def extract_document_structure(image_path):
    """Extract hierarchical document structure."""
    
    from surya.layout import LayoutPredictor
    from surya.reading_order import ReadingOrderPredictor
    
    image = Image.open(image_path)
    
    # Get layout
    layout_predictor = LayoutPredictor()
    layout_results = layout_predictor([image])
    
    # Get reading order
    order_predictor = ReadingOrderPredictor()
    order_results = order_predictor([image], layout_results)
    
    structure = {
        'title': None,
        'sections': [],
        'tables': [],
        'figures': []
    }
    
    current_section = None
    
    for element in order_results[0].ordered_bboxes:
        if element.label == 'Title':
            structure['title'] = element
        elif element.label == 'Section-header':
            current_section = {'header': element, 'content': []}
            structure['sections'].append(current_section)
        elif element.label == 'Table':
            structure['tables'].append(element)
        elif element.label == 'Figure':
            structure['figures'].append(element)
        elif current_section and element.label in ['Text', 'List-item']:
            current_section['content'].append(element)
    
    return structure
```

### Table Region Extraction
```python
def extract_table_regions(image_path):
    """Extract table regions from document."""
    
    from surya.layout import LayoutPredictor
    
    image = Image.open(image_path)
    layout_predictor = LayoutPredictor()
    results = layout_predictor([image])
    
    tables = []
    
    for element in results[0].bboxes:
        if element.label == 'Table':
            bbox = element.bbox
            
            # Crop table region
            table_image = image.crop(bbox)
            
            tables.append({
                'bbox': bbox,
                'image': table_image,
                'confidence': element.confidence
            })
    
    return tables
```

## Examples

### Example 1: Academic Paper Analysis
```python
from surya.layout import LayoutPredictor
from surya.reading_order import ReadingOrderPredictor
from pdf2image import convert_from_path

def analyze_academic_paper(pdf_path):
    """Analyze structure of academic paper."""
    
    images = convert_from_path(pdf_path)
    
    layout_predictor = LayoutPredictor()
    order_predictor = ReadingOrderPredictor()
    
    paper_structure = {
        'pages': [],
        'element_counts': {
            'Title': 0,
            'Section-header': 0,
            'Text': 0,
            'Table': 0,
            'Figure': 0,
            'Formula': 0,
            'Footnote': 0
        }
    }
    
    layout_results = layout_predictor(images)
    order_results = order_predictor(images, layout_results)
    
    for page_num, (layout, order) in enumerate(zip(layout_results, order_results)):
        page_structure = {
            'page': page_num + 1,
            'elements': []
        }
        
        for element in order.ordered_bboxes:
            page_structure['elements'].append({
                'type': element.label,
                'bbox': element.bbox,
                'order': element.position
            })
            
            # Count element types
            if element.label in paper_structure['element_counts']:
                paper_structure['element_counts'][element.label] += 1
        
        paper_structure['pages'].append(page_structure)
    
    return paper_structure

paper = analyze_academic_paper('research_paper.pdf')
print(f"Total tables: {paper['element_counts']['Table']}")
print(f"Total figures: {paper['element_counts']['Figure']}")
```

### Example 2: Form Field Detection
```python
from surya.layout import LayoutPredictor
from PIL import Image

def detect_form_fields(image_path):
    """Detect form fields and labels."""
    
    image = Image.open(image_path)
    
    layout_predictor = LayoutPredictor()
    results = layout_predictor([image])
    
    form_fields = []
    
    for element in results[0].bboxes:
        # Look for text elements that might be labels
        if element.label == 'Text':
            # Check if there's a box/line nearby (potential input field)
            form_fields.append({
                'type': 'potential_label',
                'bbox': element.bbox,
                'confidence': element.confidence
            })
    
    return form_fields

fields = detect_form_fields('form.png')
print(f"Found {len(fields)} potential form elements")
```

### Example 3: Multi-column Article
```python
from surya.layout import LayoutPredictor
from surya.reading_order import ReadingOrderPredictor
from PIL import Image

def process_multicolumn_article(image_path):
    """Process multi-column article layout."""
    
    image = Image.open(image_path)
    
    layout_predictor = LayoutPredictor()
    order_predictor = ReadingOrderPredictor()
    
    layout_results = layout_predictor([image])
    order_results = order_predictor([image], layout_results)
    
    # Group elements by column
    image_width = image.width
    column_threshold = image_width / 2
    
    columns = {
        'left': [],
        'right': [],
        'full_width': []
    }
    
    for element in order_results[0].ordered_bboxes:
        bbox = element.bbox
        element_center = (bbox[0] + bbox[2]) / 2
        element_width = bbox[2] - bbox[0]
        
        # Determine column
        if element_width > column_threshold * 1.5:
            columns['full_width'].append(element)
        elif element_center < column_threshold:
            columns['left'].append(element)
        else:
            columns['right'].append(element)
    
    return {
        'layout': 'multi-column',
        'columns': columns,
        'reading_order': order_results[0].ordered_bboxes
    }

article = process_multicolumn_article('newspaper_page.png')
print(f"Left column: {len(article['columns']['left'])} elements")
print(f"Right column: {len(article['columns']['right'])} elements")
```

## Limitations

- Handwritten layouts may be inaccurate
- Very small text regions may be missed
- Complex nested layouts challenging
- GPU recommended for batch processing
- Multi-language support varies

## Installation

```bash
pip install surya-ocr

# For PDF processing
pip install pdf2image
```

## Resources

- [surya GitHub](https://github.com/VikParuchuri/surya)
- [Model Documentation](https://github.com/VikParuchuri/surya#models)
- [Examples](https://github.com/VikParuchuri/surya/tree/master/examples)
