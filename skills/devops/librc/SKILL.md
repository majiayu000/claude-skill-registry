---
name: librc
description: >
  librc - Service lifecycle manager using svscan supervision. ServiceManager
  communicates with supervision daemon via Unix sockets. startServices and
  stopServices control multiple services. Use for starting/stopping platform
  services, process supervision, and service orchestration.
---

# librc Skill

## When to Use

- Starting and stopping Copilot-LD services
- Managing service lifecycle programmatically
- Communicating with the supervision daemon
- Orchestrating service startup order

## Key Concepts

**ServiceManager**: Connects to svscan daemon via Unix socket to control service
processes.

**Supervision**: Services run under svscan for automatic restart and logging.

## Usage Patterns

### Pattern 1: Manage single service

```javascript
import { ServiceManager } from "@copilot-ld/librc";

const manager = new ServiceManager("/var/run/svscan.sock");
await manager.start("agent");
await manager.status("agent"); // Returns running/stopped
await manager.stop("agent");
```

### Pattern 2: Manage multiple services

```javascript
import { startServices, stopServices } from "@copilot-ld/librc";

await startServices(["agent", "llm", "memory"]);
await stopServices(["agent", "llm", "memory"]);
```

## Integration

Used by `make rc-start` and `make rc-stop`. Works with libsupervision daemon.
