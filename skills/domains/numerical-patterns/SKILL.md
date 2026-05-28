---
name: numerical-patterns
description: Numerical computing patterns for C++20 including matrix operations, iterative solvers, numerical stability, data pipelines, and HPC I/O with MPI-IO and HDF5.
---

# Numerical Computing Patterns for C++20

Domain knowledge for scientific computing, numerical methods, and HPC I/O operations.

## Matrix Operations

### Dense Matrix with BLAS Integration

```cpp
#include <span>
#include <vector>

class DenseMatrix {
public:
  DenseMatrix(size_t rows, size_t cols)
      : rows_(rows), cols_(cols), data_(rows * cols, 0.0) {}

  double& operator()(size_t i, size_t j) { return data_[i * cols_ + j]; }
  double operator()(size_t i, size_t j) const { return data_[i * cols_ + j]; }

  size_t Rows() const { return rows_; }
  size_t Cols() const { return cols_; }
  std::span<double> Data() { return data_; }
  std::span<const double> Data() const { return data_; }

  // Matrix-vector product: y = A * x
  void Apply(std::span<double> y, std::span<const double> x) const {
    assert(x.size() == cols_ && y.size() == rows_);
    for (size_t i = 0; i < rows_; ++i) {
      double sum = 0.0;
      for (size_t j = 0; j < cols_; ++j) {
        sum += data_[i * cols_ + j] * x[j];
      }
      y[i] = sum;
    }
  }

private:
  size_t rows_, cols_;
  std::vector<double> data_;  // Row-major
};
```

### Sparse Matrix (CSR Format)

```cpp
class SparseMatrixCSR {
public:
  SparseMatrixCSR(size_t rows, size_t cols,
                  std::vector<double> values,
                  std::vector<int> col_indices,
                  std::vector<int> row_ptr)
      : rows_(rows), cols_(cols),
        values_(std::move(values)),
        col_indices_(std::move(col_indices)),
        row_ptr_(std::move(row_ptr)) {}

  // SpMV: y = A * x
  void Apply(std::span<double> y, std::span<const double> x) const {
    assert(x.size() == cols_ && y.size() == rows_);
    for (size_t i = 0; i < rows_; ++i) {
      double sum = 0.0;
      for (int k = row_ptr_[i]; k < row_ptr_[i + 1]; ++k) {
        sum += values_[k] * x[col_indices_[k]];
      }
      y[i] = sum;
    }
  }

  size_t Rows() const { return rows_; }
  size_t Cols() const { return cols_; }
  size_t Nnz() const { return values_.size(); }

private:
  size_t rows_, cols_;
  std::vector<double> values_;
  std::vector<int> col_indices_;
  std::vector<int> row_ptr_;
};
```

## Iterative Solvers

### Conjugate Gradient Method

```cpp
struct SolverResult {
  int iterations;
  double residual_norm;
  bool converged;
};

template <typename MatrixType>
SolverResult ConjugateGradient(const MatrixType& A,
                                std::span<double> x,
                                std::span<const double> b,
                                double tol = 1e-10,
                                int max_iter = 10000) {
  const size_t n = x.size();
  std::vector<double> r(n), p(n), Ap(n);

  // r = b - A*x
  A.Apply(r, x);
  for (size_t i = 0; i < n; ++i) r[i] = b[i] - r[i];

  std::copy(r.begin(), r.end(), p.begin());
  double rr = DotProduct(r, r);
  double b_norm = std::sqrt(DotProduct(b, b));
  if (b_norm == 0.0) b_norm = 1.0;

  for (int iter = 0; iter < max_iter; ++iter) {
    A.Apply(Ap, p);
    double pAp = DotProduct(p, Ap);
    if (std::abs(pAp) < 1e-300) break;  // Breakdown

    double alpha = rr / pAp;

    for (size_t i = 0; i < n; ++i) {
      x[i] += alpha * p[i];
      r[i] -= alpha * Ap[i];
    }

    double rr_new = DotProduct(r, r);
    double res_norm = std::sqrt(rr_new) / b_norm;

    if (res_norm < tol) {
      return {iter + 1, res_norm, true};
    }

    double beta = rr_new / rr;
    for (size_t i = 0; i < n; ++i) {
      p[i] = r[i] + beta * p[i];
    }
    rr = rr_new;
  }

  return {max_iter, std::sqrt(rr) / b_norm, false};
}
```

### GMRES (Generalized Minimum Residual)

```cpp
template <typename MatrixType>
SolverResult GMRES(const MatrixType& A,
                   std::span<double> x,
                   std::span<const double> b,
                   int restart = 30,
                   double tol = 1e-10,
                   int max_iter = 1000) {
  const size_t n = x.size();
  std::vector<double> r(n);

  for (int outer = 0; outer < max_iter / restart; ++outer) {
    // Compute r = b - A*x
    A.Apply(r, x);
    for (size_t i = 0; i < n; ++i) r[i] = b[i] - r[i];

    double beta = L2Norm(r);
    if (beta < tol) return {outer * restart, beta, true};

    // Arnoldi process + least squares solve
    std::vector<std::vector<double>> V(restart + 1, std::vector<double>(n));
    std::vector<std::vector<double>> H(restart + 1, std::vector<double>(restart, 0.0));

    for (size_t i = 0; i < n; ++i) V[0][i] = r[i] / beta;

    // ... Arnoldi iteration and Givens rotations
    // (Full implementation follows standard GMRES algorithm)
  }

  return {max_iter, L2Norm(r), false};
}
```

## Numerical Stability

### Kahan Summation (Compensated Summation)

```cpp
double KahanSum(std::span<const double> values) {
  double sum = 0.0;
  double compensation = 0.0;

  for (double val : values) {
    double y = val - compensation;
    double t = sum + y;
    compensation = (t - sum) - y;
    sum = t;
  }
  return sum;
}
```

### Numerically Stable Norm Computation

```cpp
double StableL2Norm(std::span<const double> x) {
  if (x.empty()) return 0.0;

  // Find max absolute value to avoid overflow/underflow
  double max_val = 0.0;
  for (double val : x) {
    max_val = std::max(max_val, std::abs(val));
  }
  if (max_val == 0.0) return 0.0;

  // Scale values before squaring
  double sum = 0.0;
  for (double val : x) {
    double scaled = val / max_val;
    sum += scaled * scaled;
  }
  return max_val * std::sqrt(sum);
}
```

### Condition Number Estimation

```cpp
// Estimate condition number using power iteration
double EstimateConditionNumber(const auto& A, size_t n, int max_iter = 100) {
  std::vector<double> x(n, 1.0 / std::sqrt(n));
  std::vector<double> y(n);

  // Estimate largest singular value
  double sigma_max = 0.0;
  for (int iter = 0; iter < max_iter; ++iter) {
    A.Apply(y, x);
    sigma_max = L2Norm(y);
    if (sigma_max == 0.0) break;
    for (size_t i = 0; i < n; ++i) x[i] = y[i] / sigma_max;
  }

  // For condition number, also need smallest singular value
  // (use inverse iteration or SVD for accurate estimate)
  return sigma_max;  // Simplified: returns spectral radius
}
```

## Data Pipelines

### Streaming Processor Pattern

```cpp
template <typename T>
class DataPipeline {
public:
  using ProcessFunc = std::function<std::vector<T>(std::span<const T>)>;

  DataPipeline& AddStage(ProcessFunc func) {
    stages_.push_back(std::move(func));
    return *this;
  }

  std::vector<T> Process(std::span<const T> input) const {
    std::vector<T> current(input.begin(), input.end());
    for (const auto& stage : stages_) {
      current = stage(current);
    }
    return current;
  }

private:
  std::vector<ProcessFunc> stages_;
};

// Usage
auto pipeline = DataPipeline<double>()
    .AddStage([](std::span<const double> data) {
      // Normalize
      double max_val = *std::ranges::max_element(data);
      std::vector<double> out(data.size());
      std::ranges::transform(data, out.begin(), [max_val](double x) { return x / max_val; });
      return out;
    })
    .AddStage([](std::span<const double> data) {
      // Filter outliers
      std::vector<double> out;
      std::ranges::copy_if(data, std::back_inserter(out),
                           [](double x) { return std::abs(x) < 3.0; });
      return out;
    });

auto result = pipeline.Process(raw_data);
```

### Chunked Processing for Large Datasets

```cpp
template <typename Func>
void ProcessChunked(const std::filesystem::path& input_file,
                    const std::filesystem::path& output_file,
                    Func&& process, size_t chunk_size = 1 << 20) {
  std::ifstream in(input_file, std::ios::binary);
  std::ofstream out(output_file, std::ios::binary);

  std::vector<double> buffer(chunk_size);
  while (in) {
    in.read(reinterpret_cast<char*>(buffer.data()),
            chunk_size * sizeof(double));
    size_t count = in.gcount() / sizeof(double);
    if (count == 0) break;

    auto chunk = std::span(buffer.data(), count);
    process(chunk);

    out.write(reinterpret_cast<const char*>(chunk.data()),
              count * sizeof(double));
  }
}
```

## HPC I/O

### MPI-IO for Parallel File Access

```cpp
#include <mpi.h>

void ParallelWrite(MPI_Comm comm, const std::filesystem::path& filename,
                   std::span<const double> local_data) {
  int rank, size;
  MPI_Comm_rank(comm, &rank);
  MPI_Comm_size(comm, &size);

  MPI_File fh;
  MPI_File_open(comm, filename.c_str(),
                MPI_MODE_CREATE | MPI_MODE_WRONLY, MPI_INFO_NULL, &fh);

  // Each process writes at its offset
  MPI_Offset offset = rank * local_data.size() * sizeof(double);
  MPI_File_write_at(fh, offset, local_data.data(),
                    local_data.size(), MPI_DOUBLE, MPI_STATUS_IGNORE);

  MPI_File_close(&fh);
}

void ParallelRead(MPI_Comm comm, const std::filesystem::path& filename,
                  std::span<double> local_data) {
  MPI_File fh;
  MPI_File_open(comm, filename.c_str(), MPI_MODE_RDONLY, MPI_INFO_NULL, &fh);

  int rank;
  MPI_Comm_rank(comm, &rank);
  MPI_Offset offset = rank * local_data.size() * sizeof(double);
  MPI_File_read_at(fh, offset, local_data.data(),
                   local_data.size(), MPI_DOUBLE, MPI_STATUS_IGNORE);

  MPI_File_close(&fh);
}
```

### HDF5 Integration

```cpp
#include <hdf5.h>

class HDF5Writer {
public:
  explicit HDF5Writer(const std::string& filename)
      : file_id_(H5Fcreate(filename.c_str(), H5F_ACC_TRUNC,
                            H5P_DEFAULT, H5P_DEFAULT)) {}

  ~HDF5Writer() {
    if (file_id_ >= 0) H5Fclose(file_id_);
  }

  void WriteDataset(const std::string& name, std::span<const double> data,
                    const std::vector<hsize_t>& dims) {
    hid_t space = H5Screate_simple(dims.size(), dims.data(), nullptr);
    hid_t dset = H5Dcreate2(file_id_, name.c_str(), H5T_NATIVE_DOUBLE,
                             space, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
    H5Dwrite(dset, H5T_NATIVE_DOUBLE, H5S_ALL, H5S_ALL, H5P_DEFAULT, data.data());
    H5Dclose(dset);
    H5Sclose(space);
  }

  void WriteAttribute(const std::string& dataset, const std::string& attr_name,
                      double value) {
    hid_t dset = H5Dopen2(file_id_, dataset.c_str(), H5P_DEFAULT);
    hid_t space = H5Screate(H5S_SCALAR);
    hid_t attr = H5Acreate2(dset, attr_name.c_str(), H5T_NATIVE_DOUBLE,
                             space, H5P_DEFAULT, H5P_DEFAULT);
    H5Awrite(attr, H5T_NATIVE_DOUBLE, &value);
    H5Aclose(attr);
    H5Sclose(space);
    H5Dclose(dset);
  }

private:
  hid_t file_id_;
};

// Usage
HDF5Writer writer("simulation_output.h5");
writer.WriteDataset("/timestep_0/temperature", temp_data, {nx, ny, nz});
writer.WriteAttribute("/timestep_0/temperature", "time", current_time);
```

### Binary I/O with Metadata

```cpp
struct FileHeader {
  char magic[4] = {'H', 'P', 'C', '\0'};
  uint32_t version = 1;
  uint64_t num_elements;
  uint64_t num_dimensions;
  double time;

  static constexpr size_t kSize = 32;  // Fixed header size
};

void WriteBinaryField(const std::filesystem::path& path,
                      std::span<const double> data,
                      const std::vector<size_t>& dims,
                      double time) {
  std::ofstream out(path, std::ios::binary);
  FileHeader header;
  header.num_elements = data.size();
  header.num_dimensions = dims.size();
  header.time = time;
  out.write(reinterpret_cast<const char*>(&header), sizeof(header));
  out.write(reinterpret_cast<const char*>(dims.data()),
            dims.size() * sizeof(size_t));
  out.write(reinterpret_cast<const char*>(data.data()),
            data.size() * sizeof(double));
}
```

---

**Key Principles**:
1. Choose the right data structure for access patterns
2. Verify numerical stability with unit tests (edge cases near machine epsilon)
3. Use established libraries (BLAS, LAPACK, HDF5) for production numerics
4. Profile I/O separately from computation
5. Test with both small and large datasets
