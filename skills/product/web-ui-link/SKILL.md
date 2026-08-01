---
name: web-ui-link
description: 'Generate URLs for the LimaCharlie web application interface. Quickly
  open the web UI for any feature: dashboard, sensors, detections, D&R rules, FP rules,
  secrets, outputs, lookups, payloads, YARA rul'
---

---
name: web-ui-link
description: Generate URLs for the LimaCharlie web application interface. Quickly open the web UI for any feature: dashboard, sensors, detections, D&R rules, FP rules, secrets, outputs, lookups, payloads, YARA rules, artifacts, investigations, extensions, adapters, installation keys, billing, users, playbooks, AI agents, and more. For sensor-specific pages: timeline, console, processes, network, file-system, live-feed. For groups: members, organizations, permissions. Use for "open dashboard", "link to detections", "web UI for sensor", "open D&R rules page", "browser link", "app link", "open in web", "show me URL for", "go to".
allowed-tools:
  - Task
  - Read
---

# Web UI Link Generator

Generate direct URLs to any page in the LimaCharlie web application at `https://app.limacharlie.io`.

---

## LimaCharlie Integration

> **Prerequisites**: Run `/init-lc` to initialize LimaCharlie context.

### API Access Pattern

All LimaCharlie API calls go through the `limacharlie-api-executor` sub-agent:

```
Task(
  subagent_type="lc-essentials:limacharlie-api-executor",
  model="sonnet",
  prompt="Execute LimaCharlie API call:
    - Function: <function-name>
    - Parameters: {<params>}
    - Return: RAW | <extraction instructions>
    - Script path: {skill_base_directory}/../../scripts/analyze-lc-result.sh"
)
```

### Critical Rules

| Rule | Wrong | Right |
|------|-------|-------|
| **MCP Access** | Call `mcp__*` directly | Use `limacharlie-api-executor` sub-agent |
| **OID** | Use org name | Use UUID (call `list_user_orgs` if needed) |

---

## When to Use

Invoke this skill when users:

- Ask for a **link to a LimaCharlie feature** (e.g., "link to the secrets page", "URL for D&R rules")
- Want to **open a specific page** (e.g., "open the detections dashboard", "go to sensors")
- Need to **navigate to a sensor page** (e.g., "show me the timeline for sensor X", "processes for DESKTOP-ABC")
- Ask **"where can I..."** questions about the web interface (e.g., "where can I configure outputs?")
- Request **browser/app links** to share with team members

Common trigger phrases:
- "link to...", "URL for...", "open...", "go to...", "navigate to..."
- "where is...", "where can I find...", "how do I access..."
- "browser link", "app link", "web UI"

## Base URL

All URLs use the base: `https://app.limacharlie.io`

## URL Reference

### Organization Routes (`/orgs/{oid}/*`)

These routes require an Organization ID (OID).

| Feature | Path | Aliases/Keywords |
|---------|------|------------------|
| Dashboard | `/orgs/{oid}/dashboard` | home, overview, main |
| Sensors | `/orgs/{oid}/sensors` | endpoints, agents, hosts, machines |
| Query Console | `/orgs/{oid}/search` | search, query, lcql, hunt |
| Detections | `/orgs/{oid}/detections` | alerts, findings, incidents |
| D&R Rules | `/orgs/{oid}/dr-rules` | detection rules, d&r, dr rules |
| FP Rules | `/orgs/{oid}/fp-rules` | false positive, fp, suppression |
| Secrets Manager | `/orgs/{oid}/secrets-manager` | secrets, credentials, keys |
| Outputs | `/orgs/{oid}/outputs` | output destinations, siem, destinations |
| Lookups | `/orgs/{oid}/lookups` | lookup tables, reference data, ioc lists |
| Payloads | `/orgs/{oid}/payloads` | payload management |
| YARA Rules | `/orgs/{oid}/yara-rules` | yara, malware rules |
| Artifacts | `/orgs/{oid}/artifacts` | collected artifacts, evidence |
| Investigations | `/orgs/{oid}/investigations` | cases, incidents, timelines |
| Extensions | `/orgs/{oid}/extensions` | add-ons, subscriptions |
| External Adapters | `/orgs/{oid}/external-adapters` | adapters, data ingestion |
| Installation Keys | `/orgs/{oid}/installation-keys` | install keys, deployment keys |
| Install Sensors | `/orgs/{oid}/install-sensors` | sensor installation, deploy sensors |
| Users & Roles | `/orgs/{oid}/users` | users, permissions, access, roles |
| Billing & Usage | `/orgs/{oid}/billing-usage` | billing, usage, quota, costs |
| REST API | `/orgs/{oid}/rest-api` | api keys, api configuration |
| Integrations | `/orgs/{oid}/integrations` | third-party integrations |
| AI Agents | `/orgs/{oid}/ai-agents` | ai, agents |
| Playbooks | `/orgs/{oid}/playbooks` | automation, workflows |
| Management Logs | `/orgs/{oid}/logs/management` | audit logs, management logs |
| YARA Service | `/orgs/{oid}/yara` | yara scanning |
| Exfil Control | `/orgs/{oid}/exfil` | exfiltration, data control |
| Sensor Cull | `/orgs/{oid}/sensor-cull` | cleanup, stale sensors |
| Reliable Tasking | `/orgs/{oid}/reliable-tasking` | offline tasking |
| Vulnerabilities | `/orgs/{oid}/vulnerabilities` | vulns, cve, security issues |
| Artifact Collection | `/orgs/{oid}/artifact-collection` | collection rules |

### Sensor Routes (`/orgs/{oid}/sensors/{sid}/*`)

These routes require both Organization ID (OID) and Sensor ID (SID).

| Feature | Path | Aliases/Keywords |
|---------|------|------------------|
| Sensor Overview | `/orgs/{oid}/sensors/{sid}/overview` | sensor info, sensor details |
| Timeline | `/orgs/{oid}/sensors/{sid}/timeline` | events, event timeline, history |
| Sensor Detections | `/orgs/{oid}/sensors/{sid}/detections` | endpoint alerts |
| Live Console | `/orgs/{oid}/sensors/{sid}/console` | console, terminal, shell, cli |
| Processes | `/orgs/{oid}/sensors/{sid}/processes` | running processes, process list, ps |
| Network | `/orgs/{oid}/sensors/{sid}/network` | connections, netstat, network connections |
| File System | `/orgs/{oid}/sensors/{sid}/file-system` | files, file browser, directories |
| Live Feed | `/orgs/{oid}/sensors/{sid}/live-feed` | live events, real-time |
| Sensor Artifacts | `/orgs/{oid}/sensors/{sid}/artifacts` | endpoint artifacts |
| Event Collection | `/orgs/{oid}/sensors/{sid}/event-collection` | collection rules |
| Sensor Extensions | `/orgs/{oid}/sensors/{sid}/extensions` | endpoint extensions |
| OS Users | `/orgs/{oid}/sensors/{sid}/os-users` | local users, user accounts |
| OS Packages | `/orgs/{oid}/sensors/{sid}/os-packages` | installed packages, software, programs |
| OS Services | `/orgs/{oid}/sensors/{sid}/os-services` | services, windows services, daemons |
| Autoruns | `/orgs/{oid}/sensors/{sid}/os-autoruns` | startup, persistence, autostart |
| Analytics | `/orgs/{oid}/sensors/{sid}/analytics` | sensor analytics |
| File Integrity | `/orgs/{oid}/sensors/{sid}/integrity-rules` | fim, file integrity monitoring |
| Drivers | `/orgs/{oid}/sensors/{sid}/os-drivers` | kernel drivers |

### Group Routes (`/groups/{group_id}/*`)

These routes require a Group ID.

| Feature | Path | Aliases/Keywords |
|---------|------|------------------|
| Group Members | `/groups/{gid}/users` | group users, members, owners |
| Group Organizations | `/groups/{gid}/organizations` | group orgs, member orgs |
| Group Permissions | `/groups/{gid}/permissions` | access control |
| Group Activity | `/groups/{gid}/activity-logs` | group logs, audit |

### Global Routes (No OID Required)

| Feature | Path | Aliases/Keywords |
|---------|------|------------------|
| Marketplace | `/add-ons` | add-ons, extensions marketplace |
| User Profile | `/profile` | my profile, account settings |
| Create Organization | `/create-org` | new org, new organization |

## How to Use

### Step 1: Parse the User Request

Extract from the user's request:
- **Target feature**: What page they want (sensors, detections, secrets, etc.)
- **Organization**: Name or OID (if provided)
- **Sensor**: Hostname or SID (if requesting sensor-specific page)
- **Group**: Group ID (if requesting group page)

### Step 2: Resolve Organization ID

If the user provided an organization **name** instead of OID, or if no organization was specified:

```
Task(
  subagent_type="lc-essentials:limacharlie-api-executor",
  model="sonnet",
  prompt="Execute LimaCharlie API call:
    - Function: list_user_orgs
    - Parameters: {}
    - Return: List of organizations with their OIDs and names"
)
```

**Handling multiple organizations:**
- If user has **1 org**: Use it automatically
- If user has **multiple orgs** and none specified: Ask user to select
- If org name was provided: Match by name (case-insensitive)

### Step 3: Resolve Sensor ID (if needed)

If the user requested a sensor-specific URL but provided a **hostname** instead of SID:

```
Task(
  subagent_type="lc-essentials:limacharlie-api-executor",
  model="sonnet",
  prompt="Execute LimaCharlie API call:
    - Function: list_sensors
    - Parameters: {\"oid\": \"[oid]\"}
    - Return: Find sensor with hostname matching '[hostname]' and return its SID"
)
```

### Step 4: Match Feature to URL Path

Use the reference tables above to match the user's request to the correct URL path. Apply keyword/alias matching for flexibility.

### Step 5: Construct and Return URL

Build the complete URL by combining:
- Base URL: `https://app.limacharlie.io`
- Path with resolved OID/SID/Group ID

Return the URL in a clickable markdown format:
```
[Feature Name](https://app.limacharlie.io/orgs/{oid}/feature)
```

## Example Usage

### Example 1: Simple Organization Feature

**User**: "Give me the link to the secrets manager"

**Steps**:
1. Feature identified: `secrets-manager`
2. No org specified - call `list_user_orgs`
3. If single org, use its OID; if multiple, ask user to select
4. Construct URL

**Response**:
```
Here's the link to the Secrets Manager:

[Secrets Manager](https://app.limacharlie.io/orgs/c7e8f940-1234-5678-abcd-1234567890ab/secrets-manager)
```

### Example 2: Sensor-Specific URL

**User**: "Open the timeline for sensor DESKTOP-PROD01 in the production org"

**Steps**:
1. Feature identified: `timeline` (sensor route)
2. Org name: "production" - resolve to OID via `list_user_orgs`
3. Hostname: "DESKTOP-PROD01" - resolve to SID via `list_sensors`
4. Construct sensor timeline URL

**Response**:
```
Here's the timeline for DESKTOP-PROD01:

[Sensor Timeline](https://app.limacharlie.io/orgs/a1b2c3d4-5678-90ab-cdef-1234567890ab/sensors/abc123def456/timeline)
```

### Example 3: Multiple URLs Requested

**User**: "I need links to detections, D&R rules, and the query console"

**Response**:
```
Here are your requested links:

- [Detections](https://app.limacharlie.io/orgs/{oid}/detections)
- [D&R Rules](https://app.limacharlie.io/orgs/{oid}/dr-rules)
- [Query Console](https://app.limacharlie.io/orgs/{oid}/search)
```

### Example 4: Ambiguous Request

**User**: "Link to the rules page"

**Response**:
```
There are several types of rules in LimaCharlie. Which one would you like?

1. **D&R Rules** - Detection & Response rules
   https://app.limacharlie.io/orgs/{oid}/dr-rules

2. **FP Rules** - False Positive suppression rules
   https://app.limacharlie.io/orgs/{oid}/fp-rules

3. **YARA Rules** - Malware detection rules
   https://app.limacharlie.io/orgs/{oid}/yara-rules

4. **Artifact Collection Rules** - Data collection rules
   https://app.limacharlie.io/orgs/{oid}/artifact-collection
```

### Example 5: Unknown Feature with Suggestions

**User**: "Link to the threat intel page"

**Response**:
```
LimaCharlie doesn't have a dedicated "threat intel" page, but here are related features:

- **Lookups** - Store and query IOC lists, threat intel feeds
  https://app.limacharlie.io/orgs/{oid}/lookups

- **D&R Rules** - Create detection rules based on threat intel
  https://app.limacharlie.io/orgs/{oid}/dr-rules

- **Query Console** - Hunt for IOCs using LCQL
  https://app.limacharlie.io/orgs/{oid}/search

Would you like a link to one of these?
```

## Error Handling

### Organization Not Found
```
Organization "acme-corp" not found. Your available organizations:

- production (a1b2c3d4-5678-...)
- staging (e5f6g7h8-9012-...)
- dev (i9j0k1l2-3456-...)

Please specify which organization you'd like.
```

### Sensor Not Found
```
No sensor found with hostname "UNKNOWN-HOST" in organization "production".

Would you like me to:
1. List all sensors in this organization
2. Search for sensors with a similar hostname
```

### Missing Required Information
```
The sensor timeline page requires a sensor ID.

Please provide either:
- A sensor SID (e.g., "abc123def456...")
- OR a hostname (e.g., "DESKTOP-PROD01")

I can also list sensors in your organization if you need to find one.
```

## Notes

- **OID Format**: Organization IDs are UUIDs (e.g., `c7e8f940-1234-5678-abcd-1234567890ab`)
- **SID Format**: Sensor IDs are also UUIDs
- **Case Sensitivity**: Feature matching is case-insensitive
- **Multiple Matches**: When a request could match multiple features, present all options
- **Global Routes**: Some pages (marketplace, profile) don't require an organization context

## Related Skills

- `limacharlie-call` - For actually interacting with LimaCharlie APIs
- `lookup-lc-doc` - For documentation about LimaCharlie features
- `sensor-health` - For checking sensor status before linking to sensor pages
