---
name: Sandboxing
description: Comprehensive guide to sandboxing AI agents including code execution isolation, resource limits, security boundaries, and safe tool execution
---

# Sandboxing

## Why Sandbox Agents?

**Problem:** Agents execute code and use tools - need isolation for safety

### Risks Without Sandboxing
```
Agent executes malicious code → Compromises system
Agent uses tool incorrectly → Deletes production data
Agent consumes too many resources → Crashes server
Agent accesses sensitive data → Data breach
```

### With Sandboxing
```
Agent runs in isolated environment
Limited resources (CPU, memory, time)
Restricted permissions
Cannot harm host system
```

---

## Sandboxing Strategies

### Process Isolation
```
Run agent in separate process
Kill process if misbehaves
Process cannot access host resources
```

### Container Isolation
```
Run agent in Docker container
Container has limited resources
Cannot access host filesystem
Network access restricted
```

### VM Isolation
```
Run agent in virtual machine
Strongest isolation
Highest overhead
```

---

## Code Execution Sandboxing

### Subprocess with Timeout
```python
import subprocess
import signal

def execute_code_sandboxed(code, timeout_seconds=5):
    """Execute code in subprocess with timeout"""
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=True
        )
        return {"success": True, "output": result.stdout}
    
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Execution timeout"}
    
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr}

# Usage
result = execute_code_sandboxed("print('Hello')", timeout_seconds=5)
```

### Docker Container
```python
import docker

def execute_code_in_docker(code, timeout_seconds=30):
    """Execute code in Docker container"""
    client = docker.from_env()
    
    try:
        # Run code in container
        container = client.containers.run(
            image="python:3.9-slim",
            command=["python", "-c", code],
            detach=True,
            mem_limit="256m",  # 256MB RAM limit
            cpu_quota=50000,   # 50% CPU limit
            network_disabled=True,  # No network access
            read_only=True,    # Read-only filesystem
            remove=True        # Auto-remove after execution
        )
        
        # Wait for completion with timeout
        result = container.wait(timeout=timeout_seconds)
        logs = container.logs().decode('utf-8')
        
        return {"success": result["StatusCode"] == 0, "output": logs}
    
    except docker.errors.ContainerError as e:
        return {"success": False, "error": str(e)}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

# Usage
result = execute_code_in_docker("print('Hello from Docker')")
```

### E2B (Code Interpreter)
```python
from e2b import Sandbox

def execute_code_e2b(code, timeout_seconds=30):
    """Execute code using E2B sandbox"""
    sandbox = Sandbox(timeout=timeout_seconds)
    
    try:
        result = sandbox.run_code(code)
        return {
            "success": True,
            "output": result.stdout,
            "error": result.stderr
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}
    
    finally:
        sandbox.close()
```

---

## Resource Limits

### CPU Limit
```python
import resource

def set_cpu_limit(seconds):
    """Limit CPU time"""
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, seconds))

# Usage
set_cpu_limit(5)  # Max 5 seconds of CPU time
```

### Memory Limit
```python
def set_memory_limit(bytes):
    """Limit memory usage"""
    resource.setrlimit(resource.RLIMIT_AS, (bytes, bytes))

# Usage
set_memory_limit(256 * 1024 * 1024)  # Max 256MB
```

### Docker Resource Limits
```python
container = client.containers.run(
    image="python:3.9-slim",
    command=["python", "script.py"],
    mem_limit="256m",      # Memory limit
    memswap_limit="256m",  # Memory + swap limit
    cpu_quota=50000,       # CPU limit (50%)
    pids_limit=100,        # Max 100 processes
    ulimits=[
        docker.types.Ulimit(name='nofile', soft=1024, hard=1024)  # Max 1024 open files
    ]
)
```

---

## File System Isolation

### Temporary Directory
```python
import tempfile
import os

def execute_with_temp_dir(code):
    """Execute code in temporary directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to temp directory
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        
        try:
            # Execute code
            exec(code)
        finally:
            # Restore original directory
            os.chdir(original_dir)
        
        # Temp directory automatically deleted
```

### Read-Only Filesystem
```python
# Docker with read-only filesystem
container = client.containers.run(
    image="python:3.9-slim",
    command=["python", "-c", code],
    read_only=True,  # Cannot write to filesystem
    tmpfs={'/tmp': 'size=100M'}  # Allow writes to /tmp only
)
```

---

## Network Isolation

### Disable Network Access
```python
# Docker without network
container = client.containers.run(
    image="python:3.9-slim",
    command=["python", "-c", code],
    network_disabled=True  # No network access
)
```

### Restricted Network Access
```python
# Docker with custom network (whitelist IPs)
network = client.networks.create(
    name="agent-network",
    driver="bridge",
    ipam=docker.types.IPAMConfig(
        pool_configs=[
            docker.types.IPAMPool(subnet="172.20.0.0/16")
        ]
    )
)

container = client.containers.run(
    image="python:3.9-slim",
    command=["python", "-c", code],
    network=network.name
)
```

---

## Tool Execution Sandboxing

### Whitelist Allowed Tools
```python
ALLOWED_TOOLS = {
    "search_web",
    "get_weather",
    "calculate"
}

def execute_tool(tool_name, params):
    """Execute tool only if whitelisted"""
    if tool_name not in ALLOWED_TOOLS:
        raise PermissionError(f"Tool '{tool_name}' not allowed")
    
    # Execute tool
    return tools[tool_name](**params)
```

### Parameter Validation
```python
def validate_tool_params(tool_name, params):
    """Validate tool parameters before execution"""
    
    if tool_name == "send_email":
        # Validate email address
        if not is_valid_email(params.get("to")):
            raise ValueError("Invalid email address")
        
        # Prevent sending to external domains
        if not params["to"].endswith("@company.com"):
            raise PermissionError("Can only send to @company.com")
    
    if tool_name == "delete_file":
        # Prevent deleting system files
        if params["path"].startswith("/system/"):
            raise PermissionError("Cannot delete system files")
    
    return True

def execute_tool_safe(tool_name, params):
    validate_tool_params(tool_name, params)
    return execute_tool(tool_name, params)
```

### Rate Limiting
```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self):
        self.calls = defaultdict(list)
    
    def check_limit(self, tool_name, max_calls=10, window_seconds=60):
        """Check if tool call is within rate limit"""
        now = time.time()
        
        # Remove old calls outside window
        self.calls[tool_name] = [
            t for t in self.calls[tool_name]
            if now - t < window_seconds
        ]
        
        # Check limit
        if len(self.calls[tool_name]) >= max_calls:
            raise Exception(f"Rate limit exceeded for {tool_name}")
        
        # Record call
        self.calls[tool_name].append(now)

rate_limiter = RateLimiter()

def execute_tool_with_rate_limit(tool_name, params):
    rate_limiter.check_limit(tool_name, max_calls=10, window_seconds=60)
    return execute_tool(tool_name, params)
```

---

## Monitoring Sandboxed Execution

### Track Resource Usage
```python
import psutil

def monitor_execution(process_id):
    """Monitor resource usage of sandboxed process"""
    process = psutil.Process(process_id)
    
    while process.is_running():
        cpu_percent = process.cpu_percent(interval=1)
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        print(f"CPU: {cpu_percent}%, Memory: {memory_mb:.1f}MB")
        
        # Kill if exceeds limits
        if cpu_percent > 80:
            process.kill()
            raise Exception("CPU limit exceeded")
        
        if memory_mb > 512:
            process.kill()
            raise Exception("Memory limit exceeded")
```

### Log Sandbox Events
```python
def log_sandbox_event(event_type, details):
    """Log sandbox events for audit"""
    logger.info({
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "details": details
    })

# Usage
log_sandbox_event("code_execution", {
    "code": code,
    "timeout": timeout_seconds,
    "success": result["success"]
})

log_sandbox_event("tool_execution", {
    "tool_name": tool_name,
    "params": params,
    "result": result
})
```

---

## Security Best Practices

### 1. Principle of Least Privilege
```python
# Good: Only allow necessary tools
ALLOWED_TOOLS = {"search_web", "calculate"}

# Bad: Allow all tools
ALLOWED_TOOLS = "*"
```

### 2. Validate All Inputs
```python
# Good
def execute_tool(tool_name, params):
    validate_tool_name(tool_name)
    validate_params(params)
    return tools[tool_name](**params)

# Bad
def execute_tool(tool_name, params):
    return tools[tool_name](**params)  # No validation
```

### 3. Set Resource Limits
```python
# Good
execute_code_sandboxed(code, timeout_seconds=30, memory_limit_mb=256)

# Bad
execute_code_sandboxed(code)  # No limits
```

### 4. Isolate Network Access
```python
# Good
container = client.containers.run(
    image="python:3.9-slim",
    network_disabled=True
)

# Bad
container = client.containers.run(
    image="python:3.9-slim"
)  # Full network access
```

### 5. Use Read-Only Filesystem
```python
# Good
container = client.containers.run(
    image="python:3.9-slim",
    read_only=True,
    tmpfs={'/tmp': 'size=100M'}
)

# Bad
container = client.containers.run(
    image="python:3.9-slim"
)  # Writable filesystem
```

---

## Tools and Services

### E2B (Code Interpreter)
```python
from e2b import Sandbox

sandbox = Sandbox()
result = sandbox.run_code("print('Hello')")
sandbox.close()
```

### Firecracker (Lightweight VMs)
```python
# AWS Lambda uses Firecracker for isolation
# Fast startup (<125ms)
# Strong isolation
```

### gVisor (Google)
```python
# Container runtime with additional isolation
# Used by Google Cloud Run
```

---

## Summary

**Sandboxing:** Isolate agent execution for safety

**Strategies:**
- Process isolation
- Container isolation (Docker)
- VM isolation

**Resource Limits:**
- CPU time
- Memory usage
- Disk I/O
- Network bandwidth

**File System:**
- Temporary directories
- Read-only filesystem
- Restricted paths

**Network:**
- Disable network
- Whitelist IPs/domains

**Tool Execution:**
- Whitelist allowed tools
- Validate parameters
- Rate limiting

**Best Practices:**
- Least privilege
- Validate inputs
- Set resource limits
- Isolate network
- Read-only filesystem

**Tools:**
- E2B (code interpreter)
- Docker (containers)
- Firecracker (lightweight VMs)
- gVisor (container isolation)
