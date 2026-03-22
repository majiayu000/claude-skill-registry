---
name: memorybox
description: Zero-dependency memory maintenance CLI for OpenClaw. Keeps MEMORY.md lean with 3-tier hierarchical organization. Works alongside Mem0, Supermemory, QMD — or standalone. Install once, forget about memory management.
---

# MemoryBox

Zero-dependency memory maintenance tool for OpenClaw agents.

## What It Does

Prevents MEMORY.md bloat by organizing memory into 3 tiers:
- **Tier 1**: MEMORY.md (≤10KB, loaded every session)
- **Tier 2**: memory/domains/*.md (searched on-demand)
- **Tier 3**: memory/archive/ (old daily logs)

Works alongside Mem0, Supermemory, QMD, or standalone. Only touches file structure — never configs or plugins.

## Install

```bash
git clone https://github.com/Ramsbaby/openclaw-memorybox.git
cd openclaw-memorybox && chmod +x bin/memorybox
sudo ln -sf "$(pwd)/bin/memorybox" /usr/local/bin/memorybox
```

## Usage

```bash
memorybox doctor ~/openclaw    # Full diagnostic (start here)
memorybox split ~/openclaw     # Interactive: move bloated sections to domain files
memorybox health ~/openclaw    # Quick health score (0-100)
memorybox archive ~/openclaw   # Archive old daily logs (14+ days)
memorybox dedupe ~/openclaw    # Find duplicate content
memorybox stale ~/openclaw     # Detect outdated content
memorybox analyze ~/openclaw   # Section-by-section size breakdown
memorybox suggest ~/openclaw   # Improvement recommendations
memorybox report ~/openclaw    # Before/after token savings
memorybox init ~/openclaw      # Set up 3-tier directory structure
```

## Teach Your Agent

Add to AGENTS.md:

```markdown
## Memory Protocol
- **MEMORY.md** (≤10KB): Core facts only. Loaded everywhere — keep it lean.
- **memory/domains/*.md**: Detailed reference. Use `memory_search` to find.
- **memory/archive/**: Old logs. Rarely needed.
```

## Results

Tested on production (7 Discord channels, 48 crons):
- MEMORY.md: 20KB → 3.5KB (-83%)
- Context pressure: 98% → 7%
- Setup time: 5 minutes

## Links

- GitHub: https://github.com/Ramsbaby/openclaw-memorybox
- Companion: https://github.com/Ramsbaby/openclaw-self-healing
