---
name: vibe-fuzz-parser-inputs
description: Generates fuzz test scaffolding for parsers handling external input (YAML, JSON, config files, user input). Seeds corpus from existing fixtures and runs initial pass.
user-invocable: true
---

# vibe-fuzz-parser-inputs

Every parser will eventually see input you didn't expect. Fuzz testing finds the crashes before production does.

## When to Use This Skill

- Implementing any parser (YAML, JSON, XML, config, DSL)
- Processing user-supplied input
- Handling webhook payloads or API responses
- Parsing file formats

## When NOT to Use This Skill

- The parser is a well-tested standard library (e.g., `encoding/json`)
- You're only reading known, controlled input
- The parser is trivial (e.g., splitting a string by comma)

## Steps

### Go Fuzz Tests

1. **Create fuzz test file** (`parser_fuzz_test.go`):
   ```go
   func FuzzParseConfig(f *testing.F) {
       // Seed corpus from existing test fixtures
       files, _ := filepath.Glob("testdata/*.yaml")
       for _, file := range files {
           data, _ := os.ReadFile(file)
           f.Add(data)
       }

       // Add targeted seeds
       f.Add([]byte(""))           // empty
       f.Add([]byte("{}"))         // minimal valid
       f.Add([]byte("\x00\x00"))   // binary

       f.Fuzz(func(t *testing.T, data []byte) {
           // Should never panic
           result, err := ParseConfig(data)
           if err != nil {
               return // errors are fine
           }
           // If no error, result should be valid
           if result.Name == "" {
               t.Error("parsed successfully but Name is empty")
           }
       })
   }
   ```

2. **Seed the corpus** from:
   - Existing test fixtures
   - Real production examples
   - Known edge cases
   - Minimally valid inputs
   - Binary/garbage data

3. **Run initial fuzz**:
   ```bash
   go test -fuzz=FuzzParseConfig -fuzztime=30s
   ```

4. **Record results**:
   - Crashes found
   - New corpus entries generated
   - Edge cases discovered

5. **Fix crashes** -- Every panic or unexpected behavior becomes a permanent test case

### Other Languages

- **JavaScript/TypeScript**: Use `jest-fuzz` or `fast-check` property-based testing
- **Python**: Use `hypothesis` for property-based testing
- **Rust**: Use `cargo-fuzz` with `libfuzzer`

## Output Format

### Fuzz Test: [Parser Name]

**Seeds**: X (Y from fixtures, Z manual)
**Duration**: [fuzz time]
**Corpus growth**: X -> Y entries (Z% expansion)
**Crashes found**: N

| # | Input (hex) | Crash Type | Fix |
|---|-------------|-----------|-----|
| 1 | `\x00\xff...` | nil panic in tokenizer | Added nil check at line 42 |

### New Edge Cases Discovered
1. [Description] -- added as permanent test case
