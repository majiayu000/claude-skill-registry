# Code Skill Template

스크립트를 포함하는 스킬용

---

## 디렉토리 구조

```
my-code-skill/
├── SKILL.md
├── reference.md
└── scripts/
    ├── analyze.py
    ├── process.py
    └── validate.py
```

---

## SKILL.md 예시

```markdown
---
name: processing-pdfs
description: "Extracts text from PDFs, fills forms, merges documents. Use when working with PDF files or document extraction."
allowed-tools:
  - Bash
  - Read
  - Write
---

# PDF Processing

## Quick start

Extract text:
```bash
python scripts/extract_text.py input.pdf > output.txt
```

## Workflow

Copy this checklist:
```
Progress:
- [ ] Step 1: Analyze PDF structure
- [ ] Step 2: Extract content
- [ ] Step 3: Validate output
```

### Step 1: Analyze PDF

```bash
python scripts/analyze.py input.pdf
```

Output shows page count, form fields, and structure.

### Step 2: Extract content

```bash
python scripts/extract_text.py input.pdf > output.txt
```

### Step 3: Validate

```bash
python scripts/validate.py output.txt
```

Fix any issues before proceeding.

## Scripts reference

| Script | Purpose |
|--------|---------|
| analyze.py | PDF 구조 분석 |
| extract_text.py | 텍스트 추출 |
| fill_form.py | 폼 필드 채우기 |
| validate.py | 결과 검증 |

For detailed API: See [reference.md](reference.md)

## Dependencies

```bash
pip install pypdf pdfplumber
```
```

---

## scripts/analyze.py 예시

```python
#!/usr/bin/env python3
"""
analyze.py - PDF 구조 분석

Usage:
    python analyze.py input.pdf

Output:
    - Page count
    - Form fields
    - Text/image ratio
"""

import sys
import json
from pypdf import PdfReader

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze.py input.pdf", file=sys.stderr)
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"Error reading PDF: {e}", file=sys.stderr)
        sys.exit(1)
    
    result = {
        "page_count": len(reader.pages),
        "form_fields": [],
        "has_text": False
    }
    
    # Form fields
    if reader.get_form_text_fields():
        result["form_fields"] = list(reader.get_form_text_fields().keys())
    
    # Check for text
    for page in reader.pages:
        if page.extract_text().strip():
            result["has_text"] = True
            break
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
```

---

## 핵심 포인트

1. **워크플로우 체크리스트**: 진행 추적
2. **피드백 루프**: 검증 → 수정 → 재검증
3. **스크립트 문서화**: Usage, Output 명시
4. **에러 직접 처리**: Claude에 떠넘기지 않기
5. **의존성 명시**: pip install 명령 포함
