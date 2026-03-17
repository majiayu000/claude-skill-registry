---
name: parallel-processing-patterns
description: Parallel and concurrent processing patterns in bash including GNU Parallel, xargs, job pools, and async patterns (2025)
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

# Parallel Processing Patterns in Bash (2025)

## Overview

Comprehensive guide to parallel and concurrent execution in bash, covering GNU Parallel, xargs parallelization, job control, worker pools, and modern async patterns for maximum performance.

## GNU Parallel (Recommended)

### Installation

```bash
# Debian/Ubuntu
sudo apt-get install parallel

# macOS
brew install parallel

# From source
wget https://ftp.gnu.org/gnu/parallel/parallel-latest.tar.bz2
tar -xjf parallel-latest.tar.bz2
cd parallel-*
./configure && make && sudo make install
```

### Basic Usage

```bash
#!/usr/bin/env bash
set -euo pipefail

# Process multiple files in parallel
parallel gzip ::: *.txt

# Equivalent to:
# for f in *.txt; do gzip "$f"; done
# But runs in parallel!

# Using find with parallel
find . -name "*.jpg" | parallel convert {} -resize 50% resized/{}

# Specify number of jobs
parallel -j 8 process_file ::: *.dat

# From stdin
cat urls.txt | parallel -j 10 wget -q

# Multiple inputs
parallel echo ::: A B C ::: 1 2 3
# Output: A 1, A 2, A 3, B 1, B 2, B 3, C 1, C 2, C 3

# Paired inputs with :::+
parallel echo ::: A B C :::+ 1 2 3
# Output: A 1, B 2, C 3
```

### Input Handling

```bash
#!/usr/bin/env bash
set -euo pipefail

# Input from file
parallel -a input.txt process_line

# Multiple input files
parallel -a file1.txt -a file2.txt 'echo {1} {2}'

# Column-based input
cat data.tsv | parallel --colsep '\t' 'echo Name: {1}, Value: {2}'

# Named columns
cat data.csv | parallel --header : --colsep ',' 'echo {name}: {value}'

# Null-delimited for safety with special characters
find . -name "*.txt" -print0 | parallel -0 wc -l

# Line-based chunking
cat huge_file.txt | parallel --pipe -N1000 'wc -l'
```

### Replacement Strings

```bash
#!/usr/bin/env bash
set -euo pipefail

# {} - Full input
parallel echo 'Processing: {}' ::: file1.txt file2.txt

# {.} - Remove extension
parallel echo '{.}' ::: file.txt file.csv
# Output: file, file

# {/} - Basename
parallel echo '{/}' ::: /path/to/file.txt
# Output: file.txt

# {//} - Directory path
parallel echo '{//}' ::: /path/to/file.txt
# Output: /path/to

# {/.} - Basename without extension
parallel echo '{/.}' ::: /path/to/file.txt
# Output: file

# {#} - Job number (1-based)
parallel echo 'Job {#}: {}' ::: A B C

# {%} - Slot number (recycled job slot)
parallel -j 2 'echo "Slot {%}: {}"' ::: A B C D E

# Combined
parallel 'convert {} -resize 50% {//}/thumb_{/.}.jpg' ::: *.png
```

### Progress and Logging

```bash
#!/usr/bin/env bash
set -euo pipefail

# Show progress bar
parallel --bar process_item ::: {1..100}

# Progress with ETA
parallel --progress process_item ::: {1..100}

# Verbose output
parallel --verbose gzip ::: *.txt

# Log to file
parallel --joblog jobs.log gzip ::: *.txt

# Resume from where it left off (skip completed jobs)
parallel --joblog jobs.log --resume gzip ::: *.txt

# Results logging
parallel --results results_dir 'echo {1} + {2}' ::: 1 2 3 ::: 4 5 6
# Creates: results_dir/1/4/stdout, results_dir/1/4/stderr, etc.
```

### Resource Management

```bash
#!/usr/bin/env bash
set -euo pipefail

# CPU-based parallelism (number of cores)
parallel -j "$(nproc)" process_item ::: {1..1000}

# Leave some cores free
parallel -j '-2' process_item ::: {1..1000}  # nproc - 2

# Percentage of cores
parallel -j '50%' process_item ::: {1..1000}

# Load-based throttling
parallel --load 80% process_item ::: {1..1000}

# Memory-based throttling
parallel --memfree 2G process_item ::: {1..1000}

# Rate limiting (max jobs per second)
parallel -j 4 --delay 0.5 wget ::: url1 url2 url3 url4

# Timeout per job
parallel --timeout 60 long_process ::: {1..100}

# Retry failed jobs
parallel --retries 3 flaky_process ::: {1..100}
```

### Distributed Execution

```bash
#!/usr/bin/env bash
set -euo pipefail

# Run on multiple servers
parallel --sshloginfile servers.txt process_item ::: {1..1000}

# servers.txt format:
# 4/server1.example.com  (4 jobs on server1)
# 8/server2.example.com  (8 jobs on server2)
# :                       (local machine)

# Transfer files before execution
parallel --sshloginfile servers.txt --transferfile {} process {} ::: *.dat

# Return results
parallel --sshloginfile servers.txt --return {.}.result process {} ::: *.dat

# Cleanup after transfer
parallel --sshloginfile servers.txt --transfer --return {.}.out --cleanup \
    'process {} > {.}.out' ::: *.dat

# Environment variables
export MY_VAR="value"
parallel --env MY_VAR --sshloginfile servers.txt 'echo $MY_VAR' ::: A B C
```

### Complex Pipelines

```bash
#!/usr/bin/env bash
set -euo pipefail

# Pipe mode - distribute stdin across workers
cat huge_file.txt | parallel --pipe -N1000 'sort | uniq -c'

# Block size for pipe mode
cat data.bin | parallel --pipe --block 10M 'process_chunk'

# Keep order of output
parallel --keep-order 'sleep $((RANDOM % 3)); echo {}' ::: A B C D E

# Group output (don't mix output from different jobs)
parallel --group 'for i in 1 2 3; do echo "Job {}: line $i"; done' ::: A B C

# Tag output with job identifier
parallel --tag 'echo "output from {}"' ::: A B C

# Sequence output (output as they complete, but grouped)
parallel --ungroup 'echo "Starting {}"; sleep 1; echo "Done {}"' ::: A B C
```

## xargs Parallelization

### Basic Parallel xargs

```bash
#!/usr/bin/env bash
set -euo pipefail

# -P for parallel jobs
find . -name "*.txt" | xargs -P 4 -I {} gzip {}

# -n for items per command
echo {1..100} | xargs -n 10 -P 4 echo "Batch:"

# Null-delimited for safety
find . -name "*.txt" -print0 | xargs -0 -P 4 -I {} process {}

# Multiple arguments per process
cat urls.txt | xargs -P 10 -n 5 wget -q

# Limit max total arguments
echo {1..1000} | xargs -P 4 --max-args=50 echo
```

### xargs with Complex Commands

```bash
#!/usr/bin/env bash
set -euo pipefail

# Use sh -c for complex commands
find . -name "*.jpg" -print0 | \
    xargs -0 -P 4 -I {} sh -c 'convert "$1" -resize 50% "thumb_$(basename "$1")"' _ {}

# Multiple placeholders
paste file1.txt file2.txt | \
    xargs -P 4 -n 2 sh -c 'diff "$1" "$2" > "diff_$(basename "$1" .txt).patch"' _

# Process in batches
find . -name "*.log" -print0 | \
    xargs -0 -P 4 -n 100 tar -czvf logs_batch.tar.gz

# With failure handling
find . -name "*.dat" -print0 | \
    xargs -0 -P 4 -I {} sh -c 'process "$1" || echo "Failed: $1" >> failures.log' _ {}
```

## Job Control Patterns

### Background Job Management

```bash
#!/usr/bin/env bash
set -euo pipefail

# Track background jobs
declare -a PIDS=()

# Start jobs
for item in {1..10}; do
    process_item "$item" &
    PIDS+=($!)
done

# Wait for all
for pid in "${PIDS[@]}"; do
    wait "$pid"
done

echo "All jobs complete"

# Or wait for any to complete
wait -n  # Bash 4.3+
echo "At least one job complete"
```

### Job Pool with Semaphore

```bash
#!/usr/bin/env bash
set -euo pipefail

# Maximum concurrent jobs
MAX_JOBS=4

# Simple semaphore using a counter
job_count=0

run_with_limit() {
    local cmd=("$@")

    # Wait if at limit
    while ((job_count >= MAX_JOBS)); do
        wait -n 2>/dev/null || true
        ((job_count--))
    done

    # Start new job
    "${cmd[@]}" &
    ((job_count++))
}

# Usage
for item in {1..20}; do
    run_with_limit process_item "$item"
done

# Wait for remaining
wait
```

### FIFO-Based Job Pool

```bash
#!/usr/bin/env bash
set -euo pipefail

MAX_JOBS=4
JOB_FIFO="/tmp/job_pool_$$"

# Create job slots
mkfifo "$JOB_FIFO"
trap 'rm -f "$JOB_FIFO"' EXIT

# Initialize slots
exec 3<>"$JOB_FIFO"
for ((i=0; i<MAX_JOBS; i++)); do
    echo >&3
done

# Run with slot
run_with_slot() {
    local cmd=("$@")

    read -u 3  # Acquire slot (blocks if none available)

    {
        "${cmd[@]}"
        echo >&3  # Release slot
    } &
}

# Usage
for item in {1..20}; do
    run_with_slot process_item "$item"
done

wait
exec 3>&-
```

### Worker Pool Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

WORK_QUEUE="/tmp/work_queue_$$"
RESULT_QUEUE="/tmp/result_queue_$$"
NUM_WORKERS=4

mkfifo "$WORK_QUEUE" "$RESULT_QUEUE"
trap 'rm -f "$WORK_QUEUE" "$RESULT_QUEUE"' EXIT

# Worker function
worker() {
    local id="$1"
    while read -r task; do
        [[ "$task" == "STOP" ]] && break

        # Process task
        local result
        result=$(process_task "$task" 2>&1)
        echo "RESULT:$id:$task:$result"
    done
}

# Start workers
for ((i=0; i<NUM_WORKERS; i++)); do
    worker "$i" < "$WORK_QUEUE" > "$RESULT_QUEUE" &
done

# Result collector (background)
collect_results() {
    while read -r line; do
        [[ "$line" == "DONE" ]] && break
        echo "$line" >> results.txt
    done < "$RESULT_QUEUE"
} &
COLLECTOR_PID=$!

# Producer - send work
{
    for task in "${TASKS[@]}"; do
        echo "$task"
    done

    # Stop signals for workers
    for ((i=0; i<NUM_WORKERS; i++)); do
        echo "STOP"
    done
} > "$WORK_QUEUE"

# Signal end of results
wait  # Wait for workers
echo "DONE" > "$RESULT_QUEUE"
wait "$COLLECTOR_PID"
```

## Modern Async Patterns

### Promise-Like Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

# Async function wrapper
async() {
    local result_var="$1"
    shift
    local cmd=("$@")

    # Create temp file for result
    local result_file
    result_file=$(mktemp)

    # Run in background, save result
    {
        if "${cmd[@]}" > "$result_file" 2>&1; then
            echo "0" >> "$result_file.status"
        else
            echo "$?" >> "$result_file.status"
        fi
    } &

    # Store PID and result file location
    eval "${result_var}_pid=$!"
    eval "${result_var}_file='$result_file'"
}

# Await result
await() {
    local result_var="$1"
    local pid_var="${result_var}_pid"
    local file_var="${result_var}_file"

    # Wait for completion
    wait "${!pid_var}"

    # Get result
    cat "${!file_var}"
    local status
    status=$(cat "${!file_var}.status")

    # Cleanup
    rm -f "${!file_var}" "${!file_var}.status"

    return "$status"
}

# Usage
async result1 curl -s "https://api1.example.com/data"
async result2 curl -s "https://api2.example.com/data"
async result3 process_local_data

# Do other work here...

# Get results (blocks until complete)
data1=$(await result1)
data2=$(await result2)
data3=$(await result3)
```

### Event Loop Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

declare -A TASKS
declare -A TASK_RESULTS
TASK_COUNTER=0

# Register async task
schedule() {
    local cmd=("$@")
    local task_id=$((++TASK_COUNTER))
    local output_file="/tmp/task_${task_id}_$$"

    "${cmd[@]}" > "$output_file" 2>&1 &

    TASKS[$task_id]=$!
    TASK_RESULTS[$task_id]="$output_file"

    echo "$task_id"
}

# Check if task complete
is_complete() {
    local task_id="$1"
    ! kill -0 "${TASKS[$task_id]}" 2>/dev/null
}

# Get task result
get_result() {
    local task_id="$1"
    wait "${TASKS[$task_id]}" 2>/dev/null || true
    cat "${TASK_RESULTS[$task_id]}"
    rm -f "${TASK_RESULTS[$task_id]}"
}

# Event loop
run_event_loop() {
    local pending=("${!TASKS[@]}")

    while ((${#pending[@]} > 0)); do
        local still_pending=()

        for task_id in "${pending[@]}"; do
            if is_complete "$task_id"; then
                local result
                result=$(get_result "$task_id")
                on_task_complete "$task_id" "$result"
            else
                still_pending+=("$task_id")
            fi
        done

        pending=("${still_pending[@]}")

        # Small sleep to prevent busy-waiting
        ((${#pending[@]} > 0)) && sleep 0.1
    done
}

# Callback for completed tasks
on_task_complete() {
    local task_id="$1"
    local result="$2"
    echo "Task $task_id complete: ${result:0:50}..."
}
```

### Fan-Out/Fan-In Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

# Fan-out: distribute work
fan_out() {
    local -n items="$1"
    local workers="$2"
    local worker_func="$3"

    local chunk_size=$(( (${#items[@]} + workers - 1) / workers ))
    local pids=()

    for ((i=0; i<workers; i++)); do
        local start=$((i * chunk_size))
        local chunk=("${items[@]:start:chunk_size}")

        if ((${#chunk[@]} > 0)); then
            $worker_func "${chunk[@]}" &
            pids+=($!)
        fi
    done

    # Return PIDs for fan_in
    echo "${pids[*]}"
}

# Fan-in: collect results
fan_in() {
    local -a pids=($1)
    local results=()

    for pid in "${pids[@]}"; do
        wait "$pid"
    done
}

# Example worker
process_chunk() {
    local items=("$@")
    for item in "${items[@]}"; do
        echo "Processed: $item"
    done
}

# Usage
data=({1..100})
pids=$(fan_out data 4 process_chunk)
fan_in "$pids"
```

### Map-Reduce Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

# Map function
parallel_map() {
    local -n input="$1"
    local map_func="$2"
    local workers="${3:-$(nproc)}"

    printf '%s\n' "${input[@]}" | \
        parallel -j "$workers" "$map_func"
}

# Reduce function
reduce() {
    local reduce_func="$1"
    local accumulator="$2"

    while IFS= read -r value; do
        accumulator=$($reduce_func "$accumulator" "$value")
    done

    echo "$accumulator"
}

# Example: Sum of squares
square() { echo $(($1 * $1)); }
add() { echo $(($1 + $2)); }

numbers=({1..100})
sum_of_squares=$(
    parallel_map numbers square 4 | reduce add 0
)
echo "Sum of squares: $sum_of_squares"

# Word count example
word_count_map() {
    tr ' ' '\n' | sort | uniq -c
}

word_count_reduce() {
    sort -k2 | awk '{
        if ($2 == prev) { count += $1 }
        else { if (prev) print count, prev; count = $1; prev = $2 }
    } END { if (prev) print count, prev }'
}

cat large_text.txt | \
    parallel --pipe -N1000 word_count_map | \
    word_count_reduce
```

## Performance Optimization

### Batch Processing

```bash
#!/usr/bin/env bash
set -euo pipefail

# Process in optimal batch sizes
optimal_batch_process() {
    local items=("$@")
    local batch_size=100
    local workers=$(nproc)

    printf '%s\n' "${items[@]}" | \
        parallel --pipe -N"$batch_size" -j"$workers" '
            while IFS= read -r item; do
                process_item "$item"
            done
        '
}

# Dynamic batch sizing based on memory
dynamic_batch() {
    local mem_available
    mem_available=$(free -m | awk '/^Mem:/ {print $7}')

    # Adjust batch size based on available memory
    local batch_size=$((mem_available / 100))  # 100MB per batch
    ((batch_size < 10)) && batch_size=10
    ((batch_size > 1000)) && batch_size=1000

    parallel --pipe -N"$batch_size" process_batch
}
```

### I/O Optimization

```bash
#!/usr/bin/env bash
set -euo pipefail

# Use tmpfs for intermediate files
setup_fast_temp() {
    local tmpdir="/dev/shm/parallel_$$"
    mkdir -p "$tmpdir"
    trap 'rm -rf "$tmpdir"' EXIT
    echo "$tmpdir"
}

# Buffer I/O operations
buffered_parallel() {
    local input="$1"
    local tmpdir
    tmpdir=$(setup_fast_temp)

    # Split input into chunks
    split -l 1000 "$input" "$tmpdir/chunk_"

    # Process chunks in parallel
    parallel process_chunk {} ::: "$tmpdir"/chunk_*

    # Combine results
    cat "$tmpdir"/result_* > output.txt
}

# Avoid disk I/O with process substitution
no_disk_parallel() {
    # Instead of:
    #   command > temp.txt
    #   parallel process ::: temp.txt
    #   rm temp.txt

    # Do this:
    command | parallel --pipe process
}
```

### CPU Affinity

```bash
#!/usr/bin/env bash
set -euo pipefail

# Pin workers to specific CPUs
cpu_pinned_parallel() {
    local num_cpus
    num_cpus=$(nproc)

    for ((cpu=0; cpu<num_cpus; cpu++)); do
        taskset -c "$cpu" process_worker "$cpu" &
    done

    wait
}

# NUMA-aware processing
numa_parallel() {
    local num_nodes
    num_nodes=$(numactl --hardware | grep "available:" | awk '{print $2}')

    for ((node=0; node<num_nodes; node++)); do
        numactl --cpunodebind="$node" --membind="$node" \
            process_chunk "$node" &
    done

    wait
}
```

## Error Handling

### Graceful Failure Handling

```bash
#!/usr/bin/env bash
set -euo pipefail

# Track failures
declare -A FAILURES

parallel_with_retry() {
    local max_retries=3
    local items=("$@")

    for item in "${items[@]}"; do
        local retries=0
        local success=false

        while ((retries < max_retries)) && ! $success; do
            if process_item "$item"; then
                success=true
            else
                ((retries++))
                echo "Retry $retries for $item" >&2
                sleep $((retries * 2))  # Exponential backoff
            fi
        done

        if ! $success; then
            FAILURES["$item"]="Failed after $max_retries retries"
        fi
    done &

    wait
}

# Report failures
report_failures() {
    if ((${#FAILURES[@]} > 0)); then
        echo "Failures:" >&2
        for item in "${!FAILURES[@]}"; do
            echo "  $item: ${FAILURES[$item]}" >&2
        done
        return 1
    fi
}
```

### Cancellation Support

```bash
#!/usr/bin/env bash
set -euo pipefail

# Global cancellation flag
CANCELLED=false
declare -a WORKER_PIDS=()

cancel_all() {
    CANCELLED=true
    for pid in "${WORKER_PIDS[@]}"; do
        kill "$pid" 2>/dev/null || true
    done
}

trap cancel_all SIGINT SIGTERM

cancellable_worker() {
    local id="$1"
    while ! $CANCELLED; do
        # Check for work
        if work=$(get_next_work); then
            process_work "$work"
        else
            sleep 0.1
        fi
    done
}

# Start workers
for ((i=0; i<NUM_WORKERS; i++)); do
    cancellable_worker "$i" &
    WORKER_PIDS+=($!)
done

# Wait with interrupt support
wait || true
```

## Resources

- [GNU Parallel Tutorial](https://www.gnu.org/software/parallel/parallel_tutorial.html)
- [GNU Parallel Manual](https://www.gnu.org/software/parallel/man.html)
- [Bash Job Control](https://www.gnu.org/software/bash/manual/html_node/Job-Control.html)
- [Advanced Bash-Scripting Guide - Process Substitution](https://tldp.org/LDP/abs/html/process-sub.html)

---

**Master parallel processing for efficient multi-core utilization and faster script execution.**
