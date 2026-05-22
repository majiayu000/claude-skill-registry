---
name: hack
description: >
  Containerized security auditing and ethical hacking tools.
  All operations run in isolated Docker containers for safety.
allowed-tools:
  - run_command
  - read_file
triggers:
  - hack
  - scan
  - audit
  - security check
  - red team
  - blue team
metadata:
  short-description: Containerized security auditing and ethical hacking
  requires: docker
---

# Hack Skill

**Containerized security auditing and ethical hacking tools.**

All security operations run in **isolated Docker containers** - no tools execute on the host system. This ensures:
- Isolation from host filesystem and network
- Reproducible scanning environment
- No risk of tool vulnerabilities affecting host
- Safe execution of untrusted exploit code

## Prerequisites

- **Docker Engine** must be installed and running
- The security container image will be built automatically on first use

## Commands

### Network Scanning

```bash
# Basic port scan
./run.sh scan 192.168.1.1

# Service detection scan
./run.sh scan 192.168.1.1 --scan-type service

# Vulnerability scripts
./run.sh scan 192.168.1.1 --scan-type vuln --ports 22,80,443

# Save results
./run.sh scan 192.168.1.1 --output scan_results.txt
```

### Static Application Security Testing (SAST)

```bash
# Full audit (Semgrep + Bandit)
./run.sh audit /path/to/code

# Semgrep only
./run.sh audit /path/to/code --tool semgrep

# Bandit only (Python)
./run.sh audit /path/to/code --tool bandit

# Filter by severity
./run.sh audit /path/to/code --severity high
```

### Software Composition Analysis (SCA)

```bash
# Check Python dependencies for vulnerabilities
./run.sh sca /path/to/project

# Use safety instead of pip-audit
./run.sh sca /path/to/project --tool safety
```

### Check Available Tools

```bash
./run.sh tools
```

### Isolated Exploit Execution

```bash
# Run Python exploit in isolated container
./run.sh exploit --target 192.168.1.50 --env python --payload exploit.py

# Interactive shell in isolated environment
./run.sh exploit --target 192.168.1.50 --env kali --interactive
```

### Knowledge Base & Research

```bash
# Fetch exploits from Exploit-DB
./run.sh learn --source exploit-db

# Search GitHub for CVE PoCs
./run.sh learn --source github --query "CVE-2024-1234"

# Deep research via dogpile
./run.sh research "buffer overflow mitigation techniques"
```

## Architecture

```
+-------------------+     +------------------------+
|   Host System     |     |  Docker Container      |
|                   |     |  (hack-skill-security) |
| ./run.sh scan ... | --> |  nmap, semgrep, bandit |
|                   |     |  pip-audit, safety     |
| (No tools here)   |     |                        |
+-------------------+     +------------------------+
        |                          |
        +--- Results returned -----+
```

## Red Team / Blue Team Usage

### Red Team (Attack)
- `scan` - Discover open ports and services
- `audit` - Find vulnerabilities in target code
- `exploit` - Execute PoC in isolated environment
- `learn --source github` - Find CVE exploits
- `prove --negate` - Find counterexamples to security claims

### Blue Team (Defense)
- `audit` - Find vulnerabilities before attackers
- `sca` - Identify vulnerable dependencies
- `prove` - Formally verify security properties
- `research` - Study attack techniques to defend against

## Memory Integration

The hack skill is **deeply integrated** with the memory skill - the brain of the entire project.

### Automatic Memory Recall
All scanning and audit commands automatically query memory for relevant prior knowledge before execution:
- Previous scanning techniques that worked
- Known vulnerabilities and their mitigations
- Exploit patterns and defenses

```bash
# Scan with memory recall (enabled by default)
./run.sh scan 192.168.1.1

# Disable memory recall for faster scans
./run.sh scan 192.168.1.1 --no-recall
```

### Explicit Memory Commands
```bash
# Store security knowledge
./run.sh remember "Use nmap -sV for service detection" --title "nmap tips"
./run.sh remember "CVE-2024-1234 affects version 1.0-1.5" --tags "cve,critical"

# Recall knowledge
./run.sh recall "nmap scanning techniques"
./run.sh recall "buffer overflow exploits" --k 10
```

### Knowledge Flow
```
+----------------+     +---------------+     +------------------+
| hack skill     | --> | memory skill  | --> | Future Sessions  |
|                |     |               |     |                  |
| - scan results |     | - Store       |     | - recall before  |
| - audit finds  |     | - Embed       |     |   operations     |
| - exploits     |     | - Index       |     | - learn from     |
|                |     |               |     |   past attempts  |
+----------------+     +---------------+     +------------------+
```

## Leveraged Skills

The hack skill **delegates** to sibling skills rather than duplicating functionality:

### Core Integrations (Direct Commands)

| Skill | Command | Purpose |
|-------|---------|---------|
| `memory` | (automatic) | Recall prior exploits/solutions before every operation |
| `anvil` | `hack harden` | Thunderdome multi-agent red teaming |
| `ops-docker` | `hack docker-cleanup` | Container pruning and management |
| `treesitter` | `hack symbols` | Parse code structure before auditing |
| `taxonomy` | `hack classify` | Tag findings with bridge tags (Loyalty, Fragility, etc.) |
| `task-monitor` | (automatic) | Track long-running scan progress |

### Research Integrations (via `hack research`)

| Skill | Usage |
|-------|-------|
| `dogpile` | Deep multi-source research |
| `arxiv` | Academic security papers |
| `perplexity` | Real-time threat intelligence |
| `lean4-prove` | Formal security verification |
| `learn` | Knowledge extraction & storage |

### Skill Delegation Examples

```bash
# Red-team a codebase via anvil Thunderdome
./run.sh harden /path/to/code --issue "SQL injection in auth"

# Clean up Docker via ops-docker
./run.sh docker-cleanup --until 24h --execute

# Extract code symbols via treesitter before audit
./run.sh symbols /path/to/file.py --content

# Classify findings via taxonomy for graph storage
./run.sh classify "SQL injection vulnerability in login handler"
```

## Safety Notes

1. **Authorized Use Only** - Only use against systems you have permission to test
2. **Isolated Execution** - All tools run in Docker containers
3. **Network Isolation** - SAST audits run with `--network=none`
4. **Read-Only Mounts** - Target directories mounted read-only

## Example Workflows

### Vulnerability Assessment
```bash
# 1. Scan network
./run.sh scan 192.168.1.0/24 --scan-type basic

# 2. Audit discovered services
./run.sh audit /path/to/webapp --severity medium

# 3. Check dependencies
./run.sh sca /path/to/webapp
```

### Exploit Development
```bash
# 1. Research the vulnerability
./run.sh learn --source github --query "CVE-2024-XXXX"

# 2. Test exploit in isolation
./run.sh exploit --target test-vm --env python --payload poc.py

# 3. Verify fix with formal methods
./run.sh prove --claim "buffer overflow impossible after patch"
```
