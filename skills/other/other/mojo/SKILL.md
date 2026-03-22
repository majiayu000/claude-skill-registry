---
name: mojo
description: Expert guidance for Mojo, the programming language by Modular that combines Python's usability with C-level performance. Helps developers write high-performance AI/ML code, optimize numerical computations with SIMD and parallelism, and gradually port Python code to Mojo for orders-of-magnitude speedups.
license: Apache-2.0
compatibility: No special requirements
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
  - mojo
  - modular
  - python
  - performance
  - ai
---

# Mojo — Python-Speed Systems Language for AI


## Overview


Mojo, the programming language by Modular that combines Python's usability with C-level performance. Helps developers write high-performance AI/ML code, optimize numerical computations with SIMD and parallelism, and gradually port Python code to Mojo for orders-of-magnitude speedups.


## Instructions

### Python Compatibility

```mojo
# Mojo can run Python code directly and call Python libraries.
# Start with Python, optimize hot paths in Mojo.

from python import Python

fn main() raises:
    # Import any Python library
    let np = Python.import_module("numpy")
    let plt = Python.import_module("matplotlib.pyplot")

    # Use NumPy arrays as usual
    let data = np.random.randn(1000)
    let mean = np.mean(data)
    let std = np.std(data)
    print("Mean:", mean, "Std:", std)

    # Plot with matplotlib
    plt.hist(data, bins=30)
    plt.title("Distribution")
    plt.savefig("plot.png")
```

### High-Performance Structs

```mojo
# matrix.mojo — Custom matrix type with SIMD operations
# This runs 10-100x faster than equivalent NumPy for small matrices.

from math import sqrt
from algorithm import vectorize, parallelize

struct Matrix:
    var data: DTypePointer[DType.float64]
    var rows: Int
    var cols: Int

    fn __init__(inout self, rows: Int, cols: Int):
        self.rows = rows
        self.cols = cols
        self.data = DTypePointer[DType.float64].alloc(rows * cols)
        memset_zero(self.data, rows * cols)

    fn __getitem__(self, row: Int, col: Int) -> Float64:
        return self.data.load(row * self.cols + col)

    fn __setitem__(inout self, row: Int, col: Int, val: Float64):
        self.data.store(row * self.cols + col, val)

    fn __del__(owned self):
        self.data.free()

    fn matmul(self, other: Matrix) -> Matrix:
        """Matrix multiplication using SIMD vectorization.

        Processes multiple floating-point operations per CPU instruction.
        On a modern CPU with 256-bit SIMD, this processes 4 float64 ops
        at once — a 4x speedup over scalar code.
        """
        var result = Matrix(self.rows, other.cols)
        let simd_width = simdwidthof[DType.float64]()

        @parameter
        fn calc_row(row: Int):
            for k in range(self.cols):
                @parameter
                fn dot[simd_width: Int](col: Int):
                    result.data.store[width=simd_width](
                        row * other.cols + col,
                        result.data.load[width=simd_width](row * other.cols + col)
                        + self[row, k] * other.data.load[width=simd_width](k * other.cols + col)
                    )
                vectorize[dot, simd_width](other.cols)

        parallelize[calc_row](self.rows)    # Parallelize across CPU cores
        return result

    fn frobenius_norm(self) -> Float64:
        """Compute the Frobenius norm using SIMD reduction."""
        var sum: Float64 = 0.0
        let simd_width = simdwidthof[DType.float64]()

        @parameter
        fn accumulate[width: Int](idx: Int):
            let vals = self.data.load[width=width](idx)
            sum += (vals * vals).reduce_add()

        vectorize[accumulate, simd_width](self.rows * self.cols)
        return sqrt(sum)
```

### SIMD and Vectorization

```mojo
# simd_example.mojo — Process data in parallel lanes
from algorithm import vectorize
from sys.info import simdwidthof

fn relu_activation(inout data: DTypePointer[DType.float32], size: Int):
    """Apply ReLU activation using SIMD.

    Processes 8 float32 values simultaneously on AVX2 CPUs,
    or 16 on AVX-512. The @parameter decorator ensures the
    SIMD width is resolved at compile time.
    """
    let simd_width = simdwidthof[DType.float32]()  # 8 on AVX2

    @parameter
    fn apply_relu[width: Int](idx: Int):
        let values = data.load[width=width](idx)
        let zeros = SIMD[DType.float32, width](0)
        data.store[width=width](idx, values.max(zeros))

    vectorize[apply_relu, simd_width](size)


fn softmax(inout data: DTypePointer[DType.float32], size: Int):
    """Numerically stable softmax with SIMD operations."""
    # Find max for numerical stability
    var max_val: Float32 = data.load(0)
    for i in range(1, size):
        let val = data.load(i)
        if val > max_val:
            max_val = val

    # Compute exp(x - max) and sum
    var sum: Float32 = 0.0
    for i in range(size):
        let exp_val = math.exp(data.load(i) - max_val)
        data.store(i, exp_val)
        sum += exp_val

    # Normalize
    let inv_sum = 1.0 / sum
    let simd_width = simdwidthof[DType.float32]()

    @parameter
    fn normalize[width: Int](idx: Int):
        data.store[width=width](idx, data.load[width=width](idx) * inv_sum)

    vectorize[normalize, simd_width](size)
```

### Parallelism

```mojo
# parallel.mojo — Multi-core parallel processing
from algorithm import parallelize, vectorize
from time import now

fn parallel_image_processing(
    inout pixels: DTypePointer[DType.uint8],
    width: Int,
    height: Int,
):
    """Apply grayscale conversion in parallel across CPU cores.

    Each row is processed by a different core, and within each row,
    SIMD processes multiple pixels simultaneously.
    """
    @parameter
    fn process_row(row: Int):
        let row_offset = row * width * 3    # 3 channels (RGB)

        for col in range(width):
            let idx = row_offset + col * 3
            let r = pixels.load(idx).cast[DType.float32]()
            let g = pixels.load(idx + 1).cast[DType.float32]()
            let b = pixels.load(idx + 2).cast[DType.float32]()

            # Luminance formula: 0.299R + 0.587G + 0.114B
            let gray = (0.299 * r + 0.587 * g + 0.114 * b).cast[DType.uint8]()
            pixels.store(idx, gray)
            pixels.store(idx + 1, gray)
            pixels.store(idx + 2, gray)

    parallelize[process_row](height)    # Each core handles a subset of rows
```

## Installation

```bash
# Install Modular CLI
curl -s https://get.modular.com | sh -

# Install Mojo
modular install mojo

# Verify
mojo --version

# Run a Mojo file
mojo run my_program.mojo

# Build a binary
mojo build my_program.mojo -o my_program
```


## Examples


### Example 1: Building a feature with Mojo

**User request:**

```
Add a real-time collaborative python compatibility to my React app using Mojo.
```

The agent installs the package, creates the component with proper Mojo initialization, implements the python compatibility with event handling and state management, and adds TypeScript types for the integration.

### Example 2: Migrating an existing feature to Mojo

**User request:**

```
I have a basic high-performance structs built with custom code. Migrate it to use Mojo for better high-performance structs support.
```

The agent reads the existing implementation, maps the custom logic to Mojo's API, rewrites the components using Mojo's primitives, preserves existing behavior, and adds features only possible with Mojo (like SIMD and Vectorization, Parallelism).


## Guidelines

1. **Start with Python, optimize in Mojo** — Use Python imports for prototyping; rewrite hot loops in native Mojo for 10-1000x speedups
2. **Use SIMD for data processing** — `vectorize` processes multiple values per instruction; always prefer it over scalar loops for numeric data
3. **Parallelize across cores** — `parallelize` distributes work across CPU cores; combine with `vectorize` for maximum throughput
4. **`fn` over `def`** — Use `fn` for performance-critical functions (strict typing, no overhead); use `def` for flexibility
5. **Owned and borrowed references** — Use `borrowed` (default) for read-only, `inout` for mutation, `owned` for transfers; this enables zero-copy optimizations
6. **Compile-time metaprogramming** — Use `@parameter` for compile-time evaluation; SIMD widths, loop unrolling, and specialization happen at compile time
7. **Profile before optimizing** — Use `mojo build -O3` and benchmark; not everything needs SIMD — focus on actual bottlenecks
8. **Gradual migration** — Port one function at a time from Python to Mojo; the interop layer makes incremental adoption easy
