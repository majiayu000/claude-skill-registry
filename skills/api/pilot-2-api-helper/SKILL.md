---
name: api-integration-helper
description: Generate boilerplate code for REST API integrations with authentication, error handling, and retry logic
author: pilot-test
---

# API Integration Helper

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Generate production-ready code for integrating with REST APIs.

## Overview

This skill helps developers quickly set up REST API integrations by generating boilerplate code that handles authentication, HTTP requests, response parsing, error handling, and retries. Supports JavaScript and Python.

## When to Use

Use this skill when you need to integrate with a third-party REST API and want to generate the initial setup code rather than writing it from scratch.

## Instructions

### Step 1: Gather API Requirements

Ask the user for API details: base URL, authentication method, and target language.

### Step 2: Set Up Authentication

Generate authentication code based on the method (API key or OAuth).

For API key authentication:
```javascript
// JavaScript
const headers = {
  'Authorization': `Bearer ${process.env.API_KEY}`
};
```

```python
# Python
import os
headers = {
    'Authorization': f'Bearer {os.environ["API_KEY"]}'
}
```

### Step 3: Create HTTP Request Function

Generate a function to make HTTP requests with error handling.

```javascript
async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: headers,
    ...options
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return await response.json();
}
```

### Step 4: Add Retry Logic

Implement exponential backoff for failed requests.

```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000);
    }
  }
}
```

### Step 5: Handle Rate Limiting

Add rate limit detection and backoff.

```javascript
if (response.status === 429) {
  const retryAfter = response.headers.get('Retry-After');
  await sleep(retryAfter * 1000);
}
```

### Step 6: Generate Example Usage

Create example code showing how to use the generated functions.

```javascript
// Example: Get user data
const userData = await withRetry(() => apiRequest('/users/123'));
console.log(userData);
```

## Examples

**Example 1**: Generate code for GitHub API integration
- Input: Base URL: https://api.github.com, Auth: API key, Language: JavaScript
- Output: Complete JavaScript module with authentication and request functions

**Example 2**: Generate code for OpenAI API
- Input: Base URL: https://api.openai.com/v1, Auth: API key, Language: Python
- Output: Python module with retry logic and error handling


---
*Promise: `<promise>V0_SKILL_VERIX_COMPLIANT</promise>`*
