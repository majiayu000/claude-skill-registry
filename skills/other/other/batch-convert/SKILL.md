---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: batch-convert
description: "Batch convert documents between multiple formats using a unified pipeline"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: conversion
tags:
  - batch
  - conversion
  - bulk
  - automation
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
    - batch_convert

# Skill Capabilities
capabilities:
  - bulk_conversion
  - automation

# Language Support
languages:
  - en
  - zh
---

# Batch Convert Skill

## Overview

This skill enables batch conversion of documents between multiple formats using a unified pipeline. Convert hundreds of files at once with consistent settings, automatic format detection, and parallel processing for maximum efficiency.

## How to Use

1. Specify the source folder or files
2. Choose target format(s)
3. Optionally configure conversion options
4. I'll process all files with progress tracking

**Example prompts:**
- "Convert all PDFs in this folder to Word documents"
- "Batch convert these markdown files to PDF and HTML"
- "Process all Office files and convert to Markdown"
- "Convert this folder of images to a single PDF"

## Domain Knowledge

### Supported Format Matrix

| From | To: DOCX | To: PDF | To: MD | To: HTML | To: PPTX |
|------|----------|---------|--------|----------|----------|
| DOCX | - | ✅ | ✅ | ✅ | - |
| PDF | ✅ | - | ✅ | ✅ | - |
| MD | ✅ | ✅ | - | ✅ | ✅ |
| HTML | ✅ | ✅ | ✅ | - | - |
| XLSX | - | ✅ | ✅ | ✅ | - |
| PPTX | - | ✅ | ✅ | ✅ | - |

### Core Pipeline

```python
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import os

class DocumentConverter:
    """Unified document conversion pipeline."""
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.converters = {
            ('md', 'docx'): self._md_to_docx,
            ('md', 'pdf'): self._md_to_pdf,
            ('md', 'html'): self._md_to_html,
            ('md', 'pptx'): self._md_to_pptx,
            ('docx', 'pdf'): self._docx_to_pdf,
            ('docx', 'md'): self._docx_to_md,
            ('pdf', 'docx'): self._pdf_to_docx,
            ('pdf', 'md'): self._pdf_to_md,
            ('xlsx', 'pdf'): self._xlsx_to_pdf,
            ('xlsx', 'md'): self._xlsx_to_md,
            ('pptx', 'pdf'): self._pptx_to_pdf,
            ('pptx', 'md'): self._pptx_to_md,
            ('html', 'md'): self._html_to_md,
            ('html', 'pdf'): self._html_to_pdf,
        }
    
    def convert(self, input_path, output_format, output_dir=None):
        """Convert single file to target format."""
        input_path = Path(input_path)
        input_format = input_path.suffix[1:].lower()
        
        if output_dir:
            output_path = Path(output_dir) / f"{input_path.stem}.{output_format}"
        else:
            output_path = input_path.with_suffix(f".{output_format}")
        
        converter_key = (input_format, output_format)
        if converter_key not in self.converters:
            raise ValueError(f"Conversion not supported: {input_format} -> {output_format}")
        
        converter = self.converters[converter_key]
        return converter(input_path, output_path)
    
    def batch_convert(self, input_dir, output_format, output_dir=None, 
                      file_pattern="*", recursive=False):
        """Batch convert all matching files."""
        input_path = Path(input_dir)
        output_path = Path(output_dir) if output_dir else input_path / "converted"
        output_path.mkdir(exist_ok=True)
        
        # Find files
        if recursive:
            files = list(input_path.rglob(file_pattern))
        else:
            files = list(input_path.glob(file_pattern))
        
        # Filter to supported formats
        supported_ext = ['.md', '.docx', '.pdf', '.xlsx', '.pptx', '.html']
        files = [f for f in files if f.suffix.lower() in supported_ext]
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(self.convert, f, output_format, output_path): f
                for f in files
            }
            
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    results.append({'file': str(file), 'status': 'success', 'output': str(result)})
                except Exception as e:
                    results.append({'file': str(file), 'status': 'error', 'error': str(e)})
        
        return results
```

### Converter Implementations

```python
# Markdown conversions (using Pandoc)
def _md_to_docx(self, input_path, output_path):
    subprocess.run(['pandoc', str(input_path), '-o', str(output_path)], check=True)
    return output_path

def _md_to_pdf(self, input_path, output_path):
    subprocess.run(['pandoc', str(input_path), '-o', str(output_path)], check=True)
    return output_path

def _md_to_html(self, input_path, output_path):
    subprocess.run(['pandoc', str(input_path), '-s', '-o', str(output_path)], check=True)
    return output_path

def _md_to_pptx(self, input_path, output_path):
    subprocess.run(['marp', str(input_path), '-o', str(output_path)], check=True)
    return output_path

# Office to Markdown (using markitdown)
def _docx_to_md(self, input_path, output_path):
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(input_path))
    with open(output_path, 'w') as f:
        f.write(result.text_content)
    return output_path

def _xlsx_to_md(self, input_path, output_path):
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(input_path))
    with open(output_path, 'w') as f:
        f.write(result.text_content)
    return output_path

def _pptx_to_md(self, input_path, output_path):
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(input_path))
    with open(output_path, 'w') as f:
        f.write(result.text_content)
    return output_path

# PDF conversions
def _pdf_to_docx(self, input_path, output_path):
    from pdf2docx import Converter
    cv = Converter(str(input_path))
    cv.convert(str(output_path))
    cv.close()
    return output_path

def _pdf_to_md(self, input_path, output_path):
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(input_path))
    with open(output_path, 'w') as f:
        f.write(result.text_content)
    return output_path

# Office to PDF (using LibreOffice)
def _docx_to_pdf(self, input_path, output_path):
    subprocess.run([
        'soffice', '--headless', '--convert-to', 'pdf',
        '--outdir', str(output_path.parent), str(input_path)
    ], check=True)
    return output_path

def _xlsx_to_pdf(self, input_path, output_path):
    subprocess.run([
        'soffice', '--headless', '--convert-to', 'pdf',
        '--outdir', str(output_path.parent), str(input_path)
    ], check=True)
    return output_path

def _pptx_to_pdf(self, input_path, output_path):
    subprocess.run([
        'soffice', '--headless', '--convert-to', 'pdf',
        '--outdir', str(output_path.parent), str(input_path)
    ], check=True)
    return output_path
```

### Progress Tracking

```python
from tqdm import tqdm

def batch_convert_with_progress(converter, input_dir, output_format, output_dir=None):
    """Batch convert with progress bar."""
    input_path = Path(input_dir)
    files = list(input_path.glob('*'))
    
    results = []
    for file in tqdm(files, desc=f"Converting to {output_format}"):
        try:
            result = converter.convert(file, output_format, output_dir)
            results.append({'file': str(file), 'status': 'success'})
        except Exception as e:
            results.append({'file': str(file), 'status': 'error', 'error': str(e)})
    
    return results
```

## Best Practices

1. **Test Sample First**: Convert a few files before batch processing
2. **Check Disk Space**: Ensure sufficient space for output
3. **Use Parallel Processing**: Speed up with multiple workers
4. **Handle Errors Gracefully**: Log failures, continue processing
5. **Verify Output**: Spot-check converted files

## Common Patterns

### Format Detection Pipeline
```python
def detect_and_convert(file_path, target_format):
    """Automatically detect format and convert."""
    import mimetypes
    
    mime_type, _ = mimetypes.guess_type(str(file_path))
    
    format_map = {
        'application/pdf': 'pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
        'text/markdown': 'md',
        'text/html': 'html',
    }
    
    source_format = format_map.get(mime_type, Path(file_path).suffix[1:])
    
    converter = DocumentConverter()
    return converter.convert(file_path, target_format)
```

### Multi-Format Output
```python
def convert_to_multiple_formats(input_file, output_formats, output_dir):
    """Convert one file to multiple formats."""
    converter = DocumentConverter()
    results = {}
    
    for fmt in output_formats:
        try:
            output = converter.convert(input_file, fmt, output_dir)
            results[fmt] = {'status': 'success', 'path': str(output)}
        except Exception as e:
            results[fmt] = {'status': 'error', 'error': str(e)}
    
    return results

# Convert README to multiple formats
results = convert_to_multiple_formats(
    'README.md',
    ['docx', 'pdf', 'html'],
    './exports'
)
```

## Examples

### Example 1: Documentation Export
```python
from pathlib import Path
import json

def export_documentation(docs_dir, export_dir):
    """Export all documentation to multiple formats."""
    
    converter = DocumentConverter(max_workers=8)
    docs_path = Path(docs_dir)
    export_path = Path(export_dir)
    
    # Create format directories
    for fmt in ['pdf', 'docx', 'html']:
        (export_path / fmt).mkdir(parents=True, exist_ok=True)
    
    all_results = {}
    
    # Find all markdown files
    md_files = list(docs_path.rglob('*.md'))
    
    for md_file in md_files:
        file_results = {}
        
        for fmt in ['pdf', 'docx', 'html']:
            output_dir = export_path / fmt
            try:
                output = converter.convert(md_file, fmt, output_dir)
                file_results[fmt] = 'success'
            except Exception as e:
                file_results[fmt] = f'error: {e}'
        
        all_results[str(md_file)] = file_results
        print(f"Processed: {md_file.name}")
    
    # Save report
    with open(export_path / 'export_report.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    return all_results

results = export_documentation('./docs', './exports')
```

### Example 2: Legacy Document Migration
```python
def migrate_legacy_docs(source_dir, target_dir):
    """Migrate legacy documents to modern formats."""
    
    converter = DocumentConverter(max_workers=4)
    
    # Migration rules
    migrations = [
        ('*.doc', 'docx'),   # Old Word to new
        ('*.xls', 'xlsx'),   # Old Excel to new
        ('*.ppt', 'pptx'),   # Old PowerPoint to new
        ('*.rtf', 'docx'),   # RTF to Word
    ]
    
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    target_path.mkdir(exist_ok=True)
    
    total_migrated = 0
    errors = []
    
    for pattern, target_format in migrations:
        files = list(source_path.glob(pattern))
        
        for file in files:
            try:
                # Use LibreOffice for legacy formats
                subprocess.run([
                    'soffice', '--headless',
                    '--convert-to', target_format,
                    '--outdir', str(target_path),
                    str(file)
                ], check=True)
                
                total_migrated += 1
                print(f"Migrated: {file.name}")
                
            except Exception as e:
                errors.append({'file': str(file), 'error': str(e)})
    
    print(f"\nMigration complete: {total_migrated} files")
    print(f"Errors: {len(errors)}")
    
    return {'migrated': total_migrated, 'errors': errors}
```

### Example 3: Report Generation Pipeline
```python
def generate_reports_pipeline(data_files, template_dir, output_dir):
    """Generate reports from data files using templates."""
    
    from datetime import datetime
    
    converter = DocumentConverter()
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    reports = []
    
    for data_file in data_files:
        # Load data
        data_path = Path(data_file)
        
        # Generate markdown report
        md_content = f"""---
title: Report - {data_path.stem}
date: {datetime.now().strftime('%Y-%m-%d')}
---

# {data_path.stem} Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Data Summary

"""
        
        # Add data content (simplified)
        if data_path.suffix == '.xlsx':
            from markitdown import MarkItDown
            md = MarkItDown()
            result = md.convert(str(data_path))
            md_content += result.text_content
        
        # Save markdown
        md_file = output_path / f"{data_path.stem}_{timestamp}.md"
        with open(md_file, 'w') as f:
            f.write(md_content)
        
        # Convert to PDF and DOCX
        for fmt in ['pdf', 'docx']:
            try:
                output = converter.convert(md_file, fmt, output_path)
                reports.append({'source': str(data_file), 'output': str(output), 'format': fmt})
            except Exception as e:
                print(f"Error converting {data_file} to {fmt}: {e}")
    
    return reports
```

## Limitations

- Some format combinations not supported
- Complex formatting may be lost in conversion
- Large files may require more time
- Some conversions need external tools (LibreOffice, Pandoc)
- Quality varies by source document complexity

## Installation

```bash
# Core dependencies
pip install pdf2docx markitdown python-docx openpyxl

# Pandoc (for MD conversions)
brew install pandoc  # macOS
apt install pandoc   # Ubuntu

# Marp (for PPTX)
npm install -g @marp-team/marp-cli

# LibreOffice (for Office formats)
brew install libreoffice  # macOS
apt install libreoffice   # Ubuntu
```

## Resources

- [Pandoc Documentation](https://pandoc.org/MANUAL.html)
- [markitdown GitHub](https://github.com/microsoft/markitdown)
- [pdf2docx Documentation](https://pdf2docx.readthedocs.io/)
- [LibreOffice CLI](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html)
