#!/bin/bash

# ICP 2: Power User
#
# Get browser tasks done from your phone while the laptop runs unattended.
# Uses snapshots to save authenticated sessions, daemon for always-on state.
#
# Workflow:
# 1. Manual login once → snapshot the authenticated state
# 2. Later: agent auto-restores the snapshot → already logged in → do work
# 3. No re-authentication needed, no TOTP codes

set -e

PROFILE="agent-work"
ORIGIN="https://jira.mycompany.com"

echo "=== ICP 2: Power User Workflow ==="
echo ""

# Step 1: First time setup — create agent profile and snapshot
# (You would do this once, manually logged in)
echo "STEP 1: Create agent profile snapshot (one-time setup)"
echo "-----"
echo "# Open a session with the agent profile"
echo "SESSION=\$(pagerunner open-session --profile $PROFILE)"
echo ""
echo "# Log in manually to Jira (do this in the browser window that opens)"
echo "# Once logged in, save the snapshot"
echo "pagerunner save-snapshot \$SESSION <tab-id> $ORIGIN"
echo ""

# Step 2: Later — agent uses the snapshot (this is what runs from your phone)
echo ""
echo "STEP 2: Agent restores snapshot and does work (automated)"
echo "-----"
echo "SESSION=\$(pagerunner open-session --profile $PROFILE)"
echo "TAB=\$(pagerunner list-tabs \$SESSION | jq -r '.[0].target_id')"
echo ""
echo "# Agent is already logged in from the snapshot"
echo "pagerunner restore-snapshot \$SESSION \$TAB $ORIGIN"
echo ""
echo "# Now agent can work: read Jira, extract data, etc."
echo "pagerunner navigate \$SESSION \$TAB 'https://jira.mycompany.com/secure/RapidBoard.jspa'"
echo "CONTENT=\$(pagerunner get-content \$SESSION \$TAB)"
echo ""
echo "# Parse and summarize for WhatsApp"
echo "echo \"\$CONTENT\" | jq '.blockers' # Extract blockers"
echo ""

# Step 3: Daemon setup (optional, for true always-on)
echo ""
echo "STEP 3: Daemon setup (optional, for always-on coordination)"
echo "-----"
echo "# Start the daemon once (keeps state across sessions)"
echo "pagerunner daemon &"
echo ""
echo "# Now multiple agents can use the same snapshots + KV store"
echo "# Agent A can save state: pagerunner kv-set 'team' 'latest_pr' '42'"
echo "# Agent B can read: pagerunner kv-get 'team' 'latest_pr'"
echo ""

echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Run step 1 once to create your snapshot"
echo "2. Set up OpenClaw/Hermes trigger on your phone"
echo "3. From phone: 'Check my Jira for blockers' → daemon + snapshot → response"
