---
name: document-conversion
description: 将 DOC/DOCX/PDF/PPT/PPTX 文档转换为 Markdown 格式。自动检测 PDF 类型（电子版/扫描版），提取图片到独立目录。当管理员入库非
  Markdown 文档时使用此 Skill。触发条件：入库 DOC/DOCX/PDF/PPT/PPTX 格式文件。
---

---
name: document-conversion
description: Convert DOC/DOCX/PDF/PPT/PPTX documents to Markdown format. Automatically detect PDF type (electronic/scanned), extract images to separate directory. Use this Skill when administrator onboards non-Markdown documents. Trigger condition: Onboard DOC/DOCX/PDF/PPT/PPTX format files.
---

# Document Format Conversion

Convert various document formats to Markdown for knowledge base onboarding.

## Supported Formats

| Format | Processing Method |
|--------|------------------|
| DOCX | Pandoc conversion, preserve formatting and images |
| DOC | LibreOffice → DOCX → Pandoc |
| PDF Electronic | PyMuPDF4LLM fast conversion |
| PDF Scanned | PaddleOCR-VL online OCR |
| PPTX | pptx2md professional conversion |
| PPT | LibreOffice → PPTX → pptx2md |

## Usage

```bash
python .claude/skills/document-conversion/scripts/smart_convert.py \
    <temp_path> \
    --original-name "<original_filename>" \
    --json-output
```

**Parameters**:
- `<temp_path>`: Temporary file path (e.g. `/tmp/kb_upload_xxx.pptx`)
- `--original-name`: **Must pass original filename**, used to generate correct image directory name
- `--json-output`: Output JSON format result

## Output Format

```json
{
  "success": true,
  "markdown_file": "/path/to/output.md",
  "images_dir": "original_filename_images",
  "image_count": 5,
  "input_file": "/path/to/input.pptx"
}
```

## Processing Flow

1. Execute conversion command (must use `--original-name` and `--json-output`)
2. Parse JSON output, check `success` field
3. If `success: false`, report error and end
4. If `success: true`, record generated file path and image directory

## Important Notes

- Image directory uses original filename naming (e.g. `培训资料_images/`)
- Not passing `--original-name` will cause incorrect image reference paths
- PDF type is automatically detected, scanned version processing is slower (tens of seconds to minutes)

## Format Details

Detailed processing instructions for each format, see [FORMATS.md](FORMATS.md)
