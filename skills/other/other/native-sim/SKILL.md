---
name: native-sim
description: Host-based simulation using the Zephyr native_sim board. Covers building for Linux/macOS/Windows, automated testing, host-side debugging (GDB, Valgrind), and host-target integration. Trigger when developing application logic without hardware or setting up CI/CD tests.
---

# Zephyr Native Simulation

Develop, test, and debug Zephyr applications with the speed and convenience of your host machine.

## Core Workflows

### 1. Simulation Basics
Understand when to use `native_sim` vs. QEMU and how to map host resources.
- **Reference**: **[simulation_basics.md](references/simulation_basics.md)**
- **Key Tools**: `west build -b native_sim`.

### 2. Host-Side Debugging
Use professional host tools to find the most elusive bugs.
- **Reference**: **[debugging.md](references/debugging.md)**
- **Key Tools**: `gdb`, `valgrind`, `gprof`, `pcap`.

### 3. Automated Testing (CI/CD)
The foundation of modern firmware development.
- **Reference**: See the `testing-debugging` skill (Phase 3) for comprehensive testing workflows.
- **Key Tools**: `twister -p native_sim`.

## Quick Start
```bash
# Build for host
west build -b native_sim samples/hello_world

# Run the app
./build/zephyr/zephyr.exe

# Debug with GDB
west debug
```

## Resources

- **[References](references/)**:
  - `simulation_basics.md`: Architectural overview and usage patterns.
  - `debugging.md`: GDB, Valgrind, and profiling guide.
