---
name: run-fuzz
description: Run cargo-fuzz targets with proper nightly toolchain and options
disable-model-invocation: true
---

# Run Fuzz Target

Run fuzz tests against the scanner's parsing and decoding logic.

## Usage

- `/run-fuzz <target>` - Run specific fuzz target (default 10,000 runs)
- `/run-fuzz <target> <runs>` - Run with custom iteration count
- `/run-fuzz all` - Run all targets briefly (1,000 runs each)
- `/run-fuzz list` - List available targets

## Available Targets

| Target | Tests |
|--------|-------|
| `fuzz_anchor_soundness` | Anchor extraction correctness |
| `fuzz_b64_gate_build_and_scan` | Base64 gate construction and scanning |
| `fuzz_b64_gate_determinism` | Base64 gate deterministic behavior |
| `fuzz_b64_gate_differential` | Base64 gate differential testing |
| `fuzz_tiger_chunking` | Tiger harness chunking logic |

## Workflow

### Run Single Target

```bash
cd fuzz && cargo +nightly fuzz run <target> -- -runs=10000
```

### Run All Targets

```bash
cd fuzz
for target in fuzz_anchor_soundness fuzz_b64_gate_build_and_scan fuzz_b64_gate_determinism fuzz_b64_gate_differential fuzz_tiger_chunking; do
  echo "Running $target..."
  cargo +nightly fuzz run $target -- -runs=1000
done
```

### Check for Crashes

Crashes are saved to `fuzz/artifacts/<target>/`. To reproduce:

```bash
cargo +nightly fuzz run <target> fuzz/artifacts/<target>/<crash-file>
```

## Prerequisites

- Nightly Rust toolchain: `rustup install nightly`
- cargo-fuzz: `cargo install cargo-fuzz`
