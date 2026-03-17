---
name: pfsense-dnsmasq-interface-binding
description: |
  Restrict pfSense dnsmasq (DNS Forwarder) to specific interfaces to free port 53 on
  other interfaces for port forwarding. Use when: (1) pfSense blocks port 53 NAT port
  forward because dnsmasq is listening on *:53, (2) need to forward DNS from WAN to an
  internal DNS server while preserving client source IPs, (3) dnsmasq shows *:53 in
  sockstat despite --listen-address flags, (4) pfSense loses DNS resolution after
  restricting dnsmasq interfaces, (5) NAT rdr rules for port 53 silently fail to
  generate in /tmp/rules.debug.
author: Claude Code
version: 1.0.0
date: 2026-02-17
---

# pfSense dnsmasq Interface Binding for DNS Port Forwarding

## Problem
pfSense's dnsmasq (DNS Forwarder) binds to `*:53` by default. This prevents creating
NAT port forward rules for port 53 — pfSense silently skips generating the pf `rdr`
directive. You need to restrict dnsmasq to specific interfaces to free port 53 on other
interfaces (e.g., WAN) for forwarding to an internal DNS server.

## Context / Trigger Conditions
- Attempting to create a NAT port forward for port 53 on the WAN interface
- Port forward rule saves to config.xml but `pfctl -sn` shows no corresponding `rdr` rule
- `sockstat -4 | grep ":53"` shows `dnsmasq` on `*:53`
- Goal: Forward DNS queries from one network to an internal DNS server (e.g., Technitium)
  while preserving client source IPs (no masquerading)

## Solution

### Step 1: Bind dnsmasq to specific interfaces

Set the interface field in pfSense's dnsmasq config:

```php
ssh admin@10.0.20.1 'php -r '"'"'
require_once("config.inc");
require_once("service-utils.inc");
global $config;
$config = parse_config(true);
$config["dnsmasq"]["interface"] = "lan,opt1";  // Only LAN and OPT1, NOT wan
write_config("Bind dnsmasq to LAN and OPT1 only");
'"'"''
```

This adds `--listen-address=<IP>` flags to dnsmasq but does NOT change socket binding.

### Step 2: Add bind-dynamic (CRITICAL)

Without `bind-dynamic`, dnsmasq still binds the socket to `*:53` even with
`--listen-address` flags. The `--listen-address` only controls which queries get
responses, not the actual socket binding.

```php
ssh admin@10.0.20.1 'php -r '"'"'
require_once("config.inc");
require_once("service-utils.inc");
global $config;
$config = parse_config(true);
$existing = base64_decode($config["dnsmasq"]["custom_options"]);
if (strpos($existing, "bind-dynamic") === false) {
    $existing = "bind-dynamic\n" . $existing;
    $config["dnsmasq"]["custom_options"] = base64_encode($existing);
    write_config("Add bind-dynamic to restrict dnsmasq socket binding");
}
'"'"''
```

### Step 3: Add localhost listen address (CRITICAL)

pfSense's own `resolv.conf` points to `127.0.0.1`. Without this, pfSense itself
loses DNS resolution after the interface restriction.

```php
# Add to custom_options (base64-encoded in config):
listen-address=127.0.0.1
```

### Step 4: Restart dnsmasq

```php
services_dnsmasq_configure();
```

### Step 5: Verify binding

```bash
sockstat -4 | grep ":53 "
# Should show specific IPs, not *:53:
# 127.0.0.1:53
# 10.0.10.1:53  (lan)
# 10.0.20.1:53  (opt1)
# NOT 192.168.1.2:53 (wan)
```

### Step 6: Add the port forward rule

**Critical format note**: The `source` field must use `array("any" => "")`, NOT
`array("network" => "192.168.1.0/24")`. The CIDR source format silently fails to
generate the pf `rdr` directive.

```php
ssh admin@10.0.20.1 'php -r '"'"'
require_once("config.inc");
require_once("filter.inc");
require_once("shaper.inc");
global $config;
$config = parse_config(true);

$rule = array(
    "source" => array("any" => ""),           // MUST be "any", not CIDR
    "destination" => array(
        "network" => "wanip",
        "port" => "53"
    ),
    "ipprotocol" => "inet",
    "protocol" => "udp",
    "target" => "10.0.20.204",                // Internal DNS server
    "local-port" => "53",
    "interface" => "wan",
    "associated-rule-id" => "pass",
    "descr" => "DNS to internal DNS (preserve client IP)",
    "created" => array("time" => (string)time(), "username" => "admin"),
    "updated" => array("time" => (string)time(), "username" => "admin")
);
array_unshift($config["nat"]["rule"], $rule);
write_config("Add DNS port forward");
filter_configure();
'"'"''
```

### Step 7: Verify the redirect rule

```bash
pfctl -sn | grep "domain\|:53"
# Should show: rdr pass on vtnet0 inet proto udp from any to 192.168.1.2 port = domain -> 10.0.20.204
```

## Verification

1. pfSense own DNS: `nslookup google.com 127.0.0.1` (from pfSense shell)
2. Internal DNS: `nslookup google.com 10.0.20.1` (from LAN/OPT1 clients)
3. Port forward: `dig @192.168.1.2 example.com` (from WAN-side client)
4. Client IP: Check DNS server logs — should show real client IP, not pfSense IP

## Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Missing `bind-dynamic` | sockstat shows `*:53`, port forward still blocked | Add `bind-dynamic` to custom_options |
| Missing `listen-address=127.0.0.1` | pfSense loses all DNS resolution | Add to custom_options |
| Source `"network" => "CIDR"` in NAT rule | Rule saves to config but no `rdr` in `pfctl -sn` | Use `"any" => ""` instead |
| Using local `$config` variable | Config not persisted after PHP exit | Always use `global $config` |
| Not calling `filter_configure()` | Rule in config.xml but not in pf | Call after `write_config()` |
| Custom options not base64 | dnsmasq fails to start | pfSense stores custom_options as base64 |

## Notes
- `bind-dynamic` is preferred over `bind-interfaces` because it handles interfaces that
  come up after dnsmasq starts (e.g., VPN tunnels)
- The pf `rdr` rule is a redirect, not masquerade — source IP is preserved
- dnsmasq custom_options in pfSense config.xml are base64-encoded
- Check `/tmp/rules.debug` for the generated pf ruleset (before loading into pf)
- Use `pfctl -sn` to see rules actually loaded in the running firewall

## See also
- `pfsense` — General pfSense management skill
- `k8s-ndots-search-domain-nxdomain-flood` — Related DNS optimization
