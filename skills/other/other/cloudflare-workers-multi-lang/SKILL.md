---
name: workers-multi-lang
description: Multi-language Workers development with Rust, Python, and WebAssembly. Use when building Workers in languages other than JavaScript/TypeScript, or when integrating WASM modules for performance-critical code.
version: 1.0.0
---

# Multi-Language Workers Development

Build Cloudflare Workers using Rust, Python, or WebAssembly for performance-critical operations.

## Language Comparison

| Feature | JavaScript/TS | Rust | Python |
|---------|---------------|------|--------|
| **Startup** | Fast | Fastest (WASM) | Moderate |
| **CPU Perf** | Good | Excellent | Good |
| **Memory** | Higher | Lower | Higher |
| **Bundle Size** | Smaller | Medium | Larger |
| **Type Safety** | Optional (TS) | Strict | Optional |
| **Best For** | General apps | CPU-intensive | Data/ML |

## Quick Decision

```
Need maximum performance? → Rust/WASM
Heavy computation (crypto, image processing)? → Rust/WASM
Data processing, ML inference? → Python
General web apps? → JavaScript/TypeScript
```

## Top 10 Multi-Lang Errors

| Error | Language | Cause | Solution |
|-------|----------|-------|----------|
| `WebAssembly.instantiate() failed` | Rust | Invalid WASM | Check wasm-pack build output |
| `Module parse failed: Unexpected token` | Rust | ESM/CJS mismatch | Use `--target bundler` |
| `Cannot find module` | Python | Missing dep | Add to pyproject.toml |
| `Out of memory` | All | Large WASM | Enable streaming instantiation |
| `Exceeded CPU time limit` | All | Long computation | Chunk processing |
| `wasm-bindgen version mismatch` | Rust | Dep conflict | Align versions in Cargo.toml |
| `RuntimeError: unreachable` | Rust | Panic in WASM | Add proper error handling |
| `TypeError: not a function` | Rust | Missing export | Add `#[wasm_bindgen]` attribute |
| `Python worker startup timeout` | Python | Slow init | Minimize imports |
| `SharedArrayBuffer not supported` | All | Security | Add COOP/COEP headers |

## Rust Quick Start

```bash
# Install tools
cargo install wasm-pack

# Create project
cargo new --lib my-worker
cd my-worker

# Add to Cargo.toml
cat >> Cargo.toml << 'EOF'
[lib]
crate-type = ["cdylib"]

[dependencies]
wasm-bindgen = "0.2"
worker = "0.3"
console_error_panic_hook = "0.1"

[profile.release]
opt-level = "s"
lto = true
EOF
```

```rust
// src/lib.rs
use worker::*;

#[event(fetch)]
async fn fetch(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    console_error_panic_hook::set_once();

    Router::new()
        .get("/", |_, _| Response::ok("Hello from Rust!"))
        .get("/compute", |_, _| {
            // CPU-intensive computation
            let result = heavy_computation();
            Response::ok(format!("Result: {}", result))
        })
        .run(req, env)
        .await
}

fn heavy_computation() -> u64 {
    (1..1_000_000).filter(|n| is_prime(*n)).count() as u64
}

fn is_prime(n: u64) -> bool {
    if n < 2 { return false; }
    (2..=(n as f64).sqrt() as u64).all(|i| n % i != 0)
}
```

## Python Quick Start (Workers for Platforms)

```toml
# pyproject.toml
[project]
name = "my-worker"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

```python
# src/entry.py
from js import Response, Headers

async def on_fetch(request, env):
    url = request.url

    if "/compute" in url:
        result = heavy_computation()
        return Response.new(f"Result: {result}")

    return Response.new("Hello from Python!")

def heavy_computation():
    """CPU-intensive computation"""
    return sum(1 for n in range(2, 100000) if is_prime(n))

def is_prime(n):
    if n < 2:
        return False
    return all(n % i != 0 for i in range(2, int(n**0.5) + 1))
```

## WASM Module Integration

```typescript
// Load and use WASM module in TypeScript Worker
import wasmModule from './pkg/my_lib_bg.wasm';
import { init, process_data } from './pkg/my_lib';

let wasmInstance: WebAssembly.Instance;

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Initialize WASM once
    if (!wasmInstance) {
      wasmInstance = await WebAssembly.instantiate(wasmModule);
      init();
    }

    // Use WASM function
    const result = process_data(inputData);

    return Response.json({ result });
  },
};
```

## When to Load References

| Reference | Load When |
|-----------|-----------|
| `references/rust-workers.md` | Building Workers with Rust/WASM |
| `references/python-workers.md` | Using Python on Workers for Platforms |
| `references/wasm-integration.md` | Integrating WASM modules in any Worker |

## Performance Tips

1. **WASM Initialization**: Cache instance, use streaming
2. **Memory**: Use typed arrays for data transfer
3. **Bundle Size**: Enable LTO, strip debug info
4. **Cold Starts**: Keep WASM modules small
5. **Data Transfer**: Minimize JS/WASM boundary crossings

## See Also

- `workers-performance` - General optimization techniques
- `workers-testing` - Testing multi-language Workers
- `cloudflare-worker-base` - Basic Workers setup
