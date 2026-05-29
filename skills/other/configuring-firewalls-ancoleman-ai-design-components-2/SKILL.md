---
name: configuring-firewalls
description: Configure host-based firewalls (iptables, nftables, UFW) and cloud security groups (AWS, GCP, Azure) with practical rules for common scenarios like web servers, databases, and bastion hosts. Use when exposing services, hardening servers, or implementing network segmentation with defense-in-depth strategies.
---

# Configuring Firewalls

## Purpose

Guide engineers through configuring firewalls across host-based (iptables, nftables, UFW), cloud-based (AWS Security Groups, NACLs), and container-based (Kubernetes NetworkPolicies) environments with practical rule examples and safety patterns to prevent lockouts and security misconfigurations.

## When to Use This Skill

**Trigger Phrases:**
- "Configure firewall for [server/service]"
- "Set up security groups for [AWS resource]"
- "Allow port [X] through firewall"
- "Block IP address [X.X.X.X]"
- "Set up UFW on Ubuntu server"
- "Create iptables/nftables rules"
- "Configure bastion host firewall"
- "Implement egress filtering"

**Common Scenarios:**
- Initial server setup and hardening
- Exposing a new service (web server, API, database)
- Implementing network segmentation
- Creating bastion host or jump box
- Migrating from iptables to nftables
- Configuring cloud security groups
- Troubleshooting connectivity issues

## Decision Framework: Which Firewall Tool?

### Cloud Environments

**AWS:**
- Instance-level control → **Security Groups** (stateful, allow-only rules)
- Subnet-level enforcement → **Network ACLs** (stateless, allow + deny rules)
- Use both for defense-in-depth

**GCP:**
- Use **VPC Firewall Rules** (stateful, priority-based)

**Azure:**
- Use **Network Security Groups** (NSGs) (stateful, priority-based)

### Host-Based Linux Firewalls

**Ubuntu/Debian + Simplicity:**
- Use **UFW** (Uncomplicated Firewall) - recommended for most users
- Front-end for iptables/nftables with simplified syntax

**RHEL/CentOS/Fedora:**
- Use **firewalld** (default on Red Hat ecosystem)
- Zone-based configuration with dynamic updates

**Modern Distro + Advanced Control:**
- Use **nftables** (best performance, modern standard)
- O(log n) performance vs iptables O(n)
- Unified IPv4/IPv6/NAT syntax

**Legacy Systems:**
- Use **iptables** (migrate to nftables when feasible)
- Required for older kernels (< 4.14)

### Kubernetes/Containers

- Use **NetworkPolicies** (requires CNI plugin: Calico, Cilium, Weave)
- See references/k8s-networkpolicies.md

### Stateful vs Stateless

**Stateful (recommended for most cases):**
- Automatically allows return traffic
- Simpler configuration
- Examples: Security Groups, UFW, nftables default

**Stateless (specialized use):**
- Must explicitly allow both directions
- Fine-grained control, less state tracking
- Examples: Network ACLs, custom nftables rules

## Quick Start Examples

### UFW (Ubuntu/Debian)

```bash
# 1. Set defaults
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. CRITICAL: Allow SSH before enabling (prevent lockout)
sudo ufw allow ssh
sudo ufw limit ssh  # Rate-limit to prevent brute force

# 3. Allow web traffic
sudo ufw allow http    # Port 80
sudo ufw allow https   # Port 443

# 4. Allow from specific IP (e.g., database access)
sudo ufw allow from 192.168.1.100 to any port 5432

# 5. Enable firewall
sudo ufw enable

# 6. Verify rules
sudo ufw status verbose
```

For complete UFW patterns, see references/ufw-patterns.md

### nftables (Modern Linux)

```nftables
#!/usr/sbin/nft -f
# /etc/nftables.conf

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # Accept loopback
        iif "lo" accept

        # Accept established connections (stateful)
        ct state established,related accept

        # Drop invalid packets
        ct state invalid drop

        # Allow SSH
        tcp dport 22 accept

        # Allow HTTP/HTTPS
        tcp dport { 80, 443 } accept

        # Log dropped packets
        log prefix "nftables-drop: " drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

Apply: `sudo nft -f /etc/nftables.conf`
Enable on boot: `sudo systemctl enable nftables`

For advanced patterns (sets, maps), see references/nftables-patterns.md

### AWS Security Groups (Terraform)

```hcl
# Web server security group
resource "aws_security_group" "web" {
  name        = "web-server-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  # Allow HTTP/HTTPS from anywhere
  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow SSH from bastion only
  ingress {
    description     = "SSH from bastion"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  # Allow all outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-server-sg"
  }
}
```

For Security Groups vs NACLs guide, see references/aws-security-groups.md

## Safety Checklist

Before enabling any firewall:

- [ ] **Always allow SSH before enabling** (prevent lockout)
- [ ] Test rules before enabling (dry-run when possible)
- [ ] Enable logging for debugging
- [ ] Document rules in version control (Git)
- [ ] Verify externally with nmap: `nmap -Pn <server-ip>`
- [ ] Have console access (cloud) or physical access (on-prem)
- [ ] Start with default deny, explicitly allow required traffic
- [ ] Use rate limiting for SSH (`ufw limit ssh`)

## Common Patterns

### Pattern 1: Basic Web Server

**Requirements:**
- Allow HTTP (80) and HTTPS (443) from anywhere
- Allow SSH from specific IP or bastion only
- Default deny all other inbound traffic

**UFW:**
```bash
sudo ufw default deny incoming
sudo ufw allow from 203.0.113.0/24 to any port 22  # Office IP
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

**nftables:**
See references/nftables-patterns.md for complete example

**AWS Security Group:**
See references/aws-security-groups.md for Terraform module

### Pattern 2: Database Server (Private)

**Requirements:**
- Allow database port (5432, 3306, etc.) from app tier only
- No public internet access
- SSH from bastion only

See references/database-patterns.md for implementation

### Pattern 3: Bastion Host (Jump Box)

**Purpose:** Single hardened entry point for SSH access

See references/bastion-pattern.md for complete implementation

### Pattern 4: Egress Filtering

**Purpose:** Control outbound traffic to prevent data exfiltration

See references/egress-filtering.md for implementation

## Key Concepts

### Stateful Firewalls

Track connection state (established, related, new):
- Automatically allow return traffic
- Simpler rule configuration
- Used by: Security Groups, UFW, nftables (default)

### Stateless Firewalls

No connection tracking:
- Must explicitly allow both directions
- Must allow ephemeral ports (1024-65535) for return traffic
- Used by: Network ACLs

### Defense-in-Depth

Layer multiple firewall controls:
- **Cloud:** Security Groups + NACLs
- **Host:** UFW/nftables + fail2ban
- **Container:** NetworkPolicies

### Rule Evaluation

**Security Groups (AWS):** All rules evaluated, most permissive wins
**Network ACLs (AWS):** Sequential evaluation, first match wins
**nftables/iptables:** Sequential, first match wins
**UFW:** Sequential by rule number

## Universal Best Practices

1. **Default Deny:** Start with deny-all, explicitly allow required traffic
2. **Principle of Least Privilege:** Only open necessary ports/IPs
3. **No 0.0.0.0/0 on Sensitive Ports:** Never allow SSH/RDP/database from anywhere
4. **Version Control:** Store firewall rules in Git
5. **Logging:** Enable and monitor firewall logs
6. **Regular Audits:** Review rules quarterly, remove unused
7. **Don't Mix Tools:** Avoid running iptables and nftables simultaneously
8. **Test Before Production:** Use staging environment first

## Advanced Topics

**Bastion Host Architecture:**
See references/bastion-pattern.md for single entry point patterns

**DMZ (Demilitarized Zone):**
See references/dmz-pattern.md for network segmentation

**Egress Filtering:**
See references/egress-filtering.md for outbound traffic control

**Kubernetes NetworkPolicies:**
See references/k8s-networkpolicies.md for pod-to-pod isolation

**Migrating iptables to nftables:**
See references/migration-guide.md for conversion process

**Cloud Firewall Comparisons:**
- AWS: references/aws-security-groups.md
- GCP: references/gcp-firewall.md
- Azure: references/azure-nsg.md

## Troubleshooting

**"I locked myself out via SSH":**
- Cloud: Use console/session manager to access
- On-prem: Physical console access or IPMI/iLO
- Prevention: Always allow SSH before enabling firewall

**Connection timeouts:**
- Check if firewall is blocking traffic: `sudo ufw status` or `sudo nft list ruleset`
- Verify service is listening: `ss -tuln | grep <port>`
- Test externally: `nmap -Pn <ip> -p <port>`
- Check logs: `/var/log/ufw.log` or `journalctl -u nftables`

**AWS: Ephemeral port issues:**
- NACLs need return traffic: Allow 1024-65535 inbound
- Security Groups are stateful (no ephemeral config needed)

**Kubernetes pods can't communicate:**
- Check NetworkPolicies: `kubectl get networkpolicies -n <namespace>`
- Verify CNI plugin supports NetworkPolicies (Calico, Cilium)
- Test without policies first

For complete troubleshooting guide, see references/troubleshooting.md

## Common Mistakes to Avoid

❌ **Allowing 0.0.0.0/0 on SSH/RDP** → Use bastion or VPN
❌ **Forgetting to enable firewall** → Rules configured but not active
❌ **Not testing before enabling** → Risk of lockout
❌ **Missing ephemeral ports in NACLs** → Return traffic blocked
❌ **Running iptables + nftables** → Conflicts and unpredictable behavior
❌ **No logging** → Can't debug or audit
❌ **Large port ranges** → Unnecessary attack surface
❌ **Not documenting rules** → Future confusion

## Tool-Specific Commands

### UFW

```bash
# Status
sudo ufw status verbose
sudo ufw status numbered

# Add rules
sudo ufw allow <port>/<protocol>
sudo ufw allow from <ip> to any port <port>
sudo ufw limit ssh  # Rate limiting

# Delete rules
sudo ufw delete <rule-number>
sudo ufw delete allow 80/tcp

# Logging
sudo ufw logging on
tail -f /var/log/ufw.log

# Reset (disable and remove all rules)
sudo ufw reset
```

### nftables

```bash
# List ruleset
sudo nft list ruleset

# Load config
sudo nft -f /etc/nftables.conf

# Flush all rules
sudo nft flush ruleset

# Add rule dynamically
sudo nft add rule inet filter input tcp dport 8080 accept

# Enable on boot
sudo systemctl enable nftables
```

### iptables

```bash
# List rules
sudo iptables -L -v -n
sudo iptables -L INPUT --line-numbers

# Add rule
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Delete rule
sudo iptables -D INPUT <rule-number>

# Save rules
sudo netfilter-persistent save  # Debian/Ubuntu
sudo service iptables save      # RHEL/CentOS
```

### AWS CLI

```bash
# List security groups
aws ec2 describe-security-groups --group-ids sg-xxxxx

# List NACLs
aws ec2 describe-network-acls --network-acl-ids acl-xxxxx

# Add rule to security group
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

For infrastructure as code approach, use Terraform (see references/aws-security-groups.md)

## Examples Directory

Complete working examples available in:

- `examples/ufw/` - UFW configuration scripts
- `examples/nftables/` - nftables rulesets
- `examples/iptables/` - iptables rule scripts
- `examples/terraform-aws/` - AWS Security Groups and NACLs
- `examples/terraform-gcp/` - GCP firewall rules
- `examples/terraform-azure/` - Azure NSGs
- `examples/kubernetes/` - NetworkPolicy manifests

## Integration Points

**Related Skills:**

- **security-hardening** - Firewalls are one component of server hardening. See security-hardening skill for SSH hardening, fail2ban, auditd, and SELinux.

- **building-ci-pipelines** - CI runners need network access to repos and artifact stores. Configure firewall rules for self-hosted runners.

- **deploying-applications** - Applications need firewall rules for service exposure. See deploying-applications for integration.

- **infrastructure-as-code** - Manage firewalls as code with Terraform/CloudFormation. See infrastructure-as-code for IaC best practices.

- **kubernetes-operations** - Advanced K8s networking beyond basic NetworkPolicies. See kubernetes-operations for Services, Ingress, and CNI configuration.

- **network-architecture** - Broader network design patterns. See network-architecture for VPC design, subnets, and routing.

## Reference Files

**Tool-Specific Guides:**
- references/ufw-patterns.md - Complete UFW guide with examples
- references/nftables-patterns.md - nftables syntax, sets, maps, logging
- references/iptables-patterns.md - iptables basics and migration path
- references/migration-guide.md - Convert iptables to nftables

**Cloud Provider Guides:**
- references/aws-security-groups.md - Security Groups vs NACLs with Terraform
- references/gcp-firewall.md - GCP VPC firewall rules
- references/azure-nsg.md - Azure Network Security Groups

**Advanced Patterns:**
- references/bastion-pattern.md - Jump box architecture
- references/dmz-pattern.md - Network segmentation with DMZ
- references/egress-filtering.md - Outbound traffic control
- references/k8s-networkpolicies.md - Kubernetes pod isolation

**Support:**
- references/troubleshooting.md - Common issues and solutions
- references/decision-tree.md - Visual guide for tool selection
