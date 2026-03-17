---
name: Model Manager
description: Test, validate, and add new AI models to the eval suite. Use when user asks to add new models, test model access, check pricing, or update models.yml.
---

# Model Manager

Test API access, validate configurations, and add new AI models to the AILANG eval suite.

## Quick Start

**Most common usage:**
```bash
# User says: "Can we add GPT-5.1 to the eval suite?"
# This skill will:
# 1. Test API access to GPT-5.1
# 2. Find the correct API model name
# 3. Look up pricing information
# 4. Update models.yml configuration
# 5. Run a test benchmark to verify
```

## When to Use This Skill

Invoke this skill when:
- User asks to "add a new model" to eval suite
- User mentions checking if a model is "accessible" or "available"
- User wants to "test API access" to a model
- User asks to "update models.yml" or "check pricing"
- User says "can we use [model name]?" for evaluations

## Available Scripts

### `scripts/test_model_access.sh <provider> <model-name>`
Test API access to a model and display authentication status.

**Usage:**
```bash
# Test OpenAI model
scripts/test_model_access.sh openai gpt-5.1

# Test Anthropic model
scripts/test_model_access.sh anthropic claude-sonnet-4-5-20250929

# Test Google Gemini via Vertex AI
scripts/test_model_access.sh google gemini-3-pro-preview-11-2025
```

**Output:**
```
Testing: openai/gpt-5.1
✓ OPENAI_API_KEY found
✓ API call successful
✓ Model: gpt-5.1-2025-11-13
✓ Tokens: 13 input, 10 output (10 reasoning)
Ready to add to models.yml
```

### `scripts/find_model_info.sh <model-keywords>`
Search for model information using web search and return API names + pricing.

**Usage:**
```bash
# Find GPT-5.1 info
scripts/find_model_info.sh "GPT-5.1 API model name pricing"

# Find Gemini 3 Pro info
scripts/find_model_info.sh "Gemini 3 Pro API documentation"
```

**Output:**
```
Searching for: GPT-5.1 API model name pricing
✓ Found API names:
  - gpt-5.1 (Thinking mode)
  - gpt-5.1-chat-latest (Instant mode)
✓ Pricing:
  Input: $1.25 per 1M tokens
  Output: $10.00 per 1M tokens
  Cached: $0.125 per 1M tokens
```

### `scripts/update_models_yml.sh <friendly-name> <api-name> <provider> <input-price> <output-price>`
Add a new model to models.yml configuration.

**Usage:**
```bash
# Add GPT-5.1
scripts/update_models_yml.sh \
  gpt5-1 \
  "gpt-5.1" \
  openai \
  0.00125 \
  0.01
```

**Output:**
```
Adding model to models.yml:
  Friendly name: gpt5-1
  API name: gpt-5.1
  Provider: openai
  Pricing: $0.00125 / $0.01 per 1K tokens

✓ Updated models.yml
✓ Validated YAML syntax
✓ Ready to test
```

### `scripts/verify_vertex_model.sh <model-name>`
Check if a Gemini model is available in Vertex AI.

**Usage:**
```bash
# Check if Gemini 3 Pro is available
scripts/verify_vertex_model.sh gemini-3-pro-preview-11-2025
```

**Output:**
```
Checking Vertex AI for: gemini-3-pro-preview-11-2025
✓ GCP project: multivac-internal-prod
✓ Access token obtained
✗ Model not found (404)
Recommendation: Monitor for availability, check again in 1-2 weeks
```

### `scripts/run_test_benchmark.sh <model-name>`
Run a small test benchmark to verify model works end-to-end.

**Usage:**
```bash
# Test GPT-5.1 with fizzbuzz benchmark
scripts/run_test_benchmark.sh gpt5-1
```

**Output:**
```
Running test benchmark: fizzbuzz
Model: gpt5-1
✓ Benchmark completed
✓ Result: PASS (100%)
✓ Tokens: 245 input, 89 output
✓ Cost: $0.002
Model is ready for production use
```

## Workflow

### 1. Test API Access

**First, verify you can call the model:**

```bash
# Use test_model_access.sh
scripts/test_model_access.sh openai gpt-5.1
```

**What to check:**
- API key is set (OPENAI_API_KEY, ANTHROPIC_API_KEY, or gcloud auth)
- API call succeeds (not 401/403/404)
- Model returns expected structure
- Token usage is reported

**For Gemini models:**
- Uses Vertex AI (not public API)
- Requires `gcloud auth application-default login`
- Check availability with `verify_vertex_model.sh`

### 2. Find Model Information

**Search for official documentation:**

```bash
# Find API model name and pricing
scripts/find_model_info.sh "GPT-5.1 API documentation pricing"
```

**What to gather:**
- Exact API model name (e.g., `gpt-5.1` not `GPT-5.1`)
- Provider (openai, anthropic, google)
- Input price per 1K tokens
- Output price per 1K tokens
- Context limits (if relevant)
- Special features (adaptive reasoning, caching, etc.)

**Reference:** See [resources/provider_endpoints.md](resources/provider_endpoints.md)

### 3. Update models.yml

**Add the model configuration:**

```bash
# Add to models.yml
scripts/update_models_yml.sh \
  <friendly-name> \
  <api-name> \
  <provider> \
  <input-per-1k> \
  <output-per-1k>
```

**Naming conventions:**
- Friendly name: `gpt5-1`, `claude-sonnet-4-5`, `gemini-3-pro`
- API name: Exact string for API calls
- Use hyphens, lowercase

**Also update:**
- Model suites (`benchmark_suite`, `extended_suite`, `dev_models`)
- Add notes about special features
- Document agent CLI support (if available)

### 4. Run Test Benchmark

**Verify end-to-end:**

```bash
# Test with a simple benchmark
scripts/run_test_benchmark.sh <model-name>
```

**What to verify:**
- Benchmark completes successfully
- Results are reasonable (not garbage output)
- Token usage matches expectations
- Cost calculation works
- No errors in logs

### 5. Document the Model

**Update relevant documentation:**
- Add model to this skill's resource guide
- Note any special parameters (e.g., `max_completion_tokens` for GPT-5.1)
- Document authentication requirements
- Add to teaching prompts if needed

### 6. Optional: Run Full Eval

**If model looks good:**

```bash
# Run small eval suite
ailang eval-suite --models <model-name> --benchmarks fizzbuzz,recursion_factorial

# Run full suite (expensive!)
make eval-baseline EVAL_VERSION=vX.Y.Z FULL=true
```

## Resources

### Provider Endpoints
See [resources/provider_endpoints.md](resources/provider_endpoints.md) for:
- API endpoint URLs for each provider
- Authentication methods
- How to test access manually
- Common errors and fixes

### Pricing Guide
See [resources/pricing_guide.md](resources/pricing_guide.md) for:
- How to find official pricing
- Price conversion (per 1M → per 1K)
- Cost calculation verification
- Caching and discounts

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (workflow and script descriptions)
2. **Execute as needed**: Scripts in `scripts/` (testing, updating, verification)
3. **Load on demand**: Resources (detailed endpoint docs, pricing references)

## Notes

**Important:**
- Always test API access BEFORE updating models.yml
- Vertex AI (Gemini) requires gcloud auth, not API key
- GPT-5.1+ uses `max_completion_tokens` instead of `max_tokens`
- New models may not be available in all regions immediately
- Check for preview/beta status before adding to production suites

**Prerequisites:**
- API keys set in environment (OPENAI_API_KEY, ANTHROPIC_API_KEY)
- For Gemini: `gcloud` CLI installed and authenticated
- For Gemini: GCP project set (`gcloud config set project PROJECT_ID`)
- `curl`, `python3`, and `jq` available in PATH

**Files modified by this skill:**
- `internal/eval_harness/models.yml` - Model configurations
- (Optional) `prompts/vX.Y.Z.md` - Teaching prompts
- (Optional) `.claude/skills/model-manager/resources/` - Local model database
