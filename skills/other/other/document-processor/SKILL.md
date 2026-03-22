---
name: document-processor
description: |
  Processa documentos empresariais (PDF, XLSX, DOCX) para extracao de requisitos,
  validacao de dados e criacao de documentos profissionais.
  Use quando: extrair texto de PDF, processar planilhas Excel, criar/editar Word,
  validar documentos, converter formatos.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
user-invocable: true
---

# Document Processor Skill

## Proposito

Processa documentos empresariais com qualidade production-grade:
- **PDF**: Extracao de texto/tabelas, OCR para escaneados, merge, split
- **XLSX**: Leitura de dados, validacao de formulas, criacao de relatorios
- **DOCX**: Extracao de texto, tracked changes, criacao profissional

## Principios de Design

### 1. Validation-First
Sempre validar ANTES de processar. Coletar TODOS os erros antes de reportar.

### 2. Multi-Tool Strategy
- **Extracao**: Python (pdfplumber, openpyxl, python-docx)
- **Validacao**: CLI (LibreOffice headless, pdftotext)
- **OCR**: tesseract-ocr

### 3. Zero-Error Policy
Planilhas e documentos criados devem ter ZERO erros de formula ou formatacao.

## Comandos

### /doc-extract {arquivo}

Extrai texto e dados de um documento.

```bash
/doc-extract requirements.pdf
/doc-extract financials.xlsx
/doc-extract spec.docx
```

**Output**: Texto estruturado, tabelas em formato markdown, metadados.

### /doc-validate {arquivo}

Valida integridade do documento.

```bash
/doc-validate report.xlsx  # Verifica formulas
/doc-validate contract.docx  # Verifica formatacao
```

**Output**: JSON com status e erros encontrados.

### /doc-create {tipo} {nome}

Cria documento profissional a partir de template.

```bash
/doc-create xlsx requirement-matrix
/doc-create docx technical-spec
```

**Tipos suportados**:
- `xlsx`: Planilha com formatacao profissional
- `docx`: Documento Word com estilos padrao

## Workflow de Extracao

### PDF

```python
# 1. Detectar tipo (texto vs escaneado)
# 2. Extrair com pdfplumber (texto) ou OCR (escaneado)
# 3. Preservar layout e tabelas
# 4. Retornar estruturado

python scripts/extract_pdf.py input.pdf --output json
```

### XLSX

```python
# 1. Abrir com openpyxl
# 2. Iterar sheets e celulas
# 3. Preservar formulas como metadata
# 4. Validar com LibreOffice headless

python scripts/process_xlsx.py input.xlsx --mode extract
python scripts/process_xlsx.py input.xlsx --mode validate
```

### DOCX

```python
# 1. Abrir com python-docx
# 2. Extrair paragrafos, tabelas, headers
# 3. Detectar tracked changes (OOXML)
# 4. Preservar estrutura

python scripts/process_docx.py input.docx --mode extract
```

## Validacao de Planilhas

### Tipos de Erros Detectados

| Codigo | Descricao | Exemplo |
|--------|-----------|---------|
| `#VALUE!` | Tipo incompativel | `=A1+B1` onde B1 e texto |
| `#REF!` | Referencia invalida | Celula deletada referenciada |
| `#DIV/0!` | Divisao por zero | `=A1/0` |
| `#NAME?` | Nome desconhecido | Funcao inexistente |
| `#N/A` | Valor nao disponivel | VLOOKUP sem match |
| `#NUM!` | Numero invalido | `=SQRT(-1)` |
| `#NULL!` | Intersecao nula | Range invalido |

### Output de Validacao

```json
{
  "status": "errors_found",
  "total_errors": 3,
  "errors": [
    {"cell": "B5", "type": "#REF!", "formula": "=A1+Sheet2!Z99"},
    {"cell": "C10", "type": "#DIV/0!", "formula": "=A10/B10"},
    {"cell": "D15", "type": "#VALUE!", "formula": "=SUM(D1:D14)"}
  ],
  "suggestions": [
    "B5: Verifique se Sheet2!Z99 existe",
    "C10: B10 esta vazio ou zero",
    "D15: Range contem valores nao-numericos"
  ]
}
```

## Tracked Changes (DOCX)

### Detectar Alteracoes

```python
# Tracked changes estao em tags OOXML:
# <w:ins> = insercao
# <w:del> = delecao
# <w:rPrChange> = mudanca de formatacao

python scripts/process_docx.py contract.docx --mode changes
```

### Output

```json
{
  "has_tracked_changes": true,
  "changes": [
    {
      "type": "insertion",
      "author": "John Doe",
      "date": "2026-01-10T14:30:00Z",
      "text": "novo texto inserido"
    },
    {
      "type": "deletion",
      "author": "Jane Smith",
      "date": "2026-01-11T09:15:00Z",
      "text": "texto removido"
    }
  ]
}
```

## Dependencias

### Obrigatorias (Python)

```bash
pip install pdfplumber openpyxl python-docx pandas
```

### Opcionais (Sistema)

```bash
# PDF avancado
apt install poppler-utils

# OCR para PDFs escaneados
apt install tesseract-ocr

# Validacao de formulas XLSX
apt install libreoffice
```

### Verificar Instalacao

```bash
python scripts/validate.py --check-deps
```

## Integracao com SDLC

| Fase | Uso |
|------|-----|
| **Phase 1 (Discovery)** | Extrair requisitos de PDFs de stakeholders |
| **Phase 2 (Requirements)** | Processar matrizes de requisitos (XLSX) |
| **Phase 3 (Architecture)** | Ler especificacoes tecnicas (DOCX) |
| **Phase 7 (Release)** | Gerar release notes (DOCX), reports (XLSX) |

## Boas Praticas

1. **Sempre validar antes de processar** - Use `/doc-validate` primeiro
2. **Preferir extracao estruturada** - Tabelas como arrays, nao texto
3. **Preservar metadados** - Autor, data, versao
4. **Reportar todos os erros** - Nao falhar no primeiro erro
5. **Usar templates padronizados** - Para documentos criados

## Troubleshooting

### PDF nao extrai texto

```bash
# Verificar se e escaneado
pdftotext input.pdf - | head -20

# Se vazio, usar OCR
python scripts/extract_pdf.py input.pdf --ocr
```

### XLSX com formulas quebradas

```bash
# Validar formulas
python scripts/process_xlsx.py input.xlsx --mode validate

# Listar todas as formulas
python scripts/process_xlsx.py input.xlsx --mode formulas
```

### DOCX corrompido

```bash
# Tentar reparar via LibreOffice
libreoffice --headless --convert-to docx input.docx
```

## Referencias

- [pdfplumber documentation](https://github.com/jsvine/pdfplumber)
- [openpyxl documentation](https://openpyxl.readthedocs.io/)
- [python-docx documentation](https://python-docx.readthedocs.io/)
- [OOXML Spec](https://docs.microsoft.com/en-us/openspecs/office_standards)
