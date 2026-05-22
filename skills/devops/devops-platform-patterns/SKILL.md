---
name: devops-platform-patterns
description: Platform-specific IaC checklists for DigitalOcean, Hetzner, AWS, and Cloudflare.
allowed-tools: []
---

# DevOps Platform Patterns

Platform-specific verification checklists for infrastructure code.

## DigitalOcean

| Check | Pass | Fail |
|-------|------|------|
| VPC used for private networking | Private network configured | Public networking only |
| Reserved IPs for production | Static IPs assigned | Ephemeral IPs for critical services |
| Managed database in same region | Co-located DB | Cross-region latency |
| Spaces for state backend | Remote state in Spaces | Local state only |
| Firewall attached to all droplets | Firewall rules applied | No firewall |

**Best Practices:**
- Use `digitalocean_vpc` for internal communication
- Attach firewalls via `digitalocean_firewall` with inbound rules
- Store Terraform state in DigitalOcean Spaces with versioning

## Hetzner

| Check | Pass | Fail |
|-------|------|------|
| Private network configured | Network created | No private networking |
| Firewall rules defined | Rules restrict access | Open to internet |
| SSH keys managed via resource | `hcloud_ssh_key` used | Keys in user_data only |
| Placement groups for HA | Servers distributed | Single point of failure |

**Best Practices:**
- Use `hcloud_network` + `hcloud_network_subnet` for internal traffic
- Apply `hcloud_firewall` to all servers
- Use placement groups with `spread` type for critical workloads

## AWS

| Check | Pass | Fail |
|-------|------|------|
| VPC with private subnets | Multi-AZ VPC | Default VPC usage |
| Security groups least-privilege | Specific ports/IPs | 0.0.0.0/0 ingress |
| IAM roles over access keys | Instance profiles | Hardcoded credentials |
| KMS encryption for data | Customer-managed keys | No encryption |
| CloudTrail enabled | Audit logging on | No audit trail |

**Best Practices:**
- Never use default VPC for production
- Prefer `aws_iam_role` with instance profiles over access keys
- Enable S3 bucket versioning and encryption by default
- Use `aws_kms_key` for sensitive data encryption

## Cloudflare

| Check | Pass | Fail |
|-------|------|------|
| API tokens over global key | Scoped tokens | Global API key |
| WAF rules configured | Protection enabled | No WAF |
| SSL mode is strict | Full (strict) mode | Flexible SSL |
| Rate limiting on endpoints | Rules applied | No rate limiting |

**Best Practices:**
- Create scoped API tokens per environment/purpose
- Set SSL mode to `strict` for origin protection
- Apply rate limiting to authentication endpoints
- Enable Bot Management if available

## Cross-Platform Checks

| Check | Applies To | Verification |
|-------|------------|--------------|
| Private networking | All | Internal services not exposed |
| Firewall/security groups | All | Explicit allow rules only |
| State backend remote | All | Not in local tfstate |
| Encryption at rest | All | Data encrypted |
| Audit logging | AWS, Cloudflare | Activity tracked |
