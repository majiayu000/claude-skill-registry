---
description: Run PlatformIO tests for PrivacyLRS to validate code changes and security fixes
triggers:
  - run PrivacyLRS tests
  - test PrivacyLRS
  - run tests
  - execute PrivacyLRS test suite
  - validate PrivacyLRS changes
  - pio test
  - test security fixes
  - run unit tests
---

# PrivacyLRS Test Runner

Run automated tests for the PrivacyLRS codebase using PlatformIO's unit testing framework.

## Description

This skill runs the PrivacyLRS test suite, which consists of 11 test categories with 74 total test cases. Tests verify protocol handling, data structures, cryptographic operations (when present), and communication protocols. All tests run on the host system without requiring embedded hardware.

## When to Use This Skill

- After implementing security fixes to verify functionality
- Before creating pull requests
- During code reviews
- To validate changes don't break existing functionality
- For regression testing
- To verify cryptographic implementations (when tests exist)

## Prerequisites

1. PlatformIO must be installed:
   ```bash
   python3 -m pip install platformio
   ```

2. You must be in the PrivacyLRS source directory:
   ```bash
   cd $HOME/inavflight/PrivacyLRS/src
   ```

## Usage

### Run All Tests

**Basic command:**
```bash
cd $HOME/inavflight/PrivacyLRS/src
PLATFORMIO_BUILD_FLAGS="-DRegulatory_Domain_ISM_2400" pio test -e native
```

**Expected output:**
- 11 test suites
- 74 test cases
- ~21 seconds total duration
- All tests should PASS

### Run Specific Test

**Single test category:**
```bash
cd $HOME/inavflight/PrivacyLRS/src
pio test -e native --filter test_crc
```

**Available test categories:**
- `test_fmap` - Frequency mapping
- `test_fhss` - Frequency hopping
- `test_msp` - MSP protocol
- `test_msp2crsf2msp` - Protocol conversion
- `test_fifo` - FIFO buffers
- `test_stubborn` - Reliable transmission
- `test_telemetry` - Telemetry encoding
- `test_msp_vtx` - VTX control
- `test_crsf` - Crossfire protocol
- `test_ota` - OTA packets
- `test_crc` - CRC algorithms

### Verbose Output

**For debugging test failures:**
```bash
pio test -e native -vv  # Very verbose
```

### List Available Tests

**Without running:**
```bash
pio test -e native --list-tests
```

### Clean Build

**If tests behave unexpectedly:**
```bash
pio test -e native --clean
```

## Test Categories

### Protocol Tests
- **test_crsf** - Crossfire protocol handling (2 tests)
- **test_msp** - MultiWii Serial Protocol (4 tests)
- **test_msp2crsf2msp** - Protocol conversion (9 tests)
- **test_msp_vtx** - Video transmitter control (2 tests)

### Data Structure Tests
- **test_fifo** - FIFO buffer implementation (3 tests)
- **test_fmap** - Frequency mapping (2 tests)

### Communication Tests
- **test_fhss** - Frequency hopping (5 tests)
- **test_ota** - Over-the-air packets (18 tests)
- **test_telemetry** - Telemetry data (11 tests)
- **test_stubborn** - Reliable transmission (13 tests)

### Algorithm Tests
- **test_crc** - CRC calculation algorithms (5 tests)

## Security Testing Notes

### Current Test Coverage

**⚠️ CRITICAL GAP: No encryption tests currently exist**

The existing test suite does NOT include:
- ❌ ChaCha20 cipher tests
- ❌ Encryption/decryption tests
- ❌ Key derivation tests
- ❌ Counter synchronization tests
- ❌ Random number generation tests
- ❌ Replay protection tests

**This means:**
- Security fixes cannot be validated with existing tests
- Cryptographic implementations are not regression tested
- Counter synchronization fixes cannot be verified

### Required New Tests (For Security Validation)

To test security findings from the comprehensive analysis, create:

**test_encryption/** directory with:
1. `test_chacha20.cpp` - Basic ChaCha20 functionality
2. `test_counter_sync.cpp` - **CRITICAL** - Packet loss handling
3. `test_key_derivation.cpp` - Master/session key generation
4. `test_encrypt_decrypt.cpp` - Full encryption cycle
5. `test_resync.cpp` - Resynchronization mechanism
6. `test_replay_protection.cpp` - Replay attack prevention
7. `test_rng.cpp` - Random number generation quality

**How to create encryption tests:**
```bash
# Create test directory
mkdir -p $HOME/inavflight/PrivacyLRS/src/test/test_encryption

# Create test file (example structure)
cat > test_encryption/test_chacha20.cpp <<'EOF'
#include <unity.h>
#include "encryption.h"

void test_encrypt_decrypt_roundtrip(void) {
    // Test implementation here
    uint8_t plaintext[16] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
    uint8_t encrypted[16];
    uint8_t decrypted[16];

    EncryptMsg(encrypted, plaintext);
    DecryptMsg(decrypted);

    TEST_ASSERT_EQUAL_MEMORY(plaintext, decrypted, 16);
}

void setUp(void) {}
void tearDown(void) {}

void process(void) {
    UNITY_BEGIN();
    RUN_TEST(test_encrypt_decrypt_roundtrip);
    UNITY_END();
}

int main(int argc, char **argv) {
    process();
    return 0;
}
EOF

# Run new test
pio test -e native --filter test_encryption
```

## Interpreting Test Results

### Success Output
```
================= 74 test cases: 74 succeeded in 00:00:21.441 =================
```

All tests passed - code is functioning correctly.

### Failure Output
```
test/test_crc/test_crc.cpp:288: test_crc14_implementation_compatibility [FAILED]
```

Test failed - indicates bug or regression. Check:
1. What changed since last successful run
2. Test assertion details
3. Expected vs actual values

### Build Errors
```
error: 'functionName' was not declared in this scope
```

Compilation failed - fix syntax/compilation errors before tests can run.

## Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `-e native` | Run on native environment (host PC) | Required for all commands |
| `--filter <name>` | Run only specific test | `--filter test_crc` |
| `-v, -vv, -vvv` | Increase verbosity | `-vv` for detailed output |
| `--list-tests` | Show available tests | Don't run, just list |
| `--without-building` | Skip compilation | If already built |
| `--clean` | Clean before building | Force full rebuild |

## Workflow for Testing Security Fixes

### Step 1: Create Failing Test (TDD Approach)
```bash
# Write test that demonstrates the vulnerability
mkdir -p test/test_encryption
# Create test file that FAILS with current code
pio test -e native --filter test_encryption
# Expected: FAILED (vulnerability exists)
```

### Step 2: Implement Security Fix
```bash
# Edit source code to fix vulnerability
# Example: Fix counter synchronization in common.cpp
```

### Step 3: Verify Fix
```bash
# Run test again
pio test -e native --filter test_encryption
# Expected: PASSED (fix works)
```

### Step 4: Regression Test
```bash
# Run ALL tests to ensure no breakage
pio test -e native
# Expected: All 74+ tests PASSED
```

### Step 5: Performance Check
```bash
# Measure timing before/after fix
pio test -e native -vv | grep "Duration"
# Ensure no significant performance degradation
```

## Troubleshooting

### Issue: "platformio: command not found"
**Solution:**
```bash
python3 -m pip install platformio
# Add ~/.local/bin to PATH if needed
```

### Issue: "Environment 'native' does not exist"
**Solution:**
```bash
# Ensure you're in correct directory
cd $HOME/inavflight/PrivacyLRS/src
# Verify platformio.ini exists
ls platformio.ini
```

### Issue: "Platform 'native' is not installed"
**Solution:**
```bash
cd $HOME/inavflight/PrivacyLRS/src
platformio pkg install --platform native
platformio pkg update
```

### Issue: Tests fail unexpectedly
**Solution:**
```bash
# Clean and rebuild
pio test -e native --clean
# If still failing, check recent code changes
git diff
```

### Issue: "No such file or directory"
**Solution:**
```bash
# Verify you're in PrivacyLRS/src directory
pwd
# Should show: $HOME/inavflight/PrivacyLRS/src
```

## Performance Benchmarks

**Baseline (as of 2025-11-30):**
- Total test time: ~21.4 seconds
- Longest individual test: test_fmap (~6.7 seconds, includes first-time setup)
- Average test time: ~1.5 seconds
- Total test cases: 74
- Success rate: 100%

**After implementing security fixes:**
- Re-run tests and compare timing
- Acceptable overhead: <10% increase in total test time
- If >10% slower, investigate optimization opportunities

## CI/CD Integration

Tests run automatically on GitHub Actions for every push/PR:

```yaml
# From .github/workflows/build.yml
- name: Run PlatformIO Tests
  run: |
    cd src
    platformio pkg install --platform native
    platformio pkg update
    PLATFORMIO_BUILD_FLAGS="-DRegulatory_Domain_ISM_2400" pio test -e native
```

## Quick Reference Card

**Basic test run:**
```bash
cd ~/Documents/planes/inavflight/PrivacyLRS/src && \
PLATFORMIO_BUILD_FLAGS="-DRegulatory_Domain_ISM_2400" pio test -e native
```

**Single test:**
```bash
cd ~/Documents/planes/inavflight/PrivacyLRS/src && \
pio test -e native --filter test_crc
```

**Verbose output:**
```bash
cd ~/Documents/planes/inavflight/PrivacyLRS/src && \
pio test -e native -vv
```

**Clean build:**
```bash
cd ~/Documents/planes/inavflight/PrivacyLRS/src && \
pio test -e native --clean
```

## Related Files

- Test infrastructure notes: `claude/security-analyst/privacylrs-test-infrastructure-notes.md`
- Security findings: `claude/security-analyst/sent/2025-11-30-1500-findings-privacylrs-comprehensive-analysis.md`
- Test directory: `PrivacyLRS/src/test/`
- PlatformIO config: `PrivacyLRS/src/platformio.ini`
- CI/CD config: `PrivacyLRS/.github/workflows/build.yml`

## Additional Resources

- PlatformIO Unit Testing: https://docs.platformio.org/page/plus/unit-testing.html
- Unity Testing Framework: http://www.throwtheswitch.org/unity
- Test infrastructure notes: See detailed notes in security-analyst workspace

---

## Related Skills

- **test-privacylrs-hardware** - Flash and test on real ESP32 hardware
- **create-pr** - Create pull requests (run tests before PR creation)

---

**Skill created by:** Security Analyst / Cryptographer
**Date:** 2025-11-30
**Purpose:** Enable automated testing for security fix validation
