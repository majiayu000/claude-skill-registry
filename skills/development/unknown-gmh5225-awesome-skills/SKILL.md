---
name: security-skills-guide
description: Guide for security-related Agent Skills including penetration testing, code auditing, threat hunting, and forensics skills.
---

# Security Skills Guide

## Scope

Use this skill when:

- Finding or adding security-related skills
- Understanding cybersecurity skill categories
- Organizing security skills in README.md

## Security Skill Categories

### Penetration Testing

| Category | Skills |
|----------|--------|
| Web Application | Burp Suite, FFUF fuzzing, SQL injection, XSS testing |
| Network | Nmap, Wireshark, SMTP/SSH testing |
| Cloud | AWS/Azure/GCP penetration testing |
| Active Directory | Kerberoasting, DCSync, pass-the-hash |

### Code Auditing

| Category | Skills |
|----------|--------|
| Static Analysis | CodeQL, Semgrep, Slither |
| Smart Contracts | Solidity security, Move auditing |
| Variant Analysis | Finding similar vulnerabilities |

### Threat Hunting

| Category | Skills |
|----------|--------|
| Detection Rules | Sigma rules, YARA |
| Forensics | File metadata, memory analysis |
| Incident Response | Triage, investigation |

## Key Security Skill Repositories

### Trail of Bits Security Team
- `trailofbits/skills` - Static analysis, code auditing, smart contracts

### Antigravity Collection
- `sickn33/antigravity-awesome-skills` - 50+ cybersecurity skills

### Community Skills
- `mhattingpete/claude-skills-marketplace` - Computer forensics skills

## Where to Add Security Skills in README

- **Penetration testing tools**: `Cybersecurity & Penetration Testing`
- **Code analysis tools**: `Security & Systems` or `Development & Code Tools`
- **Threat hunting**: `Security & Systems`
- **Smart contract security**: `Development & Code Tools` (if dev-focused)

## Security Skill Best Practices

1. **Clear scope**: Define what the skill does and doesn't do
2. **Legal warnings**: Include responsible use disclaimers
3. **Tool requirements**: List required external tools
4. **Safe defaults**: Use non-destructive operations by default
5. **Logging**: Include audit trail capabilities

## Example Security Skill Structure

```
threat-hunting/
├── SKILL.md           # Main instructions
├── scripts/
│   ├── sigma-search.py
│   └── log-parser.sh
├── references/
│   └── sigma-rules.md
└── templates/
    └── report.md
```

## Full Resource List

For more detailed security skill resources, complete link lists, or the latest information, use WebFetch to retrieve the full README.md:

```
https://raw.githubusercontent.com/gmh5225/awesome-skills/refs/heads/main/README.md
```

The README.md contains the complete categorized resource list with all links.
