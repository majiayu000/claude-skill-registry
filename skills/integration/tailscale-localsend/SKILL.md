---
name: tailscale-localsend
description: Tailscale + LocalSend Peer Discovery
version: 1.0.0
---

# Tailscale + LocalSend Peer Discovery

Discover peers via Tailscale mesh and exchange files via LocalSend protocol.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Tailscale API  │────▶│  Peer Discovery  │────▶│  LocalSend API  │
│  (mesh network) │     │  (propagator)    │     │  (file xfer)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## Discovery Flow

1. **Tailscale Status**: `tailscale status --json` → get mesh peers
2. **LocalSend Probe**: UDP multicast 224.0.0.167:53317 → find localsend-enabled peers  
3. **Intersection**: Peers on both networks get deterministic Gay.jl colors

## Usage

```bash
# Discover peers on tailscale with localsend
just ts-localsend-discover

# Send file to peer
just ts-localsend-send <peer> <file>

# Receive mode
just ts-localsend-receive
```

## Python API

```python
from tailscale_localsend import TailscaleLocalSend

tls = TailscaleLocalSend(seed=0x6761795f636f6c6f)

# Discover peers
peers = tls.discover()
# [{'name': 'macbook', 'tailscale_ip': '100.x.x.x', 'localsend_port': 53317, 'color': '#A855F7'}]

# Send file
tls.send(peer='macbook', file='data.json')

# Receive (blocking)
tls.receive(callback=lambda f: print(f"Got {f}"))
```

## Protocol Details

### Tailscale Discovery
- Uses `tailscale status --json` for mesh peers
- Extracts TailscaleIPs for each peer
- Falls back to Tailscale API if CLI unavailable

### LocalSend Protocol
- **Multicast**: 224.0.0.167:53317 (UDP)
- **Announce**: JSON with alias, fingerprint, port
- **Transfer**: REST API over HTTPS
  - `POST /api/localsend/v2/prepare-upload`
  - `POST /api/localsend/v2/upload?sessionId=...`

### Color Assignment
Each peer gets deterministic color from Gay.jl:
```python
peer_color = gay_color_at(hash(peer_fingerprint) % 1000, seed=GAY_SEED)
```

## Integration with epistemic-arbitrage

```python
from epistemic_arbitrage import ArbitrageNetwork

network = ArbitrageNetwork(seed=1069)
for peer in tls.discover():
    network.add_cell(peer['name'], knowledge=peer.get('files', 0))
    
# Propagate knowledge between peers
network.add_propagator(:peer_sync, sources, targets)
network.run_parallel(n_workers=len(peers))
```

## Commands

```bash
just ts-peers          # List tailscale peers
just ls-peers          # List localsend peers  
just ts-ls-bridge      # Bridge both networks
```

Base directory: ~/.codex/skills/tailscale-localsend



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `distributed-systems`: 3 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 7. Propagators

**Concepts**: propagator, cell, constraint, bidirectional, TMS

### GF(3) Balanced Triad

```
tailscale-localsend (−) + SDF.Ch7 (○) + [balancer] (+) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch1: Flexibility through Abstraction

### Connection Pattern

Propagators flow constraints bidirectionally. This skill propagates information.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.