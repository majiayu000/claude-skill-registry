---
name: yara
description: Create YARA rules for file/memory pattern matching
---

# YARA Rule Creation

Create file-based detection signatures:
- String patterns
- Hex byte patterns
- PE characteristics
- Import analysis
- Entropy checks

## Required Context
1. **Sample**: Malware sample or pattern description
2. **Strings**: Key strings to match
3. **Context**: Malware family, false positive considerations

## Output
- YARA rule with metadata
- Test commands

## Testing
```bash
yara -s rule.yar sample.exe
yara -r rule.yar /samples/
```

## Example
```
/yara
Sample: /samples/cobalt_beacon.exe
Focus: Unique strings, API imports
```
