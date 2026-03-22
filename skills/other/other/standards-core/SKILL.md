---
name: standards-core
description: Map K–12 Math/ELA standards (CCSS or state) to pages, lessons, tasks, and assessments in large PDF textbooks. Use when asked to compute alignment coverage, gaps, off-grade content, redundancy, or to output a per-standard evidence matrix with page anchors.
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Standards-Core

## What this Skill does
Given one or more PDF textbooks (teacher + student editions), produce:
- **coverage_matrix.csv / .json** — standard ↔ {taught, practiced, assessed}, intensity, off-grade flags, redundancy.
- **evidence.jsonl** — for each standard: top page hits with quoted spans and `book_id:page:start:end` anchors.
- **pages.jsonl** — page-level text index (one JSON object per page).

## How to run
1. Prefer the installed `document-skills/pdf` to extract page text and tables. If not present, fall back to `pdftotext` (if available).
2. Build a page index: write `outputs/pages.jsonl` with {book_id, page, text}.
3. Load a **standards pack** (YAML) defining standards, grade ranges, and keyword lexicons.
4. Run `scripts/align_standards.py` to propose hits, then refine with LLM judgments for borderline matches.
5. Compute coverage, off-grade %, and redundancy per standard; write to `outputs/coverage.json` and `outputs/coverage.csv`.
6. For each standard with a rating, capture ≥1 quoted span + page anchor in `outputs/evidence.jsonl`. If none found, mark: `"unrated": "evidence not found"`.

## Inputs (ask the user or read CLI args)
- subject: math|ela
- grades: e.g., 3–5
- standards_pack: path to YAML (CCSS or state) with `id`, `grade`, `keywords[]`, `anti_keywords[]`, `examples[]`
- pdfs: list of files
- out_dir: outputs/

## Deterministic first, generative second
- Use Python scripts for parsing, counting, CSV/JSON writing.
- Use the model only for disambiguation (e.g., near-miss span classification) and for short rationales.

## Scripts to call
- `scripts/align_standards.py --pages outputs/pages.jsonl --standards standards/<pack>.yaml --subject {math|ela} --grades <range> --out outputs`

## Evidence requirements
- Do NOT claim a standard is covered without at least one quoted span and page anchor.
- If evidence is missing, set the status `"unrated": "evidence not found"` and surface a TODO.

## Minimal standards pack example (save as standards/ccss_math_sample.yaml)
```yaml
standards:
  - id: "3.NF.A.1"
    grade: 3
    keywords: ["fraction", "equal parts", "numerator", "denominator"]
    anti_keywords: ["percent"]
  - id: "4.OA.A.3"
    grade: 4
    keywords: ["multi-step", "word problem", "interpret", "remainders"]
    anti_keywords: []
```

## Output file formats

### coverage.json
```json
{
  "metadata": {
    "subject": "math",
    "grades": "3-5",
    "books": ["math_grade3.pdf"],
    "total_standards": 15
  },
  "standards": [
    {
      "id": "3.NF.A.1",
      "grade": 3,
      "taught": true,
      "practiced": true,
      "assessed": false,
      "intensity": "high",
      "off_grade_percent": 5,
      "redundancy_count": 2,
      "evidence_found": true,
      "top_pages": [12, 15, 18],
      "rationale": "Clear instruction with multi-page practice problems"
    },
    {
      "id": "3.NF.A.1",
      "grade": 3,
      "taught": false,
      "practiced": false,
      "assessed": false,
      "intensity": "none",
      "off_grade_percent": 0,
      "redundancy_count": 0,
      "evidence_found": false,
      "unrated": "evidence not found"
    }
  ],
  "summary": {
    "total_covered": 12,
    "total_uncovered": 3,
    "coverage_percent": 80
  }
}
```

### evidence.jsonl (one object per line)
```jsonl
{"standard": "3.NF.A.1", "pages": [12, 15, 18], "top_hit": {"page": 12, "book_id": "math_grade3", "quote": "A fraction is an equal part of a whole", "anchor": "math_grade3:12:45:92", "context": "Instruction section on Understanding Fractions"}}
{"standard": "3.NF.A.2", "pages": [20], "top_hit": {"page": 20, "book_id": "math_grade3", "quote": "On a number line, locate 1/2, 1/3, 1/4", "anchor": "math_grade3:20:120:165", "context": "Practice worksheet"}}
{"standard": "4.OA.A.1", "unrated": "evidence not found"}
```

### pages.jsonl (one object per page)
```jsonl
{"book_id": "math_grade3", "page": 1, "text": "Chapter 1: Understanding Numbers... [page content]"}
{"book_id": "math_grade3", "page": 2, "text": "Lesson 1.1: Counting and Place Value... [page content]"}
```

## Workflow example
```bash
# 1. Extract and index PDF pages
scripts/align_standards.py --extract-pages math_grade3.pdf --out outputs

# 2. Run standards alignment
scripts/align_standards.py \
  --pages outputs/pages.jsonl \
  --standards standards/ccss_math_grade3.yaml \
  --subject math \
  --grades 3 \
  --out outputs

# 3. Review outputs
# - outputs/coverage.json
# - outputs/coverage.csv
# - outputs/evidence.jsonl
```

## Error handling
- If a PDF cannot be read, log and skip with a warning.
- If a standards pack is malformed, halt with a descriptive error.
- If no evidence is found for a standard, mark unrated and raise a TODO comment for manual review.
