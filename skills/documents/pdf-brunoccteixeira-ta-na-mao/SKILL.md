---
name: pdf
description: Processar PDFs (laudos, comprovantes)
---

Utiliza o MCP `pdf-ocr` configurado em `.mcp.json` para extrair texto de PDFs.

## Extrair Texto de PDF

### PDF Local
```
mcp__pdf-ocr__extract_text file_path="/caminho/para/arquivo.pdf"
```

### PDF com OCR (imagens/escaneados)
```
mcp__pdf-ocr__extract_text_ocr file_path="/caminho/para/arquivo.pdf"
```

## Casos de Uso no Tá na Mão

### 1. Laudo Médico (BPC)
```
# Extrair texto do laudo
mcp__pdf-ocr__extract_text_ocr file_path="/tmp/laudo_medico.pdf"

# Analisar para verificar CID e informações
```

### 2. Comprovante de Residência
```
mcp__pdf-ocr__extract_text file_path="/tmp/comprovante.pdf"

# Buscar endereço e CEP no texto extraído
```

### 3. Extrato de Benefício
```
mcp__pdf-ocr__extract_text file_path="/tmp/extrato_bf.pdf"

# Analisar valores e datas
```

### 4. Documento do CRAS
```
mcp__pdf-ocr__extract_text file_path="/tmp/parecer_cras.pdf"
```

## Workflow Completo

```
1. Receber PDF do usuário (upload ou path)
2. Extrair texto com MCP
3. Analisar conteúdo relevante
4. Retornar informações em linguagem simples
```

## Dicas

- **PDFs digitais**: Use `extract_text` (mais rápido)
- **PDFs escaneados**: Use `extract_text_ocr` (mais lento, mas funciona com imagens)
- **PDFs protegidos**: Podem não funcionar

## Informações a Extrair por Tipo

| Documento | Informações Relevantes |
|-----------|----------------------|
| Laudo médico | CID, descrição, médico, data |
| Comprovante residência | Endereço, CEP, nome titular |
| Extrato benefício | Valor, parcela, data pagamento |
| Carteira trabalho | Nome, PIS, admissão/demissão |
| RG/CPF | Número, nome, data nascimento |

## Segurança

- Não armazenar PDFs com dados sensíveis
- Deletar arquivos temporários após processamento
- Mascarar CPF em logs: `***{cpf[-4:]}`
