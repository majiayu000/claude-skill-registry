---
name: dingtalk-ai-web-search
description: 网页搜索与实时信息检索。需要查找最新资讯、实时数据、技术文档、热点事件，或用户说"搜一下"、"帮我查"、"查资料"、"web search"等时使用。基于小宿AI智能搜索，支持关键词搜索、时间范围过滤（一天/一周/一月/一年）、自定义结果数量、JSON 输出。
---

## 会话开始：连通性检查

**每次新会话开始，先运行 `--ping` 检查，再执行实际搜索：**

```bash
bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh --ping
```

根据结果处理：

| 结果 | 含义 | 处理方式 |
|------|------|----------|
| `✓ 连通成功，可用工具: web_search` | 正常 | 直接开始搜索 |
| `错误：未配置 MCP URL` | 从未配置或配置丢失 | 向用户索取 MCP 配置（见下方） |
| `连接失败: ...` | URL 失效或网络问题 | 让用户重新获取配置并执行 `--save` |

---

## 配置缺失时：向用户索取 MCP 配置

让用户打开以下页面，复制 MCP 配置 JSON 后提供给你：
```
https://mcp.dingtalk.com/#/detail?detailType=instanceMcpDetail&instanceId=78440
```

配置格式示例：
```json
{
  "mcpServers": {
    "小宿智能搜索": {
      "type": "streamable-http",
      "url": "https://mcp-gw.dingtalk.com/server/..."
    }
  }
}
```

收到配置后，运行连通性测试并永久保存（将 JSON 作为字符串传入 `-c`）：
```bash
bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh --save -c '{"mcpServers":{"小宿智能搜索":{"type":"streamable-http","url":"<用户提供的URL>"}}}'
```

- 成功：输出 `✓ 连通成功，可用工具: ...` 并提示已保存，后续无需再传 `-c`
- 失败：根据报错提示处理（配置格式错误 / 网络不通 / URL 无效）

---

## 快速参考

| 场景 | 命令 |
|------|------|
| **会话开始连通检查** | `bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh --ping` |
| **保存配置（需 -c 传入 JSON）** | `bash ... --save -c '<MCP JSON配置>'` |
| 普通搜索 | `bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh -q "关键词"` |
| 限定时间范围 | `bash ... -q "关键词" -f oneWeek` |
| 返回更多结果 | `bash ... -q "关键词" -n 10` |
| JSON 输出 | `bash ... -q "关键词" --json` |

---

## 基础用法

```bash
bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh -q "Python asyncio 最佳实践"
```

---

## 时间筛选

```bash
# 一周内的最新文章
bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh -q "LLM 评测基准 2025" -f oneWeek

# 一个月内
bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh -q "AI 编程工具对比" -f oneMonth
```

可选值: `noLimit`（默认）| `oneDay` | `oneWeek` | `oneMonth` | `oneYear`

---

## JSON 输出（便于程序处理）

```bash
bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh -q "FastAPI 性能优化" -n 5 --json
```

输出格式：
```json
[
  {
    "title": "页面标题",
    "url": "https://...",
    "snippet": "内容摘要...",
    "site": "网站名称",
    "published": "2025-01-01",
    "source": "小宿智能搜索"
  }
]
```

---

## 典型工作流

### 调研某个技术主题
```bash
bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh -q "LangGraph checkpoint 持久化方案" -n 5
```

### 获取实时信息
```bash
# 近一周新闻
bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh -q "OpenAI o3 发布" -f oneWeek -n 8
```

### 多轮深入调研
```bash
# 第一轮：宽泛了解
bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh -q "Rust 异步运行时对比" -n 5
# 第二轮：聚焦具体问题
bash <CURRENT_SKILL_MD_PATH_DIR>/scripts/search.sh -q "tokio vs async-std 性能基准测试 2024" -f oneYear -n 5
```
