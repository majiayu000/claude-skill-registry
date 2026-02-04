---
name: hf-papers-reporter
description: Generate Word reports from Hugging Face Daily Papers. Downloads top papers, extracts abstracts and introductions from PDFs, extracts figures, and compiles everything into a formatted Word document with cover images. Use when user asks for 'HF daily papers', 'Hugging Face papers report', 'download papers and make a summary', or any request to fetch, analyze, and document papers from huggingface.co/papers.
---

# Hugging Face Daily Papers Reporter

Generate professional Word reports from Hugging Face Daily Papers with full text extraction and image capture.

## What This Skill Does

1. Scrapes huggingface.co/papers for the top papers
2. Downloads PDFs from arXiv
3. Extracts Abstract and Introduction sections
4. Extracts figures/images from PDFs
5. Generates a formatted Word document (.docx) with:
   - Paper titles and arXiv links
   - Cover images from HF
   - Full abstracts
   - Introduction sections
   - Extracted figures from papers

## Quick Start

Run the main script to generate today's report:

```bash
cd /path/to/hf-papers-reporter
python3 scripts/process_papers.py
```

Output will be saved to `output/HF_Daily_Papers_Report.docx`

## Dependencies

Install required packages:
```bash
pip3 install PyMuPDF python-docx Pillow beautifulsoup4 requests
```

## How It Works

### Step 1: Fetch Paper List
- Scrapes huggingface.co/papers
- Extracts arXiv IDs, titles, and cover image URLs

### Step 2: Download & Process (per paper)
```
Download PDF from arxiv.org/pdf/{id}.pdf
    ↓
Extract text (first 5 pages)
    - Abstract (regex match)
    - Introduction (regex match)
    ↓
Extract images (first 5 pages, max 3 per page)
    - Compress to 600x400
    ↓
Download cover image from HF CDN
    - Compress to 800x600
```

### Step 3: Generate Word Document
- Title page with report name and date
- Each paper as a section with:
  - Cover image (centered)
  - Abstract section
  - Introduction section  
  - Extracted figures (up to 4)

## Output Structure

```
hf_papers/
├── pdfs/           # Downloaded PDFs
├── images/         # Cover images + extracted figures
└── output/
    ├── HF_Daily_Papers_Report.docx
    └── papers_data.json
```

## Known Issues & Solutions

| Issue | Cause | Fix |
|-------|-------|-----|
| XML encoding error | PDF text contains control characters | Script auto-cleans 0x00-0x1F chars |
| No abstract found | PDF structure varies | Multiple regex patterns tried |
| Large PDFs | Some papers are 20MB+ | Only first 5 pages processed |

## Customization

To modify the number of papers (default: 10), edit the `PAPERS` list in `scripts/process_papers.py`.

To change image sizes, modify the `thumbnail()` calls in the script.
