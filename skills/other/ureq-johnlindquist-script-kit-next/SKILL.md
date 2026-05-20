---
name: ureq
description: Simple blocking HTTP client for Rust
---

# ureq

ureq is a simple, safe HTTP client written in pure Rust. It uses **blocking I/O** instead of async, which keeps the API simple and dependencies minimal. This is ideal for script-kit-gpui's AI provider calls where simplicity trumps concurrent request handling.

## Why Blocking Can Be Good

- **Simpler mental model**: No async/await, no runtime, no Pin<Box<Future>>
- **Easier error handling**: Standard Result types, no async error propagation complexity
- **Lower dependency count**: No tokio/async-std runtime required
- **Thread-based concurrency**: Spawn threads for parallel requests if needed
- **Perfect for CLI tools**: Where async overhead isn't justified

## Key Types

### Agent

Connection pool + configuration holder. Reuse across requests for connection reuse.

```rust
use ureq::Agent;
use std::time::Duration;

let agent: Agent = Agent::config_builder()
    .timeout_connect(Some(Duration::from_secs(10)))
    .timeout_recv_body(Some(Duration::from_secs(60)))
    .build()
    .new_agent();
```

### RequestBuilder

Fluent builder for constructing requests.

```rust
let response = agent.post("https://api.example.com")
    .header("Content-Type", "application/json")
    .header("Authorization", "Bearer token")
    .send_json(&body)?;
```

### Response / Body

Response wraps the HTTP response. Body provides methods to read response data.

```rust
// Get status
let status = response.status();

// Read as JSON (requires `json` feature)
let data: MyStruct = response.into_body().read_json()?;

// Read as string
let text: String = response.into_body().read_to_string()?;

// Get a reader for streaming
let reader = response.into_body().into_reader();
```

### Error

Unified error type covering network, protocol, and HTTP status errors.

```rust
use ureq::Error;

match agent.get(url).call() {
    Ok(response) => { /* success */ }
    Err(Error::StatusCode(code)) => { /* 4xx/5xx */ }
    Err(e) => { /* network/protocol error */ }
}
```

## Usage in script-kit-gpui

script-kit-gpui uses ureq for AI provider API calls (OpenAI, Anthropic, Vercel Gateway).

### Agent Creation Pattern

```rust
const CONNECT_TIMEOUT_SECS: u64 = 10;
const READ_TIMEOUT_SECS: u64 = 60;

fn create_agent() -> ureq::Agent {
    ureq::Agent::config_builder()
        .timeout_connect(Some(Duration::from_secs(CONNECT_TIMEOUT_SECS)))
        .timeout_recv_body(Some(Duration::from_secs(READ_TIMEOUT_SECS)))
        .build()
        .new_agent()
}
```

### Provider Struct Pattern

```rust
pub struct OpenAiProvider {
    config: ProviderConfig,
    agent: ureq::Agent,  // Reused across requests
}

impl OpenAiProvider {
    pub fn new(api_key: impl Into<String>) -> Self {
        Self {
            config: ProviderConfig::new("openai", "OpenAI", api_key),
            agent: create_agent(),
        }
    }
}
```

## Request Building

### GET Request

```rust
let response = ureq::get("https://api.example.com/data")
    .header("Authorization", "Bearer token")
    .call()?;
```

### POST with JSON

```rust
let body = serde_json::json!({
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello"}]
});

let response = agent
    .post("https://api.openai.com/v1/chat/completions")
    .header("Content-Type", "application/json")
    .header("Authorization", &format!("Bearer {}", api_key))
    .send_json(&body)?;
```

### Headers for AI APIs

```rust
// OpenAI
.header("Authorization", &format!("Bearer {}", api_key))

// Anthropic
.header("x-api-key", api_key)
.header("anthropic-version", "2023-06-01")

// SSE streaming
.header("Accept", "text/event-stream")
```

## Response Handling

### Status Codes

By default, ureq returns `Error::StatusCode` for 4xx/5xx responses. Handle explicitly:

```rust
match agent.post(url).send_json(&body) {
    Ok(response) => {
        // 2xx success
        let json: serde_json::Value = response.into_body().read_json()?;
    }
    Err(Error::StatusCode(code)) => {
        // 4xx/5xx - API error
        eprintln!("API error: {}", code);
    }
    Err(e) => {
        // Network/timeout/etc
        return Err(e.into());
    }
}
```

### JSON Parsing

Requires `json` feature in Cargo.toml:

```rust
// Deserialize to struct
let data: MyResponse = response.into_body().read_json()?;

// Deserialize to Value for dynamic parsing
let json: serde_json::Value = response.into_body().read_json()?;
let content = json["choices"][0]["message"]["content"].as_str();
```

### Using anyhow Context

```rust
use anyhow::{Context, Result};

let response = agent
    .post(url)
    .send_json(&body)
    .context("Failed to send request to OpenAI API")?;

let json: serde_json::Value = response
    .into_body()
    .read_json()
    .context("Failed to parse OpenAI response")?;
```

## Streaming Responses

For AI streaming (SSE), convert body to a reader and process line-by-line:

```rust
use std::io::{BufRead, BufReader};

let response = agent
    .post(url)
    .header("Accept", "text/event-stream")
    .send_json(&body)?;

// Convert to buffered reader
let reader = BufReader::new(response.into_body().into_reader());

// Process SSE lines
for line in reader.lines() {
    let line = line?;
    
    // Handle CRLF
    let line = line.trim_end_matches('\r');
    
    // Empty line = end of event
    if line.is_empty() {
        continue;
    }
    
    // Parse data lines
    if let Some(data) = line.strip_prefix("data: ") {
        if data == "[DONE]" {
            break;
        }
        
        // Parse JSON and extract content
        if let Ok(parsed) = serde_json::from_str::<serde_json::Value>(data) {
            if let Some(content) = parsed["choices"][0]["delta"]["content"].as_str() {
                on_chunk(content.to_string());
            }
        }
    }
}
```

### SSE Helper Pattern (from script-kit-gpui)

```rust
fn stream_sse_lines<R: BufRead>(
    reader: R,
    mut on_data: impl FnMut(&str) -> Result<bool>,
) -> Result<()> {
    let mut data_buf = String::new();

    for line in reader.lines() {
        let mut line = line.context("Failed to read SSE line")?;
        if line.ends_with('\r') {
            line.pop();
        }

        if line.is_empty() {
            if data_buf.is_empty() {
                continue;
            }
            if data_buf == "[DONE]" {
                break;
            }
            if !on_data(&data_buf)? {
                break;
            }
            data_buf.clear();
            continue;
        }

        if let Some(d) = line.strip_prefix("data: ") {
            if !data_buf.is_empty() {
                data_buf.push('\n');
            }
            data_buf.push_str(d);
        }
    }
    Ok(())
}
```

## Timeouts

Configure at Agent level:

```rust
Agent::config_builder()
    .timeout_connect(Some(Duration::from_secs(10)))   // TCP connect
    .timeout_recv_body(Some(Duration::from_secs(60))) // Body receive
    .timeout_global(Some(Duration::from_secs(120)))   // Total request
    .build()
```

## TLS

ureq uses rustls by default (pure Rust TLS). For native TLS:

```rust
use ureq::tls::{TlsConfig, TlsProvider};

let config = Config::builder()
    .tls_config(
        TlsConfig::builder()
            .provider(TlsProvider::NativeTls)  // Use OS TLS
            .build()
    )
    .build();
```

## Anti-patterns

### Don't Create Agent Per Request

```rust
// BAD: Creates new connection pool each time
fn make_request() {
    let agent = ureq::agent();
    agent.get(url).call()
}

// GOOD: Reuse agent
struct Client {
    agent: ureq::Agent,
}
impl Client {
    fn make_request(&self) {
        self.agent.get(url).call()
    }
}
```

### Don't Ignore Status Codes

```rust
// BAD: Assumes success
let json = agent.get(url).call()?.into_body().read_json()?;

// GOOD: Handle error responses
match agent.get(url).call() {
    Ok(resp) => resp.into_body().read_json()?,
    Err(Error::StatusCode(code)) => {
        // Log or handle API error
        return Err(anyhow!("API returned {}", code));
    }
    Err(e) => return Err(e.into()),
}
```

### Don't Block Forever on Streaming

```rust
// BAD: No timeout, hangs forever if server stops sending
for line in reader.lines() { ... }

// GOOD: Set timeout_recv_body on agent, or implement read timeout
Agent::config_builder()
    .timeout_recv_body(Some(Duration::from_secs(60)))
    .build()
```

### Don't Forget Content-Type

```rust
// BAD: Server may reject or misparse
agent.post(url).send(json_string)?;

// GOOD: Set Content-Type explicitly
agent.post(url)
    .header("Content-Type", "application/json")
    .send(json_string)?;

// BEST: Use send_json which sets Content-Type automatically
agent.post(url).send_json(&body)?;
```

## Feature Flags

Enable in Cargo.toml:

```toml
[dependencies]
ureq = { version = "3", features = ["json", "gzip"] }
```

- **rustls** (default): TLS via rustls
- **native-tls**: OS-native TLS
- **json**: serde_json integration (send_json, read_json)
- **gzip**: Automatic gzip decompression
- **cookies**: Cookie jar support
- **charset**: Non-UTF-8 charset handling

## Quick Reference

| Operation | Code |
|-----------|------|
| GET | `ureq::get(url).call()?` |
| POST JSON | `agent.post(url).send_json(&body)?` |
| Add header | `.header("Key", "value")` |
| Read JSON | `resp.into_body().read_json::<T>()` |
| Read string | `resp.into_body().read_to_string()` |
| Get reader | `resp.into_body().into_reader()` |
| Status code | `resp.status()` |
| Set timeout | `Agent::config_builder().timeout_global(...)` |
