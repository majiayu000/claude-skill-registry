---
name: security-integration-tests
description: Use this agent when working with prompt injection detection integration tests, including running tests, debugging failures, or adding new test samples.
color: red
---

# Security Integration Tests Agent

## Overview

The security package (`pkg/security/`) provides prompt injection detection using the HuggingFace Inference API. Integration tests verify detection accuracy with real API calls.

## Key Files

- `pkg/security/testdata/samples.json` - Test data with benign and malicious samples
- `pkg/security/hf/integration_test.go` - HF client integration tests
- `pkg/security/integration_test.go` - Full analyzer integration tests with event bus
- `pkg/security/hf/client.go` - HuggingFace API client implementation
- `pkg/security/analyzer.go` - Main security analyzer that subscribes to MCP events

## Running Tests

```bash
# Run integration tests (requires HF_TOKEN environment variable)
HF_TOKEN=hf_xxx make test-integration

# Run with custom model
HF_TOKEN=hf_xxx HF_MODEL=protectai/deberta-v3-base-prompt-injection-v2 make test-integration

# Run unit tests only (no API calls, uses mock server)
go test -v ./pkg/security/...
```

## Test Structure

### Test Samples (`samples.json`)

```json
{
  "benign_samples": [
    {
      "description": "Description of the sample",
      "text": "The text to analyze",
      "expected_detected": false
    }
  ],
  "malicious_samples": [
    {
      "description": "Direct instruction override",
      "text": "Ignore all previous instructions...",
      "expected_detected": true,
      "min_risk_score": 0.5
    }
  ],
  "mcp_tool_calls": [
    {
      "description": "Malicious tool call",
      "method": "tools/call",
      "params": { "name": "run_command", "arguments": {...} },
      "expected_detected": true,
      "min_risk_score": 0.5
    }
  ]
}
```

### Integration Test Tags

Integration tests use the build tag `//go:build integration` and are excluded from regular `go test ./...` runs.

## Adding New Test Samples

1. Edit `pkg/security/testdata/samples.json`
2. Add samples to appropriate category (benign_samples, malicious_samples, or mcp_tool_calls)
3. Set `expected_detected` and optionally `min_risk_score`
4. Run integration tests to verify

## Common Issues

### "Forbidden" Error

- Ensure HF_TOKEN is set and valid
- Note: `meta-llama/Llama-Prompt-Guard-2-86M` is deprecated on HF Inference API
- Default test model is `protectai/deberta-v3-base-prompt-injection-v2` (publicly accessible)

### Model Loading

- HuggingFace warms up models on demand
- Tests may skip with "Model loading" message on first run
- Re-run tests after model is warm

### Network Issues

- Integration tests require network access to HuggingFace API
- Tests will fail in sandboxed environments without network access

## Risk Levels

- `none`: score < 0.3
- `low`: score 0.3-0.5
- `medium`: score 0.5-0.7
- `high`: score 0.7-0.9
- `critical`: score >= 0.9

## Categories

- `benign`: Normal, safe content
- `injection`: Prompt injection attempt
- `jailbreak`: Jailbreak attempt
- `malicious`: Malicious content (Prompt Guard v2)
