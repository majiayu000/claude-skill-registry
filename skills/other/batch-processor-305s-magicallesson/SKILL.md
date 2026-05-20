---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: batch-processor
description: "Process multiple documents in bulk with parallel execution"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: workflow
tags:
  - batch
  - processor
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
  - batch_processing
  - automation

# Language Support
languages:
  - en
  - zh
---

# Batch Processor Skill

## Overview

This skill enables efficient bulk processing of documents - convert, transform, extract, or analyze hundreds of files with parallel execution and progress tracking.

## How to Use

1. Describe what you want to accomplish
2. Provide any required input data or files
3. I'll execute the appropriate operations

**Example prompts:**
- "Convert 100 PDFs to Word documents"
- "Extract text from all images in a folder"
- "Batch rename and organize files"
- "Mass update document headers/footers"

## Domain Knowledge


### Batch Processing Patterns

```
Input: [file1, file2, ..., fileN]
         │
         ▼
    ┌─────────────┐
    │  Parallel   │  ← Process multiple files concurrently
    │  Workers    │
    └─────────────┘
         │
         ▼
Output: [result1, result2, ..., resultN]
```

### Python Implementation

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from tqdm import tqdm

def process_file(file_path: Path) -> dict:
    """Process a single file."""
    # Your processing logic here
    return {"path": str(file_path), "status": "success"}

def batch_process(input_dir: str, pattern: str = "*.*", max_workers: int = 4):
    """Process all matching files in directory."""
    
    files = list(Path(input_dir).glob(pattern))
    results = []
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, f): f for f in files}
        
        for future in tqdm(as_completed(futures), total=len(files)):
            file = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({"path": str(file), "error": str(e)})
    
    return results

# Usage
results = batch_process("/documents/invoices", "*.pdf", max_workers=8)
print(f"Processed {len(results)} files")
```

### Error Handling & Resume

```python
import json
from pathlib import Path

class BatchProcessor:
    def __init__(self, checkpoint_file: str = "checkpoint.json"):
        self.checkpoint_file = checkpoint_file
        self.processed = self._load_checkpoint()
    
    def _load_checkpoint(self):
        if Path(self.checkpoint_file).exists():
            return json.load(open(self.checkpoint_file))
        return {}
    
    def _save_checkpoint(self):
        json.dump(self.processed, open(self.checkpoint_file, "w"))
    
    def process(self, files: list, processor_func):
        for file in files:
            if str(file) in self.processed:
                continue  # Skip already processed
            
            try:
                result = processor_func(file)
                self.processed[str(file)] = {"status": "success", **result}
            except Exception as e:
                self.processed[str(file)] = {"status": "error", "error": str(e)}
            
            self._save_checkpoint()  # Resume-safe
```


## Best Practices

1. **Use progress bars (tqdm) for user feedback**
2. **Implement checkpointing for long jobs**
3. **Set reasonable worker counts (CPU cores)**
4. **Log failures for later review**

## Installation

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## Resources

- [Custom Repository](https://github.com/claude-office-skills/skills)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)
