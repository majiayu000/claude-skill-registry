---
name: vt
description: Spin up intentionally vulnerable environments from the terminal using Docker. Use when the user wants to practice security testing, set up CTF labs, exploit CVEs, or deploy vulnerable web apps like DVWA, Juice Shop, or WebGoat.
---

# Vulnerable Target (vt)

vt is a Go CLI tool that creates intentionally vulnerable environments for security professionals, researchers, and educators using Docker Compose.

> **CAUTION**: vt creates intentionally vulnerable environments - always run in isolated networks (VMs/sandboxes) and never expose to the internet.

## Installation

### Prerequisites

- Go 1.24+
- Docker & Docker Compose

### Install with Go

```bash
go install github.com/happyhackingspace/vt/cmd/vt@latest
```

### Build from Source

```bash
git clone https://github.com/HappyHackingSpace/vt.git
cd vt
go build -o vt cmd/vt/main.go
mv vt /usr/local/bin/
```

## Command Reference

| Command | Description |
|---------|-------------|
| `vt template --list` | List all available templates |
| `vt template --list --filter <tag>` | Filter templates by tag (sqli, xss, ssrf, etc.) |
| `vt template --update` | Update templates from remote repository |
| `vt start --id <template-id>` | Start a vulnerable environment |
| `vt start --tags <tag1,tag2>` | Start all templates matching tags |
| `vt ps` | List running environments |
| `vt stop --id <template-id>` | Stop an environment |
| `vt stop --tags <tag1,tag2>` | Stop all templates matching tags |
| `vt -v debug <command>` | Run with debug verbosity |

## Available Templates

| Template | Type | Description |
|----------|:----:|-------------|
| `vt-dvwa` | Lab | Damn Vulnerable Web Application |
| `vt-juice-shop` | Lab | OWASP Juice Shop |
| `vt-webgoat` | Lab | OWASP WebGoat |
| `vt-bwapp` | Lab | Buggy Web Application |
| `vt-mutillidae-ii` | Lab | OWASP Mutillidae II |

More templates at [vt-templates](https://github.com/HappyHackingSpace/vt-templates).

## Examples

```bash
# List templates with SQL injection vulnerabilities
vt template --list --filter sqli

# Start DVWA
vt start --id vt-dvwa

# Start all XSS-related labs
vt start --tags xss

# Check running environments
vt ps

# Stop a specific environment
vt stop --id vt-dvwa
```

## Use Cases

| Use Case | Template |
|----------|----------|
| Practice SQL Injection | vt-dvwa |
| Learn XSS Exploitation | vt-dvwa |
| Test OWASP Top 10 | vt-juice-shop |
| Exploit Real CVEs | vt-2025-29927 |
| API Security Testing | vt-webgoat |
| Train Security Teams | vt-mutillidae-ii |

## References

- Repository: https://github.com/HappyHackingSpace/vt
- Templates: https://github.com/HappyHackingSpace/vt-templates
