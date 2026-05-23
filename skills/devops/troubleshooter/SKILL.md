---
name: dapr-troubleshooter
description: Proactively detect and diagnose DAPR runtime issues based on error patterns, log analysis, and common misconfigurations. Provides immediate solutions for service invocation failures, state management issues, pub/sub problems, and deployment errors. Use when encountering DAPR errors or unexpected behavior.
allowed-tools: Read, Grep, Glob, Bash
---

# DAPR Troubleshooter

This skill proactively detects DAPR issues and provides immediate solutions based on error patterns and common problems.

## When to Use

Claude automatically uses this skill when:
- Error messages contain DAPR-related keywords
- Application fails to connect to DAPR sidecar
- Service invocation returns errors
- State or pub/sub operations fail
- Deployment or startup issues occur

## Error Pattern Detection

### Connection Errors

**Pattern:** `connection refused`, `dial tcp`, `sidecar not ready`

```
Error: connection refused to localhost:3500
```

**Diagnosis:**
- DAPR sidecar is not running
- Wrong DAPR port configured
- Application started before sidecar

**Solutions:**
1. Verify DAPR is running: `dapr list`
2. Check sidecar health: `curl http://localhost:3500/v1.0/healthz`
3. Start with DAPR: `dapr run --app-id myapp -- python main.py`
4. In Kubernetes, check sidecar injection: `kubectl get pod -o yaml | grep dapr`

### Service Invocation Errors

**Pattern:** `404 Not Found`, `app-id not found`, `method not found`

```
Error: ERR_DIRECT_INVOKE: app id order-service not found
```

**Diagnosis:**
- Target service not running
- App-id mismatch (case-sensitive)
- Service not registered with DAPR

**Solutions:**
1. Verify target is running: `dapr list`
2. Check exact app-id (case-sensitive)
3. Ensure target has DAPR sidecar enabled
4. Check network connectivity between services

### State Store Errors

**Pattern:** `state store not found`, `failed to save state`, `ERR_STATE`

```
Error: state store statestore is not found
```

**Diagnosis:**
- State store component not configured
- Component name mismatch
- Backend service unavailable
- Authentication failure

**Solutions:**
1. Check component exists: `ls ./components/`
2. Verify component name matches code
3. Test backend connection (Redis, Cosmos, etc.)
4. Check secrets are accessible

### Pub/Sub Errors

**Pattern:** `pubsub not found`, `failed to publish`, `subscription error`

```
Error: pubsub pubsub is not configured
```

**Diagnosis:**
- Pub/sub component not configured
- Topic name mismatch
- Subscriber endpoint not registered
- Message handler error

**Solutions:**
1. Verify pubsub component exists
2. Check topic names match exactly
3. Ensure subscription route is registered
4. Return proper response from handler: `{"status": "SUCCESS"}`

### Component Configuration Errors

**Pattern:** `failed to init component`, `component error`, `invalid configuration`

```
Error: error initializing component statestore: connection refused
```

**Diagnosis:**
- Invalid component YAML
- Backend service not running
- Wrong credentials/connection string
- Missing required metadata

**Solutions:**
1. Validate YAML syntax
2. Start backend (Redis, etc.): `docker run -d -p 6379:6379 redis`
3. Check connection string/credentials
4. Verify all required metadata fields

### Workflow Errors

**Pattern:** `workflow not found`, `activity failed`, `workflow timeout`

```
Error: workflow order_workflow not found
```

**Diagnosis:**
- Workflow runtime not started
- Workflow not registered
- Activity not registered
- State store not configured

**Solutions:**
1. Ensure `wf_runtime.start()` is called
2. Check workflow is decorated with `@wf_runtime.workflow`
3. Verify activities are registered
4. Configure state store for workflow persistence

## Diagnostic Commands

### Check DAPR Installation
```bash
dapr --version
dapr status
```

### List Running Applications
```bash
dapr list
```

### View DAPR Logs
```bash
# Local
dapr logs --app-id myapp

# Kubernetes
kubectl logs deployment/myapp -c daprd
```

### Test Sidecar Health
```bash
curl http://localhost:3500/v1.0/healthz
```

### Check Loaded Components
```bash
curl http://localhost:3500/v1.0/metadata
```

### Test Service Invocation
```bash
curl http://localhost:3500/v1.0/invoke/target-app/method/health
```

### Test State Store
```bash
# Save state
curl -X POST http://localhost:3500/v1.0/state/statestore \
  -H "Content-Type: application/json" \
  -d '[{"key":"test","value":"hello"}]'

# Get state
curl http://localhost:3500/v1.0/state/statestore/test
```

### Test Pub/Sub
```bash
curl -X POST http://localhost:3500/v1.0/publish/pubsub/test-topic \
  -H "Content-Type: application/json" \
  -d '{"message":"test"}'
```

## Common Fixes Quick Reference

| Error | Quick Fix |
|-------|-----------|
| Sidecar not running | `dapr run --app-id myapp -- python main.py` |
| Redis not running | `docker run -d -p 6379:6379 redis` |
| Component not found | Check component file in `./components/` |
| App-id not found | Verify target app is running with `dapr list` |
| 404 on invoke | Check method path and HTTP verb |
| Pub/sub not delivering | Return `{"status": "SUCCESS"}` from handler |
| Secret not found | Configure secret store component |
| State save failed | Check state store backend is running |
| Workflow not starting | Call `wf_runtime.start()` |

## Environment Checklist

Run this checklist when troubleshooting:

```
[ ] DAPR CLI installed (dapr --version)
[ ] DAPR runtime initialized (dapr init)
[ ] Docker running (for local mode)
[ ] Application started with dapr run
[ ] Components in ./components/ directory
[ ] Component names match code references
[ ] Backend services running (Redis, etc.)
[ ] Correct ports configured
[ ] No firewall blocking localhost
[ ] Secrets configured if needed
```

## Log Analysis

### Key Log Patterns

```
# Successful startup
"dapr initialized. Status: Running"

# Component loaded
"component [statestore] loaded"

# Sidecar ready
"dapr sidecar is ready"

# Connection established
"connected to placement service"

# Errors to watch for
"error initializing component"
"failed to connect"
"connection refused"
"unauthorized"
"not found"
```

### Enable Debug Logging

```bash
# Local development
dapr run --log-level debug --app-id myapp -- python main.py

# Kubernetes
kubectl set env deployment/myapp DAPR_LOG_LEVEL=debug
```

## Integration with Other Skills

This troubleshooter integrates with:
- `config-validator` - Validates component YAML syntax
- `dapr-debugger` agent - Deep debugging assistance
- `azure-deployer` agent - Azure-specific troubleshooting
