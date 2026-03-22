---
name: memory-forensics
cluster: blue-team
description: "Analyzes volatile memory dumps to detect malware, rootkits, and security breaches in digital forensics."
tags: ["forensics","memory-analysis","security"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "memory forensics analysis security ram dump volatility"
---

# memory-forensics

## Purpose
This skill enables analysis of volatile memory dumps using tools like Volatility to identify malware, rootkits, and security breaches, supporting digital forensics investigations.

## When to Use
Use this skill during incident response for suspected breaches, when analyzing RAM dumps from compromised systems, or for proactive security assessments on endpoints with potential malware infections.

## Key Capabilities
- Parse memory dumps to extract processes, network connections, and injected code using Volatility's plugins.
- Detect hidden processes and rootkits via checks for process hollowing or DKOM (Direct Kernel Object Manipulation).
- Analyze hibernation files or pagefiles for artifacts like command history or encryption keys.
- Support for multiple dump formats, including raw, VMware, and crash dumps, with automated profile detection.

## Usage Patterns
Invoke this skill via CLI commands in a Python script or directly in a terminal. Always specify the memory dump file and required plugins. For automation, wrap commands in a function that handles file paths and outputs. Use environment variables for API keys if extending to cloud-based forensics tools.

Example pattern in Python:
```python
import subprocess
dump_file = 'memory.dmp'
subprocess.run(['volatility', '-f', dump_file, 'pslist'])
```

## Common Commands/API
Use Volatility framework commands for core functionality. Set the VOLATILITY_PROFILE env var for profile mismatches, e.g., `$VOLATILITY_PROFILE=Win7SP1x64`.

- Command: `volatility -f memory.dmp imageinfo` — Identifies the OS profile from the dump.
  - Flags: `-f` for file path, `--profile=Win10x64` to override auto-detection.
- Command: `volatility -f memory.dmp malfind` — Scans for injected code or malware hooks.
  - Example: Pipe output: `volatility -f memory.dmp malfind > malware_output.txt`
- API Endpoint: If using Volatility3 via Python API, import as `from volatility3.framework import interfaces`, then call `interfaces.configuration.ConfObject()` for configurations.
  - Snippet: 
    ```python
    from volatility3 import framework
    config = framework.require_plugin('windows').build_configuration()
    config['primary'] = 'memory.dmp'
    ```
- Config Format: JSON-based, e.g., `{"plugin": "pslist", "dumpfile": "memory.dmp"}` for custom runs.

## Integration Notes
Integrate by installing Volatility via pip (`pip install volatility`), then call from scripts. For authentication in cloud forensics (e.g., AWS Memory DB analysis), use env vars like `$AWS_ACCESS_KEY_ID` and `$AWS_SECRET_ACCESS_KEY`. Ensure the skill runs in a isolated environment to avoid contamination; pass dump files via secure paths. For multi-tool integration, chain with tools like strings or YARA by piping outputs, e.g., `volatility -f memory.dmp strings | grep suspicious`.

## Error Handling
Handle common errors by checking Volatility's exit codes; e.g., if profile not found, use `imageinfo` first. For file not found errors, validate paths before running. In scripts, wrap commands in try-except blocks:
```python
try:
    result = subprocess.run(['volatility', '-f', 'memory.dmp', 'pslist'], capture_output=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e.returncode} - {e.stderr.decode()}")
```
Log detailed errors for debugging, and use `$VOLATILITY_DEBUG=1` env var to enable verbose output.

## Concrete Usage Examples
1. **Detect Malware in a Windows Dump:** Load a memory dump from a suspected infected machine and scan for anomalies.
   - Command: `volatility -f infected.dmp --profile=Win10x64 malfind`
   - Steps: First run `volatility -f infected.dmp imageinfo` to confirm profile, then analyze output for PID and virtual address of suspicious processes.
2. **Investigate Rootkit Presence:** Analyze a Linux memory dump for hidden kernel modules.
   - Command: `volatility -f linux.dmp linux_pslist`
   - Steps: Cross-reference with `linux_modules` to spot discrepancies, then use `strings` on flagged addresses for further inspection.

## Graph Relationships
- Related to: blue-team cluster skills like "incident-response" (depends on outputs) and "threat-intelligence" (provides input data).
- Connected via: tags such as "forensics" and "security", linking to skills like "network-forensics" for comprehensive breach analysis.
