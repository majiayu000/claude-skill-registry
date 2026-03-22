---
name: log-analysis
cluster: blue-team
description: "Analyzes system and application logs to detect anomalies and security threats in blue-team operations."
tags: ["logs","forensics","security"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "log analysis security monitoring forensics blue-team"
---

# log-analysis

## Purpose
This skill analyzes system and application logs to identify anomalies, security threats, and patterns indicative of breaches, supporting blue-team operations by providing actionable insights for incident response.

## When to Use
Use this skill during forensic investigations, real-time monitoring, or post-incident reviews. Apply it when logs show unusual activity, such as repeated failed logins or unexpected network traffic, or for routine security audits in environments like cloud servers or on-premise systems.

## Key Capabilities
- Detect anomalies using machine learning-based pattern recognition on log data.
- Identify threats like SQL injection attempts or malware indicators via signature matching.
- Parse multiple log formats (e.g., syslog, Apache access logs) and extract metadata for correlation.
- Generate reports with severity levels and recommendations for mitigation.
- Support for filtering logs by time, IP, or user ID to narrow down investigations.

## Usage Patterns
Invoke this skill via CLI for quick analysis or integrate it into scripts for automated workflows. Always provide log input paths or streams, and specify analysis parameters. For example, pipe logs from a file or API, then apply filters before running detection. Use environment variables for authentication, like `$LOG_ANALYSIS_API_KEY`, to secure API calls. Ensure logs are in plain text or JSON format for optimal parsing.

## Common Commands/API
Use the CLI tool with commands like `log-analysis scan` for basic operations. For API integration, call endpoints like `POST /api/v1/logs/analyze` with a JSON payload.

- CLI Example: Scan a local file for threats:
  ```
  log-analysis scan --file /var/log/syslog --anomaly true --output report.json
  ```
  This flags anomalies and saves results to a file.

- API Example: Send logs for analysis:
  ```
  curl -X POST https://api.openclaw.com/api/v1/logs/analyze \
  -H "Authorization: Bearer $LOG_ANALYSIS_API_KEY" \
  -d '{"logs": [{"line": "ERROR: Unauthorized access"}], "filters": {"ip": "192.168.1.1"}}'
  ```
  This analyzes specified logs and returns JSON with detected threats.

- Common Flags: `--file <path>` for input, `--anomaly` for ML-based detection, `--threshold 0.8` for sensitivity level.
- Config Format: Use JSON for custom rules, e.g.:
  ```
  {
    "rules": [
      {"pattern": "Failed login", "severity": "high"}
    ]
  }
  ```
  Load via `--config config.json`.

## Integration Notes
Integrate with tools like ELK Stack or Splunk by streaming logs via API. Set `$LOG_ANALYSIS_API_KEY` as an environment variable for authentication. For example, in a Python script, import the SDK and authenticate:
  ```
  import log_analysis_sdk
  client = log_analysis_sdk.Client(api_key=os.environ['LOG_ANALYSIS_API_KEY'])
  response = client.analyze(logs_data)
  ```
  Handle webhooks for real-time alerts by registering a callback URL. Ensure compatibility by matching log formats; convert non-standard logs using tools like jq.

## Error Handling
Check for errors like invalid log formats or authentication failures. Use try-catch blocks in scripts:
  ```
  try:
      result = log_analysis.scan('--file invalid.log')
  except FileNotFoundError:
      print("Error: Log file not found. Verify path and permissions.")
  ```
  Common errors include 401 Unauthorized (missing `$LOG_ANALYSIS_API_KEY`) or 400 Bad Request (malformed JSON). Log errors with timestamps and retry transient issues up to 3 times with exponential backoff. Validate inputs before commands, e.g., check if files exist using `os.path.exists()`.

## Concrete Usage Examples
1. **Detect anomalies in server logs:** Run `log-analysis scan --file /var/log/auth.log --anomaly true` to identify potential brute-force attacks. Review the output JSON for entries like {"event": "Failed login", "count": 5, "threat": "high"}, then correlate with firewall logs for further investigation.
   
2. **Integrate with a monitoring script:** In a Bash script, fetch logs from a remote server and analyze:
   ```
   logs=$(curl http://server/logs.txt)
   echo "$logs" | log-analysis scan --stream --threshold 0.7
   ```
   This detects threats in real-time streams, outputting alerts for anomalies like unusual user activity, and pipes results to a SIEM for automated response.

## Graph Relationships
- Related to: forensics (via shared tags for log parsing), security (for threat detection overlap), blue-team cluster (as a core component for operations).
- Links: Connects to skills like "incident-response" for follow-up actions and "network-monitoring" for correlated data analysis.
