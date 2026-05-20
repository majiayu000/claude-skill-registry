---
name: codex-security-specialist
description: Apply layered security routing for network, infrastructure, application security, compliance, and DevSecOps concerns. Use to select focused security reference files with strict context boundaries before implementation, audit, or review.
load_priority: on-demand
---

## TL;DR
Detect security domain from task signals -> load matching references from routing table -> enforce max 4 references first pass. Never bulk-load all references. Security tasks require extra care — always prefer defense-in-depth.

# Security Specialist

## Activation

1. Activate when the task involves security configuration, hardening, network setup, compliance, or vulnerability assessment.
2. Activate on explicit `$codex-security-specialist`.
3. Activate when `codex-domain-specialist` detects security-heavy tasks beyond application security scope.

## Core Security Principles

Before any implementation, apply these principles:

1. **Defense in depth** — never rely on a single security layer.
2. **Least privilege** — grant minimum access required for the task.
3. **Fail secure** — when a security mechanism fails, deny access by default.
4. **Zero trust** — verify explicitly, never trust implicitly, even inside the network.
5. **Separation of duties** — no single person/process should control all security aspects.
6. **Audit everything** — log all security-relevant events with tamper-proof storage.

## Primary Domain Detection

| Signal | Primary Domain |
| --- | --- |
| TCP/IP, port, protocol, packet, routing, subnet, CIDR, OSI | Network Fundamentals |
| firewall, iptables, UFW, Security Group, ACL, ingress, egress | Firewall & Access Control |
| VPN, WireGuard, OpenVPN, tunnel, IPsec, remote access | VPN & Tunneling |
| DNS, DNSSEC, DoH, DoT, zone, record, nameserver, domain | DNS Security |
| SSL, TLS, certificate, HTTPS, Let's Encrypt, CA, chain, OCSP | SSL/TLS & Certificates |
| SSH, Linux hardening, permissions, users, PAM, sudo, audit | Infrastructure Hardening |
| Vault, KMS, secret, key rotation, credential, token | Secret Management |
| Docker security, container scan, K8s RBAC, Pod Security | Container Security |
| AWS IAM, Security Group, VPC, Azure AD, GCP IAM, cloud | Cloud Security |
| OWASP, CVE, vulnerability, exploit, injection, XSS deep | OWASP & Vulnerabilities |
| pentest, penetration testing, recon, enumeration, exploit | Penetration Testing |
| Nmap, Nessus, ZAP, Burp Suite, scanning, vulnerability scan | Vulnerability Scanning |
| incident, breach, forensics, response, containment, recovery | Incident Response |
| SIEM, ELK, Splunk, log analysis, correlation, alert | SIEM & Log Analysis |
| STRIDE, DREAD, threat model, attack tree, risk assessment | Threat Modeling |
| encryption, AES, RSA, hashing, bcrypt, argon2, SHA | Cryptography |
| PKI, X.509, digital signature, key pair, certificate authority | PKI & Certificates |
| SAST, DAST, SCA, dependency scan, code scan, security CI | DevSecOps |
| ISO 27001, SOC 2, GDPR, PCI-DSS, compliance, audit | Compliance |
| zero trust, microsegmentation, identity-aware proxy | Zero Trust |
| DDoS, rate limiting, WAF, CDN protection, traffic scrubbing | DDoS Mitigation |
| IDS, IPS, Snort, Suricata, intrusion detection | IDS/IPS |
| supply chain, dependency, SBom, package integrity | Supply Chain Security |

## Routing Decision Table

| Primary Domain | Always Load | Load On Signal | Never Load |
| --- | --- | --- | --- |
| Network Fundamentals | `network-fundamentals.md` | `firewall-rules.md`, `network-segmentation.md` | `compliance/`, `devsecops/` |
| Firewall & Access Control | `firewall-rules.md` | `network-fundamentals.md`, `network-segmentation.md` | `cryptography/`, `compliance/` |
| VPN & Tunneling | `vpn-tunneling.md` | `network-fundamentals.md`, `ssl-tls-certificates.md` | `compliance/`, `container-security.md` |
| DNS Security | `dns-security.md` | `network-fundamentals.md`, `ssl-tls-certificates.md` | `container-security.md`, `pentest/` |
| SSL/TLS & Certificates | `ssl-tls-certificates.md` | `network-fundamentals.md`, `dns-security.md` | `pentest/`, `siem/` |
| Infrastructure Hardening | `linux-hardening.md` | `firewall-rules.md`, `secret-management.md` | `cloud-security.md` |
| Secret Management | `secret-management.md` | `linux-hardening.md`, `container-security.md` | `dns-security.md` |
| Container Security | `container-security.md` | `linux-hardening.md`, `devsecops-pipeline.md` | `vpn-tunneling.md` |
| Cloud Security | `cloud-security-aws.md` | `network-segmentation.md`, `secret-management.md` | `linux-hardening.md` (direct) |
| OWASP & Vulnerabilities | `owasp-top10-deep.md` | `vulnerability-scanning.md`, `devsecops-pipeline.md` | `vpn-tunneling.md` |
| Penetration Testing | `pentest-methodology.md` | `vulnerability-scanning.md`, `owasp-top10-deep.md` | `compliance/` |
| Incident Response | `incident-response.md` | `siem-log-analysis.md`, `threat-modeling.md` | `vpn-tunneling.md` |
| Cryptography | `cryptography-guide.md` | `ssl-tls-certificates.md`, `pki-certificates.md` | `firewall-rules.md` |
| DevSecOps | `devsecops-pipeline.md` | `sast-dast-sca.md`, `supply-chain-security.md` | `vpn-tunneling.md` |
| Compliance | `iso27001-checklist.md` | relevant domain checklist | `pentest/`, `cryptography/` (details) |
| Zero Trust | `zero-trust-architecture.md` | `network-segmentation.md`, `secret-management.md` | `dns-security.md` |
| Vulnerability Scanning | `vulnerability-scanning.md` | `owasp-top10-deep.md`, `devsecops-pipeline.md` | `vpn-tunneling.md`, `compliance/` |
| SIEM & Log Analysis | `siem-log-analysis.md` | `incident-response.md`, `ids-ips-patterns.md` | `vpn-tunneling.md`, `cryptography/` |
| Threat Modeling | `threat-modeling.md` | `owasp-top10-deep.md`, `incident-response.md` | `firewall-rules.md`, `dns-security.md` |
| PKI & Certificates | `pki-certificates.md` | `ssl-tls-certificates.md`, `cryptography-guide.md` | `firewall-rules.md`, `pentest/` |
| DDoS Mitigation | `ddos-mitigation.md` | `firewall-rules.md`, `network-fundamentals.md` | `compliance/`, `cryptography/` |
| IDS/IPS | `ids-ips-patterns.md` | `siem-log-analysis.md`, `network-fundamentals.md` | `compliance/`, `dns-security.md` |
| Supply Chain Security | `supply-chain-security.md` | `devsecops-pipeline.md`, `sast-dast-sca.md` | `vpn-tunneling.md`, `firewall-rules.md` |
| API Security | `api-security-advanced.md` | `owasp-top10-deep.md`, `zero-trust-architecture.md` | `dns-security.md`, `vpn-tunneling.md` |

## Context Boundary Enforcement

1. Max context load: 4 references first pass.
2. Security isolation:
   - Network tasks: do not load application security or compliance details.
   - Compliance tasks: do not load offensive security (pentest, exploit).
   - DevSecOps tasks: do not load network infrastructure details.
3. Cross-domain trigger:
   - Vulnerability found: load `incident-response.md` as supplemental.
   - Secret exposure: load `secret-management.md` regardless of primary domain.
   - Production deployment: load `ssl-tls-certificates.md` + relevant hardening.
4. Always declare loaded and skipped references.

## Starter Templates

| Template | Use When |
| --- | --- |
| `iptables-rules.sh` | Configuring Linux firewall rules |
| `nginx-ssl-hardened.conf` | Setting up production-grade HTTPS with hardened TLS |
| `ssh-hardening.sh` | Hardening SSH server configuration |
| `docker-security-scan.yml` | Adding container security scanning to CI |
| `vault-setup.hcl` | Setting up HashiCorp Vault for secrets |
| `security-headers.js` | Configuring comprehensive security headers (Express) |
| `rate-limiter-advanced.js` | Advanced rate limiting with Redis backend |
| `csp-policy.js` | Content Security Policy builder |
| `security-ci-pipeline.yml` | Security-focused CI/CD pipeline (SAST/DAST/SCA) |
| `pentest-checklist.md` | Pre-deployment penetration testing checklist |

## Operating Rules

1. Never bulk-load all references.
2. Security advice must be accurate — when uncertain, flag with `⚠️ VERIFY:` and explain what to verify.
3. Always provide both the "what" (config/code) and the "why" (threat it mitigates).
4. Default to the most secure option; relax only when user explicitly requests.
5. Never log or output secrets, keys, or credentials in examples — use placeholders.
6. When providing attack/exploit knowledge, always include the defensive countermeasure.

## Reference Files

- `references/linux-hardening.md`: OS hardening, user management, kernel security, and audit logging.
- `references/secret-management.md`: secret lifecycle, Vault/AWS SM/Docker secrets, rotation procedures.
- `references/container-security.md`: Dockerfile hardening, image scanning, runtime security, K8s pod security.
- `references/cloud-security-aws.md`: IAM, VPC, S3 security, encryption, monitoring and compliance.
- `references/api-security-advanced.md`: multi-layer API protection, rate limiting tiers, output filtering.
- `references/zero-trust-architecture.md`: identity-centric security, risk scoring, microsegmentation, mTLS.
- `references/ddos-mitigation.md`: 4-layer defense architecture, CDN/WAF/Nginx/app rate limiting.
- `references/ids-ips-patterns.md`: detection patterns, host/network alerts, and Suricata-style rules.
- `references/security-audit-framework.md`: audit checklists, access review, and reporting framework.
- `references/network-fundamentals.md`: OSI model security, TCP/IP, common ports, CIDR subnetting, network security tools.
- `references/firewall-rules.md`: iptables, UFW, AWS Security Groups, Docker port binding security.
- `references/vpn-tunneling.md`: WireGuard configuration, SSH tunneling techniques, key rotation.
- `references/dns-security.md`: DNSSEC, DoH/DoT, SPF/DKIM/DMARC, DNS threats and defenses.
- `references/ssl-tls-certificates.md`: TLS configuration, Let's Encrypt, certificate chain, OCSP stapling.
- `references/network-segmentation.md`: zone architecture, AWS VPC, Docker networks, K8s NetworkPolicy.
- `references/owasp-top10-deep.md`: A01-A10 with vulnerable and fixed code examples.
- `references/pentest-methodology.md`: 6-phase methodology, recon tools, exploitation, reporting.
- `references/vulnerability-scanning.md`: scanner types, ZAP/Nmap commands, scanning schedule.
- `references/incident-response.md`: NIST IR phases, severity levels, containment, post-mortem.
- `references/siem-log-analysis.md`: ELK stack, security events, alert rules, retention policy.
- `references/threat-modeling.md`: STRIDE/DREAD frameworks, trust boundaries, threat model template.
- `references/devsecops-pipeline.md`: shift-left architecture, pre-commit hooks, CI/CD security stages.
- `references/sast-dast-sca.md`: Semgrep/SonarQube/CodeQL, ZAP DAST, Snyk SCA, custom rules.
- `references/iac-security.md`: tfsec/Checkov, common misconfigs, secure Terraform patterns.
- `references/supply-chain-security.md`: attack vectors, defense layers, SBOM, package provenance.
- `references/iso27001-checklist.md`: Annex A controls mapped to developer actions.
- `references/gdpr-compliance.md`: 7 principles, user rights code, consent management, breach notification.
- `references/soc2-checklist.md`: trust service criteria, control activities, evidence requirements.
- `references/cryptography-guide.md`: algorithm decision tables, AES-256-GCM, key management.
- `references/pki-certificates.md`: X.509 fields, cert types, mTLS setup, internal CA.
