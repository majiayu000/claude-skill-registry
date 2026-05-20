---
name: compact-core:compilation-tooling
description: Use when working with the Compact compiler (compactc), configuring build settings, understanding zkir/prover/verifier output artifacts, setting up COMPACT_PATH, or integrating VS Code language server support for Midnight smart contract development.
---

# Compilation Tooling

Complete guide to the Compact compiler (`compactc`), project organization, build workflows, and understanding compilation output.

## Quick Reference

### Basic Compilation

```bash
# Compile a contract
compactc contract.compact -o output/

# Compile with debug mode (faster, no ZK proofs)
compactc contract.compact -o output/ --skip-zk

# Generate VS Code language server support
compactc contract.compact -o output/ --vscode
```

### Compiler Flags

| Flag | Description | Example |
|------|-------------|---------|
| `-o, --output` | Output directory | `-o build/` |
| `--skip-zk` | Skip ZK proof generation (dev mode) | `--skip-zk` |
| `--vscode` | Generate VS Code language server files | `--vscode` |
| `-I, --include` | Add include path | `-I ./lib` |
| `--verbose` | Verbose output | `--verbose` |
| `--json` | JSON output format | `--json` |
| `--no-typescript` | Skip TypeScript generation | `--no-typescript` |

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `COMPACT_PATH` | Include path resolution | `export COMPACT_PATH="/libs:/project/src"` |
| `MIDNIGHT_NETWORK` | Target network | `export MIDNIGHT_NETWORK="testnet"` |

## Output Artifacts

Compilation produces several output files:

```
output/
├── zkir/                    # Zero-knowledge intermediate representation
│   ├── circuit_name.zkir    # Circuit IR for each exported circuit
│   └── ...
├── keys/
│   ├── prover/              # Prover keys (for proof generation)
│   │   └── circuit_name.pk
│   └── verifier/            # Verifier keys (for on-chain verification)
│       └── circuit_name.vk
├── contract.ts              # TypeScript types and contract interface
├── witnesses.ts             # Witness type definitions
└── index.ts                 # Main export file
```

## Development Workflow

```
1. Write Compact contract
2. Compile with --skip-zk for fast iteration
3. Run TypeScript tests
4. When ready: Full compile (generates ZK keys)
5. Deploy to testnet
```

### Fast Development Loop

```bash
# Fast iteration (no proof generation)
compactc contract.compact -o build/ --skip-zk

# Full build for deployment
compactc contract.compact -o build/
```

## Project Structure

Recommended project layout for Midnight DApps:

```
my-midnight-project/
├── contracts/
│   ├── main.compact           # Main contract entry point
│   ├── types.compact          # Shared type definitions
│   └── lib/                   # Helper modules
│       └── utils.compact
├── src/                       # TypeScript application code
│   ├── index.ts
│   ├── witnesses.ts           # Witness implementations
│   └── deploy.ts
├── build/                     # Compiled output (gitignored)
│   ├── zkir/
│   ├── keys/
│   └── *.ts
├── tests/
│   └── contract.test.ts
├── package.json
├── tsconfig.json
└── .env                       # Environment configuration
```

## VS Code Integration

Generate language server support for VS Code:

```bash
compactc contract.compact -o build/ --vscode
```

This creates `.vscode/` configuration for:
- Syntax highlighting
- Error diagnostics
- Type checking
- Go to definition

## References

For detailed documentation:

- [Compiler Usage](./references/compiler-usage.md) - All compactc flags and options
- [Project Structure](./references/project-structure.md) - Recommended project layouts
- [Output Artifacts](./references/output-artifacts.md) - Understanding compiled output

## Examples

Working project templates and scripts:

- [Project Template](./examples/project-template/) - Complete starter project
- [Build Scripts](./examples/build-scripts/) - Build, watch, and validation scripts
