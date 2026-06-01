---
name: firewall-appliance
description: >
  · Manage OPNsense/pfSense via SSH: pfctl, pf rules, CARP, CrowdSec, pfBlockerNG. Triggers: 'opnsense', 'pfsense', 'pfctl', 'CARP', 'configctl'. Not for Linux firewalls.
license: MIT
compatibility: "Requires SSH access to OPNsense or pfSense appliance"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-30"
  effort: high
  argument_hint: "[platform-or-task-or-host]"
---

# Firewall Appliance: OPNsense & pfSense Management

Manage, troubleshoot, and harden OPNsense and pfSense firewalls via SSH. Both are FreeBSD-based,
pf-powered firewall distributions - most concepts, commands, and patterns apply to both.

**Target versions** (May 2026):
- OPNsense CE: 26.1.7 (current Community Edition stable, "Witty Woodpecker"; CE ships odd quarters .1/.7). Business Edition is 26.4.x (even quarters .4/.10) - do not quote the BE number as the CE version
- pfSense CE: 2.8.1 / pfSense Plus: 26.03
- CrowdSec: v1.7.7

## When to use

- Managing or troubleshooting OPNsense and pfSense firewalls over SSH
- Reviewing pf rules, NAT, CARP, Unbound, WireGuard, CrowdSec, or pfBlockerNG on these appliances
- Configuring VLANs, CARP HA failover, or interface assignments on firewall appliances
- Debugging connectivity between networks or VLANs routed through OPNsense/pfSense
- Hardening BSD firewall appliances and validating safe remote-change workflows

## When NOT to use

- Linux networking, reverse proxies, VPN setup, or nftables work outside firewall appliances - use **networking**
- Cloud firewall rules, WAF configuration, or AWS/GCP/Azure network ACLs - use **networking** or the relevant IaC skill (**terraform**, **ansible**)
- General shell scripting or local shell behavior outside the BSD firewall context - use **command-prompt**
- Fleet-wide configuration management via playbooks - use **ansible**
- Offensive testing, exploitation, or post-exploitation - use **lockpick**
- Application-level security review or dependency scanning - use **security-audit**

## AI Self-Check

Before returning any firewall commands, verify:

- [ ] Platform confirmed (OPNsense vs pfSense) - commands differ between them
- [ ] No commands that could lock out SSH or management access
- [ ] Config backup taken (or reminded) before destructive changes
- [ ] `pfctl` rules tested with `-n` (dry run) before applying
- [ ] Service names correct for the target platform (`configctl` vs `service`)
- [ ] Plugin names use correct prefix (`os-*` for OPNsense, unprefixed for pfSense)
- [ ] CARP changes target the master node, not the backup
- [ ] Shell syntax is POSIX sh (heredoc), not bash/zsh (csh/tcsh is the default shell on both)
- [ ] No firmware or plugin updates without explicit user confirmation
- [ ] Blast radius stated for any change affecting network connectivity
- [ ] DNS impact considered - changes to Unbound, DHCP, or firewall rules on port 53 can
  break name resolution for all clients on affected VLANs
- [ ] CrowdSec/pfBlockerNG checked when diagnosing blocks - bans look identical to firewall
  drops from the client side
- [ ] VLAN interface assigned before adding rules - unassigned VLANs pass no traffic through
  the firewall even if the trunk is tagged correctly
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Platform/version checked**: OPNsense, pfSense, FreeBSD, pf, and plugin commands match the appliance version
- [ ] **Lockout path prevented**: remote firewall changes preserve management access and rollback

---

## Performance

- Prefer rule ordering that rejects high-volume unwanted traffic early and keeps expensive inspection scoped.
- Use aliases/tables for large address sets instead of expanding repetitive rules.
- Check state table, DNSBL, IDS/IPS, and plugin load before blaming WAN latency.


---

## Best Practices

- Export configuration before rule, NAT, VPN, CARP, or package changes.
- Make HA changes one node at a time and verify CARP state before touching the peer.
- Keep emergency console or out-of-band access available for management-plane changes.


## Workflow

### Step 1: Detect platform

If the platform is not obvious from context, **ask the user** which one they're running before
issuing commands. Identify the target device explicitly - never assume which firewall you're
talking to. Key differences at a glance:

| | OPNsense | pfSense |
|---|---|---|
| Base OS | FreeBSD (migrated from HardenedBSD in 2021) | FreeBSD |
| Config path | `/conf/config.xml` | `/cf/conf/config.xml` |
| Service control | `configctl service restart <svc>` | `pfSsh.php playback svc restart <svc>` or `service <svc> restart` |
| Plugin prefix | `os-<name>` (e.g., `os-wireguard`) | No prefix (e.g., `pfSense-pkg-WireGuard`) |
| PHP shell | N/A | `pfSsh.php` (interactive PHP shell) |
| Quick rule add | N/A | `easyrule pass wan tcp <src> <dst> <port>` |
| IP blocking | CrowdSec (`os-crowdsec`) | pfBlockerNG |
| Root shell | `csh` | `tcsh` (same heredoc workaround applies) |
| IDS/IPS config | `/tmp/suricata_*.log`, eve.json | `/var/log/suricata/suricata.log`, eve.json |
| Firmware CLI | `configctl firmware check/status` | `pkg-static update` + GUI |
| Template engine | `configd` + `configctl template` | PHP-generated configs |
| REST API | Yes (`/api/`, key/secret auth) | Yes (similar, different endpoints) |
| Licensing | Free, open source | CE: free but slower updates; Plus: $129/yr on non-Netgate HW |
| Release cadence | Bi-weekly, fixed schedule | Irregular, Netgate hardware prioritized |

**2026 status**: OPNsense is the clear choice for new deployments. pfSense CE gets slower updates and zero priority; Plus costs $129/year on non-Netgate hardware. Migration from pfSense to OPNsense has no automated path - expect ~60% clean config transfer, manual rebuild for NAT rules, VPN, and DNS forwarder settings.

**When platform is unknown**, these commands work on both:
```
pfctl -sr                # firewall rules
pfctl -ss                # state table
ifconfig                 # interfaces
pkg info                 # installed packages
netstat -rn              # routing table
sockstat -4l             # listening sockets
```

### Step 2: Back up config

Before any change that modifies rules, services, plugins, or firmware:
- OPNsense: `configctl firmware backup` or GUI export (System > Configuration > Backups)
- pfSense: GUI export (Diagnostics > Backup & Restore) or copy `/cf/conf/config.xml`
- For major upgrades on virtualized firewalls, pair config backup with a hypervisor snapshot

Skip this step only for read-only operations (diagnostics, log review, status checks).

### Step 3: Execute the task

Apply changes using the platform-appropriate commands. Refer to the domain sections below
and the reference files for specifics. For any change that affects connectivity:
- Test `pfctl` rules with `-n` (dry run) before applying
- State the blast radius ("this will drop all VPN tunnels for ~30s")
- On HA pairs, always change on the master node and let XMLRPC sync propagate

### Step 4: Verify

After every change, confirm the firewall is healthy:
- Connectivity: can you still reach the device? Can clients reach the internet?
- Logs: check `/var/log/filter.log`, service logs, and CrowdSec/Suricata if active
- Service status: `configctl service list` (OPNsense) or `service -e` (pfSense)
- State table: `pfctl -si | grep entries` - watch for unexpected drops or state exhaustion

---

## Quick Task Procedures

### Creating a firewall rule (VLAN to server)

1. Identify the interface the traffic originates from (e.g., `opt1` for VLAN 50)
2. **Confirm the VLAN interface is assigned**: `ifconfig` must show the VLAN interface UP. If the VLAN is not assigned to an OPNsense/pfSense interface yet (Interfaces > Assignments), it cannot have rules - assign it first.
3. **Check existing rules**: `pfctl -sr | grep <iface>` - new interfaces have no rules (implicit deny all). Confirm the baseline before adding anything so you know exactly what you're changing.
4. Create aliases for source subnet and destination server (keeps rules readable):
   - OPNsense API: `curl -X POST -u key:secret https://<fw>/api/firewall/alias/addItem -d '{"alias":{"name":"WebServer","type":"host","content":"10.0.1.100"}}'`
   - OPNsense CLI: `configctl template reload OPNsense/Filter` (after editing alias via API or XML). To verify the alias was created: `configctl template list | grep Alias`, then confirm with `pfctl -t WebServer -T show`.
   - pfSense: `easyrule` doesn't support aliases - use GUI or edit `/cf/conf/config.xml` directly
5. Add a pass rule on the **VLAN interface** (not WAN - pf evaluates rules on the interface where traffic enters): source = alias, destination = server alias, port = 443
6. Place the allow rule above any block-all rule for that interface (OPNsense/pfSense interface rules use `quick` by default, so the FIRST matching rule wins - put the specific allow above the broad block)
7. Test: `pfctl -n -f /tmp/rules.debug` (OPNsense) to dry-run before applying
8. Apply: `configctl filter reload` (OPNsense) or `pfSsh.php playback svc restart filter` (pfSense)
9. Verify: `pfctl -sr | grep <alias>` to confirm the rule is active

### Creating a block rule (isolate IoT VLAN)

Block IoT devices from reaching internal networks while allowing internet access:

1. Identify the IoT VLAN interface (e.g., `opt3` for VLAN 30)
2. Create an alias for RFC1918 ranges: name `RFC1918`, type `Network`, content `10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16`
3. Add a **block** rule on the IoT interface: source = IoT subnet, destination = `RFC1918` alias, action = block. This prevents IoT from reaching any internal network.
4. Add a **pass** rule below it: source = IoT subnet, destination = any, ports = 53 (DNS), 443 (HTTPS). This allows internet access for the permitted services.
5. Rule order matters: with `quick` (the OPNsense/pfSense default) the FIRST matching rule wins, so the RFC1918 block must come before the broad pass rule - otherwise the pass matches first and lets the traffic through.
6. Test and apply as above: `pfctl -n -f /tmp/rules.debug`, then `configctl filter reload`

### Troubleshooting connectivity after VLAN changes

Work through these steps in order. **Do not skip ahead or assume the root cause** - each step eliminates one layer. The most common failure is a missing outbound NAT rule, not a firewall rule. Also check CrowdSec (`cscli decisions list`) and Suricata early - their blocks look identical to firewall drops from the client side.

**Prerequisite**: the VLAN must be assigned to a firewall interface before it can have rules, DHCP, or NAT. In OPNsense: Interfaces > Assignments > add the VLAN, then enable it and set its IP. In pfSense: Interfaces > Interface Assignments. An unassigned VLAN passes no traffic through the firewall even if the parent trunk is tagged correctly.

1. **Interface assigned and UP?** `ifconfig` - is the VLAN interface listed and UP? If not: assign it (see prerequisite above). If listed but DOWN: enable it in the GUI or check the parent interface.
2. **Blocklist check**: `cscli decisions list` (OPNsense CrowdSec) or check pfBlockerNG deny logs (pfSense) - CrowdSec and pfBlockerNG bans look identical to firewall drops from the client side. Clear false positives before digging into rules.
3. **Services running?** `configctl service list` (OPNsense) or `service -e` (pfSense) - confirm DHCP, DNS (Unbound), and the packet filter are running. A stopped DHCP server on the new VLAN means clients never get an IP.
4. **Rules present?** `pfctl -sr` - any pass rules on the new VLAN interface? New interfaces have no rules by default (deny all).
5. **NAT configured?** Check outbound NAT rules include the new VLAN subnet. On OPNsense: Firewall > NAT > Outbound. Missing outbound NAT is the #1 cause of "VLAN can't reach internet."
6. **DNS working?** `drill google.com @<firewall-ip>` from a VLAN client. If this fails but ping to 8.8.8.8 works, it's a DNS issue, not a firewall rule.
7. **Packet capture**: `tcpdump -ni <vlan-iface> host <client-ip>` - are packets arriving at the firewall?
   - **Reading tcpdump output**: each line shows `timestamp src > dst: proto`. Look for: (a) request packets from the client arriving on the VLAN interface, (b) reply packets going back. If you see requests but no replies, the firewall is blocking or NAT is missing. If you see no packets at all, the issue is below the firewall - check VLAN tagging, trunk config, and switch ports. Use `-v` for header details or `-X` for payload hex when deeper inspection is needed.
8. If packets arrive but no response: the rule or NAT is the problem. If no packets: the VLAN trunk, switch tagging, or interface assignment is wrong - check the physical/virtual layer before touching firewall config.

---

## FreeBSD Mental Model

Read `references/platform-and-operations.md` for the detailed FreeBSD shell model, key commands,
config system, REST API, IPv6 gotchas, SOPs, and recovery procedures.

- Treat both platforms as FreeBSD appliances, not Linux hosts.
- For anything beyond trivial SSH one-liners, prefer piping a POSIX `sh` heredoc instead of fighting `csh` or `tcsh`.
- Guard non-zero informational commands with `; true` when running checks in parallel.

## Operations and Common Tasks

- Identify the target device explicitly before changing anything.
- Back up config before risky changes or upgrades.
- Check plugin or package layers early because they often explain traffic behavior that looks like a firewall-rule problem.
- Treat firmware, plugin, backup, and HA work as operational procedures, not casual single commands.
- Use `references/plugins.md` for plugin specifics and `references/hardening.md` for hardening and CARP guidance.

---

## Reference Files

- `references/platform-and-operations.md` - FreeBSD shell model, key commands, config system,
  REST API, IPv6 gotchas, SOPs, and recovery procedures (both platforms)
- `references/plugins.md` - operational guidance for common OPNsense plugins (CrowdSec,
  WireGuard, Suricata, HAProxy, ACME, FRR, etc.). For pfSense package equivalents, map
  concepts using the platform comparison table above.
- `references/hardening.md` - comprehensive hardening checklist. OPNsense-focused but most
  items apply to pfSense with equivalent settings in its GUI/config.

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** FIREWALL-APPLIANCE
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/firewall-appliance/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **networking** - for Linux reverse proxies, VPNs, DNS, nftables, and cloud network ACLs (AWS/GCP/Azure security groups, WAF rules) outside BSD firewall appliances
- **terraform** - for provisioning and managing cloud firewall rules, WAF policies, and network ACLs as infrastructure-as-code
- **ansible** - for fleet-wide firewall automation or playbook-based configuration management
- **command-prompt** - for general shell scripting and local shell behavior; this skill covers the FreeBSD firewall context
- **security-audit** - for defensive security review of application code and supply chain, rather than firewall administration
- **lockpick** - for authorized offensive testing and post-exploitation, not defensive firewall operations

---

## Rules

These exist because bricking a firewall remotely means driving to wherever it is.

- **Never** modify rules that could lock out SSH access. If the change touches the SSH port or the
  management interface, triple-check the rule order and confirm with the user.
- **Never** disable the LAN interface or change its IP without explicit confirmation and a rollback
  plan.
- **Never** apply firmware or plugin updates without asking first - updates can reboot the device
  and may require physical console access if something goes wrong.
- **Always** confirm destructive changes: rule deletions, service disables, plugin removals,
  state table flushes (`pfctl -Fa`).
- **Estimate blast radius**: if a change could cause network disruption beyond the target device,
  warn the user with specifics (e.g., "this will drop all VPN tunnels for ~30s").
- **OPNsense CrowdSec**: don't delete decisions or bouncers without understanding why they exist.
  A ban that looks wrong might be catching a real attack.
- **pfSense pfBlockerNG**: don't disable feed lists without understanding what they block.
  Review the deny logs before removing feeds.
- **HA/CARP (both platforms)**: never make config changes directly on the backup node - XMLRPC
  sync from master will overwrite them. Always change on master and let sync propagate.
- **pfSense `easyrule`**: convenient but creates rules without descriptions. Document what you
  added and why. Consider using the GUI or config.xml for permanent rules instead.
