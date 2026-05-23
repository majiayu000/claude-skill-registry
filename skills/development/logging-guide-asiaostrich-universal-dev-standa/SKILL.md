---
name: logging
description: |
  实作结构化日誌，包含正确的日誌层级和敏感数据处理。
  使用时机：新增日誌、除錯、设置可觀测性。
  关鍵字：logging, log level, structured logging, observability, 日誌, 记录, 结构化日誌。
source: ../../../../skills/logging-guide/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2026-01-08
status: current
---

# 日誌指南

> **语言**: [English](../../../../skills/logging-guide/SKILL.md) | 简体中文

**版本**: 1.0.0
**最後更新**: 2025-12-30
**適用範圍**: Claude Code Skills

---

## 目的

此技能幫助在所有環境中实作一致、结构化且可操作的应用程序日誌。

## 快速參考

### 日誌层级

| 层级 | 代码 | 使用时机 | 生产環境 |
|------|------|----------|----------|
| **TRACE** | 10 | 非常详细的除錯信息 | 关閉 |
| **DEBUG** | 20 | 详细的除錯信息 | 关閉 |
| **INFO** | 30 | 正常操作事件 | 開啟 |
| **WARN** | 40 | 潛在問題，可恢復 | 開啟 |
| **ERROR** | 50 | 需要注意的错误 | 開啟 |
| **FATAL** | 60 | 嚴重故障 | 開啟 |

### 层级选择决策樹

```
只用於除錯？               → DEBUG（生产環境关閉）
正常操作完成？             → INFO
意外但没問題的情况？       → WARN
操作失败？                 → ERROR
应用程序無法繼續？         → FATAL
```

### 各层级使用时机

| 层级 | 範例 |
|------|------|
| **TRACE** | 函式进入/離開、回圈迭代、变數值 |
| **DEBUG** | 状态变更、设置值、查詢參數 |
| **INFO** | 应用啟动/关閉、使用者操作、排程任务 |
| **WARN** | 已棄用 API、重試嘗試、資源接近上限 |
| **ERROR** | 失败的操作、捕獲的例外、集成失败 |
| **FATAL** | 無法恢復的错误、啟动失败、失去关鍵資源 |

## 结构化日誌

### 必要欄位

```json
{
  "timestamp": "2025-01-15T10:30:00.123Z",
  "level": "INFO",
  "message": "使用者登入成功",
  "service": "auth-service",
  "environment": "production"
}
```

### 建议欄位

```json
{
  "timestamp": "2025-01-15T10:30:00.123Z",
  "level": "INFO",
  "message": "使用者登入成功",
  "service": "auth-service",
  "environment": "production",
  "trace_id": "abc123",
  "span_id": "def456",
  "user_id": "usr_12345",
  "request_id": "req_67890",
  "duration_ms": 150,
  "http_method": "POST",
  "http_path": "/api/v1/login",
  "http_status": 200
}
```

### 欄位命名慣例

使用 `snake_case` 并加上領域前綴：

| 領域 | 常用欄位 |
|------|----------|
| HTTP | http_method, http_path, http_status, http_duration_ms |
| 数据庫 | db_query_type, db_table, db_duration_ms, db_rows_affected |
| 佇列 | queue_name, queue_message_id, queue_delay_ms |
| 使用者 | user_id, user_role, user_action |
| 请求 | request_id, trace_id, span_id |

## 详细指南

完整标准請參考：
- [日誌标准](../../core/logging-standards.md)

### AI 優化格式（节省 Token）

AI 助手可使用 YAML 格式文件以減少 Token 使用量：
- 基礎标准：`ai/standards/logging.ai.yaml`

## 敏感数据处理

### 絕对不要记录

- 密码或机密
- API 金鑰或 Token
- 信用卡号码
- 身分证字号
- 完整的认证 Token

### 遮罩或编修

```javascript
// 不好
logger.info('登入嘗試', { password: userPassword });

// 好
logger.info('登入嘗試', { password: '***已编修***' });

// 好 - 部分遮罩
logger.info('卡片已处理', { last_four: '4242' });
```

### PII 处理

- 盡可能记录使用者 ID 而非電子郵件
- 对敏感查詢使用雜湊識别码
- 设置数据保留政策

## 错误日誌

### 必要的错误欄位

```json
{
  "level": "ERROR",
  "message": "数据庫連线失败",
  "error_type": "ConnectionError",
  "error_message": "連线被拒絕",
  "error_code": "ECONNREFUSED",
  "stack": "Error: Connection refused\n    at connect (/app/db.js:45:11)..."
}
```

### 错误上下文

务必包含：
- 嘗試的操作是什麼
- 相关識别码（user_id, request_id）
- 输入參數（已清理）
- 重試次數（如適用）

```javascript
logger.error('处理订单失败', {
  error_type: err.name,
  error_message: err.message,
  order_id: orderId,
  user_id: userId,
  retry_count: 2,
  stack: err.stack
});
```

## 日誌格式

### JSON 格式（生产環境）

```json
{"timestamp":"2025-01-15T10:30:00.123Z","level":"INFO","message":"请求完成","request_id":"req_123","duration_ms":45}
```

### 人类可读格式（开发環境）

```
2025-01-15T10:30:00.123Z [INFO] 请求完成 request_id=req_123 duration_ms=45
```

## 效能考量

### 各環境的日誌量

| 環境 | 层级 | 策略 |
|------|------|------|
| 开发 | DEBUG | 所有日誌 |
| 测试 | INFO | 大部分日誌 |
| 生产 | INFO | 高流量端点採样 |

### 高流量端点

- 使用採样（每 100 筆记录 1 筆）
- 聚合指標而非个别日誌
- 使用獨立的日誌串流

## 检查清单

### 必要欄位

- [ ] timestamp（ISO 8601）
- [ ] level
- [ ] message
- [ ] service name
- [ ] request_id 或 trace_id

### 安全性

- [ ] 没有密码或机密
- [ ] 没有完整 Token
- [ ] PII 已遮罩或雜湊
- [ ] 信用卡從不记录
- [ ] 保留政策已设置

---

## 设置偵测

此技能支援项目特定设置。

### 偵测順序

1. 检查現有的日誌程序庫设置
2. 检查 `CONTRIBUTING.md` 中的日誌指南
3. 若無找到，**预设使用结构化 JSON 日誌**

### 首次设置

若未找到日誌标准：

1. 建议：「此项目尚未设置日誌标准。您要设置结构化日誌嗎？」
2. 建议在 `CONTRIBUTING.md` 中记录：

```markdown
## 日誌标准

### 日誌层级
- DEBUG: 僅开发環境，详细診斷信息
- INFO: 正常操作（啟动、使用者操作、任务）
- WARN: 意外但可恢復的情况
- ERROR: 需要調查的失败

### 必要欄位
所有日誌必須包含：timestamp, level, message, service, request_id

### 敏感数据
絕不记录：密码、Token、信用卡、身分证字号
```

---

## 相关标准

- [日誌标准](../../core/logging-standards.md)
- [错误码标准](../../core/error-code-standards.md)

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2025-12-30 | 初始發布 |

---

## 授权

此技能採用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
