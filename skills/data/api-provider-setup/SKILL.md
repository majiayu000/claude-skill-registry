---
name: api-provider-setup
description: 添加和配置第三方 API 中转站供应商到 OpenClaw。当用户需要添加新的 API 供应商、配置中转站、设置自定义模型端点时使用此技能。支持 Anthropic 兼容和 OpenAI 兼容的 API 格式。
---

# API Provider Setup

为 OpenClaw 添加和配置第三方 API 中转站供应商。

## 配置位置

配置文件：`~/.openclaw/openclaw.json`

在 `models.providers` 部分添加自定义供应商。

## 配置模板

### Anthropic 兼容 API（如 anapi、智谱）

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "供应商名称": {
        "baseUrl": "https://api.example.com",
        "apiKey": "sk-your-api-key",
        "auth": "api-key",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "model-id",
            "name": "显示名称",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 8192,
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          }
        ]
      }
    }
  }
}
```

### OpenAI 兼容 API（如 OpenRouter）

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "供应商名称": {
        "baseUrl": "https://api.example.com/v1",
        "apiKey": "sk-your-api-key",
        "auth": "api-key",
        "api": "openai-completions",
        "models": [
          {
            "id": "gpt-4",
            "name": "GPT-4",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

## 关键字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `baseUrl` | ✅ | API 端点地址（不含 /v1/messages 等路径） |
| `apiKey` | ✅ | API 密钥 |
| `auth` | ✅ | 认证方式，通常为 `api-key` |
| `api` | ✅ | API 格式：`anthropic-messages` 或 `openai-completions` |
| `models` | ✅ | 该供应商支持的模型列表 |
| `models[].id` | ✅ | 模型 ID（调用时使用） |
| `models[].name` | ❌ | 显示名称 |
| `models[].contextWindow` | ❌ | 上下文窗口大小 |
| `models[].maxTokens` | ❌ | 最大输出 token 数 |
| `models[].reasoning` | ❌ | 是否支持推理模式 |

## 添加模型别名

在 `agents.defaults.models` 中添加别名：

```json
{
  "agents": {
    "defaults": {
      "models": {
        "供应商/模型id": {
          "alias": "简短别名"
        }
      }
    }
  }
}
```

## 设置为默认模型

在 `agents.defaults.model` 中设置：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "供应商/模型id",
        "fallbacks": [
          "备选供应商1/模型id",
          "备选供应商2/模型id"
        ]
      }
    }
  }
}
```

## 添加流程

1. **获取供应商信息**
   - Base URL
   - API Key
   - API 格式（Anthropic 或 OpenAI 兼容）
   - 支持的模型列表

2. **使用 gateway config.patch 添加**
   ```
   gateway config.patch 添加供应商配置
   ```

3. **重启 Gateway 生效**
   ```
   gateway restart
   ```

4. **测试新模型**
   ```
   session_status(model="新供应商/模型id")
   ```

## 常见中转站配置示例

### Anapi (Anthropic 中转)
```json
"anapi": {
  "baseUrl": "https://anapi.9w7.cn",
  "apiKey": "sk-xxx",
  "auth": "api-key",
  "api": "anthropic-messages",
  "models": [{"id": "opus-4.5", "name": "Opus 4.5", "contextWindow": 200000}]
}
```

### 智谱 ZAI
```json
"zai": {
  "baseUrl": "https://open.bigmodel.cn/api/anthropic",
  "apiKey": "xxx.xxx",
  "auth": "api-key",
  "api": "anthropic-messages",
  "models": [{"id": "glm-4.7", "name": "GLM-4.7", "contextWindow": 200000}]
}
```

### OpenRouter VIP
```json
"openrouter-vip": {
  "baseUrl": "https://openrouter.vip/v1",
  "apiKey": "sk-xxx",
  "auth": "api-key",
  "api": "openai-completions",
  "models": [{"id": "gpt-5.2", "name": "GPT-5.2", "contextWindow": 200000}]
}
```

## 故障排查

1. **401 Unauthorized** - API Key 错误或过期
2. **404 Not Found** - baseUrl 路径错误
3. **模型不存在** - 检查 models[].id 是否正确
4. **格式错误** - 检查 api 字段是否匹配供应商的 API 格式
