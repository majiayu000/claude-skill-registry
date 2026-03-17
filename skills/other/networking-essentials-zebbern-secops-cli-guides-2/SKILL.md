---
name: Networking Essentials
description: |
  The assistant provides comprehensive networking fundamentals including OSI model, TCP/IP, cabling, VLAN configuration, and Cisco router/switch commands. Activate when users ask about "network basics," "OSI model," "TCP/IP addressing," "subnetting," "VLAN configuration," "Cisco commands," or "network infrastructure."
version: "1.0.0"
tags:
  - networking
  - cisco
  - routing
  - switching
  - tcp-ip
  - infrastructure
---

# Networking Essentials

## Purpose

Provide foundational networking knowledge required for penetration testing including OSI model concepts, TCP/IP addressing, subnetting, cable standards, and Cisco device configuration. Enable understanding of network infrastructure for effective security assessments.

## Inputs/Prerequisites

- Basic computer literacy
- Access to network devices or simulator (Packet Tracer, GNS3)
- Understanding of binary and hexadecimal notation
- Network topology information for target environment

## Outputs/Deliverables

- Properly configured network infrastructure
- Subnetting calculations and IP schemes
- VLAN segmentation plans
- Router and switch configurations
- Network documentation for assessments

## Core Workflow

### 1. Understand Network Types

**Network Categories:**
- **LAN (Local Area Network)**: Single location, high speed
- **WAN (Wide Area Network)**: Multiple locations, geographic dispersion
- **Internet**: Global interconnection of networks

**LAN Architectures:**
- **Client/Server**: Centralized resources and management
- **Peer-to-Peer**: Decentralized, each device shares resources

### 2. Master Cable Standards

**UTP Cable Categories:**

| Category | Speed | Use Case |
|----------|-------|----------|
| CAT 3 | 10 Mbps | Ethernet |
| CAT 5 | 100 Mbps | Fast Ethernet |
| CAT 5e | 1 Gbps | Gigabit Ethernet |
| CAT 6 | 1 Gbps | Multi-Gigabit |

**Cable Wiring Standards:**

**Straight-Through (T568A to T568A):**
- Use: PC to Switch, Router to Switch
- Pin 1-8 same on both ends

**Crossover (T568A to T568B):**
- Use: PC to PC, Switch to Switch, Router to Router
- Transmit/Receive pairs swapped

**T568A Pinout:**
1. Green/White (TX+)
2. Green (TX-)
3. Orange/White (RX+)
4. Blue
5. Blue/White
6. Orange (RX-)
7. Brown/White
8. Brown

### 3. Apply OSI Model

**Seven Layers (Top to Bottom):**

| Layer | Name | Function | Protocols/Devices |
|-------|------|----------|-------------------|
| 7 | Application | User interface | HTTP, FTP, SMTP |
| 6 | Presentation | Data formatting | SSL, JPEG, ASCII |
| 5 | Session | Connection management | NetBIOS, RPC |
| 4 | Transport | End-to-end delivery | TCP, UDP |
| 3 | Network | Routing and addressing | IP, ICMP, Routers |
| 2 | Data Link | Frame transmission | Ethernet, Switches |
| 1 | Physical | Bit transmission | Cables, Hubs |

**Remember:** "All People Seem To Need Data Processing"

### 4. Configure TCP/IP Addressing

**IP Address Classes:**

| Class | Range | Default Mask | Networks |
|-------|-------|--------------|----------|
| A | 1-126 | 255.0.0.0 | Large organizations |
| B | 128-191 | 255.255.0.0 | Medium organizations |
| C | 192-223 | 255.255.255.0 | Small organizations |

**Private IP Ranges:**
- Class A: 10.0.0.0 - 10.255.255.255
- Class B: 172.16.0.0 - 172.31.255.255
- Class C: 192.168.0.0 - 192.168.255.255

**Subnetting Calculation:**

```
Network: 192.168.1.0/26
Subnet Mask: 255.255.255.192

Subnets: 2^2 = 4 subnets
Hosts per subnet: 2^6 - 2 = 62 hosts

Subnet 1: 192.168.1.0 - 192.168.1.63
Subnet 2: 192.168.1.64 - 192.168.1.127
Subnet 3: 192.168.1.128 - 192.168.1.191
Subnet 4: 192.168.1.192 - 192.168.1.255
```

### 5. Configure Cisco Routers

**Basic Router Commands:**

```
! Enter privileged mode
Router> enable
Router#

! Enter configuration mode
Router# configure terminal
Router(config)#

! Set hostname
Router(config)# hostname R1

! Configure interface
Router(config)# interface FastEthernet 0/0
Router(config-if)# ip address 192.168.1.1 255.255.255.0
Router(config-if)# no shutdown

! Save configuration
Router# copy running-config startup-config

! Show commands
Router# show ip interface brief
Router# show running-config
Router# show ip route
```

**Configure Static Routing:**

```
Router(config)# ip route 10.0.0.0 255.0.0.0 192.168.1.2
Router(config)# ip route 0.0.0.0 0.0.0.0 192.168.1.1  ! Default route
```

**Configure RIP Routing:**

```
Router(config)# router rip
Router(config-router)# version 2
Router(config-router)# network 192.168.1.0
Router(config-router)# network 10.0.0.0
```

### 6. Configure Cisco Switches

**Basic Switch Commands:**

```
! Configure management VLAN
Switch(config)# interface vlan 1
Switch(config-if)# ip address 192.168.1.10 255.255.255.0
Switch(config-if)# no shutdown

! Configure port
Switch(config)# interface FastEthernet 0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
```

**VLAN Configuration:**

```
! Create VLAN
Switch(config)# vlan 10
Switch(config-vlan)# name SALES
Switch(config-vlan)# exit

! Assign port to VLAN
Switch(config)# interface range fa0/1-10
Switch(config-if-range)# switchport access vlan 10

! Configure trunk port
Switch(config)# interface GigabitEthernet 0/1
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk allowed vlan 10,20,30
```

**Inter-VLAN Routing (Router-on-a-Stick):**

```
Router(config)# interface FastEthernet 0/0.10
Router(config-subif)# encapsulation dot1Q 10
Router(config-subif)# ip address 192.168.10.1 255.255.255.0

Router(config)# interface FastEthernet 0/0.20
Router(config-subif)# encapsulation dot1Q 20
Router(config-subif)# ip address 192.168.20.1 255.255.255.0
```

### 7. Configure Access Lists

**Standard ACL (Filter by Source IP):**

```
! Deny specific host
Router(config)# access-list 10 deny host 192.168.1.100
Router(config)# access-list 10 permit any

! Apply to interface
Router(config)# interface FastEthernet 0/0
Router(config-if)# ip access-group 10 in
```

**Extended ACL (Filter by Source, Destination, Port):**

```
! Block Telnet from specific network
Router(config)# access-list 100 deny tcp 192.168.1.0 0.0.0.255 any eq 23
Router(config)# access-list 100 permit ip any any

! Apply to interface
Router(config-if)# ip access-group 100 in
```

### 8. Configure NAT

**Static NAT:**

```
Router(config)# ip nat inside source static 192.168.1.10 203.0.113.10
Router(config)# interface FastEthernet 0/0
Router(config-if)# ip nat inside
Router(config)# interface Serial 0/0
Router(config-if)# ip nat outside
```

**Dynamic NAT with PAT:**

```
Router(config)# access-list 1 permit 192.168.1.0 0.0.0.255
Router(config)# ip nat pool MYPOOL 203.0.113.1 203.0.113.1 netmask 255.255.255.0
Router(config)# ip nat inside source list 1 pool MYPOOL overload
```

## Quick Reference

### Common Subnet Masks

| CIDR | Mask | Hosts |
|------|------|-------|
| /24 | 255.255.255.0 | 254 |
| /25 | 255.255.255.128 | 126 |
| /26 | 255.255.255.192 | 62 |
| /27 | 255.255.255.224 | 30 |
| /28 | 255.255.255.240 | 14 |
| /29 | 255.255.255.248 | 6 |
| /30 | 255.255.255.252 | 2 |

### Essential Show Commands

```
show ip interface brief
show running-config
show ip route
show vlan brief
show interfaces trunk
show access-lists
show ip nat translations
```

## Constraints

- VLAN hopping attacks possible without proper trunk security
- Weak ACLs can be bypassed
- NAT can complicate penetration testing
- Routing protocols can be exploited if not secured
- Switch CAM tables can be flooded

## Examples

### Example 1: Basic Network Scan Understanding

```bash
# Scan reveals network structure
nmap -sn 192.168.1.0/24

# Identify VLANs through ARP
arp-scan -l

# Discover routing
traceroute 10.0.0.1
```

### Example 2: VLAN Enumeration

```bash
# Check for VLAN hopping vulnerability
yersinia -G

# DTP attack (if trunk misconfigured)
yersinia dtp -attack 1
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No connectivity | Verify cable type (straight vs crossover) |
| Cannot reach gateway | Check IP configuration and subnet mask |
| VLAN isolation | Verify trunk configuration and allowed VLANs |
| Routing not working | Check ip routing enabled and routes configured |
| ACL blocking traffic | Review access-list and interface application |
| NAT not translating | Verify inside/outside interface designation |
