---
name: digitalocean-networking
description: DigitalOcean networking services including VPC, firewalls, load balancers, reserved IPs, DNS, IPv6, and NAT gateway. Use when designing or securing network connectivity for DigitalOcean workloads.
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean networking services including VPC, firewalls, load balancers, reserved IPs, DNS, IPv6, and NAT gateway. Use when designing or securing network connectivity for DigitalOcean workloads."
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# DigitalOcean Networking Skill

---
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean networking: VPC, firewalls, load balancers, reserved IPs, DNS, IPv6, NAT gateway."
    when_to_use:
      - "When designing private networks or segmentation"
      - "When securing inbound and outbound traffic"
      - "When configuring load balancing and DNS"
    quick_start:
      - "Create a VPC for private traffic"
      - "Apply firewalls to compute"
      - "Attach load balancers and reserved IPs"
      - "Configure DNS records"
  token_estimate:
    entry: 90-110
    full: 3800-5000
---

## Overview

DigitalOcean networking services secure and control traffic with VPC networking, firewalls, load balancing, DNS, IPv6, and reserved IPs.

## VPC

Use VPC to create private network segments for Droplets, Kubernetes, and managed databases.

- Create a VPC in the same region as compute resources.
- Attach resources that need private communication.

## Firewalls

Use stateful firewalls to restrict inbound and outbound traffic.

- Define inbound and outbound rules by protocol and port.
- Apply rules to Droplets and other resources.

## Load Balancers

Use load balancers to distribute traffic across backend resources.

- Configure health checks and target pools.
- Terminate TLS and forward to backend services.

## Reserved IPs

Use reserved IPs to keep stable public endpoints.

- Assign reserved IPs to Droplets.
- Remap IPs during failover or migration.

## DNS and IPv6

- Manage DNS records for DigitalOcean and external resources.
- Enable IPv6 for dual-stack support.

## NAT Gateway

Use NAT Gateway for outbound connectivity from private subnets.

## Networking Workflow

- Create a VPC per environment.
- Attach compute and databases to the VPC.
- Apply firewalls to limit inbound access.
- Add load balancers for public entry points.
- Configure DNS and reserved IPs for stable routing.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **digitalocean-compute**: Droplets, App Platform, and Kubernetes placement.
- **digitalocean-managed-databases**: Private database connectivity.
- **digitalocean-management**: Monitoring and uptime checks.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**DigitalOcean Docs**:
- Networking: https://docs.digitalocean.com/products/networking/
- VPC: https://docs.digitalocean.com/products/networking/vpc/
- Firewalls: https://docs.digitalocean.com/products/networking/firewalls/
- Load Balancers: https://docs.digitalocean.com/products/networking/load-balancers/
- Reserved IPs: https://docs.digitalocean.com/products/networking/reserved-ips/
- DNS: https://docs.digitalocean.com/products/networking/dns/
- IPv6: https://docs.digitalocean.com/products/networking/ipv6/
- NAT Gateway: https://docs.digitalocean.com/products/networking/vpc/how-to/create-nat-gateway/
