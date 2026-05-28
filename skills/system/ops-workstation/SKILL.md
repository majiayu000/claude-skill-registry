---
name: ops-workstation
description: >
  Workstation diagnostics, health monitoring, and maintenance.
  Knows this machine and can help troubleshoot, clean up, and maintain it.
triggers:
  - check system
  - memory usage
  - memory leak
  - gpu status
  - disk space
  - drive health
  - why did it crash
  - out of memory
  - system slow
  - workstation specs
  - install drive
  - cleanup
  - maintenance
  - duplicate files
  - find duplicates
  - duplicate movies
  - wasted space
  - slim storage
  - recover space
  - free up space
  - cache cleanup
  - model cache
  - lower quality
  - media duplicates
  - network status
  - dns check
  - temperature
  - temps
  - thermal
  - container health
  - docker status
---

# Workstation Ops

Diagnose, monitor, and maintain this workstation.

## This Machine

| Component | Spec |
|-----------|------|
| Motherboard | MSI TRX40 PRO 10G |
| CPU | AMD Threadripper 3960X (24c/48t) |
| RAM | 256 GB DDR4 |
| GPU | NVIDIA RTX A5000 (24GB) |
| Boot | WD Black SN850X 4TB → `/` |
| Storage | Seagate IronWolf 12TB → `/mnt/storage12tb` |

## Commands

| Command | What it does |
|---------|--------------|
| `./run.sh` | Quick resource check |
| `./run.sh memory` | What's using RAM |
| `./run.sh gpu` | GPU status & VRAM |
| `./run.sh health` | Drive health & maintenance status |
| `./run.sh net` | Network diagnostics (link/IP/DNS/sockets) |
| `./run.sh temps` | Temperature monitoring (CPU/GPU/NVMe) |
| `./run.sh containers` | Docker container health |
| `./run.sh slim` | Find storage savings (media, caches, models) |
| `./run.sh duplicates` | Find exact duplicate files |
| `./run.sh crashes` | Check for OOM/crashes |
| `./run.sh specs` | Hardware docs & upgrade procedures |

## Agent Quick Reference

**"Is the system healthy?"**
```bash
./run.sh health
```

**"What's using all the memory?"**
```bash
./run.sh memory
```

**"Will my model fit in GPU?"**
```bash
./run.sh gpu --need 8000
```

**"Something crashed"**
```bash
./run.sh crashes --oom
```

**"Where can I recover storage?"**
```bash
./run.sh slim                      # Overview of all opportunities
./run.sh slim --media              # Lower quality media versions
./run.sh slim --caches             # Cache cleanup (pip, docker, npm)
./run.sh slim --models             # ML model caches
```

**"Is the network OK?"**
```bash
./run.sh net                       # LAN, DNS, sockets, gateway
./run.sh net --json                # Agent-parseable JSON
./run.sh net --no-external         # Skip external ICMP checks
OUTPUT=json ./run.sh net           # Alternative JSON output
```

**"Are temps safe?"**
```bash
./run.sh temps                     # Markdown summary (exit code: 0=OK, 1=WARN, 2=CRIT)
./run.sh temps --json              # JSON with exit codes
./run.sh temps --warn 70 --crit 80 # Custom thresholds
```

**"How are my containers?"**
```bash
./run.sh containers                # Docker status, restart counts
./run.sh containers --json         # Agent-parseable JSON
```

**"Find duplicate movies"**
```bash
./run.sh duplicates --dry-run              # Quick check by size
./run.sh duplicates                         # Full scan with checksums
./run.sh duplicates --type mkv --min-size 500  # Only large .mkv files
```

**"What can I clean up?"**
```bash
./run.sh health --cleanup
```

**"How do I add a hard drive?"**
```bash
./run.sh specs --procedures
```

## Maintenance Recommendations

The skill will identify these issues automatically:

| Issue | How to check | How to fix |
|-------|--------------|------------|
| High memory | `./run.sh memory` | Close IDEs, kill idle Claude Code |
| Disk filling up | `./run.sh slim` | Clear caches, remove duplicates |
| Lower quality media | `./run.sh slim --media` | Delete lower quality versions |
| Large caches | `./run.sh slim --caches` | `pip cache purge`, `docker prune` |
| Duplicate files | `./run.sh duplicates` | Review and remove exact duplicates |
| Drive failing | `sudo ./run.sh health --drives` | Replace drive |
| Pending updates | `./run.sh health` | `sudo apt upgrade` |

## Quick Cleanup

```bash
# See all storage savings opportunities
./run.sh slim

# Caches (can recover 30+ GB)
pip cache purge
npm cache clean --force
docker system prune -a
huggingface-cli delete-cache  # ML models

# System
sudo apt autoremove -y && sudo apt clean
sudo journalctl --vacuum-size=500M

# Find lower quality media versions
./run.sh slim --media
```

## Hardware Reference

See [WORKSTATION.md](./WORKSTATION.md) for:
- Full hardware specs with mermaid diagrams
- Drive layout and available slots
- Step-by-step upgrade procedures (NVMe, SATA, RAM, GPU)
