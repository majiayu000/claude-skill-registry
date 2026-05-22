---
name: google-ai
cluster: ai-apis
description: "Google Gemini API for Pro/Flash/Ultra models with 1M token context."
tags: ["ai-apis","api"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "keywords"
---

# google-ai

## Purpose
This skill enables interaction with Google's Gemini API, allowing access to Pro, Flash, and Ultra models for tasks like text generation, chat, and embedding with up to 1M token context. It's designed for integrating advanced AI capabilities into applications via RESTful endpoints.

## When to Use
Use this skill when you need large-context AI processing, such as summarizing long documents, generating code from detailed specs, or handling multi-turn conversations. Apply it in scenarios requiring Google-specific models, like when OpenAI alternatives are insufficient or when integrating with Google Cloud ecosystems.

## Key Capabilities
- Access Gemini Pro for general tasks, Flash for faster inference, and Ultra for complex reasoning.
- Handle contexts up to 1M tokens, ideal for processing books or codebases.
- Support multimodal inputs (text, images) via specific endpoints.
- Embeddings generation for semantic search, using models like text-embedding-004.
- Rate limiting and quotas managed per API key, with up to 1,000 requests per minute.

## Usage Patterns
Always initialize with authentication via the `$GOOGLE_API_KEY` environment variable. For OpenClaw, invoke this skill by prefixing commands with the skill ID, e.g., `google-ai generate`. Use JSON payloads for requests and handle responses as JSON objects. Pattern: Set up a request with model selection, then send via HTTP POST; parse the response for output. For repeated use, cache API responses to avoid rate limits.

## Common Commands/API
The primary endpoint is `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`. Use HTTP POST requests with a JSON body. For example:
```json
{
  "contents": [{"parts": [{"text": "Write a function for sorting arrays"}]}]
}
```
CLI example: Run `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $GOOGLE_API_KEY" -d '{"contents": [{"parts": [{"text": "Hello"}]}]}' https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent`. Common flags: `--model gemini-pro` for model selection, or `--max-tokens 1024` to limit output. For embeddings, use `https://generativelanguage.googleapis.com/v1beta/models/{model}:embedContent` with payload like:
```json
{
  "model": "models/text-embedding-004",
  "content": "Embed this text"
}
```
In OpenClaw, execute via `google-ai embed --text "Sample text" --model text-embedding-004`.

## Integration Notes
Set the `$GOOGLE_API_KEY` as an environment variable before use, e.g., `export GOOGLE_API_KEY=your_api_key`. In OpenClaw configs, add under [skills] section: `google-ai = { api_key = "$GOOGLE_API_KEY", default_model = "gemini-pro" }`. Ensure your project is enabled in Google Cloud Console under AI Studio. For asynchronous operations, use webhooks or polling; integrate with other skills by chaining outputs, e.g., pipe `google-ai` results to a search skill. Handle retries with exponential backoff for transient errors.

## Error Handling
Check HTTP status codes: 401 for invalid API key (re-authenticate using `$GOOGLE_API_KEY`), 429 for rate limits (wait and retry with a delay). Parse JSON errors for details, e.g., if "code": "INVALID_ARGUMENT", validate your request body. In OpenClaw, wrap commands in try-catch blocks: e.g., `try { execute "google-ai generate" } catch { log error and retry after 5 seconds }`. Always validate inputs to avoid 400 errors, such as ensuring model names match exactly (e.g., "gemini-1.0-pro").

## Concrete Usage Examples
1. Generate code: To create a Python function, use `google-ai generate --model gemini-pro --prompt "Write a function to merge two sorted lists"`. This sends a POST to the endpoint and returns the code snippet.
2. Embed text for search: For semantic similarity, run `google-ai embed --model text-embedding-004 --text "Example query"`, then compare embeddings in your application using cosine similarity.

## Graph Relationships
- Cluster: Connected to "ai-apis" for shared AI endpoint handling.
- Tags: Linked to "ai-apis" and "api" for discoverability in API-related skills.
- Related Skills: Integrates with "openai" for model comparisons; depends on "google-cloud" for authentication flows.
