---
name: defense-in-depth
description: Apply layered security architecture. Use when designing security controls, hardening systems, or reviewing security posture. Covers multiple security layers.
allowed-tools: Read, Glob, Grep
---

# Defense in Depth

## Security Layers

```
┌─────────────────────────────────┐
│         Perimeter Security       │  WAF, DDoS Protection
├─────────────────────────────────┤
│         Network Security         │  Firewalls, VPNs, Segmentation
├─────────────────────────────────┤
│         Host Security            │  OS Hardening, Patching
├─────────────────────────────────┤
│         Application Security     │  AuthN, AuthZ, Input Validation
├─────────────────────────────────┤
│         Data Security            │  Encryption, Access Control
└─────────────────────────────────┘
```

## Layer Controls

### 1. Perimeter
- Web Application Firewall (WAF)
- DDoS protection
- Rate limiting
- Bot detection

### 2. Network
- Network segmentation (VPCs, subnets)
- Security groups / firewalls
- VPN for internal access
- Zero-trust network access

### 3. Host
- OS hardening
- Patch management
- Endpoint protection
- File integrity monitoring

### 4. Application
- Authentication (OAuth2, OIDC)
- Authorization (RBAC, ABAC)
- Input validation
- Output encoding
- Session management
- Secure headers

### 5. Data
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Key management
- Data masking
- Access logging

## Security Checklist

- [ ] WAF configured with OWASP rules
- [ ] Network segmentation in place
- [ ] All traffic encrypted (TLS)
- [ ] Authentication on all endpoints
- [ ] Least privilege access controls
- [ ] Secrets managed securely
- [ ] Audit logging enabled
- [ ] Backups encrypted and tested

## Principle of Least Privilege

Grant only the minimum permissions needed:
- Use IAM roles, not long-lived credentials
- Scope permissions to specific resources
- Regular access reviews
- Just-in-time access for sensitive operations
