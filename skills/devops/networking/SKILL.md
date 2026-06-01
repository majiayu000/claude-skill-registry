---
name: networking
description: >
  · Configure/troubleshoot Linux networking: DNS, proxies, VPNs, VLANs, nftables, routing. Triggers: 'dns', 'reverse proxy', 'vpn', 'wireguard', 'tailscale', 'vlan', 'nftables', 'bgp', 'ospf', 'frrouting'. Not OPNsense: firewall-appliance.
license: MIT
compatibility: "Requires Linux. Tools vary by task: nftables, WireGuard, dig, mtr, tcpdump"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-25"
  effort: high
  argument_hint: "<task-or-topology>"
---

# Networking: Configuration, Troubleshooting, and Optimization

Configure, troubleshoot, and optimize Linux networking infrastructure. Covers DNS, reverse proxies,
VPNs, firewalls (nftables), VLANs, subnetting, high availability, dynamic routing, and network
performance tuning.

**Target versions** (May 2026):

| Tool | Version | Notes |
|------|---------|-------|
| Caddy | 2.11.2 | Auto-HTTPS, Caddyfile + JSON API |
| Nginx | 1.30.0 stable / 1.29.8 mainline | New stable branch released Apr 2026; verify current advisories |
| Traefik | 3.6.14 | Gateway API native, v2 EOL approaching |
| HAProxy | 3.3.7 stable / 3.2.16 LTS | LTS EOL 2030-Q2 |
| WireGuard tools | 1.0.20260223 | Kernel module + userspace tools |
| strongSwan | 6.0.6 | swanctl config (legacy ipsec.conf deprecated) |
| nftables | 1.1.6 | iptables successor, default on modern distros |
| keepalived | 2.3.4 | VRRP + health checks |
| Unbound | 1.24.2 | CVE-2025-11411 fix (unsolicited NS RRSets) |
| CoreDNS | 1.14.2 | K8s default DNS, plugin-based |
| FRRouting | 10.6.0 | BGP, OSPF, IS-IS, PIM |
| Tailscale / Headscale | Headscale 0.28.0 | Self-hosted control server |
| cloudflared | 2026.3.0 | Cloudflare Tunnel (outbound-only) |
| OpenVPN | 2.7.2 / 2.6.20 LTS | 2.7.x: multi-socket, DCO; 2.6 is the LTS branch |

## When to use

- Configuring DNS servers (Unbound, CoreDNS, dnsmasq, BIND9, Pi-hole, AdGuard Home)
- Setting up or troubleshooting reverse proxies and load balancers
- VPN configuration (WireGuard, OpenVPN, IPsec) and overlay networks
- Linux firewall rules (nftables, legacy iptables)
- VLAN configuration, subnetting, network segmentation
- High availability with keepalived/VRRP, floating IPs
- Network diagnostics (tcpdump, mtr, ss, dig, iperf3, Wireshark/tshark)
- TCP/network performance tuning (MTU, buffers, congestion control, bufferbloat)
- Dynamic routing with FRRouting (BGP, OSPF)
- TLS/certificate management for network services
- Split-horizon DNS, DNS-over-HTTPS/TLS, DNSSEC

## When NOT to use

- OPNsense/pfSense firewall appliance management (use **firewall-appliance**)
- Web browsing, scraping, or headless page interaction - use **browse**
- Kubernetes networking: NetworkPolicy, Gateway API, service mesh, CNI (use **kubernetes**)
- Broad Kubernetes cluster health checks, node status, and post-maintenance diagnostics (use **cluster-health**)
- Docker/container networking: bridge, overlay, Compose networks (use **docker**)
- Cloud VPCs, security groups, managed load balancers (use **terraform**)
- Network config management at scale via playbooks (use **ansible**)
- Offensive pentesting, exploitation, lateral movement (use **lockpick**)
- Application-level security review, SSRF, header injection (use **security-audit**)
- CI/CD-automated network configuration management at pipeline scale (use **ci-cd**)

---

## AI Self-Check

Before returning any generated network configuration, verify:

- [ ] **No hardcoded secrets**: passwords, PSKs, API keys use placeholders or env vars
- [ ] **Correct interface names**: didn't assume `eth0` - modern Linux uses predictable names
  (`enp0s3`, `ens18`, etc.). Ask or check `ip link` output
- [ ] **MTU considered**: VPN tunnels need reduced MTU (WireGuard: 1420, OpenVPN: ~1400, VXLAN:
  1450). Mismatched MTU causes silent packet drops
- [ ] **DNS resolver order**: systemd-resolved vs /etc/resolv.conf vs NetworkManager - check
  which DNS manager is active before modifying
- [ ] **Firewall persistence**: nftables rules need `nft list ruleset > /etc/nftables.conf` or
  a service to persist across reboots. Raw `nft add` commands are ephemeral
- [ ] **Port conflicts checked**: reverse proxy ports (80, 443) may conflict with existing
  services. Verify with `ss -tlnp`
- [ ] **TLS versions**: minimum TLS 1.2 for all services. TLS 1.3 preferred where supported
- [ ] **Private IP ranges correct**: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 (not /24)
- [ ] **Subnet overlap**: VPN address ranges must not overlap with LAN or other VPN ranges
- [ ] **IPv6 considered**: dual-stack config or explicit disable. Half-configured IPv6 leaks
  traffic around IPv4-only VPNs
- [ ] **Backup before modifying**: save current config before changes (`nft list ruleset >
  backup.nft`, `cp nginx.conf nginx.conf.bak`). Network misconfigs can lock out remote access
- [ ] **Service reload vs restart**: prefer graceful reload (`nginx -s reload`, `systemctl
  reload`) over restart to avoid dropping active connections
- [ ] **IP forwarding enabled**: any config involving routing, VPN, or inter-VLAN traffic
  needs `net.ipv4.ip_forward = 1` (and `net.ipv6.conf.all.forwarding = 1` for dual-stack).
  Without it, the kernel silently drops forwarded packets
- [ ] **systemd-resolved conflict**: if deploying a local DNS server (Unbound, CoreDNS,
  dnsmasq), check whether systemd-resolved is binding port 53. Disable its stub listener
  (`DNSStubListener=no`) or bind your server to a different port
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Topology verified**: interface names, routes, DNS resolvers, namespaces, VPN state, and firewall backend are observed before changes
- [ ] **Rollback path preserved**: remote network changes include timed rollback, console access, or an alternate path

---

## Performance

- Measure path, DNS, TLS, and application latency separately before tuning.
- Use packet captures with narrow filters and time windows to avoid huge captures and privacy spill.
- Prefer persistent nftables sets, DNS caches, and proxy connection reuse where appropriate.


---

## Best Practices

- Diagnose before changing: capture current routes, rules, addresses, and resolver state.
- Change one layer at a time: DNS, routing, firewall, proxy, VPN, or application.
- Keep emergency access open when editing firewall, VPN, or default-route configuration remotely.


## Workflow

### Step 1: Identify the task type

| Task type | Start with | Reference |
|-----------|------------|-----------|
| **Troubleshoot** | Symptoms, recent changes, affected scope | `references/troubleshooting.md` |
| **Configure DNS** | Current resolver, authoritative vs recursive, split-horizon needs | `references/dns.md` |
| **Set up reverse proxy** | Which proxy, upstream services, TLS requirements | `references/reverse-proxies.md` |
| **Configure VPN** | Topology (p2p, hub-spoke, mesh), protocol choice | `references/vpn.md` |
| **Network segmentation** | VLANs, subnets, nftables zones, namespaces | `references/segmentation.md` |
| **High availability** | keepalived/VRRP, floating IPs, health checks | `references/ha.md` |

### Step 2: Gather context

Before writing config or running commands:

1. **What distro and init system?** (systemd vs OpenRC - affects service management)
2. **What's the current network state?** (`ip addr`, `ip route`, `ss -tlnp`, `resolvectl status`)
3. **Is there an existing firewall?** (`nft list ruleset`, `iptables-save`)
4. **Who manages DNS?** (`resolvectl status` or `cat /etc/resolv.conf` - check for systemd-resolved stub)
5. **Any existing VPN/overlay?** (`wg show`, `tailscale status`, `ip link` for tun/wg/vxlan devices)
6. **Is this behind NAT?** (affects VPN, reverse proxy, and HA design)

### Step 3: Implement

Read the appropriate reference file for detailed patterns. Key principles:

- **Test before persisting.** Add nftables rules, verify connectivity, then save. Apply reverse
  proxy config changes with `--dry-run` or syntax check first (`caddy validate`, `nginx -t`,
  `haproxy -c`).
- **One change at a time.** Network misconfigs can lock you out. If working over SSH, set a
  revert timer (`at now + 5 minutes <<< 'systemctl restart networking'`).
- **Log what you changed.** Network debugging is 10x harder when you don't know what changed.

### Step 4: Validate

| What to validate | How |
|-----------------|-----|
| DNS resolution | `dig @server domain A +short`, `dig domain AAAA +short` |
| Reverse proxy | `curl -vk https://domain` (check cert, headers, upstream response) |
| VPN tunnel | `wg show` (WireGuard), `ping` across tunnel, check `ip route` |
| Firewall rules | `nft list ruleset`, test both allowed and blocked traffic |
| VLAN tagging | `ip -d link show`, `tcpdump -e -i interface` (check 802.1Q tags) |
| HA failover | Stop primary, verify VIP migrates, check `journalctl -u keepalived` |
| Performance | `iperf3 -c server`, `mtr target`, check for packet loss and jitter |

---

## Quick Reference: Diagnostic Tools

| Tool | Purpose | Key usage |
|------|---------|-----------|
| `ip` | Interface, route, neighbor, rule management | `ip addr`, `ip route`, `ip neigh`, `ip link` |
| `ss` | Socket statistics (replaces netstat) | `ss -tlnp` (TCP listeners), `ss -ulnp` (UDP) |
| `dig` | DNS queries | `dig @8.8.8.8 example.com A +short` |
| `mtr` | Combined traceroute + ping | `mtr -n --report target` (non-interactive) |
| `tcpdump` | Packet capture | `tcpdump -i any -nn port 53` (DNS traffic) |
| `tshark` | Wireshark CLI | `tshark -i any -f 'port 443' -Y 'tls.handshake'` |
| `curl` | HTTP testing | `curl -vk -o /dev/null https://target` (verbose TLS info) |
| `iperf3` | Bandwidth testing | Server: `iperf3 -s` / Client: `iperf3 -c server` |
| `nft` | nftables rule management | `nft list ruleset`, `nft monitor trace` |
| `wg` | WireGuard status | `wg show`, `wg showconf wg0` |
| `resolvectl` | systemd-resolved status | `resolvectl status`, `resolvectl query domain` |
| `doggo` | Modern dig alternative | `doggo example.com A @8.8.8.8 --json` |
| `nmap` | Port scanning, service detection | `nmap -sV -p 1-1024 target` |
| `socat` | Multipurpose relay | `socat TCP-LISTEN:8080,fork TCP:backend:80` |

---

## Quick Reference: CIDR Cheat Sheet

| CIDR | Netmask | Hosts | Common use |
|------|---------|-------|------------|
| /32 | 255.255.255.255 | 1 | Host route, loopback |
| /31 | 255.255.255.254 | 2 | Point-to-point link (RFC 3021) |
| /30 | 255.255.255.252 | 2 | Legacy point-to-point |
| /29 | 255.255.255.248 | 6 | Small service subnet |
| /28 | 255.255.255.240 | 14 | DMZ, management |
| /27 | 255.255.255.224 | 30 | Small office |
| /26 | 255.255.255.192 | 62 | Department |
| /25 | 255.255.255.128 | 126 | Floor / building wing |
| /24 | 255.255.255.0 | 254 | Standard LAN segment |
| /16 | 255.255.0.0 | 65534 | Large campus / datacenter |
| /8 | 255.0.0.0 | 16M+ | Class A (10.0.0.0/8) |

**Private ranges (RFC 1918):** `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
**CGNAT (RFC 6598):** `100.64.0.0/10` (used by Tailscale, carrier NAT)
**Link-local:** `169.254.0.0/16` (IPv4), `fe80::/10` (IPv6)
**ULA (IPv6):** `fd00::/8` (private, like RFC 1918 for IPv6)

---

## Quick Reference: DNS Record Types

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | `example.com. 300 IN A 93.184.216.34` |
| AAAA | IPv6 address | `example.com. 300 IN AAAA 2606:2800:220:1::` |
| CNAME | Alias to another name | `www.example.com. IN CNAME example.com.` |
| MX | Mail server | `example.com. IN MX 10 mail.example.com.` |
| TXT | Arbitrary text (SPF, DKIM, verification) | `example.com. IN TXT "v=spf1 ..."` |
| SRV | Service location | `_sip._tcp.example.com. IN SRV 10 5 5060 sip.example.com.` |
| NS | Nameserver delegation | `example.com. IN NS ns1.example.com.` |
| CAA | Certificate authority authorization | `example.com. IN CAA 0 issue "letsencrypt.org"` |
| SVCB/HTTPS | Service binding (newer) | `example.com. IN HTTPS 1 . alpn="h2,h3"` |
| PTR | Reverse DNS | `34.216.184.93.in-addr.arpa. IN PTR example.com.` |

---

## Quick Reference: Reverse Proxy Selection

| Proxy | Best for | TLS | Config style | L4 support |
|-------|----------|-----|-------------|------------|
| **Caddy** | Simple setups, auto-HTTPS | Automatic (ACME) | Caddyfile / JSON API | Yes (experimental) |
| **Nginx** | High traffic, static files | Manual or certbot | nginx.conf | Yes (stream module) |
| **Traefik** | Docker/K8s, dynamic backends | Automatic (ACME) | Labels / file / K8s CRDs | Yes (TCP/UDP) |
| **HAProxy** | Pure load balancing, L4/L7 | Manual | haproxy.cfg | Yes (native) |

### Caddy reverse proxy quick start

```
# /etc/caddy/Caddyfile - three subdomains, auto-HTTPS
app.example.com {
    reverse_proxy localhost:3000
}

api.example.com {
    reverse_proxy localhost:8080
}

grafana.example.com {
    reverse_proxy localhost:3001
}
```

Caddy handles TLS certificate provisioning automatically via ACME (Let's Encrypt). DNS A/AAAA
records for all three subdomains must point to the host. Validate: `caddy validate --config /etc/caddy/Caddyfile`.

Read `references/reverse-proxies.md` for configuration patterns, TLS setup,
health checks, rate limiting, and WebSocket/gRPC proxying.

---

## Quick Reference: VPN Protocol Selection

| Protocol | Speed | Complexity | Key exchange | Best for |
|----------|-------|-----------|--------------|----------|
| **WireGuard** | Fastest | Minimal config | Noise (Curve25519) | P2P, hub-spoke, general use |
| **OpenVPN** | Good | Complex PKI | TLS/x509 | Legacy, tap mode (L2) |
| **IPsec (strongSwan)** | Good | Most complex | IKEv2 | Site-to-site, standards compliance |
| **Tailscale/Headscale** | Fast (WG underneath) | Zero config | WG + DERP relays | Overlay mesh, remote access |
| **Nebula** | Fast | Low | Certificate-based | Large mesh, Slack-scale |

### WireGuard site-to-site quick start

```ini
# Site A (/etc/wireguard/wg0.conf) - 10.0.1.0/24
[Interface]
PrivateKey = <SITE_A_PRIVATE_KEY>
Address = 10.100.0.1/30
ListenPort = 51820
# MTU = 1420 for most setups; subtract 80 more if over PPPoE

[Peer]
PublicKey = <SITE_B_PUBLIC_KEY>
Endpoint = site-b.example.com:51820
AllowedIPs = 10.0.2.0/24, 10.100.0.2/32
PersistentKeepalive = 25

# Site B (/etc/wireguard/wg0.conf) - 10.0.2.0/24
[Interface]
PrivateKey = <SITE_B_PRIVATE_KEY>
Address = 10.100.0.2/30
ListenPort = 51820

[Peer]
PublicKey = <SITE_A_PUBLIC_KEY>
Endpoint = site-a.example.com:51820
AllowedIPs = 10.0.1.0/24, 10.100.0.1/32
PersistentKeepalive = 25
```

Both sides need `net.ipv4.ip_forward = 1` in `/etc/sysctl.d/`. **AllowedIPs** is the remote
subnet (not `0.0.0.0/0` - that's full-tunnel, not site-to-site). Key generation:
`wg genkey | tee privatekey | wg pubkey > publickey`.

Read `references/vpn.md` for setup patterns, key management, MTU tuning,
NAT traversal, and overlay network comparison.

---

## Quick Reference: nftables vs iptables

iptables is legacy. nftables is the default on Debian 11+, RHEL 9+, Arch, and most modern distros.

```
# Minimal nftables ruleset - stateful firewall with SSH
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    ct state established,related accept
    iif lo accept
    tcp dport 22 accept
    icmp type echo-request accept
    icmpv6 type { echo-request, nd-neighbor-solicit, nd-router-advert } accept
  }
  chain forward { type filter hook forward priority 0; policy drop; }
  chain output { type filter hook output priority 0; policy accept; }
}
```

Read `references/segmentation.md` for VLAN setup, nftables zones, network
namespaces, and inter-VLAN routing patterns.

---

## PCI-DSS 4.0 Relevance

Network configuration touches several PCI-DSS requirements:

| Req | Area | What to check |
|-----|------|--------------|
| 1.2 | Network security controls | Firewall rules restrict inbound/outbound to minimum necessary |
| 1.3 | CDE segmentation | VLANs, nftables, or physical separation between CDE and other networks |
| 1.4 | Trusted/untrusted boundaries | Reverse proxy TLS termination, WAF placement |
| 2.2 | Hardening | Disable unnecessary services, unused ports closed |
| 4.1 | Encryption in transit | TLS 1.2+ everywhere, no plaintext on untrusted segments |
| 11.3 | Network monitoring | IDS/IPS (Suricata), log aggregation, flow analysis |

---

## Reference Files

- `references/dns.md` - DNS server comparison, DNSSEC, split-horizon,
  DoH/DoT, Pi-hole/AdGuard, troubleshooting
- `references/reverse-proxies.md` - Caddy, Nginx, Traefik, HAProxy
  configuration patterns, TLS, WebSocket, gRPC, rate limiting
- `references/vpn.md` - WireGuard, OpenVPN, IPsec/strongSwan setup,
  overlay networks (Tailscale, Headscale, Nebula, ZeroTier), key management
- `references/segmentation.md` - VLANs, subnetting, nftables firewall
  patterns, network namespaces, IPv6
- `references/troubleshooting.md` - Diagnostic methodology, tool deep-dives,
  common issues, performance tuning
- `references/ha.md` - keepalived/VRRP, floating IPs, HAProxy + keepalived
  HA, health check patterns

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** NETWORKING
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/networking/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **firewall-appliance** - manages BSD-based firewall appliances (OPNsense, pfSense). This skill
  handles Linux networking; firewall-appliance handles FreeBSD appliance firewalls. If the user
  mentions pfctl, CARP, or OPNsense/pfSense hostnames, route to firewall-appliance.
- **kubernetes** - owns K8s networking (NetworkPolicy, Gateway API, service mesh, CNI). This
  skill covers general DNS and proxy config; K8s-specific networking goes to kubernetes.
- **cluster-health** - owns read-only Kubernetes cluster diagnostics. If the request is
  "is the cluster healthy?" rather than "configure DNS/proxy/routing", route there.
- **docker** - owns container networking (bridge, Compose networks, port mapping). This skill
  covers host-level Linux networking.
- **terraform** - owns cloud infrastructure (VPCs, security groups, cloud LBs, Route53). This
  skill covers bare-metal/VM networking.
- **ansible** - manages config at scale via playbooks. This skill provides the networking
  knowledge; ansible handles the automation wrapper.
- **lockpick** - offensive network testing, exploitation, lateral movement. This skill covers
  defensive configuration and hardening.
- **security-audit** - application-level security review (SSRF, header injection). This skill
  covers network-layer security (firewalls, TLS, segmentation).
- **browse** - web browsing, scraping, headless page interaction. This skill covers network
  infrastructure, not web content retrieval.
- **ci-cd** - pipeline design for automated network config management. This skill provides the networking knowledge; ci-cd handles pipeline orchestration around it.

## Rules

1. **Ask which interface.** Never assume `eth0`. Modern Linux uses predictable interface names.
   Check with `ip link` or ask the user.
2. **Test before persisting.** Network misconfigs can lock you out of remote machines. Apply
   changes temporarily, verify connectivity (especially SSH), then persist.
3. **MTU matters.** VPN tunnels, VXLAN, and PPPoE all reduce effective MTU. Mismatched MTU
   causes silent packet drops that are painful to debug. Always calculate and set explicitly.
4. **Check who manages DNS.** systemd-resolved, NetworkManager, and manual /etc/resolv.conf
   fight each other. Identify the active manager before making DNS changes.
5. **Verify the existing firewall.** Check `nft list ruleset` and `iptables-save` before
   adding rules. Mixing nftables and iptables on the same system causes unpredictable behavior.
6. **No plaintext on untrusted segments.** TLS 1.2+ for all services. If something needs to
   cross an untrusted network without TLS, tunnel it through a VPN.
7. **Subnet overlap kills VPNs.** Before assigning VPN address ranges, inventory all LAN
   subnets and existing VPN ranges. Overlapping ranges cause routing black holes.
8. **Defer to specialized skills.** OPNsense/pfSense -> firewall-appliance. K8s networking -> kubernetes.
   Container networking -> docker. Cloud infra -> terraform. Pentesting -> lockpick.
