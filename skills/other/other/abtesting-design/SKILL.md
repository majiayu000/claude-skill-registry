---
name: abtesting-design
cluster: abtesting
description: "Hypothesis formation, null/alternative, control/variant setup, randomization hash-based, stratification"
tags: ["experiment-design","hypothesis","randomization"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "ab test design hypothesis control variant randomization stratify"
---

# abtesting-design

## Purpose
This skill enables precise A/B test design for OpenClaw, covering hypothesis formulation (e.g., null and alternative), setup of control/variant groups, hash-based randomization, and stratification to ensure balanced experiments.

## When to Use
Use this skill when designing experiments for feature comparisons, such as testing website layouts, app features, or marketing campaigns, to validate hypotheses with statistical rigor and minimize bias.

## Key Capabilities
- Formulate hypotheses: Define null (e.g., "No difference in click rates") and alternative (e.g., "Variant increases clicks by 10%").
- Set up groups: Configure control and variant setups with parameters like sample sizes and metrics.
- Implement randomization: Use hash-based methods (e.g., SHA-256 on user IDs) for assignment to reduce selection bias.
- Apply stratification: Divide users into strata (e.g., by demographics) to balance groups, using algorithms like stratified sampling.

## Usage Patterns
Always start by defining your hypothesis and groups. Use CLI for quick designs or API for programmatic integration. Provide all required inputs (e.g., hypothesis strings, variant names) in a single command or request. For repeated use, store configurations in JSON files and reference them via flags. Validate inputs before execution to avoid runtime errors.

## Common Commands/API
- CLI Command: Run `openclaw abtesting-design --hypothesis-null "No effect on conversion" --hypothesis-alt "Variant increases conversion" --variants control,variantA --randomize hash --stratify age,gender` to design a test. Use `--config path/to/config.json` for JSON configs like {"variants": ["control", "variantA"], "strata": ["age", "gender"]}.
- API Endpoint: Send a POST request to `/api/abtesting/design` with a JSON body, e.g., {"hypothesis_null": "No difference", "hypothesis_alt": "Increase in engagement", "variants": ["control", "variantB"], "randomization": "hash", "stratification": ["device_type"]}. Set auth via header: `Authorization: Bearer $OPENCLAW_API_KEY`.
- Code Snippet (Python): 
  ```python
  import requests
  headers = {'Authorization': f'Bearer {os.environ["OPENCLAW_API_KEY"]}'}
  data = {"hypothesis_null": "No effect", "variants": ["control", "variant"]}
  response = requests.post('https://api.openclaw.com/api/abtesting/design', json=data, headers=headers)
  ```
- Code Snippet (CLI in Script): 
  ```bash
  export OPENCLAW_API_KEY=your_key_here
  openclaw abtesting-design --hypothesis-null "Baseline equal" --variants control,testVariant --output results.json
  ```

## Integration Notes
Integrate by setting `$OPENCLAW_API_KEY` as an environment variable for authentication. For multi-service setups, chain this skill with data tools (e.g., via OpenClaw's workflow API at `/api/workflows/add`). Use JSON configs for consistency, e.g., {"api_endpoint": "/api/abtesting/design", "auth_env": "OPENCLAW_API_KEY"}. Ensure your application handles asynchronous responses by polling `/api/abtesting/status/{job_id}`.

## Error Handling
Check for errors by parsing response codes: HTTP 400 for invalid inputs (e.g., missing hypothesis), 401 for auth failures. In code, use try-except blocks: 
```python
try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"Error: {e.response.status_code} - {e.response.text}")
    # Retry with corrected inputs, e.g., add missing fields
```
For CLI, capture output and check for strings like "Error: Invalid hypothesis format" then adjust flags accordingly.

## Concrete Usage Examples
1. **Email Subject Line Test**: To compare two email subjects, run `openclaw abtesting-design --hypothesis-null "Open rates are equal" --hypothesis-alt "Subject B increases opens" --variants control,subjectB --randomize hash --stratify location` then use the output JSON to assign users via their IDs in your email system.
2. **App Feature A/B Test**: For testing a new login button, use the API: Send POST to `/api/abtesting/design` with {"hypothesis_null": "No change in login time", "variants": ["old_button", "new_button"], "stratification": ["user_type"]} and apply the returned randomization function (e.g., hash-based) in your app code to segment users.

## Graph Relationships
- Related Cluster: abtesting (e.g., links to skills like abtesting-analysis for post-design steps).
- Related Tags: experiment-design (connects to data-collection skills), hypothesis (ties to statistical-modeling tools), randomization (integrates with user-segmentation utilities).
