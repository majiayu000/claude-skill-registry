---
name: deepseek-integration
description: 当用户要求"DeepSeek API 集成"、"AI 服务"、"生成回复建议"、"调用 LLM"、"HTTP 请求"、"流式响应"、"连接池优化"、"重试策略"，或者提到"DeepSeek"、"API 调用"、"reqwest"、"streaming"时使用此技能。用于 DeepSeek API 集成、HTTP 客户端配置、错误处理、流式响应、连接池优化和 API 密钥管理。
version: 1.0.0
---

# DeepSeek Integration Skill

Expert guidance for integrating DeepSeek API with reqwest HTTP client, streaming responses, and error handling.

## Overview

WeReply uses DeepSeek API to generate reply suggestions:
- **HTTP Client**: reqwest with connection pooling
- **API Endpoint**: `https://api.deepseek.com/v1/chat/completions`
- **Authentication**: API key via Bearer token
- **Response Format**: JSON (non-streaming) or Server-Sent Events (streaming)
- **Configuration**: API key stored in system keychain

## HTTP Client Configuration

### Reqwest Client Setup

```rust
use reqwest::{Client, ClientBuilder};
use std::time::Duration;
use std::sync::Arc;

pub struct DeepSeekClient {
    client: Arc<Client>,
    api_key: String,
    api_endpoint: String,
}

impl DeepSeekClient {
    pub fn new(api_key: String) -> anyhow::Result<Self> {
        let client = ClientBuilder::new()
            .pool_max_idle_per_host(10)  // 连接池最大空闲连接数
            .timeout(Duration::from_secs(30))  // 请求超时30秒
            .connect_timeout(Duration::from_secs(10))  // 连接超时10秒
            .build()?;

        Ok(Self {
            client: Arc::new(client),
            api_key,
            api_endpoint: "https://api.deepseek.com/v1/chat/completions".to_string(),
        })
    }

    pub fn with_custom_endpoint(mut self, endpoint: String) -> Self {
        self.api_endpoint = endpoint;
        self
    }
}
```

### Connection Pooling Best Practices

```rust
// ✓ 共享 Client 实例（连接池复用）
pub struct AppState {
    deepseek_client: Arc<DeepSeekClient>,
}

// ✗ 每次创建新 Client（无连接池复用）
pub async fn bad_example() {
    let client = DeepSeekClient::new(api_key).unwrap();  // 不要这样做
}
```

## API Request Pattern

### Basic Request/Response

```rust
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
pub struct ChatCompletionRequest {
    model: String,
    messages: Vec<ChatMessage>,
    #[serde(skip_serializing_if = "Option::is_none")]
    temperature: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    max_tokens: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    stream: Option<bool>,
}

#[derive(Serialize, Deserialize)]
pub struct ChatMessage {
    role: String,  // "system", "user", "assistant"
    content: String,
}

#[derive(Deserialize)]
pub struct ChatCompletionResponse {
    id: String,
    model: String,
    choices: Vec<ChatChoice>,
    usage: Usage,
}

#[derive(Deserialize)]
pub struct ChatChoice {
    index: u32,
    message: ChatMessage,
    finish_reason: String,
}

#[derive(Deserialize)]
pub struct Usage {
    prompt_tokens: u32,
    completion_tokens: u32,
    total_tokens: u32,
}
```

### Making API Requests

```rust
impl DeepSeekClient {
    pub async fn generate_completion(
        &self,
        messages: Vec<ChatMessage>,
    ) -> anyhow::Result<ChatCompletionResponse> {
        let request = ChatCompletionRequest {
            model: "deepseek-chat".to_string(),
            messages,
            temperature: Some(0.7),
            max_tokens: Some(1000),
            stream: Some(false),
        };

        let response = self.client
            .post(&self.api_endpoint)
            .header("Authorization", format!("Bearer {}", self.api_key))
            .header("Content-Type", "application/json")
            .json(&request)
            .send()
            .await?;

        // 检查 HTTP 状态码
        if !response.status().is_success() {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            return Err(anyhow!(
                "DeepSeek API 请求失败: {} - {}",
                status,
                error_text
            ));
        }

        // 解析响应
        let completion = response.json::<ChatCompletionResponse>().await?;

        Ok(completion)
    }
}
```

## Streaming Response Pattern

### Event Stream Processing

```rust
use futures::stream::StreamExt;
use serde_json;

impl DeepSeekClient {
    pub async fn generate_completion_stream(
        &self,
        messages: Vec<ChatMessage>,
        on_chunk: impl Fn(String) + Send + 'static,
    ) -> anyhow::Result<String> {
        let request = ChatCompletionRequest {
            model: "deepseek-chat".to_string(),
            messages,
            temperature: Some(0.7),
            max_tokens: Some(1000),
            stream: Some(true),  // 启用流式响应
        };

        let response = self.client
            .post(&self.api_endpoint)
            .header("Authorization", format!("Bearer {}", self.api_key))
            .header("Content-Type", "application/json")
            .json(&request)
            .send()
            .await?;

        if !response.status().is_success() {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            return Err(anyhow!(
                "DeepSeek API 请求失败: {} - {}",
                status,
                error_text
            ));
        }

        let mut stream = response.bytes_stream();
        let mut full_content = String::new();
        let mut buffer = String::new();

        while let Some(chunk_result) = stream.next().await {
            let chunk = chunk_result?;
            let chunk_str = String::from_utf8_lossy(&chunk);

            buffer.push_str(&chunk_str);

            // 处理 SSE 格式：data: {...}\n\ndata: {...}\n\n
            for line in buffer.lines() {
                if line.starts_with("data: ") {
                    let json_str = &line[6..];  // 去掉 "data: " 前缀

                    if json_str == "[DONE]" {
                        break;
                    }

                    if let Ok(chunk_data) = serde_json::from_str::<StreamChunk>(json_str) {
                        if let Some(choice) = chunk_data.choices.first() {
                            if let Some(content) = &choice.delta.content {
                                full_content.push_str(content);
                                on_chunk(content.clone());
                            }
                        }
                    }
                }
            }

            buffer.clear();
        }

        Ok(full_content)
    }
}

#[derive(Deserialize)]
struct StreamChunk {
    choices: Vec<StreamChoice>,
}

#[derive(Deserialize)]
struct StreamChoice {
    delta: Delta,
    finish_reason: Option<String>,
}

#[derive(Deserialize)]
struct Delta {
    #[serde(skip_serializing_if = "Option::is_none")]
    content: Option<String>,
}
```

### Tauri Event Integration

```rust
use tauri::Manager;

#[tauri::command]
#[specta::specta]
pub async fn generate_suggestions_stream(
    context_messages: Vec<String>,
    style: String,
    state: State<'_, AppState>,
    app_handle: tauri::AppHandle,
) -> ApiResponse<String> {
    let client = state.deepseek_client.clone();

    // 构建消息
    let messages = build_chat_messages(context_messages, style);

    // 流式生成，实时发送到前端
    match client.generate_completion_stream(messages, move |chunk| {
        // 发送 chunk 到前端
        app_handle.emit_all("suggestion-chunk", chunk).ok();
    }).await {
        Ok(full_text) => api_ok(full_text),
        Err(e) => api_err(format!("生成建议失败: {}", e)),
    }
}
```

## Error Handling and Retry

### Exponential Backoff Retry

```rust
use tokio::time::{sleep, Duration};

impl DeepSeekClient {
    pub async fn generate_completion_with_retry(
        &self,
        messages: Vec<ChatMessage>,
        max_retries: u32,
    ) -> anyhow::Result<ChatCompletionResponse> {
        let mut retry_count = 0;
        let mut backoff_ms = 1000;  // 初始退避时间 1 秒

        loop {
            match self.generate_completion(messages.clone()).await {
                Ok(response) => return Ok(response),
                Err(e) => {
                    retry_count += 1;

                    if retry_count > max_retries {
                        return Err(anyhow!(
                            "DeepSeek API 调用失败，已重试 {} 次: {}",
                            max_retries,
                            e
                        ));
                    }

                    // 判断是否可重试的错误
                    if !is_retryable_error(&e) {
                        return Err(e);
                    }

                    tracing::warn!(
                        error = %e,
                        retry_count = retry_count,
                        backoff_ms = backoff_ms,
                        "DeepSeek API 调用失败，等待重试"
                    );

                    // 指数退避
                    sleep(Duration::from_millis(backoff_ms)).await;
                    backoff_ms = (backoff_ms * 2).min(30000);  // 最大退避 30 秒
                }
            }
        }
    }
}

fn is_retryable_error(error: &anyhow::Error) -> bool {
    let error_msg = error.to_string().to_lowercase();

    // 网络错误、超时、429 (Rate Limit)、5xx 服务器错误可重试
    error_msg.contains("timeout")
        || error_msg.contains("network")
        || error_msg.contains("429")
        || error_msg.contains("500")
        || error_msg.contains("502")
        || error_msg.contains("503")
        || error_msg.contains("504")
}
```

### Error Classification

```rust
#[derive(Debug, thiserror::Error)]
pub enum DeepSeekError {
    #[error("API 密钥无效")]
    InvalidApiKey,

    #[error("请求超时")]
    Timeout,

    #[error("请求频率超限")]
    RateLimitExceeded,

    #[error("服务不可用")]
    ServiceUnavailable,

    #[error("网络错误: {0}")]
    NetworkError(String),

    #[error("响应解析错误: {0}")]
    ParseError(String),

    #[error("未知错误: {0}")]
    Unknown(String),
}

impl DeepSeekClient {
    fn classify_error(status_code: u16, body: &str) -> DeepSeekError {
        match status_code {
            401 => DeepSeekError::InvalidApiKey,
            408 | 504 => DeepSeekError::Timeout,
            429 => DeepSeekError::RateLimitExceeded,
            500 | 502 | 503 => DeepSeekError::ServiceUnavailable,
            _ => DeepSeekError::Unknown(body.to_string()),
        }
    }
}
```

## Message Construction Pattern

### Building Chat Messages

```rust
pub fn build_chat_messages(
    context_messages: Vec<String>,
    style: &str,
) -> Vec<ChatMessage> {
    let mut messages = Vec::new();

    // 系统提示词
    let system_prompt = format!(
        "你是一个微信回复建议助手。请根据聊天上下文，用{}风格生成3条简短的回复建议。\
        每条建议不超过50字，自然流畅，符合微信聊天习惯。",
        get_style_description(style)
    );

    messages.push(ChatMessage {
        role: "system".to_string(),
        content: system_prompt,
    });

    // 聊天上下文
    let context = context_messages.join("\n");
    messages.push(ChatMessage {
        role: "user".to_string(),
        content: format!("聊天记录：\n{}\n\n请生成3条回复建议：", context),
    });

    messages
}

fn get_style_description(style: &str) -> &str {
    match style {
        "formal" => "正式、礼貌",
        "friendly" => "亲切、友好",
        "humorous" => "幽默、轻松",
        _ => "自然、随和",
    }
}
```

### Response Parsing

```rust
pub fn parse_suggestions(response_text: &str) -> Vec<String> {
    // DeepSeek 可能返回带编号的列表，如：
    // 1. 建议1
    // 2. 建议2
    // 3. 建议3

    let mut suggestions = Vec::new();

    for line in response_text.lines() {
        let trimmed = line.trim();

        // 匹配带编号的建议（如 "1. xxx" 或 "1) xxx"）
        if let Some(content) = trimmed.strip_prefix(|c: char| c.is_numeric()) {
            if let Some(content) = content.strip_prefix(". ").or(content.strip_prefix(") ")) {
                suggestions.push(content.trim().to_string());
            }
        }
    }

    // 如果没找到带编号的建议，尝试按换行分割
    if suggestions.is_empty() {
        suggestions = response_text
            .lines()
            .map(|l| l.trim().to_string())
            .filter(|l| !l.is_empty())
            .collect();
    }

    suggestions
}
```

## Configuration Management

### API Key from System Keychain

```rust
use keyring::Entry;

pub fn get_deepseek_api_key() -> anyhow::Result<String> {
    let entry = Entry::new("wereply", "deepseek_api_key")?;
    entry.get_password()
        .context("未找到 DeepSeek API 密钥，请在设置中配置")
}

pub fn set_deepseek_api_key(api_key: &str) -> anyhow::Result<()> {
    let entry = Entry::new("wereply", "deepseek_api_key")?;
    entry.set_password(api_key)?;
    Ok(())
}
```

### Environment Variable Fallback

```rust
use std::env;

pub fn get_api_endpoint() -> String {
    env::var("DEEPSEEK_API_ENDPOINT")
        .unwrap_or_else(|_| "https://api.deepseek.com/v1/chat/completions".to_string())
}

pub fn get_model_name() -> String {
    env::var("DEEPSEEK_MODEL")
        .unwrap_or_else(|_| "deepseek-chat".to_string())
}
```

## Testing

### Mock HTTP Client

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use mockito::{mock, server_url};

    #[tokio::test]
    async fn test_generate_completion() {
        // 模拟 DeepSeek API 响应
        let _m = mock("POST", "/v1/chat/completions")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{
                "id": "chatcmpl-123",
                "model": "deepseek-chat",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "1. 好的，谢谢！\n2. 收到，马上处理。\n3. 了解，没问题。"
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": 20,
                    "completion_tokens": 30,
                    "total_tokens": 50
                }
            }"#)
            .create();

        let client = DeepSeekClient::new("test_api_key".to_string())
            .unwrap()
            .with_custom_endpoint(server_url());

        let messages = vec![
            ChatMessage {
                role: "user".to_string(),
                content: "测试消息".to_string(),
            },
        ];

        let response = client.generate_completion(messages).await.unwrap();

        assert_eq!(response.model, "deepseek-chat");
        assert_eq!(response.choices.len(), 1);
        assert!(response.choices[0].message.content.contains("好的"));
    }

    #[tokio::test]
    async fn test_retry_on_error() {
        // 模拟失败后成功的情况
        let _m1 = mock("POST", "/v1/chat/completions")
            .with_status(503)
            .with_body("Service Unavailable")
            .create();

        let _m2 = mock("POST", "/v1/chat/completions")
            .with_status(200)
            .with_body(r#"{"id": "test", "choices": []}"#)
            .create();

        let client = DeepSeekClient::new("test_key".to_string())
            .unwrap()
            .with_custom_endpoint(server_url());

        let messages = vec![];
        let result = client.generate_completion_with_retry(messages, 3).await;

        assert!(result.is_ok());
    }
}
```

## Performance Optimization

### Request Timeout Configuration

```rust
pub struct DeepSeekConfig {
    pub connect_timeout_secs: u64,
    pub request_timeout_secs: u64,
    pub max_retries: u32,
}

impl Default for DeepSeekConfig {
    fn default() -> Self {
        Self {
            connect_timeout_secs: 10,
            request_timeout_secs: 30,
            max_retries: 3,
        }
    }
}
```

### Batch Request Processing

```rust
use futures::future::join_all;

pub async fn generate_multiple_suggestions(
    &self,
    requests: Vec<Vec<ChatMessage>>,
) -> Vec<anyhow::Result<ChatCompletionResponse>> {
    // 并发处理多个请求
    let futures = requests.into_iter().map(|messages| {
        let client = self.clone();
        async move {
            client.generate_completion(messages).await
        }
    });

    join_all(futures).await
}
```

## Security Best Practices

### API Key Validation

```rust
pub fn validate_api_key(api_key: &str) -> anyhow::Result<()> {
    if api_key.is_empty() {
        return Err(anyhow!("API 密钥不能为空"));
    }

    if !api_key.starts_with("sk-") {
        return Err(anyhow!("API 密钥格式错误"));
    }

    if api_key.len() < 20 {
        return Err(anyhow!("API 密钥长度不足"));
    }

    Ok(())
}
```

### Logging Without Sensitive Data

```rust
use tracing::info;

pub async fn log_api_call(
    &self,
    message_count: usize,
    response_length: usize,
) {
    info!(
        message_count = message_count,
        response_length = response_length,
        "DeepSeek API 调用成功"
    );
    // ❌ 不要记录 API 密钥或消息内容
}
```

## When to Use This Skill

Activate this skill when:
- Integrating DeepSeek API
- Implementing AI-powered features
- Working with HTTP clients (reqwest)
- Handling streaming responses
- Implementing retry logic
- Managing API keys securely
- Optimizing API performance
- Testing API integrations
