---
name: pfsense-nat-rule-creation
description: |
  Create NAT port forward rules on pfSense programmatically via PHP/SSH.
  Use when: (1) adding port forwards for new K8s services, (2) NAT rules
  added via PHP don't appear in pfctl output, (3) config_read_array() throws
  "undefined function" error, (4) destination "wanip" not working in NAT rules,
  (5) rules saved to config.xml but not loaded into pfctl. Covers the correct
  PHP array structure, config API differences between pfSense versions, and
  the required pfctl reload step.
author: Claude Code
version: 1.0.0
date: 2026-02-21
---

# pfSense NAT Rule Creation via PHP

## Problem
Creating NAT port forward rules on pfSense programmatically via SSH/PHP has
multiple gotchas around the config API, rule structure, and rule loading.

## Context / Trigger Conditions
- Adding a port forward for a new Kubernetes service (e.g., TURN, game server)
- Using `ssh admin@10.0.20.1` + PHP to automate pfSense config
- NAT rules don't appear in `pfctl -sn` after `write_config()` + `filter_configure()`
- `config_read_array()` throws "Call to undefined function"
- Rules saved to config.xml but pfctl doesn't have them

## Solution

### Correct PHP for adding NAT rules

```php
<?php
require_once("config.inc");
require_once("filter.inc");
global $config;  // NOT config_read_array() — that doesn't exist in pfSense 2.7.x

$config["nat"]["rule"][] = array(
    "interface"          => "wan",
    "ipprotocol"         => "inet",          // Required! Must be "inet" for IPv4
    "protocol"           => "tcp/udp",       // Or "udp" or "tcp"
    "source"             => array("any" => ""),
    "destination"        => array(
        "network" => "wanip",               // Use "network" => "wanip", NOT "address" => "wanip"
        "port"    => "3478"                  // Single port or "start:end" for range
    ),
    "target"             => "10.0.20.200",   // Internal destination IP
    "local-port"         => "3478",          // Internal port (for ranges, just the start port)
    "descr"              => "My port forward",
    "associated-rule-id" => "pass"           // Auto-create firewall pass rule
);

write_config("Description for config history");
filter_configure();
```

### Key gotchas

1. **`config_read_array()` doesn't exist** in pfSense 2.7.x. Use `global $config` instead.

2. **Destination format**: Use `"network" => "wanip"`, NOT `"address" => "wanip"` or `"address" => "192.168.1.2"`. The `"network"` key with `"wanip"` tells pfSense to resolve the WAN IP dynamically.

3. **`ipprotocol` is required**: Must include `"ipprotocol" => "inet"` or rules won't generate in `/tmp/rules.debug`.

4. **Port ranges**: Use `"port" => "49152:49252"` for ranges. The `"local-port"` should be just the start port — pfSense maps the range automatically.

5. **Rules may not load immediately**: After `write_config()` + `filter_configure()`, rules appear in `/tmp/rules.debug` but may not be in pfctl until the next filter reload. Force with:
   ```bash
   pfctl -f /tmp/rules.debug
   ```

6. **SSH quoting**: The pfsense.py `php` command breaks on `\n` in strings. For multi-line PHP, write a `.php` file, `scp` it, and execute:
   ```bash
   scp script.php admin@10.0.20.1:/tmp/
   ssh admin@10.0.20.1 "php /tmp/script.php"
   ```

### Execution via pfsense.py

For simple single-line PHP (no newlines or backslashes):
```bash
python3 .claude/pfsense.py php 'require_once("config.inc"); ...; echo "Done";'
```

For complex scripts, use scp + ssh as above.

## Verification

```bash
# Check rules in config
ssh admin@10.0.20.1 "grep 'YOUR_PORT' /cf/conf/config.xml"

# Check generated pf rules
ssh admin@10.0.20.1 "grep 'YOUR_PORT' /tmp/rules.debug"

# Check active pfctl rules
python3 .claude/pfsense.py pfctl "-sn" | grep YOUR_PORT
```

## Notes
- Existing working NAT rules on this pfSense use the same structure (check WireGuard port 51820 as reference)
- The `associated-rule-id: pass` auto-creates a WAN firewall rule to allow the forwarded traffic
- pfSense applies NAT rules across ALL interfaces when using the web UI, but PHP-created rules only apply to the specified interface
- See also: `pfsense` skill for general pfSense management
