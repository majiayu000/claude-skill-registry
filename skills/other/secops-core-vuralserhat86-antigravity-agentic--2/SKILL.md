---
name: secops_core
router_kit: SecurityKit
description: Comprehensive SecOps skill for application security, vulnerability management, compliance, and secure development practices. Includes security scanning, vulnerability assessment, compliance checking, and security automation. Use when implementing security controls, conducting security audits, responding to vulnerabilities, or ensuring compliance requirements.
metadata:
  skillport:
    category: auto-healed
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, secops core, software engineering, standards, testing, utilities, version control, workflow]      - secops_core
---

# Senior Secops

Complete toolkit for senior secops with modern tools and best practices.

## Quick Start

### Main Capabilities

This skill provides three core capabilities through automated scripts:

```bash
# Script 1: Security Scanner
python scripts/security_scanner.py [options]

# Script 2: Vulnerability Assessor
python scripts/vulnerability_assessor.py [options]

# Script 3: Compliance Checker
python scripts/compliance_checker.py [options]
```

## Core Capabilities

### 1. Security Scanner

Automated tool for security scanner tasks.

**Features:**
- Automated scaffolding
- Best practices built-in
- Configurable templates
- Quality checks

**Usage:**
```bash
python scripts/security_scanner.py <project-path> [options]
```

### 2. Vulnerability Assessor

Comprehensive analysis and optimization tool.

**Features:**
- Deep analysis
- Performance metrics
- Recommendations
- Automated fixes

**Usage:**
```bash
python scripts/vulnerability_assessor.py <target-path> [--verbose]
```

### 3. Compliance Checker

Advanced tooling for specialized tasks.

**Features:**
- Expert-level automation
- Custom configurations
- Integration ready
- Production-grade output

**Usage:**
```bash
python scripts/compliance_checker.py [arguments] [options]
```

## Reference Documentation

### Security Standards

Comprehensive guide available in `references/security_standards.md`:

- Detailed patterns and practices
- Code examples
- Best practices
- Anti-patterns to avoid
- Real-world scenarios

### Vulnerability Management Guide

Complete workflow documentation in `references/vulnerability_management_guide.md`:

- Step-by-step processes
- Optimization strategies
- Tool integrations
- Performance tuning
- Troubleshooting guide

### Compliance Requirements

Technical reference guide in `references/compliance_requirements.md`:

- Technology stack details
- Configuration examples
- Integration patterns
- Security considerations
- Scalability guidelines

## Tech Stack

**Languages:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Database:** PostgreSQL, Prisma, NeonDB, Supabase
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions, CircleCI
**Cloud:** AWS, GCP, Azure

## Development Workflow

### 1. Setup and Configuration

```bash
# Install dependencies
npm install
# or
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### 2. Run Quality Checks

```bash
# Use the analyzer script
python scripts/vulnerability_assessor.py .

# Review recommendations
# Apply fixes
```

### 3. Implement Best Practices

Follow the patterns and practices documented in:
- `references/security_standards.md`
- `references/vulnerability_management_guide.md`
- `references/compliance_requirements.md`

## Best Practices Summary

### Code Quality
- Follow established patterns
- Write comprehensive tests
- Document decisions
- Review regularly

### Performance
- Measure before optimizing
- Use appropriate caching
- Optimize critical paths
- Monitor in production

### Security
- Validate all inputs
- Use parameterized queries
- Implement proper authentication
- Keep dependencies updated

### Maintainability
- Write clear code
- Use consistent naming
- Add helpful comments
- Keep it simple

## Common Commands

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python scripts/vulnerability_assessor.py .
python scripts/compliance_checker.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Common Issues

Check the comprehensive troubleshooting section in `references/compliance_requirements.md`.

### Getting Help

- Review reference documentation
- Check script output messages
- Consult tech stack documentation
- Review error logs

## Resources

- Pattern Reference: `references/security_standards.md`
- Workflow Guide: `references/vulnerability_management_guide.md`
- Technical Guide: `references/compliance_requirements.md`
- Tool Scripts: `scripts/` directory


# Merged Content from security-audit

---
name: secops_core
description: Güvenlik taraması, vulnerability detection, OWASP kontrolleri ve secure coding practices rehberi.
metadata:
  skillport:
    category: security
    tags:
      - security
      - vulnerability
      - owasp
      - audit
---

# 🔒 Security Audit

> Kapsamlı güvenlik taraması ve vulnerability detection rehberi.

---

## 📋 İçindekiler

1. [OWASP Top 10 Kontrolleri](#1-owasp-top-10-kontrolleri)
2. [Kod Güvenlik Analizi](#2-kod-güvenlik-analizi)
3. [Dependency Güvenliği](#3-dependency-güvenliği)
4. [Authentication & Authorization](#4-authentication--authorization)
5. [Data Protection](#5-data-protection)

---

## 1. OWASP Top 10 Kontrolleri

### A01: Broken Access Control
```checklist
- [ ] Role-based access control (RBAC) implementasyonu
- [ ] URL/API endpoint authorization
- [ ] Direct object reference koruması
- [ ] CORS policy kontrolü
```

### A02: Cryptographic Failures
```checklist
- [ ] Sensitive data şifreleme (at-rest, in-transit)
- [ ] TLS 1.2+ kullanımı
- [ ] Güçlü hashing algoritmaları (bcrypt, argon2)
- [ ] Secret management (env, vault)
```

### A03: Injection
```checklist
- [ ] SQL injection koruması (parametrized queries)
- [ ] XSS prevention (output encoding)
- [ ] Command injection kontrolü
- [ ] NoSQL injection koruması
```

### A07: Cross-Site Scripting (XSS)
```checklist
- [ ] Input validation
- [ ] Output encoding/escaping
- [ ] Content Security Policy (CSP)
- [ ] HTTPOnly cookies
```

---

## 2. Kod Güvenlik Analizi

### Statik Analiz Araçları
```bash
# JavaScript/TypeScript
npm audit
npx eslint --ext .js,.ts . --rule 'security/*'

# Python
pip-audit
bandit -r .

# Genel
semgrep --config=auto .
```

### Kontrol Listesi
| Kontrol | Açıklama | Öncelik |
|---------|----------|---------|
| Hardcoded secrets | API key, password, token | 🔴 Kritik |
| Unsafe deserialization | JSON/XML parsing | 🔴 Kritik |
| Path traversal | File system access | 🟡 Yüksek |
| Regex DoS | ReDoS vulnerabilities | 🟡 Yüksek |

---

## 3. Dependency Güvenliği

### npm/yarn
```bash
npm audit --audit-level=high
npm audit fix

# Alternatif
npx snyk test
```

### Python
```bash
pip-audit
safety check
```

### Dependency Update Stratejisi
1. **Haftalık**: Minor/patch updates
2. **Aylık**: Major version review
3. **Acil**: Critical vulnerability patch

---

## 4. Authentication & Authorization

### Best Practices
- JWT token expiration (15-30 dakika access, 7 gün refresh)
- Secure password policy (min 12 karakter, complexity)
- Rate limiting (login attempts)
- MFA implementasyonu

### Session Security
```javascript
// Express.js örnek
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,
    httpOnly: true,
    sameSite: 'strict',
    maxAge: 3600000 // 1 saat
  }
}));
```

---

## 5. Data Protection

### PII (Personal Identifiable Information)
- Data minimization prensibi
- Encryption at rest
- Access logging
- Data retention policy

### GDPR/KVKK Uyumu
```checklist
- [ ] Consent management
- [ ] Right to deletion
- [ ] Data portability
- [ ] Privacy policy
```

---

## 🛠️ Hızlı Komutlar

```bash
# Full security scan
npm audit && npx eslint . && semgrep --config=auto .

# Dependency vulnerability check
npm audit --audit-level=critical
```

---

*Security Audit v1.0 - 2025 Best Practices*


# Merged Content from container-security

---
name: secops_core
description: |
  This skill enables Claude to scan container images and running containers for vulnerabilities using tools like Trivy and Snyk. It identifies potential security risks in container environments. Use this skill when the user requests a security assessment of a container image, asks to identify vulnerabilities in a container, or wants to improve the security posture of their containerized applications. Trigger terms include "scan container," "container security," "vulnerability assessment," "Trivy scan," or "Snyk scan."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
---

## Overview

This skill empowers Claude to perform comprehensive security scans of container images and running containers. By leveraging industry-standard tools, it identifies vulnerabilities and provides insights for remediation, enhancing the overall security of containerized applications.

## How It Works

1. **Receiving Request**: Claude receives a user request to scan a container for vulnerabilities.
2. **Executing Scan**: Claude utilizes tools like Trivy or Snyk to perform the security scan on the specified container image or running container.
3. **Reporting Results**: Claude presents a detailed report of identified vulnerabilities, including severity levels and potential remediation steps.

## When to Use This Skill

This skill activates when you need to:
- Assess the security of a container image before deployment.
- Identify vulnerabilities in a running container within a production environment.
- Generate a security report for compliance purposes.

## Examples

### Example 1: Pre-Deployment Security Check

User request: "Scan this Docker image for vulnerabilities before I deploy it: myapp:latest"

The skill will:
1. Initiate a Trivy scan on the `myapp:latest` Docker image.
2. Return a report listing all identified vulnerabilities, their severity, and suggested fixes.

### Example 2: Runtime Container Security Assessment

User request: "Scan the running container with ID abc123xyz for security vulnerabilities."

The skill will:
1. Execute a Snyk scan on the container with ID `abc123xyz`.
2. Provide a report detailing any vulnerabilities found in the running container, along with remediation advice.

## Best Practices

- **Specify Image Name**: Always provide the full image name (including tag) for accurate scanning.
- **Review Severity Levels**: Pay close attention to high and critical severity vulnerabilities and address them promptly.
- **Regular Scanning**: Schedule regular container security scans to detect new vulnerabilities as they are discovered.

## Integration

This skill can be integrated with other CI/CD pipeline tools to automate security checks as part of the deployment process. It also provides data that can be used with reporting and dashboarding tools to visualize security posture over time.

# Merged Content from deps-security

---
name: secops_core
description: Dependency security audit, vulnerability scanning ve automated updates.
metadata:
  skillport:
    category: development
    tags:
      - security
      - audit
      - vulnerabilities
    related:
      - deps-npm
---

# 🔐 Deps Security

> Dependency security ve vulnerability management.

---

## 🔍 Security Audit

```bash
# npm audit
npm audit
npm audit fix

# Snyk
npx snyk test
npx snyk monitor
```

---

## 🤖 Automated Updates (Dependabot)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule:
      interval: weekly
    open-pull-requests-limit: 10
```

---

## ⚠️ Vulnerability Response

| Severity | Action |
|----------|--------|
| Critical | Hemen update |
| High | 24 saat içinde |
| Medium | Sprint içinde |
| Low | Planla |

---

## 🔒 Lock File

```bash
# ZORUNLU: Lock file commit et
git add package-lock.json
```

---

*SecOps Core v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/) & [CNCF Cloud Native Security](https://github.com/cncf/tag-security)

### Aşama 1: Secure Supply Chain (Shift Left)
- [ ] **SCA (Software Composition Analysis)**: `npm audit`, `snyk` veya `trivy` ile 3. parti kütüphane zafiyetlerini CI/CD'de bloklayacak şekilde tara.
- [ ] **Secret Scanning**: `git-secrets` veya `trufflehog` ile kod deposuna şifre/token pushlanmasını engelle (Pre-commit hook).
- [ ] **Image Scanning**: Build edilen Docker imajlarını registry'ye atmadan önce tara.

### Aşama 2: Application Security (Build & Deploy)
- [ ] **SAST (Static Application Security Testing)**: Kodun derlenmesi sırasında `SonarQube` veya `CodeQL` ile güvenlik açıklarını (SQLi, XSS) tara.
- [ ] **DAST (Dynamic Application Security Testing)**: Uygulama çalışırken `OWASP ZAP` ile dışarıdan saldırı simülasyonu yap.
- [ ] **IaC Scanning**: Terraform veya Kubernetes manifestlerini `checkov` veya `kics` ile yanlış konfigürasyonlara karşı tara.

### Aşama 3: Runtime Security & Monitoring
- [ ] **Runtime Protection**: Konteynerların içinde yetkisiz process çalışmasını `Falco` ile izle.
- [ ] **Vulnerability Management**: Bulunan açıklar için SLA belirle (Critical: 24h, High: 1 hafta) ve takip et.
- [ ] **Penetration Testing**: Yılda en az bir kez profesyonel sızma testi yaptır.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Pipeline güvenlik taramasını geçemeyen build'i durduruyor mu? |
| 2 | Secrets yönetimi için Vault veya Cloud KMS kullanılıyor mu? (Environment variable'da plain text yok). |
| 3 | Tüm güvenlik bulguları merkezi bir dashboard'da toplanıyor mu? (DefectDojo vb.). |
