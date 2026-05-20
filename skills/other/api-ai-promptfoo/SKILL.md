---
name: api-ai-promptfoo
description: Testing and evaluation framework for LLM prompts and applications -- promptfooconfig.yaml, assertions, model-graded evals, red teaming, CI/CD integration, custom providers, and comparative evaluation
---

# Promptfoo Patterns

> **Quick Guide:** Use promptfoo for systematic LLM evaluation. Define prompts, providers, and test cases in `promptfooconfig.yaml`. Use assertion types (`contains`, `is-json`, `llm-rubric`, `similar`, `cost`, `latency`) to validate outputs. Use `promptfoo eval` to run, `promptfoo view` for results UI. Use model-graded assertions (`llm-rubric`, `factuality`) for subjective quality. Use `promptfoo redteam run` for security scanning. Use `--share` flag or `promptfoo share` to share results. All provider API keys come from environment variables -- never hardcode them.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define test cases with explicit `assert` arrays -- tests without assertions only capture output without validating it)**

**(You MUST use `llm-rubric` for subjective quality evaluation -- do NOT rely solely on deterministic assertions for natural language output)**

**(You MUST set `threshold` on similarity and model-graded assertions -- omitting thresholds uses defaults that may not match your quality bar)**

**(You MUST use environment variables for all API keys -- never hardcode keys in promptfooconfig.yaml or provider configs)**

**(You MUST run `promptfoo eval --fail-on-error` in CI pipelines -- bare `promptfoo eval` exits 0 even when assertions fail)**

</critical_requirements>

---

**Auto-detection:** promptfoo, promptfooconfig, promptfooconfig.yaml, promptfoo eval, promptfoo view, promptfoo redteam, llm-rubric, model-graded-closedqa, promptfoo share, promptfoo cache, assertion type, LLM evaluation, prompt testing, red teaming, PROMPTFOO_CONFIG

**When to use:**

- Writing or evaluating LLM prompts across one or more providers
- Setting up automated test suites for LLM-powered features
- Comparing model outputs side-by-side (GPT vs Claude vs Gemini)
- Running model-graded evaluations (LLM-as-a-judge)
- Red teaming LLM applications for security vulnerabilities
- Integrating LLM quality gates into CI/CD pipelines
- Validating structured output (JSON, function calls) from LLMs

**Key patterns covered:**

- `promptfooconfig.yaml` structure (prompts, providers, tests, defaultTest)
- Assertion types (deterministic, model-graded, performance)
- Custom TypeScript providers
- Red teaming configuration (plugins, strategies)
- CI/CD integration with GitHub Actions
- Programmatic API (`evaluate()` function)
- Result sharing and caching

**When NOT to use:**

- Unit testing application code (use your test runner)
- Load testing / benchmarking API throughput (use k6, Artillery, etc.)
- Runtime monitoring of production LLM calls (use observability tooling)

---

## Examples Index

- [Core: Config & Assertions](examples/core.md) -- promptfooconfig.yaml structure, providers, prompts, test cases, assertion types
- [Model-Graded & Advanced Assertions](examples/model-graded.md) -- llm-rubric, factuality, similar, context evaluation, custom assertions
- [Red Teaming](examples/red-teaming.md) -- Security scanning, plugins, strategies, presets
- [Custom Providers & Programmatic API](examples/custom-providers.md) -- TypeScript providers, evaluate() function, CI/CD integration
- [Quick API Reference](reference.md) -- CLI commands, assertion type table, provider IDs, red team plugins

---

<philosophy>

## Philosophy

Promptfoo brings **test-driven development to LLM applications**. Instead of manually checking outputs, you define expected behaviors as assertions and run them systematically across prompts and providers.

**Core principles:**

1. **Declarative test definitions** -- YAML config over imperative test scripts. Define prompts, providers, test cases, and assertions in `promptfooconfig.yaml`. No code required for standard evaluations.
2. **Assertion-driven validation** -- Every test case should have assertions. Deterministic assertions (`contains`, `is-json`, `equals`) for structured output; model-graded assertions (`llm-rubric`, `factuality`) for subjective quality.
3. **Comparative evaluation** -- Run the same tests across multiple providers or prompt variants simultaneously. The results matrix shows which combination performs best.
4. **Shift-left LLM testing** -- Catch prompt regressions in CI before they reach production. Use `--fail-on-error` for quality gates.
5. **Red teaming as a first-class concern** -- Security scanning for prompt injection, PII leakage, harmful content, and jailbreak vulnerabilities is built in, not bolted on.

**When to use promptfoo:**

- Developing or iterating on LLM prompts
- Comparing providers or models for a specific task
- Validating that prompt changes don't cause regressions
- Security-scanning LLM applications before deployment
- Running model-graded evaluations at scale

**When NOT to use:**

- Unit testing non-LLM code (use Vitest, Jest, etc.)
- Real-time production monitoring (use observability tools)
- Load testing API endpoints (use k6, Artillery)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic Configuration

Every promptfoo project starts with `promptfooconfig.yaml`. Three required sections: `prompts`, `providers`, `tests`.

```yaml
# promptfooconfig.yaml
description: "Translation quality evaluation"

prompts:
  - "Convert the following to {{language}}: {{input}}"

providers:
  - openai:gpt-4o
  - anthropic:messages:claude-sonnet-4-6

tests:
  - vars:
      language: French
      input: Hello world
    assert:
      - type: icontains
        value: "bonjour"
      - type: llm-rubric
        value: "Output is a natural French translation, not word-for-word"
```

**Why good:** Declarative config, multi-provider comparison, both deterministic and model-graded assertions

```yaml
# BAD: Tests without assertions
tests:
  - vars:
      language: French
      input: Hello world
  # No assert array -- output is captured but never validated
```

**Why bad:** Tests without assertions only log output, they never fail -- you lose the entire point of automated evaluation

**See:** [examples/core.md](examples/core.md) for prompts from files, provider config, defaultTest, variable loading from CSV

---

### Pattern 2: Deterministic Assertions

Use for outputs with predictable, verifiable structure.

```yaml
assert:
  # String matching
  - type: contains
    value: "error"
  - type: icontains # case-insensitive
    value: "success"
  - type: not-contains
    value: "internal server error"
  - type: starts-with
    value: "{"
  - type: regex
    value: "\\d{4}-\\d{2}-\\d{2}" # date pattern

  # Structured output
  - type: is-json
  - type: contains-json
  - type: is-valid-openai-tools-call

  # Performance
  - type: cost
    threshold: 0.01 # max $0.01 per call
  - type: latency
    threshold: 5000 # max 5 seconds
```

**Why good:** Fast, deterministic, no LLM cost for evaluation, catches structural regressions immediately

```yaml
# BAD: Using llm-rubric for JSON validation
assert:
  - type: llm-rubric
    value: "Output must be valid JSON"
```

**Why bad:** Expensive (requires LLM call), slower, non-deterministic -- `is-json` does this deterministically for free

**See:** [examples/core.md](examples/core.md) for all deterministic assertion types with examples

---

### Pattern 3: Model-Graded Assertions

Use for subjective quality where deterministic checks cannot capture intent.

```yaml
assert:
  - type: llm-rubric
    value: "Response is helpful, accurate, and conversational in tone"
    provider: openai:gpt-4o

  - type: factuality
    value: "The capital of France is Paris. It has a population of ~2.1 million."
    provider: openai:gpt-4o

  - type: similar
    value: "The weather in Paris is sunny today"
    threshold: 0.8

  - type: model-graded-closedqa
    value: "Paris is the capital of France"
    provider: openai:gpt-4o
```

**Why good:** Evaluates subjective quality that deterministic assertions cannot capture, configurable grading provider

```yaml
# BAD: No threshold on similar assertion
assert:
  - type: similar
    value: "expected output"
    # Missing threshold -- uses default which may be too lenient or strict
```

**Why bad:** Default similarity threshold may not match your quality bar, always set it explicitly

**See:** [examples/model-graded.md](examples/model-graded.md) for llm-rubric with custom providers, context evaluation, factuality, custom grading prompts

---

### Pattern 4: Red Teaming

Use `redteam` section to scan for security vulnerabilities.

```yaml
# promptfooconfig.yaml
targets:
  - openai:gpt-4o

redteam:
  purpose: "Customer support chatbot for an e-commerce platform"
  numTests: 10
  plugins:
    - harmful
    - pii
    - contracts
    - hallucination
    - prompt-extraction
  strategies:
    - jailbreak
    - prompt-injection
```

**Why good:** Declarative security scanning, purpose provides context for realistic attacks, composable plugins and strategies

```yaml
# BAD: Red team without purpose
redteam:
  plugins:
    - harmful
  # Missing purpose -- attacks will be generic and less effective
```

**Why bad:** Without `purpose`, the red team generator creates generic attacks that miss application-specific vulnerabilities

**See:** [examples/red-teaming.md](examples/red-teaming.md) for presets (OWASP, NIST), advanced strategies, multi-turn attacks

---

### Pattern 5: Custom TypeScript Provider

Use when your LLM integration is not a direct API call (RAG pipelines, agent chains, custom middleware).

```typescript
// providers/my-app.ts
import type {
  ApiProvider,
  ProviderOptions,
  ProviderResponse,
  CallApiContextParams,
} from "promptfoo";

// NOTE: default export required by promptfoo's file:// provider loader
export default class MyAppProvider implements ApiProvider {
  private config: Record<string, unknown>;

  constructor(options: ProviderOptions) {
    this.config = options.config || {};
  }

  id(): string {
    return "my-app-provider";
  }

  async callApi(
    prompt: string,
    context?: CallApiContextParams,
  ): Promise<ProviderResponse> {
    // Call your application's LLM pipeline
    const result = await myApp.processQuery(prompt);

    return {
      output: result.answer,
      tokenUsage: {
        total: result.totalTokens,
        prompt: result.promptTokens,
        completion: result.completionTokens,
      },
      cost: result.cost,
    };
  }
}
```

```yaml
# promptfooconfig.yaml
providers:
  - file://providers/my-app.ts
```

**Why good:** Type-safe, full control over LLM pipeline, reports token usage and cost for assertions

**See:** [examples/custom-providers.md](examples/custom-providers.md) for inline function providers, programmatic API, CI/CD integration

---

### Pattern 6: CI/CD Integration

Run evaluations in CI with quality gates.

```yaml
# .github/workflows/llm-eval.yml
name: LLM Eval
on:
  pull_request:
    paths:
      - "prompts/**"
      - "promptfooconfig.yaml"
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - uses: actions/cache@v4
        with:
          path: ~/.cache/promptfoo
          key: ${{ runner.os }}-promptfoo-v1
      - name: Run eval
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: npx promptfoo@latest eval --fail-on-error -o results.json --share
```

**Why good:** Caches LLM responses across runs, `--fail-on-error` fails the CI job on assertion failures, `--share` generates a shareable results URL

```bash
# BAD: CI without --fail-on-error
npx promptfoo eval -c promptfooconfig.yaml
# Always exits 0 -- CI never fails even with broken assertions
```

**Why bad:** Without `--fail-on-error`, promptfoo eval exits 0 regardless of assertion results, making the CI check meaningless

**See:** [examples/custom-providers.md](examples/custom-providers.md) for npm scripts, quality gate thresholds, programmatic evaluation

</patterns>

---

<decision_framework>

## Decision Framework

### Which Assertion Type to Use

```
What are you validating?
+-- Exact or structural match?
|   +-- Exact text -> equals
|   +-- Contains substring -> contains / icontains
|   +-- Regex pattern -> regex
|   +-- Valid JSON -> is-json
|   +-- Valid function call -> is-valid-openai-tools-call
|   +-- Cost under budget -> cost (with threshold)
|   +-- Response time -> latency (with threshold)
+-- Subjective quality?
|   +-- General quality criteria -> llm-rubric
|   +-- Factual accuracy against ground truth -> factuality
|   +-- Semantic similarity -> similar (with threshold)
|   +-- Closed-domain QA accuracy -> model-graded-closedqa
|   +-- RAG context fidelity -> context-faithfulness
+-- Custom logic?
    +-- JavaScript function -> javascript
    +-- Python function -> python
    +-- External service -> webhook
```

### When to Use Red Teaming vs Eval

```
What are you testing?
+-- Prompt quality and correctness?
|   +-- Use promptfoo eval with test cases and assertions
+-- Security vulnerabilities?
|   +-- Use promptfoo redteam run with plugins and strategies
+-- Both?
    +-- Run eval for quality, redteam for security -- separate configs or sections
```

### Provider Selection

```
How does your LLM integration work?
+-- Direct API call to OpenAI/Anthropic/etc?
|   +-- Use built-in provider: openai:gpt-4o, anthropic:messages:claude-sonnet-4-6
+-- Custom pipeline (RAG, agents, middleware)?
|   +-- Use custom TypeScript provider: file://providers/my-app.ts
+-- HTTP endpoint?
|   +-- Use HTTP provider: id: https://api.example.com/chat
+-- Multiple providers to compare?
    +-- List all in providers array -- promptfoo runs tests against each
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Tests without `assert` arrays (output is captured but never validated -- tests always "pass")
- Missing `--fail-on-error` in CI (promptfoo eval exits 0 even when assertions fail)
- Hardcoded API keys in `promptfooconfig.yaml` (use environment variables)
- Using `llm-rubric` for checks that `is-json` or `contains` can do deterministically (wastes money and adds non-determinism)
- Red teaming without `purpose` (generic attacks miss application-specific vulnerabilities)

**Medium Priority Issues:**

- Missing `threshold` on `similar` assertions (default may not match your quality bar)
- Not caching in CI (every run makes full API calls -- expensive and slow)
- Using `model-graded-closedqa` when `llm-rubric` would be simpler (closedqa is for specific ground-truth QA)
- Not setting `provider` on model-graded assertions (uses default which may not be the grader you want)
- Running red team with default `numTests: 5` in production scans (too few for comprehensive coverage)

**Common Mistakes:**

- Confusing `prompts` (the LLM prompt templates) with `tests` (the evaluation cases) -- prompts define what to send, tests define what to check
- Using `equals` for natural language output (LLM output is non-deterministic, use `llm-rubric` or `similar`)
- Forgetting `{{variable}}` syntax in prompts (promptfoo uses Nunjucks templating, not `${variable}`)
- Putting assertions in `defaultTest` that should only apply to specific tests (assertions in `defaultTest` apply to ALL tests)
- Using `file://` paths without the prefix (promptfoo treats bare paths as literal strings, not file references)

**Gotchas & Edge Cases:**

- `promptfoo eval` caches LLM responses by default -- use `promptfoo cache clear` or `--no-cache` to force fresh calls
- `--share` uploads results to promptfoo's servers -- do not use with sensitive data unless self-hosting
- Red team `strategies` wrap `plugins` output -- a plugin generates the malicious content, a strategy delivers it (e.g., via jailbreak encoding)
- `defaultTest.assert` merges with per-test assertions, it does not replace them -- both arrays run
- CSV test files map column headers to variable names -- header `input` becomes `{{input}}` in prompts
- `transform` in test options runs JavaScript on the output before assertions -- useful for extracting JSON from markdown-wrapped responses
- Provider configs in YAML use `config:` key for model parameters (`temperature`, `max_tokens`), not top-level fields
- The `weight` property on assertions affects scoring in the results UI but does not change pass/fail behavior

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define test cases with explicit `assert` arrays -- tests without assertions only capture output without validating it)**

**(You MUST use `llm-rubric` for subjective quality evaluation -- do NOT rely solely on deterministic assertions for natural language output)**

**(You MUST set `threshold` on similarity and model-graded assertions -- omitting thresholds uses defaults that may not match your quality bar)**

**(You MUST use environment variables for all API keys -- never hardcode keys in promptfooconfig.yaml or provider configs)**

**(You MUST run `promptfoo eval --fail-on-error` in CI pipelines -- bare `promptfoo eval` exits 0 even when assertions fail)**

**Failure to follow these rules will produce untested, insecure, or falsely-passing LLM evaluation pipelines.**

</critical_reminders>
