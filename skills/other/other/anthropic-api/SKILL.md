---
name: anthropic-api
cluster: ai-apis
description: "Anthropic Claude API for AI models with tool use and extended context."
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

# anthropic-api

## Purpose
This skill integrates with Anthropic's Claude API to leverage advanced AI models for tasks requiring tool use and extended context, enabling complex interactions like function calling and long-form processing.

## When to Use
Use this skill for scenarios involving sophisticated AI reasoning, such as analyzing large documents, generating code with tools, or handling multi-step workflows. It's ideal when standard models fall short, like in research, automation, or interactive applications.

## Key Capabilities
- Access Claude models (e.g., claude-3-haiku, claude-3-sonnet) via API for text generation and completion.
- Support tool use, allowing the AI to call external functions based on JSON-defined tools.
- Handle extended contexts up to 200K tokens for processing long inputs.
- Real-time streaming responses for interactive sessions.
- Fine-grained control over parameters like temperature (0.0-1.0) and top_p (0-1).

## Usage Patterns
To use this skill in OpenClaw, first set the API key as an environment variable (e.g., export ANTHROPIC_API_KEY=your_key). Invoke the skill via OpenClaw's execute command, passing parameters like model and prompt. For HTTP-based integration, make POST requests to the API endpoint. Always include authentication headers. Structure requests with JSON bodies containing "messages" array for conversation history and "tools" for function definitions.

## Common Commands/API
- **Endpoint**: POST https://api.anthropic.com/v1/messages
- **Authentication**: Set header 'Authorization: Bearer $ANTHROPIC_API_KEY' (use env var for security).
- **Key Parameters**: In request body, include "model" (e.g., "claude-3-5-sonnet-20241001"), "max_tokens" (e.g., 1024), "temperature" (e.g., 0.7), and "tools" as an array of JSON objects (e.g., [{"name": "get_weather", "description": "Fetch weather data"}]).
- **CLI Example**: Use curl for testing: curl -X POST https://api.anthropic.com/v1/messages -H "Authorization: Bearer $ANTHROPIC_API_KEY" -H "Content-Type: application/json" -d '{"model": "claude-3-haiku", "messages": [{"role": "user", "content": "Hello"}]}'
- **Code Snippet (Python)**:
  import requests
  response = requests.post('https://api.anthropic.com/v1/messages', headers={'Authorization': f'Bearer {os.environ["ANTHROPIC_API_KEY"]}'}, json={'model': 'claude-3-haiku', 'messages': [{'role': 'user', 'content': 'Summarize this.'}]})
  print(response.json())
- **Config Format**: In OpenClaw, configure via skill settings with YAML like: api_key: $ANTHROPIC_API_KEY, default_model: claude-3-sonnet.

## Integration Notes
In OpenClaw, load this skill with `openclaw load anthropic-api`. Set up environment variables for keys (e.g., ANTHROPIC_API_KEY) to avoid hardcoding. For tool integration, define tools in your prompt as JSON arrays and handle responses in a loop to process AI-generated actions. Ensure your application handles rate limits (e.g., 10 requests per minute) by implementing retry logic with exponential backoff. Test integrations in a sandbox environment before production use.

## Error Handling
Common errors include 401 (unauthorized) for invalid API keys—check if $ANTHROPIC_API_KEY is set correctly. Handle 429 (rate limit) by waiting and retrying with a delay (e.g., time.sleep(60)). For 400 (bad request), validate your JSON payload, especially the "messages" structure. In code, use try-except blocks: try: response = requests.post(...) except requests.exceptions.HTTPError as e: print(f"Error: {e.response.status_code} - {e.response.text}"); if e.response.status_code == 429: retry_after = int(e.response.headers.get('Retry-After', 60)); time.sleep(retry_after).

## Usage Examples
1. **Text Completion Task**: To generate a summary, use OpenClaw with: openclaw execute anthropic-api --prompt "Summarize the key points of quantum computing" --model claude-3-haiku. This sends a POST request and returns the AI response directly.
2. **Tool Use Example**: For fetching data, define a tool and prompt: openclaw execute anthropic-api --prompt "Get the current weather for New York" --tools '[{"name": "get_weather", "description": "Fetch weather", "parameters": {"location": "string"}}]'. The AI will respond with a tool call, which you handle by executing the function and feeding back the result.

## Graph Relationships
- Related to cluster: ai-apis
- Tagged with: ai-apis, api
- Connected skills: openai-api (for comparative AI capabilities), function-caller (for enhanced tool integration)
