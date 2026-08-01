---
name: openclaw-config
description: 本文档定义了 OpenClaw 配置的标准规范，确保所有配置修改都正确、安全、可追溯。
---

# OpenClaw 配置全局规范

## 概述

本文档定义了 OpenClaw 配置的标准规范，确保所有配置修改都正确、安全、可追溯。

**版本**: OpenClaw 2026.2.1
**最后更新**: 2026-02-02

---

## 📁 配置文件结构

### 主要配置文件

| 文件路径 | 用途 | 格式 |
|---------|------|------|
| `~/.openclaw/openclaw.json` | 主配置文件 | JSON5 |
| `~/.openclaw/agents/main/agent/models.json` | Agent 模型配置 | JSON |
| `~/.openclaw/agents/main/agent/auth-profiles.json` | API 密钥和认证 | JSON |
| `~/.openclaw/agents/main/agent/agent.json` | Agent 特定配置 | JSON |

### 配置文件层级

```
~/.openclaw/
├── openclaw.json              # 主配置（Gateway + Channels + Agents）
├── .env                       # 环境变量（可选）
├── agents/
│   └── main/
│       └── agent/
│           ├── models.json        # 模型定义
│           ├── auth-profiles.json # 认证配置
│           └── agent.json         # Agent 配置
├── credentials/
│   └── whatsapp/              # WhatsApp 认证
└── logs/                      # 日志目录
```

---

## 🔧 配置修改方法

### 方法 1: CLI 命令（推荐）

```bash
# 查看配置
openclaw config get <path>

# 设置配置
openclaw config set <path> <value>

# 删除配置
openclaw config unset <path>

# 模型相关
openclaw models set <provider/model>
openclaw models fallbacks add <provider/model>
openclaw models aliases set <alias> <provider/model>
```

### 方法 2: Gateway RPC

```bash
# 获取配置（包含 hash）
openclaw gateway call config.get --params '{}'

# 部分更新（推荐）
openclaw gateway call config.patch --params '{
  "raw": "{ channels: { telegram: { enabled: true } } }",
  "baseHash": "<hash-from-config.get>"
}'

# 完整替换（谨慎使用）
openclaw gateway call config.apply --params '{
  "raw": "<完整配置>",
  "baseHash": "<hash>"
}'
```

### 方法 3: 直接编辑文件

⚠️ **注意事项**：
1. 编辑前备份：`cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak`
2. 使用 JSON5 格式（支持注释和尾逗号）
3. 编辑后验证：`openclaw doctor`
4. 重启生效：`openclaw gateway restart`

---

## 📋 配置结构规范

### 完整配置模板

```json5
{
  // 元数据（自动管理）
  "meta": {
    "lastTouchedVersion": "2026.2.1",
    "lastTouchedAt": "2026-02-02T12:00:00.000Z"
  },

  // 环境变量
  "env": {
    "vars": {
      "OPENROUTER_VIP_API_KEY": "sk-xxx",
      "ZAI_API_KEY": "xxx"
    }
  },

  // 认证配置
  "auth": {
    "profiles": {
      "github-copilot:github": {
        "provider": "github-copilot",
        "mode": "token"
      },
      "zai:default": {
        "provider": "zai",
        "mode": "api_key"
      }
    }
  },

  // 模型配置
  "models": {
    "mode": "merge",
    "providers": {
      "<provider-name>": {
        "baseUrl": "https://api.example.com",
        "apiKey": "sk-xxx",
        "auth": "api-key",           // api-key | oauth | token
        "api": "anthropic-messages", // anthropic-messages | openai-completions
        "models": [
          {
            "id": "model-id",
            "name": "Display Name",
            "reasoning": false,
            "input": ["text"],       // text | image
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  },

  // Agent 配置
  "agents": {
    "defaults": {
      "model": {
        "primary": "provider/model",
        "fallbacks": ["provider/model2", "provider/model3"]
      },
      "models": {
        "provider/model": {
          "alias": "shortname"
        }
      },
      "workspace": "/home/aa/clawd",
      "compaction": {
        "mode": "safeguard"
      },
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 8
      }
    }
  },

  // 消息配置
  "messages": {
    "ackReactionScope": "group-mentions",
    "queue": {
      "mode": "collect",
      "debounceMs": 1000,
      "cap": 20
    }
  },

  // 命令配置
  "commands": {
    "native": "auto",
    "nativeSkills": "auto"
  },

  // 钩子配置
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "boot-md": { "enabled": true },
        "command-logger": { "enabled": true },
        "session-memory": { "enabled": true }
      }
    }
  },

  // 通道配置
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "selfChatMode": true,
      "allowFrom": ["+xxx"],
      "groupPolicy": "allowlist",
      "mediaMaxMb": 50
    },
    "telegram": {
      "enabled": true,
      "dmPolicy": "allowlist",
      "botToken": "xxx:xxx",
      "allowFrom": ["user_id"],
      "groupPolicy": "allowlist",
      "streamMode": "partial"
    }
  },

  // Gateway 配置
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "xxx"
    },
    "tailscale": {
      "mode": "off",
      "resetOnExit": false
    }
  },

  // Skills 配置
  "skills": {
    "install": {
      "nodeManager": "npm"
    }
  },

  // 插件配置
  "plugins": {
    "entries": {
      "whatsapp": { "enabled": true },
      "telegram": { "enabled": true }
    }
  }
}
```

---

## 🎯 常用配置操作

### 1. 切换默认模型

```bash
# CLI 方式（推荐）
openclaw models set anapi/opus-4.5

# 验证
openclaw models status
```

### 2. 添加模型别名

```bash
openclaw models aliases set opus45 anapi/opus-4.5
```

### 3. 配置模型降级列表

```bash
openclaw models fallbacks add zai/glm-4.7
openclaw models fallbacks add github-copilot/claude-sonnet-4-5
```

### 4. 添加新的模型供应商

在 `~/.openclaw/openclaw.json` 的 `models.providers` 中添加：

```json5
"<provider-name>": {
  "baseUrl": "https://api.example.com",
  "apiKey": "sk-xxx",
  "auth": "api-key",
  "api": "anthropic-messages",  // 或 "openai-completions"
  "models": [
    {
      "id": "model-id",
      "name": "Model Name",
      "reasoning": false,
      "input": ["text"],
      "contextWindow": 200000,
      "maxTokens": 8192
    }
  ]
}
```

### 5. 配置 Telegram

```json5
"channels": {
  "telegram": {
    "enabled": true,
    "botToken": "BOT_TOKEN",
    "dmPolicy": "allowlist",
    "allowFrom": ["USER_ID"],
    "groupPolicy": "allowlist",
    "streamMode": "partial"
  }
}
```

### 6. 配置 WhatsApp

```json5
"channels": {
  "whatsapp": {
    "dmPolicy": "allowlist",
    "selfChatMode": true,
    "allowFrom": ["+PHONE_NUMBER"],
    "groupPolicy": "allowlist",
    "mediaMaxMb": 50
  }
}
```

---

## ⚠️ 配置修改检查清单

在修改任何配置前，必须确认：

### 修改前
- [ ] 备份当前配置
- [ ] 确认修改的配置路径正确
- [ ] 确认值的格式正确（字符串/数字/布尔/数组/对象）

### 修改时
- [ ] 使用正确的 JSON5 语法
- [ ] API 密钥不要暴露在日志中
- [ ] 敏感信息使用环境变量引用 `${VAR_NAME}`

### 修改后
- [ ] 运行 `openclaw doctor` 验证配置
- [ ] 运行 `openclaw gateway restart` 重启生效
- [ ] 验证功能正常工作
- [ ] 告知用户修改内容

---

## 🔐 敏感信息处理

### API 密钥存储位置

| 类型 | 存储位置 |
|------|---------|
| 模型 API Key | `~/.openclaw/openclaw.json` → `models.providers.<name>.apiKey` |
| OAuth Token | `~/.openclaw/agents/main/agent/auth-profiles.json` |
| 环境变量 | `~/.openclaw/.env` 或 `env.vars` |

### 环境变量引用

```json5
{
  "models": {
    "providers": {
      "custom": {
        "apiKey": "${CUSTOM_API_KEY}"
      }
    }
  }
}
```

---

## 🛠️ 故障排查

### 配置验证失败

```bash
# 查看详细错误
openclaw doctor

# 自动修复
openclaw doctor --fix
```

### Gateway 无法启动

```bash
# 检查状态
openclaw gateway status

# 查看日志
openclaw logs

# 强制重启
openclaw gateway restart --force
```

### 模型不可用

```bash
# 检查模型状态
openclaw models status

# 检查认证
openclaw models auth status
```

---

## 📝 配置变更记录模板

每次修改配置时，记录以下信息：

```markdown
### 配置变更 - YYYY-MM-DD HH:MM

**修改内容**:
- 修改了 xxx

**修改原因**:
- 因为 xxx

**影响范围**:
- 影响 xxx 功能

**验证结果**:
- [ ] doctor 通过
- [ ] 功能测试通过

**回滚方法**:
- 恢复备份：`cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json`
```

---

## 📚 参考资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [配置示例](https://docs.openclaw.ai/gateway/configuration-examples)
- [模型供应商](https://docs.openclaw.ai/providers)
- [通道配置](https://docs.openclaw.ai/channels)

---

## 🔄 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-02-02 | 初始版本 |

---

*本规范由小a维护，确保所有配置修改都正确、安全、可追溯。*
