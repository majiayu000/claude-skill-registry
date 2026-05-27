---
name: battle
description: >
  Red vs Blue team security competition orchestrator. Runs long-running overnight
  battles with 1000s of interactions, scoring, and insight generation.
allowed-tools:
  - Bash
  - Read
triggers:
  - battle
  - thunderdome
  - red vs blue
  - overnight battle
  - security competition
  - red team vs blue team
metadata:
  short-description: Red vs Blue team security competition
  requires: docker
---

# Battle Skill

**Red vs Blue Team Security Competition Orchestrator**

Pits a Red Team (attack) against a Blue Team (defense) in a long-running competitive loop. Each team leverages all `.pi/skills` to attack or defend a target codebase.

## Architecture

Based on research into RvB framework, DARPA AIxCC, and Microsoft PyRIT:

```
┌─────────────────────────────────────────────────────────┐
│                 Battle Orchestrator                      │
│  - Game loop (RvB pattern)                              │
│  - Concurrent Red/Blue execution                        │
│  - Entropy-driven termination                           │
│  - Checkpointing for overnight runs                     │
└─────────────────────────────────────────────────────────┘
         │                              │
    ┌────┴────┐                    ┌────┴────┐
    │ Red Team │                   │ Blue Team│
    │ (Thread) │                   │ (Thread) │
    ├──────────┤                   ├──────────┤
    │ Skills:  │                   │ Skills:  │
    │ - hack   │                   │ - anvil  │
    │ - memory │                   │ - memory │
    └──────────┘                   └──────────┘
         │                              │
         └──────────┬───────────────────┘
                    │
    ┌───────────────┴────────────────────┐
    │           Digital Twin              │
    │  ┌─────────────────────────────┐   │
    │  │ Mode: git_worktree          │   │
    │  │   - Red attacks arena       │   │
    │  │   - Blue patches workspace  │   │
    │  │   - Cherry-pick to test     │   │
    │  ├─────────────────────────────┤   │
    │  │ Mode: docker                │   │
    │  │   - Isolated containers     │   │
    │  │   - Battle network          │   │
    │  ├─────────────────────────────┤   │
    │  │ Mode: qemu                  │   │
    │  │   - Emulated firmware       │   │
    │  │   - GDB attach points       │   │
    │  └─────────────────────────────┘   │
    └────────────────────────────────────┘
```

## Digital Twin Modes

The battle skill supports multiple target types through its Digital Twin system:

### 1. Source Code (git_worktree)
For battling over git repositories. Creates isolated git worktrees for each team.

```bash
./run.sh battle /path/to/repo --rounds 100
```

### 2. Docker Container (docker)
For battling over containerized applications. Spins up separate containers for each team.

```bash
# Using a Docker image
./run.sh battle --docker-image nginx:latest --rounds 100

# Using a Dockerfile in the target directory
./run.sh battle /path/with/Dockerfile --mode docker
```

### 3. Firmware/Microprocessor (qemu)
For battling over firmware and embedded systems. Boots firmware in QEMU emulator.

```bash
# Auto-detect architecture from ELF header
./run.sh battle firmware.elf --rounds 100

# Specify machine type explicitly
./run.sh battle firmware.bin --qemu-machine arm
./run.sh battle firmware.bin --qemu-machine riscv64
./run.sh battle bios.rom --qemu-machine x86_64
```

Supported QEMU machines:
- `arm` - ARM Cortex-M (STM32, etc.)
- `aarch64` - ARM64
- `riscv32`/`riscv64` - RISC-V
- `x86_64`/`i386` - x86
- `mips` - MIPS (routers, embedded)

### 4. Copy Mode (fallback)
For non-git directories. Creates simple file copies for each team.

## Commands

```bash
# Start a battle (10 rounds for testing)
./run.sh battle /path/to/codebase --rounds 10

# Start overnight battle (1000 rounds)
./run.sh battle /path/to/codebase --overnight

# Battle a Docker container
./run.sh battle --docker-image myapp:latest --rounds 100

# Battle firmware with QEMU
./run.sh battle firmware.bin --qemu-machine arm --rounds 100

# Check battle status
./run.sh status

# Resume interrupted battle
./run.sh resume <battle-id>

# Generate report from completed battle
./run.sh report <battle-id>
```

## Scoring System (AIxCC-style)

| Metric | Weight | Description |
|--------|--------|-------------|
| Vulnerability Discovery | 1x | Red team finds vulnerability |
| Exploit Proof | +0.5x | Red team proves exploitability |
| Successful Patch | 3x | Blue team patches vulnerability |
| Time Decay | Variable | Faster responses score higher |
| Functionality Preserved | Required | Patches must not break code |

### Scores

- **TDSR** (True Defense Success Rate): Vulnerabilities fixed AND code works
- **FDSR** (Fake Defense Success Rate): Attack blocked but code broken
- **ASC** (Attack Success Count): Total unique exploits discovered

## Game Loop (Learning-Based)

Each round follows a **learn → act → reflect** pattern:

```
Round k:

┌─────────────────────────────────────────────────────────────┐
│                    1. RESEARCH PHASE                         │
├─────────────────────────────────────────────────────────────┤
│ Red Team:                      Blue Team:                    │
│ - Recall past attack attempts  - Recall past defenses        │
│ - Query /dogpile for new       - Query /dogpile for          │
│   exploitation techniques        hardening strategies        │
│ - Review opponent's patterns   - Analyze attack evolution    │
│ (Budget: 3 research calls max)                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    2. ACTION PHASE                           │
├─────────────────────────────────────────────────────────────┤
│ Red Team Attack:               Blue Team Defense:            │
│ - Execute learned strategy     - Apply patches via anvil     │
│ - AFL++ fuzzing with coverage  - Verify via QCOW2 overlay    │
│ - Collect crashes/findings     - Run regression tests        │
│ - Tag findings with /taxonomy  - Tag patches with /taxonomy  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   3. REFLECTION PHASE                        │
├─────────────────────────────────────────────────────────────┤
│ Both Teams:                                                  │
│ - Archive round episode (actions, outcomes, learnings)       │
│ - Store successful strategies in /memory                     │
│ - Update belief about opponent's capabilities                │
│ - Evolve strategy for next round                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   4. SCORING & CHECKPOINT                    │
├─────────────────────────────────────────────────────────────┤
│ - Calculate AIxCC-style scores                               │
│ - Check termination conditions                               │
│ - Save checkpoint (QEMU state + team memories)              │
└─────────────────────────────────────────────────────────────┘
```

### Memory Architecture

Each team maintains isolated knowledge:

```
battle_red_<battle_id>/           battle_blue_<battle_id>/
├── strategies/                   ├── strategies/
│   ├── successful_attacks        │   ├── successful_patches
│   └── failed_attempts           │   └── broken_defenses
├── research/                     ├── research/
│   └── dogpile_results           │   └── dogpile_results
├── episodes/                     ├── episodes/
│   ├── round_001.json            │   ├── round_001.json
│   └── round_002.json            │   └── round_002.json
└── taxonomy/                     └── taxonomy/
    ├── cwe_classifications       ├── mitigation_types
    └── severity_scores           └── effectiveness_scores
```

Teams **cannot access opponent's memory** - this creates true adversarial learning.

## Termination Conditions

Battle ends when ANY condition is met:

1. **Null Production**: Both teams fail to generate new findings for 3 rounds
2. **Maximum Rounds**: Configured limit reached
3. **Metric Convergence**: Scores stable for 5 consecutive rounds
4. **Kill Switch**: Manual termination via `./run.sh stop`

## Task Monitor Integration

Battles register with task-monitor for overnight progress tracking:

```bash
# View battle progress in TUI
.pi/skills/task-monitor/run.sh tui --filter battle
```

## Report Output

After battle completion, generates:

- **Executive Summary**: Winner, key metrics, risk score
- **Vulnerability Report**: By severity, category, remediation status
- **Attack Evolution**: How Red team adapted over rounds
- **Defense Timeline**: Blue team improvements over time
- **Recommendations**: Prioritized security improvements

## Leveraged Skills

| Skill | Team | Purpose |
|-------|------|---------|
| hack | Red | Scanning, auditing, exploitation |
| anvil | Blue | Multi-agent patching (Thunderdome) |
| memory | Both | Recall prior strategies |
| treesitter | Blue | Code structure analysis |
| taxonomy | Both | Classify findings |
| task-monitor | Orchestrator | Progress tracking |
| ops-docker | Both | Container management |

## Example Battle

```bash
# Start 100-round battle on current project
./run.sh battle --target . --rounds 100

# Output:
# Battle ID: battle_20250128_221500
# Target: /home/user/project
# Rounds: 100
#
# Registering with task-monitor...
# Starting Round 1/100...
# [Red] Scanning target with hack...
# [Red] Found 3 potential vulnerabilities
# [Blue] Analyzing attack logs...
# [Blue] Generating patch for SQL injection...
# [Blue] Patch applied, running verification...
# Round 1 complete. Red: 3 pts, Blue: 9 pts
# ...
#
# Battle Complete!
# Winner: Blue Team (847 pts vs 423 pts)
# Report: ./reports/battle_20250128_221500.md
```
