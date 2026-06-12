---
name: continuous-monitoring
description: Set up nightly monitoring of subdomain changes, JS file diffs, new endpoints, and CVE matches against in-scope assets, with Discord/Slack/Telegram notifications. Use when the user has an active engagement and wants to be alerted to new attack surface without manual re-recon.
metadata:
  type: skill
  phase: recon
  tools: [cron, github-actions, notify, anew, diff, subfinder, httpx, nuclei]
---

# Continuous Monitoring

> Sleep. Sub registered overnight. Discord pings. You hunt it before everyone else.

## When to invoke

**Trigger phrases:**
- "monitor target"
- "alert on new subdomain"
- "watch this program"
- "set up continuous recon"

## What we monitor

| Signal | Why it matters | Frequency |
|---|---|---|
| New subdomains | New attack surface, often less tested | Nightly |
| Subdomain takeover candidates | Free critical if found early | Nightly |
| JS file hash changes | New endpoints, removed mitigations | Daily |
| New endpoints in JS | Hidden routes shipped in deploys | Daily |
| HTTP status changes (200 → 401 etc.) | New restrictions / new exposures | Daily |
| New tech in fingerprint | New stack = new vuln classes | Weekly |
| CVE matches against fingerprint | 0-days → 1-day exploitation window | Daily |
| GitHub commits to public repos | Secrets, hints, new features | Hourly |
| Cert transparency new certs | New subdomains often pre-deployed in CT | Hourly |
| Wayback URL diff | New paths historical scanners pick up | Daily |

## Two deployment models

### A. Cron-based (your VPS, $5/month)
```
┌────────────────────────────────────────┐
│ DigitalOcean / Linode / Hetzner VPS    │
│  - cron jobs                           │
│  - bash scripts                        │
│  - state in ~/ccs-state/                │
│  - notify → Discord webhook            │
└────────────────────────────────────────┘
```

### B. GitHub Actions (free, no VPS)
```
┌────────────────────────────────────────┐
│ GitHub Actions                         │
│  - scheduled workflows                 │
│  - state in repo artifacts             │
│  - notify → Discord webhook            │
└────────────────────────────────────────┘
```

We'll cover both.

## Setup A — Cron on a VPS

### Step 1: Notify configuration

Use [`notify`](https://github.com/projectdiscovery/notify) — supports Discord/Slack/Telegram/Teams.

```bash
mkdir -p ~/.config/notify
cat > ~/.config/notify/provider-config.yaml <<EOF
discord:
  - id: "ccs-alerts"
    discord_webhook_url: "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
slack:
  - id: "ccs-alerts"
    slack_webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK"
telegram:
  - id: "ccs-alerts"
    telegram_api_key: "YOUR_BOT_TOKEN"
    telegram_chat_id: "YOUR_CHAT_ID"
EOF

# Test
echo "Test alert from claude-cybersecurity-skills" | notify -id ccs-alerts -bulk
```

### Step 2: Subdomain monitoring script

```bash
# scripts/monitor-subs.sh
#!/usr/bin/env bash
set -euo pipefail

TARGETS_FILE="$HOME/ccs-state/targets.txt"   # one root domain per line
STATE_DIR="$HOME/ccs-state"
mkdir -p "$STATE_DIR/subs"

while read TARGET; do
    OLD="$STATE_DIR/subs/$TARGET.txt"
    NEW="$STATE_DIR/subs/$TARGET.new.txt"

    # Run passive recon
    (subfinder -d "$TARGET" -all -silent;
     assetfinder --subs-only "$TARGET";
     curl -s "https://crt.sh/?q=%25.${TARGET}&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g') | \
        sort -u > "$NEW"

    if [[ -f "$OLD" ]]; then
        # Diff
        DIFF=$(comm -13 <(sort "$OLD") <(sort "$NEW"))
        if [[ -n "$DIFF" ]]; then
            COUNT=$(echo "$DIFF" | wc -l)
            echo -e "🆕 New subdomains for **$TARGET** ($COUNT)\n\`\`\`\n$DIFF\n\`\`\`" | \
                notify -id ccs-alerts -bulk -silent

            # Auto-probe new ones for quick wins
            echo "$DIFF" | httpx -silent -tech-detect -title -status-code | \
                tee -a "$STATE_DIR/subs/$TARGET.probed.log" | \
                notify -id ccs-alerts -bulk -silent

            # Check for takeover candidates
            echo "$DIFF" | nuclei -t http/takeovers/ -silent -nc -severity high,critical | \
                notify -id ccs-alerts -bulk -silent
        fi
    else
        echo "[*] Initial baseline for $TARGET ($(wc -l < "$NEW") subs)"
    fi

    mv "$NEW" "$OLD"
done < "$TARGETS_FILE"
```

### Step 3: JS file monitoring

```bash
# scripts/monitor-js.sh
#!/usr/bin/env bash
set -euo pipefail

URLS_FILE="$HOME/ccs-state/js-urls.txt"  # JS file URLs to monitor
STATE_DIR="$HOME/ccs-state/js"
mkdir -p "$STATE_DIR"

while read JS_URL; do
    HASH_FILE="$STATE_DIR/$(echo "$JS_URL" | md5sum | cut -d' ' -f1).hash"
    CURRENT_HASH=$(curl -s "$JS_URL" | md5sum | cut -d' ' -f1)

    if [[ -f "$HASH_FILE" ]]; then
        OLD_HASH=$(cat "$HASH_FILE")
        if [[ "$OLD_HASH" != "$CURRENT_HASH" ]]; then
            # Get the diff in endpoints
            OLD_ENDPOINTS_FILE="$STATE_DIR/$(echo "$JS_URL" | md5sum | cut -d' ' -f1).endpoints"

            curl -s "$JS_URL" > /tmp/current.js
            python3 ~/tools/LinkFinder/linkfinder.py -i /tmp/current.js -o cli 2>/dev/null | sort -u > /tmp/current.endpoints

            if [[ -f "$OLD_ENDPOINTS_FILE" ]]; then
                NEW_ENDPOINTS=$(comm -13 <(sort "$OLD_ENDPOINTS_FILE") /tmp/current.endpoints)
                if [[ -n "$NEW_ENDPOINTS" ]]; then
                    echo -e "🔧 JS changed: $JS_URL\n**New endpoints:**\n\`\`\`\n$NEW_ENDPOINTS\n\`\`\`" | \
                        notify -id ccs-alerts -bulk -silent
                fi
            fi

            mv /tmp/current.endpoints "$OLD_ENDPOINTS_FILE"
        fi
    fi

    echo "$CURRENT_HASH" > "$HASH_FILE"
done < "$URLS_FILE"
```

### Step 4: Cert transparency real-time

Subscribe to certstream for near-instant new-cert alerts:

```python
# scripts/certstream-monitor.py
import certstream
import re
import requests

WEBHOOK = "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
TARGETS = ["target.com", "anothertarget.io"]

def callback(message, context):
    if message['message_type'] != 'certificate_update':
        return
    domains = message['data']['leaf_cert']['all_domains']
    for d in domains:
        for t in TARGETS:
            if d.endswith("." + t) or d == t:
                msg = f"🆕 New cert: `{d}` (target: {t})"
                requests.post(WEBHOOK, json={"content": msg})
                return

certstream.listen_for_events(callback, url='wss://certstream.calidog.io/')
```

Run as systemd service:
```ini
# /etc/systemd/system/certstream-monitor.service
[Unit]
Description=Cert Transparency Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/user/ccs-state/scripts/certstream-monitor.py
Restart=always
User=user

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now certstream-monitor
```

### Step 5: Crontab

```cron
# Subdomain enumeration
0 3 * * * /home/user/ccs-state/scripts/monitor-subs.sh >> /var/log/ccs-monitor.log 2>&1

# JS monitoring (every 6 hours)
0 */6 * * * /home/user/ccs-state/scripts/monitor-js.sh >> /var/log/ccs-monitor.log 2>&1

# Nuclei sweep of in-scope (daily)
0 5 * * * /home/user/ccs-state/scripts/nuclei-sweep.sh >> /var/log/ccs-monitor.log 2>&1

# Weekly tech re-fingerprint
0 6 * * 1 /home/user/ccs-state/scripts/refingerprint.sh >> /var/log/ccs-monitor.log 2>&1
```

## Setup B — GitHub Actions

### .github/workflows/monitor.yml

```yaml
name: BB Continuous Monitoring

on:
  schedule:
    - cron: '0 3 * * *'    # daily 3am UTC
  workflow_dispatch:        # manual trigger

jobs:
  monitor-subs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.22'

      - name: Install tools
        run: |
          go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
          go install github.com/projectdiscovery/httpx/cmd/httpx@latest
          go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
          go install github.com/projectdiscovery/notify/cmd/notify@latest
          go install github.com/tomnomnom/anew@latest

      - name: Configure notify
        run: |
          mkdir -p ~/.config/notify
          cat > ~/.config/notify/provider-config.yaml <<EOF
          discord:
            - id: "ccs-alerts"
              discord_webhook_url: "${{ secrets.DISCORD_WEBHOOK }}"
          EOF

      - name: Run monitoring
        env:
          CHAOS_KEY: ${{ secrets.CHAOS_KEY }}
        run: |
          chmod +x scripts/monitor-subs.sh
          ./scripts/monitor-subs.sh

      - name: Commit state
        run: |
          git config user.name "ccs-monitor"
          git config user.email "monitor@claude-cybersecurity-skills"
          git add state/
          git diff --staged --quiet || git commit -m "monitor: state update $(date -u +%Y-%m-%dT%H:%MZ)"
          git push
```

Configure secrets in GitHub repo settings:
- `DISCORD_WEBHOOK`
- `CHAOS_KEY`
- (any other API keys)

## Nuclei daily sweep

Hit all alive in-scope hosts with critical/high templates daily:

```bash
# scripts/nuclei-sweep.sh
#!/usr/bin/env bash
set -euo pipefail

ALIVE="$HOME/ccs-state/all-alive.txt"

nuclei -list "$ALIVE" \
    -severity critical,high \
    -rate-limit 50 \
    -bulk-size 25 \
    -concurrency 25 \
    -silent \
    -nc \
    -json -o "$HOME/ccs-state/nuclei-daily.json"

# Diff against yesterday
NEW_FINDINGS=$(comm -13 \
    <(sort "$HOME/ccs-state/nuclei-yesterday.json" 2>/dev/null) \
    <(sort "$HOME/ccs-state/nuclei-daily.json"))

if [[ -n "$NEW_FINDINGS" ]]; then
    echo -e "🚨 New nuclei findings:\n\`\`\`json\n$NEW_FINDINGS\n\`\`\`" | \
        notify -id ccs-alerts -bulk -silent
fi

cp "$HOME/ccs-state/nuclei-daily.json" "$HOME/ccs-state/nuclei-yesterday.json"
```

## GitHub commit monitoring (for OSS targets)

```bash
# scripts/github-watch.sh
# Watches commits on target's public GitHub orgs
GH_ORGS=("target-inc" "target-oss")

for ORG in "${GH_ORGS[@]}"; do
    LAST_SHA_FILE="$HOME/ccs-state/gh-$ORG.sha"

    # Get latest events
    LATEST=$(gh api "orgs/$ORG/events" --jq '.[0].id')

    if [[ -f "$LAST_SHA_FILE" ]]; then
        OLD=$(cat "$LAST_SHA_FILE")
        if [[ "$OLD" != "$LATEST" ]]; then
            EVENTS=$(gh api "orgs/$ORG/events" --jq '.[] | select(.type=="PushEvent") | "\(.repo.name): \(.payload.commits[].message)"' | head -5)
            echo -e "📦 Activity in **$ORG**:\n$EVENTS" | notify -id ccs-alerts -bulk -silent
        fi
    fi

    echo "$LATEST" > "$LAST_SHA_FILE"
done
```

## State structure

```
~/ccs-state/
├── targets.txt              ← one root domain per line
├── subs/
│   ├── target.com.txt       ← yesterday's list
│   └── target.com.probed.log
├── js/
│   ├── <hash>.hash          ← last-seen hash
│   └── <hash>.endpoints     ← last-seen endpoint list
├── js-urls.txt              ← JS files to monitor
├── all-alive.txt
├── nuclei-daily.json
├── nuclei-yesterday.json
├── gh-target-inc.sha
└── logs/
```

## Tuning alerts (avoid notification fatigue)

```yaml
# rules.yaml — what to alert on
alert_rules:
  subdomain_new:
    threshold: 1                # alert on any new sub
    quiet_hours: "22-08"        # don't ping at night
  takeover_candidate:
    threshold: 1
    severity: high              # always alert
  nuclei_finding:
    severity: [critical, high]  # skip medium/low to reduce noise
  js_change:
    only_with_new_endpoints: true  # don't alert on cosmetic changes
```

## Cross-references

- `[[subdomain-enum]]` — the engine behind monitoring
- `[[js-analysis]]` — for endpoint diffs
- `[[subdomain-takeover]]` — auto-check on new subs
- `[[scope-analysis]]` — only alert on in-scope assets

## Common pitfalls

1. **Monitoring out-of-scope assets.** Alerts you can't act on. Filter first.
2. **Notification fatigue.** Tune `severity` and `quiet_hours` aggressively.
3. **State loss.** If `~/ccs-state/` is wiped, you re-baseline = many false "new" alerts.
4. **VPS IP blocked.** Some targets ban scanner IPs. Rotate or use Cloud Run / Lambda.
5. **API rate limits.** Don't run subfinder every hour — daily is enough for most.

## Pro tips

- **Separate webhooks per priority** (one for "new subs", one for "critical findings").
- **Use Telegram for mobile alerts** — instant push.
- **Tag alerts with target name** in the message for fast triage.
- **Auto-create a private issue** in your private bug-bounty repo for each finding.
- **Track your "first to find" rate** — measures how quickly you act on monitoring alerts.

## Real-world example

```
[Day 1, 3am UTC]
🆕 New subdomain for target.com (1):
admin-staging.target.com  [200] Tech: Spring Boot 2.5.4, Actuator

[Day 1, 9am — you wake up]
You check: /actuator/env → exposed. CRITICAL.
Report submitted by 10am. Triaged within 2h. $5,000 bounty by EOD.
```

This is **the difference** between manual recon and automated monitoring.
