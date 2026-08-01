#!/bin/bash

# ICP 4: Server-Side / Infrastructure
#
# Persistent headless automation with multi-agent coordination.
# Agents coordinate via shared KV store, snapshots, and session state.
#
# Architecture:
# - pagerunner daemon: persistent process holding DB lock + socket server
# - Agent A, B, C: multiple processes/cron jobs connecting to daemon
# - Shared state: KV store, snapshots, open sessions (survive across runs)

set -e

echo "=== ICP 4: Daemon + Multi-Agent Coordination ==="
echo ""

# Step 1: Start the daemon (once)
echo "STEP 1: Start daemon (one-time)"
echo "-----"
echo ""
echo "# Launch daemon in background"
echo "pagerunner daemon &"
echo "# Output: Listening on ~/.pagerunner/daemon.sock"
echo ""
echo "# Verify it's running"
echo "ps aux | grep 'pagerunner daemon'"
echo ""
echo "# Check logs"
echo "tail -f ~/.pagerunner/daemon.log"
echo ""

# Step 2: Agent A — collect data
echo "STEP 2: Agent A — collect data from external API/website"
echo "-----"
echo ""
cat > /tmp/agent-a.sh << 'EOF'
#!/bin/bash
# Agent A: Scrape pricing data and store in KV store

SESSION=$(pagerunner open-session --profile agent)
TAB=$(pagerunner list-tabs "$SESSION" | jq -r '.[0].target_id')

pagerunner navigate "$SESSION" "$TAB" "https://api.example.com/prices"
PRICES=$(pagerunner get-content "$SESSION" "$TAB" | jq '.prices')

# Store result in KV store for Agent B
pagerunner kv-set "pricing-pipeline" "latest-prices" "$PRICES"
pagerunner kv-set "pricing-pipeline" "last-run" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "Agent A: Stored $(echo "$PRICES" | jq 'length') prices to KV store"
pagerunner close-session "$SESSION"
EOF

echo "# File: /tmp/agent-a.sh"
echo "bash /tmp/agent-a.sh"
echo "# Output: Agent A: Stored 150 prices to KV store"
echo ""

# Step 3: Agent B — process data
echo "STEP 3: Agent B — read Agent A's data and process"
echo "-----"
echo ""
cat > /tmp/agent-b.sh << 'EOF'
#!/bin/bash
# Agent B: Read prices from KV store, process, and store results

SESSION=$(pagerunner open-session --profile agent)
TAB=$(pagerunner list-tabs "$SESSION" | jq -r '.[0].target_id')

# Read from KV store (stored by Agent A)
PRICES=$(pagerunner kv-get "pricing-pipeline" "latest-prices")
LAST_RUN=$(pagerunner kv-get "pricing-pipeline" "last-run")

echo "Agent B: Found $(echo "$PRICES" | jq 'length') prices from run at $LAST_RUN"

# Process: find outliers, calculate aggregates, etc.
PROCESSED=$(echo "$PRICES" | jq 'map(select(.price > 1000)) | length')
echo "Agent B: Found $PROCESSED high-priced items"

# Store processed results for Agent C
pagerunner kv-set "pricing-pipeline" "processed-results" "{\"high_price_count\": $PROCESSED}"

pagerunner close-session "$SESSION"
EOF

echo "# File: /tmp/agent-b.sh"
echo "bash /tmp/agent-b.sh"
echo "# Output: Agent B: Found 150 prices from run at 2024-03-23T10:30:45Z"
echo "# Output: Agent B: Found 28 high-priced items"
echo ""

# Step 4: Agent C — report
echo "STEP 4: Agent C — generate report"
echo "-----"
echo ""
cat > /tmp/agent-c.sh << 'EOF'
#!/bin/bash
# Agent C: Read all processed data and generate report

# Read all available data from KV store
PRICES=$(pagerunner kv-get "pricing-pipeline" "latest-prices")
RESULTS=$(pagerunner kv-get "pricing-pipeline" "processed-results")
LAST_RUN=$(pagerunner kv-get "pricing-pipeline" "last-run")

# Generate report
cat > report.json << REPORT
{
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "data_from": "$LAST_RUN",
  "total_prices": $(echo "$PRICES" | jq 'length'),
  "high_price_count": $(echo "$RESULTS" | jq '.high_price_count'),
  "status": "complete"
}
REPORT

echo "Report generated: report.json"
cat report.json
EOF

echo "# File: /tmp/agent-c.sh"
echo "bash /tmp/agent-c.sh"
echo ""

# Step 5: Cron job (automated pipeline)
echo "STEP 5: Automate with cron"
echo "-----"
echo ""
echo "# Add to crontab -e"
echo "0 9 * * * bash /tmp/agent-a.sh  # 9am: collect prices"
echo "5 9 * * * bash /tmp/agent-b.sh  # 9:05am: process"
echo "10 9 * * * bash /tmp/agent-c.sh # 9:10am: report"
echo ""

# Step 6: Stop daemon
echo "STEP 6: Stop daemon (when done)"
echo "-----"
echo ""
echo "pkill -f 'pagerunner daemon'"
echo ""

# Summary
echo "=== Summary ==="
echo ""
echo "Architecture:"
echo "┌─────────────────────────────────────────────────┐"
echo "│  pagerunner daemon (persistent)                 │"
echo "│  └─ DB lock + Unix socket (~/.pagerunner/...)   │"
echo "│                                                  │"
echo "│  Agents (A, B, C) + Cron jobs                   │"
echo "│  └─ Connect to daemon over socket               │"
echo "│  └─ Share KV store, snapshots, sessions         │"
echo "└─────────────────────────────────────────────────┘"
echo ""
echo "Benefits:"
echo "- No duplicate Chrome instances (one daemon, many agents)"
echo "- Shared authenticated state (snapshots)"
echo "- Persistent KV store (agents pass data)"
echo "- Audit logging (compliance trail)"
echo "- Scheduled reliability (cron jobs)"
echo ""
