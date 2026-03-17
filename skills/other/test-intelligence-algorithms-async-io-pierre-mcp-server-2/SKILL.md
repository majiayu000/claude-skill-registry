---
name: test-intelligence-algorithms
description: Validates sports science algorithms (VDOT, TSS, TRIMP, FTP, VO2max, Recovery, Nutrition) for correctness
user-invocable: true
---

# Test Intelligence Algorithms Skill

## Purpose
Validates sports science algorithms (VDOT, TSS, TRIMP, FTP, VO2max, Recovery, Nutrition) for mathematical correctness and physiological plausibility.

## CLAUDE.md Compliance
- ✅ Uses synthetic athlete data (no external dependencies)
- ✅ Deterministic tests with known outcomes
- ✅ Tests edge cases and error conditions
- ✅ Validates against research-based reference values

## Usage
Run this skill:
- After modifying algorithm implementations
- After changing algorithm configurations
- Before releases
- When validating sports science accuracy
- After updating physiological constants

## Prerequisites
- Rust toolchain
- Intelligence test fixtures in `tests/`

## Commands

### All Intelligence Tests
```bash
# Run all intelligence algorithm tests
cargo test intelligence -- --nocapture
```

### Basic Intelligence Tests
```bash
# Fundamental algorithm validation
cargo test --test intelligence_tools_basic_test -- --nocapture
```

### Advanced Intelligence Tests
```bash
# Complex scenarios and edge cases
cargo test --test intelligence_tools_advanced_test -- --nocapture
```

## Specific Algorithm Tests

### VDOT (Running Performance)
```bash
# Test VDOT calculation
cargo test test_vdot -- --nocapture

# Test race predictions
cargo test test_race_prediction -- --nocapture

# Test training paces
cargo test test_training_paces -- --nocapture
```

**Expected Values:**
```
Beginner (5K in 30:00):    VDOT ≈ 30-33
Intermediate (5K in 22:30): VDOT ≈ 45-48
Elite (5K in 16:00):       VDOT ≈ 67-70
```

### TSS/CTL/ATL/TSB (Training Load)
```bash
# Test Training Stress Score
cargo test test_tss -- --nocapture

# Test Chronic Training Load
cargo test test_ctl -- --nocapture

# Test Acute Training Load
cargo test test_atl -- --nocapture

# Test Training Stress Balance
cargo test test_tsb -- --nocapture
```

**Expected Values:**
```
Easy ride (IF=0.65, 60min):     TSS ≈ 40
Threshold (IF=1.00, 60min):     TSS = 100
VO2max interval (IF=1.15, 20min): TSS ≈ 44

Fresh athlete:   CTL=80, ATL=40 => TSB=+40
Fatigued:       CTL=70, ATL=100 => TSB=-30
```

### TRIMP (Training Impulse)
```bash
# Test TRIMP calculation
cargo test test_trimp -- --nocapture

# Test gender differences
cargo test test_trimp_gender -- --nocapture
```

**Expected Values:**
```
Male, 60min @ 75% HRmax:   TRIMP ≈ 90-110
Female, 60min @ 75% HRmax: TRIMP ≈ 80-95
```

### FTP (Functional Threshold Power)
```bash
# Test FTP estimation
cargo test test_ftp -- --nocapture

# Test 20-minute protocol
cargo test test_ftp_20min -- --nocapture

# Test 8-minute protocol
cargo test test_ftp_8min -- --nocapture

# Test ramp test
cargo test test_ftp_ramp -- --nocapture
```

**Expected Values:**
```
Beginner:     FTP ≈ 150W (20min test: 158W × 0.95)
Intermediate: FTP ≈ 250W (20min test: 263W × 0.95)
Elite:        FTP ≈ 380W (20min test: 400W × 0.95)
```

### VO2max (Aerobic Capacity)
```bash
# Test VO2max estimation
cargo test test_vo2max -- --nocapture

# Test Cooper 12-minute test
cargo test test_cooper_test -- --nocapture

# Test VDOT to VO2max conversion
cargo test test_vdot_to_vo2max -- --nocapture
```

**Expected Values:**
```
Beginner:     VO2max ≈ 35 ml/kg/min (Cooper: 1800m)
Intermediate: VO2max ≈ 49 ml/kg/min (Cooper: 2600m)
Elite:        VO2max ≈ 67 ml/kg/min (Cooper: 3400m)
```

### Recovery & Sleep
```bash
# Test recovery score calculation
cargo test test_recovery -- --nocapture

# Test sleep quality analysis
cargo test test_sleep_analysis -- --nocapture

# Test sleep stage scoring
cargo test test_sleep_stages -- --nocapture
```

**Expected Values:**
```
Well-rested: Recovery score > 70, Sleep quality > 80%
Adequate:    Recovery score 50-70, Sleep quality 60-80%
Poor:        Recovery score < 50, Sleep quality < 60%
```

### Nutrition
```bash
# Test BMR/TDEE calculation
cargo test test_nutrition -- --nocapture

# Test macronutrient distribution
cargo test test_macros -- --nocapture
```

**Expected Values:**
```
Adult male (70kg, 30yo):
  BMR ≈ 1700 kcal/day (Mifflin-St Jeor)
  TDEE (moderate activity) ≈ 2600 kcal/day
```

## Success Criteria
- ✅ All algorithm tests pass
- ✅ Results match published reference values (±5%)
- ✅ Edge cases handled gracefully (errors returned)
- ✅ Physiological bounds validated
- ✅ Algorithm variants configurable
- ✅ No panic on invalid inputs
- ✅ Calculations deterministic (same input = same output)
- ✅ Performance acceptable (< 10µs per calculation)

## Related Files
- `tests/intelligence_tools_basic_test.rs` - Basic algorithm tests
- `tests/intelligence_tools_advanced_test.rs` - Advanced scenarios
- `src/intelligence/algorithms/` - Algorithm implementations
- `src/intelligence/physiological_constants.rs` - Bounds and constants
- `book/src/intelligence-methodology.md` - Research documentation

## Related Skills
- `run-full-test-suite` - Full test execution
