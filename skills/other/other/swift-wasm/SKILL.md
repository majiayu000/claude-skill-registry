---
name: swift-wasm
description: Swift WASM development for setup, build, optimize, debug, and test workflows in Raven and related apps.
---

# Swift WASM Development Skill

Comprehensive guidance for Swift 6.2 WebAssembly workflows used by Raven.

## Quick Actions

- `setup`: Set up Swift toolchain and WASM SDK
- `build`: Build the current project for WASM
- `dev`: Start development workflow/server
- `optimize`: Build an optimized production bundle
- `debug`: Diagnose build/runtime WASM issues
- `test`: Run tests and browser validation

## Project Docs To Prefer

- `QUICKSTART.md`
- `Documentation/GettingStarted.md`
- `Docs/bundle-size-quickstart.md`

## Setup Commands

```bash
brew install swiftly
swiftly install 6.2.3
swiftly use 6.2.3
swift --version

swift sdk install \
  https://download.swift.org/swift-6.2.3-release/wasm-sdk/swift-6.2.3-RELEASE/swift-6.2.3-RELEASE_wasm.artifactbundle.tar.gz \
  --checksum 394040ecd5260e68bb02f6c20aeede733b9b90702c2204e178f3e42413edad2a

swift sdk list
```

## Build Commands

```bash
swift build --swift-sdk swift-6.2.3-RELEASE_wasm
swift build --swift-sdk swift-6.2.3-RELEASE_wasm -c release -Xswiftc -Osize
```

## Optimization Commands

```bash
swift build \
  --swift-sdk swift-6.2.3-RELEASE_wasm \
  -c release \
  -Xswiftc -Osize \
  -Xswiftc -whole-module-optimization \
  -Xlinker --lto-O3 \
  -Xlinker --gc-sections \
  -Xlinker --strip-debug
```

## Typical Issues

- "No available targets compatible with wasm32-unknown-wasip1": wrong Swift toolchain or missing WASM SDK
- large WASM bundle: missing `-Osize` / LTO / strip
- stale browser behavior: cached WASM artifact

## Working Norms

- Prefer official swift.org toolchains for reproducible builds.
- For example apps, build inside each example directory when possible.
- Confirm output location under `.build/wasm32-unknown-wasip1/`.
