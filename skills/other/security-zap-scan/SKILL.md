---
name: security-zap-scan
description: "Run an OWASP ZAP baseline security scan locally using Docker. Checks for the ZAP baseline script, executes the scan, and summarizes findings by risk level with remediation recommendations."
allowed-tools: ["Bash", "Read"]
---

# OWASP ZAP Baseline Security Scan

Run a ZAP baseline security scan against the local application.

## Workflow

1. **Check prerequisites**:
   - Verify Docker is installed and running: `docker info`
   - Check if `scripts/zap-baseline.sh` exists in the project

2. **Execute scan**:
   - If the script exists, run: `bash scripts/zap-baseline.sh`
   - If the script does not exist, inform the user that this project does not have a ZAP baseline scan configured

3. **Analyze results**:
   - After the scan completes, read `zap-report.html` (or `zap-report.md` for text)
   - Summarize findings:
     - Total number of alerts by risk level (High, Medium, Low, Informational)
     - List each Medium+ finding with its rule ID, name, and recommended fix
     - Categorize findings as "infrastructure-level" (fix at CDN/proxy) vs "application-level" (fix in code)

4. **Handle failures**:
   - If the scan failed, explain what failed and suggest concrete remediation steps

## Execution

Run the scan now.
