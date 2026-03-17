---
name: dfir
cluster: blue-team
description: "Perform digital forensics and incident response to detect, analyze, and mitigate cybersecurity incidents."
tags: ["dfir","forensics","incident-response"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "digital forensics incident response blue team cybersecurity investigation mitigation"
---

# dfir

## Purpose
This skill enables the AI to perform digital forensics and incident response (DFIR) tasks, including detecting anomalies, analyzing artifacts, and mitigating threats in cybersecurity incidents. It focuses on tools like Volatility for memory analysis and Autopsy for disk forensics, helping to investigate breaches systematically.

## When to Use
Use this skill during active incidents, such as malware infections or data breaches, when quick analysis is needed. Apply it for proactive threat hunting in blue-team operations or post-incident reviews to gather evidence. Avoid it for routine monitoring; reserve for scenarios requiring deep forensic examination.

## Key Capabilities
- Memory forensics: Parse memory dumps using Volatility to extract processes and network connections.
- Disk analysis: Examine file systems with Autopsy to identify deleted files or timelines.
- Incident response: Automate artifact collection and threat mitigation, e.g., isolating hosts via scripts.
- Malware detection: Scan binaries with YARA rules to match indicators of compromise (IOCs).
- Reporting: Generate timelines and reports from analyzed data for evidence preservation.

## Usage Patterns
Invoke this skill via OpenClaw's Python API by importing the module and calling methods with required parameters. Always specify input files or targets explicitly. For CLI-based tools, wrap them in OpenClaw functions to handle execution. Use asynchronous patterns for long-running tasks, like `await openclaw.dfir.analyze()`. Pass authentication via environment variables, e.g., set `$DFIR_API_KEY` before running.

## Common Commands/API
Use the OpenClaw DFIR API endpoints for integration:
- Endpoint: `/api/dfir/analyze-memory` – Requires POST with JSON body: `{"file_path": "memory.dump", "profile": "Win10x64"}`. Example response: JSON object with processes list.
- Endpoint: `/api/dfir/scan-disk` – POST with `{"device": "/dev/sda1", "rules": ["suspicious.exe"]}`. Authenticate with header: `Authorization: Bearer $DFIR_API_KEY`.

Common CLI commands wrapped in OpenClaw:
- Volatility command: `openclaw.dfir.run_volatility('-f memory.dump --profile=Win10x64 pslist')` – Outputs process list from a dump.
- Autopsy command: `openclaw.dfir.run_autopsy('case_name', '/path/to/evidence')` – Starts a case and adds evidence for analysis.

Code snippets:
```python
import openclaw
result = openclaw.dfir.analyze_memory_dump('memory.dump', profile='Win10x64')
print(result['processes'])  # Returns a list of running processes
```
```python
openclaw.dfir.scan_with_yara('suspicious.bin', rule_file='yara.rules')
# Outputs matches like: [{'rule': 'malware', 'offset': 1024}]
```

Config formats: Use JSON for API requests, e.g., `{"api_key": os.environ.get('DFIR_API_KEY'), "options": {"timeout": 300}}`. For local tools, provide a YAML config file like:
```
tools:
  volatility: /usr/bin/volatility
  autopsy: /opt/autopsy/bin/autopsy
```

## Integration Notes
Integrate this skill with other blue-team tools by chaining API calls, e.g., first use threat-intelligence skill to get IOCs, then pass to `/api/dfir/scan-disk`. Set up environment variables for keys: `export DFIR_API_KEY=your_key_here`. For multi-tool workflows, use OpenClaw's orchestration: `openclaw.workflow.run(['dfir', 'threat-intelligence'])`. Ensure dependencies like Volatility are installed via `pip install volatility3` or system packages. Handle file paths securely to avoid exposure.

## Error Handling
Check for errors in API responses by parsing HTTP status codes (e.g., 401 for auth failures, 404 for missing files). Use try-except blocks in code: 
```python
try:
    openclaw.dfir.analyze_memory_dump('invalid.dump')
except openclaw.DfirError as e:
    print(f"Error: {e.code} - {e.message}")  # e.code might be 'FILE_NOT_FOUND'
```
Log errors with timestamps and retry transient issues (e.g., network errors) up to 3 times using `openclaw.utils.retry()`. Validate inputs before commands, e.g., check if file exists with `os.path.exists()`. If authentication fails, prompt for `$DFIR_API_KEY` and re-authenticate.

## Concrete Usage Examples
1. **Analyze a memory dump for suspicious processes:** Load a memory dump file and identify running processes. Code: 
   ```python
   import openclaw
   processes = openclaw.dfir.analyze_memory_dump('evidence/memory.dump', profile='Linux_x64')
   suspicious = [p for p in processes if 'malware' in p['name']]
   openclaw.dfir.report_findings(suspicious)
   ```
   This detects and logs potential threats, then generates a report for incident response.

2. **Scan a disk for IOCs and mitigate:** Use YARA rules to scan a mounted disk and isolate if threats are found. Code:
   ```python
   import openclaw
   matches = openclaw.dfir.scan_with_yara('/mnt/evidence', rule_file='ioc_rules.yara')
   if matches:
       openclaw.dfir.mitigate_threat('isolate_host', target='192.168.1.5')
   ```
   This automates detection and response, e.g., firewalling the host to prevent spread.

## Graph Relationships
- Related to: threat-intelligence (shares IOC data), security-monitoring (feeds alerts for analysis).
- Depends on: blue-team cluster (for coordinated defense tools).
- Conflicts with: red-team skills (e.g., penetration-testing, as they simulate attacks).
