---
name: parallel-file-processor
description: Process multiple files in parallel with aggregation and progress tracking. Use for batch file operations, directory scanning, ZIP handling, and parallel data processing with 2-3x performance improvement.
version: 1.1.0
category: development
related_skills:
  - data-pipeline-processor
  - yaml-workflow-executor
  - engineering-report-generator
---

# Parallel File Processor

> Version: 1.1.0
> Category: Development
> Last Updated: 2026-01-02

Process multiple files concurrently with intelligent batching, progress tracking, and result aggregation for significant performance improvements.

## Quick Start

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import pandas as pd

def process_csv(file_path: Path) -> dict:
    """Process a single CSV file."""
    df = pd.read_csv(file_path)
    return {'file': file_path.name, 'rows': len(df), 'columns': len(df.columns)}

# Get all CSV files
files = list(Path('data/raw/').glob('*.csv'))

# Process in parallel
results = []
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(process_csv, f): f for f in files}
    for future in as_completed(futures):
        results.append(future.result())

print(f"Processed {len(results)} files")
```

## When to Use

- Processing large numbers of files (100+ files)
- Batch operations on directory contents
- Extracting data from multiple ZIP archives
- Aggregating results from parallel operations
- CPU-bound file transformations
- IO-bound file operations with proper concurrency

## Core Pattern

```
Directory Scan -> Filter -> Batch -> Parallel Process -> Aggregate -> Output
```

## Implementation

### Core Components

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    List, Dict, Any, Callable, Optional, Generator, TypeVar, Generic
)
from enum import Enum
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')
R = TypeVar('R')

class ProcessingMode(Enum):
    """Processing execution mode."""
    SEQUENTIAL = "sequential"
    THREAD_POOL = "thread_pool"
    PROCESS_POOL = "process_pool"
    ASYNC = "async"

@dataclass
class FileInfo:
    """File metadata container."""
    path: Path
    size_bytes: int
    modified_time: float
    extension: str
    relative_path: Optional[str] = None

    @classmethod
    def from_path(cls, path: Path, base_path: Path = None) -> 'FileInfo':
        """Create FileInfo from path."""
        stat = path.stat()
        relative = str(path.relative_to(base_path)) if base_path else None
        return cls(
            path=path,
            size_bytes=stat.st_size,
            modified_time=stat.st_mtime,
            extension=path.suffix.lower(),
            relative_path=relative
        )

@dataclass
class ProcessingResult(Generic[T]):
    """Result of processing a single file."""
    file_info: FileInfo
    success: bool
    result: Optional[T] = None
    error: Optional[str] = None
    duration_seconds: float = 0.0

@dataclass
class BatchResult(Generic[T]):
    """Aggregated results from batch processing."""
    total_files: int = 0
    successful: int = 0
    failed: int = 0
    results: List[ProcessingResult[T]] = field(default_factory=list)
    total_duration_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_files == 0:
            return 100.0
        return (self.successful / self.total_files) * 100

    def successful_results(self) -> List[T]:
        """Get list of successful results only."""
        return [r.result for r in self.results if r.success and r.result is not None]
```

### File Scanner

```python
import fnmatch
from typing import List, Optional, Set, Generator
from pathlib import Path

class FileScanner:
    """
    Scan directories for files matching patterns.

    Supports glob patterns, extension filtering, and size limits.
    """

    def __init__(self,
                 include_patterns: List[str] = None,
                 exclude_patterns: List[str] = None,
                 extensions: Set[str] = None,
                 min_size: int = 0,
                 max_size: int = None,
                 recursive: bool = True):
        """
        Initialize file scanner.

        Args:
            include_patterns: Glob patterns to include (e.g., ['*.csv', '*.xlsx'])
            exclude_patterns: Glob patterns to exclude (e.g., ['*_backup*'])
            extensions: File extensions to include (e.g., {'.csv', '.xlsx'})
            min_size: Minimum file size in bytes
            max_size: Maximum file size in bytes
            recursive: Scan subdirectories
        """
        self.include_patterns = include_patterns or ['*']
        self.exclude_patterns = exclude_patterns or []
        self.extensions = extensions
        self.min_size = min_size
        self.max_size = max_size
        self.recursive = recursive

    def scan(self, directory: Path) -> Generator[FileInfo, None, None]:
        """
        Scan directory and yield matching files.

        Args:
            directory: Directory to scan

        Yields:
            FileInfo for each matching file
        """
        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        if not directory.is_dir():
            raise ValueError(f"Not a directory: {directory}")

        # Choose iteration method
        if self.recursive:
            files = directory.rglob('*')
        else:
            files = directory.glob('*')

        for path in files:
            if path.is_file() and self._matches(path):
                try:
                    yield FileInfo.from_path(path, directory)
                except Exception as e:
                    logger.warning(f"Could not get info for {path}: {e}")

    def _matches(self, path: Path) -> bool:
        """Check if file matches all criteria."""
        name = path.name

        # Check include patterns
        if not any(fnmatch.fnmatch(name, p) for p in self.include_patterns):
            return False

        # Check exclude patterns
        if any(fnmatch.fnmatch(name, p) for p in self.exclude_patterns):
            return False

        # Check extension
        if self.extensions and path.suffix.lower() not in self.extensions:
            return False

        # Check size
        try:
            size = path.stat().st_size
            if size < self.min_size:
                return False
            if self.max_size and size > self.max_size:
                return False
        except OSError:
            return False

        return True

    def count(self, directory: Path) -> int:
        """Count matching files without loading all info."""
        return sum(1 for _ in self.scan(directory))

    def list_files(self, directory: Path) -> List[FileInfo]:
        """Get all matching files as list."""
        return list(self.scan(directory))
```

### Parallel Processor

```python
import time
from concurrent.futures import (
    ThreadPoolExecutor, ProcessPoolExecutor,
    as_completed, Future
)
from typing import Callable, TypeVar, Generic, List
import asyncio
from functools import partial

T = TypeVar('T')
R = TypeVar('R')

class ParallelProcessor(Generic[T, R]):
    """
    Process items in parallel with configurable execution modes.
    """

    def __init__(self,
                 processor: Callable[[T], R],
                 mode: ProcessingMode = ProcessingMode.THREAD_POOL,
                 max_workers: int = None,
                 batch_size: int = None,
                 timeout: float = None):
        """
        Initialize parallel processor.

        Args:
            processor: Function to process each item
            mode: Processing mode (thread, process, async)
            max_workers: Maximum concurrent workers
            batch_size: Items per batch (for memory management)
            timeout: Timeout per item in seconds
        """
        self.processor = processor
        self.mode = mode
        self.max_workers = max_workers or self._default_workers()
        self.batch_size = batch_size or 100
        self.timeout = timeout

        self._progress_callback: Optional[Callable[[int, int], None]] = None

    def _default_workers(self) -> int:
        """Get default worker count based on mode."""
        import os
        cpu_count = os.cpu_count() or 4

        if self.mode == ProcessingMode.PROCESS_POOL:
            return cpu_count
        elif self.mode == ProcessingMode.THREAD_POOL:
            return cpu_count * 2  # IO-bound benefits from more threads
        else:
            return cpu_count

    def on_progress(self, callback: Callable[[int, int], None]):
        """Set progress callback: callback(completed, total)."""
        self._progress_callback = callback
        return self

    def process(self, items: List[T]) -> BatchResult[R]:
        """
        Process all items and return aggregated results.

        Args:
            items: Items to process

        Returns:
            BatchResult with all results
        """
        start_time = time.time()
        total = len(items)

        if self.mode == ProcessingMode.SEQUENTIAL:
            result = self._process_sequential(items)
        elif self.mode == ProcessingMode.THREAD_POOL:
            result = self._process_threaded(items)
        elif self.mode == ProcessingMode.PROCESS_POOL:
            result = self._process_multiprocess(items)
        elif self.mode == ProcessingMode.ASYNC:
            result = asyncio.run(self._process_async(items))
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

        result.total_duration_seconds = time.time() - start_time
        return result

    def _process_threaded(self, items: List[T]) -> BatchResult[R]:
        """Process items using thread pool."""
        result = BatchResult(total_files=len(items))
        completed = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_item = {
                executor.submit(self._process_single, item): item
                for item in items
            }

            # Collect results as they complete
            for future in as_completed(future_to_item):
                proc_result = future.result()
                result.results.append(proc_result)

                if proc_result.success:
                    result.successful += 1
                else:
                    result.failed += 1
                    if proc_result.error:
                        result.errors.append(proc_result.error)

                completed += 1
                if self._progress_callback:
                    self._progress_callback(completed, len(items))

        return result

    def _process_single(self, item: T) -> ProcessingResult[R]:
        """Process a single item with error handling."""
        start_time = time.time()

        # Create FileInfo if item is a Path or FileInfo
        if isinstance(item, Path):
            file_info = FileInfo.from_path(item)
        elif isinstance(item, FileInfo):
            file_info = item
        else:
            # Create dummy FileInfo for non-file items
            file_info = FileInfo(
                path=Path(""),
                size_bytes=0,
                modified_time=0,
                extension=""
            )

        try:
            result = self.processor(item)
            return ProcessingResult(
                file_info=file_info,
                success=True,
                result=result,
                duration_seconds=time.time() - start_time
            )
        except Exception as e:
            return ProcessingResult(
                file_info=file_info,
                success=False,
                error=str(e),
                duration_seconds=time.time() - start_time
            )
```

### File Processor

```python
class FileProcessor:
    """
    High-level file processing with parallel execution.

    Combines scanning, filtering, and parallel processing.
    """

    def __init__(self,
                 scanner: FileScanner = None,
                 mode: ProcessingMode = ProcessingMode.THREAD_POOL,
                 max_workers: int = None):
        self.scanner = scanner or FileScanner()
        self.mode = mode
        self.max_workers = max_workers

    def process_directory(self,
                         directory: Path,
                         processor: Callable[[FileInfo], Any],
                         progress_callback: Callable[[int, int], None] = None
                         ) -> BatchResult:
        """Process all matching files in a directory."""
        files = self.scanner.list_files(directory)
        logger.info(f"Found {len(files)} files to process")

        if not files:
            return BatchResult()

        parallel = ParallelProcessor(
            processor=processor,
            mode=self.mode,
            max_workers=self.max_workers
        )

        if progress_callback:
            parallel.on_progress(progress_callback)

        return parallel.process(files)

    def aggregate_csv(self,
                      directory: Path,
                      output_path: Path = None,
                      **read_kwargs) -> pd.DataFrame:
        """Read and aggregate all CSV files in directory."""
        self.scanner = FileScanner(extensions={'.csv'})

        def read_csv(file_info: FileInfo) -> pd.DataFrame:
            df = pd.read_csv(file_info.path, **read_kwargs)
            df['_source_file'] = file_info.path.name
            return df

        result = self.process_directory(directory, read_csv)
        dfs = result.successful_results()

        if not dfs:
            return pd.DataFrame()

        combined = pd.concat(dfs, ignore_index=True)

        if output_path:
            combined.to_csv(output_path, index=False)

        return combined

    def extract_all_zips(self,
                         directory: Path,
                         output_directory: Path
                         ) -> BatchResult:
        """Extract all ZIP files in directory."""
        import zipfile

        self.scanner = FileScanner(extensions={'.zip'})
        output_directory.mkdir(parents=True, exist_ok=True)

        def extract_zip(file_info: FileInfo) -> Dict:
            extract_dir = output_directory / file_info.path.stem
            extract_dir.mkdir(exist_ok=True)

            with zipfile.ZipFile(file_info.path, 'r') as zf:
                zf.extractall(extract_dir)
                return {
                    'source': str(file_info.path),
                    'destination': str(extract_dir),
                    'files_extracted': len(zf.namelist())
                }

        return self.process_directory(directory, extract_zip)
```

### Progress Tracking

```python
from datetime import datetime, timedelta
import sys

class ProgressTracker:
    """Track and display processing progress."""

    def __init__(self,
                 total: int,
                 description: str = "Processing",
                 show_eta: bool = True,
                 bar_width: int = 40):
        self.total = total
        self.description = description
        self.show_eta = show_eta
        self.bar_width = bar_width
        self.completed = 0
        self.start_time: Optional[datetime] = None

    def start(self):
        """Start tracking."""
        self.start_time = datetime.now()
        self.completed = 0
        self._display()

    def update(self, completed: int, total: int):
        """Update progress."""
        self.completed = completed
        self.total = total
        self._display()

    def _display(self):
        """Display progress bar."""
        if self.total == 0:
            return

        pct = self.completed / self.total
        filled = int(self.bar_width * pct)
        bar = '#' * filled + '-' * (self.bar_width - filled)

        # Calculate ETA
        eta_str = ""
        if self.show_eta and self.start_time and self.completed > 0:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            rate = self.completed / elapsed
            remaining = (self.total - self.completed) / rate if rate > 0 else 0
            eta_str = f" ETA: {timedelta(seconds=int(remaining))}"

        line = (f"\r{self.description}: |{bar}| "
                f"{self.completed}/{self.total} ({pct*100:.1f}%){eta_str}")

        sys.stdout.write(line)
        sys.stdout.flush()

        if self.completed == self.total:
            print()

    def finish(self):
        """Mark processing as complete."""
        self.completed = self.total
        self._display()
```

### Result Aggregator

```python
import json

class ResultAggregator:
    """Aggregate and export batch processing results."""

    def __init__(self, batch_result: BatchResult):
        self.batch_result = batch_result

    def to_dataframe(self) -> pd.DataFrame:
        """Convert results to DataFrame."""
        data = []
        for r in self.batch_result.results:
            row = {
                'file_path': str(r.file_info.path),
                'file_name': r.file_info.path.name,
                'file_size': r.file_info.size_bytes,
                'success': r.success,
                'duration_seconds': r.duration_seconds,
                'error': r.error
            }

            if r.success and isinstance(r.result, dict):
                for k, v in r.result.items():
                    if not k.startswith('_'):
                        row[f'result_{k}'] = v

            data.append(row)

        return pd.DataFrame(data)

    def summary(self) -> Dict[str, Any]:
        """Generate summary statistics."""
        return {
            'total_files': self.batch_result.total_files,
            'successful': self.batch_result.successful,
            'failed': self.batch_result.failed,
            'success_rate_pct': self.batch_result.success_rate,
            'total_duration_seconds': self.batch_result.total_duration_seconds,
            'avg_duration_seconds': (
                self.batch_result.total_duration_seconds /
                self.batch_result.total_files
                if self.batch_result.total_files > 0 else 0
            ),
            'errors': self.batch_result.errors[:10]
        }

    def export_csv(self, path: Path):
        """Export results to CSV."""
        df = self.to_dataframe()
        df.to_csv(path, index=False)

    def export_json(self, path: Path):
        """Export summary to JSON."""
        summary = self.summary()
        with open(path, 'w') as f:
            json.dump(summary, f, indent=2)

    def combine_dataframes(self) -> pd.DataFrame:
        """Combine results that are DataFrames."""
        dfs = [r for r in self.batch_result.successful_results()
               if isinstance(r, pd.DataFrame)]

        if not dfs:
            return pd.DataFrame()

        return pd.concat(dfs, ignore_index=True)
```

## YAML Configuration

### Basic Configuration

```yaml
# config/parallel_processing.yaml

scan:
  directory: "data/raw/"
  recursive: true

  include_patterns:
    - "*.csv"
    - "*.xlsx"

  exclude_patterns:
    - "*_backup*"
    - "~$*"

  extensions:
    - ".csv"
    - ".xlsx"

  size_limits:
    min_bytes: 100
    max_bytes: 104857600  # 100MB

processing:
  mode: thread_pool  # sequential, thread_pool, process_pool, async
  max_workers: 8
  batch_size: 100
  timeout_seconds: 30

output:
  results_csv: "data/results/processing_results.csv"
  summary_json: "data/results/summary.json"
  combined_output: "data/processed/combined.csv"

progress:
  enabled: true
  show_eta: true
```

## Usage Examples

### Example 1: Process CSV Files

```python
from parallel_file_processor import (
    FileScanner, FileProcessor, ProcessingMode,
    ProgressTracker, ResultAggregator
)
from pathlib import Path
import pandas as pd

# Define processing function
def process_csv(file_info):
    """Extract statistics from CSV file."""
    df = pd.read_csv(file_info.path)
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'memory_mb': df.memory_usage(deep=True).sum() / 1e6,
        'numeric_columns': len(df.select_dtypes(include='number').columns)
    }

# Setup scanner and processor
scanner = FileScanner(extensions={'.csv'})
processor = FileProcessor(
    scanner=scanner,
    mode=ProcessingMode.THREAD_POOL,
    max_workers=8
)

# Create progress tracker
tracker = ProgressTracker(0, "Processing CSVs")
tracker.start()

# Process with progress
result = processor.process_directory(
    Path("data/raw/"),
    process_csv,
    progress_callback=tracker.update
)

tracker.finish()

# Aggregate results
aggregator = ResultAggregator(result)
print(f"\nSummary: {aggregator.summary()}")
aggregator.export_csv(Path("data/results/csv_stats.csv"))
```

### Example 2: Parallel ZIP Extraction

```python
# Extract all ZIPs in parallel
processor = FileProcessor(mode=ProcessingMode.THREAD_POOL)

result = processor.extract_all_zips(
    directory=Path("data/archives/"),
    output_directory=Path("data/extracted/")
)

print(f"Extracted {result.successful} ZIP files")
print(f"Failed: {result.failed}")

# Get extraction details
aggregator = ResultAggregator(result)
df = aggregator.to_dataframe()
total_files = df['result_files_extracted'].sum()
print(f"Total files extracted: {total_files}")
```

### Example 3: Aggregate Data from Multiple Sources

```python
# Aggregate CSV files with custom processing
def load_and_clean(file_info):
    """Load CSV and perform basic cleaning."""
    df = pd.read_csv(file_info.path)

    # Clean column names
    df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]

    # Add metadata
    df['_source'] = file_info.path.name
    df['_loaded_at'] = pd.Timestamp.now()

    return df

processor = FileProcessor(
    scanner=FileScanner(extensions={'.csv'}),
    mode=ProcessingMode.THREAD_POOL
)

result = processor.process_directory(
    Path("data/monthly_reports/"),
    load_and_clean
)

# Combine all DataFrames
aggregator = ResultAggregator(result)
combined_df = aggregator.combine_dataframes()

print(f"Combined {len(combined_df)} rows from {result.successful} files")
combined_df.to_csv("data/combined_reports.csv", index=False)
```

### Example 4: Custom Batch Processing

```python
from parallel_file_processor import ParallelProcessor, ProcessingMode

# Process list of items (not files)
items = list(range(1000))

def heavy_computation(item):
    """CPU-intensive calculation."""
    import math
    result = sum(math.sin(i * item) for i in range(10000))
    return {'item': item, 'result': result}

# Use process pool for CPU-bound work
processor = ParallelProcessor(
    processor=heavy_computation,
    mode=ProcessingMode.PROCESS_POOL,
    max_workers=4
)

# Track progress
def show_progress(completed, total):
    pct = (completed / total) * 100
    print(f"\rProgress: {pct:.1f}%", end='', flush=True)

processor.on_progress(show_progress)

result = processor.process(items)
print(f"\nCompleted {result.successful}/{result.total_files} items")
```

## Performance Tips

### Mode Selection

| Workload Type | Recommended Mode | Reason |
|---------------|------------------|--------|
| File I/O | `THREAD_POOL` | IO-bound, threads avoid GIL issues |
| Data parsing | `THREAD_POOL` | Pandas releases GIL during IO |
| CPU computation | `PROCESS_POOL` | Bypasses GIL for true parallelism |
| Network requests | `ASYNC` | Best for many concurrent connections |
| Simple operations | `SEQUENTIAL` | Overhead may exceed benefit |

### Worker Count

```python
import os

# IO-bound (reading files, network)
io_workers = os.cpu_count() * 2

# CPU-bound (heavy computation)
cpu_workers = os.cpu_count()

# Memory-constrained (large files)
memory_workers = max(2, os.cpu_count() // 2)
```

### Batch Size

- **Small files (<1MB):** Large batches (500-1000)
- **Medium files (1-100MB):** Medium batches (50-100)
- **Large files (>100MB):** Small batches (10-20) or one at a time

## Best Practices

### Do

1. Choose correct processing mode for workload type
2. Use progress callbacks for long operations
3. Batch large file sets to manage memory
4. Log individual failures for debugging
5. Consider retry logic for transient errors
6. Monitor memory usage with large DataFrames

### Don't

1. Use process pool for IO-bound tasks
2. Skip error handling in processor functions
3. Load all results into memory at once
4. Ignore batch result statistics
5. Use too many workers for memory-constrained tasks

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `MemoryError` | Too many files loaded | Use batching or streaming |
| `PermissionError` | File access denied | Check file permissions |
| `TimeoutError` | Processing too slow | Increase timeout or optimize |
| `OSError` | Too many open files | Reduce max_workers |

### Error Template

```python
def safe_process_directory(directory: Path, processor: Callable) -> dict:
    """Process directory with comprehensive error handling."""
    try:
        if not directory.exists():
            return {'status': 'error', 'message': 'Directory not found'}

        file_processor = FileProcessor()
        result = file_processor.process_directory(directory, processor)

        if result.failed > 0:
            return {
                'status': 'partial',
                'successful': result.successful,
                'failed': result.failed,
                'errors': result.errors[:10]
            }

        return {'status': 'success', 'processed': result.successful}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}
```

## Execution Checklist

- [ ] Processing mode matches workload type
- [ ] Worker count appropriate for resources
- [ ] Batch size prevents memory issues
- [ ] Progress callback configured for feedback
- [ ] Error handling in processor function
- [ ] Results aggregated and exported
- [ ] Summary statistics reviewed
- [ ] Failed files identified and logged

## Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Throughput | 2-3x sequential | Parallel speedup factor |
| Success Rate | >99% | Percentage of files processed |
| Memory Usage | <4GB | Peak memory consumption |
| Error Rate | <1% | Processing failures |

## Related Skills

- [data-pipeline-processor](../data-pipeline-processor/SKILL.md) - Data transformation
- [yaml-workflow-executor](../yaml-workflow-executor/SKILL.md) - Workflow automation
- [engineering-report-generator](../engineering-report-generator/SKILL.md) - Report generation

---

## Version History

- **1.1.0** (2026-01-02): Upgraded to SKILL_TEMPLATE_v2 format with Quick Start, Error Handling, Metrics, Execution Checklist, additional examples
- **1.0.0** (2024-10-15): Initial release with FileScanner, ParallelProcessor, progress tracking, result aggregation
