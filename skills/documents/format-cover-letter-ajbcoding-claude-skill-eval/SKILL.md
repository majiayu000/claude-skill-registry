---
name: format-cover-letter
description: Intelligent cover letter formatting with semantic understanding of structure and content (project, gitignored)
---

# Format Cover Letter Skill

## Purpose

Format cover letters with intelligent style application and automatic play title italicization. Uses the shared career documents template with 19 semantic styles and learns from your corrections over time.

## Usage

**Format with just body text (metadata auto-inferred):**
```
Format this cover letter: [paste body paragraphs only]
```
I'll infer contact block, date, recipient, and RE line!

**Format with complete JSON:**
```
Format this cover letter: [paste full JSON with metadata]
```

**Format from file:**
```
Format my-cover-letter.txt
```

## How It Works

1. **Semantic Analysis**: I analyze content to understand elements (contact info, recipient address, RE line, body text, etc.)

2. **Style Mapping**: Based on context, I assign appropriate styles:
   - "ANTHONY BYRNES" at top → Contact Name
   - "RE: Position Title" → RE Line (bold orange)
   - Body text mentioning "Louis & Keely: Live at the Sahara" → Auto-italicized via dictionary

3. **Hybrid Inline Styling**: Play/production titles automatically italicized:
   - Dictionary lookup (95% of cases - no manual markup needed)
   - Manual override for new/unknown plays
   - Exclusion for edge cases

4. **Generate Document**: Create formatted .docx using template

5. **Visual Preview**: Show PDF preview for review

6. **Learn from Corrections**: If you correct a style choice, I remember for next time

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
- Play Title - Italic for productions (auto-styled via dictionary!)
- Institution - Bold for school/company names
- Job Title - Bold italic for positions
- Orange Emphasis - Highlight text
- Gray Text - Dates, secondary info

## Cover Letter Elements

**Contact Block** (top of page):
```
ANTHONY BYRNES
T: 213.305.3132
E: anthonybyrnes@mac.com
```

**Recipient Address**:
```
Colburn School
200 South Grand Avenue
Los Angeles, CA 90012
```

**RE Line** (bold orange, same as section headers):
```
RE: General Manager of Performances & Events Division
```

**Body Text** with auto-italicized play titles:
```
For Louis & Keely: Live at the Sahara, I generated $1.4 million...
```
→ "Louis & Keely: Live at the Sahara" automatically italicized from dictionary

**Signature**:
```
Sincerely,

[signature image]

Anthony Byrnes
```

## Metadata Inference (NEW!)

**You provide:** Raw text or minimal JSON (just body paragraphs)

**I infer:**
- Contact block (from defaults.yaml)
- Date line (today's date)
- Recipient address (from job description or content)
- RE line (from job title)
- Salutation (extracted from content)

**Smart Job Description Matching:**

1. I search `career-applications/*/00-job-description.md` files
2. Match based on organization/position mentioned in your letter
3. **Confirm with you:** "Found job description for UCLA - Associate Dean. Use this?"
4. Extract recipient and RE line from confirmed job description

**Confirmation Before Formatting:**

```
Inferred Metadata:

Contact:       ✓ ANTHONY BYRNES
               ✓ T: 213.305.3132
               ✓ E: anthonybyrnes@mac.com

Date:          November 11, 2025

Recipient:     UCLA School of Theater, Film and Television

RE:            Associate Dean and Chief Administrative Officer [CAO]

Salutation:    Dear Search Committee,

Looks correct? (yes/modify/[field name])
```

**Configuration:**
- Defaults: `~/.claude/skills/format-cover-letter/defaults.yaml`
- Job descriptions: Auto-searched in career-applications/

## Workflow

**Step 1: Analyze Content**

I'll parse your content and create JSON structure:

```json
{
  "document_metadata": {
    "type": "cover-letter",
    "author_name": "Anthony Byrnes",
    "document_title": "Position Title Cover Letter"
  },
  "content": [
    {"text": "ANTHONY BYRNES", "style": "Contact Name", "type": "paragraph"},
    {"text": "RE: Position Title", "style": "RE Line", "type": "paragraph"},
    {"text": "Body with play title...", "style": "Body Text", "type": "paragraph"}
  ]
}
```

**Step 2: Generate Document**

I'll call the formatter to create your .docx:

```python
import json
import subprocess
from pathlib import Path

# Save content mapping
mapping_file = "/tmp/cover_letter_mapping.json"
with open(mapping_file, 'w') as f:
    json.dump(data, f, indent=2)

# Format document
result = subprocess.run([
    "python3",
    "format_cv.py",
    mapping_file,
    output_path,
    "--document-type", "cover-letter",
    "--preview"
], capture_output=True, text=True, cwd=str(Path.home() / "PycharmProjects/career-lexicon-builder"))
```

**Step 3: Visual Preview**

I'll convert to PDF and show you what it looks like using the `open` command.

**Step 4: Review**

You can request changes: "That venue should be italic" or "Don't emphasize that number"

**Step 5: Learn (if corrections made)**

If you made corrections, I'll update `learned-preferences.yaml` and add new plays to `play-titles-dictionary.yaml`.

## Hybrid Inline Styling

**The Problem**: Manually marking up every play title is tedious:
```json
{
  "text": "For Louis & Keely: Live at the Sahara, I...",
  "runs": [
    {"text": "For ", "style": null},
    {"text": "Louis & Keely: Live at the Sahara", "style": "Play Title"},
    {"text": ", I...", "style": null}
  ]
}
```

**The Solution**: Dictionary auto-styling (95% of cases):
```json
{
  "text": "For Louis & Keely: Live at the Sahara, I...",
  "style": "Body Text"
}
```
→ "Louis & Keely: Live at the Sahara" automatically italicized from dictionary!

**Dictionary Location**:
```
~/.claude/skills/format-cover-letter/play-titles-dictionary.yaml
```

**Example dictionary**:
```yaml
productions:
  - "Louis & Keely: Live at the Sahara"
  - "Romeo & Juliet"
  - "Hamlet"

programs:
  - "Experience LA!"
```

**Manual Override** (for new/unknown plays):
```json
{
  "text": "For My New Play, I generated...",
  "style": "Body Text",
  "inline_styles": [
    {"text": "My New Play", "style": "Play Title"}
  ]
}
```

**Exclusion** (when dictionary shouldn't apply):
```json
{
  "text": "We decided NOT to produce Romeo & Juliet.",
  "inline_styles": [
    {"text": "Romeo & Juliet", "exclude": true}
  ]
}
```

## Learning System

**You:** "Add 'The Tempest' to the dictionary"

**Me:** ✓ Added to `play-titles-dictionary.yaml`

**Next cover letter:** Automatically italicizes "The Tempest" without asking.

## Signature Images

**Setup signature:**
1. Create PNG of your signature (~1.5 inches wide, transparent background)
2. Save to: `~/.claude/skills/format-cover-letter/signatures/signature.png`
3. Reference in JSON: `{"text": "signature", "style": "Signature Image", "type": "image"}`

**If signature missing:** System logs warning and continues without image.

## Template Location

**Shared template path:**
```
cv_formatting/templates/career-documents-template.docx
```

**Why shared?** Same template as format-resume ensures visual consistency across CV and cover letter.

## Key Differences from CV Formatting

| Aspect | CV (format-resume) | Cover Letter (this skill) |
|--------|-------------------|---------------------------|
| **Organization** | Timeline-based sections | Narrative paragraphs |
| **Section Headers** | Orange, 11pt | Orange, 13pt (bug fixed!) |
| **Main Content** | Timeline entries, bullets | Body text paragraphs |
| **Special Elements** | Hanging indent timelines | Contact block, RE line, signature |
| **Inline Styling** | Manual only | Hybrid (dictionary + manual) |

**IMPORTANT**: Section headers are **ALWAYS ORANGE** for both CVs and cover letters. Earlier versions incorrectly made cover letter headers black.

## Error Handling

**Template not found:**
```
Run: python generate_cv_template.py
```

**PDF preview not available:**
```
Install: brew install libreoffice
```

**Image generation skipped:**
```
Install: brew install poppler
```

## Files

- `career-documents-template.docx` - Shared template with 19 semantic styles
- `format_cv.py` - Main formatting script
- `play-titles-dictionary.yaml` - Known plays for auto-italicization
- `learned-preferences.yaml` - Your accumulated corrections
- `signatures/` - Directory for signature images

## JSON Export for Wrapper Application

After formatting the cover letter, export structured formatting metadata to enable wrapper application integration.

### Phase 6: JSON Export

**Write to:** `cover-letter-formatted-v1.json` (increment version if exists)

**Implementation:**
1. Check if `cover-letter-formatted-v1.json` already exists
2. If exists, increment version: `cover-letter-formatted-v2.json`, `cover-letter-formatted-v3.json`, etc.
3. Extract formatting metadata from the document generation process
4. Write JSON file with proper formatting (2-space indentation)
5. Save to same directory as output files

**Structure:**
```json
{
  "metadata": {
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "version": 1,
    "skill": "format-cover-letter",
    "input_file": "cover-letter-draft.md",
    "output_file": "cover-letter-formatted.pdf"
  },
  "formatting_metadata": {
    "template": "career-documents-template.docx",
    "template_path": "cv_formatting/templates/career-documents-template.docx",
    "font": "Helvetica",
    "font_size": 11,
    "margins": {
      "top": 0.75,
      "bottom": 0.75,
      "left": 1.0,
      "right": 1.0
    },
    "line_spacing": 1.15,
    "paragraph_spacing": 0.15,
    "letterhead": true,
    "signature": "included"
  },
  "content_structure": {
    "header": {
      "name": "ANTHONY BYRNES",
      "contact": {
        "phone": "213.305.3132",
        "email": "anthonybyrnes@mac.com"
      },
      "validation": "passed"
    },
    "date": {
      "text": "November 12, 2025",
      "format": "MMMM DD, YYYY",
      "validation": "passed"
    },
    "recipient": {
      "organization": "UCLA School of Theater, Film and Television",
      "address_lines": [
        "UCLA School of Theater, Film and Television",
        "102 East Melnitz Hall",
        "Los Angeles, CA 90095"
      ],
      "validation": "passed"
    },
    "re_line": {
      "text": "RE: Associate Dean and Chief Administrative Officer [CAO]",
      "style": "RE Line",
      "validation": "passed"
    },
    "salutation": {
      "text": "Dear Search Committee,",
      "validation": "passed"
    },
    "body": [
      {
        "paragraph": 1,
        "purpose": "opening",
        "word_count": 85,
        "has_play_titles": true,
        "inline_styles_applied": 2,
        "validation": "passed"
      },
      {
        "paragraph": 2,
        "purpose": "body",
        "word_count": 120,
        "has_play_titles": true,
        "inline_styles_applied": 3,
        "validation": "passed"
      },
      {
        "paragraph": 3,
        "purpose": "body",
        "word_count": 95,
        "has_play_titles": false,
        "inline_styles_applied": 1,
        "validation": "passed"
      },
      {
        "paragraph": 4,
        "purpose": "closing",
        "word_count": 42,
        "has_play_titles": false,
        "inline_styles_applied": 0,
        "validation": "passed"
      }
    ],
    "closing": {
      "salutation": "Sincerely,",
      "signature_space": true,
      "signature_image": true,
      "name": "Anthony Byrnes",
      "validation": "passed"
    }
  },
  "validation_results": {
    "total_checks": 12,
    "passed": 12,
    "failed": 0,
    "warnings": 0,
    "checks": [
      {"check": "header_present", "status": "passed"},
      {"check": "date_format_correct", "status": "passed"},
      {"check": "recipient_complete", "status": "passed"},
      {"check": "re_line_formatted", "status": "passed"},
      {"check": "salutation_professional", "status": "passed"},
      {"check": "body_paragraphs_present", "status": "passed"},
      {"check": "play_titles_italicized", "status": "passed"},
      {"check": "inline_styles_applied", "status": "passed"},
      {"check": "closing_complete", "status": "passed"},
      {"check": "signature_included", "status": "passed"},
      {"check": "page_count_valid", "status": "passed"},
      {"check": "professional_tone", "status": "passed"}
    ],
    "issues": []
  },
  "styling_metadata": {
    "play_titles_dictionary_used": true,
    "dictionary_matches": [
      "Louis & Keely: Live at the Sahara",
      "Romeo & Juliet"
    ],
    "manual_inline_styles": [
      {"text": "The New Play", "style": "Play Title", "reason": "not in dictionary"}
    ],
    "exclusions": [],
    "styles_applied": {
      "Contact Name": 1,
      "Contact Info": 2,
      "Date Line": 1,
      "Recipient Address": 3,
      "RE Line": 1,
      "Body Text": 4,
      "Play Title": 5,
      "Institution": 3,
      "Job Title": 2
    }
  },
  "metrics": {
    "page_count": 1,
    "word_count": 342,
    "paragraph_count": 4,
    "sentence_count": 18,
    "estimated_read_time_seconds": 80,
    "average_paragraph_length": 85,
    "readability_score": 0.90,
    "professionalism_score": 0.93,
    "visual_appeal_score": 0.91
  },
  "output_files": [
    {
      "type": "docx",
      "path": "cover-letter-formatted.docx",
      "size_bytes": 87654,
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "type": "pdf",
      "path": "cover-letter-formatted.pdf",
      "size_bytes": 156432,
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ],
  "learned_preferences": {
    "new_plays_added": ["The New Play"],
    "style_corrections": [],
    "user_feedback": ""
  }
}
```

**Present to user:**
```
Formatting complete! Saved to:
- cover-letter-formatted.docx (formatted document)
- cover-letter-formatted.pdf (visual preview)
- cover-letter-formatted-v1.json (structured metadata)

Document metrics:
- Pages: 1
- Word count: 342
- Paragraphs: 4
- Validation: 12/12 checks passed
- Readability score: 0.90

All play titles automatically italicized from dictionary. Ready for review!
```

## Related

- Format Resume Skill: `~/.claude/skills/format-resume/skill.md`
- Implementation Handoff: `docs/handoffs/2025-11-11-cover-letter-formatting-implementation-complete.md`
- Template generation: `python generate_cv_template.py`

---

**Ready to format your cover letter?**

Just say: "Format this cover letter: [your content]"
