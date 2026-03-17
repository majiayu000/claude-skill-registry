---
name: numpy-specialist
description: Master NumPy array operations including vectorization, broadcasting, memory layout, and performance optimization. Use PROACTIVELY when working with numerical computing, array operations, or scientific computing in Python.
---

# NumPy Specialist

Master efficient numerical computing with NumPy, focusing on vectorization, broadcasting, and memory management.

## When to Use This Skill

- Numerical array operations
- Scientific computing
- Linear algebra computations
- Signal processing
- Image manipulation
- Machine learning data preparation
- Performance-critical numerical code

## Quick Reference

```python
import numpy as np

# Array creation
np.array([1, 2, 3])                    # From list
np.zeros((3, 4))                       # Zero matrix
np.ones((3, 4), dtype=np.float32)      # Ones with dtype
np.arange(0, 10, 0.5)                  # Range with step
np.linspace(0, 1, 100)                 # 100 points between 0-1
np.random.randn(3, 4)                  # Random normal

# Key operations
arr.shape, arr.dtype, arr.ndim         # Properties
arr.reshape(2, 6)                      # Reshape
np.sum(arr, axis=0)                    # Sum along axis
np.dot(a, b), a @ b                    # Matrix multiply
```

---

## Array Creation

### Basic Creation Methods

```python
import numpy as np

# ✅ From Python sequences
arr = np.array([1, 2, 3, 4])
matrix = np.array([[1, 2], [3, 4]])

# ✅ With explicit dtype for memory control
arr = np.array([1, 2, 3], dtype=np.float32)
integers = np.array([1, 2, 3], dtype=np.int32)

# ✅ Pre-allocated arrays
zeros = np.zeros((1000, 1000), dtype=np.float32)
ones = np.ones((100, 100))
empty = np.empty((100, 100))  # Uninitialized (fast)
full = np.full((10, 10), fill_value=7)

# ✅ Identity and diagonal
eye = np.eye(5)  # 5x5 identity
diag = np.diag([1, 2, 3, 4])  # Diagonal matrix
```

### Ranges and Spaces

```python
# ✅ Linear spacing
arr = np.arange(0, 100, 5)           # [0, 5, 10, ..., 95]
arr = np.linspace(0, 1, 50)          # 50 points between 0 and 1
arr = np.logspace(0, 3, 4)           # [1, 10, 100, 1000]

# ✅ Meshgrid for 2D coordinates
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sqrt(X**2 + Y**2)  # Distance from origin
```

### Random Arrays

```python
# ✅ Reproducible random generation
rng = np.random.default_rng(seed=42)

uniform = rng.random((100, 100))           # Uniform [0, 1)
normal = rng.standard_normal((100, 100))   # Standard normal
integers = rng.integers(0, 100, size=(10, 10))  # Random integers
choice = rng.choice([1, 2, 3, 4], size=20) # Random choice

# ✅ Shuffling and sampling
rng.shuffle(arr)                 # In-place shuffle
permuted = rng.permutation(arr)  # Return shuffled copy
sample = rng.choice(arr, size=10, replace=False)  # Without replacement
```

---

## Vectorization

### Replace Loops with Vector Operations

```python
# ❌ SLOW: Python loops
result = []
for i in range(len(arr)):
    result.append(arr[i] ** 2)
result = np.array(result)

# ❌ SLOW: List comprehension (still Python loop)
result = np.array([x ** 2 for x in arr])

# ✅ FAST: Vectorized operation (10-100x faster)
result = arr ** 2

# Performance comparison
arr = np.arange(1_000_000)
# Loop: ~500ms
# Vectorized: ~5ms
```

### Universal Functions (ufuncs)

```python
# ✅ Built-in ufuncs are highly optimized
arr = np.array([1, 4, 9, 16, 25])

# Element-wise operations
np.sqrt(arr)      # [1, 2, 3, 4, 5]
np.exp(arr)       # e^x for each element
np.log(arr)       # Natural log
np.sin(arr)       # Trigonometric
np.abs(arr)       # Absolute value

# Comparison operations
np.greater(arr, 5)     # [False, False, True, True, True]
np.maximum(arr1, arr2)  # Element-wise max
np.clip(arr, 3, 10)    # Clip values to range
```

### Custom Vectorized Functions

```python
# ✅ Vectorize custom functions
def custom_func(x):
    if x < 0:
        return 0
    elif x < 10:
        return x * 2
    else:
        return x ** 2

vectorized_func = np.vectorize(custom_func)
result = vectorized_func(arr)

# ⚠️ Note: np.vectorize is convenient but not truly vectorized
# For best performance, use np.where or np.select

# ✅ BETTER: np.where for conditions
result = np.where(arr < 0, 0, np.where(arr < 10, arr * 2, arr ** 2))

# ✅ BETTER: np.select for multiple conditions
conditions = [arr < 0, arr < 10]
choices = [0, arr * 2]
result = np.select(conditions, choices, default=arr ** 2)
```

---

## Broadcasting

### Understanding Broadcasting Rules

```python
# Broadcasting automatically expands arrays for operations
# Rules:
# 1. Arrays with fewer dims get leading dims of size 1
# 2. Dimensions of size 1 stretch to match the other array
# 3. Arrays must have compatible shapes

# Scalar broadcasts to all elements
arr = np.array([1, 2, 3])
result = arr + 5  # [6, 7, 8]

# 1D broadcasts across rows
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])  # Shape (2, 3)
row = np.array([1, 0, 1])      # Shape (3,)
result = matrix + row           # Broadcasting row to each matrix row

# Column vector broadcasts across columns
column = np.array([[10], [20]])  # Shape (2, 1)
result = matrix + column          # [[11, 12, 13], [24, 25, 26]]
```

### Practical Broadcasting Examples

```python
# ✅ Normalize columns (subtract mean, divide by std)
data = np.random.randn(100, 5)  # 100 samples, 5 features
mean = data.mean(axis=0)         # Shape (5,)
std = data.std(axis=0)           # Shape (5,)
normalized = (data - mean) / std  # Broadcasting works!

# ✅ Outer product via broadcasting
x = np.array([1, 2, 3])[:, np.newaxis]  # Shape (3, 1)
y = np.array([4, 5, 6])[np.newaxis, :]  # Shape (1, 3)
outer = x * y  # Shape (3, 3) - outer product

# ✅ Distance matrix (pairwise distances)
points = np.random.randn(100, 3)  # 100 points in 3D
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]  # (100, 100, 3)
distances = np.sqrt((diff ** 2).sum(axis=2))  # (100, 100)
```

### Avoiding Broadcasting Errors

```python
# ❌ Incompatible shapes
a = np.ones((3, 4))  # Shape (3, 4)
b = np.ones((2, 3))  # Shape (2, 3)
# a + b  # ValueError: shapes not aligned

# ✅ Check shapes before operations
print(f"Shape A: {a.shape}, Shape B: {b.shape}")

# ✅ Reshape to make compatible
b = b.reshape(3, 2)  # Now (3, 2)
# Still incompatible with (3, 4)

# ✅ Use np.broadcast_shapes to verify
try:
    result_shape = np.broadcast_shapes(a.shape, b.shape)
except ValueError as e:
    print(f"Cannot broadcast: {e}")
```

---

## Memory Layout

### Views vs Copies

```python
# ✅ Slicing creates a VIEW (shares memory)
arr = np.array([1, 2, 3, 4, 5])
view = arr[1:4]
view[0] = 999
print(arr)  # [1, 999, 3, 4, 5] - Original modified!

# ✅ Explicit copy when needed
arr = np.array([1, 2, 3, 4, 5])
copy = arr[1:4].copy()
copy[0] = 999
print(arr)  # [1, 2, 3, 4, 5] - Original unchanged

# ✅ Check if array shares memory
print(np.shares_memory(arr, view))  # True
print(np.shares_memory(arr, copy))  # False
```

### Contiguous Memory Layout

```python
# C-order (row-major) vs F-order (column-major)
c_array = np.array([[1, 2, 3], [4, 5, 6]], order='C')
f_array = np.array([[1, 2, 3], [4, 5, 6]], order='F')

print(c_array.flags['C_CONTIGUOUS'])  # True
print(f_array.flags['F_CONTIGUOUS'])  # True

# ✅ Operations on contiguous arrays are faster
# If performance matters, ensure contiguity
arr = np.ascontiguousarray(arr)
```

### Memory-Efficient Operations

```python
# ✅ In-place operations to save memory
arr = np.random.randn(10000, 10000).astype(np.float32)

# ❌ Creates new array (doubles memory)
arr = arr * 2

# ✅ In-place modification (no extra memory)
arr *= 2
np.multiply(arr, 2, out=arr)

# ✅ Use out parameter for ufuncs
result = np.empty_like(arr)
np.sqrt(arr, out=result)
```

---

## Data Types

### Choosing the Right dtype

```python
# ✅ Use smallest dtype that fits your data
# Floating point
np.float16  # Half precision (2 bytes)
np.float32  # Single precision (4 bytes) - Often sufficient
np.float64  # Double precision (8 bytes) - Default

# Integer
np.int8     # -128 to 127
np.int16    # -32,768 to 32,767
np.int32    # -2B to 2B
np.int64    # Very large integers - Default

# Unsigned
np.uint8    # 0 to 255 (images)
np.uint16   # 0 to 65,535
np.uint32   # 0 to 4B

# ✅ Memory comparison
arr_64 = np.random.randn(1000, 1000)  # Default float64
arr_32 = arr_64.astype(np.float32)     # Half the memory

print(f"float64: {arr_64.nbytes / 1024**2:.1f} MB")  # 7.6 MB
print(f"float32: {arr_32.nbytes / 1024**2:.1f} MB")  # 3.8 MB
```

### Type Coercion

```python
# ⚠️ NumPy arrays have single dtype - values are coerced
arr = np.array([1, 2, 'three'])
print(arr.dtype)  # '<U21' (string!) - integers became strings

# ✅ Be explicit about dtype
arr = np.array([1, 2, 3], dtype=np.float32)

# ✅ Convert types safely
float_arr = np.array([1.5, 2.7, 3.2])
int_arr = float_arr.astype(np.int32)  # Truncates: [1, 2, 3]
```

---

## Indexing and Slicing

### Advanced Indexing

```python
arr = np.arange(20).reshape(4, 5)

# ✅ Boolean indexing
mask = arr > 10
filtered = arr[mask]  # 1D array of values > 10

# ✅ Fancy indexing (integer arrays)
rows = np.array([0, 2, 3])
cols = np.array([1, 3, 4])
selected = arr[rows, cols]  # Elements at (0,1), (2,3), (3,4)

# ✅ Combining boolean and integer indexing
row_mask = np.array([True, False, True, False])
arr[row_mask, 2]  # Column 2 from rows 0 and 2

# ✅ np.where for conditional selection
indices = np.where(arr > 10)  # Returns (row_indices, col_indices)
values = arr[indices]
```

### Assigning with Indexing

```python
# ✅ Boolean assignment
arr[arr < 0] = 0  # Clip negative values to 0

# ✅ Fancy index assignment
arr[[0, 2, 4], :] = 999  # Set entire rows

# ✅ np.put and np.take for 1D operations
np.put(arr, [0, 5, 10], [100, 200, 300])
values = np.take(arr, [0, 5, 10])
```

---

## Linear Algebra

### Matrix Operations

```python
# ✅ Matrix multiplication
A = np.random.randn(100, 50)
B = np.random.randn(50, 30)

result = A @ B          # Preferred syntax
result = np.dot(A, B)   # Equivalent
result = np.matmul(A, B)  # Equivalent

# ✅ Other products
inner = np.inner(v1, v2)     # Inner product
outer = np.outer(v1, v2)     # Outer product
cross = np.cross(v1, v2)     # Cross product (3D vectors)

# ✅ Matrix operations
inv = np.linalg.inv(A)       # Inverse
det = np.linalg.det(A)       # Determinant
rank = np.linalg.matrix_rank(A)
trace = np.trace(A)           # Sum of diagonal
```

### Decompositions

```python
# ✅ Eigenvalue decomposition
eigenvalues, eigenvectors = np.linalg.eig(A)

# ✅ SVD
U, S, Vh = np.linalg.svd(A)

# ✅ QR decomposition
Q, R = np.linalg.qr(A)

# ✅ Cholesky decomposition (symmetric positive-definite)
L = np.linalg.cholesky(A)
```

### Solving Systems

```python
# Solve Ax = b
A = np.array([[3, 2], [1, 4]])
b = np.array([7, 6])

# ✅ Direct solve (preferred)
x = np.linalg.solve(A, b)

# ✅ Least squares (for overdetermined systems)
x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
```

---

## Performance Optimization

### Pre-allocation

```python
# ❌ Growing arrays dynamically
result = np.array([])
for i in range(10000):
    result = np.append(result, i ** 2)  # Copies entire array each time!

# ✅ Pre-allocate and fill
result = np.empty(10000)
for i in range(10000):
    result[i] = i ** 2

# ✅ BEST: Vectorize entirely
result = np.arange(10000) ** 2
```

### Use Appropriate Functions

```python
# ✅ Use specialized functions when available
arr = np.random.randn(1000, 1000)

# Sum
np.sum(arr)          # Optimized
# NOT: sum(arr.flatten())

# Max/Min
np.max(arr)          # Optimized
np.argmax(arr)       # Index of max

# Statistics
np.mean(arr)
np.std(arr)
np.median(arr)
np.percentile(arr, 95)
```

### Profiling

```python
# ✅ Use %timeit in Jupyter/IPython
# %timeit np.sum(arr)

# ✅ Or use timeit module
import timeit

time = timeit.timeit(
    'np.sum(arr)',
    globals={'np': np, 'arr': arr},
    number=100
)
print(f"Average: {time/100*1000:.2f} ms")
```

---

## Common Pitfalls

| Pitfall                | Problem              | Solution                   |
| ---------------------- | -------------------- | -------------------------- |
| Python loops           | Very slow            | Vectorize with ufuncs      |
| Growing arrays         | O(n²) copies         | Pre-allocate               |
| View vs copy confusion | Unintended mutations | Use `.copy()` explicitly   |
| Default float64        | Memory waste         | Specify `dtype=np.float32` |
| Shape mismatch         | Broadcasting errors  | Check `.shape` first       |
| Type coercion          | Data corruption      | Set `dtype` explicitly     |

## Best Practices Summary

1. **Vectorize Everything** - No Python loops for array ops
2. **Pre-allocate Arrays** - Use `np.empty()`, `np.zeros()`
3. **Choose Right dtype** - `float32` often sufficient
4. **Understand Views** - Use `.copy()` when needed
5. **Master Broadcasting** - Avoid explicit loops
6. **Use Built-in Functions** - `np.sum()`, not `sum()`
7. **Profile Performance** - `%timeit` for bottlenecks
8. **Consider Memory** - In-place ops, contiguous arrays


## Parent Hub
- [_data-ai-mastery](../_data-ai-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-data-pipeline](../_workflow-data-pipeline/SKILL.md)
