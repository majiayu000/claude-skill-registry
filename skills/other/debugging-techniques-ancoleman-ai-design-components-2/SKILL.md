---
name: debugging-techniques
description: Debugging workflows for Python (pdb, debugpy), Go (delve), Rust (lldb), and Node.js, including container debugging (kubectl debug, ephemeral containers) and production-safe debugging techniques with distributed tracing and correlation IDs. Use when setting breakpoints, debugging containers/pods, remote debugging, or production debugging.
---

# Debugging Techniques

## Purpose

Provides systematic debugging workflows for local, remote, container, and production environments across Python, Go, Rust, and Node.js. Covers interactive debuggers, container debugging with ephemeral containers, and production-safe techniques using correlation IDs and distributed tracing.

## When to Use This Skill

Trigger this skill for:
- Setting breakpoints in Python, Go, Rust, or Node.js code
- Debugging running containers or Kubernetes pods
- Setting up remote debugging connections
- Safely debugging production issues
- Inspecting goroutines, threads, or async tasks
- Analyzing core dumps or stack traces
- Choosing the right debugging tool for a scenario

## Quick Reference by Language

### Python Debugging

**Built-in: pdb**
```python
# Python 3.7+
def buggy_function(x, y):
    breakpoint()  # Stops execution here
    return x / y

# Older Python
import pdb
pdb.set_trace()
```

**Essential pdb commands:**
- `list` (l) - Show code around current line
- `next` (n) - Execute current line, step over functions
- `step` (s) - Execute current line, step into functions
- `continue` (c) - Continue until next breakpoint
- `print var` (p) - Print variable value
- `where` (w) - Show stack trace
- `quit` (q) - Exit debugger

**Enhanced tools:**
- `ipdb` - Enhanced pdb with tab completion, syntax highlighting (`pip install ipdb`)
- `pudb` - Terminal GUI debugger (`pip install pudb`)
- `debugpy` - VS Code integration (included in Python extension)

**Debugging tests:**
```bash
pytest --pdb  # Drop into debugger on test failure
```

For detailed Python debugging patterns, see `references/python-debugging.md`.

### Go Debugging

**Delve - Official Go debugger**

**Installation:**
```bash
go install github.com/go-delve/delve/cmd/dlv@latest
```

**Basic usage:**
```bash
dlv debug main.go              # Debug main package
dlv test github.com/me/pkg     # Debug test suite
dlv attach <pid>               # Attach to running process
dlv debug -- --config prod.yaml  # Pass arguments
```

**Essential commands:**
- `break main.main` (b) - Set breakpoint at function
- `break file.go:10` (b) - Set breakpoint at line
- `continue` (c) - Continue execution
- `next` (n) - Step over
- `step` (s) - Step into
- `print x` (p) - Print variable
- `goroutine` (gr) - Show current goroutine
- `goroutines` (grs) - List all goroutines
- `goroutines -t` - Show goroutine stacktraces
- `stack` (bt) - Show stack trace

**Goroutine debugging:**
```bash
(dlv) goroutines                 # List all goroutines
(dlv) goroutines -t              # Show stacktraces
(dlv) goroutines -with user      # Filter user goroutines
(dlv) goroutine 5                # Switch to goroutine 5
```

For detailed Go debugging patterns, see `references/go-debugging.md`.

### Rust Debugging

**LLDB - Default Rust debugger**

**Compilation:**
```bash
cargo build  # Debug build includes symbols by default
```

**Usage:**
```bash
rust-lldb target/debug/myapp   # LLDB wrapper for Rust
rust-gdb target/debug/myapp    # GDB wrapper (alternative)
```

**Essential LLDB commands:**
- `breakpoint set -f main.rs -l 10` - Set breakpoint at line
- `breakpoint set -n main` - Set breakpoint at function
- `run` (r) - Start program
- `continue` (c) - Continue execution
- `next` (n) - Step over
- `step` (s) - Step into
- `print variable` (p) - Print variable
- `frame variable` (fr v) - Show local variables
- `backtrace` (bt) - Show stack trace
- `thread list` - List all threads

**VS Code integration:**
- Install CodeLLDB extension (`vadimcn.vscode-lldb`)
- Configure `launch.json` for Rust projects

For detailed Rust debugging patterns, see `references/rust-debugging.md`.

### Node.js Debugging

**Built-in: node --inspect**

**Basic usage:**
```bash
node --inspect-brk app.js       # Start and pause immediately
node --inspect app.js           # Start and run
node --inspect=0.0.0.0:9229 app.js  # Specify host/port
```

**Chrome DevTools:**
1. Open `chrome://inspect`
2. Click "Open dedicated DevTools for Node"
3. Set breakpoints, inspect variables

**VS Code integration:**
Configure `launch.json`:
```json
{
  "type": "node",
  "request": "launch",
  "name": "Launch Program",
  "program": "${workspaceFolder}/app.js"
}
```

**Docker debugging:**
```dockerfile
EXPOSE 9229
CMD ["node", "--inspect=0.0.0.0:9229", "app.js"]
```

For detailed Node.js debugging patterns, see `references/nodejs-debugging.md`.

## Container & Kubernetes Debugging

### kubectl debug with Ephemeral Containers

**When to use:**
- Container has crashed (kubectl exec won't work)
- Using distroless/minimal image (no shell, no tools)
- Need debugging tools without rebuilding image
- Debugging network issues

**Basic usage:**
```bash
# Add ephemeral debugging container
kubectl debug -it <pod-name> --image=nicolaka/netshoot

# Share process namespace (see other container processes)
kubectl debug -it <pod-name> --image=busybox --share-processes

# Target specific container
kubectl debug -it <pod-name> --image=busybox --target=app
```

**Recommended debugging images:**
- `nicolaka/netshoot` (~380MB) - Network debugging (curl, dig, tcpdump, netstat)
- `busybox` (~1MB) - Minimal shell and utilities
- `alpine` (~5MB) - Lightweight with package manager
- `ubuntu` (~70MB) - Full environment

**Node debugging:**
```bash
kubectl debug node/<node-name> -it --image=ubuntu
```

**Docker container debugging:**
```bash
docker exec -it <container-id> sh

# If no shell available
docker run -it --pid=container:<container-id> \
           --net=container:<container-id> \
           busybox sh
```

For detailed container debugging patterns, see `references/container-debugging.md`.

## Production Debugging

### Production Debugging Principles

**Golden rules:**
1. **Minimal performance impact** - Profile overhead, limit scope
2. **No blocking operations** - Use non-breaking techniques
3. **Security-aware** - Avoid logging secrets, PII
4. **Reversible** - Can roll back quickly (feature flags, Git)
5. **Observable** - Structured logging, correlation IDs, tracing

### Safe Production Techniques

**1. Structured Logging**
```python
import logging
import json

logger = logging.getLogger(__name__)
logger.info(json.dumps({
    "event": "user_login_failed",
    "user_id": user_id,
    "error": str(e),
    "correlation_id": request_id
}))
```

**2. Correlation IDs (Request Tracing)**
```go
func handleRequest(w http.ResponseWriter, r *http.Request) {
    correlationID := r.Header.Get("X-Correlation-ID")
    if correlationID == "" {
        correlationID = generateUUID()
    }
    ctx := context.WithValue(r.Context(), "correlationID", correlationID)
    log.Printf("[%s] Processing request", correlationID)
}
```

**3. Distributed Tracing (OpenTelemetry)**
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        span.add_event("Order validated")
```

**4. Error Tracking Platforms**
- Sentry - Exception tracking with context
- New Relic - APM with error tracking
- Datadog - Logs, metrics, traces
- Rollbar - Error monitoring

**Production debugging workflow:**
1. **Detect** - Error tracking alert, log spike, metric anomaly
2. **Locate** - Find correlation ID, search logs, view distributed trace
3. **Reproduce** - Try to reproduce in staging with production data (sanitized)
4. **Fix** - Create feature flag, deploy to canary first
5. **Verify** - Check error rates, review logs, monitor traces

For detailed production debugging patterns, see `references/production-debugging.md`.

## Decision Framework

### Which Debugger for Which Language?

| Language | Primary Tool | Installation | Best For |
|----------|-------------|--------------|----------|
| **Python** | pdb | Built-in | Simple scripts, server environments |
| | ipdb | `pip install ipdb` | Enhanced UX, IPython users |
| | debugpy | VS Code extension | IDE integration, remote debugging |
| **Go** | delve | `go install github.com/go-delve/delve/cmd/dlv@latest` | All Go debugging, goroutines |
| **Rust** | rust-lldb | System package | Mac, Linux, MSVC Windows |
| | rust-gdb | System package | Linux, prefer GDB |
| **Node.js** | node --inspect | Built-in | All Node.js debugging, Chrome DevTools |

### Which Technique for Which Scenario?

| Scenario | Recommended Technique | Tools |
|----------|----------------------|-------|
| Local development | Interactive debugger | pdb, delve, lldb, node --inspect |
| Bug in test | Test-specific debugging | pytest --pdb, dlv test, cargo test |
| Remote server | SSH tunnel + remote attach | VS Code Remote, debugpy |
| Container (local) | docker exec -it | sh/bash + debugger |
| Kubernetes pod | Ephemeral container | kubectl debug --image=nicolaka/netshoot |
| Distroless image | Ephemeral container (required) | kubectl debug with busybox/alpine |
| Production issue | Log analysis + error tracking | Structured logs, Sentry, correlation IDs |
| Goroutine deadlock | Goroutine inspection | delve goroutines -t |
| Crashed process | Core dump analysis | gdb core, lldb -c core |
| Distributed failure | Distributed tracing | OpenTelemetry, Jaeger, correlation IDs |
| Race condition | Race detector + debugger | go run -race, cargo test |

### Production Debugging Safety Checklist

Before debugging in production:
- [ ] Will this impact performance? (Profile overhead)
- [ ] Will this block users? (Use non-breaking techniques)
- [ ] Could this expose secrets? (Avoid variable dumps)
- [ ] Is there a rollback plan? (Git branch, feature flag)
- [ ] Have we tried logs first? (Less invasive)
- [ ] Do we have correlation IDs? (Trace requests)
- [ ] Is error tracking enabled? (Sentry, New Relic)
- [ ] Can we reproduce in staging? (Safer environment)

## Common Debugging Workflows

### Workflow 1: Local Development Bug

1. **Insert breakpoint** in code (language-specific)
2. **Start debugger** (dlv debug, rust-lldb, node --inspect-brk)
3. **Execute to breakpoint** (run, continue)
4. **Inspect variables** (print, frame variable)
5. **Step through code** (next, step, finish)
6. **Identify issue** and fix

### Workflow 2: Test Failure Debugging

**Python:**
```bash
pytest --pdb  # Drops into pdb on failure
```

**Go:**
```bash
dlv test github.com/user/project/pkg
(dlv) break TestMyFunction
(dlv) continue
```

**Rust:**
```bash
cargo test --no-run
rust-lldb target/debug/deps/myapp-<hash>
(lldb) breakpoint set -n test_name
(lldb) run test_name
```

### Workflow 3: Kubernetes Pod Debugging

**Scenario: Pod with distroless image, network issue**

```bash
# Step 1: Check pod status
kubectl get pod my-app-pod -o wide

# Step 2: Check logs first
kubectl logs my-app-pod

# Step 3: Add ephemeral container if logs insufficient
kubectl debug -it my-app-pod --image=nicolaka/netshoot

# Step 4: Inside debug container, investigate
curl localhost:8080
netstat -tuln
nslookup api.example.com
```

### Workflow 4: Production Error Investigation

**Scenario: API returning 500 errors**

```bash
# Step 1: Check error tracking (Sentry)
# - Find error details, stack trace
# - Copy correlation ID from error report

# Step 2: Search logs for correlation ID
# In log aggregation tool (ELK, Splunk):
# correlation_id:"abc-123-def"

# Step 3: View distributed trace
# In tracing tool (Jaeger, Datadog):
# Search by correlation ID, review span timeline

# Step 4: Reproduce in staging
# Use production data (sanitized) if needed
# Add additional logging if needed

# Step 5: Fix and deploy
# Create feature flag for gradual rollout
# Deploy to canary environment first
# Monitor error rates closely
```

## Additional Resources

For language-specific deep dives:
- `references/python-debugging.md` - pdb, ipdb, pudb, debugpy detailed guide
- `references/go-debugging.md` - Delve CLI, goroutine debugging, conditional breakpoints
- `references/rust-debugging.md` - LLDB vs GDB, ownership debugging, macro debugging
- `references/nodejs-debugging.md` - node --inspect, Chrome DevTools, Docker debugging

For environment-specific patterns:
- `references/container-debugging.md` - kubectl debug, ephemeral containers, node debugging
- `references/production-debugging.md` - Structured logging, correlation IDs, OpenTelemetry, error tracking

For decision support:
- `references/decision-trees.md` - Expanded debugging decision frameworks

For hands-on examples:
- `examples/` - Step-by-step debugging sessions for each language

## Related Skills

For authentication patterns, see the `auth-security` skill.
For performance profiling (complementary to debugging), see the `performance-engineering` skill.
For Kubernetes operations (kubectl debug is part of), see the `kubernetes-operations` skill.
For test debugging strategies, see the `testing-strategies` skill.
For observability setup (logging, tracing), see the `observability` skill.
