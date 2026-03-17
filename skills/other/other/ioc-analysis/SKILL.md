---
name: ioc-analysis
cluster: blue-team
description: "Analyzes indicators of compromise (IOCs) to detect and respond to cybersecurity threats."
tags: ["ioc-analysis","threat-detection","blue-team"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "ioc analysis indicators compromise detection security threats"
---

# ioc-analysis

## Purpose
This skill enables the analysis of indicators of compromise (IOCs), such as IP addresses, domains, file hashes, and URLs, to identify potential threats, correlate them with known attack patterns, and generate actionable insights for cybersecurity defense.

## When to Use
- Use during incident response when a suspicious artifact (e.g., an IP from a log) needs immediate verification.
- Apply in proactive threat hunting to scan for IOCs in network traffic or endpoint data.
- Integrate into automated workflows for daily security monitoring of external feeds.

## Key Capabilities
- Parse and enrich IOCs using threat intelligence databases, including IP geolocation, domain reputation, and hash matching.
- Detect anomalies by cross-referencing IOCs against predefined threat feeds or custom rulesets.
- Generate reports with severity scores, related threats, and recommended mitigations.
- Support bulk analysis for processing multiple IOCs in a single operation.
- Integrate with logging systems to automate alerts based on analysis results.

## Usage Patterns
Always initialize the skill with authentication via the `$OPENCLAW_API_KEY` environment variable. Use the CLI for quick queries or the API for programmatic integration. For CLI, pipe inputs from files; for API, handle requests in loops for batch processing. Validate IOC formats before submission (e.g., IPv4 as dotted decimal). Structure workflows to check for errors after each call and retry transient failures.

## Common Commands/API
- CLI Command: Run `openclaw ioc-analysis --ioc 192.168.1.1 --type ip --output json` to analyze an IP; add `--feed custom` for a specific threat feed.
- CLI Flag Details: Use `--timeout 30` to set request timeout in seconds; `--verbose` for detailed logs.
- API Endpoint: POST to `https://api.openclaw.com/v1/ioc-analysis` with JSON body like `{"ioc": "example.com", "type": "domain"}`.
- API Authentication: Include header `Authorization: Bearer $OPENCLAW_API_KEY`.
- Config Format: Use JSON for configurations, e.g., `{"feeds": ["virustotal", "alienvault"], "threshold": 0.7}` in a file passed via `--config path/to/config.json`.
- Code Snippet (Python):
  ```python
  import os
  import requests
  api_key = os.environ.get('OPENCLAW_API_KEY')
  response = requests.post('https://api.openclaw.com/v1/ioc-analysis', headers={'Authorization': f'Bearer {api_key}'}, json={'ioc': '8.8.8.8', 'type': 'ip'})
  print(response.json()['threats'])
  ```
- Another Code Snippet (Shell):
  ```bash
  export OPENCLAW_API_KEY=your_key_here
  curl -H "Authorization: Bearer $OPENCLAW_API_KEY" -X POST https://api.openclaw.com/v1/ioc-analysis -d '{"ioc": "badfile.exe", "type": "hash"}'
  ```

## Integration Notes
Integrate by importing the OpenClaw SDK in your application; for example, in Python, use `from openclaw import IOCAnalyzer`. Set up webhooks for real-time notifications by configuring `{"webhook_url": "https://your.endpoint.com/alerts"}` in the API request body. Combine with other blue-team skills by chaining outputs, e.g., pipe IOC results to a `threat-detection` skill. Ensure compatibility by matching API versions (e.g., v1) and handle rate limits with exponential backoff. For containerized environments, mount config files as volumes and inject `$OPENCLAW_API_KEY` via secrets.

## Error Handling
Check HTTP status codes after API calls; for 401, prompt for re-authentication. For 429 (rate limit), implement a retry loop with delays: wait 5 seconds and retry up to 3 times. Parse JSON errors for specifics, e.g., if "error": "Invalid IOC format", validate inputs first using regex (e.g., for IPs: `r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'`). In CLI, capture stderr and exit codes; use try-except in code snippets to log exceptions and fallback to default actions.

## Concrete Usage Examples
1. **Example 1: Analyze a Suspicious IP**  
   During an incident, query an IP from a firewall log: Run `openclaw ioc-analysis --ioc 192.168.1.100 --type ip --feed virustotal`. This returns JSON with threats like "associated with malware C2". In code: Use the snippet above, then if response['score'] > 0.5, trigger a block command.
   
2. **Example 2: Bulk Domain Check**  
   For threat hunting, process a list of domains from a CSV: First, create a config file with `{"ioc_list": ["example.com", "malicious.site"], "type": "domain"}`, then run `openclaw ioc-analysis --config domains.json --output report.csv`. In a script, loop through the list via API calls and aggregate results for reporting.

## Graph Relationships
- Related to: threat-detection (shares IOC data for enhanced alerting)
- Connected via: blue-team cluster (collaborates on incident response workflows)
- Links to: red-team skills (for simulation and testing of IOC detection)
- Dependencies: Requires access to external feeds like VirusTotal or AlienVault for enrichment
