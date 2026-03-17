# Network Security Setup SOP

```yaml
metadata:
  skill_name: when-setting-network-security-use-network-security-setup
  version: 1.0.0
  category: specialized-tools
  difficulty: intermediate
  estimated_duration: 25-45 minutes
  trigger_patterns:
    - "network security"
    - "configure network isolation"
    - "trusted domains"
    - "firewall rules"
    - "network access control"
  dependencies:
    - Claude Code sandbox
    - Network configuration access
  agents:
    - security-manager
    - cicd-engineer
  success_criteria:
    - Trusted domains configured
    - Access policies implemented
    - Environment variables set
    - Network tests passing
    - Documentation complete
```

## Overview

Configure Claude Code sandbox network isolation with trusted domains, custom access policies, and environment variables for secure network communication.

## Agent Responsibilities

### security-manager
- Design network security architecture
- Define trusted domains and policies
- Validate security configurations
- Create security documentation

### cicd-engineer
- Implement network configurations
- Deploy firewall rules
- Setup environment variables
- Create monitoring tools

## Phase 1: Audit Network Requirements

Identify required network access, external dependencies, and security constraints.

```bash
mkdir -p network-security/{policies,config,tests,docs}

# Document network requirements
cat > network-security/docs/NETWORK-REQUIREMENTS.md << 'EOF'
# Network Access Requirements

## External Dependencies
- Anthropic API (api.anthropic.com)
- GitHub (github.com, *.github.com)
- NPM Registry (npmjs.org)
- PyPI (pypi.org)
- Docker Hub (docker.io)

## Required Ports
- Outbound: 80 (HTTP), 443 (HTTPS), 22 (SSH)
- Inbound: 3000, 5000, 8000, 8080 (Application)

## Protocols
- Allowed: HTTP/HTTPS, SSH, Git
- Blocked: FTP, Telnet, SMTP

## Rate Limits
- 100 requests/minute
- Burst: 150 requests
EOF
```

## Phase 2: Design Security Policies

Create comprehensive network security policies with allow/deny rules.

```bash
cat > network-security/policies/network-policy.json << 'EOF'
{
  "network_security": {
    "mode": "whitelist",
    "trusted_domains": [
      "*.anthropic.com",
      "api.openai.com", 
      "github.com",
      "*.github.com",
      "raw.githubusercontent.com",
      "npmjs.org",
      "registry.npmjs.org",
      "pypi.org",
      "files.pythonhosted.org",
      "docker.io",
      "registry-1.docker.io"
    ],
    "blocked_domains": [
      "*.malicious.com",
      "suspicious.net"
    ],
    "allowed_ports": {
      "outbound": [80, 443, 22],
      "inbound": [3000, 5000, 8000, 8080]
    },
    "rate_limiting": {
      "enabled": true,
      "requests_per_minute": 100,
      "burst": 150
    },
    "dns_filtering": {
      "enabled": true,
      "block_private_ips": true,
      "block_localhost_bypass": true
    }
  }
}
EOF
```

## Phase 3: Implement Network Isolation

Deploy firewall rules, DNS filtering, and access controls.

```bash
cat > network-security/config/configure-network.sh << 'EOF'
#!/bin/bash
set -e

echo "Configuring network security..."

# Configure firewall (iptables)
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 3000 -j ACCEPT
iptables -A INPUT -p tcp --dport 8000 -j ACCEPT

# DNS filtering
cat >> /etc/hosts << 'HOSTS'
127.0.0.1 malicious.com
127.0.0.1 suspicious.net
HOSTS

# Environment variables
cat > /etc/environment.d/network-security.conf << 'ENV'
HTTPS_PROXY=""
NO_PROXY="localhost,127.0.0.1"
TRUSTED_DOMAINS="anthropic.com,github.com,npmjs.org,pypi.org,docker.io"
ENV

echo "Network security configured"
EOF

chmod +x network-security/config/configure-network.sh
```

## Phase 4: Test Access Controls

Validate network policies through comprehensive testing.

```bash
cat > network-security/tests/network-tests.sh << 'EOF'
#!/bin/bash

echo "Testing Network Security..."

# Test trusted domain access
curl -s --max-time 5 https://api.anthropic.com && echo "✓ Trusted domain accessible"

# Test blocked domain
! curl -s --max-time 5 https://malicious.com && echo "✓ Blocked domain inaccessible"

# Test allowed ports
nc -zv localhost 3000 && echo "✓ Port 3000 accessible"

echo "Network tests complete"
EOF

chmod +x network-security/tests/network-tests.sh
```

## Phase 5: Document Configuration

Create comprehensive documentation for network security setup.

```bash
cat > network-security/docs/DEPLOYMENT.md << 'EOF'
# Network Security Deployment

## Quick Start
1. Review requirements
2. Deploy configuration: `./network-security/config/configure-network.sh`
3. Test policies: `./network-security/tests/network-tests.sh`
4. Monitor: Check logs for violations

## Trusted Domains
- Anthropic API
- GitHub
- NPM/PyPI
- Docker Hub

## Monitoring
- Connection logs: `/var/log/connections.log`
- Firewall logs: `/var/log/firewall.log`
- DNS queries: `/var/log/dns.log`

## Maintenance
- Review monthly
- Update trusted domains as needed
- Audit logs weekly
EOF
```

## Workflow Summary

**Duration:** 25-45 minutes

**Deliverables:**
- Network security policies
- Firewall configuration
- DNS filtering
- Test suite
- Documentation

## Best Practices

1. **Whitelist Approach**: Deny by default
2. **Least Privilege**: Minimal access
3. **Regular Testing**: Weekly validation
4. **Continuous Monitoring**: Real-time logs
5. **Documentation**: Keep updated

