---
name: mcdonald
description: 麦当劳助手 - 查询/领取优惠券、活动日历、餐品营养信息、门店查询
version: 1.0.0
author: hi-yu
metadata: {"openclaw": {"emoji": "🍔", "category": "lifestyle", "tags": ["麦当劳", "优惠券", "美食", "快餐"]}}
---

# 🍔 麦当劳助手

当用户询问麦当劳相关问题时，使用此 skill 调用麦当劳 MCP 服务获取实时数据。

## 适用场景

- 查询/领取优惠券
- 查看活动日历
- 查询餐品营养信息
- 搭配指定热量套餐

## 配置要求

### 必需配置
用户需要在 MCP 官网注册并获取 API Token：
- 访问 https://mcp.mcd.cn 获取 Token
- 设置环境变量 `MCD_TOKEN` 或在调用时替换 `<YOUR_TOKEN>`

### 可选配置
- `MCD_MCP_URL`: MCP 服务地址，默认 `https://mcp.mcd.cn`

## 调用方式

使用 exec 工具执行 curl 命令调用 MCP 服务：

```bash
MCD_URL="${MCD_MCP_URL:-https://mcp.mcd.cn}"
MCD_AUTH="Authorization: Bearer ${MCD_TOKEN:-<YOUR_TOKEN>}"

curl -s -X POST "$MCD_URL" \
  -H "$MCD_AUTH" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"<工具名>","arguments":{<参数>}},"id":1}'
```

## 可用工具

### 1. 查询可领优惠券 (available-coupons)

查看当前可领取的所有优惠券。

**触发词**: "有什么优惠券"、"可以领什么券"、"今天有什么优惠"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"available-coupons","arguments":{}},"id":1}'
```

### 2. 一键领取优惠券 (auto-bind-coupons)

自动领取所有可用优惠券到账户。

**触发词**: "帮我领券"、"一键领券"、"全部领取"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"auto-bind-coupons","arguments":{}},"id":1}'
```

### 3. 查询我的优惠券 (my-coupons)

查看已领取的优惠券列表。

**触发词**: "我有哪些优惠券"、"我的券"、"已领取的券"

**参数**:
- `page`: 页码，默认 "1"
- `pageSize`: 每页数量，默认 "50"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"my-coupons","arguments":{"page":"1","pageSize":"50"}},"id":1}'
```

### 4. 查询活动日历 (campaign-calender)

查看近期麦当劳活动安排。

**触发词**: "最近有什么活动"、"麦当劳活动"、"促销活动"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"campaign-calender","arguments":{}},"id":1}'
```

### 5. 查询餐品营养信息 (list-nutrition-foods)

获取麦当劳常见餐品的营养成分数据，包括能量、蛋白质、脂肪、碳水化合物、钠、钙等信息。适用于用户咨询热量、营养或搭配指定热量套餐。

**触发词**: "热量"、"卡路里"、"营养信息"、"多少大卡"、"帮我搭配XX卡的套餐"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"list-nutrition-foods","arguments":{}},"id":1}'
```

### 6. 获取当前时间 (now-time-info)

返回当前的完整时间信息，帮助判断活动是否在有效期内。

**触发词**: "现在几点"、"今天几号"（通常无需用户触发，AI 自动调用以判断活动时效）

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"now-time-info","arguments":{}},"id":1}'
```

## 响应处理

### 成功响应
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "..."}],
    "structuredContent": {...}
  },
  "id": 1
}
```

解析 `result.content[0].text` 或 `result.structuredContent` 获取数据。

### 错误响应
```json
{
  "jsonrpc": "2.0",
  "error": {"code": -32000, "message": "Token expired"},
  "id": 1
}
```

常见错误：
- `Token expired`: Token 过期，需要重新获取
- `Unauthorized`: Token 无效
- `Rate limited`: 请求过于频繁，稍后再试

## 输出格式建议

### 优惠券列表
以表格或清单形式展示，包含：
- 优惠券名称
- 优惠金额/折扣
- 有效期
- 使用条件

### 营养信息
以表格展示，包含：
- 餐品名称
- 热量 (kcal)
- 蛋白质 (g)
- 脂肪 (g)
- 碳水化合物 (g)

## 使用示例

**用户**: 今天麦当劳有什么优惠券可以领？

**AI 执行**:
```bash
curl -s -X POST "https://mcp.mcd.cn" -H "Authorization: Bearer $MCD_TOKEN" -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"available-coupons","arguments":{}},"id":1}'
```

**AI 回复**: 
> 当前可领取的优惠券：
> 1. 🍟 麦辣鸡腿堡套餐立减5元 (有效期至2月10日)
> 2. 🥤 任意饮品第二杯半价 (有效期至2月15日)
> ...
> 
> 需要帮你一键领取吗？

## 注意事项

1. **Token 安全**: 不要在公开场合暴露用户的 MCD_TOKEN
2. **频率限制**: 避免短时间内大量请求
3. **数据时效**: 优惠券和活动信息实时变化，建议用户及时查询
4. **热量搭配**: 使用营养信息帮用户搭配套餐时，注意计算总热量

## 更新日志

- v1.0.0: 初始版本，支持优惠券、活动、营养、门店查询
