---
name: checkpoint-workflow-builder
description: Build resumable state-machine workflows with checkpoint patterns, progress preservation, and automatic recovery for complex multi-phase operations that need to survive interruptions, timeouts, and failures.
license: MIT
tags: [workflow, state-machine, checkpoints, resumable, reliability, fault-tolerance]
---

# Checkpoint Workflow Builder

Design and implement fault-tolerant workflows that can resume from any point of failure.

## Overview

Complex workflows often fail mid-execution due to:
- Network timeouts
- System crashes
- Resource exhaustion
- External service failures
- User interruptions

This skill teaches you to build workflows that:
- Save progress at key checkpoints
- Resume from last successful state
- Handle partial failures gracefully
- Provide clear progress visibility
- Enable manual intervention points

## When to Use

Use this skill when:
- Building multi-phase data pipelines
- Implementing long-running migration scripts
- Creating deployment workflows
- Processing large batches of items
- Orchestrating multi-system operations
- Building ETL (Extract, Transform, Load) workflows
- Implementing saga patterns for distributed systems
- Creating user-facing wizards with save/resume

## Core Concepts

### State Machine Pattern

```
┌─────────┐
│  INIT   │
└────┬────┘
     │
     ▼
┌────────────┐
│  DOWNLOAD  │
└─────┬──────┘
      │
      ▼
┌────────────┐
│  PROCESS   │
└─────┬──────┘
      │
      ▼
┌────────────┐
│  VALIDATE  │
└─────┬──────┘
      │
      ▼
┌────────────┐
│  FINALIZE  │
└─────┬──────┘
      │
      ▼
┌────────────┐
│  COMPLETE  │
└────────────┘
```

Each state:
- Has clear entry conditions
- Performs specific operations
- Saves checkpoint before transition
- Can be resumed independently

## Basic Implementation

### Simple State Machine

```bash
#!/bin/bash
# state-machine.sh - Basic resumable workflow

STATE_FILE=".workflow_state"

# Read current state (default: INIT)
CURRENT_STATE=$(cat "$STATE_FILE" 2>/dev/null || echo "INIT")

echo "Current state: $CURRENT_STATE"

case "$CURRENT_STATE" in
    INIT)
        echo "=== Phase 1: Initialization ==="

        # Initialize workspace
        mkdir -p workspace
        mkdir -p results

        # Download dependencies
        echo "Setting up environment..."

        # Save next state
        echo "DOWNLOAD" > "$STATE_FILE"
        echo "✓ Initialization complete"
        echo "Run again to continue"
        ;;

    DOWNLOAD)
        echo "=== Phase 2: Download Data ==="

        # Download data files
        echo "Downloading data..."
        # curl -o workspace/data.zip https://example.com/data.zip

        # Verify download
        if [ -f "workspace/data.zip" ]; then
            echo "EXTRACT" > "$STATE_FILE"
            echo "✓ Download complete"
            echo "Run again to continue"
        else
            echo "✗ Download failed - fix and run again"
            exit 1
        fi
        ;;

    EXTRACT)
        echo "=== Phase 3: Extract Data ==="

        # Extract files
        echo "Extracting data..."
        # unzip workspace/data.zip -d workspace/

        echo "PROCESS" > "$STATE_FILE"
        echo "✓ Extraction complete"
        echo "Run again to continue"
        ;;

    PROCESS)
        echo "=== Phase 4: Process Data ==="

        # Process data
        echo "Processing data..."
        # ./process_data.sh workspace/ results/

        echo "VALIDATE" > "$STATE_FILE"
        echo "✓ Processing complete"
        echo "Run again to continue"
        ;;

    VALIDATE)
        echo "=== Phase 5: Validate Results ==="

        # Validate results
        echo "Validating results..."
        # ./validate.sh results/

        if [ $? -eq 0 ]; then
            echo "FINALIZE" > "$STATE_FILE"
            echo "✓ Validation passed"
            echo "Run again to finalize"
        else
            echo "✗ Validation failed"
            echo "Fix issues and change state to PROCESS to reprocess"
            exit 1
        fi
        ;;

    FINALIZE)
        echo "=== Phase 6: Finalize ==="

        # Cleanup and finalize
        echo "Finalizing workflow..."
        # mv results/ final/
        # rm -rf workspace/

        echo "COMPLETE" > "$STATE_FILE"
        echo "✓ Workflow complete!"
        ;;

    COMPLETE)
        echo "=== Workflow Already Complete ==="
        echo "Results available in: final/"
        ;;

    *)
        echo "✗ Unknown state: $CURRENT_STATE"
        echo "Reset with: echo 'INIT' > $STATE_FILE"
        exit 1
        ;;
esac
```

### Enhanced with Progress Tracking

```bash
#!/bin/bash
# enhanced-state-machine.sh - With detailed progress

STATE_FILE=".workflow_state"
PROGRESS_FILE=".workflow_progress.json"

# Initialize progress tracking
init_progress() {
    cat > "$PROGRESS_FILE" << EOF
{
  "current_state": "INIT",
  "started_at": "$(date -Iseconds)",
  "updated_at": "$(date -Iseconds)",
  "phases": {
    "INIT": {"status": "pending", "started": null, "completed": null},
    "DOWNLOAD": {"status": "pending", "started": null, "completed": null},
    "PROCESS": {"status": "pending", "started": null, "completed": null},
    "VALIDATE": {"status": "pending", "started": null, "completed": null},
    "FINALIZE": {"status": "pending", "started": null, "completed": null}
  }
}
EOF
}

# Update progress
update_progress() {
    local state="$1"
    local status="$2"  # "running", "completed", "failed"

    local timestamp="$(date -Iseconds)"

    if [ ! -f "$PROGRESS_FILE" ]; then
        init_progress
    fi

    jq --arg state "$state" \
       --arg status "$status" \
       --arg timestamp "$timestamp" \
       '.current_state = $state |
        .updated_at = $timestamp |
        .phases[$state].status = $status |
        (.phases[$state].started //= $timestamp) |
        (if $status == "completed" then .phases[$state].completed = $timestamp else . end)' \
       "$PROGRESS_FILE" > "$PROGRESS_FILE.tmp"

    mv "$PROGRESS_FILE.tmp" "$PROGRESS_FILE"
}

# Show progress
show_progress() {
    if [ ! -f "$PROGRESS_FILE" ]; then
        echo "No progress file found"
        return
    fi

    echo "=== Workflow Progress ==="
    echo ""
    jq -r '.phases | to_entries | .[] |
        "[\(.value.status | ascii_upcase)] \(.key)" +
        (if .value.started then " (started: " + .value.started + ")" else "" end)' \
        "$PROGRESS_FILE"
    echo ""
    echo "Current: $(jq -r '.current_state' $PROGRESS_FILE)"
    echo "Updated: $(jq -r '.updated_at' $PROGRESS_FILE)"
}

# Workflow implementation
run_workflow() {
    CURRENT_STATE=$(cat "$STATE_FILE" 2>/dev/null || echo "INIT")

    # Show progress before executing
    show_progress

    case "$CURRENT_STATE" in
        INIT)
            update_progress "INIT" "running"
            echo "Initializing..."
            # ... initialization logic ...
            update_progress "INIT" "completed"
            echo "DOWNLOAD" > "$STATE_FILE"
            ;;

        DOWNLOAD)
            update_progress "DOWNLOAD" "running"
            echo "Downloading..."
            # ... download logic ...
            update_progress "DOWNLOAD" "completed"
            echo "PROCESS" > "$STATE_FILE"
            ;;

        # ... other states ...
    esac
}

run_workflow
```

## Advanced Patterns

### Pattern 1: Batched Checkpoint

```bash
#!/bin/bash
# batched-checkpoint.sh - Process items with batch checkpoints

ITEMS_FILE="items.txt"
CHECKPOINT_FILE=".batch_checkpoint"
BATCH_SIZE=10

# Load checkpoint
if [ -f "$CHECKPOINT_FILE" ]; then
    LAST_COMPLETED=$(cat "$CHECKPOINT_FILE")
    echo "Resuming from item $LAST_COMPLETED"
else
    LAST_COMPLETED=0
fi

TOTAL_ITEMS=$(wc -l < "$ITEMS_FILE")
ITEMS_PROCESSED=0

# Process in batches
tail -n +$((LAST_COMPLETED + 1)) "$ITEMS_FILE" | while read -r item; do
    # Process item
    echo "Processing: $item"
    process_item "$item"

    ITEMS_PROCESSED=$((ITEMS_PROCESSED + 1))

    # Checkpoint every batch
    if [ $((ITEMS_PROCESSED % BATCH_SIZE)) -eq 0 ]; then
        CURRENT_POSITION=$((LAST_COMPLETED + ITEMS_PROCESSED))
        echo "$CURRENT_POSITION" > "$CHECKPOINT_FILE"

        echo "Checkpoint: $CURRENT_POSITION/$TOTAL_ITEMS"

        # Optional: Break for timeout management
        if [ $((ITEMS_PROCESSED)) -ge $((BATCH_SIZE * 5)) ]; then
            echo "Processed 5 batches ($(($BATCH_SIZE * 5)) items)"
            echo "Run again to continue"
            exit 0
        fi
    fi
done

# Final checkpoint
echo "$TOTAL_ITEMS" > "$CHECKPOINT_FILE"
echo "✓ All items processed!"
```

### Pattern 2: Rollback Support

```bash
#!/bin/bash
# rollback-workflow.sh - State machine with rollback

STATE_FILE=".state"
ROLLBACK_DIR=".rollback"

mkdir -p "$ROLLBACK_DIR"

# Save rollback point
save_rollback() {
    local state="$1"
    local timestamp=$(date +%s)

    tar -czf "$ROLLBACK_DIR/${state}_${timestamp}.tar.gz" workspace/ 2>/dev/null || true
    echo "${state}_${timestamp}" > "$ROLLBACK_DIR/latest"
}

# Perform rollback
rollback() {
    local rollback_point="$1"

    if [ -z "$rollback_point" ]; then
        rollback_point=$(cat "$ROLLBACK_DIR/latest" 2>/dev/null)
    fi

    if [ -z "$rollback_point" ] || [ ! -f "$ROLLBACK_DIR/${rollback_point}.tar.gz" ]; then
        echo "✗ No rollback point found"
        exit 1
    fi

    echo "Rolling back to: $rollback_point"

    # Restore from backup
    rm -rf workspace/
    tar -xzf "$ROLLBACK_DIR/${rollback_point}.tar.gz"

    # Set state
    STATE=$(echo "$rollback_point" | cut -d'_' -f1)
    echo "$STATE" > "$STATE_FILE"

    echo "✓ Rolled back to state: $STATE"
}

# In workflow
case "$CURRENT_STATE" in
    DOWNLOAD)
        save_rollback "PRE_DOWNLOAD"
        # ... download logic ...
        ;;

    PROCESS)
        save_rollback "PRE_PROCESS"
        # ... process logic ...
        ;;
esac
```

### Pattern 3: Parallel Phase Execution

```bash
#!/bin/bash
# parallel-phases.sh - Execute independent phases in parallel

STATE_FILE=".parallel_state.json"

# Initialize parallel state
init_parallel_state() {
    cat > "$STATE_FILE" << EOF
{
  "phase_a": "pending",
  "phase_b": "pending",
  "phase_c": "pending",
  "finalize": "pending"
}
EOF
}

# Update phase status
update_phase() {
    local phase="$1"
    local status="$2"

    jq --arg phase "$phase" --arg status "$status" \
       '.[$phase] = $status' "$STATE_FILE" > "$STATE_FILE.tmp"
    mv "$STATE_FILE.tmp" "$STATE_FILE"
}

# Check if all phases complete
all_phases_complete() {
    local incomplete=$(jq -r '[.phase_a, .phase_b, .phase_c] | map(select(. != "completed")) | length' "$STATE_FILE")
    [ "$incomplete" -eq 0 ]
}

# Execute phase
execute_phase() {
    local phase="$1"
    local current_status=$(jq -r ".$phase" "$STATE_FILE")

    if [ "$current_status" = "completed" ]; then
        echo "$phase: Already complete"
        return 0
    fi

    echo "$phase: Running"
    update_phase "$phase" "running"

    # Phase-specific logic
    case "$phase" in
        phase_a)
            # Independent task A
            task_a
            ;;
        phase_b)
            # Independent task B
            task_b
            ;;
        phase_c)
            # Independent task C
            task_c
            ;;
    esac

    if [ $? -eq 0 ]; then
        update_phase "$phase" "completed"
        echo "$phase: Completed"
    else
        update_phase "$phase" "failed"
        echo "$phase: Failed"
        return 1
    fi
}

# Main workflow
[ ! -f "$STATE_FILE" ] && init_parallel_state

# Run independent phases
execute_phase "phase_a"
execute_phase "phase_b"
execute_phase "phase_c"

# Check if ready for finalization
if all_phases_complete; then
    finalize_status=$(jq -r '.finalize' "$STATE_FILE")

    if [ "$finalize_status" != "completed" ]; then
        echo "All phases complete. Finalizing..."
        finalize
        update_phase "finalize" "completed"
        echo "✓ Workflow complete!"
    fi
else
    echo "Some phases incomplete. Run again to retry."
fi
```

## Real-World Examples

### Example 1: Database Migration Workflow

```bash
#!/bin/bash
# db-migration-workflow.sh

STATE_FILE=".migration_state"
MIGRATION_LOG="migration.log"

log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$MIGRATION_LOG"
}

CURRENT_STATE=$(cat "$STATE_FILE" 2>/dev/null || echo "INIT")

case "$CURRENT_STATE" in
    INIT)
        log "=== Starting Migration ==="
        log "Checking prerequisites..."

        # Verify database connection
        psql -U user -d database -c "SELECT 1" > /dev/null 2>&1 || {
            log "✗ Database connection failed"
            exit 1
        }

        # Verify backup destination
        [ -d "/backups" ] || mkdir -p /backups

        echo "BACKUP" > "$STATE_FILE"
        log "✓ Prerequisites checked"
        ;;

    BACKUP)
        log "=== Creating Backup ==="

        BACKUP_FILE="/backups/db_$(date +%Y%m%d_%H%M%S).sql"
        pg_dump -U user database > "$BACKUP_FILE"

        if [ -f "$BACKUP_FILE" ] && [ -s "$BACKUP_FILE" ]; then
            log "✓ Backup created: $BACKUP_FILE"
            echo "MIGRATE" > "$STATE_FILE"
        else
            log "✗ Backup failed"
            exit 1
        fi
        ;;

    MIGRATE)
        log "=== Running Migration ==="

        # Apply migration scripts in order
        for script in migrations/*.sql; do
            log "Applying: $(basename $script)"

            psql -U user -d database -f "$script" >> "$MIGRATION_LOG" 2>&1

            if [ $? -ne 0 ]; then
                log "✗ Migration failed: $script"
                log "To rollback: ./db-migration-workflow.sh rollback"
                exit 1
            fi
        done

        echo "VALIDATE" > "$STATE_FILE"
        log "✓ Migrations applied"
        ;;

    VALIDATE)
        log "=== Validating Migration ==="

        # Run validation queries
        VALIDATION_RESULT=$(psql -U user -d database -f validation.sql 2>&1)

        if echo "$VALIDATION_RESULT" | grep -q "PASS"; then
            log "✓ Validation passed"
            echo "COMPLETE" > "$STATE_FILE"
        else
            log "✗ Validation failed"
            log "$VALIDATION_RESULT"
            log "Review and fix, then change state to MIGRATE to retry"
            exit 1
        fi
        ;;

    COMPLETE)
        log "=== Migration Complete ==="
        log "Database migrated successfully"
        ;;

    rollback)
        log "=== Rolling Back Migration ==="

        # Find latest backup
        LATEST_BACKUP=$(ls -t /backups/db_*.sql | head -1)

        if [ -z "$LATEST_BACKUP" ]; then
            log "✗ No backup found"
            exit 1
        fi

        log "Restoring from: $LATEST_BACKUP"

        psql -U user -d database < "$LATEST_BACKUP"

        log "✓ Rollback complete"
        echo "INIT" > "$STATE_FILE"
        ;;
esac
```

### Example 2: Data Pipeline Workflow

```bash
#!/bin/bash
# data-pipeline.sh - ETL pipeline with checkpoints

STATE_FILE=".pipeline_state.json"

init_state() {
    cat > "$STATE_FILE" << EOF
{
  "state": "EXTRACT",
  "extracted_files": [],
  "transformed_files": [],
  "loaded_records": 0,
  "total_records": 0
}
EOF
}

[ ! -f "$STATE_FILE" ] && init_state

CURRENT_STATE=$(jq -r '.state' "$STATE_FILE")

case "$CURRENT_STATE" in
    EXTRACT)
        echo "=== Extract Phase ==="

        # Extract from sources
        for source in source1 source2 source3; do
            # Check if already extracted
            if jq -e ".extracted_files | index(\"$source\")" "$STATE_FILE" > /dev/null; then
                echo "✓ $source already extracted"
                continue
            fi

            echo "Extracting from: $source"
            extract_from_source "$source" > "raw_data/$source.csv"

            # Update state
            jq ".extracted_files += [\"$source\"]" "$STATE_FILE" > "$STATE_FILE.tmp"
            mv "$STATE_FILE.tmp" "$STATE_FILE"
        done

        # Move to next state
        jq '.state = "TRANSFORM"' "$STATE_FILE" > "$STATE_FILE.tmp"
        mv "$STATE_FILE.tmp" "$STATE_FILE"

        echo "✓ Extraction complete"
        ;;

    TRANSFORM)
        echo "=== Transform Phase ==="

        for file in raw_data/*.csv; do
            filename=$(basename "$file")

            # Check if already transformed
            if jq -e ".transformed_files | index(\"$filename\")" "$STATE_FILE" > /dev/null; then
                echo "✓ $filename already transformed"
                continue
            fi

            echo "Transforming: $filename"
            transform_data "$file" > "processed_data/$filename"

            # Update state
            jq ".transformed_files += [\"$filename\"]" "$STATE_FILE" > "$STATE_FILE.tmp"
            mv "$STATE_FILE.tmp" "$STATE_FILE"
        done

        # Count total records for loading
        TOTAL=$(wc -l processed_data/*.csv | tail -1 | awk '{print $1}')
        jq ".total_records = $TOTAL | .state = \"LOAD\"" "$STATE_FILE" > "$STATE_FILE.tmp"
        mv "$STATE_FILE.tmp" "$STATE_FILE"

        echo "✓ Transformation complete"
        ;;

    LOAD)
        echo "=== Load Phase ==="

        LOADED=$(jq -r '.loaded_records' "$STATE_FILE")
        TOTAL=$(jq -r '.total_records' "$STATE_FILE")

        echo "Progress: $LOADED/$TOTAL records"

        # Load data in batches
        BATCH_SIZE=1000

        tail -n +$((LOADED + 1)) processed_data/combined.csv | head -$BATCH_SIZE | while read record; do
            load_record "$record"
            LOADED=$((LOADED + 1))

            # Checkpoint every 100 records
            if [ $((LOADED % 100)) -eq 0 ]; then
                jq ".loaded_records = $LOADED" "$STATE_FILE" > "$STATE_FILE.tmp"
                mv "$STATE_FILE.tmp" "$STATE_FILE"
            fi
        done

        # Check if complete
        LOADED=$(jq -r '.loaded_records' "$STATE_FILE")
        if [ "$LOADED" -ge "$TOTAL" ]; then
            jq '.state = "COMPLETE"' "$STATE_FILE" > "$STATE_FILE.tmp"
            mv "$STATE_FILE.tmp" "$STATE_FILE"
            echo "✓ Loading complete"
        else
            echo "Loaded $LOADED/$TOTAL - run again to continue"
        fi
        ;;

    COMPLETE)
        echo "=== Pipeline Complete ==="
        jq '.' "$STATE_FILE"
        ;;
esac
```

## Best Practices

### ✅ DO

1. **Design clear states** - Each state has single responsibility
2. **Save frequently** - Checkpoint after each significant operation
3. **Validate transitions** - Verify state before transitioning
4. **Handle failures** - Plan for failure at every state
5. **Log everything** - Comprehensive logging for debugging
6. **Enable inspection** - Make state file human-readable (JSON)
7. **Support rollback** - Save enough info to undo
8. **Test resumption** - Verify workflow resumes correctly

### ❌ DON'T

1. **Don't mix concerns** - Keep states focused
2. **Don't skip validation** - Validate before each transition
3. **Don't hide state** - Make current state obvious
4. **Don't lose progress** - Always save before risky operations
5. **Don't ignore errors** - Handle errors explicitly
6. **Don't hardcode paths** - Use configuration
7. **Don't forget cleanup** - Remove checkpoint files when done
8. **Don't nest too deep** - Keep state machine flat

## Quick Reference

```bash
# Basic state machine
STATE=$(cat .state || echo "INIT")
case "$STATE" in
    STATE1) action1; echo "STATE2" > .state ;;
    STATE2) action2; echo "STATE3" > .state ;;
esac

# With progress tracking (JSON)
jq '.state = "NEW_STATE" | .updated = "'$(date -Iseconds)'"' .state.json

# Checkpoint pattern
process_batch && echo "$POSITION" > .checkpoint

# Rollback support
tar -czf .rollback/pre_${STATE}.tar.gz data/

# Reset workflow
echo "INIT" > .state && rm .progress.json
```

---

**Version**: 1.0.0
**Author**: Harvested from timeout-prevention and state machine patterns
**Last Updated**: 2025-11-18
**License**: MIT
**Key Principle**: Every operation should be resumable from its last successful checkpoint.

Build workflows that never lose progress! 🔄
