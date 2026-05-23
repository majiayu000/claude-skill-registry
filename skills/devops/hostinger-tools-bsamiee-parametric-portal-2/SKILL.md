---
name: hostinger-tools
type: complex
depth: base
user-invocable: false
description: >-
  Executes Hostinger API operations managing VPS instances, Docker Compose, DNS, domains, billing, firewalls, SSH keys, snapshots. Use when controlling
  virtual machines, containers, domain configuration, or hosting infrastructure.
---

# [H1][HOSTINGER-TOOLS]
>**Dictum:** *Unified interface reduces API complexity.*

<br>

Invokes Hostinger API through Python wrapper using `HOSTINGER_TOKEN` env var. Base URL: `https://developers.hostinger.com`.

[IMPORTANT] Zero-arg commands default to `page=1`, `limit=30`. Uses `--key value` flag syntax. Hostinger also provides an MCP server and n8n node for automation.

---
## [1][VPS_CORE]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-list
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-view --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-start --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-stop --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-restart --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-metrics --id 1196440 --from 2025-01-01 --to 2025-01-07
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-actions --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-action-view --id 1196440 --action-id 71183700
```

---
## [2][VPS_CONFIG]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-hostname-set --id 1196440 --hostname myserver.example.com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-hostname-reset --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-nameservers-set --id 1196440 --ns1 8.8.8.8 --ns2 8.8.4.4
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-password-set --id 1196440 --password "SecurePass123!"
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-panel-password-set --id 1196440 --password "PanelPass123!"
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-ptr-create --id 1196440 --ip-id 1154886 --domain mail.example.com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-ptr-delete --id 1196440 --ip-id 1154886
```

---
## [3][VPS_RECOVERY]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-recovery-start --id 1196440 --root-password "TempPass123!"
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-recovery-stop --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py vps-recreate --id 1196440 --template-id 1007 --password "NewPass123!"
```

---
## [4][DOCKER]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py docker-list --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py docker-view --id 1196440 --project myapp
uv run .claude/skills/hostinger-tools/scripts/hostinger.py docker-containers --id 1196440 --project myapp
uv run .claude/skills/hostinger-tools/scripts/hostinger.py docker-logs --id 1196440 --project myapp
uv run .claude/skills/hostinger-tools/scripts/hostinger.py docker-create --id 1196440 --project myapp --content "version: '3'..."
uv run .claude/skills/hostinger-tools/scripts/hostinger.py docker-start --id 1196440 --project myapp
uv run .claude/skills/hostinger-tools/scripts/hostinger.py docker-stop --id 1196440 --project myapp
uv run .claude/skills/hostinger-tools/scripts/hostinger.py docker-restart --id 1196440 --project myapp
uv run .claude/skills/hostinger-tools/scripts/hostinger.py docker-update --id 1196440 --project myapp
uv run .claude/skills/hostinger-tools/scripts/hostinger.py docker-delete --id 1196440 --project myapp
```

---
## [5][FIREWALL]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py firewall-list
uv run .claude/skills/hostinger-tools/scripts/hostinger.py firewall-view --id 12345
uv run .claude/skills/hostinger-tools/scripts/hostinger.py firewall-create --name "Web Server"
uv run .claude/skills/hostinger-tools/scripts/hostinger.py firewall-delete --id 12345
uv run .claude/skills/hostinger-tools/scripts/hostinger.py firewall-activate --firewall-id 12345 --vps-id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py firewall-deactivate --firewall-id 12345 --vps-id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py firewall-sync --firewall-id 12345 --vps-id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py firewall-rule-create --id 12345 --protocol SSH --port 22 --source any --source-detail any
uv run .claude/skills/hostinger-tools/scripts/hostinger.py firewall-rule-update --id 12345 --rule-id 67890 --protocol TCP --port 443 --source any --source-detail any
uv run .claude/skills/hostinger-tools/scripts/hostinger.py firewall-rule-delete --id 12345 --rule-id 67890
```

---
## [6][SSH_KEYS]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py ssh-key-list
uv run .claude/skills/hostinger-tools/scripts/hostinger.py ssh-key-create --name "MacBook" --key "ssh-ed25519 AAAA..."
uv run .claude/skills/hostinger-tools/scripts/hostinger.py ssh-key-delete --id 380228
uv run .claude/skills/hostinger-tools/scripts/hostinger.py ssh-key-attach --key-ids 380228 --vps-id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py ssh-key-attached --vps-id 1196440
```

---
## [7][SCRIPTS]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py script-list
uv run .claude/skills/hostinger-tools/scripts/hostinger.py script-view --id 12345
uv run .claude/skills/hostinger-tools/scripts/hostinger.py script-create --name "Setup" --content "#!/bin/bash\napt update"
uv run .claude/skills/hostinger-tools/scripts/hostinger.py script-update --id 12345 --name "Setup v2" --content "#!/bin/bash\napt upgrade"
uv run .claude/skills/hostinger-tools/scripts/hostinger.py script-delete --id 12345
```

---
## [8][SNAPSHOTS]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py snapshot-view --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py snapshot-create --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py snapshot-delete --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py snapshot-restore --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py backup-list --id 1196440
uv run .claude/skills/hostinger-tools/scripts/hostinger.py backup-restore --id 1196440 --backup-id 67890
```

---
## [9][DNS]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py dns-records --domain example.com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py dns-snapshots --domain example.com
```

---
## [10][DOMAINS]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-list
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-view --domain example.com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-check --domain example --tlds com,net,io
```

---
## [11][DOMAIN_EXTENDED]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-lock-enable --domain example.com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-lock-disable --domain example.com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-privacy-enable --domain example.com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-privacy-disable --domain example.com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-forwarding-view --domain example.com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-forwarding-create --domain example.com --redirect-url https://target.com --redirect-type 301
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-forwarding-delete --domain example.com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py domain-nameservers-set --domain example.com --ns1 ns1.hostinger.com --ns2 ns2.hostinger.com
```

---
## [12][WHOIS]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py whois-list
uv run .claude/skills/hostinger-tools/scripts/hostinger.py whois-list --tld com
uv run .claude/skills/hostinger-tools/scripts/hostinger.py whois-view --id 12345
uv run .claude/skills/hostinger-tools/scripts/hostinger.py whois-create --tld com --entity-type individual --country US --whois-details '{"first_name":"John"}'
uv run .claude/skills/hostinger-tools/scripts/hostinger.py whois-delete --id 12345
uv run .claude/skills/hostinger-tools/scripts/hostinger.py whois-usage --id 12345
```

---
## [13][BILLING]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py billing-catalog
uv run .claude/skills/hostinger-tools/scripts/hostinger.py billing-catalog --category VPS
uv run .claude/skills/hostinger-tools/scripts/hostinger.py billing-payment-methods
uv run .claude/skills/hostinger-tools/scripts/hostinger.py billing-payment-method-set-default --id 40404360
uv run .claude/skills/hostinger-tools/scripts/hostinger.py billing-payment-method-delete --id 40404360
uv run .claude/skills/hostinger-tools/scripts/hostinger.py billing-subscriptions
uv run .claude/skills/hostinger-tools/scripts/hostinger.py billing-subscription-cancel --id AzqaEWV5FiDYT4Ka3
uv run .claude/skills/hostinger-tools/scripts/hostinger.py billing-auto-renewal-enable --id AzqaEWV5FiDYT4Ka3
uv run .claude/skills/hostinger-tools/scripts/hostinger.py billing-auto-renewal-disable --id AzqaEWV5FiDYT4Ka3
```

---
## [14][HOSTING]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py hosting-orders-list
uv run .claude/skills/hostinger-tools/scripts/hostinger.py hosting-websites-list
uv run .claude/skills/hostinger-tools/scripts/hostinger.py hosting-website-create --domain mysite.com --order-id 12345
uv run .claude/skills/hostinger-tools/scripts/hostinger.py hosting-website-create --domain mysite.com --order-id 12345 --datacenter us
uv run .claude/skills/hostinger-tools/scripts/hostinger.py hosting-datacenters-list --order-id 12345
```

---
## [15][REFERENCE]

```bash
uv run .claude/skills/hostinger-tools/scripts/hostinger.py datacenter-list
uv run .claude/skills/hostinger-tools/scripts/hostinger.py template-list
uv run .claude/skills/hostinger-tools/scripts/hostinger.py template-view --id 1007
```

---
## [16][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [PATTERN]       | [RESPONSE]                 |
| :-----: | --------------- | -------------------------- |
|   [1]   | List commands   | `{items: object[]}`        |
|   [2]   | View commands   | `{id: int, item: object}`  |
|   [3]   | Action commands | `{id: int, action: bool}`  |
|   [4]   | Create commands | `{id: int, created: bool}` |

---
## [17][ENVIRONMENT]

| [VAR]             | [REQUIRED] | [DESCRIPTION]              |
| ----------------- | ---------- | -------------------------- |
| `HOSTINGER_TOKEN` | Yes        | Hostinger API bearer token |

---
## [18][ERROR_HANDLING]

- HTTP errors print `[ERROR] <status>: <body>` and exit 1
- Missing token: `[ERROR] HOSTINGER_TOKEN environment variable not set`
- VPS not found: `[ERROR] 404: Virtual machine not found`
- Action pending: `[ERROR] 409: Action already in progress`; wait for completion

