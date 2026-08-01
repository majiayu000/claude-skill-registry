---
name: deploying-osquery-fleet
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: deploying-osquery-fleet
description: >-
  Deploy and manage osquery across endpoint fleets for real-time system
  visibility. Covers query packs, scheduled queries, fleet management with
  FleetDM/Kolide, file integrity monitoring, and threat hunting with SQL.
domain: cybersecurity
subdomain: blue-team
tags:
  - osquery
  - endpoint-security
  - fleet-management
  - threat-hunting
  - file-integrity
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1082", "T1057"]
---

# Deploying Osquery Fleet

## Overview

Osquery exposes the operating system as a relational database, allowing
security teams to query endpoints using SQL. When deployed at scale with
a fleet manager (FleetDM, Kolide), it provides real-time visibility into
processes, users, network connections, installed software, and system
configuration across Windows, macOS, and Linux.

## Prerequisites

| Requirement | Purpose |
|---|---|
| osquery package | `apt install osquery` or MSI/PKG installer |
| Fleet manager (optional) | FleetDM or Kolide for central management |
| TLS infrastructure | Secure agent-to-server communication |
| Log aggregation | Ship osquery results to SIEM |

## Key Concepts

### Essential Security Queries

```sql
-- Running processes with network connections
SELECT p.pid, p.name, p.path, p.cmdline, p.uid,
       l.address, l.port, l.protocol
FROM processes p
JOIN listening_ports l ON p.pid = l.pid
WHERE l.port != 0;

-- Users with login shells
SELECT username, uid, gid, shell, directory
FROM users
WHERE shell NOT LIKE '%nologin%'
  AND shell NOT LIKE '%false%';

-- Installed packages (Linux)
SELECT name, version, source, arch
FROM deb_packages
ORDER BY name;

-- Cron jobs (persistence detection)
SELECT event, minute, hour, day_of_month, month,
       day_of_week, command, path
FROM crontab;

-- Kernel modules loaded
SELECT name, size, status, used_by
FROM kernel_modules
WHERE status = 'Live';

-- SSH authorized keys
SELECT uid, username, key, key_file
FROM users
JOIN authorized_keys USING (uid);

-- SUID binaries
SELECT path, permissions, uid, gid
FROM suid_bin;

-- Open files by process
SELECT p.name, p.pid, p.uid, of.path
FROM processes p
JOIN process_open_files of ON p.pid = of.pid
WHERE of.path LIKE '/etc/%';
```

### Threat Hunting Queries

```sql
-- Processes running from temp directories
SELECT pid, name, path, cmdline, uid, parent
FROM processes
WHERE path LIKE '/tmp/%'
   OR path LIKE '/var/tmp/%'
   OR path LIKE '/dev/shm/%';

-- Recently modified files in sensitive directories
SELECT path, filename, mtime, atime, uid, gid, mode
FROM file
WHERE (path LIKE '/etc/%%' OR path LIKE '/usr/bin/%%')
  AND mtime > (strftime('%s', 'now') - 86400);

-- DNS resolvers (detect DNS hijacking)
SELECT * FROM dns_resolvers;

-- Browser extensions (potential malware)
SELECT name, identifier, version, path, browser_type
FROM chrome_extensions
WHERE NOT identifier LIKE 'com.google%';

-- Docker containers running
SELECT id, name, image, status, started_at
FROM docker_containers
WHERE status = 'running';
```

### Query Packs

```json
{
  "queries": {
    "processes_listening": {
      "query": "SELECT p.name, l.port, l.address, l.protocol FROM listening_ports l JOIN processes p ON l.pid = p.pid;",
      "interval": 300,
      "description": "Processes with listening ports",
      "snapshot": true
    },
    "crontab_snapshot": {
      "query": "SELECT * FROM crontab;",
      "interval": 3600,
      "description": "Cron job inventory",
      "snapshot": true
    },
    "suid_binaries": {
      "query": "SELECT * FROM suid_bin;",
      "interval": 3600,
      "description": "SUID binary inventory",
      "snapshot": true
    },
    "process_events": {
      "query": "SELECT pid, path, cmdline, uid, time FROM process_events;",
      "interval": 60,
      "description": "Process creation events"
    }
  }
}
```

### osquery.conf

```json
{
  "options": {
    "host_identifier": "hostname",
    "schedule_splay_percent": 10,
    "logger_plugin": "tls",
    "tls_hostname": "fleet.example.com",
    "tls_server_certs": "/etc/osquery/fleet.pem",
    "enroll_secret_path": "/etc/osquery/enroll_secret",
    "disable_events": false,
    "enable_file_events": true,
    "enable_process_events": true
  },
  "schedule": {
    "system_info": {
      "query": "SELECT * FROM system_info;",
      "interval": 3600
    }
  },
  "packs": {
    "security": "/etc/osquery/packs/security.json"
  },
  "file_paths": {
    "etc": ["/etc/%%"],
    "binaries": ["/usr/bin/%%", "/usr/sbin/%%"],
    "ssh": ["/root/.ssh/%%", "/home/%/.ssh/%%"]
  }
}
```

## Workflow

1. **Install** — Deploy osquery package to endpoints
2. **Configure** — Set osquery.conf with fleet enrollment or local mode
3. **Packs** — Deploy security query packs for scheduled monitoring
4. **Enroll** — Agents connect to fleet manager and register
5. **Query** — Run live queries across fleet for threat hunting
6. **Alert** — Configure differential results to trigger SIEM alerts
7. **Maintain** — Update packs as new threats emerge

## Detection

```yaml
title: Osquery Fleet Detection
id: 08468794-63c5-4992-aa70-027069be5e85
status: experimental
description: Detects suspicious activity related to deploying osquery fleet techniques in blue team context
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine: "*deploying*osquery*"
  condition: selection
level: medium
tags:
  - attack.t1082
  - attack.t1057
  - attack.defense_evasion
falsepositives:
  - Security team running authorized detection validation tools
```

## Verification

| Check | Method |
|---|---|
| osqueryd running | `systemctl status osqueryd` — active |
| Config valid | `osqueryctl config-check` — no errors |
| Events enabled | `osqueryi "SELECT * FROM osquery_events;"` — subscriptions active |
| Fleet enrolled | Fleet UI shows host online |
| Results flowing | SIEM receives osquery JSON logs |

## References

- [Osquery Documentation](https://osquery.readthedocs.io/)
- [Osquery Schema](https://osquery.io/schema/)
- [FleetDM](https://fleetdm.com/)
- [Palantir osquery-configuration](https://github.com/palantir/osquery-configuration)
