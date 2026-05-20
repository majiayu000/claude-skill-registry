---
name: model-fallback
description: 模型自动降级与故障切换。当主模型请求失败、超时、达到速率限制或配额耗尽时，自动切换到备用模型，确保服务连续性。支持多供应商、多优先级的智能模型选择，提供健康监控、自动重试和错误恢复机制。
allowed-tools: Bash, Read, Write, Edit, Exec
---

# 模型自动降级与故障切换

## 概述

本技能提供完整的模型自动降级和故障切换解决方案，确保在主模型不可用时自动切换到备用模型，维持 AI 助手的持续服务能力。

## 核心功能

### 1. 智能模型选择

根据任务类型和模型状态智能选择最合适的模型：

```yaml
优先级顺序:
  1. anapi/opus-4.5         # 最强能力，最高优先级
  2. zai/glm-4.7            # 中文优化，性价比高
  3. openrouter-vip/gpt-5.2-codex  # 编码专用
  4. github-copilot/claude-sonnet-4-5  # 免费备用
```

### 2. 故障检测与处理

自动检测以下故障并触发切换：

- **超时错误** (timeout): 请求超过设定时间
- **速率限制** (rate_limit): API 调用频率超限
- **配额耗尽** (quota_exceeded): token 配额用尽
- **认证错误** (authentication): API 密钥失效
- **服务不可用** (service_unavailable): 供应商服务故障
- **网络错误** (network_error): 连接失败

### 3. 重试机制

智能重试策略：

```yaml
重试配置:
  最大重试次数: 3
  初始延迟: 1000ms
  最大延迟: 10000ms
  退避倍数: 2.0
  使用备用模型: true
```

重试时间线：
```
第1次失败 → 等待 1s → 重试
第2次失败 → 等待 2s → 重试
第3次失败 → 等待 4s → 切换模型
```

### 4. 健康监控

持续监控所有模型供应商的健康状态：

```bash
# 每5分钟检查一次
检查项目:
  - API 端点连通性
  - 响应时间
  - 错误率
  - 配额使用情况
```

## 快速开始

### 1. 配置模型降级

配置文件：`~/.openclaw/agents/main/agent/agent.json`

```json
{
  "model": "anapi/opus-4.5",
  "modelFallback": [
    "zai/glm-4.7",
    "openrouter-vip/gpt-5.2-codex",
    "github-copilot/claude-sonnet-4-5"
  ],
  "retry": {
    "maxAttempts": 3,
    "initialDelayMs": 1000,
    "maxDelayMs": 10000,
    "backoffMultiplier": 2.0,
    "useFallbackOnFailure": true
  }
}
```

### 2. 启动监控

```bash
# 启动后台监控
~/.openclaw/scripts/monitor-models.sh start

# 查看监控状态
~/.openclaw/scripts/monitor-models.sh status

# 停止监控
~/.openclaw/scripts/monitor-models.sh stop
```

### 3. 手动触发切换

```bash
# 运行降级检查脚本
~/.openclaw/scripts/model-fallback.sh
```

## 工作流程

### 正常请求流程

```
用户请求
    ↓
选择主模型 (anapi/opus-4.5)
    ↓
发送请求到 API
    ↓
成功 → 返回结果
```

### 故障切换流程

```
用户请求
    ↓
选择当前模型
    ↓
发送请求 → 失败/超时
    ↓
重试 (最多3次)
    ↓
仍然失败?
    ↓
切换到备用模型 (zai/glm-4.7)
    ↓
发送请求
    ↓
成功 → 返回结果并记录
```

### 监控流程

```
监控守护进程 (每5分钟)
    ↓
检查所有模型健康状态
    ↓
├─ 主模型健康 → 保持当前
└─ 主模型不健康 → 切换到最佳可用模型
    ↓
更新状态文件
    ↓
记录日志
```

## 错误处理策略

### 1. 超时错误 (Timeout)

```json
{
  "timeout": {
    "switchModel": true,
    "retryCount": 2,
    "timeoutMs": 60000,
    "fallbackTo": "zai/glm-4.7"
  }
}
```

**行为**：
- 超过 60 秒视为超时
- 重试 2 次后仍超时则切换模型

### 2. 速率限制 (Rate Limit)

```json
{
  "rateLimit": {
    "switchModel": true,
    "cooldownMs": 60000,
    "alert": true,
    "fallbackTo": "zai/glm-4.7"
  }
}
```

**行为**：
- 收到 429 错误码
- 冷却 60 秒后尝试恢复
- 立即切换到备用模型

### 3. 配额耗尽 (Quota Exceeded)

```json
{
  "quotaExceeded": {
    "switchModel": true,
    "alert": true,
    "fallbackTo": "zai/glm-4.7",
    "checkInterval": 3600000
  }
}
```

**行为**：
- 配额用尽时切换模型
- 每小时检查一次主模型是否恢复
- 发送告警通知

### 4. 认证错误 (Authentication)

```json
{
  "authenticationError": {
    "switchModel": true,
    "alert": true,
    "disableModel": true
  }
}
```

**行为**：
- API 密钥失效时立即切换
- 禁用故障模型（不自动恢复）
- 发送紧急告警

## 智能路由规则

根据任务类型自动选择最合适的模型：

```json
{
  "routing": {
    "strategy": "priority-fallback",
    "rules": [
      {
        "name": "coding-task",
        "match": {
          "contentContains": ["代码", "code", "编程", "函数"]
        },
        "preferModels": [
          "openrouter-vip/gpt-5.2-codex",
          "anapi/opus-4.5"
        ]
      },
      {
        "name": "chinese-task",
        "match": {
          "language": "zh"
        },
        "preferModels": [
          "zai/glm-4.7",
          "anapi/opus-4.5"
        ]
      },
      {
        "name": "vision-task",
        "match": {
          "hasImage": true
        },
        "preferModels": [
          "anapi/opus-4.5"
        ]
      }
    ]
  }
}
```

## 监控与日志

### 日志文件位置

```bash
~/.openclaw/logs/model-fallback.log    # 切换日志
~/.openclaw/logs/model-monitor.log     # 监控日志
~/.openclaw/logs/model-status.json     # 状态报告
```

### 查看实时日志

```bash
# 查看切换日志
tail -f ~/.openclaw/logs/model-fallback.log

# 查看监控日志
tail -f ~/.openclaw/logs/model-monitor.log

# 查看所有日志
tail -f ~/.openclaw/logs/*.log
```

### 状态报告

```bash
# 查看当前状态
~/.openclaw/scripts/monitor-models.sh status

# JSON 格式状态
cat ~/.openclaw/logs/model-status.json | python3 -m json.tool
```

## 脚本说明

### model-fallback.sh

模型降级切换脚本，负责：
- 测试所有配置的模型
- 选择最佳可用模型
- 执行模型切换
- 记录切换日志

**用法**：
```bash
~/.openclaw/scripts/model-fallback.sh
```

### monitor-models.sh

健康监控守护进程，负责：
- 定期检查模型健康状态
- 自动触发故障切换
- 生成状态报告
- 管理 PID 文件

**用法**：
```bash
~/.openclaw/scripts/monitor-models.sh {start|stop|restart|status|check}
```

### test-model-fallback.sh

测试脚本，用于：
- 验证配置正确性
- 测试切换逻辑
- 模拟故障场景
- 生成测试报告

**用法**：
```bash
~/clawd/scripts/test-model-fallback.sh
```

## 配置文件详解

### agent.json 完整配置

```json
{
  "model": "anapi/opus-4.5",
  "modelFallback": [
    "zai/glm-4.7",
    "openrouter-vip/gpt-5.2-codex",
    "github-copilot/claude-sonnet-4-5"
  ],
  "retry": {
    "maxAttempts": 3,
    "initialDelayMs": 1000,
    "maxDelayMs": 10000,
    "backoffMultiplier": 2.0,
    "useFallbackOnFailure": true
  },
  "errorHandling": {
    "rateLimit": {
      "switchModel": true,
      "cooldownMs": 60000,
      "alert": true
    },
    "timeout": {
      "switchModel": true,
      "retryCount": 2,
      "timeoutMs": 60000
    },
    "quotaExceeded": {
      "switchModel": true,
      "alert": true,
      "fallbackTo": "zai/glm-4.7"
    },
    "authenticationError": {
      "switchModel": true,
      "alert": true,
      "disableModel": true
    }
  },
  "models": {
    "anapi/opus-4.5": {
      "provider": "anapi",
      "alias": "opus45",
      "maxTokens": 200000,
      "timeoutMs": 60000,
      "priority": 1,
      "supports": ["vision", "tools", "long-context"],
      "costFactor": "high"
    },
    "zai/glm-4.7": {
      "provider": "zai",
      "alias": "zai47",
      "maxTokens": 200000,
      "timeoutMs": 60000,
      "priority": 2,
      "supports": ["tools", "long-context"],
      "costFactor": "medium",
      "bestFor": ["chinese", "general-purpose"]
    },
    "openrouter-vip/gpt-5.2-codex": {
      "provider": "openrouter-vip",
      "alias": "codex52",
      "maxTokens": 100000,
      "timeoutMs": 30000,
      "priority": 3,
      "supports": ["coding"],
      "costFactor": "low",
      "bestFor": ["coding", "code-generation"]
    },
    "github-copilot/claude-sonnet-4-5": {
      "provider": "github-copilot",
      "alias": "sonnet",
      "maxTokens": 200000,
      "timeoutMs": 60000,
      "priority": 4,
      "supports": ["tools", "long-context"],
      "costFactor": "free",
      "bestFor": ["fallback", "general-purpose"]
    }
  },
  "monitoring": {
    "enabled": true,
    "checkIntervalMs": 300000,
    "logFile": "$HOME/.openclaw/logs/model-fallback.log",
    "alertOnFailure": true
  }
}
```

## 故障排查

### 问题 1: 模型未自动切换

**检查**：
```bash
# 查看配置文件
cat ~/.openclaw/agents/main/agent/agent.json | grep modelFallback

# 查看日志
tail -20 ~/.openclaw/logs/model-fallback.log

# 手动运行切换脚本
~/.openclaw/scripts/model-fallback.sh
```

### 问题 2: 监控未运行

**检查**：
```bash
# 查看进程
ps aux | grep monitor-models

# 查看PID文件
cat ~/.openclaw/logs/model-monitor.pid

# 重启监控
~/.openclaw/scripts/monitor-models.sh restart
```

### 问题 3: 所有模型都不可用

**检查**：
```bash
# 查看状态报告
~/.openclaw/scripts/monitor-models.sh status

# 检查 API 密钥
cat ~/.openclaw/agents/main/agent/auth-profiles.json

# 测试网络连接
ping -c 3 anapi.9w7.cn
ping -c 3 open.bigmodel.cn
```

## 性能优化

### 减少切换频率

```json
{
  "retry": {
    "maxAttempts": 5,        // 增加重试次数
    "initialDelayMs": 2000   // 增加初始延迟
  }
}
```

### 优化响应时间

为不同任务选择最快的模型：

```json
{
  "routing": {
    "rules": [
      {
        "name": "quick-response",
        "match": {
          "priority": "speed"
        },
        "preferModels": [
          "github-copilot/claude-sonnet-4-5",  // 通常响应最快
          "zai/glm-4.7"
        ]
      }
    ]
  }
}
```

## 集成到 OpenClaw

配置完成后，模型降级功能会自动集成到 OpenClaw Gateway：

1. **自动重启 Gateway**:
```bash
openclaw gateway restart
```

2. **验证配置**:
```bash
openclaw status | grep Model
```

3. **查看日志**:
```bash
journalctl -u openclaw-gateway -f | grep model
```

## 最佳实践

### 1. 定期检查

每周运行一次全面检查：
```bash
~/clawd/scripts/test-model-fallback.sh
```

### 2. 监控日志

每天查看切换日志：
```bash
grep "切换模型" ~/.openclaw/logs/model-fallback.log | tail -10
```

### 3. 更新配置

当添加新模型时，更新 `agent.json`：
```json
{
  "modelFallback": [
    "anapi/opus-4.5",
    "zai/glm-4.7",
    "new-model-here",  // 新模型
    "github-copilot/claude-sonnet-4-5"
  ]
}
```

### 4. 备份配置

定期备份配置文件：
```bash
cp ~/.openclaw/agents/main/agent/agent.json \
   ~/.openclaw/agents/main/agent/agent.json.backup
```

## 相关文件

- `~/.openclaw/agents/main/agent/agent.json` - 主配置文件
- `~/.openclaw/agents/main/agent/auth-profiles.json` - API 密钥
- `~/.openclaw/scripts/model-fallback.sh` - 切换脚本
- `~/.openclaw/scripts/monitor-models.sh` - 监控脚本
- `~/clawd/scripts/test-model-fallback.sh` - 测试脚本
- `~/clawd/docs/model-fallback-strategy.md` - 技术文档

## 支持的模型

当前配置的模型及其特性：

| 模型 | 供应商 | 优先级 | 最大Token | 特长 |
|------|--------|--------|----------|------|
| opus-4.5 | anapi | 1 | 200k | 最强能力，视觉 |
| glm-4.7 | zai | 2 | 200k | 中文优化 |
| gpt-5.2-codex | openrouter-vip | 3 | 100k | 编码专用 |
| sonnet-4.5 | github-copilot | 4 | 200k | 免费备用 |

## TODO

- [ ] 添加更多供应商
- [ ] 实现基于成本的模型选择
- [ ] 添加模型性能指标收集
- [ ] 实现预测性模型切换
- [ ] 集成告警通知（Telegram/邮件）
- [ ] 添加 WebUI 监控面板
