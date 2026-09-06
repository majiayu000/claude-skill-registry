---
name: rust-ffi
description: 'Use when calling C libraries from Rust, generating bindings with bindgen, exporting Rust functions to C with cbindgen, writing safe wrappers over unsafe FFI, or linking system libraries.'
---

# Rust FFI

Rust calls C through `unsafe extern` blocks and exports to C through `extern "C"` functions. The unsafe surface stays at the boundary; everything behind it is a safe API.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Calling a C library from Rust, generating bindings with bindgen, exporting a Rust API to C with cbindgen, wrapping an unsafe FFI boundary in a safe API, or linking a system or vendored C library. |
| Authority | Reversible local. Writes only the target crate's Cargo.toml, build.rs, wrapper header, source files, and the generated C header inside the project. Rollback is version control. No remote mutation. |
| Side effect | Creates or edits crate build and source files; bindgen output lands in `OUT_DIR`, cbindgen output at the named header path. |
| Done | `cargo build` succeeds, the FFI boundary is declared or generated, and every unsafe call sits behind a safe wrapper or an exported `extern "C"` function. |

## Inputs

1. **C library** (required): headers, library name, and whether it is system-installed, vendored, or built from source.
2. **Direction** (required): C-to-Rust, Rust-to-C, or both.
3. **Crate layout** (optional): single crate or a `-sys` crate plus a safe wrapper crate; inferred from the workspace when omitted.
4. **Edition** (optional): edition 2024 is assumed, so extern blocks are `unsafe extern` and `no_mangle` is written `#[unsafe(no_mangle)]`.

## Procedure

1. **Pick the binding strategy.** Declare functions by hand for a handful of calls; use bindgen when the header surface is real. Done when: the strategy is named.

```rust
use std::ffi::{c_char, c_int, c_void, CString};

unsafe extern "C" {
    fn my_lib_init(config: *const c_char) -> c_int;
    fn my_lib_process(handle: *mut c_void, data: *const u8, len: usize) -> c_int;
    fn my_lib_cleanup(handle: *mut c_void);
}
```

2. **Generate bindings with bindgen when the header surface is large.** Restrict output with allowlists so system headers do not leak into the generated file. Done when: `build.rs` writes `bindings.rs` into `OUT_DIR` and `lib.rs` includes it.

```toml
[build-dependencies]
bindgen = "0.70"
```

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=wrapper.h");
    println!("cargo:rustc-link-lib=mylib");
    println!("cargo:rustc-link-search=/usr/local/lib");

    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .clang_arg("-I/usr/local/include")
        .allowlist_function("mylib_.*")
        .allowlist_type("MyLib.*")
        .allowlist_var("MYLIB_.*")
        .derive_debug(true)
        .derive_default(true)
        .blocklist_type("__va_list_tag")
        .generate()
        .expect("bindgen failed");

    let out = std::path::PathBuf::from(std::env::var("OUT_DIR").unwrap());
    bindings.write_to_file(out.join("bindings.rs")).unwrap();
}
```

```rust
// src/lib.rs
#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
```

3. **Structure the sys crate.** A `-sys` crate owns the link and the raw bindings; the safe crate depends on it. The `links` manifest key tells Cargo which native library the crate links. Done when: the layout matches the pattern.

```text
mylib-sys/
  Cargo.toml      # links = "mylib"
  build.rs        # probes pkg-config, falls back to a vendored cc build
  wrapper.h
  src/lib.rs      # includes the generated bindings
mylib/
  Cargo.toml      # depends on mylib-sys
  src/lib.rs      # safe API
```

```rust
// mylib-sys/build.rs
fn main() {
    if let Ok(lib) = pkg_config::probe_library("mylib") {
        for path in lib.include_paths {
            println!("cargo:include={}", path.display());
        }
        return;
    }
    cc::Build::new()
        .file("vendor/mylib/src/mylib.c")
        .include("vendor/mylib/include")
        .compile("mylib");
    println!("cargo:rerun-if-changed=vendor/mylib/src/mylib.c");
}
```

4. **Wrap every unsafe call in a safe API.** Check for null handles, map C error codes to `Result`, free resources in `Drop`, and add `Send` or `Sync` only after verifying the C library's threading contract. Done when: no safe public function reaches `unsafe` without a validity check.

```rust
pub struct MyLib {
    handle: *mut ffi::mylib_t,
}

impl MyLib {
    pub fn new(config: &str) -> Result<Self, Error> {
        let c = CString::new(config).map_err(|_| Error::InvalidConfig)?;
        let handle = unsafe { ffi::mylib_create(c.as_ptr()) };
        if handle.is_null() {
            return Err(Error::InitFailed);
        }
        Ok(Self { handle })
    }
}

impl Drop for MyLib {
    fn drop(&mut self) {
        unsafe { ffi::mylib_destroy(self.handle) };
    }
}
```

5. **Export Rust to C with cbindgen.** Exported functions are `extern "C"` with `#[unsafe(no_mangle)]`; ownership crosses the boundary through `Box::into_raw` and `Box::from_raw`. Done when: the generated header exists at the configured path.

```rust
#[unsafe(no_mangle)]
pub extern "C" fn mylib_destroy(ptr: *mut MyLib) {
    if !ptr.is_null() {
        unsafe { drop(Box::from_raw(ptr)) };
    }
}
```

```rust
// build.rs
fn main() {
    let crate_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
    cbindgen::Builder::new()
        .with_crate(crate_dir)
        .with_language(cbindgen::Language::C)
        .generate()
        .expect("cbindgen failed")
        .write_to_file("include/mylib.h");
}
```

6. **Link the library.** Emit link directives from build.rs: `cargo:rustc-link-lib=static=name`, `dylib=name`, or `framework=name` on macOS, plus `cargo:rustc-link-search=` for nonstandard paths. Done when: `cargo build` links without unresolved `-l` errors.

7. **Verify the boundary.** Build the crate, confirm the generated bindings or header exist, and exercise one call across the boundary. Done when: the call returns the expected result.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| bindgen cannot parse the header | Reduce `wrapper.h` to the needed includes and pass include paths and defines through `clang_arg`. |
| Library not found at link time | Add `cargo:rustc-link-search`, probe with pkg-config, or build the vendored source with `cc`. |
| C constructor returns null | Map it to `Result` or `Option`; never store a null handle. |
| Thread-safety unknown | Do not add `Send` or `Sync`; the default is neither until the C library's locking contract is verified. |
| Panic would cross the boundary | Return an error code or use `catch_unwind`; unwinding out of an `extern "C"` function aborts. Use `extern "C-unwind"` only when the C side is built to propagate. |
| Partial result | Files already written remain; the report names the failed step and its command output. Rollback is version control. |

## Output

1. A crate that builds with a verified call across the FFI boundary.
2. A report listing files written, the safe API surface, and the link directives emitted.
3. bindgen builder options, cbindgen.toml keys, `cc`, pkg-config, and safety patterns are in `references/bindgen-cbindgen.md`.
