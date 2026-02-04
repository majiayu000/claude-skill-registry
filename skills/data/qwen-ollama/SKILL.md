---
name: Qwen-Ollama
description: Using Qwen 2.5 models via Ollama for local LLM inference, text analysis, and AI-powered automation
---

# Qwen via Ollama

Local LLM inference using Qwen 2.5 models through Ollama. Enables text analysis, summarization, code generation, and structured data analysis without cloud dependencies.

## Instructions

When helping users with Ollama and Qwen models, follow these guidelines:

1. **Installation First**: Always verify Ollama is installed and the desired model is pulled before attempting API calls
2. **Use Appropriate Model Size**: Recommend qwen2.5:7b for balanced performance (4.7 GB), or smaller/larger based on available resources
3. **Set Proper Timeouts**: Default 120s timeout for analysis tasks, longer for complex generation
4. **Handle Streaming**: Use `"stream": false` for simple cases, streaming for real-time feedback
5. **System Prompts**: Define personality and role in system message for consistent behavior
6. **Validate Responses**: Always check the `done` field and handle partial responses appropriately

## Examples

### Example 1: Basic Installation and Setup
```
User: I want to use Qwen locally for text analysis

Claude: I'll help you set up Ollama with Qwen 2.5:

1. Install Ollama service
2. Pull the qwen2.5:7b model (4.7 GB)
3. Verify it's working

[Provides installation commands from Quick Setup pattern below]
```

### Example 2: Rust Integration for Analysis
```
User: I need to analyze server logs with an LLM in my Rust application

Claude: I'll create an Ollama client using reqwest to send logs to Qwen 2.5:
- Async client with timeout
- JSON serialization for requests/responses
- Error handling for network issues

[Provides implementation using Rust Client pattern below]
```

### Example 3: System Prompt for Personality
```
User: How do I make the LLM respond with a specific personality?

Claude: Use the chat API with a system message to define behavior:
- System role sets the personality/instructions
- User role contains the actual query
- The model maintains this context throughout

[Provides chat completion example from System Prompts pattern below]
```

---

# Reference Implementation Details

The sections below contain proven working patterns from production systems.

**Reference Files in This Folder**:
- `OllamaClient.rs` - Complete Rust client implementation from Marvinous project

## Quick Setup

**Installation:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Qwen 2.5 model (7B variant, 4.7 GB)
ollama pull qwen2.5:7b

# Verify installation
ollama list
systemctl status ollama
```

**Model Variants:**
- `qwen2.5:0.5b` - Tiny (500 MB) for testing
- `qwen2.5:7b` - Balanced (4.7 GB) **recommended**
- `qwen2.5:14b` - Better quality (8.7 GB)
- `qwen2.5:32b` - Highest quality (19 GB)

## Basic API Patterns

### Generate Completion (Simple Text)

**Endpoint:** `POST http://localhost:11434/api/generate`

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:7b",
    "prompt": "Explain RAID levels in servers",
    "stream": false
  }'
```

**Response:**
```json
{
  "model": "qwen2.5:7b",
  "response": "RAID (Redundant Array of Independent Disks) provides...",
  "done": true
}
```

### Chat Completion (With Context)

**Endpoint:** `POST http://localhost:11434/api/chat`

```bash
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:7b",
    "messages": [
      {"role": "system", "content": "You are a server monitoring expert."},
      {"role": "user", "content": "What does IPMI provide?"}
    ],
    "stream": false
  }'
```

## Rust Client Pattern

**Location:** `Marvinous/src/llm/client.rs`
**Purpose:** Async Ollama client with timeout and error handling

### Dependencies

```toml
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tokio = { version = "1", features = ["full"] }
```

### Client Implementation

```rust
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::time::Duration;

#[derive(Serialize)]
struct GenerateRequest {
    model: String,
    prompt: String,
    stream: bool,
}

#[derive(Deserialize)]
struct GenerateResponse {
    response: String,
    done: bool,
}

pub struct OllamaClient {
    client: Client,
    endpoint: String,
    model: String,
}

impl OllamaClient {
    pub fn new(endpoint: &str, model: &str, timeout_secs: u64) -> Self {
        let client = Client::builder()
            .timeout(Duration::from_secs(timeout_secs))
            .build()
            .expect("Failed to create HTTP client");

        Self {
            client,
            endpoint: endpoint.to_string(),
            model: model.to_string(),
        }
    }

    pub async fn generate(&self, prompt: &str) -> Result<String, Box<dyn std::error::Error>> {
        let request = GenerateRequest {
            model: self.model.clone(),
            prompt: prompt.to_string(),
            stream: false,
        };

        let response = self.client
            .post(format!("{}/api/generate", self.endpoint))
            .json(&request)
            .send()
            .await?
            .json::<GenerateResponse>()
            .await?;

        Ok(response.response)
    }
}
```

**Usage:**
```rust
#[tokio::main]
async fn main() {
    let client = OllamaClient::new("http://localhost:11434", "qwen2.5:7b", 120);
    let result = client.generate("Analyze this system log").await.unwrap();
    println!("{}", result);
}
```

**Key Points:**
- Timeout prevents hanging on long generations (default 120s)
- Non-streaming mode returns complete response
- Error handling for network and parsing failures

## System Prompts Pattern

**Location:** `Marvinous/src/llm/prompt.rs`
**Purpose:** Define LLM personality and behavior

### Chat API with System Message

```rust
#[derive(Serialize)]
struct ChatMessage {
    role: String,
    content: String,
}

#[derive(Serialize)]
struct ChatRequest {
    model: String,
    messages: Vec<ChatMessage>,
    stream: bool,
}

let messages = vec![
    ChatMessage {
        role: "system".to_string(),
        content: "You are Marvin, the Paranoid Android. Respond with existential dread.".to_string(),
    },
    ChatMessage {
        role: "user".to_string(),
        content: "How are the servers?".to_string(),
    },
];

let request = ChatRequest {
    model: "qwen2.5:7b".to_string(),
    messages,
    stream: false,
};
```

**System Prompt Best Practices:**
1. Define the role clearly ("You are X")
2. Specify output format expectations
3. Include personality traits if desired
4. Set constraints (length, tone, structure)
5. Provide domain context

## Common Use Cases

### 1. Log Analysis

**Prompt Pattern:**
```
Analyze these server logs and identify issues:

[log entries]

Focus on:
- Error patterns
- Security events
- Performance anomalies
```

### 2. Data Summarization

**Prompt Pattern:**
```
Summarize this IPMI sensor data:

{json_data}

Highlight:
- Anomalies or concerning values
- Temperature trends
- Fan speed issues
```

### 3. Code Generation

**Prompt Pattern:**
```
Write a Rust function that:
- Parses smartctl JSON output
- Extracts drive health metrics
- Returns structured data

Use serde for JSON parsing.
```

## Model Parameters

### Temperature Control

```json
{
  "model": "qwen2.5:7b",
  "prompt": "...",
  "options": {
    "temperature": 0.7
  }
}
```

**Temperature Values:**
- `0.0` - Deterministic (same output every time)
- `0.3-0.7` - Balanced creativity/consistency
- `1.0+` - Maximum creativity/randomness

### Context Window

Qwen 2.5 supports **32K tokens** context window (approximately 24K words).

## Troubleshooting

### "Connection Refused" Error

**Cause:** Ollama service not running

**Solution:**
```bash
sudo systemctl start ollama
sudo systemctl status ollama
```

### "Model Not Found" Error

**Cause:** Model not pulled locally

**Solution:**
```bash
ollama list           # Check available models
ollama pull qwen2.5:7b  # Pull the model
```

### Timeout Errors

**Cause:** Generation taking longer than client timeout

**Solution:**
```rust
// Increase timeout for complex tasks
let client = Client::builder()
    .timeout(Duration::from_secs(300))  // 5 minutes
    .build()?;
```

### Out of Memory

**Cause:** Model too large for available RAM/VRAM

**Solution:**
```bash
# Use smaller model
ollama pull qwen2.5:0.5b

# Or check memory usage
free -h
nvidia-smi  # For GPU memory
```

## VRAM Management

### Model Auto-Unloading

Ollama automatically unloads models from VRAM after inactivity to free GPU memory:

**Check Current Status:**
```bash
ollama ps                  # List loaded models
nvidia-smi                 # Check VRAM usage
```

**Model Lifecycle:**
```
1. Request arrives → Model loads to VRAM (~4.7 GB for qwen2.5:7b)
2. Inference runs → GPU processes prompt (5-10 seconds)
3. Response sent → Model stays in VRAM (configured timeout)
4. Timeout expires → Model automatically unloaded (VRAM freed)
```

**Configure Auto-Unload Timeout:**

Edit `/etc/systemd/system/ollama.service.d/models-location.conf`:

```ini
[Service]
Environment="OLLAMA_MODELS=/var/lib/ollama/models"
Environment="OLLAMA_KEEP_ALIVE=30s"
```

**Timeout Options:**
- `OLLAMA_KEEP_ALIVE=0` - Unload immediately after each request
- `OLLAMA_KEEP_ALIVE=30s` - Keep for 30 seconds (recommended for shared GPU)
- `OLLAMA_KEEP_ALIVE=5m` - Keep for 5 minutes (default)
- `OLLAMA_KEEP_ALIVE=-1` - Keep loaded indefinitely

After changes:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

### Manual VRAM Control

**Immediately Unload Model:**
```bash
ollama stop qwen2.5:7b
# Frees VRAM instantly for other GPU work
```

**Pre-Load Model (Warm Start):**
```bash
echo "test" | ollama run qwen2.5:7b >/dev/null 2>&1
# Loads model into VRAM before batch jobs
```

**VRAM Management Script:**

Create `~/scripts/ollama-vram.sh`:
```bash
#!/bin/bash
case "$1" in
    status)
        nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader
        echo ""
        ollama ps
        ;;
    unload)
        ollama ps --format json | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | \
        while read model; do ollama stop "$model"; done
        echo "VRAM freed"
        ;;
    load)
        echo "test" | ollama run qwen2.5:7b >/dev/null 2>&1
        ollama ps
        ;;
esac
```

**Usage:**
```bash
chmod +x ~/scripts/ollama-vram.sh

# Check VRAM status
~/scripts/ollama-vram.sh status

# Free VRAM before CUDA work
~/scripts/ollama-vram.sh unload
python train_model.py  # Your GPU work here

# Pre-warm for batch inference
~/scripts/ollama-vram.sh load
```

### Performance Optimization

**GPU Acceleration:**

Ollama automatically uses NVIDIA GPUs if available:

```bash
# Monitor GPU during generation
nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv -l 1
```

**Concurrent Requests:**

```bash
# Increase max loaded models for high concurrency
OLLAMA_MAX_LOADED_MODELS=2 ollama serve
```

**Force CPU-Only:**

```bash
# Disable GPU (use CPU inference)
CUDA_VISIBLE_DEVICES="" ollama serve
```

## Production Deployment

### Systemd Service

Ollama installs as a systemd service automatically:

```bash
# Check status
systemctl status ollama

# View logs
journalctl -u ollama -f

# Restart service
sudo systemctl restart ollama
```

### Configuration

Edit `/etc/systemd/system/ollama.service` to set environment variables:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_MAX_LOADED_MODELS=2"
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

## Best Practices Summary

1. **Validate Installation**: Always check `ollama list` before assuming model availability
2. **Set Appropriate Timeouts**: 120s for analysis, 300s for complex generation
3. **Use System Prompts**: Define behavior in system message for consistency
4. **Handle Errors**: Network issues, timeouts, and parsing failures are common
5. **Monitor Resources**: Watch GPU/CPU memory during sustained workloads
6. **Cache Results**: Store frequently-used completions to reduce inference time
7. **Keep Prompts Focused**: Clear, specific instructions produce better results

## Reference Implementation

See **Marvinous** project for complete production example:
- `/home/matt/Marvinous/src/llm/client.rs` - Ollama API client
- `/home/matt/Marvinous/src/llm/prompt.rs` - Prompt building
- `/etc/marvinous/system-prompt.txt` - System prompt with Marvin's personality
- `/etc/marvinous/marvinous.toml` - Configuration with model/endpoint settings
