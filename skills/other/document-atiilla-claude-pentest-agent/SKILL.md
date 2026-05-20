---
name: document
description: Malicious document analysis - Office macros, PDF JavaScript, RTF exploits
---

# Document Analysis

Analyze malicious documents:
- Office files (macro extraction, OLE objects)
- PDF (JavaScript, embedded files, exploits)
- RTF (OLE objects, exploits)

## Required Context
1. **Document**: File path
2. **Type**: Office, PDF, RTF (auto-detect)

## Output
- Macro/script code (deobfuscated)
- Embedded objects
- IOCs extracted
- MITRE ATT&CK mapping

## Tools Used
olevba, oleobj, pdf-parser, pdfid, rtfobj

## Example
```
/document
File: /samples/invoice.docm
```
