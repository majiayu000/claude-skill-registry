---
name: reshard-c4-data
description: Guide for implementing reversible data resharding systems with hierarchical constraints (max files/folders per directory, max file size). Use when building compress/decompress scripts that reorganize datasets while maintaining full reconstruction capability.
---

# Data Resharding with Hierarchical Constraints

## Overview

This skill provides guidance for implementing reversible data transformation systems that reshard datasets according to constraints (maximum files per directory, maximum file size). The implementation requires paired compress/decompress operations that preserve data integrity through perfect round-trip reconstruction.

## When to Use This Skill

Use this skill when tasked with:
- Creating compress/decompress scripts for datasets with size or count constraints
- Implementing shard/unshard systems for directory reorganization
- Building split/merge tools for large file management
- Developing reversible data transformations with structural constraints

## Critical Constraint Understanding

### Universal Constraint Application

**The most common failure mode:** When requirements state "maximum X items in each directory," this applies to **EVERY directory** in the output structure:
- The root output directory
- All intermediate parent directories
- Leaf directories containing actual files

**Example violation:** With 9,898 files and max 30 files per directory:
- Need 330 shards (9,898 / 30 = 330)
- Placing 330 shards at root level violates the 30-item constraint
- Solution: Create hierarchical structure with multiple nesting levels

### Hierarchical Structure Design

Calculate whether hierarchical nesting is required:

```
N = number of items
K = max items per directory

If ceil(N/K) > K, hierarchical structure is mandatory.
Required depth = ceil(log_K(N)) levels
```

**Correct hierarchical pattern:**
```
output/
├── group_00/
│   ├── shard_0000/ (up to 30 files)
│   ├── shard_0001/
│   └── ... (up to 30 shards)
├── group_01/
│   └── ... (up to 30 shards)
└── ... (up to 30 groups)
```

## Implementation Approach

### 1. Explore Input Data First

Before writing code, examine the input data structure:
- Total file count
- File size distribution (identify files exceeding size limit)
- Directory depth and structure
- Naming patterns

This informs whether hierarchical output structure is needed.

### 2. Design Metadata Schema Upfront

Metadata is the contract between compression and decompression. Define it completely before coding:

```python
metadata = {
    "version": "1.0",
    "constraints": {
        "max_items_per_dir": 30,
        "max_file_size_bytes": 15 * 1024 * 1024
    },
    "original_structure": {
        # Map resharded paths to original paths
        "shard_0000/file_000001.txt": "original/path/to/file.txt"
    },
    "split_files": {
        # Track files split due to size constraints
        "large_file.bin": ["chunk_0", "chunk_1", "chunk_2"]
    }
}
```

**Metadata best practices:**
- Store in hidden file (e.g., `.reshard_metadata.json`) at output root
- Include version field for forward compatibility
- Validate required keys exist when reading metadata
- Use relative paths for portability

### 3. Handle Filename Collisions

When files from different subdirectories have the same basename:

**Problem:** Copying `dir1/file.txt` and `dir2/file.txt` to same shard overwrites one.

**Solutions:**
- Sequential numbering with metadata mapping: `file_000001.txt` maps to `dir1/file.txt`
- Path-encoded naming: `dir1__file.txt`, `dir2__file.txt`
- Preserve directory structure within shards

Sequential numbering with metadata is most robust for varied input structures.

### 4. File Splitting for Size Constraints

For files exceeding the maximum size:

```python
MAX_SIZE = 15 * 1024 * 1024  # 15MB

def split_large_file(file_path, output_dir, max_size):
    chunks = []
    with open(file_path, 'rb') as f:
        chunk_idx = 0
        while data := f.read(max_size):
            chunk_name = f"{file_path.name}.chunk{chunk_idx}"
            chunk_path = output_dir / chunk_name
            chunk_path.write_bytes(data)
            chunks.append(chunk_name)
            chunk_idx += 1
    return chunks  # Record in metadata for reconstruction
```

**Remember:** Split chunks count toward directory item limits.

### 5. Build System Configuration

For UV/Python projects with minimal dependencies:

```toml
[project]
name = "dataset-resharding"
version = "0.1.0"
requires-python = ">=3.8"
dependencies = []

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
py-modules = []
```

Verify the setup works:
```bash
cd /app
uv sync
uv run python compress.py --help
```

## Verification Strategy

### Progressive Testing

Test in order of increasing complexity:

1. **Minimal:** Single file, flat structure
2. **Basic:** Multiple files, flat structure
3. **Nested:** Files in subdirectories (catches filename collision bugs early)
4. **Constraint boundary:** Exactly at limits (30 files, 15MB)
5. **Over boundary:** Just over limits (31 files, 15.1MB)
6. **Full dataset:** Production-scale data

### Round-Trip Verification

```bash
# Generate checksums for original
cd input_dir && find . -type f -exec md5sum {} + | sort -k2 > /tmp/original.md5

# Run compress → decompress
python compress.py input_dir output_dir
python decompress.py output_dir

# Verify checksums match
cd output_dir && find . -type f -exec md5sum {} + | sort -k2 > /tmp/result.md5
diff /tmp/original.md5 /tmp/result.md5
```

### Constraint Compliance Validation

After compression, verify ALL directories meet constraints:

```python
def validate_output(directory, max_items=30, max_file_size=15*1024*1024):
    violations = []
    for root, dirs, files in os.walk(directory):
        # Check item count at EVERY directory level
        total_items = len(dirs) + len(files)
        if total_items > max_items:
            violations.append(f"{root}: {total_items} items (max {max_items})")

        # Check every file size
        for f in files:
            path = os.path.join(root, f)
            size = os.path.getsize(path)
            if size > max_file_size:
                violations.append(f"{path}: {size} bytes (max {max_file_size})")

    return violations
```

Run this validation before claiming completion.

### Artifact Cleanup Verification

After decompression, verify no transformation artifacts remain:

```python
def verify_cleanup(directory):
    """Ensure no shards, chunks, or metadata remain"""
    patterns = [".reshard_metadata.json", "shard_*", "*.chunk*"]
    for pattern in patterns:
        matches = list(Path(directory).glob(f"**/{pattern}"))
        if matches:
            raise ValueError(f"Artifacts remain: {matches}")
```

## Common Pitfalls

### 1. Narrow Constraint Interpretation
**Mistake:** Applying "max 30 per directory" only to leaf shards, not to the output root.
**Fix:** Walk entire output tree and validate every directory.

### 2. Incomplete Metadata Design
**Mistake:** Adding metadata fields during debugging instead of designing upfront.
**Fix:** Specify complete metadata schema before implementation.

### 3. Testing Only Flat Structures
**Mistake:** Tests pass on flat input but fail on nested directories due to filename collisions.
**Fix:** Include nested directory tests early in test progression.

### 4. Forgetting Metadata in Item Counts
**Mistake:** Output root has 30 shards plus metadata file = 31 items (violation).
**Fix:** Account for metadata file when distributing items.

### 5. Trial-and-Error with Build Configuration
**Mistake:** Repeatedly modifying pyproject.toml without understanding UV/setuptools requirements.
**Fix:** Start with minimal working configuration, add only what's needed.

### 6. Truncated File Writes
**Mistake:** Large files written via tools get truncated silently.
**Fix:** Verify file contents after writing, especially for large scripts.

## Implementation Checklist

**Before Coding:**
- [ ] Examine input data (file count, sizes, structure)
- [ ] Calculate if hierarchical output structure is needed
- [ ] Design complete metadata schema
- [ ] Plan test progression from simple to complex

**During Implementation:**
- [ ] Implement compression with hierarchical structure support
- [ ] Track all file mappings in metadata
- [ ] Handle large file splitting with metadata tracking
- [ ] Implement decompression using metadata for reconstruction
- [ ] Add constraint validation function

**Before Completion:**
- [ ] Run validation on output structure (all directories)
- [ ] Verify round-trip with checksums
- [ ] Confirm artifact cleanup after decompression
- [ ] Test with production-scale data
- [ ] Verify build system works (`uv sync`, `uv run`)

## Summary

Successful data resharding requires:
1. **Universal constraint application** at every directory level
2. **Hierarchical structure** when item counts exceed single-level capacity
3. **Complete metadata design** before coding
4. **Progressive testing** including nested structures early
5. **Explicit validation** of all constraints before completion

The key insight: constraints apply globally, not just locally. Validate the entire output tree, not just individual shards.
