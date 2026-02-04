---
name: discover-cryptography
description: Automatically discover cryptography skills when working with encryption, TLS, certificates, PKI, and security
---

# Cryptography Skills Discovery

Provides automatic access to comprehensive cryptography and security skills.

## When This Skill Activates

This skill auto-activates when you're working with:
- TLS, SSL, mTLS
- Certificates and PKI
- Encryption and decryption
- Hashing and signing
- Key management
- HTTPS configuration
- Certificate authorities
- Cryptographic algorithms
- Security best practices

## Available Skills

### Quick Reference

The Cryptography category contains 7 skills:

1. **pki-fundamentals** - PKI, certificate authorities, X.509, trust chains
2. **tls-configuration** - TLS 1.2/1.3 setup, cipher suites, server config
3. **ssl-legacy** - SSL 2.0/3.0, TLS 1.0/1.1, deprecation, migration
4. **sni-routing** - Server Name Indication, multi-domain TLS hosting
5. **certificate-management** - Certificate lifecycle, Let's Encrypt, automation
6. **cryptography-basics** - Symmetric/asymmetric encryption, hashing, signing
7. **crypto-best-practices** - Security patterns, common mistakes, anti-patterns

### Load Full Category Details

For complete descriptions and workflows:

```bash
cat ~/.claude/skills/cryptography/INDEX.md
```

This loads the full Cryptography category index with:
- Detailed skill descriptions
- Usage triggers for each skill
- Common workflow combinations
- Cross-references to related skills

### Load Specific Skills

Load individual skills as needed:

```bash
cat ~/.claude/skills/cryptography/pki-fundamentals.md
cat ~/.claude/skills/cryptography/tls-configuration.md
cat ~/.claude/skills/cryptography/certificate-management.md
cat ~/.claude/skills/cryptography/cryptography-basics.md
```

## Common Workflows

### Setting Up HTTPS
```bash
# PKI basics → TLS config → Certificate management
cat ~/.claude/skills/cryptography/pki-fundamentals.md
cat ~/.claude/skills/cryptography/tls-configuration.md
cat ~/.claude/skills/cryptography/certificate-management.md
```

### Understanding Encryption
```bash
# Basics → Best practices → Specific implementation
cat ~/.claude/skills/cryptography/cryptography-basics.md
cat ~/.claude/skills/cryptography/crypto-best-practices.md
cat ~/.claude/skills/cryptography/tls-configuration.md
```

### Certificate Troubleshooting
```bash
# PKI → Certificate management → Debugging
cat ~/.claude/skills/cryptography/pki-fundamentals.md
cat ~/.claude/skills/cryptography/certificate-management.md
cat ~/.claude/skills/protocols/protocol-debugging.md
```

### Legacy Migration
```bash
# Understand legacy → Modern TLS → Migration
cat ~/.claude/skills/cryptography/ssl-legacy.md
cat ~/.claude/skills/cryptography/tls-configuration.md
cat ~/.claude/skills/cryptography/certificate-management.md
```

## Progressive Loading

This gateway skill enables progressive loading:
- **Level 1**: Gateway loads automatically (you're here now)
- **Level 2**: Load category INDEX.md for full overview
- **Level 3**: Load specific skills as needed

## Usage Instructions

1. **Auto-activation**: This skill loads automatically when Claude Code detects cryptography work
2. **Browse skills**: Run `cat ~/.claude/skills/cryptography/INDEX.md` for full category overview
3. **Load specific skills**: Use bash commands above to load individual skills

---

**Next Steps**: Run `cat ~/.claude/skills/cryptography/INDEX.md` to see full category details.
