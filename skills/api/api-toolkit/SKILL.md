# API Toolkit Skill

通用 API 调用工具包，用于快速接入任何 RESTful API。

## 使用场景

- 调用第三方 API 服务
- 测试和调试 API 端点
- 构建自动化工作流
- 数据获取和同步

## 核心能力

### 1. HTTP 请求

```bash
# GET 请求
curl -s "https://api.example.com/endpoint" \
  -H "Authorization: Bearer $(pass show tokens/example-api)"

# POST 请求
curl -s -X POST "https://api.example.com/endpoint" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"key": "value"}'

# 带查询参数
curl -s "https://api.example.com/search?q=query&limit=10"
```

### 2. 认证方式

| 方式 | 示例 |
|------|------|
| Bearer Token | `-H "Authorization: Bearer $TOKEN"` |
| API Key Header | `-H "X-API-Key: $KEY"` |
| Basic Auth | `-u "user:pass"` |
| Query Param | `?api_key=$KEY` |

### 3. 响应处理

```bash
# JSON 解析
curl -s ... | jq '.data'

# 提取特定字段
curl -s ... | jq -r '.items[].name'

# 错误检查
response=$(curl -s -w "\n%{http_code}" ...)
body=$(echo "$response" | head -n -1)
code=$(echo "$response" | tail -n 1)
```

## 常用 API 模板

### 天气 API (wttr.in)
```bash
curl -s "wttr.in/Shanghai?format=j1" | jq '.current_condition[0]'
```

### GitHub API
```bash
curl -s "https://api.github.com/users/USERNAME/repos" \
  -H "Authorization: token $(pass show tokens/github)"
```

### Telegram Bot API
```bash
curl -s "https://api.telegram.org/bot$TOKEN/sendMessage" \
  -d "chat_id=$CHAT_ID" \
  -d "text=$MESSAGE"
```

## 安全注意事项

1. **密钥管理** - 使用 `pass` 存储，不硬编码
2. **日志脱敏** - 不在输出中显示完整密钥
3. **速率限制** - 遵守 API 的调用频率限制
4. **错误处理** - 检查响应状态码

## 添加新 API

1. 获取 API 文档和密钥
2. 存储密钥：`pass insert tokens/new-api`
3. 测试基本调用
4. 记录到 TOOLS.md

## 相关文件

- `TOOLS.md` - 记录已配置的 API
- `SECURITY.md` - 安全策略
- `memory/audit-*.log` - 操作审计
