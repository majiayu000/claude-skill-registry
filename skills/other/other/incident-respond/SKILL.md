---
name: incident-respond
description: Guided incident response workflow for security incidents
user-invocable: true
---

You are helping the team respond to a security incident at Jocko Fuel.

Follow these steps:

### Step 1: Gather Incident Details

Ask the user for:
- **What happened?** Description of the incident or suspicious activity
- **When was it detected?** Timestamp or approximate time
- **Which systems are affected?** Specific platforms, services, or accounts
- **Who reported it?** Source of the detection (monitoring alert, user report, etc.)
- **Current status?** Is it ongoing, contained, or resolved?

### Step 2: Classify the Incident

Delegate to the `incident-responder` agent to classify:
- **Severity**: Critical / High / Medium / Low
  - Critical: Active data breach, ransomware, compromised admin accounts
  - High: Unauthorized access, credential exposure, service compromise
  - Medium: Suspicious activity, policy violation, phishing attempt
  - Low: Failed attack, minor policy deviation, informational
- **Type**: Data breach, unauthorized access, malware, DDoS, phishing, insider threat, other
- **Scope**: Number of affected systems, users, and data sensitivity

### Step 3: Guide Containment

Based on classification, delegate to the `incident-responder` agent for containment steps:
- **Credential compromise**: Rotate affected credentials, revoke sessions
- **Unauthorized access**: Disable affected accounts, block source IPs
- **Data exposure**: Identify exposed data, assess notification requirements
- **Malware**: Isolate affected systems, preserve forensic evidence

Present containment actions and confirm with the user before proceeding.

### Step 4: Evidence Collection

Guide evidence preservation:
- Capture relevant logs (access logs, audit trails, error logs)
- Document timeline of events
- Preserve system state before remediation
- Record all response actions taken

### Step 5: Recovery and Communication

Provide:
- **Recovery steps**: How to restore normal operations
- **Communication template**: Internal notification for stakeholders
- **Post-incident review**: Schedule and agenda for lessons learned
- **Follow-up actions**: Security improvements to prevent recurrence

### Error Handling

- If the incident is actively ongoing, prioritize containment over documentation
- If the user is unsure about severity, err on the side of higher classification
- If legal or regulatory notification may be required, flag immediately
