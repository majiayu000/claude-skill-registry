---
name: format-resume
description: Intelligently format CV/resume content using semantic understanding and visual verification
---

# Format Resume Skill

## Purpose

Format CV/resume content with intelligent style application based on semantic context. Uses a clean template with 19 semantic styles and learns from your corrections over time.

## Usage

**Format new content:**
```
Format this CV: [paste content]
```

**Format from file:**
```
Format my-cv-draft.txt as a resume
```

## How It Works

**Key Principle: Intelligence lives in the skill (Claude analyzes text). Python code is just helpers.**

1. **Semantic Analysis**: I (Claude) analyze your raw text to understand what each element represents
   - I don't use regex patterns - I understand semantic context
   - "Anthony Byrnes" at top → CV Name
   - "EDUCATION" in caps → Section Header
   - "2023 - Present California State University" → Timeline Entry + Institution
   - "Romeo & Juliet" in productions → Play Title (not Job Title, even though both are bold italic!)

2. **Create JSON Structure**: Convert raw text to structured format with style assignments

3. **User Confirmation**: Show you my analysis, get confirmation or corrections

4. **Apply Learned Patterns**: Python helpers apply previously learned preferences

5. **Generate Document**: Create formatted .docx using template with page headers

6. **Visual Preview**: Show PDF preview images for review

7. **Learn from Corrections**: If you correct a style choice, I save it to learned-preferences.yaml

## The 19 Styles

**Paragraph Styles:**
- CV Name - Your name at top
- Contact Name - Bold, 10pt (cover letter header)
- Contact Info - Regular, 10pt (phone/email)
- Recipient Address - Regular, 11pt (organization address)
- RE Line - Bold, 13pt, ORANGE (position/subject line)
- Date Line - Right-aligned, 11pt (document date)
- Section Header - Bold, ORANGE (11pt for CV, 13pt for cover letter)
- Body Text - Standard paragraphs, 11pt
- Timeline Entry - Date + institution with hanging indent (CV only)
- Page Header - Bold, 10pt (page 2+ headers)
- Bullet Standard, Bullet Gray, Bullet Emphasis - List variations

**Character Styles (inline):**
- Play Title - Bold italic for productions (most common!)
- Institution - Bold for school/company names
- Job Title - Bold italic for positions
- Orange Emphasis - Highlight text
- Gray Text - Dates, secondary info

**Note:** Shares template with format-cover-letter skill (career-documents-template.docx)

## Workflow

**Step 1: You Provide Raw Text**

```
User: "Format this CV: [pastes raw text]"
```

**Step 2: I (Claude) Analyze and Create JSON**

I analyze your content using semantic understanding (not regex):

```
I see:
- Name: "ANTHONY BYRNES" → CV Name style
- Contact: "T: 213.305.3132" → Contact Info style
- Section: "EDUCATION" → Section Header (orange, 11pt)
- Timeline: "2020-2024 California State University, Long Beach" → Timeline Entry
  - inline: "California State University, Long Beach" → Institution (bold)
- Position: "Interim Associate Dean, College of the Arts" → Body Text
  - inline: "Interim Associate Dean" → Job Title (bold italic)
- Bullet: "Led $29M budget..." → Bullet Standard

Here's my JSON interpretation:
{
  "document_metadata": {
    "type": "cv",
    "author_name": "ANTHONY BYRNES",
    "document_title": "Curriculum Vitae",
    "page_header": {
      "enabled": true,
      "left": "ANTHONY BYRNES - Curriculum Vitae",
      "right": "page"
    }
  },
  "content": [
    {"text": "ANTHONY BYRNES", "style": "CV Name"},
    {"text": "T: 213.305.3132", "style": "Contact Info"},
    ...
  ]
}

Looks correct? (yes/show json/corrections)
```

**Step 3: You Confirm or Correct**

- Say "yes" → I proceed to formatting
- Say "Line 5 should be Gray Text" → I update JSON
- Say "show json" → I display full JSON for manual editing

**Step 4: Apply Learned Patterns**

Python helpers load learned-preferences.yaml and apply any previously learned style rules:

```python
from cv_formatting.learning_system import LearningSystem

learning = LearningSystem()
content = learning.apply_learned_patterns(content)
```

This is simple pattern matching - the intelligence came from your previous corrections.

**Step 5: Generate Document**

I save the JSON and call Python helpers to create formatted .docx:

```python
import json
import subprocess
from pathlib import Path

# Save JSON structure
mapping_file = "/tmp/cv_mapping.json"
with open(mapping_file, 'w') as f:
    json.dump(content_mapping, f, indent=2)

# Format document (Python helper just applies styles from JSON)
result = subprocess.run([
    "python3",
    "format_cv.py",
    mapping_file,
    output_path,
    "--document-type", "cv",
    "--preview"
], capture_output=True, text=True, cwd=str(Path.home() / "PycharmProjects/career-lexicon-builder"))
```

**Step 6: Visual Preview**

I convert to PDF and show you page images.

You can request changes: "That committee role should be gray text"

**Step 7: Learn (if corrections made)**

If you make corrections, I save them to learned-preferences.yaml:

```python
learning.learn_correction(
    text="Graduate Studies Advisory Committee",
    context="service section",
    preferred_style="Gray Text"
)
```

Next time I analyze a CV, I'll automatically suggest Gray Text for committee roles.

**Step 8: Finalize**

Once you're happy with the preview, I save the final document (e.g., "anthony-byrnes-cv.docx").

## LLM-Based Analysis vs. Regex Patterns

**Why LLM analysis (me, Claude) is better:**

- ✅ Understands semantic context (not just patterns)
- ✅ Handles variations naturally ("PhD" vs "Ph.D." vs "Doctor of Philosophy")
- ✅ Distinguishes context: "Dean" in experience → Job Title, "Dean" in service → Gray Text
- ✅ Can explain reasoning to you
- ✅ Learns from corrections through conversation

**Python helpers only:**
- Load defaults from YAML
- Apply previously learned patterns (simple matching)
- Find files, generate dates
- NO semantic analysis in Python code

**Example: Bold Italic Context Discrimination**

I distinguish based on semantic context, not just formatting:

- "***Interim Associate Dean***" after "2023 - Present CSULB" → Job Title (follows employer)
- "***Romeo & Juliet***" in productions list → Play Title (in artistic works context)

Traditional regex can't do this because both are bold italic. I understand the context.

## Learning System

**Three-layer learning** stored in `learned-preferences.yaml`:

**Layer 1: Style Corrections**
```yaml
style_rules:
  - pattern: "committee"
    context: "service section"
    preferred_style: "Gray Text"
    learned_date: "2025-11-11"
    example: "Graduate Studies Advisory Committee"
```

**Layer 2: Metadata Patterns**
```yaml
metadata_defaults:
  document_title: "Curriculum Vitae"  # not "Resume"
  page_header_enabled: true
  date_format: "MMMM YYYY"
```

**Layer 3: Section Patterns**
```yaml
section_patterns:
  EDUCATION:
    order: ["Timeline Entry", "Body Text", "Bullet Standard"]
    inline_institution: true
```

Corrections are automatically saved. No "save preferences" button needed.

**You:** "That should be gray text, it's a committee role"

**Me:** "✓ Updated formatting rules: committee roles → Gray Text"

**Next CV:** Automatically applies gray to committee roles without asking.

## Error Handling

**If template missing:**
- "Template not found. Run generate_cv_template.py first"

**If LibreOffice/Poppler unavailable:**
- "PDF preview not available (LibreOffice not installed)"
- "Continuing with .docx only..."

**If style mapping unclear:**
- "I'm not sure if this is a Job Title or Play Title - can you clarify?"

## Files

- `career-documents-template.docx` - Shared template with 19 semantic styles
- `format_cv.py` - Main formatting script
- `style-mappings.yaml` - Base semantic inference rules
- `learned-preferences.yaml` - Your accumulated corrections

## Page Headers for Multi-Page CVs

CVs spanning multiple pages automatically get professional headers on page 2+:

- **Format:** "ANTHONY BYRNES - Curriculum Vitae        page 2"
- **Style:** Helvetica 10pt, bold, gray (RGB 128, 128, 128)
- **Alignment:** Left text aligns with body, right text at 6.5 inches
- **Clean first page:** No header on page 1
- **Same implementation as cover letters** (already working!)

## Metadata Inference

Python helpers load from `defaults.yaml` and generate page header config:

```python
from cv_formatting.metadata_inference import MetadataHelper

helper = MetadataHelper()
metadata = helper.infer_cv_metadata(content)

# Returns:
{
  "type": "cv",
  "author_name": "ANTHONY BYRNES",
  "document_title": "Curriculum Vitae",
  "last_updated": "November 2025",
  "version": "Academic",
  "page_header": {
    "enabled": true,
    "left": "ANTHONY BYRNES - Curriculum Vitae",
    "right": "page"
  }
}
```

Detects:
- **Contact Information:** From defaults.yaml
- **Document Title:** "Curriculum Vitae", "Resume", or "CV" (from defaults or learned)
- **Version:** Academic, Industry, Arts, or General (simple keyword detection)
- **Page Header Config:** Generated automatically from template

## Configuration Files

**defaults.yaml** - Your contact info and preferences:
```yaml
contact:
  name: "ANTHONY BYRNES"
  phone: "213.305.3132"
  email: "anthonybyrnes@mac.com"

cv_defaults:
  document_title: "Curriculum Vitae"
  page_header:
    enabled: true
    format: "{name} - {title}"

preferences:
  version: "Academic"
```

**learned-preferences.yaml** - Three-layer learning system:
```yaml
style_rules: []           # Layer 1: Style corrections
metadata_defaults: {}     # Layer 2: Metadata patterns
section_patterns: {}      # Layer 3: Section structures
```

## JSON Export for Wrapper Application

After successfully formatting the resume and creating the output files, export structured metadata.

**Write to:** `resume-formatted-v1.json` (increment version if exists)

**Implementation:**
1. Check if `resume-formatted-v1.json` already exists in output directory
2. If exists, increment version number: `resume-formatted-v2.json`, `resume-formatted-v3.json`, etc.
3. Extract formatting metadata from the JSON structure and output files
4. Write JSON file with proper formatting (2-space indentation)
5. Save to same directory as formatted resume

**Structure:**
```json
{
  "metadata": {
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "version": 1,
    "skill": "format-resume",
    "input_file": "resume-content.md",
    "output_file": "resume-formatted.pdf"
  },
  "formatting_metadata": {
    "template": "career-documents-template.docx",
    "document_type": "cv",
    "font": "Helvetica",
    "font_size": 11,
    "margins": {
      "top": 0.5,
      "bottom": 0.5,
      "left": 0.5,
      "right": 0.5
    },
    "line_spacing": 1.15,
    "section_spacing": 0.15,
    "page_header": {
      "enabled": true,
      "left": "ANTHONY BYRNES - Curriculum Vitae",
      "right": "page"
    }
  },
  "sections": [
    {
      "name": "Contact Information",
      "content_preview": "ANTHONY BYRNES\nT: 213.305.3132\nE: anthonybyrnes@mac.com",
      "styles_used": ["CV Name", "Contact Info"],
      "validation": "passed",
      "issues": []
    },
    {
      "name": "Professional Experience",
      "entries": 5,
      "styles_used": ["Section Header", "Timeline Entry", "Body Text", "Bullet Standard"],
      "validation": "passed",
      "issues": []
    },
    {
      "name": "Education",
      "entries": 3,
      "styles_used": ["Section Header", "Timeline Entry", "Body Text"],
      "validation": "passed",
      "issues": []
    }
  ],
  "validation_results": {
    "total_checks": 15,
    "passed": 14,
    "failed": 0,
    "warnings": 1,
    "issues": [
      {
        "type": "warning",
        "section": "Professional Summary",
        "message": "Summary slightly long (95 words, recommend <90)",
        "severity": "low"
      }
    ]
  },
  "metrics": {
    "page_count": 2,
    "word_count": 542,
    "section_count": 7,
    "estimated_read_time_seconds": 130,
    "ats_compatibility_score": 0.92,
    "readability_score": 0.88,
    "visual_appeal_score": 0.90
  },
  "style_analysis": {
    "total_styles_used": 12,
    "paragraph_styles": ["CV Name", "Contact Info", "Section Header", "Timeline Entry", "Body Text", "Bullet Standard", "Bullet Gray"],
    "character_styles": ["Institution", "Job Title", "Play Title", "Gray Text"],
    "learned_corrections_applied": 3,
    "manual_overrides": 0
  },
  "output_files": [
    {
      "type": "pdf",
      "path": "anthony-byrnes-cv.pdf",
      "size_bytes": 245632,
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "type": "docx",
      "path": "anthony-byrnes-cv.docx",
      "size_bytes": 123456,
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ]
}
```

**Present to user:**
```
Formatting complete! Saved to:
- anthony-byrnes-cv.docx (formatted document)
- anthony-byrnes-cv.pdf (preview)
- resume-formatted-v1.json (formatting metadata)

Formatting summary:
- Pages: 2
- Sections: 7
- Styles used: 12 (7 paragraph, 5 character)
- Validation: 14/15 checks passed (1 warning)
- ATS compatibility: 92%

Would you like to:
1. Review the PDF preview
2. Make style corrections
3. Export a different format
```

## Related

- Design: `docs/plans/2025-11-09-cv-style-extraction-and-formatting-design.md`
- CV Enhancements: `docs/plans/2025-11-11-cv-formatting-enhancements-design.md`
- Template generation: `python generate_cv_template.py`
- Validation: `python validate_template.py`
