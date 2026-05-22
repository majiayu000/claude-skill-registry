---
name: vibe-golden-file-testing
description: Implements snapshot/golden file tests with temporal normalization so tests don't break daily. Use when implementing tests that compare output against expected snapshots.
user-invocable: true
---

# vibe-golden-file-testing

Golden file tests are powerful but brittle. This skill makes them robust.

## When to Use This Skill

- Implementing tests that compare output against saved expected output
- Tests that currently break because dates, timestamps, or IDs change
- API response testing with dynamic fields
- CLI output testing

## When NOT to Use This Skill

- Simple unit tests with static assertions
- Tests where the exact output IS the requirement (byte-for-byte)
- Performance benchmarks

## The Problem

Golden tests break when they contain:
- Dates/timestamps (`2026-02-28` → different tomorrow)
- UUIDs/IDs (random each run)
- Hostnames/ports (different per environment)
- File paths (absolute paths differ per machine)
- Durations (`took 1.23s` → varies by machine)

## Steps

1. **Identify dynamic fields** in the output being tested

2. **Create normalizer function**:
   ```
   func normalizeOutput(s string) string {
       // Dates: 2026-02-28 → REDACTED_DATE
       s = dateRegex.ReplaceAll(s, "REDACTED_DATE")
       // UUIDs: 550e8400-... → REDACTED_UUID
       s = uuidRegex.ReplaceAll(s, "REDACTED_UUID")
       // Timestamps: 1709136000 → REDACTED_TS
       s = tsRegex.ReplaceAll(s, "REDACTED_TS")
       // Durations: 1.23s → REDACTED_DURATION
       s = durationRegex.ReplaceAll(s, "REDACTED_DURATION")
       return s
   }
   ```

3. **Apply normalization** to BOTH:
   - The actual output (at test time)
   - The golden file (at generation time)

4. **Generate golden file** with update flag:
   ```
   if os.Getenv("UPDATE_GOLDEN") == "1" {
       os.WriteFile(goldenPath, normalized, 0644)
   }
   ```

5. **Document update command**:
   ```
   # To update golden files:
   UPDATE_GOLDEN=1 go test ./...
   ```

## Common Normalizations

| Pattern | Regex | Replacement |
|---------|-------|-------------|
| ISO Date | `\d{4}-\d{2}-\d{2}` | REDACTED_DATE |
| ISO DateTime | `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}` | REDACTED_DATETIME |
| UUID | `[0-9a-f]{8}-[0-9a-f]{4}-...` | REDACTED_UUID |
| Unix timestamp | `\b1[6-9]\d{8}\b` | REDACTED_TS |
| Duration | `\d+\.?\d*[µnm]?s` | REDACTED_DURATION |
| Absolute path | `/home/\w+/` or `C:\\Users\\` | REDACTED_PATH |
| Port | `:\d{4,5}\b` | :REDACTED_PORT |

## Output Format

### Golden File Setup: [Test Name]

**Dynamic fields found**: X
**Normalizations applied**: Y
**Golden file**: [path]
**Update command**: `UPDATE_GOLDEN=1 [test command]`
