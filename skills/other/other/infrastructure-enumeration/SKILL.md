---
name: infrastructure-enumeration
description: >
  Enumeration of infrastructure services: DNS, SMTP, SNMP, IPMI, NFS,
  TFTP, RPC/MSRPC, and HTTP/HTTPS surface detection. Checks zone
  transfers, open relays, default community strings, cipher zero, NFS
  exports, and web technology fingerprinting. Use after network-recon
  identifies infrastructure ports.
keywords:
  - DNS zone transfer
  - SMTP relay
  - SNMP community string
  - IPMI cipher zero
  - NFS no_root_squash
  - TFTP
  - RPC null session
  - HTTP tech detect
  - snmpwalk
  - onesixtyone
  - showmount
tools:
  - nmap
  - snmpwalk
  - onesixtyone
  - dnsrecon
  - smtp-user-enum
  - httpx
opsec: medium
---

# Infrastructure Enumeration

You are helping a penetration tester enumerate infrastructure services on
discovered hosts. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.
When present:
- Print `[infrastructure-enumeration] Activated → <target>` on activation.
- Save significant output to `engagement/evidence/` with descriptive filenames
  (e.g., `dns-zone-transfer-10.10.10.5.txt`, `snmp-walk-10.10.10.20.txt`).

## Scope Boundary

This skill covers **infrastructure service enumeration only** — misconfigs,
default credentials, and info disclosure on non-web, non-AD services, plus
surface-level HTTP/HTTPS tech detection.

**Out of scope — route instead:**
- Deep web application testing
- Kerberos/LDAP/domain enumeration
- Credential brute force
- Exploitation of discovered vulns → return to orchestrator

Do not load or execute another skill. Stay in methodology.

## State Management

Call `get_state_summary()` to read current engagement state. Use it to:
- Skip services already enumerated
- Leverage existing credentials (e.g., SNMP community strings already found)
- Check Blocked section for previous failures

**Interim writes** — write critical discoveries immediately via state-interim:
- SNMP community string → `add_credential(username="", secret="<community>", secret_type="other", source="SNMP on <host>")`
- SNMP network interfaces revealing subnets → `add_pivot(source="SNMP on <host>", destination="<subnet>", method="SNMP interface enumeration")`
- LDAP signing not required → `add_vuln(title="LDAP signing not required on <host>", host="<host>", vuln_type="ldap-signing", severity="medium")`
- LDAP anonymous bind → `add_vuln(title="LDAP anonymous bind on <host>", host="<host>", vuln_type="null-session", severity="medium")`
- Domain name from rootDSE/LDAP → `add_pivot(source="LDAP rootDSE on <host>", destination="<domain>", method="LDAP enumeration")`
- NFS no_root_squash → `add_vuln(title="NFS no_root_squash on <host>:<share>", host="<host>", vuln_type="nfs-misconfig", severity="high")`
- IPMI cipher 0 → `add_vuln(title="IPMI cipher zero on <host>", host="<host>", vuln_type="ipmi-cipher-zero", severity="critical")`
- DNS zone transfer → `add_vuln(title="DNS zone transfer on <host>", host="<host>", vuln_type="zone-transfer", severity="medium")`
- SMTP open relay → `add_vuln(title="SMTP open relay on <host>", host="<host>", vuln_type="open-relay", severity="high")`

Report all findings in your return summary.

## Prerequisites

- Network access to target host(s)
- Port list from orchestrator or network-recon (open TCP/UDP ports)
- For SNMP/IPMI/TFTP: UDP scan results (UDP-only services)

**Only run sections for ports that are actually open.** Skip sections entirely
if the relevant ports are not open — do not scan for ports yourself.

## DNS — Port 53

```bash
nmap -sV -p53 --script dns-zone-transfer,dns-cache-snoop,dns-nsid TARGET_IP

# Zone transfer (requires domain name — check state or reverse DNS)
dig axfr @TARGET_IP target.com
host -l target.com TARGET_IP

# Reverse DNS sweep (discover hostnames on the subnet)
dnsrecon -r 10.10.10.0/24 -n TARGET_IP

# Subdomain brute force
dnsenum --dnsserver TARGET_IP --enum target.com \
  -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

**Quick wins:** Zone transfer (full DNS dump), wildcard records, internal
hostnames revealing naming conventions and services.

## SMTP — Ports 25/465/587

```bash
nmap -sV -p25,465,587 --script smtp-commands,smtp-enum-users,smtp-open-relay,smtp-vuln* TARGET_IP

# User enumeration via VRFY/RCPT/EXPN
smtp-user-enum -M VRFY -U users.txt -t TARGET_IP
smtp-user-enum -M RCPT -U users.txt -t TARGET_IP
smtp-user-enum -M EXPN -U users.txt -t TARGET_IP
```

**Quick wins:** Open relay (send mail as anyone), user enumeration (valid
accounts), NTLM auth info leak (`MAIL FROM:<> AUTH NTLM` reveals internal
hostname/domain).

## RPC/MSRPC — Ports 111/135

```bash
# Linux RPC (port 111)
rpcinfo -p TARGET_IP
showmount -e TARGET_IP  # NFS preview

# Windows MSRPC (port 135)
rpcclient -U "" -N TARGET_IP
rpcclient -U "" -N TARGET_IP -c "enumdomusers;enumdomgroups;getdompwinfo"
rpcdump.py TARGET_IP | grep -E "Protocol|Provider"
```

**Quick wins:** Null session user enumeration, NFS shares via rpcinfo,
MSRPC endpoint map revealing internal services.

## LDAP — Ports 389/636/3268

```bash
# rootDSE query (always allowed per RFC)
ldapsearch -x -H ldap://TARGET_IP -b "" -s base namingContexts

# Anonymous directory read
ldapsearch -x -H ldap://TARGET_IP -b "DC=domain,DC=local" \
  "(objectClass=user)" sAMAccountName description memberOf

nmap -sV -p389,636,3268 --script ldap-rootdse,ldap-search TARGET_IP
```

**Quick wins:** Anonymous bind, password in description, rootDSE domain
disclosure, LDAP signing not required.

→ STOP and return with: what was achieved, new findings, context for next steps.
domain name from rootDSE, anonymous bind results.

## Kerberos — Port 88

DO NOT enumerate. Kerberos enumeration and ticket requests belong to AD skills.

→ STOP and return with: what was achieved, new findings, context for next steps.
domain name, any credentials found.

## HTTP/HTTPS — Ports 80/443/8080/8443

```bash
# HTTP enumeration
nmap -sV -p80,443,8080,8443 \
  --script http-title,http-headers,http-methods,http-robots.txt,http-enum TARGET_IP

# Tech stack identification
whatweb TARGET_IP
httpx -u TARGET_IP -ports 80,443,8080,8443 \
  -title -tech-detect -status-code -follow-redirects
```

**Quick wins:** Default credentials on management interfaces (Tomcat, Jenkins,
phpMyAdmin), exposed admin panels, directory listing, `.git`/`.svn` exposed,
phpinfo(), server-status/server-info.

→ STOP and return with: what was achieved, new findings, context for next steps.
URL, tech stack, interesting headers or findings. Do not execute web fuzzing
or directory brute force inline.

## SNMP — Ports 161/162 (UDP)

```bash
# Community string brute force
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt TARGET_IP

# Walk with found community string
snmpwalk -v2c -c public TARGET_IP .1
snmpwalk -v2c -c public TARGET_IP NET-SNMP-EXTEND-MIB::nsExtendOutputFull

# Bulk walk for speed
snmpbulkwalk -v2c -c public TARGET_IP .1 > snmp_full_dump.txt

# Specific high-value OIDs
snmpwalk -v2c -c public TARGET_IP 1.3.6.1.4.1.77.1.2.25  # Windows users
snmpwalk -v2c -c public TARGET_IP 1.3.6.1.2.1.25.4.2.1.2  # Running processes
snmpwalk -v2c -c public TARGET_IP 1.3.6.1.2.1.6.13.1.3    # TCP connections
snmpwalk -v2c -c public TARGET_IP 1.3.6.1.2.1.25.6.3.1.2  # Installed software
```

**Quick wins:** Default `public`/`private` community strings, user enumeration,
running process list, installed software, network interfaces revealing new
subnets, Net-SNMP Extend RCE (check `nsExtendOutputFull`).

## IPMI — Port 623 (UDP)

```bash
nmap -sU -p623 --script ipmi-version,ipmi-cipher-zero TARGET_IP
ipmitool -I lanplus -H TARGET_IP -U "" -P "" user list
# RAKP hash disclosure: msf auxiliary/scanner/ipmi/ipmi_dumphashes
```

**Quick wins:** Cipher 0 (auth bypass), default creds (admin/admin,
ADMIN/ADMIN), RAKP hash disclosure for offline cracking.

## NFS — Port 2049

```bash
showmount -e TARGET_IP
nmap -sV -p2049 --script nfs-ls,nfs-showmount,nfs-statfs TARGET_IP

# Mount and explore (requires sudo — note in return if unavailable)
sudo mount -t nfs TARGET_IP:/share /mnt/nfs -o nolock
ls -la /mnt/nfs/
```

**Quick wins:** World-readable shares (credential files, configs), writable
shares (SUID binary plant), no_root_squash (root file injection for privesc).

## TFTP — Port 69 (UDP)

```bash
nmap -sU -p69 --script tftp-enum TARGET_IP

# Grab common files
tftp TARGET_IP -c get /etc/passwd
tftp TARGET_IP -c get running-config
tftp TARGET_IP -c get startup-config
```

**Quick wins:** Open TFTP with config files (router/switch configs),
credential files, firmware images.

## Escalate or Pivot

After enumeration, return to the orchestrator with routing recommendations:
- **Web services** (pass URLs, tech stack)
- **AD services** (LDAP/Kerberos) (pass DC IP, domain, anon bind results)
- **SNMP RCE** (Net-SNMP Extend) → note in return for orchestrator
- **NFS no_root_squash** → note for privesc chaining if shell access exists
- **IPMI hashes** (pass hash type and values)
- **Credentials found** → list all for orchestrator to record and test
- **New subnets/hosts** → list for orchestrator to add as targets

## Troubleshooting

- **SNMP timeouts**: UDP — firewalls silently drop. Note "SNMP filtered/no
  response" rather than "no service."
- **DNS zone transfer denied**: Expected on most servers. Proceed to reverse
  DNS sweep and subdomain brute force.
- **NFS mount denied**: Exports may restrict by source IP. Note the export
  list and restrictions — orchestrator may route from a pivot host.
- **SMTP anti-enumeration**: Server returns identical responses for valid and
  invalid users. Note and move on.
- **rpcclient null session denied**: Note as blocked. Try authenticated access
  if credentials exist in state.
