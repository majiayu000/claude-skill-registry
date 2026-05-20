---
name: swift-wasm
description: Swift WASM development with Swift 6.2 APIs. Use for setting up WASM toolchains, building for WebAssembly, optimizing bundles, debugging WASM apps, or troubleshooting Swift WASM issues.
allowed-tools: Bash, Read, Grep, Glob, WebFetch, WebSearch
user-invocable: true
argument-hint: [setup|build|dev|optimize|debug|test]
---

# Swift WASM Development Skill

Comprehensive support for Swift 6.2 WebAssembly development using official toolchains, Carton, and modern WASM APIs.

## Quick Actions

When invoked with arguments:
- `setup` - Set up Swift 6.2.3 + WASM SDK or Carton
- `build` - Build the current project for WASM
- `dev` - Start development server with hot reload
- `optimize` - Build optimized production bundle
- `debug` - Debug WASM build issues
- `test` - Run tests in browser

When invoked without arguments or when the user asks about Swift WASM:
- Analyze their needs and provide appropriate guidance
- Reference existing documentation in the project
- Execute appropriate commands

## Project Documentation

This project has excellent existing documentation:
- **NATIVE_WASM_SETUP.md** - Official Swift 6.2.3 + WASM SDK setup
- **CARTON_WORKFLOW.md** - Complete Carton development workflow
- **QUICKSTART.md** - Getting started guide

Always reference these docs when helping users.

## Swift 6.2 WASM Key Facts (2026)

### Official Support
- Swift 6.2+ includes **native WebAssembly support** (no custom forks needed)
- Two SDK variants: `swift-6.2.3-RELEASE_wasm` (full stdlib) and `swift-6.2.3-RELEASE_wasm-embedded` (tiny)
- Target triple: `wasm32-unknown-wasip1` (newer than `wasm32-unknown-wasi`)
- Official distribution via swift.org

### Tooling Options

**Option 1: Official Swift 6.2.3 + WASM SDK (Production)**
- Latest Swift with official WASM support
- ~50MB SDK download
- Requires swiftly toolchain manager
- Best for production and CI/CD

**Option 2: Carton (Development)**
- All-in-one development tool
- Built-in dev server with hot reload
- Automatic SwiftWasm download
- Uses SwiftWasm 6.0.2 (slightly older)
- Best for rapid development

### Key Libraries
- **JavaScriptKit** - Swift/JavaScript interop (currently 0.19.2 in this project)
- **WasmKit** - WebAssembly runtime in Swift (included with Swift 6.2+)
- **BridgeJS** - TypeScript to Swift code generation
- **PackageToJS** - Export Swift to JavaScript

## Common Commands Reference

### Setup Commands

```bash
# Install swiftly (Swift toolchain manager)
brew install swiftly

# Install swift.org Swift 6.2.3
swiftly install 6.2.3
swiftly use 6.2.3

# Verify (should NOT say "Apple Swift")
swift --version

# Install WASM SDK
swift sdk install \
  https://download.swift.org/swift-6.2.3-release/wasm-sdk/swift-6.2.3-RELEASE/swift-6.2.3-RELEASE_wasm.artifactbundle.tar.gz \
  --checksum 394040ecd5260e68bb02f6c20aeede733b9b90702c2204e178f3e42413edad2a

# Verify SDK installation
swift sdk list
```

### Build Commands

```bash
# Native WASM build (debug)
swift build --swift-sdk swift-6.2.3-RELEASE_wasm

# Native WASM build (optimized production)
swift build --swift-sdk swift-6.2.3-RELEASE_wasm -c release -Xswiftc -Osize

# Carton development server
carton dev

# Carton production bundle
carton bundle --release

# Carton with size optimization
carton bundle --release -Xswiftc -Osize -Xswiftc -whole-module-optimization
```

### Optimization Commands

```bash
# Build with all optimizations
swift build \
  --swift-sdk swift-6.2.3-RELEASE_wasm \
  -c release \
  -Xswiftc -Osize \
  -Xswiftc -whole-module-optimization \
  -Xlinker --lto-O3 \
  -Xlinker --gc-sections \
  -Xlinker --strip-debug

# Post-process optimization (requires wasm-opt from binaryen)
wasm-opt -O3 input.wasm -o output.wasm

# Compress with Brotli
brotli -q 11 optimized.wasm
```

### Development Commands

```bash
# Start simple dev server
python3 -m http.server 8000

# Watch for changes (manual)
swift build --swift-sdk swift-6.2.3-RELEASE_wasm && python3 -m http.server 8000

# Check build output
ls -lh .build/wasm32-unknown-wasip1/release/
```

### Testing Commands

```bash
# Run tests with Carton
carton test

# Run tests in specific browser
carton test --environment chrome
carton test --environment firefox
carton test --environment safari
```

## Workflow Patterns

### Pattern 1: Quick Development (Carton)

```bash
# One-time setup
echo "wasm-6.0.2-RELEASE" > .swift-version

# Daily workflow
carton dev
# Edit Sources/*.swift
# Browser auto-refreshes on save
```

### Pattern 2: Production Build (Official SDK)

```bash
# Ensure using swift.org toolchain
swiftly use 6.2.3

# Build optimized
swift build --swift-sdk swift-6.2.3-RELEASE_wasm -c release -Xswiftc -Osize

# Serve for testing
python3 -m http.server 8000
```

### Pattern 3: CI/CD Pipeline

```bash
# Install toolchain
swiftly install 6.2.3
swiftly use 6.2.3

# Install SDK
swift sdk install <URL> --checksum <CHECKSUM>

# Build
swift build --swift-sdk swift-6.2.3-RELEASE_wasm -c release

# Deploy .build/wasm32-unknown-wasip1/release/*.wasm
```

## Troubleshooting Guide

### "No available targets compatible with wasm32-unknown-wasip1"

**Cause:** Using Apple's Xcode Swift instead of swift.org Swift

**Solution:**
```bash
brew install swiftly
swiftly install 6.2.3
swiftly use 6.2.3
swift --version  # Should NOT say "Apple"
```

### Build is Slow

**Cause:** First build compiles all dependencies

**Solutions:**
- Use debug builds during development: `swift build --swift-sdk swift-6.2.3-RELEASE_wasm`
- Use Carton for incremental builds: `carton dev`
- Cache .build/ directory in CI/CD

### WASM File Too Large

**Typical sizes:**
- Debug: 3-5 MB
- Release: 800KB - 1.5 MB
- Release + Osize: 400-600 KB
- Brotli compressed: 150-250 KB

**Solutions:**
- Use `-Xswiftc -Osize` flag
- Enable link-time optimization: `-Xlinker --lto-O3`
- Strip debug symbols: `-Xlinker --strip-debug`
- Use wasm-opt: `wasm-opt -O3 input.wasm -o output.wasm`
- Compress with Brotli for serving

### Carton vs Native SDK Issues

**Problem:** Mixed Swift versions (Raven built with 6.2, app with 6.0)

**Solution:** Usually fine (ABI compatible), but for best results:
- Development: Use Carton (easier)
- Production: Use native SDK (latest features)
- CI/CD: Use native SDK (reproducible)

### JavaScriptKit Version Mismatch

**Current project:** Pinned to JavaScriptKit 0.19.2 for Swift 6.0 compatibility

**If upgrading:**
- Check SwiftWasm compatibility matrix
- Test thoroughly before upgrading
- Latest is 0.33.0+ (Feb 2026)

### Page Shows "Loading..." Forever

**Debugging steps:**
1. Open browser console (Cmd+Option+I)
2. Check for errors:
   - 404: WASM file not found (check path)
   - MIME type: Server not serving .wasm correctly
   - Instantiation: WASM runtime error
3. Verify WASM file exists: `ls -lh .build/wasm32-unknown-wasip1/*/YourApp.wasm`
4. Check file size (should be >100KB for real apps)

## Performance Best Practices

### Binary Size
- Use `-Osize` for size optimization
- Avoid heavy dependencies
- Enable whole-module optimization
- Use embedded SDK for size-critical apps
- Post-process with wasm-opt

### Load Time
- Compress with Brotli (3x smaller)
- Use CDN for JavaScriptKit runtime
- Preload WASM file: `<link rel="preload" href="/app.wasm" as="fetch" crossorigin>`
- Enable HTTP/2 or HTTP/3
- Use streaming compilation: `WebAssembly.instantiateStreaming()`

### Runtime Performance
- Minimize Swift/JS bridging calls
- Batch DOM updates
- Use async/await for non-blocking operations
- Profile with Chrome DevTools

### Development Speed
- Use Carton for hot reload
- Debug builds for faster iteration
- Release builds only for production
- Cache dependencies

## Debugging Techniques

### Browser DevTools

**Enable DWARF support in Chrome:**
1. Build with debug info: `swift build --swift-sdk swift-6.2.3-RELEASE_wasm -c debug`
2. Open Chrome DevTools
3. Sources tab → Enable DWARF support
4. Set breakpoints in Swift source
5. Step through code with full variable inspection

**Console debugging:**
```swift
import JavaScriptKit

// Log to browser console
let console = JSObject.global.console
console.log("Debug message:", someValue)
```

### LLDB Debugging

Swift 6.2 includes LLDB WebAssembly support:
```bash
# Build with debug symbols
swift build --swift-sdk swift-6.2.3-RELEASE_wasm -c debug

# Use WasmKit for debugging
# (Integration with LLDB for WASM targets)
```

### Performance Profiling

```bash
# Chrome DevTools Performance tab
# Record → Interact with app → Stop → Analyze

# Memory profiling
# Chrome DevTools Memory tab → Take heap snapshot
```

## Deployment Platforms

### Static Hosts (Recommended)
- **Netlify** - Zero config, automatic deploys
- **Vercel** - Edge network, serverless functions
- **GitHub Pages** - Free, simple, version controlled
- **Cloudflare Pages** - Global CDN, fast edge deployment

### Edge Computing
- **Cloudflare Workers** - Run WASM at the edge
- **Fastly Compute** - WASM-based edge compute

### Cloud Storage + CDN
- **AWS S3 + CloudFront** - Scalable, full control
- **Azure Static Web Apps** - Integrated CI/CD
- **Google Cloud Storage + CDN** - Global distribution

## Task Execution Logic

When invoked:

1. **Determine user intent** from argument or question
2. **Check current state:**
   - Which Swift version? (`swift --version`)
   - Is WASM SDK installed? (`swift sdk list`)
   - Is Carton available? (`carton --version`)
   - What's in Package.swift? (read file)
3. **Execute appropriate action:**
   - Setup: Guide through installation
   - Build: Choose Carton vs native based on context
   - Dev: Start appropriate dev server
   - Optimize: Apply production optimizations
   - Debug: Diagnose and fix issues
   - Test: Run appropriate test suite
4. **Provide next steps** and reference documentation

## Example Interactions

### User: "Set up Swift WASM"
1. Check if swiftly is installed
2. Install Swift 6.2.3 if needed
3. Install WASM SDK
4. Verify installation
5. Point to NATIVE_WASM_SETUP.md for details

### User: "Build my app"
1. Check if Carton is available
2. If yes and .swift-version exists: use Carton
3. Otherwise: use native SDK build
4. Display build output and file sizes
5. Suggest next steps (serve, optimize, deploy)

### User: "Why is my WASM file 5MB?"
1. Check current build configuration
2. Explain typical sizes
3. Suggest optimization flags
4. Run optimized build
5. Compare before/after sizes

### User: "Deploy to production"
1. Build optimized bundle
2. Show deployment options
3. Provide example configs for common platforms
4. Verify build output is ready

## Reference Links

- [Swift.org WASM Getting Started](https://swift.org/documentation/articles/wasm-getting-started.html)
- [SwiftWasm Book](https://book.swiftwasm.org/)
- [JavaScriptKit Documentation](https://swiftwasm.github.io/JavaScriptKit/)
- [Carton GitHub](https://github.com/swiftwasm/carton)
- [Swiftly Toolchain Manager](https://github.com/swiftlang/swiftly)
- [WasmKit Runtime](https://github.com/swiftwasm/WasmKit)

## Notes for Claude

- **Always check project docs first** - NATIVE_WASM_SETUP.md, CARTON_WORKFLOW.md, QUICKSTART.md
- **Verify before executing** - Check Swift version, SDK availability, etc.
- **Use appropriate tool** - Carton for dev, native SDK for production
- **Explain trade-offs** - Speed vs size, debug vs release, Carton vs native
- **Provide file references** - Use `file:line` format for navigation
- **Show actual output** - Run commands and display results
- **Suggest next steps** - Don't leave users hanging
- **Reference sizes** - Always show before/after when optimizing
- **Be platform-aware** - macOS vs Linux differences in setup
- **Check for updates** - Swift WASM ecosystem evolves rapidly

## Current Project Configuration

This Raven project uses:
- Swift 6.2.3 (`.swift-version`)
- JavaScriptKit 0.19.2 (pinned for compatibility)
- Platforms: macOS 13+, iOS 16+
- Optimized Package.swift with WASM flags

When helping with this project, respect these constraints and don't suggest breaking changes without discussion.
