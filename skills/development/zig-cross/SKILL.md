---
name: zig-cross
description: 'Use when building Zig or C for another platform with Zig: target triples, -mcpu features, zig cc cross-compiles, multi-target build.zig, bare-metal Cortex-M, or WebAssembly. Not GCC: use cross-gcc.'
---

# Zig cross-compilation

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user wants a binary for a different OS or CPU from Zig or C sources, asks which Zig triple names a board or platform, needs a CPU feature set, or targets bare metal or WebAssembly. |
| Authority | Read-only. The skill emits commands, `build.zig` loops, and triple choices to chat; the user runs them. Rollback is not needed. No remote mutation. |
| Side effect | Chat output; scratch cross builds write into a scratch directory. |
| Done | The triple, CPU, and command for the target are reported, the triple appears in `zig targets` on the installed Zig, and a scratch build for that triple produces a file whose format `file` reports as the target's. |

## Inputs

- Zig version from `zig version`: required. Commands ran on Zig 0.14.1.
- Target platform: required. OS or bare metal, architecture, ABI, and the exact CPU when known.
- Sources: required. Zig, C, or both.
- Linker script for bare-metal targets: required when the target is freestanding.
- macOS SDK path when targeting macOS: required for anything beyond a plain executable that needs system frameworks.

## Procedure

1. Compose the triple `<arch>-<os>-<abi>` from the lists `zig targets` prints (a ZON document; sections `.arch`, `.os`, `.abi`, and `.libc` for the triples with a bundled libc). Common choices: `x86_64-linux-gnu`, `x86_64-linux-musl` (static), `aarch64-linux-gnu`, `aarch64-linux-musl`, `arm-linux-gnueabihf` (32-bit ARM with FPU), `x86_64-windows-gnu`, `aarch64-macos-none`, `x86_64-macos-none`, `wasm32-freestanding`, `wasm32-wasi`, `thumb-freestanding-eabihf` (Cortex-M with FPU; the CPU selects the M variant), `riscv32-freestanding-none`. Done when: the triple appears in `zig targets`.
2. Build Zig for the target: `zig build-exe src/main.zig -target aarch64-linux-gnu -O ReleaseFast`, or through the build system with `zig build -Dtarget=aarch64-linux-gnu -Doptimize=ReleaseFast`. Windows from Linux or macOS: `-target x86_64-windows-gnu` produces a `.exe`. macOS from Linux: `-target aarch64-macos-none` links a plain executable; code that needs Apple frameworks needs the macOS SDK. Done when: `file` reports the target's executable format.
3. Select the CPU with `-mcpu`. `-mcpu native` detects the build host and is wrong for a cross build; `-mcpu baseline` is the portable floor for the architecture; add or remove features with `+` and `-`, for example `-mcpu x86_64+avx2+bmi2`, `-mcpu x86_64_v3`, `-mcpu cortex_a72` (Raspberry Pi 4), `-mcpu cortex_m4+vfp4`, `-mcpu neoverse_n1`, `-mcpu apple_m1`. CPU and feature names are listed per architecture under `.cpus` in `zig targets`. Done when: the CPU name is present in that list.
4. Cross-compile C with `zig cc`, which needs no system cross toolchain: `zig cc -target aarch64-linux-gnu -O2 -o myapp-arm64 main.c`, `zig cc -target x86_64-windows-gnu main.c -o myapp.exe`, `zig cc -target x86_64-linux-musl -static main.c -o myapp-static`. In a Makefile, define one `CC` per platform, such as `CC_LINUX_ARM64 = zig cc -target aarch64-linux-gnu`. Done when: the C artifact matches the target format.
5. Build every target from one `build.zig`: loop over `std.Target.Query` values, resolve each with `b.resolveTargetQuery(t)`, and give each executable a distinct name:

   ```zig
   const targets = [_]std.Target.Query{
       .{ .cpu_arch = .x86_64, .os_tag = .linux, .abi = .gnu },
       .{ .cpu_arch = .aarch64, .os_tag = .linux, .abi = .gnu },
       .{ .cpu_arch = .x86_64, .os_tag = .windows, .abi = .gnu },
       .{ .cpu_arch = .aarch64, .os_tag = .macos },
   };
   for (targets) |t| {
       const exe = b.addExecutable(.{
           .name = b.fmt("myapp-{s}-{s}", .{ @tagName(t.cpu_arch.?), @tagName(t.os_tag.?) }),
           .root_module = b.createModule(.{
               .root_source_file = b.path("src/main.zig"),
               .target = b.resolveTargetQuery(t),
               .optimize = .ReleaseFast,
           }),
       });
       b.installArtifact(exe);
   }
   ```

   Done when: `zig-out/bin` holds one artifact per target.
6. Target bare metal: `zig build-exe src/main.zig -target thumb-freestanding-eabihf -mcpu cortex_m4+vfp4 -O ReleaseSmall -T linker.ld`. The root file supplies `pub fn panic(msg: []const u8, _: ?*std.builtin.StackTrace, _: ?usize) noreturn` and an exported entry point named in the linker script, such as `export fn _start() void`. Freestanding code cannot use std facilities that need an OS (threads, files, `std.debug.print`); the compiler reports `Unsupported operating system freestanding` when it does. Done when: the ELF links with the script's entry symbol.
7. Target WebAssembly. Browser: `zig build-exe src/main.zig -target wasm32-freestanding -O ReleaseSmall --export=init --export=update -fno-entry`, where each exported function is `export fn`. WASI: `zig build-exe src/main.zig -target wasm32-wasi -O ReleaseSafe` produces `main.wasm` for a WASI runtime. Done when: `file` reports a WebAssembly module.
8. Confirm with a scratch build and `file` on the output. Done when: the reported format is the target's.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| `available architectures:` listing after `-target` | The arch name is not one Zig uses; `thumbv7em` is not an arch, `thumb` plus `-mcpu cortex_m4` is. |
| Feature warnings such as `is not a recognized feature` | Distribution Zig builds against a different LLVM; the build still completes. Report it as noise, not failure. |
| `Unsupported operating system freestanding` | An std call needs an OS; remove it from the freestanding path. |
| macOS build needs frameworks | Provide the SDK via `--sysroot` and framework paths; a plain executable needs nothing. |
| System cross toolchain required by the build | GCC triplets, sysroots, and QEMU: use cross-gcc. Rust's equivalent: use rust-cross. |

## Output

A chat report with the triple and CPU, the build command or `build.zig` loop, the bare-metal or WebAssembly specifics when they apply, and the `file` line from the scratch build proving the target format. The triple and CPU lists are in `references/zig-target-triples.md`.
