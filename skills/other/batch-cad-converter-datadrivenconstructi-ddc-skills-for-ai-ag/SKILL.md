---
slug: "batch-cad-converter"
display_name: "Batch CAD Converter"
description: "Batch convert multiple CAD/BIM files (Revit, IFC, DWG, DGN) with progress tracking, error handling, and consolidated reporting."
---

# Batch CAD/BIM Converter

## Business Case

### Problem Statement
Large projects and archives contain hundreds or thousands of CAD/BIM files:
- Manual conversion is tedious and error-prone
- Different formats require different converters
- Progress tracking is needed for long operations
- Error handling is critical for large batches

### Solution
Unified batch converter handling all supported formats with progress tracking, error recovery, and consolidated reporting.

### Business Value
- **Multi-format** - Revit, IFC, DWG, DGN in one workflow
- **Error recovery** - Continue on failures
- **Progress tracking** - Monitor large batches
- **Reporting** - Consolidated conversion results

## Python Implementation

```python
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
import time
import json
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed


class CADFormat(Enum):
    """Supported CAD/BIM formats."""
    REVIT = (".rvt", ".rfa")
    IFC = (".ifc",)
    DWG = (".dwg",)
    DGN = (".dgn",)


class ConversionStatus(Enum):
    """Status of conversion operation."""
    PENDING = "pending"
    CONVERTING = "converting"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ConversionResult:
    """Result of single file conversion."""
    input_file: str
    output_file: Optional[str]
    format: str
    status: ConversionStatus
    start_time: datetime
    end_time: Optional[datetime]
    duration_seconds: float
    error_message: Optional[str] = None
    file_size_kb: float = 0


@dataclass
class BatchResult:
    """Result of batch conversion."""
    total_files: int
    successful: int
    failed: int
    skipped: int
    total_duration: float
    results: List[ConversionResult]
    start_time: datetime
    end_time: datetime


class BatchCADConverter:
    """Batch convert multiple CAD/BIM files."""

    # Default converter paths
    DEFAULT_CONVERTERS = {
        'revit': 'RvtExporter.exe',
        'ifc': 'IfcExporter.exe',
        'dwg': 'DwgExporter.exe',
        'dgn': 'DgnExporter.exe'
    }

    def __init__(self, converter_dir: str = ".",
                 converters: Dict[str, str] = None):
        self.converter_dir = Path(converter_dir)
        self.converters = converters or self.DEFAULT_CONVERTERS
        self.results: List[ConversionResult] = []
        self.progress_callback: Optional[Callable] = None

    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """Set callback for progress updates."""
        self.progress_callback = callback

    def _get_format(self, file_path: Path) -> Optional[str]:
        """Detect CAD format from extension."""
        ext = file_path.suffix.lower()

        for format_name, extensions in [
            ('revit', ('.rvt', '.rfa')),
            ('ifc', ('.ifc',)),
            ('dwg', ('.dwg',)),
            ('dgn', ('.dgn',))
        ]:
            if ext in extensions:
                return format_name

        return None

    def _get_converter(self, format_name: str) -> Optional[Path]:
        """Get converter path for format."""
        if format_name not in self.converters:
            return None

        converter = self.converter_dir / self.converters[format_name]
        if converter.exists():
            return converter

        # Try in system PATH
        return Path(self.converters[format_name])

    def convert_file(self, input_file: str,
                     output_dir: Optional[str] = None,
                     options: List[str] = None) -> ConversionResult:
        """Convert single file."""

        input_path = Path(input_file)
        start_time = datetime.now()

        # Detect format
        format_name = self._get_format(input_path)
        if not format_name:
            return ConversionResult(
                input_file=input_file,
                output_file=None,
                format='unknown',
                status=ConversionStatus.SKIPPED,
                start_time=start_time,
                end_time=datetime.now(),
                duration_seconds=0,
                error_message="Unsupported format"
            )

        # Get converter
        converter = self._get_converter(format_name)
        if not converter:
            return ConversionResult(
                input_file=input_file,
                output_file=None,
                format=format_name,
                status=ConversionStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                duration_seconds=0,
                error_message=f"Converter not found for {format_name}"
            )

        # Build command
        cmd = [str(converter), str(input_path)]
        if options:
            cmd.extend(options)

        # Execute
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Determine output file
            output_file = input_path.with_suffix('.xlsx')
            if output_dir:
                output_file = Path(output_dir) / output_file.name

            if result.returncode == 0 and output_file.exists():
                return ConversionResult(
                    input_file=input_file,
                    output_file=str(output_file),
                    format=format_name,
                    status=ConversionStatus.SUCCESS,
                    start_time=start_time,
                    end_time=end_time,
                    duration_seconds=duration,
                    file_size_kb=output_file.stat().st_size / 1024
                )
            else:
                return ConversionResult(
                    input_file=input_file,
                    output_file=None,
                    format=format_name,
                    status=ConversionStatus.FAILED,
                    start_time=start_time,
                    end_time=end_time,
                    duration_seconds=duration,
                    error_message=result.stderr or "Conversion failed"
                )

        except subprocess.TimeoutExpired:
            return ConversionResult(
                input_file=input_file,
                output_file=None,
                format=format_name,
                status=ConversionStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                duration_seconds=3600,
                error_message="Timeout exceeded (1 hour)"
            )

        except Exception as e:
            return ConversionResult(
                input_file=input_file,
                output_file=None,
                format=format_name,
                status=ConversionStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                duration_seconds=0,
                error_message=str(e)
            )

    def batch_convert(self, input_folder: str,
                      output_folder: Optional[str] = None,
                      include_subfolders: bool = True,
                      formats: List[str] = None,
                      options: Dict[str, List[str]] = None,
                      parallel: bool = False,
                      max_workers: int = 4) -> BatchResult:
        """Convert all files in folder."""

        start_time = datetime.now()
        input_path = Path(input_folder)

        # Find all supported files
        files = []
        pattern = "**/*" if include_subfolders else "*"

        for ext in ['.rvt', '.rfa', '.ifc', '.dwg', '.dgn']:
            files.extend(input_path.glob(f"{pattern}{ext}"))

        # Filter by format if specified
        if formats:
            files = [f for f in files if self._get_format(f) in formats]

        total_files = len(files)
        self.results = []

        # Create output directory
        if output_folder:
            Path(output_folder).mkdir(parents=True, exist_ok=True)

        # Process files
        if parallel and total_files > 1:
            self._convert_parallel(files, output_folder, options, max_workers)
        else:
            self._convert_sequential(files, output_folder, options)

        end_time = datetime.now()

        # Calculate statistics
        successful = sum(1 for r in self.results if r.status == ConversionStatus.SUCCESS)
        failed = sum(1 for r in self.results if r.status == ConversionStatus.FAILED)
        skipped = sum(1 for r in self.results if r.status == ConversionStatus.SKIPPED)

        return BatchResult(
            total_files=total_files,
            successful=successful,
            failed=failed,
            skipped=skipped,
            total_duration=(end_time - start_time).total_seconds(),
            results=self.results,
            start_time=start_time,
            end_time=end_time
        )

    def _convert_sequential(self, files: List[Path],
                            output_folder: Optional[str],
                            options: Dict[str, List[str]]):
        """Convert files sequentially."""

        total = len(files)
        for i, file_path in enumerate(files, 1):
            if self.progress_callback:
                self.progress_callback(i, total, str(file_path))

            format_name = self._get_format(file_path)
            format_options = options.get(format_name, []) if options else []

            result = self.convert_file(str(file_path), output_folder, format_options)
            self.results.append(result)

            status_symbol = "✓" if result.status == ConversionStatus.SUCCESS else "✗"
            print(f"[{i}/{total}] {status_symbol} {file_path.name}")

    def _convert_parallel(self, files: List[Path],
                          output_folder: Optional[str],
                          options: Dict[str, List[str]],
                          max_workers: int):
        """Convert files in parallel."""

        total = len(files)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}

            for file_path in files:
                format_name = self._get_format(file_path)
                format_options = options.get(format_name, []) if options else []
                future = executor.submit(self.convert_file, str(file_path), output_folder, format_options)
                futures[future] = file_path

            completed = 0
            for future in as_completed(futures):
                completed += 1
                result = future.result()
                self.results.append(result)

                if self.progress_callback:
                    self.progress_callback(completed, total, str(futures[future]))

    def generate_report(self, batch_result: BatchResult,
                        output_path: str = None) -> str:
        """Generate conversion report."""

        report = {
            'summary': {
                'total_files': batch_result.total_files,
                'successful': batch_result.successful,
                'failed': batch_result.failed,
                'skipped': batch_result.skipped,
                'success_rate': round(batch_result.successful / batch_result.total_files * 100, 1) if batch_result.total_files > 0 else 0,
                'total_duration_seconds': round(batch_result.total_duration, 2),
                'start_time': batch_result.start_time.isoformat(),
                'end_time': batch_result.end_time.isoformat()
            },
            'results': [
                {
                    'input': r.input_file,
                    'output': r.output_file,
                    'format': r.format,
                    'status': r.status.value,
                    'duration': round(r.duration_seconds, 2),
                    'error': r.error_message
                }
                for r in batch_result.results
            ]
        }

        report_json = json.dumps(report, indent=2)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_json)

        return report_json


# Progress callback example
def print_progress(current: int, total: int, file_name: str):
    """Print progress to console."""
    percent = current / total * 100
    print(f"Progress: {current}/{total} ({percent:.1f}%) - {file_name}")
```

## Quick Start

```python
# Initialize batch converter
converter = BatchCADConverter(converter_dir="C:/DDC/")

# Set progress callback
converter.set_progress_callback(print_progress)

# Convert all files
result = converter.batch_convert(
    input_folder="C:/Projects",
    output_folder="C:/Converted",
    include_subfolders=True
)

print(f"Success: {result.successful}/{result.total_files}")
```

## Common Use Cases

### 1. Convert Specific Formats Only
```python
result = converter.batch_convert(
    input_folder="C:/Archive",
    formats=['revit', 'ifc'],  # Only Revit and IFC
    parallel=True,
    max_workers=4
)
```

### 2. With Format-Specific Options
```python
options = {
    'revit': ['complete', 'bbox', 'rooms'],
    'ifc': ['bbox'],
    'dwg': []
}
result = converter.batch_convert(
    input_folder="C:/Projects",
    options=options
)
```

### 3. Generate Report
```python
result = converter.batch_convert("C:/Projects")
report = converter.generate_report(result, "conversion_report.json")
```

## Resources
- **GitHub**: [cad2data Pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto)
