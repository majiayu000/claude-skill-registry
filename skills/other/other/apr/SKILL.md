---
name: apr
description: Run APR (Automated Plan Reviser) workflow for FCP specification refinement. Use when asked to run APR, revision rounds, spec review, integrate GPT feedback, or harmonize docs. Handles Oracle remote setup, running rounds, integrating feedback, and syncing README/implementation docs.
---

# APR - Automated Plan Reviser for FCP

This skill automates iterative specification refinement using GPT Pro 5.2 Extended Reasoning via Oracle.

## Quick Start

**Run next round (fully automated):**
```
run apr round <N>
```

This will:
1. Run `apr run <N> --wait` to get GPT Pro feedback
2. Read and analyze all revisions
3. Integrate each revision into FCP_Specification_V2.md
4. Harmonize README.md with changes
5. Harmonize docs/fcp_model_connectors_rust.md
6. Commit changes in logical groups with detailed messages
7. Push to remote

**Run continuous rounds:**
```
keep running apr rounds starting from <N>
```

## Overview

The Flywheel Connector Protocol (FCP) specification is refined through multiple rounds of GPT Pro review. Each round:
1. Sends README + spec (optionally + implementation) to GPT Pro 5.2
2. Receives detailed revision suggestions with rationale
3. Integrates feedback into the spec via Claude Code
4. Harmonizes README and implementation docs
5. Commits with detailed messages

## Oracle Remote Setup (One-Time)

For headless/SSH environments, Oracle can delegate browser automation to a local machine.

### On the LOCAL machine (with browser/GUI):
```bash
# Install Oracle if needed
npm install -g @steipete/oracle

# Start server (keep this terminal open)
# IMPORTANT: Use port 9333 (not 9222) to avoid conflict with Chrome DevTools
oracle serve --port 9333 --token "flywheel-apr-2026"
```

### On the REMOTE machine (this server):
```bash
# Add to shell config for persistence
echo 'export ORACLE_REMOTE_HOST="100.114.183.31:9333"' >> ~/.zshrc
echo 'export ORACLE_REMOTE_TOKEN="flywheel-apr-2026"' >> ~/.zshrc
source ~/.zshrc

# Test connection
oracle -p "test connection" -e browser -m "5.2 Pro"
```

**Why port 9333?** Oracle serve listens on this port for incoming requests. When it
receives a request, it launches Chrome which uses port 9222 for DevTools Protocol.
Using 9333 for the server avoids the port conflict.

**Tailscale IPs for this setup:**
- Mac Mini: `100.114.183.31`
- iMac: `100.81.209.68`
- This server (threadripperje): `100.91.120.17`

## Commands

**Important: Always run APR from the project directory:**
```bash
cd /data/projects/flywheel_connectors
```

### Check Status
```bash
apr status          # Check Oracle sessions
apr list            # List workflows
apr history         # Show revision history
apr dashboard       # Interactive analytics
```

### Run a Revision Round
```bash
# Standard round (README + spec only)
apr run <N> --wait

# Include implementation doc (manual override)
apr run <N> --include-impl --wait

# With impl_every_n: 4 in workflow config, impl is auto-included on rounds 4, 8, 12...

# Preview without sending
apr run <N> --dry-run

# Render prompt for manual paste
apr run <N> --render --output /tmp/prompt.md
```

### How Documents Are Sent

APR pastes document contents **inline** (not as file attachments). This is more reliable:
- No "duplicate file" errors from ChatGPT
- No silent upload failures
- Works consistently for documents up to ~200KB

### View and Compare Rounds
```bash
apr show <N>        # View round output
apr diff <N> <M>    # Compare two rounds
apr diff <N>        # Compare round N vs N-1
```

## Automated Integration Workflow

When user requests a round, Claude Code performs these steps automatically:

### Step 1: Run APR and Get Feedback
```bash
apr run <N> --wait
```

### Step 2: Read and Analyze Revisions
- Read `.apr/rounds/fcp/round_<N>.md`
- Parse all revision suggestions
- Create todo list for each revision

### Step 3: Integrate Each Revision
For each revision in the GPT Pro output:
- Locate relevant sections in FCP_Specification_V2.md
- Apply changes (add structs, modify enums, update comments)
- Ensure NORMATIVE sections are properly marked

### Step 4: Harmonize README.md
- Update terminology table if new concepts added
- Update architecture sections for protocol changes
- Update security sections for new safety features
- Keep descriptions concise and user-focused

### Step 5: Harmonize Implementation Doc
- Update docs/fcp_model_connectors_rust.md
- Sync all struct definitions with spec
- Update code examples to match new signatures
- Ensure NORMATIVE annotations match spec

### Step 6: Commit and Push
Create logical commits:
1. Main spec changes (docs(fcp): ...)
2. README harmonization (docs(readme): ...)
3. Implementation doc (docs(connectors): ...)
4. APR round output (chore(apr): ...)

Then push to remote.

## After Compaction Recovery

If context compaction occurs, re-prime before continuing:
```
Reread AGENTS.md so it's still fresh in your mind. Also reread the entire
V2 spec so it's fresh before you read docs/fcp_model_connectors_rust.md.
```

## Key Files

| File | Purpose |
|------|---------|
| `FCP_Specification_V2.md` | Main protocol specification (~145 KB) |
| `README.md` | Project overview and quick start (~44 KB) |
| `docs/fcp_model_connectors_rust.md` | Rust implementation guide (~70 KB) |
| `AGENTS.md` | Development rules and guidelines (~25 KB) |
| `.apr/rounds/fcp/round_N.md` | GPT Pro outputs for each round |

## Workflow Configuration

The APR workflow is configured in `.apr/workflows/fcp.yaml`:
- **Documents**: README.md, FCP_Specification_V2.md, docs/fcp_model_connectors_rust.md
- **Model**: GPT Pro 5.2 with Extended Thinking
- **Output**: `.apr/rounds/fcp/`
- **impl_every_n**: 4 (auto-include implementation every 4th round)

## Tips

1. **impl_every_n handles periodic inclusion** - With `impl_every_n: 4`, rounds 4, 8, 12... auto-include implementation
2. **Don't skip harmonization** - Changes should flow through all docs
3. **Watch for convergence** - Use `apr stats` to see if changes are dampening
4. **Target 15-20 rounds** - For complex protocols, more iterations = better spec
5. **New session per round** - Start fresh GPT Pro conversations to avoid context pollution

## Troubleshooting

### Oracle Connection Issues
```bash
# Check if Oracle server is running on local machine
# On local: oracle serve --port 9333 --token "..."

# Verify Tailscale connectivity
tailscale ping 100.114.183.31

# Test Oracle directly
oracle -p "test" -e browser -m "5.2 Pro" -v
```

### APR Issues
```bash
# Verbose mode for debugging
apr run <N> -v

# Check workflow config
cat .apr/workflows/fcp.yaml

# Verify files exist
ls -la README.md FCP_Specification_V2.md docs/fcp_model_connectors_rust.md

# Clear stale lock
rm -f .apr/.locks/fcp_round_<N>.lock
```

## Round History

| Round | Status | Key Changes |
|-------|--------|-------------|
| 1 | Complete | Initial refinements |
| 2 | Complete | sender_instance_id, ZoneRekeyPolicy, ApprovalToken, session nonces, GC mirroring, simulate, RoleObject, NetworkConstraints, WASI |
| 3 | Complete | RFC2119, Provenance MIN/MAX merge, SanitizerReceipt, basis points, KIDs, foreign_refs, FCPC framing, ResourceObject, RevocationFreshnessPolicy, fuzzing |
| 4 | Pending | - |
