---
name: reference-indexer
description: |
  Indexa documentos de referencia para uso no RAG.
  Extrai texto de PDFs, processa e adiciona ao corpus.
  Use quando: adicionar documento, buscar referencia, listar docs.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
user-invocable: true
---

# Reference Indexer Skill

## Proposito

Esta skill gerencia documentos de referencia externa, indexando-os para uso no RAG.

## Comandos

### /ref-add {path}

Adiciona documento ao indice de referencias:

```bash
/ref-add .project/references/legal/lei-13775-2018.pdf
```

Acoes:
1. Valida o arquivo
2. Extrai texto (se PDF/Word)
3. Cria resumo automatico
4. Adiciona ao corpus RAG
5. Atualiza indice

### /ref-search {query}

Busca nos documentos de referencia:

```bash
/ref-search "prazo de aceite duplicata"
```

Retorna:
- Documentos relevantes
- Trechos com contexto
- Score de relevancia

### /ref-list

Lista todos os documentos indexados:

```bash
/ref-list
```

Mostra:
- Documentos por categoria
- Status de indexacao
- Data de adicao

### /ref-remove {path}

Remove documento do indice:

```bash
/ref-remove .project/references/legal/documento-antigo.pdf
```

## Formatos Suportados

| Formato | Extensao | Metodo de Extracao |
|---------|----------|-------------------|
| PDF | .pdf | pdftotext / PyPDF2 |
| Word | .docx | python-docx |
| Markdown | .md | Direto |
| Texto | .txt | Direto |
| HTML | .html | BeautifulSoup |

## Estrutura de Referencias

```
.project/references/
├── legal/              # Leis, regulamentos, normas
├── technical/          # RFCs, especificacoes tecnicas
├── business/           # Regras de negocio, manuais
├── internal/           # Documentos internos
└── _index.yml          # Indice de documentos
```

## Indice de Documentos

Arquivo `_index.yml`:

```yaml
index:
  version: 1
  updated_at: "2026-01-12T..."

documents:
  - id: "ref-001"
    path: "legal/lei-13775-2018.pdf"
    title: "Lei 13.775/2018 - Duplicatas Eletrônicas"
    category: legal
    added_at: "2026-01-12T..."
    indexed: true
    summary: "Lei que regulamenta as duplicatas escriturais..."
    keywords:
      - duplicata
      - escritural
      - eletronica
    page_count: 5

  - id: "ref-002"
    path: "technical/icp-brasil.pdf"
    title: "Padrões ICP-Brasil"
    category: technical
    added_at: "2026-01-12T..."
    indexed: true
```

## Extracao de Texto

### PDF

```bash
# Usando pdftotext (poppler-utils)
pdftotext -layout input.pdf output.txt

# Usando Python
python3 << 'EOF'
import PyPDF2

with open('input.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    print(text)
EOF
```

### Word (docx)

```python
from docx import Document

doc = Document('input.docx')
text = '\n'.join([p.text for p in doc.paragraphs])
print(text)
```

## Integracao com RAG

Documentos indexados sao adicionados ao corpus RAG:

```yaml
corpus_entry:
  id: "ref-001"
  source: "references/legal/lei-13775-2018.pdf"
  type: "reference"
  category: "legal"
  content: "{texto extraido}"
  embeddings: [...]  # Gerado pelo RAG
  metadata:
    title: "Lei 13.775/2018"
    page: 1
    section: "Art. 1"
```

## Workflow de Indexacao

```yaml
indexing_workflow:
  1_validate:
    - Verificar formato suportado
    - Verificar tamanho (max 50MB)
    - Verificar permissoes

  2_extract:
    - Extrair texto do documento
    - Limpar formatacao
    - Dividir em chunks

  3_analyze:
    - Gerar resumo automatico
    - Extrair keywords
    - Classificar categoria

  4_index:
    - Adicionar ao corpus RAG
    - Gerar embeddings
    - Atualizar indice

  5_verify:
    - Testar busca
    - Verificar qualidade
```

## Configuracao

No `settings.json`:

```json
{
  "memory": {
    "rag_corpus": ".project/corpus",
    "max_document_size_mb": 50,
    "chunk_size": 1000,
    "chunk_overlap": 200
  }
}
```

## Boas Praticas

1. **Nomeie arquivos descritivamente**: `lei-13775-2018-duplicatas.pdf`
2. **Organize por categoria**: legal, technical, business
3. **Mantenha versoes**: Nao sobrescreva, versione
4. **Documente a fonte**: Adicione de onde veio
5. **Resuma docs longos**: Crie resumos para PDFs grandes

## Troubleshooting

### PDF nao extrai texto

Alguns PDFs sao imagens escaneadas. Use OCR:

```bash
ocrmypdf input.pdf output.pdf
pdftotext output.pdf -
```

### Documento muito grande

Divida em partes menores ou aumente `max_document_size_mb`.

### Encoding incorreto

Force UTF-8 na extracao:

```bash
pdftotext -enc UTF-8 input.pdf output.txt
```
