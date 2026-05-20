---
name: test-mcp-compliance
description: Validates Model Context Protocol (MCP) compliance by running official compliance test suite against Pierre server
user-invocable: true
---

# MCP Compliance Validation Skill

## Purpose
Validates Model Context Protocol (MCP) compliance by running the official compliance test suite against the Pierre server.

## CLAUDE.md Compliance
- ✅ Uses existing validation script (no new code)
- ✅ No external dependencies beyond test suite
- ✅ Deterministic test execution

## Usage
Run this skill before:
- Protocol handler changes
- Tool modifications
- SDK releases
- Production deployments

## Prerequisites
- `mcp-compliance` repository cloned to `../mcp-compliance/`
- Pierre server must be runnable

## Commands

### Quick Validation
```bash
# Ensure mcp-compliance repo exists and run tests
./scripts/ci/ensure-mcp-compliance.sh
```

### Detailed Validation
```bash
# 1. Ensure compliance suite is installed
./scripts/ci/ensure-mcp-compliance.sh

# 2. Start Pierre server
cargo run --bin pierre-mcp-server &
SERVER_PID=$!
sleep 3

# 3. Run compliance tests
cd ../mcp-compliance
bun test -- --server="http://localhost:8081/mcp"
TEST_RESULT=$?
cd -

# 4. Cleanup
kill $SERVER_PID

# 5. Exit with test result
exit $TEST_RESULT
```

### Manual Compliance Check
```bash
# Check JSON-RPC 2.0 compliance
rg "jsonrpc.*2\.0" src/mcp/ --type rust -n | head -10

# Verify error code compliance
rg "error.*code.*-32[0-9]{3}" src/mcp/ --type rust -A 3 | head -20

# Check tool schema format
rg "struct ToolDefinition|inputSchema" src/protocols/universal/tool_registry.rs --type rust -A 10 | head -30
```

## Success Criteria
- ✅ All MCP compliance tests pass
- ✅ JSON-RPC 2.0 format validated
- ✅ Tool schemas match specification
- ✅ Error responses properly formatted

## Troubleshooting

**Issue:** `mcp-compliance` repo not found
```bash
# Clone the compliance suite
git clone https://github.com/modelcontextprotocol/mcp-compliance ../mcp-compliance
cd ../mcp-compliance
bun install
cd -
```

**Issue:** Server won't start
```bash
# Check if port 8081 is in use
lsof -i :8081
# Kill existing process or use different port
```

**Issue:** Tests timeout
```bash
# Increase timeout in compliance suite
# Or run server separately and ensure it's responsive
curl -X POST http://localhost:8081/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## Related Files
- `scripts/ci/ensure-mcp-compliance.sh` - Compliance runner script
- `src/mcp/protocol.rs` - MCP protocol implementation
- `src/protocols/universal/tool_registry.rs` - Tool definitions

## Related Skills
- `run-full-test-suite` - Full test suite execution
