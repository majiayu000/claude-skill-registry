---
name: deobfuscate
description: Script deobfuscation - PowerShell, JavaScript, VBScript, batch
---

# Script Deobfuscation

Decode obfuscated scripts:
- PowerShell (Base64, concatenation, IEX)
- JavaScript (eval, unescape, charcode)
- VBScript (Chr, Execute)
- Batch (variable manipulation, carets)

## Required Context
1. **Script**: File path or paste content
2. **Type**: PowerShell, JavaScript, VBScript, batch (auto-detect)

## Output
- Deobfuscation steps
- Final decoded script
- Functionality analysis
- IOCs extracted

## Example
```
/deobfuscate
Script: powershell -enc SQBFAFgAIAAo...
```
