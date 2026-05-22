---
name: cleaning-wsl-docker
description: Reclaims SSD disk space consumed by WSL2/Docker. Use when user reports disk space issues, Docker build failures due to space, or slow WSL performance. Handles Docker prune, cache cleanup, VHDX compaction, and prevention setup. MUST BE USED when "disk full", "out of space", or "VHDX" mentioned.
---

# WSL2/Docker Disk Space Cleanup

## Problem

WSL2 stores all data in `ext4.vhdx` files that:
- **GROW** automatically when adding files/building Docker images
- **NEVER SHRINK** automatically when files are deleted
- `docker system prune` frees space inside WSL but NOT on Windows SSD

## Workflow

```
PHASE 1: Diagnose → PHASE 2: Cleanup → PHASE 3: Compact VHDX → PHASE 4: Prevent
```

---

## PHASE 1: Diagnose

### Check VHDX Size
```powershell
# Find VHDX files and sizes
Get-ChildItem -Path "$env:LOCALAPPDATA" -Recurse -Filter "ext4.vhdx" -ErrorAction SilentlyContinue |
  Select-Object FullName, @{N='SizeGB';E={[math]::Round($_.Length/1GB,2)}}
```

### Check Docker Usage
```bash
wsl -e bash -c "docker system df -v"
```

---

## PHASE 2: Cleanup (Inside WSL)

### Docker Cleanup
```bash
wsl -e bash -c "
  docker stop \$(docker ps -aq) 2>/dev/null
  docker container prune -f
  docker image prune -a -f
  docker builder prune -a -f
  # CAUTION: Only if volumes are disposable
  # docker volume prune -f
  docker system df
"
```

### Project Caches
```bash
wsl -e bash -c "cd /mnt/c/path/to/project && \
  rm -rf .mypy_cache .pytest_cache .ruff_cache htmlcov __pycache__ && \
  find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null"
```

### Unbounded Logs
```bash
wsl -e bash -c "rm -rf main/logs/traces/* main/logs/workflow_test* main/logs/langfuse/*"
```

---

## PHASE 3: Compact VHDX (CRITICAL - Reclaims Windows Space)

**IMPORTANT:** This phase requires Administrator privileges. The AI agent CANNOT run diskpart directly. You MUST provide manual instructions to the user.

### Step 1: Shutdown WSL (AI can run this)
```powershell
wsl --shutdown
wsl --list --running  # Should show "no running distributions"
```

### Step 2: Find VHDX Path (AI can run this)
```powershell
Get-ChildItem -Path "$env:LOCALAPPDATA" -Recurse -Filter "ext4.vhdx" -ErrorAction SilentlyContinue | Select-Object FullName
```

### Step 3: Update compact-wsl.txt Script
Edit `.claude/skills/cleaning-wsl-docker/compact-wsl.txt` with the correct VHDX path:
```
select vdisk file="C:\Users\USERNAME\AppData\Local\wsl\{GUID}\ext4.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
```

### Step 4: MANUAL USER ACTION REQUIRED
**Tell the user to run these commands in Administrator PowerShell:**

```
1. Press Win + X
2. Click "Terminal (Admin)" or "PowerShell (Admin)"
3. Click Yes on UAC prompt
4. Run:

diskpart /s "PROJECT_ROOT/.claude/skills/cleaning-wsl-docker/compact-wsl.txt"
```

**If "file in use" error:**
```cmd
wsl --shutdown
taskkill /F /IM wslservice.exe
taskkill /F /IM wsl.exe
:: Wait 10 seconds, retry diskpart
```

### Step 5: Verify (AI can run after user completes)
```powershell
Get-ChildItem -Path "$env:LOCALAPPDATA" -Recurse -Filter "ext4.vhdx" | Select-Object FullName, @{N='SizeGB';E={[math]::Round($_.Length/1GB,2)}}
```

---

## PHASE 4: Prevent Future Bloat

### Update .wslconfig
Add to `C:\Users\USERNAME\.wslconfig`:
```ini
[experimental]
sparseVhd=true           # Auto-reclaim space (WSL 2.0+)
autoMemoryReclaim=gradual
```

Then: `wsl --shutdown` to apply.

### Weekly Maintenance
```powershell
# Run in Admin PowerShell
wsl -e bash -c "docker container prune -f && docker image prune -a -f && docker builder prune -a -f"
wsl --shutdown
# Then run diskpart compact
```

---

## Expected Recovery

| Action | Recovery |
|--------|----------|
| Docker image prune | 2-10 GB |
| Docker builder prune | 10-100 GB |
| Cache cleanup | 200-500 MB |
| VHDX compaction | 5-50 GB |

---

## Checklist

- [ ] Diagnose: Check VHDX size and Docker usage
- [ ] Docker: Prune containers, images, build cache
- [ ] Caches: Remove .mypy_cache, .pytest_cache, etc.
- [ ] Logs: Clean unbounded log directories
- [ ] WSL: Shutdown completely
- [ ] VHDX: Compact using diskpart (Admin required)
- [ ] Prevent: Enable sparseVhd in .wslconfig
