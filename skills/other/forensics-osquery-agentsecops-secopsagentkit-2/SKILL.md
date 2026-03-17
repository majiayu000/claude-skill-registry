---
name: forensics-osquery
description: >
  SQL-powered forensic investigation and system interrogation using osquery to query
  operating systems as relational databases. Enables rapid evidence collection, threat
  hunting, and incident response across Linux, macOS, and Windows endpoints.
  Use when: (1) Investigating security incidents and collecting forensic artifacts,
  (2) Threat hunting across endpoints for suspicious activity, (3) Analyzing running
  processes, network connections, and persistence mechanisms, (4) Collecting system
  state during incident response, (5) Querying file hashes, user activity, and system
  configuration for compromise indicators, (6) Building detection queries for continuous
  monitoring with osqueryd.
version: 0.1.0
maintainer: SirAppSec
category: incident-response
tags: [forensics, osquery, incident-response, threat-hunting, endpoint-detection, dfir, live-forensics, sql]
frameworks: [MITRE-ATT&CK, NIST]
dependencies:
  tools: [osquery]
  platforms: [linux, macos, windows]
references:
  - https://github.com/osquery/osquery
  - https://osquery.io/
  - https://osquery.readthedocs.io/
---

# osquery Forensics & Incident Response

## Overview

osquery transforms operating systems into queryable relational databases, enabling security analysts to investigate compromises using SQL rather than traditional CLI tools. This skill provides forensic investigation workflows, common detection queries, and incident response patterns for rapid evidence collection across Linux, macOS, and Windows endpoints.

**Core capabilities**:
- SQL-based system interrogation for process, network, file, and user analysis
- Cross-platform forensic artifact collection (Linux, macOS, Windows)
- Live system analysis without deploying heavyweight forensic tools
- Threat hunting queries mapped to MITRE ATT&CK techniques
- Scheduled monitoring with osqueryd for continuous detection
- Integration with SIEM and incident response platforms

## Quick Start

### Interactive Investigation (osqueryi)

```bash
# Launch interactive shell
osqueryi

# Check running processes
SELECT pid, name, path, cmdline, uid FROM processes WHERE name LIKE '%suspicious%';

# Identify listening network services
SELECT DISTINCT processes.name, listening_ports.port, listening_ports.address, processes.pid, processes.path
FROM listening_ports
JOIN processes USING (pid)
WHERE listening_ports.address != '127.0.0.1';

# Find processes with deleted executables (potential malware)
SELECT name, path, pid, cmdline FROM processes WHERE on_disk = 0;

# Check persistence mechanisms (Linux/macOS cron jobs)
SELECT command, path FROM crontab;
```

### One-Liner Forensic Queries

```bash
# Single query execution
osqueryi --json "SELECT * FROM logged_in_users;"

# Export query results for analysis
osqueryi --json "SELECT * FROM processes;" > processes_snapshot.json

# Check for suspicious kernel modules (Linux)
osqueryi --line "SELECT name, used_by, status FROM kernel_modules WHERE name NOT IN (SELECT name FROM known_good_modules);"
```

## Core Workflows

### Workflow 1: Initial Incident Response Triage

For rapid assessment of potentially compromised systems:

Progress:
[ ] 1. Collect running processes and command lines
[ ] 2. Identify network connections and listening ports
[ ] 3. Check user accounts and recent logins
[ ] 4. Examine persistence mechanisms (scheduled tasks, startup items)
[ ] 5. Review suspicious file modifications and executions
[ ] 6. Document findings with timestamps and process ancestry
[ ] 7. Export evidence to JSON for preservation

Work through each step systematically. Use bundled triage script for automated collection.

**Execute triage**: `./scripts/osquery_triage.sh > incident_triage_$(date +%Y%m%d_%H%M%S).json`

### Workflow 2: Threat Hunting for Specific TTPs

When hunting for specific MITRE ATT&CK techniques:

1. **Select Target Technique**
   - Identify technique from threat intelligence (e.g., T1055 - Process Injection)
   - Map technique to observable system artifacts
   - See [references/mitre-attack-queries.md](references/mitre-attack-queries.md) for pre-built queries

2. **Build Detection Query**
   - Identify relevant osquery tables (processes, file_events, registry, etc.)
   - Join tables to correlate related artifacts
   - Use [references/table-guide.md](references/table-guide.md) for schema reference

3. **Execute Hunt**
   ```sql
   -- Example: Hunt for credential dumping (T1003)
   SELECT p.pid, p.name, p.cmdline, p.path, p.parent, pm.permissions
   FROM processes p
   JOIN process_memory_map pm ON p.pid = pm.pid
   WHERE p.name IN ('mimikatz.exe', 'procdump.exe', 'pwdump.exe')
      OR p.cmdline LIKE '%sekurlsa%'
      OR (pm.path = '/etc/shadow' OR pm.path LIKE '%SAM%');
   ```

4. **Analyze Results**
   - Review process ancestry and command-line arguments
   - Check file hashes against threat intelligence
   - Document timeline of suspicious activity

5. **Pivot Investigation**
   - Use findings to identify additional indicators
   - Query related artifacts (network connections, files, registry)
   - Expand hunt scope if compromise confirmed

### Workflow 3: Persistence Mechanism Analysis

Detecting persistence across platforms:

**Linux/macOS Persistence**:
```sql
-- Cron jobs
SELECT * FROM crontab;

-- Systemd services (Linux)
SELECT name, path, status, source FROM systemd_units WHERE source != '/usr/lib/systemd/system';

-- Launch Agents/Daemons (macOS)
SELECT name, path, program, run_at_load FROM launchd WHERE run_at_load = 1;

-- Bash profile modifications
SELECT * FROM file WHERE path IN ('/etc/profile', '/etc/bash.bashrc', '/home/*/.bashrc', '/home/*/.bash_profile');
```

**Windows Persistence**:
```sql
-- Registry Run keys
SELECT key, name, path, type FROM registry WHERE key LIKE '%Run%' OR key LIKE '%RunOnce%';

-- Scheduled tasks
SELECT name, action, path, enabled FROM scheduled_tasks WHERE enabled = 1;

-- Services
SELECT name, display_name, status, path, start_type FROM services WHERE start_type = 'AUTO_START';

-- WMI event consumers
SELECT name, command_line_template FROM wmi_cli_event_consumers;
```

Review results for:
- Unusual executables in startup locations
- Base64-encoded or obfuscated commands
- Executables in temporary or user-writable directories
- Recently modified persistence mechanisms

### Workflow 4: Network Connection Analysis

Investigating suspicious network activity:

```sql
-- Active network connections with process details
SELECT p.name, p.pid, p.path, p.cmdline, ps.remote_address, ps.remote_port, ps.state
FROM processes p
JOIN process_open_sockets ps ON p.pid = ps.pid
WHERE ps.remote_address NOT IN ('127.0.0.1', '::1', '0.0.0.0')
ORDER BY ps.remote_port;

-- Listening ports mapped to processes
SELECT DISTINCT p.name, lp.port, lp.address, lp.protocol, p.path, p.cmdline
FROM listening_ports lp
LEFT JOIN processes p ON lp.pid = p.pid
WHERE lp.address NOT IN ('127.0.0.1', '::1')
ORDER BY lp.port;

-- DNS lookups (requires events table or process monitoring)
SELECT name, domains, pid FROM dns_resolvers;
```

**Investigation checklist**:
- [ ] Identify non-standard listening ports (not 80, 443, 22, 3389)
- [ ] Check processes with external connections
- [ ] Review destination IPs against threat intelligence
- [ ] Correlate connections with process execution timeline
- [ ] Validate legitimate business purpose for connections

### Workflow 5: File System Forensics

Analyzing file modifications and suspicious files:

```sql
-- Recently modified files in sensitive locations
SELECT path, filename, size, mtime, ctime, md5, sha256
FROM hash
WHERE path LIKE '/etc/%' OR path LIKE '/tmp/%' OR path LIKE 'C:\Windows\Temp\%'
  AND mtime > (strftime('%s', 'now') - 86400);  -- Last 24 hours

-- Executable files in unusual locations
SELECT path, filename, size, md5, sha256
FROM hash
WHERE (path LIKE '/tmp/%' OR path LIKE '/var/tmp/%' OR path LIKE 'C:\Users\%\AppData\%')
  AND (filename LIKE '%.exe' OR filename LIKE '%.sh' OR filename LIKE '%.py');

-- SUID/SGID binaries (Linux/macOS) - potential privilege escalation
SELECT path, filename, mode, uid, gid
FROM file
WHERE (mode LIKE '%4%' OR mode LIKE '%2%')
  AND path LIKE '/usr/%' OR path LIKE '/bin/%';
```

**File analysis workflow**:
1. Identify suspicious files by location and timestamp
2. Extract file hashes (MD5, SHA256) for threat intel lookup
3. Review file permissions and ownership
4. Check for living-off-the-land binaries (LOLBins) abuse
5. Document file metadata for forensic timeline

## Forensic Query Patterns

### Pattern 1: Process Analysis

Standard process investigation queries:

```sql
-- Processes with network connections
SELECT p.pid, p.name, p.path, p.cmdline, ps.remote_address, ps.remote_port
FROM processes p
JOIN process_open_sockets ps ON p.pid = ps.pid;

-- Process tree (parent-child relationships)
SELECT p1.pid, p1.name AS process, p1.cmdline,
       p2.pid AS parent_pid, p2.name AS parent_name, p2.cmdline AS parent_cmdline
FROM processes p1
LEFT JOIN processes p2 ON p1.parent = p2.pid;

-- High-privilege processes (UID 0 / SYSTEM)
SELECT pid, name, path, cmdline, uid, euid FROM processes WHERE uid = 0 OR euid = 0;
```

### Pattern 2: User Activity Monitoring

Track user accounts and authentication:

```sql
-- Currently logged in users
SELECT user, tty, host, time, pid FROM logged_in_users;

-- User accounts with login shells
SELECT username, uid, gid, shell, directory FROM users WHERE shell NOT LIKE '%nologin%';

-- Recent authentication events (requires auditd/Windows Event Log integration)
SELECT * FROM user_events WHERE time > (strftime('%s', 'now') - 3600);

-- Sudo usage history (Linux/macOS)
SELECT username, command, time FROM sudo_usage_history ORDER BY time DESC LIMIT 50;
```

### Pattern 3: System Configuration Review

Identify configuration changes:

```sql
-- Kernel configuration and parameters (Linux)
SELECT name, value FROM kernel_info;
SELECT path, key, value FROM sysctl WHERE key LIKE 'kernel.%';

-- Installed packages (detect unauthorized software)
SELECT name, version, install_time FROM deb_packages ORDER BY install_time DESC LIMIT 20;  -- Debian/Ubuntu
SELECT name, version, install_time FROM rpm_packages ORDER BY install_time DESC LIMIT 20;  -- RHEL/CentOS

-- System information
SELECT hostname, computer_name, local_hostname FROM system_info;
```

## Security Considerations

- **Sensitive Data Handling**: osquery can access sensitive system information (password hashes, private keys, process memory). Limit access to forensic analysts and incident responders. Export query results to encrypted storage. Sanitize logs before sharing with third parties.

- **Access Control**: Requires root/administrator privileges on investigated systems. Use dedicated forensic user accounts with audit logging. Restrict osqueryd configuration files (osquery.conf) to prevent query tampering. Implement least-privilege access to query results.

- **Audit Logging**: Log all osquery executions for forensic chain-of-custody. Record analyst username, timestamp, queries executed, and systems queried. Maintain immutable audit logs for compliance and legal requirements. Use `osqueryd --audit` flag for detailed logging.

- **Compliance**: osquery supports NIST SP 800-53 AU (Audit and Accountability) controls and NIST Cybersecurity Framework detection capabilities. Enables evidence collection for GDPR data breach investigations (Article 33). Query results constitute forensic evidence - maintain integrity and chain-of-custody.

- **Safe Defaults**: Use read-only queries during investigations to avoid system modification. Test complex queries in lab environments before production use. Monitor osqueryd resource consumption to prevent denial of service. Disable dangerous tables (e.g., `curl`, `yara`) in osqueryd configurations unless explicitly needed.

## Bundled Resources

### Scripts

- `scripts/osquery_triage.sh` - Automated triage collection script for rapid incident response
- `scripts/osquery_hunt.py` - Threat hunting query executor with MITRE ATT&CK mapping
- `scripts/parse_osquery_json.py` - Parse and analyze osquery JSON output
- `scripts/osquery_to_timeline.py` - Generate forensic timelines from osquery results

### References

- `references/table-guide.md` - Comprehensive osquery table reference for forensic investigations
- `references/mitre-attack-queries.md` - Pre-built queries mapped to MITRE ATT&CK techniques
- `references/platform-differences.md` - Platform-specific tables and query variations (Linux/macOS/Windows)
- `references/osqueryd-deployment.md` - Deploy osqueryd for continuous monitoring and fleet management

### Assets

- `assets/osquery.conf` - Production osqueryd configuration template for security monitoring
- `assets/forensic-packs/` - Query packs for incident response scenarios
  - `ir-triage.conf` - Initial triage queries
  - `persistence-hunt.conf` - Persistence mechanism detection
  - `lateral-movement.conf` - Lateral movement indicators
  - `credential-access.conf` - Credential dumping detection

## Common Investigation Scenarios

### Scenario 1: Webshell Detection

Detect webshells on compromised web servers:

```sql
-- Check web server processes with suspicious child processes
SELECT p1.name AS webserver, p1.pid, p1.cmdline,
       p2.name AS child, p2.cmdline AS child_cmdline
FROM processes p1
JOIN processes p2 ON p1.pid = p2.parent
WHERE p1.name IN ('httpd', 'nginx', 'apache2', 'w3wp.exe')
  AND p2.name IN ('bash', 'sh', 'cmd.exe', 'powershell.exe', 'perl', 'python');

-- Files in web directories with recent modifications
SELECT path, filename, mtime, md5, sha256
FROM hash
WHERE path LIKE '/var/www/%' OR path LIKE 'C:\inetpub\wwwroot\%'
  AND (filename LIKE '%.php' OR filename LIKE '%.asp' OR filename LIKE '%.jsp')
  AND mtime > (strftime('%s', 'now') - 604800);  -- Last 7 days
```

### Scenario 2: Ransomware Investigation

Identify ransomware indicators:

```sql
-- Processes writing to many files rapidly (potential encryption activity)
SELECT p.name, p.pid, p.cmdline, COUNT(fe.path) AS files_modified
FROM processes p
JOIN file_events fe ON p.pid = fe.pid
WHERE fe.action = 'WRITE' AND fe.time > (strftime('%s', 'now') - 300)
GROUP BY p.pid
HAVING files_modified > 100;

-- Look for ransom note files
SELECT path, filename FROM file
WHERE filename LIKE '%DECRYPT%' OR filename LIKE '%README%' OR filename LIKE '%RANSOM%';

-- Check for file extension changes (encrypted files)
SELECT path, filename FROM file
WHERE filename LIKE '%.locked' OR filename LIKE '%.encrypted' OR filename LIKE '%.crypto';
```

### Scenario 3: Privilege Escalation Detection

Detect privilege escalation attempts:

```sql
-- Processes running as root from non-standard paths
SELECT pid, name, path, cmdline, uid, euid FROM processes
WHERE (uid = 0 OR euid = 0)
  AND path NOT LIKE '/usr/%'
  AND path NOT LIKE '/sbin/%'
  AND path NOT LIKE '/bin/%'
  AND path NOT LIKE 'C:\Windows\%';

-- SUID binaries (Linux/macOS)
SELECT path, filename, uid, gid FROM file
WHERE mode LIKE '%4%' AND path NOT IN (SELECT path FROM known_suid_binaries);

-- Sudoers file modifications
SELECT * FROM file WHERE path = '/etc/sudoers' AND mtime > (strftime('%s', 'now') - 86400);
```

## Integration Points

### SIEM Integration

Forward osqueryd logs to SIEM platforms:

- **Splunk**: Use Splunk Add-on for osquery or universal forwarder
- **Elasticsearch**: Configure osqueryd to output JSON logs, ingest with Filebeat
- **Sentinel**: Stream logs via Azure Monitor Agent or custom ingestion
- **QRadar**: Use QRadar osquery app or log source extension

Configure osqueryd result logging:
```json
{
  "options": {
    "logger_plugin": "filesystem",
    "logger_path": "/var/log/osquery",
    "disable_logging": false
  }
}
```

### EDR/XDR Integration

Combine with endpoint detection:
- Correlate osquery results with EDR alerts
- Use osquery for EDR alert enrichment and investigation
- Deploy osquery packs based on EDR threat intelligence
- Augment EDR telemetry with custom osquery tables

### Threat Intelligence Enrichment

Enrich findings with threat intel:
- Query file hashes against VirusTotal, MISP, or threat feeds
- Match network indicators with IOC databases
- Tag findings with MITRE ATT&CK techniques
- Generate hunting hypotheses from threat reports

## Troubleshooting

### Issue: osquery Not Finding Expected Results

**Solution**: Verify table availability and platform compatibility
- Check table schema: `osqueryi ".schema processes"`
- List available tables: `osqueryi ".tables"`
- Review platform-specific tables in [references/platform-differences.md](references/platform-differences.md)
- Some tables require specific osquery versions or kernel features

### Issue: High Resource Consumption

**Solution**: Optimize query performance and scheduling
- Use indexed columns in WHERE clauses (pid, uid, path)
- Avoid unbounded queries without filters
- Reduce osqueryd query frequency in osquery.conf
- Limit result set sizes with LIMIT clause
- Monitor with: `SELECT * FROM osquery_info; SELECT * FROM osquery_schedule;`

### Issue: Permission Denied Errors

**Solution**: Ensure proper privilege escalation
- Run osqueryi with sudo/admin privileges: `sudo osqueryi`
- Some tables require root access (kernel_modules, process_memory_map)
- Check file permissions on osqueryd configuration files
- Review SELinux/AppArmor policies blocking osquery

## Best Practices

1. **Document Queries**: Maintain query library with descriptions and expected results
2. **Test Before Production**: Validate queries in lab before running on production systems
3. **Minimize Scope**: Use WHERE clauses to limit query scope and reduce performance impact
4. **Export Results**: Save query output for evidence preservation (`--json` or `--csv` flags)
5. **Correlate Findings**: Join multiple tables for comprehensive artifact analysis
6. **Version Control**: Track osquery configuration and query packs in Git
7. **Monitor Performance**: Watch osqueryd CPU/memory usage during scheduled queries
8. **Update Regularly**: Keep osquery updated for latest table schemas and security patches

## MITRE ATT&CK Coverage

osquery enables detection and investigation of techniques across the ATT&CK matrix:

- **Initial Access**: Detect suspicious services and scheduled tasks (T1053)
- **Execution**: Monitor process creation and command-line arguments (T1059)
- **Persistence**: Identify registry modifications, cron jobs, startup items (T1547, T1053)
- **Privilege Escalation**: Find SUID binaries, sudo abuse, service creation (T1548, T1543)
- **Defense Evasion**: Detect process injection, file deletion, timestomping (T1055, T1070)
- **Credential Access**: Hunt for credential dumping tools and access (T1003, T1552)
- **Discovery**: Track system enumeration activities (T1082, T1083, T1057)
- **Lateral Movement**: Monitor remote service creation and authentication (T1021)
- **Collection**: Detect archive creation and data staging (T1560, T1074)
- **Exfiltration**: Identify unusual network connections and data transfers (T1041)

See [references/mitre-attack-queries.md](references/mitre-attack-queries.md) for technique-specific detection queries.

## References

- [osquery GitHub Repository](https://github.com/osquery/osquery)
- [osquery Schema Documentation](https://osquery.io/schema/)
- [osquery Deployment Guide](https://osquery.readthedocs.io/en/stable/deployment/)
- [osquery SQL Reference](https://osquery.readthedocs.io/en/stable/introduction/sql/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
