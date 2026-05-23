---
name: rust-gpu
description: "GPU 内存与计算专家。处理 CUDA, OpenCL, GPU memory, compute shader, memory coalescing, zero-copy, 显存管理, 异构计算"
globs: ["**/*.rs"]
---

# GPU 内存与计算

## 核心问题

**如何在 Rust 中高效管理 GPU 内存和异构计算？**

GPU 计算需要特殊的内存管理策略和同步机制。

---

## GPU 内存架构

```
┌─────────────────────────────────────────┐
│              GPU 显存                    │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐       │
│  │   Global    │  │   Shared    │       │
│  │   Memory    │  │   Memory    │       │
│  │  (VRAM)     │  │  (SMEM)     │       │
│  └─────────────┘  └─────────────┘       │
│                                         │
│  ┌─────────────┐  ┌─────────────┐       │
│  │  Constant   │  │   Local     │       │
│  │   Memory    │  │   Memory    │       │
│  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────┘
        ↓                    ↑
   CPU (通过 PCIe)      GPU 计算单元
```

---

## 内存类型对比

| 内存类型 | 位置 | 延迟 | 大小 | 用途 |
|---------|------|------|------|------|
| Global | VRAM | 高 | 大 | 输入/输出数据 |
| Shared | SMEM | 低 | 小 | 线程块内通信 |
| Constant | 缓存 | 中 | 中 | 只读数据 |
| Local | 寄存器/VRAM | 高 | 小 | 线程私有 |
| Register | SM | 最低 | 极小 | 线程私有 |

---

## CUDA 内存管理 (rust-cuda)

```rust
// 使用 rust-cuda 或 cuda-sys
use cuda_sys::ffi::*;

// 设备内存分配
let mut d_ptr: *mut f32 = std::ptr::null_mut();
unsafe {
    cudaMalloc(&mut d_ptr as *mut *mut f32, size * std::mem::size_of::<f32>())
};

// 主机到设备拷贝
unsafe {
    cudaMemcpy(
        d_ptr as *mut c_void,
        h_ptr as *const c_void,
        size * std::mem::size_of::<f32>(),
        cudaMemcpyHostToDevice
    );
};

// 设备到主机拷贝
let mut h_result: Vec<f32> = vec![0.0; size];
unsafe {
    cudaMemcpy(
        h_result.as_mut_ptr() as *mut c_void,
        d_ptr as *const c_void,
        size * std::mem::size_of::<f32>(),
        cudaMemcpyDeviceToHost
    );
};

// 释放设备内存
unsafe {
    cudaFree(d_ptr as *mut c_void);
};
```

---

## 零拷贝内存

```rust
// 零拷贝：共享主机和设备内存
let mut h_ptr: *mut f32 = std::ptr::null_mut();

// 使用 cudaMallocHost 分配固定内存（页锁定）
unsafe {
    cudaMallocHost(&mut h_ptr as *mut *mut f32, size * std::mem::size_of::<f32>())
};

// 固定内存可以直接被 GPU 访问，无需拷贝
// 但会影响系统内存压力

// 使用 cudaMemcpyAsync 进行异步拷贝（与计算重叠）
let stream: cudaStream_t = std::ptr::null_mut();
unsafe {
    cudaMemcpyAsync(
        d_ptr as *mut c_void,
        h_ptr as *const c_void,
        size * std::mem::size_of::<f32>(),
        cudaMemcpyHostToDevice,
        stream
    );
};

// 同步等待
unsafe {
    cudaStreamSynchronize(stream);
};
```

---

## 统一内存 (Unified Memory)

```rust
// 使用统一内存，CPU 和 GPU 自动管理数据迁移
let mut unified_ptr: *mut f32 = std::ptr::null_mut();

unsafe {
    // 分配统一内存
    cudaMallocManaged(&mut unified_ptr as *mut *mut f32, size * std::mem::size_of::<f32>());
};

// CPU 访问
unsafe {
    for i in 0..size {
        *unified_ptr.add(i) = i as f32;
    }
};

// GPU 访问（自动迁移到设备）
// 调用 CUDA kernel
launch_kernel(unified_ptr, size);

// CPU 访问结果（自动迁移回主机）
unsafe {
    println!("Result: {}", unified_ptr.add(0).read());
};

// 释放
unsafe {
    cudaFree(unified_ptr as *mut c_void);
};
```

---

## 内存合并访问

```rust
// 合并访问模式 - 优化全局内存带宽
// ❌ 错误：非合并访问
__global__ void bad_access(float* data) {
    int idx = threadIdx.x + blockIdx.x * 32; // 跨步访问
    float value = data[idx * 32];  // 每个线程访问间隔 32 * sizeof(float)
}

// ✅ 正确：合并访问
__global__ void coalesced_access(float* data) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x; // 连续访问
    float value = data[idx];  // 所有线程连续访问
}
```

---

## 共享内存使用

```rust
// 使用共享内存减少全局内存访问
__global__ void shared_memory_reduce(float* input, float* output) {
    __shared__ float sdata[256];  // 每个块 256 字节共享内存
    
    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    // 从全局内存加载到共享内存
    sdata[tid] = input[idx];
    __syncthreads();
    
    // 规约计算
    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            sdata[tid] += sdata[tid + s];
        }
        __syncthreads();
    }
    
    // 写回结果
    if (tid == 0) {
        output[blockIdx.x] = sdata[0];
    }
}
```

---

## 内存对齐

```rust
// 内存对齐优化
const size_t ALIGNMENT = 256;  // 256 字节对齐

// 使用 cudaMalloc 返回的指针已经对齐
// 但自定义数据结构需要对齐
struct alignas(256) AlignedData {
    float4 position;  // 16 字节
    float4 normal;    // 16 字节
    // ... 自动填充到 256 字节
};

// 检查对齐
assert(((uintptr_t)ptr % ALIGNMENT) == 0);
```

---

## 性能优化检查表

| 优化项 | 检查点 |
|-------|-------|
| 内存合并 | 线程访问连续内存 |
| 共享内存 | 减少全局内存访问 |
| 内存对齐 | 256 字节对齐 |
| 异步操作 | 计算与传输重叠 |
| 固定内存 | 使用页锁定内存 |
| 批处理 | 减少内核启动开销 |

---

## 与其他技能关联

```
rust-gpu
    │
    ├─► rust-performance → 性能优化
    ├─► rust-unsafe → 底层内存操作
    └─► rust-embedded → no_std 设备
```

