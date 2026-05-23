---
name: process-substitution-fifos
description: Process substitution, named pipes (FIFOs), and advanced IPC patterns for efficient bash data streaming (2025)
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

# Process Substitution & FIFOs (2025)

## Overview

Master advanced inter-process communication patterns in bash using process substitution, named pipes (FIFOs), and efficient data streaming techniques. These patterns enable powerful data pipelines without temporary files.

## Process Substitution Basics

### Input Process Substitution `<(command)`

```bash
#!/usr/bin/env bash
set -euo pipefail

# Compare two command outputs
diff <(sort file1.txt) <(sort file2.txt)

# Compare remote and local files
diff <(ssh server 'cat /etc/config') /etc/config

# Merge sorted files
sort -m <(sort file1.txt) <(sort file2.txt) <(sort file3.txt)

# Read from multiple sources simultaneously
paste <(cut -f1 data.tsv) <(cut -f3 data.tsv)

# Feed command output to programs expecting files
# Many programs require filename arguments, not stdin
wc -l <(grep "error" *.log)

# Process API response with tool expecting file
jq '.items[]' <(curl -s "https://api.example.com/data")

# Source environment from command output
source <(aws configure export-credentials --format env)

# Feed to while loop without subshell issues
while IFS= read -r line; do
    ((count++))
    process "$line"
done < <(find . -name "*.txt")
echo "Processed $count files"  # Variable survives!
```

### Output Process Substitution `>(command)`

```bash
#!/usr/bin/env bash
set -euo pipefail

# Write to multiple destinations simultaneously (tee alternative)
echo "Log message" | tee >(logger -t myapp) >(mail -s "Alert" admin@example.com)

# Compress and checksum in one pass
tar cf - /data | tee >(gzip > backup.tar.gz) >(sha256sum > backup.sha256)

# Send output to multiple processors
generate_data | tee >(processor1 > result1.txt) >(processor2 > result2.txt) > /dev/null

# Log and process simultaneously
./build.sh 2>&1 | tee >(grep -i error > errors.log) >(grep -i warning > warnings.log)

# Real-time filtering with multiple outputs
tail -f /var/log/syslog | tee \
    >(grep --line-buffered "ERROR" >> errors.log) \
    >(grep --line-buffered "WARNING" >> warnings.log) \
    >(grep --line-buffered "CRITICAL" | mail -s "Critical Alert" admin@example.com)
```

### Combining Input and Output Substitution

```bash
#!/usr/bin/env bash
set -euo pipefail

# Transform and compare
diff <(sort input.txt | uniq) <(sort reference.txt | uniq)

# Pipeline with multiple branches
cat data.csv | tee \
    >(awk -F, '{print $1}' > column1.txt) \
    >(awk -F, '{print $2}' > column2.txt) \
    | wc -l

# Complex data flow
process_data() {
    local input="$1"

    # Read from process substitution, write to multiple outputs
    while IFS= read -r line; do
        echo "$line" | tee \
            >(echo "LOG: $line" >> "$log_file") \
            >(process_line "$line" >> results.txt)
    done < <(cat "$input" | filter_input)
}
```

## Named Pipes (FIFOs)

### Creating and Using FIFOs

```bash
#!/usr/bin/env bash
set -euo pipefail

# Create FIFO
mkfifo my_pipe

# Clean up on exit
trap 'rm -f my_pipe' EXIT

# Writer (in background or separate terminal)
echo "Hello from writer" > my_pipe &

# Reader (blocks until data available)
cat < my_pipe

# With timeout (using read)
if read -t 5 line < my_pipe; then
    echo "Received: $line"
else
    echo "Timeout waiting for data"
fi
```

### Bidirectional Communication

```bash
#!/usr/bin/env bash
set -euo pipefail

# Create two FIFOs for bidirectional communication
REQUEST_PIPE="/tmp/request_$$"
RESPONSE_PIPE="/tmp/response_$$"

mkfifo "$REQUEST_PIPE" "$RESPONSE_PIPE"
trap 'rm -f "$REQUEST_PIPE" "$RESPONSE_PIPE"' EXIT

# Server process
server() {
    while true; do
        if read -r request < "$REQUEST_PIPE"; then
            case "$request" in
                "QUIT")
                    echo "BYE" > "$RESPONSE_PIPE"
                    break
                    ;;
                "TIME")
                    date > "$RESPONSE_PIPE"
                    ;;
                "UPTIME")
                    uptime > "$RESPONSE_PIPE"
                    ;;
                *)
                    echo "UNKNOWN: $request" > "$RESPONSE_PIPE"
                    ;;
            esac
        fi
    done
}

# Client function
send_request() {
    local request="$1"
    echo "$request" > "$REQUEST_PIPE"
    cat < "$RESPONSE_PIPE"
}

# Start server in background
server &
SERVER_PID=$!

# Send requests
send_request "TIME"
send_request "UPTIME"
send_request "QUIT"

wait "$SERVER_PID"
```

### Producer-Consumer Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

WORK_QUEUE="/tmp/work_queue_$$"
mkfifo "$WORK_QUEUE"
trap 'rm -f "$WORK_QUEUE"' EXIT

# Producer
producer() {
    local item
    for item in {1..100}; do
        echo "TASK:$item"
    done
    echo "DONE"
}

# Consumer (can have multiple)
consumer() {
    local id="$1"
    while read -r item; do
        [[ "$item" == "DONE" ]] && break
        echo "Consumer $id processing: $item"
        sleep 0.1  # Simulate work
    done
}

# Start consumers (they'll block waiting for data)
consumer 1 < "$WORK_QUEUE" &
consumer 2 < "$WORK_QUEUE" &
consumer 3 < "$WORK_QUEUE" &

# Start producer
producer > "$WORK_QUEUE"

wait
echo "All work complete"
```

### FIFO with File Descriptors

```bash
#!/usr/bin/env bash
set -euo pipefail

FIFO="/tmp/fd_fifo_$$"
mkfifo "$FIFO"
trap 'rm -f "$FIFO"' EXIT

# Open FIFO for read/write on FD 3
# Opening for both prevents blocking on open
exec 3<>"$FIFO"

# Write to FIFO via FD
echo "Message 1" >&3
echo "Message 2" >&3

# Read from FIFO via FD
read -r msg1 <&3
read -r msg2 <&3
echo "Got: $msg1, $msg2"

# Close FD
exec 3>&-
```

## Coprocess (Bash 4+)

### Basic Coprocess Usage

```bash
#!/usr/bin/env bash
set -euo pipefail

# Start coprocess (bidirectional pipe)
coproc BC { bc -l; }

# Send data to coprocess
echo "scale=10; 355/113" >&"${BC[1]}"

# Read result
read -r result <&"${BC[0]}"
echo "Pi approximation: $result"

# More calculations
echo "sqrt(2)" >&"${BC[1]}"
read -r sqrt2 <&"${BC[0]}"
echo "Square root of 2: $sqrt2"

# Close write end to signal EOF
exec {BC[1]}>&-

# Wait for coprocess to finish
wait "$BC_PID"
```

### Named Coprocess

```bash
#!/usr/bin/env bash
set -euo pipefail

# Named coprocess for Python interpreter
coproc PYTHON { python3 -u -c "
import sys
for line in sys.stdin:
    exec(line.strip())
"; }

# Send Python commands
echo "print('Hello from Python')" >&"${PYTHON[1]}"
read -r output <&"${PYTHON[0]}"
echo "Python said: $output"

echo "print(2**100)" >&"${PYTHON[1]}"
read -r big_num <&"${PYTHON[0]}"
echo "2^100 = $big_num"

# Cleanup
exec {PYTHON[1]}>&-
wait "$PYTHON_PID" 2>/dev/null || true
```

### Coprocess Pool Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

# Create pool of worker coprocesses
declare -A WORKERS
declare -A WORKER_PIDS

start_workers() {
    local count="$1"
    local i

    for ((i=0; i<count; i++)); do
        # Each worker runs a processing loop
        coproc "WORKER_$i" {
            while IFS= read -r task; do
                [[ "$task" == "QUIT" ]] && exit 0
                # Simulate work
                sleep 0.1
                echo "DONE:$task"
            done
        }

        # Store FDs dynamically
        local -n write_fd="WORKER_${i}[1]"
        local -n read_fd="WORKER_${i}[0]"
        local -n pid="WORKER_${i}_PID"

        WORKERS["$i,in"]="$write_fd"
        WORKERS["$i,out"]="$read_fd"
        WORKER_PIDS["$i"]="$pid"
    done
}

# Note: Coprocess pool management is complex
# Consider GNU Parallel for production workloads
```

## Advanced Patterns

### Progress Monitoring with FIFO

```bash
#!/usr/bin/env bash
set -euo pipefail

PROGRESS_PIPE="/tmp/progress_$$"
mkfifo "$PROGRESS_PIPE"
trap 'rm -f "$PROGRESS_PIPE"' EXIT

# Progress monitor
monitor_progress() {
    local total="$1"
    local current=0

    while read -r update; do
        ((current++))
        local pct=$((current * 100 / total))
        printf "\rProgress: [%-50s] %d%%" \
            "$(printf '#%.0s' $(seq 1 $((pct/2))))" "$pct"
    done < "$PROGRESS_PIPE"
    echo
}

# Worker that reports progress
do_work() {
    local items=("$@")
    local item

    for item in "${items[@]}"; do
        process_item "$item"
        echo "done" > "$PROGRESS_PIPE"
    done
}

# Usage
items=(item1 item2 item3 ... item100)
monitor_progress "${#items[@]}" &
MONITOR_PID=$!

do_work "${items[@]}"

exec 3>"$PROGRESS_PIPE"  # Keep pipe open
exec 3>&-                 # Close to signal completion
wait "$MONITOR_PID"
```

### Log Aggregator with Multiple FIFOs

```bash
#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="/tmp/logs_$$"
mkdir -p "$LOG_DIR"

# Create FIFOs for each log level
for level in DEBUG INFO WARN ERROR; do
    mkfifo "$LOG_DIR/$level"
done

trap 'rm -rf "$LOG_DIR"' EXIT

# Aggregator process
aggregate_logs() {
    local output_file="$1"

    # Open all FIFOs for reading
    exec 3<"$LOG_DIR/DEBUG"
    exec 4<"$LOG_DIR/INFO"
    exec 5<"$LOG_DIR/WARN"
    exec 6<"$LOG_DIR/ERROR"

    while true; do
        # Use select-like behavior with read timeout
        read -t 0.1 -r msg <&3 && echo "[DEBUG] $(date '+%H:%M:%S') $msg" >> "$output_file"
        read -t 0.1 -r msg <&4 && echo "[INFO]  $(date '+%H:%M:%S') $msg" >> "$output_file"
        read -t 0.1 -r msg <&5 && echo "[WARN]  $(date '+%H:%M:%S') $msg" >> "$output_file"
        read -t 0.1 -r msg <&6 && echo "[ERROR] $(date '+%H:%M:%S') $msg" >> "$output_file"
    done
}

# Logging functions
log_debug() { echo "$*" > "$LOG_DIR/DEBUG"; }
log_info()  { echo "$*" > "$LOG_DIR/INFO"; }
log_warn()  { echo "$*" > "$LOG_DIR/WARN"; }
log_error() { echo "$*" > "$LOG_DIR/ERROR"; }

# Start aggregator
aggregate_logs "/var/log/app.log" &
AGGREGATOR_PID=$!

# Application code uses logging functions
log_info "Application started"
log_debug "Processing item"
log_warn "Resource running low"
log_error "Critical failure"

# Cleanup
kill "$AGGREGATOR_PID" 2>/dev/null
```

### Data Pipeline with Buffering

```bash
#!/usr/bin/env bash
set -euo pipefail

# Buffered pipeline stage
buffered_stage() {
    local name="$1"
    local buffer_size="${2:-100}"
    local buffer=()

    while IFS= read -r line || [[ ${#buffer[@]} -gt 0 ]]; do
        if [[ -n "$line" ]]; then
            buffer+=("$line")
        fi

        # Flush when buffer full or EOF
        if [[ ${#buffer[@]} -ge $buffer_size ]] || [[ -z "$line" && ${#buffer[@]} -gt 0 ]]; then
            printf '%s\n' "${buffer[@]}" | process_batch
            buffer=()
        fi
    done
}

# Parallel pipeline with process substitution
run_parallel_pipeline() {
    local input="$1"

    cat "$input" | \
        tee >(filter_a | transform_a > output_a.txt) \
            >(filter_b | transform_b > output_b.txt) \
            >(filter_c | transform_c > output_c.txt) \
        > /dev/null

    # Wait for all background processes
    wait
}
```

### Streaming JSON Processing

```bash
#!/usr/bin/env bash
set -euo pipefail

# Stream JSON array elements
stream_json_array() {
    local url="$1"

    # Use jq to stream array elements one per line
    curl -s "$url" | jq -c '.items[]' | while IFS= read -r item; do
        process_json_item "$item"
    done
}

# Parallel JSON processing with process substitution
parallel_json_process() {
    local input="$1"
    local workers=4

    # Split input across workers
    jq -c '.[]' "$input" | \
        parallel --pipe -N100 --jobs "$workers" '
            while IFS= read -r item; do
                echo "$item" | jq ".processed = true"
            done
        ' | jq -s '.'
}

# Transform JSON stream
transform_json_stream() {
    jq -c '.' | while IFS= read -r obj; do
        # Process with bash
        local id
        id=$(echo "$obj" | jq -r '.id')

        # Enrich and output
        echo "$obj" | jq --arg ts "$(date -Iseconds)" '. + {timestamp: $ts}'
    done
}
```

## Bash 5.3 In-Shell Substitution

### No-Fork Command Substitution

```bash
#!/usr/bin/env bash
# Requires Bash 5.3+
set -euo pipefail

# Traditional: forks subshell
result=$(echo "hello")

# Bash 5.3: No fork, runs in current shell
result=${ echo "hello"; }

# Significant for variable modifications
counter=0
# Traditional - counter stays 0 (subshell)
result=$(counter=$((counter + 1)); echo "$counter")
echo "Counter: $counter"  # Still 0

# Bash 5.3 - counter is modified (same shell)
result=${ counter=$((counter + 1)); echo "$counter"; }
echo "Counter: $counter"  # Now 1

# REPLY variable syntax (even more concise)
${ REPLY="computed value"; }
echo "$REPLY"

# Or using ${| } syntax
${| REPLY=$(expensive_computation); }
echo "Result: $REPLY"
```

### Performance-Critical Pipelines

```bash
#!/usr/bin/env bash
# Requires Bash 5.3+
set -euo pipefail

# Build result without forks
build_path() {
    local parts=("$@")
    local result=""

    for part in "${parts[@]}"; do
        # No fork for each concatenation
        result=${ printf '%s/%s' "$result" "$part"; }
    done

    echo "${result#/}"
}

# Accumulate values efficiently
accumulate() {
    local -n arr="$1"
    local sum=0

    for val in "${arr[@]}"; do
        # In-shell arithmetic capture
        sum=${ echo $((sum + val)); }
    done

    echo "$sum"
}
```

## Error Handling in Pipelines

### Pipeline Error Detection

```bash
#!/usr/bin/env bash
set -euo pipefail

# Check all pipeline stages
run_pipeline() {
    local result

    # pipefail ensures we catch errors in any stage
    if ! result=$(stage1 | stage2 | stage3); then
        echo "Pipeline failed" >&2
        return 1
    fi

    echo "$result"
}

# PIPESTATUS for detailed error info
run_with_status() {
    cmd1 | cmd2 | cmd3

    local -a status=("${PIPESTATUS[@]}")

    for i in "${!status[@]}"; do
        if [[ "${status[$i]}" -ne 0 ]]; then
            echo "Stage $i failed with status ${status[$i]}" >&2
        fi
    done

    # Return highest exit status
    local max=0
    for s in "${status[@]}"; do
        ((s > max)) && max="$s"
    done
    return "$max"
}
```

### Cleanup on Pipeline Failure

```bash
#!/usr/bin/env bash
set -euo pipefail

# Track resources for cleanup
declare -a CLEANUP_PIDS=()
declare -a CLEANUP_FILES=()

cleanup() {
    local pid file

    for pid in "${CLEANUP_PIDS[@]}"; do
        kill "$pid" 2>/dev/null || true
    done

    for file in "${CLEANUP_FILES[@]}"; do
        rm -f "$file" 2>/dev/null || true
    done
}

trap cleanup EXIT

# Register cleanup
register_pid() { CLEANUP_PIDS+=("$1"); }
register_file() { CLEANUP_FILES+=("$1"); }

# Example usage
run_safe_pipeline() {
    local fifo="/tmp/pipeline_$$"
    mkfifo "$fifo"
    register_file "$fifo"

    producer > "$fifo" &
    register_pid "$!"

    consumer < "$fifo" &
    register_pid "$!"

    wait
}
```

## Best Practices

### FIFO Naming Convention

```bash
#!/usr/bin/env bash
set -euo pipefail

# Include PID and descriptive name
create_fifo() {
    local name="$1"
    local fifo="/tmp/${name}_$$_$(date +%s)"
    mkfifo -m 600 "$fifo"  # Restrictive permissions
    echo "$fifo"
}

# Use tmpdir for security
create_secure_fifo() {
    local name="$1"
    local tmpdir
    tmpdir=$(mktemp -d)
    local fifo="$tmpdir/$name"
    mkfifo -m 600 "$fifo"
    echo "$fifo"
}
```

### Preventing Deadlocks

```bash
#!/usr/bin/env bash
set -euo pipefail

# ✗ DEADLOCK - writer blocks, reader never starts
# mkfifo pipe
# echo "data" > pipe  # Blocks forever

# ✓ SAFE - open both ends or use background
mkfifo pipe
trap 'rm -f pipe' EXIT

# Option 1: Background writer
echo "data" > pipe &
cat < pipe

# Option 2: Open for read/write
exec 3<>pipe
echo "data" >&3
read -r data <&3
exec 3>&-

# Option 3: Non-blocking open (requires careful handling)
exec 3<pipe &
exec 4>pipe
echo "data" >&4
read -r data <&3
```

### Timeout Patterns

```bash
#!/usr/bin/env bash
set -euo pipefail

# Read with timeout
read_with_timeout() {
    local fifo="$1"
    local timeout="$2"
    local result

    if read -t "$timeout" -r result < "$fifo"; then
        echo "$result"
        return 0
    else
        echo "Timeout after ${timeout}s" >&2
        return 1
    fi
}

# Write with timeout (using timeout command)
write_with_timeout() {
    local fifo="$1"
    local timeout="$2"
    local data="$3"

    if timeout "$timeout" bash -c "echo '$data' > '$fifo'"; then
        return 0
    else
        echo "Write timeout after ${timeout}s" >&2
        return 1
    fi
}
```

## Resources

- [Bash Reference - Process Substitution](https://www.gnu.org/software/bash/manual/html_node/Process-Substitution.html)
- [Bash Reference - Coprocesses](https://www.gnu.org/software/bash/manual/html_node/Coprocesses.html)
- [BashFAQ - Process Substitution](https://mywiki.wooledge.org/ProcessSubstitution)
- [Named Pipes (FIFOs)](https://www.gnu.org/software/libc/manual/html_node/FIFO-Special-Files.html)

---

**Master process substitution and FIFOs for efficient inter-process communication without temporary files.**
