---
name: nex-codebase-navigation
description: Navigate and index the NATS NEX codebase. Key codepaths, file structure, and architecture overview.
triggers:
  - "NEX codebase"
  - "NEX source"
  - "NEX architecture"
  - "nex code"
  - "synadia-io/nex"
  - "NEX internals"
---

# NEX Codebase Navigation

## Overview

NEX (NATS Execution Engine) is a workload deployment and execution system built on NATS. This skill indexes the codebase structure for efficient navigation.

## Repository Structure (synadia-io/nex)

### Top-Level Directories

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `cmd/nex/` | CLI entry point | `main.go`, `node.go`, `workload.go` |
| `client/` | Go client library | `client.go`, `options.go` |
| `node/` | NexNode implementation | `node.go`, `handlers.go`, `minter.go` |
| `agent/` | Agent interface + SDK | `agent.go` |
| `models/` | Shared data models | `events.go`, `subjects.go`, `nexfile.go` |
| `natsext/` | NATS utilities | `requestmany.go` |
| `_test/` | Test fixtures | `nexlet_inmem/inmemagent.go` |
| `docs/` | Documentation | Architecture guides |

### Key Codepaths

#### 1. CLI → Workload Deployment

```
cmd/nex/main.go           # Entry point, Kong CLI parsing
  └─ cmd/nex/workload.go  # `nex workload start` handler
       └─ client/client.go
            ├─ Auction()           # Bid for workload placement
            └─ StartWorkload()     # Deploy to winning bidder
```

**Key functions:**
- `client.Auction()` - Broadcasts auction request, collects bids
- `client.StartWorkload()` - Sends deployment request to selected node

#### 2. Node Startup + Agent Registration

```
node/node.go: NewNexNode()     # Create node with identity
  └─ node/node.go: Start()     # Start NATS handlers
       └─ node/handlers.go     # NATS microservice endpoints
            ├─ handleAuction()              # Respond to auction requests
            ├─ handleAuctionDeployWorkload() # Mint creds + deploy
            └─ handleAgentRegister()        # Accept agent registration
```

**Key functions:**
- `NewNexNode()` - Initializes node with config, identity keys
- `Start()` - Registers NATS micro handlers, starts heartbeat
- `handleAuction()` - Evaluates auction request, returns bid
- `handleAuctionDeployWorkload()` - Mints credentials, deploys to agent

#### 3. Agent Lifecycle

```
agent/agent.go: Agent interface   # 9 required methods
  └─ Register()                   # Declare capabilities
  └─ StartWorkload()              # Deploy + emit WorkloadStartedEvent
  └─ StopWorkload()               # Terminate + emit WorkloadStoppedEvent
  └─ Heartbeat()                  # Report health every 30s

_test/nexlet_inmem/inmemagent.go  # Reference implementation
```

**Agent interface methods:**
```go
type Agent interface {
    // Lifecycle
    Start(ctx context.Context) error
    Stop() error

    // Registration
    Register(parentId string) error
    AgentID() string

    // Workload management
    StartWorkload(request *StartWorkloadRequest) (*WorkloadInfo, error)
    StopWorkload(workloadId string) error
    ListWorkloads() ([]WorkloadInfo, error)

    // Health
    Heartbeat() AgentHeartbeat
}
```

#### 4. Credential Minting

```
node/minter.go: SigningKeyMinter
  └─ Mint()                       # Create JWT with scoped permissions
       └─ WorkloadClaims()        # Pub: _INBOX.>, Sub: logs.{ns}.>, _INBOX.>
```

**Workload permissions (scoped JWT):**
- Publish: `_INBOX.>` (request-reply responses)
- Subscribe: `logs.{namespace}.>`, `_INBOX.>` (requests)
- Response limit: 1 message per request

## File Quick Reference

| Need to... | File | Function/Type |
|------------|------|---------------|
| Understand CLI commands | `cmd/nex/*.go` | Kong command structs |
| See client SDK methods | `client/client.go` | `Client` struct |
| Implement custom agent | `agent/agent.go` | `Agent` interface |
| Find event types | `models/events.go` | `*Event` structs |
| See NATS subjects | `models/subjects.go` | Subject constants |
| Check Nexfile format | `models/nexfile.go` | `Nexfile` struct |
| Understand auction | `node/handlers.go` | `handleAuction()` |
| See credential minting | `node/minter.go` | `SigningKeyMinter` |

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         NEX Architecture                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────┐  │
│  │   Client    │───▶│  NexNode    │───▶│   Agent (Nexlet)        │  │
│  │  (CLI/SDK)  │    │  (Host)     │    │   (Runtime Executor)    │  │
│  └─────────────┘    └─────────────┘    └─────────────────────────┘  │
│        │                  │                       │                  │
│        │    1. Auction    │    2. Deploy          │    3. Execute    │
│        ▼                  ▼                       ▼                  │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    NATS Messaging Fabric                         ││
│  │  $NEX.SVC.<namespace>.control.*  (auction, deploy)               ││
│  │  $NEX.FEED.<namespace>.event.*   (lifecycle events)              ││
│  │  $NEX.FEED.<namespace>.logs.*    (workload logs)                 ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

## NATS Subjects

### Control Plane (Request-Reply)

| Subject | Purpose | Handler |
|---------|---------|---------|
| `$NEX.SVC.<ns>.control.AUCTION` | Workload placement auction | `handleAuction()` |
| `$NEX.SVC.<ns>.control.AUCTIONDEPLOY.<bid>` | Deploy to winning bidder | `handleAuctionDeployWorkload()` |
| `$NEX.SVC.<ns>.workloads.LIST` | List running workloads | `handleListWorkloads()` |
| `$NEX.SVC.<ns>.workloads.STOP` | Stop a workload | `handleStopWorkload()` |
| `$NEX.SVC.<ns>.nodes.INFO` | Get node information | `handleNodeInfo()` |
| `$NEX.SVC.<ns>.agents.REGISTER` | Agent registration | `handleAgentRegister()` |

### Data Plane (Pub/Sub)

| Subject | Purpose | Payload |
|---------|---------|---------|
| `$NEX.FEED.<ns>.event.*` | Lifecycle events | `*Event` structs |
| `$NEX.FEED.<ns>.logs.<wid>.out` | Workload stdout | Raw bytes |
| `$NEX.FEED.<ns>.logs.<wid>.err` | Workload stderr | Raw bytes |
| `$NEX.FEED.<ns>.metrics.<wid>` | Workload metrics | JSON metrics |

## deepwiki Queries

Use deepwiki MCP for detailed exploration:

```typescript
// Get wiki structure
mcp__deepwiki__read_wiki_structure({ repoName: "synadia-io/nex" })

// Ask about specific components
mcp__deepwiki__ask_question({
  repoName: "synadia-io/nex",
  question: "How does the auction system work?"
})

// Explore agent interface
mcp__deepwiki__ask_question({
  repoName: "synadia-io/nex",
  question: "What methods must an agent implement?"
})

// Understand credential minting
mcp__deepwiki__ask_question({
  repoName: "synadia-io/nex",
  question: "How are workload credentials scoped?"
})
```

## Wiki Pages Index

| Section | Topic | Key Concepts |
|---------|-------|--------------|
| 1 | Introduction | Overview, use cases |
| 2 | Getting Started | Installation, quickstart |
| 3 | Core Concepts | Nodes, Agents, Workloads |
| 4 | System Architecture | Component, Node, Agent arch |
| 5 | NexNode | Lifecycle, Handlers, Config, Auction |
| 6 | Agents | Interface, Native, Lifecycle, Custom |
| 7 | Workloads | Types, Deployment, Nexfile |
| 8 | Client Library | Node Ops, Workload Ops |
| 9 | CLI Tool | Config, Node Commands, Workload Commands |
| 10 | Security | Credentials, JWT, Secrets |
| 11 | Data Models | Schemas, Events |
| 12 | Development | Build, Test, Debug |

## Workload Lifecycles

| Lifecycle | Behavior | Auto-restart | Use Case |
|-----------|----------|--------------|----------|
| `service` | Long-running | Yes (on failure) | API servers, processors |
| `job` | Run-to-completion | No | Batch tasks, migrations |
| `function` | Event-triggered | Per-invocation | Webhooks, transforms |

## Event Types

```go
// Node events
type NexNodeStartedEvent struct { ... }
type NexNodeStoppedEvent struct { ... }

// Agent events
type AgentStartedEvent struct { ... }
type AgentStoppedEvent struct { ... }

// Workload events
type WorkloadStartedEvent struct {
    WorkloadId    string
    NodeId        string
    WorkloadName  string
    Namespace     string
    Type          string
    Lifecycle     string
}
type WorkloadStoppedEvent struct { ... }
type WorkloadTriggeredEvent struct { ... }  // For functions
```

## Configuration Files

### Node Configuration

```json
{
  "node_name": "my-node",
  "nexus": "default",
  "tags": {
    "env": "production",
    "region": "us-west"
  },
  "agents": ["native"],
  "nats": {
    "servers": ["nats://localhost:4222"],
    "credentials": "/path/to/creds.creds"
  },
  "events": {
    "destinations": ["nats", "logs"]
  }
}
```

### Nexfile Format

```yaml
name: my-workload
type: native
lifecycle: service
description: My workload description
tags:
  env: production
start_request:
  uri: "file:///path/to/binary"
  argv: ["--config", "/etc/app.yaml"]
  environment:
    LOG_LEVEL: "debug"
  workdir: "/app"
```

## Building Custom Agents

Reference the in-memory test agent:

```go
// _test/nexlet_inmem/inmemagent.go

type InMemoryAgent struct {
    id        string
    parentId  string
    workloads map[string]*WorkloadInfo
    nc        *nats.Conn
}

func (a *InMemoryAgent) Register(parentId string) error {
    a.parentId = parentId
    // Register capabilities with parent node
    return a.nc.Publish(
        fmt.Sprintf("$NEX.SVC.%s.agents.REGISTER", a.parentId),
        registerPayload,
    )
}

func (a *InMemoryAgent) StartWorkload(req *StartWorkloadRequest) (*WorkloadInfo, error) {
    // Validate request
    // Start execution
    // Return workload info
}
```

## Debugging Tips

1. **Enable verbose logging:**
   ```bash
   nex -v node up
   ```

2. **Subscribe to events:**
   ```bash
   nats sub "$NEX.FEED.default.event.>"
   ```

3. **Watch logs:**
   ```bash
   nats sub "$NEX.FEED.default.logs.>"
   ```

4. **Check node status:**
   ```bash
   nex node list --json
   ```

## Related Skills

- `/nex-cli-guide` - Complete CLI reference
- `/nex-effect-services` - Effect-TS integration patterns

## References

- [NEX GitHub](https://github.com/synadia-io/nex)
- [NATS Documentation](https://docs.nats.io/)
- [NATS Micro Services](https://docs.nats.io/nats-concepts/service-infra)
