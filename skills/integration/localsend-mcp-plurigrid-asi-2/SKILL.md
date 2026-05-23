---
name: localsend-mcp
description: LocalSend-based P2P transfer with MCP server design for NATS/Tailscale discovery and throughput tuning.
source: local
license: UNLICENSED
---

# LocalSend MCP Skill

## Use This Skill When
- The user mentions LocalSend, AirDrop-like transfer, or peer-to-peer file sharing.
- The task asks for an MCP server or tool set around LocalSend.
- Discovery/advertising needs to use NATS or Tailscale before transferring data.

## Reality Check (LocalSend in This Repo)
- `localsend` (Flox package) launches a GUI and does not exit for `--help`.
- Discovery uses UDP multicast `224.0.0.167:53317` (LAN only).
- Transfer runs HTTPS on port `53317`; direct IPs are required across subnets.
- For headless automation, prefer a CLI client (e.g., `jocalsend`) or a small protocol wrapper.

## Architecture: Advertise -> Negotiate -> Transfer -> Tune

1. **Advertise** capabilities over NATS (or Tailscale if LAN multicast is blocked).
2. **Negotiate** transport and parameters (LAN multicast vs direct IP).
3. **Transfer** via LocalSend protocol/CLI.
4. **Tune** throughput until spectral gap <= 0.25 (>= 75% of target throughput).

## MCP Tool Set (Draft)

**Discovery / Advertising**
- `localsend_advertise`:
  - Inputs: `agent_id`, `device_name`, `localsend_port`, `tailscale_ip?`, `capabilities`, `spectral_gap_target`
- `localsend_list_peers`:
  - Inputs: `source` = `localsend_multicast` | `nats` | `tailscale`

**Session Negotiation**
- `localsend_negotiate`:
  - Inputs: `peer_id`, `preferred_transport`, `max_chunk_bytes`, `max_parallel`
  - Output: `session_id`, `transport`, `target_ip`, `port`

**Transfer**
- `localsend_send`:
  - Inputs: `session_id`, `file_path`, `chunk_bytes`, `parallelism`
- `localsend_receive`:
  - Inputs: `session_id`, `dest_dir`, `accept`

**Throughput Tuning**
- `localsend_probe`:
  - Inputs: `session_id`, `probe_bytes`, `probe_parallelism`
  - Output: `throughput_bps`, `rtt_ms`, `loss_rate`
- `localsend_session_status`:
  - Inputs: `session_id`
  - Output: `bytes_sent`, `bytes_received`, `throughput_bps`, `spectral_gap`

## Spectral Gap Heuristic (Practical)

Define:
```
spectral_gap = 1.0 - (observed_throughput / target_throughput)
```
Stop tuning when `spectral_gap <= 0.25`.

**Tuning Loop**:
1. Start `chunk_bytes = 256KB`, `parallelism = 1`
2. Increase parallelism to 2, 4, 8 while loss < 1%
3. Increase chunk size up to 1MB while RTT stable
4. Recompute spectral gap each step

## Integration Points in This Repo
- NATS broadcast helpers: `lib/synadia_broadcast.rb`
- Tailscale patterns: `lib/tailscale_file_transfer_skill.rb`
- MCP server reference: `mcp_unified_server.py`

<<<<<<< HEAD
=======
## GitHub GraphQL (GH CLI) Reference

Use `gh api graphql` for contributor snapshots (limit: `history(first: 100)`):

```bash
gh api graphql \
  -F owner=localsend \
  -F name=localsend \
  -F history=100 \
  -f query='query($owner:String!,$name:String!,$history:Int!){
    repository(owner:$owner,name:$name){
      defaultBranchRef{name target{
        ... on Commit{
          history(first:$history){
            nodes{author{user{login} name}}
          }
        }
      }}
    }
  }'
```

Aggregate top contributors:
```bash
gh api graphql -F owner=localsend -F name=localsend -F history=100 -f query='query($owner:String!,$name:String!,$history:Int!){repository(owner:$owner,name:$name){defaultBranchRef{name target{... on Commit{history(first:$history){nodes{author{user{login} name}}}}}}}}' \
  | jq -r '.data.repository.defaultBranchRef.target.history.nodes[].author | if .user then .user.login else .name end' \
  | sort | uniq -c | sort -nr | head -20
```

## Duck Lake Snapshots (Feedback + Bidirectional Flow)

Persist LocalSend sessions and GitHub snapshots into DuckDB for time travel:

```sql
CREATE TABLE IF NOT EXISTS localsend_sessions (
  session_id TEXT,
  peer_id TEXT,
  direction TEXT, -- send|receive
  bytes BIGINT,
  throughput_bps DOUBLE,
  spectral_gap DOUBLE,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS localsend_contributors_snapshot (
  snapshot_at TIMESTAMP,
  repo TEXT,
  contributor TEXT,
  commit_count INT
);
```

Store snapshots per run and query later with existing DuckDB time-travel commands.

>>>>>>> origin/feature/skill-connectivity-hub-20251226
## Implementation Notes
- Avoid assuming LocalSend has a stable CLI; verify with `jocalsend --help` if installed.
- If multicast discovery fails (Tailscale), use NATS to exchange `target_ip` + `port`.
- Keep tool outputs structured; avoid dumping large blobs through MCP.
