---
name: ucp-conformance
description: Run and write UCP conformance tests — validate a UCP implementation against the official test suite covering checkout lifecycle, orders, fulfillment, payments, idempotency, webhooks, and security. Use when testing or validating a UCP implementation.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Conformance Testing

## Before running tests

**Fetch the latest test suite**: Web-search `github Universal-Commerce-Protocol conformance` and fetch the README for current setup instructions, test data format, and CLI flags.

Repository: https://github.com/Universal-Commerce-Protocol/conformance

## Conceptual Architecture

### What the Conformance Suite Tests

The official suite contains ~13 test files covering:

| Test File | What It Validates |
|-----------|-------------------|
| Checkout lifecycle | Full create → update → complete → verify flow |
| Order management | Order creation, status transitions, data integrity |
| Fulfillment | Shipping/pickup methods, group selection, option validation |
| Card credentials | Payment credential format, tokenization |
| Webhooks | Delivery, retry, signature verification |
| Idempotency | Duplicate request handling, cache behavior |
| Invalid input | Error responses for malformed requests |
| Protocol compliance | Headers, TLS, version negotiation |
| Data validation | Schema compliance, required fields, type correctness |
| Service bindings | REST/MCP/A2A transport correctness |
| Business logic | Totals calculation, tax, discount application |
| AP2 integration | Mandate generation, signing, verification |
| Security (simulation URLs) | URL validation, injection prevention |

### How to Run

1. Clone the conformance repo
2. Install dependencies with `uv sync`
3. Start your UCP server locally
4. Run tests pointing at your server:

```bash
uv run checkout_lifecycle_test.py \
  --server_url=http://localhost:8182 \
  --simulation_secret=your-secret \
  --conformance_input=test_data/your_store/conformance_input.json
```

### Test Data

Tests require a `conformance_input.json` file that describes your store's products, prices, and expected behaviors. Check the sample test data in the repo for the format.

### Writing Custom Conformance Tests

When extending UCP with custom capabilities:
1. Use the same test patterns as the official suite
2. Test capability negotiation (extension present/absent)
3. Test schema validation against your custom schemas
4. Test error cases specific to your extension
5. Test idempotency for all mutating operations

### Integration with CI/CD

- Run conformance tests as part of your CI pipeline
- Use the `--server_url` flag to point at staging environments
- Track test pass rates as a quality gate for deployments

Always fetch the latest test suite before running — new tests are added as the spec evolves.
