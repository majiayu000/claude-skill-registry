---
name: nex-cli-guide
description: NATS NEX CLI usage guide. Node and workload commands, flags, configuration.
triggers:
  - "nex CLI"
  - "nex commands"
  - "nex node"
  - "nex workload"
  - "nexfile"
  - "nex start"
  - "nex deploy"
---

# NEX CLI Guide

## Installation

```bash
# From source
go install github.com/synadia-io/nex/cmd/nex@latest

# Or download binary from releases
# https://github.com/synadia-io/nex/releases
```

## Global Flags

| Flag | Description | Default |
|------|-------------|---------|
| `-s, --server` | NATS server URLs (comma-separated) | `nats://localhost:4222` |
| `--timeout` | Request timeout | `5s` |
| `--creds` | NATS credentials file | - |
| `--user` | NATS username | - |
| `--password` | NATS password | - |
| `--nkey` | NATS NKey for auth | - |
| `-n, --namespace` | NEX namespace (nexus name) | `nexus` |
| `--json` | Output raw JSON | `false` |
| `--config` | Path to config file | - |
| `-v, --verbose` | Enable verbose output | `false` |

## Configuration Precedence

Configuration is loaded in this order (later overrides earlier):

1. `/etc/nex/config.json` (system)
2. `~/.config/nex/config.json` (user)
3. `./config.json` (local)
4. Command-line flags (highest priority)

### Configuration File Format

```json
{
  "servers": "nats://localhost:4222",
  "namespace": "default",
  "timeout": "5s",
  "credentials": "/path/to/creds.creds"
}
```

---

## Node Commands

### `nex node up`

Start a NEX node (host that runs agents/workloads).

```bash
# Basic startup
nex -s nats://127.0.0.1:4222 node up

# With custom name and tags
nex node up \
  --node-name my-node \
  --tags "env=production;region=us-west" \
  --agents "native" \
  --show-workload-logs

# Production setup with persistence
nex node up \
  --node-name prod-node-01 \
  --tags "env=prod;region=us-east-1" \
  --state kv \
  --events nats,logs \
  --issuer-signing-key "SAABC..."
```

**Flags:**

| Flag | Description | Default |
|------|-------------|---------|
| `--node-name` | Node identifier | (random UUID) |
| `--node-seed` | NKey seed for identity | (generated) |
| `--node-xkey-seed` | XKey seed for encryption | (generated) |
| `--nexus` | Nexus name (namespace) | `nexus` |
| `--tags` | Node tags for placement (key=value;...) | - |
| `--agents` | Agent types to initialize | - |
| `--agent-restart-limit` | Max agent restart attempts | `3` |
| `--disable-native-start` | Don't start native agent | `false` |
| `--allow-remote-agent-registration` | Allow remote nexlets | `false` |
| `--show-workload-logs` | Show workload stdout/stderr | `false` |
| `--state` | Enable state persistence (`kv`) | - |
| `--events` | Event destinations (`nats`, `logs`) | - |
| `--issuer-signing-key` | JWT signing seed for creds | - |
| `--issuer-signing-key-root-account` | Root account public key | - |

### `nex node list`

List all running NEX nodes.

```bash
# List all nodes
nex node list

# Filter by tags
nex node list --filter "nex.nexus=mynexus"
nex node list --filter "env=production"

# JSON output for scripting
nex node list --json
```

**Flags:**

| Flag | Description |
|------|-------------|
| `--filter` | Filter by tag (key=value) |
| `--json` | Output raw JSON |

### `nex node info`

Get detailed information about a specific node.

```bash
# Basic info
nex node info <NODE_ID>

# Full info with agent details and workloads
nex node info <NODE_ID> --full

# JSON output
nex node info <NODE_ID> --json
```

**Flags:**

| Flag | Description |
|------|-------------|
| `--full` | Include agent and workload details |
| `--json` | Output raw JSON |

### `nex node lameduck`

Graceful shutdown - stop accepting new workloads, allow existing to drain.

```bash
# Lame duck specific node
nex node lameduck --node-id <NODE_ID> --delay 2m

# Lame duck by tag (all matching nodes)
nex node lameduck --tag env=staging --delay 1m
```

**Flags:**

| Flag | Description | Default |
|------|-------------|---------|
| `--node-id` | Target specific node ID | - |
| `--tag` | Target nodes by tag | - |
| `--delay` | Drain delay before shutdown | `30s` |

---

## Workload Commands

### `nex workload start`

Deploy a workload to the cluster.

```bash
# From Nexfile (recommended)
nex workload start -f Nexfile

# From Nexfile with placement tags
nex workload start -f Nexfile --tags "region=us-west"

# Inline definition (for scripting)
nex workload start \
  --type native \
  --lifecycle service \
  --name my-service \
  --start-request '{"uri":"file:///usr/local/bin/myapp","argv":["--config","/etc/app.yaml"]}'
```

**Flags:**

| Flag | Description |
|------|-------------|
| `--nexfile, -f` | Path to Nexfile (YAML/JSON) |
| `--type` | Workload type (e.g., `native`) |
| `--lifecycle` | `service`, `job`, or `function` |
| `--name` | Workload name |
| `--start-request` | Inline JSON for start params |
| `--tags` | Placement tags (key=value;...) |
| `--description` | Workload description |

### `nex workload ls`

List running workloads.

```bash
# List all workloads
nex workload ls

# With metadata
nex workload ls --show-metadata

# Filter by type
nex workload ls --type native

# JSON output
nex workload ls --json
```

**Flags:**

| Flag | Description |
|------|-------------|
| `--show-metadata` | Include workload metadata |
| `--type` | Filter by workload type |
| `--json` | Output raw JSON |

### `nex workload stop`

Terminate a running workload.

```bash
nex workload stop <WORKLOAD_ID>

# With graceful timeout
nex workload stop <WORKLOAD_ID> --timeout 30s
```

### `nex workload info`

Get detailed information about a workload.

```bash
nex workload info <WORKLOAD_ID>
nex workload info <WORKLOAD_ID> --json
```

### `nex workload clone`

Duplicate a workload (re-auction to new capacity).

```bash
# Clone to additional capacity
nex workload clone <WORKLOAD_ID>

# Clone with different placement
nex workload clone <WORKLOAD_ID> --tags "region=canary"

# Clone and stop original (migration)
nex workload clone <WORKLOAD_ID> --stop
```

**Flags:**

| Flag | Description |
|------|-------------|
| `--tags` | Override placement tags |
| `--stop` | Stop original after clone succeeds |

---

## Nexfile Format

The Nexfile defines a workload for deployment.

### YAML Format (Recommended)

```yaml
# Required fields
name: "my-workload"           # Human-readable name
type: native                  # Agent type
lifecycle: service            # service | job | function

# Start request (agent-specific)
start_request:
  uri: "file:///path/to/binary"
  argv:
    - "--config"
    - "/etc/app.yaml"
  environment:
    LOG_LEVEL: "debug"
    DATABASE_URL: "postgres://..."
  workdir: "/app"

# Optional metadata
description: "My awesome service"
tags:
  region: "us-west"
  env: "production"
  team: "platform"
```

### JSON Format

```json
{
  "name": "my-workload",
  "type": "native",
  "lifecycle": "service",
  "description": "My awesome service",
  "tags": {
    "region": "us-west",
    "env": "production"
  },
  "start_request": {
    "uri": "file:///path/to/binary",
    "argv": ["--config", "/etc/app.yaml"],
    "environment": {
      "LOG_LEVEL": "debug"
    },
    "workdir": "/app"
  }
}
```

### Lifecycle Types

#### Service (Long-Running)

```yaml
name: "api-server"
type: native
lifecycle: service
start_request:
  uri: "file:///usr/local/bin/api"
  argv: ["--port", "8080"]
  environment:
    PORT: "8080"
```

- Runs continuously
- Auto-restarts on failure
- Use for: API servers, stream processors, daemons

#### Job (Run-to-Completion)

```yaml
name: "db-migration"
type: native
lifecycle: job
start_request:
  uri: "file:///usr/local/bin/migrate"
  argv: ["--dry-run=false"]
```

- Runs once to completion
- No auto-restart
- Use for: Batch tasks, migrations, backups

#### Function (Event-Triggered)

```yaml
name: "webhook-handler"
type: native
lifecycle: function
start_request:
  uri: "file:///usr/local/bin/handler"
  # Trigger configured via NATS subject
```

- Invoked per-event
- Scales to zero when idle
- Use for: Webhooks, data transforms, event handlers

---

## Environment Variables

### Injected into Workloads

NEX automatically injects these environment variables:

| Variable | Description |
|----------|-------------|
| `NEX_WORKLOAD_NATS_SERVERS` | NATS server URLs |
| `NEX_WORKLOAD_NATS_NKEY` | NKey for auth |
| `NEX_WORKLOAD_NATS_B64_JWT` | Base64-encoded JWT |
| `NEX_WORKLOAD_ID` | Unique workload identifier |
| `NEX_NAMESPACE` | Current namespace |
| `NEX_NODE_ID` | Host node identifier |

### Using Injected Credentials

```go
// Go example
servers := os.Getenv("NEX_WORKLOAD_NATS_SERVERS")
jwt := os.Getenv("NEX_WORKLOAD_NATS_B64_JWT")
nkey := os.Getenv("NEX_WORKLOAD_NATS_NKEY")

nc, err := nats.Connect(servers, nats.UserJWTAndSeed(jwt, nkey))
```

```typescript
// TypeScript example
const servers = process.env.NEX_WORKLOAD_NATS_SERVERS
const jwt = Buffer.from(process.env.NEX_WORKLOAD_NATS_B64_JWT!, 'base64').toString()
const nkey = process.env.NEX_WORKLOAD_NATS_NKEY

const nc = await connect({
  servers: servers?.split(','),
  authenticator: jwtAuthenticator(jwt, new TextEncoder().encode(nkey)),
})
```

---

## Monitoring

### Subscribe to Events

```bash
# All events
nats sub "$NEX.FEED.default.event.>"

# Specific event types
nats sub "$NEX.FEED.default.event.WorkloadStarted"
nats sub "$NEX.FEED.default.event.WorkloadStopped"
```

### Subscribe to Logs

```bash
# All logs
nats sub "$NEX.FEED.default.logs.>"

# Specific workload
nats sub "$NEX.FEED.default.logs.<WORKLOAD_ID>.>"

# Only stdout
nats sub "$NEX.FEED.default.logs.<WORKLOAD_ID>.out"

# Only stderr
nats sub "$NEX.FEED.default.logs.<WORKLOAD_ID>.err"
```

### Event Types

| Event | Description |
|-------|-------------|
| `NexNodeStartedEvent` | Node started |
| `NexNodeStoppedEvent` | Node stopped |
| `AgentStartedEvent` | Agent registered |
| `AgentStoppedEvent` | Agent terminated |
| `WorkloadStartedEvent` | Workload deployed |
| `WorkloadStoppedEvent` | Workload terminated |
| `WorkloadTriggeredEvent` | Function invoked |

---

## Examples

### Deploy a Simple Service

```bash
# Create Nexfile
cat > Nexfile.yaml << 'EOF'
name: hello-service
type: native
lifecycle: service
start_request:
  uri: "file:///usr/local/bin/hello"
  environment:
    GREETING: "Hello from NEX!"
EOF

# Deploy
nex workload start -f Nexfile.yaml

# Check status
nex workload ls

# View logs
nats sub "$NEX.FEED.default.logs.>"
```

### Deploy with Placement Constraints

```bash
# Deploy only to production nodes
nex workload start -f Nexfile.yaml --tags "env=production"

# Deploy to specific region
nex workload start -f Nexfile.yaml --tags "region=us-west-2"
```

### Rolling Update

```bash
# Clone with new image/config (clone goes to different node)
nex workload clone <OLD_ID> --tags "version=v2"

# Verify new workload is healthy
nex workload info <NEW_ID>

# Stop old workload
nex workload stop <OLD_ID>
```

### Batch Job

```bash
cat > migration.yaml << 'EOF'
name: db-migration-v42
type: native
lifecycle: job
start_request:
  uri: "file:///usr/local/bin/migrate"
  argv: ["--version", "42", "--apply"]
  environment:
    DATABASE_URL: "postgres://localhost/mydb"
EOF

nex workload start -f migration.yaml

# Watch for completion
nats sub "$NEX.FEED.default.event.WorkloadStopped"
```

---

## Troubleshooting

### Node Won't Start

```bash
# Check NATS connectivity
nats server check

# Run with verbose logging
nex -v node up

# Check for port conflicts
netstat -tlnp | grep 4222
```

### Workload Won't Deploy

```bash
# Check available nodes
nex node list

# Verify node has matching tags
nex node info <NODE_ID> --full

# Check auction (verbose)
nex -v workload start -f Nexfile.yaml
```

### Workload Keeps Restarting

```bash
# Check logs
nats sub "$NEX.FEED.default.logs.<WORKLOAD_ID>.err"

# Check events for failure reason
nats sub "$NEX.FEED.default.event.WorkloadStopped"

# Get workload info
nex workload info <WORKLOAD_ID>
```

## Related Skills

- `/nex-codebase-navigation` - Source code exploration
- `/nex-effect-services` - Effect-TS integration patterns

## References

- [NEX GitHub](https://github.com/synadia-io/nex)
- [NEX Documentation](https://github.com/synadia-io/nex/tree/main/docs)
- [NATS CLI](https://docs.nats.io/running-a-nats-service/clients)
