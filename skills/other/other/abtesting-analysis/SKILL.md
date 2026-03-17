---
name: abtesting-analysis
cluster: abtesting
description: "Results: uplift calculation, significance interpretation, long-run effects, Simpson\'s paradox, novelty effect"
tags: ["analysis","uplift","novelty-effect","decision"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "ab test results analysis uplift novelty effect segment decision simpson"
---

# abtesting-analysis

## Purpose
This skill enables detailed analysis of A/B test results, including uplift calculations, statistical significance interpretation, evaluation of long-run effects, detection of Simpson's paradox, and assessment of novelty effects to inform decisions.

## When to Use
Use this skill when processing A/B test data from experiments, such as website variants or app features, to quantify impacts like conversion rate differences. Apply it for data-driven decisions in marketing, product development, or UX testing, especially when segmenting users or checking for hidden biases.

## Key Capabilities
- Calculate uplift: Computes percentage lift in metrics (e.g., revenue) between control and variant groups.
- Interpret significance: Uses t-tests or chi-squared tests to determine p-values and confidence intervals.
- Analyze long-run effects: Models decay or persistence of effects over time using exponential smoothing.
- Detect Simpson's paradox: Identifies reversed trends across aggregated vs. segmented data.
- Assess novelty effect: Evaluates initial spikes in metrics that fade, via time-series comparison.

## Usage Patterns
Invoke this skill via CLI for quick analysis or integrate it into scripts for automated workflows. Always provide input data in JSON format, specifying metrics and segments. For example, pipe data from a file and output results to console or a file. Handle authentication by setting the environment variable `$OPENCLAW_API_KEY` before running commands.

Example 1: Analyze a basic A/B test for click-through rate.
```bash
openclaw abtesting analyze --input results.json --metric ctr --groups control variant
```
This command processes the JSON file, calculates uplift, and checks significance.

Example 2: Detect Simpson's paradox in segmented data.
```python
import os
os.environ['OPENCLAW_API_KEY'] = 'your_api_key_here'
response = requests.post('https://api.openclaw.ai/abtesting/analyze', json={'file': 'segments.json', 'check': 'simpson'})
print(response.json()['paradox_detected'])  # Outputs True or False
```
This script sends segmented data to the API and retrieves paradox insights.

## Common Commands/API
Use the CLI command `openclaw abtesting analyze` with these flags:
- `--input <file>`: Path to JSON input file (e.g., {"control": {"clicks": 1000, "conversions": 50}, "variant": {"clicks": 1200, "conversions": 72}})
- `--metric <string>`: Metric to analyze, like "conversions" or "revenue".
- `--significance`: Performs statistical tests; outputs p-value and CI.
- `--uplift`: Calculates relative uplift; e.g., outputs {"uplift": 0.15} for 15% lift.
- `--check-novelty`: Analyzes time-series for novelty; requires `--time-window 7d`.

API endpoint: POST to `https://api.openclaw.ai/abtesting/analyze` with JSON payload, e.g.:
```json
{
  "data": {"control": [...], "variant": [...]},
  "metric": "revenue",
  "options": {"significance": true, "simpson": true}
}
```
Response format: JSON object with keys like "uplift_value", "p_value", and "effects".

## Integration Notes
Integrate by importing the OpenClaw SDK in Python or using curl for API calls. Set `$OPENCLAW_API_KEY` as an environment variable for authentication. For config files, use YAML for advanced options, e.g.:
```yaml
analysis:
  metric: conversions
  segments: [age_group, region]
```
Ensure data is formatted as arrays of objects (e.g., [ {"user_id": 1, "group": "control", "value": 10} ]). Avoid rate limits by batching requests; use webhooks for asynchronous processing if analyzing large datasets.

## Error Handling
Check for common errors like invalid input formats (e.g., non-JSON files) by wrapping commands in try-catch blocks. If authentication fails, verify `$OPENCLAW_API_KEY` and handle with HTTP 401 errors. For API calls, catch exceptions for network issues or invalid responses:
```python
try:
    response = requests.post('https://api.openclaw.ai/abtesting/analyze', headers={'Authorization': f'Bearer {os.environ.get("OPENCLAW_API_KEY")}'})
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"Error: {e} - Check API key and input data")
```
Log errors with details like "Insufficient data points for significance" and retry with corrected inputs.

## Graph Relationships
- Related to cluster: abtesting (e.g., shares data models with other abtesting skills).
- Connected via tags: analysis (links to data processing skills), uplift (ties to metrics tools), novelty-effect (associates with behavioral analysis), decision (integrates with recommendation engines).
