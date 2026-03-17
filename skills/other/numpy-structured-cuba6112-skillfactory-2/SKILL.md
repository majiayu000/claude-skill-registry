---
name: numpy-structured
description: Structured and record arrays for C-interoperability, binary blob interpretation, and multi-field tabular data handling. Triggers: structured array, record array, compound dtype, multi-field index.
---

## Overview
Structured arrays allow ndarrays to contain data with different types in named "fields," mimicking C structs. They are used primarily for interfacing with binary data from external sources and interpreting complex memory layouts without converting to high-level objects like Pandas DataFrames.

## When to Use
- Interpreting binary blobs or file headers from C/C++ applications.
- Storing tabular data where each row has multiple related attributes (e.g., ID, Timestamp, Value).
- Mapping hardware-aligned buffers to named fields for easier access.
- Performing multi-field updates on a shared data buffer.

## Decision Tree
1. Need to map names to columns in a single array buffer?
   - Use a structured array with a compound `dtype`.
2. Working with binary data from a file?
   - Use `arr.view(dtype=your_struct_dtype)` to interpret bytes without copying.
3. Selecting multiple fields?
   - Use a list of names `arr[['id', 'name']]`. This returns a view.

## Workflows
1. **Defining a Complex Data Record**
   - Construct a dtype using a list of tuples: `[('id', 'i4'), ('coord', 'f8', (3,))]`.
   - Instantiate the array with the custom dtype.
   - Access the 'coord' field to get an (N, 3) view of the coordinates.

2. **Mapping Binary Data to Structs**
   - Load raw bytes from a file or buffer.
   - View the buffer as a structured array: `arr.view(dtype=my_struct_dtype)`.
   - Access named fields to extract typed data from the raw binary.

3. **Multi-field View Modification**
   - Select a subset of fields using a list of names: `arr[['field1', 'field2']]`.
   - Update the resulting view with a new value.
   - Verify the original structured array has been modified in the specified fields.

## Non-Obvious Insights
- **Positional Assignment:** Assignment between two structured arrays is based on field position, not field name. If field 1 is 'id' in Array A and 'val' in Array B, Array B's 'val' will be assigned to Array A's 'id'.
- **Scalar Broadcasting:** Assigning a single scalar to a structured element (a whole row) will assign that value to all fields in the row.
- **Pandas vs Structured:** While structured arrays handle tabular data, they lack the high-level analysis features of Pandas; use them for low-level memory mapping and binary I/O, not statistical analysis.

## Evidence
- "Structured datatypes are designed to be able to mimic ‘structs’ in the C language, and share a similar memory layout." [Source](https://numpy.org/doc/stable/user/basics.rec.html)
- "Assignment between two structured arrays occurs as if the source elements had been converted to tuples... regardless of field names." [Source](https://numpy.org/doc/stable/user/basics.rec.html)

## Scripts
- `scripts/numpy-structured_tool.py`: Demonstrates defining compound dtypes and field views.
- `scripts/numpy-structured_tool.js`: Simulated struct field access.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)