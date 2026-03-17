---
name: BGP Routing Protocol
description: This skill should be used when the user asks to "configure BGP", "manipulate BGP path selection", "implement BGP confederations", "configure route reflectors", "use BGP communities", or "troubleshoot BGP routing". It provides comprehensive BGP configuration and path manipulation techniques.
version: 1.0.0
tags: [bgp, routing, networking, cisco, path-selection, confederations]
---

# BGP Routing Protocol

## Purpose

Master Border Gateway Protocol (BGP) configuration and path manipulation for enterprise and ISP networks. This skill covers BGP peering, attribute manipulation, confederations, route reflectors, communities, and advanced path control techniques essential for network engineers and penetration testers analyzing routing infrastructure.

## Prerequisites

### Required Environment
- Cisco IOS routers or equivalent
- Multi-AS topology for practice
- Console/SSH access to devices

### Required Knowledge
- IP addressing and subnetting
- Basic routing concepts
- Cisco IOS CLI familiarity

## Outputs and Deliverables

1. **BGP Peering** - Established neighbor relationships
2. **Path Manipulation** - Controlled route selection
3. **Scalable Design** - Confederations and route reflectors
4. **Policy Implementation** - Community-based filtering

## Core Workflow

### Phase 1: Basic BGP Configuration

Establish BGP peering relationships:

```cisco
! Basic eBGP configuration
router bgp 65001
 bgp router-id 1.1.1.1
 neighbor 10.0.0.2 remote-as 65002
 network 192.168.1.0 mask 255.255.255.0

! eBGP with loopback (requires ebgp-multihop)
router bgp 65001
 neighbor 2.2.2.2 remote-as 65002
 neighbor 2.2.2.2 update-source Loopback0
 neighbor 2.2.2.2 ebgp-multihop 3

! Static route for loopback reachability
ip route 2.2.2.2 255.255.255.255 Serial0/0
```

**iBGP Configuration:**
```cisco
! iBGP peering (same AS)
router bgp 65001
 neighbor 3.3.3.3 remote-as 65001
 neighbor 3.3.3.3 update-source Loopback0
 neighbor 3.3.3.3 next-hop-self
```

### Phase 2: BGP Path Selection Process

Understand the BGP best path selection algorithm:

| Priority | Attribute | Preference |
|----------|-----------|------------|
| 1 | Weight | Highest |
| 2 | Local Preference | Highest |
| 3 | Locally Originated | Prefer local |
| 4 | AS-Path Length | Shortest |
| 5 | Origin | IGP < EGP < Incomplete |
| 6 | MED | Lowest |
| 7 | eBGP over iBGP | Prefer eBGP |
| 8 | IGP Metric | Lowest |
| 9 | Router ID | Lowest |

**Verification Commands:**
```cisco
show ip bgp
show ip bgp summary
show ip bgp neighbors
show ip bgp 192.168.1.0/24
```

### Phase 3: Weight Attribute

Influence local path selection (Cisco-proprietary):

```cisco
! Set weight for specific neighbor
router bgp 65001
 neighbor 10.0.0.2 weight 1000

! Set weight using route-map (preferred)
ip prefix-list NETWORK-A seq 5 permit 192.168.1.0/24

route-map SET-WEIGHT permit 10
 match ip address prefix-list NETWORK-A
 set weight 500
route-map SET-WEIGHT permit 20

router bgp 65001
 neighbor 10.0.0.2 route-map SET-WEIGHT in
```

**Key Points:**
- Default weight is 0 (32768 for locally originated)
- Higher weight preferred
- Only locally significant
- Not advertised to neighbors

### Phase 4: Local Preference

Influence AS-wide path selection:

```cisco
! Set local preference for incoming routes
ip prefix-list PREFER-PATH seq 5 permit 10.0.0.0/8

route-map SET-LOCPREF permit 10
 match ip address prefix-list PREFER-PATH
 set local-preference 200
route-map SET-LOCPREF permit 20

router bgp 65001
 neighbor 10.0.0.2 route-map SET-LOCPREF in
```

**Key Points:**
- Default local preference is 100
- Higher value preferred
- Exchanged between iBGP peers
- Used for outbound traffic engineering

**Verification:**
```cisco
show ip bgp
! Look for LocPrf column
```

### Phase 5: AS-Path Prepending

Influence inbound traffic by lengthening AS-path:

```cisco
! Prepend own AS number to outgoing updates
route-map PREPEND permit 10
 set as-path prepend 65001 65001 65001

router bgp 65001
 neighbor 10.0.0.2 route-map PREPEND out
```

**Key Points:**
- Only prepend your own AS number
- Makes path less preferred to remote ASes
- Used for inbound traffic engineering
- Too much prepending can be ignored

### Phase 6: MED (Multi-Exit Discriminator)

Influence inbound traffic between same AS connections:

```cisco
! Set MED for outgoing routes
route-map SET-MED permit 10
 set metric 100

router bgp 65001
 neighbor 10.0.0.2 route-map SET-MED out

! Compare MED from different ASes (not default)
router bgp 65001
 bgp always-compare-med
 bgp bestpath as-path ignore
```

**Key Points:**
- Default MED is 0
- Lower MED preferred
- Only compared for paths from same AS by default
- Suggests preferred entry point to remote AS

### Phase 7: Origin Attribute

Manipulate path preference via origin code:

```cisco
! Set origin in route-map
route-map SET-ORIGIN permit 10
 set origin incomplete

route-map SET-ORIGIN-EGP permit 10
 set origin egp 1

router bgp 65001
 neighbor 10.0.0.2 route-map SET-ORIGIN out
```

**Origin Codes:**
- `i` - IGP (from network command) - Most preferred
- `e` - EGP (legacy) - Middle preference
- `?` - Incomplete (redistributed) - Least preferred

### Phase 8: BGP Confederations

Scale iBGP with sub-AS design:

```cisco
! Sub-AS 65501 configuration
router bgp 65501
 bgp confederation identifier 65000
 bgp confederation peers 65502
 neighbor 10.0.0.2 remote-as 65502
 neighbor 10.0.0.2 next-hop-self
 neighbor 3.3.3.3 remote-as 65501

! Sub-AS 65502 configuration
router bgp 65502
 bgp confederation identifier 65000
 bgp confederation peers 65501
 neighbor 10.0.0.1 remote-as 65501
 neighbor 4.4.4.4 remote-as 65502
```

**Key Points:**
- Appears as single AS to external peers
- Sub-AS numbers typically private (65xxx)
- Confederation peers use special eBGP rules
- Reduces full-mesh iBGP requirement

### Phase 9: Route Reflectors

Alternative iBGP scaling solution:

```cisco
! Route Reflector configuration
router bgp 65001
 neighbor 2.2.2.2 remote-as 65001
 neighbor 2.2.2.2 route-reflector-client
 neighbor 3.3.3.3 remote-as 65001
 neighbor 3.3.3.3 route-reflector-client

! Client configuration (no special config needed)
router bgp 65001
 neighbor 1.1.1.1 remote-as 65001
```

**Reflection Rules:**
- Routes from eBGP peer → Reflect to all clients and non-clients
- Routes from client → Reflect to all clients and non-clients
- Routes from non-client → Reflect only to clients

### Phase 10: BGP Communities

Tag routes for policy application:

```cisco
! Enable community sending
router bgp 65001
 neighbor 10.0.0.2 send-community

! Set community on routes
route-map SET-COMMUNITY permit 10
 set community 65001:100

! Match community for filtering
ip community-list standard BLOCK permit 65001:999

route-map FILTER-COMMUNITY deny 10
 match community BLOCK
route-map FILTER-COMMUNITY permit 20

! Well-known communities
set community no-export       ! Don't advertise outside AS
set community no-advertise    ! Don't advertise to any peer
set community local-as        ! Don't advertise outside local AS
```

**Peer Groups for Efficiency:**
```cisco
router bgp 65001
 neighbor INTERNAL peer-group
 neighbor INTERNAL remote-as 65001
 neighbor INTERNAL update-source Loopback0
 neighbor INTERNAL next-hop-self
 neighbor 2.2.2.2 peer-group INTERNAL
 neighbor 3.3.3.3 peer-group INTERNAL
 neighbor 4.4.4.4 peer-group INTERNAL
```

## Quick Reference

### BGP Attributes

| Attribute | Scope | Manipulation |
|-----------|-------|--------------|
| Weight | Local router | route-map set weight |
| Local-Pref | Within AS | route-map set local-preference |
| AS-Path | Global | route-map set as-path prepend |
| MED | Between ASes | route-map set metric |
| Origin | Global | route-map set origin |

### Common Commands

| Command | Purpose |
|---------|---------|
| `show ip bgp` | Display BGP table |
| `show ip bgp summary` | Neighbor summary |
| `show ip bgp neighbors` | Detailed neighbor info |
| `clear ip bgp *` | Reset all BGP sessions |
| `debug ip bgp updates` | Debug BGP updates |

### Path Selection Shortcuts

| Goal | Best Method |
|------|-------------|
| Prefer outbound path | Local Preference (higher) |
| Influence inbound traffic | AS-Path Prepend |
| Prefer backup link | Weight (local) |
| Signal entry preference | MED (lower) |

## Constraints and Limitations

### Design Considerations
- iBGP requires full mesh or RR/Confederation
- eBGP peers must be directly connected (or ebgp-multihop)
- Synchronization rule with IGP
- Next-hop reachability critical

### Security Implications
- BGP hijacking via unauthorized announcements
- Route leaks between providers
- Lack of built-in authentication (use MD5)
- Prefix filtering essential

## Troubleshooting

### Neighbor Not Establishing

**Symptoms:** State stuck in Active/Idle

**Solutions:**
1. Verify reachability between peers
2. Check AS number configuration
3. Verify update-source for loopback peering
4. Check ebgp-multihop for non-direct connections
5. Verify no ACL blocking TCP 179

### Routes Not in Table

**Symptoms:** Neighbors up but missing routes

**Solutions:**
1. Verify network statement or redistribution
2. Check route-map filtering
3. Verify next-hop reachability
4. Check prefix-list/filter-list
5. Verify synchronization requirements

### Path Selection Issues

**Symptoms:** Wrong path selected

**Solutions:**
1. Check weight settings (highest priority)
2. Verify local preference values
3. Compare AS-path lengths
4. Check MED values (if same AS)
5. Use `show ip bgp <prefix>` for detailed analysis
