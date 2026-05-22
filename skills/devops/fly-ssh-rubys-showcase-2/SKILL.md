---
name: fly-ssh
description: Use when asked to run "fly ssh console", SSH into Fly.io machines, inspect files on production machines, check processes on Fly.io, or examine deployed machine state. Covers critical pitfalls like no shell support and Debian vs macOS command differences.
---

# Fly SSH Console Usage

## Critical Considerations

### 1. Machine Must Be Running

Fly.io machines may be stopped. Before using `fly ssh console`, ensure a machine is running:

**Option A: Start machine explicitly**
```bash
# List machines to find IDs
fly machines list -a smooth-nav

# Start a specific machine
fly machine start <machine-id> -a smooth-nav
```

**Option B: Wake machine with HTTP request**
```bash
# Fetch a page to auto-start the machine
curl -I https://smooth-nav.fly.dev/
```

### 2. No Shell - Direct Command Execution Only

`fly ssh console` executes commands directly, **not through a shell**. This means:

❌ **Don't use**:
- Pipes: `ps aux | grep puma`
- Redirection: `echo "test" > file.txt`
- Shell operators: `&&`, `||`, `;`
- Shell expansions: `*.txt`, `~`, `$HOME`

✅ **Do use**:
- Direct commands: `ps auxww`
- Multiple separate `fly ssh console` calls for complex operations
- Command-specific options instead of pipes

**Example - Wrong vs Right**:
```bash
# ❌ Wrong (pipe won't work)
fly ssh console -a smooth-nav -C "ps aux | grep puma"

# ✅ Right (use grep command directly)
fly ssh console -a smooth-nav -C "ps auxww" | grep puma

# Or use ps filtering
fly ssh console -a smooth-nav -C "ps -C puma -o pid,user,%mem,%cpu,command"
```

### 3. Debian Linux Commands (Not macOS)

The Fly.io machines run **Debian Linux**, which has different command options than macOS.

#### Common Differences

**ps command**:
```bash
# ❌ macOS syntax (doesn't work on Linux)
fly ssh console -a smooth-nav -C "ps auxww -o %mem"

# ✅ Debian Linux syntax
fly ssh console -a smooth-nav -C "ps auxww"
fly ssh console -a smooth-nav -C "ps -eo pid,user,%mem,%cpu,command"
fly ssh console -a smooth-nav -C "ps -C navigator -o pid,%mem,command"
```

**Memory inspection**:
```bash
# Show all processes with memory usage
fly ssh console -a smooth-nav -C "ps auxww"

# Show specific process
fly ssh console -a smooth-nav -C "ps -C navigator -o pid,user,%mem,vsz,rss,command"

# Show top memory consumers
fly ssh console -a smooth-nav -C "ps aux --sort=-%mem | head -20"
```

**File operations**:
```bash
# List files
fly ssh console -a smooth-nav -C "ls -lah /data/db"

# Read file
fly ssh console -a smooth-nav -C "cat /rails/config/navigator.yml"

# Check disk usage
fly ssh console -a smooth-nav -C "df -h"
```

## Common Use Cases

### Memory Usage Analysis

```bash
# Get comprehensive process list with memory
fly ssh console -a smooth-nav -C "ps auxww"

# Show only relevant processes (filter locally)
fly ssh console -a smooth-nav -C "ps auxww" | grep -E 'navigator|puma|redis'

# Check specific process memory
fly ssh console -a smooth-nav -C "ps -C navigator -o pid,user,%mem,vsz,rss,command"
```

**Understanding ps memory columns**:
- `%MEM` - Percentage of physical RAM used
- `VSZ` - Virtual memory size (KB)
- `RSS` - Resident Set Size (actual physical memory in KB)

### Process Inspection

```bash
# List all running processes
fly ssh console -a smooth-nav -C "ps auxww"

# Check if specific process is running
fly ssh console -a smooth-nav -C "ps -C puma -o pid,command"

# Show process tree
fly ssh console -a smooth-nav -C "ps auxwwf"

# Count processes by name
fly ssh console -a smooth-nav -C "ps aux" | grep -c puma
```

### File and Directory Inspection

```bash
# List databases
fly ssh console -a smooth-nav -C "ls -lh /data/db/*.sqlite3"

# Check configuration
fly ssh console -a smooth-nav -C "cat /rails/config/navigator.yml"

# Check logs (most recent lines)
fly ssh console -a smooth-nav -C "tail -100 /data/log/production.log"

# Check disk space
fly ssh console -a smooth-nav -C "df -h /data"
```

### Network and Port Inspection

```bash
# Check listening ports
fly ssh console -a smooth-nav -C "netstat -tlnp"

# Check specific port
fly ssh console -a smooth-nav -C "netstat -tlnp" | grep 28080
```

## Region-Specific Commands

```bash
# Specify region
fly ssh console -a smooth-nav -r iad -C "ps auxww"

# List available regions
fly regions list -a smooth-nav
```

## Multi-Application Commands

```bash
# Compare smooth-nav (with optimizations)
fly ssh console -a smooth-nav -C "ps auxww" | grep -E 'navigator|puma|redis'

# Compare smooth (original)
fly ssh console -a smooth -C "ps auxww" | grep -E 'navigator|puma|redis'
```

## Debugging Tips

### Check if machine is accessible
```bash
# Ping the machine
fly ssh console -a smooth-nav -C "echo ok"
```

### Check Navigator status
```bash
# Check if Navigator is running
fly ssh console -a smooth-nav -C "ps -C navigator -o pid,user,command"

# Check Navigator version
fly ssh console -a smooth-nav -C "navigator --version"
```

### Check Rails processes
```bash
# Check Action Cable
fly ssh console -a smooth-nav -C "ps auxww" | grep "cable/config.ru"

# Check tenant Rails apps
fly ssh console -a smooth-nav -C "ps auxww" | grep "rails/config.ru"
```

### Verify environment
```bash
# Check environment variables (for specific process)
fly ssh console -a smooth-nav -C "cat /proc/1/environ" | tr '\0' '\n'
```

## Performance Considerations

- Each `fly ssh console` call incurs network latency
- For complex analysis, consider multiple separate calls rather than trying to use shell features
- Filter output locally (on your machine) rather than trying to filter remotely

## Example Workflows

### Analyze memory after deployment
```bash
# 1. Ensure machine is running
curl -I https://smooth-nav.fly.dev/

# 2. Wait a few seconds for cold start to complete
sleep 5

# 3. Get process list
fly ssh console -a smooth-nav -C "ps auxww" > /tmp/smooth-nav-ps.txt

# 4. Analyze locally
grep -E 'navigator|puma|redis' /tmp/smooth-nav-ps.txt
```

### Compare memory usage across apps
```bash
# Get both process lists
fly ssh console -a smooth-nav -C "ps auxww" > /tmp/nav-ps.txt
fly ssh console -a smooth -C "ps auxww" > /tmp/smooth-ps.txt

# Compare
echo "=== smooth-nav ==="
grep -E 'navigator|puma|redis' /tmp/nav-ps.txt

echo "=== smooth ==="
grep -E 'navigator|puma|redis' /tmp/smooth-ps.txt
```

### Check if Action Cable is running
```bash
# Quick check
fly ssh console -a smooth-nav -C "ps auxww" | grep -q "cable/config.ru" && echo "Action Cable running" || echo "Action Cable NOT running"
```

## Common Errors and Solutions

### Error: "no machines available"
**Solution**: Machine is stopped. Start it with `fly machine start` or trigger with HTTP request.

### Error: "connection refused"
**Solution**: Machine might be starting. Wait 10-30 seconds and retry.

### Error: "command not found"
**Solution**: Verify the command exists in Debian. Check available commands with:
```bash
fly ssh console -a smooth-nav -C "which <command>"
```

### Pipe or redirection doesn't work
**Solution**: Don't use shell operators in `-C` argument. Filter/redirect on your local machine instead.
