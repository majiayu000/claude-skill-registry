---
name: remote-exec
description: "Execute commands on remote machines via SSH. Handles git sync, file transfer, and long-running jobs. Use when user says 'run on homelab', 'sync and run', 'process on macmini', or 'tmux job'."
allowed-tools: Bash, Read, Glob
---

# Remote Exec

You are an expert at executing commands across a multi-machine Tailscale network using the brain/body architecture.

## When To Use

- User says "run this on [machine]" or "execute on [machine]"
- User says "sync and run" (git push/pull + execute)
- User says "process files on macmini" (data transfer workflow)
- User says "start long job on [machine]" (tmux workflow)
- User needs GPU processing (macmini)
- User needs Docker/services (homelab)

## Architecture: Brain/Body Model

| Role | Machine | Purpose |
|------|---------|---------|
| Brain | oci-dev | Claude Code runs here (cheap compute) |
| Body | homelab | Data storage, Docker services, main data drive |
| Muscle | macmini | GPU, Whisper, video processing |

## Machine Registry

| Machine | Hostname | User | Purpose |
|---------|----------|------|---------|
| oci-dev | oci-dev.deer-panga.ts.net | ubuntu | Claude Code, OCI resources |
| homelab | homelab.deer-panga.ts.net | khamel83 | Data storage, Docker |
| macmini | omars-mac-mini.deer-panga.ts.net | macmini | GPU, transcription |
| macbook-air | omars-macbook-air.deer-panga.ts.net | khamel83 | Local development |

### Resource Breakdown

**oci-dev** (Brain)
- Repos: ~/github
- Compute: 4 ARM cores, 24GB RAM, 193GB disk
- Object Storage: khamel-storage (20GB free)
- Autonomous DB: khameldb (20GB Oracle free)
- Purpose: Claude Code execution, lightweight APIs, OCI resources

**homelab** (Body)
- Repos: ~/github
- Data: /mnt/main-drive (26TB MergerFS pool)
- Docker: 53+ services
- Purpose: Data storage, media, Docker services

**macmini** (Muscle)
- Repos: ~/github
- GPU: Apple Silicon
- Whisper: Local transcription
- Purpose: GPU processing, video, transcription

**macbook-air** (Mobile)
- Repos: ~/github
- Purpose: Local development, testing

## SSH Config (Required)

Each machine must have SSH aliases configured. Use the installer:

```bash
# Quick install - fetches latest config from oneshot repo
curl -fsSL https://raw.githubusercontent.com/Khamel83/oneshot/master/ssh/install.sh | bash
```

The installer:
- Adds/updates managed SSH aliases (oci, homelab, macmini, etc.)
- Detects conflicts with existing manual entries
- Backs up your config before making changes
- Supports both LAN and Tailscale IPs (use `-ts` suffix for Tailscale)

**Manual config** (if installer fails, add this to `~/.ssh/config`):
```bash
Host homelab
    HostName 100.112.130.100
    User khamel83
    IdentityFile ~/.ssh/id_ed25519

Host macmini
    HostName 100.113.216.27
    User macmini
    IdentityFile ~/.ssh/id_ed25519

Host oci-dev
    HostName 100.126.13.70
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
```

## Prerequisites Check

```bash
echo "=== Testing SSH Connectivity (via aliases) ==="
ssh -o BatchMode=yes -o ConnectTimeout=5 oci-dev "echo 'oci-dev: OK'" 2>/dev/null || echo "oci-dev: FAILED"
ssh -o BatchMode=yes -o ConnectTimeout=5 homelab "echo 'homelab: OK'" 2>/dev/null || echo "homelab: FAILED"
ssh -o BatchMode=yes -o ConnectTimeout=5 macmini "echo 'macmini: OK'" 2>/dev/null || echo "macmini: FAILED"
echo "=== Tailscale Status ==="
tailscale status 2>/dev/null | head -10 || echo "Tailscale not installed locally"
```

## Detect Current Machine

```bash
LOCAL_HOST=$(hostname)
case "$LOCAL_HOST" in
  homelab*) CURRENT_MACHINE="homelab" ;;
  oci-dev*|instance*) CURRENT_MACHINE="oci-dev" ;;
  omars-mac-mini*|macmini*) CURRENT_MACHINE="macmini" ;;
  omars-macbook-air*) CURRENT_MACHINE="macbook-air" ;;
  *) CURRENT_MACHINE="unknown" ;;
esac
echo "Current machine: $CURRENT_MACHINE"
```

## Workflow A: Sync and Run

Push code via git, pull on target, execute command, stream output.

### Variables

| Input | Description | Example |
|-------|-------------|---------|
| TARGET | Machine name | homelab |
| REPO | Repository name | atlas |
| BRANCH | Git branch | main |
| COMMAND | Command to run | python scripts/index.py |

### Script

```bash
# Variables - set these
TARGET="homelab"
REPO="my-project"
BRANCH="main"
COMMAND="python scripts/process.py"

# Machine lookup
case "$TARGET" in
  oci-dev) USER="ubuntu"; HOST="oci-dev.deer-panga.ts.net"; REPO_BASE="~/github" ;;
  homelab) USER="khamel83"; HOST="homelab.deer-panga.ts.net"; REPO_BASE="~/github" ;;
  macmini) USER="macmini"; HOST="omars-mac-mini.deer-panga.ts.net"; REPO_BASE="~/github" ;;
  macbook-air) USER="khamel83"; HOST="omars-macbook-air.deer-panga.ts.net"; REPO_BASE="~/github" ;;
  *) echo "Unknown target: $TARGET"; exit 1 ;;
esac

# Step 1: Push local changes
echo "=== Pushing to origin/$BRANCH ==="
git push origin "$BRANCH"

# Step 2: Pull and execute on remote
echo "=== Executing on $TARGET ==="
ssh -o BatchMode=yes -o ConnectTimeout=10 "$USER@$HOST" << REMOTE
  set -e
  cd "$REPO_BASE/$REPO"

  # Stash if dirty
  if [ -n "\$(git status --porcelain)" ]; then
    echo "Stashing uncommitted changes..."
    git stash push -m "remote-exec auto-stash \$(date +%Y%m%d-%H%M%S)"
    STASHED=true
  fi

  # Pull latest
  echo "Pulling from origin/$BRANCH..."
  if ! git pull --ff-only origin "$BRANCH" 2>&1; then
    echo "ERROR: Cannot fast-forward. Remote has diverged."
    exit 1
  fi

  # Execute
  echo "=== Running: $COMMAND ==="
  $COMMAND

  # Restore stash
  if [ "\$STASHED" = true ]; then
    git stash pop || echo "WARNING: Stash conflict"
  fi
REMOTE
```

## Workflow B: Process on Remote (Data Transfer)

Transfer files to target machine, process, transfer results back.

### Variables

| Input | Description | Example |
|-------|-------------|---------|
| SOURCE_MACHINE | Where files are | homelab |
| TARGET_MACHINE | Where to process | macmini |
| SOURCE_PATH | Path to files | /mnt/main-drive/videos/raw/*.mp4 |
| TARGET_TEMP | Temp dir on target | ~/data/processing |
| PROCESSOR | Script to run | whisper-transcribe.py |
| RESULT_PATH | Where to put results | /mnt/main-drive/videos/transcribed |

### Script

```bash
# Variables - set these
SOURCE_USER="khamel83"
SOURCE_HOST="homelab.deer-panga.ts.net"
SOURCE_PATH="/mnt/main-drive/videos/raw"

TARGET_USER="macmini"
TARGET_HOST="omars-mac-mini.deer-panga.ts.net"
TARGET_TEMP="~/data/processing"

PROCESSOR="python ~/github/atlas/scripts/transcribe.py"
RESULT_PATH="/mnt/main-drive/videos/transcribed"

# Step 1: Transfer files to target
echo "=== Transferring files to $TARGET_HOST ==="
ssh "$TARGET_USER@$TARGET_HOST" "mkdir -p $TARGET_TEMP"
rsync -avz --progress \
  "$SOURCE_USER@$SOURCE_HOST:$SOURCE_PATH/" \
  "$TARGET_USER@$TARGET_HOST:$TARGET_TEMP/"

# Step 2: Process on target
echo "=== Processing on $TARGET_HOST ==="
ssh "$TARGET_USER@$TARGET_HOST" << REMOTE
  cd $TARGET_TEMP
  $PROCESSOR
REMOTE

# Step 3: Transfer results back
echo "=== Transferring results to $SOURCE_HOST ==="
ssh "$SOURCE_USER@$SOURCE_HOST" "mkdir -p $RESULT_PATH"
rsync -avz --progress \
  "$TARGET_USER@$TARGET_HOST:$TARGET_TEMP/output/" \
  "$SOURCE_USER@$SOURCE_HOST:$RESULT_PATH/"

echo "=== Done! Results at $RESULT_PATH ==="
```

## Workflow C: Long-Running Job (tmux)

Start command in tmux session on target, return monitoring instructions.

### Variables

| Input | Description | Example |
|-------|-------------|---------|
| TARGET | Machine name | homelab |
| JOB_NAME | Short description | docker-rebuild |
| COMMAND | Long-running command | docker compose up --build |
| WORKING_DIR | Directory to run in | ~/github/homelab |

### Script

```bash
# Variables - set these
TARGET="homelab"
JOB_NAME="index-rebuild"
COMMAND="python scripts/full_index.py"
WORKING_DIR="~/github/atlas"

# Machine lookup
case "$TARGET" in
  homelab) USER="khamel83"; HOST="homelab.deer-panga.ts.net" ;;
  macmini) USER="macmini"; HOST="omars-mac-mini.deer-panga.ts.net" ;;
  oci-dev) USER="ubuntu"; HOST="oci-dev.deer-panga.ts.net" ;;
  *) echo "Unknown target: $TARGET"; exit 1 ;;
esac

# Session naming: remote-exec-{machine}-{timestamp}-{job}
TIMESTAMP=$(date +%Y%m%d-%H%M)
SESSION="remote-exec-${TARGET}-${TIMESTAMP}-${JOB_NAME}"

# Start tmux session
echo "=== Starting tmux session: $SESSION ==="
ssh "$USER@$HOST" "tmux new-session -d -s '$SESSION' -c '$WORKING_DIR' '$COMMAND; echo \"=== DONE ===\"; read'"

echo ""
echo "=== Job started ==="
echo "Session: $SESSION"
echo ""
echo "Monitor commands:"
echo "  Attach:  ssh $USER@$HOST \"tmux attach -t $SESSION\""
echo "  List:    ssh $USER@$HOST \"tmux ls\""
echo "  Kill:    ssh $USER@$HOST \"tmux kill-session -t $SESSION\""
echo "  Logs:    ssh $USER@$HOST \"tmux capture-pane -t $SESSION -p\""
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| SSH timeout | Tailscale down | Run `tailscale status`, restart if needed |
| Permission denied | Wrong user/key | Check SSH key, verify user in machine table |
| Git conflict | Diverged branches | Pull with rebase, manual merge on remote |
| Command not found | Missing dep | SSH and install: `ssh user@host "apt install pkg"` |
| Disk full | No space | Check with `ssh user@host "df -h"` |
| tmux not found | Not installed | `apt install tmux` (Linux) / `brew install tmux` (Mac) |

## Common Commands

```bash
# Check services on homelab
ssh khamel83@homelab.deer-panga.ts.net "docker ps"

# View logs on homelab
ssh khamel83@homelab.deer-panga.ts.net "docker logs -f service-name"

# Check GPU on macmini
ssh macmini@omars-mac-mini.deer-panga.ts.net "nvidia-smi" 2>/dev/null || echo "No NVIDIA GPU"

# Disk space on all machines
for m in "ubuntu@oci-dev.deer-panga.ts.net" "khamel83@homelab.deer-panga.ts.net" "macmini@omars-mac-mini.deer-panga.ts.net"; do
  echo "=== $m ===" && ssh -o ConnectTimeout=5 "$m" "df -h /" 2>/dev/null || echo "Unreachable"
done
```

## Anti-Patterns

- Running interactive commands without tmux (use Workflow C)
- Transferring large files without compression (`rsync -z`)
- Not checking remote disk space before rsync
- Hardcoding paths instead of using variables
- Running on wrong machine (always verify TARGET matches intent)
- Forgetting that oci-dev is disposable (don't store unique data there)
- Syncing gitignored data via git (use rsync for data transfers)

## Keywords

remote, ssh, execute, macmini, homelab, oci-dev, sync and run, rsync, tmux, run on, process on, long job, tailscale, brain body
