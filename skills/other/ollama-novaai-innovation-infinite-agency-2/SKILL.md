---
name: ollama
description: Ollama API Documentation
---

# Ollama Skill

Comprehensive assistance with Ollama development - the local AI model runtime for running and interacting with large language models programmatically.

## When to Use This Skill

This skill should be triggered when:
- Running local AI models with Ollama
- Building applications that interact with Ollama's API
- Implementing chat completions, embeddings, or streaming responses
- Setting up Ollama authentication or cloud models
- Configuring Ollama server (environment variables, ports, proxies)
- Using Ollama with OpenAI-compatible libraries
- Troubleshooting Ollama installations or GPU compatibility
- Implementing tool calling, structured outputs, or vision capabilities
- Working with Ollama in Docker or behind proxies
- Creating, copying, pushing, or managing Ollama models

## Quick Reference

### 1. Basic Chat Completion (cURL)

Generate a simple chat response:

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma3",
  "messages": [
    {
      "role": "user",
      "content": "Why is the sky blue?"
    }
  ]
}'
```

### 2. Simple Text Generation (cURL)

Generate a text response from a prompt:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3",
  "prompt": "Why is the sky blue?"
}'
```

### 3. Python Chat with OpenAI Library

Use Ollama with the OpenAI Python library:

```python
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            'role': 'user',
            'content': 'Say this is a test',
        }
    ],
    model='llama3.2',
)
```

### 4. Vision Model (Image Analysis)

Ask questions about images:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")

response = client.chat.completions.create(
    model="llava",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": "data:image/png;base64,iVBORw0KG...",
                },
            ],
        }
    ],
    max_tokens=300,
)
```

### 5. Generate Embeddings

Create vector embeddings for text:

```python
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

embeddings = client.embeddings.create(
    model="all-minilm",
    input=["why is the sky blue?", "why is the grass green?"],
)
```

### 6. Structured Outputs (JSON Schema)

Get structured JSON responses:

```python
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

class FriendInfo(BaseModel):
    name: str
    age: int
    is_available: bool

class FriendList(BaseModel):
    friends: list[FriendInfo]

completion = client.beta.chat.completions.parse(
    temperature=0,
    model="llama3.1:8b",
    messages=[
        {"role": "user", "content": "Return a list of friends in JSON format"}
    ],
    response_format=FriendList,
)

friends_response = completion.choices[0].message
if friends_response.parsed:
    print(friends_response.parsed)
```

### 7. JavaScript/TypeScript Chat

Use Ollama with the OpenAI JavaScript library:

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
  baseURL: "http://localhost:11434/v1/",
  apiKey: "ollama",  // required but ignored
});

const chatCompletion = await openai.chat.completions.create({
  messages: [{ role: "user", content: "Say this is a test" }],
  model: "llama3.2",
});
```

### 8. Authentication for Cloud Models

Sign in to use cloud models:

```bash
# Sign in from CLI
ollama signin

# Then use cloud models
ollama run gpt-oss:120b-cloud
```

Or use API keys for direct cloud access:

```bash
export OLLAMA_API_KEY=your_api_key

curl https://ollama.com/api/generate \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -d '{
    "model": "gpt-oss:120b",
    "prompt": "Why is the sky blue?",
    "stream": false
  }'
```

### 9. Configure Ollama Server

Set environment variables for server configuration:

**macOS:**
```bash
# Set environment variable
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"

# Restart Ollama application
```

**Linux (systemd):**
```bash
# Edit service
systemctl edit ollama.service

# Add under [Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"

# Reload and restart
systemctl daemon-reload
systemctl restart ollama
```

**Windows:**
```
1. Quit Ollama from task bar
2. Search "environment variables" in Settings
3. Edit or create OLLAMA_HOST variable
4. Set value: 0.0.0.0:11434
5. Restart Ollama from Start menu
```

### 10. Check Model GPU Loading

Verify if your model is using GPU:

```bash
ollama ps
```

Output shows:
- `100% GPU` - Fully loaded on GPU
- `100% CPU` - Fully loaded in system memory
- `48%/52% CPU/GPU` - Split between both

## Key Concepts

### Base URLs

- **Local API (default)**: `http://localhost:11434/api`
- **Cloud API**: `https://ollama.com/api`
- **OpenAI Compatible**: `/v1/` endpoints for OpenAI libraries

### Authentication

- **Local**: No authentication required for `http://localhost:11434`
- **Cloud Models**: Requires signing in (`ollama signin`) or API key
- **API Keys**: For programmatic access to `https://ollama.com/api`

### Models

- **Local Models**: Run on your machine (e.g., `gemma3`, `llama3.2`, `qwen3`)
- **Cloud Models**: Suffix `-cloud` (e.g., `gpt-oss:120b-cloud`, `qwen3-coder:480b-cloud`)
- **Vision Models**: Support image inputs (e.g., `llava`)

### Common Environment Variables

- `OLLAMA_HOST` - Change bind address (default: `127.0.0.1:11434`)
- `OLLAMA_CONTEXT_LENGTH` - Context window size (default: `2048` tokens)
- `OLLAMA_MODELS` - Model storage directory
- `OLLAMA_ORIGINS` - Allow additional web origins for CORS
- `HTTPS_PROXY` - Proxy server for model downloads

### Error Handling

**Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (model doesn't exist)
- `429` - Too Many Requests (rate limit)
- `500` - Internal Server Error
- `502` - Bad Gateway (cloud model unreachable)

**Error Format:**
```json
{
  "error": "the model failed to generate a response"
}
```

### Streaming vs Non-Streaming

- **Streaming** (default): Returns response chunks as JSON objects (NDJSON)
- **Non-Streaming**: Set `"stream": false` to get complete response in one object

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **llms-txt.md** - Complete API reference covering:
  - All API endpoints (`/api/generate`, `/api/chat`, `/api/embed`, etc.)
  - Authentication methods (signin, API keys)
  - Error handling and status codes
  - OpenAI compatibility layer
  - Cloud models usage
  - Streaming responses
  - Configuration and environment variables

- **llms.md** - Documentation index listing all available topics:
  - API reference (version, model details, chat, generate, embeddings)
  - Capabilities (embeddings, streaming, structured outputs, tool calling, vision)
  - CLI reference
  - Cloud integration
  - Platform-specific guides (Linux, macOS, Windows, Docker)
  - IDE integrations (VS Code, JetBrains, Xcode, Zed, Cline)

Use the reference files when you need:
- Detailed API parameter specifications
- Complete endpoint documentation
- Advanced configuration options
- Platform-specific setup instructions
- Integration guides for specific tools

## Working with This Skill

### For Beginners

Start with these common patterns:
1. **Simple generation**: Use `/api/generate` endpoint with a prompt
2. **Chat interface**: Use `/api/chat` with messages array
3. **OpenAI compatibility**: Use OpenAI libraries with `base_url='http://localhost:11434/v1/'`
4. **Check GPU usage**: Run `ollama ps` to verify model loading

Read `llms-txt.md` section on "Introduction" and "Quickstart" for foundational concepts.

### For Intermediate Users

Focus on:
- **Embeddings** for semantic search and RAG applications
- **Structured outputs** with JSON schema validation
- **Vision models** for image analysis
- **Streaming** for real-time response generation
- **Authentication** for cloud models

Check the specific API endpoints in `llms-txt.md` for detailed parameter options.

### For Advanced Users

Explore:
- **Tool calling** for function execution
- **Custom model creation** with Modelfiles
- **Server configuration** with environment variables
- **Proxy setup** for network-restricted environments
- **Docker deployment** with custom configurations
- **Performance optimization** with GPU settings

Refer to platform-specific sections in `llms.md` and configuration details in `llms-txt.md`.

### Common Use Cases

**Building a chatbot:**
1. Use `/api/chat` endpoint
2. Maintain message history in your application
3. Stream responses for better UX
4. Handle errors gracefully

**Creating embeddings for search:**
1. Use `/api/embed` endpoint
2. Store embeddings in vector database
3. Perform similarity search
4. Implement RAG (Retrieval Augmented Generation)

**Running behind a firewall:**
1. Set `HTTPS_PROXY` environment variable
2. Configure proxy in Docker if containerized
3. Ensure certificates are trusted

**Using cloud models:**
1. Run `ollama signin` once
2. Pull cloud models with `-cloud` suffix
3. Use same API endpoints as local models

## Troubleshooting

### Model Not Loading on GPU

**Check:**
```bash
ollama ps
```

**Solutions:**
- Verify GPU compatibility in documentation
- Check CUDA/ROCm installation
- Review available VRAM
- Try smaller model variants

### Cannot Access Ollama Remotely

**Problem:** Ollama only accessible from localhost

**Solution:**
```bash
# Set OLLAMA_HOST to bind to all interfaces
export OLLAMA_HOST="0.0.0.0:11434"
```

See "How do I configure Ollama server?" in `llms-txt.md` for platform-specific instructions.

### Proxy Issues

**Problem:** Cannot download models behind proxy

**Solution:**
```bash
# Set proxy (HTTPS only, not HTTP)
export HTTPS_PROXY=https://proxy.example.com

# Restart Ollama
```

See "How do I use Ollama behind a proxy?" in `llms-txt.md`.

### CORS Errors in Browser

**Problem:** Browser extension or web app cannot access Ollama

**Solution:**
```bash
# Allow specific origins
export OLLAMA_ORIGINS="chrome-extension://*,moz-extension://*"
```

See "How can I allow additional web origins?" in `llms-txt.md`.

## Resources

### Official Documentation
- Main docs: https://docs.ollama.com
- API Reference: https://docs.ollama.com/api
- Model Library: https://ollama.com/models

### Official Libraries
- Python: https://github.com/ollama/ollama-python
- JavaScript: https://github.com/ollama/ollama-js

### Community
- GitHub: https://github.com/ollama/ollama
- Community Libraries: See GitHub README for full list

## Notes

- This skill was generated from official Ollama documentation
- All examples are tested and working with Ollama's API
- Code samples include proper language detection for syntax highlighting
- Reference files preserve structure from official docs with working links
- OpenAI compatibility means most OpenAI code works with minimal changes

## Quick Command Reference

```bash
# CLI Commands
ollama signin                    # Sign in to ollama.com
ollama run gemma3               # Run a model interactively
ollama pull gemma3              # Download a model
ollama ps                       # List running models
ollama list                     # List installed models

# Check API Status
curl http://localhost:11434/api/version

# Environment Variables (Common)
export OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_CONTEXT_LENGTH=8192
export OLLAMA_ORIGINS="*"
export HTTPS_PROXY="https://proxy.example.com"
```
