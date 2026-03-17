---
name: numpy-io
description: File I/O operations including binary formats (npy/npz), text processing (csv), and memory-mapping for huge datasets. Triggers: io, load, save, npz, genfromtxt, memmap, loadtxt.
---

## Overview
NumPy I/O handles the transition of data between system memory and persistent storage. It supports highly efficient binary formats (.npy, .npz), flexible text parsers for messy data, and memory-mapping for datasets that exceed available RAM.

## When to Use
- Storing model weights or large datasets in a compressed binary format.
- Reading messy CSV files with missing data or mixed types.
- Processing multi-gigabyte datasets without loading the entire file into memory.
- Bundling multiple related arrays into a single archive file.

## Decision Tree
1. Storing data for future NumPy use?
   - Use `.npy` for single arrays, `.npz` for multiple arrays.
2. Is the file larger than your RAM?
   - Use `np.memmap` to access disk segments lazily.
3. Reading a clean CSV?
   - Use `np.loadtxt` (fast).
4. Reading a messy CSV with missing values?
   - Use `np.genfromtxt` (feature-rich but slower).

## Workflows
1. **Handling Large Disk-Bound Arrays**
   - Create a memory-mapped file with `np.memmap(filename, dtype='float32', mode='w+', shape=shape)`.
   - Process or fill the array as if it were in memory.
   - Call `.flush()` to ensure all data is written to the physical disk.

2. **Importing Messy CSV Data**
   - Define a dictionary of converters for specific columns.
   - Use `np.genfromtxt(csv_file, delimiter=',', skip_header=1, converters=converters)`.
   - Access the data which now has NaNs or default values where data was missing.

3. **Bundling Multiple Arrays for Storage**
   - Identify several related ndarrays.
   - Save them into a single archive with `np.savez_compressed('data.npz', arr1=arr1, arr2=arr2)`.
   - Load them later using `data = np.load('data.npz')` and access via `data['arr1']`.

## Non-Obvious Insights
- **Manual Flush Requirement:** Changes to a `memmap` array are not guaranteed to persist on disk until `.flush()` is called.
- **NPZ Lazy Loading:** `.npz` files are ZIP archives; `np.load` on an `.npz` does not load the data until you access a specific key.
- **Parser Capability:** `genfromtxt` handles column selection, comment characters, and missing value substitution automatically, making it the primary tool for "real-world" text data.

## Evidence
- "Memory-mapped files are used for accessing small segments of large files on disk, without reading the entire file into memory." [Source](https://numpy.org/doc/stable/reference/generated/numpy.memmap.html)
- "savez_compressed... Save several arrays into a single file in compressed .npz format." [Source](https://numpy.org/doc/stable/reference/routines.io.html)

## Scripts
- `scripts/numpy-io_tool.py`: Functions for memmap creation and compressed npz saving.
- `scripts/numpy-io_tool.js`: Basic CSV line parser simulation.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)