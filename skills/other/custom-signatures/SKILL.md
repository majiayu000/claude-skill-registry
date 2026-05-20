---
name: custom-signatures
description: Create and deploy custom IOCs, YARA rules, Sigma rules, and STIX indicators for THOR scans.
---

# Custom Signatures Skill

Goal: Help users create, format, and deploy custom detection content for THOR.

## Overview

THOR processes all files in the `./custom-signatures` folder. The file extension and filename tags determine how each file is interpreted:

| Extension | Type | Description |
|-----------|------|-------------|
| `.txt` | Simple IOCs | CSV-style IOC files (hashes, filenames, C2s, etc.) |
| `.dat` | Encrypted IOCs | Encrypted simple IOCs (via thor-util) |
| `.yar` | YARA rules | Plain text YARA rules |
| `.yas` | Encrypted YARA | Encrypted YARA rules |
| `.yml` | Sigma rules | Log detection rules |
| `.yms` | Encrypted Sigma | Encrypted Sigma rules |
| `.json` | STIX v2 | STIXv2 JSON indicators |
| `.jsos` | Encrypted STIX | Encrypted STIX indicators |

## Simple IOCs

Filename tags determine IOC type. Tag is detected via regex `\Wc2\W` (word boundary match).

| Tag in Filename | Purpose | Example Filename |
|-----------------|---------|------------------|
| `c2` or `domains` | IPs, hostnames, CIDR ranges | `case22-c2-iocs.txt` |
| `filename` or `filenames` | Regex-based path/name IOCs | `apt-filename-iocs.txt` |
| `hash` or `hashes` | MD5, SHA1, SHA256, Imphash | `misp-hashes.txt` |
| `keyword` or `keywords` | String-based keywords | `incident-keywords.txt` |
| `trusted-hash` | Whitelist hashes (reduce score) | `my-trusted-hashes.txt` |
| `handles` | Mutex/Event values | `malware-handles.txt` |
| `pipes` | Named pipes | `c2-pipes.txt` |

## Rules

### YARA Rules

**Critical:** The filename determines how THOR initializes the rule. See [YARA Rules Reference](reference/yara-rules.md#yara-rule-types) for full details.

| Filename Contains | Rule Type | Applied To |
|-------------------|-----------|------------|
| (none), `process` | Generic rules | Files, process memory, DeepDive chunks |
| `meta` | Meta rules | All files (first 64KB + externals) |
| `keyword` | Keyword rules | THOR module output (tasks, services, etc.) |
| `registry` | Registry rules | Registry keys/values |
| `log` | Log rules | Log lines, event log entries |

**Common mistake:** Using `limit = "ScheduledTasks"` without `keyword` in the filename. This causes the rule to be initialized as a **generic rule** (file/memory scanner), which won't match module output like scheduled task names.

### Sigma Rules

Applied to Windows Eventlogs and log files. By default only `high` and `critical` levels shown.

### STIX v2

Supports file observables (name, path, hashes, size, timestamps) and registry key observables.

## THOR-Specific YARA Enhancements

### Score Attribute

```yara
meta:
    score = 80  // Default is 75 if not specified
```

### External Variables

Available in generic and meta YARA rules:

| Variable | Description | Example |
|----------|-------------|---------|
| `filename` | File name only | `cmd.exe` |
| `filepath` | Path without filename | `C:\temp` |
| `extension` | Extension with dot, lowercase | `.exe` |
| `filetype` | Magic header type | `EXE`, `ZIP`, `PDF` |
| `filesize` | Size in bytes | (YARA built-in) |
| `owner` | File owner | `NT-AUTHORITY\SYSTEM` |
| `filemode` | POSIX-style file mode | |
| `unpack_parent` | Immediate container | `ZIP` |
| `unpack_source` | Full unpack chain | `EMAIL>ZIP` |

### Restriction Attributes

```yara
meta:
    type = "memory"      // or "file" - restrict to memory/file only
    limit = "Mutex"      // Restrict to specific module
    nodeepdive = 1       // Exclude from DeepDive
    falsepositive = 1    // Reduce score instead of add
```

## Reference Documentation

- [Simple IOCs](reference/simple-iocs.md) - Hash, filename, C2, keyword IOC formats
- [YARA Rules](reference/yara-rules.md) - Generic and specific YARA rules for THOR
- [Sigma Rules](reference/sigma-rules.md) - Log detection with Sigma
- [STIX IOCs](reference/stix-iocs.md) - STIX v2 indicator format

## Examples

- [examples/hash-iocs.md](examples/hash-iocs.md) - Hash IOC file examples
- [examples/filename-iocs.md](examples/filename-iocs.md) - Filename/path IOC patterns
- [examples/yara-enhanced.md](examples/yara-enhanced.md) - YARA rules with THOR externals

## Quick Reference

### File Naming

```
# Good - tag detected
case22-c2-domains.txt       ✓ (c2 tag)
misp-export-hashes.txt      ✓ (hashes tag)
incident-filename-iocs.txt  ✓ (filename tag)

# Bad - tag not detected
myc2iocs.txt                ✗ (no word boundary)
filenameiocs.txt            ✗ (no word boundary)
```

### Deployment

```bash
# Place files in custom-signatures folder
cp my-hashes.txt /path/to/thor/custom-signatures/

# For YARA rules, use yara subfolder
cp my-rules.yar /path/to/thor/custom-signatures/yara/

# Encrypt sensitive IOCs (optional)
thor-util encrypt --file my-c2-domains.txt
# Creates my-c2-domains.dat
```

### Testing

```bash
# Run with custom signatures only
./thor-macosx --customonly -p /target/path

# Verify IOC loading in startup
./thor-macosx 2>&1 | grep -i "custom\|ioc\|signature"
```
