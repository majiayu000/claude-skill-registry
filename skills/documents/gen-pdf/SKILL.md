---
name: gen-pdf
description: Converts a Markdown file to a styled PDF with DevExpert branding (logo in bottom-right corner). Use when asked to generate a PDF from a Markdown document, or when any DevExpert proposal/document needs to be exported as PDF.
---

# gen-pdf — Generador de PDFs con estilo Obsidian + DevExpert

Convierte cualquier fichero Markdown a PDF con un acabado visual cercano al export de Obsidian (tipografía y jerarquía neutras) y mantiene el logo de DevExpert en la esquina inferior derecha.

## Cuándo usar esta skill

- El usuario pide generar un PDF a partir de un fichero `.md`
- Se acaba de crear o actualizar un documento/propuesta y hay que exportarlo
- El usuario pide añadir el logo de DevExpert a un PDF existente

## Dependencias

```bash
pip install markdown-it-py[plugins] weasyprint reportlab PyPDF2
```

## Rutas clave

- **Logo DevExpert:** `assets/devexpert-logo.png` (relativo a la carpeta de la skill)
- **Output por defecto:** `~/Documents/aipal/40-archive/`

## Script de generación

Usa el siguiente script Python. Acepta `input_md` y `output_pdf` como variables:

```python
import os
import tempfile
from pathlib import Path

from markdown_it import MarkdownIt
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from weasyprint import CSS, HTML

md = MarkdownIt("commonmark", {"breaks": True, "html": True}).enable("table")

CSS_STYLES = """
@page {
  size: A4;
  margin: 30mm 24mm 26mm 24mm;
}

html, body {
  margin: 0;
  padding: 0;
  color: #111111;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Helvetica, Arial, sans-serif;
  font-size: 12pt;
  line-height: 1.46;
}

p {
  margin: 0 0 0.82em 0;
}

h1, h2, h3, h4 {
  color: #111111;
  font-weight: 800;
  line-height: 1.12;
  margin: 0;
}

h1 {
  font-size: 24pt;
  margin-bottom: 0.9em;
}

h2 {
  font-size: 20pt;
  margin-top: 1.1em;
  margin-bottom: 0.74em;
}

h3 {
  font-size: 16pt;
  margin-top: 0.95em;
  margin-bottom: 0.58em;
}

h4 {
  font-size: 13pt;
  margin-top: 0.8em;
  margin-bottom: 0.4em;
}

strong {
  color: #111111;
  font-weight: 800;
}

ul, ol {
  margin: 0.35em 0 0.9em 1.28em;
  padding: 0;
}

li {
  margin-bottom: 0.24em;
}

li::marker {
  color: #a0a0a0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.9em 0 1.1em 0;
  font-size: 10.5pt;
}

th, td {
  border: 1px solid #d4d4d4;
  padding: 7px 10px;
  text-align: left;
  vertical-align: top;
}

th {
  background: #f3f3f3;
  color: #111111;
  font-weight: 700;
}

tr:nth-child(even) td {
  background: #fafafa;
}

blockquote {
  border-left: 3px solid #d0d0d0;
  padding-left: 12px;
  color: #303030;
  margin: 0.8em 0;
}

code {
  font-family: "SF Mono", "SFMono-Regular", Menlo, Consolas, "Liberation Mono", monospace;
  font-size: 0.9em;
  background: #f5f5f5;
  padding: 0.08em 0.28em;
  border-radius: 4px;
}

pre code {
  display: block;
  white-space: pre-wrap;
  padding: 0.8em;
}

a {
  color: #111111;
  text-decoration: underline;
  text-decoration-color: #c1c1c1;
}

hr {
  border: 0;
  height: 0;
  margin: 0;
  padding: 0;
  background: transparent;
  page-break-after: always;
  break-after: page;
}
"""


def resolve_logo_path(explicit_logo_path=None):
    if explicit_logo_path:
        explicit_path = Path(explicit_logo_path).expanduser()
        if explicit_path.exists():
            return explicit_path

    candidates = []
    env_logo = os.getenv("GEN_PDF_LOGO_PATH")
    if env_logo:
        candidates.append(Path(env_logo).expanduser())

    skill_dir = os.getenv("GEN_PDF_SKILL_DIR")
    if skill_dir:
        candidates.append(Path(skill_dir).expanduser() / "assets" / "devexpert-logo.png")

    candidates.extend(
        [
            Path.cwd() / "assets" / "devexpert-logo.png",
            Path.home() / ".claude" / "skills" / "gen-pdf" / "assets" / "devexpert-logo.png",
        ]
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def gen_pdf(input_md, output_pdf, add_logo=True, logo_path=None):
    input_md_path = Path(input_md).expanduser()
    output_pdf_path = Path(output_pdf).expanduser()
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    content = input_md_path.read_text(encoding="utf-8")
    html_content = md.render(content)
    full_html = f"""<!doctype html>
<html>
  <head><meta charset="utf-8" /></head>
  <body>{html_content}</body>
</html>"""

    HTML(string=full_html, base_url=str(input_md_path.parent)).write_pdf(
        str(output_pdf_path), stylesheets=[CSS(string=CSS_STYLES)]
    )

    if not add_logo:
        return

    resolved_logo = resolve_logo_path(logo_path)
    if not resolved_logo:
        return

    reader = PdfReader(str(output_pdf_path))
    writer = PdfWriter()

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_logo_pdf = temp_file.name

    page_width, _ = A4
    canvas_obj = canvas.Canvas(temp_logo_pdf, pagesize=A4)
    canvas_obj.drawImage(
        str(resolved_logo),
        page_width - 128,
        14,
        width=110,
        height=27,
        mask="auto",
        preserveAspectRatio=True,
    )
    canvas_obj.showPage()
    canvas_obj.save()

    logo_overlay_page = PdfReader(temp_logo_pdf).pages[0]
    for page in reader.pages:
        page.merge_page(logo_overlay_page)
        writer.add_page(page)

    with output_pdf_path.open("wb") as output_file:
        writer.write(output_file)

    os.unlink(temp_logo_pdf)
```

## Instrucciones de uso

1. Importa o copia la función `gen_pdf` en un script temporal en `/tmp/`
2. Llámala con `input_md` = ruta al fichero Markdown y `output_pdf` = ruta de salida
3. Mantén `add_logo=True` para documentos DevExpert
4. Si ejecutas fuera de la carpeta de la skill, define `GEN_PDF_SKILL_DIR` o `GEN_PDF_LOGO_PATH`
5. Tras generar, copia al directorio temporal de Telegram (`$TMPDIR/aipal/documents/`) y responde con `[[document:/ruta]]`

## Notas

- Los `---` en el Markdown fuerzan salto de página en el PDF
- Los saltos de línea simples se respetan (`breaks=True`)
- Las tablas Markdown se renderizan con estilo neutro
- Las imágenes referenciadas en el Markdown se resuelven con `base_url` del fichero de entrada
