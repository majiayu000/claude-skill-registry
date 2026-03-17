---
name: orcaflex-batch-manager
description: Manage large-scale OrcaFlex batch processing with parallel execution,
  adaptive worker scaling, memory optimization, and progress tracking for efficient
  simulation campaigns.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- batch processing
- parallel simulations
- batch manager
- run multiple models
- simulation campaign
- large batch
- parallel OrcaFlex
- job queue
---
# OrcaFlex Batch Manager Skill

Manage large-scale OrcaFlex batch processing with parallel execution, adaptive resource management, and comprehensive progress tracking.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
orcaflex_version: '>=11.0'
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
  - Linux
  - macOS
```

## Changelog

### [1.0.0] - 2026-01-17

**Added:**
- Initial release with parallel batch processing
- Adaptive worker scaling based on system resources
- Chunk-based processing for large batches
- Progress tracking and performance metrics

## When to Use

- Running large simulation campaigns (100+ cases)
- Parallel processing of multiple OrcaFlex models
- Sensitivity studies with many parameter combinations
- Operability matrices covering many sea states
- Multi-seed Monte Carlo simulations
- Overnight batch processing with monitoring

## Batch Processing Features

### Parallel Execution

| Feature | Description |
|---------|-------------|
| ThreadPoolExecutor | Parallel model processing |
| Adaptive scaling | Workers adjust based on CPU/memory |
| File-size optimization | Thread allocation by file complexity |
| Chunk processing | Memory-efficient large batch handling |

### Resource Management

| Resource | Management Strategy |
|----------|---------------------|
| CPU | Worker count = CPU cores - 2 (max 30) |
| Memory | Monitor usage, reduce workers if >80% |
| Disk I/O | Batch file reads, optimize writes |
| License | Respect OrcaFlex license limits |

## Configuration

### Basic Batch Configuration

```yaml
# configs/batch_config.yml

batch:
  # Input files
  input:
    directory: "models/"
    pattern: "*.yml"           # or *.dat
    recursive: false

  # Output settings
  output:
    directory: "results/"
    sim_subdirectory: ".sim"
    log_directory: "logs/"

  # Processing settings
  processing:
    mode: "parallel"           # parallel, sequential, chunked
    max_workers: 20            # Maximum parallel workers
    adaptive_scaling: true     # Auto-adjust workers

    # Chunk settings for large batches
    chunk_size: 50             # Files per chunk
    pause_between_chunks: 5    # Seconds

  # Analysis settings
  analysis:
    run_statics: true
    run_dynamics: true
    simulation_duration: 10800  # 3 hours

  # Error handling
  error_handling:
    continue_on_error: true
    max_retries: 2
    timeout_per_file: 3600     # 1 hour max per file

  # Progress tracking
  progress:
    enabled: true
    update_interval: 10        # Seconds
    save_checkpoint: true
    checkpoint_interval: 100   # Files
```

### Advanced Batch Configuration

```yaml
# configs/batch_advanced.yml

batch:
  # Input filtering
  input:
    directory: "models/operability/"
    pattern: "*.yml"
    filters:
      include_patterns:
        - "*_100yr_*"
        - "*_10yr_*"
      exclude_patterns:
        - "*_draft_*"
        - "*_test_*"
    sort_by: "file_size"       # Process largest first

  # Resource optimization
  resources:
    max_workers: 30
    min_workers: 4

    # CPU management
    cpu_threshold: 90          # Reduce workers if >90%
    cpu_check_interval: 30     # Seconds

    # Memory management
    memory_threshold: 80       # Reduce workers if >80%
    memory_check_interval: 60  # Seconds

    # File size optimization
    file_size_scaling: true
    small_file_threshold: 1    # MB
    large_file_threshold: 10   # MB
    workers_for_large: 5       # Fewer workers for large files

  # Processing pipeline
  pipeline:
    stages:
      - name: "validation"
        enabled: true
        action: "validate_model"

      - name: "preprocessing"
        enabled: true
        action: "prepare_environment"

      - name: "simulation"
        enabled: true
        action: "run_simulation"

      - name: "postprocessing"
        enabled: true
        action: "extract_results"

  # Notifications
  notifications:
    on_start: true
    on_complete: true
    on_error: true
    email: null                # Optional email alerts

  # Performance tracking
  metrics:
    track_per_file: true
    track_memory: true
    track_cpu: true
    export_metrics: true
    metrics_file: "batch_metrics.json"
```

## Python API

### Basic Batch Processing

```python
from digitalmodel.orcaflex.universal.batch_processor import BatchProcessor
from pathlib import Path

def run_batch(input_dir: str, output_dir: str, max_workers: int = 20):
    """
    Run batch processing on OrcaFlex models.

    Args:
        input_dir: Directory containing model files
        output_dir: Directory for results
        max_workers: Maximum parallel workers
    """
    # Initialize processor
    processor = BatchProcessor(
        input_directory=Path(input_dir),
        output_directory=Path(output_dir),
        max_workers=max_workers
    )

    # Run batch
    results = processor.process_batch()

    # Report results
    print(f"Processed: {results['total_files']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")
    print(f"Total time: {results['total_time']:.1f}s")
    print(f"Average time: {results['avg_time_per_file']:.1f}s")

    return results

# Example usage
results = run_batch(
    input_dir="models/operability/",
    output_dir="results/operability/",
    max_workers=20
)
```

### Adaptive Parallel Processing

```python
from digitalmodel.orcaflex.universal.batch_processor import BatchProcessor
from pathlib import Path
import psutil

class AdaptiveBatchProcessor(BatchProcessor):
    """Batch processor with adaptive resource management."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_workers = kwargs.get("max_workers", 20)

    def _calculate_optimal_workers(self) -> int:
        """Calculate optimal worker count based on system resources."""
        # CPU-based scaling
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory-based scaling
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        # Calculate workers
        cpu_workers = max(1, cpu_count - 2)

        # Reduce if CPU high
        if cpu_percent > 90:
            cpu_workers = max(1, cpu_workers // 2)
        elif cpu_percent > 80:
            cpu_workers = int(cpu_workers * 0.75)

        # Reduce if memory high
        if memory_percent > 85:
            cpu_workers = max(1, cpu_workers // 2)
        elif memory_percent > 75:
            cpu_workers = int(cpu_workers * 0.75)

        # Apply limits
        workers = min(cpu_workers, self.initial_workers, 30)

        return max(1, workers)

    def _process_parallel(self, files: list) -> list:
        """Process files with adaptive worker count."""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results = []
        workers = self._calculate_optimal_workers()

        print(f"Starting with {workers} workers")

        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit all tasks
            futures = {
                executor.submit(self._process_single, f): f
                for f in files
            }

            # Process completions
            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        "file": str(file_path),
                        "success": False,
                        "error": str(e)
                    })

                # Periodically re-evaluate workers
                if len(results) % 10 == 0:
                    new_workers = self._calculate_optimal_workers()
                    if new_workers != workers:
                        print(f"Adjusting workers: {workers} -> {new_workers}")

        return results

# Example usage
processor = AdaptiveBatchProcessor(
    input_directory=Path("models/"),
    output_directory=Path("results/"),
    max_workers=30
)

results = processor.process_batch()
```

### Chunk-Based Processing

```python
from digitalmodel.orcaflex.universal.batch_processor import BatchProcessor
from pathlib import Path
import time

def process_in_chunks(
    input_dir: str,
    output_dir: str,
    chunk_size: int = 50,
    pause_seconds: int = 5
) -> dict:
    """
    Process large batch in chunks with pause between.

    Args:
        input_dir: Input directory
        output_dir: Output directory
        chunk_size: Files per chunk
        pause_seconds: Pause between chunks

    Returns:
        Combined results dictionary
    """
    processor = BatchProcessor(
        input_directory=Path(input_dir),
        output_directory=Path(output_dir)
    )

    # Get all files
    files = processor._get_input_files()
    total_files = len(files)

    print(f"Total files: {total_files}")
    print(f"Chunk size: {chunk_size}")
    print(f"Number of chunks: {(total_files + chunk_size - 1) // chunk_size}")

    all_results = []

    # Process in chunks
    for i in range(0, total_files, chunk_size):
        chunk = files[i:i + chunk_size]
        chunk_num = i // chunk_size + 1

        print(f"\nProcessing chunk {chunk_num}...")

        chunk_results = processor._process_parallel(chunk)
        all_results.extend(chunk_results)

        # Progress update
        completed = len(all_results)
        successful = sum(1 for r in all_results if r.get("success", False))

        print(f"Progress: {completed}/{total_files} ({100*completed/total_files:.1f}%)")
        print(f"Successful: {successful}")

        # Pause between chunks (except last)
        if i + chunk_size < total_files:
            print(f"Pausing {pause_seconds}s before next chunk...")
            time.sleep(pause_seconds)

    return {
        "total_files": total_files,
        "successful": sum(1 for r in all_results if r.get("success", False)),
        "failed": sum(1 for r in all_results if not r.get("success", True)),
        "results": all_results
    }

# Example: Process 500 files in chunks of 50
results = process_in_chunks(
    input_dir="models/sensitivity/",
    output_dir="results/sensitivity/",
    chunk_size=50,
    pause_seconds=10
)
```

### Progress Tracking and Checkpoints

```python
from digitalmodel.orcaflex.universal.batch_processor import BatchProcessor
from pathlib import Path
import json
import time

class CheckpointBatchProcessor(BatchProcessor):
    """Batch processor with checkpoint save/restore."""

    def __init__(self, checkpoint_file: str = "batch_checkpoint.json", **kwargs):
        super().__init__(**kwargs)
        self.checkpoint_file = Path(checkpoint_file)
        self.processed_files = set()
        self._load_checkpoint()

    def _load_checkpoint(self):
        """Load checkpoint if exists."""
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, "r") as f:
                checkpoint = json.load(f)
                self.processed_files = set(checkpoint.get("processed_files", []))
            print(f"Loaded checkpoint: {len(self.processed_files)} files already processed")

    def _save_checkpoint(self):
        """Save current progress."""
        checkpoint = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "processed_files": list(self.processed_files)
        }
        with open(self.checkpoint_file, "w") as f:
            json.dump(checkpoint, f, indent=2)

    def process_batch(self) -> dict:
        """Process batch with checkpoint support."""
        # Get files
        all_files = self._get_input_files()

        # Filter already processed
        pending_files = [
            f for f in all_files
            if str(f) not in self.processed_files
        ]

        print(f"Total files: {len(all_files)}")
        print(f"Already processed: {len(self.processed_files)}")
        print(f"Pending: {len(pending_files)}")

        if not pending_files:
            print("All files already processed!")
            return {"total_files": len(all_files), "pending": 0}

        # Process pending files
        results = []
        for i, file_path in enumerate(pending_files):
            try:
                result = self._process_single(file_path)
                results.append(result)
                self.processed_files.add(str(file_path))

                # Save checkpoint periodically
                if (i + 1) % 10 == 0:
                    self._save_checkpoint()
                    print(f"Checkpoint saved: {len(self.processed_files)} files")

            except Exception as e:
                results.append({
                    "file": str(file_path),
                    "success": False,
                    "error": str(e)
                })

        # Final checkpoint
        self._save_checkpoint()

        return {
            "total_files": len(all_files),
            "newly_processed": len(pending_files),
            "successful": sum(1 for r in results if r.get("success", False)),
            "failed": sum(1 for r in results if not r.get("success", True))
        }

# Example: Resumable batch processing
processor = CheckpointBatchProcessor(
    checkpoint_file="operability_checkpoint.json",
    input_directory=Path("models/"),
    output_directory=Path("results/")
)

# Can be interrupted and resumed
results = processor.process_batch()
```

### File Size Optimization

```python
from pathlib import Path
import os

def sort_by_file_size(files: list, reverse: bool = True) -> list:
    """
    Sort files by size for optimal processing order.

    Processing large files first with fewer workers,
    then small files with more workers.

    Args:
        files: List of file paths
        reverse: If True, largest first

    Returns:
        Sorted file list
    """
    file_sizes = [(f, os.path.getsize(f)) for f in files]
    file_sizes.sort(key=lambda x: x[1], reverse=reverse)
    return [f for f, _ in file_sizes]

def allocate_workers_by_size(file_path: Path, max_workers: int = 20) -> int:
    """
    Allocate workers based on file size.

    Args:
        file_path: Path to model file
        max_workers: Maximum available workers

    Returns:
        Recommended workers for this file
    """
    size_mb = os.path.getsize(file_path) / (1024 * 1024)

    if size_mb > 20:
        # Very large file - use fewer workers
        return min(3, max_workers)
    elif size_mb > 10:
        # Large file
        return min(5, max_workers)
    elif size_mb > 5:
        # Medium file
        return min(10, max_workers)
    else:
        # Small file - use full parallelism
        return max_workers

# Example usage
files = list(Path("models/").glob("*.yml"))
sorted_files = sort_by_file_size(files, reverse=True)

for f in sorted_files[:5]:
    workers = allocate_workers_by_size(f)
    print(f"{f.name}: {os.path.getsize(f)/1024/1024:.1f} MB -> {workers} workers")
```

### Performance Metrics

```python
from dataclasses import dataclass, field
from typing import Dict, List
import time
import json

@dataclass
class BatchMetrics:
    """Track batch processing performance metrics."""

    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0
    file_times: Dict[str, float] = field(default_factory=dict)
    file_successes: Dict[str, bool] = field(default_factory=dict)
    worker_counts: List[int] = field(default_factory=list)
    memory_usage: List[float] = field(default_factory=list)

    def record_file(self, file_name: str, duration: float, success: bool):
        """Record file processing result."""
        self.file_times[file_name] = duration
        self.file_successes[file_name] = success

    def complete(self):
        """Mark batch as complete."""
        self.end_time = time.time()

    def summary(self) -> dict:
        """Generate summary statistics."""
        total_files = len(self.file_times)
        successful = sum(1 for s in self.file_successes.values() if s)
        total_time = self.end_time - self.start_time

        times = list(self.file_times.values())

        return {
            "total_files": total_files,
            "successful": successful,
            "failed": total_files - successful,
            "success_rate": successful / total_files * 100 if total_files > 0 else 0,
            "total_time_seconds": total_time,
            "avg_time_per_file": sum(times) / len(times) if times else 0,
            "min_file_time": min(times) if times else 0,
            "max_file_time": max(times) if times else 0,
            "processing_rate": total_files / total_time * 3600 if total_time > 0 else 0  # files/hour
        }

    def export(self, file_path: str):
        """Export metrics to JSON."""
        with open(file_path, "w") as f:
            json.dump({
                "summary": self.summary(),
                "file_times": self.file_times,
                "file_successes": self.file_successes
            }, f, indent=2)

# Example usage with metrics
metrics = BatchMetrics()

for file_path in files:
    start = time.time()
    try:
        # Process file
        result = process_single_file(file_path)
        success = True
    except Exception:
        success = False

    duration = time.time() - start
    metrics.record_file(file_path.name, duration, success)

metrics.complete()
print(metrics.summary())
metrics.export("batch_metrics.json")
```

## Output Formats

### Batch Results JSON

```json
{
  "batch_id": "operability_20260117_143022",
  "start_time": "2026-01-17T14:30:22",
  "end_time": "2026-01-17T18:45:33",
  "total_files": 500,
  "successful": 495,
  "failed": 5,
  "success_rate": 99.0,
  "total_time_seconds": 15311,
  "avg_time_per_file": 30.62,
  "processing_rate": 117.5,
  "failed_files": [
    {
      "file": "case_245.yml",
      "error": "Static analysis failed to converge"
    }
  ]
}
```

### Progress Log

```
2026-01-17 14:30:22 - Batch started: 500 files
2026-01-17 14:30:22 - Workers: 20 (adaptive)
2026-01-17 14:31:45 - Progress: 50/500 (10.0%) - Success: 50
2026-01-17 14:33:12 - Progress: 100/500 (20.0%) - Success: 100
2026-01-17 14:33:12 - Checkpoint saved
2026-01-17 14:35:40 - Workers adjusted: 20 -> 15 (memory 82%)
...
2026-01-17 18:45:33 - Batch complete: 495 successful, 5 failed
```

## Best Practices

### Resource Management

1. **CPU headroom** - Keep 2 cores free for system
2. **Memory monitoring** - Reduce workers if >80% used
3. **Disk I/O** - Use SSD for results directory
4. **Network** - Minimize network storage for sim files

### Error Handling

1. **Continue on error** - Don't stop batch for single failure
2. **Retry logic** - Retry failed files with single worker
3. **Timeout** - Set reasonable per-file timeout
4. **Logging** - Log all failures with details

### Performance

1. **Sort by size** - Process large files first
2. **Chunk processing** - Break very large batches
3. **Checkpoint** - Save progress for resumability
4. **Off-hours** - Run large batches overnight

## Error Handling

```python
try:
    results = processor.process_batch()
except MemoryError:
    print("Out of memory - reduce workers or chunk size")

except OSError as e:
    print(f"File system error: {e}")
    print("Check disk space and permissions")
```

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [orcaflex-operability](../orcaflex-operability/SKILL.md) - Multi-sea-state campaigns
- [orcaflex-post-processing](../orcaflex-post-processing/SKILL.md) - Extract results
- [orcaflex-results-comparison](../orcaflex-results-comparison/SKILL.md) - Compare results

## References

- Python concurrent.futures documentation
- psutil system monitoring
- Source: `src/digitalmodel/modules/orcaflex/universal/batch_processor.py`
- Source: `src/digitalmodel/modules/orcaflex/orcaflex_parallel_analysis.py`
