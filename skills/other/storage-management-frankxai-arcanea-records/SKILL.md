---
name: storage-management
description: >
  Arcanea Storage Guardian System. Continuous disk management for Windows + WSL2 environments.
  Audit, clean, migrate, monitor, backup, and visualize storage across C:/ and D:/ drives.
  Security council ensures nothing critical is deleted. Agent team manages all operations.
version: 1.0.0
author: Arcanea
tags: [storage, disk, cleanup, backup, monitoring, windows, wsl2, security]
triggers:
  - storage
  - disk space
  - cleanup
  - free space
  - disk full
  - out of space
  - storage audit
  - move to D
  - backup
  - cloud sync
---

# The Storage Guardian System

> *"A creator's tools must serve the work, not consume it. Guard your space as fiercely as you guard your craft."*

---

## System Architecture

```
+------------------------------------------------------------------+
|                   STORAGE GUARDIAN COUNCIL                        |
+------------------------------------------------------------------+
|                                                                  |
|  LYSSANDRIA (Earth)     - Chief Architect: Migration & Structure |
|  DRACONIA (Fire)        - Purge Commander: Aggressive Cleanup    |
|  LYRIA (Sight)          - Audit Oracle: Deep Analysis & Viz      |
|  MAYLINN (Wind)         - Cloud Syncer: Backup & Cloud Ops      |
|  SHINKAMI (Source)       - Security Arbiter: Delete Prevention    |
|                                                                  |
+------------------------------------------------------------------+
           |              |              |              |
     +-----------+  +-----------+  +-----------+  +-----------+
     |  AUDIT    |  |  CLEAN    |  |  MIGRATE  |  |  MONITOR  |
     |  ENGINE   |  |  ENGINE   |  |  ENGINE   |  |  ENGINE   |
     +-----------+  +-----------+  +-----------+  +-----------+
```

---

## The Five Guardians of Storage

### 1. Lyssandria - The Migration Architect (Earth Gate)

**Domain**: Structural reorganization, D:/ migration, symlink strategy
**Principle**: "Move intelligently. Every byte should live where it serves best."

**Responsibilities**:
- WSL2 export/import to D:/
- Docker data relocation
- Game library migration (Steam, Epic, Riot)
- Symlink creation and management
- pnpm/npm store relocation
- Directory structure optimization

**Decision Matrix**:
```
IF size > 5GB AND not_system_critical:
  -> Recommend D:/ migration with symlink
IF frequently_accessed AND on_D:
  -> Consider junction point for performance
IF development_dependency:
  -> Use pnpm store-dir or npm cache config
```

### 2. Draconia - The Purge Commander (Fire Gate)

**Domain**: Aggressive but safe cleanup operations
**Principle**: "Burn what's dead. Feed the living."

**Responsibilities**:
- Windows temp file cleanup
- Docker system prune
- npm/pnpm cache pruning
- Old node_modules detection (npkill)
- Git garbage collection across repos
- Browser cache cleanup
- Electron app cache cleanup (Claude Desktop, Perplexity, Slack, etc.)
- Windows Update cleanup
- Recycle Bin enforcement

**Safe Deletion Rules**:
```
ALWAYS SAFE:
  - %TEMP%/* (Windows temp)
  - C:\Windows\Temp\* (with elevation)
  - Recycle Bin contents
  - Docker dangling images
  - npm/pnpm cache (re-downloadable)
  - node_modules in inactive projects
  - .next / .turbo / dist / build caches

REQUIRES REVIEW (Shinkami approval):
  - Docker volumes
  - Git objects (after gc)
  - Application data folders
  - Anything > 1GB

NEVER DELETE:
  - .env files
  - .git directories (only gc inside them)
  - Active project source code
  - Database files (.sqlite3, .db)
  - SSH keys, GPG keys, credentials
  - OneDrive root structure
  - Windows system files
```

### 3. Lyria - The Audit Oracle (Sight Gate)

**Domain**: Deep analysis, visualization, reporting
**Principle**: "See everything. Understand before you act."

**Responsibilities**:
- Full disk audit (PowerShell + WSL2)
- Treemap visualization generation
- Weekly storage reports
- Growth trend tracking
- Anomaly detection (sudden space consumption)
- File age analysis (find stale data)
- Duplicate file detection

**Audit Levels**:
```
QUICK (30 seconds):
  - Drive free space
  - Top 10 folders by size
  - Known bloat locations check

STANDARD (5 minutes):
  - Full user profile scan
  - AppData breakdown
  - All node_modules enumeration
  - Docker disk usage
  - WSL2 VHDX size vs actual usage

DEEP (30 minutes):
  - Full C:/ scan via WizTree/PowerShell
  - Duplicate file detection
  - File age histogram
  - Growth rate calculation
  - Cross-drive comparison
```

**Report Format**:
```
=== ARCANEA STORAGE REPORT ===
Date: {date}
Guardian: Lyria (Sight Gate)

DRIVE STATUS:
  C:/ {used}GB / {total}GB ({pct}%) [{bar}] {status_emoji}
  D:/ {used}GB / {total}GB ({pct}%) [{bar}] {status_emoji}

TOP CONSUMERS:
  1. {path} - {size}GB ({category})
  2. ...

CHANGES SINCE LAST AUDIT:
  + {path} grew by {delta}GB
  - {path} shrunk by {delta}GB

RECOMMENDATIONS:
  [CRITICAL] ...
  [HIGH] ...
  [MEDIUM] ...

SECURITY COUNCIL STATUS: {verdict}
```

### 4. Maylinn - The Cloud Syncer (Wind Gate)

**Domain**: Cloud backup, sync, offsite protection
**Principle**: "Let the important things flow freely between ground and sky."

**Responsibilities**:
- OneDrive Files On-Demand management
- rclone automation for critical backups
- Cloud archive strategy
- Backup verification
- Restore testing

**Backup Priority Tiers**:
```
TIER 1 - IRREPLACEABLE (Daily sync):
  - Source code (.git repos)
  - Configuration files (.claude/, .env.example)
  - Creative work (book/, lore/, designs)
  - Database exports
  - SSH/GPG keys (encrypted)

TIER 2 - IMPORTANT (Weekly sync):
  - Documents
  - Project documentation
  - Design assets (Figma exports)
  - Notes and research

TIER 3 - REBUILDABLE (Monthly or on-demand):
  - node_modules (npm install recreates)
  - Build artifacts (.next, dist)
  - Docker images (pull recreates)
  - Cache files

TIER 4 - DISPOSABLE (Never backup):
  - Temp files
  - Browser cache
  - Electron cache
  - Windows Update files
```

**OneDrive Optimization** (for your 220GB situation):
```
CRITICAL FIX: Enable "Files On-Demand"
  Settings > OneDrive > Advanced Settings > Files On-Demand: ON

This keeps files in cloud, downloads only when opened.
Free files: Right-click > "Free up space"

Expected recovery: 150-200 GB on C:/
```

### 5. Shinkami - The Security Arbiter (Source Gate)

**Domain**: Final approval for destructive operations, safety verification
**Principle**: "The Source protects all paths. No deletion without understanding."

**Responsibilities**:
- Review all deletion proposals > 1GB
- Verify backup exists before large deletions
- Check for active processes using target files
- Validate symlink integrity after migration
- Maintain deletion audit log
- Rollback capability for recent operations
- Protect secrets and credentials

**Security Protocol**:
```
BEFORE ANY DESTRUCTIVE OPERATION:
  1. Lyria audits the target (what exactly will be affected?)
  2. Maylinn verifies backup status (is it backed up?)
  3. Shinkami checks dependencies (is anything using this?)
  4. Shinkami checks recoverability (can we undo this?)
  5. IF all clear -> Draconia executes
  6. Log operation to audit trail

VETO CONDITIONS (operation blocked):
  - No backup exists for non-rebuildable data
  - Active process holds file lock
  - Path contains known critical files
  - Operation would delete > 50GB without explicit approval
  - Target is in NEVER_DELETE list
```

---

## Operations Playbook

### OP-1: Emergency Space Recovery

When C:/ free space < 10 GB:

```
Step 1: Draconia clears safe targets
  -> Empty Recycle Bin
  -> Clear %TEMP%
  -> Docker system prune -f
  -> pnpm store prune

Step 2: Maylinn enables OneDrive Files On-Demand
  -> Free up non-recent files
  -> Expected recovery: 50-200 GB

Step 3: Lyssandria migrates WSL2 to D:/
  -> wsl --export / wsl --import
  -> Expected recovery: 20-30 GB

Step 4: Lyria generates post-recovery report
```

### OP-2: Weekly Maintenance

```
Every Sunday:
  1. Lyria runs STANDARD audit
  2. Draconia cleans safe targets
  3. Lyssandria compacts WSL2 VHDX
  4. Maylinn syncs Tier 1 backups
  5. Generate weekly report
```

### OP-3: Monthly Deep Clean

```
First Saturday:
  1. Lyria runs DEEP audit
  2. Draconia runs npkill for stale node_modules
  3. Draconia runs git gc across all repos
  4. Lyssandria reviews symlink health
  5. Maylinn runs full backup verification
  6. Shinkami reviews deletion audit log
```

### OP-4: Migration Procedure

For moving any large directory from C:/ to D:/:

```
1. Lyria: Measure current size and location
2. Shinkami: Verify nothing critical will break
3. Maylinn: Ensure backup exists
4. Lyssandria: Execute migration
   a. Copy to D:/ target
   b. Verify integrity (checksum or file count)
   c. Remove original
   d. Create symlink/junction
   e. Test functionality
5. Lyria: Verify space recovered
6. Log operation
```

---

## Tool Requirements

### Windows (PowerShell)
- **WizTree** - Fast disk visualization (MFT-based)
- **Storage Sense** - Built-in auto-cleanup
- **Disk Cleanup** (cleanmgr) - System cleanup
- **diskpart** or **Optimize-VHD** - VHDX compaction

### WSL2 (Bash)
- **dust** (`apt install du-dust`) - Visual disk usage
- **gdu** (`apt install gdu`) - Interactive disk explorer
- **ncdu** (`apt install ncdu`) - Classic disk usage
- **npkill** (`npx npkill`) - node_modules finder
- **rclone** (`apt install rclone`) - Cloud sync

### Package Managers
- **pnpm store prune** - Clean unreferenced packages
- **npm cache clean --force** - Clear npm cache
- **uv cache clean** - Clear Python/uv cache
- **docker system prune** - Clean Docker

---

## Quick Commands Reference

```bash
# === AUDIT ===
# Quick space check
powershell.exe -Command "Get-PSDrive C,D | Select Name,@{N='UsedGB';E={[math]::Round(\$_.Used/1GB,1)}},@{N='FreeGB';E={[math]::Round(\$_.Free/1GB,1)}}"

# Top folders in user home
powershell.exe -Command "Get-ChildItem C:\Users\frank -Dir -Force | %{ [PSCustomObject]@{N=\$_.Name;GB=[math]::Round((Get-ChildItem \$_.FullName -Recurse -Force -EA 0 | Measure Length -Sum).Sum/1GB,2)} } | Sort GB -Desc | Select -First 15 | ft -Auto"

# WSL2 VHDX size
powershell.exe -Command "Get-ChildItem 'C:\Users\frank\AppData\Local\Packages\*\LocalState\ext4.vhdx' -Force -EA 0 | %{ Write-Host ('{0:N2} GB  {1}' -f (\$_.Length/1GB), \$_.FullName) }"

# Docker disk usage
docker system df 2>/dev/null

# === CLEAN ===
# Safe temp cleanup
powershell.exe -Command "Remove-Item \$env:TEMP\* -Recurse -Force -EA 0; Write-Host 'Temp cleaned'"

# Docker cleanup
docker system prune -f 2>/dev/null

# pnpm cleanup
pnpm store prune 2>/dev/null

# uv cache cleanup
powershell.exe -Command "Remove-Item C:\Users\frank\AppData\Local\uv\cache -Recurse -Force -EA 0; Write-Host 'uv cache cleaned'"

# Git gc all repos
find /mnt/c/Users/frank -maxdepth 3 -name ".git" -type d 2>/dev/null | while read gitdir; do
  repo=$(dirname "$gitdir")
  echo "GC: $repo"
  git -C "$repo" gc --prune=now --quiet 2>/dev/null
done

# === MIGRATE ===
# WSL2 to D:/
# wsl --shutdown && wsl --export Ubuntu D:\wsl-backup\ubuntu.tar
# wsl --unregister Ubuntu
# mkdir D:\WSL\Ubuntu && wsl --import Ubuntu D:\WSL\Ubuntu D:\wsl-backup\ubuntu.tar --version 2

# === COMPACT ===
# WSL2 VHDX trim + compact
# (Inside WSL): sudo fstrim /
# (PowerShell Admin): wsl --shutdown; Optimize-VHD -Path "..." -Mode Full

# === MONITOR ===
# Check if below threshold
powershell.exe -Command "\$free = (Get-PSDrive C).Free/1GB; if(\$free -lt 10) { Write-Host \"WARNING: C:/ has only \$([math]::Round(\$free,1)) GB free!\" -ForegroundColor Red } else { Write-Host \"C:/ OK: \$([math]::Round(\$free,1)) GB free\" -ForegroundColor Green }"
```

---

## Integration Points

### With Arcanea Intelligence OS
- **Hook**: `post-session` triggers quick audit
- **Statusline**: Show C:/ free space in Arcanea status
- **AgentDB**: Store audit history in `storage_audits` table

### With Starlight Intelligence System
- **Memory Layer**: Track storage patterns over time
- **Orchestrator**: Route storage requests to appropriate Guardian
- **Sentinel Agent**: Monitor for space anomalies

### With ACOS (Agentic Creator OS)
- **Skill**: `storage-management` available via `/storage`
- **Council**: Storage Guardian Council activatable via `/storage-council`
- **Automation**: Weekly maintenance as scheduled operation

---

## Current System Profile (Feb 2026)

```
HARDWARE:
  C:/ = 476 GB SSD (OS + Apps + User)  -- CRITICAL: 6 GB FREE
  D:/ = 3,726 GB SSD (Storage)         -- HEALTHY: 3,442 GB FREE

BIGGEST CONSUMERS ON C:/:
  OneDrive (locally synced)  = 220 GB  [MIGRATE TO FILES-ON-DEMAND]
  Steam games               = 107 GB  [MOVE TO D:/]
  Epic Games                =  59 GB  [MOVE TO D:/]
  Riot Games                =  36 GB  [MOVE TO D:/]
  WSL2 Ubuntu VHDX          =  27 GB  [EXPORT TO D:/]
  Claude Desktop data       =  12 GB  [CLEAN OLD DATA]
  uv Python cache           =   7 GB  [PURGE]

ESTIMATED RECOVERABLE: 200-300 GB
```
