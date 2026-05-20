---
name: cs
cluster: computer-science
description: "Root CS: theoretical foundations, problem classification, complexity theory"
tags: ["computer-science","theory"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "computer science theory fundamentals complexity"
---

## Purpose
This skill enables OpenClaw to handle core computer science theory, focusing on theoretical foundations (e.g., Turing machines, automata), problem classification (e.g., P vs NP), and complexity theory (e.g., Big O analysis). It provides precise tools for reasoning about algorithms and computational limits.

## When to Use
Use this skill when tackling theoretical CS problems, such as verifying algorithm efficiency, classifying problem types (e.g., decidable vs undecidable), or optimizing code based on complexity metrics. Apply it during algorithm design, code reviews, or when debugging performance issues in theoretical contexts.

## Key Capabilities
- Analyze time and space complexity of code snippets using Big O notation.
- Classify problems as P, NP, NP-complete, or undecidable based on input descriptions.
- Generate explanations of CS fundamentals, like finite state machines or halting problems.
- Compare algorithm complexities, e.g., via asymptotic analysis.
- Handle edge cases in theory, such as reduction proofs for problem classification.

## Usage Patterns
To use this skill, invoke it via OpenClaw's CLI or API. Always provide inputs like code snippets or problem descriptions. For CLI, prefix commands with `openclaw cs`. For API, use HTTP requests to endpoints like `/api/cs/analyze`. Set the environment variable `$OPENCLAW_API_KEY` for authentication before any operation. Example pattern: Load the skill in your script, then call functions with required parameters, handling responses synchronously.

To analyze complexity:
1. Prepare a code snippet as a string.
2. Call the function with flags for output format (e.g., JSON).
3. Parse the response for Big O results.

For problem classification:
1. Describe the problem in a JSON object.
2. Use the classify command with relevant flags.
3. Validate the output against expected categories.

## Common Commands/API
- CLI Command: `openclaw cs analyze-complexity --code "def func(arr): for i in arr: print(i)" --output json`
  - Flags: `--code` for input code (required), `--output` for format (e.g., json, text).
  - Output: JSON like `{"big_o": "O(n)", "description": "Linear time complexity"}`.
- CLI Command: `openclaw cs classify-problem --description "Determine if a graph has a Hamiltonian path" --detail full`
  - Flags: `--description` for problem text, `--detail` for output depth (e.g., full for proofs).
  - Output: String like "NP-complete, reducible from TSP".
- API Endpoint: POST to `/api/cs/analyze` with body `{"code": "def func(...)", "type": "complexity"}`
  - Headers: Include `Authorization: Bearer $OPENCLAW_API_KEY`.
  - Response: JSON object, e.g., `{"status": "success", "big_o": "O(n^2)"}`.
- API Endpoint: GET `/api/cs/classify?query=traveling+salesman`
  - Query Params: `query` for problem description.
  - Config Format: Use JSON in request body, e.g., `{"query": "string", "options": {"depth": 1}}`.

Code Snippet Example 1 (Python):
```python
import openclaw
openclaw.set_api_key(os.environ['OPENCLAW_API_KEY'])
result = openclaw.cs.analyze_complexity(code="def sum_list(lst): return sum(lst)")
print(result['big_o'])  # Outputs: O(n)
```

Code Snippet Example 2 (Python):
```python
import openclaw
response = openclaw.cs.classify_problem(description="Shortest path in weighted graph")
print(response['classification'])  # Outputs: e.g., "P, solvable via Dijkstra"
```

## Integration Notes
Integrate this skill by importing the OpenClaw library in your code and calling CS-specific modules. For multi-skill workflows, chain outputs (e.g., use classification results in an algorithms skill). Configuration: Store settings in a `.openclawrc` file with format like `{"cs": {"default_output": "json", "api_endpoint": "/api/cs"}}`. Ensure `$OPENCLAW_API_KEY` is set in your environment. For asynchronous use, wrap API calls in try-except blocks and handle retries for rate limits.

## Error Handling
Check for errors like invalid inputs (e.g., malformed code) by parsing response codes: HTTP 400 for bad requests, 401 for auth failures. Use OpenClaw's error objects, e.g., in Python: `try: result = openclaw.cs.analyze_complexity(...) except openclaw.errors.InvalidInputError as e: print(e.message)  # e.g., "Code snippet must be a string"`. For CLI, errors return as stderr with codes (e.g., exit code 1 for failures). Always validate inputs before calling, and retry on transient errors like network issues with exponential backoff.

## Graph Relationships
- Related to: algorithms (for practical implementations), data-structures (for complexity interactions).
- Clusters with: computer-science (as root node), theory (for shared fundamentals).
- Dependencies: Requires core OpenClaw runtime; links to advanced topics like machine-learning for theoretical extensions.
