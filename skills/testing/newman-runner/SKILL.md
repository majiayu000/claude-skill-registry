---
name: newman-runner
description: Run and analyze Newman (Postman CLI) tests. Use when running API tests, validating Postman collections, testing HTTP endpoints, or when user mentions Newman, Postman tests, API validation.
allowed-tools: Bash, Read, Write
---

# Newman Runner

This skill provides tools to run Newman (Postman CLI) tests and analyze the results for API testing and validation.

## Instructions

### Running Newman Tests

1. **Verify Newman Installation**
   - Check if Newman is installed: `which newman`
   - If not installed, install with: `npm install -g newman`

2. **Run Collection**
   - Use script: `scripts/run-newman.sh <collection.json>`
   - Or manually: `newman run collection.json --reporters cli,json --reporter-json-export output.json`

3. **Analyze Results**
   - Parse JSON output with: `scripts/analyze-newman-results.py output.json`
   - Extract: Pass/fail status, response times, error messages, assertions

### Available Scripts

- **`scripts/run-newman.sh`** - Run Newman with standard options
- **`scripts/analyze-newman-results.py`** - Parse Newman JSON output
- **`scripts/validate-collection.sh`** - Validate Postman collection structure

## Examples

**Example 1: Run API Tests**
```bash
# Run Newman tests on Postman collection
./scripts/run-newman.sh my-api-tests.json

# Analyze results
./scripts/analyze-newman-results.py newman-results.json
```

**Example 2: Validate Collection**
```bash
# Check collection is valid before running
./scripts/validate-collection.sh my-collection.json
```

## Requirements

- Newman installed globally: `npm install -g newman`
- Valid Postman collection JSON file
- Python 3.7+ for analysis scripts

## Success Criteria

- ✅ Newman tests run successfully
- ✅ Results parsed and analyzed
- ✅ Pass/fail status clearly reported
- ✅ Error details extracted for failures
