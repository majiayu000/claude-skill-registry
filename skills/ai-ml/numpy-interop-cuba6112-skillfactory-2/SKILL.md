---
name: numpy-interop
description: Protocols for cross-library data exchange including DLPack, buffer interfaces, and __array_ufunc__ for overriding NumPy functions. Triggers: DLPack, interoperability, __array_interface__, __array_ufunc__, buffer protocol.
---

## Overview
NumPy Interoperability encompasses the protocols that allow different numerical libraries (PyTorch, TensorFlow, SciPy) to exchange data without redundant copies. It focuses on modern standards like DLPack and the implementation of custom behavior for non-NumPy objects using the `__array_ufunc__` protocol.

## When to Use
- Passing data from a GPU-based library (like PyTorch) back to the CPU for NumPy analysis.
- Implementing custom array-like objects that should work seamlessly with `np.sin()` or `np.add()`.
- Interfacing with low-level C/C++ extensions using memory pointers and typestrings.
- Avoiding memory copies when moving large tensors between frameworks.

## Decision Tree
1. Exchanging data with a modern tensor library (PyTorch)?
   - Use `np.from_dlpack()`.
2. Creating a custom class that needs to handle NumPy operations?
   - Implement the `__array_ufunc__` method.
3. Accessing raw memory pointers for a C extension?
   - Inspect the `__array_interface__` attribute.

## Workflows
1. **Converting PyTorch Tensors to NumPy**
   - Ensure the PyTorch tensor is on the CPU: `tensor.cpu()`.
   - Convert using `np.from_dlpack(tensor)`.
   - The resulting NumPy array is a view of the tensor's memory.

2. **Overriding NumPy Ops for Subclasses**
   - Implement the `__array_ufunc__` method in a custom class.
   - Define how standard operations (like `np.sin`) should behave for your object.
   - Call `np.sin(my_obj)` and observe that your custom implementation is executed.

3. **Low-Level Memory Access via Interface**
   - Inspect an object's `__array_interface__` attribute.
   - Retrieve the 'data' pointer and 'typestr'.
   - Use these to wrap the memory in a third-party C/C++ extension for high-performance processing.

## Non-Obvious Insights
- **CPU Limitation:** NumPy currently only supports DLPack for CPU-resident data; GPU-resident objects must be moved to host memory before conversion.
- **Writeability Requirement:** Current NumPy implementations of DLPack primarily support writeable arrays; read-only arrays may fail to export.
- **Legacy Interfaces:** `__array_struct__` is considered legacy; developers should prioritize the buffer protocol or DLPack for new library integrations.

## Evidence
- "DLPack is yet another protocol to convert foreign objects to NumPy arrays in a language and device agnostic manner." [Source](https://numpy.org/doc/stable/user/basics.interoperability.html)
- "As long as foreign objects implement the __array_ufunc__ or __array_function__ protocols, it is possible to operate on them without the need for explicit conversion." [Source](https://numpy.org/doc/stable/user/basics.interoperability.html)

## Scripts
- `scripts/numpy-interop_tool.py`: Example of __array_ufunc__ implementation and DLPack usage.
- `scripts/numpy-interop_tool.js`: Simulated memory pointer inspection.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)