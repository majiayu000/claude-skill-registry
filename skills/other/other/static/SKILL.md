---
name: static
description: Binary reverse engineering - PE/ELF analysis, Ghidra, capability detection
---

# Static Malware Analysis

Analyze binaries without execution:
- File triage (type, packer, entropy)
- String analysis (FLOSS)
- PE/ELF structure analysis
- Import/export analysis
- Ghidra reverse engineering
- Capability detection (capa)
- IOC extraction

## Required Context
1. **Sample**: File path
2. **Depth**: Quick triage or full analysis
3. **Focus**: Persistence, C2, credentials, etc.
4. **Output**: Report, IOCs, YARA rule

## Tools Used
Ghidra, radare2, strings, floss, capa, binwalk, objdump, readelf

## Example
```
/static
Sample: /samples/malware.exe
Depth: Full analysis
Output: IOCs + YARA rule
```
