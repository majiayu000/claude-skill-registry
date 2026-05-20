---
name: linux-cgroups
cluster: linux
description: "cgroups v2: memory limits per OpenClaw instance, CPU quotas, OOM protection, systemd slices"
tags: ["cgroups","memory","limits","linux","performance"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "cgroups memory limits cpu quota oom linux resource control slice"
---

# linux-cgroups

## Purpose
This skill enables precise resource management for OpenClaw instances using Linux cgroups v2, focusing on memory limits, CPU quotas, OOM (Out-Of-Memory) protection, and systemd slices to prevent resource exhaustion and optimize performance on multi-process systems.

## When to Use
Use this skill when running multiple OpenClaw instances on a Linux server to isolate resources, enforce limits on high-demand tasks, or protect against OOM kills in production environments. Apply it in scenarios with shared hosts, like containers or virtualized setups, to ensure fair CPU and memory allocation.

## Key Capabilities
- Set memory limits to cap usage per OpenClaw instance, e.g., via `memory.max` to prevent swapping.
- Enforce CPU quotas using `cpu.max` for bandwidth control, limiting CPU time slices.
- Enable OOM protection with `memory.oom.group` to prioritize processes and avoid abrupt terminations.
- Manage systemd slices for hierarchical resource grouping, allowing nested cgroups for complex setups.

## Usage Patterns
To apply cgroups, create a cgroup hierarchy, set limits, and assign processes. Always run as root or with sufficient privileges. For OpenClaw, wrap instance launches in cgroup contexts to enforce per-instance limits. Example: Create a slice for OpenClaw, then assign processes to it. Use Bash scripts for automation, checking cgroup paths under `/sys/fs/cgroup/` for v2.

## Common Commands/API
Interact with cgroups via CLI tools or directly via filesystem. No API keys needed; use system-level access.
- **CLI Commands**:
  - Create a cgroup: `sudo cgcreate -g memory,cpu:/openclaw_slice`
  - Set memory limit: `sudo cgset -r memory.max=512M /openclaw_slice` (limits to 512 MB)
  - Set CPU quota: `sudo cgset -r cpu.max=100000 50000 /openclaw_slice` (limits to 1 CPU core at 50% usage)
  - Execute process in cgroup: `sudo cgexec -g memory,cpu:/openclaw_slice openclaw --run task`
- **Code Snippets** (in Bash or Python):
  ```bash
  # Bash example to set and apply memory limit
  sudo cgcreate -g memory:/openclaw
  sudo cgset -r memory.max=1G /openclaw
  sudo cgexec -g memory:/openclaw openclaw --instance id1
  ```
  ```python
  # Python snippet using subprocess (requires root)
  import subprocess
  subprocess.run(['cgcreate', '-g', 'memory:/openclaw'])
  subprocess.run(['cgset', '-r', 'memory.max=1G', '/openclaw'])
  subprocess.run(['cgexec', '-g', 'memory:/openclaw', 'openclaw', '--instance', 'id1'])
  ```
- **Config Formats**: Edit cgroup files directly, e.g., echo values to `/sys/fs/cgroup/your_slice/memory.max`. For systemd, define slices in `.slice` files under `/etc/systemd/system/`, like `[Slice]\nMemoryMax=512M`.

## Integration Notes
Integrate with OpenClaw by wrapping commands in cgroup execution, e.g., modify startup scripts to include `cgexec`. Ensure the host uses cgroups v2 (check with `stat /sys/fs/cgroup/unified`); if v1, migrate via `systemctl`. For multi-instance setups, use environment variables like `OPENCLAW_CGROUP_PATH=/openclaw_slice` to pass cgroup details. Monitor usage with `systemd-cgtop` or `cat /sys/fs/cgroup/your_slice/memory.current`.

## Error Handling
Common errors include permission denials (fix with `sudo`), invalid cgroup paths (verify with `ls /sys/fs/cgroup/`), or OOM events (check logs with `dmesg | grep -i oom`). Handle by:
- Checking return codes in scripts: `if [ $? -ne 0 ]; then echo "Cgroup creation failed"; fi`
- Monitoring memory pressure: Use `cat /sys/fs/cgroup/your_slice/memory.oom_control` and alert if OOM is triggered.
- Debugging: Run `systemctl status your_slice` for systemd slices; parse errors in code like:
  ```python
  try:
      subprocess.run(['cgset', '-r', 'memory.max=1G', '/openclaw'], check=True)
  except subprocess.CalledProcessError as e:
      print(f"Error: {e.returncode} - {e.output}")
  ```

## Concrete Usage Examples
1. **Limit memory for a single OpenClaw instance**: Create a cgroup slice, set a 2GB memory cap, and run the instance. Command sequence: `sudo cgcreate -g memory:/openclaw_inst1; sudo cgset -r memory.max=2G /openclaw_inst1; sudo cgexec -g memory:/openclaw_inst1 openclaw --instance inst1 --task process_data`. This prevents the instance from exceeding 2GB, avoiding OOM for other processes.
2. **Apply CPU quota to multiple instances**: Set a CPU limit for a group of OpenClaw tasks. Example: `sudo cgcreate -g cpu:/openclaw_group; sudo cgset -r cpu.max=200000 100000 /openclaw_group; sudo cgexec -g cpu:/openclaw_group openclaw --instance inst2 --task compute_loop`. This enforces a quota of 2 CPU cores at 50% each, ensuring balanced performance across instances.

## Graph Relationships
- Related to: linux (cluster), as it builds on core Linux resource management.
- Connected via tags: cgroups (direct), memory (capability), limits (feature), performance (outcome).
- Links to other skills: cpu-management (for deeper CPU controls), oom-handler (for advanced OOM strategies).
