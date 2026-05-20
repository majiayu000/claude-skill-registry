---
name: add-vasp
description: Configure VASP integration. Connect your HPC cluster or local VASP installation so the agent can run VASP calculations via the 213 built-in computation skills.
---

# Add VASP Integration

This skill configures VASP access for MatClaw. VASP is proprietary and cannot be bundled in the container, so we connect to your existing VASP installation — either on a remote HPC cluster (via SSH) or on the local host (via volume mount).

## Phase 1: Pre-flight

### Check if already configured

```bash
ls ~/.vasp-remote/config.json 2>/dev/null
```

If config exists, show it with `vasp-remote config` and ask the user if they want to reconfigure.

### Ask the user

Use `AskUserQuestion` to determine the setup mode:

> How is VASP available to you?
>
> 1. **Remote HPC cluster** — I have SSH access to a cluster with VASP installed (most common)
> 2. **Local installation** — VASP is installed on this machine
> 3. **I don't have VASP** — Skip this, use QE and MACE instead

If option 3, tell the user that all 213 computation skills already work without VASP (Method A: MACE for fast screening, Method B: QE for DFT accuracy). Exit.

## Phase 2: SSH Cluster Setup

### Collect cluster details

Ask the user for:

| Field | Example | Required |
|-------|---------|----------|
| SSH host | `login.hpc.example.edu` | Yes |
| SSH user | `jdoe` | Yes |
| SSH key path (on host) | `~/.ssh/id_rsa` | Yes (or use default) |
| VASP binary path on cluster | `/opt/vasp/6.4.3/bin/vasp_std` | Yes |
| POTCAR directory on cluster | `/opt/vasp/potpaw_PBE` | No (agent generates POTCAR) |
| Scratch/work directory | `/scratch/jdoe/vasp-jobs` | Yes |
| Scheduler type | `slurm` or `pbs` | Yes |
| Default queue/partition | `normal` | No |
| Default number of cores | `16` | No (default: 16) |
| Default walltime | `24:00:00` | No (default: 24:00:00) |
| Modules to load | `vasp/6.4.3 intel/2024` | No |

### Write configuration

```bash
mkdir -p ~/.vasp-remote
cat > ~/.vasp-remote/config.json << 'JSONEOF'
{
  "mode": "ssh",
  "ssh": {
    "host": "<HOST>",
    "user": "<USER>",
    "key": "<KEY_PATH>",
    "vasp_bin": "<VASP_BIN>",
    "potcar_dir": "<POTCAR_DIR>",
    "work_dir": "<WORK_DIR>",
    "scheduler": "<slurm|pbs>",
    "queue": "<QUEUE>",
    "nprocs": <NPROCS>,
    "walltime": "<WALLTIME>",
    "modules": "<MODULES>"
  }
}
JSONEOF
```

Replace all `<PLACEHOLDERS>` with the user's actual values.

### Set up SSH key for container access

The container agent needs to reach the cluster. The user's SSH key must be mounted into the container.

Check if there's a VASP-specific SSH key already, or use the default:

```bash
# Verify the key exists
ls -la <KEY_PATH>
```

Add the SSH key mount to container-runner by setting the environment variable:

```bash
# Add to .env file
echo "VASP_SSH_KEY_PATH=<KEY_PATH>" >> .env
```

Then update `src/container-runner.ts` to mount SSH keys. In the `buildVolumeMounts` function, after the Gmail credentials section, add:

```typescript
// VASP remote SSH key (for cluster access from container)
const vaspSshKey = process.env.VASP_SSH_KEY_PATH;
if (vaspSshKey && fs.existsSync(vaspSshKey)) {
  // Mount the specific key file
  mounts.push({
    hostPath: path.dirname(vaspSshKey),
    containerPath: '/home/node/.ssh',
    readonly: true,
  });
}

// VASP remote configuration
const vaspConfigDir = path.join(homeDir, '.vasp-remote');
if (fs.existsSync(vaspConfigDir)) {
  mounts.push({
    hostPath: vaspConfigDir,
    containerPath: '/home/node/.vasp-remote',
    readonly: true,
  });
}
```

### Test SSH connection

```bash
# Test from host first
ssh -i <KEY_PATH> -o BatchMode=yes -o ConnectTimeout=10 <USER>@<HOST> "echo OK && which vasp_std || ls <VASP_BIN>"
```

If this fails, troubleshoot:
- Key permissions: `chmod 600 <KEY_PATH>`
- Host key: `ssh-keyscan <HOST> >> ~/.ssh/known_hosts`
- Firewall/VPN: user may need to be on campus network

### Test from container

Rebuild and test:

```bash
npm run build
echo '{"prompt":"Run: vasp-remote config","groupFolder":"test","chatJid":"test@g.us","isMain":false,"secrets":{"ANTHROPIC_API_KEY":"...","ANTHROPIC_BASE_URL":"https://api.anthropic.com"}}' | docker run -i \
  -v ./workspace:/workspace/group \
  -v ~/.vasp-remote:/home/node/.vasp-remote:ro \
  -v ~/.ssh:/home/node/.ssh:ro \
  matclaw-agent:latest
```

## Phase 3: Local VASP Setup

### Collect local details

| Field | Example | Required |
|-------|---------|----------|
| VASP binary path | `/opt/vasp/bin/vasp_std` | Yes |
| POTCAR directory | `/opt/vasp/potpaw_PBE` | No |
| Number of cores | `4` | No (default: 4) |

### Write configuration

```bash
mkdir -p ~/.vasp-remote
cat > ~/.vasp-remote/config.json << 'JSONEOF'
{
  "mode": "local",
  "local": {
    "vasp_bin": "<VASP_BIN>",
    "potcar_dir": "<POTCAR_DIR>",
    "nprocs": <NPROCS>
  }
}
JSONEOF
```

### Set up volume mounts

Add to `src/container-runner.ts` in `buildVolumeMounts`:

```typescript
// Local VASP binary mount
const vaspBinPath = process.env.VASP_BIN_PATH;
if (vaspBinPath && fs.existsSync(vaspBinPath)) {
  mounts.push({
    hostPath: path.dirname(vaspBinPath),
    containerPath: '/opt/vasp/bin',
    readonly: true,
  });
}

// Local VASP POTCAR library mount
const vaspPpPath = process.env.VASP_PP_PATH;
if (vaspPpPath && fs.existsSync(vaspPpPath)) {
  mounts.push({
    hostPath: vaspPpPath,
    containerPath: '/opt/vasp/pp',
    readonly: true,
  });
}
```

Add to `.env`:

```bash
VASP_BIN_PATH=/opt/vasp/bin/vasp_std
VASP_PP_PATH=/opt/vasp/potpaw_PBE
```

### Test

```bash
vasp_std --version  # or just check it exists
```

## Phase 4: Rebuild Container

The container needs `openssh-client` for SSH mode and the `vasp-remote` script:

```bash
./container/build.sh
```

## Phase 5: Verify

Ask the user to test with a simple calculation:

> VASP is now configured! Try asking me to calculate something, for example:
> "Relax the structure of Si using VASP"
>
> The agent will:
> 1. Generate INCAR, POSCAR, KPOINTS, POTCAR
> 2. Run `vasp-remote run` to execute on your cluster
> 3. Parse vasprun.xml and return the results

## How It Works

```
Agent (in container)
  ├─ Reads skill → generates VASP input files
  ├─ Runs: vasp-remote run
  │   ├─ SSH mode: scp files → sbatch → poll → fetch results
  │   └─ Local mode: mpirun vasp_std
  └─ Parses vasprun.xml with pymatgen → returns results
```

The `vasp-remote` script is at `/usr/local/bin/vasp-remote` inside the container. It reads config from `~/.vasp-remote/config.json` (mounted from host).

All 213 computation skills with VASP methods work automatically — they generate input files and the agent calls `vasp-remote run` instead of `vasp_std` directly.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `Config not found` | Not configured | Run `/add-vasp` |
| `SSH connection refused` | Network/firewall | Check VPN, try `ssh -v` from host |
| `Permission denied (publickey)` | Wrong key or permissions | `chmod 600 ~/.ssh/id_rsa` |
| `vasp_std: not found` | Wrong binary path | Check `ssh user@host "which vasp_std"` |
| `sbatch: command not found` | Wrong scheduler type | Try `pbs` instead of `slurm` |
| Job stuck in PENDING | Queue full | Try different queue: `vasp-remote run --queue express` |
| Dynamic library errors (local) | Container lib mismatch | Use SSH mode instead |

## Removal

```bash
rm -rf ~/.vasp-remote
# Remove VASP_* lines from .env
# Remove VASP mount sections from src/container-runner.ts
```
