---
name: testing
description: "Use when running tests to validate implementations, collecting test evidence, or debugging failures. Load in TEST state. Covers unit tests (pytest/jest), API tests (curl), browser tests (Claude-in-Chrome), database verification. All results are code-verified, not LLM-judged."
keywords: test, verify, pytest, jest, api, browser, evidence
---

# Testing

Comprehensive testing for TEST state.

## Instructions

1. Run unit tests: `scripts/run-unit-tests.sh`
2. Run API tests: `scripts/run-api-tests.sh`
3. Run browser tests (if UI): via Claude-in-Chrome MCP
4. Verify database (if data): `scripts/verify-database.sh`
5. Collect evidence: `scripts/collect-evidence.sh`
6. Report results (code verified, not judged)

## Exit Criteria (Code Verified)

```bash
# All must return exit code 0
scripts/run-unit-tests.sh
scripts/run-api-tests.sh
[ -f "/tmp/test-evidence/results.json" ]
jq '.all_passed == true' /tmp/test-evidence/results.json
```

## References

| File | Load When |
|------|-----------|
| references/unit-testing.md | Writing/running unit tests |
| references/api-testing.md | Testing API endpoints |
| references/browser-testing.md | UI testing with Chrome |
| references/database-testing.md | Database verification |
