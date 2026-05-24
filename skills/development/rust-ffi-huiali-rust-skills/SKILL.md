---
name: rust-ffi
description: "FFI 跨语言互操作专家。处理 C/C++ 互操作、bindgen、PyO3、Java JNI、内存布局、数据转换等问题。触发词：FFI, C, C++, bindgen, cbindgen, PyO3, jni, extern, libc, CString, CStr, 跨语言, 互操作, 绑定"
globs: ["**/*.rs"]
---

# FFI 跨语言互操作

## 核心问题

**如何安全地在 Rust 和其他语言之间传递数据？**

FFI 是危险的。任何错误都可能导致未定义行为。

---

## 绑定生成

### C/C++ → Rust (bindgen)

```bash
# 自动生成 bindings
bindgen input.h \
    --output src/bindings.rs \
    --whitelist-type 'my_*' \
    --whitelist-function 'my_*'
```

### Rust → C (cbindgen)

```bash
# 生成 C 头文件
cbindgen --crate mylib --output include/mylib.h
```

---

## 数据类型映射

| Rust | C | 注意事项 |
|-----|---|---------|
| `i32` | `int` | 通常匹配 |
| `i64` | `long long` | 跨平台注意 |
| `usize` | `uintptr_t` | 指针大小 |
| `*const T` | `const T*` | 只读 |
| `*mut T` | `T*` | 可写 |
| `&CStr` | `const char*` | UTF-8 保证 |
| `CString` | `char*` | 所有权转移 |
| `NonNull<T>` | `T*` | 非空指针 |

---

## 常见模式

### 调用 C 函数

```rust
use std::ffi::{CStr, CString};
use libc::c_int;

#[link(name = "curl")]
extern "C" {
    fn curl_version() -> *const libc::c_char;
    fn curl_easy_perform(curl: *mut c_int) -> c_int;
}

fn get_version() -> String {
    unsafe {
        let ptr = curl_version();
        CStr::from_ptr(ptr).to_string_lossy().into_owned()
    }
}
```

### 传递字符串

```rust
// ✅ 安全方式
fn process_c_string(s: &CStr) {
    unsafe {
        some_c_function(s.as_ptr());
    }
}

// 需要 String 时
fn get_c_string() -> CString {
    CString::new("hello").unwrap()
}
```

### 回调函数

```rust
extern "C" fn callback(data: *mut libc::c_void) {
    unsafe {
        let user_data: &mut UserData = &mut *(data as *mut UserData);
        user_data.count += 1;
    }
}

fn register_callback(callback: extern "C" fn(*mut c_void), data: *mut c_void) {
    unsafe {
        some_c_lib_register(callback, data);
    }
}
```

---

## 错误处理

### C 错误码

```rust
fn call_c_api() -> Result<(), Box<dyn std::error::Error>> {
    let result = unsafe { c_function_that_returns_int() };
    if result < 0 {
        return Err(format!("C API error: {}", result).into());
    }
    Ok(())
}
```

### panic 跨越 FFI

```rust
// FFI 边界上的 panic 应该被捕获或禁止
#[no_mangle]
pub extern "C" fn safe_call() {
    std::panic::catch_unwind(|| {
        rust_code_that_might_panic()
    }).ok();  // 忽略 panic
}
```

---

## 内存管理

| 场景 | 谁释放 | 怎么做 |
|-----|-------|-------|
| C 分配，Rust 使用 | C | 不要 free |
| Rust 分配，C 使用 | Rust | 传指针，C 用完通知 Rust |
| 共享缓冲区 | 协商 | 文档说明 |

---

## 常见陷阱

| 陷阱 | 后果 | 避免 |
|-----|------|-----|
| 字符串编码错误 | 乱码 | 用 CStr/CString |
| 生命周期不匹配 | use-after-free | 明确所有权 |
| 跨线程传递非 Send | 数据竞争 | Arc + 锁 |
| 胖指针传 C | 内存损坏 | 扁平化数据 |
| 忘记 `#[no_mangle]` | 符号找不到 | 明确导出 |

---

## 语言绑定工具

| 语言 | 工具 | 场景 |
|-----|------|-----|
| Python | PyO3 | Python 扩展 |
| Java | jni | Android/JVM |
| Node.js | napi-rs | Node.js 扩展 |
| C# | cppwinrt | Windows |
| Go | cgo | Go 桥接 |

---

## 安全准则

1. **最小化 unsafe**：只包装必要的 C 调用
2. **防御性编程**：检查空指针、范围
3. **文档明确**：谁负责释放内存
4. **测试覆盖**：FFI 错误极难调试
5. **用 Miri 检查**：发现未定义行为

---

## C++ 异常处理

### cxx 库

```rust
// 使用 cxx 实现安全的 C++ FFI
use cxx::CxxString;
use cxx::CxxVector;

#[cxx::bridge]
mod ffi {
    unsafe extern "C++" {
        include!("my_library.h");
        
        type MyClass;
        
        fn do_something(&self, input: i32) -> i32;
        fn get_data(&self) -> &CxxString;
        fn process_vector(&self, vec: &CxxVector<i32>) -> i32;
    }
    
    #[namespace = "mylib"]
    unsafe extern "C++" {
        fn free_resource(ptr: *mut c_void);
    }
}

struct RustWrapper {
    ptr: *mut c_void,
}

impl RustWrapper {
    pub fn new() -> Self {
        unsafe {
            Self {
                ptr: mylib::create_object(),
            }
        }
    }
    
    pub fn do_something(&self, input: i32) -> i32 {
        unsafe {
            (*self.ptr).do_something(input)
        }
    }
}

impl Drop for RustWrapper {
    fn drop(&mut self) {
        unsafe {
            mylib::free_resource(self.ptr);
        }
    }
}
```

### C++ 异常 → Rust Result

```rust
// C++ 抛出的异常会转换为 Rust panic
// 需要用 catch_unwind 捕获

#[no_mangle]
pub extern "C" fn safe_cpp_call() -> i32 {
    let result = std::panic::catch_unwind(|| {
        unsafe {
            cpp_function_that_might_throw()
        }
    });
    
    match result {
        Ok(value) => value,
        Err(_) => {
            // C++ 异常被捕获，返回错误码
            -1
        }
    }
}

// 更好的方式：自定义错误转换
#[no_mangle]
pub extern "C" fn checked_cpp_call(error_code: *mut i32) -> *const c_char {
    let result = std::panic::catch_unwind(|| {
        unsafe {
            cpp_function()
        }
    });
    
    match result {
        Ok(Ok(value)) => {
            // 成功
            value.as_ptr()
        }
        Ok(Err(e)) => {
            // C++ 错误
            if !error_code.is_null() {
                unsafe { *error_code = e.code(); }
            }
            std::ptr::null()
        }
        Err(_) => {
            // C++ 异常
            if !error_code.is_null() {
                unsafe { *error_code = -999; }
            }
            std::ptr::null()
        }
    }
}
```

### 栈展开问题

```rust
// C++ 栈展开与 Rust 的交互很复杂

// 1. 禁止 panic 跨越 FFI 边界
#[no_mangle]
pub extern "C" fn rust_function() {
    // Rust 代码可能 panic
    // 但这会导致 C++ 栈展开时调用 Rust 的 drop，
    // 可能导致 UB
    
    // 解决方案：catch_unwind
    let _ = std::panic::catch_unwind(|| {
        risky_rust_code()
    });
}

// 2. C++ 析构函数与 Rust Drop
// C++ 析构函数在栈展开时会调用
// Rust Drop 在 panic 时也会调用
// 两者同时存在可能导致问题

// 解决方案：使用 ManuallyDrop
struct Wrapper {
    inner: ManuallyDrop<InnerType>,
}

impl Drop for Wrapper {
    fn drop(&mut self) {
        // 防止两次清理
        // 但 C++ 析构函数可能仍然会调用
    }
}
```

### C++ 智能指针桥接

```rust
// 使用 cxx 桥接 std::unique_ptr
#[cxx::bridge]
mod ffi {
    unsafe extern "C++" {
        include!("memory");
        
        type UniquePtr<T>;
        
        // 所有权转移：Rust → C++
        fn take_unique_ptr(ptr: Box<UniquePtr<T>>) -> *mut T;
        
        // 所有权转移：C++ → Rust
        fn create_unique_ptr() -> Box<UniquePtr<T>>;
        fn release_unique_ptr(ptr: Box<UniquePtr<T>>) -> *mut T;
    }
}

// 手动桥接 std::shared_ptr
struct SharedPtr<T> {
    ptr: *mut T,
    ref_count: usize,
}

impl<T> SharedPtr<T> {
    pub fn new(ptr: *mut T) -> Self {
        Self {
            ptr,
            ref_count: 1,
        }
    }
    
    pub fn clone(&mut self) {
        self.ref_count += 1;
    }
    
    pub fn drop(&mut self) {
        self.ref_count -= 1;
        if self.ref_count == 0 {
            unsafe {
                // 调用 C++ delete
                cpp_delete(self.ptr);
            }
        }
    }
}

unsafe impl<T> Send for SharedPtr<T> {}
unsafe impl<T> Sync for SharedPtr<T> {}
```

---

## 常见问题

| 问题 | 原因 | 解决 |
|-----|------|-----|
| C++ 异常导致 panic | 未捕获异常 | catch_unwind |
| 内存双重释放 | 所有权不清 | 明确协议 |
| 胖指针损坏 | 布局不匹配 | \#[repr(C)] |
| 符号未导出 | \#[no_mangle] 缺失 | 添加属性 |
| 线程安全问题 | 非 Send/Sync | Arc + 锁 |

