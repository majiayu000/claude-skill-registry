---
name: optimize-network
description: Safely diagnose and improve local network speed, latency, jitter, DNS, Wi-Fi, Ethernet, macOS network services, and bufferbloat. Use this skill whenever the user asks to optimize internet/network speed, make the network faster, diagnose slow Wi-Fi, latency, packet loss, DNS delay, unstable Codex/AI tool connectivity, or asks about the viral Codex network optimization workflow. Always protect VPN/proxy tools such as Clash Verge, Mihomo, Shadowrocket, Tailscale, V2Ray, Surge, and corporate VPNs; do not modify or disable them unless the user explicitly asks for that specific change.
allowed-tools: Bash
metadata:
  argument-hint: "[diagnose|optimize|report|skill] [target-domain]"
---

# Optimize Network

Use this skill to run a safe, evidence-first network optimization workflow. The default posture is read-only diagnosis, then small reversible experiments, then before/after verification. Never treat VPN, proxy, TUN, or routing tools as junk processes.

## Safety Contract

Follow these rules before any command that could affect connectivity:

- Intent lock: the goal is speed, latency, responsiveness, and stability, not cleaning network configuration.
- Proxy/VPN protection: do not stop, restart, unload, delete, reconfigure, or bypass Clash, Mihomo, Shadowrocket, Tailscale, V2Ray, Surge, WireGuard, OpenVPN, corporate VPNs, or their TUN interfaces unless the user explicitly requests that exact operation.
- Default read-only: diagnostics may run directly; changes require a short proposal with risk, rollback, and expected effect.
- Reversible first: prefer temporary A/B tests, service reordering, DNS experiments, cache flushes, and user-confirmed app closure over deletion.
- No silent degradation: if a change breaks access to AI tools, proxy, remote work, DNS, or LAN devices, revert it or report the blocker immediately.
- No destructive cleanup: do not delete network locations, profiles, VPN configs, proxy configs, launch agents, routes, or firewall rules. If deletion looks useful, propose disable/dry-run first.
- Sudo caution: any `sudo`, interface down/up, DHCP reset, route change, or network service disable must be confirmed by the user first.
- Remote session caution: if the user may be connected through SSH, remote desktop, RustDesk, Tailscale, or VPN, ask before any change that could disconnect them.

## Routing Decision

Choose one mode and state it briefly:

- `execute_direct`: read-only diagnosis, report generation, or a user-approved reversible command.
- `plan_first`: multi-step optimization, DNS change, service-order change, AWDL/AirDrop test, or anything that may affect connectivity.
- `clarify_first`: OS is unknown, user is remote over the network, proxy/VPN ownership is unclear, or the requested change would modify VPN/proxy/TUN state.

Use these handoff fields in the report: goal, context, constraints, actions, evidence, decision, rollback, next step.

## Evidence Hierarchy

Prefer fresh local measurements over assumptions:

1. System route/proxy/DNS state: `scutil --nwi`, `scutil --dns`, `scutil --proxy`, `route -n get default`.
2. Link quality: gateway ping, packet loss, Wi-Fi RSSI/noise/Tx Rate/channel, Ethernet state.
3. Responsiveness: macOS `networkQuality -v` and, when available, `speedtest-cli`.
4. DNS: repeated `dig +tries=1 +time=2 +stats` against relevant domains.
5. Process/network load: `nettop`, `lsof`, Mihomo read-only connections API when present.
6. Before/after comparison from the same commands, same route/proxy state, and close in time.

Do not claim improvement from a single noisy datapoint. Call out variance when results are mixed.

## Workflow

### 1. Preflight

Identify the operating system and active path:

```bash
uname -a
sw_vers 2>/dev/null || true
command -v networkQuality || true
command -v speedtest-cli || true
command -v speedtest || true
scutil --nwi 2>/dev/null || true
scutil --proxy 2>/dev/null || true
```

If macOS is detected, prefer the bundled read-only snapshot helper:

```bash
~/.claude/skills/optimize-network/scripts/macos_network_snapshot.sh
```

Run the bandwidth/responsiveness portion only when the user is ready for a bandwidth-consuming test:

```bash
RUN_NETWORKQUALITY=1 ~/.claude/skills/optimize-network/scripts/macos_network_snapshot.sh
```

If testing from a local Codex skill copy instead of an installed Claude Arsenal copy, use the equivalent path under `~/.codex/skills/optimize-network/scripts/`.

### 2. Baseline

Record:

- OS, timestamp, active network service/interface, default gateway, route table summary.
- Whether tests are direct or proxied. If system proxy/TUN is active, say that throughput and latency measure the proxy path.
- `networkQuality -v` or `speedtest-cli` download/upload/latency.
- Gateway ping and at least one regional public ping.
- DNS servers and `dig` timing for user-relevant domains.
- Wi-Fi channel, band, RSSI/noise, Tx Rate, and PHY mode when available.
- Active proxy/VPN processes and read-only connection counts if relevant.

### 3. Diagnose Top Bottlenecks

Limit the finding list to the most likely 3-4 bottlenecks. Common categories:

- Local link jitter: gateway ping spikes, Wi-Fi channel contention, AWDL/AirDrop/Handoff scanning, router CPU/load.
- Bufferbloat: good bandwidth but high loaded latency in `networkQuality`.
- DNS instability: repeated lookup variance or slow first query for domains the user actually uses.
- Proxy path mismatch: speed tests or AI tools are routed through slow proxy groups or residential nodes.
- Service order drift: unused adapters ahead of the active Wi-Fi/Ethernet service.
- Background traffic: high network throughput from sync, browser, remote desktop, update, or chat apps.
- MTU/path issues: large ping failure with DF set, packet loss to nearby destinations.

Separate confirmed facts from hypotheses.

### 4. Safe Optimization Menu

Only apply a change after explaining risk and rollback.

**DNS A/B test**

Use when DNS lookup is repeatedly slow or inconsistent. Save current DNS first:

```bash
networksetup -getdnsservers Wi-Fi
```

Candidate examples for China mainland networks: `223.5.5.5`, `119.29.29.29`, `114.114.114.114`. Test by setting, flushing cache, repeating `dig` and `curl -w`, then keep only if it clearly improves results. Roll back with the saved DNS:

```bash
networksetup -setdnsservers Wi-Fi <saved-dns...>
dscacheutil -flushcache
```

**Network service order**

Use when inactive adapters are above the real interface and route evidence suggests confusion. First show the current order:

```bash
networksetup -listnetworkserviceorder
```

Propose the exact new order. Preserve VPN/proxy services and do not remove them. Apply only after confirmation:

```bash
networksetup -ordernetworkservices "<primary>" "<secondary>" "<other-services...>"
```

**Unused service disable**

Use only for clearly unused physical/virtual adapters, and prefer disable over delete. Never disable VPN/proxy/TUN services by default. Show:

```bash
networksetup -listallnetworkservices
```

Apply only after confirmation:

```bash
networksetup -setnetworkserviceenabled "<service-name>" off
```

Rollback:

```bash
networksetup -setnetworkserviceenabled "<service-name>" on
```

**AWDL/AirDrop A/B test**

Use when Wi-Fi signal is strong but gateway ping has periodic spikes. This may affect AirDrop, AirPlay, Handoff, Universal Control, and Apple Watch unlock. It usually requires `sudo`, so confirm first.

Test window:

```bash
sudo ifconfig awdl0 down
ping -c 30 <gateway>
sudo ifconfig awdl0 up
```

Do not leave `awdl0` down unless the user explicitly wants that tradeoff.

**mDNS/DNS cache refresh**

Use when local name resolution or stale DNS is suspected. `dscacheutil -flushcache` is low risk. `mDNSResponder` restart needs confirmation if sudo is required:

```bash
dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

**Background traffic**

Report top talkers from `nettop` or `lsof`. Do not kill processes. Suggest the user pause sync/download/remote desktop apps or ask for confirmation before closing anything.

**Bufferbloat / SQM**

If loaded latency is high while bandwidth is adequate, local macOS tweaks are unlikely to fix the root cause. Recommend router-side SQM/CAKE/FQ-CoDel if available, with upload/download shaping at roughly 85-90% of measured stable throughput. Treat this as manual router work unless the user explicitly asks for router configuration.

**Proxy path optimization**

If Clash/Mihomo is active, inspect read-only state before proposing changes:

```bash
curl -s --max-time 2 --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/connections
curl -s --max-time 2 --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/configs
```

Summarize only the fields needed for diagnosis. Do not paste raw `/configs`, full proxy definitions, provider URLs, auth material, or full connection host lists into a public report. Do not change proxy groups, TUN, rules, DNS hijack, or route exclusions from this skill unless the user explicitly asks. If a proxy-specific fix is needed and a `clash-doctor` or `clash-routes` skill exists, use that skill or hand off to it.

### 5. Verify

Repeat the baseline commands after each accepted change. Compare:

- Download/upload capacity.
- Idle latency and loaded latency/responsiveness.
- Gateway ping min/avg/max/stddev and packet loss.
- DNS query times for the same domains.
- Route/proxy state to confirm VPN/proxy still works.
- User-relevant app endpoint timing, such as `chatgpt.com`, `api.openai.com`, GitHub, package registries, or the user's work domains.

If results are mixed, revert the change unless the user prefers the tradeoff.

## Report Template

Use this structure:

```markdown
**Routing**
Mode: execute_direct | plan_first | clarify_first
Goal:
Constraints:

**Baseline**
- Path: direct | system proxy | TUN | unknown
- Download/upload:
- Idle latency:
- Loaded latency/responsiveness:
- Gateway ping:
- DNS:
- Wi-Fi/Ethernet:

**Findings**
1. [Evidence-backed bottleneck]
2. [Evidence-backed bottleneck]
3. [Evidence-backed bottleneck]

**Actions**
- Done:
- Skipped:
- Proposed:
- Rollback:

**After**
- Same metrics as baseline.
- Delta:

**Decision**
- Keep/revert/no change:
- Remaining risks:
- Next step:
```

## Completion Checklist

Before finalizing, ensure:

- The current proxy/VPN state was identified and preserved.
- Every modification has a rollback command or was reverted.
- Before/after metrics come from this session.
- The report distinguishes local link, DNS, proxy path, router/SQM, and ISP causes.
- No claim is based on an assumed tool output or an earlier run.

## Test Prompts

Use these prompts when evaluating the skill manually:

- "帮我安全优化 macOS 网络，Clash 和 Tailscale 绝对不能动。"
- "我的 Wi-Fi 信号很好但 ping 路由器偶尔 100ms，帮我诊断，不要直接改配置。"
- "把 Codex 网络优化流程跑一遍，输出 before/after 报告和可回滚建议。"

## Version

v1.0 - 2026-05-24 - Initial proxy-safe Codex network optimization workflow based on the viral Codex network optimization pattern and local macOS/Clash diagnostic lessons.
