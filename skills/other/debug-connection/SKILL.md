---
name: debug-connection
description: Debug WebSocket connection issues between CLI and FigJam plugin. Use when diagrams aren't syncing or connection fails.
---

# WebSocket Connection Debugging

## Architecture

```
┌─────────────┐     WebSocket      ┌─────────────────┐    postMessage    ┌─────────────────┐
│  CLI serve  │ ◄───────────────► │  Plugin UI      │ ◄───────────────► │  Plugin Main    │
│  (Bun)      │   ws://...:3456   │  (ui.ts)        │                   │  (code.ts)      │
└─────────────┘                   └─────────────────┘                   └─────────────────┘
     │                                   │                                     │
     │ File watcher                      │ Browser APIs                        │ Figma API
     │ YAML parsing                      │ WebSocket client                    │ Canvas rendering
     └───────────────────────────────────┴─────────────────────────────────────┘
```

## Common Issues & Solutions

### 1. Connection Refused

**Symptoms**: Plugin shows "Connecting..." indefinitely

**Check**:
```bash
# Is CLI serve running?
ps aux | grep "figram serve"

# Check port availability (default: 3456)
lsof -i :3456
```

**Solution**: Start CLI with `bun run packages/cli/src/index.ts serve diagram.yaml`

### 2. Connection Drops

**Symptoms**: Works initially, then stops syncing

**Check**:
- Plugin UI console for WebSocket close events
- CLI terminal for error messages

**Solution**: Check for YAML parse errors blocking updates

### 3. Patches Not Applied

**Symptoms**: Connected but canvas doesn't update

**Debug steps**:
1. Check CLI output for patch generation
2. Check Plugin UI console for received messages
3. Check Plugin Main console for rendering errors

### 4. YAML Parse Errors

**Symptoms**: CLI shows validation errors

**Solution**: Validate YAML syntax and schema compliance

### 5. Secret Mismatch

**Symptoms**: Connection established but immediately closed

**Check**: Ensure `--secret` flag value matches between CLI and plugin

### 6. JSON Import Errors

**Symptoms**: Import dialog shows an error alert

**Check**:
- JSON must be an object
- DSL JSON requires `version`, `docId`, and `nodes` array
- IR JSON requires `version`, `docId`, and `nodes` object

**Solution**: Fix validation errors shown in the alert (path + message)

## Debugging Tools

### CLI Side
```bash
# Run with verbose output
DEBUG=* bun run packages/cli/src/index.ts serve diagram.yaml

# Specify custom port
bun run packages/cli/src/index.ts serve diagram.yaml --port 8080

# With authentication
bun run packages/cli/src/index.ts serve diagram.yaml --secret mysecret
```

### Plugin UI Side
1. Right-click plugin UI → Inspect
2. Check Console for WebSocket events
3. Check Network tab for WS frames

### Plugin Main Side
1. Figma Desktop → Plugins → Development → Open console
2. Check for rendering errors

## WebSocket Protocol

### Plugin → CLI Messages

```typescript
// Connection initiation
interface HelloMessage {
  type: "hello";
  docId: string;
  secret?: string;  // If server requires authentication
}

// Request full sync (e.g., after reconnection)
interface RequestFullMessage {
  type: "requestFull";
  docId: string;
}
```

### CLI → Plugin Messages

```typescript
// Full document sync
interface FullMessage {
  type: "full";
  rev: number;        // Current revision number
  ir: IRDocument;     // Complete normalized document
}

// Incremental update
interface PatchMessage {
  type: "patch";
  baseRev: number;    // Expected current revision
  nextRev: number;    // New revision after applying
  ops: PatchOp[];     // Operations to apply
}

// Error notification
interface ErrorMessage {
  type: "error";
  message: string;
}
```

### Patch Operations

```typescript
type PatchOp =
  | { op: "upsertNode"; node: IRNode }
  | { op: "removeNode"; id: string }
  | { op: "upsertEdge"; edge: IREdge }
  | { op: "removeEdge"; id: string };
```

## Quick Diagnostic

```bash
# 1. Start CLI serve (default port: 3456)
bun run packages/cli/src/index.ts serve examples/diagram.yaml

# 2. Test WebSocket with wscat (if installed)
wscat -c ws://localhost:3456

# 3. Send hello message
{"type":"hello","docId":"test"}

# 4. Check YAML is valid
bun run packages/cli/src/index.ts build examples/diagram.yaml
```

## Message Flow

```
Plugin                          CLI
  │                              │
  │──── HelloMessage ───────────►│  (docId, secret?)
  │                              │
  │◄──── FullMessage ───────────│  (rev, ir)
  │                              │
  │      [YAML file changes]     │
  │                              │
  │◄──── PatchMessage ──────────│  (baseRev, nextRev, ops)
  │                              │
  │      [Plugin reconnects]     │
  │                              │
  │──── RequestFullMessage ─────►│  (docId)
  │                              │
  │◄──── FullMessage ───────────│  (rev, ir)
  │                              │
```
