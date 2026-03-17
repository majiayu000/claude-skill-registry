---
name: hive-run
description: Build and run Hive integration tests. Use when you need to test Ethereum clients using Hive's simulation framework.
argument-hint: "[simulator] [--client client-name]"
disable-model-invocation: true
---

# Run Hive Tests

Build Hive and run integration test simulations against Ethereum clients.

## Arguments

- `$0`: Simulator to run (e.g., `ethereum/sync`, `ethereum/rpc`)
- `--client`: Client to test against (e.g., `core-geth`, `go-ethereum`)

## Hive Structure

- Client definitions: `hive/clients/<name>/`
- Simulators: `hive/simulators/<category>/<name>/`
- Clients are Docker containers configured via `HIVE_*` environment variables

## Workflow

1. Navigate to the hive directory
2. Build hive if needed:
   ```bash
   go build .
   ```
3. Run the specified simulator:
   ```bash
   ./hive --sim $0 --client <client>
   ```
4. Report the test results

## Common Simulators

- `ethereum/sync` - Block synchronization tests
- `ethereum/rpc` - JSON-RPC API tests
- `ethereum/consensus` - Consensus mechanism tests

## Example Usage

```
/hive-run ethereum/sync --client core-geth
/hive-run ethereum/rpc --client go-ethereum
```

## Troubleshooting

If tests fail:
1. Check Docker is running and accessible
2. Verify the client image builds successfully
3. Check hive logs in the workspace directory
4. Consult [Hive Documentation](https://github.com/ethereum/hive/tree/master/docs)
