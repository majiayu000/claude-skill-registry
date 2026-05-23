---
name: rust-embedded
description: "嵌入式与 no_std 专家。处理 no_std, embedded-hal, 裸机开发, 中断, DMA, 资源受限环境等问题。触发词：no_std, embedded, embedded-hal, microcontroller, firmware, ISR, DMA, 嵌入式, 裸机"
globs: ["**/*.rs", "**/Cargo.toml"]
---

# 嵌入式与 no_std 开发

## 核心问题

**如何在资源受限环境或没有标准库的情况下编程？**

no_std 不是 Rust 的子集，而是一种不同的编程模式。

---

## no_std 基础

```rust
#![no_std]
// 不能使用 std, alloc, test

use core::panic::PanicMessage;

// 必须实现 panic handler
#[panic_handler]
fn panic(info: &PanicMessage) -> ! {
    loop {}
}

// 可选：定义全局分配器
#[global_allocator]
static ALLOC: some_allocator::Allocator = some_allocator::Allocator;
```

### 可用模块

| 模块 | 用途 |
|-----|------|
| `core` | 基本语言特性 |
| `alloc` | 堆分配（需 allocator） |
| `compiler_builtins` | 编译器内置函数 |

---

## 嵌入式-hal

```rust
use embedded_hal as hal;
use hal::digital::v2::OutputPin;

// 抽象硬件访问
fn blink_led<L: OutputPin>(mut led: L) -> ! {
    loop {
        led.set_high().unwrap();
        delay_ms(1000);
        led.set_low().unwrap();
        delay_ms(1000);
    }
}
```

### 常用 trait

| trait | 操作 |
|-------|------|
| `OutputPin` | 设置高低电平 |
| `InputPin` | 读取引脚 |
| `SpiBus` | SPI 通信 |
| `I2c` | I2C 通信 |
| `Serial` | 串口 |

---

## 中断处理

```rust
#![no_std]
#![feature(abi_vectorcall)]

use cortex_m::interrupt::{free, Mutex};
use cortex_m::peripheral::NVIC;

// 共享状态
static MY_DEVICE: Mutex<Cell<Option<MyDevice>>> = Mutex::new(None);

#[interrupt]
fn TIM2() {
    free(|cs| {
        let device = MY_DEVICE.borrow(cs).take();
        if let Some(dev) = device {
            // 处理中断
            dev.handle();
            MY_DEVICE.borrow(cs).set(Some(dev));
        }
    });
}

// 启用中断
fn enable_interrupt(nvic: &mut NVIC, irq: interrupt::TIM2) {
    nvic.enable(irq);
}
```

---

## 内存管理

### 栈大小

```toml
[profile.dev]
panic = "abort"  # 减少二进制大小

[profile.release]
lto = true
opt-level = "z"  # 最小化大小
```

### 避免动态分配

```rust
// 用栈数组代替 Vec
let buffer: [u8; 256] = [0; 256];

// 或使用定长环形缓冲区
struct RingBuffer {
    data: [u8; 256],
    write_idx: usize,
    read_idx: usize,
}
```

---

## 外设访问模式

```rust
// 寄存器映射
const GPIOA_BASE: *const u32 = 0x4002_0000 as *const u32;
const GPIOA_ODR: *const u32 = (GPIOA_BASE + 0x14) as *const u32;

// 安全抽象
mod gpioa {
    use super::*;
    
    pub fn set_high() {
        unsafe {
            GPIOA_ODR.write_volatile(1 << 5);
        }
    }
}
```

---

## 常见问题

| 问题 | 原因 | 解决 |
|-----|------|-----|
| panic 死循环 | 没有 panic handler | 实现 #[panic_handler] |
| 栈溢出 | 中断嵌套或大局部变量 | 增加栈、减小局部变量 |
| 内存损坏 | 裸指针操作 | 用 safe abstraction |
| 程序不运行 | 链接脚本问题 | 检查 startup code |
| 外设不响应 | 时钟未使能 | 先配置 RCC |

---

## 资源受限技巧

| 技巧 | 效果 |
|-----|------|
| `opt-level = "z"` | 最小化大小 |
| `lto = true` | 链接时优化 |
| `panic = "abort"` | 去掉 unwinding |
| `codegen-units = 1` | 更好的优化 |
| 避免 alloc | 用栈或静态数组 |

---

## 项目配置示例

```toml
[package]
name = "my-firmware"
version = "0.1.0"
edition = "2024"

[dependencies]
cortex-m = "0.7"
cortex-m-rt = "0.7"
embedded-hal = "1.0"
nb = "1.0"

[profile.dev]
panic = "abort"

[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
```

---

## WebAssembly 多线程

### SharedArrayBuffer

```rust
// 需要在服务器端配置 Cross-Origin-Opener-Policy
// 浏览器才能使用 SharedArrayBuffer

// wasm-bindgen 配置
[dependencies]
wasm-bindgen = { version = "0.2", features = ["enable-threads"] }

// 使用 atomic 内存序
use std::sync::atomic::{AtomicUsize, Ordering};

static COUNTER: AtomicUsize = AtomicUsize::new(0);

#[wasm_bindgen]
pub fn increment_counter() -> usize {
    COUNTER.fetch_add(1, Ordering::SeqCst)
}

#[wasm_bindgen]
pub fn get_counter() -> usize {
    COUNTER.load(Ordering::SeqCst)
}
```

### Atomics 与内存序

```rust
use std::sync::atomic::{AtomicI32, Ordering};

// 不同内存序的性能和可见性权衡
#[wasm_bindgen]
pub fn atomic_demo() {
    let atom = AtomicI32::new(0);
    
    // 最强保证，最慢
    atom.store(1, Ordering::SeqCst);
    
    // 释放语义（生产者）
    atom.store(2, Ordering::Release);
    
    // 获取语义（消费者）
    let val = atom.load(Ordering::Acquire);
    
    // 松散语义，最快，但可能 reordered
    atom.store(3, Ordering::Relaxed);
    let val = atom.load(Ordering::Relaxed);
}
```

### 线程局部存储 (TLS)

```rust
// WASM 线程局部存储
use std::cell::RefCell;

thread_local! {
    static THREAD_ID: RefCell<u32> = RefCell::new(0);
}

#[wasm_bindgen]
pub fn set_thread_id(id: u32) {
    THREAD_ID.with(|tid| {
        *tid.borrow_mut() = id;
    });
}

#[wasm_bindgen]
pub fn get_thread_id() -> u32 {
    THREAD_ID.with(|tid| *tid.borrow())
}
```

---

## RISC-V 嵌入式开发

### 基础设置

```rust
// Cargo.toml
[package]
name = "riscv-firmware"
version = "0.1.0"
edition = "2024"

[dependencies]
riscv = "0.10"
embedded-hal = "1.0"

[profile.release]
opt-level = "z"
lto = true
```

### 中断与异常

```rust
// RISC-V 中断处理
#![no_std]

use riscv::register::{
    mie::MIE,
    mstatus::MSTATUS,
    mip::MIP,
};

/// 启用机器中断
pub fn enable_interrupt() {
    // 启用外部中断、计时器中断、软件中断
    unsafe {
        MIE::set_mext();
        MIE::set_mtimer();
        MIE::set_msip();
        
        // 全局中断使能
        MSTATUS::set_mie();
    }
}

/// 禁用所有中断
pub fn disable_interrupt() {
    unsafe {
        MSTATUS::clear_mie();
    }
}
```

### 内存屏障

```rust
// RISC-V 内存屏障
use riscv::asm;

/// 数据内存屏障 - 确保所有内存访问完成
fn data_memory_barrier() {
    unsafe {
        asm!("fence iorw, iorw");
    }
}

/// 指令屏障 - 确保指令流更新可见
fn instruction_barrier() {
    unsafe {
        asm!("fence i, i");
    }
}
```

### 原子操作

```rust
// 使用 riscv::atomic 模块
use riscv::asm::atomic;

fn atomic_add(dst: &mut usize, val: usize) {
    unsafe {
        // 使用 amoadd.w 指令
        atomic::amoadd(dst as *mut usize, val);
    }
}

fn compare_and_swap(ptr: &mut usize, old: usize, new: usize) -> bool {
    unsafe {
        // 使用 amoswap.w 指令
        let current = atomic::amoswap(ptr as *mut usize, new);
        current == old
    }
}
```

### 多核同步

```rust
// RISC-V 机器间中断 (IPI)
const M_SOFT_INT: *mut u32 = 0x3FF0_FFF0 as *mut u32;

fn send_soft_interrupt(core_id: u32) {
    unsafe {
        // 设置软件中断位
        M_SOFT_INT.write_volatile(1 << core_id);
    }
}

fn clear_soft_interrupt(core_id: u32) {
    unsafe {
        M_SOFT_INT.write_volatile(0);
    }
}
```

### RISC-V 特权级

```rust
// RISC-V 特权级检查
use riscv::register::{mstatus, misa};

fn check_privilege_level() -> u8 {
    // 读取当前特权级
    // 0 = User, 1 = Supervisor, 2 = Hypervisor, 3 = Machine
    (mstatus::read().bits() >> 11) & 0b11
}

fn is_machine_mode() -> bool {
    check_privilege_level() == 3
}

/// 获取可用的 ISA 扩展
fn get_isa_extensions() -> String {
    let misa = misa::read();
    format!("{:?}", misa)
}
```

---

## RISC-V 性能优化

| 优化点 | 方法 |
|-------|------|
| 内存访问 | 使用非对齐访问指令（如果支持） |
| 原子操作 | 使用 A 扩展指令 |
| 乘除法 | 使用 M 扩展指令 |
| 向量操作 | 使用 V 扩展（RV64V） |
| 压缩指令 | 使用 C 扩展减少代码大小 |

---