---
name: evidence-binder
description: Compile quoted evidence and page snapshots from standards-core output into a reviewer-ready binder. Exports to Markdown, PDF, or DOCX with page-level anchors, standard groupings, and professional formatting for EdReports-style curriculum reviews.
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Evidence-Binder

## What this Skill does
Transforms standards-core outputs (`coverage.json`, `evidence.jsonl`, `pages.jsonl`) into a polished, reviewer-ready document:
- **Markdown binder** — hierarchical standards + evidence with page anchors and quoted spans.
- **PDF export** — formatted, multi-page report with bookmarks and page numbers.
- **DOCX export** — editable Word document for reviewer markup and collaboration.

Perfect for EdReports-style curriculum reviews and evidence-based alignment audits.

## How to run
1. Receive inputs from standards-core skill (or user provides paths).
2. Read `coverage.json`, `evidence.jsonl`, `pages.jsonl`.
3. Template-render the evidence into Markdown.
4. Convert Markdown → PDF via `pandoc` or `weasyprint` (optional).
5. Convert Markdown → DOCX via `pandoc` (optional).
6. Write outputs to `binder/` directory.

## Inputs (ask user or read from CLI)
- coverage_json: path to `outputs/coverage.json`
- evidence_jsonl: path to `outputs/evidence.jsonl`
- pages_jsonl: path to `outputs/pages.jsonl`
- title: e.g., "Grade 3 Math Textbook Alignment Review"
- subject: math|ela
- format: markdown|pdf|docx|all
- out_dir: binder/

## Deterministic rendering
- Use Jinja2 or Handlebars template for Markdown layout.
- Organize by standard → pages → quotes.
- Include page anchors (e.g., `math_grade3:12:45:92`) for traceability.
- Bold or highlight uncovered standards.

## Scripts to call
- `scripts/render_binder.py --coverage outputs/coverage.json --evidence outputs/evidence.jsonl --pages outputs/pages.jsonl --format {markdown|pdf|docx|all} --out binder`

## Output structure
```
binder/
├── alignment_report.md
├── alignment_report.pdf
├── alignment_report.docx
├── index.html (optional, for web preview)
└── evidence_log.jsonl (audit trail)
```

## Markdown template structure (templates/binder_base.jinja2)
```markdown
# Curriculum Alignment Review
## {{ title }}

**Subject:** {{ subject }}
**Grades:** {{ grades }}
**Books:** {{ books | join(', ') }}
**Review Date:** {{ date }}

---

## Executive Summary
- **Total Standards:** {{ total_standards }}
- **Covered:** {{ total_covered }} ({{ coverage_percent }}%)
- **Uncovered:** {{ total_uncovered }}
- **Off-Grade Content:** {{ off_grade_percent }}%

---

## Standards Coverage by Grade

{% for grade_group in standards | groupby('grade') %}
### Grade {{ grade_group.key }}

{% for standard in grade_group.list %}
#### {{ standard.id }} — {{ standard.description }}

**Status:** {% if standard.taught %}✓ Taught{% else %}✗ Not Taught{% endif %} |
**Practiced:** {% if standard.practiced %}✓{% else %}✗{% endif %} |
**Assessed:** {% if standard.assessed %}✓{% else %}✗{% endif %}

**Intensity:** {{ standard.intensity }}
**Evidence:** {{ standard.evidence_found | ternary('Found', 'NOT FOUND') }}

{% if standard.evidence_found %}
**Key Pages:** {{ standard.top_pages | join(', ') }}

**Top Evidence:**
> {{ standard.top_hit.quote }}
>
> — *{{ standard.top_hit.book_id }}, Page {{ standard.top_hit.page }}* [`{{ standard.top_hit.anchor }}`]

**Context:** {{ standard.top_hit.context }}

{% if standard.redundancy_count > 1 %}
**Note:** This standard appears {{ standard.redundancy_count }} times across the textbook.
{% endif %}

{% else %}
⚠️ **NO EVIDENCE FOUND** — This standard may not be adequately covered in the textbook.
{% endif %}

---

{% endfor %}
{% endfor %}

## Uncovered Standards

The following standards lack evidence in the provided materials:

{% for standard in standards | selectattr('evidence_found', 'false') %}
- **{{ standard.id }}** (Grade {{ standard.grade }})
{% endfor %}

---

## Methodology Notes

This alignment review was conducted using automated standards-mapping software with manual verification of boundary cases. All evidence references include page anchors (`book_id:page:start:end`) for direct verification.

**Standards Pack:** {{ standards_pack_version }}
**Generated:** {{ generation_timestamp }}
```

## Example output snapshot (Markdown)

```markdown
# Curriculum Alignment Review
## Grade 3 Math Textbook

**Subject:** Math
**Grades:** 3
**Books:** math_grade3.pdf
**Review Date:** 2025-10-17

---

## Executive Summary
- **Total Standards:** 15
- **Covered:** 12 (80%)
- **Uncovered:** 3
- **Off-Grade Content:** 2%

---

## Standards Coverage by Grade

### Grade 3

#### 3.NF.A.1 — Understand a fraction 1/b as the quantity formed by 1 part when a whole is partitioned into b equal parts

**Status:** ✓ Taught | **Practiced:** ✓ | **Assessed:** ✗

**Intensity:** High
**Evidence:** Found

**Key Pages:** 12, 15, 18

**Top Evidence:**
> A fraction is an equal part of a whole. When we divide a shape into equal parts, each part is one fraction of the whole.
>
> — *math_grade3, Page 12* [`math_grade3:12:45:92`]

**Context:** Instruction section on Understanding Fractions

**Note:** This standard appears 2 times across the textbook.

---

#### 3.NF.A.2 — Understand a fraction as a number on the number line; represent fractions on a number line diagram

**Status:** ✓ Taught | **Practiced:** ✓ | **Assessed:** ✗

**Intensity:** Medium
**Evidence:** Found

**Key Pages:** 20

**Top Evidence:**
> On a number line, locate 1/2, 1/3, and 1/4 by marking equal intervals.
>
> — *math_grade3, Page 20* [`math_grade3:20:120:165`]

**Context:** Practice worksheet

---

#### 3.OA.A.1 — Interpret products of whole numbers

**Status:** ✗ Taught | **Practiced:** ✗ | **Assessed:** ✗

**Intensity:** None
**Evidence:** NOT FOUND

⚠️ **NO EVIDENCE FOUND** — This standard may not be adequately covered in the textbook.
```

## Export options

### PDF (via pandoc + weasyprint)
```bash
pandoc alignment_report.md -o alignment_report.pdf \
  --pdf-engine=weasyprint \
  -V colorlinks \
  --toc
```

### DOCX (via pandoc)
```bash
pandoc alignment_report.md -o alignment_report.docx \
  --toc \
  --reference-doc templates/reference.docx
```

## Workflow example
```bash
# Generate Markdown binder from standards-core outputs
scripts/render_binder.py \
  --coverage outputs/coverage.json \
  --evidence outputs/evidence.jsonl \
  --pages outputs/pages.jsonl \
  --title "Grade 3 Math Alignment Review" \
  --format all \
  --out binder

# Review generated files
ls -lah binder/
cat binder/alignment_report.md
```

## Error handling
- If coverage.json is missing, halt with descriptive error.
- If evidence.jsonl is empty, generate a binder noting "No evidence compiled."
- Gracefully handle missing optional fields (e.g., `redundancy_count`).
- If pandoc is not available, offer Markdown-only mode and warn user.

## Accessibility & reproducibility
- Include generation timestamp and standards pack version in binder footer.
- All quotes include full page anchors for verification by independent reviewers.
- Binder is self-contained; can be shared as standalone PDF or DOCX.
