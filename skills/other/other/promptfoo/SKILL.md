---
name: promptfoo
description: |
  Promptfoo evaluation framework for testing and comparing LLM outputs.
  Use when writing eval configs, creating test cases, debugging eval runs, or working with assertions.
allowed-tools:
  - Bash(npx promptfoo:*)
  - Bash(npm run evals:*)
  - WebFetch(domain:www.promptfoo.dev)
---

# Promptfoo

[Promptfoo](https://www.promptfoo.dev/) is a CLI tool for testing and comparing LLM outputs.

## Config File

The CLI auto-discovers `promptfooconfig.yaml` in the current directory. Use `-c path` for other locations.

Supported extensions: `.yaml`, `.json`, `.js`

## Configuration

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: "What this eval tests"

prompts:
  - file://prompt.txt
  - |
    Inline prompt with {{variable}} substitution

providers:
  - anthropic:messages:claude-sonnet-4-5-20250929

defaultTest:
  options:
    provider:
      config:
        temperature: 0.0
        max_tokens: 4096

tests:
  - description: "What this case tests"
    vars:
      variable: "value"
      from_file: file://data/input.txt
    assert:
      - type: contains
        value: "expected substring"

# Or load tests from files
tests: file://cases/all.yaml

outputPath: ./results.json

evaluateOptions:
  maxConcurrency: 4
```

## Provider IDs

| Model | ID |
|-------|----|
| Opus 4.5 | `anthropic:messages:claude-opus-4-5-20251101` |
| Sonnet 4.5 | `anthropic:messages:claude-sonnet-4-5-20250929` |
| Haiku 4.5 | `anthropic:messages:claude-haiku-4-5-20251001` |

Provider config: `temperature`, `max_tokens`, `top_p`, `top_k`, `tools`, `tool_choice`

## Prompts

- `file://path.txt` — load from file (path relative to config)
- Inline string with `{{variable}}` Nunjucks substitution
- Chat format via JSON: `[{"role": "system", "content": "..."}, {"role": "user", "content": "{{input}}"}]`

## Assertion Types

| Type | Use | Value |
|------|-----|-------|
| `contains` | Substring match | `"expected text"` |
| `icontains` | Case-insensitive substring | `"expected text"` |
| `equals` | Exact match | `"exact value"` |
| `regex` | Pattern match | `"\\d{4}-\\d{2}-\\d{2}"` |
| `is-json` | Valid JSON output | — |
| `contains-json` | Output contains JSON | — |
| `starts-with` | Prefix match | `"prefix"` |
| `cost` | Max cost | `threshold: 0.01` |
| `latency` | Max response time (ms) | `threshold: 5000` |
| `javascript` | Custom JS expression | `output.includes('x')` |
| `python` | Custom Python | `file://check.py:fn_name` |
| `llm-rubric` | LLM-as-judge | rubric text |
| `similar` | Semantic similarity | `value: "text"`, `threshold: 0.8` |
| `model-graded-factuality` | Fact checking | — |

Prefix any assertion with `not-` to negate (e.g., `not-contains`).

### llm-rubric

Uses an LLM to grade output against a rubric:

```yaml
assert:
  - type: llm-rubric
    value: |
      The response should:
      - Mention at least 3 factors
      - Include specific examples
    threshold: 0.7
    provider: anthropic:messages:claude-sonnet-4-5-20250929
```

### javascript

Inline expressions or functions. Access `output` (string) and `context` (with `vars`, `prompt`):

```yaml
assert:
  - type: javascript
    value: output.length > 100 && output.includes('route')
  - type: javascript
    value: |
      const data = JSON.parse(output);
      return data.calories >= 200 && data.calories <= 300;
```

## Test Organization

Split cases into separate files and reference them:

```yaml
tests:
  - file://cases/basic.yaml
  - file://cases/edge-cases.yaml
```

Each case file contains a YAML array of test objects.

## CLI

```bash
npx promptfoo eval                         # Run with auto-discovered config
npx promptfoo eval -c path/to/config.yaml  # Specific config
npx promptfoo eval --filter-metadata key=v # Filter tests
npx promptfoo view                         # Web UI for results
npx promptfoo cache clear                  # Clear result cache
```

## References

Consult the [configuration reference](https://www.promptfoo.dev/docs/configuration/reference/) and [Anthropic provider docs](https://www.promptfoo.dev/docs/providers/anthropic/) for full details.
