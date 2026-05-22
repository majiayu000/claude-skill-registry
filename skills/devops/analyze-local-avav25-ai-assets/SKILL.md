---
name: analyze-local
description: Analyze local Docker environment — collect container status, logs, networking, resource usage, and diagnose issues. Applies SRE or DevOps roles for investigation. Use standalone or as part of local environment bugfixing.
context: fork
allowed-tools: Read, Grep, Glob, Bash
---

# Analyze Local Docker Environment

Systematic analysis of the local Docker environment. Collects container status, logs, networking, resource usage, and diagnoses issues. Works standalone or as an entry point for local bugfixing.

## 1. Clarify the Goal

Ask the user:

- **What is the problem or question?** (e.g., "container won't start", "service unreachable", "high memory usage", "just want a health check")
- **Which services are affected?** (specific container names, or "all")
- **When did the issue start?** (after a code change, config update, restart, or unknown)

If invoked as part of a bugfix flow — extract the problem statement from the parent context instead of asking.

## 2. Apply Appropriate Role

Select and apply the role based on the problem type:

| Problem Type | Primary Role | Rationale |
|---|---|---|
| Container crashes, restarts, health checks | `Agent(sre-engineer)` | Reliability, observability, troubleshooting |
| Networking, DNS, port conflicts, connectivity | `Agent(sre-engineer)` | K8s/Docker networking diagnostics |
| Dockerfile, image builds, compose config | `Agent(devops-engineer)` | Container orchestration, Docker expertise |
| CI/CD pipeline failures in local env | `Agent(devops-engineer)` | Build and deploy pipeline expertise |
| Resource exhaustion (CPU, memory, disk) | `Agent(sre-engineer)` | Capacity, resource management |
| Application errors visible in logs | Stack-specific role | `Agent(java-engineer)`, `Agent(python-engineer)`, `Agent(frontend-engineer)` based on service stack |
| General / unclear | `Agent(software-engineer)` | Broad debugging methodology |

Announce the applied role to the user. If multiple problem types are present, apply multiple roles.

## 3. Collect Environment Snapshot

Run the following diagnostic commands to gather the current state. Present results as a structured summary.

### 3a. Docker Daemon and System

```
// turbo
docker version
docker info --format '{{.OperatingSystem}} | Containers: {{.Containers}} (Running: {{.ContainersRunning}}, Stopped: {{.ContainersStopped}}) | Images: {{.Images}}'
docker system df
```

**Record**: Docker version, OS, total containers, disk usage.

### 3b. Container Status

```
// turbo
docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.State}}"
```

**Record**: For each container — name, image, status (Up/Exited/Restarting), ports, uptime.

**Flag issues**:
- Containers in `Exited` or `Restarting` state
- Containers with `unhealthy` health status
- Missing containers that should be running (ask user for expected services)

### 3c. Docker Compose (if applicable)

If a `docker-compose.yml` or `compose.yaml` is present in the project:

```
// turbo
docker compose ps -a
docker compose config --services
```

**Record**: Compose project name, service list, which services are up/down.

### 3d. Logs for Problematic Containers

For each container flagged in 3b (or the user-specified service):

```
docker logs --tail 100 --timestamps <container_name>
```

**Record**: Last 100 lines of logs. Look for:
- Error messages, stack traces, exceptions
- Connection refused / timeout errors
- OOM killed signals
- Configuration errors (missing env vars, wrong paths)

### 3e. Networking

```
// turbo
docker network ls
docker network inspect <network_name>
```

For connectivity issues:
```
docker exec <container> ping -c 2 <target_host>
docker exec <container> nslookup <service_name>
docker port <container>
```

**Record**: Networks, container IP assignments, port mappings, DNS resolution.

### 3f. Resource Usage

```
// turbo
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"
```

**Record**: CPU %, memory usage/limit, network I/O, block I/O per container.

**Flag issues**:
- Memory usage > 80% of limit
- CPU consistently > 90%
- Containers without memory limits set

### 3g. Volumes and Mounts

```
// turbo
docker volume ls
docker inspect --format '{{range .Mounts}}{{.Type}}: {{.Source}} -> {{.Destination}} ({{.Mode}}){{"\n"}}{{end}}' <container_name>
```

**Record**: Volume mounts, bind mounts, permissions (ro/rw).

## 4. Analyze Findings

Using the applied role's expertise, analyze the collected data:

1. **Correlate**: Match the user's problem statement with the diagnostic data
2. **Identify root cause**: Use the applied role's debugging methodology
3. **Check common causes** (in order of likelihood):

<common_issues>
- **Container won't start**: Missing env vars, wrong image tag, port conflict, entrypoint error, missing volume mount
- **Service unreachable**: Wrong port mapping, network mismatch, DNS not resolving, firewall/security group, service not listening on 0.0.0.0
- **Container restarts repeatedly**: OOM killed (check `docker inspect` for OOMKilled), health check failing, application crash loop, dependency not ready
- **Slow performance**: Resource limits too low, no memory limit (swapping), disk I/O bottleneck, too many containers for available resources
- **Build failures**: Dockerfile syntax, missing build context files, base image unavailable, layer cache invalidation
- **Volume/data issues**: Permission denied (user mismatch), stale volume data, bind mount path wrong on host
</common_issues>

## 5. Present Diagnosis

Structure the diagnosis as:

```
## Environment Summary
- Docker: [version], [OS]
- Containers: [running]/[total] | Compose: [yes/no]
- Disk usage: [used/available]

## Findings
### [Issue 1: title]
- **Symptom**: what was observed
- **Evidence**: specific log lines, metrics, or status
- **Root cause**: why it's happening
- **Severity**: critical / warning / info

### [Issue 2: title]
...

## Recommendations
1. [Fix for issue 1] — [command or config change]
2. [Fix for issue 2] — [command or config change]
...

## Environment Health: [HEALTHY | DEGRADED | CRITICAL]
```

## 6. Fix or Escalate

Based on the diagnosis:

- **If fix is straightforward** (restart, config change, env var): Propose the fix and apply after user approval
- **If fix requires code changes**: Transition to the appropriate stack-specific role and apply the bugfix following the role's debugging methodology
- **If fix requires infrastructure changes** (Dockerfile, compose, networking): Apply with `Agent(devops-engineer)` patterns
- **If root cause is unclear**: Propose additional diagnostic steps (increase log verbosity, attach to container, profile resource usage)

After applying any fix, re-run the relevant diagnostic commands from Step 3 to verify the fix resolved the issue.

## 7. Summary

Present the completed analysis:

- **Problem**: original user report
- **Role(s) applied**: which roles were used
- **Root cause**: what was found
- **Fix applied**: what was changed (or "no fix needed — environment is healthy")
- **Verification**: confirmation that the issue is resolved
- **Prevention**: recommendations to avoid recurrence (e.g., add health checks, set resource limits, pin image versions)

## Integration

- **Called by**: `/bugfix` (environment diagnostics step)
- **Roles**: `Agent(devops-engineer)`, `Agent(sre-engineer)`
