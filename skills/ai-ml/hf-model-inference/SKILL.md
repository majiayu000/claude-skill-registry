---
name: hf-model-inference
description: Guidance for deploying HuggingFace models as inference APIs/services. This skill applies when tasks involve downloading pre-trained models from HuggingFace Hub, creating REST APIs for model inference, building Flask/FastAPI services around ML models, or setting up sentiment analysis, text classification, or other NLP inference endpoints.
---

# HuggingFace Model Inference

## Overview

This skill provides guidance for deploying HuggingFace Transformers models as inference services. Common use cases include creating REST APIs for sentiment analysis, text classification, named entity recognition, and other NLP tasks using pre-trained models from the HuggingFace Hub.

## Workflow

### Phase 1: Environment Setup

1. **Create project directory structure**
   - Establish a dedicated directory for the inference service
   - Plan for model storage (models can be large, ensure adequate disk space)

2. **Install dependencies**
   - Core packages: `transformers`, `torch` (or `tensorflow`), `flask`/`fastapi`
   - Check package manager availability (`pip`, `uv`, `conda`) before installing
   - Example: `pip install transformers torch flask`

3. **Download the model**
   - Use `transformers` library to download and cache the model
   - Consider downloading during service startup vs. as a separate step
   - Verify model download completed successfully before proceeding

### Phase 2: API Implementation

1. **Choose the inference approach**
   - **Pipeline API** (simpler): `pipeline("sentiment-analysis", model="model-name")`
   - **Direct model loading** (more control): `AutoModelForSequenceClassification.from_pretrained()`
   - Document the choice rationale

2. **Implement the Flask/FastAPI service**
   - Define clear endpoint routes (e.g., `/sentiment`, `/classify`)
   - Implement proper request parsing and validation
   - Return structured JSON responses with consistent format

3. **Critical: Verify file completeness after writing**
   - Always read back written files to confirm content integrity
   - Check that all functions and error handlers are complete
   - Look for truncation indicators (incomplete strings, missing closing braces)

### Phase 3: Error Handling

Implement handlers for these cases:

| Error Case | HTTP Status | Response Format |
|------------|-------------|-----------------|
| Missing required field | 400 | `{"error": "description"}` |
| Empty input text | 400 | `{"error": "text cannot be empty"}` |
| Invalid JSON | 400 | `{"error": "invalid JSON"}` |
| Wrong HTTP method | 405 | Method not allowed |
| Internal model error | 500 | `{"error": "inference failed"}` |

### Phase 4: Testing and Verification

**Test all response aspects systematically:**

```bash
# Test with verbose output including status code
curl -w "\nHTTP Status: %{http_code}\n" -X POST http://localhost:5000/endpoint \
  -H "Content-Type: application/json" \
  -d '{"text": "test input"}'
```

**Required test cases:**
- Valid positive input
- Valid negative input
- Missing required fields
- Empty string input
- Invalid JSON body
- Wrong HTTP method
- Large input text

**Verification checklist:**
- [ ] HTTP status codes are correct (not just response body)
- [ ] Response JSON structure matches specification
- [ ] All error cases return appropriate messages
- [ ] Service handles concurrent requests

### Phase 5: Cleanup

- Remove temporary scripts (e.g., model download scripts)
- Verify no sensitive data in committed files
- Document the service endpoints and usage

## Common Pitfalls

### 1. File Write Truncation
**Problem**: File content may be truncated during write operations without obvious errors.
**Prevention**: Always read back written files immediately after creation to verify completeness.

### 2. Incomplete Error Testing
**Problem**: Testing only the "happy path" without verifying error handling.
**Prevention**: Use curl with `-w "%{http_code}"` to explicitly verify HTTP status codes, not just response bodies.

### 3. Premature Success Declaration
**Problem**: Declaring task complete after tests pass without verifying implementation details.
**Prevention**: Review actual file contents and test edge cases before marking complete.

### 4. Leftover Artifacts
**Problem**: Temporary scripts and files remain after task completion.
**Prevention**: Track created files and clean up helper scripts that are no longer needed.

### 5. Missing Input Validation
**Problem**: Not handling empty strings, whitespace-only input, or non-string values.
**Prevention**: Implement validation for all input edge cases:
```python
if not isinstance(text, str):
    return jsonify({"error": "'text' must be a string"}), 400
if not text.strip():
    return jsonify({"error": "'text' cannot be empty"}), 400
```

## Efficient Workflow Practices

- **Batch related operations**: Combine multiple test requests into a test script rather than running individually
- **Download models inline**: Consider downloading models within the service startup rather than separate scripts
- **Minimize state updates**: Update task tracking at meaningful milestones, not after every small action

## Response Format Reference

Standard inference response structure:

```json
{
  "label": "POSITIVE",
  "score": 0.9876
}
```

Standard error response structure:

```json
{
  "error": "descriptive error message"
}
```

## Resources

See `references/` for additional guidance on:
- HuggingFace model selection and loading patterns
- Flask/FastAPI best practices for ML services
- Testing strategies for inference endpoints
