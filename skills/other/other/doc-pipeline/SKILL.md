---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: doc-pipeline
description: "Chain document operations into reusable pipelines"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: workflow
tags:
  - pipeline
  - workflow
  - document
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

# Skill Capabilities
capabilities:
  - document_workflow
  - pipeline_automation

# Language Support
languages:
  - en
  - zh
---

# Doc Pipeline Skill

## Overview

This skill enables building document processing pipelines - chain multiple operations (extract, transform, convert) into reusable workflows with data flowing between stages.

## How to Use

1. Describe what you want to accomplish
2. Provide any required input data or files
3. I'll execute the appropriate operations

**Example prompts:**
- "PDF → Extract Text → Translate → Generate DOCX"
- "Image → OCR → Summarize → Create Report"
- "Excel → Analyze → Generate Charts → Create PPT"
- "Multiple inputs → Merge → Format → Output"

## Domain Knowledge


### Pipeline Architecture

```
Stage 1      Stage 2      Stage 3      Stage 4
┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐
│Extract│ → │Transform│ → │ AI   │ → │Output│
│ PDF  │    │  Data  │    │Analyze│   │ DOCX │
└──────┘    └──────┘    └──────┘    └──────┘
     │           │           │           │
     └───────────┴───────────┴───────────┘
                 Data Flow
```

### Pipeline DSL (Domain Specific Language)

```yaml
# pipeline.yaml
name: contract-review-pipeline
description: Extract, analyze, and report on contracts

stages:
  - name: extract
    operation: pdf-extraction
    input: $input_file
    output: $extracted_text
    
  - name: analyze
    operation: ai-analyze
    input: $extracted_text
    prompt: "Review this contract for risks..."
    output: $analysis
    
  - name: report
    operation: docx-generation
    input: $analysis
    template: templates/review_report.docx
    output: $output_file
```

### Python Implementation

```python
from typing import Callable, Any
from dataclasses import dataclass

@dataclass
class Stage:
    name: str
    operation: Callable
    
class Pipeline:
    def __init__(self, name: str):
        self.name = name
        self.stages: list[Stage] = []
    
    def add_stage(self, name: str, operation: Callable):
        self.stages.append(Stage(name, operation))
        return self  # Fluent API
    
    def run(self, input_data: Any) -> Any:
        data = input_data
        for stage in self.stages:
            print(f"Running stage: {stage.name}")
            data = stage.operation(data)
        return data

# Example usage
pipeline = Pipeline("contract-review")
pipeline.add_stage("extract", extract_pdf_text)
pipeline.add_stage("analyze", analyze_with_ai)
pipeline.add_stage("generate", create_docx_report)

result = pipeline.run("/path/to/contract.pdf")
```

### Advanced: Conditional Pipelines

```python
class ConditionalPipeline(Pipeline):
    def add_conditional_stage(self, name: str, condition: Callable, 
                               if_true: Callable, if_false: Callable):
        def conditional_op(data):
            if condition(data):
                return if_true(data)
            return if_false(data)
        return self.add_stage(name, conditional_op)

# Usage
pipeline.add_conditional_stage(
    "ocr_if_needed",
    condition=lambda d: d.get("has_images"),
    if_true=run_ocr,
    if_false=lambda d: d
)
```


## Best Practices

1. **Keep stages focused (single responsibility)**
2. **Use intermediate outputs for debugging**
3. **Implement stage-level error handling**
4. **Make pipelines configurable via YAML/JSON**

## Installation

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## Resources

- [Custom Repository](https://github.com/claude-office-skills/skills)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)
