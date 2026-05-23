---
name: network-fundamentals-cloud
description: Networking fundamentals as they apply to cloud infrastructure — virtual networks, subnets, routers, NAT, floating IPs, security groups, VLAN/VXLAN segmentation, load balancing, SDN concepts, and how Neutron-style cloud networks sit on top of physical topology. Covers TCP behavior at scale, congestion control, tail latency, overlay networks, and the operational gotchas that come from network layering. Use when designing cloud network topology, debugging cross-AZ latency, or reviewing a proposed VPC/SG design.
type: skill
category: cloud-systems
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/cloud-systems/network-fundamentals-cloud/SKILL.md
superseded_by: null
---
# Network Fundamentals for Cloud

The cloud's network is physical hardware pretending to be software. Virtual networks, subnets, security groups, and load balancers are abstractions over a datacenter's actual wires and switches — and every abstraction leaks at the operational layer. This skill covers the networking concepts a cloud-systems practitioner needs to design, debug, and reason about cloud network topology, and the places where the underlying physical reality surfaces as a surprise.

**Agent affinity:** hamilton-cloud (datacenter network economics), vogels (service-oriented network boundaries), dean (high-performance intra-datacenter networking)

**Concept IDs:** cloud-neutron-networking, cloud-security-groups-policies, cloud-multi-service-coordination

## The OSI Layers, Minus the Nonsense

Cloud networking mostly lives at four layers:

- **L2 (link).** MAC addresses, Ethernet frames, VLAN tags, ARP. The layer virtual switches speak.
- **L3 (network).** IP addresses, routing, subnets. Where SDN controllers live.
- **L4 (transport).** TCP, UDP, QUIC. Where load balancers often terminate.
- **L7 (application).** HTTP, gRPC, database protocols. Where service meshes live.

The cloud network is a stack of overlays: your L2 frames are encapsulated in L3 IP packets that traverse the physical network, unwrapped at the other end, and delivered as if they were on the same switch. Understanding that the overlay and underlay are distinct helps when debugging "this ping should work" moments.

## Virtual Networks and Tenant Isolation

A cloud virtual network gives a tenant a dedicated L2 or L3 network with their own address space, independent of other tenants on the same hardware. Two common isolation mechanisms:

**VLANs (IEEE 802.1Q).** A 12-bit tag in the Ethernet frame. Maximum 4094 VLANs per physical network — fine for a small datacenter, inadequate for a cloud with thousands of tenants.

**VXLAN (RFC 7348).** Encapsulates Ethernet frames in UDP, with a 24-bit segment ID (about 16 million segments). Frames are tunneled over the L3 network, so the physical topology doesn't need to provide L2 adjacency. VXLAN (and its cousins GENEVE, NVGRE, STT) is how large clouds do multi-tenant network isolation.

The virtual network abstraction in Neutron or AWS VPC presents the tenant with a subnet, a default gateway, security groups, and routes — and hides VXLAN or the cloud-specific overlay entirely. When it breaks, troubleshooting requires descending into the overlay.

## Subnets, Routers, and the Default Gateway

A subnet is an IP range (e.g., 10.0.1.0/24) assigned to a virtual network, along with DHCP for instance addresses and a default gateway address. Instances in the subnet can talk to each other directly; to reach other subnets they route through the gateway.

A virtual router connects multiple subnets. In a typical cloud setup:

- Each project has one or more networks, each with one or more subnets.
- A virtual router connects the project's subnets to each other (east-west).
- The router also connects to an external network (the provider's internet-facing network) for north-south traffic.
- SNAT (source NAT) on the router lets instances reach the internet without having globally routable addresses.
- Floating IPs (1:1 DNAT) give specific instances public addresses.

The router is a virtual construct but its forwarding is real — every packet hits some SDN data plane.

## Security Groups: Stateful L3/L4 Firewalls

A security group is a stateful firewall applied per-instance (or per-port). It has two rule sets:

- **Ingress rules.** Traffic entering the instance. Default deny-all.
- **Egress rules.** Traffic leaving the instance. Default allow-all in most clouds (this is the security trap).

Rules specify protocol, port range, and source/destination (as CIDR or as another security group). The "source is another security group" is the key pattern — it gives a handle you can reason about without knowing instance IPs.

Statefulness means: if an instance initiates an outbound connection and egress rules permit it, the return traffic is automatically allowed even though no ingress rule exists. Reply traffic follows the conntrack flow.

**Default-deny discipline.** The baseline security group should allow only the minimum needed. A rule allowing `0.0.0.0/0` on port 22 is almost always a mistake in production.

## Load Balancers

Three common shapes:

**L4 (TCP/UDP) load balancer.** Distributes connections at the transport layer. Doesn't see HTTP headers. Fast and protocol-agnostic. Good for non-HTTP or when preserving client IP matters.

**L7 (HTTP) load balancer.** Terminates the TCP connection, reads HTTP headers, applies routing rules based on host/path/headers, forwards to backend. Can do TLS termination, rewrite headers, inject tracing.

**Global load balancer.** DNS-based or Anycast-based. Routes clients to the nearest healthy region. Composed with L4 or L7 load balancers per region.

Health checks determine which backends are "in" the load balancing pool. Tuning health check sensitivity is a classic trade-off: strict checks remove unhealthy backends quickly but also remove healthy ones under transient load; lenient checks send traffic to dying backends.

## TCP at Cloud Scale

TCP works differently inside a datacenter than on the open internet.

**Intra-datacenter.** Low RTT (microseconds), low loss, high bandwidth. TCP's standard loss-as-congestion-signal is too coarse — a single lost packet causes window collapse and latency spikes. DCTCP, BBR, and other modern congestion controls use RTT or ECN instead of loss.

**Cross-region.** High RTT (tens of milliseconds), noticeable loss. Classical TCP works, but throughput is bound by window size / RTT.

**Incast.** Many senders transmit to one receiver simultaneously. Synchronized window collapse causes sustained throughput drops. The classic example is MapReduce shuffle.

**Head-of-line blocking.** TCP delivers bytes in order, so a single lost packet stalls delivery of subsequent packets even if they arrived. HTTP/2's multiplexing exposed this — one HTTP/2 stream's loss stalls all streams. QUIC fixes it by moving to UDP and doing its own ordering per stream.

## Tail Latency and the P99 Discipline

At cloud scale, average latency is misleading. A service with 1 ms average latency and a 50 ms P99 is a service where 1 in 100 requests takes 50x longer. Because most user-visible requests fan out to many services, P99 latency of individual services becomes the common-case latency of the whole system.

**Dean's tail-at-scale observations.** Sources of tail latency: GC pauses, periodic daemons, background maintenance, kernel scheduling quanta, contention on shared resources.

**Mitigations.**

- **Hedged requests.** Send to two replicas after a short delay; use whichever responds first. Costs 2x for a small subset of requests.
- **Tied requests.** Send to multiple replicas immediately with a "cancel if another beats you" marker. Costs little once the first responds.
- **Good admission control.** Reject rather than queue when the backend is at its limit. Slow failures are worse than fast failures.

## SDN and Control Plane Separation

Software-Defined Networking separates the control plane (where routes and policies are computed) from the data plane (where packets are forwarded). Benefits:

- Policies are defined centrally and pushed to switches.
- Network state is a database, not the aggregate of dozens of devices.
- Changes propagate quickly and can be rolled back atomically.

Protocols like OpenFlow, Open vSwitch, and vendor-specific APIs are the plumbing. Cloud networking teams build SDN control planes that compose tenant virtual networks, security groups, and load balancers into actual forwarding rules on physical switches and virtual switches.

## MTU and the Fragmentation Problem

Every network path has a maximum transmission unit. When a packet exceeds it, the router either fragments it or sends ICMP "fragmentation needed" back to the sender. Overlay networks reduce effective MTU because the outer encapsulation consumes bytes:

- Physical Ethernet MTU: 1500 bytes.
- VXLAN adds ~50 bytes of headers.
- Effective MTU for tenants: 1450 bytes.

If the tenant's TCP stack thinks MTU is 1500 and ICMP is filtered (common mistake), connections mysteriously stall on large packets. Setting MTU correctly in DHCP / route advertisements, and not filtering ICMP "fragmentation needed" messages, is an operational must-do.

## Common Failure Modes

| Failure | Symptom | Root cause |
|---|---|---|
| Asymmetric routing | TCP connections stall mid-session | Return path goes through a different stateful firewall |
| MTU mismatch | Large writes hang, small ones work | Overlay MTU smaller than expected, ICMP filtered |
| ARP table overflow | Intermittent "no route to host" | Too many instances on one L2 segment |
| Cross-AZ latency spike | P99 inflation, P50 fine | Traffic leaking to non-local AZ due to routing policy |
| Security group leak | Instance reachable from unexpected source | `0.0.0.0/0` rule committed inadvertently |
| Load balancer health flap | Backends cycle in and out | Health check too aggressive, or shared resource causing correlated failures |
| BGP withdrawal | Region unreachable | Upstream routing change, dark fiber cut |

## When to Use This Skill

- Designing a VPC / tenant network topology for a new cloud deployment.
- Debugging a network-layer incident (latency, drops, partial reachability).
- Reviewing security group rules for over-permissiveness.
- Planning multi-region or multi-AZ traffic patterns.
- Sizing load balancers and health check policies.
- Optimizing for tail latency in a high-fan-out service.

## When NOT to Use This Skill

- Single-host networking. Local loopback has its own patterns.
- Pure application-level concerns that do not interact with the network fabric.

## Decision Guidance

| Need | Recommended |
|---|---|
| Tenant isolation at scale | VXLAN/GENEVE overlay |
| Intra-datacenter L4 | DCTCP or BBR-like congestion control |
| Cross-region replication | TCP with larger windows, or QUIC |
| High fan-out services | Hedged or tied requests, tight timeouts |
| Public API endpoint | L7 LB with TLS termination, WAF in front |
| Service mesh east-west | L4+L7 combined via sidecar |
| Failure-domain isolation | Distinct AZs, distinct BGP sessions, distinct power |

## References

- Dean, J., Barroso, L. (2013). "The Tail at Scale." CACM 56(2).
- Alizadeh, M., et al. (2010). "Data Center TCP (DCTCP)." SIGCOMM.
- Cardwell, N., et al. (2017). "BBR: Congestion-based Congestion Control." CACM.
- Mahalingam, M., et al. (2014). "VXLAN: A Framework for Overlaying Virtualized Layer 2 Networks." RFC 7348.
- Barroso, L., Clidaras, J., Holzle, U. (2013). *The Datacenter as a Computer*. Morgan & Claypool.
- Neutron documentation, OpenStack project.
- AWS VPC documentation.
