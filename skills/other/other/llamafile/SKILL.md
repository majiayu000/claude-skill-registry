---
name: llamafile
description: When setting up local LLM inference without cloud APIs. When running GGUF models locally. When needing OpenAI-compatible API from a local model. When building offline/air-gapped AI tools. When troubleshooting local LLM server connections.
---

# Llamafile

Configure and manage Mozilla Llamafile - a cross-platform executable distribution format that runs LLMs locally with an OpenAI-compatible API.

## When to Use This Skill

Use this skill when:

- Installing llamafile binary and GGUF model files
- Starting llamafile server with optimal configuration
- Integrating llamafile with LiteLLM or OpenAI SDK
- Configuring llamafile for different performance profiles (GPU, CPU, network access)
- Troubleshooting llamafile server startup or API connection issues
- Building applications requiring local LLM inference
- Setting up commit message tools, code review systems, or other developer tools with local AI
- Managing llamafile as a background service
- Selecting and downloading appropriate GGUF models
- Validating OpenAI-compatible API responses

## Core Capabilities

### What Llamafile Provides

Llamafile combines llama.cpp with Cosmopolitan Libc to create single-file executables that:

- Run on macOS, Windows, Linux, FreeBSD, OpenBSD, NetBSD
- Support AMD64 and ARM64 architectures
- Serve OpenAI-compatible HTTP API on localhost
- Load GGUF model files for inference
- Provide `/health` endpoint for monitoring
- Support GPU acceleration (CUDA, Metal, Vulkan)
- Enable embeddings generation with `--embedding` flag

### API Compatibility

Llamafile exposes these OpenAI-compatible endpoints when running with `--server`:

| Endpoint                                    | Description                | Requirements       |
| ------------------------------------------- | -------------------------- | ------------------ |
| `http://localhost:8080/v1/chat/completions` | Chat completions (primary) | Server mode        |
| `http://localhost:8080/v1/completions`      | Text completions           | Server mode        |
| `http://localhost:8080/v1/embeddings`       | Generate embeddings        | `--embedding` flag |
| `http://localhost:8080/health`              | Health check               | Server mode        |

**Critical Detail**: All OpenAI-compatible endpoints require `/v1` prefix in the URL path.

## Installation

### Download Llamafile Binary

```bash
# Download llamafile v0.9.3 binary
curl -L -o llamafile https://github.com/mozilla-ai/llamafile/releases/download/0.9.3/llamafile-0.9.3

# Make executable
chmod 755 llamafile

# Verify version
./llamafile --version
```

**Alternative download sources:**

- GitHub Release: `https://github.com/mozilla-ai/llamafile/releases/download/0.9.3/llamafile-0.9.3`
- SourceForge Mirror: `https://sourceforge.net/projects/llamafile.mirror/files/0.9.3/`

### Download GGUF Model

Llamafile requires GGUF format models. Download from Hugging Face:

```bash
# Recommended: Gemma 3 3B (balanced speed/quality, ~2GB)
curl -L -o gemma-3-3b.gguf \
  https://huggingface.co/Mozilla/gemma-3-3b-it-gguf/resolve/main/gemma-3-3b-it-Q4_K_M.gguf

# Alternative: Pre-packaged llamafile with embedded model
curl -LO https://huggingface.co/Mozilla/llava-v1.5-7b-llamafile/resolve/main/llava-v1.5-7b-q4.llamafile
chmod +x llava-v1.5-7b-q4.llamafile
```

**Recommended models by use case:**

| Model | Size | Use Case | Download |
| --- | --- | --- | --- |
| Gemma 3 3B | ~2GB | Balanced speed/quality | [Mozilla/gemma-3-3b-it-gguf](https://huggingface.co/Mozilla/gemma-3-3b-it-gguf) |
| Qwen3-0.6B | ~500MB | Fast, lower quality | [Mozilla/Qwen3-0.6B-gguf](https://huggingface.co/Mozilla/Qwen3-0.6B-gguf) |
| Mistral 7B | ~4GB | Higher quality, slower | [Mozilla/Mistral-7B-gguf](https://huggingface.co/Mozilla/Mistral-7B-gguf) |
| Llama 3.1 8B | ~5GB | Best quality, slowest | [Mozilla/Llama-3.1-8B-gguf](https://huggingface.co/Mozilla/Llama-3.1-8B-gguf) |

**Quantization recommendation**: Use Q4_K_M quantized models for optimal balance of quality and performance.

## Server Configuration

### Basic Server Command

Start llamafile server for local API access:

```bash
./llamafile --server \
    -m /path/to/model.gguf \
    --nobrowser \
    --port 8080 \
    --host 127.0.0.1
```

**Critical flags explained:**

- `--server`: Required to enable HTTP API endpoints
- `-m`: Path to GGUF model file (required)
- `--nobrowser`: Prevents auto-opening browser on startup
- `--port 8080`: Default port (note: NOT 8000)
- `--host 127.0.0.1`: Localhost only (secure default)

### Performance-Optimized Configuration

For GPU-accelerated inference with higher throughput:

```bash
./llamafile --server \
    -m /path/to/model.gguf \
    --nobrowser \
    --port 8080 \
    --host 127.0.0.1 \
    --ctx-size 4096 \
    --n-gpu-layers 99 \
    --threads 8 \
    --cont-batching \
    --parallel 4
```

**Advanced flags:**

| Flag | Purpose | Default | When to Use |
| --- | --- | --- | --- |
| `--ctx-size` | Prompt context window size | 512 | Increase for longer conversations |
| `--n-gpu-layers` | GPU offload layer count | 0 | Set to 99 to offload all layers to GPU |
| `--threads` | CPU threads for generation | Auto | Set explicitly for consistent performance |
| `--threads-batch` | Threads for batch processing | Same as `--threads` | Tune separately for prompt vs generation |
| `--cont-batching` | Continuous batching | Off | Enable for multiple concurrent requests |
| `--parallel` | Parallel sequence count | 1 | Increase for concurrent request handling |
| `--mlock` | Lock model in memory | Off | Prevent swapping on systems with sufficient RAM |
| `--embedding` | Enable embeddings endpoint | Off | Required for `/v1/embeddings` API |

### Network-Accessible Configuration

To allow connections from other machines (development/testing only):

```bash
./llamafile --server \
    -m /path/to/model.gguf \
    --nobrowser \
    --host 0.0.0.0 \
    --port 8080
```

**Security warning**: Binding to `0.0.0.0` exposes the API to network access. Use only in trusted environments.

## API Integration

### Using LiteLLM (Recommended)

LiteLLM provides unified interface for llamafile and cloud LLM providers.

```python
import litellm

response = litellm.completion(
    model="llamafile/gemma-3-3b",  # MUST use llamafile/ prefix
    messages=[{"role": "user", "content": "Hello, world!"}],
    api_base="http://localhost:8080/v1",  # MUST include /v1 suffix
    temperature=0.3,
    max_tokens=200
)

print(response.choices[0].message.content)
```

**Critical requirements for LiteLLM:**

1. Model name MUST use `llamafile/` prefix for routing
2. `api_base` MUST include `/v1` suffix
3. No API key required (any placeholder value works)

**Related skill**: For comprehensive LiteLLM configuration, activate the litellm skill:

```
Skill(command: "litellm")
```

### Using OpenAI Python SDK

Direct integration with OpenAI SDK for llamafile endpoints:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",  # MUST include /v1
    api_key="sk-no-key-required"  # Any value works
)

response = client.chat.completions.create(
    model="local-model",  # Model name is flexible
    messages=[
        {"role": "user", "content": "Hello, world!"}
    ],
    temperature=0.3,
    max_tokens=200
)

print(response.choices[0].message.content)
```

### Using curl for Testing

Verify llamafile server is responding correctly:

```bash
# Health check
curl http://localhost:8080/health

# Chat completions
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0.3,
    "max_tokens": 200
  }'

# Embeddings (requires --embedding flag on server)
curl http://localhost:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local",
    "input": ["Hello world"]
  }'
```

## Server Management

### Process Management Script

Python script to start llamafile as background process with health checking:

```python
import subprocess
import time
import httpx

def start_llamafile(
    llamafile_path: str,
    model_path: str,
    port: int = 8080,
    host: str = "127.0.0.1"
) -> subprocess.Popen:
    """Start llamafile server as background process."""
    cmd = [
        llamafile_path,
        "--server",
        "-m", model_path,
        "--nobrowser",
        "--port", str(port),
        "--host", host,
    ]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    _wait_for_server(host, port)
    return process


def _wait_for_server(host: str, port: int, timeout: int = 30) -> None:
    """Wait for server to respond to health checks."""
    url = f"http://{host}:{port}/health"
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = httpx.get(url, timeout=2)
            if response.status_code == 200:
                return
        except httpx.RequestError:
            pass
        time.sleep(0.5)
    raise TimeoutError(f"Server did not start within {timeout} seconds")
```

### Configuration File Pattern

Example TOML configuration for applications using llamafile:

```toml
# ~/.config/app-name/config.toml
[ai]
model = "llamafile/gemma-3-3b"  # Must use llamafile/ prefix
temperature = 0.3
max_tokens = 200

[llamafile]
path = "/home/user/.local/bin/llamafile"
model_path = "/home/user/.local/share/app-name/models/gemma-3-3b.gguf"
api_base = "http://127.0.0.1:8080/v1"  # Include /v1 suffix
```

## Troubleshooting

### Server Fails to Start

**Check if port is already in use:**

```bash
# Find process using port 8080
lsof -i :8080

# Kill existing process
kill $(lsof -t -i :8080)
```

**Verify model file exists and is readable:**

```bash
ls -lh /path/to/model.gguf
```

**Check llamafile binary permissions:**

```bash
ls -la /path/to/llamafile
# Should show: -rwxr-xr-x (executable)

# Fix permissions if needed
chmod 755 /path/to/llamafile
```

### Connection Refused Errors

**Verify server is running:**

```bash
# Check health endpoint
curl http://localhost:8080/health

# Check server is listening
netstat -tlnp | grep 8080
# or
lsof -i :8080
```

**Common causes:**

1. Server not started with `--server` flag
2. Wrong port number (8080 vs 8000)
3. Missing `/v1` in API URL path
4. Server bound to `127.0.0.1` but accessing from another machine

### API Errors

**Test basic connectivity:**

```bash
# Verbose health check
curl -v http://localhost:8080/health

# Test chat completions with verbose output
curl -v http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"test","messages":[{"role":"user","content":"Hi"}]}'
```

**Common API issues:**

| Error              | Cause                | Solution                          |
| ------------------ | -------------------- | --------------------------------- |
| 404 Not Found      | Missing `/v1` in URL | Add `/v1` before endpoint path    |
| Connection refused | Server not running   | Start server with `--server` flag |
| Timeout            | Model loading slowly | Wait longer or use smaller model  |
| Invalid model      | Wrong model path     | Verify `-m` path to GGUF file     |

### Performance Issues

**Optimize inference speed:**

1. Use quantized models (Q4_K_M recommended)
2. Enable GPU acceleration: `--n-gpu-layers 99`
3. Increase threads: `--threads 8`
4. Enable continuous batching: `--cont-batching`
5. Reduce context size if not needed: `--ctx-size 2048`

**Check GPU availability:**

```bash
# NVIDIA GPU
nvidia-smi

# AMD GPU
rocm-smi

# Apple Metal (check activity monitor)
```

## Common Pitfalls

Avoid these frequent errors when using llamafile:

1. **Port 8000 vs 8080**: Llamafile defaults to **port 8080**, not 8000
2. **Missing `/v1` in API URL**: Always include `/v1` suffix for OpenAI-compatible endpoints
3. **LiteLLM prefix**: Must use `llamafile/` prefix in model name for proper routing
4. **API key confusion**: No real API key needed, but some clients require placeholder value
5. **Starting server from hooks**: Application hooks should check if server is running, not start it
6. **Model path issues**: Ensure GGUF file exists and is readable before starting server
7. **Binary permissions**: Llamafile must be executable (`chmod 755`)
8. **GPU layers on CPU**: Setting `--n-gpu-layers` on CPU-only systems causes errors

## Version Information

**Current stable version**: 0.9.3 (May 14, 2025)

**Version constants:**

```
LLAMAFILE_MAJOR = 0
LLAMAFILE_MINOR = 9
LLAMAFILE_PATCH = 3
```

**Recent changes in 0.9.3:**

- Added Phi4 model support
- Added Qwen3 model support
- Respects NO_COLOR environment variable
- Fixed URL handling in JavaScript (preserves path when building relative URLs)
- Added Plaintext output option to LocalScore

## Related Skills and Tools

**Skills to activate:**

- `litellm` - For unified LLM provider interface and routing
  ```
  Skill(command: "litellm")
  ```

**External tools:**

- LiteLLM - Unified interface for multiple LLM providers
- OpenAI Python SDK - Direct OpenAI-compatible API access
- llama.cpp - Underlying inference engine
- GGUF format - Model format specification

## References

### Official Documentation

- [Mozilla llamafile GitHub](https://github.com/mozilla-ai/llamafile) - Primary repository and source code
- [Mozilla llamafile Documentation](https://mozilla-ai.github.io/llamafile/) - Official documentation site
- [LiteLLM llamafile Provider](https://docs.litellm.ai/docs/providers/llamafile) - LiteLLM integration guide
- [llama.cpp Server Documentation](https://github.com/ggml-org/llama.cpp/tree/master/examples/server) - Underlying server implementation
- [Releases Page](https://github.com/mozilla-ai/llamafile/releases) - Binary downloads and changelog

### Model Resources

- [Hugging Face Mozilla Models](https://huggingface.co/Mozilla) - Official Mozilla GGUF models
- [GGUF Format Specification](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md) - Model file format details

### Related Technologies

- [Cosmopolitan Libc](https://justine.lol/cosmopolitan/) - Cross-platform binary format
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - LLM inference engine
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) - API compatibility reference
