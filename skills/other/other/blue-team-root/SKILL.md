---
name: blue-team-root
cluster: blue-team
description: "Fundamental blue team skills for detecting threats, responding to incidents, and defending systems in cybersecurity."
tags: ["blue-team","cybersecurity","defense","incident-response"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "blue team cybersecurity defense monitoring incident response"
---

# blue-team-root

## Purpose
This skill provides core blue-team functionalities for cybersecurity, enabling threat detection, incident response, and system defense. It integrates with tools like intrusion detection systems and logging frameworks to protect against cyber threats.

## When to Use
Use this skill when monitoring network traffic for anomalies, responding to security incidents, or hardening systems. Apply it in real-time threat detection scenarios, such as during a suspected breach, or for proactive defense in environments like cloud infrastructures or on-premise servers.

## Key Capabilities
- **Threat Detection**: Scan networks using tools like Snort; example: detect intrusions by analyzing packet captures with `snort -A console -q -c /etc/snort/snort.conf`.
- **Incident Response**: Automate containment via scripts that isolate affected hosts; e.g., use a Python snippet to block IP: `import subprocess; subprocess.run(['iptables', '-A', 'INPUT', '-s', '192.168.1.1', '-j', 'DROP'])`.
- **System Defense**: Configure firewalls and monitoring; set up OSSEC for real-time alerting with config like `<global><email_notification>yes</email_notification></global>` in ossec.conf.
- **Log Analysis**: Parse logs with ELK stack; query Elasticsearch endpoint `/logs/_search` with JSON payload `{"query": {"match": {"message": "suspicious login"}}}`.
- **Vulnerability Scanning**: Run Nessus scans via API; endpoint `POST /scans` requires JSON body like `{"policy_id": 1, "targets": ["192.168.1.0/24"]}`.

## Usage Patterns
Invoke this skill in OpenClaw by calling the skill ID "blue-team-root" with specific parameters. For example, to detect threats, use: `openclaw execute blue-team-root --action detect --target 192.168.1.0/24`. In code, integrate via OpenClaw SDK: `from openclaw import Skill; skill = Skill('blue-team-root'); result = skill.run(action='respond', incident_id='INC001')`. Always set auth with environment variable `$OPENCLAW_API_KEY` before execution. Chain with other skills by piping outputs, e.g., detect then respond: `openclaw execute blue-team-root --action detect | openclaw execute blue-team-root --action respond`.

## Common Commands/API
- **CLI Commands**: Use `openclaw blue-team-root detect --flags -i interface -t timeout` to start network monitoring; flags include `-i` for interface and `-t` for scan timeout in seconds.
- **API Endpoints**: Access via HTTP POST to `https://api.openclaw.ai/blue-team/detect` with body `{"target": "192.168.1.0/24", "auth": "$OPENCLAW_API_KEY"}`; response includes JSON like `{"status": "detected", "threats": ["SQL injection"]}`.
- **Code Snippets**: For incident response, use: `response = requests.post('https://api.openclaw.ai/blue-team/respond', json={"incident": "INC001", "action": "isolate"}); print(response.json()['status'])`. Another: `os.system('snort -c /etc/snort.conf -A fast > detection.log')` to log detections.
- **Config Formats**: Use YAML for configurations, e.g., `detection: { threshold: 5, rules: ['rule1', 'rule2'] }`; load in Python with `import yaml; config = yaml.safe_load(open('config.yaml'))`.

## Integration Notes
Integrate with external tools by exporting results to SIEM systems like Splunk via webhook: `openclaw blue-team-root --action export --format json --url https://splunk.example.com/api`. For authentication, always use `$OPENCLAW_API_KEY` in headers, e.g., `headers = {'Authorization': f'Bearer {os.environ.get("OPENCLAW_API_KEY")}'} in Python requests. Combine with red-team skills for simulations; pipe output directly, e.g., `openclaw execute red-team-sim | openclaw execute blue-team-root --action detect`. Ensure compatibility by matching API versions, like OpenClaw v2.0.

## Error Handling
Handle errors by checking API responses for status codes; if 401, retry with refreshed `$OPENCLAW_API_KEY`. For CLI, use try-except in scripts: `try: subprocess.run(['snort', '-c', 'config'], check=True) except subprocess.CalledProcessError as e: print(f"Error: {e.returncode} - {e.output}")`. Common issues include network timeouts; implement retries with exponential backoff, e.g., `for attempt in range(3): try: requests.get(url) except requests.exceptions.Timeout: time.sleep(2**attempt)`. Log all errors to a file for auditing, using Python's logging: `import logging; logging.basicConfig(filename='blue-team.log', level=logging.ERROR)`.

## Concrete Usage Examples
1. **Threat Detection Example**: To detect potential threats on a network, run: `openclaw execute blue-team-root --action detect --target 192.168.1.0/24 --auth $OPENCLAW_API_KEY`. This scans the subnet and returns anomalies; follow up by parsing the JSON output to alert on high-severity items.
2. **Incident Response Example**: For an active incident, use: `openclaw execute blue-team-root --action respond --incident_id INC002 --steps isolate,notify`. This isolates the affected host and sends notifications; in code, verify with `if response['status'] == 'success': print('Incident contained')`.

## Graph Relationships
- **Parent Cluster**: Connected to "blue-team" cluster for broader cybersecurity operations.
- **Related Skills**: Links to "incident-response" (ID: blue-team-ir) for advanced response tactics; and "threat-intelligence" (ID: blue-team-ti) for intelligence gathering.
- **Downstream Dependencies**: Requires "logging-core" skill for log access; outputs to "alerting-system" for notifications.
