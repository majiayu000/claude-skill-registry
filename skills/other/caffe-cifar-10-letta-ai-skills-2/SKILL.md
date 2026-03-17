---
name: caffe-cifar-10
description: Guidance for building and training with the Caffe deep learning framework on CIFAR-10 dataset. This skill applies when tasks involve compiling Caffe from source, training convolutional neural networks on image classification datasets, or working with legacy deep learning frameworks that have compatibility issues with modern systems.
---

# Caffe CIFAR-10 Training

## Overview

This skill provides procedural guidance for building the Caffe deep learning framework from source and training models on the CIFAR-10 dataset. Caffe is a legacy framework (circa 2014-2017) with known compatibility issues on modern systems, requiring careful handling of dependencies and configuration.

## Pre-Build Research Phase

Before attempting to build Caffe, research known compatibility issues for the target system:

1. **Identify system versions**: Check OpenCV version (`pkg-config --modversion opencv4`), Python version, compiler version, and CUDA version if applicable
2. **Research compatibility matrix**: Caffe 1.0 has documented incompatibilities with:
   - OpenCV 4.x (API changes from OpenCV 3.x)
   - Python 3.8+ (various issues)
   - Modern C++ compilers with stricter standards
3. **Locate required patches**: Search for Caffe patches specific to the system configuration (e.g., "Caffe OpenCV 4 patch", "Caffe Python 3.12 compatibility")
4. **Consider alternatives**: Evaluate whether using a Docker image, conda environment, or compatibility fork would be more reliable than patching the build

## Build Workflow

### Step 1: Clone Repository with Correct Version

```bash
git clone https://github.com/BVLC/caffe.git
cd caffe
git checkout v1.0  # Note: tag is "v1.0", not "v1.0.0"
```

**Verification**: Confirm the checkout with `git describe --tags`

### Step 2: Install Dependencies

Install all required dependencies before configuration:

- Protocol Buffers (protobuf, libprotobuf-dev)
- Boost libraries (libboost-all-dev)
- GLOG and GFLAGS
- HDF5 (libhdf5-dev)
- LMDB (liblmdb-dev)
- LevelDB (libleveldb-dev)
- Snappy (libsnappy-dev)
- OpenCV (with version compatibility consideration)
- BLAS library (OpenBLAS, MKL, or ATLAS)
- Python development headers if using Python bindings

**Verification**: For each library, verify installation with `pkg-config --exists <library>` or check header file presence

### Step 3: Configure Makefile.config

Copy and modify the configuration template:

```bash
cp Makefile.config.example Makefile.config
```

Key configuration decisions:

1. **CPU vs GPU mode**: Set `CPU_ONLY := 1` for CPU-only builds
2. **OpenCV version handling**:
   - If OpenCV 4.x is installed, patches are required (see Common Pitfalls)
   - Do NOT simply set `OPENCV_VERSION := 3` - this causes compilation failures
3. **Python configuration**: Set exactly ONE Python configuration block; remove or comment out the other
4. **BLAS library**: Ensure BLAS_LIB points to the correct library

**Verification**: Review the final Makefile.config for consistency - no duplicate definitions, no conflicting settings

### Step 4: Apply Compatibility Patches

For OpenCV 4.x compatibility, modify source files that use deprecated APIs:

- `cv::CV_LOAD_IMAGE_COLOR` → `cv::IMREAD_COLOR`
- `CV_CAP_PROP_*` → `cv::CAP_PROP_*`
- Header includes may need updating

**Verification**: Grep for deprecated symbols before building

### Step 5: Build with Conservative Settings

```bash
make clean  # If retrying after failure
make all -j2  # Start with low parallelism
```

**Critical**: Avoid `make -j$(nproc)` initially - this can exhaust memory and cause silent failures. Scale up parallelism only after confirming stable compilation.

**Verification**: Check that build completes without OOM kills (`dmesg | grep -i kill`)

### Step 6: Build Tests and Python Bindings

```bash
make test -j2
make pycaffe -j2
```

**Verification**: Run `make runtest` to verify build integrity

## CIFAR-10 Training Workflow

### Step 1: Download Dataset

```bash
cd data/cifar10
./get_cifar10.sh
```

**Verification**: Check that LMDB or LevelDB files are created in the expected location

### Step 2: Modify Training Configuration

For custom iteration counts, edit `examples/cifar10/cifar10_quick_solver.prototxt`:

- `max_iter`: Set to desired iteration count
- `snapshot`: Set snapshot frequency appropriately
- `test_interval`: Adjust based on max_iter

**Verification**: Validate prototxt syntax before training

### Step 3: Train Model

```bash
./examples/cifar10/train_quick.sh
```

**Verification**: Monitor output for loss convergence and accuracy metrics

### Step 4: Verify Output

Confirm model files are created at the expected paths with expected accuracy.

## Common Pitfalls

### OpenCV 4 Incompatibility

**Symptom**: Compilation errors referencing `CV_LOAD_IMAGE_COLOR`, `CV_LOAD_IMAGE_GRAYSCALE`, or similar

**Cause**: Caffe 1.0 was written for OpenCV 2.x/3.x APIs

**Solution**: Apply OpenCV 4 compatibility patches to source files, or build OpenCV 3.x from source

**Wrong approach**: Setting `OPENCV_VERSION := 3` without patching - this tells Caffe to expect OpenCV 3 APIs but doesn't make OpenCV 4 compatible

### Build Killed by OOM

**Symptom**: Build process terminates with "Killed" message, no error output

**Cause**: Parallel compilation exhausting system memory

**Solution**: Use `make -j2` or even `make -j1` for memory-constrained systems

**Verification**: Check `dmesg | tail -20` for OOM killer messages

### Inconsistent Makefile.config

**Symptom**: Conflicting or duplicate definitions cause unexpected build behavior

**Cause**: Incremental edits leaving multiple Python configurations or conflicting library paths

**Solution**: Plan all configuration changes before editing; review entire file for consistency after editing

### Premature Task Completion

**Symptom**: Marking steps complete before verification, leading to compounding errors

**Cause**: Assuming commands succeeded based on lack of immediate error

**Solution**: Verify each step explicitly before proceeding:
- After dependency install: verify with pkg-config or header checks
- After configuration: review entire Makefile.config
- After build: run tests before proceeding

### Missing Python Headers

**Symptom**: Build fails looking for Python.h or numpy headers

**Cause**: PYTHON_INCLUDE paths in Makefile.config don't match system paths

**Solution**: Use `python3 -c "import sysconfig; print(sysconfig.get_paths()['include'])"` and `python3 -c "import numpy; print(numpy.get_include())"` to get correct paths

## Verification Checklist

Before marking any major step complete, verify:

- [ ] Dependencies: All libraries found by pkg-config or headers present
- [ ] Configuration: Makefile.config has no duplicate or conflicting entries
- [ ] Build: Completed without OOM or silent failures
- [ ] Tests: `make runtest` passes
- [ ] Dataset: Data files exist at expected paths
- [ ] Training: Model file created with expected metrics
