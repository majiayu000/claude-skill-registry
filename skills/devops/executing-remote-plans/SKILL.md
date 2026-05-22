---
name: executing-remote-plans
description: |
  Distributed HEC-RAS execution across remote workers (PsExec, Docker, SSH, cloud).
  Handles worker initialization, queue scheduling, and result aggregation. Use when
  setting up remote execution, distributed computation, cloud workflows, scaling
  HEC-RAS across machines, parallel processing on multiple computers, Windows remote
  execution, container-based execution, session-based remote execution, PsExec
  configuration, Docker worker setup, or multi-machine HEC-RAS workflows.
  Triggers: remote execution, distributed execution, PsExec, Docker worker, SSH execution, cloud execution, parallel remote, multi-machine, session_id, remote worker, worker initialization, queue scheduling, network share, container execution.
---

# Executing Remote Plans

Execute HEC-RAS plans across multiple remote machines using distributed workers.

> **PRIMARY SOURCES**: This skill is a lightweight navigator. For complete details, see:
> - `ras_commander/remote/AGENTS.md` - Coding conventions, architecture
> - `.claude/rules/hec-ras/remote.md` - Machine setup (Group Policy, Registry, session_id)
> - `examples/500_remote_execution_psexec.ipynb` - Complete PsExec workflow

## Quick Start

```python
from ras_commander import init_ras_project, init_ras_worker, compute_parallel_remote

# Initialize project
init_ras_project("/path/to/project", "6.6")

# Create PsExec worker (Windows remote)
worker = init_ras_worker(
    "psexec",
    hostname="192.168.1.100",
    share_path=r"\\192.168.1.100\RasRemote",
    session_id=2,  # CRITICAL: Query with "query session /server:hostname"
    cores_total=16,
    cores_per_plan=4
)

# Execute plans remotely
results = compute_parallel_remote(
    plan_numbers=["01", "02", "03"],
    workers=[worker],
    num_cores=4
)

# Check results
for plan_num, result in results.items():
    if result.success:
        print(f"Plan {plan_num}: SUCCESS ({result.execution_time:.1f}s)")
        print(f"  HDF: {result.hdf_path}")
    else:
        print(f"Plan {plan_num}: FAILED - {result.error_message}")
```

## CRITICAL: Session-Based Execution

**HEC-RAS is a GUI application** and REQUIRES session-based execution:

```python
worker = init_ras_worker(
    "psexec",
    hostname="192.168.1.100",
    share_path=r"\\192.168.1.100\RasRemote",
    session_id=2,  # CRITICAL: NOT system account
    ...
)
```

**NEVER use `system_account=True`** - HEC-RAS will hang without desktop session.

### Determining Session ID

**Query from controlling machine**:
```bash
query session /server:192.168.1.100

# Output:
# SESSIONNAME       USERNAME        ID  STATE
# console           Administrator    2  Active
#                                    ^
#                            Use this value
```

**Typical Values**:
- Session 0: SYSTEM (services only, NO DESKTOP)
- Session 1: Sometimes system (varies by Windows version)
- **Session 2**: Typical interactive user (MOST COMMON)
- Session 3+: Additional RDP sessions

See `ras_commander/remote/AGENTS.md` lines 97-101 for critical implementation notes.

## Worker Types

### Local Worker
Parallel execution on local machine:
```python
worker = init_ras_worker(
    "local",
    worker_folder="C:/RasRemote",
    cores_total=8,
    cores_per_plan=2
)
```

### PsExec Worker
Windows remote via network share:
```python
worker = init_ras_worker(
    "psexec",
    hostname="192.168.1.100",
    share_path=r"\\192.168.1.100\RasRemote",  # UNC path from controlling machine
    worker_folder=r"C:\RasRemote",             # Local path on remote machine
    session_id=2,                              # CRITICAL: Query with "query session"
    cores_total=16,
    cores_per_plan=4
)
```

**Setup Requirements** (see `REMOTE_WORKER_SETUP_GUIDE.md`):
1. Network share created (`C:\RasRemote` shared as `\\hostname\RasRemote`)
2. Group Policy configuration (network access, local logon, batch job rights)
3. Registry key: `LocalAccountTokenFilterPolicy=1`
4. Remote Registry service running
5. User in Administrators group

### Docker Worker
Container execution (local or remote):
```python
# Local Docker
worker = init_ras_worker(
    "docker",
    docker_image="hecras:6.6",
    cores_total=8,
    cores_per_plan=4,
    preprocess_on_host=True  # Windows preprocessing, Linux execution
)

# Remote Docker via SSH
worker = init_ras_worker(
    "docker",
    docker_image="hecras:6.6",
    docker_host="ssh://user@192.168.1.100",
    ssh_key_path="~/.ssh/docker_worker",
    share_path=r"\\192.168.1.100\DockerShare",
    remote_staging_path=r"C:\DockerShare",
    cores_total=8,
    cores_per_plan=4
)
```

**Docker Prerequisites**:
- Docker Desktop installed (local) or Docker daemon on remote
- Python packages: `pip install docker paramiko`
- HEC-RAS Docker image built (see `ras-commander-cloud` repo)
- SSH key configured for remote execution

## Distributed Execution

```python
results = compute_parallel_remote(
    plan_numbers=["01", "02", "03"],  # Plans to execute
    workers=[worker1, worker2],        # List of initialized workers
    num_cores=4,                       # Cores per plan execution
    clear_geompre=False,               # Clear geometry preprocessor files
    max_concurrent=None,               # Max simultaneous executions (default: all slots)
    autoclean=True                     # Delete temp folders after execution
)
```

**Returns**: `Dict[str, ExecutionResult]`
- `plan_number` - Plan that was executed
- `worker_id` - Worker that executed the plan
- `success` - True if successful
- `hdf_path` - Path to output HDF file
- `error_message` - Error message if failed
- `execution_time` - Execution time in seconds

## Queue-Aware Scheduling

Workers execute in priority order (lower `queue_priority` first):

```python
# Local workers execute first (priority 0)
local = init_ras_worker("local", queue_priority=0, cores_total=8, cores_per_plan=2)

# Remote workers used when local full (priority 1)
remote = init_ras_worker("psexec", hostname="...", queue_priority=1, ...)

# Cloud workers for overflow (priority 2)
cloud = init_ras_worker("docker", docker_host="...", queue_priority=2, ...)

# Plans fill local slots first, then remote, then cloud
results = compute_parallel_remote(
    plan_numbers=["01", "02", "03", "04", "05", "06"],
    workers=[local, remote, cloud]
)
```

**Worker Slots**: Workers with `max_parallel_plans > 1` create multiple slots:
- Worker with `cores_total=16` and `cores_per_plan=4` → 4 parallel slots
- Each slot can run one plan at a time
- Total slots = sum of all worker `max_parallel_plans`

## Mixed Worker Pools

Combine local, remote, and cloud workers:

```python
# Local worker (priority 0)
local = init_ras_worker(
    "local",
    worker_folder="C:/RasRemote",
    cores_total=8,
    cores_per_plan=2,
    queue_priority=0
)

# Remote PsExec worker (priority 1)
remote = init_ras_worker(
    "psexec",
    hostname="192.168.1.100",
    share_path=r"\\192.168.1.100\RasRemote",
    session_id=2,
    cores_total=16,
    cores_per_plan=4,
    queue_priority=1
)

# Docker worker (priority 2)
docker = init_ras_worker(
    "docker",
    docker_image="hecras:6.6",
    docker_host="ssh://user@192.168.1.200",
    ssh_key_path="~/.ssh/docker",
    cores_total=8,
    cores_per_plan=4,
    queue_priority=2
)

# Execute with queue-aware scheduling
results = compute_parallel_remote(
    plan_numbers=["01", "02", "03", "04", "05", "06", "07", "08"],
    workers=[local, remote, docker]
)
```

## Result Processing

```python
results = compute_parallel_remote(plan_numbers=["01", "02"], workers=[worker])

for plan_num, result in results.items():
    print(f"\nPlan {plan_num}:")
    print(f"  Worker: {result.worker_id}")
    print(f"  Success: {result.success}")
    print(f"  Time: {result.execution_time:.1f}s")

    if result.success:
        print(f"  HDF: {result.hdf_path}")

        # Verify HDF
        from ras_commander import HdfResultsPlan
        msgs = HdfResultsPlan.get_compute_messages(result.hdf_path)
        if "completed successfully" in msgs.lower():
            print(f"  Status: Verified successful")
    else:
        print(f"  Error: {result.error_message}")
```

## Common Issues

### PsExec Worker Hangs

**Symptom**: No error, HDF not created

**Diagnosis**:
```bash
# Check session ID
query session /server:192.168.1.100

# Verify user is Administrator
net localgroup Administrators

# Check Remote Registry service
sc query RemoteRegistry
```

**Fix**: Ensure `session_id=2` (or correct session) and all configuration requirements met.

See `REMOTE_WORKER_SETUP_GUIDE.md` for complete setup instructions.

### Permission Denied

**Symptom**: "Access is denied"

**Fix**: Check:
1. Registry key: `LocalAccountTokenFilterPolicy=1`
2. Group Policy settings (network access, local logon, batch job)
3. Share permissions (Share + NTFS)

### Network Path Not Found

**Symptom**: Cannot access `\\hostname\share`

**Diagnosis**:
```bash
# Test from controlling machine
dir \\192.168.1.100\RasRemote

# Check firewall (port 445 SMB)
Test-NetConnection -ComputerName 192.168.1.100 -Port 445

# Verify Remote Registry running
sc \\192.168.1.100 query RemoteRegistry
```

### Docker Connection Failed

**Symptom**: Cannot connect to Docker daemon

**Diagnosis**:
```bash
# Test Docker locally
docker ps

# Test remote Docker via SSH
ssh user@192.168.1.100 "docker info"
```

**Fix**: Ensure Docker Desktop running (local) or SSH keys configured (remote)

## Architecture Overview

### Module Structure
See `ras_commander/remote/AGENTS.md` for complete module structure and coding conventions.

```
ras_commander/remote/
├── __init__.py         # Exports all public classes and functions
├── RasWorker.py        # RasWorker base dataclass + init_ras_worker()
├── PsexecWorker.py     # PsexecWorker (IMPLEMENTED)
├── LocalWorker.py      # LocalWorker (IMPLEMENTED)
├── DockerWorker.py     # DockerWorker (IMPLEMENTED, requires docker+paramiko)
├── SshWorker.py        # SshWorker (stub, requires paramiko)
├── WinrmWorker.py      # WinrmWorker (stub, requires pywinrm)
├── SlurmWorker.py      # SlurmWorker (stub)
├── AwsEc2Worker.py     # AwsEc2Worker (stub, requires boto3)
├── AzureFrWorker.py    # AzureFrWorker (stub, requires azure-*)
├── Execution.py        # compute_parallel_remote() + helpers
└── Utils.py            # Shared utilities
```

### Factory Pattern
```python
# Top-level factory function (recommended)
worker = init_ras_worker(worker_type, **config)

# Lazy imports and routing to worker-specific functions
# See RasWorker.py lines 84-92 for implementation
```

### Lazy Loading
Workers with optional dependencies implement `check_*_dependencies()`:
- Docker: `pip install docker paramiko`
- SSH: `pip install paramiko`
- AWS: `pip install boto3`

See `ras_commander/remote/AGENTS.md` lines 58-68 for lazy loading pattern.

## Primary Sources

1. **`ras_commander/remote/AGENTS.md`** (156 lines)
   - Module structure and naming conventions
   - Import patterns and coding standards
   - Critical implementation notes (session_id, UNC paths, etc.)
   - Worker implementation pattern
   - Adding new workers

2. **`examples/500_remote_execution_psexec.ipynb`**
   - Complete PsExec workflow
   - Session ID determination
   - Network share setup
   - Error handling and debugging

3. **`.claude/rules/hec-ras/remote.md`**
   - Critical configuration requirements
   - Group Policy configuration
   - Registry key setup
   - Troubleshooting common issues
   - Session ID determination

## See Also

- **Skill**: `executing-plans` - Local plan execution
- **Skill**: `processing-hdf-results` - Results analysis
- **CLAUDE.md**: Remote Execution Subpackage section
- **Documentation**: ras-commander.readthedocs.io (remote execution)
