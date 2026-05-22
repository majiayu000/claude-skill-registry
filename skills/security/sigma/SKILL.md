---
name: sigma
description: Create Sigma detection rules for SIEM log-based detection
---

# Sigma Rule Creation

Create SIEM-agnostic detection rules:
- Process execution patterns
- Registry modifications
- Network connections
- Authentication events
- File operations

## Required Context
1. **Pattern**: What to detect (TTP, behavior, IOC)
2. **Log Source**: Sysmon, Security, EDR, etc.
3. **Context**: False positive considerations

## Output
- Sigma YAML rule
- SIEM conversion commands (Splunk, Elastic, Sentinel)

## Sigma Conversion
```bash
sigma convert -t splunk rule.yml
sigma convert -t elasticsearch rule.yml
sigma convert -t azure-sentinel rule.yml
```

## Example
```
/sigma
Pattern: Office spawning PowerShell with encoded commands
Source: Sysmon Event 1
```
