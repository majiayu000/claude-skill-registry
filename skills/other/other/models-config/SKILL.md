---
name: models-config
description: Model configuration editor for ~/.pi/agent/models.json with multi-protocol curl testing support.

---

# Models Config Skill

## 功能

编辑和管理 `~/.pi/agent/models.json` 配置文件，支持多种 API 协议的测试和验证，以及从 https://models.dev/api.json 自动获取模型价格信息。

## 配置结构

```json
{
  "providers": {
    "provider-name": {
      "baseUrl": "https://api.example.com",
      "apiKey": "sk-xxx",
      "api": "anthropic-messages|openai-completions|openai-responses",
      "authHeader": true
    }
  }
}
```

## 使用方法

### 基本操作

```bash
# 编辑配置文件
bat ~/.pi/agent/models.json

# 验证 JSON 格式
python3 -m json.tool ~/.pi/agent/models.json
```

### 协议类型

| API 类型 | 用途 | 端点格式 |
|---------|------|---------|
| `anthropic-messages` | Claude 消息 API | `/v1/messages` |
| `openai-completions` | OpenAI Completions API | `/v1/chat/completions` |
| `openai-responses` | OpenAI Responses API | `/v1/responses` |

## 测试方法

### 1. Anthropic Messages API

```bash
export ANTHROPIC_BASE_URL=https://api.xairouter.com
export ANTHROPIC_AUTH_TOKEN=sk-XvsJhNdiXcDYA3e5hzD1AJP5ploMAaFuMTUxp3bHRfCiZRNt

curl $ANTHROPIC_BASE_URL/v1/messages \
  -H "x-api-key: $ANTHROPIC_AUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### 2. OpenAI Completions API (Chat)

```bash
export OPENAI_BASE_URL=http://127.0.0.1:8317/v1
export OPENAI_API_KEY=proxypal-local

curl $OPENAI_BASE_URL/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "model": "glm-4.7",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### 3. OpenAI Responses API

```bash
export OPENAI_BASE_URL=http://127.0.0.1:8317/v1
export OPENAI_API_KEY=proxypal-local

curl $OPENAI_BASE_URL/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "model": "glm-4.7",
    "input": "Hello"
  }'
```

### 4. 简化测试脚本

```bash
#!/usr/bin/env bash
# test-model.sh

PROVIDER=$1
BASE_URL=$2
API_KEY=$3
MODEL=$4

echo "Testing $PROVIDER with model $MODEL..."

case "$PROVIDER" in
  anthropic)
    curl -s "$BASE_URL/v1/messages" \
      -H "x-api-key: $API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d "{\"model\":\"$MODEL\",\"max_tokens\":256,\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}]}" \
      | jq .
    ;;
  openai-chat)
    curl -s "$BASE_URL/chat/completions" \
      -H "Authorization: Bearer $API_KEY" \
      -H "content-type: application/json" \
      -d "{\"model\":\"$MODEL\",\"max_tokens\":256,\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}]}" \
      | jq .
    ;;
  openai-responses)
    curl -s "$BASE_URL/responses" \
      -H "Authorization: Bearer $API_KEY" \
      -H "content-type: application/json" \
      -d "{\"model\":\"$MODEL\",\"input\":\"Hi\"}" \
      | jq .
    ;;
esac
```

**使用示例：**

```bash
# 测试 Anthropic
bash test-model.sh anthropic \
  https://api.xairouter.com \
  sk-XvsJhNdiXcDYA3e5hzD1AJP5ploMAaFuMTUxp3bHRfCiZRNt \
  claude-sonnet-4-5

# 测试 OpenAI Chat
bash test-model.sh openai-chat \
  http://127.0.0.1:8317/v1 \
  proxypal-local \
  glm-4.7
```

## 常见配置

### 本地服务 (ProxyPal)

```json
{
  "proxypal": {
    "baseUrl": "http://127.0.0.1:8317/v1",
    "apiKey": "proxypal-local",
    "api": "openai-completions",
    "authHeader": true
  }
}
```

### Cloud 服务 (xAIRouter)

```json
{
  "xairouter": {
    "baseUrl": "https://api.xairouter.com",
    "apiKey": "sk-xxx",
    "api": "anthropic-messages",
    "authHeader": true
  }
}
```

### Ngrok 隧道

```json
{
  "ngrok": {
    "baseUrl": "https://xxx.ngrok-free.dev/v1",
    "apiKey": "proxypal-local",
    "api": "openai-responses",
    "authHeader": true
  }
}
```

## 价格更新功能

从 https://models.dev/api.json 获取模型价格并更新到配置文件。

### 使用方法

```bash
# 更新所有模型价格
bun ~/.pi/agent/skills/models-config/update-prices.ts
```

### 工作原理

1. 从 https://models.dev/api.json 获取最新价格数据
2. 读取 `~/.pi/agent/models.json` 配置文件
3. 按 model ID 智能匹配价格信息
4. 更新 cost 字段（input/output/cacheRead/cacheWrite）
5. 显示更新摘要

### 匹配规则

**优先级（从高到低）：**

1. **精确匹配**：model ID 完全相同
2. **标准化匹配**：去除前缀、版本号后相同
   - `anthropic/claude-sonnet-4-5` → `claude-sonnet-4-5`
   - `claude-sonnet-4-5-20250929` → `claude-sonnet-4-5`
3. **模糊匹配**：基于 Levenshtein 距离的相似度匹配（≥70%）
   - 自动匹配最佳相似度的模型
   - 显示匹配相似度百分比

**支持的别名映射：**

| 你的模型 ID | 匹配到 |
|------------|--------|
| `opus4.5` | `claude-opus-4-5` |
| `claude-sonnet-4-5-20250929` | `claude-sonnet-4-5` |
| `claude-haiku-4-5-20251001` | `claude-haiku-4-5` |
| `z-ai/glm4.7` | `glm-4.7` |
| `minimaxai/minimax-m2.1` | `minimax-m2.1` |

### 模糊匹配示例

即使你的供应商不在 models.dev 中，只要模型名称相似，也会自动匹配：

```bash
bun ~/.pi/agent/skills/models-config/update-prices.ts

# 输出示例：
✓ Updated: claude-sonnet-4-5
  Old: {"input":0,"output":0,"cacheRead":0,"cacheWrite":0}
  New: {"input":2.6,"output":13,"cacheRead":0.26,"cacheWrite":3.2}
✓ Updated: glm-4.7
  Fuzzy matched "glm-4.7" -> "zai-glm-4.7" (85.7% similarity)
  Old: {"input":0,"output":0,"cacheRead":0,"cacheWrite":0}
  New: {"input":0,"output":0,"cacheRead":0,"cacheWrite":0}

=== Summary ===
Updated: 15 models
Not found: 3 models

Models without price data:
  - custom-model-x
  - experimental-beta
```

## 注意事项

1. **baseUrl 格式**：
   - `anthropic-messages`: 不需要 `/v1` 后缀
   - `openai-*`: 通常需要 `/v1` 后缀

2. **认证方式**：
   - Anthropic: `x-api-key` header
   - OpenAI: `Authorization: Bearer` header

3. **测试前检查**：
   - 确认服务端口已启动（如 `curl http://127.0.0.1:8317`）
   - 检查 API Key 有效性
   - 验证网络连通性

4. **价格更新**：
   - 模糊匹配阈值：70% 相似度
   - 匹配成功会显示相似度百分比
   - 未匹配的模型会在摘要中列出
   - 价格单位：美元/百万 tokens ($/1M tokens)
