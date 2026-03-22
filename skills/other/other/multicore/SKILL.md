---
name: multicore
description: Developing for multicore systems in Zephyr RTOS. Covers Symmetric Multiprocessing (SMP), Asymmetric Multiprocessing (AMP) with OpenAMP/RPMsg, inter-processor communication (IPC) patterns, and Linkable Extensions (LLEXT). Trigger when designing for SoCs with multiple homogeneous or heterogeneous cores.
---

# Zephyr Multicore Development

Leverage multiple CPU cores to increase performance, isolate critical tasks, and integrate heterogeneous systems.

## Core Workflows

### 1. SMP Configuration
Run the Zephyr kernel and your threads across multiple identical cores.
- **Reference**: **[smp_configuration.md](references/smp_configuration.md)**
- **Key Tools**: `CONFIG_SMP`, `k_spinlock`, Thread Affinity.

### 2. OpenAMP & RPMsg
Communicate between heterogeneous cores (e.g., A-series and M-series) using standard protocols.
- **Reference**: **[openamp_rpmsg.md](references/openamp_rpmsg.md)**
- **Key Tools**: `CONFIG_OPENAMP`, message vrings, Resource Tables.

### 3. IPC Patterns
Implement efficient data exchange between cores using high-level services or low-level mailboxes.
- **Reference**: **[ipc_patterns.md](references/ipc_patterns.md)**
- **Key Tools**: `IPC Service`, IPM drivers, Shared Memory.

### 4. LLEXT (Linkable Extensions)
Dynamically load and run binary modules at runtime without a full firmware update.
- **Reference**: **[llext_basics.md](references/llext_basics.md)**
- **Key Tools**: `CONFIG_LLEXT`, dynamic ELF loading, Symbol Export.

## Quick Start (SMP prj.conf)
```kconfig
# Enable SMP for dual-core SoCs
CONFIG_SMP=y
CONFIG_MP_NUM_CPUS=2
```
```c
// Using spinlocks for cross-core sync
struct k_spinlock lock;
k_spinlock_key_t key = k_spin_lock(&lock);
// ... critical section ...
k_spin_unlock(&lock, key);
```

## Professional Patterns (Architecture Design)
- **Linux Bridging**: Use OpenAMP/RPMsg to bridge Zephyr real-time logic with a Linux application controller.
- **Core Isolation**: Pin high-frequency interrupts (e.g., motor control) to Core 1 and keep the main application on Core 0 to prevent jitter.
- **Zero-Copy Transfers**: Use shared memory regions for large data (video/audio) and only pass meta-data via IPC channels to minimize overhead.

## Automation Tools
- **[smp_config_check.py](scripts/smp_config_check.py)**: Validate SMP-related Kconfig consistency in `prj.conf`.

## Examples & Templates
- **[rpmsg_channel_contract.md](assets/rpmsg_channel_contract.md)**: Starter channel contract for RPMsg endpoint design.

## Validation Checklist
- [ ] SMP builds run with expected CPU count and no cross-core race regressions.
- [ ] OpenAMP/RPMsg endpoint exchange passes bidirectional message tests.
- [ ] IPC latency and throughput remain within target budget under load.
- [ ] LLEXT module load/unload path resolves symbols and handles failure cases safely.

## Resources

- **[References](references/)**:
  - `smp_configuration.md`: Configuration and spinlocks.
  - `openamp_rpmsg.md`: AMP and Linux interoperability.
  - `ipc_patterns.md`: Mailboxes and high-level IPC services.
  - `llext_basics.md`: Dynamic code loading.
- **[Scripts](scripts/)**:
  - `smp_config_check.py`: SMP config consistency checker.
- **[Assets](assets/)**:
  - `rpmsg_channel_contract.md`: RPMsg interface contract template.
