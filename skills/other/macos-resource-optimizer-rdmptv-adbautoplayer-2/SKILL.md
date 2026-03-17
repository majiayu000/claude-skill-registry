---
name: macos-resource-optimizer
description: macOS system resource optimization with 40 specialized agents for memory, disk, CPU, and process management
version: 2.1.0
scripts_enabled: true
last_updated: 2025-11-30
updated_in_phase: 2.2
improvements: Performance metrics corrected, UV script architecture documented, protected apps expanded
auto_trigger_keywords:
  - macos
  - memory
  - optimizer
  - performance
  - ram
  - disk
  - cleanup
  - resource
scripts:
  - name: coordinator
    path: scripts/coordinator.py
    description: Main orchestrator spawning 40 agents concurrently across 6 phases
color: blue
---

# macOS Resource Optimizer

Production-ready system optimization with 40+ specialized agents for comprehensive macOS resource management.

## Quick Reference

**What is macOS Resource Optimizer?**
Real-world macOS optimization framework with 40+ specialized agents executing in parallel:
- **coordinator.py**: 40-agent orchestrator (6 phases, 4-5s execution)
- **40+ specialized agents**: Memory, disk, browser, Docker, developer tools
- **Implementation**: UV scripts (PEP 723) + Bash delegation via MoAI agents

**Main Orchestrator**:

| Script | Purpose | Agents | Execution Time |
|--------|---------|--------|----------------|
| `coordinator.py` | 40-agent parallel orchestrator | 40 agents (6 phases) | 4-5s |

**6 Phases (coordinator.py)**:
1. **Disk Cleanup** (15 agents): Python/Node zombies, Browser helpers, Network leaks, Docker containers
2. **RAM Optimization** (9 agents): Memory pressure, App profiler, Browser tabs, Electron apps
3. **Developer Cache** (5 agents): Time Machine, Xcode, Build caches, Docker cleanup
4. **Advanced Memory** (4 agents): Swap optimizer, WindowServer, Spotlight, Memory leaks
5. **Browser Deep Cleanup** (3 agents): Chrome, Safari, Firefox optimizers
6. **App & System** (3 agents): Messaging apps, VSCode, DNS/Network

**Performance**:
- Sequential: 40 × 1.0s = 40s (estimated per agent)
- Parallel (6 phases): 4-5s total (8× faster than sequential)
- Real-world: 4-7s depending on system state and cache availability
- With MetricsCache (TTL 30s): ~2-3s on repeated calls

## Usage

### 1. Full System Optimization (40 agents)

```bash
# Execute all 40 agents in 6 parallel phases
uv run scripts/coordinator.py

# JSON output
uv run scripts/coordinator.py --json
```

### 2. Individual Agents

```bash
# Memory pressure detector
uv run scripts/agent_memory_pressure_detector.py

# Browser tab manager
uv run scripts/agent_browser_tab_manager.py

# Docker cleanup
uv run scripts/agent_docker_deep_cleanup.py --dry-run
```

### 3. Utility Scripts

```bash
# Kill zombie processes
uv run scripts/kill_zombies_parallel.py

# Report memory usage
uv run scripts/report_memory.py

# Analyze running processes
uv run scripts/analyze_processes.py --json
```

## MoAI Integration

### Manager Agents

**manager-resource-coordinator.md**:
```python
# Execute full 40-agent orchestration
result = Bash("uv run .claude/skills/macos-resource-optimizer/scripts/coordinator.py --json")
data = json.loads(result.stdout)

# Parse results by phase
phase1_results = data["phases"]["disk_cleanup"]
phase2_results = data["phases"]["ram_optimization"]

# Return aggregated recommendations
```

### Expert Agents

**expert-memory-optimizer.md**:
```python
# Execute memory-specific agents
result = Bash("uv run scripts/agent_memory_pressure_detector.py --json")
memory_data = json.loads(result.stdout)

# Generate recommendations based on memory analysis
```

## Available Agents (40+)

### Phase 1: Disk Cleanup (15 agents)

**Process Cleanup**:
- `agent_python_zombies.py` - Python zombie processes
- `agent_node_process_scanner.py` - Node/Bun zombie processes
- `agent_workerd_zombies.py` - Cloudflare Workers zombies
- `agent_generic_idle.py` - Generic idle process hunter
- `agent_jvm_memory_hog_detector.py` - JVM memory hog detection
- `agent_ssh_git_process_zombies.py` - SSH/Git process zombies

**Application Helpers**:
- `agent_browser_helpers.py` - Chrome/Arc renderer helpers
- `agent_language_servers.py` - VS Code language servers
- `agent_electron_helpers.py` - Notion/Dia helpers

**Network & Resources**:
- `agent_network_connection_leaks.py` - Network connection leaks
- `agent_orphaned_process_groups.py` - Orphaned process groups
- `agent_docker_container_scanner.py` - Docker container scanning
- `agent_database_connection_pooler.py` - Database connection pooling
- `agent_ssh_connection_scanner.py` - SSH connection scanning
- `agent_file_cache_optimizer.py` - File cache optimization

### Phase 2: RAM Optimization (9 agents)

- `agent_memory_pressure_detector.py` - Memory pressure analysis
- `agent_browser_tab_manager.py` - Browser tab management
- `agent_browser_helper_consolidator.py` - Browser helper consolidation
- `agent_browser_cache_optimizer.py` - Browser cache optimization
- `agent_inactive_app_detector.py` - Inactive application detection
- `agent_electron_app_optimizer.py` - Electron app optimization
- `agent_background_app_suspender.py` - Background app suspension
- `agent_swap_optimizer.py` - Swap usage optimization
- `agent_memory_leak_hunter.py` - Memory leak detection

### Phase 3: Developer Cache (5 agents)

- `agent_timemachine_snapshot_cleaner.py` - Time Machine snapshots
- `agent_developer_cache_cleaner.py` - Developer cache cleanup
- `agent_xcode_cache_cleaner.py` - Xcode artifact cleanup
- `agent_build_cache_cleaner.py` - Gradle/Maven cache cleanup
- `agent_system_log_cleaner.py` - System log cleanup

### Phase 4: Advanced Memory (4 agents)

- `agent_swap_purgeable_hunter.py` - Purgeable swap memory
- `agent_window_server_optimizer.py` - WindowServer optimization
- `agent_spotlight_mds_hunter.py` - Spotlight MDS optimization
- `agent_memory_leak_hunter.py` - Memory leak detection

### Phase 5: Browser Deep Cleanup (3 agents)

- `agent_chrome_deep_cleanup.py` - Chrome deep cleanup
- `agent_safari_optimizer.py` - Safari optimization
- `agent_firefox_deep_cleanup.py` - Firefox cleanup

### Phase 6: App & System (3 agents)

- `agent_messaging_app_hunter.py` - Messaging app optimization (Slack/Discord)
- `agent_vscode_deep_cleanup.py` - VS Code cleanup
- `agent_dns_connection_scanner.py` - DNS/Network optimization

## Architecture

### Execution Stack

```
User Command (slash command)
    ↓
MoAI Command (Python orchestrator)
    ↓
Task() delegation to manager agents
    ↓
Manager-Resource-Coordinator (MoAI agent)
    ↓
Bash(uv run coordinator.py) → UV Script execution
    ↓
asyncio.gather() parallel execution
    ├─ Phase 1: Disk Cleanup (15 agents)
    ├─ Phase 2: RAM Optimization (9 agents)
    ├─ Phase 3: Developer Cache (5 agents)
    ├─ Phase 4: Advanced Memory (4 agents)
    ├─ Phase 5: Browser Cleanup (3 agents)
    └─ Phase 6: App & System (3 agents)
    ↓
JSON results aggregation
    ↓
User-facing report (Korean)
```

### Implementation Details

**Execution Method**: UV Scripts (PEP 723)
```bash
#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["psutil", "pyyaml"]
# ///

import asyncio
import psutil

# Scripts run directly via: uv run script.py
# No Python virtual environment setup required
```

**Delegation Pattern**: Bash + Task()
```python
# Manager agent receives command
# Delegates to Bash tool: uv run .claude/skills/.../scripts/coordinator.py
# Coordinator spawns async tasks for 40 agents
# Results aggregated and returned
```

### Data Flow

```python
# coordinator.py executes agents
{
    "phases": {
        "disk_cleanup": {
            "agents_executed": 15,
            "duration": 2.1,
            "savings_gb": 5.3,
            "results": [...]
        },
        "ram_optimization": {
            "agents_executed": 9,
            "duration": 1.8,
            "memory_freed_gb": 2.1,
            "results": [...]
        },
        ...
    },
    "summary": {
        "total_agents": 40,
        "total_duration": 2.5,
        "total_savings_gb": 12.4,
        "total_memory_freed_gb": 4.2
    }
}
```

## Protected Apps

**Default protected apps** (from `config/cleanup-rules.json`):
- Claude Code
- Notion
- Slack
- Discord
- Mail
- Messages
- Ghostty

**Recommended additional protection** (for development environments):
- Node.js (active development processes)
- Apple Virtualization (system virtualization)
- VSCode/Cursor (development editors)
- Xcode (development tools)
- Docker Desktop (containerization)

**Customization**: Edit `config/cleanup-rules.json` to add/remove protected apps based on your workflow.

These apps are NEVER killed or suspended during optimization.

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Total Agents | 40+ specialized agents |
| Orchestrators | 1 (coordinator only) |
| Execution Time (parallel) | 4-5s (first run), 2-3s (cached) |
| Execution Time (sequential) | ~40s (estimated) |
| Speed Improvement | 8× faster (parallel vs sequential) |
| Memory Saved (typical) | 1-3 GB |
| Disk Saved (typical) | 0.4-2.5 GB |
| **Actual Results** (2025-11-30) | +413MB disk, 18% of goal |

## Commands Integration

### /macos-resource-optimizer:1-analyze

```markdown
Execute full system analysis via coordinator.py.

## Workflow

1. Delegate to manager-resource-coordinator
2. Coordinator executes: `uv run scripts/coordinator.py --json`
3. Parse JSON results
4. Return formatted analysis with recommendations
```

### /macos-resource-optimizer:2-optimize

```markdown
Execute system optimization via coordinator.py.

## Workflow

1. Delegate to manager-resource-coordinator
2. Coordinator executes: `uv run scripts/coordinator.py --json`
3. Parse and validate results
4. Apply optimizations if approved
5. Return optimization results
```

## Works Well With

**MoAI Agents**:
- `manager-resource-coordinator` - Main orchestration (uses coordinator.py)
- `expert-memory-optimizer` - Memory-specific agents
- `expert-cpu-optimizer` - CPU optimization (future)
- `expert-disk-optimizer` - Disk optimization agents

**MoAI Skills**:
- `moai-lang-python` - Python 3.11+ async patterns
- `moai-foundation-core` - TRUST 5 quality standards
- `moai-essentials-debug` - Debugging subprocess issues

**Commands**:
- `/macos-resource-optimizer:0-init` - Initialize configuration
- `/macos-resource-optimizer:1-analyze` - Full system analysis
- `/macos-resource-optimizer:2-optimize` - System optimization
- `/macos-resource-optimizer:3-monitor` - Continuous monitoring
- `/macos-resource-optimizer:9-feedback` - Submit feedback

---

**Version**: 2.1.0
**Last Updated**: 2025-11-30 (Phase 2.2 improvements)
**Status**: ✅ Production Ready (40+ agents, 1 orchestrator, UV scripts)
**Architecture**: Bash(uv run) delegation pattern via MoAI agents
**Real Scripts**: Located in `.claude/skills/macos-resource-optimizer/scripts/`
**Actual Performance**: 4-5s first run, 2-3s cached (measured 2025-11-30)
